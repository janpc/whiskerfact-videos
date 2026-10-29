"""Cierre v4: Mr. Whiskerfact dentro de su círculo.
A · gafas:   el círculo entra con rebote; dentro, el gato parpadea, se sube las gafas y guiña.
B · pizarra: el eslogan se escribe solo en la pizarra; el gato, en su círculo debajo, lo sigue con la mirada y guiña.
Uso: python3 outro4.py a|b [preview t1 t2 ...]
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import outro2 as o
from outro2 import clamp, eo, eio, back_out, lerp

W, H, FPS = B.W, B.H, B.FPS
HERE = o.HERE

# ---------- el círculo ----------
_disc = None
def disc():
    global _disc
    if _disc is None:
        yy = np.linspace(0, 1, 1080)[:, None, None]
        arr = (np.array(o.m.NAVY1) * (1 - yy) + np.array(o.m.NAVY2) * yy) * np.ones((1, 1080, 1))
        _disc = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    return _disc
MASK = Image.new("L", (2160, 2160), 0); ImageDraw.Draw(MASK).ellipse([0, 0, 2159, 2159], fill=255)
MASK = MASK.resize((1080, 1080), Image.LANCZOS)

def badge(ch, ring_pulse=0.0):
    """personaje (1080x1800) dentro del avatar redondo de 1080"""
    im = disc().copy()
    im.alpha_composite(ch.crop((0, 10, 1080, 1090)))
    out = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    out.paste(im, (0, 0), MASK)
    ring = Image.new("RGBA", (2160, 2160), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([24, 24, 2136, 2136], outline=B.GOLD, width=28)
    out.alpha_composite(ring.resize((1080, 1080), Image.LANCZOS))
    return out

def put_badge(img, b, size, cx, cy, pulse=0.0):
    s = b.resize((int(size), int(size)), Image.LANCZOS)
    img.alpha_composite(s, (int(cx - size / 2), int(cy - size / 2)))
    if pulse > 0:
        r = size / 2 + 6 + 30 * eo(pulse)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([cx - r, cy - r, cx + r, cy + r], outline=B.GOLD + (int(200 * (1 - pulse)),), width=8)
        img.alpha_composite(ov)

# ---------- A · gafas ----------
DUR_A = 4.8
WORDS_A = [0.7, 1.0, 2.6, 2.9]
WINK = WORDS_A[-1] + 0.15 + 0.2    # el guiño llega cuando ya se ha leído la última palabra
def frame_a(t):
    img = o.BG.copy(); o.chrome(img)
    state = "open"
    if 0.85 <= t < 0.97: state = "closed"
    if WINK <= t < WINK + 0.45: state = "wink"
    paw_args, g_oy = None, 0
    if 1.2 <= t < 2.3:
        up = eo((t - 1.2) / 0.4) if t < 1.85 else 1 - eio((t - 1.85) / 0.45)
        py = lerp(1350, 640, up) - 14 * eio((t - 1.6) / 0.2)
        paw_args = (lerp(860, 770, up), py, (860, 1150))
        g_oy = -14 * eio((t - 1.6) / 0.2)
    elif t >= 2.3:
        g_oy = -14
    tilt = 4 * math.sin(clamp((t - WINK) / 0.45) * math.pi)
    dy = -6 if 1.2 <= t < 1.9 else 0
    lift = 6 * clamp((t - (WINK - 0.05)) / 0.2) * (1 - clamp((t - (WINK + 0.55)) / 0.3))
    b = badge(o.character(state, 0, dy, g_oy, brow_lift=lift, tilt=tilt, paw_args=paw_args))
    k = back_out(t / 0.5)
    size = 600 * (0.55 + 0.45 * k)
    cy = lerp(1750, 1060, eo(t / 0.5))
    pulse = clamp((t - WINK) / 0.7) if WINK <= t < WINK + 0.7 else 0
    put_badge(img, b, size, 540, cy, pulse)
    o.word_slogan(img, t, WORDS_A)
    return img

# ---------- B · pizarra ----------
DUR_B = 5.2
CHALK = ImageFont.truetype(B.FONT_DIR + "InterDisplay-Bold.otf", 104)
def chalk_text():
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay); spans = []
    for s, y in o.LINES_B:
        w = CHALK.getlength(s); x = W / 2 - w / 2
        d.text((x, y), s, font=CHALK, fill=255); spans.append((x, x + w, y))
    noise = np.random.default_rng(7).uniform(0.5, 1.0, (H, W))
    a = (np.array(lay.filter(ImageFilter.GaussianBlur(0.6)), np.float32) * noise).astype(np.uint8)
    return a, spans
CHALK_A, SPANS = chalk_text()
WRITE = [(0.5, 1.9), (2.0, 3.1)]
BCX, BCY, BSIZE = 540, 1300, 440

def frame_b(t):
    img = o.BG.copy(); o.chrome(img)
    ba = eo(t / 0.35)
    bl = o.BOARD_IMG.copy(); bl.putalpha(bl.split()[3].point(lambda v: int(v * ba)))
    img.alpha_composite(bl)
    reveal = np.zeros((H, W), np.float32); tip = None
    for (x0, x1, y), (ws, we) in zip(SPANS, WRITE):
        k = clamp((t - ws) / (we - ws))
        if k <= 0: continue
        xr = lerp(x0, x1, k)
        reveal[y - 10:y + 150, :int(xr)] = 1
        if k < 1: tip = (xr, y + 60)
    chalk = Image.new("RGBA", (W, H), (240, 244, 238, 0))
    chalk.putalpha(Image.fromarray((CHALK_A * reveal).astype(np.uint8)))
    img.alpha_composite(chalk)
    state, dx, dy = "open", 0, 0
    if tip:
        vx, vy = tip[0] - BCX, tip[1] - BCY; n = math.hypot(vx, vy) or 1
        dx, dy = 14 * vx / n, 14 * vy / n
    if 3.25 <= t < 3.37: state = "closed"
    if 3.7 <= t < 4.15: state = "wink"
    tilt = -5 * eio((t - 3.6) / 0.3) * (1 - eio((t - 4.4) / 0.4))
    lift = 6 * clamp((t - 3.6) / 0.2) * (1 - clamp((t - 4.3) / 0.3))
    b = badge(o.character(state, dx, dy, 0, brow_lift=lift, tilt=tilt))
    k = back_out((t - 0.1) / 0.5)
    size = BSIZE * (0.55 + 0.45 * k) if t >= 0.1 else 1
    cy = lerp(1800, BCY, eo((t - 0.1) / 0.5))
    pulse = clamp((t - 3.7) / 0.7) if 3.7 <= t < 4.4 else 0
    if t >= 0.1: put_badge(img, b, size, BCX, cy, pulse)
    return img

def render(which):
    fn, dur = (frame_a, DUR_A) if which == "a" else (frame_b, DUR_B)
    out = os.path.join(HERE, "out", f"outro_circulo_{'gafas' if which == 'a' else 'pizarra'}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                          "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for n in range(int(dur * FPS)):
        p.stdin.write(fn(n / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(out + ".tmp.mp4", out)
    return out

if __name__ == "__main__":
    which = sys.argv[1]
    if sys.argv[2:3] == ["preview"]:
        fn = frame_a if which == "a" else frame_b
        ims = [fn(float(x)).convert("RGB").resize((360, 640)) for x in sys.argv[3:]]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
        sh.save(os.path.join(HERE, "out", f"outro4_{which}_preview.jpg"), quality=88); sys.exit()
    print(render(which))
