"""Portada Mr. Whiskerfact (fotograma 0 + miniatura). Misma plantilla en TODOS los reels:
fondo vivo del color de la categoría, título corto en 2 líneas (blanco + línea de acento), ilustración grande
en el centro, gato abajo a la izquierda, marca arriba. Solo cambian color, título e ilustración."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import library as LIB

W, H = B.W, B.H

def _font(w, size): return ImageFont.truetype(B.FONT_DIR + f"Inter-{w}.otf", size)

def _outlined(img, text, font, xy, fill, ink=(24, 16, 20), r=9, anchor="mm"):
    d = ImageDraw.Draw(img)
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=r, stroke_fill=ink)

def make_cover(cat, line1, line2, illus, out, mascot_path=None):
    """illus: lista de (biblioteca, nombre, cx, cy, alto, rot) en coordenadas del lienzo 1080x1920"""
    c = B.CATEGORIES[cat]["color"]
    top = tuple(int(v * 0.95) for v in c); bot = tuple(int(v * 0.42) for v in c)
    img = Image.new("RGBA", (W, H))
    px = img.load(); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * k) for i in range(3)) + (255,))
    # rayos suaves detrás de la ilustración
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
    cx, cy = 540, 1080
    for i in range(14):
        a0 = i * math.tau / 14; a1 = a0 + math.tau / 28
        rd.polygon([(cx, cy), (cx + 1800 * math.cos(a0), cy + 1800 * math.sin(a0)), (cx + 1800 * math.cos(a1), cy + 1800 * math.sin(a1))], fill=(255, 255, 255, 26))
    img.alpha_composite(rays)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([140, 760, 940, 1400], fill=(255, 255, 255, 70))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
    # marca + categoría (zona segura)
    d = ImageDraw.Draw(img)
    d.text((90, 290), "MR. WHISKERFACT", font=_font("ExtraBold", 38), fill=B.GOLD, anchor="lm", stroke_width=4, stroke_fill=(24, 16, 20))
    lab = B.CATEGORIES[cat]["label"]; f = _font("Black", 34); tw = d.textlength(lab, font=f)
    d.rounded_rectangle([990 - tw - 44, 266, 990, 316], radius=25, fill=(255, 255, 255), outline=(24, 16, 20), width=5)
    d.text((990 - tw / 2 - 22, 291), lab, font=f, fill=(24, 16, 20), anchor="mm")
    # título (máx. 2 líneas, muy grande)
    _outlined(img, line1.upper(), _font("Black", 150), (540, 470), (255, 255, 255), r=12)
    acc = (255, 222, 90)
    _outlined(img, line2.upper(), _font("Black", 150), (540, 640), acc, r=12)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([340, 742, 740, 754], radius=6, fill=(24, 16, 20))
    # ilustración
    for lib, name, x, y, h, rot in illus:
        LIB.place(img, lib, name, x, y, height=h, rot=rot, anchor="center")
    # gato
    mp = mascot_path or B.MASCOT["file"]
    try:
        m = Image.open(mp).convert("RGBA"); s = 420; m = m.resize((s, int(m.size[1] * s / m.size[0])), Image.LANCZOS)
        img.alpha_composite(m, (60, 1500 - 40))
    except Exception as ex:
        print("sin mascota:", ex)
    img.convert("RGB").save(out, quality=92)
    return out

if __name__ == "__main__":
    make_cover("body", "Bone vs", "steel", [("bone_steel_items", "femur", 380, 1090, 480, -10), ("bone_steel_items", "steel_bar", 700, 1090, 480, 10)], "/tmp/cover_test.png")
