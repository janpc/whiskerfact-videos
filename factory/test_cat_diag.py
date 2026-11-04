"""Vídeo de DIAGNÓSTICO del ciclo de andar (0 créditos, sin voz): el gato queda quieto en el centro.
  WALK_SKIP=0 WALK_SHEET=<hoja.png> python3 test_cat_diag.py [salida.mp4]
Parte A: cámara lenta, cada dibujo del ciclo numerado, con la línea de suelo y una vertical por el centro del cuerpo.
Parte B: «cinta de correr» a velocidad normal: las marcas del suelo se desplazan a la velocidad de avance; si los pies resbalan
         respecto a las marcas, la velocidad no encaja con el ciclo.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
F = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, F)
import test_cat_video as T

W, H, FPS = T.W, T.H, 30
BASE = 1200
SLOW_FPS = 2.5; CYCLES = 2
N = len(T.WALK)
A_DUR = N * CYCLES / SLOW_FPS
B_DUR = 6.0
FONT = ImageFont.truetype(T.FONT, 120); SMALL = ImageFont.truetype(T.FONT, 64)

def base_img(label):
    im = Image.new("RGBA", (W, H), (20, 60, 44, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, BASE, W, H), fill=(14, 40, 30, 255))
    d.text((60, 120), label, font=SMALL, fill=(255, 245, 225, 255), stroke_width=5, stroke_fill=T.INK + (255,))
    return im, d

def frame(t):
    if t < A_DUR:
        i = int(t * SLOW_FPS) % N
        im, d = base_img("A: slow motion (frame by frame)")
        d.line((0, BASE, W, BASE), fill=(255, 255, 255, 255), width=3)               # suelo
        d.line((540, 300, 540, BASE), fill=(255, 220, 120, 255), width=2)             # centro del cuerpo
        T.place_walk(im, i, 540, BASE, T.K)
        d.text((60, 260), f"{i + 1} / {N}", font=FONT, fill=(255, 220, 120, 255), stroke_width=6, stroke_fill=T.INK + (255,))
    else:
        tt = t - A_DUR
        im, d = base_img("B: treadmill (normal speed)")
        d.line((0, BASE, W, BASE), fill=(255, 255, 255, 255), width=3)
        off = (T.SPEED * tt) % 160
        for k in range(-1, W // 160 + 2):
            x = k * 160 - off
            d.rectangle((x, BASE + 16, x + 70, BASE + 34), fill=(255, 220, 120, 255))      # marcas del suelo (se mueven hacia atrás)
            d.rectangle((x + 20, BASE + 70, x + 40, BASE + 82), fill=(190, 160, 90, 255))
        T.place_walk(im, int(tt * T.WALK_FPS), 540, BASE, T.K)
    arr = np.asarray(im.convert("RGB"))
    return arr

def main(out):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int((A_DUR + B_DUR) * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(F, "out", "test_cat_diag.mp4"))
