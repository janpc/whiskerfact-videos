"""Gato v4: cuerpos con rebeca (hoja mixta 4x4 de Gemini) alineados con la cabeza v3 por la PAJARITA.
  python3 v4/parts_body.py -> v4/body_<pose>.png (lienzo CANVAS, con la cabeza en HEAD_AT) y v4/body_contact.jpg
La cabeza se pone encima con un corte suave por el cuello (CUT_Y en el lienzo de la base); el cuerpo aporta cuello, camisa, pajarita y rebeca.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, V3)
import parts as P

CANVAS = (1400, 1900); HEAD_AT = (188, 0)
POSES = {0: "stand", 1: "arms_crossed", 2: "point_right", 3: "paw_up", 5: "shrug", 6: "explain", 7: "stand_back",
         12: "hands_on_hips", 13: "stand_front", 14: "book", 15: "wave"}

def bow_box(im, region):
    a = np.asarray(im.convert("RGB")).astype(int); R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = (R > 70) & (R < 150) & (G < 75) & (B < 90) & (R > G + 30)
    x0, y0, x1, y1 = region; mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    lab, n = ndimage.label(ndimage.binary_closing(mm, iterations=2))
    best, bs = None, 0
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        s = len(xs) - 2 * abs(xs.mean() - (x0 + x1) / 2)
        if len(xs) > 60 and s > bs: best, bs = (xs.min(), ys.min(), xs.max(), ys.max()), s
    return best

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA")
    hb = bow_box(base, (300, 800, 724, 1024)); hcx, hcy, hw = (hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2, hb[2] - hb[0]
    print("pajarita cabeza", hb)
    S = Image.open(os.path.join(D, "sheet_cuerpo_mixta.jpg")).convert("RGB"); cw = S.width / 4
    thumbs = []
    for i, name in POSES.items():
        r, c = divmod(i, 4)
        cell = S.crop((round(c * cw) + 2, round(r * cw) + 2, round((c + 1) * cw) - 2, round((r + 1) * cw) - 2))
        bb = bow_box(cell, (30, 20, cell.width - 30, int(cell.height * 0.5))) or bow_box(cell, (30, 20, cell.width - 30, int(cell.height * 0.75)))
        cell = P.key(cell)
        sc = hw / (bb[2] - bb[0])
        # la pajarita del cuerpo cae donde estaba la de la cabeza
        p = P.place(cell, sc, ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2), (hcx + HEAD_AT[0], hcy + HEAD_AT[1]), CANVAS)
        p.save(os.path.join(D, f"body_{name}.png")); print(name, "escala", round(sc, 2), "pajarita", bb)
        t = Image.new("RGBA", CANVAS, (255, 255, 255, 255)); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").resize((350, 475)))
    sh = Image.new("RGB", (350 * 6, 475 * 2), "white")
    for k, t in enumerate(thumbs): sh.paste(t, ((k % 6) * 350, (k // 6) * 475))
    sh.save(os.path.join(D, "body_contact.jpg"), quality=88)

if __name__ == "__main__":
    main()
