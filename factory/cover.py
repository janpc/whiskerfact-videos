"""Portada Mr. Whiskerfact (plantilla A «rayos»). Misma plantilla en TODOS los reels y la usa también la escena del gancho
(el primer fotograma del vídeo ES la portada, sin cortes): fondo vivo del color de la categoría con rayos, marca + categoría
arriba, título corto en 2 líneas (blanco + amarillo), pregunta debajo, ilustración grande en el centro y el gato abajo."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import library as LIB

W, H = B.W, B.H
INK = (24, 16, 20)
_cache = {}

def _font(w, size):
    k = (w, size)
    if k not in _cache: _cache[k] = ImageFont.truetype(B.FONT_DIR + f"Inter-{w}.otf", size)
    return _cache[k]

def _grad(cat):
    k = ("g", cat)
    if k not in _cache:
        c = B.CATEGORIES[cat]["color"]
        top = tuple(int(v * 0.95) for v in c); bot = tuple(int(v * 0.42) for v in c)
        img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img)
        for y in range(H):
            kk = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * kk) for i in range(3)) + (255,))
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([140, 760, 940, 1400], fill=(255, 255, 255, 70))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
        _cache[k] = img
    return _cache[k]

def draw_bg(img, cat, angle=0.0):
    """fondo de la portada; `angle` gira los rayos (animación)"""
    img.alpha_composite(_grad(cat))
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
    cx, cy = 540, 1080
    for i in range(14):
        a0 = angle + i * math.tau / 14; a1 = a0 + math.tau / 28
        rd.polygon([(cx, cy), (cx + 1800 * math.cos(a0), cy + 1800 * math.sin(a0)), (cx + 1800 * math.cos(a1), cy + 1800 * math.sin(a1))], fill=(255, 255, 255, 26))
    img.alpha_composite(rays)

def draw_header(img, cat):
    d = ImageDraw.Draw(img)
    d.text((90, 290), "MR. WHISKERFACT", font=_font("ExtraBold", 38), fill=B.GOLD, anchor="lm", stroke_width=4, stroke_fill=INK)
    lab = B.CATEGORIES[cat]["label"]; f = _font("Black", 34); tw = d.textlength(lab, font=f)
    d.rounded_rectangle([990 - tw - 44, 266, 990, 316], radius=25, fill=(255, 255, 255), outline=INK, width=5)
    d.text((990 - tw / 2 - 22, 291), lab, font=f, fill=INK, anchor="mm")

def draw_title(img, line1, line2, sub="", a=1.0):
    lay = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    kw = dict(anchor="mm", stroke_width=12, stroke_fill=INK)
    d.text((540, 150), line1.upper(), font=_font("Black", 150), fill=(255, 255, 255), **kw)
    d.text((540, 320), line2.upper(), font=_font("Black", 150), fill=(255, 222, 90), **kw)
    if sub: d.text((540, 470), sub, font=_font("ExtraBold", 74), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=INK)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay, (0, 320))

def make_cover(cat, line1, line2, illus, out, sub="", mascot_path=None):
    """illus: lista de (biblioteca, nombre, cx, cy, alto, rot) en coordenadas del lienzo 1080x1920"""
    img = Image.new("RGBA", (W, H)); draw_bg(img, cat)
    draw_header(img, cat); draw_title(img, line1, line2, sub)
    for lib, name, x, y, h, rot in illus:
        LIB.place(img, lib, name, x, y, height=h, rot=rot, anchor="center")
    try:
        m = Image.open(mascot_path or B.MASCOT["file"]).convert("RGBA"); s = 420
        m = m.resize((s, int(m.size[1] * s / m.size[0])), Image.LANCZOS); img.alpha_composite(m, (60, 1460))
    except Exception as ex:
        print("sin mascota:", ex)
    img.convert("RGB").save(out, quality=92)
    return out
