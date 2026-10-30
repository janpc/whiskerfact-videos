"""Motor común para reels con voz: cada vídeo solo define sus escenas (dibujo) y este módulo hace el resto.

Un reel nuevo (ver pyramids.py como ejemplo):
    R = Reel("history")
    V = VoiceReel(R, "pyramids", [("hook", "Slaves"), ("context", "For"), ..., ("wrap", "So")])
    @V.scene("hook")
    def hook(img, T, t, s, e): ...dibuja sobre img (fondo ya puesto)...
    V.sounds("context", [(0.0, "whoosh", 0.8), (1.2, "pop", 0.6)])   # tiempos relativos al inicio de la escena
    V.main()        # python3 pyramids.py [render|preview t1 t2 ...|mux]

Qué hace:
- carga voice/<slug>_brad.mp3 y voice/<slug>_brad_words.json (de align.py, gratis) y corta las escenas
  a medio camino entre la última palabra de una escena y la primera de la siguiente (palabra de apertura);
- subtítulos palabra a palabra en la zona caption (menos en el gancho, que ya está en pantalla);
- cierre "gafas" con el eslogan narrado y el guiño tras la última palabra;
- audio: voz + efectos atenuados bajo la voz + música documental animada con ducking; loudnorm a brand.VOICE_LUFS.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image
import brand as B, music as M, sfx as SFX
from reel_lib import clamp, eo, W, FPS, HERE, outro_frame
import outro4

SLOGAN_AT = 0.6
SLOGAN_WORDS = {"brad": [0.07, 0.38, 1.39, 1.62]}   # inicio de cada palabra en voice/slogan_<voz>.mp3
SLOGAN_END = {"brad": 2.31}
OUTRO_LEN = 4.8

class VoiceReel:
    def __init__(self, R, slug, openers, voice="brad"):
        self.R, self.slug, self.voice = R, slug, voice
        vdir = os.path.join(HERE, "voice")
        self.voice_mp3 = os.path.join(vdir, f"{slug}_{voice}.mp3")
        self.slogan_mp3 = os.path.join(vdir, f"slogan_{voice}.mp3")
        off = B.VOICE["offset"]
        self.words = [(w, s + off, e + off) for w, s, e in json.load(open(os.path.join(vdir, f"{slug}_{voice}_words.json")))]
        first, i = {}, 0
        for name, word in openers:                      # primera palabra de cada escena, en orden
            while self.words[i][0].strip('"“”,.?!:') != word: i += 1
            first[name] = i; i += 1
        names = [n for n, _ in openers]
        cut = [0.0] + [(self.words[first[n] - 1][2] + self.words[first[n]][1]) / 2 for n in names[1:]]
        self.outro_at = round(self.words[-1][2] + 0.6, 2)
        self.sc = {n: (cut[k], cut[k + 1] if k + 1 < len(names) else self.outro_at) for k, n in enumerate(names)}
        self.first = first
        R.total = self.outro_at + OUTRO_LEN
        self.draw = {}
        outro4.WORDS_A = [SLOGAN_AT + t for t in SLOGAN_WORDS[voice]]
        outro4.WINK = SLOGAN_AT + SLOGAN_END[voice] + 0.2
        self.blocks = self._blocks()
        for n in names[1:]: R.sound(self.sc[n][0] + 0.05, "tap", 0.7)      # entra el título de cada escena

    # ---------- escenas ----------
    def scene(self, name):
        def deco(fn): self.draw[name] = fn; return fn
        return deco

    def sounds(self, name, lst):
        s, e = self.sc[name]
        for dt, n, g in lst: self.R.sound(min(s + dt, e - 0.2), n, g)

    def word_time(self, word, after=0.0):
        """momento en que se dice una palabra (la primera tras `after`), para sincronizar animaciones"""
        return next(s for w, s, e in self.words if w.strip('"“”,.?!:').lower() == word.lower() and s >= after)

    def frame_at(self, T):
        if T >= self.outro_at: return outro_frame(self.R, T - self.outro_at)
        for n, (s, e) in self.sc.items():
            if s <= T < e:
                img = self.R.bg.copy()
                out = self.draw[n](img, T, T - s, s, e)
                img = out if out is not None else img
                if n == "hook": img = self.R.punch(img, T, 0.0, dur=0.3, amt=0.06)   # golpe de entrada en el fotograma 0
                elif self.autofit: img = self._fit(n, img)
                if n != "hook": self._subs(img, T)
                return img
        return self.R.bg.copy()

    # ---------- encuadre automático de la ilustración ----------
    # Los dibujos tienden a quedarse pequeños. Cada escena (menos el gancho) se reencuadra sola:
    # se mide lo dibujado en la zona de ilustración en un fotograma representativo, y se escala
    # (como mucho FIT_MAX) y centra para llenar la caja segura: a la izquierda de los botones de la app.
    autofit = True
    FIT_ZONE = (735, 1380)                     # y: bajo el subtítulo, sobre los subtítulos de voz
    FIT_BOX = (70, 760, B.SAFE_RIGHT_LOW, 1370)  # x0, y0, x1, y1 donde debe caber el dibujo
    FIT_MAX = 1.45
    FIT_MIN = 0.92                             # no encoger más: un dibujo ancho no debe quedarse en una tira diminuta

    def _content_mask(self, img):
        y0, y1 = self.FIT_ZONE
        a = np.asarray(img.convert("RGB"), dtype=np.int16)[y0:y1]
        b = self.R.bg_arr[y0:y1].astype(np.int16)
        d = np.abs(a - b).max(axis=2)
        return np.clip((d - 6) / 18.0, 0, 1)        # 0 = fondo, 1 = dibujo (bordes suaves)

    def _fit_params(self, n):
        if not hasattr(self, "_fits"): self._fits = {}
        if n in self._fits: return self._fits[n]
        s, e = self.sc[n]
        boxes = []
        for k in (0.55, 0.8, 0.95):             # unión de varios momentos: lo que entra tarde también cuenta
            img = self.R.bg.copy(); t = s + (e - s) * k
            out = self.draw[n](img, t, t - s, s, e); img = out if out is not None else img
            m = self._content_mask(img) > 0.5
            ys, xs = np.nonzero(m)
            if len(xs) > 200: boxes.append((xs.min(), ys.min() + self.FIT_ZONE[0], xs.max(), ys.max() + self.FIT_ZONE[0]))
        if not boxes: self._fits[n] = None; return None
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
        bx0, by0, bx1, by1 = self.FIT_BOX
        sc = max(self.FIT_MIN, min((bx1 - bx0) / max(1, x1 - x0), (by1 - by0) / max(1, y1 - y0), self.FIT_MAX))
        self._fits[n] = (x0, y0, x1, y1, sc, (bx0 + bx1) / 2, (by0 + by1) / 2)
        return self._fits[n]

    def _fit(self, n, img):
        p = self._fit_params(n)
        if p is None: return img
        x0, y0, x1, y1, sc, cx, cy = p
        if abs(sc - 1) < 0.03 and abs((x0 + x1) / 2 - cx) < 10 and abs((y0 + y1) / 2 - cy) < 10: return img
        zy0, zy1 = self.FIT_ZONE
        alpha = (self._content_mask(img) * 255).astype(np.uint8)
        layer = img.crop((0, zy0, W, zy1)).convert("RGBA"); layer.putalpha(Image.fromarray(alpha))
        out = img.copy()
        out.paste(self.R.bg.crop((0, zy0, W, zy1)), (0, zy0))        # limpia la zona y la vuelve a pintar escalada
        nw, nh = int(W * sc), int((zy1 - zy0) * sc)
        big = layer.resize((nw, nh), Image.LANCZOS)
        ox = int(cx - ((x0 + x1) / 2) * sc); oy = int(cy - ((y0 + y1) / 2 - zy0) * sc)
        out.alpha_composite(big, (ox, oy)) if (ox >= 0 and oy >= 0) else out.paste(big, (ox, oy), big)
        return out

    # ---------- gancho ----------
    def hook_text(self, img, T, e, line1, line2, ask_word):
        """gancho completo y legible desde el fotograma 0: las dos líneas ya están en pantalla;
        cuando el narrador dice `ask_word` la pregunta da un pequeño latido (no aparece tarde)"""
        R = self.R
        fade = clamp((e - T) / B.EXIT)
        y = B.ZONES["title"][0] + 10
        s1 = R.sprite(line1, "hook", B.TEXT); s2 = R.sprite(line2, "hook", R.acc_t)
        R.put(img, s1, W / 2, y, fade, "mt")
        tq = self.word_time(ask_word)
        k = 1 + 0.08 * math.sin(math.pi * (T - tq) / 0.35) if tq <= T < tq + 0.35 else 1.0
        spr = s2 if k == 1.0 else s2.resize((int(s2.size[0] * k), int(s2.size[1] * k)), Image.LANCZOS)
        R.put(img, spr, W / 2, y + s1.size[1] - 4 + s2.size[1] / 2, fade, "mm")

    # ---------- subtítulos ----------
    def _blocks(self):
        R = self.R; f, size, lh = R.font("voicesub")
        blocks, cur = [], []
        def fits(ws): return len(R.wrap(" ".join(w for w, _, _ in ws), f, B.SUBS_MAX_W)) <= 2
        for w in self.words:
            if cur and not fits(cur + [w]): blocks.append(cur); cur = []
            cur.append(w)
            if w[0].rstrip('"”')[-1:] in ".?!" and len(cur) >= 3: blocks.append(cur); cur = []
        if cur: blocks.append(cur)
        return [(b, b[0][1], (blocks[i + 1][0][1] - 0.05 - B.SUBS_BLOCK_EXIT) if i + 1 < len(blocks) else b[-1][2] + 0.4) for i, b in enumerate(blocks)]

    def _subs(self, img, T):
        R = self.R
        f, size, lh = R.font("voicesub"); lhp = int(size * lh); y0 = B.ZONES["caption"][0]
        for words, t0, t1 in self.blocks:
            if not (t0 <= T < t1 + B.SUBS_BLOCK_EXIT): continue
            out_a = 1 - clamp((T - t1) / B.SUBS_BLOCK_EXIT)
            k = 0
            for li, line in enumerate(R.wrap(" ".join(w for w, _, _ in words), f, B.SUBS_MAX_W)):
                x = B.SUBS_CENTER_X - f.getlength(line) / 2
                for wtxt in line.split():
                    _, s, e = words[k]; k += 1
                    a = clamp((T - s) / B.SUBS_WORD_FADE) * out_a
                    if a > 0:
                        col = R.acc_t if s <= T < e + 0.05 else B.TEXT
                        R.put(img, R.sprite(wtxt, "voicesub", col, align="left"), x, y0 + li * lhp, a, "lt", dy=(1 - eo(a)) * B.SUBS_WORD_RISE)
                    x += f.getlength(wtxt + " ")

    # ---------- audio ----------
    @staticmethod
    def _load(path, n, at):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SFX.SR), "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        v = np.frombuffer(raw, np.float32); out = np.zeros(n, np.float32); i = int(at * SFX.SR)
        v = v[: max(0, n - i)]; out[i:i + len(v)] = v
        return out

    def build_audio(self, path):
        O = self.outro_at; total = O + OUTRO_LEN; n = int(total * SFX.SR)
        voice = self._load(self.voice_mp3, n, B.VOICE["offset"]) + self._load(self.slogan_mp3, n, O + SLOGAN_AT)
        voice /= (np.max(np.abs(voice)) or 1)
        L = int(0.25 * SFX.SR)
        env = np.clip(np.convolve((np.abs(voice) > 0.02).astype(np.float32), np.ones(L) / L, "same") * 4, 0, 1)
        gens = dict(tap=lambda: SFX.tap(587.33), whoosh=lambda: SFX.whoosh(0.45), pop=SFX.pop, click=SFX.click,
                    clink=SFX.clink, sparkle=SFX.sparkle, bubble=lambda: SFX.pop(900, 500, 0.09))
        kept = []
        for e in sorted(self.R.events):
            if sum(1 for k in kept if e[0] - k[0] < 1.0) < B.SFX_MAX_PER_SECOND: kept.append(e)
        outro_fx = [(O, SFX.whoosh(0.5), 0.6), (O + 0.42, SFX.pop(), 0.9), (O + 0.86, SFX.click(), 0.4),
                    (O + 1.6, SFX.clink(), 0.9), (O + outro4.WINK, SFX.sparkle(), 0.9)]
        fx = SFX.mix([(t, gens[nm](), g) for t, nm, g in kept] + outro_fx, total)[:n]
        fx = fx / (np.max(np.abs(fx)) or 1) * 0.9 * 10 ** (B.SFX_UNDER_VOICE_DB / 20) * (1 - 0.5 * env)
        music_file = os.path.join(HERE, "voice", f"{self.slug}_music.mp3")   # música compuesta para este vídeo (ElevenLabs)
        if os.path.exists(music_file):
            bed = self._load(music_file, n, 0.0)
            t = np.arange(n) / SFX.SR
            bed = bed * np.clip((total - t) / 1.5, 0, 1)                  # fundido final con el cierre
            bed = bed * 10 ** ((-16.0 - 20 * np.log10(np.sqrt(np.mean(bed ** 2)) + 1e-9)) / 20)   # mismo volumen medio que la música sintetizada
        else:
            bed = M.upbeat_doc_bed(total, self.R.cat, swell_at=O - 8)[:n]
        bed = M.duck(bed, env, B.MUSIC_DUCK_DB) * 0.9 * 10 ** (B.MUSIC_UNDER_VOICE_DB / 20 + 0.25)
        mix = voice * 0.9 + fx + bed
        SFX.write_wav(path, mix / max(1.0, np.max(np.abs(mix)) / 0.95))

    # ---------- salida ----------
    @property
    def name(self): return f"whiskerfact_{self.slug}"

    def mux(self):
        out_dir = os.path.join(HERE, "out", self.name)
        wav = os.path.join(out_dir, "audio_voice.wav"); self.build_audio(wav)
        final = os.path.join(HERE, "out", f"{self.name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(out_dir, "silent.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", f"loudnorm=I={B.VOICE_LUFS}:TP=-1.5", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        "-movflags", "+faststart", final], check=True)
        return final

    def preview(self, ts):
        ims = [self.frame_at(float(t)).convert("RGB").resize((360, 640)) for t in ts]
        cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
        sh = Image.new("RGB", (360 * cols, 640 * rows))
        for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 360, (i // cols) * 640))
        p = os.path.join(HERE, "out", f"{self.slug}_preview.jpg"); sh.save(p, quality=88); print(p)

    def main(self):
        mode = sys.argv[1] if len(sys.argv) > 1 else "render"
        if mode == "times":
            for n, (s, e) in self.sc.items(): print(f"{n:10s} {s:6.2f} {e:6.2f}")
            print("outro", self.outro_at, "total", round(self.outro_at + OUTRO_LEN, 2)); return
        if mode == "preview":
            ts = sys.argv[2:] or [round((s + e) / 2, 2) for s, e in self.sc.values()] + [self.outro_at + 3.5]
            return self.preview(ts)
        if mode == "render":
            # dibuja con el renderizador común (rechaza vídeos de menos de B.MIN_DURATION)
            self.R.mux = lambda *a, **k: None    # la mezcla sin voz de Reel no hace falta: la hace self.mux()
            self.R.render(list(self.sc.items()), self.frame_at, self.name, self.outro_at)
        print(self.mux())
