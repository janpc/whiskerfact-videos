"""Estilo visual de Mr. Whiskerfact, inspirado en el videoclip de la autora («Daxter - Hold Me Now»).

Lo que se toma del videoclip (adaptado, no copiado):
- ilustración plana con CONTORNO fino y oscuro en figuras y objetos;
- paisajes en CAPAS de siluetas (bosques, colinas) con cielos en degradado de atardecer o noche estrellada;
- fondos crema cálidos para escenas «de cerca» (manos, objetos, esquemas);
- momentos PSICODÉLICOS (remolino ondulado, manchas líquidas, mosaico glitch) para el giro o el dato sorprendente;
- siluetas de color con brillo dentro de esos momentos.
Lo que NO se toma: el ritmo lento. Aquí todo se mueve siempre (deriva, parallax, pulso) y cada momento psicodélico dura 1-2 s.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import brand as B

W, H = B.W, B.H
OUTLINE = (44, 32, 30)          # contorno: marrón casi negro, no negro puro
OUTLINE_W = 4                   # px a 1080 de ancho
CREAM = (233, 226, 190)         # fondo crema del videoclip
NIGHT = (44, 42, 120)           # azul noche con estrellas
SUNSET = [(70, 52, 120), (196, 96, 130), (246, 176, 96), (250, 214, 120)]   # violeta -> rosa -> naranja -> amarillo
FOREST = [(30, 70, 52), (24, 60, 44), (18, 48, 36), (12, 36, 28)]          # verdes de lejos (claro) a cerca (oscuro)
GROUND = (40, 44, 30)           # suelo oscuro

def mix(c1, c2, k): return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))

def cat_palette(cat):
    """paleta psicodélica de 6 tonos derivada del color de la categoría (rueda alrededor de su tono)"""
    import colorsys
    r, g, b = [v / 255 for v in B.CATEGORIES[cat]["color"]]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    out = []
    for dh, dl in ((0, 0), (0.1, 0.12), (-0.1, -0.08), (0.45, 0.06), (0.2, 0.18), (-0.22, -0.02)):
        rr, gg, bb = colorsys.hls_to_rgb((h + dh) % 1, min(0.78, max(0.32, 0.55 + dl)), min(0.62, s * 0.6))   # tonos apagados, tipo pastel
        out.append((int(rr * 255), int(gg * 255), int(bb * 255)))
    return out

# ---------- cielos y paisajes en capas ----------
def sky(img, top, bottom, y0=0, y1=H):
    arr = np.linspace(0, 1, y1 - y0)[:, None, None]
    grad = (np.array(top) * (1 - arr) + np.array(bottom) * arr) * np.ones((1, W, 1))
    img.paste(Image.fromarray(grad.astype(np.uint8)), (0, y0))

def sunset_sky(img, y0=0, y1=1400):
    n = len(SUNSET) - 1; h = (y1 - y0) // n
    for i in range(n): sky(img, SUNSET[i], SUNSET[i + 1], y0 + i * h, y0 + (i + 1) * h if i < n - 1 else y1)

def stars(img, T, n=60, seed=3, y1=1100, a=1.0):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y, r, ph = rng.uniform(0, W), rng.uniform(0, y1), rng.uniform(1.5, 4), rng.uniform(0, 6.3)
        k = (0.55 + 0.45 * math.sin(T * 2.2 + ph)) * a
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix(NIGHT, (255, 255, 245), k))

def treeline(img, base_y, height, color, T=0.0, speed=0.0, seed=1, bumps=9):
    """fila de copas frondosas en silueta: racimos de círculos con borde irregular (como los bosques del videoclip),
    con deriva horizontal para el parallax"""
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    period = W + 400
    shift = (T * speed) % period
    trees = [(rng.uniform(0, period), rng.uniform(0.75, 1.0) * height, rng.uniform(0.8, 1.2)) for _ in range(bumps * 2)]
    d.rectangle([0, base_y - height * 0.35, W, base_y + 400], fill=color)
    for x0, h, wk in trees:
        x = (x0 - shift) % period - 200
        r = h * 0.32 * wk
        for k in range(7):                      # copa: racimo de círculos
            ang = k / 7 * math.pi
            cx = x + math.cos(ang) * r * 0.9 + rng.uniform(-8, 8)
            cy = base_y - h * 0.55 - math.sin(ang) * r * 0.7 + rng.uniform(-8, 8)
            rr = r * rng.uniform(0.55, 0.8)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color)
        d.ellipse([x - r, base_y - h * 0.55 - r * 0.6, x + r, base_y - h * 0.55 + r * 1.2], fill=color)

def hills(img, base_y, amp, color, phase=0.0):
    pts = [(x, base_y - amp * (0.5 + 0.5 * math.sin(x / 260 + phase))) for x in range(-20, W + 40, 20)]
    ImageDraw.Draw(img).polygon(pts + [(W + 40, H), (-20, H)], fill=color)

# cielos y terrenos para VARIAR: el videoclip es una referencia, no una plantilla
SKIES = {
    "sunset": SUNSET,
    "dawn":   [(64, 84, 150), (150, 140, 190), (240, 180, 170), (252, 222, 170)],
    "dusk":   [(30, 36, 90), (96, 60, 130), (200, 100, 120), (236, 150, 110)],
    "day":    [(70, 140, 210), (120, 180, 230), (180, 216, 240), (220, 236, 246)],
    "storm":  [(40, 44, 60), (70, 76, 96), (110, 116, 130), (150, 150, 160)],
}
TERRAINS = {   # 3 capas de lejos a cerca
    "forest": FOREST,
    "pines":  [(36, 76, 70), (28, 62, 58), (20, 48, 46), (14, 36, 34)],
    "autumn": [(150, 80, 50), (120, 60, 40), (90, 44, 30), (60, 30, 22)],
    "hills":  [(80, 110, 70), (60, 90, 56), (44, 70, 42), (30, 52, 30)],
    "dunes":  [(214, 160, 100), (196, 140, 84), (170, 116, 66), (130, 86, 48)],
    "waves":  [(60, 120, 170), (44, 100, 150), (30, 80, 128), (20, 60, 100)],
    "city":   [(70, 64, 100), (54, 50, 84), (40, 36, 66), (28, 26, 48)],
}

def dunes(img, base_y, amp, color, T=0.0, speed=0.0, seed=1, waves=False):
    """colinas suaves / dunas / olas en silueta con deriva para el parallax"""
    rng = np.random.default_rng(seed); ph = rng.uniform(0, 6.3); f = rng.uniform(180, 300) if not waves else 90
    sh = T * speed
    pts = [(x, base_y - amp * (0.5 + 0.5 * math.sin((x + sh) / f + ph)) - (amp * 0.25 * math.sin((x + sh) / (f * 0.45) + ph * 2) if not waves else 0))
           for x in range(-20, W + 40, 12)]
    ImageDraw.Draw(img).polygon(pts + [(W + 40, H), (-20, H)], fill=color)

def skyline(img, base_y, height, color, T=0.0, speed=0.0, seed=1):
    """edificios en silueta (ciudad)"""
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(img); period = W + 300; sh = (T * speed) % period
    x = 0
    while x < period:
        w = rng.uniform(50, 130); h = rng.uniform(0.35, 1.0) * height
        xx = (x - sh) % period - 150
        d.rectangle([xx, base_y - h, xx + w - 6, base_y + 400], fill=color)
        x += w

def landscape(img, T, night=False, ground_y=1330, sky_kind=None, terrain="forest", seed=0):
    """paisaje completo en capas: cielo, 3 capas de terreno con parallax y suelo oscuro.
    sky_kind: sunset | dawn | dusk | day | storm (por defecto sunset, o noche si night=True)
    terrain: forest | pines | autumn | hills | dunes | waves | city. seed cambia la forma de las capas."""
    if night:
        sky(img, (24, 22, 70), NIGHT, 0, ground_y); stars(img, T, y1=ground_y - 300, seed=3 + seed)
    else:
        pal = SKIES[sky_kind or "sunset"]; n = len(pal) - 1; h = ground_y // n
        for i in range(n): sky(img, pal[i], pal[i + 1], i * h, (i + 1) * h if i < n - 1 else ground_y)
    cols = TERRAINS[terrain]
    for i, (c, hh, sp) in enumerate(zip(cols, (300, 240, 190), (6, 12, 22))):
        by = ground_y - 120 + i * 60
        if terrain in ("forest", "autumn"): treeline(img, by, hh, c, T, sp, seed=i + 2 + seed)
        elif terrain == "pines": treeline(img, by, hh * 1.2, c, T, sp, seed=i + 7 + seed, bumps=14)
        elif terrain == "city": skyline(img, by, hh * 1.3, c, T, sp, seed=i + seed)
        else: dunes(img, by, hh * (0.5 if terrain != "waves" else 0.25), c, T, sp * (4 if terrain == "waves" else 1), seed=i + seed, waves=terrain == "waves")
    ImageDraw.Draw(img).rectangle([0, ground_y, W, H], fill=cols[3] if terrain == "waves" else GROUND)   # base oscura: los subtítulos se leen encima

# ---------- momentos psicodélicos (para el giro / el dato sorprendente) ----------
def swirl(T, cat, size=(W, H), cx=0.5, cy=0.5, bands=5, speed=0.9):
    """espiral de bandas de color que gira con suavidad (el remolino del videoclip, con la paleta de la categoría)"""
    pal = np.array(cat_palette(cat), dtype=np.float32)
    w, h = size[0] // 2, size[1] // 2                       # a media resolución y escalado bilineal: bordes limpios
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx / w - cx, (yy / h - cy) * h / w
    r = np.sqrt(dx * dx + dy * dy); ang = np.arctan2(dy, dx)
    v = r * bands * 2 + 0.12 * np.sin(ang * 5 + T * 1.5) - T * speed + ang / (2 * math.pi) * len(pal)   # sin costura
    idx = np.floor(v).astype(int) % len(pal)
    return Image.fromarray(pal[idx].astype(np.uint8)).resize(size, Image.BILINEAR).convert("RGBA")

def blobs(T, cat, size=(W, H), scale=3.0):
    """manchas líquidas tipo camuflaje que fluyen (las «manchas» del videoclip)"""
    pal = np.array(cat_palette(cat), dtype=np.float32)
    w, h = size[0] // 2, size[1] // 2                       # a media resolución: bordes limpios
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) / w * scale
    f = (np.sin(xx * 2.1 + T * 0.9) + np.sin(yy * 1.7 - T * 0.7) + np.sin((xx + yy) * 1.3 + T * 1.1)
         + np.sin(np.sqrt(xx * xx + yy * yy) * 2.5 - T * 1.3))
    idx = np.floor((f + 4) / 8 * len(pal) * 1.5).astype(int) % len(pal)
    return Image.fromarray(pal[idx].astype(np.uint8)).resize(size, Image.NEAREST).filter(ImageFilter.SMOOTH_MORE).convert("RGBA")

def glitch(T, cat, size=(W, H), seed=0):
    """mosaico de rectángulos de color que cambia a saltos (12 veces por segundo)"""
    pal = cat_palette(cat); step = int(T * 12)
    rng = np.random.default_rng(seed * 1000 + step)
    im = Image.new("RGBA", size, pal[0] + (255,)); d = ImageDraw.Draw(im)
    for _ in range(70):
        x, y = rng.uniform(0, size[0]), rng.uniform(0, size[1])
        w, h = rng.uniform(40, 260), rng.uniform(30, 180)
        d.rectangle([x, y, x + w, y + h], fill=pal[rng.integers(len(pal))] + (255,))
    return im

def glow_silhouette(mask, T, cat, glow=(255, 250, 220)):
    """silueta rellena de manchas de color con halo brillante; mask: imagen L con la forma"""
    fill = blobs(T * 1.5, cat, mask.size, scale=5)
    halo = Image.new("RGBA", mask.size, glow + (0,))
    halo.putalpha(mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)))
    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    out.alpha_composite(halo)
    fill.putalpha(mask); out.alpha_composite(fill)
    return out

def wow_moment(img, T, t0, cat, kind="swirl", dur=1.6, center=(W / 2, H / 2)):
    """fondo psicodélico breve. Entra como un círculo que se abre desde el centro (0,25 s) y sale cerrándose:
    nada de fundidos. Solo para el momento MÁS loco del vídeo. Devuelve la intensidad (0..1)."""
    k = eo((T - t0) / 0.25) * eo((t0 + dur - T) / 0.25) if t0 <= T <= t0 + dur else 0.0
    if k <= 0: return 0.0
    bg = (swirl(T, cat) if kind == "swirl" else blobs(T, cat) if kind == "blobs" else glitch(T, cat))
    if k < 1:
        R = k * math.hypot(W, H) / 2 * 1.05
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse([center[0] - R, center[1] - R, center[0] + R, center[1] + R], fill=255)
        bg.putalpha(m)
    img.alpha_composite(bg)
    return k

def eo(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------- contorno ----------
def outlined_polygon(d, pts, fill, s=1, width=OUTLINE_W):
    d.polygon(pts, fill=fill)
    d.line(list(pts) + [pts[0]], fill=OUTLINE, width=int(width * s), joint="curve")

def outlined_ellipse(d, box, fill, s=1, width=OUTLINE_W):
    d.ellipse(box, fill=fill, outline=OUTLINE, width=int(width * s))

def card(img, box, color=CREAM, radius=36, a=1.0):
    """tarjeta crema (escena «de cerca» del videoclip) sobre el fondo de la categoría"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 10, y0 + 14, x1 + 10, y1 + 14], radius=radius, fill=(0, 0, 0, int(70 * a)))
    d.rounded_rectangle(box, radius=radius, fill=color + (int(255 * a),), outline=OUTLINE + (int(255 * a),), width=OUTLINE_W)
    img.alpha_composite(ov)

# ---------- contorno automático (post-proceso) ----------
def ink(img, mask, box, strength=0.95, thick=3, thresh=38):
    """contorno marrón oscuro del videoclip sobre lo ilustrado:
    - silueta: un aro de `thick` px POR FUERA de cada forma (las líneas finas y los textos quedan con borde, no tapados);
    - bordes internos entre colores, solo dentro de formas grandes (no dentro de pelos, líneas ni letras).
    img: RGBA a modificar; mask: array 0..1 (H,W) de lo que es dibujo; box: (x0,y0,x1,y1) zona a tratar."""
    x0, y0, x1, y1 = box
    a = np.asarray(img.convert("RGB"), dtype=np.int16)[y0:y1, x0:x1]
    m = mask[y0:y1, x0:x1] > 0.5
    mi = Image.fromarray((m * 255).astype(np.uint8))
    ring = np.asarray(mi.filter(ImageFilter.MaxFilter(2 * thick - 1)), bool) & ~m
    solid = np.asarray(mi.filter(ImageFilter.MinFilter(21)).filter(ImageFilter.MaxFilter(17)), bool)  # formas anchas (no letras ni pelos)
    dx = np.zeros(m.shape, bool); dy = np.zeros(m.shape, bool)
    dx[:, 1:] = np.abs(a[:, 1:] - a[:, :-1]).sum(-1) > thresh
    dy[1:] = np.abs(a[1:] - a[:-1]).sum(-1) > thresh
    inner = np.asarray(Image.fromarray(((dx | dy) & solid).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(thick)), bool) & solid
    e = Image.fromarray(((ring | inner) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).point(lambda v: int(v * strength))
    lay = Image.new("RGBA", (x1 - x0, y1 - y0), OUTLINE + (255,)); lay.putalpha(e)
    img.alpha_composite(lay, (x0, y0))
