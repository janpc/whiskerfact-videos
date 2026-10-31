"""Base común de todos los reels de Mr. Whiskerfact: fondo, marca, texto, subtítulos,
mascota, golpes visuales, efectos de sonido, cierre y render. Todo sale de brand.py.
"""
import math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import sfx as SFX

W, H, FPS = B.W, B.H, B.FPS
HERE = os.path.dirname(os.path.abspath(__file__))

QA_LOG = None            # qa.py lo convierte en lista para registrar cada texto pintado
QA_META = {}
QA_STATE = {"T": 0.0, "scene": None}
NOINK = {"mask": None}   # VoiceReel la crea por fotograma; library.place marca ahí los personajes (sin contorno extra)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back_out(x, k=1.7):
    x = clamp(x) - 1; return x * x * ((k + 1) * x + k) + 1
def lerp(a, b, k): return a + (b - a) * k
def lerpc(c1, c2, k): return tuple(int(lerp(c1[i], c2[i], k)) for i in range(3))
def win(t, a, b):
    return clamp((t - a) / B.ENTER) * clamp((b - t) / B.EXIT)

class Reel:
    def __init__(self, category):
        self.cat = category
        self.acc = B.CATEGORIES[category]["color"]
        self.acc_t = B.accent_text_for(category)
        self.track = B.surface_for(category)
        top, bot = B.bg_for(category)
        yy = np.linspace(0, 1, H)[:, None, None]
        self.bg_arr = (np.array(top) * (1 - yy) + np.array(bot) * yy) * np.ones((1, W, 1))
        self.bg = Image.fromarray(self.bg_arr.astype(np.uint8)).convert("RGBA")
        self.total = 60.0
        self.events = []          # (t, nombre_sfx, ganancia)
        self._tc = {}; self._fonts = {}
        self._av = Image.open(os.path.join(HERE, B.MASCOT["file"])).convert("RGBA"); self._avs = {}

    # ---------- texto ----------
    def font(self, style):
        w, size, lh = B.TYPE[style]
        if (w, size) not in self._fonts:
            self._fonts[(w, size)] = ImageFont.truetype(B.FONT_DIR + f"InterDisplay-{w}.otf", size)
        return self._fonts[(w, size)], size, lh

    @staticmethod
    def wrap(s, f, maxw):
        out = []
        for para in s.split("\n"):
            line = ""
            for w in para.split(" "):
                t = (line + " " + w).strip()
                if f.getlength(t) <= maxw or not line: line = t
                else: out.append(line); line = w
            out.append(line)
        return out

    def sprite(self, s, style, color, maxw=B.TEXT_MAX_W, align="center"):
        key = (s, style, color, maxw, align)
        if key in self._tc: return self._tc[key]
        f, size, lh = self.font(style)
        lines = self.wrap(s, f, maxw)
        assert len(lines) <= B.MAX_LINES.get(style, 9), f"demasiadas líneas: {s!r} ({style})"
        asc, desc = f.getmetrics(); lhp = int(size * lh)
        sw = B.TEXT_STROKE.get(style, 0)          # borde oscuro del estilo videoclip: se lee sobre cualquier fondo
        tw = int(max(f.getlength(l) for l in lines)) + 8 + 2 * sw; th = lhp * (len(lines) - 1) + asc + desc + 8 + 2 * sw
        im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        for i, l in enumerate(lines):
            lw = f.getlength(l)
            x = (tw - lw) / 2 if align == "center" else (sw if align == "left" else tw - lw - sw)
            dr.text((x, i * lhp + sw), l, font=f, fill=color + (255,), stroke_width=sw, stroke_fill=B.TEXT_STROKE_COLOR + (255,))
        self._tc[key] = im
        QA_META[id(im)] = (s, style, color)
        return im

    @staticmethod
    def put(img, spr, x, y, a=1.0, anchor="mt", dy=0.0):
        if a <= 0.003: return
        if QA_LOG is not None and id(spr) in QA_META:          # control de calidad: qué texto, dónde y cuándo
            w0, h0 = spr.size
            ox0 = {"l": 0, "m": w0 / 2, "r": w0}[anchor[0]]; oy0 = {"t": 0, "m": h0 / 2, "b": h0}[anchor[1]]
            t, st, col = QA_META[id(spr)]
            bb = spr.getbbox() or (0, 0, w0, h0)                    # caja ajustada a las letras (sin márgenes)
            X0, Y0 = x - ox0, y - oy0 + dy
            QA_LOG.append(dict(T=QA_STATE["T"], scene=QA_STATE["scene"], text=t, style=st, color=col, a=a,
                               box=(int(X0 + bb[0]), int(Y0 + bb[1]), int(X0 + bb[2]), int(Y0 + bb[3]))))
        if a < 1:
            spr = spr.copy(); spr.putalpha(spr.split()[3].point(lambda v: int(v * a)))
        w, h = spr.size
        ox = {"l": 0, "m": w / 2, "r": w}[anchor[0]]; oy = {"t": 0, "m": h / 2, "b": h}[anchor[1]]
        img.alpha_composite(spr, (int(x - ox), int(y - oy + dy)))

    def put_text(self, img, spr, x, y, a=1.0, anchor="mt", text=""):
        """imagen que CONTIENE texto (sellos, carteles, números dentro del dibujo): va a la capa de etiquetas, así no
        recibe el contorno automático (que emborrona las letras) y el control de calidad la ve como texto"""
        if text: QA_META[id(spr)] = (text, "label", (40, 30, 30))
        self.put(self.label_layer if self.label_layer is not None else img, spr, x, y, a, anchor)

    label_layer = None     # si VoiceReel lo pone, las etiquetas se dibujan aparte y van ENCIMA del contorno (no se emborronan)
    def txt(self, img, s, y, style, color=None, a=1.0, x=W / 2, anchor="mt", rise=True, maxw=B.TEXT_MAX_W, align="center"):
        color = color or B.TEXT
        if style == "label" and self.label_layer is not None: img = self.label_layer
        if style == "label" and sum(color) > 380 and a > 0.003:     # etiqueta clara: pastilla oscura detrás, se lee sobre cualquier fondo
            spr = self.sprite(s, style, color, maxw, align); w, h = spr.size
            ox = {"l": 0, "m": w / 2, "r": w}[anchor[0]]; oy = {"t": 0, "m": h / 2, "b": h}[anchor[1]]
            dy = (1 - eo(a)) * B.RISE if rise else 0
            pill = Image.new("RGBA", (w + 36, h + 14), (0, 0, 0, 0))
            ImageDraw.Draw(pill).rounded_rectangle([0, 0, w + 35, h + 13], radius=(h + 14) // 2, fill=(30, 22, 22, 170))
            self.put(img, pill, x - ox - 18 + (w + 36) / 2, y - oy - 2 + dy, a, "mt")
        self.put(img, self.sprite(s, style, color, maxw, align), x, y, a, anchor, dy=(1 - eo(a)) * B.RISE if rise else 0)

    def caption(self, img, text, t, t0, t1, style="body", y=None, wps=B.SUBS_NO_VOICE_WPS):
        """subtítulos palabra a palabra: cada palabra entra a su tiempo; la que entra va en el color de categoría"""
        if t < t0 or t >= t1 + B.SUBS_BLOCK_EXIT: return
        y = y or B.ZONES["caption"][0] + 10
        f, size, lh = self.font(style); lhp = int(size * lh)
        lines = self.wrap(text, f, B.TEXT_MAX_W)
        assert len(lines) <= B.MAX_LINES[style], f"subtítulo demasiado largo: {text!r}"
        out_a = 1 - clamp((t - t1) / B.SUBS_BLOCK_EXIT)
        k = 0
        for li, line in enumerate(lines):
            x = W / 2 - f.getlength(line) / 2
            for w in line.split():
                at = t0 + k / wps; k += 1
                a = clamp((t - at) / B.SUBS_WORD_FADE) * out_a
                if a > 0:
                    hot = t - at < 1 / wps
                    col = self.acc_t if hot else B.TEXT
                    spr = self.sprite(w, style, col, align="left")
                    self.put(img, spr, x, y + li * lhp, a, "lt", dy=(1 - eo(a)) * B.SUBS_WORD_RISE)
                x += f.getlength(w + " ")
        return t0 + k / wps            # cuándo termina de aparecer

    def caption_end(self, text, t0, wps=B.SUBS_NO_VOICE_WPS):
        return t0 + len(text.split()) / wps

    # ---------- marca ----------
    def chrome(self, img, T):
        y0 = B.ZONES["brand"][0]
        self.put(img, self.sprite("MR. WHISKERFACT", "brand", B.GOLD, align="left"), 140, y0 + 6, 1, "lt")
        chip = self.sprite(B.CATEGORIES[self.cat]["label"], "chip", B.CHIP_TEXT)
        cw = chip.size[0] + 32
        dr = ImageDraw.Draw(img)
        dr.rounded_rectangle([940 - cw, y0, 940, y0 + 40], radius=20, fill=self.acc)
        self.put(img, chip, 940 - cw / 2, y0 + 22, 1, "mm")
        dr.rounded_rectangle([140, y0 + 52, 940, y0 + 58], radius=3, fill=self.track)
        dr.rounded_rectangle([140, y0 + 52, 140 + 800 * clamp(T / self.total), y0 + 58], radius=3, fill=self.acc)

    def mascot(self, img, size, x, y, a=1.0, rot=0.0):
        size = int(size)
        if size < 8 or a <= 0.003: return
        if size not in self._avs: self._avs[size] = self._av.resize((size, size), Image.LANCZOS)
        mm = self._avs[size]
        if rot: mm = mm.rotate(rot, resample=Image.BICUBIC)
        self.put(img, mm, x, y, a, "lt")

    def hook_mascot(self, img, T, t_in, t_out):
        if T < t_in: return
        k = eo((T - t_in) / B.MASCOT["hook"]["enter"]) * clamp((t_out - T) / B.EXIT)
        x, y = B.MASCOT["hook"]["pos"]
        self.mascot(img, B.MASCOT["hook"]["size"] - 20, x, lerp(1580, y, k))

    # ---------- golpes visuales ----------
    @staticmethod
    def flash(img, t, at, dur=0.3, strength=0.4):
        k = 1 - clamp((t - at) / dur) if t >= at else 0
        if k > 0: img.alpha_composite(Image.new("RGBA", (W, H), (255, 248, 230, int(255 * strength * k))))
        return img

    @staticmethod
    def punch(img, t, at, dur=0.35, amt=0.05):
        if not (at <= t < at + dur): return img
        k = 1 + amt * (1 - eo((t - at) / dur))
        w2, h2 = int(W * k), int(H * k)
        big = img.resize((w2, h2), Image.BILINEAR)
        return big.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))

    # ---------- sonido ----------
    def sound(self, at, name, gain=1.0):
        self.events.append((at, name, gain))

    def build_audio(self, path, outro_at):
        gens = dict(tap=lambda: SFX.tap(587.33), whoosh=lambda: SFX.whoosh(0.45), pop=SFX.pop, click=SFX.click,
                    clink=SFX.clink, sparkle=SFX.sparkle, bubble=lambda: SFX.pop(900, 500, 0.09))
        ev = sorted(self.events)
        kept = []
        for e in ev:   # nunca más de B.SFX_MAX_PER_SECOND por segundo
            if sum(1 for k in kept if e[0] - k[0] < 1.0) < B.SFX_MAX_PER_SECOND: kept.append(e)
        mixed = [(t, gens[n](), g) for t, n, g in kept]
        mixed += [(outro_at + t, s, g) for t, s, g in SFX.OUTRO_GAFAS()]
        total = outro_at + B.MASCOT["outro"]["dur"]
        x = SFX.mix(mixed, total)
        x = x * (10 ** (-10 / 20))        # efectos con picos a unos -12 dBFS: acompañan y dejan sitio a la voz
        if B.MUSIC_ON:
            import music as M
            styles = {"documentary": M.doc_bed, "documentary_upbeat": M.upbeat_doc_bed}
            bed = styles[B.MUSIC_STYLE](total, self.cat, swell_at=outro_at - 8) if B.MUSIC_STYLE in styles else M.bed(total, self.cat)
            n = min(len(bed), len(x)); x = x[:n] + bed[:n] * 10 ** (B.MUSIC_PEAK_DB / 20)
        SFX.write_wav(path, x)
        return len(kept), len(ev)

    # ---------- render ----------
    def render(self, scenes, frame_at, name, outro_at):
        total = outro_at + B.MASCOT["outro"]["dur"]
        if total < B.MIN_DURATION:   # TikTok solo paga vídeos de más de un minuto: no se renderiza nada más corto
            raise SystemExit(f"{name}: dura {total:.1f} s, mínimo {B.MIN_DURATION} s. Alarga el guion.")
        out_dir = os.path.join(HERE, "out", name); os.makedirs(out_dir, exist_ok=True)
        jobs =list(scenes) + [("outro", (outro_at, outro_at + B.MASCOT["outro"]["dur"]))]
        from multiprocessing import Pool
        global _JOB
        _JOB = (frame_at, out_dir)
        only = [x for x in os.environ.get("ONLY", "").split(",") if x]     # ONLY=escena1,escena2: rehace solo esas
        todo = [(i, j) for i, j in enumerate(jobs) if not only or j[0] in only
                or not os.path.exists(os.path.join(out_dir, f"{i:02d}_{j[0]}.mp4"))]
        with Pool(max(2, min(4, (os.cpu_count() or 2)))) as pool:
            for n in pool.imap_unordered(_render_one, todo): print("ok", n, flush=True)
        lst = os.path.join(out_dir, "list.txt")
        with open(lst, "w") as f:
            for i, (n, _) in enumerate(jobs): f.write(f"file '{i:02d}_{n}.mp4'\n")
        silent = os.path.join(out_dir, "silent.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
        return self.mux(name, outro_at)

    def mux(self, name, outro_at):
        """mezcla el audio y lo une al vídeo ya renderizado (sin volver a dibujar)"""
        out_dir = os.path.join(HERE, "out", name); silent = os.path.join(out_dir, "silent.mp4")
        wav = os.path.join(out_dir, "audio.wav")
        kept, total = self.build_audio(wav, outro_at)
        final = os.path.join(HERE, "out", f"{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", "loudnorm=I=-20:TP=-1.5", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", final], check=True)
        print(f"sfx {kept}/{total}", final)
        return final

_JOB = None
def _render_one(arg):
    i, (name, (s, e)) = arg
    frame_at, out_dir = _JOB
    tmp = os.path.join(out_dir, f"{i:02d}_{name}.tmp.mp4"); fin = os.path.join(out_dir, f"{i:02d}_{name}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for n in range(round(s * FPS), round(e * FPS)):
        p.stdin.write(frame_at(n / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, fin)
    return name

def outro_frame(reel, t):
    """cierre: el gato nuevo (mascot.py) dice el eslogan dentro de su círculo, con el fondo y la marca de la categoría"""
    import outro2, outro5
    outro2.CAT = reel.cat
    outro2.BG = reel.bg
    return outro5.frame(t)
