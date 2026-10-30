"""Cierre v5: el Mr. Whiskerfact nuevo (por piezas, mascot.py) dentro de su círculo DICE el eslogan.
El círculo entra con rebote, el gato mira a cámara, habla con los labios sincronizados (fonemas reales de
voice/slogan_<voz>.mp3), el eslogan aparece palabra a palabra en dorado, y al acabar guiña y sonríe.
Misma duración y huecos que el v4 (B.MASCOT["outro"]["dur"]), así la música y los efectos siguen encajando.
  python3 outro5.py preview 0.3 1.2 2.9 3.3   -> out/outro5_preview.jpg
"""
import json, math, os, sys
from PIL import Image
import brand as B
import outro2 as o
import outro4 as o4
from outro2 import clamp, eo, back_out, lerp
from mascot import Cat, phone_align

W, H, FPS = B.W, B.H, B.FPS
HERE = o.HERE
SLOGAN_AT = 0.4
WORDS = [SLOGAN_AT + t for t in (0.07, 0.38, 1.39, 1.62)]   # voice_reel lo reajusta según la voz
WINK = SLOGAN_AT + 2.31 + 0.15
VOICE = "brad"

_cat, _mouths = None, None
def cat():
    global _cat
    if _cat is None: _cat = Cat()
    return _cat

def mouths():
    """bocas por fotograma del cierre (fonemas en caché: voice/slogan_<voz>_phones.json)"""
    global _mouths
    if _mouths is None:
        mp3 = os.path.join(HERE, "voice", f"slogan_{VOICE}.mp3")
        cache = mp3.replace(".mp3", "_phones.json")
        if not os.path.exists(cache): json.dump(phone_align(mp3, B.SLOGAN), open(cache, "w"))
        ph = json.load(open(cache))
        n = int(B.MASCOT["outro"]["dur"] * FPS) + 2
        _mouths = cat().lipsync(ph, FPS, n, SLOGAN_AT)
    return _mouths

def badge(face):
    """gato (1024) dentro del círculo navy con aro dorado (1080)"""
    im = o4.disc().copy()
    f = face.resize((980, 980), Image.LANCZOS)
    im.alpha_composite(f, (50, 40))                       # cabeza grande y centrada; los hombros los corta el círculo
    out = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    out.paste(im, (0, 0), o4.MASK)
    ring = Image.new("RGBA", (2160, 2160), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(ring).ellipse([24, 24, 2136, 2136], outline=B.GOLD, width=28)
    out.alpha_composite(ring.resize((1080, 1080), Image.LANCZOS))
    return out

def face_at(t):
    i = min(int(t * FPS), len(mouths()) - 1)
    mouth, eyes, gaze = mouths()[i], None, (0, 0)
    if t < 0.3: gaze = (-0.6, 0.1)                          # llega mirando a un lado...
    elif 0.3 <= t < 0.38: eyes = "closed"                  # ...parpadea y mira a cámara
    if WINK <= t < WINK + 0.5: eyes, mouth = "wink", "smile"
    elif t >= WINK + 0.5: eyes, mouth = "happy", "happy"
    return cat().frame(mouth, eyes, gaze)

def frame(t):
    img = o.BG.copy(); o.chrome(img)
    k = back_out(t / 0.5)
    size = 640 * (0.55 + 0.45 * k)
    cy = lerp(1750, 1060, eo(t / 0.5))
    tilt = 4 * math.sin(clamp((t - WINK) / 0.45) * math.pi / 2)
    b = badge(face_at(t))
    if tilt: b = b.rotate(tilt, Image.BICUBIC)
    nod = 0
    pulse = clamp((t - WINK) / 0.7) if WINK <= t < WINK + 0.7 else 0
    o4.put_badge(img, b, size, 540, cy + nod, pulse)
    o.word_slogan(img, t, WORDS)
    return img

if __name__ == "__main__":
    if sys.argv[1:2] == ["preview"]:
        o.BG = Image.new("RGBA", (W, H), (30, 40, 70, 255))
        ims = [frame(float(x)).convert("RGB").resize((360, 640)) for x in sys.argv[2:]]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
        sh.save(os.path.join(HERE, "out", "outro5_preview.jpg"), quality=88)
        print("ok")
