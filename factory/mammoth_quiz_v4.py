"""mammoth_quiz con el ESTILO del 6/11 (plantilla: earth_tunnel_v4.py) (gato v4 hablando con sincronía labial, color por escena, letra Londrina Solid, tarjeta plana, grano).
Salida: out/whiskerfact_mammoth_quiz.mp4
  python3 mammoth_quiz_v4.py preview | clip <t0> [s] | render | mux
Igual que wifi_bands_v4.py: el gato solo sale en escenas SIN tarjeta (gancho, revelación «Ready? It's B» y cierre), a la izquierda,
con subtítulos estrechos a su derecha; el resto de escenas conserva su disposición.
"""
import os, sys, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "mascot", "v4"))
import brand as B
import reel_lib as RL
import style as ST

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

import mammoth_quiz as WB
import mascot as M
WB.CAT = True
V, R = WB.V, WB.R
BLOCKS_WIDE = V.blocks
_w, _c = B.SUBS_MAX_W, B.SUBS_CENTER_X
B.SUBS_MAX_W = 450; BLOCKS_NARROW = V._blocks(); B.SUBS_MAX_W = _w
R.hook_mascot = lambda *a, **k: None
type(V).name = property(lambda s: "whiskerfact_mammoth_quiz")

W, H, FPS = B.W, B.H, B.FPS
BLUE, ORANGE, GREEN, PURPLE, WINE, TEAL = (38, 98, 150), (150, 84, 40), (36, 112, 84), (84, 62, 130), (116, 52, 84), (30, 104, 120)
SCENE_COL = dict(opts=TEAL, optc=TEAL, rising=BLUE, dna=PURPLE, grew=PURPLE, why=WINE, maybe=GREEN)
def grad(col):
    top = col; bot = tuple(int(c * 0.72) for c in col)
    yy = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top) * (1 - yy) + np.array(bot) * yy) * np.ones((1, W, 1))
    return arr, Image.fromarray(arr.astype(np.uint8)).convert("RGBA"), tuple(int(c * 0.5) for c in col)
GR = {n: grad(c) for n, c in SCENE_COL.items()}
ORIG_BG = (R.bg_arr, R.bg)

EYES = dict(hook="curious", reveal="proud", wrap="sly")
POSE_PLAN = dict(hook=[(0, "stand_front"), (3.0, "explain")],
                 reveal=[(0, "hand_on_chin"), (1.2, "explain")],
                 wrap=[(0, "stand_front"), (1.0, "shrug")])   # 6/11: pose y respiración se quedan; lo que se quitó es el balanceo desde la cintura
def pose_at(n, t):
    cur = "stand_front"
    for t0, p in POSE_PLAN.get(n, [(0, "stand_front")]):
        if t >= t0: cur = p
    return cur

CAT_MODE = dict(hook="low", reveal="low", wrap="low")
cat = M.Cat4()
MOUTH = {}

def lipsync_all():
    tmp = tempfile.mkdtemp(); off = B.VOICE["offset"]
    for n, (s, e) in V.sc.items():
        if n not in CAT_MODE: continue
        ws = [w for w in V.words if s - 0.02 <= w[1] < e]
        if not ws: MOUTH[n] = None; continue
        wav = os.path.join(tmp, n + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, s - off):.3f}", "-to", f"{e - off:.3f}", "-i", V.voice_mp3, "-c:a", "libmp3lame", "-q:a", "2", wav], check=True)
        ph = M.phone_align(wav, " ".join(w[0] for w in ws))
        MOUTH[n] = cat.lipsync(ph, FPS, int((e - s) * FPS) + 2, max(0.0, off - s), lead=3)      # la voz entra a los 0,3 s: en el gancho (s=0) el recorte empieza en 0 pero suena en T=0,3, así que hay que retrasar la boca esos 0,3 s
        print("lipsync", n, len(ph), flush=True)
lipsync_all()

def _load_all(o, seen=None):
    seen = seen if seen is not None else set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, Image.Image): o.load()
    elif isinstance(o, dict):
        for v in o.values(): _load_all(v, seen)
    elif isinstance(o, (list, tuple)):
        for v in o: _load_all(v, seen)
    elif hasattr(o, "__dict__"):
        for v in vars(o).values(): _load_all(v, seen)
_load_all(cat)

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
CARD_DEF, FIT_DEF = (56, 742, 1024, 1384), (70, 760, B.SAFE_RIGHT_LOW, 1370)
def draw_cat(im, n, s, T):
    sc, cx, top = 0.36, 235, {"hook": 1190, "reveal": 1300, "wrap": 1300}[n]
    i = min(int((T - s) * FPS), len(MOUTH[n]) - 1) if MOUTH.get(n) else 0
    mouth = MOUTH[n][i] if MOUTH.get(n) else "smile"
    eyes = "closed" if blinking(T) else EYES[n]
    t = T - s; pose = pose_at(n, t)
    c = cat_img(pose, mouth, eyes, sc)
    for t0, p in POSE_PLAN.get(n, []):
        if -1e-6 <= t - t0 < POSE_FADE:
            prev = pose_at(n, t0 - 1e-3)
            if prev != pose: c = Image.blend(cat_img(prev, mouth, eyes, sc), c, max(0.0, t - t0) / POSE_FADE)
    br = 1 + 0.006 * np.sin(2 * np.pi * T / 3.2)           # respiración (se mantiene)
    cc = c.resize((round(c.width * br), round(c.height * br)), Image.LANCZOS)
    x0 = round(cx - 700 * sc - (cc.width - c.width) / 2); y0 = round(top - (cc.height - c.height))
    im.alpha_composite(cc, (x0, y0)) if x0 >= 0 else im.paste(cc, (x0, y0), cc)

_orig = V.frame_at
def frame_at(T):
    n, s = scene_of(T)
    if n in GR: R.bg_arr, R.bg = GR[n][0], GR[n][1]
    else: R.bg_arr, R.bg = ORIG_BG
    mode = CAT_MODE.get(n)
    V.FIT_BOX = FIT_DEF; V.FIT_MIN = 0.92
    narrow = mode == "low"
    V.blocks = BLOCKS_NARROW if narrow else BLOCKS_WIDE
    B.SUBS_MAX_W, B.SUBS_CENTER_X = (450, 668) if narrow else (_w, _c)
    im = _orig(T)
    if n is not None:
        im = im.convert("RGBA")
        if mode: draw_cat(im, n, s, T)
        a = np.asarray(im.convert("RGB")).astype(np.float32) + _grain
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    return im
_grain = np.random.default_rng(7).normal(0, 1.6, (H, W, 1)).astype(np.float32)
V.frame_at = frame_at

if __name__ == "__main__":
    V.main()
