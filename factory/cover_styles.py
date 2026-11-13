import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import brand as B
import library as LIB
import cover as C
W, H = B.W, B.H
INK = (24, 16, 20)
def F(w, s): return ImageFont.truetype(B.FONT_DIR + f"Inter-{w}.otf", s)
def cat_img(size):
    m = Image.open(B.MASCOT["file"]).convert("RGBA"); return m.resize((size, int(m.size[1] * size / m.size[0])), Image.LANCZOS)
def grad(top, bot):
    img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * k) for i in range(3)) + (255,))
    return img
def head(img, cat, dark=False):
    d = ImageDraw.Draw(img); c = B.CATEGORIES[cat]["color"]
    d.text((90, 290), "MR. WHISKERFACT", font=F("ExtraBold", 38), fill=B.GOLD, anchor="lm", stroke_width=4, stroke_fill=INK)
    lab = B.CATEGORIES[cat]["label"]; f = F("Black", 34); tw = d.textlength(lab, font=f)
    d.rounded_rectangle([990 - tw - 44, 266, 990, 316], radius=25, fill=c if dark else (255, 255, 255), outline=INK, width=5)
    d.text((990 - tw / 2 - 22, 291), lab, font=f, fill=INK if not dark else (255, 255, 255), anchor="mm")
def outl(img, t, f, xy, fill, r=10, anchor="mm"):
    ImageDraw.Draw(img).text(xy, t, font=f, fill=fill, anchor=anchor, stroke_width=r, stroke_fill=INK)
def put(img, illus):
    for lib, name, x, y, h, rot in illus: LIB.place(img, lib, name, x, y, height=h, rot=rot, anchor="center")

def style_a(cat, l1, l2, illus, out):          # RAYOS
    C.make_cover(cat, l1, l2, illus, out)

def style_b(cat, l1, l2, illus, out):          # PÓSTER OSCURO + disco de color
    c = B.CATEGORIES[cat]["color"]; top, bot = B.bg_for(cat)
    img = grad(top, bot); head(img, cat, dark=True)
    disc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(disc)
    dd.ellipse([90, 420, 990, 1320], fill=c + (255,), outline=(255, 255, 255, 255), width=14)
    dd.ellipse([140, 470, 940, 1270], outline=(255, 255, 255, 90), width=6)
    img.alpha_composite(disc); put(img, illus)
    acc = B.accent_text_for(cat); dd = ImageDraw.Draw(img)
    def fit(t, mx, sz=170):
        while dd.textlength(t, font=F("Black", sz)) > mx: sz -= 6
        return F("Black", sz)
    outl(img, l1.upper(), fit(l1.upper(), 640), (80, 1415), (255, 255, 255), 12, "lm")
    outl(img, l2.upper(), fit(l2.upper(), 640), (80, 1585), acc, 12, "lm")
    m = cat_img(280); img.alpha_composite(m, (730, 1500))
    img.convert("RGB").save(out, quality=92)

def style_c(cat, l1, l2, illus, out):          # TARJETA EDITORIAL crema con marco de color
    c = B.CATEGORIES[cat]["color"]
    img = Image.new("RGBA", (W, H), c + (255,)); d = ImageDraw.Draw(img)
    for x in range(-H, W, 70): d.line([(x, H), (x + H, 0)], fill=tuple(min(255, v + 18) for v in c) + (255,), width=18)
    head(img, cat)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([70, 360, 1010, 1250], radius=56, fill=(250, 244, 226), outline=INK, width=10)
    put(img, illus)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([70, 1290, 1010, 1640], radius=56, fill=INK)
    outl(img, l1.upper(), F("Black", 130), (540, 1400), (255, 255, 255), 0)
    outl(img, l2.upper(), F("Black", 130), (540, 1540), B.accent_text_for(cat), 0)
    m = cat_img(230); img.alpha_composite(m, (790, 1010))
    img.convert("RGB").save(out, quality=92)

THEMES = [
    ("body", "Bone vs", "steel", [("bone_steel_items", "femur", 380, 860, 440, -10), ("bone_steel_items", "steel_bar", 700, 860, 440, 10)]),
    ("nature", "Vampire", "bats", [("vampire_bat", "fly_front", 540, 860, 480, 0)]),
    ("tech", "Wi-Fi vs", "microwave", [("wifi_objects", "router", 360, 880, 340, 0), ("wifi_objects", "microwave", 720, 880, 340, 0)]),
]
if __name__ == "__main__":
    for name, fn in (("a", style_a), ("b", style_b), ("c", style_c)):
        outs = []
        for cat, l1, l2, il in THEMES:
            dy = {"a": 220, "b": 0, "c": -40}[name]; k = {"a": 1.0, "b": 0.85, "c": 0.9}[name]
            il2 = [(a, b, 540 + (x - 540) * k, y + dy, h * k, r) for a, b, x, y, h, r in il]
            p = f"/tmp/cv_{name}_{cat}.png"; fn(cat, l1, l2, il2, p); outs.append(p)
        sheet = Image.new("RGB", (3 * 540 + 40, 960), (20, 20, 20))
        for i, p in enumerate(outs): sheet.paste(Image.open(p).resize((540, 960)), (i * 560, 0))
        sheet.save(f"/tmp/sheet_{name}.jpg", quality=88)
    print("ok")
