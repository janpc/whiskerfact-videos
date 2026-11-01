"""Reel: Pop quiz: what's the hottest planet in our solar system? Mr. Whiskerfact, formato quiz, categoría Space. Voz de Brad.

Fuentes (dos por dato): ver voice/hottest_planet_claims.md
- Venus es el planeta más caliente, no Mercurio: NASA (Mercury facts); NASA Space Place; RMG
- Mercurio: 430 °C de día, -180 °C de noche, casi sin atmósfera, el calor escapa al espacio: NASA; The Conversation (USC); Live Science
- Venus: aire casi todo CO2, presión ~90 veces la de la Tierra, efecto invernadero, >450 °C día y noche, funde el plomo:
  The Conversation (USC); RMG; Sky at Night; NASA Space Place; Live Science
- Un giro de Venus (243 días) dura más que su año (225 días): RMG; NASA Space Place
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("space")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, "hottest_planet", [
    ("hook", "Pop"), ("options", "A"), ("clock", "Comment"), ("reveal", "It's"), ("mercury", "Mercury"),
    ("noair", "But"), ("drops", "and"), ("venus", "Venus's"), ("sunlight", "Sunlight"), ("blanket", "Carbon"),
    ("greenhouse", "Scientists"), ("result", "The"), ("footnote", "Footnote"), ("wrap", "So"), ("final", "but")])

# ---------- paleta del dibujo ----------
MERC = (150, 146, 150); MERC_D = (104, 100, 108); MERC_C = (124, 120, 126)
VEN = (236, 196, 120); VEN_D = (206, 156, 84); VEN_L = (250, 224, 160)
MARS = (206, 96, 60); MARS_D = (160, 66, 44)
SUN = (255, 196, 64); SUN_L = (255, 232, 140)
HEAT = (232, 64, 40)
COLD = (90, 160, 236)
INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (36, 80, 150)
CO2_C = (60, 60, 64); CO2_O = (214, 70, 60)
LEAD = (126, 132, 146); LEAD_L = (176, 182, 196)
GROUND_V = (150, 80, 44)

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
def label_in(T, at, e):
    """entra con su palabra, pero nunca tan tarde que no dé tiempo a leerla (>= 1,9 s)"""
    return clamp((T - min(at, e - 1.9)) / 0.3)
def label(img, text, y, color, a, x):
    R.txt(img, text, y, "label", color, a, x=x, rise=False)

# ---------- planetas ----------
def planet(img, x, y, r, kind, a=1.0, T=0.0, lit=None, glow=0.0):
    """planeta plano con textura. kind: mercury | venus | mars.
    lit: None = todo iluminado; si no, ángulo (rad) hacia el Sol: la otra mitad queda en sombra."""
    if a <= 0.003 or r < 2: return
    def fn(d, P, s):
        if glow > 0:
            for k in range(4):
                rr = r * (1.12 + 0.12 * k)
                circ(d, P, x, y, rr, (255, 170, 80, int(60 * glow * (1 - k / 4))))
        if kind == "mercury":
            circ(d, P, x, y, r, MERC)
            for ox, oy, rr in ((-0.35, -0.3, 0.18), (0.3, 0.15, 0.22), (-0.1, 0.45, 0.12), (0.45, -0.4, 0.1), (-0.5, 0.2, 0.1)):
                circ(d, P, x + ox * r, y + oy * r, rr * r, MERC_C)
                circ(d, P, x + ox * r + 0.03 * r, y + oy * r + 0.03 * r, rr * r * 0.7, MERC_D)
        elif kind == "venus":
            circ(d, P, x, y, r, VEN)
            for k, (oy, hh) in enumerate(((-0.62, 0.1), (-0.28, 0.12), (0.08, 0.1), (0.42, 0.12), (0.72, 0.07))):   # bandas de nubes que fluyen
                top, bot = [], []
                for i in range(41):
                    u = -1 + 2 * i / 40
                    lim = math.sqrt(max(0.0, 1 - u * u))
                    wob = 0.05 * math.sin(u * 5 + T * 1.2 + k * 1.7)
                    ya, yb = max(oy - hh + wob, -lim), min(oy + hh + wob, lim)
                    if ya < yb: top.append(P(x + u * r, y + ya * r)); bot.append(P(x + u * r, y + yb * r))
                if len(top) > 2: d.polygon(top + bot[::-1], fill=VEN_D if k % 2 == 0 else VEN_L)
        else:
            circ(d, P, x, y, r, MARS)
            for ox, oy, rr in ((-0.3, 0.1, 0.25), (0.35, -0.2, 0.18), (0.1, 0.5, 0.15)):
                circ(d, P, x + ox * r, y + oy * r, rr * r, MARS_D)
            d.chord([P(x - 0.5 * r, y - 1.0 * r), P(x + 0.5 * r, y - 0.8 * r)], 0, 360, fill=(246, 240, 236))
        if lit is not None:   # sombra: media luna oscura del lado contrario al Sol
            m = Image.new("L", (int(4 * r * s) + 4, int(4 * r * s) + 4), 0)
            dm = ImageDraw.Draw(m)
            c = 2 * r * s + 2
            dm.ellipse([c - r * s, c - r * s, c + r * s, c + r * s], fill=200)
            ox, oy = math.cos(lit) * r * 0.55 * s, math.sin(lit) * r * 0.55 * s
            dm.ellipse([c + ox - 1.12 * r * s, c + oy - 1.12 * r * s, c + ox + 1.12 * r * s, c + oy + 1.12 * r * s], fill=0)
            px, py = P(x, y)
            d.bitmap((int(px - c), int(py - c)), m, fill=(20, 18, 40, 200))
    aa(img, (x - 1.7 * r, y - 1.7 * r, x + 1.7 * r, y + 1.7 * r), fn, a)

def sun(img, x, y, r, a=1.0, T=0.0):
    def fn(d, P, s):
        for k in range(12):
            an = k / 12 * 2 * math.pi + T * 0.4
            rr = r * (1.25 + 0.06 * math.sin(T * 4 + k))
            d.polygon([P(x + math.cos(an - 0.13) * r * 0.95, y + math.sin(an - 0.13) * r * 0.95),
                       P(x + math.cos(an) * rr, y + math.sin(an) * rr),
                       P(x + math.cos(an + 0.13) * r * 0.95, y + math.sin(an + 0.13) * r * 0.95)], fill=SUN)
        circ(d, P, x, y, r, SUN)
        circ(d, P, x - 0.2 * r, y - 0.2 * r, 0.55 * r, SUN_L)
    aa(img, (x - 1.4 * r, y - 1.4 * r, x + 1.4 * r, y + 1.4 * r), fn, a)

def thermometer(img, x, y0, y1, level, col, a=1.0):
    """termómetro vertical: bulbo abajo en y1, tubo hasta y0; level 0..1"""
    def fn(d, P, s):
        d.rounded_rectangle([P(x - 34, y0 - 10), P(x + 34, y1)], radius=34 * s, fill=(246, 244, 238))
        circ(d, P, x, y1, 62, (246, 244, 238))
        circ(d, P, x, y1, 46, col)
        top = lerp(y1 - 40, y0 + 20, clamp(level))
        d.rounded_rectangle([P(x - 18, top), P(x + 18, y1)], radius=18 * s, fill=col)
        for i in range(6):
            yy = lerp(y1 - 70, y0 + 30, i / 5)
            d.line([P(x + 34, yy), P(x + 58, yy)], fill=INK_T, width=int(5 * s))
    aa(img, (x - 70, y0 - 20, x + 70, y1 + 70), fn, a)

def wavy(d, P, s, x0, y0, x1, y1, col, w=8, amp=12, n=3.0, ph=0.0, head=True):
    """flecha ondulada (calor / infrarrojo) de (x0,y0) a (x1,y1)"""
    L = math.hypot(x1 - x0, y1 - y0) or 1; ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    pts = []
    for i in range(41):
        u = i / 40; o = amp * math.sin(u * n * 2 * math.pi + ph)
        pts.append(P(x0 + ux * L * u + nx * o, y0 + uy * L * u + ny * o))
    d.line(pts, fill=col, width=int(w * s), joint="curve")
    if head:
        hx, hy = x1, y1
        d.polygon([P(hx + ux * 22, hy + uy * 22), P(hx - ux * 6 + nx * 18, hy - uy * 6 + ny * 18), P(hx - ux * 6 - nx * 18, hy - uy * 6 - ny * 18)], fill=col)

def straight(d, P, s, x0, y0, x1, y1, col, w=10):
    L = math.hypot(x1 - x0, y1 - y0) or 1; ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    d.line([P(x0, y0), P(x1 - ux * 10, y1 - uy * 10)], fill=col, width=int(w * s))
    d.polygon([P(x1 + ux * 20, y1 + uy * 20), P(x1 - ux * 8 + nx * 18, y1 - uy * 8 + ny * 18), P(x1 - ux * 8 - nx * 18, y1 - uy * 8 - ny * 18)], fill=col)

def co2(d, P, s, x, y, k=1.0, rot=0.0):
    """molécula O=C=O"""
    r = 20 * k
    for sg in (-1, 1):
        circ(d, P, x + sg * math.cos(rot) * 1.6 * r, y + sg * math.sin(rot) * 1.6 * r, r * 0.9, CO2_O)
    circ(d, P, x, y, r, CO2_C)

def paw(img, x, y, r, col, a=1.0):
    def fn(d, P, s):
        d.ellipse([P(x - r, y - 0.2 * r), P(x + r, y + r)], fill=col)
        for ox, oy in ((-0.95, -0.55), (-0.35, -0.95), (0.35, -0.95), (0.95, -0.55)):
            circ(d, P, x + ox * r, y + oy * r, 0.36 * r, col)
    aa(img, (x - 1.5 * r, y - 1.5 * r, x + 1.5 * r, y + 1.2 * r), fn, a)

def stamp(img, text, x, y, k, col=RED_T, rot=-6):
    """sello que cae de golpe; texto a tamaño final y giro pequeño (<= 8°), en la capa de etiquetas"""
    if k <= 0: return
    spr = R.sprite(text, "number", col)
    w, h = spr.size
    box = Image.new("RGBA", (w + 60, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle([4, 4, w + 56, h + 36], radius=22, fill=(246, 238, 214, 255), outline=col + (255,), width=12)
    box.alpha_composite(spr, (30, 20))
    box = box.rotate(rot, resample=Image.BICUBIC, expand=True)
    sc = 1 + 0.5 * (1 - eo(k))
    if sc > 1.01: box = box.resize((int(box.size[0] * sc), int(box.size[1] * sc)), Image.LANCZOS)
    R.put_text(img, box, x, y, clamp(k * 3), "mm", text=text)

ROW = [(250, "mercury", 70, "A · Mercury"), (500, "venus", 92, "B · Venus"), (750, "mars", 78, "C · Mars")]
HOOK_ROW = [(190, "mercury", 92), (470, "venus", 135), (760, "mars", 104)]

# ---------- escenas ----------
@V.scene("hook")
def _(img, T, t, s, e):
    for i, (x, k, r) in enumerate(HOOK_ROW):
        planet(img, x, 1120 + 12 * math.sin(T * 2.2 + i * 1.6), r, k, 1.0, T)
    def q(d, P, s_):     # ondas de calor sobre los tres: ¿cuál quema más?
        for i, (x, k, r) in enumerate(HOOK_ROW):
            for j in range(2):
                ph = T * 6 + j * 2 + i
                wavy(d, P, s_, x - 30 + 60 * j, 1120 - r - 30, x - 30 + 60 * j, 1120 - r - 120, HEAT, w=8, amp=10, n=1.5, ph=ph, head=False)
    aa(img, (60, 780, 920, 1010), q, 0.5 + 0.5 * clamp(T / 0.25))
    R.chrome(img, T)
    V.hook_text(img, T, e, "Pop quiz:", "Hottest planet in our solar system?", "hottest")
    R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.25, "whoosh", 0.5), (0.6, "pop", 0.8)])

def row(img, T, a, appear=(0, 0, 0), y=1060, sc=1.0, dim=(0, 0, 0), col=B.TEXT):
    for i, (x, k, r, lab) in enumerate(ROW):
        p = back_out(appear[i]) if appear[i] > 0 else 0
        if p <= 0: continue
        planet(img, x, y + 10 * math.sin(T * 2 + i), r * 1.3 * sc * clamp(p, 0, 1.2), k, a * (1 - 0.6 * dim[i]), T)
        label(img, lab, y + 135 * sc, col, a * clamp(appear[i] * 2) * (1 - 0.6 * dim[i]), x)

@V.scene("options")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ts = [wt("A", s), wt("B", s), wt("C", s)]
    row(img, T, 1.0, appear=tuple(clamp((T - x + 0.1) / 0.4) for x in ts))
    R.chrome(img, T)
    title(img, T, s, e, "Pick one")
V.sounds("options", [(rel("options", "A"), "pop", 0.8), (rel("options", "B"), "pop", 0.8), (rel("options", "C"), "pop", 0.8)])

@V.scene("clock")
def _(img, T, t, s, e):
    a = win(T, s, e)
    row(img, T, 1.0, appear=(1, 1, 1), y=860, sc=0.62, col=INK_T)
    t3, t2, t1 = wt("Three", s), wt("two", s), wt("one", s)
    k = back_out(t / 0.4)
    cx, cy, rr = 470, 1200, 140 * clamp(k, 0, 1.1)
    def fn(d, P, s_):
        circ(d, P, cx, cy, rr + 14, INK_T)
        circ(d, P, cx, cy, rr, (246, 244, 238))
        for i in range(12):
            an = i / 12 * 2 * math.pi
            d.line([P(cx + math.cos(an) * rr * 0.8, cy + math.sin(an) * rr * 0.8), P(cx + math.cos(an) * rr * 0.92, cy + math.sin(an) * rr * 0.92)], fill=INK_T, width=int(6 * s_))
        an = -math.pi / 2 + math.floor((T - s) * 2) / 2 * math.pi * 0.5    # aguja que avanza a saltos (tic, tac)
        d.line([P(cx, cy), P(cx + math.cos(an) * rr * 0.75, cy + math.sin(an) * rr * 0.75)], fill=RED_T, width=int(10 * s_))
        circ(d, P, cx, cy, 14, RED_T)
        for j, tj in enumerate((t3, t2, t1)):     # tres puntos que se encienden: 3, 2, 1
            on = clamp((T - tj) / 0.15)
            col = lerpc((90, 90, 110), HEAT, on)
            circ(d, P, cx + 220, cy - 90 + j * 90, 30 + 6 * on, col)
    aa(img, (cx - rr - 30, cy - rr - 30, cx + 280, cy + rr + 30), fn, a * clamp(k))
    R.chrome(img, T)
    title(img, T, s, e, "Comment your answer!")
ts_clock = [0.6 + 0.5 * i for i in range(7)]
V.sounds("clock", [(0.05, "whoosh", 0.6)] + [(x, "click", 0.5) for x in (rel("clock", "Three"), rel("clock", "two"), rel("clock", "one"))]
         + [(rel("clock", "your"), "click", 0.35), (rel("clock", "before"), "click", 0.35)])

@V.scene("reveal")
def _(img, T, t, s, e):
    a = win(T, s, e)
    vt = wt("Venus", s)
    k = back_out((T - s) / 0.5)
    planet(img, 480, 1040 + 8 * math.sin(T * 2), 185 * clamp(k, 0, 1.1), "venus", a, T, glow=0.6 + 0.4 * math.sin(T * 3) ** 2)
    stamp(img, "VENUS", 480, 1250, clamp((T - vt - 1.3) / 0.35))
    R.chrome(img, T)
    title(img, T, s, e, "It's Venus!")
    R.txt(img, "I checked twice", TITLE_Y + 110, "subtitle", ACC_T, win(T, wt("checked", s), e))
    return R.punch(img, T, vt + 1.3, amt=0.07)
V.sounds("reveal", [(0.0, "sparkle", 0.9), (rel("reveal", "Venus") + 1.3, "pop", 1.0), (rel("reveal", "checked"), "tap", 0.6)])

@V.scene("mercury")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ct = wt("closest", s); ht = wt("thirty", s)
    sun(img, 220, 1060, 150, a * eo(t / 0.4), T)
    u = eio(t / 1.2)
    planet(img, lerp(700, 470, u), 1060, 70, "mercury", a, T, lit=math.pi)
    def heat(d, P, s_):
        for j in range(3):
            ph = T * 7 + j
            wavy(d, P, s_, 400, 1000 + 60 * j, 400 - 0 * j, 1000 + 60 * j, HEAT, head=False)
    lvl = 0.25 + 0.7 * eio((T - wt("sunny", s)) / 1.6)
    thermometer(img, 720, 820, 1230, lvl, HEAT, a * clamp((T - wt("sunny", s) + 0.3) / 0.3))
    label(img, "closest to the Sun", 1250, B.TEXT, a * label_in(T, ct, e), 340)
    label(img, "430 °C by day", 790, B.TEXT, a * label_in(T, ht, e), 560)
    R.chrome(img, T)
    title(img, T, s, e, "Mercury: closest")
V.sounds("mercury", [(0.05, "whoosh", 0.6), (rel("mercury", "closest"), "pop", 0.7), (rel("mercury", "sunny"), "whoosh", 0.5), (rel("mercury", "thirty"), "click", 0.7)])

@V.scene("noair")
def _(img, T, t, s, e):
    a = win(T, s, e)
    nt = wt("night", s); et = wt("escapes", s)
    turn = eio((T - nt) / 1.0)            # el lado de noche gira hacia nosotros
    cx, cy, r = 470, 1090, 190
    planet(img, cx, cy, r, "mercury", a, T, lit=lerp(math.pi * 0.85, math.pi * 1.6, turn))
    def ring(d, P, s_):      # exosfera: apenas unos puntos sueltos, nada de manta
        for i in range(18):
            an = i / 18 * 2 * math.pi + T * 0.2
            circ(d, P, cx + math.cos(an) * (r + 30), cy + math.sin(an) * (r + 30), 5, (200, 210, 240))
    aa(img, (cx - r - 50, cy - r - 50, cx + r + 50, cy + r + 50), ring, a)
    ek = clamp((T - et + 0.3) / 0.4)
    if ek > 0:
        def esc(d, P, s_):
            for i in range(5):
                an = -math.pi / 2 + (i - 2) * 0.5
                u = ((T - et) * 0.7 + i * 0.2) % 1
                r0, r1 = r * 0.9 + u * 40, r + 60 + u * 60
                wavy(d, P, s_, cx + math.cos(an) * r0, cy + math.sin(an) * r0 * 0.9, cx + math.cos(an) * r1, cy + math.sin(an) * r1 * 0.9,
                     HEAT + (int(255 * (1 - u)),), w=8, amp=8, n=2, ph=T * 6)
        aa(img, (cx - r - 140, cy - r - 160, cx + r + 140, cy + 40), esc, a * ek)
    label(img, "almost no atmosphere", 1285, B.TEXT, a * clamp((t - 0.2) / 0.3), cx)
    label(img, "heat escapes", 790, (255, 190, 170), a * label_in(T, et, e), cx)
    R.chrome(img, T)
    title(img, T, s, e, "No blanket of air")
V.sounds("noair", [(0.05, "whoosh", 0.6), (rel("noair", "night"), "whoosh", 0.6), (rel("noair", "escapes"), "sparkle", 0.6)])

@V.scene("drops")
def _(img, T, t, s, e):
    a = win(T, s, e)
    mt = wt("minus", s)
    planet(img, 330, 1080, 170, "mercury", a, T, lit=math.pi * 1.6)
    def frost(d, P, s_):
        for i in range(7):
            an = i / 7 * 2 * math.pi + T * 0.5
            x, y = 330 + math.cos(an) * 205, 1080 + math.sin(an) * 205
            for k in range(3):
                b = an + k * math.pi / 3
                d.line([P(x - math.cos(b) * 16, y - math.sin(b) * 16), P(x + math.cos(b) * 16, y + math.sin(b) * 16)], fill=COLD, width=int(5 * s_))
    aa(img, (100, 850, 560, 1310), frost, a * clamp((T - mt + 0.3) / 0.5))
    lvl = lerp(0.9, 0.12, eio((t - 0.2) / 1.8))
    thermometer(img, 700, 820, 1230, lvl, lerpc(HEAT, COLD, eio((t - 0.2) / 1.8)), a)
    label(img, "−180 °C at night", 1305, BLUE_T, a * label_in(T, mt, e), 500)
    R.chrome(img, T)
    title(img, T, s, e, "Freezing nights")
V.sounds("drops", [(0.05, "whoosh", 0.6), (rel("drops", "minus"), "click", 0.8)])

@V.scene("venus")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ct = wt("carbon", s); pt = wt("pressure", s)
    def mols(d, P, s_):
        n = int(26 * clamp((T - ct + 0.3) / 1.2))
        rng = np.random.default_rng(4)
        for i in range(n):
            x0, y0 = rng.uniform(110, 860), rng.uniform(790, 1090)
            x = x0 + 18 * math.sin(T * 1.3 + i); y = y0 + 12 * math.cos(T * 1.1 + i * 2)
            co2(d, P, s_, x, y, 0.9, rot=T * 0.8 + i)
    aa(img, (70, 750, 910, 1140), mols, a)
    gk = eo((T - pt + 0.2) / 0.4)
    gx, gy, gr = 470, 1230, 120
    if gk > 0:
        def gauge(d, P, s_):
            circ(d, P, gx, gy, gr + 12, INK_T); circ(d, P, gx, gy, gr, (246, 244, 238))
            for i in range(9):
                an = math.pi * (1.0 + i / 8)
                d.line([P(gx + math.cos(an) * gr * 0.72, gy + math.sin(an) * gr * 0.72), P(gx + math.cos(an) * gr * 0.9, gy + math.sin(an) * gr * 0.9)], fill=INK_T, width=int(5 * s_))
            v = eio((T - pt) / 1.2)
            an = math.pi * (1.05 + 0.9 * v) + 0.03 * math.sin(T * 20) * v
            d.line([P(gx, gy), P(gx + math.cos(an) * gr * 0.8, gy + math.sin(an) * gr * 0.8)], fill=RED_T, width=int(9 * s_))
            circ(d, P, gx, gy, 14, RED_T)
        aa(img, (gx - gr - 20, gy - gr - 20, gx + gr + 20, gy + gr + 20), gauge, a * gk)
    label(img, "mostly CO₂", 790, B.TEXT, a * label_in(T, ct, e), 470)
    label(img, "~90× Earth's pressure", 1060, B.TEXT, a * label_in(T, pt, e), 470)
    R.chrome(img, T)
    title(img, T, s, e, "Venus: a thick CO₂ sky")
V.sounds("venus", [(0.05, "whoosh", 0.6), (rel("venus", "carbon"), "bubble", 0.7), (rel("venus", "pressure"), "whoosh", 0.6), (rel("venus", "ninety"), "click", 0.8)])

# cortes de la atmósfera de Venus (escenas sunlight / blanket / greenhouse), sobre la tarjeta crema
def cutaway(img, T, a, clouds=1.0):
    def fn(d, P, s_):
        d.rectangle([P(110, 1230), P(870, 1340)], fill=GROUND_V)                          # suelo
        for i in range(6):
            d.polygon([P(110 + i * 130, 1230), P(170 + i * 130, 1190 + (i % 2) * 15), P(240 + i * 130, 1230)], fill=(170, 96, 52))
        for k in range(3):                                                              # capa de nubes
            y = 900 + k * 26
            pts = [P(x, y + 12 * math.sin(x / 70 + T * 0.8 + k)) for x in range(110, 871, 20)]
            d.line(pts, fill=(222, 196, 140, int(255 * clouds)), width=int(26 * s_))
    aa(img, (100, 860, 880, 1350), fn, a)

@V.scene("sunlight")
def _(img, T, t, s, e):
    a = win(T, s, e)
    gt = wt("ground", s); it = wt("infrared", s)
    cutaway(img, T, a)
    def rays(d, P, s_):
        for i, x in enumerate((240, 470, 700)):
            u = clamp((T - s - i * 0.15) / 0.9)
            if i == 1:   # parte de la luz se refleja en las nubes
                straight(d, P, s_, x - 60, 780, lerp(x - 60, x - 30, u), lerp(780, 880, u), SUN, 9)
                if u >= 1: straight(d, P, s_, x - 30, 880, x + 10, 790, SUN + (180,), 7)
            else:
                straight(d, P, s_, x, 780, x + 40 * u, lerp(780, 1200, u), SUN, 10)
    aa(img, (120, 760, 860, 1240), rays, a)
    ik = clamp((T - it + 0.3) / 0.5)
    if ik > 0:
        def ir(d, P, s_):
            for x in (200, 740, 820):
                wavy(d, P, s_, x, 1210, x, lerp(1210, 1000, ik), HEAT, w=9, amp=12, n=2.5, ph=T * 6)
        aa(img, (200, 960, 860, 1240), ir, a)
    label(img, "sunlight", 790, INK_T, a * clamp((t - 0.2) / 0.3), 330)
    label(img, "infrared heat", 1110, RED_T, a * label_in(T, it, e), 430)
    R.chrome(img, T)
    title(img, T, s, e, "The ground glows with heat")
V.sounds("sunlight", [(0.05, "whoosh", 0.6), (rel("sunlight", "ground"), "pop", 0.6), (rel("sunlight", "infrared"), "sparkle", 0.6)])

def bouncing(d, P, s_, T, k, n=4):
    """flechas de calor que suben, chocan con el CO2 y vuelven al suelo"""
    for i in range(n):
        x = 220 + i * 180
        u = ((T * 0.8 + i * 0.27) % 1)
        if u < 0.5: y0, y1 = 1210, lerp(1210, 960, u * 2)
        else: y0, y1 = 960, lerp(960, 1210, (u - 0.5) * 2)
        wavy(d, P, s_, x + (0 if u < 0.5 else 40), y0, x + (0 if u < 0.5 else 40), y1, HEAT + (int(255 * k),), w=9, amp=10, n=2, ph=T * 6)

@V.scene("blanket")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tt = wt("traps", s); bt = wt("blanket", s)
    cutaway(img, T, a)
    def fn(d, P, s_):
        rng = np.random.default_rng(9)
        for i in range(14):
            x, y = rng.uniform(150, 830), rng.uniform(960, 1090)
            co2(d, P, s_, x + 10 * math.sin(T + i), y + 8 * math.cos(T * 1.2 + i), 0.8, rot=T + i)
        bouncing(d, P, s_, T, clamp((T - tt) / 0.4))
    aa(img, (120, 900, 860, 1240), fn, a)
    bk = eo((T - bt) / 0.6)
    if bk > 0:      # manta acolchada que cae sobre el aire
        def quilt(d, P, s_):
            y = lerp(840, 900, bk)
            d.rounded_rectangle([P(120, y - 50), P(860, y + 40)], radius=30 * s_, fill=(176, 56, 72))
            for x in range(170, 860, 90):
                d.line([P(x, y - 46), P(x, y + 36)], fill=(140, 40, 56), width=int(5 * s_))
        aa(img, (110, 700, 870, 930), quilt, a)
    label(img, "heat trapped", 1125, RED_T, a * label_in(T, tt, e), 470)
    R.chrome(img, T)
    title(img, T, s, e, "CO₂ traps the heat")
V.sounds("blanket", [(0.05, "whoosh", 0.5), (rel("blanket", "traps"), "pop", 0.7), (rel("blanket", "blanket"), "whoosh", 0.7)])

@V.scene("greenhouse")
def _(img, T, t, s, e):
    a = win(T, s, e)
    xt = wt("extreme", s)
    g = eio((T - s) / 2.5)
    planet(img, 400, 1070, 210, "venus", a, T, glow=0.3 + 0.7 * g)
    def ring(d, P, s_):     # el calor da vueltas dentro de la atmósfera, sin salir
        for i in range(6):
            an = T * 1.6 + i / 6 * 2 * math.pi
            r = 255
            x0, y0 = 400 + math.cos(an) * r, 1070 + math.sin(an) * r
            x1, y1 = 400 + math.cos(an + 0.45) * r, 1070 + math.sin(an + 0.45) * r
            straight(d, P, s_, x0, y0, x1, y1, HEAT, 8)
    aa(img, (100, 770, 700, 1370), ring, a)
    thermometer(img, 780, 830, 1240, lerp(0.4, 0.97, g), HEAT, a)
    R.chrome(img, T)
    title(img, T, s, e, "Extreme greenhouse effect", delay=0.0)
    return R.punch(img, T, xt)
V.sounds("greenhouse", [(0.05, "whoosh", 0.6), (rel("greenhouse", "extreme"), "pop", 0.8), (rel("greenhouse", "greenhouse"), "sparkle", 0.5)])

@V.scene("result")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ft = wt("fifty", s); dt = wt("day", s); nt = wt("night", s); lt = wt("lead", s)
    thermometer(img, 230, 800, 1220, lerp(0.5, 0.97, eio((T - ft + 0.5) / 1.0)), HEAT, a)
    # sol y luna se turnan: el termómetro no se mueve
    day = 0.5 + 0.5 * math.cos((T - dt) * math.pi / 0.9) if T >= dt else 1.0
    sun(img, 470, 860, 60 * day, a * day, T)
    def moon(d, P, s_):
        circ(d, P, 470, 860, 52, (240, 236, 210)); circ(d, P, 492, 846, 44, (0, 0, 0, 0))
    if T >= dt: aa(img, (400, 790, 540, 930), moon, a * (1 - day))
    # bloque de plomo que se derrite
    m = eio((T - lt) / 1.2)
    def lead(d, P, s_):
        h = 150 * (1 - 0.8 * m); w = 200 + 180 * m
        d.rounded_rectangle([P(620 - w / 2, 1240 - h), P(620 + w / 2, 1240)], radius=(14 + 40 * m) * s_, fill=LEAD)
        d.rounded_rectangle([P(620 - w / 2 + 14, 1240 - h + 12), P(620 + w / 2 - 30, 1240 - h + 30)], radius=8 * s_, fill=LEAD_L)
        if m > 0:
            for j in range(3):
                x = 620 - w / 2 + 40 + j * (w - 80) / 2
                d.ellipse([P(x - 16, 1240 - h + 20), P(x + 16, 1240 - h + 52 + 30 * m)], fill=LEAD)
    lk = clamp((T - s - 0.2) / 0.4)
    aa(img, (380, 1050, 880, 1260), lead, a * lk)
    label(img, "450+ °C", 1280, B.TEXT, a * label_in(T, ft, e), 230)
    label(img, "day or night", 960, B.TEXT, a * label_in(T, nt, e), 470)
    label(img, "lead melts", 1280, B.TEXT, a * clamp((T - min(lt, e - 2.4)) / 0.3), 620)
    R.chrome(img, T)
    title(img, T, s, e, "Over 450 °C")
    return R.punch(img, T, lt, amt=0.05)
V.sounds("result", [(0.05, "whoosh", 0.6), (rel("result", "fifty"), "click", 0.8), (rel("result", "night"), "tap", 0.5), (rel("result", "lead"), "bubble", 0.8), (rel("result", "melt"), "bubble", 0.6)])

@V.scene("footnote")
def _(img, T, t, s, e):
    a = win(T, s, e)
    st_ = wt("spin", s); yt = wt("year", s)
    k = back_out(t / 0.4)
    paw(img, 140, 1300, 30, INK_T, a * clamp(k))
    cx, cy, orb = 470, 1110, 190
    sun(img, cx, cy, 60, a, T)
    def path(d, P, s_):
        d.ellipse([P(cx - orb, cy - orb), P(cx + orb, cy + orb)], outline=(150, 120, 90), width=int(4 * s_))
    aa(img, (cx - orb - 6, cy - orb - 6, cx + orb + 6, cy + orb + 6), path, a)
    u = clamp((T - st_ + 0.6) / 3.2)                    # una vuelta al Sol...
    an = -math.pi / 2 + u * 2 * math.pi
    vx, vy = cx + math.cos(an) * orb, cy + math.sin(an) * orb
    planet(img, vx, vy, 52, "venus", a, T)
    spin = -math.pi / 2 + u * 2 * math.pi * (225 / 243)  # ...y todavía no ha completado un giro sobre sí misma
    def mark(d, P, s_):
        d.line([P(vx, vy), P(vx + math.cos(spin) * 52, vy + math.sin(spin) * 52)], fill=RED_T, width=int(7 * s_))
        circ(d, P, vx + math.cos(spin) * 52, vy + math.sin(spin) * 52, 10, RED_T)
    aa(img, (vx - 70, vy - 70, vx + 70, vy + 70), mark, a)
    label(img, "spin: 243 days", 790, RED_T, a * label_in(T, st_, e), 660)
    label(img, "year: 225 days", 790, INK_T, a * clamp((T - min(yt, e - 2.4)) / 0.3), 300)
    R.chrome(img, T)
    title(img, T, s, e, "Footnote")
    R.txt(img, "1 spin takes longer than 1 year", TITLE_Y + 110, "subtitle", ACC_T, win(T, min(st_, e - 2.4), e))
V.sounds("footnote", [(0.05, "pop", 0.7), (rel("footnote", "slowly"), "whoosh", 0.5), (rel("footnote", "spin"), "click", 0.6), (rel("footnote", "year"), "sparkle", 0.8)])

def finale(img, T):
    tw = 0.85 + 0.15 * math.sin(T * 5)
    def star(d, P, s_):     # Venus brillando sobre el horizonte
        for k in range(4):
            circ(d, P, 640, 900, 70 * tw * (1 - k * 0.2), (255, 246, 210, 60 + 50 * k))
        d.polygon([P(640, 840), P(652, 888), P(700, 900), P(652, 912), P(640, 960), P(628, 912), P(580, 900), P(628, 888)], fill=(255, 252, 236))
    aa(img, (560, 820, 720, 980), star, 1.0)
    R.chrome(img, T)
    R.txt(img, "Now you know:", TITLE_Y, "title", B.TEXT_2, win(T, V.sc["wrap"][0], V.outro_at + 1))
    R.txt(img, "CO₂ blanket → hottest planet", TITLE_Y + 97, "title", ACC_T, win(T, V.sc["wrap"][0] + 0.8, V.outro_at + 1))

import library as LIB
@V.scene("wrap")
def _(img, T, t, s, e):
    finale(img, T)
    pose = "point" if t > 0.8 else "front"
    LIB.place(img, "child_girl", pose, 330, 1330, height=420, squash=(1.0, 1.0 + 0.01 * math.sin(T * 2.5)))
    return R.flash(img, T, V.word_time("know"), strength=0.3)
V.sounds("wrap", [(0.05, "whoosh", 0.8), (rel("wrap", "know"), "sparkle", 0.7)])

@V.scene("final")
def _(img, T, t, s, e):
    finale(img, T)
    vt = wt("blanket", s)
    planet(img, 230, 1180, 70, "mercury", 1.0, T)
    planet(img, 560, 1110, 120, "venus", 1.0, T, glow=clamp((T - vt) / 0.6))
    label(img, "closer", 1270, B.TEXT, label_in(T, s, e), 230)
    label(img, "hotter", 1275, B.TEXT, label_in(T, vt, e), 560)
    return R.punch(img, T, vt)
V.sounds("final", [(0.05, "pop", 0.6), (rel("final", "blanket"), "sparkle", 0.7)])

# ---------- fondos (style.py): espacio, Venus y un cierre en la Tierra ----------
CARD = (56, 742, 1024, 1384)
def card_bg(img, T, t): ST.card(img, CARD)
def space(img, T, t, seed=11):
    ST.sky(img, (10, 8, 34), (34, 22, 70), 0, H); ST.stars(img, T, 110, seed=seed, y1=H - 200)
def venus_sky(img, T, t, seed=1):
    """superficie de Venus: cielo naranja turbio y llanuras de roca"""
    ST.sky(img, (96, 52, 30), (226, 150, 74), 0, 1330)
    for i, (c, amp) in enumerate((((176, 96, 50), 60), ((140, 72, 40), 46), ((104, 52, 30), 34))):
        ST.dunes(img, 1250 + i * 40, amp, c, T, speed=4 + 6 * i, seed=seed + i)
    ImageDraw.Draw(img).rectangle([0, 1330, W, H], fill=(60, 30, 20))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(5):      # neblina que se mueve
        y = 300 + k * 200 + 20 * math.sin(T * 0.6 + k)
        d.rectangle([0, y, W, y + 60], fill=(255, 210, 150, 26))
    img.alpha_composite(ov)

V.backdrop("hook")(space)
V.backdrop("options")(lambda img, T, t: space(img, T, t, 21))
V.backdrop("clock")(card_bg)

@V.backdrop("reveal")
def _(img, T, t):
    space(img, T, t, 5)
    ST.wow_moment(img, T, V.sc["reveal"][0] + 0.05, R.cat, "swirl", dur=1.4)    # el giro: remolino, solo con el título

V.backdrop("mercury")(lambda img, T, t: space(img, T, t, 31))
V.backdrop("noair")(lambda img, T, t: space(img, T, t, 41))
V.backdrop("drops")(card_bg)
V.backdrop("venus")(venus_sky)
for n in ("sunlight", "blanket"): V.backdrop(n)(card_bg)
V.backdrop("greenhouse")(lambda img, T, t: space(img, T, t, 51))
V.backdrop("result")(lambda img, T, t: venus_sky(img, T, t, 4))
V.backdrop("footnote")(card_bg)
for n in ("wrap", "final"): V.backdrop(n)(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="hills", seed=3))

if __name__ == "__main__":
    V.main()
