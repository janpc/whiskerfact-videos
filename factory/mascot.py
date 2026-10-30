"""Mr. Whiskerfact animado por piezas (sprites v3 de Gemini, recortados y alineados por mascot/v3/parts.py).

Capas: cara base sin boca -> pupilas dibujadas (la mirada se mueve) -> ojos de otra pose si hace falta -> boca.
La boca sigue la voz: la LETRA decide la forma y el VOLUMEN cuánto se abre; cada forma dura >= 3 fotogramas y los
saltos grandes (cerrada -> muy abierta) pasan por una boca intermedia, como en la animación 2D clásica.

Uso:
  cat = Cat()
  img = cat.frame(mouth="ah", eyes=None, gaze=(0.3, 0), size=820)       # RGBA
  track = cat.lipsync(words, rms, fps, t_offset)                         # lista de bocas por fotograma
  python3 mascot.py   -> mascot/v3/test_v4.mp4 (eslogan + mirada + expresiones)
"""
import math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
from skimage.morphology import convex_hull_image

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "mascot", "v3")

MOUTHS = {"smile": 1, "m": 2, "slight": 3, "a": 4, "ah": 5, "e": 6, "ee": 7, "o": 8, "oo": 9, "f": 10, "l": 11, "happy": 12}
OPEN = {"smile": 0, "m": 0, "f": 1, "slight": 1, "l": 1, "e": 2, "ee": 2, "a": 2, "o": 2, "ah": 3, "oo": 3, "happy": 3}
EYES = {"half": 2, "closed": 3, "happy": 4, "wink": 5, "brow": 7, "sly": 9}
AMBER, PUPIL = (185, 134, 68), (76, 47, 46)
EYE_BOX = [(328, 436, 445, 515), (612, 435, 730, 515)]     # ojos de la base (lienzo de 1024)
PUPIL_WH = (44, 68)

class Cat:
    def __init__(self):
        self.base = Image.open(os.path.join(DIR, "base.png")).convert("RGBA")
        self.mouth = {k: Image.open(os.path.join(DIR, f"mouth_{v:02d}.png")) for k, v in MOUTHS.items()}
        self.eyes = {k: Image.open(os.path.join(DIR, f"eyes_{v:02d}.png")) for k, v in EYES.items()}
        # interior de cada ojo (almendra ámbar) para dibujar la pupila recortada
        a = np.asarray(self.base.convert("RGB")).astype(int)
        self.eye_masks = []
        for x0, y0, x1, y1 in EYE_BOX:
            sub = a[y0 - 4:y1 + 5, x0 - 4:x1 + 5]; r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
            am = (r > 150) & (g > 80) & (g < 175) & (b < 100) & (r - b > 90)
            hull = convex_hull_image(am)
            self.eye_masks.append(((x0 - 4, y0 - 4), Image.fromarray((hull * 255).astype(np.uint8))))
        self._cache = {}

    def _eyes_layer(self, gaze):
        """pupilas en su sitio + desplazamiento gaze (-1..1, -1..1) dentro de la almendra"""
        key = (round(gaze[0], 2), round(gaze[1], 2))
        if key in self._cache: return self._cache[key]
        layer = Image.new("RGBA", self.base.size, (0, 0, 0, 0))
        for (ox, oy), m in self.eye_masks:
            w, h = m.size
            e = Image.new("RGBA", (w, h), AMBER + (255,)); d = ImageDraw.Draw(e)
            d.ellipse([0, h * 0.55, w, h * 1.6], fill=(170, 116, 54, 255))          # sombra baja del iris
            cx, cy = w / 2 + gaze[0] * w * 0.26, h / 2 + gaze[1] * h * 0.16
            pw, ph = PUPIL_WH
            d.ellipse([cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2], fill=PUPIL + (255,))
            d.ellipse([cx - pw / 2 - 2, cy - ph / 2 + 6, cx - pw / 2 + 16, cy - ph / 2 + 24], fill=(255, 252, 240, 255))  # brillo
            e.putalpha(m.point(lambda v: 255 if v > 0 else 0).filter(__import__("PIL.ImageFilter").ImageFilter.MinFilter(5)))
            layer.alpha_composite(e, (ox, oy))
        self._cache[key] = layer
        return layer

    def frame(self, mouth="smile", eyes=None, gaze=(0, 0), size=None):
        img = self.base.copy()
        if eyes is None: img.alpha_composite(self._eyes_layer(gaze))
        else: img.alpha_composite(self.eyes[eyes])
        img.alpha_composite(self.mouth[mouth])
        return img.resize((size, size), Image.LANCZOS) if size else img

    # ---------- labios ----------
    @staticmethod
    def shape_for(ch, loud):
        if ch in "mbp": return "m"
        if ch in "fv": return "f"
        if ch in "ltdn": return "slight"          # la boca con lengua queda rara al hablar
        if ch == "a": return "ah" if loud else "a"
        if ch == "e": return "e"
        if ch in "iy": return "ee"
        if ch == "o": return "oo" if loud else "o"
        if ch == "u": return "oo"
        return "slight" if not loud else "a"

    def lipsync(self, words, rms, fps, n, t_offset=0.0, rest="smile"):
        """words: [(palabra, t0, t1)] en s; rms: volumen normalizado por fotograma (0..~1). Devuelve n bocas."""
        raw = []
        for i in range(n):
            T, v = i / fps - t_offset, (rms[i] if i < len(rms) else 0)
            cur = None
            for w, a, b in words:
                if a <= T < b:
                    letters = [c for c in w.lower() if c.isalpha()] or ["e"]
                    ch = letters[min(len(letters) - 1, int((T - a) / (b - a) * len(letters)))]
                    cur = "smile" if v < 0.12 else self.shape_for(ch, v > 0.55)
                    break
            raw.append(cur or rest)
        out, held = [], 99
        for k in raw:                                       # mínimo 3 fotogramas por forma
            if not out or (k != out[-1] and held >= 3):
                if out and abs(OPEN[k] - OPEN[out[-1]]) >= 2:   # salto grande: una boca intermedia
                    out.append("slight" if min(OPEN[k], OPEN[out[-1]]) == 0 else "a"); held = 1; continue
                out.append(k); held = 1
            else:
                out.append(out[-1]); held += 1
        return out[:n]

def rms_track(path, fps, offset, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32); hop = 16000 // fps
    r = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    r = np.concatenate([np.zeros(int(offset * fps)), r / (np.percentile(r, 95) + 1e-9)])
    return np.pad(r, (0, max(0, n - len(r))))[:n]

# ---------- prueba ----------
if __name__ == "__main__":
    FPS, SIZE, CAT = 30, 1080, 900
    AT = 0.6
    WORDS = [("class", 0.07, 0.36), ("dismissed", 0.38, 1.25), ("stay", 1.39, 1.60), ("curious", 1.62, 2.31)]
    end = AT + WORDS[-1][2]
    total = end + 5.4
    n = int(total * FPS)
    voice = os.path.join(HERE, "voice", "slogan_brad.mp3")
    rms = rms_track(voice, FPS, AT, n)
    cat = Cat()
    mouths = cat.lipsync(WORDS, rms, FPS, n, AT)
    env = np.convolve(rms, np.ones(5) / 5, "same")

    def plan(T):
        """(ojos, mirada, boca forzada)"""
        t = T - end
        if T < 0.35: return None, (-0.7, 0), None                       # mira a un lado...
        if T < AT: return ("closed" if T < 0.42 else None), (0, 0), None   # ...parpadea y mira a cámara
        if t < 0: return None, (0, 0), None
        if t < 0.2: return None, (0, 0), "smile"
        if t < 0.75: return "wink", (0, 0), "smile"
        if t < 1.6: return "happy", (0, 0), "happy"
        if t < 2.3: return None, (0.75, -0.3), "smile"                 # mira arriba a la derecha (pensando)
        if t < 2.4: return "half", (0, 0), "smile"
        if t < 3.3: return "brow", (0, 0), "smile"
        if t < 4.2: return "sly", (0, 0), "smile"
        if t < 4.3: return "closed", (0, 0), "smile"
        return None, (-0.5, 0.2), "smile"

    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SIZE}x{SIZE}",
                          "-r", str(FPS), "-i", "-", "-itsoffset", str(AT), "-i", voice,
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-af", "apad", "-t", f"{total:.2f}", os.path.join(DIR, "test_v4.mp4")],
                         stdin=subprocess.PIPE)
    gz = np.array([0.0, 0.0])
    for i in range(n):
        T = i / FPS
        eyes, target, force = plan(T)
        gz += (np.array(target) - gz) * 0.45                           # movimiento rápido de ojos (sacada) y para
        face = cat.frame(force or mouths[i], eyes, tuple(gz), CAT)
        e = env[i]
        breathe = 5 * math.sin(T * 2 * math.pi * 0.7)
        nod = -16 * e
        tilt = 2 * math.sin(T * 2 * math.pi * 0.33) + 2.5 * e * math.sin(T * 8)
        if 0 <= T - end < 0.75: tilt += 4 * math.sin(min(1, (T - end) / 0.25) * math.pi / 2)
        spr = face.rotate(tilt, Image.BICUBIC, center=(CAT // 2, CAT))
        fr = Image.new("RGBA", (SIZE, SIZE), (40, 48, 96, 255))
        fr.alpha_composite(spr, ((SIZE - CAT) // 2, int(SIZE - CAT + 120 + breathe + nod)))
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    print("ok", f"{total:.1f} s")
