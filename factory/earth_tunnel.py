"""Reel: What if you dug a hole straight through the Earth and jumped in? Mr. Whiskerfact, categoría Science,
formato what-if. Voz de Brad. Experimento B1-hook-style, opción `statement`.

Fuentes (dos por dato): ver voice/earth_tunnel_claims.md
- Caída por un túnel sin aire a través del centro: ~38 min con la densidad real de la Tierra (42 min si fuese uniforme):
  Klotz, Am. J. Phys. 83, 231 (2015) https://arxiv.org/abs/1308.1342 ; Live Science
  https://www.livescience.com/50312-how-long-to-fall-through-earth.html
- Pozo más profundo ~12 km (Kola); centro a ~6.371 km: ScienceAlert; NASA Earth Fact Sheet
- La gravedad sube ~9 % bajo la superficie (máx. ~1,09 g); velocidad máxima ~8 km/s en el modelo simple: Klotz (2015)
- Con aire, un vehículo aerodinámico tardaría ~1,8 años en llegar al centro; el movimiento se amortigua:
  Concannon & Giordano, Gravity Tunnel Drag (2016) https://arxiv.org/
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("science")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "earth_tunnel", [
    ("hook", "Through"), ("imagine", "Imagine"), ("reality", "Reality"), ("jump", "Jump"), ("stronger", "Weirdly"),
    ("speed", "Halfway"), ("back", "Then"), ("pop", "After"), ("swing", "Unless"), ("air", "But"),
    ("drag", "Drag"), ("teaches", "What"), ("wrap", "So"), ("final", "Dead")])

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (36, 80, 150)
TRAV = (232, 64, 40)          # el viajero: punto rojo
TRAV_L = (255, 226, 150)
UNI = (222, 160, 96)          # Tierra uniforme (un solo color)
IT = "earth_tunnel_items"

def wt(word, s): return V.word_time(word, after=s)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]

# ---------- utilidades ----------
def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def sprite(img, name, pose, x, y, size, a=1.0, anchor="center", flip=False, rot=0.0):
    LIB.place(img, name, pose, x, y, height=size, a=a, anchor=anchor, flip=flip, rot=rot)

def dot(img, x, y, a=1.0, r=17, glow=0.0):
    """el viajero: punto rojo con borde claro; glow (0-1) añade un halo dorado"""
    def fn(d, P, s):
        if glow > 0:
            for k in range(5, 0, -1):
                rr = r + 8 * k
                d.ellipse([P(x - rr, y - rr), P(x + rr, y + rr)], fill=(255, 214, 120, int(34 * glow)))
        d.ellipse([P(x - r - 4, y - r - 4), P(x + r + 4, y + r + 4)], fill=(255, 250, 235))
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=TRAV)
    aa(img, (x - r - 60, y - r - 60, x + r + 60, y + r + 60), fn, a)

def lab(img, text, y, col, a, x=W / 2, style="label"):
    R.txt(img, text, y, style, col, a, x=x, rise=False)

def title(img, T, s, e, text, color=B.TEXT, y=TITLE_Y, delay=0.0):
    R.txt(img, text, y, "title", color, win(T, s + delay, e))

def cutaway(img, cx, cy, size, a=1.0):
    sprite(img, IT, "earth_cutaway", cx, cy, size, a)

def trav_y(cy, size, u):
    """u en [-1, 1]: -1 = salida de arriba, 0 = centro, 1 = salida de abajo"""
    return cy + u * 0.455 * size

def arrow_up(img, x, y, size, a=1.0):
    sprite(img, IT, "arrow_down", x, y, size, a, rot=180)

CARD = (56, 742, 1024, 1384)
def card_bg(img, T, t): ST.card(img, CARD)

# =====================================================================  ESCENAS
@V.scene("hook")
def _(img, T, t, s, e):
    cx, cy, size = CX - 20, 1090, 560
    cutaway(img, cx, cy, size)
    u = -1 + 2 * eio(((T * 0.55) % 1.0))            # el viajero cae sin parar por el túnel
    dot(img, cx, trav_y(cy, size, u), 1.0, glow=0.5)
    k = eo((t - 0.3) / 0.35)
    lab(img, "38 min", 1370 - 10, B.TEXT, clamp(k), x=CX - 20)
    R.chrome(img, T)
    V.hook_text(img, T, e, "Airless tunnel through Earth:", "38 minutes. Where do you stop?", "stop")
    R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.7), (0.9, "whoosh", 0.5)])

@V.scene("imagine")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = 330, 1060, 460
    cutaway(img, cx, cy, size, a)
    items = (("heat", "no heat", 900), ("spin", "no spin", 1010), ("gravity", "just gravity", 1120))
    for w, text, y in items:
        k = back_out((T - wt(w, s) + 0.1) / 0.35)
        if k > 0: lab(img, text, y, INK_T, a * clamp(k), x=730)
    R.chrome(img, T)
    title(img, T, s, e, "A perfect tunnel")
V.sounds("imagine", [(0.1, "whoosh", 0.6)] + [(wt(w, V.sc["imagine"][0]) - V.sc["imagine"][0], "pop", 0.6) for w in ("heat", "spin", "gravity")])

@V.scene("reality")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = 400, 1070, 480
    cutaway(img, cx, cy, size, a)
    top = cy - 0.455 * size
    tw, ts6 = wt("twelve", s), wt("six", s)
    k1 = eo((T - tw + 0.1) / 0.4)
    if k1 > 0:                                       # la muesca de 12 km (el pozo más profundo), muy pequeña
        def fn(d, P, s_):
            d.polygon([P(cx - 7, top - 6), P(cx + 7, top - 6), P(cx, top + 22)], fill=RED_T)
        aa(img, (cx - 20, top - 14, cx + 20, top + 30), fn, a * clamp(k1))
        lab(img, "12 km: deepest hole", 765, INK_T, a * clamp(k1), x=CX)
    k2 = eio((T - ts6) / 1.4)
    if k2 > 0:                                       # el radio hasta el centro
        def fn2(d, P, s_):
            y1 = lerp(top + 28, cy, k2)
            d.line([P(cx + 70, top + 28), P(cx + 70, y1)], fill=RED_T, width=int(8 * s_))
            d.polygon([P(cx + 56, y1 - 4), P(cx + 84, y1 - 4), P(cx + 70, y1 + 20)], fill=RED_T)
        aa(img, (cx + 40, top, cx + 100, cy + 40), fn2, a)
        lab(img, "6,400 km", 1250, RED_T, a * clamp(k2 * 2), x=cx + 250)
        lab(img, "to the center", 1310, INK_T, a * clamp(k2 * 2), x=cx + 250)
    R.chrome(img, T)
    title(img, T, s, e, "Reality check")
V.sounds("reality", [(0.1, "tap", 0.6), (rel("reality", "twelve"), "click", 0.7), (rel("reality", "six"), "whoosh", 0.6)])

@V.scene("jump")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, IT, "hole_entry", CX - 20, 1180, 360, a, anchor="center")
    fall = eio((t - 0.35) / 1.1)                      # salta y cae al pozo
    hop = 0.0 if t < 0.35 else math.sin(clamp((t - 0.35) / 1.1) * math.pi) * 0.4
    if fall < 1.0:
        sc = 1.0 - 0.55 * fall
        gy = 1070 - 75 * hop + 120 * fall
        pose = "jump" if fall < 0.6 else "scared"
        LIB.place(img, "child_girl", pose, CX - 40, gy, height=290 * sc, a=1.0 - fall ** 3, anchor="bottom")
    sp = wt("speed", s)
    k = back_out((T - sp + 0.1) / 0.4)
    if k > 0:
        sprite(img, IT, "arrow_down", 800, 980 + 14 * math.sin(T * 5), 180 * clamp(k, 0, 1.15), a)
        lab(img, "faster and faster", 1130, B.TEXT, a * clamp(k), x=770)
    R.chrome(img, T)
    title(img, T, s, e, "Jump!")
V.sounds("jump", [(0.0, "whoosh", 0.7), (0.4, "pop", 0.7), (1.4, "whoosh", 0.6)])

@V.scene("stronger")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = 250, 1060, 400
    cutaway(img, cx, cy, size, a)
    u = -0.92 + 0.92 * eio(t / 3.4)                  # baja hacia el interior
    dot(img, cx, trav_y(cy, size, min(u, 0.0)), a)
    # medidor de gravedad: sube hasta +9 %
    mx, my0, mh = 560, 1280, 400
    nine = wt("nine", s)
    g = eo((T - nine + 0.3) / 0.9)
    def fn(d, P, s_):
        d.rounded_rectangle([P(mx - 38, my0 - mh), P(mx + 38, my0)], radius=18 * s_, fill=(214, 206, 170), outline=INK_T, width=int(5 * s_))
        fh = (mh - 18) * (0.2 + 0.55 * g)
        d.rounded_rectangle([P(mx - 28, my0 - 10 - fh), P(mx + 28, my0 - 10)], radius=12 * s_, fill=lerpc((90, 160, 236), (232, 64, 40), g))
    aa(img, (mx - 60, my0 - mh - 20, mx + 60, my0 + 20), fn, a)
    lab(img, "gravity", my0 + 10, INK_T, a, x=mx)
    lab(img, "+9 %", 1000, RED_T, a * clamp(g * 2), x=mx + 150)
    th = wt("checked", s)
    LIB.place(img, "scientist", "think" if T > th else "surprised", 800, 1350, height=380, a=a)
    R.chrome(img, T)
    title(img, T, s, e, "Gravity gets stronger")
V.sounds("stronger", [(0.1, "tap", 0.6), (rel("stronger", "nine"), "pop", 0.8), (rel("stronger", "checked"), "click", 0.6)])

@V.scene("speed")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = CX - 60, 1050, 500
    cutaway(img, cx, cy, size, a)
    reach = eio(t / 1.6)
    dy = trav_y(cy, size, -1 + reach)
    for k in range(6):                                # estelas de velocidad cuando llega al centro
        if reach > 0.2:
            def fn(d, P, s_, k=k):
                d.line([P(cx + (k - 2.5) * 10, dy - 40 - 30 * k), P(cx + (k - 2.5) * 10, dy - 130 - 30 * k)], fill=(255, 250, 235, 200), width=int(5 * s_))
            aa(img, (cx - 80, dy - 330, cx + 80, dy - 20), fn, a * clamp((reach - 0.2) * 2) * 0.7)
    dot(img, cx, dy, a, glow=clamp(reach))
    e8 = wt("eight", s)
    lab(img, "~8 km/s", 765, RED_T, a * clamp((T - e8 + 0.1) / 0.3), x=CX)
    sat = wt("Satellite", s)
    lab(img, "satellite speed", 1300, INK_T, a * clamp((T - sat + 0.1) / 0.3), x=CX - 20)
    R.chrome(img, T)
    title(img, T, s, e, "Top speed at the center")
    return R.punch(img, T, s + 1.5)
V.sounds("speed", [(0.0, "whoosh", 0.8), (1.5, "pop", 0.7), (rel("speed", "eight"), "click", 0.7), (rel("speed", "Satellite"), "sparkle", 0.6)])

@V.scene("back")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = CX - 60, 1050, 500
    cutaway(img, cx, cy, size, a)
    prog = 1 - (1 - clamp(t / (e - s)) ) ** 2.2       # sube frenando: se acerca a la salida despacio
    dot(img, cx, trav_y(cy, size, -0.98 * prog), a)
    for i in range(3):
        arrow_up(img, cx + 190, 1180 - i * 110 + 6 * math.sin(T * 4 + i), 100, a * 0.9)
    lab(img, "slowing down", 1300, INK_T, a * clamp((t - 0.6) / 0.3), x=CX - 40)
    R.chrome(img, T)
    title(img, T, s, e, "Gravity pulls you back")
V.sounds("back", [(0.1, "whoosh", 0.6), (1.4, "tap", 0.5)])

@V.scene("pop")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, IT, "stopwatch", 250, 1090, 330, a)
    t38 = wt("thirty-eight", s)
    hand = clamp((T - s) / max(0.1, (t38 - s)))
    def fn(d, P, s_):                                 # aguja que da la vuelta hasta 38 min
        cx_, cy_ = 250, 1100
        an = -math.pi / 2 + hand * 2 * math.pi * 0.63
        d.line([P(cx_, cy_), P(cx_ + math.cos(an) * 95, cy_ + math.sin(an) * 95)], fill=RED_T, width=int(9 * s_))
        d.ellipse([P(cx_ - 12, cy_ - 12), P(cx_ + 12, cy_ + 12)], fill=RED_T)
    aa(img, (100, 950, 400, 1250), fn, a)
    lab(img, "38 min", 1290, RED_T, a * clamp((T - t38 + 0.1) / 0.3), x=250)
    cx, cy, size = 690, 1090, 420
    cutaway(img, cx, cy, size, a)
    pr = eio((T - s - 0.2) / max(0.5, (t38 - s)))
    dot(img, cx, trav_y(cy, size, -1 + 2 * clamp(pr) + 0.0), a)
    pop = wt("pop", s)
    k = back_out((T - pop) / 0.35)
    if k > 0:
        lab(img, "other side!", 1300, INK_T, a * clamp(k), x=cx)
    R.chrome(img, T)
    title(img, T, s, e, "Out the other side")
    return R.punch(img, T, pop)
V.sounds("pop", [(0.1, "whoosh", 0.6), (rel("pop", "thirty-eight"), "click", 0.7), (rel("pop", "pop"), "pop", 0.9)])

@V.scene("swing")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = CX - 60, 1050, 500
    cutaway(img, cx, cy, size, a)
    u = math.cos(t * 2 * math.pi / 2.6) * 0.98         # va y viene por el túnel
    dot(img, cx, trav_y(cy, size, u), a, glow=0.3)
    lab(img, "again and again", 1300, INK_T, a * clamp((T - wt("again", s) + 0.1) / 0.3), x=CX - 40)
    R.chrome(img, T)
    title(img, T, s, e, "Back and forth")
V.sounds("swing", [(0.1, "whoosh", 0.6), (1.3, "tap", 0.5), (2.6, "tap", 0.5)])

@V.scene("air")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = 330, 1090, 460
    cutaway(img, cx, cy, size, a)
    rng = np.random.default_rng(5)
    def fn(d, P, s_):                                  # partículas de aire dentro del túnel
        for i in range(26):
            yy = cy - 0.44 * size + ((rng.uniform(0, 0.88) * size + T * 20 * (1 + (i % 3))) % (0.88 * size))
            xx = cx + rng.uniform(-9, 9)
            d.ellipse([P(xx - 3, yy - 3), P(xx + 3, yy + 3)], fill=(255, 255, 255, 190))
    aa(img, (cx - 30, cy - 0.46 * size, cx + 30, cy + 0.46 * size), fn, a)
    slow = eio(t / 5.0)
    dot(img, cx, trav_y(cy, size, -0.96 + 0.18 * slow), a)       # avanza muy despacio
    one = wt("one", s)
    k = back_out((T - one + 0.1) / 0.4)
    lab(img, "~1.8 years", 800, RED_T, a * clamp(k), x=720)
    lab(img, "streamlined vehicle", 870, INK_T, a * clamp(k), x=720)
    lab(img, "to the center", 940, INK_T, a * clamp(k), x=720)
    sw = wt("study", s)
    LIB.place(img, "scientist", "point" if T > sw else "talk", 800, 1360, height=300, a=a * clamp((T - s) / 0.4))
    R.chrome(img, T)
    title(img, T, s, e, "Now add air")
V.sounds("air", [(0.1, "whoosh", 0.6), (rel("air", "one"), "click", 0.7)])

@V.scene("drag")
def _(img, T, t, s, e):
    a = win(T, s, e)
    cx, cy, size = CX - 60, 1050, 500
    cutaway(img, cx, cy, size, a)
    amp = 0.55 * math.exp(-t / 1.6)                     # oscilación amortiguada hasta quedarse en el centro
    u = amp * math.cos(t * 2 * math.pi / 1.7)
    dot(img, cx, trav_y(cy, size, u), a, glow=clamp((t - 3.4) / 1.0))
    lab(img, "stops at the center", 1300, INK_T, a * clamp((T - wt("stop", s) + 0.1) / 0.3), x=CX - 40)
    R.chrome(img, T)
    title(img, T, s, e, "Drag kills the swing")
V.sounds("drag", [(0.1, "tap", 0.6), (0.9, "tap", 0.4), (1.8, "tap", 0.3), (2.6, "tap", 0.25)])

@V.scene("teaches")
def _(img, T, t, s, e):
    a = win(T, s, e)
    r = 150
    def disc(d, P, s_, x, layered):
        d.ellipse([P(x - r - 6, 1000 - r - 6), P(x + r + 6, 1000 + r + 6)], fill=INK_T)
        d.ellipse([P(x - r, 1000 - r), P(x + r, 1000 + r)], fill=UNI)
    aa(img, (60, 820, 460, 1180), lambda d, P, s_: disc(d, P, s_, 260, False), a * clamp((T - s) / 0.4))
    cutaway(img, 700, 1000, 2 * r + 10, a * clamp((T - wt("Our", s) + 0.3) / 0.4))
    k42 = wt("forty-two", s); k38 = wt("thirty-eight", s)
    lab(img, "even Earth", 1190, INK_T, a * clamp((T - s - 0.3) / 0.4), x=260)
    lab(img, "42 min", 1255, RED_T, a * clamp((T - k42 + 0.1) / 0.3), x=260)
    lab(img, "real Earth", 1190, INK_T, a * clamp((T - wt("Our", s)) / 0.4), x=700)
    lab(img, "38 min", 1255, RED_T, a * clamp((T - k38 + 0.1) / 0.3), x=700)
    R.chrome(img, T)
    title(img, T, s, e, "Mass spread matters")
V.sounds("teaches", [(0.1, "whoosh", 0.6), (rel("teaches", "forty-two"), "click", 0.7), (rel("teaches", "thirty-eight"), "click", 0.7)])

def finale(img, T, t, s, e):
    a = win(T, s, e + 1)
    sprite(img, IT, "hole_entry", 600, 1180, 360, a)
    R.chrome(img, T)
    R.txt(img, "Now you know:", TITLE_Y, "title", B.TEXT_2, win(T, V.sc["wrap"][0], V.outro_at + 1))
    R.txt(img, "you'd end up at the center", TITLE_Y + 97, "title", ACC_T, win(T, V.sc["wrap"][0] + 0.8, V.outro_at + 1))

@V.scene("wrap")
def _(img, T, t, s, e):
    finale(img, T, t, s, e)
    LIB.place(img, "child_girl", "think", 250, 1330, height=420, squash=(1.0, 1.0 + 0.01 * math.sin(T * 2.5)))
    return R.flash(img, T, s + 0.2, strength=0.2)
V.sounds("wrap", [(0.05, "whoosh", 0.7)])

@V.scene("final")
def _(img, T, t, s, e):
    finale(img, T, t, s, e)
    LIB.place(img, "child_girl", "happy" if t > 0.5 else "shrug", 250, 1330, height=420, squash=(1.0, 1.0 + 0.01 * math.sin(T * 2.5)))
    return R.punch(img, T, s)
V.sounds("final", [(0.05, "pop", 0.7), (0.9, "sparkle", 0.7)])

# ---------- fondos ----------
def space(img, T, t, seed=11):
    ST.sky(img, (10, 8, 34), (34, 22, 70), 0, H); ST.stars(img, T, 110, seed=seed, y1=H - 200)

V.backdrop("hook")(space)
for n in ("imagine", "reality", "stronger", "speed", "back", "pop", "swing", "air", "drag", "teaches"):
    V.backdrop(n)(card_bg)
V.backdrop("jump")(lambda img, T, t: ST.landscape(img, T, sky_kind="day", terrain="hills", seed=2))
for n in ("wrap", "final"): V.backdrop(n)(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="hills", seed=3))

if __name__ == "__main__":
    V.main()
