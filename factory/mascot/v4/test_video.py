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
SC = 0.44; DESK_Y = 1390      # escala del lienzo del gato; la mesa tapa el corte de la cintura (todos los cuerpos llegan al menos a y=1642 del lienzo)
T0, T1 = 69.2, 76.8
WORDS = json.load(open(os.path.join(F, "voice", "wifi_bands_brad_words.json")))[185:207]
BG, FLOOR, INK, ACCENT, CREAM = TF.BG, TF.FLOOR, TF.INK, TF.ACCENT, TF.CREAM
FONT = os.path.join(D, "fonts", "LondrinaSolid-Regular.ttf")

POSES = [(0, "stand_front", "amused"), (71.5, "stand_front", "curious"), (72.5, "stand_front", "excited"), (75.4, "stand_front", "sly")]   # una sola pose: solo cambian la expresión y la boca
FADE = 6
TITLES = [(0, [("Final: 5 GHz wins", CREAM)]), (71.5, [("My take:", CREAM), ("use BOTH", ACCENT)])]


LIB = os.path.join(F, "library", "class_objects")
WALL = (46, 110, 140); WALL2 = (38, 96, 124); WOOD = (150, 100, 62); BOARD = (34, 72, 64); CHALK = (240, 238, 226)

def sprite(name, h, ol=4):
    im = Image.open(os.path.join(LIB, name + ".png")).convert("RGBA")
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    return TF.outline(im, ol)

def build_set():
    """clase del gato: pizarra con tiza (el tema del vídeo), estantes con objetos con significado (casco con orejas, robot, telescopio, caja de Schrödinger) y mesa.
    Color dominante de la escena = la pared (cambia por escena); lo importante queda fuera de la zona de botones (x > 900, y > 900)."""
    im = Image.new("RGB", (W, H), WALL); d = ImageDraw.Draw(im)
    d.rectangle((0, 1130, W, 1250), fill=WALL2)                                    # friso inferior de la pared
    d.rectangle((0, 1250, W, H), fill=FLOOR)                                       # suelo
    d.rectangle((0, 1250, W, 1262), fill=(24, 62, 82))                             # zócalo
    d.rounded_rectangle((650, 650, 1000, 900), radius=12, fill=WOOD, outline=INK, width=7)   # pizarra pequeña a la derecha del gato (con el gato delante no se pierde)
    d.rounded_rectangle((672, 672, 978, 878), radius=7, fill=BOARD, outline=INK, width=5)
    ch = ImageFont.truetype(os.path.join(D, "fonts", "CaveatBrush-Regular.ttf"), 44)
    xs = np.linspace(690, 962, 300)
    for y0, wl, amp, lab in ((742, 26, 12, "5 GHz"), (838, 90, 12, "2.4 GHz")):            # ondas a tiza: corta (5) y larga (2.4)
        d.line([(x, y0 + amp * math.sin((x - 690) / wl * 2 * math.pi)) for x in xs], fill=CHALK, width=5, joint="curve")
        d.text((690, y0 - 66), lab, font=ch, fill=ACCENT)
    d.rectangle((650, 900, 1000, 910), fill=(120, 78, 46)); d.rectangle((760, 900, 860, 916), fill=CHALK)   # repisa y tiza
    d.rounded_rectangle((10, 840, 330, 866), radius=6, fill=WOOD, outline=INK, width=5)       # estante con casco y robot
    for name, h, x, y in (("helmet", 170, 24, 840), ("robot", 150, 170, 840)):
        sp = sprite(name, h); im.paste(sp, (x, y - sp.height + 4), sp)
    sp = sprite("telescope", 270, 5); im.paste(sp, (14, 1390 - sp.height + 6), sp)         # telescopio, junto a la mesa
    sp = sprite("box_closed", 210, 5); im.paste(sp, (690, 1390 - sp.height + 8), sp)       # caja de Schrödinger sobre la mesa, cola asomando
    return im

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
    base = build_set(); 
    grain = np.random.default_rng(7).normal(0, 1.6, (H, W, 1)).astype(np.float32)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", out], stdin=subprocess.PIPE)
    blink = {int(x * FPS) + k for x in (1.1, 3.4, 5.9) for k in range(3)}
    def render(i, pose, eyes, mouth):
        t = T0 + i / FPS
        key = (pose, mouth, eyes)
        if key not in cache: cache[key] = cat.frame_body(pose, mouth, eyes, outline=6, fixed=(0, 0, 1400, 1700), scale=SC, sharpen=70)
        c = cache[key]
        im = base.copy(); dd = ImageDraw.Draw(im)
        lines = at(TITLES, t)[1]
        for k, (s, col) in enumerate(lines): TF.text_outlined(dd, (W / 2, 330 + k * 135), s, f1, col)
        br = 1 + 0.008 * math.sin(2 * math.pi * (i / FPS) / 3.2)           # respiración mínima (anclada en la mesa)
        cc = c.resize((round(c.width * br), round(c.height * br)), Image.LANCZOS)
        x0 = (W - 1400 * SC) / 2 - 70 - 6 * SC - (cc.width - c.width) / 2; y0 = DESK_Y - 1625 * SC - 6 - (cc.height - c.height)
        im.paste(cc, (round(x0), round(y0)), cc)
        dd.rounded_rectangle((60, 1390, W - 60, 1580), radius=18, fill=(176, 120, 72), outline=INK, width=8)
        dd.rectangle((60, 1390, W - 60, 1410), fill=(196, 140, 90))
        # subtítulo: grupo de 3 palabras con la actual en acento
        cur = max((j for j, w in enumerate(WORDS) if w[1] - T0 <= (i + 1) / FPS), default=0)
        g0 = (cur // 3) * 3; grp = [w[0] for w in WORDS[g0:g0 + 3]]
        widths = [dd.textlength(w + " ", font=f2) for w in grp]; x = 485 - sum(widths) / 2
        for j, w in enumerate(grp):
            TF.text_outlined(dd, (x, 1450), w, f2, ACCENT if g0 + j == cur else CREAM, sw=7, anchor="la"); x += widths[j]
        return im
    for i in range(n):
        t = T0 + i / FPS
        _, pose, eyes = at(POSES, t)
        if i in blink: eyes = "closed"
        mouth = mouths[i]
        poses_now = at(POSES, t)
        im = render(i, poses_now[1], eyes, mouth)
        ch = [e for e in POSES if e[0] <= t and e[1] != at(POSES, e[0] - 1e-3)[1]] if t > POSES[0][0] else []
        if ch:
            tc = ch[-1][0]; k = (t - tc) * FPS
            if 0 <= k < FADE:
                prev = at(POSES, tc - 1e-3)[1]
                im = Image.blend(render(i, prev, eyes, mouth), im, (k + 1) / (FADE + 1))
        arr = np.clip(np.asarray(im).astype(np.float32) + grain, 0, 255).astype(np.uint8)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close(); ff.wait(); print(out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, "test_video.mp4"))
