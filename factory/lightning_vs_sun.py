"""Reel: Lightning vs the Sun: which is really hotter? Mr. Whiskerfact, categoría Science, formato versus.
Voz de Brad. Tanda B2-length, opción `short` (variante): ejecutar con REEL_LENGTH=short. Bucle (loop=True).

Fuentes (dos por dato): ver voice/lightning_vs_sun_claims.md
- Rayo ~50.000 °F, 5 veces la superficie del Sol: NWS (lightning-temperature, MLB), NOAA NSSL, Britannica
- Superficie del Sol ~10.000 °F y núcleo > 27 millones °F: NASA Sun facts, Britannica, Space.com
- Fulguritas: Britannica, Utah Geological Survey
- Un destello dura menos de un segundo: NWS MLB, NOAA NSSL

Sol, rayo, termómetros, barras y marcador por código (vectorial); biblioteca (lightning_items, large_w47) a ≤1,5x.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import brand as B
import style as ST
import library as LIB
import cover as cover_mod
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

SLUG = "lightning_vs_sun"
CATEGORY = "science"
R = Reel(CATEGORY)
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "Lightning"), ("rounds", "Three"), ("heat", "Lightning"), ("surf", "The"), ("five", "So"),
    ("glass", "That"), ("flash", "Next"), ("long", "The"), ("core", "Final"), ("touch", "Lightning"),
    ("score", "Score"), ("take", "Honestly"), ("bridge", "So")], loop=True)
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (30, 70, 150)
YELLOW = (255, 222, 90)
BOLT_Y = (255, 228, 70)
SUN_A, SUN_B = (255, 196, 60), (246, 140, 40)
RED = (222, 64, 60)
CARD = (56, 742, 1024, 1384)
LI, LW = "lightning_items", "large_w47"
LINE1, LINE2, SUB = "Lightning", "vs Sun", "Which is really hotter?"

def wt(word, s): return V.word_time(word.strip('"“”,.?!:'), after=s)
def rel(scene, word): return wt(word, V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))
def on(T, word, s, e, need=1.6, lead=0.1): return clamp((T - min(wt(word, s), e - need) + lead) / 0.3)

def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def item(img, lib, name, x, y, h, a=1.0, anchor="center", flip=False, rot=0.0):
    LIB.place(img, lib, name, x, y, height=h, a=a, anchor=anchor, flip=flip, rot=rot)

def glow(img, cx, cy, r, col, a):
    if a <= 0.01: return
    g = Image.new("RGBA", (int(r * 3), int(r * 3)), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([r * 0.5, r * 0.5, r * 2.5, r * 2.5], fill=col + (int(150 * a),))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.35))
    img.alpha_composite(g, (int(cx - r * 1.5), int(cy - r * 1.5)))

# ---------- dibujos vectoriales ----------
BOLT_PTS = [(0.10, -0.50), (-0.24, 0.04), (-0.02, 0.04), (-0.14, 0.50), (0.26, -0.10), (0.04, -0.10), (0.18, -0.50)]
def bolt(img, cx, cy, h, a=1.0, rot=0.0):
    """rayo en zigzag (el «personaje» del rayo)"""
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = [(cx + (x * cr - y * sr) * h, cy + (x * sr + y * cr) * h) for x, y in BOLT_PTS]
    def fn(d, P, s):
        d.polygon([P(*p) for p in pts], fill=BOLT_Y, outline=INK_T, width=int(9 * s))
        hi = [(cx + (x * 0.55 * cr - y * 0.8 * sr) * h - 0.03 * h, cy + (x * 0.55 * sr + y * 0.8 * cr) * h) for x, y in BOLT_PTS[:4]]
        d.line([P(*p) for p in hi[:3]], fill=(255, 250, 200), width=int(7 * s), joint="curve")
    aa(img, (cx - h * 0.6, cy - h * 0.6, cx + h * 0.6, cy + h * 0.6), fn, a)

def strike(img, x0, y0, x1, y1, seed, a=1.0, w=14):
    """descarga quebrada de la nube al suelo, con brillo"""
    rng = np.random.default_rng(seed)
    n = 9; pts = [(x0, y0)]
    for i in range(1, n):
        k = i / n
        pts.append((lerp(x0, x1, k) + (55 if i % 2 else -55) + rng.uniform(-15, 15), lerp(y0, y1, k)))
    pts.append((x1, y1))
    def fn(d, P, s):
        d.line([P(*p) for p in pts], fill=INK_T, width=int((w + 22) * s))
        d.line([P(*p) for p in pts], fill=BOLT_Y, width=int((w + 8) * s))
        d.line([P(*p) for p in pts], fill=(255, 255, 235), width=int(w * 0.5 * s))
        br = [pts[4], (pts[4][0] + 70, pts[4][1] + 60), (pts[4][0] + 95, pts[4][1] + 140)]
        d.line([P(*p) for p in br], fill=INK_T, width=int(16 * s)); d.line([P(*p) for p in br], fill=BOLT_Y, width=int(7 * s))
    aa(img, (min(x0, x1) - 80, y0 - 10, max(x0, x1) + 80, y1 + 10), fn, a)

def sun(img, cx, cy, r, T, a=1.0, rays=True, face=False):
    """Sol vectorial grande (los discos grandes, por código: sin dientes)"""
    def fn(d, P, s):
        if rays:
            for i in range(12):
                ang = T * 0.35 + i * math.tau / 12
                c, sn = math.cos(ang), math.sin(ang)
                r0, r1, wdt = r * 1.12, r * 1.36, 0.10
                p = [(cx + r0 * math.cos(ang - wdt), cy + r0 * math.sin(ang - wdt)), (cx + r1 * c, cy + r1 * sn),
                     (cx + r0 * math.cos(ang + wdt), cy + r0 * math.sin(ang + wdt))]
                d.polygon([P(*q) for q in p], fill=SUN_A, outline=INK_T, width=int(7 * s))
        d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=SUN_B, outline=INK_T, width=int(9 * s))
        d.ellipse([P(cx - r * 0.84, cy - r * 0.86), P(cx + r * 0.8, cy + r * 0.78)], fill=SUN_A)
        d.arc([P(cx - r * 0.62, cy - r * 0.64), P(cx + r * 0.5, cy + r * 0.5)], 200, 250, fill=(255, 236, 150), width=int(12 * s))
    m = r * 1.45
    aa(img, (cx - m, cy - m, cx + m, cy + m), fn, a)

def thermo(img, cx, top, h, f, col, a=1.0, plate=False):
    """termómetro vectorial; f = llenado 0..1"""
    w = h * 0.16; br = w * 1.05
    def fn(d, P, s):
        if plate:
            d.rounded_rectangle([P(cx - br * 1.6, top - 26), P(cx + br * 1.6, top + h + br * 1.4)], radius=int(40 * s), fill=(236, 226, 196), outline=INK_T, width=int(6 * s))
        d.rounded_rectangle([P(cx - w / 2, top), P(cx + w / 2, top + h)], radius=int(w / 2 * s), fill=(250, 248, 240), outline=INK_T, width=int(8 * s))
        d.ellipse([P(cx - br, top + h - br * 0.6), P(cx + br, top + h + br * 1.4)], fill=col, outline=INK_T, width=int(8 * s))
        fy = top + h - (h - w * 0.6) * clamp(f)
        d.rounded_rectangle([P(cx - w * 0.26, fy), P(cx + w * 0.26, top + h + br * 0.2)], radius=int(w * 0.26 * s), fill=col)
        for k in range(1, 6):
            y = top + h * k / 6.5
            d.line([P(cx + w / 2 - 4, y), P(cx + w / 2 + 18, y)], fill=INK_T, width=int(5 * s))
    aa(img, (cx - br * 1.7, top - 30, cx + br * 1.7, top + h + br * 1.5), fn, a)

def bar(img, x, base, w, h, col, a=1.0):
    def fn(d, P, s):
        if h > 2: d.rounded_rectangle([P(x - w / 2, base - h), P(x + w / 2, base)], radius=int(14 * s), fill=col, outline=INK_T, width=int(7 * s))
    aa(img, (x - w / 2 - 10, base - max(h, 4) - 10, x + w / 2 + 10, base + 10), fn, a)

def scoreboard(img, cy, l, r, a=1.0, k=1.0):
    """marcador: rayo  l – r  Sol. k anima el último cambio (pop)"""
    if a <= 0.01: return
    def fn(d, P, s):
        d.rounded_rectangle([P(230, cy - 70), P(850, cy + 70)], radius=int(70 * s), fill=(250, 244, 226), outline=INK_T, width=int(8 * s))
    aa(img, (220, cy - 80, 860, cy + 80), fn, a)
    bolt(img, 320, cy, 120, a)
    sun(img, 760, cy, 42, 0, a)
    R.txt(img, f"{l}  –  {r}", cy - 52, "title", INK_T, a, x=540, rise=False)

ROUND_COL = [(70, 90, 170), (190, 110, 40)]
def split_bg(img, T, t):
    """pantalla partida del versus: izquierda tormenta (rayo), derecha cálida (Sol)"""
    ST.sky(img, (34, 40, 74), (64, 70, 110), 0, H)
    warm = Image.new("RGBA", (W // 2, H), (0, 0, 0, 0))
    ST.sky(warm, (168, 84, 40), (226, 140, 60), 0, H)
    img.alpha_composite(warm, (W // 2, 0))
    d = ImageDraw.Draw(img)
    d.line([(W // 2, 640), (W // 2, 1390)], fill=INK_T, width=8)

# =====================================================================  ESCENAS
HOOK_BOLT = (330, 980, 390)
HOOK_SUN = (680, 1040, 150)
def hook_art(img, T, a=1.0, settle=0.0, Tref=None):
    """dibujo de la portada: el rayo parpadea junto al Sol (algo se mueve desde 0 s). En el puente `Tref` alinea la
    animación para que el ÚLTIMO fotograma sea idéntico al primero"""
    Tr = T if Tref is None else Tref
    x, y, h = HOOK_BOLT
    sx, sy, sr = HOOK_SUN
    bob = 5 * math.sin(Tr * 2.4)
    glow(img, sx, sy, sr * 1.1, (255, 190, 80), a * 0.8)
    sun(img, sx, sy + bob * 0.5, sr * (1 + 0.04 * eo(Tr / 0.4)), Tr, a=a)
    fl = 0.55 + 0.45 * abs(math.sin(Tr * 5.0))
    glow(img, x, y, h * 0.42, (255, 250, 180), a * fl)
    bolt(img, x, y - bob, h * (1 + 0.04 * eo(Tr / 0.4)), a=a, rot=8)

@V.scene("hook")
def _(img, T, t, s, e):
    hook_art(img, T)
    cover_mod.draw_header(img, CATEGORY)
    cover_mod.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "hotter?"), "tap", 0.7)])

@V.scene("rounds")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k1 = eo((T - s) / 0.4)
    bolt(img, lerp(120, 290, k1), 1030, 330, a, rot=6)
    sun(img, lerp(960, 790, k1), 1040, 120, T, a)
    tr = wt("Round", s)
    for i in range(3):
        kd = clamp((T - s - 0.25 - 0.18 * i) / 0.25)
        def dot(d, P, s_, i=i, kd=kd):
            cx = 440 + i * 100; rr = 30 * eo(kd)
            col = YELLOW if (T >= tr and i == 0) else (250, 248, 240)
            if rr > 1: d.ellipse([P(cx - rr, 1250 - rr), P(cx + rr, 1250 + rr)], fill=col, outline=INK_T, width=int(6 * s_))
        aa(img, (390, 1200, 690, 1300), dot, a)
    R.txt(img, "VS", 980, "number", YELLOW, a * clamp((T - s - 0.2) / 0.3), x=540, rise=False)
    R.chrome(img, T)
    R.txt(img, "3 rounds", TITLE_Y, "title", B.TEXT, win(T, s, tr - 0.05))
    R.txt(img, "Round 1: Heat", TITLE_Y, "title", YELLOW, a * clamp((T - tr) / 0.25))
    return R.punch(img, T, tr, amt=0.04)
V.backdrop("rounds")(split_bg)
V.sounds("rounds", [(0.05, "whoosh", 0.6), (0.3, "tap", 0.5), (0.5, "tap", 0.5), (rel("rounds", "Round"), "pop", 0.8)])

@V.scene("heat")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tl = s + 0.05
    item(img, LI, "storm_cloud", 360, 860, 200, a=a)          # 227x140 → ×1,43
    ks = clamp((T - tl) / 0.12)
    fl = 1.0 if (T - tl) % 1.6 < 0.9 else 0.35
    glow(img, 320, 1120, 150, (255, 250, 200), a * ks * fl * 0.7)
    if ks > 0: bolt(img, 330, 1110, 440, a * ks * (0.6 + 0.4 * fl), rot=4)
    tf = wt("fifty", s)
    f = 0.15 + 0.82 * eio((T - wt("heat", s)) / max(0.4, tf - wt("heat", s) + 0.6))
    thermo(img, 700, 830, 400, f, RED, a, plate=True)
    lab(img, "~50,000°F", 760, YELLOW, a * on(T, "fifty", s, e, need=2.2), x=640)
    R.chrome(img, T)
    title(img, T, s, e, "Lightning")
    return R.punch(img, T, tl, amt=0.05)
V.backdrop("heat")(lambda img, T, t: ST.landscape(img, T, sky_kind="storm", terrain="hills", seed=3))
V.sounds("heat", [(0.0, "whoosh", 0.8), (rel("heat", "fifty"), "pop", 0.8)])

@V.scene("surf")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    sun(img, lerp(260, 330, k), 1060, 230, T * 0.3, a, rays=False)
    lab(img, "Visible surface", 760, INK_T, a * on(T, "visible", s, e, need=2.4), x=360)
    thermo(img, 760, 880, 360, 0.28 * eio((T - s) / 1.0), (240, 150, 40), a)
    lab(img, "~10,000°F", 1300, RED_T, a * on(T, "About", s, e, need=1.8), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "The Sun")
V.backdrop("surf")(lambda img, T, t: ST.card(img, CARD))
V.sounds("surf", [(0.05, "whoosh", 0.6), (rel("surf", "ten"), "click", 0.8)])

@V.scene("five")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = 0.35 + 0.65 * eio((T - s - 0.1) / 1.4)
    base = 1300
    tp = wt("Point,", s)
    ab = a * (1 - clamp((T - tp + 0.05) / 0.25))          # en «Point» las barras dejan sitio al marcador
    bar(img, 360, base, 190, 500 * k, BOLT_Y, ab)
    bar(img, 720, base, 190, 100 * k, SUN_B, ab)
    bolt(img, 360, base - 500 * k - 90, 130, ab)
    sun(img, 720, base - 100 * k - 80, 50, T, ab)
    lab(img, "5x hotter", 900, YELLOW, a * on(T, "runs", s, e, need=2.0) * (1 if T < tp - 0.1 else 0), x=620)
    kp = clamp((T - tp + 0.05) / 0.25)
    R.chrome(img, T)
    title(img, T, s, e, "Air vs surface")
    if kp > 0:
        scoreboard(img, 1050, 1, 0, a * kp)
    return R.punch(img, T, tp, amt=0.05)
V.backdrop("five")(lambda img, T, t: (ST.sky(img, (24, 30, 70), (62, 46, 110)), ST.stars(img, T, n=70, seed=4, y1=H)))
V.sounds("five", [(0.05, "whoosh", 0.6), (0.2, "tap", 0.5), (rel("five", "five"), "sparkle", 0.7), (rel("five", "Point,"), "pop", 1.0)])

@V.scene("glass")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tg = wt("glass", s)
    kg = clamp((T - tg + 0.15) / 0.35)
    k = eo((T - s) / 0.5)
    item(img, LW, "beach_strike", 470, lerp(1090, 1060, k), 560, a=a * (1 - kg))     # 454 → ×1,23
    item(img, LI, "fulgurite", 420, lerp(1150, 1060, eo(kg)), 320, a=a * kg, rot=-6)  # 210 → ×1,52
    lab(img, "Sand to glass", 790, YELLOW, a * on(T, "glass", s, e, need=2.0), x=470)
    lab(img, "Fulgurite", 1280, B.TEXT, a * on(T, "called", s, e, need=1.8), x=470)
    R.chrome(img, T)
    title(img, T, s, e, "Hot enough to melt sand")
V.backdrop("glass")(lambda img, T, t: ST.landscape(img, T, sky_kind="storm", terrain="dunes", seed=6))
V.sounds("glass", [(0.05, "whoosh", 0.6), (rel("glass", "sand"), "tap", 0.6), (rel("glass", "glass"), "sparkle", 0.8)])

@V.scene("flash")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, LI, "stopwatch", 330, 1060, 310, a=a, rot=-4 * math.sin(T * 1.5))            # 209 → ×1,44
    tf = wt("flash", s)
    tg = wt("second", s)
    fl = 0.75 + 0.25 * abs(math.sin(T * 9))
    kf = (1 - clamp((T - tg - 0.25) / 0.12)) * clamp((T - s - 0.1) / 0.15)    # el rayo está… y se apaga en «second»
    bolt(img, 700, 1020, 360 * (1 + 0.06 * clamp((T - tf) / 0.1) * (1 - clamp((T - tf - 0.2) / 0.3))), a * kf, rot=6)
    if kf > 0.05: glow(img, 700, 1020, 160, (255, 240, 150), a * kf * fl)
    lab(img, "< 1 second", 1270, RED_T, a * on(T, "over", s, e, need=2.0), x=520)
    R.chrome(img, T)
    R.txt(img, "Round 2: Staying power", TITLE_Y, "title", YELLOW, win(T, s, e) * k)
    return R.punch(img, T, tf, amt=0.05)
V.backdrop("flash")(lambda img, T, t: ST.card(img, CARD))
V.sounds("flash", [(0.05, "whoosh", 0.6), (rel("flash", "flash"), "pop", 0.9), (rel("flash", "less"), "click", 0.7)])

@V.scene("long")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.6)
    sun(img, 330, lerp(1150, 1030, k), 175, T, a)
    item(img, LI, "hourglass_space", 720, 1050, 300, a=a, rot=8 * math.sin(T * 0.8))   # 207 → ×1,45
    tp = wt("Point,", s)
    lab(img, "Billions of years", 1290, YELLOW, a * on(T, "shining", s, e, need=2.0) * (1 if T < tp - 0.1 else 0), x=520)
    kp = clamp((T - tp + 0.05) / 0.25)
    R.chrome(img, T)
    title(img, T, s, e, "The Sun")
    if kp > 0: scoreboard(img, 880, 1, 1, a * kp)
    return R.punch(img, T, tp, amt=0.05)
V.backdrop("long")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="dunes", seed=2))
V.sounds("long", [(0.05, "whoosh", 0.6), (rel("long", "billions"), "sparkle", 0.6), (rel("long", "Point,"), "pop", 1.0)])

WOW_DUR = 1.4
@V.scene("core")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tc = wt("core", s)
    k = eo((T - s) / 0.6)
    kz = eio((T - tc + 0.2) / 1.2)
    item(img, LW, "sun_cutaway", 520, 1060, lerp(500, 600, kz) * (0.92 + 0.08 * k), a=a)   # 441 → ≤×1,36
    tm = wt("million", s)
    lab(img, "Core: 27 million°F", 1300, YELLOW, a * clamp((T - max(tm, tc + WOW_DUR + 0.05)) / 0.25), x=500)
    R.chrome(img, T)
    R.txt(img, "Round 3: Deep inside", TITLE_Y, "title", YELLOW, win(T, s, e) * k)
    return R.punch(img, T, tc, amt=0.05)
def core_bg(img, T, t):
    s = V.sc["core"][0]; tc = wt("core", s)
    ST.sky(img, (10, 12, 34), (30, 22, 60)); ST.stars(img, T, n=90, seed=12, y1=H)
    ST.wow_moment(img, T, tc - 0.05, CATEGORY, "glitch", dur=WOW_DUR, center=(520, 1060))
V.backdrop("core")(core_bg)
V.sounds("core", [(0.05, "whoosh", 0.6), (rel("core", "core") - 0.05, "sparkle", 0.9), (rel("core", "million"), "pop", 0.7)])

@V.scene("touch")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((T - s - 0.05) / 1.0)
    base = 1320
    bar(img, 330, base, 170, 6 + 4 * k, BOLT_Y, a)          # ~50.000 °F frente a 27 millones: a esta escala, casi nada
    bolt(img, 330, base - 90, 120, a)
    bar(img, 690, base, 170, 540 * k, SUN_B, a)
    sun(img, 690, base - 540 * k - 10, 60, T, a * clamp(k * 3 - 2))
    lab(img, "Lightning", 1080, INK_T, a * clamp((T - s - 0.3) / 0.3), x=330)
    tp = wt("Point,", s)
    kp = clamp((T - tp + 0.05) / 0.25)
    R.chrome(img, T)
    title(img, T, s, e, "Not even close")
    if kp > 0: scoreboard(img, 880, 1, 2, a * kp)
    return R.punch(img, T, tp, amt=0.05)
V.backdrop("touch")(lambda img, T, t: ST.card(img, CARD))
V.sounds("touch", [(0.05, "whoosh", 0.6), (0.4, "tap", 0.5), (rel("touch", "Point,"), "pop", 1.0)])

@V.scene("score")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tb = wt("bolt", s)
    k = eo((T - s) / 0.4)
    scoreboard(img, 830, 1, 2, a * k)
    kb = on(T, "bolt", s, e, need=2.6)
    bolt(img, 300, 1130, 260 * (0.9 + 0.1 * eo(kb)), a, rot=6)
    sun(img, 760, 1110, 120, T, a)
    lab(img, "Surface: bolt", 1290, YELLOW, a * kb, x=300)
    lab(img, "Core: Sun", 1290, YELLOW, a * on(T, "not", s, e, need=2.0), x=760)
    R.chrome(img, T)
    R.txt(img, "Sun wins 2–1", TITLE_Y, "title", YELLOW, a * clamp((T - wt("two", s)) / 0.3))
    return R.punch(img, T, wt("Sun.", s), amt=0.05)
V.backdrop("score")(split_bg)
V.sounds("score", [(0.05, "whoosh", 0.6), (rel("score", "Sun."), "pop", 1.0), (rel("score", "heart."), "tap", 0.7)])

@V.scene("take")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.6)
    sun(img, 800, lerp(860, 820, k), 95, T, a)
    def beam(d, P, s_):
        d.polygon([P(760, 880), P(860, 880), P(560, 1330), P(300, 1330)], fill=(255, 236, 150, 90))
    aa(img, (290, 860, 880, 1340), beam, a * k)
    R.chrome(img, T)
    title(img, T, s, e, "Nap spot: sunbeam")
V.backdrop("take")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="hills", seed=8))
V.sounds("take", [(0.05, "whoosh", 0.5), (rel("take", "sunbeam."), "sparkle", 0.5)])

@V.scene("bridge")
def _(img, T, t, s, e):
    end = V.outro_at
    Tl = V.last_t
    # la animación del gancho corre «hacia atrás» desde el último fotograma: en Tl vale exactamente lo mismo que en T=0
    hook_art(img, T, a=clamp((T - s) / B.ENTER), Tref=T - Tl)
    cover_mod.draw_header(img, CATEGORY)
    ka = clamp((T - (end - 0.7)) / 0.55)
    if ka > 0: cover_mod.draw_title(img, LINE1, LINE2, SUB, a=ka)
    return R.punch(img, max(0.0, V.last_t - T), 0.0, dur=0.3, amt=0.06)
V.sounds("bridge", [(0.05, "whoosh", 0.6)])

V.backdrop("hook")(lambda img, T, t: cover_mod.draw_bg(img, CATEGORY, 0.05 * T))
V.hook_like = {"hook", "bridge"}

def bridge_bg(img, T, t):
    """rayos de la portada: al final del bucle quedan en el mismo ángulo que en T=0"""
    cover_mod.draw_bg(img, CATEGORY, 0.05 * (T - V.last_t))
V.backdrop("bridge")(bridge_bg)

if __name__ == "__main__":
    V.main()
