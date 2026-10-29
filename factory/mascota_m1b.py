"""M1 con ojos ámbar: nuevas combinaciones de pelaje y ropa."""
import os
from PIL import Image, ImageDraw, ImageFont
import mascota3 as m

S, WHITE = m.S, m.WHITE
AMBER = (232, 176, 62)
BASE = dict(m.VARIANTS["B"], acc=["glasses"], iris=AMBER, pocket=None, pen=False)
VARIANTS = [
    dict(BASE, name="1 · Gris humo", sub="Jersey de cuello alto gris marengo",
         fur=(118, 124, 140), fur_d=(88, 94, 110), top=("turtle", (78, 80, 96))),
    dict(BASE, name="2 · Caramelo", sub="Rebeca crema y pajarita azul marino",
         fur=(200, 132, 76), fur_d=(160, 98, 50), muzzle=(255, 240, 222), top=("cardi", (232, 220, 196)),
         tie=("bow", (40, 56, 110))),
    dict(BASE, name="3 · Gris azulado", sub="Americana azul marino y pañuelo",
         top=("blazer", (40, 56, 104)), tie=None, pocket=(255, 199, 74)),
    dict(BASE, name="4 · Chocolate", sub="Rebeca mostaza y corbata verde",
         fur=(116, 82, 64), fur_d=(84, 58, 44), muzzle=(240, 222, 204), top=("cardi", (212, 158, 48)),
         tie=("long", (46, 104, 76)), pen=True),
    dict(BASE, name="5 · Plata", sub="Jersey de cuello alto granate",
         fur=(184, 190, 206), fur_d=(146, 152, 172), top=("turtle", (128, 40, 56))),
    dict(BASE, name="6 · Gris atigrado", sub="Rebeca verde oliva y pajarita granate",
         fur=(140, 146, 160), fur_d=(100, 106, 122), top=("cardi", (104, 112, 70)), tie=("bow", (136, 36, 52))),
]

def behind(dr, v, oy):
    def q(x, y): return (x * S, (y + oy) * S)
    kind, c = v["top"]; cd = tuple(int(x * 0.74) for x in c)
    if kind == "turtle":
        dr.polygon([q(320, 1010), q(380, 840), q(700, 840), q(760, 1010)], fill=c)
        dr.rounded_rectangle([*q(400, 810), *q(680, 905)], radius=36 * S, fill=c)
        for x in range(420, 670, 26):
            dr.line([q(x, 822), q(x, 894)], fill=cd, width=5 * S)
        return
    dr.polygon([q(320, 1010), q(380, 830), q(540, 900), q(700, 830), q(760, 1010)], fill=c)
    dr.polygon([q(440, 852), q(540, 990), q(640, 852)], fill=WHITE)
    if kind == "blazer":
        dr.polygon([q(380, 830), q(440, 852), q(520, 990), q(430, 1010)], fill=cd)
        dr.polygon([q(700, 830), q(640, 852), q(560, 990), q(650, 1010)], fill=cd)
        dr.polygon([q(500, 860), q(540, 900), q(580, 860)], fill=(220, 224, 236))   # cuello de camisa
    else:
        dr.line([q(440, 852), q(540, 990)], fill=cd, width=10 * S)
        dr.line([q(640, 852), q(540, 990)], fill=cd, width=10 * S)
        for y in (940, 985):
            dr.ellipse([*q(490, y - 10), *q(510, y + 10)], fill=cd)
    if v.get("tie") and v["tie"][0] == "long":
        dr.polygon([q(526, 880), q(554, 880), q(562, 990), q(518, 990)], fill=v["tie"][1])
    if v["pocket"]:
        dr.polygon([q(628, 930), q(676, 930), q(668, 900), q(652, 912), q(640, 898)], fill=v["pocket"])
        dr.line([q(622, 932), q(680, 932)], fill=cd, width=5 * S)
    if v["pen"]:
        dr.rectangle([*q(632, 905), *q(644, 975)], fill=(40, 40, 50))
        dr.rectangle([*q(630, 900), *q(646, 912)], fill=(255, 199, 74))

def front(dr, v, oy):
    def q(x, y): return (x * S, (y + oy) * S)
    if v.get("tie") and v["tie"][0] == "bow":
        c = v["tie"][1]
        dr.polygon([q(540, 880), q(470, 850), q(470, 910)], fill=c)
        dr.polygon([q(540, 880), q(610, 850), q(610, 910)], fill=c)
        dr.ellipse([*q(522, 860), *q(558, 900)], fill=tuple(int(x * 0.78) for x in c))

def avatar(v):
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
    cat = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cat)
    behind(d, v, -10); m.draw_cat(d, v, oy=-10); front(d, v, -10)
    im.alpha_composite(Image.composite(cat, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))
    return im.resize((1080, 1080), Image.LANCZOS)

if __name__ == "__main__":
    W, H = 1800, 1560
    sheet = Image.new("RGB", (W, H)); sd = ImageDraw.Draw(sheet)
    for y in range(H):
        k = y / H
        sd.line([(0, y), (W, y)], fill=tuple(int(m.NAVY1[i] * (1 - k) + m.NAVY2[i] * k) for i in range(3)))
    f0 = ImageFont.truetype(m.FD + "InterDisplay-Bold.otf", 44)
    f1 = ImageFont.truetype(m.FD + "InterDisplay-Black.otf", 44)
    f2 = ImageFont.truetype(m.FD + "InterDisplay-Medium.otf", 26)
    sd.text((W / 2, 48), "Whiskerfact · ojos ámbar, nuevas combinaciones", font=f0, fill=WHITE, anchor="mt")
    for i, v in enumerate(VARIANTS):
        av = avatar(v); av.save(os.path.join(m.OUT, f"whiskerfact_ambar_{i + 1}.png"))
        sm = av.resize((480, 480), Image.LANCZOS)
        x = 80 + (i % 3) * 580; y = 130 + (i // 3) * 710
        sheet.paste(sm, (x, y), sm)
        sd.text((x + 240, y + 510), v["name"], font=f1, fill=WHITE, anchor="mt")
        sd.text((x + 240, y + 572), v["sub"], font=f2, fill=(150, 160, 190), anchor="mt")
    sheet.save(os.path.join(m.OUT, "whiskerfact_ambar.png"))
    print("ok")
