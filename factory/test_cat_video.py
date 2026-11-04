"""Prueba de VÍDEO del gato doméstico normal de la biblioteca (`cat`) y de los objetos nuevos (0 créditos, sin voz).
  python3 test_cat_video.py [salida.mp4]
Escenas: andar y parar en el centro -> curioso y alerta -> noche con ojos brillantes -> correr (de derecha a izquierda).
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, F)
import library as LIB
import brand

W, H, FPS = 1080, 1920, 30
GROUND_Y = 1420
K = 2.2                                   # escala sobre la hoja (los sprites miden ~240 px): ampliar más los vuelve blandos
FONT = os.path.join(F, "mascot", "v4", "fonts", "LondrinaSolid-Regular.ttf")
INK = (58, 36, 30)
WALK_FPS = 6                              # ciclo de 8 dibujos (walk1..walk8): un ciclo = dos pasos
# un ciclo desplaza el cuerpo ~1,56 veces el ancho del dibujo de contacto (pie que se apoya: de delante a atrás en ~60 % del ciclo)
SPEED = 1.56 * LIB.get("cat", "walk1").width * K * WALK_FPS / 8      # px/s: los pies no patinan
X0, XC = -900, 540
T_STOP = (XC - X0) / SPEED                # llega al centro
T_CURIOUS, T_ALERT, T_NIGHT, T_RUN = T_STOP + 0.9, T_STOP + 2.7, T_STOP + 4.5, T_STOP + 8.1
RUN_SPEED = 950
DUR = T_RUN + 2.8

def lerp(a, b, k): return a + (b - a) * k
def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)

def background(t):
    day_top, day_bot = brand.bg_for("nature")
    night_top, night_bot = (12, 16, 36), (22, 28, 56)
    dark = ease((t - (T_NIGHT - 0.8)) / 1.0) * (1 - ease((t - (T_RUN - 0.6)) / 0.8))
    top = tuple(lerp(a, b, dark) for a, b in zip(day_top, night_top))
    bot = tuple(lerp(a, b, dark) for a, b in zip(day_bot, night_bot))
    ys = np.linspace(0, 1, H)[:, None, None]
    arr = np.array(top, np.float32)[None, None, :] * (1 - ys) + np.array(bot, np.float32)[None, None, :] * ys
    im = Image.fromarray(np.repeat(arr, W, axis=1).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle((0, GROUND_Y, W, H), fill=tuple(int(c * 0.55) for c in bot) + (255,))
    d.rectangle((0, GROUND_Y, W, GROUND_Y + 8), fill=tuple(int(c * 0.8) for c in bot) + (255,))
    return im

def label(im, text, t0, t1, t):
    a = ease((t - t0) / 0.3) * (1 - ease((t - t1) / 0.3))
    if a <= 0.01: return
    f = ImageFont.truetype(FONT, 96)
    tmp = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, 150), text, font=f, fill=(255, 245, 225, int(255 * a)), stroke_width=7, stroke_fill=INK + (int(255 * a),))
    im.alpha_composite(tmp)

def feathered(im, name, pose, cx, cy, scale, a=1.0, feather=40):
    """tarjeta con el borde difuminado (los ojos de la hoja traen fondo rectangular)"""
    spr = LIB.get(name, pose)
    s = spr.resize((round(spr.width * scale), round(spr.height * scale)), Image.LANCZOS)
    m = Image.new("L", s.size, 0); ImageDraw.Draw(m).rectangle((feather, feather, s.width - feather, s.height - feather), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(feather / 2.2))
    al = np.minimum(np.asarray(s.split()[3]).astype(np.float32), np.asarray(m).astype(np.float32)) * a
    s.putalpha(Image.fromarray(al.astype(np.uint8)))
    im.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def frame(t):
    im = background(t)
    breath = (1, 1 + 0.012 * math.sin(t * 2.4))
    base = GROUND_Y + 6
    if t < T_CURIOUS:
        if t < T_STOP:
            LIB.place(im, "cat", LIB.cycle("cat", "walk", t, fps=WALK_FPS), X0 + SPEED * t, base, scale=K, xanchor="head")
        else:
            LIB.place(im, "cat", "side", XC, base, scale=K, squash=breath, xanchor="head")
        label(im, "walks", 0.2, T_CURIOUS + 0.4, t)
    elif t < T_NIGHT:
        pose = "curious" if t < T_ALERT else "alert"
        LIB.place(im, "cat", pose, XC, base, scale=K, squash=breath, xanchor="head")
        label(im, "curious... alert", T_CURIOUS + 0.2, T_NIGHT - 0.3, t)
    elif t < T_RUN:
        k = ease((t - (T_NIGHT + 0.3)) / 0.5)
        LIB.place(im, "cat", "stare", 540, base, scale=K * 1.1, squash=breath)
        feathered(im, "cat_eye_night_items", "eyes_glow", 540, 580, 2.0 * (0.85 + 0.15 * k), a=k)
        label(im, "night vision", T_NIGHT + 0.1, T_RUN - 0.3, t)
    else:
        x = 1300 - RUN_SPEED * (t - T_RUN)
        LIB.place(im, "cat", LIB.cycle("cat", "run", t, fps=10), x, base, scale=K, flip=True, xanchor="head")
        label(im, "runs", T_RUN + 0.2, DUR - 0.3, t)
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    arr += np.random.default_rng(int(t * FPS)).normal(0, 1.6, (H, W, 1)).astype(np.float32)   # grano plano sutil
    return arr.clip(0, 255).astype(np.uint8)

def main(out):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(F, "out", "test_cat.mp4"))
