"""Control de calidad automático de un reel ANTES de publicarlo.
  python3 qa.py <slug>            (después de `python3 <slug>.py render`)
Muestrea el vídeo a 5 fps con el mismo motor que lo dibuja (sabe qué texto hay, dónde y cuándo) y revisa el mp4 final.
Escribe out/<slug>_qa.md (informe) y out/<slug>_qa.jpg (fotogramas con los fallos marcados en rojo).
Sale con código 1 si hay algún FALLO: ese reel no se publica hasta corregirlo. Los AVISOS se revisan a ojo.

Qué comprueba
- Textos: contraste con lo que tienen detrás, que no se pisen entre sí, que no caigan bajo los botones de la app
  ni fuera de pantalla, y que las etiquetas y títulos duren lo bastante para leerse.
- Dibujo: escenas que se salen de la banda de ilustración (cortes) y tramos en los que no se mueve nada.
- Vídeo final: duración mínima, fotogramas negros, volumen (LUFS) y picos.
"""
import importlib, json, math, os, re, subprocess, sys
from collections import defaultdict
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand as B
import reel_lib as RL

FPS_QA = 5
SMALL = {"label", "voicesub", "chip", "brand"}

def lum(c):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast(c1, c2):
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)

def fit_box(V, scene, box):
    """las cajas de texto dentro de la banda de ilustración se mueven con el reencuadre automático"""
    p = V._fit_params(scene) if scene and V.autofit and scene != "hook" else None
    zy0, zy1 = V.FIT_ZONE
    cy = (box[1] + box[3]) / 2
    if p is None or not (zy0 <= cy <= zy1): return box
    x0, y0, x1, y1, sc, cx, cyy = p
    ox = cx - ((x0 + x1) / 2) * sc; oy = cyy - ((y0 + y1) / 2 - zy0) * sc
    return (int(box[0] * sc + ox), int((box[1] - zy0) * sc + oy), int(box[2] * sc + ox), int((box[3] - zy0) * sc + oy))

def run(slug):
    out_dir = os.path.join(HERE, "out")
    sys.argv = [f"{slug}.py", "qa"]
    mod = importlib.import_module(slug)
    V, R = mod.V, mod.R
    fails, warns = [], []
    # 1) encuadre (calcula todos los reencuadres antes de registrar textos)
    for n in V.sc:
        if n != "hook": V._fit_params(n)          # el gancho nunca se reencuadra
    for w in getattr(V, "warnings", []): fails.append(("—", f"Dibujo cortado: {w}"))
    # 2) muestreo
    RL.QA_LOG = []
    times = [i / FPS_QA for i in range(int(V.outro_at * FPS_QA))]
    frames, small = {}, {}
    for T in times:
        start = len(RL.QA_LOG)
        img = V.frame_at(T).convert("RGB")
        frames[T] = np.asarray(img.resize((270, 480)), np.int16)
        small[T] = img
        for e in RL.QA_LOG[start:]: e["T"] = T
    log = RL.QA_LOG; RL.QA_LOG = None
    bad_frames = defaultdict(list)          # T -> [(box, motivo)]

    # 3) textos
    by_T = defaultdict(list)
    for e in log:
        e["box"] = fit_box(V, e["scene"], e["box"])
        by_T[e["T"]].append(e)
    worst = {}
    for T, es in by_T.items():
        arr = np.asarray(small[T], np.int16)
        vis = [e for e in es if e["a"] > 0.6]
        for e in vis:
            x0, y0, x1, y1 = e["box"]
            st = e["style"]
            if st in ("brand", "chip"): continue
            # fuera de pantalla / bajo los botones de la app
            if x0 < 10 or x1 > B.W - 10:
                fails.append((f"{T:.1f}s", f"Texto fuera de pantalla: «{e['text']}»")); bad_frames[T].append((e["box"], "fuera"))
            if st != "voicesub" and y1 > B.RAIL_TOP and x1 > B.SAFE_RIGHT_LOW + 15:
                fails.append((f"{T:.1f}s", f"Texto bajo los botones de la app: «{e['text']}»")); bad_frames[T].append((e["box"], "botones"))
            # contraste: color del texto frente a lo que hay detrás (mediana de la caja sin los píxeles del texto)
            if B.TEXT_STROKE.get(st, 0) > 0: continue                 # con borde oscuro se lee sobre cualquier fondo
            if st == "label" and sum(e["color"]) > 380: continue        # etiqueta clara: lleva pastilla oscura
            xa, ya, xb, yb = max(0, x0), max(0, y0), min(B.W, x1), min(B.H, y1)
            if xb - xa < 4 or yb - ya < 4: continue
            patch = arr[ya:yb, xa:xb].reshape(-1, 3)
            far = patch[np.abs(patch - np.array(e["color"])).sum(1) > 90]
            if len(far) < 20: continue
            bg = np.median(far, axis=0)
            c = contrast(e["color"], bg)
            need = 4.5 if st in SMALL else 3.0
            k = (e["text"], st)
            if c < need and (k not in worst or c < worst[k][0]): worst[k] = (c, T, e["box"], need)
        # textos que se pisan (los subtítulos palabra a palabra no cuentan entre sí)
        boxes = [e for e in vis if e["style"] not in ("brand", "chip")]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a["style"] == b["style"] == "voicesub": continue
                ix = max(0, min(a["box"][2], b["box"][2]) - max(a["box"][0], b["box"][0]))
                iy = max(0, min(a["box"][3], b["box"][3]) - max(a["box"][1], b["box"][1]))
                area = min((a["box"][2] - a["box"][0]) * (a["box"][3] - a["box"][1]), (b["box"][2] - b["box"][0]) * (b["box"][3] - b["box"][1]))
                if area and ix * iy / area > 0.15:
                    fails.append((f"{T:.1f}s", f"Textos que se pisan: «{a['text']}» y «{b['text']}»"))
                    bad_frames[T] += [(a["box"], "pisa"), (b["box"], "pisa")]
    for (t, st), (c, T, box, need) in worst.items():
        msg = f"Contraste bajo ({c:.1f}:1, mínimo {need}) en «{t}» ({st})"
        (fails if c < 2.0 else warns).append((f"{T:.1f}s", msg)); bad_frames[T].append((box, "contraste"))
    # duración en pantalla de etiquetas y títulos
    seen = defaultdict(list)
    for e in log:
        if e["style"] in ("label", "title", "number", "subtitle") and e["a"] > 0.6: seen[(e["text"], e["style"])].append(e["T"])
    for (t, st), ts in seen.items():
        ts = sorted(set(ts)); runs, cur = [], [ts[0]]
        for x in ts[1:]:
            if x - cur[-1] <= 1.5 / FPS_QA: cur.append(x)
            else: runs.append(cur); cur = [x]
        runs.append(cur)
        dur = max(r[-1] - r[0] + 1 / FPS_QA for r in runs)
        need = B.LABEL_MIN_ON if st == "label" else 1.2
        if dur < need:
            (fails if dur < 0.8 * need else warns).append((f"{ts[0]:.1f}s", f"«{t}» ({st}) solo {dur:.1f}s en pantalla (mínimo {need}s)"))

    # 4) ritmo: tramos sin movimiento en la ilustración
    still = 0.0; start = None
    for i in range(1, len(times)):
        d = np.abs(frames[times[i]][180:450] - frames[times[i - 1]][180:450]).mean()
        if d < 0.35:
            still += 1 / FPS_QA; start = start if start is not None else times[i - 1]
        else:
            if still > 2.0: (fails if still > 3.5 else warns).append((f"{start:.1f}s", f"Nada se mueve durante {still:.1f}s"))
            still, start = 0.0, None
    # 5) mp4 final
    mp4 = os.path.join(out_dir, f"whiskerfact_{slug}.mp4")
    if not os.path.exists(mp4):
        fails.append(("—", f"No existe {mp4}: falta el render"))
    else:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                   capture_output=True, text=True).stdout.strip() or 0)
        if dur < B.MIN_DURATION: fails.append(("—", f"Duración {dur:.1f}s, por debajo del mínimo {B.MIN_DURATION}s"))
        er = subprocess.run(["ffmpeg", "-nostats", "-i", mp4, "-af", "ebur128=peak=true", "-vf", "blackdetect=d=0.3:pic_th=0.97",
                             "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.findall(r"I:\s+(-?[\d.]+) LUFS", er); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", er)
        if m:
            I = float(m[-1])
            if not -19 <= I <= -13: fails.append(("—", f"Volumen {I} LUFS (debe estar entre -19 y -13)"))
        if p and float(p[-1]) > -0.5: warns.append(("—", f"Pico de audio {p[-1]} dBFS (riesgo de saturación)"))
        for a_, b_ in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", er):
            fails.append((f"{float(a_):.1f}s", f"Fotogramas negros hasta {float(b_):.1f}s"))

    # 6) informe y hoja de fotogramas
    def dedup(lst):
        seen_, out = set(), []
        for t, m in lst:
            if m not in seen_: seen_.add(m); out.append((t, m))
        return out
    fails, warns = dedup(fails), dedup(warns)
    marked = sorted(bad_frames)[:12] or times[:: max(1, len(times) // 12)][:12]
    tiles = []
    for T in marked:
        im = small[T].copy(); d = ImageDraw.Draw(im)
        for box, why in bad_frames.get(T, []):
            d.rectangle(box, outline=(255, 40, 40), width=8)
        d.rectangle([B.SAFE_RIGHT_LOW, B.RAIL_TOP, B.W, 1700], outline=(255, 200, 0), width=3)
        d.text((20, 20), f"{T:.1f}s", fill=(255, 255, 0))
        tiles.append(im.resize((270, 480)))
    cols = min(6, len(tiles)); rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (270 * cols, 480 * rows), (0, 0, 0))
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * 270, (i // cols) * 480))
    sheet.save(os.path.join(out_dir, f"{slug}_qa.jpg"), quality=85)
    lines = [f"# QA {slug}", "", f"**{'NO PUBLICAR' if fails else 'OK para publicar'}** · {len(fails)} fallos · {len(warns)} avisos", ""]
    lines += ["## Fallos"] + [f"- {t} · {m}" for t, m in fails] + [""] if fails else []
    lines += ["## Avisos"] + [f"- {t} · {m}" for t, m in warns] + [""] if warns else []
    lines += [f"Hoja: out/{slug}_qa.jpg (rojo = problema, amarillo = zona de botones de la app)"]
    rep = os.path.join(out_dir, f"{slug}_qa.md"); open(rep, "w").write("\n".join(lines))
    print("\n".join(lines))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(run(sys.argv[1]))
