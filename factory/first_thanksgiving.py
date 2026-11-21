"""Reel: Pop quiz: what was NOT at the first Thanksgiving? Mr. Whiskerfact, categoría History, formato quiz.
Reel temático (Thanksgiving US, 26/11/2026). Tanda B2-length, rol `base`, longitud `standard`. Bucle (loop=True).
Estilo v4 (gato hablando): first_thanksgiving_v4.py.

Fuentes (dos por dato): ver voice/first_thanksgiving_claims.md
- Cinco ciervos, ~90 hombres, tres días, cuatro hombres «fowling»: carta de Winslow (Plimoth Patuxet, Pilgrim Hall); Smithsonian; MA Commonwealth Museum
- Sin mantequilla ni harina de trigo, probablemente sin horno, poco azúcar: Smithsonian; History.com; Mental Floss; FamilySearch
- Pavo incierto: Smithsonian; History.com; Mental Floss
- «First Thanksgiving» lo bautiza Alexander Young en 1841: Plimoth; Smithsonian
- Mejillones y anguilas probables: Smithsonian; Mental Floss

Nada de harvest_feast_1621 (lleva un pavo asado y salsa de arándanos en la mesa: contradiría el guion).
Sprites de la biblioteca (thanksgiving_items, large_thanksgiving, pilgrim_man, wampanoag_man) a ≤1,5x;
tarjetas de opciones, reloj, soles, aspas, contador y sello por código.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
import cover as cover_mod
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

SLUG = "first_thanksgiving"
CATEGORY = "history"
R = Reel(CATEGORY)
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "Pop"), ("opts", "A"), ("optc", "C"), ("reveal", "Ready"), ("picture", "Picture"), ("arrive", "The"),
    ("together", "Together"), ("deer", "Deer"), ("birds", "Birds"), ("turkey", "Turkey"), ("why", "Why"),
    ("sugar", "Sugar"), ("pumpkins", "Pumpkins"), ("footnote", "Footnote"), ("letter", "Almost"), ("bonus", "Bonus"),
    ("bridge", "So")], loop=True)
_rd = next(st for w, st, en in V.words if w == "Ready?")      # el corte optc/revelación va justo antes de «Ready?»: el reloj corre en el silencio
V.sc["optc"] = (V.sc["optc"][0], _rd - 0.12); V.sc["reveal"] = (_rd - 0.12, V.sc["reveal"][1])
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano (pies en el suelo, filas fijas)
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
GOLD = (246, 196, 84)
YELLOW = (255, 222, 90)
CARD = (56, 742, 1024, 1384)
TI, LT = "thanksgiving_items", "large_thanksgiving"
PIL_M, WAM = "pilgrim_man", "wampanoag_man"
LINE1, LINE2, SUB = "1621", "Menu", "What was NOT there?"
GY = 1388          # pies de lo que está de pie, dentro del suelo oscuro (horizonte en 1330)
CAT = False        # first_thanksgiving_v4.py lo pone a True

def wt(word, s): return V.word_time(word, after=s)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))
def on(T, word, s, e, need=2.0, lead=0.1): return clamp((T - min(wt(word, s), e - need) + lead) / 0.3)
def until(T, word, s, e, need=2.0):
    tw = min(wt(word, s), e - need) - 0.1
    return 1 - clamp((T - (tw - 0.2)) / 0.15)

def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def item(img, lib, name, x, y, h, a=1.0, anchor="center", flip=False, rot=0.0, squash=(1.0, 1.0)):
    LIB.place(img, lib, name, x, y, height=h, a=a, anchor=anchor, flip=flip, rot=rot, squash=squash)

def badge(img, letter, x, y, a, col=GOLD, r=46):
    def fn(d, P, s): d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=col, outline=INK_T, width=int(5 * s))
    aa(img, (x - r - 4, y - r - 4, x + r + 4, y + r + 4), fn, a)
    if a > 0.003: R.put_text(img, R.sprite(letter, "label", INK_T), x, y + 2, a, "mm", text=letter)

_stamp_cache = {}
def stamp(img, text, cx, cy, k, a=1.0, col=RED_T):
    """sello a tamaño final en la capa de etiquetas, inclinación pequeña (6°), entra con golpe"""
    if a <= 0.003 or k <= 0: return
    if text not in _stamp_cache:
        f = cover_mod._font("Black", 88)
        tw = int(ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(text, font=f))
        lay = Image.new("RGBA", (tw + 120, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([14, 14, tw + 106, 206], radius=26, outline=col, width=14, fill=(255, 250, 240, 235))
        d.text(((tw + 120) / 2, 112), text, font=f, fill=col, anchor="mm")
        _stamp_cache[text] = lay.rotate(-6, resample=Image.BICUBIC, expand=True)
    spr = _stamp_cache[text]
    sc = 1 + 0.35 * (1 - eo(k))
    if sc > 1.001: spr = spr.resize((int(spr.width * sc), int(spr.height * sc)), Image.LANCZOS)
    R.put_text(img, spr, cx, cy, a * clamp(k * 3), "mm", text=text)

def cross(img, x, y, r, k, a=1.0):
    """aspa roja que se dibuja en dos trazos"""
    if k <= 0: return
    def fn(d, P, s):
        k1, k2 = clamp(k * 2), clamp(k * 2 - 1)
        d.line([P(x - r, y - r), P(x - r + 2 * r * k1, y - r + 2 * r * k1)], fill=RED_T, width=int(16 * s))
        if k2 > 0: d.line([P(x + r, y - r), P(x + r - 2 * r * k2, y - r + 2 * r * k2)], fill=RED_T, width=int(16 * s))
    aa(img, (x - r - 12, y - r - 12, x + r + 12, y + r + 12), fn, a)

def clock(img, x, y, r, frac, a=1.0):
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

def sun(img, x, y, r, lit, a=1.0):
    def fn(d, P, s):
        col = (255, 200, 70) if lit > 0.5 else (120, 110, 130)
        for k in range(8):
            an = k / 8 * 2 * math.pi
            d.line([P(x + math.cos(an) * r * 1.2, y + math.sin(an) * r * 1.2), P(x + math.cos(an) * r * 1.6, y + math.sin(an) * r * 1.6)], fill=col, width=int(8 * s))
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=col, outline=INK_T, width=int(5 * s))
    rr = r * (1 + 0.15 * (1 - eo(lit)) * (lit > 0))
    aa(img, (x - r * 1.8, y - r * 1.8, x + r * 1.8, y + r * 1.8), fn, a)

def paw(img, x, y, r, a=1.0):
    def fn(d, P, s):
        d.ellipse([P(x - r, y - r * 0.6), P(x + r, y + r * 0.9)], fill=RED_T)
        for dx, dy in ((-0.95, -0.95), (-0.32, -1.35), (0.32, -1.35), (0.95, -0.95)):
            d.ellipse([P(x + dx * r - r * 0.32, y + dy * r - r * 0.32), P(x + dx * r + r * 0.32, y + dy * r + r * 0.32)], fill=RED_T)
    aa(img, (x - r * 1.5, y - r * 1.9, x + r * 1.5, y + r), fn, a)

def walker(img, name, x, base, h, T, moving, flip=False, a=1.0, still="front"):
    """paseo a 8 dibujos/s mientras se mueve; si no, pose quieta"""
    pose = f"walk{int(T * 8) % 4 + 1}" if moving else still
    LIB.place(img, name, pose, x, base, height=h, a=a, flip=flip)

# =====================================================================  ESCENAS
HOOK_ITEMS = [("deer", 225, 1030, 300, 0.0), ("duck", 750, 1080, 230, 1.7), ("pumpkin_pie", 505, 990, 220, 3.1)]
def hook_art(img, T, a=1.0, settle=0.0):
    """dibujo de la portada: las tres opciones grandes. En T=0 y al final del puente (settle=1) están en reposo exacto"""
    for name, x, y, h, ph in HOOK_ITEMS:
        bob = 8 * (math.sin(T * 2.6 + ph) - math.sin(ph)) * (1 - settle)
        grow = 1 + 0.05 * eo(T / 0.35) * (1 - settle) if name == "pumpkin_pie" else 1.0     # la tarta «late» en los primeros 0,3 s
        item(img, TI, name, x, y + bob, h * grow, a=a)

@V.scene("hook")
def _(img, T, t, s, e):
    hook_art(img, T)
    cover_mod.draw_header(img, CATEGORY)
    cover_mod.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))
    if not CAT: R.hook_mascot(img, T, 0.0, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "NOT"), "tap", 0.7)])

ROWS = [("A", "Deer", "deer", 880), ("B", "Wildfowl", "duck", 1075), ("C", "Pumpkin pie", "pumpkin_pie", 1265)]
def option_row(img, i, a, T=0.0, dim=1.0):
    L, text, name, y = ROWS[i]
    if a <= 0.003: return
    dx = 40 * (1 - eo(a))
    badge(img, L, 130 + dx, y + 4 * math.sin(T * 2.6 + i * 1.3), a * dim)
    item(img, TI, name, 330 + dx, y, 150, a * dim)
    lab(img, text, y - 28, INK_T, a * dim, x=640 + dx)

@V.scene("opts")
def _(img, T, t, s, e):
    a = win(T, s, e + 1)
    option_row(img, 0, a * clamp((T - s - 0.05) / 0.35), T=T)
    option_row(img, 1, a * clamp((T - wt("B", s) + 0.1) / 0.35), T=T)
    R.chrome(img, T)
    title(img, T, s, e + 1, "Pop quiz!")
V.sounds("opts", [(0.05, "pop", 0.7), (rel("opts", "B"), "pop", 0.7)])

@V.scene("optc")
def _(img, T, t, s, e):
    option_row(img, 0, 1.0, T=T); option_row(img, 1, 1.0, T=T)
    option_row(img, 2, clamp((T - s - 0.05) / 0.35), T=T)
    tc = wt("Comment", s)
    t_tick = wt("you", s) + 0.25
    frac = clamp(math.floor(max(0.0, T - t_tick) * 5) / 5 / 1.6)
    clock(img, 540, 655, 52, frac, clamp((T - tc + 0.2) / 0.3))
    R.chrome(img, T)
    R.txt(img, "Comment your answer!", TITLE_Y, "title", B.TEXT, win(T, tc - 0.2, e))
V.sounds("optc", [(0.05, "pop", 0.7)] + [(rel("optc", "you") + 0.25 + 0.5 * k, "click", 0.8) for k in range(3)])

WOW_DUR = 1.3
@V.scene("reveal")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tc = wt("C", s)
    k = eo((T - s) / 0.4)
    item(img, TI, "pumpkin_pie", 500, lerp(1150, 1110, k), 280, a=a)
    stamp(img, "NOT THERE", 500, 960, clamp((T - tc - 0.05) / 0.25), a)
    R.chrome(img, T)
    title(img, T, s, e, "It's C!")
    return R.punch(img, T, tc + 0.1, amt=0.06)
def reveal_bg(img, T, t):
    s = V.sc["reveal"][0]
    ST.landscape(img, T, sky_kind="sunset", terrain="autumn", seed=1)
    ST.wow_moment(img, T, V.word_time("C", after=s) - 0.05, CATEGORY, "swirl", dur=WOW_DUR, center=(500, 1100))
V.backdrop("reveal")(reveal_bg)
V.sounds("reveal", [(0.05, "whoosh", 0.7), (rel("reveal", "C") - 0.05, "sparkle", 0.9), (rel("reveal", "C") + 0.1, "pop", 1.0)])

@V.scene("picture")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    item(img, LT, "plymouth_1621", 480, 1095, lerp(430, 470, k), a=a)
    lab(img, "Autumn 1621", 785, INK_T, a * on(T, "autumn", s, e, need=1.8), x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Plymouth, 1621")
V.sounds("picture", [(0.05, "whoosh", 0.6), (rel("picture", "autumn"), "tap", 0.6)])

@V.scene("arrive")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tw = wt("Wampanoag", s) - 0.2
    kw = clamp((T - tw) / 1.0)                       # entra andando 1 s (8 dibujos/s)
    xw = lerp(960, 660, kw)
    pp = "wave" if T >= tw + 1.1 else "front"
    LIB.place(img, PIL_M, pp, 280, GY, height=350, a=a)
    if T >= tw: walker(img, WAM, xw, GY, 345, T, kw < 1.0, flip=True, a=a, still="three_quarter_left")
    lab(img, "Colonists", 970, B.TEXT, a * on(T, "Plymouth", s, e, need=4.0), x=270)
    lab(img, "~90 men", 970, YELLOW, a * on(T, "ninety", s, e, need=2.0), x=660)
    R.chrome(img, T)
    title(img, T, s, e, "Massasoit arrives")
V.backdrop("arrive")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="autumn", seed=3))
V.sounds("arrive", [(0.05, "whoosh", 0.6), (rel("arrive", "Wampanoag") - 0.2, "tap", 0.5), (rel("arrive", "ninety"), "pop", 0.7)])

@V.scene("together")
def _(img, T, t, s, e):
    a = win(T, s, e)
    td = wt("three", s)
    item(img, TI, "cooking_pot", 540, 1335, 260, a=a, anchor="bottom")
    item(img, TI, "corn_ears", 270, 1335, 170, a=a, anchor="bottom")
    item(img, TI, "pumpkin", 790, 1335, 170, a=a, anchor="bottom")
    for i in range(3):
        lit = clamp((T - (td - 0.3 + 0.3 * i)) / 0.2)
        sun(img, 360 + 180 * i, 820, 38, lit, a)
    lab(img, "3 days", 905, YELLOW, a * on(T, "three", s, e, need=2.0), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "A harvest feast")
V.backdrop("together")(lambda img, T, t: ST.landscape(img, T, night=True, terrain="forest", seed=4))
V.sounds("together", [(0.05, "whoosh", 0.6)] + [(rel("together", "three") - 0.3 + 0.3 * i, "pop", 0.5) for i in range(3)])

@V.scene("deer")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tf = wt("five", s)
    LIB.place(img, WAM, "offer" if T >= wt("brought", s) else "front", 250, GY, height=345, a=a)
    kb = clamp((T - (tf - 0.3)) / 0.3)
    LIB.place(img, TI, "deer", 640, GY - 6, height=310, a=a * clamp((T - s - 0.05) / 0.3) * (1 - kb))
    for i in range(5):
        k = clamp((T - (tf - 0.1 + 0.15 * i)) / 0.25)
        LIB.place(img, TI, "deer", 480 + 90 * i, GY - 6 - (i % 2) * 40, height=170, a=a * k, squash=(1.0, 0.94 + 0.06 * eo(k)))
    lab(img, "5 deer", 785, YELLOW, a * on(T, "five", s, e, need=2.0), x=670)
    lab(img, "Gifts", 900, B.TEXT, a * on(T, "gifts", s, e, need=2.0), x=670)
    R.chrome(img, T)
    title(img, T, s, e, "A: real!")
V.backdrop("deer")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="pines", seed=5))
V.sounds("deer", [(0.05, "whoosh", 0.6), (rel("deer", "Real"), "tap", 0.6)] + [(rel("deer", "five") - 0.1 + 0.15 * i, "pop", 0.4) for i in range(5)])

@V.scene("birds")
def _(img, T, t, s, e):
    a = win(T, s, e)
    LIB.place(img, PIL_M, "point_side" if T >= wt("Four", s) else "front", 230, GY, height=350, a=a)
    for i, (x, h) in enumerate(((510, 180), (680, 160), (825, 140))):
        k = clamp((T - (s + 0.15 + 0.2 * i)) / 0.3)
        bob = 5 * math.sin(T * 2.2 + i * 1.4)
        LIB.place(img, TI, "duck", x, 1340 + bob, height=h, a=a * k, flip=i % 2 == 1)
    lab(img, "Wildfowl", 800, YELLOW, a * on(T, "Real", s, e, need=2.0), x=640)
    lab(img, "Ducks? Geese?", 880, B.TEXT, a * on(T, "probably", s, e, need=2.0), x=640)
    R.chrome(img, T)
    title(img, T, s, e, "B: real too!")
V.backdrop("birds")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="waves", seed=6))
V.sounds("birds", [(0.05, "whoosh", 0.6), (0.2, "pop", 0.4), (rel("birds", "fowling"), "tap", 0.6), (rel("birds", "probably"), "pop", 0.5)])

@V.scene("turkey")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, TI, "wild_turkey", 440, 1345, lerp(270, 295, k), a=a, anchor="bottom")
    q = R.sprite("?", "number", RED_T)
    R.put_text(img, q, 740, 930 + 8 * math.sin(T * 3), a * clamp((T - s - 0.2) / 0.3), "mm", text="?")
    lab(img, "Not sure", 830, B.TEXT, a * on(T, "Historians", s, e), x=440)
    R.chrome(img, T)
    title(img, T, s, e, "Turkey?")
V.sounds("turkey", [(0.05, "whoosh", 0.6), (0.2, "pop", 0.6), (rel("turkey", "Historians"), "tap", 0.5)])

@V.scene("why")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rows = [("No butter", "butter", 860), ("No wheat flour", "wheat", 1010), ("No oven?", "oven", 1160)]
    for text, w, y in rows:
        k = on(T, w, s, e, need=2.0)
        cross(img, 130, y + 28, 30, clamp((T - min(wt(w, s), e - 1.6) + 0.1) / 0.4), a)
        lab(img, text, y, INK_T, a * k, x=370)
    ko = clamp((T - wt("oven", s)) / 0.6)
    item(img, TI, "pumpkin_pie", 720, 1250, 200, a=a * (1 - 0.6 * ko))
    cross(img, 720, 1250, 90, ko, a)
    R.chrome(img, T)
    title(img, T, s, e, "Why no pie?")
V.sounds("why", [(0.05, "whoosh", 0.6), (rel("why", "butter"), "click", 0.7), (rel("why", "wheat"), "click", 0.7), (rel("why", "oven"), "pop", 0.8)])

@V.scene("sugar")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((T - s - 0.2) / 1.4)
    item(img, TI, "sugar_loaf", 500, 1300, 280, a=a, anchor="bottom", squash=(1.0, 1.0 - 0.45 * k))
    lab(img, "Sugar low?", 800, YELLOW, a * clamp((T - s - 0.05) / 0.3), x=500)
    R.chrome(img, T)
    title(img, T, s, e, "Sugar?")
V.backdrop("sugar")(lambda img, T, t: (ST.sky(img, (40, 26, 60), (110, 50, 70)), ST.stars(img, T, n=50, seed=8, y1=H)))
V.sounds("sugar", [(0.05, "whoosh", 0.6), (0.3, "bubble", 0.5)])

@V.scene("pumpkins")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    LIB.place(img, TI, "pumpkin", 360, GY - 40, height=lerp(220, 250, k), a=a)
    LIB.place(img, TI, "pumpkin", 620, GY - 40, height=170, a=a * clamp((T - s - 0.3) / 0.3), flip=True)
    kc = clamp((T - wt("crust", s) + 0.2) / 0.3)
    item(img, TI, "pumpkin_pie", 770, 1000, 170, a=a * kc)
    cross(img, 770, 1000, 70, clamp((T - wt("crust", s)) / 0.4), a)
    lab(img, "On the menu", 800, YELLOW, a * clamp((T - s - 0.1) / 0.3) * until(T, "crust", s, e, need=2.0), x=460)
    lab(img, "Not in a crust", 800, YELLOW, a * on(T, "crust", s, e), x=460)
    R.chrome(img, T)
    title(img, T, s, e, "Pumpkins? Yes")
V.backdrop("pumpkins")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="hills", seed=7))
V.sounds("pumpkins", [(0.05, "whoosh", 0.6), (0.3, "pop", 0.5), (rel("pumpkins", "crust"), "click", 0.7)])

@V.scene("footnote")
def _(img, T, t, s, e):
    a = win(T, s, e)
    paw(img, 150, 840, 30, a)
    lab(img, "Not \"Thanksgiving\"", 810, INK_T, a * on(T, "call", s, e, need=3.0), x=540)
    tc = min(wt("centuries", s) - 0.2, e - 2.0)
    n1 = R.sprite("1621", "number", INK_T)
    R.put_text(img, n1, 300, 1060, a * clamp((T - s - 0.1) / 0.3), "mm", text="1621")
    k2 = clamp((T - tc) / 0.3)
    def arrow(d, P, s_):
        x1 = lerp(450, 600, eo(k2))
        d.line([P(450, 1060), P(x1, 1060)], fill=RED_T, width=int(12 * s_))
        if k2 > 0.6: d.polygon([P(x1 + 30, 1060), P(x1 - 6, 1036), P(x1 - 6, 1084)], fill=RED_T)
    aa(img, (430, 1020, 650, 1100), arrow, a * clamp(k2 * 2))
    n2 = R.sprite("1841", "number", RED_T)
    R.put_text(img, n2, 770, 1060, a * k2, "mm", text="1841")
    lab(img, "Named in 1841", 1240, INK_T, a * k2, x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Footnote")
V.sounds("footnote", [(0.05, "tap", 0.5), (0.3, "pop", 0.5)] + [(rel("footnote", "centuries") - 0.2, "sparkle", 0.7)])

@V.scene("letter")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    item(img, TI, "old_letter", 450, lerp(1110, 1060, k), 300, a=a, rot=2.0 * math.sin(T * 1.1))
    LIB.place(img, "cat_eye_night_items", "candle", 740, 1320, height=240, a=a * clamp((T - s - 0.3) / 0.3))
    lab(img, "1 eyewitness letter", 790, YELLOW, a * on(T, "eyewitness", s, e, need=2.6), x=470)
    lab(img, "Edward Winslow", 1260, B.TEXT, a * on(T, "Winslow", s, e, need=2.0), x=470)
    R.chrome(img, T)
    title(img, T, s, e, "How we know")
V.backdrop("letter")(lambda img, T, t: ST.landscape(img, T, night=True, terrain="pines", seed=9))
V.sounds("letter", [(0.05, "whoosh", 0.6), (rel("letter", "eyewitness"), "pop", 0.6), (rel("letter", "Winslow"), "tap", 0.6)])

@V.scene("bonus")
def _(img, T, t, s, e):
    a = win(T, s, e)
    km = on(T, "mussels", s, e, need=2.0)
    ke = on(T, "eels", s, e, need=2.0)
    k0 = clamp((T - s - 0.1) / 0.35)
    LIB.place(img, TI, "mussels", 520, 1250, height=lerp(170, 220, eo(km)), a=a * k0)
    LIB.place(img, TI, "eel", 790 - 30 * eo(ke), 1150 + 6 * math.sin(T * 2.5), height=200, a=a * ke, rot=3 * math.sin(T * 2.0))
    lab(img, "Mussels?", 830, YELLOW, a * km, x=470)
    lab(img, "Eels?", 830, YELLOW, a * ke, x=760)
    R.chrome(img, T)
    title(img, T, s, e, "Bonus!")
V.backdrop("bonus")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="waves", seed=10))
V.sounds("bonus", [(0.05, "whoosh", 0.6), (rel("bonus", "mussels"), "pop", 0.6), (rel("bonus", "eels"), "bubble", 0.6)])

@V.scene("bridge")
def _(img, T, t, s, e):
    end = V.outro_at
    tg = wt("give", s) - 0.5
    kt = clamp((T - s) / B.ENTER) * (1 - clamp((T - tg) / 0.4))
    item(img, LT, "modern_table", 580, 985, 420, a=kt)
    kh = clamp((T - tg) / 0.4)
    if kh > 0: hook_art(img, T, a=kh, settle=clamp((T - (end - 0.9)) / 0.7))
    cover_mod.draw_header(img, CATEGORY)
    ka = clamp((T - (end - 0.7)) / 0.55)
    if ka > 0: cover_mod.draw_title(img, LINE1, LINE2, SUB, a=ka)
    return R.punch(img, max(0.0, V.last_t - T), 0.0, dur=0.3, amt=0.06)
V.sounds("bridge", [(0.05, "whoosh", 0.6), (rel("bridge", "pie"), "tap", 0.5)])

# ---------- fondos ----------
def card_bg(img, T, t): ST.card(img, CARD)
V.backdrop("hook")(lambda img, T, t: cover_mod.draw_bg(img, CATEGORY, 0.05 * T))
V.hook_like = {"hook", "bridge"}
def bridge_bg(img, T, t):
    P = math.tau / 14; Tl = V.last_t; s0 = V.sc["bridge"][0]
    m = int(0.05 * (Tl - s0) / P)
    cover_mod.draw_bg(img, CATEGORY, 0.05 * (T - Tl) + m * P)
V.backdrop("bridge")(bridge_bg)
V.backdrop("turkey")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="autumn", seed=11))
for n in ("opts", "optc", "picture", "why", "footnote"):
    V.backdrop(n)(card_bg)

if __name__ == "__main__":
    V.main()
