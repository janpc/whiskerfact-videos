"""Exporta a remotion/public SOLO materiales de origen para la versión Remotion de un reel:
voz, música, guion, tiempos de palabras, sprites de la biblioteca, piezas del gato, fuentes, efectos sueltos y la
línea de bocas por fotograma. NUNCA exporta nada compuesto por el motor de Python (fondos, fotogramas, mezcla final,
mp4 publicado, escenas de <slug>.py).

Se ejecuta DESDE factory/:   python3 ../remotion/export_raw.py <slug> --libs battery_items,large_w47
  --libs   bibliotecas de factory/library de las que Remotion puede usar sprites (las eliges mirando el guion y index.json)
Escribe también public/meta.json con el nº de fotogramas (voz + 0.3 s de entrada + 0.2 s de cola, 30 fps)."""
import os, sys, json, shutil, wave, subprocess, argparse
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("slug"); ap.add_argument("--libs", required=True)
a = ap.parse_args()
FACT = os.getcwd(); REPO = os.path.dirname(FACT); OUT = os.path.join(REPO, "remotion", "public"); D4 = "mascot/v4"
sys.path.insert(0, FACT); sys.path.insert(0, os.path.join(FACT, D4))
from PIL import Image
import mascot as M, sfx as SFX
for d in ("spr", "cat", "sfx", "fonts"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
S = a.slug
for src, dst in ((f"voice/{S}_brad.mp3", "voice.mp3"), (f"voice/{S}_music.mp3", "music.mp3"), (f"voice/{S}_brad_words.json", "words.json"), (f"voice/{S}_script.txt", "script.txt")):
    shutil.copy(src, f"{OUT}/{dst}")
for lib in a.libs.split(","):
    for f in os.listdir(f"library/{lib}"):
        if f.endswith(".png") and not f.startswith("sheet"): shutil.copy(f"library/{lib}/{f}", f"{OUT}/spr/{lib}__{f}")
shutil.copy("mascot/v3/base.png", f"{OUT}/cat/base.png"); shutil.copy("mascot/v3/eyes_03.png", f"{OUT}/cat/eyes_closed.png")
shutil.copy(f"{D4}/eyes2_01.png", f"{OUT}/cat/eyes_curious.png")
for k in ("closed", "mid", "wide", "round", "teeth", "laugh"): shutil.copy(f"{D4}/singles/mouth_{k}.png", f"{OUT}/cat/mouth_{k}.png")
for p in ("stand_front", "explain"): shutil.copy(f"{D4}/body_{p}.png", f"{OUT}/cat/body_{p}.png")
shutil.copy(f"{D4}/fonts/LondrinaSolid-Regular.ttf", f"{OUT}/fonts/Londrina.ttf")
for f in ("Black", "ExtraBold"): shutil.copy(f"/usr/share/fonts/opentype/inter/Inter-{f}.otf", f"{OUT}/fonts/Inter-{f}.otf")
TOP = 687; info = {}
for k in ("closed", "mid", "wide", "round", "teeth", "laugh"):
    im = np.asarray(Image.open(f"{OUT}/cat/mouth_{k}.png").convert("RGBA"))[..., 3] > 128; im[:, 500:560] = False; im[:645] = False
    ys = np.where(im.any(1))[0]; info[k] = TOP - int(ys.min()) if len(ys) else 0
info["round"] = 14   # corregido a mano (19/11): la boca redonda queda pegada a la nariz
json.dump(info, open(f"{OUT}/cat/mouth_dy.json", "w"))
def wav(name, x):
    x = np.asarray(x, np.float32); x = x / (np.max(np.abs(x)) or 1) * 0.9
    with wave.open(f"{OUT}/sfx/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SFX.SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
for n, fn in dict(tap=lambda: SFX.tap(587.33), whoosh=lambda: SFX.whoosh(0.45), pop=SFX.pop, click=SFX.click, sparkle=SFX.sparkle).items(): wav(n, fn())
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{OUT}/voice.mp3"]))
frames = int(round((dur + 0.3 + 0.2) * 30))
text = " ".join(open(f"voice/{S}_script.txt").read().split())
ph = M.phone_align(f"{OUT}/voice.mp3", text)
mouths = M.Cat.lipsync(None, ph, 30, frames, 0.3, lead=3)
json.dump(mouths, open(f"{OUT}/mouth.json", "w"))
json.dump({"slug": S, "frames": frames, "fps": 30, "voice_s": dur}, open(f"{OUT}/meta.json", "w"))
print("ok", S, "frames", frames, "voice", round(dur, 2), "mouths", sorted(set(mouths)))
