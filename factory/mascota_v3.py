"""Mr. Whiskerfact v3: dibujado como los personajes del videoclip de la autora.
Semi-realista: proporciones de gato de verdad, línea negra fina y uniforme, rellenos planos con muy poca sombra,
ojos almendrados con pupila vertical, pelo con borde a mechones (como el pelo y las copas de sus árboles).
  python3 mascota_v3.py  -> out/mascota_v3_propuestas.png
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
    torso = [(130, 1090), (170, 900), (260, 830), (420, 790), (540, 800), (660, 790), (820, 830), (910, 900), (950, 1090)]
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
    # orejas: altas, punta algo redondeada, mechones dentro
    for sx in (-1, 1):
        base = 540 + sx * 175
        shape(d, [(base - sx * 110, 330), (base + sx * 30, 120), (base + sx * 70, 110), (base + sx * 120, 360)], FUR)
        shape(d, [(base - sx * 60, 320), (base + sx * 38, 170), (base + sx * 88, 340)], EAR_IN, line=False)
        for k in range(3):
            stroke(d, [(base + sx * (20 + k * 18), 300), (base + sx * (34 + k * 16), 230 + k * 10)], 2)
    # cabeza: frente redondeada, mejillas anchas con mechones, barbilla estrecha
    outline = spline([(300, 470), (330, 330), (440, 255), (540, 240), (640, 255), (750, 330), (780, 470)], closed=False)
    cheekR = tufts(540, 560, 250, 190, -10, 70, 6, 0.08, seed=1)
    chin = [(600, 760), (540, 772), (480, 760)]
    cheekL = tufts(540, 560, 250, 190, 110, 190, 6, 0.08, seed=2)
    pts = outline + cheekR + chin + cheekL
    d.polygon([P(*p) for p in pts], fill=FUR)
    d.line([P(*p) for p in pts] + [P(*pts[0])], fill=INK, width=int(LW * S), joint="curve")
    # sombra plana suave en el lado derecho
    d.polygon([P(*p) for p in spline([(700, 290), (770, 400), (790, 560), (720, 700), (640, 750), (720, 600), (740, 440)])], fill=FUR_S)
    # rayas de atigrado: la «M» de la frente y mejillas, formas orgánicas
    for x0, top, w in ((490, 280, 16), (540, 262, 20), (590, 280, 16)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, top), (x0 + w / 2, top), (x0 + w / 4, top + 110), (x0, top + 120), (x0 - w / 4, top + 110)])], fill=STRIPE)
    for sx in (-1, 1):
        for k in range(3):
            y = 560 + k * 38
            d.polygon([P(*p) for p in spline([(540 + sx * 290, y - 6), (540 + sx * 200, y), (540 + sx * 290, y + 12)])], fill=STRIPE)
        stroke(d, [(540 + sx * 60, 400), (540 + sx * 170, 380), (540 + sx * 240, 410)], 9, STRIPE)
    # hocico claro con almohadillas de bigotes
    shape(d, [(450, 640), (490, 580), (540, 570), (590, 580), (630, 640), (600, 720), (540, 740), (480, 720)], FUR_L, line=False)
    for sx in (-1, 1):
        for k in range(3):
            d.ellipse([P(540 + sx * (38 + k * 16) - 3, 652 + k * 10 - 3), P(540 + sx * (38 + k * 16) + 3, 652 + k * 10 + 3)], fill=(150, 146, 146))
    # nariz: triángulo rosa con puente, filtrum y boca en W con media sonrisa
    stroke(d, [(522, 520), (528, 580)], 2.5); stroke(d, [(558, 520), (552, 580)], 2.5)
    shape(d, [(516, 592), (564, 592), (540, 622)], NOSE, smooth=False)
    stroke(d, [(540, 622), (540, 646)])
    stroke(d, [(540, 646), (522, 662), (500, 660), (486, 650)])
    stroke(d, [(540, 646), (558, 662), (580, 660), (596, 648)])
    # bigotes finos y largos
    for sx in (-1, 1):
        for k, (dy, ang) in enumerate(((0, -4), (14, 4), (28, 12))):
            stroke(d, [(540 + sx * 70, 650 + dy), (540 + sx * 200, 640 + dy + ang * 2), (540 + sx * 330, 630 + dy + ang * 5)], 2)
    # ojos almendrados, iris ámbar, pupila vertical
    for sx in (-1, 1):
        cx, cy = 540 + sx * 112, 470
        if wink and sx == 1:
            stroke(d, [(cx - 52, cy + 4), (cx, cy + 16), (cx + 52, cy + 2)], 4); continue
        eye = [(cx - 54, cy + 4), (cx - 20, cy - 32), (cx + 30, cy - 30), (cx + 56, cy - 2), (cx + 22, cy + 30), (cx - 26, cy + 30)]
        shape(d, eye, AMBER)
        d.polygon([P(*p) for p in spline([(cx - 50, cy), (cx - 20, cy - 28), (cx + 30, cy - 26), (cx + 52, cy - 4), (cx + 10, cy - 12), (cx - 30, cy - 8)])], fill=AMBER_D)
        d.ellipse([P(cx - 9, cy - 27), P(cx + 9, cy + 27)], fill=INK)
        d.ellipse([P(cx + 10, cy - 18), P(cx + 22, cy - 6)], fill=(255, 255, 255))
        stroke(d, [(cx - 58, cy + 6), (cx - 20, cy - 36), (cx + 30, cy - 34), (cx + 62, cy - 4)], 5)   # párpado superior marcado
    # gafas redondas finas
    for sx in (-1, 1):
        cx = 540 + sx * 112
        d.ellipse([P(cx - 84, 392), P(cx + 84, 548)], outline=INK, width=int(5 * S))
        stroke(d, [(cx - 54, 420), (cx - 30, 408)], 4, (255, 255, 255))
    stroke(d, [(512, 466), (540, 454), (568, 466)], 5)
    stroke(d, [(456, 466), (300, 450)], 4); stroke(d, [(624, 466), (780, 450)], 4)                  # patillas
    # cejas de pelo, una algo levantada (gesto de «¿sabías que…?»)
    stroke(d, [(400, 382), (440, 370), (478, 374)], 4)
    stroke(d, [(602, 366), (642, 356), (682, 368)], 4)

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
    sheet.save(os.path.join(OUT, "mascota_v3_propuestas.png")); print("ok")
