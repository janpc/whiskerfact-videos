"""Imágenes de perfil de las redes: foto de perfil y banner de YouTube."""
from PIL import Image, ImageDraw, ImageFont
import brand as B
OUT = "out/perfil/"
NAVY = (16, 20, 44)
av = Image.open(B.MASCOT["file"]).convert("RGBA")   # gato nuevo (mascot.py)

# foto de perfil: las redes la recortan en círculo; dejamos margen para que el aro dorado no se corte
p = Image.new("RGB", (1080, 1080), NAVY)
a = av.resize((990, 990), Image.LANCZOS); p.paste(a, (45, 45), a)
p.save(OUT + "foto_perfil_1080.png")

# banner de YouTube 2560x1440; lo importante dentro de la zona segura central 1546x423
W, H = 2560, 1440
top, bot = (12, 16, 36), (22, 28, 64)
bn = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bn)
for y in range(H):
    k = y / H; d.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
# puntos de color de las categorías dispersos por los bordes (se ven en TV, no estorban en móvil)
import random; rnd = random.Random(4)
cols = [c["color"] for c in B.CATEGORIES.values()]
for _ in range(90):
    x, y = rnd.randint(0, W), rnd.randint(0, H)
    if 440 < y < 1000 and 450 < x < 2110: continue
    r = rnd.randint(6, 22); c = rnd.choice(cols)
    d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(round(c[i] * 0.55 + top[i] * 0.45) for i in range(3)))
sx, sy = (W - 1546) // 2, (H - 423) // 2
a = av.resize((400, 400), Image.LANCZOS); bn.paste(a, (sx + 10, sy + 12), a)
F = lambda w, s: ImageFont.truetype(B.FONT_DIR + f"InterDisplay-{w}.otf", s)
x0 = sx + 470
d.text((x0, sy + 40), "Mr. Whiskerfact", font=F("Black", 120), fill=B.TEXT)
d.text((x0, sy + 185), "Curious facts, explained simply.", font=F("Medium", 50), fill=B.TEXT_2)
x = x0; y = sy + 285
for c in B.CATEGORIES.values():
    t = c["label"]; f = F("Bold", 34); w = f.getlength(t) + 44
    d.rounded_rectangle([x, y, x + w, y + 62], radius=31, fill=c["color"])
    d.text((x + 22, y + 13), t, font=f, fill=B.CHIP_TEXT); x += w + 16
bn.save(OUT + "banner_youtube_2560x1440.png")
# vista de cómo queda en móvil (solo la zona segura)
bn.crop((sx, sy, sx + 1546, sy + 423)).save(OUT + "banner_youtube_vista_movil.png")
