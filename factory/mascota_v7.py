"""Mr. Whiskerfact v7: dibujado desde cero con el diseño elegido (propuesta 1, generada por nosotros a partir de texto)
y en el estilo de la autora: línea negra fina y uniforme, colores planos, una sola sombra plana, rasgos con pocos trazos.
La silueta de cabeza y orejas y la posición de ojos, gafas y nariz se toman de la propuesta 1 (out/concepts/c1_landmarks.json).
  python3 mascota_v7.py -> out/mascota_v7.png
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw
import brand as B

HERE = os.path.dirname(os.path.abspath(__file__))
S = 3
INK = (26, 20, 22); LW = 3.2
FUR, FUR_SH, FUR_LIGHT, STRIPE = (156, 156, 160), (132, 132, 138), (226, 224, 218), (112, 112, 120)
EAR_IN, NOSE = (226, 178, 176), (220, 150, 150)
AMBER, AMBER_D = (230, 160, 52), (184, 112, 30)
GLASS = (78, 48, 40)
SHIRT, SHIRT_SH, TIE, TIE_D = (242, 236, 214), (218, 210, 184), (128, 40, 56), (100, 28, 42)
NAVY1, NAVY2 = (24, 30, 64), (40, 48, 96)

L = json.load(open(os.path.join(HERE, "out", "concepts", "c1_landmarks.json")))
SC, OX, OY = 1.10, 540 - 300 * 1.10, 112 - 26 * 1.10          # de la propuesta (600x728) al avatar (1080)
def M(x, y): return (OX + x * SC, OY + y * SC)
def P(x, y): return (x * S, y * S)

def spline(pts, n=8, closed=True):
    out = []; Ln = len(pts); rng = range(Ln) if closed else range(Ln - 1)
    for i in rng:
        p0 = pts[i - 1] if (closed or i > 0) else pts[0]; p1, p2 = pts[i], pts[(i + 1) % Ln]
        p3 = pts[(i + 2) % Ln] if (closed or i + 2 < Ln) else pts[-1]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    if not closed: out.append(pts[-1])
    return out

def fill(d, pts, col, line=True, w=LW, smooth=True):
    q = spline(pts) if smooth else pts
    d.polygon([P(*p) for p in q], fill=col)
    if line: d.line([P(*p) for p in q] + [P(*q[0])], fill=INK, width=int(w * S), joint="curve")

def line(d, pts, w=LW, col=INK, smooth=True):
    q = spline(pts, closed=False) if smooth else pts
    d.line([P(*p) for p in q], fill=col, width=int(w * S), joint="curve")

# mitad derecha de la cabeza (coordenadas del avatar), con las proporciones de la propuesta 1:
# cráneo redondeado, orejas grandes y erguidas, mofletes que se ensanchan con dos puntas de pelo suaves, barbilla redonda
HEAD_R = [(540, 212), (620, 220), (676, 240),                       # frente redondeada
          (706, 198), (734, 150), (756, 114), (770, 110), (780, 124), # borde interior de la oreja y punta
          (786, 190), (778, 262), (776, 330),                          # sien: más estrecha que los mofletes
          (800, 398), (828, 456), (846, 500), (818, 506), (830, 538), (794, 554),  # mofletes que se abren, dos puntas
          (736, 588), (640, 614), (540, 622)]                          # mandíbula y barbilla
EAR_R = [(700, 244), (740, 166), (762, 138), (774, 206), (772, 276), (728, 276)]

def head_outline():
    left = [(1080 - x, y) for x, y in reversed(HEAD_R[1:-1])]
    return HEAD_R + left

def body(d):
    fill(d, [(150, 1090), (170, 780), (250, 690), (400, 640), (540, 634), (680, 640), (830, 690), (910, 780), (930, 1090)], SHIRT)
    d.polygon([P(*p) for p in spline([(170, 780), (250, 690), (290, 750), (262, 1090), (150, 1090)])], fill=SHIRT_SH)
    line(d, [(282, 780), (300, 860)], 2.4); line(d, [(798, 780), (780, 860)], 2.4)            # pliegues
    # sombra plana bajo la barbilla y cuello de camisa en pico
    d.polygon([P(*p) for p in spline([(440, 630), (540, 650), (640, 630), (600, 680), (540, 696), (480, 680)])], fill=FUR_SH)
    fill(d, [(430, 622), (540, 676), (500, 742), (396, 662)], SHIRT, smooth=False)
    fill(d, [(650, 622), (540, 676), (580, 742), (684, 662)], SHIRT, smooth=False)
    # pajarita
    fill(d, [(540, 702), (474, 672), (470, 712), (480, 750)], TIE)
    fill(d, [(540, 702), (606, 672), (610, 712), (600, 750)], TIE)
    fill(d, [(524, 688), (556, 688), (560, 720), (520, 720)], TIE_D)
    line(d, [(540, 734), (544, 1090)], 2.4)
    for y in (946, 880): d.ellipse([P(531, y - 7), P(549, y + 7)], fill=SHIRT, outline=INK, width=int(2.2 * S))

def head(d, wink=False):
    out = head_outline()
    q = spline(out, n=8)
    d.polygon([P(*p) for p in q], fill=FUR)
    # una sola sombra plana en el lado derecho (como en sus personajes)
    sh = [(x, y) for x, y in q]
    m1 = Image.new("L", d._image.size, 0); ImageDraw.Draw(m1).polygon([P(*p) for p in q], fill=255)
    m2 = Image.new("L", d._image.size, 0); ImageDraw.Draw(m2).polygon([P(x - 26, y + 6) for x, y in q], fill=255)
    d._image.paste(FUR_SH, (0, 0), Image.fromarray(np.minimum(np.asarray(m1), 255 - np.asarray(m2))))
    # interior de las orejas: rosa plano, sin pelo
    for sx in (-1, 1):
        ear = [(540 + sx * (x - 540), y) for x, y in EAR_R]
        d.polygon([P(*p) for p in spline(ear)], fill=EAR_IN)
        line(d, [ear[0], ear[1], ear[2]], 2.4)
    # rayas del atigrado: planas, sin contorno
    for x0, w, top, ln in ((500, 16, 232, 58), (540, 20, 226, 74), (580, 16, 232, 58)):
        d.polygon([P(*p) for p in spline([(x0 - w / 2, top), (x0 + w / 2, top), (x0 + w / 5, top + ln), (x0, top + ln + 8), (x0 - w / 5, top + ln)])], fill=STRIPE)
    for sx in (-1, 1):
        for k, (y, ln) in enumerate(((440, 54), (476, 46))):
            x0 = 540 + sx * 258
            d.polygon([P(*p) for p in spline([(x0, y - 8), (x0 - sx * ln, y), (x0, y + 10)])], fill=STRIPE)
    # contorno de la cabeza encima
    d.line([P(*p) for p in q] + [P(*q[0])], fill=INK, width=int(LW * S), joint="curve")
    # hocico claro plano
    nx, ny = M(*L["nose"])
    d.polygon([P(*p) for p in spline([(nx, ny - 26), (nx + 70, ny - 6), (nx + 92, ny + 44), (nx + 54, ny + 92), (nx, ny + 104),
                                        (nx - 54, ny + 92), (nx - 92, ny + 44), (nx - 70, ny - 6)])], fill=FUR_LIGHT)
    # ojos almendrados en las posiciones de la propuesta
    for (ex, ey), sx in zip(L["eyes"], (-1, 1)):
        cx, cy = M(ex, ey)
        if wink and sx == 1:
            line(d, [(cx - 48, cy + 4), (cx, cy - 14), (cx + 48, cy + 4)], 4.5); continue
        eye = [(cx - 52, cy + 2), (cx - 22, cy - 34), (cx + 26, cy - 34), (cx + 52, cy - 2), (cx + 24, cy + 34), (cx - 26, cy + 34)]
        fill(d, eye, (250, 248, 240))
        d.ellipse([P(cx - 34, cy - 34), P(cx + 34, cy + 34)], fill=AMBER)
        d.chord([P(cx - 34, cy - 34), P(cx + 34, cy + 34)], 200, 340, fill=AMBER_D)
        d.ellipse([P(cx - 15, cy - 20), P(cx + 15, cy + 22)], fill=INK)
        d.ellipse([P(cx + 2, cy - 22), P(cx + 18, cy - 6)], fill=(255, 255, 255))
        line(d, [(cx - 56, cy + 4), (cx - 22, cy - 38), (cx + 28, cy - 38), (cx + 56, cy - 2)], 4.2)
    # gafas de pasta marrón alrededor de cada ojo (tamaño de la propuesta)
    fr = []
    for ex, ey in L["eyes"]:
        cx, cy = M(ex, ey)
        x0, y0, x1, y1 = cx - 84 * SC, cy - 64 * SC, cx + 76 * SC, cy + 62 * SC
        if cx > 540: x0, x1 = cx - 76 * SC, cx + 84 * SC
        fr.append((x0, y0, x1, y1))
        d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=34 * S, outline=INK, width=int(13 * S))
        d.rounded_rectangle([P(x0 + 3, y0 + 3), P(x1 - 3, y1 - 3)], radius=31 * S, outline=GLASS, width=int(7 * S))
    yb = fr[0][1] + 40
    line(d, [(fr[0][2], yb), (540, yb - 8), (fr[1][0], yb)], 11); line(d, [(fr[0][2], yb), (540, yb - 7), (fr[1][0], yb)], 5, GLASS)
    line(d, [(fr[0][0], yb), (fr[0][0] - 26, yb - 4)], 9); line(d, [(fr[1][2], yb), (fr[1][2] + 26, yb - 4)], 9)
    # nariz, boca en W con sonrisa y bigotes finos
    fill(d, [(nx - 22, ny - 10), (nx + 22, ny - 10), (nx + 16, ny + 6), (nx, ny + 18), (nx - 16, ny + 6)], NOSE)
    line(d, [(nx, ny + 18), (nx, ny + 38)], 3)
    line(d, [(nx, ny + 38), (nx - 22, ny + 56), (nx - 50, ny + 54), (nx - 66, ny + 40)], 3)
    line(d, [(nx, ny + 38), (nx + 22, ny + 56), (nx + 50, ny + 54), (nx + 66, ny + 40)], 3)
    line(d, [(nx - 34, ny + 84), (nx, ny + 96), (nx + 34, ny + 84)], 2.6)
    for sx in (-1, 1):
        for k in range(3):
            px, py = nx + sx * (38 + k * 18), ny + 22 + k * 8
            d.ellipse([P(px - 3, py - 3), P(px + 3, py + 3)], fill=(120, 116, 118))
        for dy in (0, 16, 32):
            line(d, [(nx + sx * 96, ny + 34 + dy * 0.5), (nx + sx * 200, ny + 26 + dy), (nx + sx * 300, ny + 22 + dy * 1.6)], 2.2)

def avatar(size=1080, wink=False):
    big = Image.new("RGBA", (1080 * S, 1080 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    d.ellipse([P(0, 0), P(1080, 1080)], fill=NAVY1); d.ellipse([P(60, 60), P(1020, 1020)], fill=NAVY2)
    layer = Image.new("RGBA", big.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    body(ld); head(ld, wink)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse([P(10, 10), P(1070, 1070)], fill=255)
    layer.putalpha(Image.fromarray(np.minimum(np.asarray(layer.split()[3]), np.asarray(mask)))); big.alpha_composite(layer)
    d = ImageDraw.Draw(big)
    d.ellipse([P(14, 14), P(1066, 1066)], outline=B.GOLD, width=int(26 * S)); d.ellipse([P(2, 2), P(1078, 1078)], outline=INK, width=int(5 * S))
    return big.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    a = avatar(); a.save(os.path.join(HERE, "out", "mascota_v7.png")); print("ok")
