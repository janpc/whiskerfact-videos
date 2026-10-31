"""Reel (Halloween): Myth or fact: do bats drink blood? Mr. Whiskerfact, formato myth, categoría Nature. Voz de Brad.

Fuentes (dos por dato): ver voice/vampire_bats_claims.md
- 1.400+ especies, solo 3 hematófagas: UTK/The Conversation 2024; BCI; PBS; UW-Madison CALS
- No chupan: corte con los incisivos y lamen: USGS; PBS; UW
- Sensores de calor en la nariz: PBS; UW; NatGeo
- Draculina, anticoagulante de la saliva: PBS; Thrombosis and Haemostasis 1995
- Dos noches sin comer -> pueden morir; comparten sangre regurgitada: NatGeo; PBS
- Drácula (1897) se convierte en murciélago; la leyenda es anterior; Linneo bautizó murciélagos «vampiro»:
  History Today; Royal Ontario Museum; Beardsley Zoo
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("nature")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "vampire_bats", [
    ("hook", "Myth"), ("stamp", "Mostly"), ("dracula", "Dracula"), ("legend", "Yet"), ("species", "Now"),
    ("three", "only"), ("cattle", "Today"), ("heat", "And"), ("cut", "Then"), ("footnote", "Footnote"),
    ("twist", "Here's"), ("share", "Luckily"), ("wrap", "So"), ("final", "Only")])

BAT = (72, 56, 86)          # murciélago: violeta oscuro
BAT_L = (112, 92, 130)      # membrana más clara
BAT_EAR = (150, 104, 128)
EYE = (255, 214, 120)
MOON = (250, 236, 180)
PUMPKIN = (236, 128, 40)
PUMPKIN_D = (196, 96, 28)
GLOW = (255, 220, 96)
COW = (238, 232, 220)
COW_SPOT = (70, 58, 54)
SKIN = (232, 176, 150)
BLOOD = (176, 30, 48)
WARM_SPOT = (236, 96, 64)
INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
PURPLE_T = (92, 52, 120)
PARCH = (240, 214, 160)

# ---------- utilidades de dibujo (antialias 2x) ----------
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
    a, b = P(x - r, y - r), P(x + r, y + r)
    d.ellipse([a, b], fill=col)

def title(img, T, s, e, text, color=B.TEXT, y=TITLE_Y, delay=0.0):
    R.txt(img, text, y, "title", color, win(T, s + delay, e))

def wt(word, s): return V.word_time(word, after=s)
def rel(name, word): return V.word_time(word, after=V.sc[name][0]) - V.sc[name][0]

# ---------- murciélago: una sola figura que también sirve de capa del conde (morph) ----------
BAT_WING = [(0.05, -0.02), (0.28, -0.20), (0.56, -0.04), (0.44, 0.10), (0.35, 0.03), (0.25, 0.14), (0.15, 0.06), (0.04, 0.12)]
CAPE = [(0.10, -0.30), (0.24, -0.08), (0.30, 0.46), (0.24, 0.52), (0.18, 0.49), (0.12, 0.53), (0.06, 0.50), (0.0, 0.53)]

def bat(img, cx, cy, size, flap=0.0, a=1.0, morph=1.0, col=BAT, eyes=True, belly=0.0, mouth=None):
    """murciélago de frente con alas abiertas. flap: -1..1 (alas arriba/abajo).
    morph: 0 = silueta del conde con capa, 1 = murciélago (transformación suave de la misma figura).
    belly: 0..1, barriga llena (roja) · mouth: None o 'fangs'"""
    m = eio(morph)
    def fn(d, P, s):
        for sg in (-1, 1):
            pts = []
            for (bx, by), (cx0, cy0) in zip(BAT_WING, CAPE):
                fx = bx * (1 + 0.0 * flap); fy = by - flap * 0.22 * (bx / 0.56)
                x = lerp(cx0, fx, m); y = lerp(cy0, fy, m)
                pts.append(P(cx + sg * x * size, cy + y * size))
            d.polygon(pts, fill=lerpc(col, BAT_L, 0.25) if m > 0.5 else col)
            # dedos de la membrana
            if m > 0.4:
                wr = pts[1]
                for k in (2, 3, 5):
                    d.line([wr, pts[k]], fill=col, width=int(5 * s))
        # cuerpo
        bw, bh = lerp(0.13, 0.11, m) * size, lerp(0.42, 0.17, m) * size
        by0 = cy + lerp(0.05, 0.02, m) * size
        d.ellipse([P(cx - bw, by0 - bh), P(cx + bw, by0 + bh)], fill=col)
        if belly > 0:
            r = 0.075 * size * belly
            d.ellipse([P(cx - r, by0 + 0.02 * size - r), P(cx + r, by0 + 0.02 * size + r)], fill=BLOOD)
        # cabeza
        hy = cy + lerp(-0.40, -0.13, m) * size; hr = lerp(0.085, 0.085, m) * size
        if m < 0.9:   # cuello de la capa
            k = 1 - m
            for sg in (-1, 1):
                d.polygon([P(cx + sg * 0.04 * size, hy + 0.06 * size), P(cx + sg * 0.17 * size * k, hy - 0.08 * size * k),
                           P(cx + sg * 0.12 * size, hy + 0.12 * size)], fill=(150, 30, 50))
        for sg in (-1, 1):   # orejas
            el = 0.12 * size * m
            d.polygon([P(cx + sg * 0.03 * size, hy - 0.04 * size), P(cx + sg * 0.075 * size, hy - 0.06 * size - el),
                       P(cx + sg * 0.085 * size, hy - 0.0 * size)], fill=col)
        d.ellipse([P(cx - hr, hy - hr), P(cx + hr, hy + hr)], fill=lerpc((210, 196, 186), col, m))
        if eyes:
            for sg in (-1, 1):
                circ(d, P, cx + sg * 0.032 * size, hy - 0.01 * size, 0.014 * size, EYE if m > 0.5 else (40, 30, 40))
        if mouth == "fangs" or m < 0.5:
            for sg in (-1, 1):
                d.polygon([P(cx + sg * 0.012 * size, hy + 0.035 * size), P(cx + sg * 0.03 * size, hy + 0.035 * size),
                           P(cx + sg * 0.021 * size, hy + 0.07 * size)], fill=(250, 250, 250))
    aa(img, (cx - 0.62 * size, cy - 0.62 * size, cx + 0.62 * size, cy + 0.62 * size), fn, a)

def hanging_bat(img, x, y, size, a=1.0, belly=0.0, mouth_open=0.0, col=BAT):
    """murciélago colgado boca abajo, alas plegadas; (x, y) = patas en la rama"""
    def fn(d, P, s):
        d.line([P(x - 0.05 * size, y), P(x - 0.03 * size, y + 0.12 * size)], fill=col, width=int(8 * s))
        d.line([P(x + 0.05 * size, y), P(x + 0.03 * size, y + 0.12 * size)], fill=col, width=int(8 * s))
        d.ellipse([P(x - 0.22 * size, y + 0.08 * size), P(x + 0.22 * size, y + 0.72 * size)], fill=col)
        d.ellipse([P(x - 0.15 * size, y + 0.16 * size), P(x + 0.15 * size, y + 0.62 * size)], fill=lerpc(col, BAT_L, 0.6))
        if belly > 0:
            r = 0.09 * size * belly; circ(d, P, x, y + 0.40 * size, r, BLOOD)
        hy = y + 0.80 * size
        for sg in (-1, 1):
            d.polygon([P(x + sg * 0.04 * size, hy + 0.04 * size), P(x + sg * 0.11 * size, hy + 0.22 * size), P(x + sg * 0.13 * size, hy)], fill=col)
        d.ellipse([P(x - 0.13 * size, hy - 0.12 * size), P(x + 0.13 * size, hy + 0.12 * size)], fill=col)
        for sg in (-1, 1): circ(d, P, x + sg * 0.05 * size, hy + 0.02 * size, 0.022 * size, EYE)
        if mouth_open > 0:
            d.ellipse([P(x - 0.04 * size, hy - 0.10 * size - 0.03 * size * mouth_open), P(x + 0.04 * size, hy - 0.06 * size)], fill=(60, 20, 30))
    aa(img, (x - 0.3 * size, y - 10, x + 0.3 * size, y + 0.98 * size), fn, a)

def moon(img, x, y, r, a=1.0):
    def fn(d, P, s):
        circ(d, P, x, y, r, MOON)
        for ox, oy, rr in ((-0.3, -0.2, 0.16), (0.25, 0.1, 0.12), (-0.05, 0.35, 0.09)):
            circ(d, P, x + ox * r, y + oy * r, rr * r, (232, 214, 156))
    aa(img, (x - r - 4, y - r - 4, x + r + 4, y + r + 4), fn, a)

def pumpkin(img, x, y, r, a=1.0, T=0.0):
    """calabaza tallada (toque de Halloween); (x, y) = centro"""
    def fn(d, P, s):
        for ox, kw in ((-0.55, 0.62), (0.55, 0.62), (0, 0.7)):
            d.ellipse([P(x + ox * r - kw * r, y - 0.78 * r), P(x + ox * r + kw * r, y + 0.78 * r)], fill=PUMPKIN if ox else PUMPKIN_D)
        d.ellipse([P(x - 0.45 * r, y - 0.8 * r), P(x + 0.45 * r, y + 0.8 * r)], fill=PUMPKIN)
        d.rounded_rectangle([P(x - 0.08 * r, y - 1.05 * r), P(x + 0.1 * r, y - 0.7 * r)], radius=6 * s, fill=(90, 110, 50))
        g = lerpc(GLOW, (255, 250, 200), 0.3 + 0.3 * math.sin(T * 9))
        for sg in (-1, 1):
            d.polygon([P(x + sg * 0.18 * r, y - 0.05 * r), P(x + sg * 0.48 * r, y - 0.05 * r), P(x + sg * 0.33 * r, y - 0.36 * r)], fill=g)
        d.polygon([P(x - 0.5 * r, y + 0.2 * r), P(x + 0.5 * r, y + 0.2 * r), P(x + 0.3 * r, y + 0.5 * r), P(x + 0.1 * r, y + 0.38 * r),
                   P(x - 0.1 * r, y + 0.5 * r), P(x - 0.3 * r, y + 0.38 * r)], fill=g)
    aa(img, (x - 1.25 * r, y - 1.1 * r, x + 1.25 * r, y + 0.85 * r), fn, a)

def cow(img, x, y, sc=1.0, a=1.0, T=0.0):
    """vaca de perfil mirando a la izquierda; (x, y) = suelo bajo el centro"""
    def fn(d, P, s):
        X = lambda v: x + v * sc; Y = lambda v: y + v * sc
        tail_sw = 10 * math.sin(T * 3)
        d.line([P(X(160), Y(-210)), P(X(200 + tail_sw), Y(-100))], fill=COW, width=int(10 * s * sc))
        circ(d, P, X(200 + tail_sw), Y(-92), 14 * sc, COW_SPOT)
        for lx in (-130, -90, 90, 130):
            d.rounded_rectangle([P(X(lx - 14), Y(-120)), P(X(lx + 14), Y(0))], radius=8 * s, fill=COW)
            d.rectangle([P(X(lx - 14), Y(-18)), P(X(lx + 14), Y(0))], fill=COW_SPOT)
        d.rounded_rectangle([P(X(-170), Y(-260)), P(X(170), Y(-100))], radius=70 * s * sc, fill=COW)
        for ox, oy, rr in ((-60, -200, 42), (60, -170, 34), (120, -230, 26)):
            d.ellipse([P(X(ox - rr * 1.3), Y(oy - rr)), P(X(ox + rr * 1.3), Y(oy + rr))], fill=COW_SPOT)
        d.ellipse([P(X(-110), Y(-150)), P(X(-60), Y(-110))], fill=(240, 180, 190))       # ubre
        bob = 4 * math.sin(T * 2)
        d.polygon([P(X(-170), Y(-250)), P(X(-230), Y(-240 + bob)), P(X(-250), Y(-160 + bob)), P(X(-160), Y(-170))], fill=COW)
        d.rounded_rectangle([P(X(-290), Y(-250 + bob)), P(X(-200), Y(-150 + bob))], radius=30 * s * sc, fill=COW)
        d.rounded_rectangle([P(X(-300), Y(-195 + bob)), P(X(-240), Y(-145 + bob))], radius=22 * s * sc, fill=(240, 180, 190))
        circ(d, P, X(-250), Y(-220 + bob), 7 * sc, (30, 26, 22))
        d.polygon([P(X(-230), Y(-250 + bob)), P(X(-210), Y(-290 + bob)), P(X(-200), Y(-246 + bob))], fill=(236, 220, 180))
        d.polygon([P(X(-220), Y(-240 + bob)), P(X(-180), Y(-252 + bob)), P(X(-200), Y(-222 + bob))], fill=COW)
    aa(img, (x - 320 * sc, y - 310 * sc, x + 240 * sc, y + 6), fn, a)

def paw(img, x, y, r, col, a=1.0):
    def fn(d, P, s):
        d.ellipse([P(x - r, y - 0.2 * r), P(x + r, y + r)], fill=col)
        for ox, oy in ((-0.95, -0.55), (-0.35, -0.95), (0.35, -0.95), (0.95, -0.55)):
            circ(d, P, x + ox * r, y + oy * r, 0.36 * r, col)
    aa(img, (x - 1.5 * r, y - 1.5 * r, x + 1.5 * r, y + 1.2 * r), fn, a)

def leader(img, p0, p1, a, col=INK_T):
    def fn(d, P, s): d.line([P(*p0), P(*p1)], fill=col, width=int(4 * s))
    aa(img, (min(p0[0], p1[0]) - 4, min(p0[1], p1[1]) - 4, max(p0[0], p1[0]) + 4, max(p0[1], p1[1]) + 4), fn, a)

def stamp(img, text, x, y, k, col=RED_T, rot=-10):
    """sello que cae de golpe (escala 1.7 -> 1)"""
    if k <= 0: return
    spr = R.sprite(text, "number", col)
    w, h = spr.size
    box = Image.new("RGBA", (w + 60, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle([4, 4, w + 56, h + 36], radius=22, fill=(246, 238, 214, 255), outline=col + (255,), width=12)
    box.alpha_composite(spr, (30, 20))
    box = box.rotate(rot, resample=Image.BICUBIC, expand=True)
    sc = 1 + 0.7 * (1 - eo(k * 1.0)); kk = clamp(k * 3)
    big = box.resize((int(box.size[0] * sc * 0.6), int(box.size[1] * sc * 0.6)), Image.LANCZOS)
    R.put(img, big, x, y, kk, "mm")

# ---------- piel de cerca (escenas heat / cut) ----------
def skin_patch(img, a, T, warm=0.0, cut=0.0, drop=0.0):
    x0, y0, x1, y1 = 520, 870, 900, 1340
    def fn(d, P, s):
        d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=40 * s, fill=SKIN)
        for i in range(7):    # pelo corto de vaca
            yy = y0 + 50 + i * 68
            for j in range(4):
                xx = x0 + 60 + j * 90 + (i % 2) * 40
                d.line([P(xx, yy), P(xx + 14, yy - 22)], fill=(180, 128, 104), width=int(4 * s))
        if warm > 0:   # vasos sanguíneos cerca de la piel: brillan con el calor
            for k, (px, py) in enumerate(((640, 1050), (780, 1160), (700, 1270))):
                r = (34 + 6 * math.sin(T * 6 + k)) * warm
                circ(d, P, px, py, r * 1.6, WARM_SPOT + (90,))
                circ(d, P, px, py, r, WARM_SPOT)
            pts = [(560, 980), (640, 1050), (780, 1160), (700, 1270), (880, 1320)]
            d.line([P(*p) for p in pts], fill=BLOOD + (int(200 * warm),), width=int(10 * s), joint="curve")
        if cut > 0:
            d.line([P(640 - 40 * cut, 1050), P(640 + 40 * cut, 1050)], fill=BLOOD, width=int(9 * s))
        if drop > 0:
            r = 22 * drop
            d.ellipse([P(640 - r, 1060), P(640 + r, 1060 + 2 * r)], fill=BLOOD)
            d.polygon([P(640 - r * 0.7, 1066), P(640 + r * 0.7, 1066), P(640, 1050)], fill=BLOOD)
    aa(img, (x0 - 6, y0 - 6, x1 + 6, y1 + 6), fn, a)

def bat_head(img, x, y, size, a=1.0, T=0.0, waves=0.0, tongue=0.0, teeth=0.0):
    """cabeza de murciélago de perfil (mirando a la derecha) con hoja nasal; (x, y) = centro de la cabeza"""
    def fn(d, P, s):
        S = size
        d.polygon([P(x - 0.2 * S, y - 0.3 * S), P(x - 0.05 * S, y - 1.0 * S), P(x + 0.15 * S, y - 0.32 * S)], fill=BAT)
        d.polygon([P(x - 0.1 * S, y - 0.36 * S), P(x - 0.04 * S, y - 0.8 * S), P(x + 0.06 * S, y - 0.36 * S)], fill=BAT_EAR)
        d.ellipse([P(x - 0.45 * S, y - 0.42 * S), P(x + 0.35 * S, y + 0.42 * S)], fill=BAT)
        d.ellipse([P(x - 0.5 * S, y + 0.1 * S), P(x + 0.1 * S, y + 0.9 * S)], fill=BAT)     # cuello / cuerpo
        d.ellipse([P(x + 0.1 * S, y - 0.18 * S), P(x + 0.62 * S, y + 0.26 * S)], fill=BAT)   # hocico
        d.polygon([P(x + 0.52 * S, y - 0.06 * S), P(x + 0.66 * S, y - 0.26 * S), P(x + 0.7 * S, y + 0.02 * S)], fill=BAT_EAR)   # hoja nasal
        circ(d, P, x + 0.62 * S, y - 0.04 * S, 0.035 * S, (40, 24, 40))
        circ(d, P, x + 0.12 * S, y - 0.12 * S, 0.06 * S, EYE); circ(d, P, x + 0.14 * S, y - 0.12 * S, 0.028 * S, (30, 20, 30))
        if teeth > 0:
            for ox in (0.48, 0.55):
                d.polygon([P(x + ox * S, y + 0.2 * S), P(x + (ox + 0.05) * S, y + 0.2 * S), P(x + (ox + 0.025) * S, y + (0.2 + 0.1 * teeth) * S)], fill=(252, 252, 250))
        if tongue > 0:
            d.rounded_rectangle([P(x + 0.45 * S, y + 0.18 * S), P(x + (0.5 + 0.28 * tongue) * S, y + 0.26 * S)], radius=8 * s, fill=(236, 110, 140))
        if waves > 0:
            for k in range(3):
                u = (T * 1.2 + k / 3) % 1
                r = (0.25 + u * 0.7) * S
                al = int(255 * waves * (1 - u))
                d.arc([P(x + 0.66 * S - r, y - 0.04 * S - r), P(x + 0.66 * S + r, y - 0.04 * S + r)], -40, 40, fill=(214, 70, 40, al), width=int(8 * s))
    aa(img, (x - 0.6 * size, y - 1.05 * size, x + 1.5 * size, y + 0.95 * size), fn, a)

# ---------- escenas ----------
def flap_of(T, f=4.0): return math.sin(T * f * 2 * math.pi / 2.2)

@V.scene("hook")
def _(img, T, t, s, e):
    bat(img, 540 + 30 * math.sin(T * 1.3), 1010 + 16 * math.sin(T * 2.6), 620, flap_of(T), 1.0)
    R.chrome(img, T)
    V.hook_text(img, T, e, "Myth or fact:", "Do bats drink blood?", "drink")
    R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.25, "whoosh", 0.5), (0.6, "pop", 0.8)])

@V.scene("stamp")
def _(img, T, t, s, e):
    a = win(T, s, e)
    mt = wt("Mostly", s)
    bat(img, 490, 1000, 600, flap_of(T) * (1 - 0.6 * clamp((T - mt) / 0.3)), a)
    stamp(img, "MOSTLY MYTH", 490, 1190, clamp((T - mt) / 0.35))
    R.chrome(img, T)
    R.txt(img, "...but the true part is weirder", TITLE_Y + 30, "subtitle", ACC_T, win(T, wt("true", s), e))
    return R.punch(img, T, mt + 0.1, amt=0.07)
V.sounds("stamp", [(rel("stamp", "Mostly") + 0.1, "pop", 1.0), (rel("stamp", "true"), "tap", 0.6)])

@V.scene("dracula")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tt = wt("transform", s)
    m = eio((T - tt) / 1.1)
    fl = flap_of(T) * m
    lift = 120 * eio((T - tt - 0.6) / 1.2)
    bat(img, 500, 1060 - lift, 640, fl, a * eo(t / 0.3), morph=m)
    R.txt(img, "Dracula, 1897", 790, "label", B.TEXT, a * clamp((T - wt("eighteen", s)) / 0.3), x=480, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Dracula made it famous")
    return R.punch(img, T, tt + 0.5)
V.sounds("dracula", [(0.1, "whoosh", 0.5), (rel("dracula", "eighteen"), "tap", 0.6), (rel("dracula", "transform"), "whoosh", 0.8),
                     (rel("dracula", "transform") + 1.0, "sparkle", 0.6)])

def scroll(img, x, y, a, T):
    def fn(d, P, s):
        d.rounded_rectangle([P(x - 150, y - 200), P(x + 150, y + 200)], radius=14 * s, fill=PARCH)
        for yy in (y - 200, y + 200):
            d.rounded_rectangle([P(x - 175, yy - 26), P(x + 175, yy + 26)], radius=26 * s, fill=(206, 170, 110))
        for i in range(6):
            yy = y - 140 + i * 50
            d.line([P(x - 110, yy), P(x + 110 - (i % 3) * 30, yy)], fill=(150, 110, 70), width=int(6 * s))
        # pequeño rostro con colmillos: la leyenda
        circ(d, P, x, y + 120, 44, (214, 200, 190))
        d.polygon([P(x - 50, y + 90), P(x, y + 70), P(x + 50, y + 90), P(x, y + 100)], fill=(40, 30, 40))
        for sg in (-1, 1):
            circ(d, P, x + sg * 16, y + 116, 6, (40, 30, 40))
            d.polygon([P(x + sg * 6, y + 138), P(x + sg * 16, y + 138), P(x + sg * 11, y + 156)], fill=(255, 255, 255))
    aa(img, (x - 180, y - 230, x + 180, y + 230), fn, a)

@V.scene("legend")
def _(img, T, t, s, e):
    a = win(T, s, e)
    nt = wt("Naturalists", s)
    sk = back_out(t / 0.45)
    scroll(img, 280, 1100 + 6 * math.sin(T * 2), a * clamp(sk), T)
    R.txt(img, "legend first", 800, "label", INK_T, a * clamp((t - 0.3) / 0.3), x=280, rise=False)
    ak = eo((T - nt) / 0.6)
    if ak > 0:
        def arr(d, P, s2):
            x1 = lerp(470, 600, ak)
            d.line([P(470, 1060), P(x1, 1060)], fill=INK_T, width=int(12 * s2))
            d.polygon([P(x1, 1036), P(x1 + 34, 1060), P(x1, 1084)], fill=INK_T)
        aa(img, (450, 1020, 650, 1100), arr, a)
    bk = back_out((T - nt - 0.4) / 0.4)
    if bk > 0: bat(img, 760, 1080, 300 * clamp(bk, 0, 1.15), flap_of(T), a)
    R.txt(img, "named later", 800, "label", PURPLE_T, a * clamp((T - nt - 0.4) / 0.3), x=760, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "The legend came first")
V.sounds("legend", [(0.05, "pop", 0.6), (rel("legend", "Naturalists"), "whoosh", 0.6), (rel("legend", "Naturalists") + 0.4, "pop", 0.8)])

GRID = [(160 + c * 112, 840 + r * 112) for r in range(5) for c in range(7)]
RED3 = (9, 17, 26)

def grid_bats(img, T, a, appear=1.0, dim=0.0, hi=0.0):
    def fn(d, P, s):
        for i, (gx, gy) in enumerate(GRID):
            k = clamp(appear * 1.6 - i / len(GRID) * 0.6)
            if k <= 0: continue
            special = i in RED3
            col = lerpc((150, 128, 170), BLOOD, hi) if special else lerpc((150, 128, 170), (70, 64, 96), dim)
            sz = (44 + (16 * hi if special else 0)) * eo(k)
            f = math.sin(T * 7 + i) * 0.5
            for sg in (-1, 1):
                d.polygon([P(gx, gy), P(gx + sg * sz * 0.6, gy - sz * (0.45 + 0.3 * f)), P(gx + sg * sz * 1.2, gy - sz * 0.1),
                           P(gx + sg * sz * 0.8, gy + sz * 0.15), P(gx + sg * sz * 0.4, gy + sz * 0.05)], fill=col)
            d.ellipse([P(gx - sz * 0.22, gy - sz * 0.35), P(gx + sz * 0.22, gy + sz * 0.3)], fill=col)
    aa(img, (80, 760, 960, 1360), fn, a)

@V.scene("species")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ft = wt("fourteen", s)
    grid_bats(img, T, a, appear=clamp((T - ft + 0.4) / 1.4))
    R.chrome(img, T)
    title(img, T, s, e, "The evidence")
    R.txt(img, "1,400+ bat species", TITLE_Y + 110, "subtitle", ACC_T, win(T, ft, e))
V.sounds("species", [(0.05, "whoosh", 0.6), (rel("species", "fourteen"), "click", 0.7), (rel("species", "fourteen") + 0.6, "click", 0.6),
                     (rel("species", "fourteen") + 1.2, "pop", 0.7)])

@V.scene("three")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tt = wt("three", s)
    grid_bats(img, T, a, appear=1.0, dim=clamp((T - tt) / 0.4), hi=back_out((T - tt) / 0.4))
    R.txt(img, "3 drink blood", 1320, "label", (255, 170, 170), a * clamp((T - tt - 0.2) / 0.3), x=480, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Just 3 feed on blood")
    return R.punch(img, T, tt)
V.sounds("three", [(rel("three", "three"), "pop", 0.9), (rel("three", "blood"), "tap", 0.6)])

@V.scene("cattle")
def _(img, T, t, s, e):
    a = win(T, s, e)
    lt = wt("livestock", s)
    cow(img, 470, 1330, 1.25, a, T)
    u = eio(t / 3.4)
    bx, by = lerp(1000, 640, u), lerp(800, 1180, u) + 20 * math.sin(T * 5)
    bat(img, bx, by, 220, flap_of(T, 6), a)
    R.txt(img, "livestock", 820, "label", B.TEXT, a * clamp((T - lt) / 0.3), x=300, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Mostly livestock")
V.sounds("cattle", [(0.1, "whoosh", 0.6), (rel("cattle", "livestock"), "pop", 0.7), (2.4, "whoosh", 0.5)])

@V.scene("heat")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ht = wt("heat", s); wt_ = wt("warm", s)
    skin_patch(img, a, T, warm=eo((T - wt_) / 0.5))
    bat_head(img, 250, 1110, 260, a, T, waves=clamp((T - ht) / 0.4))
    la = a * clamp((T - ht - 0.2) / 0.3)
    R.txt(img, "heat sensor", 772, "label", RED_T, la, x=300, rise=False)
    leader(img, (380, 830), (414, 1100), la, RED_T)
    R.txt(img, "warm spots", 772, "label", INK_T, a * clamp((T - wt_) / 0.3), x=720, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "It doesn't suck")
    return R.punch(img, T, wt("suck", s))
V.sounds("heat", [(rel("heat", "suck"), "pop", 0.8), (rel("heat", "heat"), "whoosh", 0.6), (rel("heat", "warm"), "sparkle", 0.6)])

@V.scene("cut")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ct = wt("cut", s); lt = wt("laps", s)
    approach = eio(t / 0.8)
    skin_patch(img, a, T, warm=0.6, cut=eo((T - ct) / 0.25), drop=eo((T - ct - 0.3) / 0.5))
    lick = 0.5 + 0.5 * math.sin((T - lt) * 14) if T >= lt else 0.0
    bat_head(img, lerp(200, 300, approach), 1110, 260, a, T, teeth=clamp((T - wt("teeth", s)) / 0.3), tongue=lick)
    R.txt(img, "small cut", 772, "label", RED_T, a * clamp((T - ct) / 0.3), x=720, rise=False)
    R.txt(img, "laps it up", 772, "label", INK_T, a * clamp((T - lt) / 0.3), x=300, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Cut, then lap")
V.sounds("cut", [(0.1, "whoosh", 0.5), (rel("cut", "cut"), "click", 0.8), (rel("cut", "laps"), "bubble", 0.6), (rel("cut", "laps") + 0.5, "bubble", 0.5)])

def molecule(img, x, y, a, T, k):
    def fn(d, P, s):
        pts = [(x + i * 70 - 210, y + 34 * math.sin(i * 1.3 + T * 2)) for i in range(7)]
        n = max(1, int(len(pts) * clamp(k)))
        for i in range(n - 1): d.line([P(*pts[i]), P(*pts[i + 1])], fill=PURPLE_T, width=int(10 * s))
        for i, p in enumerate(pts[:n]): circ(d, P, p[0], p[1], 26 if i % 2 else 20, (150, 110, 190) if i % 2 else (110, 170, 150))
    aa(img, (x - 260, y - 80, x + 260, y + 80), fn, a)

@V.scene("footnote")
def _(img, T, t, s, e):
    a = win(T, s, e)
    pt = wt("protein", s); ct = wt("clotting", s); dt = wt("draculin", s)
    k = back_out(t / 0.4)
    def card_fn(d, P, s2):
        d.rounded_rectangle([P(120, 800), P(880, 1330)], radius=40 * s2, fill=ST.CREAM)
    aa(img, (110, 790, 890, 1340), card_fn, a * clamp(k))
    paw(img, 200, 880, 34, INK_T, a * clamp(k))
    molecule(img, 500, 1000, a, T, eo((T - pt) / 0.8))
    # gota que sigue fluyendo (no coagula)
    fl = clamp((T - ct + 0.3) / 0.3)
    if fl > 0:
        def flow(d, P, s2):
            for j in range(5):
                u = (T * 0.8 + j / 5) % 1
                xx = lerp(220, 780, u); r = 18
                d.ellipse([P(xx - r, 1170 - r), P(xx + r, 1170 + r)], fill=BLOOD)
            d.line([P(200, 1170), P(800, 1170)], fill=BLOOD + (120,), width=int(8 * s2))
        aa(img, (180, 1140, 820, 1200), flow, a * fl)
    R.txt(img, "draculin", 1220, "label", PURPLE_T, a * clamp((T - dt) / 0.3), x=500, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Footnote")
    R.txt(img, "a blood-thinner in its spit", TITLE_Y + 110, "subtitle", ACC_T, win(T, ct - 0.4, e))
    return R.punch(img, T, dt)
V.sounds("footnote", [(0.05, "pop", 0.7), (rel("footnote", "protein"), "whoosh", 0.5), (rel("footnote", "clotting"), "bubble", 0.6),
                      (rel("footnote", "draculin"), "sparkle", 0.8)])

@V.scene("twist")
def _(img, T, t, s, e):
    a = win(T, s, e)
    nt = wt("nights", s); st = wt("starve", s)
    hungry = clamp((T - nt) / 1.2)
    bat(img, 470, 1070 + 10 * math.sin(T * 3), 560 * (1 - 0.15 * hungry), flap_of(T) * (1 - 0.5 * hungry), a, col=lerpc(BAT, (110, 100, 120), hungry))
    for i in range(2):     # dos lunas cruzan: dos noches
        u = clamp((T - nt + 0.4 - i * 0.5) / 1.4)
        if 0 < u < 1: moon(img, lerp(120, 860, u), 820 - 50 * math.sin(u * math.pi), 46, a)
    def bar(d, P, s2):
        d.rounded_rectangle([P(180, 1320), P(780, 1356)], radius=18 * s2, fill=(40, 30, 40))
        d.rounded_rectangle([P(186, 1326), P(186 + 588 * (1 - 0.92 * hungry), 1350)], radius=12 * s2, fill=lerpc((120, 220, 120), BLOOD, hungry))
    aa(img, (170, 1310, 790, 1366), bar, a * clamp((T - nt + 0.5) / 0.3))
    R.txt(img, "2 nights", 800, "label", B.TEXT, a * clamp((T - nt) / 0.3), x=480, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "The part movies skip")
    return R.punch(img, T, st)
V.sounds("twist", [(0.0, "sparkle", 0.8), (0.3, "whoosh", 0.6), (rel("twist", "nights"), "whoosh", 0.6), (rel("twist", "starve"), "pop", 0.7)])

@V.scene("share")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rt = wt("regurgitate", s); sh = wt("share", s)
    def branch(d, P, s2): d.rounded_rectangle([P(120, 800), P(880, 836)], radius=18 * s2, fill=(88, 60, 44))
    aa(img, (110, 790, 890, 846), branch, a)
    give = clamp((T - rt) / 1.0)
    hanging_bat(img, 320, 830, 400, a, belly=1 - 0.5 * give)
    hanging_bat(img, 660, 830, 400, a, belly=0.6 * clamp((T - sh) / 0.6), mouth_open=clamp((T - rt) / 0.3) * (1 - clamp((T - sh - 0.6) / 0.3)))
    u = clamp((T - rt - 0.3) / 0.9)
    if 0 < u < 1:
        def drop(d, P, s2):
            x = lerp(330, 650, u); y = 1150 - 80 * math.sin(u * math.pi)
            circ(d, P, x, y, 22, BLOOD)
        aa(img, (300, 1040, 690, 1190), drop, a)
    R.txt(img, "shared meal", 1250, "label", B.TEXT, a * clamp((T - sh) / 0.3), x=490, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Luckily, they share")
    return R.flash(img, T, sh + 0.2, strength=0.25)
V.sounds("share", [(0.05, "pop", 0.6), (rel("share", "regurgitate"), "bubble", 0.7), (rel("share", "share"), "sparkle", 0.8)])

def finale(img, T, flap=True):
    moon(img, 760, 880, 90)
    pumpkin(img, 300, 1250, 110, 1.0, T)
    bat(img, 600 + 40 * math.sin(T * 1.1), 1050 + 20 * math.sin(T * 2.2), 380, flap_of(T, 4) if flap else 0.0)
    R.chrome(img, T)
    R.txt(img, "Now you know:", TITLE_Y, "title", B.TEXT_2, win(T, V.sc["wrap"][0], V.outro_at + 1))
    R.txt(img, "3 living species drink blood", TITLE_Y + 97, "title", ACC_T, win(T, V.sc["wrap"][0] + 0.8, V.outro_at + 1))

@V.scene("wrap")
def _(img, T, t, s, e):
    finale(img, T)
    return R.flash(img, T, V.word_time("know"), strength=0.3)
V.sounds("wrap", [(0.05, "whoosh", 0.8), (rel("wrap", "know"), "sparkle", 0.7)])

@V.scene("final")
def _(img, T, t, s, e):
    finale(img, T)
    lt = wt("lap", s)
    R.txt(img, "they lap, not suck", 790, "label", B.TEXT, win(T, lt, V.outro_at + 1), x=360, rise=False)
    return R.punch(img, T, lt)
V.sounds("final", [(rel("final", "three"), "pop", 0.6), (rel("final", "lap"), "bubble", 0.7)])

# ---------- fondos (style.py) ----------
CARD = (56, 742, 1024, 1384)
def card_bg(img, T, t): ST.card(img, CARD)
def night_sky(img, T, t):
    ST.sky(img, (16, 14, 52), ST.NIGHT, 0, H); ST.stars(img, T, 80, seed=11, y1=H - 300)
def night_moon(img, T, t):
    night_sky(img, T, t); moon(img, 540, 1010, 330)
def dusk_autumn(img, T, t): ST.landscape(img, T, sky_kind="dusk", terrain="autumn", seed=1)
def dusk_autumn2(img, T, t): ST.landscape(img, T, sky_kind="dusk", terrain="autumn", seed=4)
def night_autumn(img, T, t):
    ST.landscape(img, T, night=True, terrain="autumn", seed=2); moon(img, 820, 640, 70)
def dusk_sky(img, T, t):
    pal = ST.SKIES["dusk"]; ST.sky(img, pal[0], pal[2], 0, H); ST.stars(img, T, 40, seed=5, y1=900, a=0.6)

V.backdrop("hook")(night_moon)
V.backdrop("stamp")(dusk_autumn)
V.backdrop("dracula")(night_autumn)
V.backdrop("legend")(card_bg)
for n in ("species", "three"): V.backdrop(n)(night_sky)
V.backdrop("cattle")(dusk_autumn2)
for n in ("heat", "cut"): V.backdrop(n)(card_bg)
V.backdrop("footnote")(dusk_sky)

@V.backdrop("twist")
def _(img, T, t):
    night_autumn(img, T, t)
    ST.wow_moment(img, T, V.sc["twist"][0] + 0.05, R.cat, "glitch", dur=1.4)    # el giro: mosaico glitch, solo con el título

@V.backdrop("share")
def _(img, T, t):
    night_sky(img, T, t)
    d = ImageDraw.Draw(img)      # cueva: bóveda oscura con estalactitas
    d.rectangle([0, 0, W, 760], fill=(30, 24, 36))
    for i in range(12):
        x = i * 100 + 20; h = 60 + (i * 37) % 90
        d.polygon([(x - 40, 760), (x + 40, 760), (x, 760 + h)], fill=(30, 24, 36))
    d.rectangle([0, 1380, W, H], fill=(30, 24, 36))
    d.ellipse([-200, 1300, W + 200, 1500], fill=(30, 24, 36))

for n in ("wrap", "final"): V.backdrop(n)(dusk_autumn)

if __name__ == "__main__":
    V.main()
