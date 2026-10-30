"""Animación fluida de Mr. Whiskerfact a partir de los sprites v2.
Por qué la v1 iba a saltos: cambiaba la imagen ENTERA en cada letra (cada viñeta de Gemini está redibujada y
ojos, rayas y contorno bailan unos píxeles), cada boca duraba 2 fotogramas y no había movimiento entre poses.
Aquí:
  1. capas: la cara base no cambia; solo se pega la zona de la BOCA o de los OJOS de otra pose, con borde difuminado;
  2. la boca sigue el VOLUMEN real de la voz (abierta/media/cerrada) y la letra decide la forma (o, ee, ah);
     cada boca dura al menos 3 fotogramas (sin fundidos: dejan dos bocas superpuestas);
  3. movimiento secundario: respira, la cabeza se inclina y asiente con las sílabas fuertes;
  4. los cambios de expresión se esconden detrás de un parpadeo.
  python3 mascot_anim.py -> mascot/v2/test_v3.mp4
"""
import math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "mascot", "v2")
FPS, SIZE, CAT, SPR = 30, 1080, 820, 768
SLOGAN_AT = 0.4
WORDS = [("class", 0.07, 0.36), ("dismissed", 0.38, 1.25), ("stay", 1.39, 1.60), ("curious", 1.62, 2.31)]

SP = {n[:-4]: Image.open(os.path.join(DIR, n)) for n in os.listdir(DIR)
      if n.endswith(".png") and not n.startswith(("sheet", "contact"))}

def soft_mask(box, blur):
    m = Image.new("L", (SPR, SPR), 0); ImageDraw.Draw(m).ellipse(box, fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))
MOUTH = soft_mask((262, 478, 506, 632), 14)      # boca, mentón y almohadillas de los bigotes
EYES = soft_mask((150, 270, 618, 470), 16)       # ojos, cejas y gafas

def patch(base, src, mask, k=1.0):
    if k <= 0: return base
    m = mask if k >= 1 else mask.point(lambda v: int(v * k))
    out = base.copy(); out.paste(src, (0, 0), Image.composite(src.split()[3], Image.new("L", src.size, 0), m))
    return out

# ---------- boca a partir del volumen ----------
def rms_track(path, offset):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32); hop = 16000 // FPS
    r = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    r = r / (np.percentile(r, 95) + 1e-9)
    pad = int(offset * FPS)
    return np.concatenate([np.zeros(pad), r])

def letter_at(T):
    for w, a, b in WORDS:
        a, b = a + SLOGAN_AT, b + SLOGAN_AT
        if a <= T < b:
            vowels = [c for c in w if c in "aeiouy"] or ["e"]
            return vowels[min(len(vowels) - 1, int((T - a) / (b - a) * len(vowels)))]
    return None

def mouth_targets(rms, n):
    """forma objetivo por fotograma, con mínimo de 3 fotogramas por forma"""
    raw = []
    for i in range(n):
        T, v = i / FPS, (rms[i] if i < len(rms) else 0)
        ch = letter_at(T)
        if ch is None or v < 0.18: raw.append("m" if ch else None); continue
        big = v > 0.55
        raw.append({"o": "o", "u": "o", "i": "ee", "y": "ee"}.get(ch, "ah" if big else "eh"))
    out, cur, held = [], None, 99
    for k in raw:
        if k != cur and held >= 3: cur, held = k, 0
        out.append(cur); held += 1
    return out

# ---------- guion de expresión ----------
def script(T, end):
    """devuelve (pose base, pose de ojos o None, intensidad de ojos)"""
    t = T - end
    if T < SLOGAN_AT:
        return "neutral", "half" if 0.12 < T < 0.18 else ("closed" if 0.18 <= T < 0.24 else None), 1
    if t < 0.25: return "neutral", None, 1
    if t < 0.85: return "neutral", "wink", 1                     # guiño
    if t < 1.8: return "happy", None, 1
    seq = ["point", "brow", "surprised", "look_l", "look_r", "glasses", "neutral"]
    i = int((t - 1.8) / 0.9)
    return (seq[i] if i < len(seq) else "neutral"), None, 1

def render(out_path, voice, total_extra=6.8):
    end = SLOGAN_AT + WORDS[-1][2]
    total = end + total_extra
    n = int(total * FPS)
    rms = rms_track(voice, SLOGAN_AT)
    mouths = mouth_targets(rms, n)
    env = np.convolve(np.pad(rms, (0, max(0, n - len(rms))))[:n], np.ones(5) / 5, "same")   # energía suavizada
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SIZE}x{SIZE}",
                          "-r", str(FPS), "-i", "-", "-itsoffset", str(SLOGAN_AT), "-i", voice,
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-af", "apad", "-t", f"{total:.2f}", out_path], stdin=subprocess.PIPE)
    prev_face, prev_base, fade = None, None, 0
    for i in range(n):
        T = i / FPS
        base, eyes, _ = script(T, end)
        face = SP[base]
        if eyes: face = patch(face, SP[eyes], EYES)
        # boca: fundido de 2 fotogramas con la anterior
        m, mp = mouths[i], mouths[i - 1] if i else None
        if m: face = patch(face, SP[m], MOUTH)
        # cambio de expresión escondido en un parpadeo (fundir dos caras deja ojos dobles)
        if prev_base is not None and base != prev_base: fade = 3
        if fade:
            face = patch(face, SP["closed" if fade > 1 else "half"], EYES); fade -= 1
        prev_face, prev_base = face, base
        # movimiento secundario
        e = env[i] if i < len(env) else 0
        breathe = 5 * math.sin(T * 2 * math.pi * 0.7)
        nod = -14 * e                                            # asiente con las sílabas fuertes
        tilt = 2.2 * math.sin(T * 2 * math.pi * 0.35) + 2.5 * e * math.sin(T * 9)
        if 0 <= T - end < 0.85: tilt += 4 * math.sin(min(1, (T - end) / 0.3) * math.pi / 2)   # ladea la cabeza al guiñar
        squash = 1 + 0.015 * math.sin(T * 2 * math.pi * 0.7)
        spr = face.resize((CAT, int(CAT * squash)), Image.BICUBIC).rotate(tilt, Image.BICUBIC, center=(CAT // 2, CAT))
        frame = Image.new("RGBA", (SIZE, SIZE), (40, 48, 96, 255))
        frame.alpha_composite(spr, ((SIZE - CAT) // 2, int(SIZE - spr.height + 40 + breathe + nod)))
        p.stdin.write(frame.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    return total

if __name__ == "__main__":
    out = os.path.join(DIR, "test_v3.mp4")
    print(out, f"{render(out, os.path.join(HERE, 'voice', 'slogan_brad.mp3')):.1f} s")
