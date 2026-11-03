"""Reel: 2.4 GHz or 5 GHz? Which classic Wi-Fi band wins? Mr. Whiskerfact, formato versus, categoría Tech. Voz de Brad.

Fuentes (dos por dato): ver voice/wifi_bands_claims.md
- 5 GHz suele ser más rápida; 2.4 GHz llega más lejos: ASUS, Linksys, TP-Link, UChicago DSI
- Las frecuencias altas atraviesan peor paredes y muebles: TP-Link, UChicago DSI, ASUS
- 2.4 GHz tiene solo 3 canales sin solapamiento; 5 GHz bastantes más (~20 según país/router): ASUS, Linksys, TP-Link
- El microondas trabaja a ~2,45 GHz, dentro de la banda de 2.4 y puede perturbar el Wi-Fi: Britannica, WTAMU, UT Austin, UChicago DSI
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("tech")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, "wifi_bands", [
    ("hook", "Two"), ("translate", "Quick"), ("speed", "Round"), ("fly", "so"), ("range", "Round"),
    ("meanwhile", "Meanwhile"), ("crowd", "Round"), ("picture", "Picture"), ("twenty", "often"),
    ("twist", "Now"), ("inside", "Right"), ("others", "Bluetooth"), ("final", "Final"),
    ("take", "But"), ("close", "Next")])

# ---------- paleta ----------
C24 = (244, 150, 40); C24_D = (176, 86, 8); C24_L = (255, 196, 110)
C5 = (40, 160, 230); C5_D = (16, 98, 170); C5_L = (140, 214, 255)
GREEN = (40, 170, 90)
INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BRICK = (176, 90, 62); BRICK_D = (120, 58, 42)
ROAD = (62, 66, 78); ROAD_L = (236, 232, 214)

# ---------- utilidades (antialias 2x) ----------
def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def circ(d, P, x, y, r, col):
    d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=col)

def title(img, T, s, e, text, color=B.TEXT, y=TITLE_Y, delay=0.0):
    R.txt(img, text, y, "title", color, win(T, s + delay, e))

def wt(word, s): return V.word_time(word, after=s)
def rel(name, word): return V.word_time(word, after=V.sc[name][0]) - V.sc[name][0]
def label_in(T, at, e): return clamp((T - min(at, e - 1.9)) / 0.3)
def label(img, text, y, color, a, x): R.txt(img, text, y, "label", color, a, x=x, rise=False)
def score(img, T, s, e, a5, a24, at):
    """marcador bajo el título: aparece cuando el narrador señala al ganador de la ronda"""
    R.txt(img, f"5 GHz  {a5}  –  {a24}  2.4 GHz", TITLE_Y + 110, "subtitle", ACC_T, win(T, min(at, e - 2.0), e))

CARD = (56, 742, 1024, 1384)
def card_bg(img, T, t): ST.card(img, CARD)

# ---------- ondas de radio: arcos que salen del router (frecuencia alta = arcos juntos, baja = arcos separados) ----------
def arcs(d, P, s_, ox, oy, r0, r1, spacing, off, col, ang, w=8, fade=1.0, grow=0.0):
    r = r0 + (off % spacing)
    while r < r1:
        k = (r - r0) / (r1 - r0)
        al = int(255 * clamp(1 - fade * k))
        if al > 6:
            d.arc([P(ox - r, oy - r), P(ox + r, oy + r)], ang[0], ang[1], fill=col + (al,), width=int(w * s_))
        r += spacing

def wifi_icon(d, P, s_, x, y, r, col, bars=3):
    for i in range(bars):
        rr = r * (0.45 + 0.28 * i)
        d.arc([P(x - rr, y - rr), P(x + rr, y + rr)], 225, 315, fill=col, width=int(7 * s_))
    circ(d, P, x, y, r * 0.12, col)

# ---------- pared de ladrillo ----------
def brick_wall(img, x, y0, y1, w=64, a=1.0):
    def fn(d, P, s_):
        d.rectangle([P(x, y0), P(x + w, y1)], fill=BRICK)
        yy = y0; row = 0
        while yy < y1:
            d.line([P(x, yy), P(x + w, yy)], fill=BRICK_D, width=int(4 * s_))
            off = 0 if row % 2 == 0 else w / 2
            for bx in (x + off, x + off + w):
                if x < bx < x + w: d.line([P(bx, yy), P(bx, min(yy + 30, y1))], fill=BRICK_D, width=int(4 * s_))
            yy += 30; row += 1
        d.rectangle([P(x, y0), P(x + w, y1)], outline=INK_T, width=int(5 * s_))
    aa(img, (x - 10, y0 - 10, x + w + 10, y1 + 10), fn, a)

# ---------- barra de datos ----------
def bar(img, x0, x1, y, h, k, col, a=1.0):
    def fn(d, P, s_):
        d.rounded_rectangle([P(x0, y), P(x1, y + h)], radius=h / 2 * s_, fill=(206, 196, 164), outline=INK_T, width=int(4 * s_))
        if k > 0.01:
            d.rounded_rectangle([P(x0, y), P(lerp(x0 + h, x1, clamp(k)), y + h)], radius=h / 2 * s_, fill=col, outline=INK_T, width=int(4 * s_))
    aa(img, (x0 - 10, y - 10, x1 + 10, y + h + 10), fn, a)

# ---------- carretera vista desde arriba ----------
def car(d, P, s_, x, y, w, h, col):
    d.rounded_rectangle([P(x, y), P(x + w, y + h)], radius=h * 0.3 * s_, fill=col, outline=INK_T, width=int(3 * s_))
    d.rounded_rectangle([P(x + w * 0.58, y + h * 0.18), P(x + w * 0.86, y + h * 0.82)], radius=h * 0.15 * s_, fill=(210, 232, 248))

def road(img, T, x0, x1, y0, y1, lanes, col, speed, gap, a=1.0, seed=0, label_cols=None):
    """lanes carriles; coches de color col, avanzan a `speed` px/s separados `gap` px"""
    lh = (y1 - y0) / lanes
    def fn(d, P, s_):
        d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=18 * s_, fill=ROAD, outline=INK_T, width=int(5 * s_))
        for i in range(lanes):
            if lanes > 8 and i % 2 == 0:
                d.rectangle([P(x0 + 4, y0 + lh * i), P(x1 - 4, y0 + lh * (i + 1))], fill=(76, 80, 94))
        for i in range(1, lanes if lanes <= 8 else 1):
            y = y0 + lh * i
            xx = x0 + 6
            while xx < x1 - 12:
                d.line([P(xx, y), P(min(xx + 28, x1 - 6), y)], fill=ROAD_L, width=max(1, int(min(4, lh * 0.08) * s_)))
                xx += 52
        cw, ch = (min(92, lh * 1.5), lh * 0.62) if lanes <= 8 else (34, lh * 0.55)
        rng = np.random.default_rng(seed)
        for i in range(lanes):
            off = rng.uniform(0, gap); sp = speed * rng.uniform(0.85, 1.15)
            xx = x0 - cw + ((T * sp + off) % gap) - gap
            while xx < x1:
                if xx + cw > x0 + 4 and xx < x1 - 4:
                    cx0 = max(xx, x0 + 4); cx1 = min(xx + cw, x1 - 4)
                    if cx1 - cx0 > 8: car(d, P, s_, cx0, y0 + lh * i + (lh - ch) / 2, cx1 - cx0, ch, col)
                xx += gap
    aa(img, (x0 - 10, y0 - 10, x1 + 10, y1 + 10), fn, a)

def spinner(img, x, y, r, T, col, a=1.0):
    def fn(d, P, s_):
        circ(d, P, x, y, r + 8, (246, 244, 238)); circ(d, P, x, y, r - 8, (246, 244, 238, 0))
        st = (T * 260) % 360
        d.arc([P(x - r, y - r), P(x + r, y + r)], st, st + 270, fill=col, width=int(12 * s_))
    aa(img, (x - r - 20, y - r - 20, x + r + 20, y + r + 20), fn, a)

# ---------- iconos ----------
def bluetooth(img, x, y, sz, col, a=1.0):
    def fn(d, P, s_):
        pts = [(-0.55, -0.55), (0.55, 0.55), (0, 1.05), (0, -1.05), (0.55, -0.55), (-0.55, 0.55)]
        d.line([P(x + px * sz, y + py * sz) for px, py in pts], fill=col, width=int(sz * 0.26 * s_), joint="curve")
    aa(img, (x - sz * 1.4, y - sz * 1.4, x + sz * 1.4, y + sz * 1.4), fn, a)

def cordless(img, x, y, sz, a=1.0):
    def fn(d, P, s_):
        d.rounded_rectangle([P(x - 0.42 * sz, y - 0.8 * sz), P(x + 0.42 * sz, y + 0.9 * sz)], radius=0.18 * sz * s_, fill=(72, 78, 96), outline=INK_T, width=int(5 * s_))
        d.rounded_rectangle([P(x - 0.3 * sz, y - 0.62 * sz), P(x + 0.3 * sz, y - 0.1 * sz)], radius=0.06 * sz * s_, fill=(176, 224, 190))
        for r_ in range(3):
            for c_ in range(3):
                circ(d, P, x - 0.2 * sz + c_ * 0.2 * sz, y + 0.12 * sz + r_ * 0.22 * sz, 0.05 * sz, (220, 220, 228))
        d.line([P(x + 0.3 * sz, y - 0.8 * sz), P(x + 0.3 * sz, y - 1.15 * sz)], fill=INK_T, width=int(6 * s_))
        circ(d, P, x + 0.3 * sz, y - 1.15 * sz, 0.06 * sz, RED_T)
    aa(img, (x - sz, y - 1.3 * sz, x + sz, y + sz), fn, a)

def popcorn(img, T, x, y, a=1.0):
    def fn(d, P, s_):
        for i in range(7):
            ph = (T * 1.6 + i * 0.37) % 1
            px = x + (i - 3) * 22 + 10 * math.sin(i * 2 + T * 2)
            py = y - 150 * math.sin(ph * math.pi) - 10
            r = 14 + 4 * (i % 3)
            circ(d, P, px, py, r, (252, 244, 214)); circ(d, P, px - r * 0.4, py - r * 0.3, r * 0.5, (255, 255, 250)); circ(d, P, px + r * 0.5, py + r * 0.4, r * 0.35, (240, 200, 90))
    aa(img, (x - 110, y - 200, x + 110, y + 20), fn, a)

# ---------- plano de la casa (rango): dos habitaciones separadas por una pared ----------
WALL_X = 460
RX, RY = 190, 1160            # origen de las ondas (arriba del router)
def house(img, T, a, furniture=False, far_thing=True):
    LIB.place(img, "wifi_objects", "router", RX, 1285, height=190, a=a)
    if furniture: LIB.place(img, "wifi_objects", "armchair", 340, 1285, height=150, a=a)
    brick_wall(img, WALL_X, 880, 1290, 64, a)
    if far_thing: LIB.place(img, "wifi_objects", "laptop", 690, 1285, height=150, a=a)
    def floor(d, P, s_): d.line([P(80, 1290), P(890, 1290)], fill=INK_T, width=int(6 * s_))
    aa(img, (70, 1270, 900, 1310), floor, a)

# =========================================================
@V.scene("hook")
def _(img, T, t, s, e):
    cx, base = 470, 1250
    def fn(d, P, s_):
        arcs(d, P, s_, cx, 1060, 70, 330, 32, T * 70, C5, (-42, 42), w=8, fade=1.0)
        arcs(d, P, s_, cx, 1060, 70, 330, 76, T * 70, C24, (138, 222), w=10, fade=1.0)
    aa(img, (60, 760, 900, 1340), fn, clamp(T / 0.25))
    LIB.place(img, "wifi_objects", "router", cx, base, height=250)
    label(img, "2.4 GHz", 820, C24_L, clamp(T / 0.3), 215)
    label(img, "5 GHz", 820, C5_L, clamp(T / 0.3), 735)
    R.chrome(img, T)
    V.hook_text(img, T, e, "2.4 or 5 GHz?", "Which Wi-Fi band wins?", "Which")
    R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.25, "whoosh", 0.5), (0.6, "pop", 0.8)])

@V.scene("translate")
def _(img, T, t, s, e):
    t3 = wt("Three", s)
    a = win(T, s, e)
    if T < t3 + 0.05:
        wk = wt("wiggles", s); bt = wt("billions", s)
        aa_ = a * clamp(1 - (T - (t3 - 0.15)) / 0.2)
        LIB.place(img, "wifi_objects", "router", 160, 1290, height=170, a=aa_)
        def wave(d, P, s_):
            pts = []
            for i in range(0, 601, 4):
                x = 290 + i
                amp = 105 * clamp(i / 60)
                pts.append(P(x, 1040 + amp * math.sin(i / 38 - T * 16)))
            d.line(pts, fill=C24, width=int(10 * s_), joint="curve")
            if T > wk:        # un solo ciclo, marcado con un corchete
                x0 = 560; x1 = x0 + 38 * 2 * math.pi
                d.line([P(x0, 1210), P(x0, 1230), P(x1 - 60, 1230), P(x1 - 60, 1210)], fill=INK_T, width=int(5 * s_))
        aa(img, (270, 880, 900, 1260), wave, aa_)
        label(img, "1 wiggle", 1240, INK_T, aa_ * label_in(T, wk, t3), 690)
        label(img, "billions per second", 800, C24_D, aa_ * label_in(T, bt, t3), 560)
        title(img, T, s, t3 - 0.1, "What's a gigahertz?")
    else:
        k = [clamp((T - (t3 + dt)) / 0.35) for dt in (0.0, 0.5, 1.0)]
        items = [("1", "Speed", C5), ("2", "Range", C24), ("3", "Crowding", C5)]
        for i, (n, w_, col) in enumerate(items):
            cx = 215 + i * 255; p = back_out(k[i])
            if p <= 0: continue
            def fn(d, P, s_, cx=cx, p=p, col=col):
                d.rounded_rectangle([P(cx - 112, 920 + (1 - clamp(p)) * 40), P(cx + 112, 1180 + (1 - clamp(p)) * 40)], radius=30 * s_, fill=(246, 240, 220), outline=INK_T, width=int(6 * s_))
                circ(d, P, cx, 1010 + (1 - clamp(p)) * 40, 52, col)
            aa(img, (cx - 130, 900, cx + 130, 1230), fn, clamp(p))
            R.put_text(img, R.sprite(n, "number", (255, 255, 255)), cx, 1010 + (1 - clamp(p)) * 40, clamp(k[i] * 3), "mm", text=n)
            label(img, w_, 1100, INK_T, clamp(k[i] * 2) * a, cx)
        R.txt(img, "5 GHz  0  –  0  2.4 GHz", TITLE_Y + 110, "subtitle", ACC_T, win(T, t3 + 1.3, e))
        title(img, T, t3, e, "Three rounds")
    R.chrome(img, T)
V.sounds("translate", [(0.05, "whoosh", 0.6), (rel("translate", "wiggles"), "pop", 0.6), (rel("translate", "billions"), "click", 0.7),
                       (rel("translate", "Three"), "pop", 0.8), (rel("translate", "Three") + 0.5, "pop", 0.8), (rel("translate", "Three") + 1.0, "pop", 0.8)])

@V.scene("speed")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ut = wt("Up", s); dt = wt("data", s)
    LIB.place(img, "wifi_objects", "laptop", 210, 1010, height=190, a=a)
    LIB.place(img, "wifi_objects", "router", 210, 1280, height=170, a=a)
    k5 = eio((T - ut) / 2.6); k24 = 0.42 * eio((T - ut) / 2.6)
    label(img, "5 GHz", 830, C5_D, a * clamp((T - s - 0.2) / 0.3), 560)
    bar(img, 360, 880, 910, 62, k5, C5, a)
    label(img, "2.4 GHz", 1040, C24_D, a * clamp((T - s - 0.4) / 0.3), 560)
    bar(img, 360, 880, 1120, 62, k24, C24, a)
    label(img, "usually faster", 1260, INK_T, a * label_in(T, dt, e), 620)
    R.chrome(img, T)
    title(img, T, s, e, "Round 1: Speed")
V.sounds("speed", [(0.05, "whoosh", 0.6), (rel("speed", "Up"), "whoosh", 0.7), (rel("speed", "data"), "click", 0.6)])

@V.scene("fly")
def _(img, T, t, s, e):
    a = win(T, s, e)
    dl = wt("downloads", s); vc = wt("video", s); pt = wt("Point", s)
    LIB.place(img, "wifi_objects", "router", 190, 1180, height=180, a=a)
    LIB.place(img, "wifi_objects", "laptop", 640, 1180, height=190, a=a)
    def pk(d, P, s_):       # paquetes de datos que vuelan del router al portátil
        for i in range(9):
            u = ((T * 1.5 + i / 9) % 1)
            x = lerp(300, 560, u); y = 1060 - 120 * math.sin(u * math.pi)
            d.rounded_rectangle([P(x - 16, y - 12), P(x + 16, y + 12)], radius=5 * s_, fill=C5, outline=INK_T, width=int(3 * s_))
    aa(img, (270, 880, 620, 1100), pk, a)
    label(img, "big downloads", 800, C5_D, a * label_in(T, dl, e), 470)
    label(img, "video calls", 1300, C5_D, a * label_in(T, vc, e), 470)
    k = clamp((T - pt) / 0.4)
    LIB.place(img, "young_man", "point" if k > 0 else "front", 800, 1290, height=300, a=a)
    score(img, T, s, e, 1, 0, pt)
    R.chrome(img, T)
    title(img, T, s, e, "5 GHz scores")
    return R.punch(img, T, pt + 0.1, amt=0.04)
V.sounds("fly", [(0.05, "whoosh", 0.6), (rel("fly", "downloads"), "pop", 0.6), (rel("fly", "video"), "pop", 0.6), (rel("fly", "Point"), "sparkle", 0.8)])

@V.scene("range")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ft = wt("fade", s); wl = wt("walls", s); fu = wt("furniture", s)
    house(img, T, a, furniture=True, far_thing=True)
    def fn(d, P, s_):
        arcs(d, P, s_, RX, RY, 60, 360, 30, T * 90, C5, (-38, 38), w=8, fade=1.0)
    aa(img, (140, 800, 900, 1290), fn, a * clamp((T - s - 0.1) / 0.3))
    label(img, "5 GHz fades", 800, C5_D, a * label_in(T, ft, e), 270)
    R.chrome(img, T)
    title(img, T, s, e, "Round 2: Range")
V.sounds("range", [(0.05, "whoosh", 0.6), (rel("range", "fade"), "pop", 0.7), (rel("range", "walls"), "tap", 0.6)])

@V.scene("meanwhile")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rt = wt("reaches", s); bd = wt("back", s); pt = wt("Point", s)
    house(img, T, a, furniture=False, far_thing=True)
    def fn(d, P, s_):
        arcs(d, P, s_, RX, RY, 60, 600, 74, T * 90, C24, (-30, 30), w=10, fade=0.55)
    aa(img, (140, 800, 900, 1290), fn, a * clamp((T - s - 0.1) / 0.3))
    def ico(d, P, s_): wifi_icon(d, P, s_, 690, 1070, 70, GREEN)
    aa(img, (600, 980, 780, 1100), ico, a * clamp((T - bd - 0.3) / 0.4))
    label(img, "reaches farther", 800, C24_D, a * label_in(T, rt, e), 690)
    label(img, "back bedroom", 1330, INK_T, a * label_in(T, bd, e), 700)
    k = clamp((T - pt) / 0.3)
    LIB.place(img, "young_man", "point" if k > 0 else "front", 850, 1290, height=230, a=a * clamp((T - pt + 0.5) / 0.3))
    score(img, T, s, e, 1, 1, pt)
    R.chrome(img, T)
    title(img, T, s, e, "2.4 GHz scores")
V.sounds("meanwhile", [(0.05, "whoosh", 0.6), (rel("meanwhile", "reaches"), "whoosh", 0.6), (rel("meanwhile", "back"), "sparkle", 0.7), (rel("meanwhile", "Point"), "pop", 0.8)])

@V.scene("crowd")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ch = wt("channels", s); ov = wt("overlap", s)
    road(img, T, 110, 860, 880, 1220, 3, C24, 60, 190, a, seed=2)
    label(img, "2.4 GHz", 800, C24_D, a * clamp((T - s - 0.3) / 0.3), 485)
    label(img, "3 lanes", 1260, INK_T, a * label_in(T, ch, e), 485)
    R.chrome(img, T)
    title(img, T, s, e, "Round 3: Crowding")
V.sounds("crowd", [(0.05, "whoosh", 0.6), (rel("crowd", "channels"), "pop", 0.7), (rel("crowd", "overlap"), "click", 0.6)])

@V.scene("picture")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rh = wt("rush", s); fv = wt("Five", s)
    sw = eio((T - fv + 0.1) / 0.5)
    if sw < 1:
        road(img, T, 110, 860, 880, 1220, 3, C24, 22, 120, a * (1 - sw), seed=2)
    if sw > 0:
        road(img, T, 110, 860, 860, 1240, 12, C5, 120, 150, a * sw, seed=5)
    label(img, "rush hour", 800, C24_D, a * (1 - sw) * label_in(T, rh, e), 485)
    label(img, "many more lanes", 1280, C5_D, a * sw * clamp((T - fv - 0.3) / 0.3), 485)
    R.chrome(img, T)
    title(img, T, s, e, "A three-lane highway" if T < fv else "5 GHz: way more lanes")
V.sounds("picture", [(0.05, "whoosh", 0.6), (rel("picture", "highway"), "pop", 0.6), (rel("picture", "rush"), "click", 0.5), (rel("picture", "Five"), "whoosh", 0.7)])

@V.scene("twenty")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tw = wt("twenty", s); ct = wt("country", s); pt = wt("Point", s)
    road(img, T, 110, 860, 860, 1230, 20, C5, 140, 210, a, seed=7)
    label(img, "around 20 lanes", 800, C5_D, a * label_in(T, tw, e), 485)
    label(img, "varies by country", 1260, INK_T, a * label_in(T, ct, e), 485)
    LIB.place(img, "young_man", "point" if T > pt else "front", 880, 1360, height=220, a=a * clamp((T - pt + 0.5) / 0.3))
    score(img, T, s, e, 2, 1, pt)
    R.chrome(img, T)
    title(img, T, s, e, "5 GHz scores again")
V.sounds("twenty", [(0.05, "whoosh", 0.6), (rel("twenty", "twenty"), "click", 0.7), (rel("twenty", "Point"), "sparkle", 0.8)])

@V.scene("twist")
def _(img, T, t, s, e):
    a = win(T, s, e)
    mt = wt("microwave", s); tf = wt("two", s)
    k = back_out((T - s - 0.5) / 0.5)
    LIB.place(img, "wifi_objects", "microwave", 470, 1260, height=300 * clamp(k, 0, 1.1), a=a * clamp(k * 2))
    label(img, "~2.45 GHz", 1290, C24_L, label_in(T, tf, e), 470)
    R.chrome(img, T)
    title(img, T, s, e, "Now the weird part")
    return R.punch(img, T, mt, amt=0.05)
V.sounds("twist", [(0.05, "sparkle", 0.9), (rel("twist", "microwave"), "pop", 0.8), (rel("twist", "two"), "click", 0.7)])

@V.scene("inside")
def _(img, T, t, s, e):
    a = win(T, s, e)
    it = wt("inside", s); hu = wt("Heat", s); sn = wt("stutter", s); nz = wt("noise", s)
    if T < hu - 0.15:
        aa_ = a
        def fn(d, P, s_):
            d.rounded_rectangle([P(120, 960), P(840, 1080)], radius=22 * s_, fill=(206, 196, 164), outline=INK_T, width=int(5 * s_))
            d.rounded_rectangle([P(300, 960), P(660, 1080)], radius=0, fill=C24, outline=INK_T, width=int(5 * s_))
        aa(img, (100, 940, 860, 1100), fn, aa_)
        label(img, "2.4 GHz band", 880, C24_D, aa_ * clamp((T - s - 0.3) / 0.3), 480)
        pk = back_out((T - it) / 0.4)
        def pin(d, P, s_):
            circ(d, P, 480, 1020, 28 * clamp(pk, 0, 1.1), (255, 255, 255)); circ(d, P, 480, 1020, 16 * clamp(pk, 0, 1.1), RED_T)
        aa(img, (420, 980, 540, 1060), pin, aa_ * clamp(pk * 2))
        LIB.place(img, "wifi_objects", "microwave", 480, 1235, height=140, a=aa_ * clamp(pk))
        label(img, "microwave", 1255, INK_T, aa_ * label_in(T, it, hu), 480)
        title(img, T, s, hu - 0.2, "Right inside the band")
    else:
        alt = int((T * 6) % 2)
        LIB.place(img, "wifi_objects", "microwave_open2" if alt else "microwave_open", 250, 1290, height=210, a=a)
        LIB.place(img, "wifi_objects", "laptop", 690, 1290, height=190, a=a)
        def zig(d, P, s_):       # ruido de radio: líneas rotas que van del microondas al portátil
            for j in range(3):
                pts = []
                for i in range(0, 17):
                    x = 360 + i * 20; y = 1120 + 20 * j + (22 if (i + int(T * 14) + j) % 2 else -22)
                    pts.append(P(x, y))
                d.line(pts, fill=RED_T, width=int(7 * s_), joint="curve")
        aa(img, (340, 1040, 700, 1260), zig, a * clamp((T - nz + 0.2) / 0.3))
        spinner(img, 690, 1060, 36, T, C5_D, a * clamp((T - sn + 0.6) / 0.3))
        label(img, "radio noise", 900, RED_T, a * label_in(T, nz, e), 360)
        label(img, "Wi-Fi stutters", 1330, INK_T, a * label_in(T, sn, e), 560)
        title(img, T, hu - 0.1, e, "Lunch break lag")
    R.chrome(img, T)
V.sounds("inside", [(0.05, "whoosh", 0.6), (rel("inside", "inside"), "pop", 0.8), (rel("inside", "Heat"), "whoosh", 0.7), (rel("inside", "noise"), "click", 0.6), (rel("inside", "stutter"), "bubble", 0.7)])

@V.scene("others")
def _(img, T, t, s, e):
    a = win(T, s, e)
    bt = wt("Bluetooth", s); cd = wt("cordless", s); sh = wt("share", s); hn = wt("Honestly", s)
    def box(d, P, s_):
        d.rounded_rectangle([P(110, 860), P(850, 1250)], radius=30 * s_, fill=(255, 226, 170), outline=C24_D, width=int(8 * s_))
    aa(img, (90, 840, 870, 1270), box, a)
    label(img, "same 2.4 GHz band", 800, C24_D, a * clamp((T - sh + 0.3) / 0.3), 480)
    bluetooth(img, 230, 1060, 70, (40, 90, 200), a * clamp(back_out((T - bt) / 0.4)))
    cordless(img, 480, 1070, 100, a * clamp(back_out((T - cd) / 0.4)))
    LIB.place(img, "wifi_objects", "microwave", 730, 1180, height=110, a=a * clamp(back_out((T - s - 0.1) / 0.4)))
    label(img, "Bluetooth", 1280, INK_T, a * label_in(T, bt, e), 230)
    label(img, "cordless phones", 1280, INK_T, a * label_in(T, cd, e), 560)
    k = clamp((T - hn) / 0.3)
    LIB.place(img, "young_man", "happy" if k > 0 else "front", 860, 1360, height=230, a=a * clamp((T - hn + 0.4) / 0.3))
    R.chrome(img, T)
    title(img, T, s, e, "A crowded band")
V.sounds("others", [(0.05, "whoosh", 0.6), (rel("others", "Bluetooth"), "pop", 0.7), (rel("others", "cordless"), "pop", 0.7), (rel("others", "Honestly"), "sparkle", 0.7)])

@V.scene("final")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sc = wt("score", s); fv = wt("five", s); two = wt("two", s); one = wt("one", s)
    def tiles(d, P, s_):
        d.rounded_rectangle([P(110, 900), P(470, 1200)], radius=30 * s_, fill=C5, outline=INK_T, width=int(7 * s_))
        d.rounded_rectangle([P(510, 900), P(870, 1200)], radius=30 * s_, fill=C24, outline=INK_T, width=int(7 * s_))
    aa(img, (90, 880, 890, 1220), tiles, a * clamp((T - s) / 0.3))
    label(img, "5 GHz", 830, C5_D, a * clamp((T - fv + 0.2) / 0.3), 290)
    label(img, "2.4 GHz", 830, C24_D, a * clamp((T - fv + 0.2) / 0.3), 690)
    n5 = "2" if T >= two else "0"; n24 = "1" if T >= one else "0"
    R.put_text(img, R.sprite(n5, "number", (255, 255, 255)), 290, 1050, a, "mm", text=n5)
    R.put_text(img, R.sprite(n24, "number", (255, 255, 255)), 690, 1050, a, "mm", text=n24)
    R.chrome(img, T)
    title(img, T, s, e, "Final score")
    return R.punch(img, T, two, amt=0.05)
V.sounds("final", [(0.05, "whoosh", 0.6), (rel("final", "two"), "click", 0.8), (rel("final", "one"), "click", 0.8), (rel("final", "wins"), "sparkle", 0.7)])

@V.scene("take")
def _(img, T, t, s, e):
    a = win(T, s, e)
    fv = wt("five", s); fr = wt("far", s)
    house(img, T, a, furniture=False, far_thing=False)
    LIB.place(img, "wifi_objects", "phone", 330, 1285, height=150, a=a)
    LIB.place(img, "wifi_objects", "laptop", 730, 1285, height=150, a=a)
    def fn(d, P, s_):
        arcs(d, P, s_, RX, RY, 50, 230, 30, T * 80, C5, (-35, 35), w=8, fade=0.9)
        arcs(d, P, s_, RX + 60, RY - 40, 230, 600, 70, T * 80, C24, (-18, 18), w=9, fade=0.4)
    aa(img, (140, 800, 900, 1290), fn, a)
    label(img, "near: 5 GHz", 800, C5_D, a * label_in(T, fv, e), 330)
    label(img, "far: 2.4 GHz", 800, C24_D, a * label_in(T, fr, e), 680)
    R.chrome(img, T)
    title(img, T, s, e, "My take: use both")
V.sounds("take", [(0.05, "whoosh", 0.6), (rel("take", "five"), "pop", 0.7), (rel("take", "far"), "pop", 0.7)])

@V.scene("close")
def _(img, T, t, s, e):
    a = win(T, s, e)
    fz = wt("freezes", s); pp = wt("popcorn", s); ck = wt("check", s)
    LIB.place(img, "wifi_objects", "microwave_open2" if int(T * 6) % 2 else "microwave_open", 260, 1280, height=240, a=a)
    popcorn(img, T, 260, 1100, a * clamp((T - pp + 0.3) / 0.3))
    LIB.place(img, "wifi_objects", "laptop", 700, 1280, height=200, a=a)
    spinner(img, 700, 1080, 38, T, C24_D, a * clamp((T - fz + 0.2) / 0.3))
    label(img, "check the microwave", 1300, B.TEXT, a * label_in(T, ck, e), 470)
    R.chrome(img, T)
    title(img, T, s, e, "Stream frozen?")
    return R.flash(img, T, ck, strength=0.25)
V.sounds("close", [(0.05, "whoosh", 0.6), (rel("close", "freezes"), "bubble", 0.7), (rel("close", "popcorn"), "pop", 0.8), (rel("close", "check"), "sparkle", 0.8)])

# ---------- fondos ----------
V.backdrop("hook")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="city", seed=2))
for n in ("translate", "speed", "fly", "range", "meanwhile", "crowd", "picture", "twenty", "inside", "others", "final", "take"):
    V.backdrop(n)(card_bg)

@V.backdrop("twist")
def _(img, T, t):
    ST.landscape(img, T, sky_kind="dusk", terrain="city", seed=5)
    ST.wow_moment(img, T, V.sc["twist"][0] + 0.05, R.cat, "glitch", dur=1.4)

V.backdrop("close")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="city", seed=9))

if __name__ == "__main__":
    V.main()
