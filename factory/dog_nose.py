"""Reel: What if you had a dog's nose for one day? Mr. Whiskerfact, categoría Nature, formato what_if.
Voz de Brad. Tanda B2-length, rol `base`, longitud `standard` (control). Bucle (loop=True).
Guion visual: growth/storyboards/2026-11-26_dog_nose.md (hoja nose_w48 + young_man, dog, wifi_objects).
Fuentes (dos por dato): ver voice/dog_nose_claims.md (NOVA/PBS, EarthDate, Horowitz, AKC, NPR, ScienceDaily, Nature).
Estelas de olor, vapor, barras, flechas y partículas por código (vectorial); sprites de la biblioteca a ≤1,5x.
"""
import math
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
import cover as cover_mod
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

SLUG = "dog_nose"
CATEGORY = "nature"
R = Reel(CATEGORY)
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "What"), ("plate", "You'd"), ("layers", "eggs"), ("receptors", "Scientists"), ("sugar", "One"),
    ("street", "Then"), ("cutaway", "With"), ("trail", "Footprints"), ("time", "One"), ("brain", "Relative"),
    ("news", "So"), ("twist", "Now"), ("study", "In"), ("bridge", "So")], loop=True)
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
YELLOW = (255, 222, 90)
SCENT = (255, 236, 160)
BLUE_AIR = (120, 190, 255)
CARD = (56, 742, 1024, 1384)
NW = "nose_w48"
LINE1, LINE2, SUB = "Dog nose", "for a day?", "What would you smell?"

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

# ---------- efectos de código ----------
def scent(img, p0, p1, phase, a=1.0, n=9, amp=26, waves=1.5, col=SCENT, r=11, grow=1.0):
    """estela de olor: puntos que viajan de p0 a p1 por una onda. grow recorta la estela (0..1)"""
    if a <= 0.01 or grow <= 0.01: return
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = []
    for i in range(n):
        u = (i / n + phase) % 1.0
        if u > grow: continue
        off = amp * math.sin(u * math.tau * waves)
        rr = r * (0.55 + 0.45 * math.sin(math.pi * u))
        pts.append((p0[0] + dx * u + nx * off, p0[1] + dy * u + ny * off, rr))
    x0 = min(p0[0], p1[0]) - amp - 20; x1 = max(p0[0], p1[0]) + amp + 20
    y0 = min(p0[1], p1[1]) - amp - 20; y1 = max(p0[1], p1[1]) + amp + 20
    def fn(d, P, s):
        for x, y, rr in pts:
            d.ellipse([P(x - rr, y - rr), P(x + rr, y + rr)], fill=col, outline=INK_T, width=int(4 * s))
    aa(img, (x0, y0, x1, y1), fn, a)

def steam(img, x, y_bot, h, T, a=1.0, seed=0):
    """vapor en espiral que sube (rizos)"""
    pts = []
    for i in range(7):
        u = (i / 7 + T * 0.35 + seed * 0.13) % 1.0
        pts.append((x + 30 * math.sin(u * math.tau * 1.3 + seed), y_bot - h * u, 14 * (1 - u) + 5, u))
    def fn(d, P, s):
        for px, py, rr, u in pts:
            d.ellipse([P(px - rr, py - rr), P(px + rr, py + rr)], fill=(250, 248, 240), outline=INK_T, width=int(4 * s))
    aa(img, (x - 60, y_bot - h - 30, x + 60, y_bot + 30), fn, a)

def bar(img, x0, y, w, h, col, a=1.0):
    def fn(d, P, s):
        if w > 2: d.rounded_rectangle([P(x0, y), P(x0 + w, y + h)], radius=int(h / 2 * s), fill=col, outline=INK_T, width=int(6 * s))
    aa(img, (x0 - 10, y - 10, x0 + max(w, 4) + 10, y + h + 10), fn, a)

def arrow(img, x0, x1, y, k, a=1.0, col=YELLOW):
    """flecha que se dibuja de x0 hacia x1"""
    if k <= 0.01: return
    xe = lerp(x0, x1, k); sg = 1 if x1 > x0 else -1
    def fn(d, P, s):
        d.line([P(x0, y), P(xe, y)], fill=INK_T, width=int(26 * s))
        d.line([P(x0, y), P(xe, y)], fill=col, width=int(12 * s))
        tip = [P(xe + sg * 34, y), P(xe - sg * 8, y - 34), P(xe - sg * 8, y + 34)]
        d.polygon(tip, fill=col, outline=INK_T, width=int(6 * s))
    aa(img, (min(x0, x1) - 60, y - 60, max(x0, x1) + 60, y + 60), fn, a)

def dots_trail(img, pts, k, a=1.0, col=(120, 72, 40)):
    """rastro punteado que aparece hasta la fracción k"""
    m = int(len(pts) * clamp(k))
    if m <= 0: return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    def fn(d, P, s):
        for x, y in pts[:m]:
            d.ellipse([P(x - 9, y - 9), P(x + 9, y + 9)], fill=col, outline=INK_T, width=int(3 * s))
    aa(img, (min(xs) - 20, min(ys) - 20, max(xs) + 20, max(ys) + 20), fn, a)

# =====================================================================  ESCENAS
HOOK_MAN = (560, 1310, 440)              # cx, base, alto (sprite 251x455 → ×0,97)
NOSE = (630, 1082)                       # punta de la nariz en el gancho
TRAILS = [((880, 860), 0.00), ((885, 1040), 0.33), ((870, 1230), 0.66)]
def hook_art(img, T, a=1.0, Tref=None):
    """portada: el joven con nariz de perro olfatea; tres estelas de olor viajan hacia la nariz (se mueven desde 0 s).
    En el puente `Tref` alinea la animación para que el ÚLTIMO fotograma sea idéntico al primero"""
    Tr = T if Tref is None else Tref
    x, base, h = HOOK_MAN
    bob = 6 * math.sin(Tr * 2.4)
    for (p0, ph) in TRAILS:
        scent(img, p0, (NOSE[0] + 30, NOSE[1] + bob), (ph + Tr * 0.45) % 1.0, a, n=7, amp=22)
    item(img, NW, "man_dog_nose", x, base + bob, h, a=a, anchor="bottom")

@V.scene("hook")
def _(img, T, t, s, e):
    hook_art(img, T)
    cover_mod.draw_header(img, CATEGORY)
    cover_mod.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "nose"), "sparkle", 0.6)])

@V.scene("plate")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.45)
    sq = 1 + 0.03 * math.sin(clamp((T - s - 0.3) / 0.4) * math.pi)     # rebote suave al entrar
    item(img, NW, "breakfast_plate", 470, lerp(1440, 1340, k), 470 * sq, a=a, anchor="bottom")
    for i, x in enumerate((360, 470, 580)):
        steam(img, x, 900, 150, T, a * clamp((T - s - 0.4 - 0.2 * i) / 0.3), seed=i)
    R.chrome(img, T)
    title(img, T, s, e, "Breakfast = a story")
V.backdrop("plate")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="hills", seed=4))
V.sounds("plate", [(0.05, "whoosh", 0.6), (0.35, "pop", 0.6), (rel("plate", "story"), "sparkle", 0.5)])

LAYER_ITEMS = [("fried_eggs", 240, 900, "eggs"), ("bacon", 705, 900, "bacon"), ("toast", 240, 1235, "toast"), ("coffee_mug", 705, 1235, "coffee")]
@V.scene("layers")
def _(img, T, t, s, e):
    a = win(T, s, e)
    item(img, NW, "breakfast_plate", 472, 1068, 230, a=a)
    for name, x, y, w in LAYER_ITEMS:
        tw = wt(w, s) - 0.08
        k = clamp((T - tw) / 0.3)
        if k <= 0: continue
        scent(img, (472, 1070), (x, y), (T * 0.5) % 1.0, a * k, n=6, amp=14, waves=1, grow=eo(k))
        item(img, NW, name, x, y, 225 * (0.85 + 0.15 * eo(k)), a=a * k)
    R.chrome(img, T)
    title(img, T, s, e, "Layers, not one smell")
V.backdrop("layers")(lambda img, T, t: ST.card(img, CARD))
V.sounds("layers", [(rel("layers", w) - 0.05, "pop", 0.7) for _, _, _, w in LAYER_ITEMS])

@V.scene("receptors")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, "dog", "curious", lerp(110, 200, k), 1045, 300, a=a, anchor="bottom")
    tm = wt("three", s)
    kb = eio((T - tm + 0.1) / 1.0)
    bar(img, 370, 900, 480 * kb, 70, YELLOW, a)
    lab(img, "Up to 300 million", 800, YELLOW, a * on(T, "three", s, e, need=4.0), x=590)
    ty = wt("You", s)
    ky = clamp((T - ty + 0.1) / 0.3)
    item(img, "young_man", "think", 200, 1365, 300, a=a * ky, anchor="bottom")
    bar(img, 370, 1215, 12 * eo(ky), 70, (250, 248, 240), a * ky)
    lab(img, "About 6 million", 1222, B.TEXT, a * on(T, "six", s, e, need=2.2), x=600)
    R.chrome(img, T)
    title(img, T, s, e, "Smell receptors")
    return R.punch(img, T, tm, amt=0.04)
V.backdrop("receptors")(lambda img, T, t: (ST.sky(img, (70, 48, 120), (36, 26, 74)), ST.stars(img, T, n=40, seed=9, y1=740)))
V.sounds("receptors", [(0.05, "whoosh", 0.6), (rel("receptors", "three"), "pop", 0.8), (rel("receptors", "You"), "tap", 0.6)])

@V.scene("sugar")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.45)
    tsp = wt("teaspoon", s)
    item(img, NW, "sugar_spoon", 450, lerp(790, 860, k), 230, a=a, rot=-4 + 4 * eio((T - tsp) / 0.6))
    lab(img, "1 teaspoon", 760, B.TEXT, a * on(T, "teaspoon", s, e, need=2.2), x=800)
    tg = tsp + 0.4                                   # un granito cae de la cuchara al agua
    kg = clamp((T - tg) / 0.7)
    if 0 < kg < 1:
        gy = lerp(910, 1090, kg * kg)
        def grain(d, P, s_): d.ellipse([P(268, gy - 9), P(286, gy + 9)], fill=(255, 255, 255), outline=INK_T, width=int(4 * s_))
        aa(img, (250, gy - 20, 300, gy + 20), grain, a)
    for i, (x, w) in enumerate(((262, "two"), (640, "Olympic"))):
        kp = clamp((T - wt(w, s) + 0.05) / 0.3)
        item(img, NW, "swimming_pool", x, 1150 + 20 * (1 - eo(kp)), 285, a=a * kp)
    lab(img, "2 Olympic pools", 1310, YELLOW, a * on(T, "pools", s, e, need=2.3), x=460)
    R.chrome(img, T)
    title(img, T, s, e, "A sugar test")
V.backdrop("sugar")(lambda img, T, t: ST.sky(img, (176, 222, 246), (92, 156, 214)))
V.sounds("sugar", [(0.05, "whoosh", 0.6), (rel("sugar", "teaspoon") + 0.4, "tap", 0.7), (rel("sugar", "two"), "pop", 0.7), (rel("sugar", "Olympic"), "pop", 0.7)])

@V.scene("street")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sc = 520 / 307
    step = LIB.stride("young_man", scale=sc)
    dt = max(0.0, T - s)
    x = 170 + 110 * min(dt, 3.6)          # avance lento (el joven no llega a la farola ni a la etiqueta)
    pose = LIB.cycle("young_man", "walk", T, fps=8)
    tl = wt("street", s)
    kl = clamp((T - tl + 0.1) / 0.35)
    item(img, NW, "lamp_post", 760, 1330, 380, a=a * kl, anchor="bottom")
    if kl > 0:
        scent(img, (740, 1010), (x + 40, 905), (T * 0.6) % 1.0, a * kl, n=7, amp=18)
    LIB.place(img, "young_man", pose, x, 1335, scale=sc, a=a, xanchor="head")
    lab(img, "Smell map", 770, YELLOW, a * on(T, "map", s, e, need=2.2), x=790)
    R.chrome(img, T)
    title(img, T, s, e, "Outside")
V.backdrop("street")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="city", seed=5))
V.sounds("street", [(0.05, "whoosh", 0.6), (rel("street", "street") - 0.05, "pop", 0.6), (rel("street", "map."), "sparkle", 0.6)])

CUT = (480, 1060, 500)                   # nose_cutaway 412x401 → ×1,25
@V.scene("cutaway")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, h = CUT
    k = eo((T - s) / 0.4)
    item(img, NW, "nose_cutaway", cx, cy + 20 * (1 - k), h, a=a)
    left, top = cx - 257, cy - 250
    tip = (left + 0.97 * 514, top + 0.60 * 500)
    smell = (left + 0.45 * 514, top + 0.36 * 500)
    lung = (left + 0.30 * 514, top + 0.97 * 500)
    ts = wt("sniff", s)
    ka = clamp((T - ts) / 0.3)
    if ka > 0:
        scent(img, tip, lung, (T * 0.7) % 1.0, a * ka, n=8, amp=10, waves=0.5, col=BLUE_AIR, r=9)
        t12 = wt("twelve", s)
        scent(img, tip, smell, (T * 0.7 + 0.5) % 1.0, a * clamp((T - t12 + 0.1) / 0.3), n=4, amp=16, waves=0.7, col=YELLOW, r=12)
    lab(img, "12% to smell", 770, RED_T, a * on(T, "twelve", s, e, need=2.5), x=430)
    lab(img, "The rest: lungs", 1300, INK_T, a * on(T, "special", s, e, need=1.8), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Inside the snout")
    return R.punch(img, T, wt("twelve", s), amt=0.04)
V.backdrop("cutaway")(lambda img, T, t: ST.card(img, CARD))
V.sounds("cutaway", [(0.05, "whoosh", 0.6), (rel("cutaway", "sniff,"), "whoosh", 0.5), (rel("cutaway", "twelve"), "pop", 0.8)])

@V.scene("trail")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((T - s) / 2.4)
    item(img, NW, "shoe_prints", 250, 1240, 340, a=a * clamp((T - s - 0.1) / 0.3), rot=90)
    item(img, NW, "dog_sniffing", lerp(680, 630, k), 1335, 360, a=a, anchor="bottom")
    tw = wt("way", s)
    arrow(img, 520, 130, 1050, eo((T - tw + 0.1) / 0.5), a)
    lab(img, "This way", 930, YELLOW, a * on(T, "way", s, e, need=2.0), x=330)
    R.chrome(img, T)
    title(img, T, s, e, "Which way?")
V.backdrop("trail")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="pines", seed=2))
V.sounds("trail", [(0.05, "whoosh", 0.6), (rel("trail", "way"), "tap", 0.8)])

@V.scene("time")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, NW, "shoe_prints", 255, 965, 280, a=a * k, rot=90)
    to = wt("old", s)
    ko = clamp((T - to + 0.1) / 0.3)
    item(img, NW, "shoe_prints", 690, 965, 280, a=a * max(k * 0.25, 0.28 * ko) if T >= to - 0.1 else a * k * 0.25, rot=90)
    tt = wt("time:", s)
    kc = clamp((T - tt + 0.15) / 0.3)
    def hands(d, P, s_, T=T):
        cx, cy = 472, 830
        for L, sp in ((34, 2.0), (24, 0.5)):
            ang = (T - tt) * sp * math.tau - math.pi / 2
            d.line([P(cx, cy), P(cx + L * math.cos(ang), cy + L * math.sin(ang))], fill=INK_T, width=int(7 * s_))
    item(img, "wifi_objects", "clock", 472, 830, 120, a=a * kc)
    aa(img, (420, 780, 525, 880), hands, a * kc)
    look_old = T >= to
    item(img, "dog", "sit", 472, 1365, 300, a=a, anchor="bottom", flip=not look_old)
    lab(img, "Fresh", 1090, RED_T, a * on(T, "fresh", s, e, need=2.2), x=255)
    lab(img, "Old", 1090, INK_T, a * ko, x=690)
    R.chrome(img, T)
    title(img, T, s, e, "Smelling time?")
V.backdrop("time")(lambda img, T, t: ST.card(img, CARD))
V.sounds("time", [(0.05, "whoosh", 0.6), (rel("time", "time:"), "tap", 0.7), (rel("time", "old"), "pop", 0.6), (rel("time", "fresh"), "pop", 0.7)])

@V.scene("brain")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    tf = wt("forty", s)
    pulse = 1 + 0.05 * math.sin(clamp((T - tf) / 0.5) * math.pi)
    item(img, NW, "brain_compare", 470, 1070, 300 * (0.92 + 0.08 * k) * pulse, a=a)
    lab(img, "Dog", 1250, B.TEXT, a * clamp((T - s - 0.3) / 0.3), x=262)
    lab(img, "Human", 1250, B.TEXT, a * clamp((T - s - 0.5) / 0.3), x=545)
    R.txt(img, "40x bigger", 790, "number", YELLOW, a * on(T, "forty", s, e, need=2.0), x=470, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Relative to brain size")
    return R.punch(img, T, tf, amt=0.05)
V.backdrop("brain")(lambda img, T, t: (ST.sky(img, (18, 24, 58), (44, 30, 80)), ST.stars(img, T, n=80, seed=14, y1=H)))
V.sounds("brain", [(0.05, "whoosh", 0.6), (rel("brain", "forty"), "pop", 0.9)])

@V.scene("news")
def _(img, T, t, s, e):
    a = win(T, s, e)
    item(img, NW, "lamp_post", 130, 1330, 420, a=a, anchor="bottom")
    item(img, NW, "dog_sniffing", 355, 1335, 340, a=a, anchor="bottom", rot=1.2 * math.sin(T * 3.0))
    tn = wt("news.", s)
    kn = eo((T - tn + 0.3) / 0.45)
    item(img, NW, "newspaper", lerp(1000, 700, kn), 925, 330, a=a * clamp(kn * 2), rot=lerp(-12, -4, kn))
    lab(img, "Let them sniff", 790, YELLOW, a * on(T, "Let", s, e, need=2.2), x=330)
    R.chrome(img, T)
    title(img, T, s, e, "The daily news")
V.backdrop("news")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="autumn", seed=7))
V.sounds("news", [(0.05, "whoosh", 0.6), (rel("news", "news.") - 0.2, "whoosh", 0.7), (rel("news", "sniff."), "tap", 0.6)])

WOW_DUR = 1.5
@V.scene("twist")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, "young_man", "shrug", 660, 1345, 540 * (0.96 + 0.04 * k), a=a, anchor="bottom")
    R.chrome(img, T)
    title(img, T, s, e, "Plot twist", color=YELLOW)
    return R.punch(img, T, wt("twist:", s), amt=0.05)
def twist_bg(img, T, t):
    s = V.sc["twist"][0]
    ST.sky(img, (128, 58, 92), (70, 30, 56))
    ST.wow_moment(img, T, s + 0.05, CATEGORY, "blobs", dur=WOW_DUR, center=(660, 1060))
V.backdrop("twist")(twist_bg)
V.sounds("twist", [(0.05, "sparkle", 0.9), (rel("twist", "humans"), "tap", 0.5)])

@V.scene("study")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((T - s - 0.2) / 4.5)
    tc = wt("chocolate", s)
    kc = clamp((T - tc + 0.1) / 0.3)
    dots_trail(img, [(640 + 14 * i, 1305 - 4 * math.sin(i)) for i in range(4)], kc, a)
    item(img, NW, "chocolate_bar", 785, 1325, 200, a=a * kc, anchor="bottom", rot=8)
    item(img, NW, "human_crawl_trail", lerp(340, 390, k), 1340, 400, a=a, anchor="bottom",
         rot=1.0 * math.sin(T * 2.2))
    tb = wt("blindfolded", s)
    lab(img, "Blindfolded", 830, B.TEXT, a * on(T, "blindfolded", s, e, need=2.0) * (1 if T < wt("Two", s) - 0.5 else 0), x=380)
    tt = wt("Two", s)
    R.txt(img, "2 out of 3", 765, "number", YELLOW, a * clamp((T - tt + 0.45) / 0.25), x=470, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Humans on all fours")
    return R.punch(img, T, tt, amt=0.05)
V.backdrop("study")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="forest", seed=9))
V.sounds("study", [(0.05, "whoosh", 0.6), (rel("study", "chocolate"), "pop", 0.7), (rel("study", "Two"), "sparkle", 0.9)])

@V.scene("bridge")
def _(img, T, t, s, e):
    end = V.outro_at
    Tl = V.last_t
    tcof = wt("coffee.", s)
    km = clamp((T - tcof + 0.1) / 0.3) * clamp((wt("better", s) - T) / 0.3)      # la taza aparece en «coffee» y se va
    if km > 0:
        item(img, NW, "coffee_mug", 270, 940, 150, a=km)
        steam(img, 270, 860, 120, T, km)
    hook_art(img, T, a=clamp((T - s) / B.ENTER), Tref=T - Tl)
    cover_mod.draw_header(img, CATEGORY)
    ka = clamp((T - (end - 0.7)) / 0.55)
    if ka > 0: cover_mod.draw_title(img, LINE1, LINE2, SUB, a=ka)
    return R.punch(img, max(0.0, V.last_t - T), 0.0, dur=0.3, amt=0.06)
V.sounds("bridge", [(0.05, "whoosh", 0.6), (rel("bridge", "coffee."), "pop", 0.6)])

V.backdrop("hook")(lambda img, T, t: cover_mod.draw_bg(img, CATEGORY, 0.05 * T))
V.hook_like = {"hook", "bridge"}

def bridge_bg(img, T, t):
    """rayos de la portada: al final del bucle quedan en el mismo ángulo que en T=0"""
    cover_mod.draw_bg(img, CATEGORY, 0.05 * (T - V.last_t))
V.backdrop("bridge")(bridge_bg)

if __name__ == "__main__":
    V.main()
