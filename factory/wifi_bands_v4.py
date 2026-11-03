"""wifi_bands con el ESTILO NUEVO (prueba, 0 créditos: reutiliza voz y música ya pagadas). Salida: out/whiskerfact_wifi_bands_v4.mp4
  python3 wifi_bands_v4.py preview | clip <t0> [s] | render
Cambios respecto a wifi_bands.py (que no se toca):
- gato v4 con cuerpo (rebeca) como presentador, con sincronía labial por fonemas escena a escena; abajo a la izquierda, subtítulos a su derecha;
  la ilustración se reencuadra en una tarjeta más baja para dejarle sitio; pose de pie, brazos cruzados solo en «My take»
- color dominante por escena (cambia con el momento del vídeo); letra Londrina Solid; tarjeta plana sin sombra; grano plano sutil
- gancho, giro y cierre: paisaje de ciudad (fondo complejo) con el gato más grande
"""
import os, sys, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "mascot", "v4"))
import brand as B
import reel_lib as RL
import style as ST

# --- antes de construir el reel ---
B.SUBS_MAX_W = 450; B.SUBS_CENTER_X = 668           # subtítulos a la derecha del gato (x 443-893)
B.ZONES["caption"] = (1325, 1540)
FONT = os.path.join(HERE, "mascot", "v4", "fonts", "LondrinaSolid-Regular.ttf")
def _font(self, style):
    w, size, lh = B.TYPE[style]
    k = ("L", size)
    if k not in self._fonts: self._fonts[k] = ImageFont.truetype(FONT, int(size * 1.12))
    return self._fonts[k], size, lh
RL.Reel.font = _font

def _card(img, box, color=ST.CREAM, radius=36, a=1.0):          # tarjeta plana: sin sombra
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle(box, radius=radius, fill=color + (int(255 * a),), outline=ST.OUTLINE + (int(255 * a),), width=ST.OUTLINE_W)
    img.alpha_composite(ov)
ST.card = _card

import wifi_bands as WB
import mascot as M
V, R = WB.V, WB.R
WB.CARD = (56, 742, 1024, 1250)                      # tarjeta más baja: debajo va el gato
V.FIT_BOX = (70, 760, B.SAFE_RIGHT_LOW, 1232); V.FIT_MIN = 0.45
R.hook_mascot = lambda *a, **k: None                  # el avatar pequeño del gancho se sustituye por el gato v4
type(V).name = property(lambda s: "whiskerfact_wifi_bands_v4")

W, H, FPS = B.W, B.H, B.FPS
# ---------- color por escena ----------
BLUE, ORANGE, GREEN, PURPLE, WINE, TEAL = (38, 98, 150), (150, 84, 40), (36, 112, 84), (84, 62, 130), (116, 52, 84), (30, 104, 120)
SCENE_COL = dict(translate=BLUE, speed=BLUE, fly=BLUE, range=ORANGE, meanwhile=ORANGE, crowd=GREEN, picture=GREEN, twenty=GREEN,
                 inside=PURPLE, others=PURPLE, final=WINE, take=TEAL)
def grad(col):
    top = col; bot = tuple(int(c * 0.72) for c in col)
    yy = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top) * (1 - yy) + np.array(bot) * yy) * np.ones((1, W, 1))
    return arr, Image.fromarray(arr.astype(np.uint8)).convert("RGBA"), tuple(int(c * 0.5) for c in col)
GR = {n: grad(c) for n, c in SCENE_COL.items()}
ORIG_BG = (R.bg_arr, R.bg)

# ---------- gato: expresión y pose por escena (coherente: solo cambia la pose en «take») ----------
EYES = dict(hook="curious", translate="happy", speed="excited", fly="amused", range="skeptical", meanwhile="sly", crowd="worried",
            picture="thinking", twenty="surprised", twist="surprised", inside="worried", others="skeptical", final="proud", take="sly", close="amused")
POSE = {n: "stand_front" for n in EYES}; POSE["take"] = "arms_crossed"
cat = M.Cat4(); SC_CAT = 0.36; SC_HOOK = 0.46
MOUTH = {}                                            # escena -> lista de bocas por fotograma

def lipsync_all():
    tmp = tempfile.mkdtemp(); off = B.VOICE["offset"]
    for n, (s, e) in V.sc.items():
        ws = [w for w in V.words if s - 0.02 <= w[1] < e]
        if not ws: MOUTH[n] = None; continue
        wav = os.path.join(tmp, n + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, s - off):.3f}", "-to", f"{e - off:.3f}", "-i", V.voice_mp3, "-c:a", "libmp3lame", "-q:a", "2", wav], check=True)
        ph = M.phone_align(wav, " ".join(w[0] for w in ws))
        MOUTH[n] = cat.lipsync(ph, FPS, int((e - s) * FPS) + 2, 0.0)
        print("lipsync", n, len(ph), flush=True)
lipsync_all()

_cache = {}
def cat_img(pose, mouth, eyes, sc):
    k = (pose, mouth, eyes, sc)
    if k not in _cache: _cache[k] = cat.frame_body(pose, mouth, eyes, outline=9, fixed=(0, 0, 1400, 1700), scale=sc, sharpen=70)
    return _cache[k]

BLINK = [1.1 + 3.3 * k for k in range(40)]
def blinking(T): return any(0 <= T - b < 0.1 for b in BLINK)

def scene_of(T):
    for n, (s, e) in V.sc.items():
        if s <= T < e: return n, s
    return None, 0

POSE_FADE = 0.2
def draw_cat(im, n, s, T):
    big = n in ("hook", "twist", "close")
    sc = SC_HOOK if n == "hook" else SC_CAT
    i = min(int((T - s) * FPS), len(MOUTH[n]) - 1) if MOUTH.get(n) else 0
    mouth = MOUTH[n][i] if MOUTH.get(n) else "smile"
    eyes = "closed" if blinking(T) else EYES[n]
    c = cat_img(POSE[n], mouth, eyes, sc)
    prev = list(V.sc)[list(V.sc).index(n) - 1] if n != "hook" else None
    if prev and POSE[prev] != POSE[n] and T - s < POSE_FADE:                       # fundido corto entre poses; las cabezas coinciden (misma caja fija)
        c0 = cat_img(POSE[prev], mouth, eyes, sc)
        c = Image.blend(c0, c, (T - s) / POSE_FADE)
    cx = 255 if n != "hook" else 270
    top = 1262 if n != "hook" else 1250
    br = 1 + 0.006 * np.sin(2 * np.pi * T / 3.2)
    cc = c.resize((round(c.width * br), round(c.height * br)), Image.LANCZOS)
    x0 = round(cx - 700 * sc - (cc.width - c.width) / 2); y0 = round(top - (cc.height - c.height))
    im.alpha_composite(cc, (x0, y0)) if x0 >= 0 else im.paste(cc, (x0, y0), cc)

_orig = V.frame_at
def frame_at(T):
    n, s = scene_of(T)
    if n in GR: R.bg_arr, R.bg = GR[n][0], GR[n][1]
    else: R.bg_arr, R.bg = ORIG_BG
    im = _orig(T)
    if n is not None:
        im = im.convert("RGBA")
        base = GR[n][2] if n in GR else (22, 24, 34)
        ImageDraw.Draw(im).rectangle((0, 1690, W, H), fill=base + (255,))             # banda plana: tapa el corte de la cintura (bajo los botones de la app)
        draw_cat(im, n, s, T)
        ImageDraw.Draw(im).rectangle((0, 1690, W, H), fill=base + (255,))
        a = np.asarray(im.convert("RGB")).astype(np.float32) + _grain
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    return im
_grain = np.random.default_rng(7).normal(0, 1.6, (H, W, 1)).astype(np.float32)
V.frame_at = frame_at

if __name__ == "__main__":
    V.main()
