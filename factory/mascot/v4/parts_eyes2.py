"""Gato v4: segunda hoja de ojos y cejas (Gemini no respetó el 2x2: una cara grande + 11 pequeñas). Se recorta por cajas y se alinea como parts_eyes.py.
  python3 v4/parts_eyes2.py -> v4/eyes2_<nn>.png y v4/eyes2_contact.jpg
"""
import os, sys
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, V3)
import parts as P
from parts_eyes import BROW

# (x0, y0, x1, y1) de cada cara en la hoja de 1024: 0 = grande (arriba a la derecha), el resto en celdas de 256
BOXES = [(512, 0, 1024, 512)] + [(c * 256, r * 256, c * 256 + 256, r * 256 + 256) for r, c in
         [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]]

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA"); size = base.size
    nb = P.nose_box(base, (300, 450, 724, 700))
    gb = P.glasses_box(base, nb[1]); gw, gcx, gcy = gb[2] - gb[0], (gb[0] + gb[2]) / 2, (gb[1] + gb[3]) / 2
    mask = P.soft(size, (gb[0] - 10, gb[1] - gw * BROW, gb[2] + 10, gb[3] + 12), 12)
    E = Image.open(os.path.join(D, "sheet_ojos2.png")).convert("RGB")
    thumbs = []
    for i, (x0, y0, x1, y1) in enumerate(BOXES):
        cell = P.key(E.crop((x0 + 3, y0 + 3, x1 - 3, y1 - 3)))
        try:
            n2 = P.nose_box(cell, (int(cell.width * 0.2), int(cell.height * 0.3), int(cell.width * 0.8), int(cell.height * 0.75)))
            g2 = P.glasses_box(cell, n2[1])
        except Exception as e:
            print(i, "ERROR", e); continue
        sc = gw / (g2[2] - g2[0])
        p = P.place(cell, sc, ((g2[0] + g2[2]) / 2, (g2[1] + g2[3]) / 2), (gcx, gcy), size)
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(mask))))
        p.save(os.path.join(D, f"eyes2_{i:02d}.png")); print(i, "escala", round(sc, 2))
        t = Image.new("RGBA", size, (255, 255, 255, 255)); t.alpha_composite(base); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").crop((120, 250, 920, 700)).resize((400, 225)))
    cols = 4; rows = (len(thumbs) + cols - 1) // cols
    sh = Image.new("RGB", (400 * cols, 225 * rows), "white")
    for k, t in enumerate(thumbs): sh.paste(t, ((k % cols) * 400, (k // cols) * 225))
    sh.save(os.path.join(D, "eyes2_contact.jpg"), quality=90)

if __name__ == "__main__":
    main()
