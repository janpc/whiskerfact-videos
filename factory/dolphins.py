"""Reel: How do dolphins sleep? — Mr. Whiskerfact, categoría Nature. Sin voz; subtítulos palabra a palabra y efectos."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import brand as B
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, outro_frame, W, H, FPS

R = Reel("nature")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
SUB_Y = B.ZONES["subtitle"][0]
CX, CY = B.ILLU_CENTER

# ---------- delfín ----------
SKIN, SKIN_D, BELLY = (118, 140, 172), (92, 112, 142), (206, 216, 230)
def catmull(pts, n=10):
    out = []
    P = [pts[-1]] + pts + pts[:2]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    return out
BODY = [(300, 8), (262, -2), (222, -36), (160, -62), (60, -76), (-60, -66), (-170, -40), (-262, -14), (-300, 0),
        (-262, 14), (-170, 34), (-40, 62), (100, 60), (210, 32), (262, 16)]
BELLY_PTS = [(262, 16), (210, 30), (100, 58), (-40, 60), (-170, 32), (-150, 12), (-20, 30), (110, 28), (220, 12)]
FIN = [(20, -74), (-30, -150), (-62, -146), (-70, -64)]
FLUKE = [(-292, 0), (-352, -58), (-336, -4), (-352, 56)]
PEC = [(130, 40), (70, 112), (48, 104), (78, 40)]

def dolphin(img, x, y, scale=1.0, eye="open", tilt=0.0, flip=False, alpha=1.0):
    """delfín de perfil mirando a la derecha (o a la izquierda con flip)"""
    s = 2
    size = (int(760 * scale), int(360 * scale))
    lay = Image.new("RGBA", (size[0] * s, size[1] * s), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ox, oy = size[0] / 2, size[1] / 2
    ca, sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    def T(p):
        px, py = p[0] * (-1 if flip else 1), p[1]
        rx, ry = px * ca - py * sa, px * sa + py * ca
        return ((ox + rx * scale) * s, (oy + ry * scale) * s)
    d.polygon([T(p) for p in FIN], fill=SKIN_D)
    d.polygon([T(p) for p in FLUKE], fill=SKIN_D)
    d.polygon([T(p) for p in catmull(BODY)], fill=SKIN)
    d.polygon([T(p) for p in catmull(BELLY_PTS, 6)], fill=BELLY)
    d.polygon([T(p) for p in PEC], fill=SKIN_D)
    ex, ey = T((206, -12)); r = 11 * scale * s
    if eye == "open":
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(30, 28, 40))
        d.ellipse([ex - r * 0.2, ey - r * 0.75, ex + r * 0.4, ey - r * 0.15], fill=(255, 255, 255))
    else:
        d.arc([ex - r * 1.2, ey - r, ex + r * 1.2, ey + r], 20, 160, fill=(30, 28, 40), width=int(4 * scale * s))
    bx, by = T((150, -60)); d.ellipse([bx - 6 * s * scale, by - 4 * s * scale, bx + 6 * s * scale, by + 4 * s * scale], fill=SKIN_D)  # espiráculo
    lay = lay.resize(size, Image.LANCZOS)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(x - size[0] / 2), int(y - size[1] / 2)))

# ---------- burbujas ----------
rng = np.random.default_rng(5)
BUBBLES = [(rng.uniform(80, 1000), rng.uniform(0, 1), rng.uniform(5, 14), rng.uniform(40, 90)) for _ in range(26)]
def bubbles(img, T, a=1.0):
    if a <= 0: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x0, ph, r, sp in BUBBLES:
        y = 1380 - ((ph * 700 + T * sp) % 700)
        x = x0 + 10 * math.sin(T * 1.5 + ph * 9)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(230, 255, 240, int(90 * a)), width=3)
    img.alpha_composite(ov)

def surface_line(img, y, T, a=1.0):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    pts = [(x, y + 8 * math.sin(x / 70 + T * 3)) for x in range(0, W + 20, 20)]
    d.polygon(pts + [(W, y - 200), (0, y - 200)], fill=(255, 255, 255, int(26 * a)))
    d.line(pts, fill=(220, 255, 235, int(200 * a)), width=5)
    img.alpha_composite(ov)

def spout(img, x, y, p):
    if not (0 < p < 1): return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(14):
        ang = -math.pi / 2 + (i - 6.5) * 0.12
        r = 40 + 170 * eo(p) * (0.6 + 0.4 * ((i * 7) % 5) / 4)
        px, py = x + r * math.cos(ang), y + r * math.sin(ang) + 120 * p * p
        rr = 14 * (1 - p) + 4
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(235, 250, 255, int(230 * (1 - p))))
    img.alpha_composite(ov)

# ---------- cerebro (vista superior) ----------
def brain(img, x, y, left_on, right_on, scale=1.0, a=1.0):
    """cerebro visto desde arriba: dos hemisferios con circunvoluciones; *_on de 0 (dormido) a 1 (despierto)"""
    s = 2; size = (int(600 * scale), int(460 * scale))
    lay = Image.new("RGBA", (size[0] * s, size[1] * s), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sleep_c, awake_c = (74, 92, 126), (250, 178, 160)
    cx0, cy0 = size[0] / 2, size[1] / 2
    # contorno de un hemisferio (lado derecho), en unidades de 0..1
    HEMI = [(0.04, -0.92), (0.40, -0.98), (0.78, -0.80), (0.98, -0.40), (1.0, 0.10), (0.90, 0.55),
            (0.62, 0.90), (0.25, 1.0), (0.04, 0.88), (0.06, 0.0)]
    rng2 = np.random.default_rng(11)
    GYRI = [[(rng2.uniform(0.15, 0.85), rng2.uniform(-0.8, 0.8)) for _ in range(4)] for _ in range(7)]
    for side, on in ((-1, left_on), (1, right_on)):
        col = lerpc(sleep_c, awake_c, on)
        line = lerpc((54, 68, 98), (206, 128, 116), on)
        def P(u, v): return ((cx0 + side * (8 + u * 260) * scale) * s, (cy0 + v * 210 * scale) * s)
        d.polygon([P(u, v) for u, v in catmull(HEMI, 8)], fill=col)
        for i, v0 in enumerate((-0.62, -0.22, 0.18, 0.56)):
            pts = [(u, v0 + 0.08 * math.sin(u * 14 + i * 1.3)) for u in np.linspace(0.16, 0.80 - 0.08 * abs(v0), 40)]
            d.line([P(u, v) for u, v in pts], fill=line, width=int(9 * scale * s), joint="curve")
    lay = lay.resize(size, Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (int(x - size[0] / 2), int(y - size[1] / 2)))

def zzz(img, x, y, T, a=1.0):
    if a <= 0: return
    for i in range(3):
        p = ((T * 0.7 + i / 3) % 1)
        R.txt(img, "z", y - 120 * p, "title", (220, 230, 255), a * math.sin(math.pi * p), x=x + 40 * p + i * 6, rise=False)

def eye_icon(img, x, y, open_, a=1.0, r=58):
    ov = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); X, Y = x * 2, y * 2
    if open_:
        d.ellipse([X - r * 2, Y - r * 1.25, X + r * 2, Y + r * 1.25], fill=(246, 244, 238, int(255 * a)))
        d.ellipse([X - r * 0.9, Y - r * 0.9, X + r * 0.9, Y + r * 0.9], fill=(30, 28, 40, int(255 * a)))
        d.ellipse([X - r * 0.1, Y - r * 0.6, X + r * 0.4, Y - r * 0.15], fill=(255, 255, 255, int(255 * a)))
    else:
        d.arc([X - r * 2, Y - r * 1.4, X + r * 2, Y + r * 1.0], 20, 160, fill=(246, 244, 238, int(255 * a)), width=16)
    img.alpha_composite(ov.resize((W, H), Image.LANCZOS))

def link(img, p0, p1, k, col, a=1.0):
    if k <= 0 or a <= 0: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.line([p0, (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k))], fill=col + (int(255 * a),), width=8)
    img.alpha_composite(ov)

# ---------- guion ----------
SC = dict(hook=(0, 3.5), breath=(3.5, 11), problem=(11, 17), half=(17, 24.5), eye=(24.5, 31.5),
          swap=(31.5, 37.5), third=(37.5, 44.5), calves=(44.5, 53.5))
OUTRO_AT = 53.5
R.total = OUTRO_AT + 4.8
CAP = {
    "breath": (4.6, "For you, breathing is automatic. A dolphin decides on every single breath."),
    "problem": (12.0, "If its whole brain fell asleep, it would stop breathing."),
    "half": (18.2, "One half rests while the other keeps watch and comes up for air."),
    "eye": (25.8, "The open eye is on the opposite side of the awake half."),
    "swap": (32.6, "The halves take turns, so the whole brain gets its rest."),
    "third": (39.6, "Just never all at once."),
    "calves": (47.2, "For their first month, newborn calves and their mothers stay active around the clock."),
}
for k, (t0, s) in CAP.items():   # cada bloque cabe en su escena
    assert R.caption_end(s, t0) + 0.4 <= SC[k][1], (k, R.caption_end(s, t0), SC[k][1])

# sonidos: cada animación tiene el suyo
for name, (s, e) in SC.items():
    if name != "hook": R.sound(s, "tap", 0.8)            # entra el título de la escena
R.sound(0.0, "whoosh", 0.7); R.sound(0.6, "pop", 0.8)      # delfín y mascota
R.sound(1.6, "click", 0.6)                                 # parpadeo del ojo que queda abierto
R.sound(6.6, "whoosh", 0.9)                                # sale a respirar
R.sound(11.0, "whoosh", 0.8)                               # golpe de zoom
R.sound(13.6, "click", 0.7)                                # todo se apaga
R.sound(17.6, "pop", 0.6)                                  # aparece el cerebro
R.sound(19.4, "click", 0.6)                                # una mitad se duerme
R.sound(26.0, "click", 0.6); R.sound(27.4, "whoosh", 0.6)  # ojos y línea cruzada
R.sound(33.4, "whoosh", 0.8); R.sound(35.4, "whoosh", 0.8) # las mitades se cambian
R.sound(38.0, "whoosh", 0.9)                               # crece la barra del día
R.sound(44.5, "sparkle", 0.8)                              # destello: el dato final
R.sound(45.4, "bubble", 0.7)

def frame_at(T):
    if T >= OUTRO_AT: return outro_frame(R, T - OUTRO_AT)
    img = R.bg.copy()
    bubbles(img, T, 0.8)
    # ---- HOOK ----
    s, e = SC["hook"]
    if T < e:
        bob = 14 * math.sin(T * 2.2)
        dolphin(img, CX, CY + 40 + bob, 1.15, eye="closed" if 1.5 <= T < 1.65 else "open", tilt=3 * math.sin(T * 2.2))
        zzz(img, CX - 300, CY - 40, T, clamp((T - 0.5) / 0.3))
        R.chrome(img, T)
        fade = clamp((e - T) / B.EXIT)
        l1 = "This dolphin is asleep."
        R.txt(img, l1, TITLE_Y, "hook", B.TEXT, fade, rise=False)
        R.txt(img, "Why is its eye open?", TITLE_Y + R.sprite(l1, "hook", B.TEXT).size[1] - 4, "hook", ACC_T, fade, rise=False)
        R.hook_mascot(img, T, 0.6, e)
        return img
    # ---- BREATH ----
    s, e = SC["breath"]
    if T < e:
        t = T - s
        surf_y = 860
        rise = eio((t - 2.2) / 1.0) * (1 - eio((t - 4.2) / 1.2))
        dolphin(img, CX, lerp(1150, surf_y + 70, rise) + 10 * math.sin(T * 2), 1.0, tilt=-8 * rise)
        surface_line(img, surf_y, T, win(T, s, e))
        spout(img, CX + 60, surf_y + 10, (t - 3.1) / 0.9)
        R.chrome(img, T)
        R.txt(img, "Breathing is a choice", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["breath"][1], T, CAP["breath"][0], e - 0.3)
        return img
    # ---- PROBLEM ----
    s, e = SC["problem"]
    if T < e:
        t = T - s
        off = eio((t - 2.4) / 0.6)
        brain(img, CX, CY - 20, 1 - off, 1 - off, 1.0, win(T, s, e))
        if off > 0.5:
            dr = ImageDraw.Draw(img); c = (255, 120, 110)
            R.txt(img, "No breathing", CY + 230, "label", c, win(T, s + 3.0, e), rise=False)
        R.chrome(img, T)
        R.txt(img, "So it can't fully switch off", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["problem"][1], T, CAP["problem"][0], e - 0.3)
        return R.punch(img, T, s)
    # ---- HALF ----
    s, e = SC["half"]
    if T < e:
        t = T - s
        a = eo(t / 0.5)
        sleepk = eio((t - 2.2) / 0.6)
        brain(img, CX, CY - 40, 1 - sleepk, 1.0, 0.6 + 0.4 * back_out(t / 0.5), a)
        zzz(img, CX - 150, CY - 120, T, sleepk)
        R.txt(img, "Asleep", CY + 200, "label", B.TEXT_2, sleepk, x=CX - 128, rise=False)
        R.txt(img, "Awake", CY + 200, "label", (255, 200, 160), a * clamp((t - 0.6) / 0.3), x=CX + 128, rise=False)
        R.chrome(img, T)
        R.txt(img, "1. Half the brain sleeps", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["half"][1], T, CAP["half"][0], e - 0.3)
        return img
    # ---- EYE ----
    s, e = SC["eye"]
    if T < e:
        t = T - s
        by, ey = CY - 160, CY + 200
        brain(img, CX, by, 0.0, 1.0, 0.62, win(T, s, e))
        a = win(T, s + 1.4, e)
        eye_icon(img, CX - 230, ey, True, a)
        eye_icon(img, CX + 230, ey, False, a)
        k = eo((t - 2.9) / 0.8)
        link(img, (CX + 80, by + 60), (CX - 230, ey - 80), k, (255, 200, 160), win(T, s, e))
        R.txt(img, "Awake half", by - 175, "label", (255, 200, 160), a, x=CX + 160, rise=False)
        R.txt(img, "Open eye", ey + 90, "label", B.TEXT, a, x=CX - 230, rise=False)
        R.chrome(img, T)
        R.txt(img, "2. One eye stays open", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["eye"][1], T, CAP["eye"][0], e - 0.3)
        return img
    # ---- SWAP ----
    s, e = SC["swap"]
    if T < e:
        t = T - s
        k1 = eio((t - 1.9) / 0.6); k2 = eio((t - 3.9) / 0.6)
        left = k1 * (1 - k2); right = 1 - k1 + k2 * 0
        right = 1 - k1 + k2
        brain(img, CX, CY - 40, left, clamp(right), 1.0, win(T, s, e))
        zzz(img, CX - 150 if left < 0.5 else CX + 110, CY - 120, T, win(T, s, e))
        R.chrome(img, T)
        R.txt(img, "3. Then they switch", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["swap"][1], T, CAP["swap"][0], e - 0.3)
        return img
    # ---- A THIRD ----
    s, e = SC["third"]
    if T < e:
        t = T - s
        g = eo((t - 0.5) / 1.3)
        a = win(T, s, e)
        y0 = CY - 40
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.rounded_rectangle([140, y0, 940, y0 + 80], radius=40, fill=R.track + (int(255 * a),))
        if g > 0: d.rounded_rectangle([140, y0, lerp(140, 140 + 800 / 3, g), y0 + 80], radius=40, fill=ACC + (int(255 * a),))
        img.alpha_composite(ov)
        hours = int(round(8 * g))
        R.txt(img, f"{hours} h asleep", y0 - 70, "label", ACC_T, a, x=140, anchor="lt", rise=False, align="left")
        R.txt(img, "24 h", y0 - 70, "label", B.TEXT_2, a, x=940, anchor="rt", rise=False, align="right")
        dolphin(img, CX, CY + 260 + 12 * math.sin(T * 2), 0.7, eye="open", alpha=a)
        R.chrome(img, T)
        R.txt(img, "About a third of the day", TITLE_Y, "title", B.TEXT, win(T, s, e))
        R.caption(img, CAP["third"][1], T, CAP["third"][0], e - 0.3)
        return img
    # ---- CALVES ----
    s, e = SC["calves"]
    t = T - s
    a = eo(t / 0.4)
    sw = math.sin(T * 2.4)
    dolphin(img, CX - 40 + 30 * math.sin(T * 0.8), CY - 10 + 12 * sw, 1.0, tilt=2 * sw, alpha=a)
    dolphin(img, CX + 90 + 30 * math.sin(T * 0.8 + 0.4), CY + 150 + 12 * math.sin(T * 2.4 + 0.8), 0.55, tilt=3 * sw, alpha=a)
    R.chrome(img, T)
    R.txt(img, "The wildest part:", TITLE_Y, "title", B.TEXT_2, win(T, s, e + 1))
    R.txt(img, "newborns barely sleep", TITLE_Y + 97, "title", ACC_T, win(T, s + 0.9, e + 1))
    R.caption(img, CAP["calves"][1], T, CAP["calves"][0], e - 0.3)
    return R.flash(img, T, s)

if __name__ == "__main__":
    if sys.argv[1:2] == ["preview"]:
        ts = [float(x) for x in sys.argv[2:]]
        ims = [frame_at(t).convert("RGB").resize((360, 640)) for t in ts]
        cols = min(5, len(ims))
        sh = Image.new("RGB", (360 * cols, 640 * ((len(ims) + cols - 1) // cols)))
        for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 360, (i // cols) * 640))
        sh.save(os.path.join(R.__class__.__module__ and os.path.dirname(os.path.abspath(__file__)), "out", "dolphins_preview.jpg"), quality=88)
        sys.exit()
    R.render(list(SC.items()), frame_at, "whiskerfact_dolphins", OUTRO_AT)
