"""Reel: Myth or fact: cats can see in total darkness. Mr. Whiskerfact, categoría Nature, formato myth.
Voz de Brad. Experimento B1-hook-style, opción `statement` (variante).

Fuentes (dos por dato): ver voice/cat_night_vision_claims.md
- No ven en oscuridad total; necesitan algo de luz: Univ. of Illinois ANSC 207; Ask Extension
- Tapetum lucidum detrás de la retina, refleja la luz no absorbida (segunda oportunidad) y causa el brillo: Illinois; VCA; Vet Practice News
- Muchos más bastones (luz tenue): Ask Extension; Vet Practice News
- Pupila en rendija: área ~135 veces vs ~15 en humanos: UC Berkeley / Science Advances 2015 (Phys.org); ScienceAlert
- ~1/6 de la luz que necesitamos (bastones + tapetum): Vet Practice News; Illinois; Ask Extension

Gráficos geométricos (ojo en corte, bastones, pupila, barras) por código; personajes y objetos de la biblioteca
(cat, cat_eye_night_items) sin ampliar más de ~1,5x.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("nature")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "cat_night_vision", [
    ("hook", "Cats"), ("stamp", "Verdict"), ("glow", "Blame"), ("trick", "Here's"), ("light", "Light"),
    ("bounce", "That"), ("rods", "Rods"), ("pupils", "Pupils"), ("wide", "wide"), ("sixth", "Thanks"),
    ("zero", "Zero"), ("take", "Still"), ("wrap", "So")])
V.FIT_MAX = 1.1            # 6/11: los sprites de la biblioteca no se amplían más de ~1,5x en total

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
TEAL_T = (22, 96, 104)
IT = "cat_eye_night_items"
EYE_W = (250, 246, 236)
IRIS = (150, 196, 70)
IRIS_D = (96, 140, 40)
PUPIL = (24, 20, 26)
RETINA = (226, 110, 96)
TAPETUM = (70, 200, 190)
TAPETUM_L = (170, 250, 236)
PHOTON = (255, 214, 90)
ROD = (120, 96, 190)
CONE = (236, 160, 60)

CAT = False        # cat_night_vision_v4.py lo pone a True: el gato v4 habla en gancho, «Still» y cierre
CARD = (56, 742, 1024, 1384)

def wt(word, s): return V.word_time(word, after=s)
def early(word, s, e, need=1.9): return min(wt(word, s), e - need)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))

def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def sprite(img, pose, x, y, h, a=1.0, anchor="center", name=IT, flip=False, squash=(1.0, 1.0)):
    LIB.place(img, name, pose, x, y, height=h, a=a, anchor=anchor, flip=flip, squash=squash)

def halo(img, x, y, r, k, col=(220, 255, 120)):
    """brillo suave alrededor de un ojo (k 0..1)"""
    if k <= 0.01: return
    def fn(d, P, s):
        for i in range(6, 0, -1):
            rr = r * (0.5 + 0.18 * i)
            d.ellipse([P(x - rr, y - rr), P(x + rr, y + rr)], fill=col + (int(30 * k),))
    aa(img, (x - 2.2 * r, y - 2.2 * r, x + 2.2 * r, y + 2.2 * r), fn)

def glowing_eyes(img, x, y, h, a=1.0, glow=1.0, blink=0.0):
    """los ojos que brillan en la oscuridad (biblioteca, cuadro oscuro); glow = halo; blink 0..1 cierra los ojos"""
    if glow > 0:
        for fx in (0.255, 0.735):
            halo(img, x + (fx - 0.5) * h, y + 0.02 * h, 0.13 * h, glow * a)
    sprite(img, "eyes_glow", x, y, h, a, squash=(1.0, 1.0 - 0.0 * blink))
    if blink > 0:          # párpados oscuros que bajan
        def fn(d, P, s):
            for fx in (0.255, 0.735):
                ex, ey = x + (fx - 0.5) * h, y + 0.02 * h
                d.rectangle([P(ex - 0.13 * h, ey - 0.09 * h), P(ex + 0.13 * h, ey - 0.09 * h + 0.18 * h * blink)], fill=(22, 26, 40))
        aa(img, (x - h / 2, y - h / 2, x + h / 2, y + h / 2), fn, a)

def beam(img, x0, y0, x1, y1, w0, w1, k, a=1.0, col=(255, 236, 170)):
    """haz de linterna de (x0, y0) a (x1, y1): ancho w0 -> w1; k 0..1 lo enciende"""
    if k <= 0: return
    xe = lerp(x0, x1, k); ye = lerp(y0, y1, k); we = lerp(w0, w1, k)
    def fn(d, P, s):
        d.polygon([P(x0, y0 - w0 / 2), P(xe, ye - we / 2), P(xe, ye + we / 2), P(x0, y0 + w0 / 2)], fill=col + (110,))
        d.polygon([P(x0, y0 - w0 / 4), P(xe, ye - we / 4), P(xe, ye + we / 4), P(x0, y0 + w0 / 4)], fill=col + (90,))
    aa(img, (min(x0, x1) - 4, min(y0, y1) - w1, max(x0, x1) + 4, max(y0, y1) + w1), fn, a)

def stamp(img, text, x, y, k, col=RED_T):
    """sello que cae: se dibuja a su tamaño final (sin reescalar) e inclinación pequeña; solo cae y aparece"""
    if k <= 0: return
    spr = R.sprite(text, "number", col)
    w, h = spr.size
    box = Image.new("RGBA", (w + 70, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle([4, 4, w + 66, h + 40], radius=22, fill=(246, 238, 214, 255), outline=col + (255,), width=12)
    box.alpha_composite(spr, (35, 20))
    box = box.rotate(-6, resample=Image.BICUBIC, expand=True)
    kk = eo(k)
    R.put_text(img, box, x, y - 70 * (1 - kk), clamp(k * 3), "mm", text=text)

# ---------- ojo de gato en corte (vector) ----------
EX, EY, ER = 440, 1085, 245
def ang_pt(deg, r): return EX + math.cos(math.radians(deg)) * r, EY + math.sin(math.radians(deg)) * r
def eye_cutaway(img, a=1.0, T=0.0, shine=0.0):
    def fn(d, P, s):
        # globo
        d.ellipse([P(EX - ER - 6, EY - ER - 6), P(EX + ER + 6, EY + ER + 6)], fill=INK_T)
        d.ellipse([P(EX - ER, EY - ER), P(EX + ER, EY + ER)], fill=EYE_W)
        # tapetum (mitad superior del fondo del ojo), retina por dentro, interior del ojo
        sh = 0.5 + 0.5 * math.sin(T * 3.0)
        tcol = lerpc(TAPETUM, TAPETUM_L, 0.35 * sh + 0.5 * shine)
        d.pieslice([P(EX - ER * 0.97, EY - ER * 0.97), P(EX + ER * 0.97, EY + ER * 0.97)], -80, -5, fill=tcol)
        d.pieslice([P(EX - ER * 0.97, EY - ER * 0.97), P(EX + ER * 0.97, EY + ER * 0.97)], -5, 80, fill=(150, 70, 70))
        d.pieslice([P(EX - ER * 0.89, EY - ER * 0.89), P(EX + ER * 0.89, EY + ER * 0.89)], -85, 85, fill=RETINA)
        d.ellipse([P(EX - ER * 0.81, EY - ER * 0.81), P(EX + ER * 0.81, EY + ER * 0.81)], fill=(236, 240, 232))
        # nervio óptico
        d.rounded_rectangle([P(EX + ER - 10, EY + 20), P(EX + ER + 50, EY + 60)], radius=12 * s, fill=(236, 200, 120), outline=INK_T, width=int(4 * s))
        # córnea, iris y cristalino (la luz entra por la izquierda)
        d.chord([P(EX - ER - 50, EY - 120), P(EX - ER + 70, EY + 120)], 90, 270, fill=(200, 230, 246), outline=INK_T, width=int(4 * s))
        for sg in (-1, 1):
            d.rounded_rectangle([P(EX - ER + 4, EY + sg * 52 - (0 if sg > 0 else 70)), P(EX - ER + 26, EY + sg * 52 + (70 if sg > 0 else 0))],
                                radius=8 * s, fill=IRIS_D)
        d.ellipse([P(EX - ER + 30, EY - 82), P(EX - ER + 110, EY + 82)], fill=(206, 226, 240), outline=INK_T, width=int(4 * s))
    aa(img, (EX - ER - 60, EY - ER - 10, EX + ER + 60, EY + ER + 10), fn, a)

def leader(img, x0, y0, x1, y1, a):
    def fn(d, P, s):
        d.line([P(x0, y0), P(x1, y1)], fill=INK_T, width=int(4 * s))
        d.ellipse([P(x1 - 8, y1 - 8), P(x1 + 8, y1 + 8)], fill=INK_T)
    aa(img, (min(x0, x1) - 12, min(y0, y1) - 12, max(x0, x1) + 12, max(y0, y1) + 12), fn, a)

def photon_path(u):
    """recorrido de la luz: entra por la izquierda, cruza el cristalino, atraviesa la retina, rebota en el tapetum y vuelve.
    u 0..1 -> (x, y)"""
    p0 = (EX - ER - 170, EY - 30); p1 = (EX - ER + 70, EY - 8)
    hit = ang_pt(-35, ER * 0.93); back = ang_pt(-35, ER * 0.80)
    hit_back = (back[0] - 40, back[1] + 22)
    pts = [p0, p1, hit, hit_back]
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(3)]; L = sum(segs)
    d = u * L
    for i in range(3):
        if d <= segs[i] or i == 2:
            k = clamp(d / segs[i]); return lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k), i
        d -= segs[i]

def photon(img, u, a=1.0, trail=0.12):
    def fn(d, P, s):
        for j in range(8, -1, -1):
            uu = max(0.0, u - trail * j / 8)
            x, y, _ = photon_path(uu)
            r = 17 - j
            d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=PHOTON + (int(255 * (1 - j / 10)),))
    aa(img, (EX - ER - 200, EY - ER, EX + ER + 20, EY + 80), fn, a)

# ---------- ojos dibujados por código (escena pupils) ----------
def cat_eye(img, x, y, w, h, pw, a=1.0):
    """ojo almendrado con iris verde y pupila en rendija de ancho pw (px)"""
    def fn(d, P, s):
        pts = [(x - w / 2 + w * i / 40, y - h / 2 * math.sin(math.pi * i / 40)) for i in range(41)] + \
              [(x + w / 2 - w * i / 40, y + h / 2 * math.sin(math.pi * i / 40)) for i in range(41)]
        d.polygon([P(*p) for p in pts], fill=INK_T)
        pts2 = [(x - w / 2 + 12 + (w - 24) * i / 40, y - (h / 2 - 10) * math.sin(math.pi * i / 40)) for i in range(41)] + \
               [(x + w / 2 - 12 - (w - 24) * i / 40, y + (h / 2 - 10) * math.sin(math.pi * i / 40)) for i in range(41)]
        d.polygon([P(*p) for p in pts2], fill=EYE_W)
        ri = h * 0.44
        d.ellipse([P(x - ri, y - ri), P(x + ri, y + ri)], fill=IRIS, outline=IRIS_D, width=int(6 * s))
        for k in range(12):
            an = k / 12 * 2 * math.pi
            d.line([P(x + math.cos(an) * ri * 0.45, y + math.sin(an) * ri * 0.45), P(x + math.cos(an) * ri * 0.92, y + math.sin(an) * ri * 0.92)], fill=IRIS_D, width=int(3 * s))
        ph = ri * 0.96; pw2 = max(6, pw) / 2
        d.ellipse([P(x - pw2, y - ph), P(x + pw2, y + ph)], fill=PUPIL)
        d.ellipse([P(x - ri * 0.42, y - ri * 0.55), P(x - ri * 0.2, y - ri * 0.33)], fill=(255, 255, 255, 230))
    aa(img, (x - w / 2 - 6, y - h / 2 - 6, x + w / 2 + 6, y + h / 2 + 6), fn, a)

# =====================================================================  ESCENAS
@V.scene("hook")
def _(img, T, t, s, e):
    x, y, h = (700, 1080, 350) if CAT else (CX - 40, 1080, 360)
    blink = 0.0
    if 0.3 <= t < 0.6: blink = math.sin(math.pi * (t - 0.3) / 0.3)        # parpadeo a los 0,3 s: algo se mueve enseguida
    glowing_eyes(img, x, y, h, 1.0, glow=0.75 + 0.25 * math.sin(T * 4), blink=blink)
    R.chrome(img, T)
    V.hook_text(img, T, e, "Cats can see in total darkness.", "Myth or fact?", "Myth")
    if not CAT: R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (2.6, "tap", 0.6), (4.0, "sparkle", 0.5)])

@V.scene("stamp")
def _(img, T, t, s, e):
    a = win(T, s, e)
    mt = wt("myth", s)
    pose = "surprised" if T > mt + 0.2 else "sit"
    sprite(img, pose, 330, 1350, 330, a, anchor="bottom", name="cat")
    stamp(img, "MYTH", 660, 930, clamp((T - mt) / 0.3))
    R.chrome(img, T)
    R.txt(img, "Even cats need light", TITLE_Y, "title", B.TEXT, win(T, wt("Even", s) - 0.3, e))
    return R.punch(img, T, mt + 0.05, amt=0.06)
V.sounds("stamp", [(rel("stamp", "myth") + 0.05, "pop", 1.0), (rel("stamp", "Even"), "tap", 0.6)])

@V.scene("glow")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sh = wt("Shine", s); ey = wt("eyes", s)
    on = eo((T - sh) / 0.5)
    sprite(img, "flashlight", 190, 1150, 170, a)
    beam(img, 330, 1140, 600, 1080, 60, 300, on, a)
    g = eo((T - ey) / 0.4)
    glowing_eyes(img, 660, 1080, 330, a * (0.35 + 0.65 * on), glow=g * (0.8 + 0.2 * math.sin(T * 5)))
    lab(img, "tiny lanterns", 1265, B.TEXT, a * clamp((T - early("lanterns", s, e) + 0.1) / 0.3), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Blame the glow")
V.sounds("glow", [(0.1, "whoosh", 0.6), (rel("glow", "Shine"), "click", 0.8), (rel("glow", "eyes"), "sparkle", 0.8), (rel("glow", "lanterns"), "tap", 0.5)])

@V.scene("trick")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tp = wt("tapetum", s); rt = wt("retina", s)
    eye_cutaway(img, a, T, shine=clamp((T - tp) / 0.4) * (0.5 + 0.5 * math.sin(T * 6)))
    kr = clamp((T - early("retina", s, e, 3.0) + 0.1) / 0.3)
    leader(img, 740, 1250, ang_pt(40, ER * 0.85)[0], ang_pt(40, ER * 0.85)[1], a * kr)
    lab(img, "retina", 1262, INK_T, a * kr, x=780)
    kt = clamp((T - early("tapetum", s, e) + 0.1) / 0.3)
    tx, ty = ang_pt(-45, ER * 0.93)
    leader(img, 640, 812, tx, ty, a * kt)
    lab(img, "tapetum lucidum", 762, RED_T, a * kt, x=560)
    R.chrome(img, T)
    title(img, T, s, e, "A mirror in the eye")
V.sounds("trick", [(0.1, "whoosh", 0.6), (rel("trick", "retina"), "tap", 0.6), (rel("trick", "tapetum"), "sparkle", 0.8)])

@V.scene("light")
def _(img, T, t, s, e):
    a = win(T, s, e)
    bt = wt("bounces", s)
    u = clamp((T - s - 0.2) / max(0.5, bt - s - 0.2)) * 0.82 + 0.18 * clamp((T - bt) / 0.8)
    hit = clamp((T - bt) / 0.3) * (1 - clamp((T - bt - 0.6) / 0.5))
    eye_cutaway(img, a, T, shine=hit)
    photon(img, u, a)
    if T > bt + 0.5:                                    # segunda oportunidad: la retina "atrapa" la luz
        bx, by = ang_pt(-35, ER * 0.82)
        k = clamp((T - bt - 0.5) / 0.3)
        def fn(d, P, s_):
            r = 26 + 10 * math.sin(T * 8)
            d.ellipse([P(bx - 48 - r, by + 22 - r), P(bx - 48 + r, by + 22 + r)], outline=PHOTON + (230,), width=int(6 * s_))
        aa(img, (bx - 140, by - 70, bx + 50, by + 110), fn, a * k)
    lab(img, "second chance", 1262, RED_T, a * clamp((T - early("second", s, e) + 0.1) / 0.3), x=740)
    R.chrome(img, T)
    title(img, T, s, e, "Light gets a second try")
V.sounds("light", [(0.1, "whoosh", 0.6), (rel("light", "bounces"), "clink", 0.8), (rel("light", "second"), "sparkle", 0.6)])

@V.scene("bounce")
def _(img, T, t, s, e):
    a = win(T, s, e)
    sprite(img, "flashlight", 185, 1200, 150, a)
    beam(img, 310, 1195, 560, 1110, 50, 210, eo(t / 0.5), a)
    glowing_eyes(img, 660, 1060, 330, a, glow=0.8 + 0.2 * math.sin(T * 5))
    k = eo((T - wt("reflecting", s)) / 0.5)
    if k > 0:                                           # la luz vuelve hacia la linterna
        def fn(d, P, s_):
            for i, dy in enumerate((-40, 0, 40)):
                x1 = lerp(560, 330, k); y1 = 1050 + dy * 0.5
                d.line([P(560, 1050 + dy), P(x1, y1 + 60)], fill=PHOTON + (230,), width=int(7 * s_))
                d.polygon([P(x1 - 4, y1 + 60 - 16), P(x1 - 4, y1 + 60 + 16), P(x1 - 30, y1 + 62)], fill=PHOTON + (230,))
        aa(img, (290, 980, 580, 1150), fn, a)
    lab(img, "not making light", 800, B.TEXT, a * clamp((T - early("making", s, e, 3.4) + 0.1) / 0.3), x=500)
    lab(img, "reflecting yours", 1265, B.TEXT, a * clamp((T - early("reflecting", s, e) + 0.1) / 0.3), x=500)
    R.chrome(img, T)
    title(img, T, s, e, "Reflected, not made")
V.sounds("bounce", [(0.1, "click", 0.6), (rel("bounce", "making"), "tap", 0.5), (rel("bounce", "reflecting"), "whoosh", 0.7)])

def rods_panel(img, x, y, n_rods, cones, k, a, T):
    """tira de retina: bastones (altos, violeta) y conos (ámbar); k 0..1 los va mostrando"""
    w, h = 380, 380
    cells = []
    total = n_rods + len(cones)
    ci = set(cones)
    for i in range(total):
        cells.append("cone" if i in ci else "rod")
    def fn(d, P, s):
        d.rounded_rectangle([P(x - w / 2, y - h / 2), P(x + w / 2, y + h / 2)], radius=24 * s, fill=(246, 222, 210), outline=INK_T, width=int(5 * s))
        step = (w - 40) / total
        show = int(round(k * total))
        for i, c in enumerate(cells[:show]):
            cx = x - w / 2 + 20 + step * (i + 0.5)
            bob = 3 * math.sin(T * 3 + i)
            if c == "rod":
                rw = max(5, step * 0.55)
                d.rounded_rectangle([P(cx - rw / 2, y - h / 2 + 30 + bob), P(cx + rw / 2, y + h / 2 - 30)], radius=rw / 2 * s, fill=ROD)
            else:
                d.polygon([P(cx - step * 0.45, y + h / 2 - 30), P(cx + step * 0.45, y + h / 2 - 30), P(cx, y - 10 + bob)], fill=CONE)
    aa(img, (x - w / 2 - 6, y - h / 2 - 6, x + w / 2 + 6, y + h / 2 + 6), fn, a)

@V.scene("rods")
def _(img, T, t, s, e):
    a = win(T, s, e)
    kh = eo((T - s - 0.3) / 1.0)
    kc = eo((T - wt("packed", s) + 0.6) / 1.4)
    rods_panel(img, 270, 1040, 8, [1, 4, 7, 10], kh, a, T)
    rods_panel(img, 690, 1040, 24, [11], kc, a, T)
    lab(img, "human", 1260, INK_T, a * clamp((T - s - 0.4) / 0.3), x=270)
    lab(img, "cat", 1260, INK_T, a * clamp((T - early("packed", s, e) + 0.2) / 0.3), x=680)
    kr = clamp((T - early("dim", s, e, 3.0) + 0.1) / 0.3)
    lab(img, "dim-light cells", 775, RED_T, a * kr, x=480)
    R.chrome(img, T)
    title(img, T, s, e, "Step two: rods")
V.sounds("rods", [(0.1, "whoosh", 0.6), (rel("rods", "dim"), "tap", 0.6), (rel("rods", "packed"), "sparkle", 0.7)])

@V.scene("pupils")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ch = wt("change", s)
    k = eio((T - ch) / 1.2)
    pw = lerp(16, 230, k)
    cat_eye(img, 470, 1050, 640, 380, pw, a)
    kk = clamp((T - early("thirty-five", s, e) + 0.1) / 0.3)
    lab(img, "~135-fold area", 1270, RED_T, a * kk, x=470)
    R.chrome(img, T)
    title(img, T, s, e, "Slit pupils")
    return R.punch(img, T, wt("thirty-five", s))
V.sounds("pupils", [(0.1, "whoosh", 0.6), (rel("pupils", "change"), "whoosh", 0.7), (rel("pupils", "thirty-five"), "pop", 0.8)])

@V.scene("wide")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ou = wt("Ours", s)
    k2 = eo((T - ou) / 0.45)
    a1 = a * (1 - k2)
    sprite(img, "eye_dark", 270, 980, 300, a1 * clamp((T - s) / 0.3))
    sprite(img, "eye_normal", 650, 980, 300, a1 * clamp((T - wt("thin", s) + 0.2) / 0.3))
    lab(img, "in the dark", 1150, B.TEXT, a1 * clamp((T - s - 0.1) / 0.3), x=270)
    lab(img, "in sunlight", 1150, B.TEXT, a1 * clamp((T - early("thin", s, e, 3.0) + 0.1) / 0.3), x=650)
    if k2 > 0:
        sprite(img, "eye_human", 460, 1040 + 30 * (1 - k2), 300, a * k2)
        lab(img, "ours: ~15-fold", 1250, B.TEXT, a * clamp((T - early("fifteen", s, e) + 0.1) / 0.3), x=460)
    R.chrome(img, T)
    title(img, T, s, e, "Wide open, then a slit")
V.sounds("wide", [(0.1, "tap", 0.6), (rel("wide", "thin"), "click", 0.7), (rel("wide", "Ours"), "whoosh", 0.7), (rel("wide", "fifteen"), "pop", 0.6)])

@V.scene("sixth")
def _(img, T, t, s, e):
    a = win(T, s, e)
    base = 1290
    kh = eo((T - s - 0.3) / 0.8)
    one = wt("one-sixth", s)
    kc = eo((T - one + 0.2) / 0.6)
    hh, hc = 420 * kh, 70 * kc
    def fn(d, P, s_):
        d.line([P(130, base), P(860, base)], fill=INK_T, width=int(6 * s_))
        for i in range(1, 6):          # marcas de sextos en la barra humana
            yy = base - 420 * i / 6
            if 420 * i / 6 < hh: d.line([P(240, yy), P(400, yy)], fill=(200, 160, 60), width=int(3 * s_))
        if hh > 2: d.rounded_rectangle([P(240, base - hh), P(400, base)], radius=14 * s_, fill=(255, 210, 90), outline=INK_T, width=int(5 * s_))
        if hc > 2: d.rounded_rectangle([P(580, base - hc), P(740, base)], radius=14 * s_, fill=(255, 210, 90), outline=INK_T, width=int(5 * s_))
    aa(img, (110, 840, 880, base + 10), fn, a)
    sprite(img, "bulb", 320, base - hh - 70, 120, a * kh)
    lab(img, "light we need", 1305, INK_T, a * clamp((T - s - 0.3) / 0.3), x=320)
    lab(img, "about 1/6", base - hc - 80, RED_T, a * kc, x=660)
    sprite(img, "sit", 810, base - 2, 150, a * clamp((T - early("cat", s, e) + 0.1) / 0.3), anchor="bottom", name="cat")
    lab(img, "mirror + rods", 800, TEAL_T, a * clamp((T - early("mirror", s, e, 3.5) + 0.1) / 0.3), x=680)
    R.chrome(img, T)
    title(img, T, s, e, "One-sixth the light")
    return R.punch(img, T, one + 0.2)
V.sounds("sixth", [(0.1, "whoosh", 0.6), (0.4, "tap", 0.5), (rel("sixth", "one-sixth"), "pop", 0.9)])

@V.scene("zero")
def _(img, T, t, s, e):
    a = win(T, s, e)
    dark = eio((T - s - 0.2) / 1.6)
    glowing_eyes(img, CX - 60, 1060, 340, a * (1 - 0.85 * dark), glow=(1 - dark))
    kc = clamp((T - early("can't", s, e) + 0.1) / 0.3)
    lab(img, "nothing to bounce", 800, B.TEXT, a * clamp((T - early("bounce", s, e, 3.6) + 0.1) / 0.3), x=CX - 60)
    lab(img, "can't see either", 1260, B.TEXT, a * kc, x=CX - 60)
    R.chrome(img, T)
    title(img, T, s, e, "Zero light, zero sight")
V.sounds("zero", [(0.1, "whoosh", 0.6), (1.6, "tap", 0.4), (rel("zero", "can't"), "click", 0.7)])

@V.scene("take")
def _(img, T, t, s, e):
    a = win(T, s, e)
    x = 720 if CAT else CX - 40
    sprite(img, "moon", x - 40, 880, 140, a * clamp((T - s) / 0.4))
    pose = "happy" if t > 1.4 else "curious"
    sprite(img, pose, x, 1335, 300, a, anchor="bottom", name="cat")
    R.chrome(img, T)
    title(img, T, s, e, "Pretty impressive")
V.sounds("take", [(0.1, "whoosh", 0.6), (1.4, "sparkle", 0.6)])

@V.scene("wrap")
def _(img, T, t, s, e):
    x = 720 if CAT else CX - 40
    a = win(T, s, e + 1)
    glowing_eyes(img, x, 1060, 300, a, glow=0.8 + 0.2 * math.sin(T * 4))
    R.chrome(img, T)
    R.txt(img, "Trade eyes", TITLE_Y, "title", B.TEXT, win(T, s, V.outro_at + 1))
    R.txt(img, "with a cat?", TITLE_Y + 97, "title", ACC_T, win(T, s + 0.4, V.outro_at + 1))
    return R.punch(img, T, s + 0.1)
V.sounds("wrap", [(0.05, "whoosh", 0.7), (rel("wrap", "Tell"), "pop", 0.6)])

# ---------- fondos ----------
def night(img, T, t, seed=0):
    ST.landscape(img, T, night=True, terrain="pines", seed=seed)
def dusk(img, T, t):
    ST.landscape(img, T, sky_kind="dusk", terrain="pines", seed=4)
def card_bg(img, T, t): ST.card(img, CARD)
def stamp_bg(img, T, t):
    ST.landscape(img, T, night=True, terrain="pines", seed=2)
    s0 = V.sc["stamp"][0]
    ST.wow_moment(img, T, s0 + 0.05, "nature", "glitch", dur=max(1.0, V.word_time("myth", after=s0) - s0))
def zero_bg(img, T, t):
    night(img, T, t, seed=5)
    k = eio((t - 0.2) / 1.6)
    ov = Image.new("RGBA", (W, H), (4, 4, 10, int(225 * k)))
    img.alpha_composite(ov)

V.backdrop("hook")(night)
V.backdrop("stamp")(stamp_bg)
V.backdrop("glow")(lambda img, T, t: night(img, T, t, seed=1))
V.backdrop("bounce")(lambda img, T, t: night(img, T, t, seed=3))
for n in ("trick", "light", "rods", "pupils", "sixth"):
    V.backdrop(n)(card_bg)
V.backdrop("wide")(lambda img, T, t: (ST.sky(img, (10, 8, 34), (34, 22, 70), 0, H), ST.stars(img, T, 110, seed=9, y1=H - 200)))
V.backdrop("zero")(zero_bg)
V.backdrop("take")(dusk)
V.backdrop("wrap")(dusk)

if __name__ == "__main__":
    V.main()
