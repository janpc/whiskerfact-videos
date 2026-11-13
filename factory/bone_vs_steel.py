"""Reel: Bone vs steel: which is really stronger? Mr. Whiskerfact, categoría Body, formato versus.
Voz de Brad. Rol `base` del experimento B1-hook-style: gancho en forma de pregunta (control). Estilo v4: bone_vs_steel_v4.py.

Fuentes (dos por dato): ver voice/bone_vs_steel_claims.md
- Acero estructural A36: resistencia a tracción 400-550 MPa, densidad 7,8: Wikipedia ASTM A36; Matmatch
- Hueso compacto (fémur/tibia): tracción ~135-190 MPa, densidad 1,8-2,1: Univ. Wisconsin-Madison; NHTSA (ESV); PMC
- Reparación del hueso (hematoma, callo blando, callo duro, remodelación): UNC Health; HowStuffWorks; Univ. de Hawái
- Hueso = colágeno + hidroxiapatita: Univ. de Cambridge (DoITPoMS)

Lo geométrico (probeta, barras, balanza, grietas, callo, colágeno y cristales) va por código y vectorial; personajes y objetos de la
biblioteca (scientist, bone_steel_items) sin ampliar más de ~1,5x. Rondas 1 y 2 comparan la MISMA magnitud (resistencia a tracción).
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import reel_lib as RLX
import style as ST
import library as LIB
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

R = Reel("body")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "bone_vs_steel", [
    ("hook", "Bone"), ("rules", "Let's"), ("r1", "Round"), ("r1t", "takes"), ("r1u", "That's"), ("r1b", "Pull"),
    ("r2", "Round"), ("r2b", "So"), ("r2c", "Gram"), ("r3", "Round"), ("r3b", "Break"), ("r3c", "A"),
    ("score", "Another"), ("twist", "But"), ("bw", "Bone"), ("comp", "It's"), ("wrap", "Light")])
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano: sin reencuadre automático
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (30, 74, 130)
GREEN_T = (30, 110, 70)
STEEL, STEEL_D, STEEL_L = (150, 160, 176), (96, 106, 124), (196, 204, 216)
BONE, BONE_D, BONE_L = (226, 194, 136), (170, 140, 90), (252, 246, 228)
PINK, CALLUS = (236, 168, 168), (214, 190, 140)
SB = "bone_steel_items"
SCI = "scientist"
CAT = False        # bone_vs_steel_v4.py lo pone a True: el gato v4 habla en gancho, giro y cierre
CARD = (56, 742, 1024, 1384)
GY = 1388          # pies de lo que está de pie sobre el suelo oscuro (paisajes)
CY0 = 1340         # pies sobre la tarjeta crema

def wt(word, s): return V.word_time(word, after=s)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
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

def item(img, name, x, y, h, a=1.0, anchor="center", flip=False, rot=0.0, lib=SB):
    LIB.place(img, lib, name, x, y, height=h, a=a, anchor=anchor, flip=flip, rot=rot)

def chip(img, text, x, y, a, col):
    """marcador de ronda: pastilla con texto (se dibuja a su tamaño final)"""
    if a <= 0.003: return
    spr = R.sprite(text, "label", (255, 252, 240)); w, h = spr.size
    box = Image.new("RGBA", (w + 56, h + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle([3, 3, w + 52, h + 22], radius=(h + 26) // 2, fill=col + (255,), outline=INK_T + (255,), width=6)
    box.alpha_composite(spr, (28, 13))
    R.put_text(img, box, x, y - 40 * (1 - eo(a)), clamp(a * 3), "mm", text=text)

def arrow(img, x, y0, y1, a=1.0, col=RED_T, w=22):
    """flecha vertical de y0 a y1 (la punta está en y1)"""
    if a <= 0.003: return
    def fn(d, P, s):
        sg = 1 if y1 > y0 else -1; hh = 34
        d.rectangle([P(x - w / 2, min(y0, y1 - sg * hh)), P(x + w / 2, max(y0, y1 - sg * hh))], fill=col, outline=INK_T, width=int(4 * s))
        d.polygon([P(x - w * 1.1, y1 - sg * hh), P(x + w * 1.1, y1 - sg * hh), P(x, y1)], fill=col, outline=INK_T)
    aa(img, (x - 40, min(y0, y1) - 6, x + 40, max(y0, y1) + 6), fn, a)

# ---------- probeta de tracción (la misma forma para acero y hueso: «mismas reglas») ----------
def rig(img, x, k, a=1.0, fill=STEEL, fill_d=STEEL_D, y_top=870, y_bot=1230):
    ext = 16 * k
    def fn(d, P, s):
        gt, gb = y_top - ext, y_bot + ext
        d.rounded_rectangle([P(x - 86, gt - 52), P(x + 86, gt)], radius=10 * s, fill=(70, 74, 86), outline=INK_T, width=int(5 * s))
        d.rounded_rectangle([P(x - 86, gb), P(x + 86, gb + 52)], radius=10 * s, fill=(70, 74, 86), outline=INK_T, width=int(5 * s))
        neck = 58 - 8 * k; hw = 62
        ya, yb = gt, gb
        L = yb - ya
        pts = [(x - hw, ya), (x + hw, ya), (x + hw, ya + 0.12 * L), (x + neck / 2, ya + 0.30 * L), (x + neck / 2, ya + 0.70 * L),
               (x + hw, ya + 0.88 * L), (x + hw, yb), (x - hw, yb), (x - hw, ya + 0.88 * L), (x - neck / 2, ya + 0.70 * L),
               (x - neck / 2, ya + 0.30 * L), (x - hw, ya + 0.12 * L)]
        d.polygon([P(*p) for p in pts], fill=fill, outline=INK_T)
        d.line([P(*p) for p in pts + [pts[0]]], fill=INK_T, width=int(5 * s), joint="curve")
        d.line([P(x - neck * 0.15, ya + 0.34 * L), P(x - neck * 0.15, ya + 0.66 * L)], fill=fill_d if fill == STEEL else BONE_D, width=int(6 * s))
    aa(img, (x - 100, y_top - 80, x + 100, y_bot + 90), fn, a)

# ---------- barras (ronda 1) ----------
BASE_Y, PXM = 1280, 0.95
XS, XB = 330, 640
def bar(img, x, h, col, a=1.0, w=190):
    if h <= 1: return
    def fn(d, P, s):
        d.rectangle([P(x - w / 2, BASE_Y - h), P(x + w / 2, BASE_Y)], fill=col, outline=INK_T, width=int(5 * s))
        if h > 50: d.rectangle([P(x - w / 2 + 14, BASE_Y - h + 14), P(x - w / 2 + 38, BASE_Y - 14)], fill=tuple(min(255, c + 28) for c in col))
    aa(img, (x - w / 2 - 6, BASE_Y - h - 6, x + w / 2 + 6, BASE_Y + 6), fn, a)

def baseline(img, a=1.0):
    def fn(d, P, s): d.line([P(150, BASE_Y + 3), P(880, BASE_Y + 3)], fill=INK_T, width=int(6 * s))
    aa(img, (140, BASE_Y - 4, 890, BASE_Y + 12), fn, a)

def chart1(img, ks, kb, a=1.0):
    baseline(img, a)
    hs, hb = 400 * PXM * ks, 150 * PXM * kb
    bar(img, XS, hs, STEEL, a); bar(img, XB, hb, BONE, a)
    if ks >= 0.99: lab(img, "400+ MPa", BASE_Y - 400 * PXM - 66, INK_T, a, x=XS)
    if kb >= 0.99: lab(img, "~150 MPa", BASE_Y - 150 * PXM - 66, INK_T, a, x=XB)
    lab(img, "Steel", BASE_Y + 14, INK_T, a, x=XS)
    if a > 0: lab(img, "Bone", BASE_Y + 14, INK_T, a, x=XB)

# ---------- barras por densidad (ronda 2): rangos que se solapan ----------
P2 = 3.6
def chart2(img, m, a=1.0, labels=True):
    """m=0: alturas de la ronda 1; m=1: resistencia ÷ densidad con su rango (acero 51-70, hueso 64-107)"""
    baseline(img, a)
    s0, b0 = 400 * PXM, 150 * PXM
    s_lo, s_hi, b_lo, b_hi = 51 * P2, 70 * P2, 64 * P2, 107 * P2
    hs_lo, hb_lo = lerp(s0, s_lo, m), lerp(b0, b_lo, m)
    hs_hi, hb_hi = lerp(s0, s_hi, m), lerp(b0, b_hi, m)
    for x, lo, hi, col in ((XS, hs_lo, hs_hi, STEEL), (XB, hb_lo, hb_hi, BONE)):
        bar(img, x, hi, tuple(int(c * 0.55 + 255 * 0.45) for c in col), a)       # tramo del rango: más claro
        bar(img, x, lo, col, a)
    if labels:
        lab(img, "Steel", BASE_Y + 14, INK_T, a, x=XS); lab(img, "Bone", BASE_Y + 14, INK_T, a, x=XB)

# ---------- fibras de colágeno y cristales (zoom del hueso) ----------
def micro(img, cx, cy, r, T, a=1.0, kfib=1.0, kcry=1.0):
    def fn(d, P, s):
        d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=(250, 244, 226), outline=INK_T, width=int(7 * s))
    aa(img, (cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fn, a)
    lay = Image.new("RGBA", (int(2 * r), int(2 * r)), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3)
    nf = int(9 * kfib)
    for i in range(nf):
        y = r * (-0.82 + 1.64 * i / 8) + r
        pts = [(x, y + 16 * math.sin((x / r) * 5 + i * 1.3 + T * 0.8)) for x in np.linspace(0, 2 * r, 40)]
        ld.line(pts, fill=(176, 120, 70), width=14, joint="curve")
    nc = int(34 * kcry)
    for i in range(nc):
        x, y = rng.uniform(0.15, 1.85) * r, rng.uniform(0.15, 1.85) * r
        ang = rng.uniform(-0.5, 0.5); ww, hh = 17, 7
        pts = [(x + math.cos(ang) * dx - math.sin(ang) * dy, y + math.sin(ang) * dx + math.cos(ang) * dy) for dx, dy in ((-ww, 0), (0, -hh), (ww, 0), (0, hh))]
        ld.polygon(pts, fill=(150, 200, 236), outline=INK_T)
    m = Image.new("L", lay.size, 0); ImageDraw.Draw(m).ellipse([6, 6, 2 * r - 6, 2 * r - 6], fill=255)
    lay.putalpha(Image.fromarray((np.asarray(lay.split()[3]).astype(np.float32) * np.asarray(m) / 255).astype(np.uint8)))
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (int(cx - r), int(cy - r)))

# =====================================================================  ESCENAS
@V.scene("hook")
def _(img, T, t, s, e):
    x0 = 660 if CAT else CX
    bob = 5 * math.sin(T * 2.2)
    k = 1.0 if T < 0.3 else 1.0
    item(img, "femur", x0 - 130, 950 + bob, 270, rot=-8)
    item(img, "steel_bar", x0 + 130, 950 - bob, 270, rot=8)
    R.put_text(img, R.sprite("VS", "number", RED_T), x0, 1130 + 4 * math.sin(T * 3), 1.0, "mm", text="VS")
    R.chrome(img, T)
    V.hook_text(img, T, e, "Bone vs steel:", "which is stronger?", "Which")
    if not CAT: R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "Which"), "tap", 0.7)])

ROWS = [("1", "Strength", "dumbbell", 880), ("2", "Weight", "weight_block", 1075), ("3", "Repair", "bone_healed", 1270)]
@V.scene("rules")
def _(img, T, t, s, e):
    a = win(T, s, e)
    t3 = wt("three", s)
    for i, (n, text, ic, y) in enumerate(ROWS):
        k = clamp((T - (s + 0.15 + 0.85 * i)) / 0.3)
        if k <= 0.003: continue
        dx = 40 * (1 - eo(k))
        def fn(d, P, s_, y=y, dx=dx):
            d.ellipse([P(128 + dx - 46, y - 46), P(128 + dx + 46, y + 46)], fill=(246, 196, 84), outline=INK_T, width=int(5 * s_))
        aa(img, (60 + dx, y - 52, 200 + dx, y + 52), fn, a * k)
        R.put_text(img, R.sprite(n, "label", INK_T), 128 + dx, y + 2, a * k, "mm", text=n)
        item(img, ic, 330 + dx, y, 130, a * k)
        lab(img, text, y - 28, INK_T, a * k, x=630 + dx)
    R.chrome(img, T)
    title(img, T, s, e, "3 rounds")
V.sounds("rules", [(0.15 + 0.85 * i, "pop", 0.7) for i in range(3)])

@V.scene("r1")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = clamp((T - wt("Pull", s)) / 1.4)
    rig(img, 310, eo(k), a)
    arrow(img, 310, 808, 752, a * clamp((T - wt("Pull", s) + 0.1) / 0.3))
    arrow(img, 310, 1290, 1346, a * clamp((T - wt("Pull", s) + 0.1) / 0.3))
    pose = "point" if T >= wt("raw", s) else "talk"
    LIB.place(img, SCI, pose, 700, CY0, height=340, a=a)
    lab(img, "Same test, both", 800, INK_T, a * on(T, "common", s, e), x=700)
    R.chrome(img, T)
    title(img, T, s, e, "Round 1: strength")
V.sounds("r1", [(0.1, "whoosh", 0.6), (rel("r1", "raw"), "tap", 0.5), (rel("r1", "Pull"), "click", 0.8)])

@V.scene("r1t")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tf = wt("four", s)
    chart1(img, eio((T - tf + 0.1) / 1.2), 0.0, a)
    R.chrome(img, T)
    title(img, T, s, e, "Steel: 400+ MPa")
    return R.punch(img, T, tf + 1.1, amt=0.04)
V.sounds("r1t", [(rel("r1t", "four"), "whoosh", 0.6), (rel("r1t", "four") + 1.2, "pop", 0.8)])

@V.scene("r1u")
def _(img, T, t, s, e):
    a = win(T, s, e)
    R.put_text(img, R.sprite("MPa", "number", RED_T), 540, 850, a, "mm", text="MPa")
    tf = wt("force", s)
    k = clamp((T - tf + 0.1) / 0.5)
    def fn(d, P, s_):
        d.rectangle([P(400, 1120), P(680, 1260)], fill=(236, 226, 196), outline=INK_T, width=int(6 * s_))
        for i in range(1, 7): d.line([P(400 + 40 * i, 1120), P(400 + 40 * i, 1260)], fill=(200, 188, 150), width=int(3 * s_))
    aa(img, (390, 1110, 690, 1270), fn, a)
    arrow(img, 540, 960 + 10 * math.sin(T * 4), 1112, a * k, w=26)
    lab(img, "force", 985, RED_T, a * k, x=730)
    lab(img, "area", 1285, INK_T, a * on(T, "area", s, e), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Force per area")
V.sounds("r1u", [(0.1, "pop", 0.6), (rel("r1u", "force"), "tap", 0.6), (rel("r1u", "area"), "click", 0.6)])

@V.scene("r1b")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tb = wt("breaks", s); tp = wt("Point", s)
    chart1(img, 1.0, eio((T - tb + 0.3) / 1.0), a)
    chip(img, "Steel +1", 700, 800, clamp((T - tp - 0.1) / 0.3), (176, 100, 40))
    R.chrome(img, T)
    title(img, T, s, e, "Bone: ~150 MPa")
    return R.punch(img, T, tp + 0.1, amt=0.05)
V.sounds("r1b", [(rel("r1b", "breaks") - 0.3, "whoosh", 0.5), (rel("r1b", "Point") + 0.1, "pop", 0.9)])

def balance(img, tilt, a=1.0):
    """balanza por código: acero (izq.) y hueso (der.), mismo tamaño de bloque; tilt>0 baja el lado del acero"""
    px, py, L = 490, 905, 270
    th = math.radians(tilt)
    ly, ry = py + L * math.sin(th), py - L * math.sin(th)
    lx, rx = px - L * math.cos(th), px + L * math.cos(th)
    def fn(d, P, s_):
        d.rectangle([P(px - 14, py), P(px + 14, 1330)], fill=(176, 130, 70), outline=INK_T, width=int(5 * s_))
        d.rounded_rectangle([P(px - 120, 1318), P(px + 120, 1348)], radius=8 * s_, fill=(120, 84, 48), outline=INK_T, width=int(5 * s_))
        d.line([P(lx, ly), P(rx, ry)], fill=(120, 84, 48), width=int(16 * s_))
        d.ellipse([P(px - 22, py - 22), P(px + 22, py + 22)], fill=(246, 196, 84), outline=INK_T, width=int(5 * s_))
        for (ex, ey, col, kind) in ((lx, ly, STEEL, "steel"), (rx, ry, BONE, "bone")):
            d.line([P(ex, ey), P(ex - 90, ey + 150)], fill=INK_T, width=int(4 * s_)); d.line([P(ex, ey), P(ex + 90, ey + 150)], fill=INK_T, width=int(4 * s_))
            d.rounded_rectangle([P(ex - 105, ey + 148), P(ex + 105, ey + 166)], radius=6 * s_, fill=(214, 168, 80), outline=INK_T, width=int(5 * s_))
            d.rectangle([P(ex - 70, ey + 8), P(ex + 70, ey + 148)], fill=col, outline=INK_T, width=int(6 * s_))
            if kind == "steel": d.rectangle([P(ex - 70, ey + 8), P(ex - 40, ey + 148)], fill=STEEL_L)
            else:
                for dx, dy in ((-30, 40), (20, 70), (-10, 110), (36, 30), (-42, 90)): d.ellipse([P(ex + dx - 5, ey + dy - 5), P(ex + dx + 5, ey + dy + 5)], fill=BONE_D)
    aa(img, (60, 700, 940, 1380), fn, a)
    return lx, ly, rx, ry

@V.scene("r2")
def _(img, T, t, s, e):
    a = win(T, s, e)
    th = 9 * eio((T - wt("heavier", s) + 0.3) / 1.0)
    lx, ly, rx, ry = balance(img, th, a)
    lab(img, "Same size", 790, INK_T, a * on(T, "same", s, e), x=490)
    lab(img, "4x heavier", 800, RED_T, a * on(T, "heavier", s, e, need=1.2), x=250)
    R.chrome(img, T)
    title(img, T, s, e, "Round 2: weight")
    return R.punch(img, T, wt("heavier", s) + 0.2, amt=0.04)
V.sounds("r2", [(0.1, "whoosh", 0.6), (rel("r2", "weight"), "tap", 0.5), (rel("r2", "heavier") - 0.2, "pop", 0.8)])

@V.scene("r2b")
def _(img, T, t, s, e):
    a = win(T, s, e)
    m = eio((T - wt("divide", s) - 0.1) / 1.5)
    chart2(img, m, a)
    lab(img, "strength ÷ density", 800, INK_T, a * on(T, "divide", s, e), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Per gram")
V.sounds("r2b", [(0.1, "tap", 0.6), (rel("r2b", "divide"), "whoosh", 0.6), (rel("r2b", "closes"), "pop", 0.7)])

@V.scene("r2c")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tp = wt("Point", s)
    chart2(img, 1.0, a)
    lab(img, "Bone: matches or beats", 765, INK_T, a * on(T, "matches", s, e), x=540)
    chip(img, "Bone +1", 540, 840, clamp((T - tp - 0.1) / 0.3), (60, 130, 90))
    R.chrome(img, T)
    title(img, T, s, e, "Gram for gram")
    return R.punch(img, T, tp + 0.1, amt=0.05)
V.sounds("r2c", [(0.1, "tap", 0.6), (rel("r2c", "matches"), "sparkle", 0.6), (rel("r2c", "Point") + 0.1, "pop", 0.9)])

def crack(img, x, y, k, a=1.0, size=1.0):
    """grieta que se abre en zigzag (dibujada con antialias)"""
    if k <= 0.003: return
    pts = [(-70, 30), (-40, -18), (-12, 22), (14, -24), (42, 18), (72, -22)]
    n = max(2, int(len(pts) * min(1.0, k)))
    def fn(d, P, s_):
        d.line([P(x + px * size, y + py * size) for px, py in pts[:n]], fill=(30, 20, 20), width=int(8 * s_), joint="curve")
    aa(img, (x - 100 * size, y - 60 * size, x + 100 * size, y + 60 * size), fn, a)

@V.scene("r3")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tc = wt("Crack", s)
    item(img, "steel_beam", 480, 1090, 280, a)
    kh = eio((T - tc + 0.5) / 0.5)
    ang = lerp(-55, 8, kh) if T < tc + 0.1 else 8 - 10 * eo((T - tc - 0.1) / 0.3)
    item(img, "hammer", 700 - 120 * kh, 880 + 70 * kh, 200, a * (1 - 0.0), rot=ang)
    crack(img, 470, 1090, clamp((T - tc - 0.15) / 0.3), a, size=1.1)
    lab(img, "stays cracked", 1290, RED_T, a * on(T, "stays", s, e, need=1.5), x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Round 3: repair")
    return R.punch(img, T, tc + 0.15, amt=0.05)
V.sounds("r3", [(0.1, "whoosh", 0.6), (rel("r3", "repair"), "tap", 0.5), (rel("r3", "Crack") + 0.15, "click", 1.0), (rel("r3", "stays"), "tap", 0.5)])

@V.scene("r3b")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ts = wt("starts", s)
    k = eio((T - ts) / 1.2)
    item(img, "bone_cracked", 480, 1080, 280, a)
    def fn(d, P, s_):
        rx, ry = 62 * k, 44 * k
        if k > 0.01: d.ellipse([P(480 - rx, 1082 - ry), P(480 + rx, 1082 + ry)], fill=PINK, outline=INK_T, width=int(5 * s_))
        for i in range(6):                                       # cruces verdes que suben: «se está reparando»
            ph = (T * 0.5 + i / 6) % 1.0
            x = 360 + 60 * i + 8 * math.sin(T * 2 + i); y = 1010 - 120 * ph
            f = clamp(k * 3) * (1 - ph)
            d.line([P(x - 14, y), P(x + 14, y)], fill=(60, 160, 100, int(255 * f)), width=int(7 * s_))
            d.line([P(x, y - 14), P(x, y + 14)], fill=(60, 160, 100, int(255 * f)), width=int(7 * s_))
    aa(img, (280, 860, 700, 1160), fn, a)
    lab(img, "Repair starts", 1290, GREEN_T, a * on(T, "starts", s, e, need=1.4), x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Bone fixes itself")
V.sounds("r3b", [(0.1, "whoosh", 0.6), (rel("r3b", "starts"), "sparkle", 0.7)])

@V.scene("r3c")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tsoft, thard, tre = wt("soft", s), wt("hard", s), wt("months", s)
    xs = (200, 480, 760)
    ks = [clamp((T - (tsoft - 0.1)) / 0.3), clamp((T - (thard - 0.1)) / 0.3), clamp((T - (tre - 0.1)) / 0.3)]
    for i, x in enumerate(xs):
        if ks[i] <= 0.003: continue
        nm = "bone_healed" if i == 2 else "bone_cracked"
        item(img, nm, x, 1070, 200, a * ks[i])
        if i < 2:
            def fn(d, P, s_, x=x, i=i):
                col = PINK if i == 0 else CALLUS
                rx, ry = (34, 26) if i == 0 else (30, 40)
                d.ellipse([P(x - rx, 1070 - ry), P(x + rx, 1070 + ry)], fill=col, outline=INK_T, width=int(5 * s_))
            aa(img, (x - 60, 1000, x + 60, 1140), fn, a * ks[i])
    for i in range(2):
        def fa(d, P, s_, i=i):
            x = (xs[i] + xs[i + 1]) / 2
            d.polygon([P(x - 28, 1050), P(x + 6, 1050), P(x + 6, 1034), P(x + 34, 1070), P(x + 6, 1106), P(x + 6, 1090), P(x - 28, 1090)], fill=(246, 196, 84), outline=INK_T)
        aa(img, (xs[i] + 80, 1020, xs[i + 1] - 80, 1120), fa, a * ks[i + 1])
    for i, text in enumerate(("Soft patch", "Hard bone", "Reshaping")):
        lab(img, text, 1210, INK_T, a * ks[i], x=xs[i] + (0 if i < 2 else -20))
    R.chrome(img, T)
    title(img, T, s, e, "Months to heal")
V.sounds("r3c", [(rel("r3c", "soft") - 0.1, "pop", 0.6), (rel("r3c", "hard") - 0.1, "pop", 0.6), (rel("r3c", "months") - 0.1, "sparkle", 0.6)])

@V.scene("score")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rows = [("1", "Strength", "steel_bar", "Steel", (176, 100, 40), 850), ("2", "Weight", "femur", "Bone", (60, 130, 90), 1000), ("3", "Repair", "bone_healed", "Bone", (60, 130, 90), 1150)]
    for i, (n, text, ic, who, col, y) in enumerate(rows):
        k = 1.0 if i < 2 else clamp((T - s - 0.1) / 0.3)
        if k <= 0.003: continue
        def fn(d, P, s_, y=y):
            d.ellipse([P(100 - 40, y - 40), P(100 + 40, y + 40)], fill=(246, 196, 84), outline=INK_T, width=int(5 * s_))
        aa(img, (50, y - 46, 150, y + 46), fn, a * k)
        R.put_text(img, R.sprite(n, "label", INK_T), 100, y + 2, a * k, "mm", text=n)
        lab(img, text, y - 28, INK_T, a * k, x=330)
        chip(img, who, 680, y, a * k, col)
    tf = wt("Final", s)
    kf = clamp((T - tf) / 0.35)
    chip(img, "Bone 2", 330, 1290, a * kf, (60, 130, 90))
    chip(img, "Steel 1", 700, 1290, a * clamp((T - wt("steel", tf) + 0.1) / 0.35), (176, 100, 40))
    R.chrome(img, T)
    title(img, T, s, e, "Final score")
    return R.punch(img, T, tf + 0.05, amt=0.05)
V.sounds("score", [(0.1, "pop", 0.8), (rel("score", "Final"), "sparkle", 0.8), (rel("score", "two") , "tap", 0.6), (rel("score", "one"), "tap", 0.6)])

@V.scene("twist")
def _(img, T, t, s, e):
    a = win(T, s, e)
    x0 = 700 if CAT else CX
    item(img, "steel_beam", x0, 1040 + 4 * math.sin(T * 2), 280, a)
    lab(img, "Steel: still stronger", 800, B.TEXT, a * on(T, "steel", s, e, need=1.5), x=x0)
    R.chrome(img, T)
    title(img, T, s, e, "The twist")
    return R.punch(img, T, s + 0.1, amt=0.04)
V.sounds("twist", [(0.05, "whoosh", 0.7), (rel("twist", "twist"), "pop", 0.8), (rel("twist", "steel"), "tap", 0.6)])

@V.scene("bw")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tl, tf = wt("light", s), wt("fixing", s)
    item(img, "femur", 290, 1050 + 4 * math.sin(T * 2), 280, a)
    kh = clamp((T - tf + 0.1) / 0.3)
    item(img, "bone_healed", 700, 1050, 280, a)
    lab(img, "Light", 1250, INK_T, a * on(T, "light", s, e, need=1.5), x=290)
    lab(img, "Fixes itself", 1250, GREEN_T, a * on(T, "fixing", s, e, need=1.2), x=690)
    R.chrome(img, T)
    title(img, T, s, e, "Bone's tricks")
V.sounds("bw", [(0.1, "whoosh", 0.6), (rel("bw", "light"), "pop", 0.6), (rel("bw", "fixing"), "sparkle", 0.7)])

@V.scene("comp")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tc, tm = wt("collagen", s), wt("mineral", s)
    item(img, "femur_section", 300, 1060, 450, a)
    kz = clamp((T - s - 0.2) / 0.5)
    def fn(d, P, s_):
        d.line([P(330, 1060), P(620, 1040)], fill=INK_T, width=int(5 * s_))
    aa(img, (260, 1000, 640, 1100), fn, a * kz)
    micro(img, 690, 1040, 190, T, a * kz, kfib=clamp((T - tc + 0.2) / 0.6), kcry=clamp((T - tm + 0.2) / 0.6))
    lab(img, "collagen", 790, (140, 86, 40), a * on(T, "collagen", s, e, need=1.5), x=690)
    lab(img, "mineral crystals", 1290, BLUE_T, a * on(T, "mineral", s, e, need=1.5), x=690)
    R.chrome(img, T)
    title(img, T, s, e, "A natural composite")
V.sounds("comp", [(0.1, "whoosh", 0.6), (rel("comp", "collagen"), "pop", 0.6), (rel("comp", "mineral"), "sparkle", 0.7)])

@V.scene("wrap")
def _(img, T, t, s, e):
    a = win(T, s, e + 1)
    xs = 760 if CAT else 600
    LIB.place(img, SB, "skeleton", xs, GY - 4, height=620, a=a * clamp((T - s - 0.1) / 0.4))
    R.chrome(img, T)
    R.txt(img, "Light, strong,", TITLE_Y, "title", B.TEXT, win(T, s, V.outro_at + 1))
    R.txt(img, "and alive.", TITLE_Y + 97, "title", ACC_T, win(T, wt("alive", s), V.outro_at + 1))
    return R.punch(img, T, wt("alive", s), amt=0.05)
V.sounds("wrap", [(0.05, "whoosh", 0.7), (rel("wrap", "alive"), "sparkle", 0.8)])

# ---------- fondos ----------
def card_bg(img, T, t): ST.card(img, CARD)
V.backdrop("hook")(lambda img, T, t: ST.landscape(img, T, sky_kind="dawn", terrain="city", seed=11))
for n in ("rules", "r1", "r1t", "r1u", "r1b", "r2", "r2b", "r2c", "r3", "r3b", "r3c", "score", "bw", "comp"):
    V.backdrop(n)(card_bg)
V.backdrop("twist")(lambda img, T, t: ST.landscape(img, T, sky_kind="dusk", terrain="hills", seed=12))
V.backdrop("wrap")(lambda img, T, t: ST.landscape(img, T, night=True, terrain="city", seed=14))

if __name__ == "__main__":
    V.main()
