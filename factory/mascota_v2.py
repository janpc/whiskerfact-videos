"""Mr. Whiskerfact v2: el mismo gato (atigrado gris, ojos ámbar, gafas redondas, aro dorado) redibujado con el estilo
de la autora: contorno fino marrón oscuro, rellenos planos con una sola sombra, formas suaves. Profe joven y guay.
  python3 mascota_v2.py            -> out/mascota_v2_propuestas.png (las tres versiones de ropa)
"""
import math, os
from PIL import Image, ImageDraw
import brand as B
import style as ST

S = 3                                   # sobremuestreo
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
INK = ST.OUTLINE
FUR, FUR_S, FUR_L = (148, 152, 164), (118, 122, 136), (206, 208, 214)
STRIPE = (92, 96, 112)
PINK, NOSE = (238, 168, 176), (214, 120, 132)
AMBER, AMBER_D, PUPIL = (240, 172, 54), (196, 120, 30), (34, 26, 24)
NAVY1, NAVY2 = (24, 30, 64), (40, 48, 96)

OUTFITS = {
    "bomber": dict(label="Cazadora y camiseta", jacket=(94, 110, 70), jacket_s=(72, 86, 52), shirt=(246, 242, 230), extra="zip"),
    "tee":    dict(label="Camiseta y cascos", jacket=None, shirt=(52, 92, 62), shirt_s=(40, 74, 50), extra="headphones"),
    "shirt":  dict(label="Camisa remangada y pajarita suelta", jacket=None, shirt=(236, 232, 214), shirt_s=(208, 202, 180), extra="bowtie"),
}

def P(x, y): return (x * S, y * S)
def W_(w): return int(w * S)

def smooth(pts, n=10):
    """curva cerrada suave por los puntos (Catmull-Rom): formas redondeadas, no facetadas"""
    out = []; L = len(pts)
    for i in range(L):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % L], pts[(i + 2) % L]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    return out

def ol_poly(d, pts, fill, w=5):
    d.polygon([P(*p) for p in pts], fill=fill)
    d.line([P(*p) for p in pts] + [P(*pts[0])], fill=INK, width=W_(w), joint="curve")

def ol_ell(d, box, fill, w=5):
    x0, y0, x1, y1 = box
    d.ellipse([P(x0, y0), P(x1, y1)], fill=fill, outline=INK, width=W_(w))

def body(d, o):
    """torso y ropa (zona baja del círculo)"""
    if o.get("jacket"):
        ol_poly(d, [(200, 1080), (260, 810), (440, 750), (640, 750), (820, 810), (880, 1080)], o["jacket"])
        ol_poly(d, [(445, 756), (540, 910), (635, 756)], o["shirt"])                         # camiseta en el escote
        ol_poly(d, [(445, 756), (500, 1080), (420, 1080), (380, 790)], o["jacket_s"])          # solapas
        ol_poly(d, [(635, 756), (580, 1080), (660, 1080), (700, 790)], o["jacket_s"])
        d.line([P(540, 910), P(540, 1080)], fill=INK, width=W_(4))                             # cremallera
    else:
        ol_poly(d, [(200, 1080), (260, 810), (440, 750), (640, 750), (820, 810), (880, 1080)], o["shirt"])
        d.polygon([P(300, 810), P(330, 1080), P(250, 1080)], fill=o["shirt_s"])
        d.polygon([P(780, 810), P(750, 1080), P(830, 1080)], fill=o["shirt_s"])
        ol_poly(d, [(470, 756), (540, 800), (610, 756), (590, 750), (540, 778), (490, 750)], o["shirt_s"], 4)   # cuello
    if o["extra"] == "bowtie":                                                                   # pajarita suelta, un poco torcida
        ol_poly(d, [(540, 796), (470, 762), (478, 828)], (150, 40, 52), 4)
        ol_poly(d, [(540, 796), (606, 772), (596, 834)], (150, 40, 52), 4)
        ol_ell(d, (522, 828, 558, 864), (120, 30, 42), 4)
        for x in (520, 560): d.line([P(x, 900), P(x + 6, 1080)], fill=INK, width=W_(3))      # tapeta de la camisa
    if o["extra"] == "headphones":                                                               # cascos al cuello (guiño al videoclip)
        d.arc([P(380, 700), P(700, 850)], 20, 160, fill=INK, width=W_(30))
        d.arc([P(380, 700), P(700, 850)], 20, 160, fill=(70, 70, 76), width=W_(22))
        ol_ell(d, (370, 780, 450, 880), (70, 70, 76)); ol_ell(d, (630, 780, 710, 880), (70, 70, 76))

def head(d, wink=False):
    # orejas
    for sx in (-1, 1):
        cx = 540 + sx * 230
        ol_poly(d, [(cx - sx * 90, 330), (cx + sx * 40, 120), (cx + sx * 110, 360)], FUR)
        ol_poly(d, [(cx - sx * 40, 320), (cx + sx * 36, 190), (cx + sx * 78, 335)], PINK, 4)
    # cabeza con mofletes
    ol_poly(d, smooth([(300, 410), (420, 296), (540, 276), (660, 296), (780, 410), (816, 560),
                       (760, 690), (640, 760), (540, 772), (440, 760), (320, 690), (264, 560)]), FUR, 6)
    # sombra de un lado (cel)
    d.polygon([P(*p) for p in smooth([(690, 312), (780, 410), (812, 560), (760, 690), (650, 752), (726, 640), (752, 520), (736, 410)], 6)], fill=FUR_S)
    for sx in (-1, 1):                                       # mofletes sonrosados
        cx = 540 + sx * 190
        d.ellipse([P(cx - 56, 600), P(cx + 56, 652)], fill=(232, 150, 160))
    # rayas de atigrado en la frente y mofletes
    for x0, w in ((500, 18), (540, 22), (580, 18)):
        d.polygon([P(x0 - w / 2, 290), P(x0 + w / 2, 290), P(x0 + w / 4, 380), P(x0 - w / 4, 380)], fill=STRIPE)
    for sx in (-1, 1):
        for k in range(3):
            y = 560 + k * 34
            d.line([P(540 + sx * 250, y), P(540 + sx * 190, y + 6)], fill=STRIPE, width=W_(10))
    # hocico claro
    ol_poly(d, smooth([(430, 610), (480, 566), (540, 556), (600, 566), (650, 610), (632, 690), (540, 724), (448, 690)]), (246, 244, 238), 4)
    # nariz y boca (sonrisa abierta)
    ol_poly(d, [(516, 588), (564, 588), (540, 616)], NOSE, 4)
    d.line([P(540, 616), P(540, 640)], fill=INK, width=W_(4))
    d.arc([P(488, 612), P(540, 668)], 10, 150, fill=INK, width=W_(4))
    d.arc([P(540, 612), P(592, 668)], 30, 170, fill=INK, width=W_(4))
    ol_poly(d, [(512, 650), (568, 650), (560, 676), (540, 684), (520, 676)], (160, 64, 76), 3)
    # bigotes
    for sx in (-1, 1):
        for k, dy in enumerate((-14, 6, 26)):
            d.line([P(540 + sx * 110, 620 + dy * 0.4), P(540 + sx * 290, 600 + dy * 1.6)], fill=INK, width=W_(3))
    # ojos ámbar
    for sx in (-1, 1):
        cx, cy = 540 + sx * 112, 480
        if wink and sx == 1:
            d.arc([P(cx - 50, cy - 34), P(cx + 50, cy + 40)], 200, 340, fill=INK, width=W_(7)); continue
        ol_ell(d, (cx - 58, cy - 62, cx + 58, cy + 62), (250, 246, 236), 5)
        ol_ell(d, (cx - 46, cy - 52, cx + 46, cy + 52), AMBER, 0)
        d.chord([P(cx - 46, cy - 52), P(cx + 46, cy + 52)], 200, 340, fill=AMBER_D)
        ol_ell(d, (cx - 19, cy - 34, cx + 19, cy + 34), PUPIL, 0)
        ol_ell(d, (cx + 2, cy - 34, cx + 24, cy - 12), (255, 255, 255), 0)
    # gafas redondas (más finas y modernas)
    for sx in (-1, 1):
        cx = 540 + sx * 112
        d.ellipse([P(cx - 78, 404), P(cx + 78, 556)], outline=INK, width=W_(9))
        d.ellipse([P(cx - 74, 408), P(cx + 74, 552)], outline=(60, 54, 58), width=W_(4))
        d.line([P(cx - 50, 430), P(cx - 26, 418)], fill=(255, 255, 255), width=W_(6))         # reflejo
    d.arc([P(498, 452), P(582, 500)], 200, 340, fill=INK, width=W_(8))                          # puente
    # cejas (expresivas: una algo levantada, gesto «¿sabías que…?»)
    d.line([P(388, 382), P(470, 368)], fill=STRIPE, width=W_(12))
    d.line([P(610, 362), P(692, 372)], fill=STRIPE, width=W_(12))

def avatar(outfit="bomber", size=1080, wink=False):
    big = Image.new("RGBA", (1080 * S, 1080 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    # disco navy con el aro dorado
    d.ellipse([P(0, 0), P(1080, 1080)], fill=NAVY1)
    d.ellipse([P(60, 60), P(1020, 1020)], fill=NAVY2)
    layer = Image.new("RGBA", big.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    body(ld, OUTFITS[outfit]); head(ld, wink)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse([P(10, 10), P(1070, 1070)], fill=255)
    clipped = Image.new("RGBA", big.size, (0, 0, 0, 0)); clipped.paste(layer, (0, 0), Image.composite(layer.split()[3], Image.new("L", big.size, 0), mask))
    big.alpha_composite(clipped)
    d = ImageDraw.Draw(big)
    d.ellipse([P(14, 14), P(1066, 1066)], outline=B.GOLD, width=W_(26))
    d.ellipse([P(2, 2), P(1078, 1078)], outline=INK, width=W_(6))
    return big.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    from PIL import ImageFont
    old = Image.open(os.path.join(OUT, "mrwhiskerfact_avatar.png")).convert("RGBA").resize((520, 520), Image.LANCZOS)
    tiles = [("Actual", old)] + [(o["label"], avatar(k, 520)) for k, o in OUTFITS.items()]
    sheet = Image.new("RGB", (4 * 560 + 40, 640), (233, 226, 190))
    f = ImageFont.truetype(B.FONT_DIR + "InterDisplay-SemiBold.otf", 26)
    dd = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        x = 40 + i * 560
        sheet.paste(im, (x, 40), im)
        dd.text((x + 260, 590), (f"{i}. " if i else "") + lab, font=f, fill=INK, anchor="mm")
    sheet.save(os.path.join(OUT, "mascota_v2_propuestas.png"))
    print("ok")
