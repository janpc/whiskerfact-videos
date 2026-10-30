"""Prueba de animación con los sprites v2: dice el eslogan (labios sincronizados), parpadea, guiña y enseña el resto de poses.
  python3 mascot_test.py -> mascot/v2/test_v2.mp4
"""
import math, os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "mascot", "v2")
FPS, SIZE, CAT = 30, 1080, 820
SLOGAN_AT = 0.4
WORDS = [("class", 0.07, 0.36), ("dismissed", 0.38, 1.25), ("stay", 1.39, 1.60), ("curious", 1.62, 2.31)]
VIS = {"a": "ah", "e": "eh", "i": "ee", "y": "ee", "o": "o", "u": "o", "m": "m", "b": "m", "p": "m"}

S = {n[:-4]: Image.open(os.path.join(DIR, n)).resize((CAT, CAT), Image.LANCZOS)
     for n in os.listdir(DIR) if n.endswith(".png") and not n.startswith(("sheet", "contact"))}

def mouth_track():
    """lista de (t0, t1, pose) a partir de las letras de cada palabra repartidas en su duración"""
    out = []
    for w, a, b in WORDS:
        keys = [VIS.get(ch, "eh") for ch in w]
        merged = [k for i, k in enumerate(keys) if i == 0 or k != keys[i - 1]]
        step = max(0.07, (b - a) / len(merged))
        for i, k in enumerate(merged):
            t0 = SLOGAN_AT + a + i * step
            if t0 >= SLOGAN_AT + b: break
            out.append((t0, min(t0 + step, SLOGAN_AT + b), k))
    return out

TRACK = mouth_track()
END = SLOGAN_AT + WORDS[-1][2]
SHOW = ["point", "glasses", "brow", "surprised", "look_l", "look_r", "sly"]
TOTAL = END + 0.15 + 0.5 + 0.9 + len(SHOW) * 0.7 + 0.5

def pose(T):
    for a, b, k in TRACK:
        if a <= T < b: return k
    if T < SLOGAN_AT: return "half" if 0.15 < T < 0.22 else "neutral"
    t = T - END
    if t < 0.15: return "m"
    if t < 0.65: return "wink"
    if t < 1.55: return "happy"
    i = int((t - 1.55) / 0.7)
    if i < len(SHOW): return SHOW[i]
    return "neutral"

def frame(T):
    bg = Image.new("RGBA", (SIZE, SIZE), (40, 48, 96, 255))
    bob = 6 * math.sin(T * 2 * math.pi * 0.8)               # respiración suave
    bg.alpha_composite(S[pose(T)], ((SIZE - CAT) // 2, int(SIZE - CAT + 40 + bob)))
    return bg.convert("RGB")

if __name__ == "__main__":
    out = os.path.join(DIR, "test_v2.mp4")
    voice = os.path.join(HERE, "voice", "slogan_brad.mp3")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SIZE}x{SIZE}",
                          "-r", str(FPS), "-i", "-", "-itsoffset", str(SLOGAN_AT), "-i", voice,
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-af", "apad", "-t", f"{TOTAL:.2f}", out], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out, f"{TOTAL:.1f} s")
