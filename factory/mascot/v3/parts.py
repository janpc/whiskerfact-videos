"""Mr. Whiskerfact por piezas (hojas v3 de Gemini): cara base sin boca + bocas + ojos, todo alineado con la base.
  python3 parts.py -> base.png, mouth_<n>.png, eyes_<n>.png (mismo lienzo que base.png, transparentes fuera de la pieza)
Alineación: bocas por la NARIZ (tamaño y centro), ojos por las GAFAS (ancho) y la nariz (posición).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

D = os.path.dirname(os.path.abspath(__file__))
UP = 2                                   # la base sale a 1024 px (celda de 512 x2)

def key(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    g = G - np.maximum(R, Bc)
    alpha = np.clip(1 - (g - 25) / 70, 0, 1)
    a[..., 1] = np.minimum(G, np.maximum(R, Bc) + 12)
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")
    out.putalpha(out.split()[3].filter(ImageFilter.MinFilter(3)))
    return out

def nose_box(im, region=None):
    """caja del rosa de la nariz (el mayor bloque rosa fuera de las orejas)"""
    a = np.asarray(im.convert("RGB")).astype(int)
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    m = (R > 160) & (R - G > 35) & (Bc - G > -5) & (R < 240) & (G < 175)
    if region: x0, y0, x1, y1 = region; mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    lab, n = ndimage.label(m)
    if n == 0: raise ValueError("sin nariz")
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    # la nariz: bloque grande más cercano al centro horizontal
    best, bs = None, -1
    for i, s in enumerate(sizes, 1):
        ys, xs = np.nonzero(lab == i)
        score = s - 3 * abs(xs.mean() - a.shape[1] / 2)
        if s > 30 and score > bs: best, bs = (xs.min(), ys.min(), xs.max(), ys.max()), score
    return best

def glasses_box(im, y_max):
    a = np.asarray(im.convert("RGB")).astype(int)
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    m = (R < 125) & (G < 90) & (Bc < 90) & (R > G + 8)
    m[y_max:] = False
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    big = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.25 * sizes.max()])
    ys, xs = np.nonzero(big)
    return xs.min(), ys.min(), xs.max(), ys.max()

def place(piece, scale, src_pt, dst_pt, size):
    """escala la pieza y la coloca de modo que src_pt (en la pieza) caiga en dst_pt (en el lienzo)"""
    p = piece.resize((round(piece.width * scale), round(piece.height * scale)), Image.LANCZOS)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.alpha_composite(p, (round(dst_pt[0] - src_pt[0] * scale), round(dst_pt[1] - src_pt[1] * scale)))   # noqa
    return out

def soft(size, box, blur):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).ellipse(box, fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))

def main():
    S = Image.open(os.path.join(D, "sheet_base.png")).convert("RGB")
    base = key(S.crop((512, 0, 1024, 512))).resize((1024, 1024), Image.LANCZOS)
    base.save(os.path.join(D, "base.png"))
    nb = nose_box(base, (300, 450, 724, 700)); ncx, nw = (nb[0] + nb[2]) / 2, nb[2] - nb[0]
    gb = glasses_box(base, nb[1]); gw, gcx, gcy = gb[2] - gb[0], (gb[0] + gb[2]) / 2, (gb[1] + gb[3]) / 2
    print("base nariz", nb, "gafas", gb)
    size = base.size
    # --- bocas: 4 x 3, celdas de 256 x 255 ---
    M = Image.open(os.path.join(D, "sheet_mouths.png")).convert("RGB")
    cw, ch = M.width / 4, M.height / 3
    mouth_mask = soft(size, (ncx - nw * 1.55, nb[1] + 0.35 * (nb[3] - nb[1]), ncx + nw * 1.55, nb[3] + nw * 1.75), 10)
    for i in range(12):
        r, c = divmod(i, 4)
        cell = M.crop((round(c * cw) + 4, round(r * ch) + 4, round((c + 1) * cw) - 4, round((r + 1) * ch) - 4))
        b = nose_box(cell, (40, 0, cell.width - 40, cell.height // 2))
        sc = nw / (b[2] - b[0])
        p = place(cell.convert("RGBA"), sc, ((b[0] + b[2]) / 2, b[1]), (ncx, nb[1]), size)
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(mouth_mask))))
        p.save(os.path.join(D, f"mouth_{i + 1:02d}.png"))
    # --- ojos: 3 x 3 ---
    E = Image.open(os.path.join(D, "sheet_eyes.png")).convert("RGB")
    cw = E.width / 3
    eye_mask = soft(size, (gb[0] - 10, gb[1] - gw * 0.16, gb[2] + 10, gb[3] + 12), 12)
    for i in range(9):
        r, c = divmod(i, 3)
        cell = key(E.crop((round(c * cw) + 3, round(r * cw) + 3, round((c + 1) * cw) - 3, round((r + 1) * cw) - 3)))
        n2 = nose_box(cell, (60, 120, cell.width - 60, cell.height - 40))
        g2 = glasses_box(cell, n2[1])
        sc = gw / (g2[2] - g2[0])
        p = place(cell, sc, ((g2[0] + g2[2]) / 2, (g2[1] + g2[3]) / 2), (gcx, gcy), size)
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(eye_mask))))
        p.save(os.path.join(D, f"eyes_{i + 1:02d}.png"))
        print("ojos", i + 1, "escala", round(sc, 2))

if __name__ == "__main__":
    main()
