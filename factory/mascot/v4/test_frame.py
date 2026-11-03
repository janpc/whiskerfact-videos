"""Prueba de UN fotograma del estilo nuevo (0 créditos): gato v4 con cuerpo con rebeca y expresiones nuevas, contorno algo más grueso,
color dominante por escena, grano plano muy sutil (sin relieve) y subtítulo con letra de aire manual.
  python3 v4/test_frame.py -> v4/test_frame.png y v4/test_fonts.png (comparación de letras con la actual)
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(D, "..", "v3")
sys.path.insert(0, os.path.join(D, "..", ".."))
import mascot as M
import parts_body as PB

W, H = 1080, 1920
BG = (46, 110, 140); FLOOR = (30, 78, 102); INK = (58, 36, 30); ACCENT = (255, 214, 92); CREAM = (255, 248, 232)
CUT = (790, 835)         # corte suave de la cabeza por el cuello (lienzo de la base)

def cat_image(pose="stand_front", eyes_v4=4, mouth="happy", gaze=(0.3, 0)):
    cat = M.Cat()
    body = Image.open(os.path.join(D, f"body_{pose}.png")).convert("RGBA")
    head = cat.base.copy()
    head.alpha_composite(cat._eyes_layer(gaze) if eyes_v4 is None else Image.open(os.path.join(D, f"eyes_{eyes_v4:02d}.png")).convert("RGBA"))
    head.alpha_composite(cat.mouth[mouth])
    a = np.asarray(head.split()[3]).astype(np.float32)
    ramp = np.clip((CUT[1] - np.arange(head.height)) / (CUT[1] - CUT[0]), 0, 1)[:, None]
    head.putalpha(Image.fromarray((a * ramp).astype(np.uint8)))
    out = Image.new("RGBA", PB.CANVAS, (0, 0, 0, 0))
    out.alpha_composite(body); out.alpha_composite(head, PB.HEAD_AT)
    return out.crop(out.getbbox())

def outline(img, px, color=INK):
    """contorno plano alrededor de la silueta (sin relieve)"""
    a = img.split()[3]
    big = a.filter(ImageFilter.MaxFilter(px * 2 + 1))
    o = Image.new("RGBA", img.size, color + (255,)); o.putalpha(big)
    res = Image.new("RGBA", (img.width + 2 * px, img.height + 2 * px), (0, 0, 0, 0))
    pad = Image.new("RGBA", res.size, (0, 0, 0, 0)); pad.alpha_composite(o, (px, px))
    res.alpha_composite(pad); res.alpha_composite(img, (px, px)); return res

def grain(img, amt=3):
    n = np.random.default_rng(7).normal(0, amt, (img.height, img.width, 1)).astype(np.float32)
    a = np.asarray(img.convert("RGB")).astype(np.float32) + n
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def text_outlined(d, xy, s, font, fill, stroke=INK, sw=9, anchor="ma"):
    d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)

def frame():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle((0, 1250, W, H), fill=FLOOR)                                      # suelo: plano, un tono más oscuro
    f = ImageFont.truetype(os.path.join(D, "fonts", "LondrinaSolid-Regular.ttf"), 118)
    text_outlined(d, (W / 2, 330), "What if the cat", f, CREAM); text_outlined(d, (W / 2, 465), "is BOTH?", f, ACCENT)
    cat = outline(cat_image(), 6)
    sc = 880 / cat.height; cat = cat.resize((round(cat.width * sc), 880), Image.LANCZOS)
    top = 1390 - 780
    im.paste(cat, ((W - cat.width) // 2 - 70, top), cat)
    d.rounded_rectangle((60, 1390, W - 60, 1580), radius=18, fill=(176, 120, 72), outline=INK, width=8)   # mesa de la clase: plana, tapa el corte de la cintura
    d.rectangle((60, 1390, W - 60, 1410), fill=(196, 140, 90))
    f2 = ImageFont.truetype(os.path.join(D, "fonts", "LondrinaSolid-Regular.ttf"), 66)
    text_outlined(d, (485, 1450), "alive and dead", f2, CREAM, sw=7)               # subtítulo de voz (a la izquierda de los botones)
    d.rectangle((900, 900, 1080, 1700), outline=(255, 0, 0), width=2)               # zona de botones, solo en la prueba
    return grain(im)

def fonts():
    cands = [("Actual: Inter Display Bold", "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"),
             ("Londrina Solid", os.path.join(D, "fonts", "LondrinaSolid-Regular.ttf")),
             ("Caveat Brush", os.path.join(D, "fonts", "CaveatBrush-Regular.ttf")),
             ("Gochi Hand", os.path.join(D, "fonts", "GochiHand-Regular.ttf"))]
    im = Image.new("RGB", (1080, 1000), BG); d = ImageDraw.Draw(im)
    for i, (name, p) in enumerate(cands):
        y = 40 + i * 240
        try: ft = ImageFont.truetype(p, 78)
        except Exception as e: d.text((40, y), f"{name}: no disponible ({e})", fill=CREAM); continue
        small = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf", 26)
        d.text((40, y), name, font=small, fill=(200, 215, 225))
        text_outlined(d, (40, y + 44), "Is the cat alive or not?", ft, CREAM, sw=6, anchor="la")
    return grain(im)

if __name__ == "__main__":
    frame().save(os.path.join(D, "test_frame.png")); fonts().save(os.path.join(D, "test_fonts.png")); print("ok")
