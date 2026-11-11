"""Reel: Pop quiz: when did the last woolly mammoths die out? Mr. Whiskerfact, categoría History, formato quiz.
Voz de Brad. Experimento B1-hook-style, opción `statement` (variante). Estilo v4: mammoth_quiz_v4.py.

Fuentes (dos por dato): ver voice/mammoth_quiz_claims.md
- La mayoría de los mamuts desaparecen al acabar la última glaciación (>10.000 años): Live Science; National Geographic
- El mar aísla la isla de Wrangel (frente a Siberia): Live Science; EarthSky; Sci.News
- <10 fundadores, unos cientos, ~6.000 años: Stockholm Univ. (Cell 2024); National Geographic; EarthSky
- Gran Pirámide de Keops ~2560 a. C. (~4.500 años): National Geographic; World History Encyclopedia
- Últimos mamuts ~4.000 años: Stockholm Univ.; National Geographic; Live Science
- Causa desconocida, final súbito, endogamia; quizá enfermedad o malos años: Stockholm Univ.; Advanced Science News; NatGeo
- Imperio romano 27 a. C.: Britannica; World History Encyclopedia

Lo geométrico (tarjetas de opciones, reloj, mar que sube, ADN, gérmenes) por código; personajes y objetos de la
biblioteca (woolly_mammoth, mammoth_quiz_items, ancient_person) sin ampliar más de ~1,5x.
La voz lleva 1,7 s de silencio insertado tras «tell you.» para el reloj del quiz (2 s de cuenta atrás con el corte).
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import brand as B
import reel_lib as RLX
import style as ST
import library as LIB
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

R = Reel("history")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "mammoth_quiz", [
    ("hook", "The"), ("opts", "Option"), ("optc", "C"), ("reveal", "Ready"), ("most", "Most"), ("rising", "But"),
    ("dna", "Ancient"), ("grew", "It"), ("egypt", "Meanwhile"), ("still", "Still"), ("why", "Why"),
    ("maybe", "Maybe"), ("rome", "And"), ("wrap", "Picture")])
_rd = next(st for w, st, en in V.words if w == "Ready?")            # el corte optc/revelación va justo antes de «Ready?»:
V.sc["optc"] = (V.sc["optc"][0], _rd - 0.12); V.sc["reveal"] = (_rd - 0.12, V.sc["reveal"][1])   # el reloj corre en todo el silencio
V._fits = {"opts": None, "optc": None}     # las filas de opciones no se reencuadran: no saltan entre escenas
for _n in ("reveal", "most", "egypt", "still", "rome", "wrap"): V._fits[_n] = None   # escenas con los pies en el suelo (y=1330): el reencuadre las centraba y flotaban
V.FIT_MAX = 1.1            # los sprites de la biblioteca no se amplían más de ~1,5x en total

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (30, 74, 130)
MAM, IT = "woolly_mammoth", "mammoth_quiz_items"
GOLD = (246, 196, 84)
SEA, SEA_D = (70, 140, 200), (40, 96, 160)
LAND, LAND_D, SNOW = (150, 160, 110), (110, 120, 80), (244, 248, 250)
CAT = False        # mammoth_quiz_v4.py lo pone a True: el gato v4 habla en gancho, revelación y cierre
CARD = (56, 742, 1024, 1384)
GY = 1388          # pies de lo que está de pie: DENTRO del suelo oscuro (el horizonte está en 1330); en 1330 parecían flotar

def wt(word, s): return V.word_time(word, after=s)
def early(word, s, e, need=1.9): return min(wt(word, s), e - need)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))
def on(T, word, s, e, need=1.9, lead=0.1): return clamp((T - early(word, s, e, need) + lead) / 0.3)

def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def sprite(img, pose, x, y, h, a=1.0, anchor="bottom", name=MAM, flip=False, squash=(1.0, 1.0)):
    LIB.place(img, name, pose, x, y, height=h, a=a, anchor=anchor, flip=flip, squash=squash)

def badge(img, letter, x, y, a, col=GOLD, r=46):
    def fn(d, P, s): d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=col, outline=INK_T, width=int(5 * s))
    aa(img, (x - r - 4, y - r - 4, x + r + 4, y + r + 4), fn, a)
    if a > 0.003: R.put_text(img, R.sprite(letter, "label", INK_T), x, y + 2, a, "mm", text=letter)

def stamp(img, text, x, y, k, col=RED_T):
    """sello que cae, dibujado a su tamaño final, inclinación pequeña"""
    if k <= 0: return
    spr = R.sprite(text, "number", col); w, h = spr.size
    box = Image.new("RGBA", (w + 70, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle([4, 4, w + 66, h + 40], radius=22, fill=(246, 238, 214, 255), outline=col + (255,), width=12)
    box.alpha_composite(spr, (35, 20))
    box = box.rotate(-6, resample=Image.BICUBIC, expand=True)
    R.put_text(img, box, x, y - 70 * (1 - eo(k)), clamp(k * 3), "mm", text=text)

def snow(img, T, a=1.0, n=46, seed=4, y0=740, y1=1370, x1=900):
    """copos que caen (algo se mueve desde el fotograma 0)"""
    if a <= 0.003: return
    rng = np.random.default_rng(seed); xs = rng.uniform(80, x1, n); ph = rng.uniform(0, 1, n); sp = rng.uniform(0.10, 0.18, n); rr = rng.uniform(4, 8, n)
    def fn(d, P, s):
        for x, p, v, r in zip(xs, ph, sp, rr):
            u = (p + T * v) % 1.0
            yy = y0 + 15 + (y1 - y0 - 30) * u; xx = x + 14 * math.sin(T * 1.3 + p * 9)
            d.ellipse([P(xx - r, yy - r), P(xx + r, yy + r)], fill=(255, 255, 255, 220))
    aa(img, (60, y0, x1 + 30, y1), fn, a)

# ---------- opciones (tarjeta) ----------
ROWS = [("A", "Ice Age ends", "glacier", 860), ("B", "After the pyramid", "pyramid", 1060), ("C", "Roman Empire", "colosseum", 1260)]
def option_row(img, i, a, dim=1.0, T=0.0):
    L, text, pose, y = ROWS[i]
    if a <= 0.003: return
    dx = 40 * (1 - eo(a))
    badge(img, L, 128 + dx, y + 4 * math.sin(T * 2.6 + i * 1.3), a * dim)            # las letras laten suave: nunca quieto
    sprite(img, pose, 335 + dx, y, 160, a * dim, anchor="center", name=IT)
    lab(img, text, y - 28, INK_T, a * dim, x=655 + dx)

def clock(img, x, y, r, frac, a=1.0):
    """reloj del quiz por código: aguja que salta cada cuarto de segundo, sector que se va llenando"""
    def fn(d, P, s):
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(250, 246, 232), outline=INK_T, width=int(6 * s))
        if frac > 0.002: d.pieslice([P(x - r * 0.84, y - r * 0.84), P(x + r * 0.84, y + r * 0.84)], -90, -90 + 360 * frac, fill=(240, 150, 120))
        for k in range(12):
            an = k / 12 * 2 * math.pi
            d.line([P(x + math.cos(an) * r * 0.78, y + math.sin(an) * r * 0.78), P(x + math.cos(an) * r * 0.92, y + math.sin(an) * r * 0.92)], fill=INK_T, width=int(4 * s))
        an = -math.pi / 2 + 2 * math.pi * frac
        d.line([P(x, y), P(x + math.cos(an) * r * 0.72, y + math.sin(an) * r * 0.72)], fill=RED_T, width=int(7 * s))
        d.ellipse([P(x - 9, y - 9), P(x + 9, y + 9)], fill=INK_T)
        d.rounded_rectangle([P(x - 16, y - r - 22), P(x + 16, y - r - 4)], radius=5 * s, fill=INK_T)
    aa(img, (x - r - 8, y - r - 30, x + r + 8, y + r + 8), fn, a)

# =====================================================================  ESCENAS
@V.scene("hook")
def _(img, T, t, s, e):
    x = 700 if CAT else CX - 40
    snow(img, T, x1=880)
    pose = "surprised" if t >= 0.3 else "side"            # a los 0,3 s el mamut cambia de cara: algo se mueve enseguida
    sprite(img, pose, x, GY, 300, flip=True)
    R.chrome(img, T)
    V.hook_text(img, T, e, "The last mammoths died shockingly recently.", "Pop quiz: when?", "Pop")
    if not CAT: R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "Pop"), "tap", 0.7)])

@V.scene("opts")
def _(img, T, t, s, e):
    a = win(T, s, e + 1)
    option_row(img, 0, a * clamp((T - s - 0.1) / 0.35), T=T)
    option_row(img, 1, a * clamp((T - wt("B", s) + 0.1) / 0.35), T=T)
    R.chrome(img, T)
    title(img, T, s, e + 1, "Pop quiz!")
V.sounds("opts", [(0.1, "pop", 0.7), (rel("opts", "B"), "pop", 0.7)])

@V.scene("optc")
def _(img, T, t, s, e):
    option_row(img, 0, 1.0, T=T); option_row(img, 1, 1.0, T=T)
    option_row(img, 2, clamp((T - s - 0.05) / 0.35), T=T)
    tc = wt("Comment", s)
    t_tick = wt("you", s) + 0.25                              # el reloj corre en el silencio insertado
    frac = clamp(math.floor(max(0.0, T - t_tick) * 5) / 5 / 1.6)
    clock(img, 540, 655, 52, frac, clamp((T - tc + 0.2) / 0.3))
    R.chrome(img, T)
    R.txt(img, "Comment your answer!", TITLE_Y, "title", B.TEXT, win(T, tc - 0.2, e))
V.sounds("optc", [(0.05, "pop", 0.7)] + [(rel("optc", "you") + 0.25 + 0.5 * k, "click", 0.8) for k in range(3)])

@V.scene("reveal")
def _(img, T, t, s, e):
    a = win(T, s, e)
    x = 720 if CAT else CX
    tb = wt("B", s)
    sprite(img, "pyramid", x, GY, 230, a, name=IT)
    stamp(img, "B", x + 10, 960, clamp((T - tb) / 0.3))
    R.chrome(img, T)
    title(img, T, s, e, "It's B!")
    return R.punch(img, T, tb + 0.05, amt=0.06)
V.sounds("reveal", [(0.05, "whoosh", 0.7), (rel("reveal", "B"), "pop", 1.0), (rel("reveal", "checked"), "tap", 0.5)])

@V.scene("most")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tv = wt("vanish", s)
    herd = [(190, GY, 215, False), (470, GY, 190, False), (790, GY, 225, True)]
    for i, (x, y, h, fl) in enumerate(herd):
        fade = 1 - (0.75 if i == 2 else 1.0) * eio((T - tv - 1.3 * i) / 0.7)   # uno a uno, se van (el último queda como un fantasma)
        sprite(img, "graze" if i == 1 else "side", x + 12 * t, y, h, a * fade, flip=fl)
    lab(img, "Over 10,000 years", 800, B.TEXT, a * on(T, "ten", s, e), x=480)
    lab(img, "A feels right", 960, B.TEXT, a * on(T, "feels", s, e, need=2.1), x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Most vanished early")
V.sounds("most", [(0.1, "whoosh", 0.6), (rel("most", "vanish"), "tap", 0.5), (rel("most", "vanish") + 1.3, "tap", 0.5),
                  (rel("most", "ten"), "pop", 0.6), (rel("most", "feels"), "tap", 0.5)])

@V.scene("rising")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((T - wt("rising", s)) / 2.2)
    sea_y = lerp(1300, 1160, k)
    def fn(d, P, s_):
        mainland = [(90, 1330), (100, 1060), (170, 980), (260, 960), (350, 1030), (420, 1200), (470, 1250), (560, 1250), (600, 1170),
                    (680, 1080), (770, 1070), (850, 1150), (880, 1330)]
        d.polygon([P(x, y) for x, y in mainland], fill=LAND, outline=INK_T, width=int(5 * s_))
        d.polygon([P(x, y) for x, y in [(150, 1010), (190, 975), (260, 962), (300, 990), (230, 1010)]], fill=SNOW)
        d.polygon([P(x, y) for x, y in [(690, 1085), (770, 1072), (810, 1100), (740, 1110)]], fill=SNOW)
        d.rectangle([P(70, sea_y), P(900, 1360)], fill=SEA + (235,))
        for i in range(9):
            wx = 90 + i * 92 + 20 * math.sin(T * 2 + i)
            d.arc([P(wx, sea_y - 12), P(wx + 60, sea_y + 12)], 200, 340, fill=SEA_D, width=int(5 * s_))
    aa(img, (70, 940, 905, 1365), fn, a)
    sprite(img, "side", 230, 990, 85, a)
    sprite(img, "happy", 760, 1085, 95, a, flip=True)
    lab(img, "Siberia", 800, INK_T, a * on(T, "Siberia", s, e, need=2.4), x=250)
    lab(img, "Wrangel Island", 800, RED_T, a * on(T, "Wrangel", s, e, need=3.0), x=690)
    R.chrome(img, T)
    title(img, T, s, e, "Cut off by the sea")
V.sounds("rising", [(0.1, "whoosh", 0.6), (rel("rising", "rising"), "bubble", 0.7), (rel("rising", "Wrangel"), "tap", 0.6), (rel("rising", "trapped"), "pop", 0.6)])

def helix(img, x, y0, y1, T, a=1.0):
    def fn(d, P, s):
        n = 26
        for i in range(n):
            y = lerp(y0, y1, i / (n - 1)); ph = T * 2.4 + i * 0.5
            xa, xb = x + 70 * math.sin(ph), x - 70 * math.sin(ph)
            d.line([P(xa, y), P(xb, y)], fill=(120, 110, 100), width=int(4 * s))
        for sg, col in ((1, (60, 120, 200)), (-1, (220, 90, 80))):
            pts = [P(x + sg * 70 * math.sin(T * 2.4 + i * 0.5), lerp(y0, y1, i / (n - 1))) for i in range(n)]
            d.line(pts, fill=col, width=int(12 * s), joint="curve")
    aa(img, (x - 90, y0 - 10, x + 90, y1 + 10), fn, a)

@V.scene("dna")
def _(img, T, t, s, e):
    a = win(T, s, e)
    helix(img, 210, 830, 1300, T, a)
    tf = wt("fewer", s); tg = wt("group", s)
    for i in range(8):
        cx = 440 + (i % 4) * 120; by = 1060 + (i // 4) * 170
        k = clamp((T - (tg + 0.15 * i)) / 0.25)
        sprite(img, "side", cx, by, 82, a * k, squash=(1.0, 0.94 + 0.06 * eo(k)))
    lab(img, "< 10 founders", 1250, RED_T, a * on(T, "fewer", s, e), x=620)
    R.chrome(img, T)
    title(img, T, s, e, "Ancient DNA")
V.sounds("dna", [(0.1, "whoosh", 0.6), (rel("dna", "group"), "pop", 0.5), (rel("dna", "fewer"), "pop", 0.6), (rel("dna", "animals"), "tap", 0.5)])

@V.scene("grew")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, "hourglass", 190, 1290, 300, a, name=IT)
    th = wt("hundred", s)
    n = int(8 + 32 * eio((T - s - 0.1) / max(0.5, th - s)))
    for i in range(n):
        cx = 390 + (i % 8) * 70; by = 935 + (i // 8) * 72
        sprite(img, "side", cx, by, 46, a)
    lab(img, "a few hundred", 1290, INK_T, a * on(T, "hundred", s, e, need=2.6), x=600)
    lab(img, "~6,000 years", 790, RED_T, a * on(T, "six", s, e), x=600)
    R.chrome(img, T)
    title(img, T, s, e, "Small, but stubborn")
    return R.punch(img, T, wt("six", s))
V.sounds("grew", [(0.1, "whoosh", 0.6), (0.8, "pop", 0.4), (rel("grew", "hundred"), "pop", 0.7), (rel("grew", "six"), "sparkle", 0.6)])

@V.scene("egypt")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tb = wt("built", s)
    kb = eio((T - tb) / 0.5)
    sprite(img, "pyramid_building", 620, GY - 8, 230, a * (1 - kb), name=IT)
    sprite(img, "pyramid", 620, GY - 8, 240, a * kb, name=IT)
    pose = "point" if T >= wt("King", s) else "talk"
    sprite(img, pose, 250, GY, 300, a, name="ancient_person")
    lab(img, "~4,500 years ago", 800, B.TEXT, a * on(T, "four", s, e), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Meanwhile, in Egypt")
V.sounds("egypt", [(0.1, "whoosh", 0.6), (rel("egypt", "King"), "tap", 0.5), (rel("egypt", "built"), "sparkle", 0.7), (rel("egypt", "four"), "pop", 0.6)])

@V.scene("still")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tm = wt("Mammoths", s); td = wt("disappeared", s)
    k = eo((T - tm + 0.2) / 0.4)
    fade = 1 - 0.7 * eio((T - td) / 1.2)
    snow(img, T, a, n=30, seed=9)
    sprite(img, "happy", 470, GY - 30 * (1 - k), 300, a * k * fade, flip=True)
    lab(img, "~4,000 years ago", 800, B.TEXT, a * on(T, "four", s, e), x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Still here!")
    return R.punch(img, T, tm, amt=0.06)
V.sounds("still", [(0.05, "whoosh", 0.8), (rel("still", "Mammoths"), "pop", 0.9), (rel("still", "disappeared"), "whoosh", 0.5), (rel("still", "four"), "tap", 0.5)])

@V.scene("why")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, "mammoth_skeleton", 400, 1300, 330, a, name=IT)
    q = R.sprite("?", "number", RED_T)
    R.put_text(img, q, 760, 900 + 8 * math.sin(T * 3), a * clamp((T - s - 0.2) / 0.3), "mm", text="?")
    lab(img, "inbreeding", 790, INK_T, a * on(T, "inbreeding", s, e), x=360)
    lab(img, "sudden end", 1290, RED_T, a * on(T, "sudden", s, e, need=2.0), x=640)
    R.chrome(img, T)
    title(img, T, s, e, "Cause: unknown")
V.sounds("why", [(0.1, "whoosh", 0.6), (0.2, "pop", 0.6), (rel("why", "inbreeding"), "tap", 0.6), (rel("why", "sudden"), "click", 0.7)])

def germ(img, x, y, r, T, a=1.0, seed=0):
    def fn(d, P, s):
        for k in range(10):
            an = k / 10 * 2 * math.pi + T * 0.6 + seed
            d.line([P(x + math.cos(an) * r * 0.9, y + math.sin(an) * r * 0.9), P(x + math.cos(an) * r * 1.35, y + math.sin(an) * r * 1.35)], fill=(70, 120, 60), width=int(6 * s))
            d.ellipse([P(x + math.cos(an) * r * 1.35 - 7, y + math.sin(an) * r * 1.35 - 7), P(x + math.cos(an) * r * 1.35 + 7, y + math.sin(an) * r * 1.35 + 7)], fill=(70, 120, 60))
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(150, 200, 90), outline=INK_T, width=int(5 * s))
        for dx, dy in ((-0.3, -0.2), (0.25, 0.1), (-0.1, 0.35)):
            d.ellipse([P(x + dx * r - 8, y + dy * r - 8), P(x + dx * r + 8, y + dy * r + 8)], fill=(90, 150, 60))
    aa(img, (x - r * 1.6, y - r * 1.6, x + r * 1.6, y + r * 1.6), fn, a)

@V.scene("maybe")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k1 = clamp((T - s - 0.05) / 0.3)
    for i, (gx, gy, gr) in enumerate(((250, 1010, 70), (170, 1150, 40), (330, 1170, 48))):
        germ(img, gx, gy + 6 * math.sin(T * 2 + i), gr * (0.9 + 0.1 * eo(k1)), T, a * k1, seed=i)
    lab(img, "disease?", 1250, INK_T, a * k1, x=260)
    k2 = clamp((T - wt("bad", s) + 0.3) / 0.3)
    sprite(img, "tundra", 650, 1150, 200, a * k2, name=IT)
    sprite(img, "sad", 650, 1110, 110, a * k2)
    lab(img, "bad years?", 1250, INK_T, a * k2, x=650)
    R.chrome(img, T)
    title(img, T, s, e, "Maybe...")
V.sounds("maybe", [(0.05, "pop", 0.6), (rel("maybe", "bad") - 0.3, "pop", 0.6)])

@V.scene("rome")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, "colosseum", 560, GY - 8, 220, a, name=IT)
    sprite(img, "legionary_gear", 230, GY, 150, a * clamp((T - wt("Roman", s)) / 0.3), name=IT)
    lab(img, "27 BCE", 800, B.TEXT, a * on(T, "Roman", s, e), x=500)
    tl = min(wt("thousand", s), e - 1.95)
    stamp(img, "TOO LATE", 560, 1020, clamp((T - tl) / 0.3))
    R.chrome(img, T)
    title(img, T, s, e, "C? Way too late")
    return R.punch(img, T, tl, amt=0.05)
V.sounds("rome", [(0.1, "whoosh", 0.6), (rel("rome", "Roman"), "tap", 0.6), (min(rel("rome", "thousand"), V.sc["rome"][1] - V.sc["rome"][0] - 1.95), "pop", 1.0)])

@V.scene("wrap")
def _(img, T, t, s, e):
    a = win(T, s, e + 1)
    xp, xm = (835, 650) if CAT else (680, 380)
    sprite(img, "pyramid", xp, GY - 4, 150, a * clamp((T - wt("pyramid", s) + 0.3) / 0.35), name=IT)
    sprite(img, "happy", xm, GY, 180, a * clamp((T - wt("mammoth", s) + 0.3) / 0.35))
    R.chrome(img, T)
    R.txt(img, "Same planet,", TITLE_Y, "title", B.TEXT, win(T, s, V.outro_at + 1))
    R.txt(img, "same time!", TITLE_Y + 97, "title", ACC_T, win(T, s + 0.4, V.outro_at + 1))
    return R.punch(img, T, s + 0.1)
V.sounds("wrap", [(0.05, "whoosh", 0.7), (rel("wrap", "pyramid") - 0.3, "pop", 0.6), (rel("wrap", "mammoth") - 0.3, "pop", 0.6)])

# ---------- fondos ----------
def tundra_night(img, T, t, seed=0): ST.landscape(img, T, night=True, terrain="hills", seed=seed)
def card_bg(img, T, t): ST.card(img, CARD)
def opt_bg(img, T, t): ST.card(img, CARD)
def still_bg(img, T, t):
    ST.landscape(img, T, night=True, terrain="hills", seed=5)
    s0 = V.sc["still"][0]
    ST.wow_moment(img, T, s0 + 0.05, "history", "blobs", dur=max(1.0, min(1.5, V.word_time("Mammoths", after=s0) - s0 - 0.1)))

V.backdrop("hook")(tundra_night)
for n in ("opts", "optc", "rising", "dna", "grew", "why", "maybe"):
    V.backdrop(n)(card_bg)
V.backdrop("reveal")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="dunes", seed=2))
V.backdrop("most")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="hills", seed=3))
V.backdrop("egypt")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="dunes", seed=6))
V.backdrop("still")(still_bg)
V.backdrop("rome")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="hills", seed=7))
V.backdrop("wrap")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="dunes", seed=8))

if __name__ == "__main__":
    V.main()
