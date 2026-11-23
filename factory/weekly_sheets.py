"""Hojas de ilustraciones de la semana, a partir de los guiones visuales (PLAN.md paso 5b).

  python3 weekly_sheets.py list                    # guiones visuales de week_plan.json y estado de su hoja
  python3 weekly_sheets.py prompt <storyboard.md>  # prompt de la hoja (receta + reglas de LESSONS.md) y coste
  python3 weekly_sheets.py check <hoja.png> <storyboard.md>   # comprobacion previa al recorte (no escribe nada)
  python3 weekly_sheets.py cut <hoja.png> <storyboard.md>     # recorta a la biblioteca, quita barras negras de las tiras,
                                                              # aplica correcciones de conteo y lista lo que revisar

La generacion (ElevenLabs, gemini-3.1-flash-image, 2K, 1:1, UNA referencia = growth/style_ref_objects_4x4.png) la hace el
agente con las herramientas MCP: este script no gasta creditos. Cada guion visual lleva un bloque ```sheet con JSON:
  {"sheet": "week_w48", "tags": [...], "cells": [{"name": "...", "desc": "...", "size": "BIG|normal|strip|wide"}, ...],
   "derive": {"saturn": {"from": "seven_lights", "x": [0.80, 1.0]}}}
Las celdas van en orden de lectura. `strip` = tira que cabe en una celda; `wide` = tira que se desborda a 2 celdas (cuenta como 2 y la celda siguiente queda vacia).
"""
import json, os, re, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
import library as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREAMBLE = ("The attached reference is a sheet of 16 Moon-themed objects. Use it ONLY for the drawing style (flat 2D cartoon, "
            "clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but "
            "not childish). Do NOT draw anything that appears in the reference: no lunar module, no astronaut, no framed scene, "
            "no Moon-themed items other than the ones listed below.\n\n"
            "Draw ONE image: a regular grid of exactly 4 columns x 4 rows of identical square cells, one item per cell, centred, "
            "with a clear empty margin around it. No item may be taller or wider than its cell, and nothing may touch or cross a "
            "cell edge. Each item appears exactly once. Background: perfectly flat pure green #00FF00 everywhere. No white areas, "
            "no frames, no divider lines, no borders, no shadows. Objects have NO faces, eyes or smiles. NO text, letters or "
            "numbers painted anywhere (boxes and clock faces stay empty of numerals). No characters, no hands, no logos.\n"
            "Items marked BIG fill about 85% of their cell; wide strips fill about 90% of the cell width; the others fill about "
            "65% of their cell.\n\nCells in reading order, left to right, top to bottom:\n")

def spec(md):
    t = open(md, encoding="utf-8").read()
    m = re.search(r"```sheet\s*(\{.*?\})\s*```", t, re.S)
    if not m: sys.exit(f"{md}: falta el bloque ```sheet con la hoja del guion visual")
    return json.loads(m.group(1))

def lessons_extra(path=os.path.join(L.DIR, "LESSONS.md")):
    """lineas de LESSONS.md marcadas con 'PROMPT:' se añaden al prompt (reglas aprendidas que se aplican solas)"""
    if not os.path.exists(path): return ""
    return " ".join(re.findall(r"PROMPT:\s*(.+)", open(path, encoding="utf-8").read()))

def build_prompt(sp):
    n, lines = 0, []
    for c in sp["cells"]:
        n += 2 if c.get("size") == "wide" else 1
        tag = {"BIG": "BIG: ", "strip": "WIDE STRIP: ", "wide": "WIDE STRIP (it will spill over two cells side by side, so leave the next cell empty): "}.get(c.get("size"), "")
        lines.append(f"{len(lines)+1}. {tag}{c['desc']}")
    if n > 16: sys.exit(f"la hoja necesita {n} celdas (>16): dividir el inventario o quitar elementos")
    p = PREAMBLE + ";\n".join(lines) + "."
    if n < 16: p += f"\nLeave the remaining {16 - n} cells empty (flat green)."
    ex = lessons_extra()
    return p + (f"\n{ex}" if ex else ""), n

def figures(sheet):
    im = Image.open(sheet).convert("RGB"); full = L.key(im)
    al = np.asarray(full.split()[3]) > 60
    lab, k = nd.label(nd.binary_dilation(al, iterations=6))
    sl = [s for s in nd.find_objects(lab) if (s[0].stop - s[0].start) * (s[1].stop - s[1].start) > 4000]
    return im, sl

def check(sheet, md):
    sp = spec(md); im, sl = figures(sheet)
    want = len(sp["cells"])
    print(f"hoja {im.size}; figuras encontradas {len(sl)}, esperadas {want}")
    if im.size[0] != im.size[1]: print("  FALLO: la hoja no es cuadrada (¿edición de IA?)")
    if len(sl) != want: print("  REVISAR: faltan, sobran o se tocan figuras")
    for s in sl:
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        if max(h, w) < 250: print(f"  pequeña: {w}x{h} px")
    print("Comprobar a ojo: caras en objetos, texto pintado, elementos con número (marcas, columnas), todo lo del guion presente. Ver LESSONS.md.")
    return len(sl) == want

def strip_black(path):
    a = np.asarray(Image.open(path).convert("RGBA")).copy()
    dark = (a[..., :3].max(-1) < 60) & (a[..., 3] > 0)
    lab, k = nd.label(dark)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    m = nd.binary_dilation(np.isin(lab, list(edge)), iterations=1) & (a[..., :3].max(-1) < 90)
    a[m, 3] = 0; a[:10] = 0; a[-10:] = 0; a[:, :10] = 0; a[:, -10:] = 0
    im = Image.fromarray(a); im.crop(im.getbbox()).save(path)

def cut(sheet, md):
    sp = spec(md)
    if not check(sheet, md): print("El recorte sigue, pero revisa el aviso de arriba.")
    names = [c["name"] for c in sp["cells"]]
    L.add_blobs(sheet, sp["sheet"], names, tags=tuple(sp.get("tags", [])), source="elevenlabs")
    base = os.path.join(L.DIR, sp["sheet"])
    for c in sp["cells"]:
        if c.get("size") in ("wide", "strip"): strip_black(os.path.join(base, c["name"] + ".png"))
    idx = L._index()
    for new, d in sp.get("derive", {}).items():
        im = Image.open(os.path.join(base, d["from"] + ".png")); w, h = im.size
        sub = im.crop((int(w * d["x"][0]), 0, int(w * d["x"][1]), h)); sub = sub.crop(sub.getbbox())
        sub.save(os.path.join(base, new + ".png")); idx[sp["sheet"]]["poses"][new] = f"{sp['sheet']}/{new}.png"
        print(f"  derivado {new} {sub.size}")
    json.dump(idx, open(L.INDEX, "w"), indent=1)
    for c in sp["cells"]:
        p = os.path.join(base, c["name"] + ".png")
        if os.path.exists(p): print(f"  {c['name']}: {Image.open(p).size}")
    print("Ahora: pasar la lista de comprobacion de LESSONS.md, corregir por codigo los conteos y anotar defectos nuevos en LESSONS.md.")

def status():
    plan = json.load(open(os.path.join(ROOT, "growth", "week_plan.json")))
    idx = L._index()
    for e in plan:
        sb = e.get("storyboard")
        if not sb: print(f"{e['date']}: SIN guion visual -> escribirlo antes de generar nada"); continue
        p = os.path.join(ROOT, sb)
        if not os.path.exists(p): print(f"{e['date']}: falta {sb}"); continue
        try: sp = spec(p)
        except SystemExit as x: print(f"{e['date']}: {x}"); continue
        have = sp["sheet"] in idx and all(c["name"] in idx[sp["sheet"]]["poses"] for c in sp["cells"])
        print(f"{e['date']}: hoja {sp['sheet']} {'en la biblioteca' if have else 'POR GENERAR (918 creditos, preguntar antes)'}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list": status()
    elif a[0] == "prompt": pr, n = build_prompt(spec(a[1])); print(pr); print(f"\n[{n}/16 celdas; ≈918 creditos a 2K con una referencia]")
    elif a[0] == "check": check(a[1], a[2])
    elif a[0] == "cut": cut(a[1], a[2])
    else: print(__doc__)
