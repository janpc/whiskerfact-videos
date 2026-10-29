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
import json, os, subprocess, sys
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
                if n != "hook": self._subs(img, T)
                return img
        return self.R.bg.copy()

    # ---------- subtítulos ----------
    def _blocks(self):
        R = self.R; f, size, lh = R.font("voicesub")
        blocks, cur = [], []
        def fits(ws): return len(R.wrap(" ".join(w for w, _, _ in ws), f, B.TEXT_MAX_W)) <= 2
        for w in self.words:
            if cur and not fits(cur + [w]): blocks.append(cur); cur = []
            cur.append(w)
            if w[0].rstrip('"”')[-1:] in ".?!" and len(cur) >= 3: blocks.append(cur); cur = []
        if cur: blocks.append(cur)
        return [(b, b[0][1], (blocks[i + 1][0][1] - 0.05) if i + 1 < len(blocks) else b[-1][2] + 0.4) for i, b in enumerate(blocks)]

    def _subs(self, img, T):
        R = self.R
        f, size, lh = R.font("voicesub"); lhp = int(size * lh); y0 = B.ZONES["caption"][0]
        for words, t0, t1 in self.blocks:
            if not (t0 <= T < t1 + B.SUBS_BLOCK_EXIT): continue
            out_a = 1 - clamp((T - t1) / B.SUBS_BLOCK_EXIT)
            k = 0
            for li, line in enumerate(R.wrap(" ".join(w for w, _, _ in words), f, B.TEXT_MAX_W)):
                x = W / 2 - f.getlength(line) / 2
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
