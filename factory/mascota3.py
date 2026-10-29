"""Tres propuestas de Mr. Whiskerfact para comparar."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
FD = "/usr/share/fonts/opentype/inter/"
INK = (44, 30, 34); WHITE = (246, 244, 238); GOLD = (255, 199, 74); GOLD_D = (196, 140, 34)
NAVY1 = (10, 14, 30); NAVY2 = (26, 32, 66)

VARIANTS = {
    "A": dict(name="A · Clásico", sub="Gato naranja, monóculo y pajarita",
              fur=(240, 152, 70), fur_d=(204, 112, 44), muzzle=(255, 238, 214), ear=(246, 150, 160),
              blush=(250, 128, 112), iris=None, stripes=True, head=(290, 245), acc=["monocle", "bowtie"]),
    "B": dict(name="B · Profesor", sub="Gato gris con gafas redondas y bufanda",
              fur=(150, 162, 186), fur_d=(112, 122, 148), muzzle=(250, 250, 252), ear=(240, 168, 182),
              blush=(240, 150, 160), iris=(90, 160, 235), stripes=True, head=(300, 250), acc=["glasses", "scarf"]),
    "C": dict(name="C · Científico", sub="Gato negro con gafas de laboratorio y bata",
              fur=(52, 48, 66), fur_d=(36, 33, 46), muzzle=(84, 78, 100), ear=(200, 120, 150),
              blush=(214, 104, 130), iris=(150, 226, 110), stripes=False, head=(305, 262), acc=["goggles", "coat"]),
}

def draw_cat(dr, v, oy=0):
    def q(x, y): return (x * S, (y + oy) * S)
    def box(cx, cy, rx, ry): return [*q(cx - rx, cy - ry), *q(cx + rx, cy + ry)]
    fur, fur_d = v["fur"], v["fur_d"]
    hx, hy = v["head"]
    if "coat" in v["acc"]:
        dr.polygon([q(330, 1000), q(400, 820), q(540, 900), q(680, 820), q(750, 1000)], fill=WHITE)
        dr.polygon([q(470, 870), q(540, 960), q(610, 870)], fill=(90, 160, 235))
        dr.line([q(540, 900), q(540, 1000)], fill=(200, 200, 210), width=5 * S)
    if "scarf" in v["acc"]:
        dr.rounded_rectangle([*q(330, 820), *q(750, 900)], radius=40 * S, fill=(226, 72, 72))
        dr.polygon([q(620, 870), q(700, 870), q(720, 1010), q(640, 1010)], fill=(196, 52, 56))
        for y in (836, 862):
            dr.line([q(350, y), q(730, y)], fill=(196, 52, 56), width=5 * S)
    # orejas
    dr.polygon([q(285, 470), q(330, 175), q(495, 365)], fill=fur)
    dr.polygon([q(795, 470), q(750, 175), q(585, 365)], fill=fur)
    dr.polygon([q(320, 420), q(345, 245), q(445, 360)], fill=v["ear"])
    dr.polygon([q(760, 420), q(735, 245), q(635, 360)], fill=v["ear"])
    dr.ellipse(box(540, 610, hx, hy), fill=fur)
    dr.polygon([q(540 - hx + 28, 640), q(540 - hx - 30, 700), q(540 - hx + 50, 690), q(540 - hx, 760), q(540 - hx + 90, 735)], fill=fur)
    dr.polygon([q(540 + hx - 28, 640), q(540 + hx + 30, 700), q(540 + hx - 50, 690), q(540 + hx, 760), q(540 + hx - 90, 735)], fill=fur)
    if v["stripes"]:
        for x, w in ((540, 0), (488, -14), (592, 14)):
            dr.polygon([q(x - 16, 372), q(x + 16, 372), q(x + 6 + w * 0.3, 455), q(x - 6 + w * 0.3, 455)], fill=fur_d)
    if "goggles" in v["acc"]:
        dr.rounded_rectangle([*q(540 - hx + 10, 400), *q(540 + hx - 10, 428)], radius=14 * S, fill=(70, 120, 200))
        for gx in (468, 612):
            dr.ellipse(box(gx, 405, 66, 56), fill=(70, 120, 200))
            dr.ellipse(box(gx, 405, 50, 42), fill=(170, 220, 250))
            dr.arc(box(gx - 10, 395, 30, 24), 200, 270, fill=WHITE, width=7 * S)
    # mofletes y hocico
    dr.ellipse(box(365, 680, 52, 30), fill=v["blush"])
    dr.ellipse(box(715, 680, 52, 30), fill=v["blush"])
    dr.ellipse(box(488, 712, 88, 66), fill=v["muzzle"])
    dr.ellipse(box(592, 712, 88, 66), fill=v["muzzle"])
    dr.ellipse(box(540, 760, 52, 40), fill=v["muzzle"])
    dr.polygon([q(510, 662), q(570, 662), q(540, 700)], fill=v["ear"])
    dr.chord(box(540, 718, 58, 54), 0, 180, fill=(120, 40, 52))
    dr.ellipse(box(540, 752, 30, 18), fill=(246, 120, 140))
    line_c = INK if v["fur"][0] > 90 else (20, 16, 24)
    dr.arc(box(540, 718, 58, 54), 0, 180, fill=line_c, width=7 * S)
    dr.line([q(482, 718), q(598, 718)], fill=line_c, width=7 * S)
    dr.line([q(540, 698), q(540, 718)], fill=line_c, width=7 * S)
    # ojos
    for ex in (425, 655):
        dr.ellipse(box(ex, 568, 64, 72), fill=WHITE)
        if v["iris"]:
            dr.ellipse(box(ex + 6, 574, 46, 54), fill=v["iris"])
            dr.ellipse(box(ex + 6, 578, 26, 34), fill=INK)
        else:
            dr.ellipse(box(ex + 6, 574, 44, 52), fill=INK)
        dr.ellipse(box(ex + 22, 552, 15, 17), fill=WHITE)
        dr.ellipse(box(ex - 8, 596, 7, 8), fill=WHITE)
    brow = (230, 226, 240) if v["fur"][0] < 90 else INK
    if "goggles" not in v["acc"]:
        dr.arc(box(425, 482, 58, 30), 200, 340, fill=brow, width=10 * S)
        dr.arc(box(655, 472, 62, 34), 200, 340, fill=brow, width=10 * S)
    else:
        dr.arc(box(425, 498, 50, 22), 200, 340, fill=brow, width=9 * S)
        dr.arc(box(655, 492, 54, 24), 200, 340, fill=brow, width=9 * S)
    if "glasses" in v["acc"]:
        for ex in (425, 655):
            dr.ellipse(box(ex, 568, 92, 92), outline=(60, 48, 54), width=13 * S)
            dr.arc(box(ex - 22, 546, 52, 52), 200, 260, fill=(255, 255, 255), width=7 * S)
        dr.arc(box(540, 560, 46, 30), 200, 340, fill=(60, 48, 54), width=12 * S)
    if "monocle" in v["acc"]:
        dr.ellipse(box(655, 568, 102, 102), outline=GOLD, width=16 * S)
        dr.ellipse(box(655, 568, 86, 86), outline=GOLD_D, width=4 * S)
        dr.arc(box(632, 545, 58, 58), 200, 260, fill=(255, 255, 255), width=8 * S)
        pts = [(735, 640), (760, 700), (770, 760), (760, 830), (735, 880)]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            dr.line([q(x1, y1), q(x2, y2)], fill=GOLD, width=7 * S)
    # bigotes
    wc = INK if v["fur"][0] > 90 else (230, 226, 240)
    for side in (-1, 1):
        for dy0, dy1 in ((-12, -48), (6, 6), (24, 58)):
            dr.line([q(540 + side * 110, 722 + dy0), q(540 + side * 330, 722 + dy0 + dy1)], fill=wc, width=6 * S)
    if "bowtie" in v["acc"]:
        dr.polygon([q(540, 880), q(440, 835), q(440, 925)], fill=GOLD)
        dr.polygon([q(540, 880), q(640, 835), q(640, 925)], fill=GOLD)
        dr.ellipse(box(540, 880, 26, 28), fill=GOLD_D)

def avatar(v, size=1080):
    im = Image.new("RGBA", (1080 * S, 1080 * S), (0, 0, 0, 0))
    bg = Image.new("RGB", im.size); g = ImageDraw.Draw(bg)
    for y in range(0, 1080 * S, S):
        k = y / (1080 * S)
        g.rectangle([0, y, 1080 * S, y + S], fill=tuple(int(NAVY1[i] * (1 - k) + NAVY2[i] * k) for i in range(3)))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 1080 * S - 1, 1080 * S - 1], fill=255)
    im.paste(bg, (0, 0), mask)
    ImageDraw.Draw(im).ellipse([12 * S, 12 * S, 1068 * S, 1068 * S], outline=GOLD, width=14 * S)
    if v["fur"][0] < 90:   # halo para que el gato negro destaque sobre el fondo
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse([200 * S, 230 * S, 880 * S, 930 * S], fill=(90, 110, 190, 120))
        im.alpha_composite(Image.composite(halo.filter(ImageFilter.GaussianBlur(60 * S)), Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))
    cat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_cat(ImageDraw.Draw(cat), v, oy=-10)
    im.alpha_composite(Image.composite(cat, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))
    return im.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    W, H = 1800, 860
    sheet = Image.new("RGB", (W, H)); sd = ImageDraw.Draw(sheet)
    for y in range(H):
        k = y / H
        sd.line([(0, y), (W, y)], fill=tuple(int(NAVY1[i] * (1 - k) + NAVY2[i] * k) for i in range(3)))
    f1 = ImageFont.truetype(FD + "InterDisplay-Black.otf", 52)
    f2 = ImageFont.truetype(FD + "InterDisplay-Medium.otf", 28)
    f0 = ImageFont.truetype(FD + "InterDisplay-Bold.otf", 44)
    sd.text((W / 2, 48), "Mr. Whiskerfact · tres propuestas", font=f0, fill=WHITE, anchor="mt")
    for i, (k, v) in enumerate(VARIANTS.items()):
        av = avatar(v)
        av.save(os.path.join(OUT, f"whiskerfact_{k}.png"))
        sm = av.resize((520, 520), Image.LANCZOS)
        x = 60 + i * 580
        sheet.paste(sm, (x, 140), sm)
        sd.text((x + 260, 700), v["name"], font=f1, fill=WHITE, anchor="mt")
        sd.text((x + 260, 772), v["sub"], font=f2, fill=(150, 160, 190), anchor="mt")
    sheet.save(os.path.join(OUT, "whiskerfact_propuestas.png"))
    print("ok")
