"""Mr. Whiskerfact v4: el estilo de línea fina del videoclip, pero más mono y amigable (cabeza grande y redonda, ojos grandes y brillantes, sonrisa abierta, mofletes).
Semi-realista: proporciones de gato de verdad, línea negra fina y uniforme, rellenos planos con muy poca sombra,
ojos almendrados con pupila vertical, pelo con borde a mechones (como el pelo y las copas de sus árboles).
  python3 mascota_v3.py  -> out/mascota_v4_propuestas.png
"""
import math, os
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
    # cuello de pelo
    shape(d, [(430, 700), (650, 700), (680, 820), (400, 820)], FUR)
    # hombros y ropa (caída natural, como sus personajes)
    torso = [(190, 1090), (220, 930), (300, 860), (430, 820), (540, 828), (650, 820), (780, 860), (860, 930), (890, 1090)]
    shape(d, torso, o["top"])
    d.polygon([P(*p) for p in spline([(170, 900), (260, 830), (300, 900), (260, 1090), (130, 1090)])], fill=o["top_s"])
    if o.get("under"):                                   # cazadora abierta con camiseta debajo
        shape(d, [(450, 795), (540, 820), (630, 795), (600, 1090), (480, 1090)], o["under"])
        stroke(d, [(450, 795), (470, 900), (480, 1090)]); stroke(d, [(630, 795), (612, 900), (600, 1090)])
        stroke(d, [(330, 880), (350, 960)], 2.5); stroke(d, [(760, 880), (740, 960)], 2.5)          # pliegues
    else:
        stroke(d, [(470, 796), (540, 840), (610, 796)])                                            # cuello redondo / camisa
        stroke(d, [(330, 900), (345, 990)], 2.5); stroke(d, [(752, 900), (738, 990)], 2.5)
    if o.get("bowtie"):
        shape(d, [(540, 840), (482, 812), (488, 870)], (148, 40, 52), smooth=False)
        shape(d, [(540, 840), (600, 820), (596, 878)], (148, 40, 52), smooth=False)
        shape(d, [(528, 828), (552, 828), (554, 852), (526, 852)], (118, 30, 42), smooth=False)
        stroke(d, [(540, 860), (544, 1090)], 2.5)
    if o.get("headphones"):
        stroke(d, [(400, 820), (420, 760), (540, 735), (660, 760), (680, 820)], 22, INK)
        stroke(d, [(400, 820), (420, 760), (540, 735), (660, 760), (680, 820)], 15, (64, 64, 70))
        for x in (392, 688):
            shape(d, [(x - 36, 790), (x + 36, 790), (x + 40, 870), (x - 40, 870)], (64, 64, 70))

def head(d, wink=False):
    # orejas: más cortas y redondeadas
    for sx in (-1, 1):
        base = 540 + sx * 200
        shape(d, [(base - sx * 120, 300), (base - sx * 10, 150), (base + sx * 50, 130), (base + sx * 110, 330)], FUR)
        shape(d, [(base - sx * 70, 290), (base + sx * 6, 190), (base + sx * 70, 300)], EAR_IN, line=False)
        for k in range(2):
            stroke(d, [(base + sx * (14 + k * 20), 286), (base + sx * (24 + k * 18), 236)], 2)
    # cabeza grande y redonda, mejillas mullidas con 3 mechones suaves por lado
    pts = spline([(540, 236), (690, 262), (800, 360), (842, 500), (836, 600), (868, 640), (820, 660), (842, 700),
                  (770, 730), (660, 790), (540, 806), (420, 790), (310, 730), (238, 700), (260, 660), (212, 640),
                  (244, 600), (238, 500), (280, 360), (390, 262)], n=10)
    d.polygon([P(*p) for p in pts], fill=FUR)
    d.line([P(*p) for p in pts] + [P(*pts[0])], fill=INK, width=int(LW * S), joint="curve")
    d.polygon([P(*p) for p in spline([(720, 290), (800, 380), (830, 520), (790, 680), (680, 770), (760, 640), (780, 480)])], fill=FUR_S)
    # rayas de atigrado más suaves
    for x0, top, w in ((496, 262, 14), (540, 246, 18), (584, 262, 14)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, top), (x0 + w / 2, top), (x0 + w / 4, top + 84), (x0, top + 92), (x0 - w / 4, top + 84)])], fill=STRIPE)
    for sx in (-1, 1):
        for k in range(2):
            y = 600 + k * 40
            d.polygon([P(*p) for p in spline([(540 + sx * 300, y - 6), (540 + sx * 230, y), (540 + sx * 300, y + 12)])], fill=STRIPE)
    # mofletes sonrosados
    for sx in (-1, 1):
        d.ellipse([P(540 + sx * 205 - 52, 600), P(540 + sx * 205 + 52, 650)], fill=(236, 156, 166))
    # hocico claro, más pequeño y redondo
    shape(d, [(460, 640), (500, 600), (540, 594), (580, 600), (620, 640), (600, 704), (540, 724), (480, 704)], FUR_L, line=False)
    # nariz pequeña de corazón y sonrisa abierta
    shape(d, [(522, 604), (540, 600), (558, 604), (552, 618), (540, 628), (528, 618)], NOSE)
    stroke(d, [(540, 628), (540, 646)])
    shape(d, [(506, 650), (540, 648), (574, 650), (566, 676), (540, 690), (514, 676)], (150, 54, 68))
    d.ellipse([P(526, 668), P(554, 688)], fill=(232, 120, 132))
    stroke(d, [(540, 646), (520, 652), (500, 646)]); stroke(d, [(540, 646), (560, 652), (580, 646)])
    # bigotes
    for sx in (-1, 1):
        for k, dy in enumerate((0, 16, 32)):
            stroke(d, [(540 + sx * 90, 660 + dy * 0.5), (540 + sx * 220, 652 + dy), (540 + sx * 330, 650 + dy * 1.6)], 2)
    # ojos grandes y brillantes (redondeados, iris ámbar, pupila grande y redonda, dos brillos)
    for sx in (-1, 1):
        cx, cy = 540 + sx * 120, 480
        if wink and sx == 1:
            stroke(d, [(cx - 52, cy + 6), (cx, cy - 18), (cx + 52, cy + 6)], 5); continue
        shape(d, [(cx - 62, cy), (cx - 40, cy - 52), (cx + 40, cy - 54), (cx + 64, cy - 2), (cx + 40, cy + 54), (cx - 40, cy + 54)], (252, 250, 244))
        d.ellipse([P(cx - 48, cy - 50), P(cx + 48, cy + 50)], fill=AMBER)
        d.chord([P(cx - 48, cy - 50), P(cx + 48, cy + 50)], 190, 350, fill=AMBER_D)
        d.ellipse([P(cx - 26, cy - 28), P(cx + 26, cy + 30)], fill=INK)
        d.ellipse([P(cx + 2, cy - 30), P(cx + 26, cy - 6)], fill=(255, 255, 255))
        d.ellipse([P(cx - 22, cy + 10), P(cx - 10, cy + 22)], fill=(255, 255, 255))
        stroke(d, [(cx - 64, cy + 2), (cx - 40, cy - 56), (cx + 40, cy - 58), (cx + 66, cy - 2)], 5)
    # gafas redondas finas
    for sx in (-1, 1):
        cx = 540 + sx * 120
        d.ellipse([P(cx - 88, 394), P(cx + 88, 566)], outline=INK, width=int(5 * S))
        stroke(d, [(cx - 58, 420), (cx - 34, 408)], 4, (255, 255, 255))
    stroke(d, [(512, 476), (540, 464), (568, 476)], 5)
    # cejas alegres, una levantada
    stroke(d, [(392, 370), (430, 356), (470, 360)], 5)
    stroke(d, [(610, 350), (650, 340), (690, 352)], 5)

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
    sheet.save(os.path.join(OUT, "mascota_v4_propuestas.png")); print("ok")
