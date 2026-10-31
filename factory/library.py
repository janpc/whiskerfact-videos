"""Biblioteca de personajes (personas y animales) en el estilo del gato, para no dibujarlos con formas en código.
Cada personaje tiene 2 hojas de 3x3 poses sobre verde (Gemini gratis a mano, o ElevenLabs puntualmente), recortadas aquí:
  hoja 1 «movimiento»: ciclo de andar/correr de perfil (4 fotogramas), quieto de perfil, de frente, 3/4, sentado/tumbado, salto/acción
  hoja 2 «actuación»: expresiones y gestos (contento, asustado, sorprendido, pensando, señalando, hablando, ...)

  python3 library.py add <hoja.png> <nombre> <pose1,...,pose9> [--tags a,b] [--source gemini|elevenlabs] [--grid 3x3]   (pose '-' = celda descartada)
  python3 library.py list
En una escena:
  import library as LIB
  spr = LIB.get("dog", "side")            # RGBA recortado al contenido, None si no existe
  LIB.find("animal")                       # nombres con esa etiqueta
  LIB.place(img, "dog", "side", cx, base_y, height, flip=False, a=1.0, rot=0)   # lo pega con los pies en base_y
Animar: andar/correr = recorrer walk1..walk4 (o run1..run4) a 8-10 fps mientras el sprite avanza; quieto = pose fija con
respiración (escala 1-2 %) y algún cambio de expresión; los gestos se encadenan (front -> point -> front).
Helper: LIB.cycle("dog", "run", T, fps=10) devuelve la pose del ciclo en el instante T.
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

def _cuts(im, cols, rows):
    """bordes de las celdas: si la hoja trae líneas separadoras (Gemini a veces las dibuja y no son regulares) se usan;
    si no, rejilla uniforme"""
    a = np.asarray(im).astype(int)
    green = (a[..., 1] - np.maximum(a[..., 0], a[..., 2])) > 60
    def lines(frac_axis, n, length):
        nong = 1 - green.mean(axis=frac_axis)                  # fracción no verde de cada fila/columna
        cand = [i for i in range(length) if nong[i] > 0.9]
        groups = []
        for i in cand:
            if groups and i - groups[-1][-1] <= 3: groups[-1].append(i)
            else: groups.append([i])
        inner = [int(np.mean(g)) for g in groups if 10 < np.mean(g) < length - 10]
        if len(inner) == n - 1: return [0] + inner + [length]
        return [round(k * length / n) for k in range(n + 1)]
    return lines(0, cols, im.width), lines(1, rows, im.height)

def add(sheet, name, poses, tags=(), source="gemini", grid=(3, 3)):
    im = Image.open(sheet).convert("RGB")
    cols, rows = grid
    xs, ys = _cuts(im, cols, rows)
    os.makedirs(os.path.join(DIR, name), exist_ok=True)
    k = len([f for f in os.listdir(os.path.join(DIR, name)) if f.startswith("sheet")]) + 1
    im.save(os.path.join(DIR, name, f"sheet{k}.png"))                 # un personaje puede tener varias hojas
    saved = {}
    for i, pose in enumerate(poses):
        if not pose or pose == "-": continue                            # celda que no sirve: se salta
        r, c = divmod(i, cols)
        cell = key(im.crop((xs[c] + 6, ys[r] + 6, xs[c + 1] - 6, ys[r + 1] - 6)))
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
    old = idx.get(name, dict(poses={}, tags=[], source=source))
    old["poses"].update(saved); old["tags"] = sorted(set(old["tags"]) | set(tags))
    idx[name] = old
    json.dump(idx, open(INDEX, "w"), indent=1)
    return saved

_cache = {}
def get(name, pose):
    idx = _index()
    if name not in idx or pose not in idx[name]["poses"]: return None
    k = (name, pose)
    if k not in _cache: _cache[k] = Image.open(os.path.join(DIR, idx[name]["poses"][pose])).convert("RGBA")
    return _cache[k]

def cycle(name, prefix, T, fps=9):
    """nombre de la pose de un ciclo (walk1..walkN) para el instante T"""
    poses = sorted(p for p in _index().get(name, {}).get("poses", {}) if p.startswith(prefix) and p[len(prefix):].isdigit())
    return poses[int(T * fps) % len(poses)] if poses else None

def find(tag):
    return [n for n, v in _index().items() if tag in v["tags"] or tag == n]

def place(img, name, pose, cx, base_y, height=None, flip=False, a=1.0, rot=0.0, scale=None, squash=(1.0, 1.0), anchor="bottom"):
    """pega el personaje con la base (pies) en base_y, centrado en cx.
    height: altura en px de ESTA pose; scale: factor sobre el tamaño de la hoja (usa scale en ciclos y cambios
    de pose para que el personaje no cambie de tamaño entre poses)"""
    spr = get(name, pose)
    if spr is None or a <= 0.003: return None
    k = scale if scale is not None else height / spr.height
    sx, sy = squash
    s = spr.resize((max(1, round(spr.width * k * sx)), max(1, round(spr.height * k * sy))), Image.LANCZOS)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    if rot: s = s.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1: s.putalpha(s.split()[3].point(lambda v: int(v * a)))
    y = base_y - s.height if anchor == "bottom" else (base_y - s.height / 2 if anchor == "center" else base_y)
    img.alpha_composite(s, (int(cx - s.width / 2), int(y)))
    return s.size

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        for n, v in _index().items(): print(f"{n:16s} {v['source']:10s} {','.join(v['poses'])}  [{','.join(v['tags'])}]")
    elif cmd == "add":
        sheet, name, poses = sys.argv[2], sys.argv[3], sys.argv[4].split(",")
        opts = dict(zip(sys.argv[5::2], sys.argv[6::2]))
        tags = opts.get("--tags", "").split(",") if opts.get("--tags") else []
        grid = tuple(int(v) for v in opts.get("--grid", "3x3").split("x"))
        print(add(sheet, name, poses, tags, opts.get("--source", "gemini"), grid))


# ---------- ayudas de animación (principios clásicos: arcos, aceleración, anticipación, seguimiento) ----------
import math
def ease(t): t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)

def bezier(p0, p1, p2, p3, t):
    """punto de una curva cúbica: las trayectorias van en ARCO, nunca en línea recta"""
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))

def along(p, t, dt=0.01):
    """posición y ángulo de la tangente (grados) en t de una curva bezier p=(p0,p1,p2,p3)"""
    a = bezier(*p, max(0, t - dt)); b = bezier(*p, min(1, t + dt))
    return bezier(*p, t), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))

def spring(t, amp=1.0, freq=3.0, damp=4.0):
    """oscilación amortiguada para el seguimiento (balanceo al aterrizar, rebote al pararse)"""
    return amp * math.exp(-damp * t) * math.cos(2 * math.pi * freq * t) if t >= 0 else 0.0
