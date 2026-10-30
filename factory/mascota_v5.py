"""Mr. Whiskerfact v5 (forma tipo retrato «gato con cuerpo de persona», referencia de la autora) · antes v4: el estilo de línea fina del videoclip, pero más mono y amigable (cabeza grande y redonda, ojos grandes y brillantes, sonrisa abierta, mofletes).
Semi-realista: proporciones de gato de verdad, línea negra fina y uniforme, rellenos planos con muy poca sombra,
ojos almendrados con pupila vertical, pelo con borde a mechones (como el pelo y las copas de sus árboles).
  python3 mascota_v3.py  -> out/mascota_v5_propuestas.png
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw
import brand as B

S = 3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
INK = (22, 18, 20)
LW = 3.5                                  # grosor de línea: fino, como en el videoclip
FUR, FUR_S, FUR_L, STRIPE = (150, 152, 160), (128, 130, 140), (226, 224, 220), (86, 88, 100)
EAR_IN, NOSE = (226, 160, 160), (206, 128, 136)
AMBER, AMBER_D = (232, 168, 60), (186, 116, 34)
NAVY1, NAVY2 = (24, 30, 64), (40, 48, 96)

OUTFITS = {
    "bomber": dict(label="Cazadora y camiseta", top=(96, 110, 74), top_s=(78, 90, 58), under=(244, 240, 228)),
    "tee":    dict(label="Camiseta y cascos", top=(54, 92, 62), top_s=(42, 76, 50), under=None, headphones=True),
    "shirt":  dict(label="Camisa remangada y pajarita suelta", top=(236, 232, 216), top_s=(212, 206, 186), under=None, bowtie=True),
}

def P(x, y): return (x * S, y * S)

def spline(pts, n=12, closed=True):
    out = []; L = len(pts); rng = range(L) if closed else range(L - 1)
    for i in rng:
        p0 = pts[i - 1] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % L]
        p3 = pts[(i + 2) % L] if (closed or i + 2 < L) else pts[-1]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    if not closed: out.append(pts[-1])
    return out

def shape(d, pts, fill, line=True, w=LW, smooth=True):
    q = spline(pts) if smooth else pts
    d.polygon([P(*p) for p in q], fill=fill)
    if line: d.line([P(*p) for p in q] + [P(*q[0])], fill=INK, width=int(w * S), joint="curve")

def stroke(d, pts, w=LW, col=INK, smooth=True):
    q = spline(pts, closed=False) if smooth else pts
    d.line([P(*p) for p in q], fill=col, width=int(w * S), joint="curve")

def tufts(cx, cy, rx, ry, a0, a1, n, depth, seed=0):
    """borde de pelo a mechones a lo largo de un arco de elipse (de a0 a a1 grados)"""
    rng = np.random.default_rng(seed); pts = []
    for k in range(n * 2 + 1):
        a = math.radians(a0 + (a1 - a0) * k / (n * 2))
        r = 1.0 + (depth * rng.uniform(0.7, 1.2) if k % 2 else 0)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts

def body(d, o):
    """hombros anchos de persona; la cabeza se apoya directamente en el cuello de la ropa"""
    torso = [(110, 1090), (130, 880), (230, 780), (400, 720), (540, 712), (680, 720), (850, 780), (950, 880), (970, 1090)]
    shape(d, torso, o["top"])
    if o.get("under"):                                   # cazadora abierta + camiseta
        shape(d, [(440, 716), (540, 760), (640, 716), (610, 1090), (470, 1090)], o["under"])
        shape(d, [(400, 720), (450, 716), (490, 1090), (400, 1090), (360, 820)], o["top_s"])
        shape(d, [(680, 720), (630, 716), (590, 1090), (680, 1090), (720, 820)], o["top_s"])
        stroke(d, [(250, 860), (280, 960)], 2.5); stroke(d, [(830, 860), (800, 960)], 2.5)
    else:
        shape(d, [(450, 712), (540, 756), (630, 712), (612, 738), (540, 778), (468, 738)], o["top_s"])   # cuello
        stroke(d, [(250, 860), (280, 960)], 2.5); stroke(d, [(830, 860), (800, 960)], 2.5)
    if o.get("bowtie"):
        shape(d, [(540, 772), (474, 742), (480, 806)], (148, 40, 52), smooth=False)
        shape(d, [(540, 772), (604, 748), (600, 810)], (148, 40, 52), smooth=False)
        shape(d, [(528, 760), (552, 760), (554, 784), (526, 784)], (118, 30, 42), smooth=False)
        stroke(d, [(540, 800), (544, 1090)], 2.5)
    if o.get("headphones"):
        stroke(d, [(410, 760), (430, 700), (540, 680), (650, 700), (670, 760)], 22, INK)
        stroke(d, [(410, 760), (430, 700), (540, 680), (650, 700), (670, 760)], 15, (64, 64, 70))
        for x in (404, 676):
            shape(d, [(x - 38, 728), (x + 38, 728), (x + 42, 812), (x - 42, 812)], (64, 64, 70))

def head(d, wink=False):
    X = lambda x, sx: 540 + sx * (x - 540)
    # silueta de cabeza + orejas sacada de la referencia de la autora (head_ref.json, simetrizada)
    ref = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "head_ref.json")))
    sil = spline([tuple(p) for p in ref["pts"]], n=6)
    M = lambda xr, yr: (540 + (xr - ref["cx"]) * ref["sc"], 105 + (yr - ref["y0"]) * ref["sc"])
    # sombra lateral: silueta en gris oscuro y, encima, la misma silueta desplazada a la izquierda en gris normal
    big = d._image
    m1 = Image.new("L", big.size, 0); ImageDraw.Draw(m1).polygon([P(*p) for p in sil], fill=255)
    m2 = Image.new("L", big.size, 0); ImageDraw.Draw(m2).polygon([P(x - 22, y) for x, y in sil], fill=255)
    big.paste(FUR_S, (0, 0), m1)
    big.paste(FUR, (0, 0), Image.fromarray(np.minimum(np.asarray(m1), np.asarray(m2))))
    d.line([P(*p) for p in sil] + [P(*sil[0])], fill=INK, width=int(LW * S), joint="curve")
    # interior de las orejas con mechones
    for sx in (-1, 1):
        X = lambda x: 540 + sx * (x - 540)
        e = [M(158, 104), M(165, 66), M(204, 100)]
        e = [(X(x), y) for x, y in e]
        d.polygon([P(*p) for p in e], fill=EAR_IN)
        tip, b1, b2 = e[1], e[0], e[2]
        for k in range(4):                                   # mechones finos saliendo del interior de la oreja
            t = 0.2 + k * 0.2
            bx, by = b1[0] + (b2[0] - b1[0]) * t, b1[1] + (b2[1] - b1[1]) * t
            stroke(d, [(bx, by), (bx + (tip[0] - bx) * 0.45, by + (tip[1] - by) * 0.55)], 3, FUR_L, smooth=False)
    # rayas de la frente
    for x0, top, w in ((508, 250, 14), (540, 244, 18), (572, 250, 14)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, top), (x0 + w / 2, top), (x0 + w / 4, top + 70), (x0, top + 76), (x0 - w / 4, top + 70)])], fill=STRIPE)
    # coloretes en los mofletes
    for sx in (-1, 1):
        d.ellipse([P(540 + sx * 205 - 50, 560), P(540 + sx * 205 + 50, 600)], fill=(236, 156, 166))
    # almohadillas de los bigotes: dos curvas grandes que forman una W ancha bajo la nariz (como la referencia)
    for sx in (-1, 1):
        pad = [(540, 590), (540 + sx * 60, 568), (540 + sx * 128, 590), (540 + sx * 140, 636), (540 + sx * 96, 668), (540 + sx * 30, 664), (540, 640)]
        shape(d, pad, FUR_L)
        for k in range(3):
            cx, cy = 540 + sx * (66 + k * 18), 604 + k * 10
            d.ellipse([P(cx - 3.5, cy - 3.5), P(cx + 3.5, cy + 3.5)], fill=(150, 146, 146))
    # barbilla redonda bajo las almohadillas
    stroke(d, [(470, 676), (540, 712), (610, 676)], 3.5)
    # nariz de corazón
    shape(d, [(520, 560), (540, 554), (560, 560), (555, 578), (540, 590), (525, 578)], NOSE)
    # boca abierta y sonriente entre las almohadillas
    shape(d, [(506, 640), (540, 632), (574, 640), (566, 672), (540, 690), (514, 672)], (128, 40, 56))
    d.polygon([P(*p) for p in spline([(518, 672), (530, 660), (540, 664), (550, 660), (562, 672), (540, 688)])], fill=(236, 120, 136))
    # bigotes largos
    for sx in (-1, 1):
        for dy in (0, 16, 32):
            stroke(d, [(540 + sx * 120, 610 + dy * 0.6), (540 + sx * 220, 600 + dy), (540 + sx * 330, 594 + dy * 1.7)], 2.4)
    # ojos grandes y brillantes
    for sx in (-1, 1):
        cx, cy = 540 + sx * 122, 446
        if wink and sx == 1:
            stroke(d, [(cx - 44, cy + 6), (cx, cy - 16), (cx + 44, cy + 6)], 5); continue
        shape(d, [(cx - 54, cy), (cx - 34, cy - 46), (cx + 34, cy - 48), (cx + 56, cy - 2), (cx + 34, cy + 46), (cx - 34, cy + 46)], (252, 250, 244))
        d.ellipse([P(cx - 42, cy - 44), P(cx + 42, cy + 44)], fill=AMBER)
        d.chord([P(cx - 42, cy - 44), P(cx + 42, cy + 44)], 190, 350, fill=AMBER_D)
        d.ellipse([P(cx - 22, cy - 24), P(cx + 22, cy + 26)], fill=INK)
        d.ellipse([P(cx + 2, cy - 26), P(cx + 24, cy - 4)], fill=(255, 255, 255))
        d.ellipse([P(cx - 20, cy + 8), P(cx - 9, cy + 19)], fill=(255, 255, 255))
        stroke(d, [(cx - 56, cy + 2), (cx - 34, cy - 50), (cx + 34, cy - 52), (cx + 58, cy - 2)], 5)
    # gafas anchas de pasta (como la referencia): casi todo el ancho de la cara
    for sx in (-1, 1):
        cx = 540 + sx * 128
        d.rounded_rectangle([P(cx - 112, 380), P(cx + 112, 506)], radius=40 * S, outline=INK, width=int(12 * S))
        d.rounded_rectangle([P(cx - 107, 385), P(cx + 107, 501)], radius=36 * S, outline=(92, 60, 44), width=int(7 * S))
        stroke(d, [(cx - 80, 402), (cx - 50, 394)], 4, (255, 255, 255))
    stroke(d, [(522, 420), (540, 412), (558, 420)], 9)
    # cejas: una levantada, gesto de «¿sabías que…?»
    stroke(d, [(394, 352), (430, 338), (470, 342)], 7, STRIPE)
    stroke(d, [(612, 334), (652, 322), (690, 334)], 7, STRIPE)

def avatar(outfit="bomber", size=1080, wink=False):
    big = Image.new("RGBA", (1080 * S, 1080 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    d.ellipse([P(0, 0), P(1080, 1080)], fill=NAVY1); d.ellipse([P(60, 60), P(1020, 1020)], fill=NAVY2)
    layer = Image.new("RGBA", big.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    body(ld, OUTFITS[outfit]); head(ld, wink)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse([P(10, 10), P(1070, 1070)], fill=255)
    a = np.minimum(np.asarray(layer.split()[3]), np.asarray(mask))
    layer.putalpha(Image.fromarray(a)); big.alpha_composite(layer)
    d = ImageDraw.Draw(big)
    d.ellipse([P(14, 14), P(1066, 1066)], outline=B.GOLD, width=int(26 * S))
    d.ellipse([P(2, 2), P(1078, 1078)], outline=INK, width=int(5 * S))
    return big.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    from PIL import ImageFont
    tiles = [(o["label"], avatar(k, 520)) for k, o in OUTFITS.items()]
    sheet = Image.new("RGB", (3 * 560 + 40, 640), (233, 226, 190))
    f = ImageFont.truetype(B.FONT_DIR + "InterDisplay-SemiBold.otf", 26); dd = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        x = 40 + i * 560; sheet.paste(im, (x, 40), im)
        dd.text((x + 260, 590), f"{i + 1}. {lab}", font=f, fill=INK, anchor="mm")
    sheet.save(os.path.join(OUT, "mascota_v5_propuestas.png")); print("ok")
