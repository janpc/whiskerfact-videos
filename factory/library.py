"""Biblioteca de personajes (personas y animales) en el estilo del gato, para no dibujarlos con formas en código.
Cada personaje es una hoja de 2x2 poses sobre verde (Gemini gratis a mano, o ElevenLabs puntualmente) recortada aquí.

  python3 library.py add <hoja.png> <nombre> <pose1,pose2,pose3,pose4> [--tags a,b] [--source gemini|elevenlabs] [--grid 2x2]
  python3 library.py list
En una escena:
  import library as LIB
  spr = LIB.get("dog", "side")            # RGBA recortado al contenido, None si no existe
  LIB.find("animal")                       # nombres con esa etiqueta
  LIB.place(img, "dog", "side", cx, base_y, height, flip=False, a=1.0, rot=0)   # lo pega con los pies en base_y
Las poses son imágenes completas: para animar se cambia de pose (con un parpadeo de 2 fotogramas como mucho),
y se mueve el sprite entero (andar = desplazar + leve bote; respirar = escala 1-2 %).
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "library")
INDEX = os.path.join(DIR, "index.json")

def _index():
    return json.load(open(INDEX)) if os.path.exists(INDEX) else {}

def key(im):
    """quita el verde: alfa suave y sin halo"""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    g = G - np.maximum(R, Bc)
    alpha = np.clip(1 - (g - 25) / 70, 0, 1)
    a[..., 1] = np.minimum(G, np.maximum(R, Bc) + 12)
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")
    out.putalpha(out.split()[3].filter(ImageFilter.MinFilter(3)))
    return out

def add(sheet, name, poses, tags=(), source="gemini", grid=(2, 2)):
    im = Image.open(sheet).convert("RGB")
    cols, rows = grid
    cw, ch = im.width / cols, im.height / rows
    os.makedirs(os.path.join(DIR, name), exist_ok=True)
    im.save(os.path.join(DIR, name, "sheet.png"))
    saved = {}
    for i, pose in enumerate(poses):
        r, c = divmod(i, cols)
        cell = key(im.crop((round(c * cw) + 4, round(r * ch) + 4, round((c + 1) * cw) - 4, round((r + 1) * ch) - 4)))
        # quitar trozos sueltos (restos de la celda vecina): solo el componente grande
        from scipy import ndimage
        m = np.asarray(cell.split()[3]) > 40
        lab, n = ndimage.label(m)
        if n > 1:
            sizes = ndimage.sum(m, lab, range(1, n + 1))
            keep = np.isin(lab, [j + 1 for j, s in enumerate(sizes) if s > 0.08 * sizes.max()])
            al = np.asarray(cell.split()[3]).copy(); al[~ndimage.binary_dilation(keep, iterations=3)] = 0
            cell.putalpha(Image.fromarray(al))
        bb = cell.getbbox()
        if bb: cell = cell.crop(bb)
        p = os.path.join(name, f"{pose}.png"); cell.save(os.path.join(DIR, p)); saved[pose] = p
    idx = _index()
    idx[name] = dict(poses=saved, tags=list(tags), source=source)
    json.dump(idx, open(INDEX, "w"), indent=1)
    return saved

_cache = {}
def get(name, pose):
    idx = _index()
    if name not in idx or pose not in idx[name]["poses"]: return None
    k = (name, pose)
    if k not in _cache: _cache[k] = Image.open(os.path.join(DIR, idx[name]["poses"][pose])).convert("RGBA")
    return _cache[k]

def find(tag):
    return [n for n, v in _index().items() if tag in v["tags"] or tag == n]

def place(img, name, pose, cx, base_y, height, flip=False, a=1.0, rot=0.0):
    """pega el personaje con la base (pies) en base_y, centrado en cx y con la altura dada"""
    spr = get(name, pose)
    if spr is None or a <= 0.003: return None
    w = max(1, round(spr.width * height / spr.height))
    s = spr.resize((w, int(height)), Image.LANCZOS)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    if rot: s = s.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1: s.putalpha(s.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(s, (int(cx - s.width / 2), int(base_y - s.height)))
    return s.size

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        for n, v in _index().items(): print(f"{n:16s} {v['source']:10s} {','.join(v['poses'])}  [{','.join(v['tags'])}]")
    elif cmd == "add":
        sheet, name, poses = sys.argv[2], sys.argv[3], sys.argv[4].split(",")
        opts = dict(zip(sys.argv[5::2], sys.argv[6::2]))
        tags = opts.get("--tags", "").split(",") if opts.get("--tags") else []
        grid = tuple(int(v) for v in opts.get("--grid", "2x2").split("x"))
        print(add(sheet, name, poses, tags, opts.get("--source", "gemini"), grid))
