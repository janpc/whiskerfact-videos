"""Reel: Who really built the pyramids? Mr. Whiskerfact, categoría History. Voz de Brad.

Fuentes (dos por dato):
- No eran esclavos; ~10.000 trabajadores; turnos rotativos:
  Harvard Magazine (Lehner, 2003) https://www.harvardmagazine.com/2003/07/who-built-the-pyramids-html
  AP/CBS (Hawass, 2010) https://cbsnews.com/news/more-evidence-slaves-didnt-build-pyramids
  Live Science (Redding, AERA, 2013) https://www.livescience.com/28961-ancient-giza-pyramid-builders-camp-unearthed.html
- Pueblo de los constructores con panaderías y barracones; reses, ovejas y cabras sacrificadas a diario:
  Harvard Magazine; Live Science; Ministerio de Turismo y Antigüedades de Egipto https://egymonuments.gov.eg/en/monuments/workers-town-and-cemetery/
- Nombres de cuadrillas ("Friends of Khufu", "Drunks of Menkaure"): Harvard Magazine; Mental Floss https://www.mentalfloss.com/article/541713/examples-ancient-graffiti
- Enterrados en tumbas propias junto a las pirámides, señal de respeto: AP/CBS (Hawass); egymonuments.gov.eg (cementerio de los trabajadores)
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import brand as B
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("history")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "pyramids", [
    ("hook", "Slaves"), ("movie", "For"), ("town", "But"), ("crews", "First"), ("shifts", "Many"),
    ("food", "Second"), ("meat", "Every"), ("gangs", "Third"), ("names", "like"), ("tombs", "Here's"),
    ("honor", "As"), ("wrap", "So"), ("proud", "It")])

SAND, SAND_D, SAND_L = (226, 186, 120), (170, 126, 74), (244, 214, 160)
GROUND = (120, 70, 34)
OCHRE = (214, 84, 52)
SKIN = (196, 140, 96)
CLOTH = (246, 238, 220)

# ---------- dibujo con antialias (2x dentro de una caja) ----------
def aa(img, box, fn, a=1.0):
    if a <= 0.003: return
    x0, y0, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, lambda x, y: ((x - x0) * s, (y - y0) * s), s)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0))

def pyramid(img, x, base_y, w, a=1.0, build=1.0):
    """pirámide de perfil: cara iluminada a la izquierda, sombra a la derecha, hiladas; build la levanta por capas"""
    h = w * 0.62
    def fn(d, P, s):
        top = (x, base_y - h)
        d.polygon([P(x - w / 2, base_y), P(*top), P(x + w * 0.08, base_y)], fill=SAND)
        d.polygon([P(x + w * 0.08, base_y), P(*top), P(x + w / 2, base_y)], fill=SAND_D)
        for k in range(1, 12):
            yy = base_y - h * k / 12; half = w / 2 * (1 - k / 12)
            d.line([P(x - half, yy), P(x + half, yy)], fill=(150, 110, 64), width=max(1, int(1.5 * s)))
        if build < 1:       # tapa la parte aún no construida
            cut = base_y - h * build
            d.rectangle([P(x - w / 2 - 2, base_y - h - 4), P(x + w / 2 + 2, cut)], fill=(0, 0, 0, 0))
    aa(img, (x - w / 2 - 4, base_y - h - 8, x + w / 2 + 4, base_y + 4), fn, a)

def ground(img, y, a=1.0):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle([0, y, W, B.ZONES["caption"][0] - 30], fill=GROUND + (int(110 * a),))
    d.line([(0, y), (W, y)], fill=SAND_L + (int(160 * a),), width=4)
    img.alpha_composite(ov)

def sun(img, x, y, T, a=1.0):
    def fn(d, P, s):
        for i in range(12):
            ang = i * math.pi / 6 + T * 0.3
            d.line([P(x + 80 * math.cos(ang), y + 80 * math.sin(ang)), P(x + 110 * math.cos(ang), y + 110 * math.sin(ang))],
                   fill=(255, 210, 120), width=6 * s)
        d.ellipse([P(x - 60, y - 60), P(x + 60, y + 60)], fill=(255, 196, 90))
    aa(img, (x - 120, y - 120, x + 120, y + 120), fn, a)

def worker(img, x, y, sc=1.0, a=1.0, col=CLOTH, lift=0.0):
    """trabajador esquemático: cabeza, torso con faldellín; lift levanta los brazos (saludo)"""
    def fn(d, P, s):
        d.ellipse([P(x - 14 * sc, y - 92 * sc), P(x + 14 * sc, y - 64 * sc)], fill=SKIN)
        d.rounded_rectangle([P(x - 16 * sc, y - 62 * sc), P(x + 16 * sc, y - 22 * sc)], radius=8 * sc * s, fill=SKIN)
        d.polygon([P(x - 20 * sc, y - 28 * sc), P(x + 20 * sc, y - 28 * sc), P(x + 24 * sc, y + 4 * sc), P(x - 24 * sc, y + 4 * sc)], fill=col)
        for side in (-1, 1):
            ax = x + side * 16 * sc
            hx, hy = ax + side * 12 * sc, lerp(y - 22 * sc, y - 96 * sc, lift if side == 1 else 0)
            d.line([P(ax, y - 56 * sc), P(hx, hy)], fill=SKIN, width=int(9 * sc * s))
            d.line([P(x + side * 9 * sc, y + 2 * sc), P(x + side * 11 * sc, y + 34 * sc)], fill=SKIN, width=int(10 * sc * s))
    aa(img, (x - 50 * sc, y - 110 * sc, x + 50 * sc, y + 42 * sc), fn, a)

def barracks(img, x, y, w, h, a=1.0):
    def fn(d, P, s):
        d.rectangle([P(x, y), P(x + w, y + h)], fill=(196, 150, 96))
        d.rectangle([P(x, y), P(x + w, y + h * 0.22)], fill=(150, 104, 60))
        for k in range(int(w // 46)):
            d.rectangle([P(x + 16 + k * 46, y + h * 0.45), P(x + 32 + k * 46, y + h)], fill=(90, 56, 30))
    aa(img, (x - 2, y - 2, x + w + 2, y + h + 2), fn, a)

def bread(img, x, y, sc=1.0, a=1.0):
    """pan cónico egipcio (molde bedja)"""
    def fn(d, P, s):
        d.polygon([P(x - 34 * sc, y), P(x, y - 110 * sc), P(x + 34 * sc, y)], fill=(214, 152, 78))
        d.polygon([P(x - 10 * sc, y - 40 * sc), P(x, y - 100 * sc), P(x + 4 * sc, y - 40 * sc)], fill=(240, 190, 112))
        d.ellipse([P(x - 36 * sc, y - 10 * sc), P(x + 36 * sc, y + 10 * sc)], fill=(170, 108, 52))
    aa(img, (x - 40 * sc, y - 116 * sc, x + 40 * sc, y + 14 * sc), fn, a)

def animal(img, kind, x, y, sc=1.0, a=1.0):
    """vaca, oveja o cabra de perfil, mirando a la derecha"""
    def fn(d, P, s):
        if kind == "sheep":
            for dx, dy, r in ((-40, 0, 40), (0, -12, 44), (40, 0, 40), (-20, 18, 34), (22, 18, 34)):
                d.ellipse([P(x + (dx - r) * sc, y + (dy - r) * sc), P(x + (dx + r) * sc, y + (dy + r) * sc)], fill=(240, 236, 226))
            body_c, head_c = (240, 236, 226), (60, 52, 50)
        else:
            body_c = (150, 96, 60) if kind == "cow" else (190, 170, 140)
            head_c = (120, 74, 44) if kind == "cow" else (170, 150, 120)
            bw = 70 if kind == "cow" else 52
            d.rounded_rectangle([P(x - bw * sc, y - 34 * sc), P(x + bw * sc, y + 30 * sc)], radius=26 * sc * s, fill=body_c)
        lx = 60 if kind == "cow" else 46
        for k in (-lx + 10, -lx + 34, lx - 34, lx - 10):
            d.line([P(x + k * sc, y + 24 * sc), P(x + k * sc, y + 70 * sc)], fill=head_c, width=int(10 * sc * s))
        hx = x + (88 if kind == "cow" else 72) * sc
        d.ellipse([P(hx - 28 * sc, y - 56 * sc), P(hx + 24 * sc, y - 8 * sc)], fill=head_c)
        if kind == "cow":
            d.line([P(hx - 14 * sc, y - 50 * sc), P(hx - 34 * sc, y - 80 * sc)], fill=(240, 230, 210), width=int(8 * sc * s))
            d.line([P(hx + 8 * sc, y - 52 * sc), P(hx + 22 * sc, y - 84 * sc)], fill=(240, 230, 210), width=int(8 * sc * s))
        if kind == "goat":
            d.arc([P(hx - 30 * sc, y - 96 * sc), P(hx + 10 * sc, y - 40 * sc)], 200, 330, fill=(110, 90, 70), width=int(8 * sc * s))
            d.polygon([P(hx + 2 * sc, y - 10 * sc), P(hx + 14 * sc, y - 10 * sc), P(hx + 6 * sc, y + 16 * sc)], fill=(110, 90, 70))
        d.ellipse([P(hx + 2 * sc, y - 40 * sc), P(hx + 10 * sc, y - 32 * sc)], fill=(20, 16, 14))
    aa(img, (x - 100 * sc, y - 100 * sc, x + 130 * sc, y + 76 * sc), fn, a)

def stone_block(img, x, y, w, h, a=1.0):
    def fn(d, P, s):
        d.polygon([P(x - w / 2, y - h / 2), P(x + w / 2, y - h / 2), P(x + w / 2 + 40, y - h / 2 - 40), P(x - w / 2 + 40, y - h / 2 - 40)], fill=SAND_L)
        d.polygon([P(x + w / 2, y - h / 2), P(x + w / 2 + 40, y - h / 2 - 40), P(x + w / 2 + 40, y + h / 2 - 40), P(x + w / 2, y + h / 2)], fill=SAND_D)
        d.rectangle([P(x - w / 2, y - h / 2), P(x + w / 2, y + h / 2)], fill=SAND)
        rng = np.random.default_rng(3)
        for _ in range(40):
            px, py = rng.uniform(x - w / 2 + 10, x + w / 2 - 10), rng.uniform(y - h / 2 + 10, y + h / 2 - 10)
            d.ellipse([P(px - 3, py - 3), P(px + 3, py + 3)], fill=(200, 160, 100))
    aa(img, (x - w / 2 - 2, y - h / 2 - 44, x + w / 2 + 44, y + h / 2 + 2), fn, a)

def painted(img, text, x, y, k, rot=-3, a=1.0):
    """texto pintado en ocre que aparece de izquierda a derecha como una pincelada"""
    if k <= 0: return
    spr = R.sprite(text, "title", OCHRE)
    spr = spr.resize((int(spr.size[0] * 0.82), int(spr.size[1] * 0.82)), Image.LANCZOS)
    w, h = spr.size
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rectangle([0, 0, int(w * eo(k)), h], fill=255)
    spr2 = Image.new("RGBA", (w, h), (0, 0, 0, 0)); spr2.paste(spr, (0, 0), m)
    spr2 = spr2.rotate(rot, resample=Image.BICUBIC, expand=True)
    R.put(img, spr2, x, y, a, "mm")

def tomb(img, x, base_y, w, a=1.0, rise=1.0):
    """mastaba: tumba de adobe de lados inclinados"""
    h = w * 0.42 * rise
    def fn(d, P, s):
        d.polygon([P(x - w / 2, base_y), P(x - w / 2 + 14, base_y - h), P(x + w / 2 - 14, base_y - h), P(x + w / 2, base_y)], fill=(176, 124, 76))
        d.rectangle([P(x - 10, base_y - h * 0.6), P(x + 10, base_y)], fill=(90, 56, 30))
    aa(img, (x - w / 2 - 2, base_y - w * 0.42 - 4, x + w / 2 + 2, base_y + 2), fn, a)

def glow(img, x, y, r, a):
    if a <= 0: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(6, 0, -1):
        rr = r * k / 6
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 214, 140, int(14 * a)))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(r / 5)))

def title(img, T, s, e, text, color=B.TEXT, y=TITLE_Y, delay=0.0):
    R.txt(img, text, y, "title", color, win(T, s + delay, e))

# ---------- escenas ----------
@V.scene("hook")
def _(img, T, t, s, e):
    sun(img, 820, 860, T, eo(t / 0.6))
    ground(img, 1290)
    pyramid(img, CX - 20, 1290, 760, 1.0, build=0.35 + 0.65 * eo(t / 0.9))
    R.chrome(img, T)
    V.hook_text(img, T, e, "Slaves didn't build the pyramids.", "So who did?", "So")
    R.hook_mascot(img, T, 0.6, e)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.6, "pop", 0.8)])

@V.scene("movie")
def _(img, T, t, s, e):
    a = win(T, s, e)
    def fn(d, P, sc):       # fotograma de película
        d.rounded_rectangle([P(150, 800), P(930, 1300)], radius=20 * sc, fill=(26, 22, 30))
        for k in range(9):
            d.rounded_rectangle([P(176 + k * 86, 816), P(212 + k * 86, 846)], radius=6 * sc, fill=(230, 220, 200))
            d.rounded_rectangle([P(176 + k * 86, 1254), P(212 + k * 86, 1284)], radius=6 * sc, fill=(230, 220, 200))
        d.rectangle([P(190, 866), P(890, 1234)], fill=(70, 52, 40))
    aa(img, (140, 790, 940, 1310), fn, a)
    pyramid(img, 540, 1180, 420, a * 0.8)
    for i in range(7):     # fila de figuras marchando dentro de la película
        x = 230 + ((i * 100 + t * 60) % 700)
        worker(img, x, 1210, 0.8, a * 0.85, col=(150, 140, 130))
    k = eo((T - V.word_time("slaves", after=s) - 0.1) / 0.3)
    if k > 0:
        R.txt(img, "SLAVES?", 1000, "number", (255, 120, 100), a * k, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "The movie version")
V.sounds("movie", [(0.2, "whoosh", 0.6), (V.word_time("slaves", after=V.sc["movie"][0]) - V.sc["movie"][0], "click", 0.7)])

@V.scene("town")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ground(img, 1290, a)
    pyramid(img, 760, 1100, 420, a * 0.9)
    town_t = V.word_time("town") - s
    for i in range(6):   # barracones que aparecen uno a uno
        k = back_out((t - town_t + 0.6 - i * 0.18) / 0.4)
        if k > 0:
            barracks(img, 130 + (i % 3) * 190, 1130 + (i // 3) * 80 - (1 - min(k, 1)) * 40, 170, 60, a * clamp(k))
    for i in range(4):
        worker(img, 220 + i * 150, 1340 - 18 * abs(math.sin(T * 3 + i)), 0.85, a * clamp((t - 1.0) / 0.4))
    R.chrome(img, T)
    title(img, T, s, e, "What they dug up")
    R.txt(img, "the builders' own town", TITLE_Y + 104, "subtitle", ACC_T, win(T, s + town_t, e))
    return R.punch(img, T, s)
V.sounds("town", [(0.0, "whoosh", 0.8)] + [(V.word_time("town") - V.sc["town"][0] - 0.6 + i * 0.36, "pop", 0.5) for i in range(3)])

@V.scene("crews")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tn = V.word_time("ten") - s
    g = eio((t - tn) / 2.2)
    n = int(round(10000 * g / 50) * 50)
    R.txt(img, f"{n:,}", 760, "number", ACC_T, a * clamp((t - tn + 0.3) / 0.3), rise=False)
    R.txt(img, "workers on site at a time", 900, "label", B.TEXT_2, a * clamp((t - tn - 1.4) / 0.4), rise=False)
    shown = int(40 * g)
    for i in range(shown):
        col, row = i % 10, i // 10
        worker(img, 145 + col * 88, 1080 + row * 70, 0.48, a, col=lerpc(CLOTH, (255, 220, 170), (i * 37 % 7) / 7))
    R.chrome(img, T)
    title(img, T, s, e, "1. About 10,000 workers")
V.sounds("crews", [(V.word_time("ten") - V.sc["crews"][0] + k * 0.55, "click", 0.5) for k in range(4)])

@V.scene("shifts")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ground(img, 1290, a)
    pyramid(img, CX, 1180, 460, a * 0.85)
    # equipo que se va (derecha) y equipo nuevo que llega (izquierda)
    home_t = V.word_time("home") - s; fresh_t = V.word_time("fresh") - s
    out_k = eio((t - home_t + 0.3) / 1.6); in_k = eio((t - fresh_t + 0.2) / 1.4)
    for i in range(4):
        worker(img, 400 + i * 90 + out_k * 640, 1340, 0.85, a * (1 - out_k), col=(200, 196, 186))
        worker(img, -260 + i * 90 + in_k * 660, 1340, 0.85, a * clamp(in_k * 3), col=(255, 226, 170))
    R.txt(img, "home  →", 1200, "label", B.TEXT_2, a * clamp((t - home_t) / 0.3) * (1 - out_k * 0.6), x=860, rise=False)
    R.txt(img, "→  new team", 1200, "label", ACC_T, a * clamp((t - fresh_t) / 0.3), x=220, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Crews came in shifts")
V.sounds("shifts", [(V.word_time("home") - V.sc["shifts"][0], "whoosh", 0.7), (V.word_time("fresh") - V.sc["shifts"][0], "whoosh", 0.7)])

@V.scene("food")
def _(img, T, t, s, e):
    a = win(T, s, e)
    bt = V.word_time("bakeries") - s; br = V.word_time("barracks") - s
    for i in range(5):
        k = back_out((t - bt - i * 0.15) / 0.35)
        if k > 0: bread(img, 200 + i * 170, 1020, 1.25 * clamp(k, 0, 1.2), a)
    for i in range(3):
        k = eo((t - br - i * 0.15) / 0.4)
        barracks(img, 140 + i * 280, 1130 + (1 - k) * 40, 240, 80, a * k)
    R.txt(img, "bakeries", 1060, "label", ACC_T, a * clamp((t - bt) / 0.3), rise=False)
    R.txt(img, "barracks", 1240, "label", B.TEXT_2, a * clamp((t - br) / 0.3), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "2. Bread, beds and meat")
V.sounds("food", [(V.word_time("bakeries") - V.sc["food"][0] + i * 0.3, "pop", 0.5) for i in range(2)] +
                  [(V.word_time("barracks") - V.sc["food"][0], "tap", 0.6)])

@V.scene("meat")
def _(img, T, t, s, e):
    a = win(T, s, e)
    for kind, word, x, y in (("cow", "cattle", 270, 1020), ("sheep", "sheep", 780, 1040), ("goat", "goats", 520, 1260)):
        k = back_out((T - V.word_time(word)) / 0.35)
        if k > 0: animal(img, kind, x, y + 4 * math.sin(T * 4 + x), 1.35 * clamp(k, 0, 1.15), a)
    R.txt(img, "every single day", 820, "subtitle", ACC_T, a * clamp((t - 0.4) / 0.3))
    R.chrome(img, T)
    title(img, T, s, e, "Meat on the menu")
V.sounds("meat", [(V.word_time(w) - V.sc["meat"][0], "pop", 0.7) for w in ("cattle", "sheep", "goats")])

@V.scene("gangs")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eo(t / 0.5)
    stone_block(img, CX - 20, 1060 + (1 - k) * 80, 760, 380, a * k)
    nt = V.word_time("names") - s
    for i in range(3):
        worker(img, 260 + i * 260, 1350, 0.9, a * clamp((t - nt) / 0.4 - i * 0.3), lift=0.7 * clamp((t - nt - 0.6) / 0.4))
    R.chrome(img, T)
    title(img, T, s, e, "3. Teams with names")
V.sounds("gangs", [(0.1, "whoosh", 0.7)])

@V.scene("names")
def _(img, T, t, s, e):
    a = win(T, s, e)
    stone_block(img, CX - 20, 1060, 760, 380, a)
    ft = V.word_time("Friends") - s; dt = V.word_time("Drunks") - s
    painted(img, "Friends of Khufu", CX - 20, 970, (t - ft) / 0.8, -3, a)
    painted(img, "Drunks of Menkaure", CX - 20, 1140, (t - dt) / 0.8, 2, a)
    rt = V.word_time("rivalry") - s
    R.txt(img, "VS", 1060, "label", ACC_T, a * clamp((t - rt) / 0.3), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Painted on the blocks")
V.sounds("names", [(V.word_time("Friends") - V.sc["names"][0], "whoosh", 0.6), (V.word_time("Drunks") - V.sc["names"][0], "whoosh", 0.6),
                   (V.word_time("rivalry") - V.sc["names"][0], "click", 0.6)])

@V.scene("tombs")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ground(img, 1290, a)
    sun(img, 860, 840, T, a)
    pyramid(img, 600, 1290, 560, a)
    tt = V.word_time("tombs") - s
    for i, (x, w) in enumerate(((180, 150), (330, 120), (930, 130))):
        tomb(img, x, 1290, w, a, rise=eo((t - tt - 0.5 + i * 0.2) / 0.5))
    glow(img, 255, 1250, 200, a * clamp((t - tt) / 0.4) * (0.7 + 0.3 * math.sin(T * 4)))
    R.chrome(img, T)
    title(img, T, s, e, "Buried beside the pyramids")
    return R.flash(img, T, s, strength=0.35)
V.sounds("tombs", [(0.0, "sparkle", 0.8), (V.word_time("tombs") - V.sc["tombs"][0], "pop", 0.7)])

@V.scene("honor")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ground(img, 1290, a)
    pyramid(img, 600, 1290, 560, a * 0.6)
    for x, w in ((180, 150), (330, 120), (930, 130)): tomb(img, x, 1290, w, a)
    ht = V.word_time("honorably") - s
    glow(img, 330, 1240, 300, a * (0.5 + 0.5 * clamp((t - ht) / 0.3)))
    sc = back_out((t - 0.4) / 0.5)
    if sc > 0:
        def fn(d, P, s2):   # estrella de honor sobre las tumbas
            pts = [P(330 + (60 if k % 2 == 0 else 26) * sc * math.cos(-math.pi / 2 + k * math.pi / 5),
                     1060 + (60 if k % 2 == 0 else 26) * sc * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
            d.polygon(pts, fill=B.GOLD)
        aa(img, (250, 980, 410, 1140), fn, a)
    R.chrome(img, T)
    title(img, T, s, e, "A sign of respect")
    return R.flash(img, T, s + ht, strength=0.3)
V.sounds("honor", [(0.4, "pop", 0.7), (V.word_time("honorably") - V.sc["honor"][0], "sparkle", 0.8)])

def finale(img, T, t, s, e, lift):
    a = win(T, s, e + 1)
    sun(img, 820, 860, T)
    ground(img, 1290)
    pyramid(img, CX - 20, 1290, 760)
    for i in range(5):
        worker(img, 200 + i * 170, 1360 - 10 * abs(math.sin(T * 2.5 + i)), 0.95, a, lift=lift(i))
    R.chrome(img, T)
    R.txt(img, "Now you know:", TITLE_Y, "title", B.TEXT_2, win(T, V.sc["wrap"][0], V.outro_at + 1))
    R.txt(img, "workers, not slaves", TITLE_Y + 97, "title", ACC_T, win(T, V.sc["wrap"][0] + 0.8, V.outro_at + 1))

@V.scene("wrap")
def _(img, T, t, s, e):
    finale(img, T, t, s, e, lambda i: 0.0)
    return R.flash(img, T, V.word_time("know"), strength=0.3)
V.sounds("wrap", [(0.05, "whoosh", 0.8), (V.word_time("know") - V.sc["wrap"][0], "sparkle", 0.7)])

@V.scene("proud")
def _(img, T, t, s, e):
    pt = V.word_time("proud") - s
    finale(img, T, t, s, e, lambda i: eo((t - pt - i * 0.12) / 0.4))
V.sounds("proud", [(V.word_time("proud") - V.sc["proud"][0], "pop", 0.7)])

if __name__ == "__main__":
    V.main()
