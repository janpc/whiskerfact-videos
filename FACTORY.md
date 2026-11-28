# Mr. Whiskerfact: nightly reel factory

This is the run book the scheduled task follows every night. One run makes one reel from idea to published post, without human input.
All public-facing content is in **English**. **The video engine is Remotion (`remotion/`, official since 28/11/2026).** The old Python/PIL renderer is retired; it is kept only in the git branch `python-engine`, as a backup. Never switch to it on your own. The Python files left in `factory/` only prepare materials (voice tightening, word timings, sprite library, cat parts, backup music). Brand constants (category colours, length limits, voice) are documented in `factory/brand.py`.

## 0. Setup
- Clone this repo. Materials scripts run from `factory/` (Python 3, PIL, numpy, scipy, scikit-image, pocketsphinx, ffmpeg; install anything missing with `pip install --break-system-packages`). The video is built in `remotion/` (Node; `npm install`).
- Read `factory/brand.py` and `remotion/README.md` fully before writing anything.
- Read `schedule.json` and `log/published.json`.
- **Write as you go** (2/11/2026: a run once stalled after scheduling and left no log, no credits and no check). Never keep important state only for the end of the run:
  - **Credits:** right after each ElevenLabs call (voice, music, image, transcription), add its line to `growth/credits.json` and update `estimated_balance` (rules in step 10), then commit and push.
  - **Log:** right after scheduling the posts (step 8), write the log entry (step 9) and push, before anything else.
  - Keep the run lean: no extra renders or reviews beyond what this file asks. The whole run should finish in well under 3 hours.

## 1. Is today a publishing day?
- `schedule.json` holds `daily_first` (5), `daily_from` (a date) and `then_gaps` ([2, 3]).
- **From `daily_from` (Europe/Madrid date) onwards, publish EVERY day** and ignore the gap rules below (decided 23/11/2026, 1 reel a day). Each daily reel needs its entry in `growth/week_plan.json` with a `storyboard` and its illustration sheet already in the library; if the entry or the sheet is missing, say so in the notification.
- Count the published entries in `log/published.json`. Entries with a `note` containing "test" don't count.
- While that count is below `daily_first`, publish every day.
- After that, the gaps between reels alternate 2 days, then 3 days, and so on. Use the gap that follows the previous one, which gives about 12–13 reels a month.
- Publish only if at least that many days have passed since the last published entry.
- If today is not a publishing day, stop quietly: no notification, no commit.

## 1b. Read the voice of the channel
- Read `PERSONALITY.md` and `FORMATS.md` in full. Every script is written by Mr. Whiskerfact in that personality, inside its hard limits, and in today's format.
- Record `variants.format` and `variants.personality` in the log.

## 2. Topic
- **Weekly plan first:** if `growth/week_plan.json` has an entry for today's date, use its topic, category and format. Still verify everything (step 3); if the topic fails verification, choose another one with the rules below and say so in the notification. Use the characters, objects and illustrations it lists from the library (`factory/library`). **If the entry has a `storyboard` field, read that file first (`growth/storyboards/<date>_<slug>.md`) and build the reel from it:** use its script as the starting point (re-verify the facts marked pending and re-check length), and place scene by scene the illustrations its table names (in Remotion: `<Item lib="week_w48" name="wall_calendar" .../>`, or `<Stand>` for characters), with the sizes, positions and movements it gives. Do not swap them for shapes drawn in code, except the code effects the storyboard lists. If a scene would need an illustration that is not in the library, say so in the notification instead of improvising it. Before rendering, check every sprite name in the storyboard exists in `factory/library/index.json`. If the entry has an `experiment` field, apply its `test` and `option` for today (see "Experiments" in step 8) and do not substitute another option.
- **Special dates first:** read `growth/calendar.json`. Make a themed reel today if both of these are true:
  - an event falls within the next 7 days;
  - fewer than that event's `reels` themed videos are already in the log (field `event`).
- A themed reel can use any category that fits.
- Publish it no later than 14:00 Madrid on the event day. Never publish one after the event.
- **Category:** otherwise, the next one in `brand.ROTATION` after the last *regular* (non-themed) log entry.
- **Topic:** an evergreen curiosity in that category that is not already in the log, and that suits today's format (FORMATS.md). Sensitive topics are fine if told neutrally (PERSONALITY.md); skip current political controversies. It must be phrased as a question a curious adult would stop scrolling for.
- **Demand check:** pick from `growth/topics.md` first, taking the highest-scored idea for the category. Otherwise write 5 candidate questions and score each from 0 to 3 on three things:
  - **(a) People ask it:** the exact question, or a close variant, appears in search results as a common question ("People also ask", forums, Q&A sites, news explainers).
  - **(b) It has a surprising answer:** a twist the viewer would not guess.
  - **(c) It's easy to show:** a clear mechanism to draw.
- Use WebSearch for (a). Choose the highest total. Add the other 4 to `growth/topics.md` with their scores for later nights.
- Avoid questions where the top results are debunks we can't verify, and topics that are a single trivia number with no "why".
- **Hook:** at most 10 words. **Both lines are fully on screen from frame 0** (the cover template draws them, see step 6), because viewers decide in the first second. The question never appears late, and something in the drawing moves within the first 0.3 s. **The hook scene IS the channel cover (decided 13/11/2026, template A «rays»):** build it with `CoverBg` and `CoverTitle` from `remotion/src/common.tsx`, see step 6. The first frame is also the cover, so it must read well on its own. Use the hook style that `growth/experiments.json` assigns today (see step 8).
  - **First-second rule (15/11/2026, after the analysis: Instagram reach depends on the 3-second skip rate; reels with 44%+ skips stayed under ~340 views, those under 42% reached 1,300+):** the most surprising image or number of the video is visible and moving in the first second, not just the title. No title-only card. **Silent test:** look at the first 3 s of the contact sheet with no sound; if the viewer cannot tell what is strange or what the question is, redo the opening scene.

## 3. Verify
- Every fact in the script must be confirmed by **two independent, reliable sources**, for example a university, a museum, NASA or NOAA, a peer-reviewed review, or Britannica.
- Prefer recent sources and check that the fact is still current.
- Record both URLs for each claim. If a claim can't be confirmed twice, cut it.
- **Precision check: do this after writing the script (step 4) and before generating the voice.** Write `factory/voice/<slug>_claims.md` with one row per factual sentence of the script. Each row contains:
  - the sentence;
  - the exact supporting sentence quoted from source 1, with its URL;
  - the exact supporting sentence quoted from source 2, with its URL;
  - **match**: yes, or no plus the reason.
- **Strictly flag these:**
  - **Absolute words:** every, all, always, never, only, no one, first, biggest, fastest. The source must say exactly that. Otherwise soften the wording ("most", "almost", "one of the").
  - **Numbers and dates:** they must match the sources. Round only in the safe direction ("about 10,000").
  - **Cause and effect:** "X causes Y" needs a source that says so, not one that only shows a link.
  - **Simplifications that become false:** "each hair has a muscle" is false, because eyelashes and eyebrows have none.
  - **Popular myths:** check them against a debunk source.
  - **Animal or mouse studies:** say so ("in mice").
- **Independent review.** Then launch a separate reviewer (the Agent tool) that has not seen your drafting. Give it only the script and the source URLs, and ask it to find any sentence a pedantic expert would call wrong or misleading.
- Fix every point it raises, or cut the sentence. Never generate the voice before the claims file is all "yes" and the reviewer has no open points.
- Commit the claims file with the reel.

## 4. Script
- **Length (profile chosen by the `length` test, 15/11/2026):** read today's option in `growth/experiments.json` (`length`, assigned by the week plan; no entry means the control `standard`). **Retention comes first** in both profiles: the shortest script that tells the whole story wins.
  - `standard`: usually 160–190 words (63–75 s), **hard cap 210 words**. The final check fails under 61 s and warns above 85 s.
  - `short` (test B2-length): **115–150 words (45–58 s), hard cap 150 words**. The final check fails under 42 s and warns above 62 s. One idea, no side stories: keep the hook, the surprise, the payoff and the closing line, and drop the second example. Run the final check with `--length short` (`node final_check.mjs <mp4> --length short`). Record `variants.length` (`standard` or `short`) and `variants.experiment`.
  - Over 1 minute only matters for TikTok Creator Rewards (10,000 followers and 100,000 views in 30 days), which is far away for now; growth comes first.
  - **Word-count gate (added 6/11/2026, before paying for the voice):** run `wc -w factory/voice/<slug>_script.txt`. The final reel lasts about `words / 2.77 + 4.2` seconds after `tighten.py` (226 words gave 86.2 s, over the QA warning; wifi_bands with 223 words gave 85.6 s). If the script has more words than the cap of today's profile (210 standard, 150 short), cut it until it passes. Cutting words is free; regenerating the voice costs about 1,300 credits. The raw ElevenLabs take is about 12% longer than the final audio, so a raw take of 90 s is normal and not a reason to regenerate.
- **Share moment (decided 15/11/2026; Instagram weights DM sends heavily for reaching new people):** **at most ONE share ask per video, counting the script, the on-screen text and the caption together**, and only when the video has a fact that is truly curious or controversial (both sources agree, and a normal person would want to show it to someone). Never on an ordinary sentence and never twice. Mark that fact `shareable: yes` in the claims file; with no such fact the video has no share ask at all. Form: right after that fact, one short line of at most 8 words in the cat's voice, for example "Send this to someone who still believes it." Never invent drama to qualify: the fact must hold up on its own. The line must follow from that exact fact and read as part of the story, not as a call to action stuck on top (16/11/2026: "Send this to your stargazing friend" after "Earth never sets" felt forced to the owner). If it does not flow, leave the share ask for the caption. Record `variants.share_ask` as `script`, `caption` or `none`.
- **Retention rules (every format):** a new visual or idea at least every 3–4 s; no scene longer than ~8 s without a change; tease the payoff early ("the answer is weirder than you think") and pay it off late; cut any sentence that only repeats or warms up.
- **Language:** plain English that is not childish. Name each complex term, then explain it in one sentence.
- **Structure:** use **the structure of today's format in `FORMATS.md`**, not one fixed template. `brand.STRUCTURE` is only the timing guide for `explainer`.
- **Loop ending (mandatory from the reel of 17/11/2026 on; decided by the owner on 16/11):** the reel has **no outro**: no slogan, no cat circle. The **last sentence of the script is a bridge**: it stays open and is completed by the hook's first words when the video replays, so the end and the start read as one sentence. Example: hook "Does Earth ever rise or set?" → last line "And that's exactly why, if you stood on the Moon and asked…". Rules: the bridge is the very last thing said (nothing after it); it must make grammatical sense joined to the hook's opening words (read them aloud together before paying the voice); it must not sound like a goodbye ("thanks", "see you", "class dismissed", "stay curious" are banned at the end). Record `variants.closing` as `loop` plus the bank type of the line before it, if any. **How to make it flow (16/11/2026: the owner found a test where the end only cut back to the hook "not fluid, not coherent"):**
  1. **Write the hook and the bridge together, as one sentence split in two.** Write the joined sentence first ("…so every astronaut up there ends up asking: does Earth ever rise or set?"), then cut it: the tail goes at the start of the video, the head at the end.
  2. **The hook must start with the joinable words.** No preface before them ("Picture yourself…", "Okay, so…"): the first spoken words are the ones the bridge hands over to.
  3. **The bridge ends with a lead-in that grammatically needs what comes next**, so the ear waits for it: "…which is exactly why people ask", "…and that brings us right back to the question", "…so the real question is". Never end on a complete statement ("…never.") followed by an unrelated hook.
  4. **It must follow from the last fact**, not jump: the bridge comments on what was just said and turns it into the hook's question or claim.
  5. **Voice:** write the bridge without a final full stop (end on the lead-in word, or a colon) so Brad does not drop his intonation as if the video had ended. Listen to the take: if it sounds like a goodbye, rewrite before paying a second take.
  5b. **Opening order for quiz / myth hooks (rule from 21/11/2026, owner):** the video must NOT open with the label «Pop quiz» or «Myth or fact» as its first words. Say the **question or claim first**, then the label (e.g. «What was NOT at the first Thanksgiving? Pop quiz time.»). Reason: the loop bridge has to join the hook's first words; if the hook starts with «Pop quiz:», the ending cannot refer back to it grammatically, whereas a question first lets the last line point back at it. The cover title (LINE1/LINE2/SUB) may still show the label. Applies from the next reel on.
  6. **Check before paying the voice:** write the joined sentence in the log as `variants.loop_join` and read it aloud. If it needs a filler word to make sense, rewrite it.
  7. **Visual join:** see step 6 («Loop ending, no outro»).
  The first loop reel (18/11/2026): after scheduling it, tell the owner in the notification that it is the first loop reel and send the joined sentence, so she can check it in the day before 20:30. The slogan "Class dismissed. Stay curious." goes as the last line of the caption instead.
- **Closing line (optional, just before the bridge):** one line from the closing bank in `FORMATS.md`. Never the same closing type as the previous reel, and avoid the type used most in the last 5 reels. **The `ask` closing (a question the viewer answers in the comments) goes in at most 1 reel out of 3 and only when the topic really invites an answer the viewer can give from their own experience (e.g. "close your eyes and imagine an apple: what do you see?"); never forced, never on every video (decision of 16/11/2026).** Record it as `variants.closing`. Never announce the next video.
- Never announce the next video.
- Each scene opens with a distinctive first word, so scene cuts can be found in the transcript.

## 5. Voice (ElevenLabs connector)
- Use `creative_generate_speech` with these settings:
  - voice `Dslrhjl3ZpzrctukrQSN` (Brad)
  - model `eleven_v4`
  - flow `Q4RWsQia6pHRGabsab5B`
- Generate the whole script, closing line included, in **one** call, with `generations_count: 1`. The default of 2 doubles the cost.
- Poll `creative_get_flow_run_status` until it is done. Never repeat a generation call, because each call is charged.
- Download the mp3 from the URL the generation status returns (today that is `elevenlabsusercontent.com`; older runs got `storage.googleapis.com`) to `factory/voice/<slug>_brad.mp3`. Both domains are allowed in the account's network settings (Settings > Capabilities > allowed domains; fixed on 6/11/2026 after the voice downloads failed with a 403 on 1/11, 3/11 and 6/11). **Make one single download attempt.** If it fails, never generate the voice again: commit the credits note with the flow, node and generation ids and send the failure notification starting with "⚠️ NO PUBLICADO HOY" (step 10) so the owner can download the take by hand.
- Save the exact script as `factory/voice/<slug>_script.txt`.
- Tighten the voice first: run `python3 tighten.py voice/<slug>_brad.mp3`. It shortens pauses to about 0.24 s, speeds the voice up by `brand.VOICE_TEMPO` and keeps the original as `_raw.mp3`. Always run it before alignment.
- Get free word timings with local forced alignment: `python3 align.py voice/<slug>_brad.mp3 voice/<slug>_script.txt voice/<slug>_brad_words.json`. Install it first with `NO_PROXY= pip install --break-system-packages pocketsphinx`.
- If a proper name is missing from the dictionary, add its phones to `EXTRA_PHONES`.
- Only if alignment fails, fall back to `creative_transcribe_audio` (about 400 credits).
- If the free tier is "busy", wait about 10 minutes and poll or retry once. If it still fails, go to step 10.
- The slogan audio (`factory/voice/slogan_brad.mp3`) is no longer used in new reels (loop ending, step 4); it stays only for re-rendering old ones.

## 6. Build the reel (Remotion)
Follow **`remotion/README.md`** for every technical step: export the materials, write `remotion/src/scenes/<slug>.tsx`, check, render and run the final check. This section holds the editorial and design rules.
- **Hook = cover (same template for every reel):** the first scene uses `<CoverBg cat angle>` and `<CoverTitle cat line1 line2 sub>`: category colour with slowly rotating rays, brand and category on top, a title of two lines (about 9 characters per line; line 2 in yellow) and the hook question. One main illustration (plus 1-2 small ones) between y 860 and 1230, clear of the cat. **Everything is on screen from frame 0** (it is the thumbnail), and something moves within 0.3 s.
- **Story:** each scene opens on a sentence boundary, lasts 3-7 s (hard limit 8 s), and something changes at least every 2 s. A visual punch about every 10 s. Every visual accent has its sound effect.
- **Many illustrations** (the owner likes it that way): in each scene the main element plus 1-2 supporting characters or objects, from the library (`factory/library/index.json`) and the storyboard. Do not replace a storyboard illustration with a shape drawn in code; code is for diagrams, numbers and effects. Library sprites are small: no more than about 1.3x (about 2x on large cards).
- **At most 1 ElevenLabs sheet per reel**, with the rules of PLAN.md step 5b/5c, only if `growth/credits.json` shows room. If a needed illustration is missing, say so in the notification.
- **Backgrounds vary in every reel.** `remotion/refs/fondos/` are style references only, never a catalogue: new skies, palettes, terrains, interiors, sea or space according to the topic. Consecutive scenes never share a background. Read `variants.look` of the last 3 log entries, do not repeat the combination, and record today's.
- **Ground:** characters and street objects stand with `Stand` (contact shadow), never floating. No walk cycles, no still pose sliding. A bust goes in `Medallion`.
- **Calm animation:** few clear moves, held poses, soft easing; never jitter or constant bouncing.
- **The cat** appears only in the hook, the last scene before the loop and the loop (at most 1 scene in 3, never on card scenes). Pose changes are a hard cut with a small hop, never a cross-fade.
- **Layout:** nothing past x=900 below y=900 (app buttons), nothing in the top 220 px or below y=1540; labels of 3 words or fewer, on screen at least 1.5 s, dark on cream cards and readable on a phone; no text covered by a drawing. On-screen text follows the same precision rules as the script. Do not repeat in a label what the subtitles already say.
- **Loop ending, no outro:** the last 6 frames equal the first one (`Reel.tsx` does it), and the last scene flows visually into the cover (same rays and main illustration).

## 6b. Music composed for this reel (ElevenLabs)
- Export the materials (without a music file the exporter writes a synthetic backup bed) and render a silent cut: `npx remotion render src/index.ts Reel out/silent.mp4 --muted --concurrency=2` (+ browser options).
- Commit it as `videos/music_src/<slug>_silent.mp4`, push, and attach it to flow `Q4RWsQia6pHRGabsab5B` with `creative_attach_reference_file` (raw GitHub URL with the commit hash).
- Run `creative_generate_in_flow` with `node_type: "video-to-music"`, `model_id: "eleven_video_to_music_v1"`, `generations_count: 1`, `connect_from` the attached node, and a 2-3 sentence **sound** prompt: genre and mood for the category and topic (see `MUSIC.md` if present), instruments, tempo, how the energy moves, "instrumental, sparse mid-range so a narrator sits on top". Never repeat the call (about 960-1,300 credits).
- Download to `factory/voice/<slug>_music.mp3`, run the exporter again and render the final video. If music fails, publish with the backup bed and say so in the notification.
- Delete `videos/music_src/*` in the next commit.

## 6c. Quality checks (mandatory)
- Before rendering: `npx tsc --noEmit -p .` and `node check.mjs --step 0.5 --overlay out/check` (buttons, edges, overlaps, grounding, loop, short-lived text). **Any FAIL blocks publishing.** Look at every WARN.
- Contact sheet (`node sheet.mjs`) and a few full-size frames: **look at them yourself** for what the script cannot see: low text contrast (it is not measured automatically), odd mouths, a drawing that shows the wrong thing, soft or ugly sprites, dull or repeated scenes. Then apply 6e.
- After the render: `node final_check.mjs <mp4> --length <standard|short>` (size, duration, loudness, peaks, black frames, loop). **Any FAIL blocks publishing.**
- Log `"qa": {"fails": 0, "warns": N}` and add "QA ✅" (or the warnings, in short) to the notification.

## 6e. Anti-slop (17/11/2026): que no parezca IA en serie
Checklist completa en el proyecto de claude.ai (`checklist-anti-slop.md`). Resumen para aplicar **con la hoja de contactos, antes del render completo**:
- **Planos:** lista de escenas con plano, color dominante y qué hay de nuevo cada 3-4 s. Dos escenas seguidas no repiten plano ni composición. El gato sale como máximo en 1 de cada 3 escenas, y solo en las que no llevan tarjeta.
- **Ilustración:** cada objeto significa algo en esa escena (sin decorado de relleno); un protagonista por escena; paleta corta (color dominante + 1 de apoyo + acento amarillo solo en la palabra clave); contorno plano y grueso, sin brillos ni degradados; algo de imperfección hecha a mano (contorno con ruido bajo, sin simetría perfecta). Rechazar imágenes con manos raras, texto inventado, objetos duplicados o estilo distinto.
- **Movimiento:** pocos movimientos y con motivo; variar entrada y salida (no el mismo tipo más de 2 veces seguidas); entrada escalonada de palabras y objetos; rebote solo en 1-2 momentos; escenas con gráfico o dato, quietas.
- **Ritmo:** alternar escenas rápidas (2-3 s) con alguna más larga (5-6 s) donde cae lo importante.
- **Preguntas de la hoja (sí/no; con 3 o más «no», rehacer antes de renderizar):** ¿cada escena se distingue de la anterior a primera vista? ¿hay ≥3 colores dominantes? ¿cada objeto tiene un porqué? ¿el gato sale solo donde aporta? ¿hay algún detalle hecho a mano? ¿los textos se leen sin tapar nada? ¿se confundiría con el vídeo anterior sin el texto?
- **Ronda de crítica con puntuación (19/11/2026, de las skills Motion Reel y animation-studio):** antes del render completo, mira la hoja de contactos **a tamaño completo y también reducida a la mitad** (lo que se ve en un móvil a un brazo) y puntúa de 1 a 10: gancho (los 3 primeros segundos, sin sonido), legibilidad en móvil, calidad del movimiento, variedad entre escenas, fidelidad al estilo de marca y sincronía con la voz. Elige los 3 peores problemas, corrígelos y repite la hoja. **Máximo 3 rondas; se renderiza cuando todas las notas son ≥7** (la hoja tarda mucho menos que el render). Anota las notas finales y los 3 cambios en `variants.slop_check`.
- **Prohibidos por defecto (señal de vídeo de plantilla):** título centrado sobre degradado, todo apareciendo con fundido, etiquetas de esquina y marcos, brillo en elementos de interfaz, explosiones de partículas genéricas. Cada entrada necesita dirección, peso y un motivo.
- **Cortes:** el primer fotograma de un corte ya muestra la imagen nueva (nunca un fotograma en blanco ni un destello a pantalla completa); máximo 1-2 destellos de pantalla completa por vídeo, en momentos de estructura (el giro, el cierre). Un barrido (whip) es un desplazamiento con las dos imágenes a la vez en pantalla. Los zooms van en espacio logarítmico (`s = a * (b / a) ** p`): da velocidad constante; una interpolación lineal se queda grande demasiado tiempo.
- **Golpes de sonido:** cada acento visual importante (aparición del dato, giro, cierre) lleva un efecto de sonido en ese mismo fotograma, y no se pone un golpe fuerte encima de una palabra hablada. Si falta sincronía, se arregla en la línea de tiempo del guion, no desplazando a mano un lado.
- **Una sola tipografía de título y una de apoyo, y un solo color de acento** salvo que la escena pida otra cosa.
- La variedad de color y de cortes se revisa a ojo en la hoja de contactos. Anota en el log `variants.slop_check` con las respuestas «no» y qué se cambió.

## 6f. Si la usuaria pide cambios antes de la hora de publicación
Corrige la escena, repite los controles, renderiza, sube el mp4 **con un nombre nuevo** (`..._v2.mp4`) y la portada, y sustituye el vídeo de los 3 posts de Buffer con `edit_post` (solo `postId` y `assets`; texto, hora y metadatos se conservan).

## 7. Upload
- Copy the final mp4 (the normalised one, README step 6) to `videos/<YYYY-MM-DD>_<slug>.mp4`, then commit and push to `main`.
- Also copy the thumbnail to `videos/<YYYY-MM-DD>_<slug>_cover.png` (frame 0, README step 6).
- Check that `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/videos/<file>` returns 200 for both the mp4 and the cover png.

## 8. Publish (Buffer connector)
Desde el 24/11/2026 se publica con **Buffer** (plan gratis), no con Metricool. Se usa el conector de claude.ai «Buffer» (herramientas `create_post`, `edit_post`, `list_posts`, `get_post`, `delete_post`). Organización «My organization», id `6b0492eb2977e5ad81690395`, zona horaria `Europe/Madrid`.
- **Canales (ids fijos):** TikTok `6b0493c48541f09ecb7bc60a`, YouTube `6b04939e8541f09ecb7bc487`, Instagram `6b04934b8541f09ecb7bc0e7`. Si `list_channels` no los devuelve o alguno sale `isDisconnected`, no programes ese canal y avísalo en la notificación.
- **Se crean 3 posts, uno por canal** (Buffer no tiene un post multi-red), con `create_post`: `mode: customScheduled`, `dueAt` con el desfase de Madrid (`+01:00` en invierno, `+02:00` en verano; hora futura), `schedulingType: automatic`, `assets: [{video: {url: <raw.githubusercontent de videos/<fichero>.mp4>, metadata: {thumbnailOffset: 0}}}]`. Buffer no admite portada propia: la portada es el fotograma 0, que ya es la portada del vídeo. Si falla una red, las otras siguen.
  - **Límites del plan gratis (comprobados el 24/11/2026):** 3 canales, **10 posts programados a la vez en toda la organización** (cada red cuenta aparte, así que un reel ocupa 3), 2 publicaciones al día en YouTube, 25 en TikTok y 50 en Instagram. Ya no hay tope mensual de 20. Los borradores no cuentan. **Antes de crear:** `list_posts` con `status: [scheduled]`; si ya hay 8 o más, no hay hueco para los 3 posts: no programes, avísalo en la notificación («⚠️ Sin huecos en Buffer: hay N posts programados») y para.
  - TikTok se publica automáticamente. Anota `variants.tiktok_mode: "api"`. **No crees un cuarto post solo para una red.**
  - Guarda los 3 ids en el log como `buffer_post_ids: {"tiktok": ..., "instagram": ..., "youtube": ...}` (los reels anteriores a esta fecha tienen `metricool_uuid`).
- **Inmediatamente después de crear los posts**, añade la entrada del log con lo que ya se sabe (campos del paso 9), haz commit y push. Luego sigue con 8b. El paso 9 solo la completa.
- **Experiments (one variable per batch):** read `growth/experiments.json` and choose every option before writing the script, because the hook style changes the script.
  - A test with status `fixed` always uses its `control` option. Do not rotate it. (From 15/11/2026 the `length` test is `testing` and `hook_style` is `fixed`; the active batch is `next_batch` B2-length, see below.)
  - The test with status `testing` uses the option in today's `week_plan.json` `experiment` field. If the plan has no entry for today, alternate: use the option with fewer videos in `log/published.json` (the `batch.control` and `batch.variant` options only), and use role `base` when today is a themed special-date reel.
  - `format` is `varied` on purpose (not an experiment): follow its rule.
  - Record `variants.experiment` as `{"batch": ..., "test": ..., "option": ..., "role": "variant"|"control"|"base"}`.
- **Time:** use the `time_slots` option chosen today, on today's date (Madrid). If the test is `decided`, follow its rule.
- **Special dates:** a themed reel goes in the earliest slot that still falls before the event.
- **Text:** this is the same text for all three networks, and it is also the YouTube description. Write it in this order:
  1. the hook;
  2. one line in today's `caption_style`;
  3. a call to action, rotating these (pick the one used least in the log, and record it as `variants.cta`):
     - "🐱 Follow for more curious facts."
     - "💾 Save this for your next trivia night."
     - "👇 Tag someone who needs to know this."
     **One share ask per video in total (see the share moment in step 4):** if the script already has one, the caption uses Follow or Save; "Tag someone" only goes in the caption when the video has a `shareable` fact and the script has no share line;
  4. one short sources line naming the institutions, for example "Sources: Harvard, Cell (2020)". No URLs;
  4b. (from 17/11/2026, loop ending) the slogan on its own line: "🎓 Class dismissed. Stay curious.";
  5. 3–5 hashtags in English (15/11/2026: more specific than before): `#mrwhiskerfact`, the topic, **one niche tag for the category** (animals `#animalfacts`, science/space `#sciencefacts`, history `#historyfacts`, tech `#techfacts`, body `#humanbody`) and `#didyouknow` or `#funfacts`. Add the event hashtag on special dates.
  Keep it under 400 characters.
- **TikTok** (`metadata.tiktok`): `isAiGenerated: true`. El título del vídeo sale del `text`. Ya no hay `privacyOption` (público por defecto) ni `autoAddMusic` (la música ya va dentro del mp4).
- **Instagram** (`metadata.instagram`): `type: reel`, `shouldShareToFeed: true`, `isAiGenerated: true`.
- **YouTube** (`metadata.youtube`): `title` = la pregunta + ` #shorts`, `categoryId` `"27"` (Education) o `"28"` (Science & Technology, para ciencia, espacio y tecnología), `privacy: public`, `madeForKids: false`, `isAiGenerated: false`. Buffer no tiene etiquetas (tags) ni tipo «short» (un vertical de menos de 3 min ya lo es): las 5 etiquetas se quitan y la descripción es el `text`.
- **No borres el mp4 de GitHub hasta que los 3 posts estén `sent`:** Buffer lee el vídeo desde la URL y no está confirmado si lo copia al crear el post.

## 8b. Schedule the post check
- Right after the three posts are created, create a one-shot scheduled task with the Claude_Code_Remote connector (`create_trigger`):
  - `run_once_at`: the publish time + 30 minutes (UTC)
  - `name`: "Mr. Whiskerfact check <slug>"
  - `notifications`: `{"push": true}`
  - `initiation`: `"human_schedule"`
  - prompt: "Clone janpc/whiskerfact-videos (attach it with push access if needed), read CHECK.md and follow it for the reel '<title>' (slug <slug>), Buffer post ids TikTok <id>, Instagram <id>, YouTube <id> (mode <tiktok_mode>), scheduled at <ISO time Europe/Madrid>. Never publish or edit posts."
- **Safety net:** at the start of every nightly run, look in the log for any published entry from the last 3 days without a `check` field and with its time already passed. Run CHECK.md for it inline and include the result in tonight's notification.

## 9. Log and clean-up
- Complete the entry written in step 8 in `log/published.json` (append it now if it is somehow missing):
  - the date, category, slug, title, hook, sources (URLs), the three Buffer post ids (`buffer_post_ids`) and the scheduled time
  - `duration_s`
  - `variants.engine: "remotion"`
  - `event` (themed reels only)
  - `variants`, as in `{"time_slot": "20:30", "hook_style": "statement", "caption_style": "teaser"}`. Include `format`, `personality`, `cta`, `closing`, `tiktok_mode`, `look`, `share_ask` and `experiment` too. Reels made from 2026-11-16 also carry `"quality_changes": ["first_second_rule", "share_rule", "niche_hashtags"]` (15/11/2026, applied in the middle of batch B2-length as quality improvements that are not measured as a test; the review must mention them when it explains a result). The weekly review needs these to compare results.
- Delete `videos/*.mp4` older than 7 days, then commit and push.

## 10. Notify
- Send one push notification. On success it gives the title, category, scheduled time and duration.
- On failure it gives the step that failed and why. **Never publish a reel that failed a check.**
- **Credits:** the account is on the ElevenLabs Starter plan, which allows commercial use. There is no tool that reads the balance, so `growth/credits.json` is the ledger:
  - (done right after each call, see step 0) one line in `spent` for every ElevenLabs call of the run: `{"date", "slug", "what", "credits"}`, using the real cost if the tool reports it, otherwise `costs_estimate`;
  - subtract the run's total from `estimated_balance`;
  - credits renew on day `renewal_day` (30) of each month: the first run on or after that day (and not yet done this month) sets `estimated_balance` to `monthly_allowance`, notes it in `spent` as a renewal line, and asks the owner for the real balance in the notification. Never add credits otherwise. When the owner gives the real balance, overwrite `balance_checked` and `estimated_balance` with it.
  If `estimated_balance` is below `warn_below`, or will not cover the next reel, add to the notification: "Quedan pocos créditos de ElevenLabs (~N). Dime el saldo real o recarga."
- If ElevenLabs refuses for lack of credits, do not publish anything. Say exactly that in the notification.
