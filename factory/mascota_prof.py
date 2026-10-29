"""Tres variantes del Profesor Whiskerfact."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import mascota3 as m

S, INK, WHITE = m.S, m.INK, m.WHITE
GLASS = (60, 48, 54)

BASE = dict(fur=(150, 162, 186), fur_d=(112, 122, 148), muzzle=(250, 250, 252), ear=(240, 168, 182),
            blush=(240, 150, 160), iris=(90, 160, 235), stripes=True, head=(300, 250))
VARIANTS = {
    "B1": dict(BASE, name="B1 · Pajarita", sub="Gafas redondas y pajarita roja",
               fur=(166, 176, 196), acc=["glasses"], extra=["bow_red"]),
    "B2": dict(BASE, name="B2 · Catedrático", sub="Gafas de media luna y chaqueta de punto",
               fur=(138, 150, 176), fur_d=(100, 110, 138), iris=(232, 180, 70), acc=[], extra=["cardigan", "halfmoon"]),
    "B3": dict(BASE, name="B3 · Graduado", sub="Birrete, gafas y bufanda de universidad",
               acc=["glasses"], extra=["uniscarf", "cap"]),
}

def behind(dr, v, oy):
    def q(x, y): return (x * S, (y + oy) * S)
    if "cardigan" in v["extra"]:
        dr.polygon([q(320, 1010), q(380, 830), q(540, 900), q(700, 830), q(760, 1010)], fill=(150, 98, 64))
        dr.polygon([q(440, 852), q(540, 990), q(640, 852)], fill=WHITE)
        dr.polygon([q(526, 880), q(554, 880), q(562, 990), q(518, 990)], fill=(70, 110, 200))
        for y in (930, 975):
            dr.ellipse([*q(494 - 9, y - 9), *q(494 + 9, y + 9)], fill=(110, 70, 44))
    if "uniscarf" in v["extra"]:
        dr.rounded_rectangle([*q(330, 820), *q(750, 900)], radius=40 * S, fill=(40, 60, 120))
        dr.polygon([q(620, 870), q(700, 870), q(720, 1010), q(640, 1010)], fill=(40, 60, 120))
        for x in (400, 500, 600, 700):
            dr.rectangle([*q(x, 820), *q(x + 34, 900)], fill=(255, 199, 74))
        for y in (900, 950):
            dr.polygon([q(625, y), q(705, y), q(709, y + 24), q(629, y + 24)], fill=(255, 199, 74))

def front(dr, v, oy):
    def q(x, y): return (x * S, (y + oy) * S)
    def box(cx, cy, rx, ry): return [*q(cx - rx, cy - ry), *q(cx + rx, cy + ry)]
    if "bow_red" in v["extra"]:
        red, red_d = (226, 72, 72), (176, 44, 50)
        dr.polygon([q(540, 880), q(430, 830), q(430, 930)], fill=red)
        dr.polygon([q(540, 880), q(650, 830), q(650, 930)], fill=red)
        for dx in (-1, 1):
            dr.line([q(540 + dx * 40, 860), q(540 + dx * 90, 848)], fill=red_d, width=5 * S)
            dr.line([q(540 + dx * 40, 900), q(540 + dx * 90, 912)], fill=red_d, width=5 * S)
        dr.ellipse(box(540, 880, 26, 30), fill=red_d)
    if "halfmoon" in v["extra"]:
        for ex in (425, 655):
            dr.chord(box(ex, 590, 82, 70), 0, 180, outline=GLASS, width=12 * S)
            dr.line([q(ex - 82, 590), q(ex + 82, 590)], fill=GLASS, width=12 * S)
        dr.line([q(507, 596), q(573, 596)], fill=GLASS, width=10 * S)
    if "cap" in v["extra"]:
        dr.polygon([q(410, 380), q(670, 380), q(650, 440), q(430, 440)], fill=(34, 36, 52))
        dr.polygon([q(540, 270), q(790, 345), q(540, 410), q(290, 345)], fill=(44, 46, 66))
        dr.polygon([q(540, 270), q(790, 345), q(540, 395), q(290, 345)], fill=(56, 58, 82))
        dr.ellipse(box(540, 338, 14, 12), fill=(255, 199, 74))
        dr.line([q(540, 338), q(735, 368), q(745, 470)], fill=(255, 199, 74), width=7 * S)
        dr.polygon([q(733, 465), q(757, 465), q(764, 520), q(726, 520)], fill=(255, 199, 74))

def avatar(v, size=1080):
    big = 1080 * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    bg = Image.new("RGB", im.size); g = ImageDraw.Draw(bg)
    for y in range(0, big, S):
        k = y / big
        g.rectangle([0, y, big, y + S], fill=tuple(int(m.NAVY1[i] * (1 - k) + m.NAVY2[i] * k) for i in range(3)))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, big - 1, big - 1], fill=255)
    im.paste(bg, (0, 0), mask)
    ImageDraw.Draw(im).ellipse([12 * S, 12 * S, 1068 * S, 1068 * S], outline=m.GOLD, width=14 * S)
    cat = Image.new("RGBA", im.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(cat)
    behind(cd, v, -10); m.draw_cat(cd, v, oy=-10); front(cd, v, -10)
    im.alpha_composite(Image.composite(cat, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))
    return im.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    W, H = 1800, 860
    sheet = Image.new("RGB", (W, H)); sd = ImageDraw.Draw(sheet)
    for y in range(H):
        k = y / H
        sd.line([(0, y), (W, y)], fill=tuple(int(m.NAVY1[i] * (1 - k) + m.NAVY2[i] * k) for i in range(3)))
    f0 = ImageFont.truetype(m.FD + "InterDisplay-Bold.otf", 44)
    f1 = ImageFont.truetype(m.FD + "InterDisplay-Black.otf", 52)
    f2 = ImageFont.truetype(m.FD + "InterDisplay-Medium.otf", 28)
    sd.text((W / 2, 48), "Profesor Whiskerfact · tres variantes", font=f0, fill=WHITE, anchor="mt")
    for i, (k, v) in enumerate(VARIANTS.items()):
        av = avatar(v); av.save(os.path.join(m.OUT, f"whiskerfact_{k}.png"))
        sm = av.resize((520, 520), Image.LANCZOS)
        x = 60 + i * 580
        sheet.paste(sm, (x, 140), sm)
        sd.text((x + 260, 700), v["name"], font=f1, fill=WHITE, anchor="mt")
        sd.text((x + 260, 772), v["sub"], font=f2, fill=(150, 160, 190), anchor="mt")
    sheet.save(os.path.join(m.OUT, "whiskerfact_profesor.png"))
    print("ok")
