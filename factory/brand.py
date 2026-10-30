"""Mr. Whiskerfact — reglas de diseño compartidas por todos los reels.

Todo vídeo importa este módulo: colores, tipos, zonas y tiempos salen de aquí,
nunca escritos a mano en la escena. Cambiar algo aquí lo cambia en todos.
"""

# ---------- lienzo ----------
W, H, FPS = 1080, 1920, 30
ENCODE = dict(codec="libx264", preset="veryfast", crf=20, pix_fmt="yuv420p")
DURATION = (65, 75)          # segundos, objetivo 68: TikTok (Creator Rewards) solo paga vídeos de MÁS de 1 minuto
MIN_DURATION = 61            # límite duro con cierre incluido; el render se niega por debajo
SCRIPT_WORDS = (165, 190)    # palabras del guion (con frase de cierre): con tighten.py Brad va a ~170 ppm -> 65-75 s con el cierre

# ---------- zonas (px, eje y) ----------
# Instagram/TikTok tapan arriba y abajo: nada importante fuera de SAFE.
SAFE_TOP, SAFE_BOTTOM, SAFE_SIDE = 250, 1540, 70
ZONES = {
    "brand":        (262, 318),   # nombre del canal + barra de progreso
    "title":        (350, 600),   # título de la escena, máx. 2 líneas
    "subtitle":     (620, 720),   # apoyo, máx. 2 líneas
    "illustration": (740, 1370),  # ilustración protagonista, centro (540, 1055)
    "caption":      (1390, 1540), # texto de pantalla o subtítulos de voz, máx. 2 líneas
}
TEXT_MAX_W = W - 2 * SAFE_SIDE   # 940
# Botones de TikTok/Instagram/YouTube (me gusta, comentar, compartir) tapan la franja derecha de la mitad baja.
# Por debajo de y=RAIL_TOP nada importante (subtítulos, etiquetas, partes clave del dibujo) pasa de x=SAFE_RIGHT_LOW.
RAIL_TOP = 900
SAFE_RIGHT_LOW = 900
SUBS_MAX_W = 800                                  # subtítulos de voz: de x=85 a x=885
SUBS_CENTER_X = (SAFE_SIDE + SAFE_RIGHT_LOW) / 2   # 485, desplazados a la izquierda de los botones
ILLU_CENTER = (540, 1055)

# ---------- color ----------
# El fondo es un degradado vertical oscuro del color de la categoría (ver bg_for).
BG_BASE = (6, 8, 16)          # casi negro del que se parte
BG_MIX = (0.16, 0.34)         # cuánto color de categoría arriba / abajo
TEXT = (246, 244, 238)        # texto principal
TEXT_2 = (196, 201, 216)      # texto secundario (≥4.5:1 en los seis fondos)
LINE = (210, 225, 255)        # contornos finos de ilustración
GOLD = (255, 199, 74)         # marca: aro del avatar, acentos del canal
WARM_LIGHT = (255, 196, 110)  # brillos y luz

CATEGORIES = {   # orden de rotación
    "science": dict(label="SCIENCE", color=(59, 130, 246)),
    "nature":  dict(label="NATURE",  color=(34, 197, 94)),
    "history": dict(label="HISTORY", color=(249, 115, 22)),
    "body":    dict(label="BODY",    color=(239, 68, 68)),
    "space":   dict(label="SPACE",   color=(139, 92, 246)),
    "tech":    dict(label="TECH",    color=(250, 204, 21)),
}
ROTATION = list(CATEGORIES)
CHIP_TEXT = (14, 18, 36)      # texto oscuro sobre la pastilla de categoría

def bg_for(category):
    """(arriba, abajo) del degradado de fondo para una categoría"""
    c = CATEGORIES[category]["color"]
    return tuple(tuple(round(BG_BASE[i] + (c[i] - BG_BASE[i]) * k) for i in range(3)) for k in BG_MIX)

def accent_text_for(category):
    """color de categoría aclarado para palabras resaltadas sobre su propio fondo"""
    c = CATEGORIES[category]["color"]
    return tuple(round(c[i] + (255 - c[i]) * 0.45) for i in range(3))

def surface_for(category):
    """pista de barras y tarjetas: el color de categoría al 50 % sobre el fondo"""
    c = CATEGORIES[category]["color"]
    return tuple(round(BG_BASE[i] + (c[i] - BG_BASE[i]) * 0.5) for i in range(3))

# ---------- tipografía (Inter Display) ----------
FONT_DIR = "/usr/share/fonts/opentype/inter/"
TYPE = {  # nombre: (peso, tamaño px, interlineado)
    "hook":     ("Black",    92, 1.15),   # pregunta del gancho
    "title":    ("Black",    84, 1.15),   # título de escena
    "number":   ("Black",   120, 1.00),   # cifra protagonista
    "subtitle": ("Medium",   44, 1.25),
    "body":     ("SemiBold", 46, 1.25),   # texto en zona caption
    "voicesub": ("SemiBold", 54, 1.20),   # subtítulos de la voz
    "label":    ("SemiBold", 38, 1.20),   # etiquetas de ilustración
    "brand":    ("SemiBold", 30, 1.00),   # nombre del canal, mayúsculas
    "chip":     ("Bold",     28, 1.00),   # pastilla de categoría
}
MAX_LINES = {"hook": 3, "title": 2, "subtitle": 2, "body": 2, "voicesub": 2, "label": 2}

# ---------- movimiento ----------
ENTER = 0.30      # s, entrada: fundido + subida de 30 px, ease-out cúbico
EXIT = 0.25       # s, salida: fundido
RISE = 30         # px

# ---------- ritmo ----------
MAX_STATIC = 2.0          # s máximos sin que cambie algo en pantalla
SCENE_LEN = (3.0, 7.0)    # s, duración de cada escena (nunca más de 8)
INTERRUPT_EVERY = 10.0    # s, un golpe visual (zoom, destello, reacción de la mascota)
MAX_PAUSE = 0.4           # s máximos de silencio en la voz (tighten.py deja las pausas en ~0,24 s)
VOICE_TEMPO = 1.07        # tighten.py acelera la voz un 7 % sin cambiar el tono
VOICE_WPM = (165, 180)    # palabras por minuto de la voz, ya ajustada con tighten.py
HOOK_MAX_WORDS = 10
FIRST_CHANGE = 0.3        # s, primer cambio visual: algo se mueve casi de inmediato (golpe de entrada en 0)
def read_time(text):          # tiempo mínimo en pantalla de un texto
    return 1.0 + 0.3 * len(text.split())
MAX_TEXT_BLOCKS = 2           # bloques de texto a la vez, sin contar marca

# ---------- estructura de un reel de 60 s ----------
STRUCTURE = [   # (sección, inicio s, fin s)
    ("hook", 0, 3),          # pregunta o gancho en pantalla desde el fotograma 0
    ("context", 3, 15),      # qué es / partes
    ("steps", 15, 45),       # 2-3 pasos numerados, uno por escena
    ("fact", 45, 56),        # dato sorprendente: cifra o comparación animada
    ("wrap", 56, 63),        # frase de cierre que responde al gancho y vuelve a su imagen ("Now you know: …")
    ("outro", 63, 68),     # animación de cierre del gato + eslogan; nunca anunciar el vídeo siguiente
]

# ---------- mascota ----------
MASCOT = dict(
    name="Mr. Whiskerfact",
    file="out/mrwhiskerfact_avatar_v3.png",          # gato por piezas (mascot.py), también foto de perfil
    hook=dict(size=260, pos=(70, 1420), enter=0.6),     # asoma abajo a la izquierda, DEBAJO del dibujo (nunca encima)
    outro=dict(module="outro5.frame", size=640, center=(540, 1060), dur=3.6,    # el gato dice el eslogan (labios sincronizados), guiña y sonríe
               sfx="sfx.OUTRO_GAFAS"),                  # igual en todos los vídeos
)

SLOGAN = "Class dismissed. Stay curious."

# borde oscuro en los textos (estilo del videoclip de la autora): legibles sobre paisajes y momentos psicodélicos
TEXT_STROKE = {"voicesub": 4, "title": 3, "hook": 4, "subtitle": 3, "number": 4}
TEXT_STROKE_COLOR = (44, 32, 30)   # palabra a palabra en GOLD bajo el gato

# ---------- subtítulos ----------
SUBS_MODE = "word"        # cada palabra aparece cuando se pronuncia
SUBS_WORD_FADE = 0.08     # s
SUBS_WORD_RISE = 8        # px
SUBS_BLOCK_EXIT = 0.2     # s, al acabar la frase
SUBS_NO_VOICE_WPS = 3.0   # palabras/s cuando no hay voz

# ---------- audio ----------
VOICE_LUFS = -16          # voz integrada
VOICE = dict(provider="elevenlabs", voice_id="Dslrhjl3ZpzrctukrQSN", name="Brad",     # narrador americano de documental
             model="eleven_v4", offset=0.3)   # entra a los 0,3 s; tiempos por palabra con eleven_scribe_v1
# El narrador también dice el eslogan en el cierre (audio aparte), y cada palabra aparece al pronunciarse.
# Flujo de voz: guion -> generate_speech -> transcribe_audio (tiempos de cada palabra) -> escenas cortadas
# entre frases -> subtítulos palabra a palabra -> mezcla con música y efectos atenuados bajo la voz.
MUSIC_UNDER_VOICE_DB = -20
MUSIC_ON = True           # música generada por music.py, tonalidad según la categoría
MUSIC_STYLE = "documentary_upbeat"   # documental con ritmo: ostinato de cuerdas, piano en motivo y bombo suave
MUSIC_PEAK_DB = -22       # muy bajita: por debajo de los efectos y, con voz, unos 20 dB bajo ella
MUSIC_DUCK_DB = -8        # cuánto más baja mientras habla la voz
SFX_UNDER_VOICE_DB = -14  # efectos por debajo de la voz
SFX = {                   # qué suena con cada gesto visual (sfx.py)
    "enter_text": "tap",          # palabra o bloque que aparece (sin voz encima)
    "punch": "whoosh",            # zoom de golpe
    "flash": "sparkle",
    "counter": "click",           # cada salto grande de un contador
    "bar_grow": "whoosh",
    "mascot_pop": "pop",
}
SFX_MAX_PER_SECOND = 2    # nunca más de dos efectos por segundo

# ---------- publicación ----------
PUBLISH = dict(
    via="metricool",                                  # conector de claude.ai: createScheduledPost
    mode="auto",                                      # totalmente automático, sin revisión previa
    networks=["tiktok", "instagram", "youtube"],      # TikTok, Instagram Reels, YouTube Shorts
    when="best_time",
    frequency=dict(daily_first_days=True, then_every_days=2),   # uno al día al arrancar, luego cada dos días                                 # getBestTimeToPostByNetwork, el mismo día del render
    tiktok=dict(privacyOption="PUBLIC_TO_EVERYONE", autoAddMusic=False),
    youtube=dict(type="short", madeForKids=False, category="EDUCATION", privacy="public"),
    instagram=dict(type="REEL"),
    caption="hook + 1 línea + 3-5 hashtags (#mrwhiskerfact + categoría + tema)",
    notify="push",                                    # aviso al móvil con el enlace y el resumen
)
