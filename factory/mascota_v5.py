"""Mr. Whiskerfact v5 (forma tipo retrato «gato con cuerpo de persona», referencia de la autora) · antes v4: el estilo de línea fina del videoclip, pero más mono y amigable (cabeza grande y redonda, ojos grandes y brillantes, sonrisa abierta, mofletes).
Semi-realista: proporciones de gato de verdad, línea negra fina y uniforme, rellenos planos con muy poca sombra,
ojos almendrados con pupila vertical, pelo con borde a mechones (como el pelo y las copas de sus árboles).
  python3 mascota_v3.py  -> out/mascota_v5_propuestas.png
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
    # orejas grandes en las esquinas: el borde exterior sube casi recto desde el lado de la cabeza
    for sx in (-1, 1):
        shape(d, [(X(300, sx), 380), (X(298, sx), 250), (X(318, sx), 126), (X(336, sx), 118), (X(470, sx), 250)], FUR)
        shape(d, [(X(318, sx), 300), (X(330, sx), 166), (X(342, sx), 160), (X(436, sx), 262)], EAR_IN, line=False)
        tuft = [(X(322, sx), 300), (X(340, sx), 236), (X(350, sx), 290), (X(366, sx), 222), (X(376, sx), 288), (X(394, sx), 236), (X(400, sx), 290)]
        d.polygon([P(*p) for p in tuft] + [P(X(400, sx), 310), P(X(322, sx), 310)], fill=FUR_L)
        stroke(d, tuft, 2, smooth=False)
    # cabeza ancha (más ancha que alta): parte de arriba casi plana entre las orejas, lados casi rectos que se abren
    # un poco en los mofletes, mandíbula en U ancha
    # pentágono invertido con esquinas suaves: arriba ancho y casi plano, lados casi rectos, y se cierra en una barbilla redondeada
    pts = spline([(540, 252), (680, 252), (770, 268), (796, 330), (800, 440), (796, 530), (760, 600), (690, 668),
                  (610, 718), (540, 734), (470, 718), (390, 668), (320, 600), (284, 530), (280, 440), (284, 330),
                  (310, 268), (400, 252)], n=10)
    d.polygon([P(*p) for p in pts], fill=FUR)
    d.line([P(*p) for p in pts] + [P(*pts[0])], fill=INK, width=int(LW * S), joint="curve")
    d.polygon([P(*p) for p in spline([(730, 268), (792, 340), (798, 520), (750, 610), (640, 700), (730, 580), (760, 420)])], fill=FUR_S)
    # rayas de la frente
    for x0, top, w in ((506, 254, 14), (540, 248, 18), (574, 254, 14)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, top), (x0 + w / 2, top), (x0 + w / 4, top + 70), (x0, top + 76), (x0 - w / 4, top + 70)])], fill=STRIPE)
    # mofletes rosados
    for sx in (-1, 1):
        d.ellipse([P(540 + sx * 172 - 44, 548), P(540 + sx * 172 + 44, 586)], fill=(236, 156, 166))
    # hocico claro y redondeado
    shape(d, [(540, 572), (600, 580), (636, 612), (628, 660), (590, 694), (540, 704), (490, 694), (452, 660), (444, 612), (480, 580)], FUR_L, line=False)
    for sx in (-1, 1):
        for k in range(3):
            cx, cy = 540 + sx * (66 + k * 14), 610 + k * 10
            d.ellipse([P(cx - 3, cy - 3), P(cx + 3, cy + 3)], fill=(150, 146, 146))
    # nariz de corazón
    shape(d, [(522, 556), (540, 551), (558, 556), (553, 572), (540, 583), (527, 572)], NOSE)
    stroke(d, [(540, 583), (540, 598)])
    # sonrisa grande y abierta: labio en W y boca en D con lengua
    mouth = [(486, 602), (512, 606), (540, 598), (568, 606), (594, 602), (586, 640), (566, 668), (540, 678), (514, 668), (494, 640)]
    shape(d, mouth, (128, 40, 56))
    tongue = [(512, 660), (526, 646), (540, 650), (554, 646), (568, 660), (556, 674), (540, 678), (524, 674)]
    d.polygon([P(*p) for p in spline(tongue)], fill=(236, 120, 136))
    stroke(d, [(486, 602), (512, 610), (540, 598)], 4); stroke(d, [(540, 598), (568, 610), (594, 602)], 4)
    for sx in (-1, 1):                                     # comisuras hacia arriba
        stroke(d, [(540 + sx * 54, 602), (540 + sx * 64, 592)], 4)
    # bigotes
    for sx in (-1, 1):
        for dy in (0, 14, 28):
            stroke(d, [(540 + sx * 96, 612 + dy * 0.5), (540 + sx * 200, 604 + dy), (540 + sx * 300, 600 + dy * 1.6)], 2)
    # ojos grandes y brillantes
    for sx in (-1, 1):
        cx, cy = 540 + sx * 104, 448
        if wink and sx == 1:
            stroke(d, [(cx - 44, cy + 6), (cx, cy - 16), (cx + 44, cy + 6)], 5); continue
        shape(d, [(cx - 52, cy), (cx - 32, cy - 44), (cx + 32, cy - 46), (cx + 54, cy - 2), (cx + 32, cy + 46), (cx - 32, cy + 46)], (252, 250, 244))
        d.ellipse([P(cx - 40, cy - 42), P(cx + 40, cy + 42)], fill=AMBER)
        d.chord([P(cx - 40, cy - 42), P(cx + 40, cy + 42)], 190, 350, fill=AMBER_D)
        d.ellipse([P(cx - 21, cy - 23), P(cx + 21, cy + 25)], fill=INK)
        d.ellipse([P(cx + 2, cy - 25), P(cx + 22, cy - 5)], fill=(255, 255, 255))
        d.ellipse([P(cx - 18, cy + 8), P(cx - 8, cy + 18)], fill=(255, 255, 255))
        stroke(d, [(cx - 54, cy + 2), (cx - 32, cy - 48), (cx + 32, cy - 50), (cx + 56, cy - 2)], 5)
    # gafas: montura gruesa redondeada (como la referencia) pero en marrón oscuro
    for sx in (-1, 1):
        cx = 540 + sx * 104
        d.rounded_rectangle([P(cx - 80, 384), P(cx + 80, 512)], radius=50 * S, outline=INK, width=int(10 * S))
        d.rounded_rectangle([P(cx - 76, 388), P(cx + 76, 508)], radius=46 * S, outline=(92, 60, 44), width=int(5 * S))
        stroke(d, [(cx - 56, 408), (cx - 34, 398)], 4, (255, 255, 255))
    stroke(d, [(520, 438), (540, 428), (560, 438)], 7)
    stroke(d, [(356, 420), (290, 412)], 6); stroke(d, [(724, 420), (790, 412)], 6)
    # cejas alegres
    stroke(d, [(410, 360), (442, 348), (476, 352)], 5)
    stroke(d, [(604, 342), (638, 332), (670, 344)], 5)

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
