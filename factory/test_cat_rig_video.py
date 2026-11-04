"""Prueba de VÍDEO del gato «recortable» (cat_rig), 0 créditos, sin voz.
  python3 test_cat_rig_video.py [salida.mp4]
Parte A (6 s): «cinta de correr»: el gato se queda en el centro y las marcas del suelo se mueven a la velocidad de avance
              (si los pies resbalan respecto a las marcas se nota).
Parte B (6 s): el gato cruza la pantalla de izquierda a derecha con sombra plana.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
F = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, F)
import cat_rig as R
import brand

W, H, FPS = 1080, 1920, 30
K = 2.4                                   # ampliación del rig (cuerpo ~225 px -> ~540 px)
HZ = 1.1                                  # ciclos de andar por segundo (un ciclo = dos pasos)
BASE = 1380
CROP = (150, 60, 650, 460)               # zona del lienzo del rig que contiene al gato
STAND_BOTTOM = R.render(R.stand_pose()).getbbox()[3]      # y del suelo dentro del lienzo del rig
PX = 350                                  # x del centro del cuerpo en el lienzo del rig
SPEED = R.advance_per_cycle() * K * HZ    # px/s de avance: lo que barren los pies en el apoyo
FONT = ImageFont.truetype(os.path.join(F, "mascot", "v4", "fonts", "LondrinaSolid-Regular.ttf"), 64)
INK = (58, 36, 30)
A_DUR, B_DUR = 6.0, 4.8

def sprite(phase):
    im = R.render(R.walk_pose(phase)).crop(CROP)
    return im.resize((round(im.width * K), round(im.height * K)), Image.LANCZOS)

def place(img, spr, cx, base):
    ox = cx - (PX - CROP[0]) * K; oy = base - (STAND_BOTTOM - CROP[1]) * K
    img.alpha_composite(spr, (int(ox), int(oy)))

def bg(label):
    top, bot = brand.bg_for("nature")
    ys = np.linspace(0, 1, H)[:, None, None]
    arr = np.array(top, np.float32)[None, None, :] * (1 - ys) + np.array(bot, np.float32)[None, None, :] * ys
    im = Image.fromarray(np.repeat(arr, W, axis=1).astype(np.uint8), "RGB").convert("RGBA"); d = ImageDraw.Draw(im)
    d.rectangle((0, BASE, W, H), fill=tuple(int(c * 0.55) for c in bot) + (255,))
    d.rectangle((0, BASE, W, BASE + 8), fill=tuple(int(c * 0.8) for c in bot) + (255,))
    d.text((60, 120), label, font=FONT, fill=(255, 245, 225, 255), stroke_width=5, stroke_fill=INK + (255,))
    return im, d

def shadow(im, cx, base, w=470, h=44, a=80):
    tmp = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse((cx - w / 2, base - h * 0.55, cx + w / 2, base + h * 0.45), fill=(0, 0, 0, a))
    im.alpha_composite(tmp)

def frame(t):
    phase = (t * HZ) % 1.0
    if t < A_DUR:
        im, d = bg("A: treadmill")
        off = (SPEED * t) % 180
        for k in range(-1, W // 180 + 2):                       # marcas del suelo hacia atrás
            x = k * 180 - off
            d.rectangle((x, BASE + 22, x + 80, BASE + 40), fill=(255, 220, 120, 255))
            d.rectangle((x + 30, BASE + 80, x + 52, BASE + 92), fill=(190, 160, 90, 255))
        place(im, sprite(phase), 540, BASE)
    else:
        tt = t - A_DUR
        im, d = bg("B: crossing")
        x = -300 + SPEED * tt
        shadow(im, x, BASE)
        place(im, sprite(phase), x, BASE)
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    arr += np.random.default_rng(int(t * FPS)).normal(0, 1.6, (H, W, 1)).astype(np.float32)
    return arr.clip(0, 255).astype(np.uint8)

def main(out):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int((A_DUR + B_DUR) * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", out, "velocidad", round(SPEED), "px/s")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(F, "out", "test_cat_rig.mp4"))
