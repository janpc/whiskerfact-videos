"""Cuerpos en alta resolución: hojas 2x2 de Gemini (celdas de 512 px o más) alineadas con la cabeza v3 por la PAJARITA.
  python3 v4/parts_body_hd.py   -> v4/body_<pose>.png (sustituye a los de la hoja 4x4) y v4/body_hd_contact.jpg
Para añadir una hoja: una entrada en SHEETS (archivo, filas/columnas, {índice de celda: nombre de pose}).
Quita las rayas divisorias y los números que Gemini dibuja (recorte con margen + componentes pequeños fuera)."""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, V3); sys.path.insert(0, D)
import parts as P
from parts_body import bow_box, CANVAS, HEAD_AT

SHEETS = [("sheet_cuerpo_A_2x2.png", 2, {0: "stand_front", 1: "arms_crossed", 2: "book", 3: "wave"})]
INSET = 0.02      # fracción de la celda que se recorta por cada lado (rayas divisorias)

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA")
    hb = bow_box(base, (300, 800, 724, 1024)); hcx, hcy, hw = (hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2, hb[2] - hb[0]
    thumbs = []
    for fn, n, poses in SHEETS:
        S = Image.open(os.path.join(D, fn)).convert("RGB"); cw = S.width / n; ch = S.height / n; m = round(cw * INSET)
        for i, name in poses.items():
            r, c = divmod(i, n)
            cell = S.crop((round(c * cw) + m, round(r * ch) + m, round((c + 1) * cw) - m, round((r + 1) * ch) - m))
            bb = bow_box(cell, (cell.width // 8, 0, cell.width * 7 // 8, int(cell.height * 0.55)))
            cell = P.key(cell)
            al = np.asarray(cell.split()[3]) > 40
            lab, k = ndimage.label(al)
            if k >= 1:
                sizes = ndimage.sum(al, lab, range(1, k + 1)); keep = [j + 1 for j, z in enumerate(sizes) if z >= 0.04 * sizes.max()]
                ok = ndimage.binary_dilation(np.isin(lab, keep), iterations=4)
                arr = np.asarray(cell).copy(); arr[..., 3] = np.where(ok, arr[..., 3], 0); cell = Image.fromarray(arr, "RGBA")
            sc = hw / (bb[2] - bb[0])
            p = P.place(cell, sc, ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2), (hcx + HEAD_AT[0], hcy + HEAD_AT[1]), CANVAS)
            p.save(os.path.join(D, f"body_{name}.png")); print(name, "escala", round(sc, 2), "pajarita", bb, "base del cuerpo", p.split()[3].getbbox())
            t = Image.new("RGBA", CANVAS, (255, 255, 255, 255)); t.alpha_composite(p)
            thumbs.append(t.convert("RGB").resize((350, 475)))
    sh = Image.new("RGB", (350 * len(thumbs), 475), "white")
    for k, t in enumerate(thumbs): sh.paste(t, (k * 350, 0))
    sh.save(os.path.join(D, "body_hd_contact.jpg"), quality=88)

if __name__ == "__main__":
    main()
