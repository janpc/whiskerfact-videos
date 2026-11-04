"""Gato v4: bocas con actitud (hoja 4x4 de Gemini) alineadas con la base v3 por la NARIZ (misma técnica que v3/parts.py).
  python3 v4/parts_mouths.py -> v4/mouth_<nn>.png (lienzo de base.png) y v4/mouths_contact.jpg
"""
import os, sys
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, V3)
import parts as P

K = float(os.environ.get('SR', 1))      # SR=2: usa la hoja reescalada por IA (_sr.png, el doble de píxeles)

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA"); size = base.size
    nb = P.nose_box(base, (300, 450, 724, 700)); ncx, nw = (nb[0] + nb[2]) / 2, nb[2] - nb[0]
    mask = P.soft(size, (ncx - nw * 1.55, nb[1] + 0.35 * (nb[3] - nb[1]), ncx + nw * 1.55, nb[3] + nw * 1.75), 10)
    M = Image.open(os.path.join(D, "sheet_bocas_4x4" + ("_sr" if K > 1 else "") + ".png")).convert("RGB"); cw = M.width / 4; m5 = round(5 * K)
    thumbs = []
    for i in range(16):
        r, c = divmod(i, 4)
        cell = M.crop((round(c * cw) + m5, round(r * cw) + m5, round((c + 1) * cw) - m5, round((r + 1) * cw) - m5))
        try:
            b = P.nose_box(cell, (round(40 * K), 0, cell.width - round(40 * K), cell.height // 2))
            sc = nw / (b[2] - b[0])
            p = P.place(cell.convert("RGBA"), sc, ((b[0] + b[2]) / 2, b[1]), (ncx, nb[1]), size)
        except Exception as e:
            print(i + 1, "ERROR", e); continue
        p.putalpha(Image.fromarray(np.minimum(np.asarray(p.split()[3]), np.asarray(mask))))
        p.save(os.path.join(D, f"mouth_{i + 1:02d}.png")); print(i + 1, "escala", round(sc, 2))
        t = Image.new("RGBA", size, (255, 255, 255, 255)); t.alpha_composite(base); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").crop((200, 480, 830, 900)).resize((315, 210)))
    sh = Image.new("RGB", (315 * 4, 210 * 4), "white")
    for k, t in enumerate(thumbs): sh.paste(t, ((k % 4) * 315, (k // 4) * 210))
    sh.save(os.path.join(D, "mouths_contact.jpg"), quality=90)

if __name__ == "__main__":
    main()
