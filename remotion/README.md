# Versión Remotion en paralelo (prueba, desde 21/11/2026)

Cada noche, DESPUÉS de que `FACTORY.md` haya publicado el reel con Python, una segunda tarea hace **la misma pieza otra vez con Remotion**, solo para compararlas. **No publica nada, no gasta créditos de ElevenLabs y no toca `factory/*.py`, `videos/*.mp4` anteriores ni `log/`.** Python sigue siendo el motor principal y el respaldo.

## Regla de oro: la versión Remotion no puede «ver» la de Python
Parte de los mismos materiales de origen y diseña las escenas por su cuenta. Está **prohibido** abrir, leer o mirar:
- `factory/<slug>.py`, `factory/<slug>_v4.py` y cualquier otro script de escenas de `factory/*.py` (salvo `mascot.py`, `sfx.py`, `library.py` para el exportador);
- `factory/out/`, el mp4 y la portada de `videos/`, y los fotogramas o QA de Python;
- el texto de los pasos de `FACTORY.md` sobre cómo se construyó ese reel (sí puedes leer 6e anti-slop y 6f).
Sí puedes usar: el guion, la voz, la música, los tiempos de palabras, `factory/library/index.json` y sus sprites, y el gato por piezas.

## Pasos
1. **Elegir el reel:** la entrada de hoy (fecha Europe/Madrid) de `log/published.json`. Si no hay, termina sin hacer nada y sin notificar. Del log usa solo `slug` y `title`.
2. **Instalar:** `cd remotion && npm install`. Navegador: si existe `/usr/bin/google-chrome` úsalo con `--browser-executable=/usr/bin/google-chrome --chrome-mode=chrome-for-testing`; si no, `npx remotion browser ensure`. Si ninguno funciona, termina con una notificación de una línea («Remotion: sin navegador»).
3. **Exportar materiales:** lee `factory/voice/<slug>_script.txt` y `factory/library/index.json`, decide qué bibliotecas te sirven y ejecuta, desde `factory/` (`pip install --break-system-packages pocketsphinx` si falta):
   `python3 ../remotion/export_raw.py <slug> --libs lib1,lib2`
   Deja en `remotion/public/` voz, música, guion, palabras, sprites (`spr/<lib>__<nombre>.png`), piezas del gato, fuentes, efectos, `mouth.json` y `meta.json` (nº de fotogramas).
4. **Diseñar las escenas** en `remotion/src/scenes/<slug>.tsx` y poner `export * from './<slug>'` en `src/scenes/current.ts`. Tomas como plantilla `src/scenes/overnight_charging.tsx` (es código Remotion mío de otro reel, no de Python) y `src/common.tsx` (Title, Label, Item, Battery, HeatWaves, fondos Grad/Stars/Skyline/Dunes/Pines/Card/Rays, Grain). El módulo exporta: `SC` (escenas [id, inicio, fin] en segundos, cortadas en los límites de frase de `public/words.json`; la última es el cierre en bucle y termina en `DUR`), `CATS` (escenas con gato), `Bg`, `Content`, `SFX`, `SWAP_AT`, `CURIOUS`, `DUR`. Reglas:
   - Texto en pantalla en inglés. Cada escena con su propio fondo y un elemento visual distinto (nada de dos escenas seguidas iguales). Aplica `FACTORY.md` 6e (anti-slop) y 6f.
   - Subtítulos van aparte (palabra a palabra, en `Subs.tsx`): no repitas en una etiqueta lo que ya dicen.
   - Deja aire: ilustraciones y etiquetas no se tocan ni se solapan; nada en la franja derecha baja (x > 900, y > 900) ni en los 220 px superiores. Los objetos dentro de una tarjeta quedan a ≥ 40 px del borde y de otras etiquetas.
   - **La primera escena (gancho) debe verse COMPLETA desde el fotograma 0** (título, ilustración y gato ya en pantalla, sin animación de entrada; solo movimiento suave): el primer fotograma tiene que servir de portada. `Reel.tsx` hace en los últimos 0,35 s un fundido de la última escena al gancho (`Content` de la primera escena con `t=0`), así que el bucle cierra solo. La plantilla `overnight_charging.tsx` es antigua y empieza en blanco; sigue `first_thanksgiving.tsx` para el gancho.
   - Usa MUCHAS ilustraciones (a la usuaria le gusta más así): en cada escena, el elemento principal más 1-2 personajes (`pilgrim_man`, etc., 32 poses con nombres de gesto: talk, point, think, shrug, worried, happy, amazed...) u objetos de apoyo; los sprites son pequeños, no los amplíes más de ≈1,3× (tarjetas grandes ≈2×).
   - Ninguna ilustración tapa un texto: comprueba en los fotogramas que Title/Label/subtítulos quedan por encima o separados ≥ 30 px (el orden de dibujo manda: lo último tapa lo anterior). Etiquetas dentro de una tarjeta como máximo hasta y=1290; los subtítulos anchos van en y=1390.
   - Todo es función de `t`/`T` (nada de `Math.random`, CSS `transition` ni animaciones por CSS).
5. **Revisar:** `npx tsc --noEmit -p .`; renderiza 12 fotogramas repartidos con `npx remotion still src/index.ts Reel out/s_<n>.png --frame=<n>` y mira la hoja de contacto. Corrige solapes, texto cortado y bocas raras antes de renderizar. Para las bocas: `CatTest` (composición) muestra las 10 formas ampliadas.
6. **Portada:** `npx remotion still src/index.ts Reel renders/<YYYY-MM-DD>_<slug>_remotion_cover.png --frame=0` (con la opciones de navegador del paso 2). Debe mostrar el gancho completo y legible.
6b. **Renderizar:** `npx remotion render src/index.ts Reel out/<slug>.mp4 --concurrency=2 --crf=16` (+ las opciones de navegador del paso 2). Después normaliza el audio sin tocar el vídeo: `ffmpeg -y -i out/<slug>.mp4 -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11 -c:a aac -b:a 192k renders/<YYYY-MM-DD>_<slug>_remotion.mp4` y mide con `ffmpeg -i <fichero> -af ebur128=peak=true -f null -` (objetivo ≈ −15 LUFS).
7. **Subir:** commit y push a `main` SOLO de `remotion/` (`src/scenes/<slug>.tsx`, `current.ts`, el mp4 de `remotion/renders/`). Borra de `remotion/renders/` los mp4 de más de 7 días. No subas `public/`, `node_modules/` ni `out/`.
8. **Notificar:** una notificación de máximo 4 líneas en español: título del reel, duración, tiempo de render, y 1-2 defectos que veas tú mismo (solapes, bocas, bucle). El enlace es `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/remotion/renders/<fichero>`.

## Lo aprendido (19-21/11/2026)
- Cada boca se alinea con su borde superior bajo la nariz y se escala desde ahí; la máscara del cuello solo afecta a la cabeza (no a la boca). La boca ancha (`ah`) se acorta a 0,72 y la redonda se agranda poco.
- El render completo tarda ≈ 4-5 min con 2 CPU. El audio sale a ≈ −20 LUFS y se sube a −15 con `loudnorm` tras el render.
- Fallos conocidos de la plantilla: grano y contorno simples; el gato queda algo más blando que en Python.
