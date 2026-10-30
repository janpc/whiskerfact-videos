"""Mr. Whiskerfact v6: desde cero, con las proporciones medidas punto a punto en la referencia de la autora
(puntas y bases de las orejas, ancho en la frente, mofletes, mandíbula y barbilla; línea de ojos, nariz y boca).
Es un dibujo propio con esa construcción, no un calco de la ilustración de stock.
  python3 mascota_v6.py -> out/mascota_v6.png y out/mascota_v6_vs_referencia.png
"""
import os
import numpy as np
from PIL import Image, ImageDraw
import brand as B
from mascota_v3 import P, S, INK, spline, shape, stroke

FUR, FUR_S, FUR_L, STRIPE = (150, 152, 160), (132, 134, 144), (214, 214, 214), (100, 102, 114)
EAR_IN, NOSE = (232, 176, 168), (226, 132, 112)
AMBER, AMBER_D = (232, 168, 60), (176, 112, 34)
NAVY1, NAVY2 = (24, 30, 64), (40, 48, 96)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def sym(pts_right):
    """recibe la mitad derecha (de arriba al centro de la barbilla) y devuelve el contorno cerrado simétrico"""
    left = [(1080 - x, y) for x, y in reversed(pts_right[1:-1])]
    return pts_right + left

# --- landmarks medidos en la referencia (mitad derecha, coordenadas del avatar de 1080) ---
HEAD_R = [(540, 228), (596, 232), (612, 238),            # arco de la frente entre las orejas
          (650, 196), (700, 140), (728, 108), (742, 106), # borde interior de la oreja hasta la punta
          (752, 130), (774, 220), (799, 331),             # borde exterior de la oreja, casi recto, baja hasta la sien
          (820, 438), (846, 520), (852, 560),             # lado de la cabeza que se abre hasta el moflete (lo más ancho)
          (840, 610), (808, 650), (740, 704), (640, 748), (540, 762)]   # mandíbula y barbilla

def head(d):
    out = spline(sym(HEAD_R), n=8)
    # oreja: interior rosado y mechones
    for sx in (-1, 1):
        X = lambda x: 540 + sx * (x - 540)
        d.polygon([P(*p) for p in spline([(X(626), 252), (X(700), 160), (X(732), 132), (X(752), 210), (X(764), 300)], n=8)], fill=EAR_IN)
    d.polygon([P(*p) for p in out], fill=FUR)
    # sombra suave del lado derecho
    m = [(x, y) for x, y in out if x > 700]
    d.polygon([P(*p) for p in spline([(760, 300), (810, 420), (846, 540), (820, 630), (720, 712), (790, 560), (790, 430)])], fill=FUR_S)
    d.line([P(*p) for p in out] + [P(*out[0])], fill=INK, width=int(3.5 * S), joint="curve")
    for sx in (-1, 1):                                    # repasar el interior de la oreja
        X = lambda x: 540 + sx * (x - 540)
        d.polygon([P(*p) for p in spline([(X(640), 262), (X(704), 180), (X(730), 150), (X(746), 220), (X(756), 300)], n=8)], fill=EAR_IN)
        for k in range(5):                                # mechones claros que salen del fondo de la oreja
            x0 = X(648 + k * 22); stroke(d, [(x0, 300), (x0 + sx * 10, 236 - k * 4), (x0 + sx * 4, 214 - k * 6)], 2.4, (244, 236, 228))
    # rayas de la frente
    for x0, w in ((508, 12), (540, 16), (572, 12)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, 240), (x0 + w / 2, 240), (x0 + w / 4, 312), (x0, 318), (x0 - w / 4, 312)])], fill=STRIPE)
    # ojos almendrados a la altura medida (y≈486), pupila vertical, párpado superior
    for sx in (-1, 1):
        cx, cy = 540 + sx * 126, 486
        eye = [(cx - 58, cy + 4), (cx - 22, cy - 26), (cx + 30, cy - 26), (cx + 58, cy - 2), (cx + 26, cy + 24), (cx - 28, cy + 24)]
        shape(d, eye, (250, 248, 240))
        d.ellipse([P(cx - 30, cy - 26), P(cx + 30, cy + 26)], fill=AMBER)
        d.chord([P(cx - 30, cy - 26), P(cx + 30, cy + 26)], 200, 340, fill=AMBER_D)
        d.ellipse([P(cx - 7, cy - 24), P(cx + 7, cy + 24)], fill=INK)
        d.ellipse([P(cx + 8, cy - 16), P(cx + 18, cy - 6)], fill=(255, 255, 255))
        stroke(d, [(cx - 62, cy + 6), (cx - 24, cy - 32), (cx + 32, cy - 32), (cx + 62, cy - 2)], 4.5)
    # cejas
    stroke(d, [(400, 404), (440, 392), (486, 398)], 7, STRIPE)
    stroke(d, [(594, 390), (640, 376), (690, 386)], 9, STRIPE)
    # gafas de pasta anchas (y 391-557 medido)
    for sx in (-1, 1):
        cx = 540 + sx * 134
        d.rounded_rectangle([P(cx - 124, 420), P(cx + 124, 548)], radius=34 * S, outline=INK, width=int(13 * S))
        d.rounded_rectangle([P(cx - 119, 425), P(cx + 119, 543)], radius=30 * S, outline=(88, 56, 40), width=int(8 * S))
    stroke(d, [(520, 452), (540, 444), (560, 452)], 10)
    stroke(d, [(296, 440), (250, 436)], 8); stroke(d, [(784, 440), (830, 436)], 8)
    # hocico: nariz, almohadillas de bigotes en W ancha y barbilla
    shape(d, [(518, 566), (540, 560), (562, 566), (556, 584), (540, 596), (524, 584)], NOSE)
    stroke(d, [(540, 596), (540, 616)])
    for sx in (-1, 1):
        stroke(d, [(540, 616), (540 + sx * 46, 640), (540 + sx * 110, 632), (540 + sx * 164, 600)], 3.5)
    stroke(d, [(468, 650), (540, 690), (612, 650)], 3.5)
    for sx in (-1, 1):
        for k in range(3):
            cx, cy = 540 + sx * (58 + k * 22), 612 + k * 6
            d.ellipse([P(cx - 3, cy - 3), P(cx + 3, cy + 3)], fill=(110, 108, 112))
        for dy in (0, 16):
            stroke(d, [(540 + sx * 110, 616 + dy), (540 + sx * 210, 606 + dy * 1.4), (540 + sx * 290, 600 + dy * 2)], 2.2)

def body(d):
    """hombros anchos y cuello de camisa; la barbilla se apoya en el cuello"""
    shape(d, [(110, 1090), (130, 900), (230, 800), (400, 736), (540, 730), (680, 736), (850, 800), (950, 900), (970, 1090)], (236, 232, 216))
    shape(d, [(430, 730), (540, 790), (500, 860), (404, 790)], (250, 248, 240))           # cuello de camisa
    shape(d, [(650, 730), (540, 790), (580, 860), (676, 790)], (250, 248, 240))
    shape(d, [(540, 798), (478, 772), (484, 832)], (148, 40, 52), smooth=False)          # pajarita
    shape(d, [(540, 798), (602, 776), (596, 836)], (148, 40, 52), smooth=False)
    shape(d, [(528, 786), (552, 786), (554, 810), (526, 810)], (118, 30, 42), smooth=False)
    stroke(d, [(540, 820), (544, 1090)], 2.5)

def avatar(size=1080):
    big = Image.new("RGBA", (1080 * S, 1080 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    d.ellipse([P(0, 0), P(1080, 1080)], fill=NAVY1); d.ellipse([P(60, 60), P(1020, 1020)], fill=NAVY2)
    layer = Image.new("RGBA", big.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    body(ld); head(ld)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse([P(10, 10), P(1070, 1070)], fill=255)
    layer.putalpha(Image.fromarray(np.minimum(np.asarray(layer.split()[3]), np.asarray(mask)))); big.alpha_composite(layer)
    d = ImageDraw.Draw(big)
    d.ellipse([P(14, 14), P(1066, 1066)], outline=B.GOLD, width=int(26 * S)); d.ellipse([P(2, 2), P(1078, 1078)], outline=INK, width=int(5 * S))
    return big.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    a = avatar(); a.save(os.path.join(OUT, "mascota_v6.png"))
    ref = "/mnt/user-data/attachments/e86e0da7-ee3f-52d5-a34d-06f11fdddf37/5c2e8c26-image.png"
    if os.path.exists(ref):
        r = Image.open(ref).convert("RGB").resize((540, 540))
        sh = Image.new("RGB", (1120, 560), (233, 226, 190)); sh.paste(r, (10, 10)); c = a.resize((540, 540)); sh.paste(c, (570, 10), c)
        sh.save(os.path.join(OUT, "mascota_v6_vs_referencia.png"))
    print("ok")
