"""Reel: Myth or fact: does charging your phone overnight ruin the battery? Mr. Whiskerfact, categoría Tech, formato myth.
Voz de Brad. Tanda B2-length, opción `short` (variante): ejecutar con REEL_LENGTH=short. Primer reel en bucle (loop=True).

Fuentes (dos por dato): ver voice/overnight_charging_claims.md
- Memoria de las baterías de níquel / el litio casi sin memoria: Australian Academy of Science; Battery University (BU-808, Memory)
- Los móviles dejan de cargar al 100 % y solo rellenan: CQUniversity; Samsung; Battery University BU-808
- Carga optimizada (~80 %, aprende la rutina): Apple 108055; Samsung (Adaptive); Google Pixel Help
- Calor y horas al 100 %: Battery University BU-808; Apple (Maximizing Battery Life); Google
- Lleno + caliente, bajo la almohada: Battery University BU-808; CQUniversity

Sprites de la biblioteca (battery_items, large_w47, wifi_objects) a ≤1,5x; iconos de batería, gráfica, ondas de calor y
cable por código.
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

SLUG = "overnight_charging"
CATEGORY = "tech"
R = Reel(CATEGORY)
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "Does"), ("stamp", "Mostly"), ("origin", "Blame"), ("memory", "recharge"), ("lithium", "Your"),
    ("first", "First"), ("many", "Many"), ("second", "Second"), ("high", "High"), ("worst", "Worst"),
    ("verdict", "The"), ("ask", "Be"), ("bridge", "Because")], loop=True)
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
GREEN = (70, 178, 84)
YELLOW = (246, 196, 60)
RED = (222, 64, 60)
CARD = (56, 742, 1024, 1384)
BI, LW, WO = "battery_items", "large_w47", "wifi_objects"
LINE1, LINE2, SUB = "Overnight", "Charging", "Does it kill your battery?"
HOOK_PHONE = (600, 1075, 380)

def wt(word, s): return V.word_time(word, after=s)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))
def on(T, word, s, e, need=1.6, lead=0.1): return clamp((T - min(wt(word, s), e - need) + lead) / 0.3)

def until(T, word, s, e, need=1.6):
    """1 hasta poco antes de que entre la etiqueta siguiente (sin solapes): sale en 0,15 s antes de `word`"""
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

def item(img, lib, name, x, y, h, a=1.0, anchor="center", flip=False, rot=0.0):
    LIB.place(img, lib, name, x, y, height=h, a=a, anchor=anchor, flip=flip, rot=rot)

def batt_color(f): return GREEN if f > 0.55 else (YELLOW if f > 0.25 else RED)

def battery(img, cx, cy, w, f, a=1.0, col=None, bolt=False, cap_line=None):
    """icono de batería vectorial: f = carga 0..1; cap_line = línea de «memoria» (fracción) en rojo"""
    h = w * 0.5
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    c = col or batt_color(f)
    def fn(d, P, s):
        d.rounded_rectangle([P(x1, cy - h * 0.18), P(x1 + w * 0.07, cy + h * 0.18)], radius=int(6 * s), fill=INK_T)
        d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=int(h * 0.18 * s), fill=(250, 248, 240), outline=INK_T, width=int(7 * s))
        pad = w * 0.06
        if f > 0.01:
            d.rounded_rectangle([P(x0 + pad, y0 + pad), P(x0 + pad + (w - 2 * pad) * clamp(f), y1 - pad)], radius=int(8 * s), fill=c)
        if cap_line is not None:
            xl = x0 + pad + (w - 2 * pad) * cap_line
            d.line([P(xl, y0 - 12), P(xl, y1 + 12)], fill=RED, width=int(8 * s))
        if bolt:
            bx, by, k = cx, cy, h * 0.42
            pts = [(bx + 0.15 * k, by - k), (bx - 0.45 * k, by + 0.12 * k), (bx - 0.02 * k, by + 0.12 * k),
                   (bx - 0.18 * k, by + k), (bx + 0.45 * k, by - 0.15 * k), (bx + 0.02 * k, by - 0.15 * k)]
            d.polygon([P(*p) for p in pts], fill=(255, 236, 90), outline=INK_T, width=int(5 * s))
    aa(img, (x0 - 14, y0 - 16, x1 + w * 0.07 + 14, y1 + 16), fn, a)

def heat_waves(img, cx, y0, y1, T, a=1.0, n=3, spread=90, col=(240, 110, 50)):
    def fn(d, P, s):
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * spread
            pts = []
            for k in range(30):
                y = y1 - (y1 - y0) * k / 29
                pts.append(P(x + 14 * math.sin(k * 0.55 - T * 6 + i), y))
            d.line(pts, fill=col, width=int(10 * s), joint="curve")
    aa(img, (cx - spread * n, y0 - 10, cx + spread * n, y1 + 10), fn, a)

def mark_noink(layer, pos):
    import reel_lib as _RL
    from PIL import ImageChops
    m = _RL.NOINK["mask"]
    if m is None or m.size != (W, H): return
    tmp = Image.new("L", (W, H), 0); tmp.paste(layer.split()[3], (int(pos[0]), int(pos[1])))
    _RL.NOINK["mask"] = ImageChops.lighter(m, tmp)

_stamp_cache = {}
def stamp(img, text, cx, cy, k, a=1.0, col=RED_T):
    """sello «MOSTLY MYTH»: texto a tamaño final en la capa de etiquetas, inclinación pequeña (≤ 6°), entra con golpe"""
    if a <= 0.003 or k <= 0: return
    if text not in _stamp_cache:
        f = cover_mod._font("Black", 110)
        tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        tw = int(tmp.textlength(text, font=f))
        lay = Image.new("RGBA", (tw + 120, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([14, 14, tw + 106, 206], radius=26, outline=col, width=14, fill=(255, 250, 240, 235))
        d.text(((tw + 120) / 2, 112), text, font=f, fill=col, anchor="mm")
        _stamp_cache[text] = lay.rotate(-6, resample=Image.BICUBIC, expand=True)
    spr = _stamp_cache[text]
    sc = 1 + 0.35 * (1 - eo(k))
    if sc > 1.001:
        spr = spr.resize((int(spr.width * sc), int(spr.height * sc)), Image.LANCZOS)
    R.put_text(img, spr, cx, cy, a * clamp(k * 3), "mm", text=text)

# =====================================================================  ESCENAS
def hook_art(img, T, a=1.0):
    x, y, h = HOOK_PHONE
    bob = 6 * math.sin(T * 2.4)
    item(img, LW, "charging_phone_big", x, y + bob, h * (1 + 0.04 * eo(T / 0.4)), a=a)
    f = 0.15 + 0.85 * ((T * 0.9) % 1.0)                     # la batería se llena una y otra vez: algo se mueve desde 0 s
    battery(img, 735, 905 + bob, 170, f, a=a, bolt=True)

@V.scene("hook")
def _(img, T, t, s, e):
    hook_art(img, T)
    cover_mod.draw_header(img, CATEGORY)
    cover_mod.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))
    R.hook_mascot(img, T, 0.0, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "kill"), "tap", 0.7)])

@V.scene("stamp")
def _(img, T, t, s, e):
    a = win(T, s, e)
    item(img, LW, "charging_phone_big", 540, 1060, 430, a=a)
    tm = wt("myth", s)
    stamp(img, "MOSTLY MYTH", 540, 1010, clamp((T - tm + 0.05) / 0.25), a)
    lab(img, "...not completely", 1250, INK_T, a * on(T, "not", s, e, need=1.5), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Myth or fact?")
    return R.punch(img, T, tm, amt=0.05)
V.sounds("stamp", [(0.05, "whoosh", 0.6), (rel("stamp", "myth"), "pop", 1.0), (rel("stamp", "not"), "tap", 0.6)])

@V.scene("origin")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k1 = eo((T - s) / 0.4)
    item(img, BI, "old_phone", lerp(200, 330, k1), 1180, 340, a=a, rot=-4)
    kb = on(T, "nickel", s, e, need=2.2)
    item(img, BI, "nicd_battery", 640, lerp(1260, 1130, eo(kb)), 300, a=a * kb)
    lab(img, "Nickel batteries", 880, B.TEXT, a * kb, x=560)
    km = on(T, "memory", s, e, need=1.5)
    lab(img, "\"Memory effect\"", 960, YELLOW, a * km, x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Old phones")
V.sounds("origin", [(0.05, "whoosh", 0.6), (rel("origin", "nickel"), "pop", 0.7), (rel("origin", "memory"), "sparkle", 0.6)])
V.backdrop("origin")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="city", seed=2))

@V.scene("memory")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tr, tl = wt("before", s), wt("lose", s)
    # descarga parcial (100 → 60 %), recarga, y la batería «recuerda» la marca: la capacidad útil parece encoger
    if T < tr: f = lerp(1.0, 0.6, eio((T - s) / max(0.3, tr - s)))
    else: f = lerp(0.6, 1.0, eio((T - tr) / 0.9))
    usable = 1.0 if T < tl - 0.1 else lerp(1.0, 0.6, eio((T - tl + 0.1) / 0.8))
    f = min(f, usable) if T >= tl - 0.1 else f
    battery(img, 520, 1010, 560, f, a=a, cap_line=0.6 if T > tr else None)
    lab(img, "Recharged at 60%", 1200, INK_T, a * on(T, "before", s, e, need=2.0) * until(T, "lose", s, e, need=1.6), x=540)
    lab(img, "Seems smaller", 1200, RED_T, a * on(T, "lose", s, e, need=1.6), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Memory effect")
V.sounds("memory", [(0.05, "tap", 0.5), (rel("memory", "before"), "click", 0.6), (rel("memory", "lose"), "whoosh", 0.6)])

@V.scene("lithium")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.5)
    item(img, LW, "battery_cutaway", 520, lerp(1120, 1040, k), 330, a=a, rot=3 * math.sin(T * 1.2))
    lab(img, "Lithium-ion", 830, B.TEXT, a * on(T, "runs", s, e, need=2.2), x=520)
    lab(img, "No memory effect", 1250, YELLOW, a * on(T, "practically", s, e, need=1.6), x=520)
    R.chrome(img, T)
    title(img, T, s, e, "Your phone")
    return R.punch(img, T, wt("practically", s), amt=0.04)
V.sounds("lithium", [(0.05, "whoosh", 0.6), (rel("lithium", "runs"), "pop", 0.6), (rel("lithium", "practically"), "sparkle", 0.7)])
V.backdrop("lithium")(lambda img, T, t: (ST.sky(img, (20, 24, 70), (60, 40, 110)), ST.stars(img, T, n=70, seed=5, y1=H)))

@V.scene("first")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tf, tu = wt("full", s), wt("top", s)
    item(img, BI, "phone_charging", 330, 1080, 360, a=a)
    if T < tf: f = lerp(0.7, 1.0, eio((T - s) / max(0.3, tf - s)))
    elif T < tu: f = 1.0
    else:
        ph = ((T - tu) % 2.0) / 2.0                        # 100 → 95 → 100: el relleno
        f = 1.0 - 0.05 * math.sin(math.pi * ph)
    battery(img, 690, 1000, 280, f, a=a, bolt=T < tf)
    lab(img, f"{int(round(f * 100))}%", 1110, INK_T, a, x=690)
    lab(img, "Stops at 100%", 800, RED_T, a * on(T, "full", s, e, need=2.6) * until(T, "top", s, e, need=1.6), x=540)
    lab(img, "Then small top-ups", 800, INK_T, a * on(T, "top", s, e, need=1.6), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Step 1: it stops")
V.sounds("first", [(0.05, "whoosh", 0.6), (rel("first", "full"), "click", 0.8), (rel("first", "top"), "tap", 0.6)])

@V.scene("many")
def _(img, T, t, s, e):
    a = win(T, s, e)
    item(img, LW, "bedroom_night", 440, 1035, 470, a=a)
    th, tf = wt("eighty", s), wt("finish", s)
    if T < th: f = lerp(0.35, 0.8, eio((T - s) / max(0.3, th - s)))
    elif T < tf: f = 0.8
    else: f = lerp(0.8, 1.0, eio((T - tf) / 0.8))
    battery(img, 820, 860, 150, f, a=a)
    lab(img, f"{int(round(f * 100))}%", 940, B.TEXT, a, x=820)
    lab(img, "Learns your routine", 1285, B.TEXT, a * on(T, "routine", s, e, need=2.2) * until(T, "eighty", s, e, need=2.0), x=470)
    lab(img, "Holds ~80%", 1285, YELLOW, a * on(T, "eighty", s, e, need=2.0) * until(T, "finish", s, e, need=1.6), x=470)
    lab(img, "100% when you unplug", 1285, YELLOW, a * on(T, "finish", s, e, need=1.6), x=470)
    R.chrome(img, T)
    title(img, T, s, e, "Smart charging")
V.sounds("many", [(0.05, "whoosh", 0.6), (rel("many", "eighty"), "pop", 0.7), (rel("many", "finish"), "sparkle", 0.6)])

WOW_DUR = 1.3
@V.scene("second")
def _(img, T, t, s, e):
    a = win(T, s, e)
    th = wt("heat", s)
    kh = clamp((T - th + 0.05) / 0.3)
    item(img, BI, "thermometer", 520, 1060 - 10 * math.sin(T * 3) * kh, 320 * (1 + 0.08 * eo(kh)), a=a)
    heat_waves(img, 520, 860, 980, T, a * kh, n=3, spread=110)
    R.chrome(img, T)
    title(img, T, s, e, "The real enemy")
    R.txt(img, "HEAT", TITLE_Y + 105, "title", (255, 222, 90), a * kh)
    return R.punch(img, T, th, amt=0.06)
def second_bg(img, T, t):
    s = V.sc["second"][0]; th = wt("heat", s)
    ST.landscape(img, T, sky_kind="sunset", terrain="dunes", seed=4)
    ST.wow_moment(img, T, th - 0.05, CATEGORY, "blobs", dur=WOW_DUR, center=(520, 1060))
V.backdrop("second")(second_bg)
V.sounds("second", [(0.05, "tap", 0.5), (rel("second", "heat") - 0.05, "sparkle", 0.9)])

GR = (150, 820, 900, 1300)     # caja de la gráfica
@V.scene("high")
def _(img, T, t, s, e):
    a = win(T, s, e)
    x0, y0, x1, y1 = GR
    k = eio((T - s - 0.2) / 2.6)
    def graph(d, P, s_):
        d.line([P(x0, y0), P(x0, y1), P(x1, y1)], fill=INK_T, width=int(7 * s_))
        n = 40; xe = x0 + (x1 - x0) * k
        cool = [P(x0 + (xe - x0) * i / n, y0 + 60 + 90 * (i / n)) for i in range(n + 1)]
        hot = [P(x0 + (xe - x0) * i / n, y0 + 60 + 330 * (i / n) ** 0.9) for i in range(n + 1)]
        if k > 0.02:
            d.line(cool, fill=(40, 140, 200), width=int(12 * s_), joint="curve")
            d.line(hot, fill=RED, width=int(12 * s_), joint="curve")
    aa(img, (x0 - 10, y0 - 10, x1 + 10, y1 + 10), graph, a)
    xe = x0 + (x1 - x0) * k
    lab(img, "Cool", y0 + 150 - 60, (30, 90, 150), a * clamp(k * 3 - 2), x=min(xe, x1) - 70)
    lab(img, "Hot", y0 + 60 + 330 - 120, RED_T, a * clamp(k * 3 - 2), x=min(xe, x1) - 60)
    lab(img, "Capacity", y0 - 40, INK_T, a, x=x0 + 110)
    lab(img, "Time", y1 + 14, INK_T, a, x=x1 - 70)
    kf = on(T, "sitting", s, e, need=2.2)
    battery(img, 360, 1180, 150, 1.0, a=a * kf)
    lab(img, "+ hours at 100%", 1230, INK_T, a * kf, x=600)
    R.chrome(img, T)
    title(img, T, s, e, "Heat ages it")
V.sounds("high", [(0.05, "whoosh", 0.6), (0.6, "tap", 0.5), (rel("high", "sitting"), "pop", 0.7)])

@V.scene("worst")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tp, tt = wt("pillow", s), wt("trapped", s)
    kp = on(T, "pillow", s, e, need=2.6)
    battery(img, 320, 1000, 280, 1.0, a=a * (1 - kp))
    item(img, BI, "thermometer", 720, 1000, 320, a=a * (1 - kp))
    lab(img, "Full + hot", 1200, YELLOW, a * on(T, "Full", s, e, need=2.0) * (1 - kp), x=520)
    kt = clamp((T - tt + 0.1) / 0.6)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([250, 960, 830, 1300], fill=(255, 90, 40, int(120 * kt * a * kp)))
    from PIL import ImageFilter
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
    item(img, LW, "phone_under_pillow", 540, 1130, 380, a=a * kp)
    heat_waves(img, 540, 900, 1010, T, a * kp * (1 - 0.6 * kt), n=3, spread=120)
    lab(img, "Heat gets trapped", 1330, YELLOW, a * on(T, "trapped", s, e, need=1.6), x=520)
    R.chrome(img, T)
    title(img, T, s, e, "Worst combo")
    return R.punch(img, T, tp, amt=0.04)
def worst_bg(img, T, t):
    ST.sky(img, (26, 30, 70), (48, 40, 96))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, H], fill=(70, 52, 60))           # colcha de la cama
    d.rectangle([0, 1250, W, 1268], fill=(52, 38, 46))
V.backdrop("worst")(worst_bg)
V.sounds("worst", [(0.05, "whoosh", 0.6), (rel("worst", "pillow"), "pop", 0.8), (rel("worst", "trapped"), "whoosh", 0.6)])

@V.scene("verdict")
def _(img, T, t, s, e):
    a = win(T, s, e)
    kv = on(T, "villain", s, e, need=3.2)
    kh = on(T, "Heat", s, e, need=2.0)
    item(img, BI, "nightstand", 300, 1150, 230, a=a)
    item(img, BI, "bedside_lamp", 250, 965, 170, a=a)
    item(img, BI, "phone_charging", 370, 1000, 150, a=a)
    lab(img, "Not the night", 1300, INK_T, a * kv, x=300)
    def tick(d, P, s_):
        d.line([P(250, 800), P(290, 840), P(360, 760)], fill=GREEN, width=int(16 * s_), joint="curve")
    aa(img, (230, 740, 380, 860), tick, a * kv)
    item(img, BI, "thermometer", 680, 1030, 230, a=a * kh)
    battery(img, 800, 1150, 130, 1.0, a=a * kh)
    lab(img, "Heat + 100%", 1300, RED_T, a * kh, x=730)
    R.chrome(img, T)
    title(img, T, s, e, "The verdict")
    return R.punch(img, T, wt("Heat", s), amt=0.04)
V.sounds("verdict", [(0.05, "whoosh", 0.6), (rel("verdict", "villain"), "pop", 0.7), (rel("verdict", "Heat"), "pop", 0.8)])

@V.scene("ask")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo((T - s) / 0.4)
    item(img, BI, "nightstand", 640, 1240, 260, a=a)
    item(img, BI, "phone_charging", 640, lerp(1150, 1030, k), 230, a=a)
    battery(img, 800, 1010, 140, 0.4 + 0.6 * ((T * 0.5) % 1.0), a=a * k, bolt=True)
    R.mascot(img, 230, 110, 980, a * eo((T - s - 0.2) / 0.4))
    R.chrome(img, T)
    title(img, T, s, e, "Charging right now?")
    lab(img, "Tell me below", 790, YELLOW, a * on(T, "Tell", s, e, need=1.5), x=540)
V.sounds("ask", [(0.05, "whoosh", 0.6), (rel("ask", "Tell"), "pop", 0.7)])
V.backdrop("ask")(lambda img, T, t: ST.landscape(img, T, night=True, terrain="pines", seed=5))

@V.scene("bridge")
def _(img, T, t, s, e):
    hook_art(img, T, a=clamp((T - s) / B.ENTER))
    cover_mod.draw_header(img, CATEGORY)
    end = V.outro_at
    ka = clamp((T - (end - 0.7)) / 0.55)                    # el título de la portada vuelve justo antes del bucle
    if ka > 0: cover_mod.draw_title(img, LINE1, LINE2, SUB, a=ka)
V.sounds("bridge", [(0.05, "whoosh", 0.6)])

# ---------- fondos ----------
def card_bg(img, T, t): ST.card(img, CARD)
V.backdrop("hook")(lambda img, T, t: cover_mod.draw_bg(img, CATEGORY, 0.05 * T))
V.backdrop("bridge")(lambda img, T, t: cover_mod.draw_bg(img, CATEGORY, 0.05 * T))
for n in ("stamp", "memory", "first", "high", "verdict"):
    V.backdrop(n)(card_bg)

if __name__ == "__main__":
    V.main()
