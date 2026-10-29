"""Reel de los delfines sincronizado con una voz de ElevenLabs.
Las escenas se cortan entre las frases de la voz, los subtítulos siguen cada palabra
y el narrador dice el eslogan en el cierre, con cada palabra apareciendo al pronunciarse.

  python3 dolphins_voice.py brad            -> renderiza y mezcla con la voz de Brad
  python3 dolphins_voice.py brad mux        -> solo vuelve a mezclar el audio
  python3 dolphins_voice.py brad preview t1 t2 ...
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
import brand as B, music as M, sfx as SFX
import dolphins as D
from dolphins import R
from reel_lib import clamp, eo, W, FPS, HERE
import outro4

VOICE = sys.argv[1] if len(sys.argv) > 1 else "brad"
VDIR = os.path.join(HERE, "voice")
VOICE_MP3 = os.path.join(VDIR, f"dolphins_{VOICE}.mp3")
SLOGAN_MP3 = os.path.join(VDIR, f"slogan_{VOICE}.mp3")
VOICE_OFF = B.VOICE["offset"]
WORDS = [(w, s + VOICE_OFF, e + VOICE_OFF) for w, s, e in json.load(open(os.path.join(VDIR, f"dolphins_{VOICE}_words.json")))]

# ---------- frase de cierre: responde al gancho antes del eslogan ----------
WRAP_MP3 = os.path.join(VDIR, f"wrap_{VOICE}.mp3")
WRAP_GAP = 0.5                                    # silencio entre la última frase y el cierre
WRAP_AT = round(WORDS[-1][2] + WRAP_GAP, 2)       # dónde entra el audio de cierre
WORDS += [(w, s + WRAP_AT, e + WRAP_AT) for w, s, e in json.load(open(os.path.join(VDIR, f"wrap_{VOICE}_words.json")))]

# ---------- escenas: cada una empieza con su frase ----------
SCENE_OPENERS = [("hook", "This"), ("breath", "For"), ("problem", "If"), ("half", "The"), ("eye", "That's"),
                 ("swap", "Then"), ("third", "In"), ("calves", "And"), ("wrap", "So")]
FIRST_WORD, i = {}, 0
for name, word in SCENE_OPENERS:      # primera palabra de cada escena, en orden, buscada en lo que dice la voz
    while WORDS[i][0] != word or (name == "wrap" and WORDS[i][1] < WRAP_AT): i += 1
    FIRST_WORD[name] = i; i += 1
names = list(FIRST_WORD)
cut = [0.0] + [(WORDS[FIRST_WORD[n] - 1][2] + WORDS[FIRST_WORD[n]][1]) / 2 for n in names[1:]]
OUTRO_AT = round(WORDS[-1][2] + 0.6, 2)
NEW_SC = {n: (cut[i], cut[i + 1] if i + 1 < len(names) else OUTRO_AT) for i, n in enumerate(names)}

OLD_SC = dict(D.SC)
D.SC.clear(); D.SC.update(NEW_SC); D.OUTRO_AT = OUTRO_AT; R.total = OUTRO_AT + 4.8
R.caption = lambda *a, **k: None

moved = []
for t, n, g in R.events:
    for k, (s, e) in OLD_SC.items():
        if s <= t < e:
            ns, ne = NEW_SC[k]; moved.append((min(ns + (t - s), ne - 0.2), n, g)); break
R.events = moved
WS = NEW_SC["wrap"][0]
HALF_T = next(s for w, s, e in WORDS if w == "Half" and s > WRAP_AT)
R.events += [(WS + 0.05, "whoosh", 0.8), (WS + 0.5, "pop", 0.6), (HALF_T, "sparkle", 0.7)]

# ---------- cierre con el eslogan narrado ----------
SLOGAN_AT = 0.6                                   # el narrador habla cuando el círculo ya ha aterrizado
SLOGAN_WORDS = {"brad": [0.07, 0.38, 1.39, 1.62]}  # inicio de cada palabra en slogan_<voz>.mp3
SLOGAN_END = {"brad": 2.31}
outro4.WORDS_A = [SLOGAN_AT + t for t in SLOGAN_WORDS[VOICE]]
outro4.WINK = SLOGAN_AT + SLOGAN_END[VOICE] + 0.2   # el guiño, justo después de la última palabra

# ---------- subtítulos de voz ----------
def build_blocks():
    f, size, lh = R.font("voicesub")
    blocks, cur = [], []
    def fits(ws): return len(R.wrap(" ".join(w for w, _, _ in ws), f, B.TEXT_MAX_W)) <= 2
    for w in WORDS:
        if cur and not fits(cur + [w]): blocks.append(cur); cur = []
        cur.append(w)
        if w[0][-1] in ".?!" and len(cur) >= 3: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    return [(b, b[0][1], (blocks[i + 1][0][1] - 0.05) if i + 1 < len(blocks) else b[-1][2] + 0.4) for i, b in enumerate(blocks)]
BLOCKS = build_blocks()

def voice_subs(img, T):
    if T < NEW_SC["hook"][1] or T >= OUTRO_AT: return
    f, size, lh = R.font("voicesub"); lhp = int(size * lh); y0 = B.ZONES["caption"][0]
    for words, t0, t1 in BLOCKS:
        if not (t0 <= T < t1 + B.SUBS_BLOCK_EXIT): continue
        out_a = 1 - clamp((T - t1) / B.SUBS_BLOCK_EXIT)
        k = 0
        for li, line in enumerate(R.wrap(" ".join(w for w, _, _ in words), f, B.TEXT_MAX_W)):
            x = W / 2 - f.getlength(line) / 2
            for wtxt in line.split():
                _, s, e = words[k]; k += 1
                a = clamp((T - s) / B.SUBS_WORD_FADE) * out_a
                if a > 0:
                    col = R.acc_t if s <= T < e + 0.05 else B.TEXT
                    R.put(img, R.sprite(wtxt, "voicesub", col, align="left"), x, y0 + li * lhp, a, "lt", dy=(1 - eo(a)) * B.SUBS_WORD_RISE)
                x += f.getlength(wtxt + " ")

def wrap_frame(T):
    """vuelve a la imagen del gancho: el delfín dormido con el ojo abierto, ahora con la respuesta"""
    s, e = NEW_SC["wrap"]; t = T - s
    img = R.bg.copy(); D.bubbles(img, T, 0.8)
    a = D.eo(t / 0.4)
    bob = 14 * D.math.sin(T * 2.2)
    D.dolphin(img, D.CX, D.CY + 40 + bob, 1.15, eye="open", tilt=3 * D.math.sin(T * 2.2), alpha=a)
    D.zzz(img, D.CX - 300, D.CY - 40, T, clamp((t - 0.4) / 0.3))
    k = clamp((T - HALF_T) / 0.5)                  # al decir "Half": medio cerebro dormido sobre el delfín
    if k > 0: D.brain(img, D.CX + 250, D.CY - 230, 0.0, 1.0, 0.38, k)
    R.chrome(img, T)
    out = D.win(T, s, e + 1)
    R.txt(img, "Now you know:", D.TITLE_Y, "title", B.TEXT_2, out)
    R.txt(img, "half of it is asleep", D.TITLE_Y + 97, "title", D.ACC_T, D.win(T, s + 0.8, e + 1))
    return R.flash(img, T, HALF_T)

def frame_at(T):
    img = wrap_frame(T) if NEW_SC["wrap"][0] <= T < OUTRO_AT else D.frame_at(T)
    voice_subs(img, T)
    return img

# ---------- audio ----------
def load(path, n, at):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SFX.SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32); out = np.zeros(n, np.float32); i = int(at * SFX.SR)
    v = v[: n - i]; out[i:i + len(v)] = v
    return out

def build_audio(path):
    total = OUTRO_AT + 4.8; n = int(total * SFX.SR)
    voice = load(VOICE_MP3, n, VOICE_OFF) + load(WRAP_MP3, n, WRAP_AT) + load(SLOGAN_MP3, n, OUTRO_AT + SLOGAN_AT)
    voice /= (np.max(np.abs(voice)) or 1)
    env = np.convolve((np.abs(voice) > 0.02).astype(np.float32), np.ones(int(0.25 * SFX.SR)) / int(0.25 * SFX.SR), "same")
    env = np.clip(env * 4, 0, 1)
    gens = dict(tap=lambda: SFX.tap(587.33), whoosh=lambda: SFX.whoosh(0.45), pop=SFX.pop, click=SFX.click,
                clink=SFX.clink, sparkle=SFX.sparkle, bubble=lambda: SFX.pop(900, 500, 0.09))
    kept = []
    for e in sorted(R.events):
        if sum(1 for k in kept if e[0] - k[0] < 1.0) < B.SFX_MAX_PER_SECOND: kept.append(e)
    O = OUTRO_AT
    outro_fx = [(O, SFX.whoosh(0.5), 0.6), (O + 0.42, SFX.pop(), 0.9), (O + 0.86, SFX.click(), 0.4),
                (O + 1.6, SFX.clink(), 0.9), (O + outro4.WINK, SFX.sparkle(), 0.9)]   # sin taps: las palabras las dice la voz
    fx = SFX.mix([(t, gens[nm](), g) for t, nm, g in kept] + outro_fx, total)[:n]
    fx = fx / (np.max(np.abs(fx)) or 1) * 0.9 * 10 ** (B.SFX_UNDER_VOICE_DB / 20) * (1 - 0.5 * env)
    bed = M.upbeat_doc_bed(total, R.cat, swell_at=OUTRO_AT - 8)[:n]
    bed = M.duck(bed, env, B.MUSIC_DUCK_DB) * 0.9 * 10 ** (B.MUSIC_UNDER_VOICE_DB / 20 + 0.25)
    mix = voice * 0.9 + fx + bed
    SFX.write_wav(path, mix / max(1.0, np.max(np.abs(mix)) / 0.95))

NAME = f"whiskerfact_dolphins_{VOICE}"
def mux():
    out_dir = os.path.join(HERE, "out", NAME)
    wav = os.path.join(out_dir, "audio_voice.wav"); build_audio(wav)
    final = os.path.join(HERE, "out", f"{NAME}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(out_dir, "silent.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", f"loudnorm=I={B.VOICE_LUFS}:TP=-1.5", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", final], check=True)
    return final

if __name__ == "__main__":
    mode = sys.argv[2] if len(sys.argv) > 2 else "render"
    if mode == "preview":
        ims = [frame_at(float(t)).convert("RGB").resize((360, 640)) for t in sys.argv[3:]]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
        sh.save(os.path.join(HERE, "out", "dolphins_voice_preview.jpg"), quality=88); sys.exit()
    if mode == "render":
        R.render(list(NEW_SC.items()), frame_at, NAME, OUTRO_AT)
    print(mux())
