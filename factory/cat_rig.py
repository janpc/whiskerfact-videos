"""Gato «recortable» (rig 2D) a partir de las piezas de `library/cat_rig/`: cuerpo, cola y 4 patas (rectas y dobladas).
Las piezas salen de dos hojas de Gemini (cuerpo sin patas + patas sueltas). Las patas giran desde el hombro/cadera, y con
`walk_pose(phase)` el pie que apoya se queda clavado en el suelo mientras el cuerpo avanza (nada de patinar).

  import cat_rig as R
  img, (px, base) = R.render(R.walk_pose(phase))     # RGBA; (px, base) = x del centro del cuerpo y y del suelo dentro de la imagen
"""
import math, os
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library", "cat_rig")
_cache = {}
def piece(name):
    if name not in _cache: _cache[name] = Image.open(os.path.join(D, name + ".png")).convert("RGBA")
    return _cache[name]

LEG_SY = 0.62; LEG_SX = 0.52        # las patas salieron muy gruesas: más largas y más estrechas que la pieza original
# anclajes sobre la pieza `body` (px de la pieza): hombro y cadera, y dónde sale la cola
SHOULDER = (0.69, 0.72); HIP = (0.27, 0.76); TAIL_AT = (0.10, 0.50)
# pivote de cada pata dentro de su pieza (fracción de ancho/alto): el extremo redondo superior
PIVOT = {"leg_nf": (0.5, 0.14), "leg_nb": (0.5, 0.2), "leg_ff": (0.5, 0.14), "leg_fb": (0.5, 0.2)}
LEGS = [("leg_fb", "back", True), ("leg_ff", "front", True), ("leg_nb", "back", False), ("leg_nf", "front", False)]   # orden de dibujo: lejanas, luego cercanas

def leg_len(name):
    p = piece(name); return p.height * LEG_SY * (1 - PIVOT[name][1])

def render(pose, body="body", canvas=(700, 520), origin=(350, 150), scale=1.0):
    """pose: dict {'body_dy':, 'body_rot':, 'tail_rot':, 'legs': {nombre: (ángulo°, plegada)}} ; ángulo + = el pie va hacia delante (derecha)"""
    W, H = canvas; im = Image.new("RGBA", canvas, (0, 0, 0, 0))
    b = piece(body); bw, bh = b.size
    ox, oy = origin[0] - bw / 2, origin[1] + pose.get("body_dy", 0)
    def paste(img, pivot_xy, at_xy, rot):
        # gira `img` alrededor de pivot_xy (px de img) y lo coloca con el pivote en at_xy
        r = img.rotate(-rot, Image.BICUBIC, expand=True)
        cx, cy = img.width / 2, img.height / 2; dx, dy = pivot_xy[0] - cx, pivot_xy[1] - cy
        a = math.radians(rot)
        # rotación horaria positiva en pantalla (y hacia abajo): (dx,dy) -> (dx cos - dy sin, dx sin + dy cos) con ángulo a
        rx = dx * math.cos(a) - dy * math.sin(a); ry = dx * math.sin(a) + dy * math.cos(a)
        px, py = r.width / 2 + rx, r.height / 2 + ry
        im.alpha_composite(r, (int(round(at_xy[0] - px)), int(round(at_xy[1] - py))))
    def leg(name, kind, far):
        ang, folded = pose["legs"][name]
        p = piece(name + "_up" if folded else name)
        s = p.resize((round(p.width * LEG_SX), round(p.height * LEG_SY)), Image.LANCZOS)
        pv = PIVOT[name]; anchor = SHOULDER if kind == "front" else HIP
        at = (ox + anchor[0] * bw, oy + anchor[1] * bh)
        paste(s, (s.width * pv[0], s.height * pv[1]), at, -ang)      # paste gira en sentido horario: -ang deja + = pie hacia delante
    for name, kind, far in LEGS:             # todas las patas DETRÁS del cuerpo: solo asoma lo que queda bajo la panza
        leg(name, kind, far)
    t = piece("tail"); paste(t, (t.width - 4, t.height - 10), (ox + TAIL_AT[0] * bw, oy + TAIL_AT[1] * bh), pose.get("tail_rot", 0))
    im.alpha_composite(b.rotate(-pose.get("body_rot", 0), Image.BICUBIC, expand=False) if pose.get("body_rot") else b, (int(round(ox)), int(round(oy))))
    return im


def stand_pose():
    return {"legs": {"leg_nf": (0, False), "leg_nb": (0, False), "leg_ff": (0, False), "leg_fb": (0, False)}}


# ---------- ciclo de andar ----------
GAIT = {"leg_nf": 0.0, "leg_fb": 0.0, "leg_ff": 0.5, "leg_nb": 0.5}       # pares diagonales: cercana delantera + lejana trasera, y al revés
BETA = 0.60                                                                # fracción del ciclo con el pie apoyado
SWING = 24.0                                                               # semi-amplitud del paso (grados)

def _ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def walk_pose(phase, amp=SWING, beta=BETA):
    """pose a la fase `phase` (0-1, un ciclo = dos pasos). El pie que apoya recorre de +amp a -amp (el cuerpo avanza por encima);
    en el balanceo la pata va plegada y vuelve de -amp a +amp."""
    legs = {}; cos_stance = []
    for name, off in GAIT.items():
        u = (phase + off) % 1.0
        if u < beta:
            ang = amp * (1 - 2 * u / beta); folded = False; cos_stance.append(math.cos(math.radians(ang)))
        else:
            sw = (u - beta) / (1 - beta); ang = -amp + 2 * amp * _ease(sw); folded = 0.12 < sw < 0.88
        legs[name] = (ang, folded)
    L = 0.5 * (leg_len("leg_nf") + leg_len("leg_nb"))
    dy = L * (1 - max(cos_stance)) if cos_stance else 0.0                  # el cuerpo baja lo justo para que la pata de apoyo más baja toque el suelo
    return {"legs": legs, "body_dy": dy + 2.5 * math.sin(2 * math.pi * 2 * phase), "tail_rot": 6 * math.sin(2 * math.pi * phase), "body_rot": 0}

def advance_per_cycle(amp=SWING, beta=BETA):
    """cuánto avanza el cuerpo (px de la pieza) en un ciclo: lo que barre un pie en el apoyo, repartido en la fracción `beta`"""
    L = 0.5 * (leg_len("leg_nf") + leg_len("leg_nb"))
    return 2 * L * math.sin(math.radians(amp)) / beta
