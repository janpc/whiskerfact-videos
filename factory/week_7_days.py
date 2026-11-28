"""Reel: Why does a week have seven days? Mr. Whiskerfact, categoría History, formato explainer.
Voz de Brad. Tanda B2-length, rol `base`, longitud `standard` (control). Bucle (loop=True).
Guion visual: growth/storyboards/2026-11-28_week_7_days.md (hoja week_w48 + moon_items, young_man, ancient_person).
Fuentes (dos por dato): voice/week_7_days_claims.md (The Conversation, TheCollector, Time and Date, Live Science,
Merriam-Webster, Almanac, World History Encyclopedia, WebExhibits, France Today, Imperium Romanum, Nundinae).
Números, cruces, barras y flechas por código (vectorial); sprites de la biblioteca a ≤1,5x.
"""
import math
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
import cover as cover_mod
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

SLUG = "week_7_days"
CATEGORY = "history"
R = Reel(CATEGORY)
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "Why"), ("sky", "A"), ("nothing", "But"), ("babylon", "Many"), ("lights", "Its"), ("moon", "Seven"),
    ("jewish", "The"), ("rome", "Rome"), ("both", "For"), ("constantine", "In"), ("names", "The"), ("spanish", "In"),
    ("notall", "Not"), ("france", "In"), ("rest", "People"), ("ended", "The"), ("habit", "So"), ("bridge", "Enjoy")], loop=True)
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
YELLOW = (255, 222, 90)
CARD = (56, 742, 1024, 1384)
WK = "week_w48"
LINE1, LINE2, SUB = "7 days", "a week?", "Why seven, not ten?"

def wt(word, s): return V.word_time(word.strip('"“”,.?!:'), after=s)
def rel(scene, word): return wt(word, V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def num(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "number", col, a, x=x, rise=False)
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
def cross(img, cx, cy, r, k, a=1.0, col=(214, 48, 60)):
    """aspa roja que se dibuja en dos trazos (k 0..1)"""
    if k <= 0.01: return
    k1, k2 = clamp(k * 2), clamp(k * 2 - 1)
    def fn(d, P, s):
        for (x0, y0, x1, y1), kk in (((cx - r, cy - r, cx + r, cy + r), k1), ((cx + r, cy - r, cx - r, cy + r), k2)):
            if kk <= 0: continue
            xe, ye = lerp(x0, x1, kk), lerp(y0, y1, kk)
            d.line([P(x0, y0), P(xe, ye)], fill=INK_T, width=int(38 * s))
            d.line([P(x0, y0), P(xe, ye)], fill=col, width=int(22 * s))
    aa(img, (cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30), fn, a)

def bar4(img, x0, y, w, h, k, a=1.0):
    """barra de 28 días en 4 tramos que se encienden de izquierda a derecha (k 0..4)"""
    def fn(d, P, s):
        seg = w / 4
        for i in range(4):
            fill = YELLOW if k >= i + 0.5 else (250, 246, 232)
            d.rounded_rectangle([P(x0 + i * seg + 6, y), P(x0 + (i + 1) * seg - 6, y + h)], radius=int(14 * s), fill=fill, outline=INK_T, width=int(6 * s))
    aa(img, (x0 - 10, y - 10, x0 + w + 10, y + h + 10), fn, a)

def highlight_col(img, x0, y0, w, h, a=1.0, col=YELLOW):
    """columna resaltada (marco amarillo) sobre un calendario"""
    def fn(d, P, s):
        d.rounded_rectangle([P(x0, y0), P(x0 + w, y0 + h)], radius=int(14 * s), outline=INK_T, width=int(18 * s))
        d.rounded_rectangle([P(x0, y0), P(x0 + w, y0 + h)], radius=int(14 * s), outline=col, width=int(9 * s))
    aa(img, (x0 - 20, y0 - 20, x0 + w + 20, y0 + h + 20), fn, a)

def arrow(img, x0, x1, y, k, a=1.0, col=YELLOW):
    if k <= 0.01: return
    xe = lerp(x0, x1, k); sg = 1 if x1 > x0 else -1
    def fn(d, P, s):
        d.line([P(x0, y), P(xe, y)], fill=INK_T, width=int(18 * s))
        d.line([P(x0, y), P(xe, y)], fill=col, width=int(8 * s))
        d.polygon([P(xe + sg * 22, y), P(xe - sg * 6, y - 22), P(xe - sg * 6, y + 22)], fill=col, outline=INK_T, width=int(5 * s))
    aa(img, (min(x0, x1) - 40, y - 40, max(x0, x1) + 40, y + 40), fn, a)

# =====================================================================  ESCENAS
CAL = (610, 1050, 440)                 # gancho: calendario de 7 columnas (cx, cy, alto; sprite 399x401 → ×1,0)
def hook_art(img, T, a=1.0, Tref=None):
    """portada: el calendario de siete columnas con un «?» que late. `Tref` alinea el puente con el fotograma 0"""
    Tr = T if Tref is None else Tref
    x, y, h = CAL
    bob = 7 * math.sin(Tr * 2.2)
    item(img, WK, "wall_calendar", x, y + bob, h, a=a, rot=1.5 * math.sin(Tr * 1.1))
    q = 1 + 0.06 * math.sin(Tr * 4.0)
    R.txt(img, "?", int(930 - 10 * q), "number", YELLOW, a, x=865, rise=False)

@V.scene("hook")
def _(img, T, t, s, e):
    hook_art(img, T)
    cover_mod.draw_header(img, CATEGORY)
    cover_mod.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "seven"), "sparkle", 0.6)])

SKY_ITEMS = [("moon_items", "sun", 210, "Sun.", "DAY"), ("moon_items", "moon_near", 470, "Moon.", "MONTH"), (WK, "seasons_wheel", 735, "seasons.", "YEAR")]
@V.scene("sky")
def _(img, T, t, s, e):
    a = win(T, s, e)
    for lib, name, x, w, label in SKY_ITEMS:
        tw = min(wt(w, s) - 0.35, e - 2.0)
        k = clamp((T - tw) / 0.35)
        if k <= 0: continue
        sq = 1 + 0.04 * math.sin(clamp((T - tw - 0.2) / 0.4) * math.pi)
        item(img, lib, name, x, lerp(1080, 1010, eo(k)), 250 * sq, a=a * k, rot=6 * math.sin(T * 0.8) if name == "seasons_wheel" else 0)
        lab(img, label, 1170, YELLOW, a * k, x=x)
    R.chrome(img, T)
    title(img, T, s, e, "Sky clocks")
V.backdrop("sky")(lambda img, T, t: ST.sky(img, (122, 196, 240), (60, 120, 196)))
V.sounds("sky", [(rel("sky", w) - 0.35, "pop", 0.7) for _, _, _, w, _ in SKY_ITEMS])

@V.scene("nothing")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, WK, "star_chart", 680, lerp(990, 960, k), 300, a=a * k)
    tq = wt("where", s)
    for i, (x, y0) in enumerate(((560, 900), (640, 860), (720, 920))):
        kq = clamp((T - tq - 0.15 * i) / 0.3)
        if kq <= 0: continue
        R.txt(img, "?", int(y0 - 40 * eo(kq) - 6 * math.sin(T * 3 + i)), "number", YELLOW, a * kq, x=x, rise=False)
    item(img, "young_man", "shrug" if T >= tq - 0.2 else "think", 280, 1365, 580, a=a, anchor="bottom")
    lab(img, "No 7-day cycle", 1215, YELLOW, a * on(T, "seven", s, e, need=2.0), x=690)
    R.chrome(img, T)
    title(img, T, s, e, "So why seven?")
V.backdrop("nothing")(lambda img, T, t: (ST.sky(img, (34, 30, 84), (18, 18, 52)), ST.stars(img, T, n=70, seed=11, y1=H)))
V.sounds("nothing", [(0.05, "whoosh", 0.6), (rel("nothing", "where"), "pop", 0.6)])

@V.scene("babylon")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    item(img, WK, "ziggurat", 420, lerp(1360, 1330, k), 440, a=a, anchor="bottom")
    tb = wt("Babylon", s)
    kt = clamp((T - (s + 0.5)) / 0.35)
    sq = 1 + 0.04 * math.sin(clamp((T - s - 0.7) / 0.4) * math.pi)
    item(img, WK, "clay_tablet", 160, lerp(1400, 1255, eo(kt)), 180 * sq, a=a * kt)
    item(img, "ancient_person", "think", 790, 1350, 470, a=a, anchor="bottom")
    lab(img, "Ancient Babylon", 790, YELLOW, a * on(T, "Babylon", s, e, need=2.1), x=440)
    R.chrome(img, T)
    title(img, T, s, e, "Roots: Babylon")
    return R.punch(img, T, tb, amt=0.04)
V.backdrop("babylon")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="dunes", seed=3))
V.sounds("babylon", [(0.05, "whoosh", 0.6), (0.55, "pop", 0.6), (rel("babylon", "Babylon."), "tap", 0.6)])

LIGHT_FX = [0.068, 0.214, 0.326, 0.447, 0.576, 0.716, 0.898]
ROW = (470, 1060, 860)                  # fila de los siete astros: cx, cy, ancho (sprite 926x125 → ×0,93)
@V.scene("lights")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ts = wt("seven", s) - 0.15
    k1 = clamp((ts + 0.2 - T) / 0.25) if T < ts + 0.2 else 0.0
    if k1 > 0:
        kz = eo((T - s) / 0.5)
        item(img, WK, "babylon_night_sky", 470, 1060, 560 * (0.94 + 0.06 * kz), a=a * k1)
    k2 = clamp((T - ts) / 0.3)
    if k2 > 0:
        cx, cy, w = ROW
        h = w * 125 / 926
        item(img, WK, "seven_lights", cx, cy, h * (0.9 + 0.1 * eo(k2)), a=a * k2)
        t_sun, t_moon, t_five = wt("Sun", s), wt("Moon", s), wt("five", s)
        t_eye = wt("eye", s)
        for i, fx in enumerate(LIGHT_FX):
            if i == 0: ti = t_sun
            elif i == 1: ti = t_moon
            else: ti = min(lerp(t_five, min(t_eye, t_five + 0.8), (i - 2) / 4), e - 2.0)
            kn = clamp((T - ti + 0.1) / 0.25)
            if kn > 0:
                lab(img, str(i + 1), int(cy - h / 2 - 90 - 14 * (1 - eo(kn))), YELLOW, a * kn, x=cx - w / 2 + fx * w)
        lab(img, "Seven moving lights", 1200, YELLOW, a * on(T, "lights", s, e, need=3.0))
    R.chrome(img, T)
    title(img, T, s, e, "Seven lights")
V.backdrop("lights")(lambda img, T, t: (ST.sky(img, (24, 26, 70), (10, 12, 40)), ST.stars(img, T, n=90, seed=5, y1=H)))
V.sounds("lights", [(0.05, "whoosh", 0.6), (rel("lights", "seven") - 0.15, "whoosh", 0.6)] +
         [(rel("lights", w), "tap", 0.6) for w in ("Sun", "Moon", "five")])

PH = (470, 1000, 640)                    # fases: cx, cy, ancho (sprite 436x92 → ×1,47)
@V.scene("moon")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, w = PH
    h = w * 92 / 436
    k = eo((T - s) / 0.4)
    item(img, WK, "moon_phases", cx, cy - 20 * (1 - k), h, a=a)
    tp = wt("phases", s)
    kb = clamp((T - tp + 0.2) / 1.6) * 4
    bar4(img, cx - w / 2, 1140, w, 56, kb, a * clamp((T - tp + 0.4) / 0.3))
    for i in range(3):
        xa = cx - w / 2 + (0.104 + 0.263 * i) * w + 50
        arrow(img, xa, xa + 0.263 * w - 100, cy - h / 2 - 50, eo((T - tp - 0.35 * i) / 0.35), a)
    lab(img, "About 7 days each", 1240, RED_T, a * on(T, "seven", s, e, need=1.8))
    R.chrome(img, T)
    title(img, T, s, e, "Moon phases")
V.backdrop("moon")(lambda img, T, t: ST.card(img, CARD))
V.sounds("moon", [(0.05, "whoosh", 0.6)] + [(rel("moon", "phases") + 0.35 * i, "tap", 0.5) for i in range(3)])

@V.scene("jewish")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.45)
    cx, cy, h = 470, 1090, 500
    item(img, WK, "wall_calendar", cx, cy + 25 * (1 - k), h, a=a)
    tsb = wt("Sabbath", s)
    kh = clamp((T - tsb + 0.1) / 0.3)
    # 7.ª columna del calendario (sprite 399x401: columnas de 0,21 a 0,93 del ancho; filas de 0,23 a 0,93)
    w = h * 399 / 401; x0 = cx - w / 2; y0 = cy - h / 2 + 25 * (1 - k)
    cw = (0.93 - 0.07) * w / 7
    if kh > 0: highlight_col(img, x0 + 0.06 * w + 6 * cw - 6, y0 + 0.29 * h, cw + 8, 0.63 * h, a * kh)
    lab(img, "Sabbath: day 7", 785, YELLOW, a * on(T, "Sabbath", s, e, need=1.8))
    R.chrome(img, T)
    title(img, T, s, e, "The Jewish week")
V.backdrop("jewish")(lambda img, T, t: ST.sky(img, (232, 160, 84), (176, 92, 46)))
V.sounds("jewish", [(0.05, "whoosh", 0.6), (rel("jewish", "Sabbath,"), "pop", 0.7)])

@V.scene("rome")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    sq = 1 + 0.03 * math.sin(clamp((T - s - 0.3) / 0.4) * math.pi)
    item(img, WK, "market_stall", 400, lerp(1420, 1345, k), 540 * sq, a=a, anchor="bottom")
    te = wt("eight-day", s)
    num(img, "8", int(770 - 20 * (1 - eo((T - te) / 0.3))), YELLOW, a * clamp((T - te + 0.1) / 0.25), x=770)
    lab(img, "Market week", 905, YELLOW, a * on(T, "market", s, e, need=1.5), x=730)
    R.chrome(img, T)
    title(img, T, s, e, "Rome: 8 days")
    return R.punch(img, T, te, amt=0.04)
V.backdrop("rome")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="hills", seed=6))
V.sounds("rome", [(0.05, "whoosh", 0.6), (rel("rome", "eight-day"), "pop", 0.8)])

@V.scene("both")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    tw = wt("won", s)
    kw = clamp((T - tw + 0.05) / 0.4)
    item(img, WK, "market_stall", lerp(150, 260, k), 1100, 300, a=a)
    item(img, WK, "wall_calendar", lerp(800, 690, k), 1100, 290 * (1 + 0.08 * eo(kw)), a=a)
    num(img, "8", 770, RED_T, a, x=260)
    num(img, "7", int(770 - 10 * eo(kw)), RED_T, a, x=690)
    lab(img, "Market week", 1275, INK_T, a, x=260)
    lab(img, "Planet week", 1275, INK_T, a, x=690)
    cross(img, 260, 1100, 130, kw, a)
    R.chrome(img, T)
    title(img, T, s, e, "Side by side")
    return R.punch(img, T, tw, amt=0.05)
V.backdrop("both")(lambda img, T, t: ST.card(img, CARD))
V.sounds("both", [(0.05, "whoosh", 0.6), (rel("both", "won."), "pop", 0.9)])

@V.scene("constantine")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.45)
    item(img, WK, "roman_coin", 450, 1125 + 30 * (1 - k), 400, a=a, rot=5 * math.sin((T - s) * 1.6))
    num(img, "321 AD", 765, YELLOW, a * clamp((T - wt("321", s) + 0.1) / 0.3), x=450)
    tsu = wt("Sunday", s)
    ks = clamp((T - tsu + 0.1) / 0.35)
    item(img, "moon_items", "sun", 770, 960 - 20 * (1 - eo(ks)), 160, a=a * ks, rot=10 * T)
    lab(img, "Sunday off", 1345, YELLOW, a * on(T, "Sunday", s, e, need=2.2), x=450)
    R.chrome(img, T)
    title(img, T, s, e, "Constantine")
V.backdrop("constantine")(lambda img, T, t: ST.sky(img, (112, 52, 108), (58, 26, 66)))
V.sounds("constantine", [(0.05, "whoosh", 0.6), (rel("constantine", "321"), "pop", 0.7), (rel("constantine", "Sunday"), "sparkle", 0.6)])

NAME_ITEMS = [(WK, "saturn", 205, 120, "Saturday", "SATURDAY"), ("moon_items", "sun", 470, 190, "Sunday", "SUNDAY"),
              ("moon_items", "moon_near", 735, 190, "Monday", "MONDAY")]
@V.scene("names")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k0 = eo((T - s) / 0.4)
    item(img, WK, "seven_lights", 470, 860 - 20 * (1 - k0), 86, a=a * (1 - 0.5 * clamp((T - wt("Saturday", s) + 0.2) / 0.4)))
    for lib, name, x, h, w, label in NAME_ITEMS:
        tw = min(wt(w, s) - 0.4, e - 2.1)
        k = clamp((T - tw) / 0.3)
        if k <= 0: continue
        item(img, lib, name, x, lerp(1100, 1060, eo(k)), h * 1.2 * (0.9 + 0.1 * eo(k)), a=a * k)
        hot = clamp((T - tw) / 0.2) * clamp((tw + 1.2 - T) / 0.3)
        lab(img, label, 1215, YELLOW if hot > 0.5 else B.TEXT, a * k, x=x)
    R.chrome(img, T)
    title(img, T, s, e, "Names from the sky")
V.backdrop("names")(lambda img, T, t: ST.card(img, CARD))
V.sounds("names", [(rel("names", w) - 0.1, "pop", 0.7) for _, _, _, _, w, _ in NAME_ITEMS])

@V.scene("spanish")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tm, tv = s + 0.6, min(wt("viernes", s), e - 2.2)
    km = eo((T - tm + 0.2) / 0.4); kv = eo((T - tv + 0.2) / 0.4)
    item(img, WK, "mars", lerp(60, 260, km), 1020, 340, a=a * clamp(km * 2), rot=4 * T)
    item(img, WK, "venus", lerp(900, 680, kv), 1020, 340, a=a * clamp(kv * 2), rot=-4 * T)
    lab(img, "Martes: Mars", 1215, YELLOW, a * on(T, "martes", s, e, need=2.5), x=260)
    lab(img, "Viernes: Venus", 1215, YELLOW, a * on(T, "viernes", s, e, need=2.1), x=680)
    R.chrome(img, T)
    title(img, T, s, e, "In Spanish")
V.backdrop("spanish")(lambda img, T, t: (ST.sky(img, (20, 52, 92), (12, 24, 52)), ST.stars(img, T, n=60, seed=21, y1=H)))
V.sounds("spanish", [(rel("spanish", "martes") - 0.2, "whoosh", 0.6), (rel("spanish", "viernes") - 0.2, "whoosh", 0.6)])

WOW_DUR = 1.4
@V.scene("notall")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, "young_man", "surprised", 520, 1350, 500 * (0.96 + 0.04 * k), a=a, anchor="bottom")
    R.chrome(img, T)
    title(img, T, s, e, "Plot twist", color=YELLOW)
    return R.punch(img, T, s + 0.05, amt=0.05)
def notall_bg(img, T, t):
    s = V.sc["notall"][0]
    ST.sky(img, (60, 64, 140), (28, 30, 80))
    ST.wow_moment(img, T, s + 0.05, CATEGORY, "swirl", dur=WOW_DUR, center=(520, 1060))
V.backdrop("notall")(notall_bg)
V.sounds("notall", [(0.05, "sparkle", 0.9)])

@V.scene("france")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, WK, "revolution_calendar", 255, 1090 + 25 * (1 - k), 340, a=a)
    tc = wt("ten-hour", s)
    kc = eo((T - tc + 0.25) / 0.4)
    item(img, WK, "decimal_clock", 705, 1090 + 25 * (1 - kc), 340, a=a * clamp(kc * 2), rot=-3 * math.floor((T - tc) * 2) if T > tc else 0)
    num(img, "1793", 770, YELLOW, a * clamp((T - wt("1793", s) + 0.1) / 0.3), x=705)
    lab(img, "10-day week", 1290, YELLOW, a * on(T, "ten-day", s, e, need=2.5), x=255)
    lab(img, "10-hour day", 1290, YELLOW, a * on(T, "ten-hour", s, e, need=1.8), x=705)
    R.chrome(img, T)
    title(img, T, s, e, "Revolution!")
V.backdrop("france")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="city", seed=8))
V.sounds("france", [(0.05, "whoosh", 0.6), (rel("france", "ten-day"), "pop", 0.7), (rel("france", "ten-hour"), "pop", 0.7)])

RC = (420, 1050, 460)                    # calendario revolucionario grande (sprite 424x389 → ×1,08)
def rc_cols(cx, cy, h):
    w = h * 424 / 389
    return cx - w / 2, cy - h / 2, w
@V.scene("rest")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    cx, cy, h = RC
    item(img, WK, "revolution_calendar", cx, cy + 25 * (1 - k), h, a=a)
    x0, y0, w = rc_cols(cx, cy + 25 * (1 - k), h)
    tr = wt("rest", s)
    kh = clamp((T - wt("ten", s) + 0.1) / 0.3)
    cw = (0.92 - 0.08) * w / 10
    if kh > 0: highlight_col(img, x0 + 0.08 * w + 9 * cw - 8, y0 + 0.36 * h, cw + 16, 0.50 * h, a * kh)
    lab(img, "Rest: day 10", 1320, RED_T, a * on(T, "ten", s, e, need=1.8), x=cx)
    item(img, "young_man", "cold", 800, 1350, 400, a=a * clamp((T - s - 0.3) / 0.3), anchor="bottom")
    R.chrome(img, T)
    title(img, T, s, e, "Rest every 10th day")
V.backdrop("rest")(lambda img, T, t: ST.card(img, CARD))
V.sounds("rest", [(0.05, "whoosh", 0.6), (rel("rest", "ten"), "pop", 0.7)])

@V.scene("ended")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, h = 470, 1090, 460
    tn = wt("ended", s)
    kf = clamp((T - wt("faded", s) + 0.1) / 0.6)
    item(img, WK, "revolution_calendar", cx, cy, h, a=a * (1 - 0.35 * kf))
    cross(img, cx, cy, 180, clamp((T - tn) / 0.4), a)
    num(img, "1806", 770, YELLOW, a * clamp((T - min(wt("1806", s), e - 1.8) + 0.1) / 0.3), x=cx)
    lab(img, "Calendar ended", 1340, YELLOW, a * on(T, "ended", s, e, need=2.0), x=cx)
    R.chrome(img, T)
    title(img, T, s, e, "Back to seven")
    return R.punch(img, T, tn, amt=0.05)
V.backdrop("ended")(lambda img, T, t: ST.sky(img, (46, 84, 140), (22, 40, 82)))
V.sounds("ended", [(0.05, "whoosh", 0.6), (rel("ended", "ended"), "pop", 0.9), (rel("ended", "1806."), "tap", 0.6)])

@V.scene("habit")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    item(img, WK, "weekend_hammock", 620, 1180 + 20 * (1 - k), 420, a=a, anchor="bottom", rot=1.2 * math.sin(T * 1.6))
    lab(img, "An old habit", 790, YELLOW, a * on(T, "habit", s, e, need=2.1), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Human-made")
V.backdrop("habit")(lambda img, T, t: ST.landscape(img, T, sky_kind="sunset", terrain="waves", seed=12))
V.sounds("habit", [(0.05, "whoosh", 0.6), (rel("habit", "habit"), "sparkle", 0.6)])

@V.scene("bridge")
def _(img, T, t, s, e):
    end = V.outro_at
    Tl = V.last_t
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
