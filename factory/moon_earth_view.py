"""Reel: What if you stood on the Moon and looked back at Earth? Mr. Whiskerfact, categoría Space, formato what_if.
Voz de Brad. Tanda B2-length, opción `short` (variante): ejecutar con REEL_LENGTH=short. Estilo v4: moon_earth_view_v4.py.

Fuentes (dos por dato): ver voice/moon_earth_view_claims.md
- La Tierra casi quieta en el cielo lunar, libración: NASA StarChild (GSFC); Smithsonian Air & Space
- Día lunar 29,5 días: Sky at Night (BBC); Live Science (cita a NASA)
- Fases de la Tierra opuestas a las de la Luna: Live Science; Big Think / Wikipedia (Earth phase)
- Rotación síncrona: NASA Science (Top Moon Questions); Sky at Night
- Se aleja ~3,8 cm al año: NASA JPL; NASA GSFC (Apollo laser ranging)

Paisaje lunar propio (cielo negro sin atmósfera, suelo gris en capas con cráteres); Tierra, Luna, Sol y astronauta de la
biblioteca (earth_tunnel_items:earth, moon_items, astronaut) a ≤1,5x; fases (terminador), órbita y flechas por código.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import brand as B
import style as ST
import library as LIB
import cover as cover_mod
from reel_lib import Reel, clamp, eo, eio, lerp, win, W, H
from voice_reel import VoiceReel

SLUG = "moon_earth_view"
R = Reel("space")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
V = VoiceReel(R, SLUG, [
    ("hook", "Picture"), ("look", "From"), ("hours", "Hours"), ("lday", "Wait"), ("phases", "Instead"), ("full", "New"),
    ("why", "So"), ("lock", "It"), ("never", "So"), ("drift", "Meanwhile"), ("wrap", "Does")])
V._fits = {n: None for n in V.sc}          # cada escena coloca sus cosas a mano
V.FIT_MAX = 1.1

INK_T = ST.OUTLINE
RED_T = (176, 40, 58)
BLUE_T = (30, 74, 130)
CAT = False        # moon_earth_view_v4.py lo pone a True: el gato v4 habla en gancho y cierre
CARD = (56, 742, 1024, 1384)
GY = 1330          # suelo lunar
MI, EI, AS = "moon_items", "earth_tunnel_items", "astronaut"

def wt(word, s): return V.word_time(word, after=s)
def rel(scene, word): return V.word_time(word, after=V.sc[scene][0]) - V.sc[scene][0]
def lab(img, text, y, col, a, x=W / 2): R.txt(img, text, y, "label", col, a, x=x, rise=False)
def title(img, T, s, e, text, color=B.TEXT, delay=0.0): R.txt(img, text, TITLE_Y, "title", color, win(T, s + delay, e))
def on(T, word, s, e, need=1.6, lead=0.1): return clamp((T - min(wt(word, s), e - need) + lead) / 0.3)

def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def item(img, lib, name, x, y, h, a=1.0, anchor="center", flip=False, rot=0.0):
    LIB.place(img, lib, name, x, y, height=h, a=a, anchor=anchor, flip=flip, rot=rot)

# ---------- cuerpo con fase (Tierra o Luna): la parte no iluminada se oscurece con el terminador ----------
_phase_cache = {}
def body(img, lib, name, cx, cy, h, lit=1.0, a=1.0, light_right=True):
    """lit: fracción iluminada 0 (nueva) .. 1 (llena); la luz viene de la derecha (o de la izquierda)"""
    if a <= 0.003: return
    size = int(h * 1.08) + 8
    k = (lib, name, int(h), round(lit, 3), light_right)
    if k not in _phase_cache:
        lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        LIB.place(lay, lib, name, size / 2, size / 2, height=h, anchor="center")
        if lit < 0.999:
            r = h / 2
            yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
            u = (xx - size / 2) / r; v = (yy - size / 2) / r
            if not light_right: u = -u
            w = np.sqrt(np.clip(1 - v * v, 0, 1))
            ut = w * math.cos(math.pi * lit)
            soft = np.clip((u - ut) / 0.06 + 0.5, 0, 1)            # 1 = de día, 0 = de noche
            arr = np.asarray(lay).astype(np.float32)
            night = np.array([22, 26, 52], np.float32)
            k_d = (1 - soft)[..., None] * 0.86
            arr[..., :3] = arr[..., :3] * (1 - k_d) + night * k_d
            lay = Image.fromarray(arr.astype(np.uint8))
        _phase_cache[k] = lay
    lay = _phase_cache[k]
    if a < 1:
        lay = lay.copy(); lay.putalpha(lay.split()[3].point(lambda vv: int(vv * a)))
    img.alpha_composite(lay, (int(cx - size / 2), int(cy - size / 2)))
    mark_noink(lay, (int(cx - size / 2), int(cy - size / 2)))

def mark_noink(layer, pos):
    """marca un sprite de biblioteca pegado desde una capa intermedia para que el contorno automático (style.ink)
    no le repase los bordes interiores (LIB.place solo lo marca si dibuja directamente en el fotograma)"""
    import reel_lib as _RL
    from PIL import ImageChops
    m = _RL.NOINK["mask"]
    if m is None or m.size != (W, H): return
    tmp = Image.new("L", (W, H), 0); tmp.paste(layer.split()[3], (int(pos[0]), int(pos[1])))
    _RL.NOINK["mask"] = ImageChops.lighter(m, tmp)

# ---------- paisaje lunar: cielo negro (sin atmósfera), estrellas y suelo gris en capas ----------
MOON_GREYS = [(120, 120, 132), (96, 96, 108), (74, 74, 86), (52, 52, 62)]
def moonscape(img, T, star_shift=0.0, seed=0, pre=None):
    ST.sky(img, (6, 6, 20), (26, 24, 58), 0, GY)
    rng = np.random.default_rng(11 + seed); d = ImageDraw.Draw(img)
    for _ in range(90):
        x, y, r, ph = rng.uniform(0, W), rng.uniform(0, GY - 200), rng.uniform(1.5, 3.6), rng.uniform(0, 6.3)
        x = (x + star_shift) % W
        k = 0.6 + 0.4 * math.sin(T * 2.0 + ph)
        d.ellipse([x - r, y - r, x + r, y + r], fill=ST.mix((26, 24, 58), (255, 255, 245), k))
    if pre: pre(img, T)
    for i, (c, amp) in enumerate(zip(MOON_GREYS[:3], (70, 50, 36))):
        ST.dunes(img, GY - 150 + i * 55, amp, c, T, 0.0, seed=i + 3 + seed)
    d = ImageDraw.Draw(img)
    d.rectangle([0, GY, W, H], fill=(40, 40, 50))
    for (x, y, rx) in ((160, 1300, 60), (520, 1262, 44), (840, 1290, 70), (330, 1215, 30), (700, 1208, 26)):
        d.ellipse([x - rx, y - rx * 0.28, x + rx, y + rx * 0.28], fill=(60, 60, 72), outline=INK_T, width=3)
        d.ellipse([x - rx * 0.8, y - rx * 0.2, x + rx * 0.8, y + rx * 0.12], fill=(84, 84, 98))

def space_bg(img, T, seed=0):
    ST.sky(img, (8, 8, 26), (34, 28, 76)); ST.stars(img, T, n=110, seed=21 + seed, y1=H)

def arrow_h(img, x0, x1, y, a=1.0, col=(246, 196, 84), w=18, both=False):
    if a <= 0.003 or x1 - x0 < 10: return
    def fn(d, P, s):
        hh = 30
        d.rectangle([P(x0 + (hh if both else 0), y - w / 2), P(x1 - hh, y + w / 2)], fill=col, outline=INK_T, width=int(4 * s))
        d.polygon([P(x1 - hh, y - w * 1.2), P(x1 - hh, y + w * 1.2), P(x1, y)], fill=col, outline=INK_T)
        if both: d.polygon([P(x0 + hh, y - w * 1.2), P(x0 + hh, y + w * 1.2), P(x0, y)], fill=col, outline=INK_T)
    aa(img, (x0 - 6, y - 40, x1 + 6, y + 40), fn, a)

# =====================================================================  ESCENAS
EARTH_HOOK = (590, 1000, 330)
@V.scene("hook")
def _(img, T, t, s, e):
    bob = 6 * math.sin(T * 2.4)
    x, y, h = EARTH_HOOK
    body(img, EI, "earth", x, y + bob, h * (1 + 0.04 * eo(T / 0.4)))
    item(img, AS, "look_up_back", 805, 1170, 250)
    cover_mod.draw_header(img, "space")
    cover_mod.draw_title(img, "Earth", "from moon", "Does it ever set?", a=clamp((e - T) / B.EXIT))
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.3, "pop", 0.6), (rel("hook", "Does"), "tap", 0.7)])

@V.scene("look")
def _(img, T, t, s, e):
    a = win(T, s, e)
    th = wt("hangs", s); tb = wt("bigger", s)
    k = eo((T - th + 0.6) / 0.8)
    body(img, EI, "earth", 520, lerp(1080, 960, k), 360 * (0.8 + 0.2 * k), a=a)
    LIB.place(img, AS, "look_up_back", 300, GY + 8, height=300, a=a)
    kb = on(T, "bigger", s, e, need=2.0)
    if kb > 0:
        body(img, MI, "moon_near", 830, 790, 70, a=a * kb)
        lab(img, "Our Moon", 838, B.TEXT, a * kb, x=815)
    lab(img, "Much bigger", 1200, B.TEXT, a * kb, x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Earth in your sky")
    return R.punch(img, T, tb, amt=0.04)
V.sounds("look", [(0.1, "whoosh", 0.6), (rel("look", "hangs") - 0.4, "whoosh", 0.5), (rel("look", "bigger"), "pop", 0.8)])

@V.scene("hours")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tw = wt("wobbling", s)
    kw = clamp((T - tw + 0.2) / 2.5)
    ang = 2 * math.pi * kw
    ex, ey = 560 + 26 * math.sin(ang), 960 + 9 * math.sin(2 * ang)
    def path(d, P, s_):
        for i in range(24):
            q = 2 * math.pi * i / 24
            px, py = 560 + 26 * math.sin(q), 960 + 9 * math.sin(2 * q)
            d.ellipse([P(px - 4, py - 4), P(px + 4, py + 4)], fill=(246, 196, 84))
    aa(img, (500, 910, 620, 1010), path, a * clamp((T - tw + 0.2) / 0.3) * 0.9)
    body(img, EI, "earth", ex, ey, 300, a=a)
    LIB.place(img, AS, "sit", 300, GY + 8, height=250, a=a)
    hrs = "+1 h" if T < s + 1.9 else ("+6 h" if T < s + 3.7 else "+12 h")      # saltos que se sostienen ≥1,5 s
    lab(img, hrs, 1150, B.TEXT, a, x=760)
    lab(img, "Almost still", 770, B.TEXT, a * on(T, "barely", s, e, need=2.0), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "Hours pass")
V.sounds("hours", [(0.1, "tap", 0.5), (rel("hours", "barely"), "pop", 0.6), (rel("hours", "wobbling"), "whoosh", 0.5)])
V.backdrop("hours")(lambda img, T, t: moonscape(img, T, star_shift=-60 * (T - V.sc["hours"][0])))

@V.scene("lday")
def _(img, T, t, s, e):
    a = win(T, s, e)
    body(img, EI, "earth", 580, 1010, 260, a=a)
    LIB.place(img, AS, "three_quarter", 250, GY + 8, height=270, a=a)
    lab(img, "~29.5 Earth days", 1190, B.TEXT, a * on(T, "about", s, e, need=2.4), x=560)
    lab(img, "Still up", 790, B.TEXT, a * on(T, "still", s, e, need=2.0), x=560)
    R.chrome(img, T)
    title(img, T, s, e, "One lunar day")
    return R.punch(img, T, wt("still", s), amt=0.04)
V.sounds("lday", [(0.1, "whoosh", 0.6), (rel("lday", "about"), "tap", 0.6), (rel("lday", "still"), "pop", 0.8)])
def sun_path(img, T):
    s, e = V.sc["lday"]
    k = 0.75 * clamp((T - s - 0.1) / (e - s - 0.4))
    ang = math.pi * (1 - k)
    item(img, MI, "sun", 540 + 420 * math.cos(ang), 1250 - 470 * math.sin(ang), 120)
V.backdrop("lday")(lambda img, T, t: moonscape(img, T, seed=1, pre=sun_path))

@V.scene("phases")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = clamp((T - wt("phases", s) + 0.2) / 2.2)
    lit = 0.5 + 0.5 * math.cos(2 * math.pi * k)          # llena -> nueva -> llena
    body(img, EI, "earth", 540, 1060, 380, lit=clamp(lit, 0.02, 1.0), a=a)
    lab(img, "Earth phases", 1290, INK_T, a * on(T, "phases", s, e, need=1.8), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Earth has phases")
V.sounds("phases", [(0.1, "whoosh", 0.6), (rel("phases", "phases"), "sparkle", 0.6), (rel("phases", "opposite"), "tap", 0.6)])

@V.scene("full")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k1 = clamp((T - s - 0.1) / 0.3); k2 = on(T, "full", s, e, need=2.0)
    body(img, MI, "moon_near", 300, 1030, 250, lit=0.03, a=a * k1)
    lab(img, "New Moon", 1220, INK_T, a * k1, x=300)
    body(img, EI, "earth", 720, 1030, 280, lit=0.97, a=a * k2)
    lab(img, "Nearly full Earth", 1220, INK_T, a * on(T, "full", s, e, need=2.0), x=700)
    R.chrome(img, T)
    title(img, T, s, e, "Flipped phases")
    return R.punch(img, T, wt("full", s), amt=0.04)
V.sounds("full", [(0.1, "pop", 0.6), (rel("full", "full"), "sparkle", 0.8)])

ORB = (520, 1065, 295)
def orbit_diagram(img, T, ang, a=1.0, marker=1.0):
    cx, cy, r = ORB
    def ring(d, P, s_):
        for i in range(48):
            q0 = 2 * math.pi * i / 48
            if i % 2: continue
            q1 = q0 + 2 * math.pi / 48
            d.line([P(cx + r * math.cos(q0), cy + r * math.sin(q0)), P(cx + r * math.cos(q1), cy + r * math.sin(q1))], fill=(200, 200, 230), width=int(4 * s_))
    aa(img, (cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10), ring, a)
    body(img, EI, "earth", cx, cy + 15, 200, a=a)
    mx, my = cx + r * math.cos(ang), cy + r * math.sin(ang)
    body(img, MI, "moon_near", mx, my, 140, a=a)
    if marker > 0:
        fx, fy = mx - 50 * math.cos(ang), my - 50 * math.sin(ang)         # punto de la cara que mira a la Tierra
        def dot(d, P, s_):
            d.ellipse([P(fx - 13, fy - 13), P(fx + 13, fy + 13)], fill=(232, 64, 80), outline=INK_T, width=int(4 * s_))
        aa(img, (fx - 20, fy - 20, fx + 20, fy + 20), dot, a * marker)

@V.scene("why")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ang = -math.pi / 2 + 0.35 * (T - s)
    orbit_diagram(img, T, ang, a, marker=on(T, "tidally", s, e, need=1.6))
    R.chrome(img, T)
    title(img, T, s, e, "Tidally locked", delay=0.0)
V.sounds("why", [(0.1, "whoosh", 0.6), (rel("why", "tidally"), "pop", 0.8)])
V.backdrop("why")(lambda img, T, t: space_bg(img, T))

@V.scene("lock")
def _(img, T, t, s, e):
    a = win(T, s, e)
    s0 = V.sc["why"][0]
    ang = -math.pi / 2 + 0.35 * (s - s0) + 1.15 * (T - s)
    orbit_diagram(img, T, ang, a)
    ks = on(T, "same", s, e, need=1.6)
    lab(img, "1 spin = 1 orbit", 895, B.TEXT, a * on(T, "once", s, e, need=2.0) * (1 - ks), x=540)
    lab(img, "Same side", 895, B.TEXT, a * ks, x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Spin = orbit")
V.sounds("lock", [(0.1, "whoosh", 0.5), (rel("lock", "once"), "pop", 0.7), (rel("lock", "same"), "tap", 0.6)])
V.backdrop("lock")(lambda img, T, t: space_bg(img, T))

WOW_DUR = 1.3
@V.scene("never")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tn = wt("never", s)
    body(img, EI, "earth", 580, 970 + 5 * math.sin(T * 2), 330, a=a)
    LIB.place(img, AS, "amazed", 300, GY + 8, height=270, a=a)
    R.chrome(img, T)
    kt = clamp((T - (tn + WOW_DUR)) / 0.2)       # el título entra cuando se cierra el momento psicodélico
    R.txt(img, "Never sets", TITLE_Y, "title", B.TEXT, a * kt)
    R.txt(img, "(from most spots)", TITLE_Y + 100, "subtitle", B.TEXT, a * kt)
    return R.punch(img, T, tn, amt=0.05)
def never_bg(img, T, t):
    s = V.sc["never"][0]; tn = wt("never", s)
    moonscape(img, T, seed=2)
    ST.wow_moment(img, T, tn - 0.1, "space", "swirl", dur=WOW_DUR, center=(580, 970))
V.backdrop("never")(never_bg)
V.sounds("never", [(0.1, "tap", 0.5), (rel("never", "never") - 0.1, "sparkle", 0.9), (rel("never", "Send"), "pop", 0.6)])

@V.scene("drift")
def _(img, T, t, s, e):
    a = win(T, s, e)
    td = wt("drifts", s)
    k = eio((T - td) / 3.0)
    mx = lerp(600, 770, k)
    body(img, EI, "earth", 250, 1050, 320, a=a)
    body(img, MI, "moon_near", mx, 1050, 150, a=a)
    arrow_h(img, 620, mx + 80, 1150, a * clamp((T - td) / 0.3) * (1 if mx > 630 else 0))
    lab(img, "+3.8 cm a year", 1240, B.TEXT, a * on(T, "three", s, e, need=2.2), x=560)
    lab(img, "Not to scale", 790, B.TEXT, a * clamp((T - s - 0.3) / 0.3), x=540)
    R.chrome(img, T)
    title(img, T, s, e, "Drifting away")
V.sounds("drift", [(0.1, "whoosh", 0.5), (rel("drift", "drifts"), "whoosh", 0.6), (rel("drift", "three"), "pop", 0.7)])
V.backdrop("drift")(lambda img, T, t: space_bg(img, T, seed=4))

@V.scene("wrap")
def _(img, T, t, s, e):
    a = win(T, s, e + 1)
    xe = 700 if CAT else 560
    body(img, EI, "earth", xe, 960 + 5 * math.sin(T * 2), 300, a=a)
    LIB.place(img, AS, "wave" if T > wt("never", s) else "look_up_back", 790 if CAT else 320, GY + 8, height=260, a=a)
    R.chrome(img, T)
    R.txt(img, "Rise or set?", TITLE_Y, "title", B.TEXT, win(T, s, V.outro_at + 1))
    R.txt(img, "Mostly never.", TITLE_Y + 97, "title", ACC_T, win(T, wt("never", s), V.outro_at + 1))
    return R.punch(img, T, wt("never", s), amt=0.05)
V.sounds("wrap", [(0.05, "whoosh", 0.7), (rel("wrap", "never"), "sparkle", 0.8)])

# ---------- fondos ----------
def card_bg(img, T, t): ST.card(img, CARD)
V.backdrop("hook")(lambda img, T, t: cover_mod.draw_bg(img, "space", 0.05 * T))
V.backdrop("look")(lambda img, T, t: moonscape(img, T))
for n in ("phases", "full"):
    V.backdrop(n)(card_bg)
V.backdrop("wrap")(lambda img, T, t: moonscape(img, T, seed=3))

if __name__ == "__main__":
    V.main()
