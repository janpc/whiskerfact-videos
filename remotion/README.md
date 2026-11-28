# Motor de vídeo de Mr. Whiskerfact (Remotion, oficial desde el 28/11/2026)

La fábrica nocturna (`FACTORY.md`) construye y publica cada reel con este proyecto. El motor antiguo en Python está retirado y guardado en la rama `python-engine` (solo como respaldo). Las reglas editoriales y de diseño están en `FACTORY.md` pasos 6 a 6f; aquí están los pasos técnicos y lo aprendido.

## Gato: cambios de pose
Corte seco con un saltito (`Reel.tsx`); nunca fundido entre dos poses, porque el gato se transparenta y parece que desaparece (26/11).

## Fondos y suelo
**Fondos:** las imágenes de `refs/fondos/` son **solo una referencia de estilo, no un catálogo: los fondos NO deben ser siempre los mismos.** En cada reel crea combinaciones y fondos nuevos según el tema (cielos, paletas, terrenos, interiores, mar, espacio...); si hace falta, amplía `common.tsx`. `Landscape`, `Card` y `Rays` son los bloques base.

**Suelo:** los personajes (y objetos de calle, como la farola) van con `Stand`, que los apoya en `FLOOR` con sombra de contacto; nunca con `Item` flotando. Un salto usa `lift`. `check.mjs` falla («flota») si un personaje no toca el suelo. Evita ciclos de andar (`walk1-4`) y poses quietas deslizándose.

Sí puedes usar: el guion, la voz, la música, los tiempos de palabras, `factory/library/index.json` y sus sprites, y el gato por piezas.

## Pasos
Antes: guion verificado, voz descargada, `tighten.py` y `align.py` ejecutados (`FACTORY.md` pasos 3-5).
1. **Instalar:** `cd remotion && npm install`. Navegador: si existe `/usr/bin/google-chrome` añade a los comandos `--browser-executable=/usr/bin/google-chrome --chrome-mode=chrome-for-testing`; si no, `npx remotion browser ensure`.
2. **Exportar materiales**, desde `factory/`: `python3 ../remotion/export_raw.py <slug> --libs lib1,lib2 --category <categoría>`. Deja en `remotion/public/` voz, música (o base de reserva), guion, palabras, sprites, gato, fuentes, efectos, `mouth.json` y `meta.json`.
3. **Escenas:** `src/scenes/<slug>.tsx` y `export * from './<slug>'` en `src/scenes/current.ts`. Plantilla: `src/scenes/week_7_days.tsx`, **cambiando el gancho por `CoverBg` + `CoverTitle`**. Exporta `SC` ([id, inicio, fin] en segundos, cortes en límites de frase de `public/words.json`; la última es el cierre en bucle y termina en `DUR`), `CATS`, `Bg`, `Content`, `SFX`, `SWAP_AT`, `CURIOUS`, `DUR`. Texto en inglés. Todo es función de `t`/`T` (nada de `Math.random`, `transition` ni animaciones CSS). Los subtítulos van aparte (`Subs.tsx`). Etiquetas dentro de una tarjeta como máximo hasta y=1290; subtítulos anchos en y=1390. Usa `Big`, `Tick`, `Cross`, `Title`, `Label`, `Item`, `Stand`, `Medallion` de `common.tsx` (llevan `data-box`; el comprobador solo ve esos).
4. **Comprobar:** `npx tsc --noEmit -p .`, `node check.mjs --step 0.5 --overlay out/check` (fotogramas con fallos en `out/check/`), `TIMES='[...]' node sheet.mjs` (hoja de contactos) y algunos fotogramas a tamaño completo (`npx remotion still src/index.ts Reel out/s.png --frame=<n>`). `CatTest` muestra las bocas ampliadas.
5. **Música:** `FACTORY.md` 6b (corte mudo con `--muted`, generar, volver a exportar).
6. **Render:** `npx remotion render src/index.ts Reel out/<slug>.mp4 --concurrency=2 --crf=16`, y normaliza el audio: `ffmpeg -y -i out/<slug>.mp4 -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11 -c:a aac -b:a 192k -movflags +faststart ../videos/<YYYY-MM-DD>_<slug>.mp4`. Portada: `npx remotion still src/index.ts Reel ../videos/<YYYY-MM-DD>_<slug>_cover.png --frame=0`.
7. **Control final:** `node final_check.mjs ../videos/<fichero>.mp4 --length <standard|short>`.
8. **Commit** de `remotion/src/scenes/`, `videos/` y lo que pida `FACTORY.md`. No subas `public/`, `node_modules/` ni `out/`.

## Lo aprendido (19-21/11/2026)
- **Bocas:** `export_raw.py` genera una imagen ya ajustada por fonema (`public/cat/mouth_<fonema>.png`: labio superior a la misma altura y una sola línea de nariz continua) y `Cat.tsx` solo la superpone. No mover ni escalar bocas en Remotion (mover la imagen entera duplicaba la nariz, 26/11). La máscara del cuello se aplica a la base de la cabeza (obligatoria: sin ella asoma la ropa antigua sobre la rebeca, 26/11), no a la boca. Tras tocarlas, mirar `CatTest`.
- El render completo tarda ≈ 4-5 min con 2 CPU. El audio sale a ≈ −20 LUFS y se sube a −15 con `loudnorm` tras el render.
- Pendiente de mejora: grano y contorno simples; el gato se ve algo blando.

- (23/11) Botones: la escena de lightning_vs_sun tenía 24 fallos de colocación (objetos con x≈850-950 bajo y=900, solapes VS/sol, «2»/sol, tick/cruz, «z z z»). Se recolocó todo con centro óptico ≈ x=485 y los subtítulos de Remotion ahora usan el mismo ancho que Python (anchos: x 70-900; con gato, x 500-900). `check.mjs` queda como paso fijo.
- (26/11) Bucle: los últimos 6 fotogramas son el primero y el fundido acaba antes; en `Bg`, la última escena ya recibe `T - DUR` (no restar otra vez: los rayos saltaban). `check.mjs` falla («bucle») si no coinciden. Un busto (dibujo cortado por la cintura) va en `Medallion`, nunca apoyado en el suelo.
- (23/11) Bucle: `Reel.tsx` dibuja el ÚLTIMO fotograma con T=0 (idéntico al primero: ojos curiosos del gancho, sin respiración, mismo grano) y en los últimos 0,35 s hace el fundido al gancho. No hace falta tocarlo en cada escena, pero el gancho (primera escena) debe ser estático en t=0 y el gato del gancho usar `CURIOUS`/`SWAP_AT` como en `lightning_vs_sun.tsx`. Medido: primer vs último fotograma = 0 en el render directo y 0,6/255 en el mp4 (compresión).
