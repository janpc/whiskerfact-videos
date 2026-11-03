# Gato v4: prompts de Gemini (3/11/2026)

Objetivo: más expresión de cara y un cuerpo para el gato, sin cambiar su diseño. Se adjunta siempre la hoja actual del gato (`v3/sheet_base.png`) como referencia de estilo. Todas las hojas: fondo verde #00FF00 plano, sin texto, sin degradados ni brillos, contorno marrón oscuro algo más grueso que el de v3, sin relieve.

Cómo se recortan hoy las hojas (`v3/parts.py`): la base y las bocas se alinean por la NARIZ; los ojos se alinean por las GAFAS y la nariz. De cada hoja de ojos solo se usa la zona de las gafas más un margen por encima: orejas, forma de cabeza e inclinación NO pasan al vídeo.

Decisiones del 3/11/2026:
- El gato lleva **rebeca verde oliva abierta sobre camisa crema, con pajarita granate**. El sprite v3 actual es un busto con camisa crema y sin rebeca; el cuerpo nuevo la añade.
- La cabeza (v3) se recorta por el cuello y el cuerpo nuevo aporta cuello, pajarita y rebeca. Pendiente de comprobar en Code que el encaje queda limpio.
- Las cejas expresivas van en la hoja de ojos (dibujadas por Gemini, encima de las gafas).

## 1. Hoja de ojos y cejas (3x3)

```
Create a NEW image in the style of the attached cat character sheet, keeping the SAME cat exactly: grey tabby, round dark brown glasses, amber eyes, pink nose.
NEW eye and eyebrow expressions: head and shoulders, front view, identical framing, size and position in every cell, glasses and nose fully visible. Ears, head shape, whiskers and the closed relaxed smile stay IDENTICAL in all cells; ONLY the eyes and eyebrows change.
One image with a 3x3 grid of equal square cells, listed left to right, top to bottom:
1 surprised: wide round eyes, both eyebrows high
2 curious: one eyebrow raised high, eyes wide
3 skeptical: one eyebrow raised, eyes half-closed
4 deadpan: flat eyebrows, half-lidded eyes, no emotion
5 amused: eyes bright with a slight squint, eyebrows relaxed
6 proud: eyes closed in a calm smile, eyebrows slightly raised
7 thinking: eyes looking up and to the side, one eyebrow raised
8 excited: very wide eyes, both eyebrows high and curved
9 worried: eyebrows tilted up in the middle, eyes wide
Small clear dark brown eyebrows just ABOVE the glasses, same outline thickness as the glasses.
Flat 2D cartoon style, clean dark brown outlines, flat colours, no gradients, no gloss.
Perfectly flat pure green background (#00FF00). No labels, text or borders. Exactly 3x3 cells.
```

## 2. Hoja del cuerpo, de cintura para arriba y sin cabeza (3x3)

```
Create a NEW image in the style of the attached cat character sheet, keeping the SAME cat design: grey tabby fur, dark brown outlines, garnet bow tie.
NEW body poses for this cat, WITHOUT the head (the head is added separately): waist-up, front view, from the neck down. Each body ends at the collar: cream shirt collar with the garnet bow tie centred on it; the area above the collar is left empty (flat green).
Outfit: open olive green cardigan over a cream shirt. Grey tabby paws with simple rounded fingers. Tail visible when it fits.
The collar and bow tie are at the SAME position and size in every cell, so the head can be placed on top.
One image with a 3x3 grid of equal square cells, listed left to right, top to bottom:
1 stand_neutral: arms relaxed at the sides
2 arms_crossed: arms crossed over the chest
3 point_right: right arm extended to the side, pointing
4 hand_on_chin: one paw raised to the chin, the other arm across the body
5 shrug: both paws raised palms up, shoulders up
6 paw_up: one paw raised, as when explaining
7 hands_on_hips: both paws on the hips
8 holding_book: holding a closed book against the chest
9 wave: one paw waving hello
Flat 2D cartoon style, clean dark brown outlines of uniform thickness (slightly thicker than the reference), flat colours, no gradients, no gloss.
Perfectly flat pure green background (#00FF00). No labels, text, borders, ground or shadows. Exactly 3x3 cells.
```

## 3. Pendiente

- Hoja de **bocas con actitud** (formato de `v3/sheet_mouths.png`, 4x3): sonrisa torcida, plana, preocupada, risa grande. Las 12 bocas actuales ya cubren los fonemas.
- Hoja de **cuerpo entero** (de pie, caminando, sentado) para la clase del gato.
- Recortar las hojas nuevas (ampliar `parts.py`), integrarlas en `mascot.py` y hacer la prueba de un fotograma antes de tocar la fábrica.
