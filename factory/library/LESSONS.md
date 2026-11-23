# Lecciones de las hojas de ilustraciones (se actualiza sola)

Lo lee el plan semanal antes de escribir los prompts de las hojas, y lo amplía cada vez que una hoja sale con defectos (ver `PLAN.md`, paso de hojas). Una línea por lección: qué pasó, fecha, regla que se aplica desde entonces.

## Orden obligatorio
1. Guion de voz → 2. guion visual escena por escena (`growth/storyboards/`) → 3. inventario sacado de esa tabla → 4. prompt de la hoja. **Nunca** al revés: una ilustración que ninguna escena usa sobra, y una escena sin ilustración se anota como pendiente.
2. Una hoja 4x4 a 2K por vídeo. **La primera generación no se consulta a la dueña** (decidido el 23/11). Si falla la comprobación, se regenera la hoja entera con el inventario o prompt corregido (no se edita), como máximo una vez sin preguntar; más veces, o saldo <8.000, se le pregunta.

## Receta que funciona (23/11/2026)
- UNA sola referencia: `growth/style_ref_objects_4x4.png`, «úsala SOLO para el estilo, no dibujes nada de lo que aparece». Con varias referencias o un collage se contamina y salen blancos y figuras repetidas.
- Rejilla: «exactamente 4 columnas × 4 filas de celdas cuadradas idénticas, un elemento por celda, ninguno más alto ni ancho que su celda, cada uno una sola vez, fondo verde puro #00FF00 en todas partes, sin blanco, marcos ni divisores».
- Tamaño: BIG ≈85 % de la celda, el resto ≈65 %.
- Coste a 2K con una referencia: 918 créditos. Editar la hoja con IA cuesta 609 y NO es fiable (devuelve 16:9 y rompe la rejilla).

## Lecciones
Cualquier línea que contenga `PROMPT: <frase en inglés>` se añade sola al final del prompt de todas las hojas (`factory/weekly_sheets.py prompt`). Úsalo para reglas que el prompt debe repetir siempre.

- 23/11 · Gemini dibuja caras sonrientes en objetos (taza) → pedir «los objetos NO tienen cara, ojos ni sonrisa».
- 23/11 · Pinta letras en los objetos («DAILY NEWS», inscripción de la moneda) → pedir «sin texto, letras ni números pintados»; las etiquetas van en la capa de texto.
- 23/11 · **No sabe contar**: relojes con 12 marcas aunque pidas 10; calendarios con 7 columnas aunque pidas 10. Cualquier elemento cuyo número importa (marcas, columnas, dedos, pasos) se corrige por código sobre el sprite (reloj y rejilla en `week_w48`), no se confía en el prompt.
- 23/11 · Una ilustración «ancha» (fila de varios objetos) ocupa dos celdas y se come la vecina; y sale sobre barra NEGRA. Si se pide una tira, contar que ocupa 2 celdas, recortarla por manchas (`library.py` `add_blobs`) y quitar el negro conectado al borde. Los elementos de la tira se pueden recortar como sprites sueltos (Saturno salió así, pequeño: 186 px).
- 23/11 · Sombras o halo verde alrededor de un objeto claro (huellas): la limpieza automática por umbral las destruye; regenerar el objeto con «sin brillo ni halo detrás» en vez de limpiar.
- 23/11 · Personajes enteros cortados en la cintura cuando pedimos una escena con persona: describirlos «de rodillas para arriba, entero dentro de UNA celda».

## Comprobación de cada hoja (checklist antes de recortar)
1. 16 celdas llenas, cada elemento una vez, ninguno cortado ni tocando otro.
2. Sin caras en objetos, sin texto pintado, sin blanco.
3. Elementos con número (marcas, columnas, pasos): contados; si fallan, corregir por código.
4. Todo lo que pide el guion visual está y nada sobra.
5. Después de recortar: anotar aquí lo que haya fallado, con fecha y regla.

- 23/11 · Para que una tira ancha (varios objetos en fila) no se coma la celda vecina: PROMPT: For any single horizontal strip item, keep it on a flat green background with no black bar behind it.
