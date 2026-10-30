"""Reel: Why do we get goosebumps? Mr. Whiskerfact, categoría Body. Voz de Brad.

Fuentes (dos por dato):
- Un músculo diminuto (arrector pili) por cada pelo; al contraerse levanta el pelo:
  Live Science https://www.livescience.com/32349-what-causes-goose-bumps.html
  WSU Ask Dr. Universe (Ryan Driskell) https://askdruniverse.wsu.edu/2021/03/09/why-do-we-get-goosebumps/
- Lo activa el sistema nervioso simpático, con frío y emociones fuertes:
  Harvard HSCRB (2020) https://hscrb.harvard.edu/news/the-real-reason-behind-goosebumps
  NYSCF https://nyscf.org/resources/why-do-we-get-goosebumps-the-answer-lies-with-the-stem-cells-that-grow-hair/
  Live Science (emociones fuertes); WSU (peligro)
- El pelo erizado atrapa aire caliente junto al cuerpo (aislamiento): Live Science; WSU; NYSCF
- El pelo erizado hace que el animal parezca más grande: Live Science; WSU
- Resto de antepasados más peludos (vestigial): Live Science; WSU
- Harvard 2020 (Cell), en ratones: el mismo nervio conecta con las células madre del folículo; con frío prolongado
  las activa y crece pelo nuevo: Harvard HSCRB / Harvard Gazette https://news.harvard.edu/gazette/?p=309236 ; NYSCF ;
  Shwartz et al., Cell 2020, doi:10.1016/j.cell.2020.06.031
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import brand as B
from reel_lib import Reel, clamp, eo, eio, back_out, lerp, lerpc, win, W, H
from voice_reel import VoiceReel

R = Reel("body")
ACC, ACC_T = R.acc, R.acc_t
TITLE_Y = B.ZONES["title"][0] + 10
CX, CY = B.ILLU_CENTER
V = VoiceReel(R, "goosebumps", [
    ("hook", "Goosebumps"), ("skin", "Under"), ("bump", "When"), ("trigger", "First"), ("nerves", "sympathetic"),
    ("warm", "Second"), ("trap", "raised"), ("bluff", "Third"), ("leftover", "Humans"), ("twist", "Here's"),
    ("reach", "that"), ("cold", "In"), ("wrap", "So"), ("coat", "Your")])

EPI = (226, 150, 132)       # epidermis
DERM = (246, 204, 184)      # dermis
FOLL = (200, 128, 108)      # folículo
HAIR_IN = (92, 58, 40)
HAIR = (250, 228, 196)      # pelo fuera de la piel (claro sobre el fondo oscuro)
MUSCLE = (196, 52, 66)
MUSCLE_HI = (255, 112, 112)
NERVE = (255, 214, 90)
STEM = (110, 226, 150)
FUR = (236, 168, 98)
COLD = (150, 200, 255)
WARM = (255, 170, 80)

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

def seg(d, P, s, pts, col, w):
    """polilínea gruesa con extremos redondeados"""
    d.line([P(*p) for p in pts], fill=col, width=int(w * s), joint="curve")
    for p in (pts[0], pts[-1]):
        x, y = P(*p); r = w * s / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)

def partial(pts, k):
    """los primeros k (0-1) de una polilínea, por longitud"""
    if k <= 0: return []
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(L); goal = tot * clamp(k)
    out = [pts[0]]
    for i, l in enumerate(L):
        if goal >= l: out.append(pts[i + 1]); goal -= l
        else:
            f = goal / l if l else 0
            out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))); break
    return out

def at_len(pts, k):
    p = partial(pts, k); return p[-1] if p else pts[0]

def curve(p0, p1, p2, n=24):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in np.linspace(0, 1, n)]

# ---------- corte de piel: un pelo, su folículo, el músculo arrector pili y el nervio ----------
def section(img, y0, k, a=1.0, mhi=0.0, nerve=0.0, reach=0.0, stem=0.0, glow_stem=0.0, new_hair=0.0, pulse=0.0, T=0.0):
    cx, w = CX, 860
    hx = cx + 70
    ang = math.radians(lerp(50, 12, eio(k)))
    dv = (math.sin(ang), math.cos(ang))                     # hacia dentro de la piel (abajo-derecha)
    bump = 44 * eio(k)
    def surf(x): return y0 - bump * math.exp(-((x - (hx - 40)) / 80) ** 2)
    E = (hx, surf(hx)); Lf = 250
    Bb = (E[0] + Lf * dv[0], E[1] + Lf * dv[1])
    P_m = (E[0] + 0.68 * Lf * dv[0], E[1] + 0.68 * Lf * dv[1])
    A = (hx - 160, surf(hx - 160) + 44)
    M = ((P_m[0] + A[0]) / 2, (P_m[1] + A[1]) / 2)
    nerve_pts = curve((cx + w / 2 - 20, y0 + 270), (hx + 200, y0 + 270), (M[0] + 10, M[1] + 16))
    S = (E[0] + 0.5 * Lf * dv[0] - 34 * dv[1], E[1] + 0.5 * Lf * dv[1] + 34 * dv[0] * 0.2)
    reach_pts = curve(at_len(nerve_pts, 0.55), (S[0] + 120, S[1] + 70), (S[0] + 22, S[1] + 6), 16)
    box = (cx - w / 2 - 10, y0 - 230, cx + w / 2 + 10, y0 + 310)

    def skin(d, P, s):
        xs = np.linspace(cx - w / 2, cx + w / 2, 60)
        top = [(x, surf(x)) for x in xs]
        d.polygon([P(*p) for p in top] + [P(cx + w / 2, y0 + 300), P(cx - w / 2, y0 + 300)], fill=DERM)
        d.polygon([P(*p) for p in top] + [P(x, y + 40) for x, y in top[::-1]], fill=EPI)
        seg(d, P, s, [E, Bb], FOLL, 44)
        x, y = P(*Bb); r = 34 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=FOLL)
        seg(d, P, s, [(E[0] + 6 * dv[0], E[1] + 6 * dv[1]), Bb], HAIR_IN, 9)
        mw = 26 * (1 + 0.45 * eio(k))
        mc = lerpc(MUSCLE, MUSCLE_HI, mhi)
        seg(d, P, s, [A, P_m], mc, mw)
        if nerve > 0: seg(d, P, s, partial(nerve_pts, nerve), NERVE, 8)
        if reach > 0: seg(d, P, s, partial(reach_pts, reach), NERVE, 7)
        if stem > 0:
            for i, (ox, oy) in enumerate(((0, 0), (16, -18), (-14, -16), (18, 14), (-16, 16), (2, 26))):
                r = 11 * clamp(stem * 1.4 - i * 0.08) * s
                col = lerpc(STEM, (230, 255, 230), glow_stem * (0.6 + 0.4 * math.sin(T * 8 + i)))
                x, y = P(S[0] + ox, S[1] + oy); d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        if pulse > 0:
            for j in range(3):
                u = (T * 0.9 + j / 3) % 1
                x, y = P(*at_len(nerve_pts, u)); r = 11 * s
                d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220, int(255 * pulse)))
        if new_hair > 0:
            nd = (math.sin(ang - 0.10), math.cos(ang - 0.10))
            ln = new_hair * (Lf + 170)
            seg(d, P, s, [(Bb[0] - 8, Bb[1]), (Bb[0] - 8 - ln * nd[0], Bb[1] - ln * nd[1])], ACC_T, 8)

    # la piel se recorta en una tarjeta redondeada
    x0, y0b, x1, y1 = [int(v) for v in box]
    s = 2; lay = Image.new("RGBA", ((x1 - x0) * s, (y1 - y0b) * s), (0, 0, 0, 0))
    P = lambda x, y: ((x - x0) * s, (y - y0b) * s)
    skin(ImageDraw.Draw(lay), P, s)
    m = Image.new("L", lay.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([P(cx - w / 2, y0 - 120), P(cx + w / 2, y0 + 300)], radius=44 * s, fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.split()[3]), np.array(m))))
    d = ImageDraw.Draw(lay)
    sway = 2 * math.sin(T * 2.2)
    tip = (E[0] - 190 * math.sin(ang + math.radians(sway)), E[1] - 190 * math.cos(ang + math.radians(sway)))
    seg(d, P, s, [E, tip], HAIR, 9)
    lay = lay.resize((x1 - x0, y1 - y0b), Image.LANCZOS)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (x0, y0b))
    return dict(E=E, A=A, M=M, S=S, Bb=Bb, P_m=P_m, tip=tip)

# ---------- fila de piel con muchos pelos (vista de perfil) ----------
def skin_row(img, y, k, length=130, n=9, a=1.0, col=HAIR, T=0.0, ghost=0.0, warm=0.0, wind=None):
    x0, x1 = 60, 1020
    roots = [x0 + 70 + i * (x1 - x0 - 140) / (n - 1) for i in range(n)]
    def surf(x):
        return y - sum(30 * eio(k) * math.exp(-((x - r + 18) / 34) ** 2) for r in roots)
    def fn(d, P, s):
        xs = np.linspace(x0, x1, 120)
        top = [(xx, surf(xx)) for xx in xs]
        d.polygon([P(*p) for p in top] + [P(x1, B.ZONES["illustration"][1]), P(x0, B.ZONES["illustration"][1])], fill=DERM)
        d.polygon([P(*p) for p in top] + [P(xx, yy + 26) for xx, yy in top[::-1]], fill=EPI)
        if warm > 0:      # aire caliente atrapado entre los pelos
            rng = np.random.default_rng(7)
            for i in range(60):
                px = rng.uniform(x0 + 30, x1 - 30); h = rng.uniform(14, length * 0.8)
                py = surf(px) - h * eio(k) - 6 + 4 * math.sin(T * 3 + i)
                r = 7 * clamp(warm * 2 - i / 60)
                if r > 0: d.ellipse([P(px - r, py - r), P(px + r, py + r)], fill=WARM + (200,))
        for i, r in enumerate(roots):
            ang = math.radians(lerp(70, 12, eio(k)) + 3 * math.sin(T * 2 + i))
            ln = length + ghost * 200
            E = (r, surf(r))
            tip = (r - ln * math.sin(ang), E[1] - ln * math.cos(ang))
            if ghost > 0:
                seg(d, P, s, [E, tip], col + (int(255 * (1 - 0.45 * ghost)),), 7 + 6 * ghost)
            else:
                seg(d, P, s, [E, tip], col, 7)
    aa(img, (x0 - 6, y - length - 230, x1 + 6, B.ZONES["illustration"][1]), fn, a)
    if wind is not None:   # rachas de aire frío que pasan a ras de piel o por encima del pelo
        def wf(d, P, s):
            for j in range(4):
                u = (wind * 0.8 + j / 4) % 1
                xx = lerp(1100, -200, u); yy = lerp(y - 20, y - length - 60, eio(k)) - j % 2 * 34
                d.line([P(xx, yy), P(xx + 150, yy)], fill=COLD + (210,), width=6 * s)
                d.polygon([P(xx - 18, yy), P(xx + 4, yy - 12), P(xx + 4, yy + 12)], fill=COLD + (210,))
        aa(img, (0, y - length - 160, W, y + 10), wf, a)

def flake(img, x, y, r, a=1.0, rot=0.0):
    def fn(d, P, s):
        for i in range(3):
            an = rot + i * math.pi / 3
            dx, dy = r * math.cos(an), r * math.sin(an)
            d.line([P(x - dx, y - dy), P(x + dx, y + dy)], fill=COLD, width=int(6 * s))
            for sg in (-1, 1):
                bx, by = x + sg * dx * 0.55, y + sg * dy * 0.55
                for t2 in (-0.6, 0.6):
                    d.line([P(bx, by), P(bx + sg * r * 0.3 * math.cos(an + t2), by + sg * r * 0.3 * math.sin(an + t2))], fill=COLD, width=int(5 * s))
    aa(img, (x - r - 6, y - r - 6, x + r + 6, y + r + 6), fn, a)

def heart(img, x, y, r, a=1.0):
    def fn(d, P, s):
        d.ellipse([P(x - r, y - r * 0.7), P(x, y + r * 0.3)], fill=(255, 92, 120))
        d.ellipse([P(x, y - r * 0.7), P(x + r, y + r * 0.3)], fill=(255, 92, 120))
        d.polygon([P(x - r * 0.96, y - 0.05 * r), P(x + r * 0.96, y - 0.05 * r), P(x, y + r)], fill=(255, 92, 120))
    aa(img, (x - r - 4, y - r - 4, x + r + 4, y + r + 4), fn, a)

def cat(img, cx, cy, sc=1.0, puff=0.0, a=1.0, T=0.0):
    """gato de perfil mirando a la derecha; puff eriza el pelo y arquea el lomo"""
    def fn(d, P, s):
        arch = 50 * puff
        # cola
        tail = curve((cx - 150 * sc, cy - 10 * sc), (cx - 260 * sc, cy - 60 * sc), (cx - 220 * sc, cy - (170 + 40 * puff) * sc))
        seg(d, P, s, tail, FUR, (24 + 30 * puff) * sc)
        if puff > 0:
            for i, p in enumerate(tail[::2]):
                for sg in (-1, 1):
                    d.line([P(*p), P(p[0] + sg * 26 * puff * sc, p[1] - 10 * sc)], fill=FUR, width=int(8 * s))
        # patas
        for lx in (-110, -70, 80, 120):
            d.line([P(cx + lx * sc, cy), P(cx + lx * sc, cy + 130 * sc)], fill=FUR, width=int(22 * sc * s))
        # cuerpo con lomo arqueado
        d.ellipse([P(cx - 170 * sc, cy - (75 + arch) * sc), P(cx + 170 * sc, cy + 55 * sc)], fill=FUR)
        if puff > 0:
            for i in range(26):
                an = math.pi + i * math.pi / 25
                bx, by = cx + 170 * sc * math.cos(an), cy - 10 * sc + (65 + arch) * sc * math.sin(an)
                ln = (22 + 10 * math.sin(i * 1.7 + T * 6)) * puff * sc
                d.polygon([P(bx - 9 * sc * math.sin(an), by + 9 * sc * math.cos(an)), P(bx + 9 * sc * math.sin(an), by - 9 * sc * math.cos(an)),
                           P(bx + ln * math.cos(an), by + ln * math.sin(an))], fill=FUR)
        # cabeza
        hx, hy = cx + 190 * sc, cy - (70 + arch * 0.4) * sc
        for ex in (-34, 22):
            d.polygon([P(hx + ex * sc, hy - 40 * sc), P(hx + (ex + 12) * sc, hy - (100 + 10 * puff) * sc), P(hx + (ex + 34) * sc, hy - 44 * sc)], fill=FUR)
        d.ellipse([P(hx - 64 * sc, hy - 62 * sc), P(hx + 64 * sc, hy + 58 * sc)], fill=FUR)
        d.ellipse([P(hx + 14 * sc, hy - 20 * sc), P(hx + 32 * sc, hy + (0 + 6 * puff) * sc)], fill=(30, 26, 22))
        d.line([P(hx + 40 * sc, hy + 26 * sc), P(hx + 62 * sc, hy + 30 * sc)], fill=(120, 70, 40), width=int(4 * s))
    aa(img, (cx - 320 * sc, cy - 300 * sc, cx + 280 * sc, cy + 150 * sc), fn, a)

def person(img, x, y, fur=0.0, a=1.0, col=(226, 170, 140), fur_col=(150, 98, 58)):
    """figura sencilla de pie; fur añade pelo por todo el contorno"""
    def fn(d, P, s):
        if fur > 0:
            rng = np.random.default_rng(int(x))
            for i in range(140):
                if i < 50:
                    an = rng.uniform(0, 2 * math.pi); bx, by = x + 50 * math.cos(an), y - 270 + 50 * math.sin(an)
                    dx, dy = math.cos(an), math.sin(an)
                else:
                    by = rng.uniform(y - 215, y - 10); sg = rng.choice((-1, 1))
                    bx = x + sg * (66 if by < y - 110 else 44); dx, dy = sg, 0.2
                ln = 26 * fur
                d.line([P(bx, by), P(bx + dx * ln, by + dy * ln)], fill=fur_col, width=int(6 * s))
        d.ellipse([P(x - 48, y - 318), P(x + 48, y - 222)], fill=col)
        d.rounded_rectangle([P(x - 62, y - 214), P(x + 62, y - 100)], radius=28 * s, fill=col)
        for sg in (-1, 1):
            d.line([P(x + sg * 30, y - 104), P(x + sg * 40, y)], fill=col, width=int(28 * s))
            d.line([P(x + sg * 62, y - 200), P(x + sg * 84, y - 104)], fill=col, width=int(22 * s))
    aa(img, (x - 130, y - 360, x + 130, y + 30), fn, a)

def mouse(img, x, y, sc=1.0, a=1.0, T=0.0):
    def fn(d, P, s):
        tail = curve((x - 110 * sc, y + 10 * sc), (x - 230 * sc, y + 70 * sc), (x - 260 * sc, y - 40 * sc + 14 * math.sin(T * 3) * sc))
        seg(d, P, s, tail, (236, 170, 170), 8 * sc)
        d.ellipse([P(x - 130 * sc, y - 70 * sc), P(x + 90 * sc, y + 50 * sc)], fill=(206, 206, 218))
        d.ellipse([P(x + 50 * sc, y - 80 * sc), P(x + 170 * sc, y + 20 * sc)], fill=(206, 206, 218))
        d.ellipse([P(x + 40 * sc, y - 130 * sc), P(x + 110 * sc, y - 60 * sc)], fill=(236, 170, 170))
        d.ellipse([P(x + 120 * sc, y - 50 * sc), P(x + 136 * sc, y - 34 * sc)], fill=(30, 26, 30))
        d.ellipse([P(x + 160 * sc, y - 20 * sc), P(x + 178 * sc, y - 2 * sc)], fill=(236, 140, 150))
        for k2 in (-1, 1):
            d.line([P(x + 170 * sc, y - 10 * sc), P(x + 230 * sc, y - 10 * sc + k2 * 18 * sc)], fill=(230, 230, 236), width=int(3 * s))
    aa(img, (x - 280 * sc, y - 140 * sc, x + 240 * sc, y + 80 * sc), fn, a)

def leader(img, p0, p1, a, col=B.TEXT_2):
    def fn(d, P, s): d.line([P(*p0), P(*p1)], fill=col, width=int(3 * s))
    aa(img, (min(p0[0], p1[0]) - 4, min(p0[1], p1[1]) - 4, max(p0[0], p1[0]) + 4, max(p0[1], p1[1]) + 4), fn, a)

def title(img, T, s, e, text, color=B.TEXT, y=TITLE_Y, delay=0.0):
    R.txt(img, text, y, "title", color, win(T, s + delay, e))

def wt(word, s): return V.word_time(word, after=s)

# ---------- escenas ----------
@V.scene("hook")
def _(img, T, t, s, e):
    k = eio((t - 0.7) / 0.7)
    skin_row(img, 1210, k, 130, T=T)
    R.chrome(img, T)
    fade = clamp((e - T) / B.EXIT)
    l1 = "Goosebumps evolved for fur."
    R.txt(img, l1, TITLE_Y, "hook", B.TEXT, fade, rise=False)
    R.txt(img, "So why do we get them?", TITLE_Y + R.sprite(l1, "hook", B.TEXT).size[1] - 4, "hook", ACC_T,
          fade * clamp((T - V.word_time("So") + 0.1) / 0.2), rise=False)
    R.hook_mascot(img, T, 0.6, e)
    return R.punch(img, T, 0.7)
V.sounds("hook", [(0.0, "whoosh", 0.7), (0.6, "pop", 0.8), (0.75, "whoosh", 0.6)])

@V.scene("skin")
def _(img, T, t, s, e):
    a = win(T, s, e)
    at = wt("arrector", s)
    g = section(img, 1000, 0.0, a, mhi=clamp((T - at) / 0.3) * (0.6 + 0.4 * math.sin(T * 6)), T=T)
    la = a * clamp((T - at) / 0.3)
    R.txt(img, "arrector pili", 800, "label", ACC_T, la, x=250, rise=False)
    leader(img, (250, 852), g["M"], la, ACC_T)
    R.txt(img, "skin", 1000 - 100, "label", B.TEXT_2, a * clamp((t - 0.6) / 0.3), x=880, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "One tiny muscle per hair")
V.sounds("skin", [(0.15, "whoosh", 0.6), (V.word_time("arrector") - V.sc["skin"][0], "click", 0.7)])

@V.scene("bump")
def _(img, T, t, s, e):
    a = win(T, s, e)
    tt = wt("tightens", s); bt = wt("bumps", s)
    k = eio((T - tt) / 1.4)
    g = section(img, 1000, k, a, mhi=clamp((T - tt) / 0.3), T=T)
    la = a * clamp((T - bt) / 0.25)
    R.txt(img, "goosebump!", 860, "label", ACC_T, la, x=300, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Muscle pulls, hair stands")
    return R.punch(img, T, bt)
V.sounds("bump", [(V.word_time("tightens") - V.sc["bump"][0], "whoosh", 0.7), (V.word_time("bumps") - V.sc["bump"][0], "pop", 0.8)])

@V.scene("trigger")
def _(img, T, t, s, e):
    a = win(T, s, e)
    nt = wt("wired", s) - 0.6
    nk = eo((T - nt) / 1.2)
    section(img, 1000, 0.0, a, nerve=nk, T=T)
    R.txt(img, "nerve", 900, "label", NERVE, a * clamp((T - nt - 0.6) / 0.3), x=880, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "1. The trigger")
V.sounds("trigger", [(V.word_time("wired") - V.sc["trigger"][0] - 0.6, "whoosh", 0.6)])

@V.scene("nerves")
def _(img, T, t, s, e):
    a = win(T, s, e)
    ct = wt("cold", s); et = wt("emotions", s); at_ = wt("autopilot", s)
    k = eio((T - ct - 0.2) / 0.8)
    section(img, 1020, k, a, nerve=1.0, pulse=clamp((T - ct) / 0.3), mhi=k, T=T)
    fk = back_out((T - ct) / 0.35); hk = back_out((T - et) / 0.35)
    if fk > 0: flake(img, 210, 860, 62 * clamp(fk, 0, 1.2), a, rot=T * 0.8)
    if hk > 0: heart(img, 880, 860, 58 * clamp(hk, 0, 1.2), a)
    R.chrome(img, T)
    title(img, T, s, e, "Sympathetic nervous system")
    R.txt(img, "your body's autopilot", 620, "subtitle", ACC_T, win(T, at_, e))
    return R.flash(img, T, et, strength=0.3)
V.sounds("nerves", [(V.word_time("autopilot") - V.sc["nerves"][0], "tap", 0.6), (V.word_time("cold", after=V.sc["nerves"][0]) - V.sc["nerves"][0], "pop", 0.7),
                    (V.word_time("emotions") - V.sc["nerves"][0], "sparkle", 0.7)])

@V.scene("warm")
def _(img, T, t, s, e):
    a = win(T, s, e)
    skin_row(img, 1290, 0.0, 190, 14, a, FUR, T=T, wind=T)
    R.txt(img, "cold air slips in", 860, "label", COLD, a * clamp((t - 0.8) / 0.3), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "2. The warmth")
V.sounds("warm", [(0.2, "whoosh", 0.5), (1.4, "whoosh", 0.4)])

@V.scene("trap")
def _(img, T, t, s, e):
    a = win(T, s, e)
    k = eio((t - 0.1) / 0.6)
    tt = wt("traps", s); jt = wt("jacket", s)
    skin_row(img, 1290, k, 190, 14, a, FUR, T=T, warm=clamp((T - tt) / 1.2), wind=T)
    R.txt(img, "warm air, trapped", 820, "label", WARM, a * clamp((T - tt) / 0.3), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "2. The warmth")
    R.txt(img, "like a puffy jacket", 620, "subtitle", ACC_T, win(T, jt, e))
    return R.punch(img, T, s + 0.1)
V.sounds("trap", [(0.1, "whoosh", 0.7), (V.word_time("traps") - V.sc["trap"][0], "bubble", 0.6), (V.word_time("jacket") - V.sc["trap"][0], "pop", 0.6)])

@V.scene("bluff")
def _(img, T, t, s, e):
    a = win(T, s, e)
    pt = wt("puffs", s); bt = wt("bigger", s)
    puff = eo((T - pt) / 0.5)
    sc = 0.95 + 0.25 * back_out((T - bt) / 0.4)
    cat(img, 500, 1180, sc, puff, a, T)
    R.txt(img, "bigger and tougher", 760, "label", ACC_T, a * clamp((T - bt) / 0.3), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "3. The bluff")
    return R.punch(img, T, bt)
V.sounds("bluff", [(0.1, "pop", 0.6), (V.word_time("puffs") - V.sc["bluff"][0], "whoosh", 0.7), (V.word_time("bigger") - V.sc["bluff"][0], "pop", 0.8)])

@V.scene("leftover")
def _(img, T, t, s, e):
    a = win(T, s, e)
    lt = wt("lost", s); ft = wt("leftover", s); at_ = wt("ancestors", s)
    person(img, 290, 1330, 1.0, a * clamp((t - 0.2) / 0.4))
    person(img, 790, 1330, 0.0, a * clamp((T - lt) / 0.4))
    ak = eo((T - lt) / 0.6)
    if ak > 0:
        leader(img, (430, 1150), (430 + 220 * ak, 1150), a, ACC_T)
        if ak > 0.9:
            def fn(d, P, s2): d.polygon([P(650, 1150), P(624, 1134), P(624, 1166)], fill=ACC_T)
            aa(img, (620, 1130, 656, 1170), fn, a)
    R.txt(img, "hairy ancestors", 930, "label", B.TEXT_2, a * clamp((T - at_) / 0.3), x=290, rise=False)
    R.txt(img, "us", 930, "label", B.TEXT_2, a * clamp((T - lt) / 0.3), x=790, rise=False)
    R.txt(img, "a leftover", 770, "number", ACC_T, a * clamp((T - ft) / 0.25), rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "We lost the fur")
    return R.punch(img, T, ft)
V.sounds("leftover", [(0.2, "pop", 0.6), (V.word_time("lost") - V.sc["leftover"][0], "whoosh", 0.6), (V.word_time("leftover") - V.sc["leftover"][0], "click", 0.8)])

@V.scene("twist")
def _(img, T, t, s, e):
    a = win(T, s, e)
    yt = wt("twenty", s); ht = wt("Harvard", s); mt = wt("mice", s)
    R.txt(img, "2020", 760, "number", ACC_T, a * clamp((T - yt) / 0.3), rise=False)
    R.txt(img, "Harvard study", 900, "label", B.TEXT_2, a * clamp((T - ht) / 0.3), rise=False)
    mk = back_out((T - mt + 0.6) / 0.4)
    if mk > 0: mouse(img, 560, 1200, 1.3 * clamp(mk, 0, 1.15), a, T)
    R.chrome(img, T)
    title(img, T, s, e, "The twist")
    return R.flash(img, T, s, strength=0.35)
V.sounds("twist", [(0.0, "sparkle", 0.8), (V.word_time("twenty") - V.sc["twist"][0], "click", 0.7), (V.word_time("mice") - V.sc["twist"][0] - 0.6, "pop", 0.7)])

@V.scene("reach")
def _(img, T, t, s, e):
    a = win(T, s, e)
    rt = wt("reaches", s); st = wt("stem", s); ft = wt("follicle", s)
    g = section(img, 1000, 0.25, a, nerve=1.0, reach=eo((T - rt) / 0.8), stem=eo((T - st) / 0.4), pulse=0.6, T=T)
    la = a * clamp((T - st) / 0.3)
    R.txt(img, "stem cells", 800, "label", STEM, la, x=250, rise=False)
    leader(img, (250, 852), g["S"], la, STEM)
    lf = a * clamp((T - ft) / 0.3)
    R.txt(img, "hair follicle", 800, "label", B.TEXT_2, lf, x=840, rise=False)
    leader(img, (840, 850), ((g["E"][0] + g["Bb"][0]) / 2 + 20, (g["E"][1] + g["Bb"][1]) / 2), lf)
    R.chrome(img, T)
    title(img, T, s, e, "Same nerve, new target")
V.sounds("reach", [(V.word_time("reaches") - V.sc["reach"][0], "whoosh", 0.6), (V.word_time("stem") - V.sc["reach"][0], "pop", 0.7),
                   (V.word_time("follicle") - V.sc["reach"][0], "tap", 0.5)])

@V.scene("cold")
def _(img, T, t, s, e):
    a = win(T, s, e)
    wk = wt("wakes", s); nt = wt("new", s)
    section(img, 1000, 0.6, a, nerve=1.0, reach=1.0, stem=1.0, glow_stem=clamp((T - wk) / 0.3), new_hair=eo((T - nt) / 1.1), pulse=1.0, T=T)
    rng = np.random.default_rng(5)
    for i in range(9):
        x = rng.uniform(120, 960); sp = rng.uniform(80, 140)
        y = 760 + ((t * sp + rng.uniform(0, 560)) % 560)
        flake(img, x, y, rng.uniform(18, 30), a * 0.8, rot=T + i)
    R.txt(img, "new hair", 800, "label", ACC_T, a * clamp((T - nt - 0.6) / 0.3), x=860, rise=False)
    R.chrome(img, T)
    title(img, T, s, e, "Cold wakes them up")
    return R.punch(img, T, wk)
V.sounds("cold", [(0.1, "sparkle", 0.6), (V.word_time("wakes") - V.sc["cold"][0], "whoosh", 0.7), (V.word_time("new") - V.sc["cold"][0], "pop", 0.7)])

def finale(img, T, ghost=0.0):
    skin_row(img, 1240, 1.0, 130, col=lerpc(HAIR, FUR, ghost), T=T, ghost=ghost)
    R.chrome(img, T)
    R.txt(img, "Now you know:", TITLE_Y, "title", B.TEXT_2, win(T, V.sc["wrap"][0], V.outro_at + 1))
    R.txt(img, "a reflex built for fur", TITLE_Y + 97, "title", ACC_T, win(T, V.sc["wrap"][0] + 0.8, V.outro_at + 1))

@V.scene("wrap")
def _(img, T, t, s, e):
    finale(img, T)
    return R.flash(img, T, V.word_time("know"), strength=0.3)
V.sounds("wrap", [(0.05, "whoosh", 0.8), (V.word_time("know") - V.sc["wrap"][0], "sparkle", 0.7)])

@V.scene("coat")
def _(img, T, t, s, e):
    ft = wt("fluffing", s); lt = wt("lost", s)
    g = eo((T - ft) / 0.7) * (1 - eio((T - lt) / 0.8))
    finale(img, T, ghost=g)
V.sounds("coat", [(V.word_time("fluffing") - V.sc["coat"][0], "whoosh", 0.7), (V.word_time("lost", after=V.sc["coat"][0]) - V.sc["coat"][0], "pop", 0.5)])

if __name__ == "__main__":
    V.main()
