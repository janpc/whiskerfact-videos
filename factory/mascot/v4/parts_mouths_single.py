"""Gato v4: bocas generadas UNA A UNA (Gemini devuelve la cara entera; se recorta solo la zona de la boca, alineada por la NARIZ).
  python3 v4/parts_mouths_single.py -> singles/mouth_<nombre>.png y singles/mouths_contact.jpg   (entrada: singles/mouth_src_<nombre>.png)
"""
import os, sys, glob
import scipy.ndimage as ndi
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3"); S = os.path.join(D, "singles")
sys.path.insert(0, V3)
import parts as P

CUSTOM = {"round": (470, 655, 590, 732)}      # Gemini añadió una sonrisa extra bajo el círculo: solo se recorta el círculo

def main():
    base = Image.open(os.path.join(V3, "base.png")).convert("RGBA"); size = base.size
    nb = P.nose_box(base, (300, 450, 724, 700)); ncx, nw = (nb[0] + nb[2]) / 2, nb[2] - nb[0]
    mask = P.soft(size, (ncx - nw * 2.0, nb[1] + 0.35 * (nb[3] - nb[1]), ncx + nw * 2.0, nb[3] + nw * 2.2), 10)
    thumbs = []
    for f in sorted(glob.glob(os.path.join(S, "mouth_src_*.png"))):
        name = os.path.basename(f)[10:-4]
        cell = Image.open(f).convert("RGB")
        b = P.nose_box(cell, (300, 450, 724, 700)); sc = nw / (b[2] - b[0])
        p = P.place(cell.convert("RGBA"), sc, ((b[0] + b[2]) / 2, b[1]), (ncx, nb[1]), size)
        arr = np.asarray(p).copy(); arr[..., 1] = np.minimum(arr[..., 1], np.maximum(arr[..., 0], arr[..., 2])); p = Image.fromarray(arr)      # quita el halo verde del croma
        # SOLO la boca: trazo oscuro + lo que encierra (lengua, dientes, interior), conectado a la línea de la nariz.
        # Así el hocico, las mejillas y los bigotes no cambian de una boca a otra (la base se ve igual siempre).
        mk = np.asarray(mask if name not in CUSTOM else P.soft(size, CUSTOM[name], 6)).astype(np.float32) / 255
        lum = np.asarray(p.convert("L")).astype(np.float32)
        dark = (lum < 125) & (mk > 0.5)
        filled = ndi.binary_fill_holes(ndi.binary_closing(dark, iterations=2))
        lab, nl = ndi.label(filled)
        cx, y0 = int(round(ncx)), int(nb[3])
        near = set(np.unique(lab[y0 - 6:y0 + 60, cx - 12:cx + 12])) - {0}
        keep = np.isin(lab, list(near)) if near else filled
        # quita los bigotes que se pegan a las comisuras (trazos finos lejos del centro)
        keep = ndi.binary_opening(keep, iterations=1) | (keep & (np.abs(np.arange(size[0])[None, :] - cx) < nw * 0.9))
        a = ndi.gaussian_filter(ndi.binary_dilation(keep, iterations=2).astype(np.float32), 1.2)
        p.putalpha(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)))
        p.save(os.path.join(S, f"mouth_{name}.png")); print(name, "escala", round(sc, 3))
        t = Image.new("RGBA", size, (255, 255, 255, 255)); t.alpha_composite(base); t.alpha_composite(p)
        thumbs.append(t.convert("RGB").crop((200, 480, 830, 900)))
    sh = Image.new("RGB", (630 * min(2, len(thumbs)), 420 * ((len(thumbs) + 1) // 2)), "white")
    for k, t in enumerate(thumbs): sh.paste(t, ((k % 2) * 630, (k // 2) * 420))
    sh.save(os.path.join(S, "mouths_contact.jpg"), quality=90)
if __name__ == "__main__": main()
