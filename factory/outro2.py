"""Dos propuestas de cierre con Mr. Whiskerfact como personaje (sin el círculo del avatar).

A · "gafas":   asoma desde abajo, mira a cámara, se sube las gafas con la pata y guiña.
B · "pizarra": junto a una pizarra; el eslogan se escribe con tiza mientras lo señala, luego se gira y guiña.
Uso: python3 outro2.py a|b [preview]
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import mascota3 as m
import mascota_m1b as mb

SS = 2                      # supermuestreo del personaje
m.S = SS; mb.S = SS         # los módulos de la mascota dibujan con esta escala
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = B.W, B.H, B.FPS
CAT = "science"
V = dict(mb.VARIANTS[5], acc=[])      # el gato definitivo, sin gafas (van aparte)
FUR, CARDI = V["fur"], V["top"][1]
GLASS = (60, 48, 54); AMBER = mb.AMBER; INK = m.INK
CW, CH = 1080, 1800         # espacio del personaje (coordenadas del avatar)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back_out(x, k=1.7):
    x = clamp(x) - 1; return x * x * ((k + 1) * x + k) + 1
def lerp(a, b, k): return a + (b - a) * k

def Q(x, y): return (x * SS, y * SS)
def BX(cx, cy, rx, ry): return [*Q(cx - rx, cy - ry), *Q(cx + rx, cy + ry)]

# ---------- piezas ----------
def torso(d):
    cd = tuple(int(c * 0.74) for c in CARDI)
    d.polygon([Q(150, 1800), Q(170, 1060), Q(230, 930), Q(340, 860), Q(540, 900), Q(740, 860), Q(850, 930), Q(910, 1060), Q(930, 1800)], fill=CARDI)
    d.line([Q(250, 1150), Q(260, 1800)], fill=cd, width=5 * SS)     # pliegues de las mangas
    d.line([Q(830, 1150), Q(820, 1800)], fill=cd, width=5 * SS)
    d.polygon([Q(440, 852), Q(540, 1060), Q(640, 852)], fill=m.WHITE)
    d.line([Q(440, 852), Q(540, 1060)], fill=cd, width=10 * SS)
    d.line([Q(640, 852), Q(540, 1060)], fill=cd, width=10 * SS)
    d.line([Q(540, 1060), Q(540, 1800)], fill=cd, width=6 * SS)
    for y in (1110, 1210, 1310):
        d.ellipse(BX(512, y, 11, 11), fill=cd)

def bowtie(d):
    c = V["tie"][1]
    d.polygon([Q(540, 880), Q(470, 850), Q(470, 910)], fill=c)
    d.polygon([Q(540, 880), Q(610, 850), Q(610, 910)], fill=c)
    d.ellipse(BX(540, 880, 18, 20), fill=tuple(int(x * 0.78) for x in c))

def eyes(d, state="open", dx=0.0, dy=0.0):
    """state: open | closed | wink (ojo izquierdo cerrado)"""
    for i, ex in enumerate((425, 655)):
        shut = state == "closed" or (state == "wink" and i == 0)
        d.ellipse(BX(ex, 568, 68, 76), fill=FUR)
        if shut:
            d.arc([*Q(ex - 50, 540), *Q(ex + 50, 610)], 20, 160, fill=INK, width=10 * SS)
            continue
        d.ellipse(BX(ex, 568, 64, 72), fill=m.WHITE)
        d.ellipse(BX(ex + 6 + dx, 574 + dy, 46, 54), fill=AMBER)
        d.ellipse(BX(ex + 6 + dx, 578 + dy, 26, 34), fill=INK)
        d.ellipse(BX(ex + 22 + dx * 0.8, 552 + dy * 0.8, 15, 17), fill=m.WHITE)
        d.ellipse(BX(ex - 8 + dx * 0.8, 596 + dy * 0.8, 7, 8), fill=m.WHITE)

def brows(d, lift=0.0):
    d.arc(BX(425, 482 - lift, 58, 30), 200, 340, fill=INK, width=10 * SS)
    d.arc(BX(655, 472 - lift, 62, 34), 200, 340, fill=INK, width=10 * SS)

def glasses(d, oy=0.0):
    for ex in (425, 655):
        d.ellipse(BX(ex, 568 + oy, 92, 92), outline=GLASS, width=13 * SS)
        d.arc(BX(ex - 22, 546 + oy, 52, 52), 200, 260, fill=(255, 255, 255), width=7 * SS)
    d.arc(BX(540, 560 + oy, 46, 30), 200, 340, fill=GLASS, width=12 * SS)

def paw(d, px, py, arm_from, pointer_to=None):
    """brazo con manga desde arm_from hasta la pata en (px, py)"""
    cd = tuple(int(c * 0.74) for c in CARDI)
    d.line([Q(*arm_from), Q(px, py + 40)], fill=cd, width=96 * SS)
    d.line([Q(*arm_from), Q(px, py + 40)], fill=CARDI, width=84 * SS)
    d.ellipse(BX(px, py + 44, 46, 18), fill=m.WHITE)                      # puño de la camisa
    if pointer_to:
        d.line([Q(px, py), Q(*pointer_to)], fill=(150, 102, 60), width=12 * SS)
        d.ellipse(BX(*pointer_to, 8, 8), fill=(240, 236, 226))
    d.ellipse(BX(px, py, 52, 46), fill=FUR)
    for tx in (-28, 0, 28):
        d.ellipse(BX(px + tx, py - 34, 17, 15), fill=FUR)
    d.ellipse(BX(px, py + 6, 20, 16), fill=(240, 160, 170))

def character(state="open", dx=0, dy=0, glasses_oy=0, brow_lift=0, tilt=0.0, paw_args=None):
    """el personaje entero en un RGBA de 1080x1800"""
    big = Image.new("RGBA", (CW * SS, CH * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    torso(d)
    head = Image.new("RGBA", big.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(head)
    m.draw_cat(hd, V, oy=0)
    eyes(hd, state, dx, dy); brows(hd, brow_lift); glasses(hd, glasses_oy)
    if tilt: head = head.rotate(tilt, resample=Image.BICUBIC, center=Q(540, 860))
    big.alpha_composite(head)
    d = ImageDraw.Draw(big); bowtie(d)
    if paw_args: paw(d, *paw_args)
    return big.resize((CW, CH), Image.LANCZOS)

# ---------- fondo y marca ----------
top, bot = B.bg_for(CAT)
yy = np.linspace(0, 1, H)[:, None, None]
BG = Image.fromarray(((np.array(top) * (1 - yy) + np.array(bot) * yy) * np.ones((1, W, 1))).astype(np.uint8)).convert("RGBA")
def fnt(style):
    w, size, lh = B.TYPE[style]
    return ImageFont.truetype(B.FONT_DIR + f"InterDisplay-{w}.otf", size), size, lh
def chrome(img):
    y0 = B.ZONES["brand"][0]; acc = B.CATEGORIES[CAT]["color"]; d = ImageDraw.Draw(img)
    f, _, _ = fnt("brand"); d.text((140, y0 + 6), "MR. WHISKERFACT", font=f, fill=B.GOLD)
    fc, _, _ = fnt("chip"); lab = B.CATEGORIES[CAT]["label"]; cw = fc.getlength(lab) + 40
    d.rounded_rectangle([940 - cw, y0, 940, y0 + 40], radius=20, fill=acc)
    d.text((940 - cw / 2, y0 + 21), lab, font=fc, fill=B.CHIP_TEXT, anchor="mm")
    d.rounded_rectangle([140, y0 + 52, 940, y0 + 58], radius=3, fill=acc)

def place(img, ch, scale, head_x, head_y):
    """coloca el personaje para que el centro de la cabeza (540,600) caiga en (head_x, head_y)"""
    s = ch.resize((int(CW * scale), int(CH * scale)), Image.LANCZOS)
    x, y = int(head_x - 540 * scale), int(head_y - 600 * scale)
    img.alpha_composite(s, (x, y)) if y < H else None

def word_slogan(img, t, times, y0=360):
    f, size, lh = fnt("title"); lhp = int(size * lh)
    lines = ["Class dismissed.", "Stay curious."]; k = 0
    for li, line in enumerate(lines):
        x = W / 2 - f.getlength(line) / 2
        for w in line.split():
            a = clamp((t - times[k]) / 0.15); k += 1
            if a > 0:
                lay = Image.new("RGBA", (int(f.getlength(w)) + 12, lhp + 20), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((0, 0), w, font=f, fill=B.GOLD + (int(255 * a),))
                img.alpha_composite(lay, (int(x), int(y0 + li * lhp + (1 - eo(a)) * 18)))
            x += f.getlength(w + " ")

# ---------- A · asoma y se ajusta las gafas ----------
DUR_A = 4.5
def frame_a(t):
    img = BG.copy(); chrome(img)
    rise = 900 * (1 - back_out(t / 0.55))
    state = "open"
    if 0.85 <= t < 0.97: state = "closed"           # parpadeo
    if 2.55 <= t < 3.0: state = "wink"
    # la pata sube a las gafas (1.2-1.6), las empuja (1.6-1.85) y baja (1.85-2.3)
    paw_args, g_oy = None, 0
    if 1.2 <= t < 2.3:
        up = eo((t - 1.2) / 0.4) if t < 1.85 else 1 - eio((t - 1.85) / 0.45)
        push = eio((t - 1.6) / 0.2) - eio((t - 2.0) / 0.3) * 0.0
        py = lerp(1350, 640, up) - 14 * push
        paw_args = (lerp(860, 770, up), py, (860, 1150))
        g_oy = -14 * eio((t - 1.6) / 0.2)
    elif t >= 2.3:
        g_oy = -14
    tilt = 4 * math.sin(clamp((t - 2.55) / 0.45) * math.pi)
    dy = -6 if 1.2 <= t < 1.9 else 0                  # mira hacia la pata
    ch = character(state, 0, dy, g_oy, brow_lift=6 * clamp((t - 2.5) / 0.2) * (1 - clamp((t - 3.1) / 0.3)), tilt=tilt, paw_args=paw_args)
    place(img, ch, 0.85, 540, 1080 + rise)
    word_slogan(img, t, [0.7, 1.0, 2.6, 2.9])
    return img

# ---------- B · pizarra ----------
DUR_B = 5.2
CHALK = ImageFont.truetype(B.FONT_DIR + "InterDisplay-SemiBoldItalic.otf" if os.path.exists(B.FONT_DIR + "InterDisplay-SemiBoldItalic.otf") else B.FONT_DIR + "Inter-SemiBoldItalic.otf", 112)
BOARD = (70, 340, 1010, 1000)
def make_board():
    x0, y0, x1, y1 = BOARD
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(128, 88, 54))
    d.rounded_rectangle([x0 + 20, y0 + 20, x1 - 20, y1 - 20], radius=8, fill=(34, 60, 50))
    # restos de tiza borrada
    rng = np.random.default_rng(3)
    smear = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(smear)
    for _ in range(14):
        cx, cy = rng.uniform(x0 + 80, x1 - 80), rng.uniform(y0 + 80, y1 - 80)
        sd.ellipse([cx - 120, cy - 30, cx + 120, cy + 30], fill=int(rng.uniform(10, 22)))
    smear = smear.filter(ImageFilter.GaussianBlur(30))
    wl = Image.new("RGBA", (W, H), (230, 236, 230, 0)); wl.putalpha(smear)
    lay.alpha_composite(wl)
    d = ImageDraw.Draw(lay)
    d.rectangle([x0 + 40, y1 - 20, x1 - 40, y1 - 4], fill=(150, 104, 66))      # repisa
    d.rounded_rectangle([x1 - 210, y1 - 34, x1 - 150, y1 - 18], radius=6, fill=(240, 236, 226))  # tiza
    return lay
BOARD_IMG = make_board()

LINES_B = [("Class dismissed.", 470), ("Stay curious.", 660)]
def chalk_text():
    """texto de tiza y su ancho por línea"""
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay); spans = []
    for s, y in LINES_B:
        w = CHALK.getlength(s); x = W / 2 - w / 2
        d.text((x, y), s, font=CHALK, fill=255); spans.append((x, x + w, y))
    noise = np.random.default_rng(7).uniform(0.55, 1.0, (H, W))
    a = (np.array(lay, np.float32) * noise).astype(np.uint8)
    return Image.fromarray(a), spans
CHALK_A, SPANS = chalk_text()
WRITE = [(0.5, 1.9), (2.0, 3.1)]      # s, escritura de cada línea

def frame_b(t):
    img = BG.copy(); chrome(img)
    ba = eo(t / 0.35)
    bl = BOARD_IMG.copy(); bl.putalpha(bl.split()[3].point(lambda v: int(v * ba)))
    img.alpha_composite(bl)
    # tiza que se va escribiendo
    reveal = np.zeros((H, W), np.uint8); tip = None
    for (x0, x1, y), (ws, we) in zip(SPANS, WRITE):
        k = clamp((t - ws) / (we - ws))
        if k <= 0: continue
        xr = lerp(x0, x1, k)
        reveal[y - 10:y + 150, :int(xr)] = 255
        if k < 1: tip = (xr, y + 70 + 10 * math.sin(t * 40))
    a = (np.array(CHALK_A, np.float32) * reveal / 255).astype(np.uint8)
    chalk = Image.new("RGBA", (W, H), (240, 244, 238, 0)); chalk.putalpha(Image.fromarray(a))
    img.alpha_composite(chalk)
    # el gato, abajo a la izquierda, delante de la pizarra
    rise = 700 * (1 - back_out((t - 0.1) / 0.5))
    hx, hy, sc = 320, 1270, 0.66
    state, dx, dy = "open", 0, 0
    if tip:  # mira a la tiza
        vx, vy = tip[0] - hx, tip[1] - hy; n = math.hypot(vx, vy) or 1
        dx, dy = 14 * vx / n, 14 * vy / n
    if 3.25 <= t < 3.37: state = "closed"
    if 3.7 <= t < 4.15: state = "wink"
    paw_args, pointer = None, None
    if t < 3.25:
        # puntero desde la pata hasta la punta de la tiza (o al final de la línea)
        target = tip or (SPANS[1][1] if t > 3.1 else SPANS[0][0], (SPANS[1][2] if t > 3.1 else SPANS[0][2]) + 80)
        pw = (800, 820)       # pata en coordenadas del personaje
        paw_args = (pw[0], pw[1], (850, 1150))
        pointer = target
    tilt = -6 * eio((t - 3.3) / 0.3) * (1 - eio((t - 4.4) / 0.4))
    ch = character(state, dx, dy, 0, brow_lift=6 * clamp((t - 3.6) / 0.2) * (1 - clamp((t - 4.3) / 0.3)), tilt=tilt, paw_args=paw_args)
    place(img, ch, sc, hx, hy + rise)
    if pointer and paw_args:
        px, py = hx + (paw_args[0] - 540) * sc, hy + rise + (paw_args[1] - 600) * sc
        ov = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.line([(px * 2, py * 2), (pointer[0] * 2, pointer[1] * 2)], fill=(150, 102, 60, 255), width=16)
        od.ellipse([pointer[0] * 2 - 10, pointer[1] * 2 - 10, pointer[0] * 2 + 10, pointer[1] * 2 + 10], fill=(240, 236, 226, 255))
        img.alpha_composite(ov.resize((W, H), Image.LANCZOS))
        # la pata vuelve a dibujarse encima del puntero
        pl = Image.new("RGBA", (CW * SS, CH * SS), (0, 0, 0, 0)); paw(ImageDraw.Draw(pl), paw_args[0], paw_args[1], (paw_args[0], paw_args[1] + 60))
        pl = pl.resize((int(CW * sc), int(CH * sc)), Image.LANCZOS)
        img.alpha_composite(pl, (int(hx - 540 * sc), int(hy + rise - 600 * sc)))
    return img

def render(which):
    fn, dur = (frame_a, DUR_A) if which == "a" else (frame_b, DUR_B)
    out = os.path.join(HERE, "out", f"outro_{'gafas' if which == 'a' else 'pizarra'}.mp4")
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
        ts = [float(x) for x in sys.argv[3:]]
        ims = [fn(t).convert("RGB").resize((360, 640)) for t in ts]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
        sh.save(os.path.join(HERE, "out", f"outro2_{which}_preview.jpg"), quality=88); sys.exit()
    print(render(which))
