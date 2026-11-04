"""Gato v4: recorta la hoja de ojos y cejas (4x4, 16 expresiones) y la alinea con la base v3 (misma técnica que v3/parts.py).
  python3 v4/parts_eyes.py -> v4/eyes_<nn>.png (lienzo de base.png) y v4/eyes_contact.jpg (las 16 sobre la base, para revisar)
"""
import os, sys
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, V3)
import parts as P

BROW = 0.30      # margen sobre las gafas (fracción del ancho de gafas): aquí hay cejas, en v3 eran 0.16

K = float(os.environ.get('SR', 1))

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA"); size = base.size
    nb = P.nose_box(base, (300, 450, 724, 700))
    gb = P.glasses_box(base, nb[1]); gw, gcx, gcy = gb[2] - gb[0], (gb[0] + gb[2]) / 2, (gb[1] + gb[3]) / 2
    mask = P.soft(size, (gb[0] - 10, gb[1] - gw * BROW, gb[2] + 10, gb[3] + 12), 12)
    E = Image.open(os.path.join(D, "sheet_ojos_4x4" + ("_sr" if K > 1 else "") + ".png")).convert("RGB"); cw = E.width / 4; m3 = round(3 * K)
    thumbs = []
    for i in range(16):
        r, c = divmod(i, 4)
        cell = P.key(E.crop((round(c * cw) + m3, round(r * cw) + m3, round((c + 1) * cw) - m3, round((r + 1) * cw) - m3)))
        n2 = P.nose_box(cell, (round(60 * K), round(90 * K), cell.width - round(60 * K), cell.height - round(40 * K)))
        g2 = P.glasses_box(cell, n2[1])
        sc = gw / (g2[2] - g2[0])
        p = P.place(cell, sc, ((g2[0] + g2[2]) / 2, (g2[1] + g2[3]) / 2), (gcx, gcy), size)
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(mask))))
        p.save(os.path.join(D, f"eyes_{i + 1:02d}.png"))
        t = Image.new("RGBA", size, (255, 255, 255, 255)); t.alpha_composite(base); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").crop((100, 330, 930, 640)).resize((415, 155)))
        print(i + 1, "escala", round(sc, 2))
    sh = Image.new("RGB", (415 * 4, 155 * 4), "white")
    for i, t in enumerate(thumbs): sh.paste(t, ((i % 4) * 415, (i // 4) * 155))
    sh.save(os.path.join(D, "eyes_contact.jpg"), quality=90)

if __name__ == "__main__":
    main()
