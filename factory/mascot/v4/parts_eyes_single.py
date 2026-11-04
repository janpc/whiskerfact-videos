"""Gato v4: ojos/cejas generados UNO A UNO (Gemini editando la cabeza base, 1024 px). Alinea por las gafas como parts_eyes.py.
  python3 v4/parts_eyes_single.py -> v4/singles/eyes_<nombre>.png y singles/contact.jpg   (entrada: singles/src_<nombre>.png)
"""
import os, sys, glob
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3"); S = os.path.join(D, "singles")
sys.path.insert(0, V3)
import parts as P
from parts_eyes import BROW

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA"); size = base.size
    nb = P.nose_box(base, (300, 450, 724, 700)); gb = P.glasses_box(base, nb[1])
    gw, gcx, gcy = gb[2] - gb[0], (gb[0] + gb[2]) / 2, (gb[1] + gb[3]) / 2
    mask = P.soft(size, (gb[0] - 10, gb[1] - gw * BROW, gb[2] + 10, gb[3] + 12), 12)
    thumbs = []
    for f in sorted(glob.glob(os.path.join(S, "src_*.png"))):
        name = os.path.basename(f)[4:-4]
        cell = P.key(Image.open(f).convert("RGB"))
        n2 = P.nose_box(cell, (int(cell.width * 0.2), int(cell.height * 0.3), int(cell.width * 0.8), int(cell.height * 0.75)))
        g2 = P.glasses_box(cell, n2[1]); sc = gw / (g2[2] - g2[0])
        p = P.place(cell, sc, ((g2[0] + g2[2]) / 2, (g2[1] + g2[3]) / 2), (gcx, gcy), size)
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(mask))))
        p.save(os.path.join(S, f"eyes_{name}.png")); print(name, "escala", round(sc, 3))
        t = Image.new("RGBA", size, (255, 255, 255, 255)); t.alpha_composite(base); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").crop((120, 250, 920, 700)).resize((400, 225)))
    sh = Image.new("RGB", (800, 225 * ((len(thumbs) + 1) // 2)), "white")
    for k, t in enumerate(thumbs): sh.paste(t, ((k % 2) * 400, (k // 2) * 225))
    sh.save(os.path.join(S, "contact.jpg"), quality=90)
if __name__ == "__main__": main()
