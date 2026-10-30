"""Recorta las hojas de expresiones de Mr. Whiskerfact (Gemini, 4x4 sobre verde) en sprites con transparencia.
  python3 sprites.py            -> mascot/v2/<nombre>.png (fondo transparente, alineados con 'neutral')
Pasos: cortar celda -> quitar el verde (alfa suave + quitar el reflejo verde del borde) -> alinear con la celda neutral
(correlación de fase sobre la zona de orejas y gafas, que no cambia entre expresiones) -> escalar x3.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from skimage.registration import phase_cross_correlation

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "mascot", "v2")
CELL, UP = 256, 3

# celda elegida para cada pose: (hoja, número 1-16)
PICK = {
    "neutral": ("A", 1), "eh": ("A", 2), "ah": ("A", 3), "o": ("A", 4), "ee": ("A", 5), "m": ("A", 6),
    "half": ("A", 7), "closed": ("A", 8),
    "wink": ("B", 1), "surprised": ("B", 2), "happy": ("B", 3), "brow": ("B", 4),
    "point": ("B", 5), "glasses": ("B", 6), "look_r": ("B", 7), "look_l": ("B", 8), "sly": ("B", 14),
}

def cell(sheet, n):
    r, c = divmod(n - 1, 4)
    return sheet.crop((c * CELL, r * CELL, (c + 1) * CELL, (r + 1) * CELL))

def key(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    g = G - np.maximum(R, Bc)                         # cuánto domina el verde
    alpha = np.clip(1 - (g - 25) / 70, 0, 1)          # <25 opaco, >95 transparente, suave entre medias
    a[..., 1] = np.minimum(G, np.maximum(R, Bc) + 12) # quita el reflejo verde del contorno
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")
    out.putalpha(out.split()[3].filter(ImageFilter.MinFilter(3)))   # recorta 1 px de borde: sin halo verde
    return out

def ref_zone(im):
    """zona de orejas y gafas (filas 0-150): igual en todas las expresiones salvo las que mueven la cabeza"""
    return np.asarray(im.convert("L")).astype(np.float32)[0:150, 30:226]

def main():
    sheets = {k: Image.open(os.path.join(DIR, f"sheet{k}.png")).convert("RGB") for k in "AB"}
    base = ref_zone(cell(sheets["A"], 1))
    for name, (s, n) in PICK.items():
        c = cell(sheets[s], n)
        shift, err, _ = phase_cross_correlation(base, ref_zone(c), upsample_factor=4)
        dy, dx = shift
        k = key(c)
        k = k.transform(k.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), resample=Image.BICUBIC)
        k = k.resize((CELL * UP, CELL * UP), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
        k.save(os.path.join(DIR, f"{name}.png"))
        print(f"{name:10s} {s}{n:<3d} desplazamiento x={dx:+.1f} y={dy:+.1f}")

if __name__ == "__main__":
    main()
