"""Prueba de VÍDEO del estilo nuevo (0 créditos): gato v4 con cuerpo, sincronía labial por fonemas y un trozo de la voz de wifi_bands.
  python3 v4/test_video.py [salida.mp4]
Trozo: 'five gigahertz wins, two to one. But my take? Use both: five near the router, two point four for the far rooms.'
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(D, "..", "..")
sys.path.insert(0, F); sys.path.insert(0, D)
import mascot as M
import test_frame as TF

W, H, FPS = 1080, 1920, 30
T0, T1 = 69.2, 76.8
WORDS = json.load(open(os.path.join(F, "voice", "wifi_bands_brad_words.json")))[185:207]
BG, FLOOR, INK, ACCENT, CREAM = TF.BG, TF.FLOOR, TF.INK, TF.ACCENT, TF.CREAM
FONT = os.path.join(D, "fonts", "LondrinaSolid-Regular.ttf")

POSES = [(0, "stand_front", "amused"), (71.5, "shrug", "curious"), (72.5, "paw_up", "excited"), (73.35, "explain", "amused"), (75.4, "point_right", "sly")]
TITLES = [(0, [("Final: 5 GHz wins", CREAM)]), (71.5, [("My take:", CREAM), ("use BOTH", ACCENT)])]

def at(table, t):
    cur = table[0]
    for e in table:
        if e[0] <= t: cur = e
    return cur

def main(out):
    tmp = tempfile.mkdtemp(); wav = os.path.join(tmp, "v.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(T0), "-to", str(T1), "-i", os.path.join(F, "voice", "wifi_bands_brad.mp3"), "-c:a", "libmp3lame", "-q:a", "2", wav], check=True)
    text = " ".join(w[0] for w in WORDS)
    ph = M.phone_align(wav, text)
    n = int((T1 - T0) * FPS)
    mouths = M.Cat4().lipsync(ph, FPS, n, 0.0)
    cat = M.Cat4(); cache = {}
    f1 = ImageFont.truetype(FONT, 118); f2 = ImageFont.truetype(FONT, 70)
    base = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(base); d.rectangle((0, 1250, W, H), fill=FLOOR)
    grain = np.random.default_rng(7).normal(0, 3, (H, W, 1)).astype(np.float32)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", out], stdin=subprocess.PIPE)
    blink = {int(x * FPS) + k for x in (1.1, 3.4, 5.9) for k in range(3)}
    for i in range(n):
        t = T0 + i / FPS
        _, pose, eyes = at(POSES, t)
        if i in blink: eyes = "closed"
        mouth = mouths[i]
        key = (pose, mouth, eyes)
        if key not in cache: cache[key] = cat.frame_body(pose, mouth, eyes, size=880, outline=6)
        c = cache[key]
        im = base.copy(); dd = ImageDraw.Draw(im)
        lines = at(TITLES, t)[1]
        for k, (s, col) in enumerate(lines): TF.text_outlined(dd, (W / 2, 330 + k * 135), s, f1, col)
        br = 1 + 0.008 * math.sin(2 * math.pi * (i / FPS) / 3.2)           # respiración mínima
        cc = c.resize((round(c.width * br), round(c.height * br)), Image.LANCZOS)
        im.paste(cc, ((W - cc.width) // 2 - 70, 1390 - cc.height + 100 + (c.height - cc.height) // 2), cc)
        dd.rounded_rectangle((60, 1390, W - 60, 1580), radius=18, fill=(176, 120, 72), outline=INK, width=8)
        dd.rectangle((60, 1390, W - 60, 1410), fill=(196, 140, 90))
        # subtítulo: grupo de 3 palabras con la actual en acento
        cur = max((j for j, w in enumerate(WORDS) if w[1] - T0 <= (i + 1) / FPS), default=0)
        g0 = (cur // 3) * 3; grp = [w[0] for w in WORDS[g0:g0 + 3]]
        widths = [dd.textlength(w + " ", font=f2) for w in grp]; x = 485 - sum(widths) / 2
        for j, w in enumerate(grp):
            TF.text_outlined(dd, (x, 1450), w, f2, ACCENT if g0 + j == cur else CREAM, sw=7, anchor="la"); x += widths[j]
        arr = np.clip(np.asarray(im).astype(np.float32) + grain, 0, 255).astype(np.uint8)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close(); ff.wait(); print(out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, "test_video.mp4"))
