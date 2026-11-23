# Mr. Whiskerfact: nightly reel factory

This is the run book the scheduled task follows every night. One run makes one reel from idea to published post, without human input.
All public-facing content is in **English**. All design rules live in `factory/brand.py`, so never hard-code colours, fonts, timings or positions in a scene.

## 0. Setup
- Clone this repo and work in `factory/`. Python 3, PIL, numpy, scipy and ffmpeg are expected. Install anything missing with `pip install --break-system-packages`.
- Read `factory/brand.py` fully before writing anything.
- Read `schedule.json` and `log/published.json`.
- **Write as you go** (2/11/2026: a run once stalled after scheduling and left no log, no credits and no check). Never keep important state only for the end of the run:
  - **Credits:** right after each ElevenLabs call (voice, music, image, transcription), add its line to `growth/credits.json` and update `estimated_balance` (rules in step 10), then commit and push.
  - **Log:** right after scheduling the posts (step 8), write the log entry (step 9) and push, before anything else.
  - Keep the run lean: no extra renders or reviews beyond what this file asks. The whole run should finish in well under 3 hours.

## 1. Is today a publishing day?
- `schedule.json` holds `daily_first` (5) and `then_gaps` ([2, 3]).
- Count the published entries in `log/published.json`. Entries with a `note` containing "test" don't count.
- While that count is below `daily_first`, publish every day.
- After that, the gaps between reels alternate 2 days, then 3 days, and so on. Use the gap that follows the previous one, which gives about 12–13 reels a month.
- Publish only if at least that many days have passed since the last published entry.
- If today is not a publishing day, stop quietly: no notification, no commit.

## 1b. Read the voice of the channel
- Read `PERSONALITY.md` and `FORMATS.md` in full. Every script is written by Mr. Whiskerfact in that personality, inside its hard limits, and in today's format.
- Record `variants.format` and `variants.personality` in the log.

## 2. Topic
- **Weekly plan first:** if `growth/week_plan.json` has an entry for today's date, use its topic, category and format. Still verify everything (step 3); if the topic fails verification, choose another one with the rules below and say so in the notification. Use the characters, objects and illustrations it lists from the library (`factory/library`). **If the entry has a `storyboard` field, read that file first (`growth/storyboards/<date>_<slug>.md`) and build the reel from it:** use its script as the starting point (re-verify the facts marked pending and re-check length), and place scene by scene the illustrations its table names (`LIB.place(img, sheet, pose, ...)`, e.g. `LIB.place(img, "week_w48", "wall_calendar", ...)`), with the sizes, positions and movements it gives. Do not swap them for shapes drawn in code, except the code effects the storyboard lists. If a scene would need an illustration that is not in the library, say so in the notification instead of improvising it. Before rendering, check every sprite name in the storyboard exists in `factory/library/index.json`. If the entry has an `experiment` field, apply its `test` and `option` for today (see "Experiments" in step 8) and do not substitute another option.
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
- **Hook:** at most 10 words. **Both lines are fully on screen from frame 0** (the cover template draws them, see step 6), because viewers decide in the first second. The question never appears late, and something in the drawing moves within the first 0.3 s. The engine adds an entry punch at frame 0. **The hook scene IS the channel cover (decided 13/11/2026, template A «rays»):** build it with `factory/cover.py` (`draw_bg`, `draw_header`, `draw_title`), see step 6. The first frame is also the cover, so it must read well on its own. Use the hook style that `growth/experiments.json` assigns today (see step 8).
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
  - `standard`: usually 160–190 words (63–75 s), **hard cap 210 words**. The renderer refuses under 61 s and QA warns above 85 s.
  - `short` (test B2-length): **115–150 words (45–58 s), hard cap 150 words**. The renderer refuses under 42 s and QA warns above 62 s. One idea, no side stories: keep the hook, the surprise, the payoff and the closing line, and drop the second example. **Run every render, QA and `reel.py` command with `REEL_LENGTH=short`** (for example `REEL_LENGTH=short python3 <slug>.py render`), otherwise the `standard` limits apply and the render fails. Record `variants.length` (`standard` or `short`) and `variants.experiment`.
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

## 6. Build the reel
- Use `factory/pyramids.py` as the template: a single file that builds on `voice_reel.VoiceReel`. That module handles scene cuts, subtitles, the outro and the audio mix. Write `factory/<slug>.py` the same way.
- **Hook = cover (mandatory, same template for every reel):** use `factory/cover.py` in the `hook` scene (see `bone_vs_steel.py`). Backdrop: `V.backdrop("hook")(lambda img, T, t: cover.draw_bg(img, CATEGORY, 0.05 * T))` (colour of the category from `brand.CATEGORIES`, slowly rotating rays). Scene body: draw the 1-2 illustration items large in the centre (`item(...)`, bobbing a little so something moves within 0.3 s), then `cover.draw_header(img, CATEGORY)` and `cover.draw_title(img, LINE1, LINE2, SUB, a=clamp((e - T) / B.EXIT))`. Do not call `R.chrome` or `V.hook_text` in this scene. `LINE1`/`LINE2` = a short title in two lines (e.g. «Bone vs / steel», max about 9 characters per line at 150 px; it appears in capitals, line 2 in yellow), `SUB` = the hook question (text in step 2). Keep the illustration between y 860 and 1300, away from the cat (top at y 1190, x 95-375, v4 cat) and with nothing below y 900 past x 900. Never prepend a separate 1-frame or 0.2 s cover to the video: it flashes when the reel loops.
- **Thumbnail:** render the same layout as a still with `cover.make_cover(CATEGORY, LINE1, LINE2, [(lib, name, x, y, h, rot), ...], "videos/<date>_<slug>_cover.png", sub=SUB)` (same item positions as the hook scene).
- Every scene starts with a distinctive word from the script.
- Split long sentences into extra scenes (the hard limit is 8 s).
- Sync animations to words with `V.word_time()`.
- Run `python3 <slug>.py times`, then `preview t1 t2 ...`, then `render`.
- The illustrations must be simple vector shapes drawn with PIL that show the real mechanism.
- Keep the rhythm rules:
  - something changes at least every 2 s
  - each scene lasts 3–7 s
  - a visual punch about every 10 s
  - every animation has its sound effect
- The background uses the category colour (`brand.bg_for`). Subtitles appear word by word with the voice.
- **The look is the author's videoclip style (`factory/style.py`; reference: `factory/goosebumps.py`).** The engine already adds a dark brown outline to every drawing (`VoiceReel.INK`) and a dark stroke to titles and subtitles (`brand.TEXT_STROKE`). Each scene gets a backdrop with `@V.backdrop("<scene>")`:
  - **Library sprites keep their own outline.** `LIB.place` marks them so the automatic outline skips them, but only when it draws straight onto the frame. If a sprite is first placed on an intermediate layer (to recolour it, add a phase shadow, rotate it…) and that layer is then composited, mark it with `mark_noink(layer, pos)` (see `moon_earth_view.py`). Otherwise the engine traces every inner edge in thick brown (2026-11-16: Earth and Moon looked smudged, the Moon like noise). Check this in the contact sheet.
  - **Close-ups** (cutaways, diagrams, objects): `ST.card(img, CARD)`, the warm cream card. Labels on the card must be dark (`ST.OUTLINE`, or a dark accent such as `(176, 40, 58)`), never the light category colours, and thin elements that sit on the card (hair, lines) must be dark too.
  - **Outdoor, animals, people, history scenes:** `ST.landscape(img, T)` (sunset, layered forests with parallax) or `ST.landscape(img, T, night=True)` (night with twinkling stars). Stand figures on the ground at y≈1330.
  - **Sky, space, cold, mystery:** a night sky (`ST.sky` + `ST.stars`).
  - **Psychedelic moments are rare and only for the truly crazy beat.** Use one only when the fact is genuinely mind-blowing (the twist, the "wait, what?" moment): `ST.wow_moment(img, T, t0, R.cat, "swirl"|"blobs"|"glitch", dur=1.3–1.6)`. Use 0–1 per reel; many reels have none. Never put one behind an explanation, a diagram or labels. It opens as a circle from the centre and closes the same way; it never fades.
  - **The hook cat never overlaps the drawing:** it sits bottom-left below the illustration (`brand.MASCOT["hook"]`). If the hook drawing reaches down there, move the drawing up.
  - **Characters (people and animals), recognisable objects and key illustrations come from the library, not from code shapes.** Check `factory/library/index.json` first (`python3 library.py list`), then use `LIB.place(img, name, pose, cx, base_y, height, flip)` in the scene. Animate by moving, flipping and lightly scaling the sprite, and by switching poses; never redraw it with primitives.
    - **Animation feel: calm and readable, as the owner prefers.** Use few, clear moves, held poses and soft easing, and keep secondary motion subtle: bob of 10 px or less, squash of 3% or less, sway of 1–2°. Wing flaps go at about 3 per second, and walk cycles at 8 drawings per second while advancing exactly one stride every 4 drawings (`LIB.stride`). Never jitter, shake or constantly bounce a character. Prefer one character doing one thing well over several busy ones.
    - **If the reel needs a character that is not in the library** and it is central to the story, generate ONE 3×3 sheet with ElevenLabs (the "movement" sheet; the acting sheet only if the story needs expressions) (`creative_generate_image`, `generations_count: 1`, model `gemini-3.1-flash-image`). Use the prompt template in `factory/library/PROMPT.md`, attaching `factory/library/STYLE_REF.png` as a reference when the monthly budget allows. Then add it to the library with `python3 library.py add ... --source elevenlabs` and commit it, so it is never paid for twice.
    - **At most 1 image per reel.** Only generate it if `growth/credits.json` shows enough room: `estimated_balance` minus the image must stay above `warn_below`, and this month's image spending must stay under `image_budget_month`. If there is not enough room, use an object, a silhouette or a different staging instead of the character.
  - **Figures and people:** draw them as clean organic silhouettes (merged shapes, smoothed) in the flat layered style, not as stick or primitive shapes. Animate state changes as one smooth transformation of the same figure (for example, a scalloped fur coat that retracts), not as two figures with an arrow between them.
  - Mix the backdrops so that consecutive scenes don't all look the same, and keep the pace fast (the videoclip's slow rhythm is NOT copied).
- **The style is a REFERENCE, not a template: no two reels may look the same.** What stays fixed is only the identity: outlines, flat colours, layered silhouettes, the cream close-up card, short psychedelic moments, the cat and the outro. Everything else changes with the topic:
  - Pick the world of the topic: `ST.landscape(..., sky_kind=sunset|dawn|dusk|day|storm, terrain=forest|pines|autumn|hills|dunes|waves|city, seed=n)`. A desert reel uses dunes, an ocean reel waves, a history reel its own place, space a starry sky. You can also draw a new backdrop for the topic (a reef, a cave, a street, a lab) in the same flat layered style.
  - Vary the psychedelic moment (`swirl`, `blobs` or `glitch`), where it falls and what it highlights.
  - Vary the compositions: close-up versus wide shot, the side the subject sits on, and silhouettes against the sky versus objects on the card.
  - Before building, read the last 3 log entries' `variants.look` and do NOT repeat the same combination of sky, terrain and psychedelic moment as the previous reel.
  - Record it in the log as `variants.look`, for example `{"skies": ["night","sunset"], "terrains": ["forest"], "wow": ["blobs","swirl"], "card": true}`.
- **Loop ending, no outro (from 17/11/2026):** build the reel with `VoiceReel(R, SLUG, OPENERS, loop=True)`. The engine then ends the video 0.15 s after the last word, with no slogan and no cat circle, and fades the music in 0.25 s so the replay joins cleanly. **The last scene must flow visually into frame 0:** use the hook's backdrop (`cover.draw_bg(img, CATEGORY, ...)`, same category colour and rays) and bring back the hook's main illustration near the hook position, so the jump to the cover is small. Check it in the contact sheet: the last frame and the first frame side by side should look like the same place. Old reels (`loop` left at False) keep the old outro (outro5) when re-rendered.
- Without the outro the reel is ≈4-5 s shorter than before: count that when checking the minimum length of the current length profile.
- **Big, rich drawings:**
  - The main subject must fill the illustration box: at least 60% of its height (about 360 px tall) and 70% of its width. Use a close-up or a cutaway, not a thin strip across the screen.
  - Add a second layer of detail where it helps: texture, small moving parts, labels with leader lines.
  - The engine re-frames each scene automatically (`VoiceReel.autofit`). It scales the drawing up to 1.45× and centres it left of the app buttons, but it cannot make a weak drawing rich, so draw big from the start.
  - Run `preview` and check that no scene shows more empty background than drawing in the band y 760–1370.
- **Nothing may be cut:** keep every drawing of a scene inside the illustration band (y 740–1370). If a drawing crosses the band edge, the engine prints `AVISO encuadre` during `preview` and does not re-frame that scene. Fix the scene (move the element into the band) until no warning appears. Look at the preview for anything cut by the band or by the screen edge.
- **Text inside a drawing** (stamps, signs, numbers, words on objects) must never be painted straight into the illustration.
  - Use `R.txt(...)`, or build the image and place it with `R.put_text(img, spr, x, y, a, anchor, text="...")`. Both go on the label layer, so the automatic outline does not blur the letters, and QA can check them.
  - Render text at its final size. Do not rotate it or scale it after drawing: with resampling the letters go soft. If a stamp must be tilted, keep the tilt small (≤ 8°) and draw the text larger, so that it ends at 100 % or above.
  - Example to avoid: the "MOSTLY MYTH" stamp of 2026-10-31 came out outlined and blurry.
- **Labels must be readable on a phone:** use 3 words or fewer, keep each one on screen for at least 1.5 s (`brand.LABEL_MIN_ON`), and never show it only during a fast transition. Labels are 46 px bold. The engine draws them above the outlines, and a light label gets a dark pill behind it automatically. Never shrink them, and never use the "label" style for long sentences.
- **Titles count as claims too:** on-screen titles and labels follow the same precision rules as the script ("A tiny muscle at the root", not "One tiny muscle per hair").
- **App buttons:** the like, comment and share buttons cover the right edge of the lower half of the screen. Below y=900 (`brand.RAIL_TOP`), no subtitle, label or key part of a drawing may go past x=900 (`brand.SAFE_RIGHT_LOW`). Voice subtitles already respect this (`brand.SUBS_MAX_W`). Place drawings and labels centred slightly left.
- **Music (ElevenLabs, composed for this reel).** After the full render works with the voice, compose the music for the finished cut:
  1. Commit `out/whiskerfact_<slug>/silent.mp4` to `videos/music_src/<slug>_silent.mp4` and push.
  2. Use `creative_attach_reference_file` with its raw GitHub URL on flow `Q4RWsQia6pHRGabsab5B`.
  3. Call `creative_generate_in_flow` with node_type `video-to-music`, model `eleven_video_to_music_v1`, `generations_count: 1` and the uploaded node as `connect_from`. It costs about 960 credits.
  4. Write the prompt about **sound only**: genre, mood, instruments, tempo and how the energy moves with the story (for example, "lifts at each scene change, mystery at the twist, warm resolution"). It must be instrumental, with a sparse mid-range so the narrator sits on top. Match the mood to the topic and category; a space reel should not sound like a history reel.
  5. Download the result to `voice/<slug>_music.mp3`. The engine then uses it automatically, matching its level and ducking it under the voice. Re-run `python3 <slug>.py mux`; there is no need to re-render.
  6. Delete `videos/music_src/` in the next commit.
  7. If music generation fails, keep the synthesized bed and say so in the notification. That alone is not a reason to skip publishing.
- **Contact sheet before the full render (automatic).** `python3 <slug>.py render` first writes `out/<slug>_contact.jpg`: two frames per scene (just after the cut and mid-scene) plus one of the outro, each with the app-buttons zone (x 900–1080, y 900–1700) boxed in red and the time in the corner. **Open it and look at it before the render goes on** (it takes seconds; the render takes ~45 min): check composition, overlapping text, cropped drawings, unreadable colours, and that nothing important falls inside the red box. If something is wrong, stop the render, fix the scene and run `python3 <slug>.py preview` again (same sheet, now at `out/<slug>_preview.jpg`; or `preview t1 t2 ...` for chosen times). **Then run the anti-slop questions of section 6e on the same sheet.**
- **One-second test for any new or risky effect** (a new texture, lettering, stamp or transition): `python3 <slug>.py clip <t0> [seconds]` renders only that second, silent, to `out/<slug>_clip.mp4`. Judge texture and movement there before building the whole scene.

## 6b. Music composed for this reel (ElevenLabs)
- After the full render, upload the silent cut as `videos/music_src/<slug>_silent.mp4` (commit and push). Then attach it to flow `Q4RWsQia6pHRGabsab5B` with `creative_attach_reference_file` using its raw GitHub URL with the commit hash.
- Run `creative_generate_in_flow` with these settings:
  - `node_type: "video-to-music"`, `model_id: "eleven_video_to_music_v1"`, `generations_count: 1`, `connect_from` the attached node
  - a 2–3 sentence **sound** prompt: genre and mood matching the category and topic, key instruments, tempo, how the energy moves (lift at scene changes, tension before the twist, warm resolution), "instrumental, sparse mid-range so a narrator sits on top"
  - never repeat the call (about 960 credits)
- Download the result to `factory/voice/<slug>_music.mp3`, then run `python3 <slug>.py mux`. The engine uses that file automatically and matches its loudness.
- If music generation fails, publish with the synthesized bed: it's still a valid reel.
- Delete `videos/music_src/*` older than 7 days during clean-up.

## 6c. Quality check (mandatory, after the final mix)
- Run `python3 qa.py <slug>`. It samples every scene at 5 fps through the same engine and checks the final mp4:
  - **text contrast**;
  - **overlapping texts**;
  - **texts under the app buttons or off screen**;
  - **on-screen time** of labels (≥ 1.5 s) and titles (≥ 1.2 s);
  - **drawings cut** by the band;
  - **stretches where nothing moves**;
  - **duration, black frames and loudness**.
- It writes `out/<slug>_qa.md` and `out/<slug>_qa.jpg`, with the problems boxed in red.
- **Any FALLO blocks publishing.** Fix the scene: hold the label longer, move it, give the text more room, split the scene. Re-render the affected scenes and run QA again until it exits with 0. AVISOS are allowed but must be looked at.
- **Then look at `out/<slug>_qa.jpg` yourself**, and at a few full frames of each scene. Check what the script cannot see: does the drawing show the right thing, is anything ugly or confusing, does the animation read clearly?
- Put the result in the log (`"qa": {"fails": 0, "warns": N}`), and add "QA ✅" (or the warnings, in short) to the notification.

## 6d. Lecciones de calidad visual (6/11/2026, earth_tunnel) — aplicar al construir cada reel
- **Sprites de la biblioteca (~150-200 px):** no ampliarlos más de ~1,5x. Lo geométrico (Tierra en corte, discos, flechas, túneles, gráficos) se dibuja por código, vectorial y con antialias; los discos grandes no pueden salir dentados.
- **Nada encima de otra cosa:** no dibujar estelas/líneas sobre un elemento ya dibujado (dejan restos); ninguna etiqueta puede tocar la cabeza de un personaje (comprobar solapes a ojo).
- **Letras sobre la tarjeta crema:** estilo `label`, color oscuro, trazo fino, tamaño algo menor; nunca el estilo de subtítulo.
- **Revisión visual obligatoria:** además de la hoja de contactos, extraer 3-4 fotogramas a tamaño completo de las escenas con más dibujos y mirarlos antes de dar el reel por bueno. Si algo se ve blando o dentado, corregirlo antes de publicar.
- **Gato hablando (v4) — OBLIGATORIO en todos los reels (integrado el 18/11/2026; antes salía el avatar fijo del canal por no estar en esta lista, y la usuaria lo vio):** después de escribir `factory/<slug>.py` (con `loop=True`), copia `factory/overnight_charging_v4.py` a `factory/<slug>_v4.py` y cambia solo: el módulo importado (`import <slug> as WB`), el nombre de salida (`whiskerfact_<slug>`), `EYES`, `POSE_PLAN`, `CAT_MODE` y la altura en `draw_cat` (gancho, la última escena con contenido antes del puente, y el puente; nunca en escenas con tarjeta) y quita de `SCENE_COL` las escenas que no existan. El v4 desactiva `R.hook_mascot` y `R.mascot`, así que en `<slug>.py` no hace falta el avatar. **Renderiza y haz la contact sheet con `REEL_LENGTH=short python3 <slug>_v4.py preview|render`** (no con `<slug>.py`): el vídeo publicado es el del v4. Si el gato sale encima del dibujo del gancho, sube el dibujo (regla de la sección 5). Mira siempre a tamaño completo: baterías sobre cielo oscuro (usa `battery(..., plate=True)`), gráficas (las líneas se dibujan progresivamente, nunca se estiran) y etiquetas que tapen líneas. Sin vaivén de cintura; sí respiración suave y cambios de pose. El labial lleva el desfase de la voz (`cat.lipsync(ph, fps, n, max(0.0, off - s), lead=3)`, ya incluido en la plantilla).

## 6e. Anti-slop (17/11/2026): que no parezca IA en serie
Checklist completa en el proyecto de claude.ai (`checklist-anti-slop.md`). Resumen para aplicar **con la hoja de contactos, antes del render completo**:
- **Planos:** lista de escenas con plano, color dominante y qué hay de nuevo cada 3-4 s. Dos escenas seguidas no repiten plano ni composición. El gato sale como máximo en 1 de cada 3 escenas, y solo en las que no llevan tarjeta.
- **Ilustración:** cada objeto significa algo en esa escena (sin decorado de relleno); un protagonista por escena; paleta corta (color dominante + 1 de apoyo + acento amarillo solo en la palabra clave); contorno plano y grueso, sin brillos ni degradados; algo de imperfección hecha a mano (contorno con ruido bajo, sin simetría perfecta). Rechazar imágenes con manos raras, texto inventado, objetos duplicados o estilo distinto.
- **Movimiento:** pocos movimientos y con motivo; variar entrada y salida (no el mismo tipo más de 2 veces seguidas); entrada escalonada de palabras y objetos; rebote solo en 1-2 momentos; escenas con gráfico o dato, quietas.
- **Ritmo:** alternar escenas rápidas (2-3 s) con alguna más larga (5-6 s) donde cae lo importante.
- **Preguntas de la hoja (sí/no; con 3 o más «no», rehacer antes de renderizar):** ¿cada escena se distingue de la anterior a primera vista? ¿hay ≥3 colores dominantes? ¿cada objeto tiene un porqué? ¿el gato sale solo donde aporta? ¿hay algún detalle hecho a mano? ¿los textos se leen sin tapar nada? ¿se confundiría con el vídeo anterior sin el texto?
- **Ronda de crítica con puntuación (19/11/2026, de las skills Motion Reel y animation-studio):** antes del render completo, mira la hoja de contactos **a tamaño completo y también reducida a la mitad** (lo que se ve en un móvil a un brazo) y puntúa de 1 a 10: gancho (los 3 primeros segundos, sin sonido), legibilidad en móvil, calidad del movimiento, variedad entre escenas, fidelidad al estilo de marca y sincronía con la voz. Elige los 3 peores problemas, corrígelos y repite la hoja. **Máximo 3 rondas; se renderiza cuando todas las notas son ≥7** (el render cuesta ~45 min; la hoja, segundos). Anota las notas finales y los 3 cambios en `variants.slop_check`.
- **Prohibidos por defecto (señal de vídeo de plantilla):** título centrado sobre degradado, todo apareciendo con fundido, etiquetas de esquina y marcos, brillo en elementos de interfaz, explosiones de partículas genéricas. Cada entrada necesita dirección, peso y un motivo.
- **Cortes:** el primer fotograma de un corte ya muestra la imagen nueva (nunca un fotograma en blanco ni un destello a pantalla completa); máximo 1-2 destellos de pantalla completa por vídeo, en momentos de estructura (el giro, el cierre). Un barrido (whip) es un desplazamiento con las dos imágenes a la vez en pantalla. Los zooms van en espacio logarítmico (`s = a * (b / a) ** p`): da velocidad constante; una interpolación lineal se queda grande demasiado tiempo.
- **Golpes de sonido:** cada acento visual importante (aparición del dato, giro, cierre) lleva un efecto de sonido en ese mismo fotograma, y no se pone un golpe fuerte encima de una palabra hablada. Si falta sincronía, se arregla en la línea de tiempo del guion, no desplazando a mano un lado.
- **Una sola tipografía de título y una de apoyo, y un solo color de acento** salvo que la escena pida otra cosa.
- `qa.py` avisa (AVISO, no bloquea) de escenas seguidas con el mismo color dominante, cortes casi invisibles y menos de 3 colores dominantes. Anota en el log `variants.slop_check` con las respuestas «no» y qué se cambió.

## 6f. Lecciones del 18/11/2026 (overnight_charging): la usuaria vio el reel antes de publicarse y encontró esto
- **Gato hablando en el gancho y en el cierre, nunca el avatar fijo del canal** (ver 6d). Antes de dar el reel por bueno, mira el primer fotograma, uno hacia el 1 s y el último: el gato debe aparecer y no debe haber ningún círculo de logo.
- **Bucle: el último fotograma tiene que ser IGUAL que el primero** (misma batería/porcentaje, mismo tamaño y posición del dibujo, mismos rayos de fondo, mismo zoom de entrada, sin subtítulo). El puente se trata como el gancho: `V.hook_like = {"hook", "bridge"}` (sin reencuadre), `hook_art(..., settle, phase)` para alinear el ciclo de la batería con `V.last_t`, `R.punch` al revés al final y `bridge_bg` con el ángulo de rayos alineado. Comprueba con el mp4 renderizado: extrae el fotograma 0 y el último y compáralos (diferencia media baja, nada que se mueva). Cualquier cosa que se anime en el gancho con el tiempo (batería que se llena, vaivén, zoom) debe volver a su estado de T=0 al final.
- **Nada pisa el dibujo del gancho:** la batería del gancho no puede tapar el enchufe ni el cable; va a un lado, libre, con el rayo pequeño (si va sobre fondo oscuro, `battery(..., plate=True)` para que el contorno no se funda con el cielo).
- **Gráficas:** las líneas se dibujan progresivamente (los puntos van apareciendo con el mismo ancho), nunca estirando una curva ya completa; el gráfico queda fuera de la zona de botones y las etiquetas («Cool», «Hot») no tapan las líneas.
- **Tarjeta con sello + texto debajo:** dibujo más pequeño y más alto dentro de la tarjeta y el texto por debajo del dibujo, sin solaparse; el sello centrado sobre el dibujo.
- **Mirar a tamaño completo las escenas con baterías, gráficos y sellos, y el primer y último fotograma, antes de publicar** (los avisos automáticos no los detectan). Si algo falla, rehacer solo esas escenas con `ONLY=hook,stamp,bridge` (sin gastar créditos: voz y música ya están en el repo) y volver a subir el mp4 y la portada (la portada = fotograma 0).
- **Si la usuaria avisa antes de la hora de publicación:** corregir, renderizar, subir el mp4 y la portada al repo y sustituir el medio en el post de Metricool con `updateScheduledPost` (mismo texto y hora; el id del post cambia en cada actualización, el uuid no).

## 7. Upload
- Copy the mp4 to `videos/<YYYY-MM-DD>_<slug>.mp4`, then commit and push to `main`.
- Also copy the thumbnail to `videos/<YYYY-MM-DD>_<slug>_cover.png` (made in step 6).
- Check that `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/videos/<file>` returns 200 for both the mp4 and the cover png.

## 8. Publish (Metricool connector)
- Call `createScheduledPost` with `blogId 7740980` and timezone `Europe/Madrid`. Create **ONE post** with the three providers (instagram, tiktok and youtube), `autoPublish: true`, and `videoThumbnailUrl` = the raw.githubusercontent URL of the `_cover.png` (TikTok personal accounts ignore thumbnails; the first frame is already the cover there).
  - **Why one post (decided 15/11/2026):** the owner is on Metricool's free plan, which allows 20 publications a month, and Metricool counts **each post (publication group), not each network**: on 1/11 one post with three networks used 1, and from 3/11 on, with TikTok as a separate post, every reel used 2 (11 used by 15/11, 9 left). One post per reel uses 1. Each network still has its own status inside the post, so a TikTok error (like the 503 of 1/11) does not stop Instagram or YouTube.
  - TikTok is published automatically too (decision of 15/11/2026; before that it was manual, since 2/11, because the first API posts got 0 views; mammoth_quiz by API on 11/11 got 265 views, the same as the manual ones). Record `variants.tiktok_mode: "api"`. **Never create a second post just for one network:** it would use another of the 20 publications. Going back to manual TikTok would need a separate post (`autoPublish: false`), so ask the owner first and tell her it costs one more publication per reel.
  - Store the single uuid in the log as `metricool_uuid` (reels from 3/11 to 13/11 also have `metricool_uuid_tiktok`; new ones do not).
  - **Monthly count:** before creating the post, call `getScheduledPosts` for the whole current month and count the posts (each post = 1). If 20 or more are already counted, do not schedule it: tell the owner in tonight's notification ("⚠️ Sin publicaciones disponibles en Metricool este mes") and stop.
- **Immediately after the post is created**, append the log entry with everything known so far (step 9 fields), commit and push. Then go on to 8b. Step 9 only completes it.
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
- **TikTok:** `tiktokData`:
  - `privacyOption PUBLIC_TO_EVERYONE`
  - `title` set to the question (required)
  - `isAigc true`
  - `autoAddMusic false`
- **Instagram:** `instagramData`:
  - `type REEL`
  - `showReelOnFeed true`
  - `isAiGenerated true`
- **YouTube:** `youtubeData`:
  - `type short`
  - `privacy public`
  - `title` set to the question plus ` #shorts`
  - `category EDUCATION` (or `SCIENCE_TECHNOLOGY` for science, space and tech)
  - `madeForKids false`
  - `isAiGeneratedContent false`
  - 5 tags
- Metricool copies the video when the post is created, so the GitHub file only needs to exist at that moment.

## 8b. Schedule the post check
- Right after `createScheduledPost` succeeds, create a one-shot scheduled task with the Claude_Code_Remote connector (`create_trigger`):
  - `run_once_at`: the publish time + 30 minutes (UTC)
  - `name`: "Mr. Whiskerfact check <slug>"
  - `notifications`: `{"push": true}`
  - `initiation`: `"human_schedule"`
  - prompt: "Clone janpc/whiskerfact-videos (attach it with push access if needed), read CHECK.md and follow it for the reel '<title>' (slug <slug>), Metricool uuid <uuid> (one post for Instagram, TikTok and YouTube; mode <tiktok_mode>), scheduled at <ISO time Europe/Madrid>. Never publish or edit posts."
- **Safety net:** at the start of every nightly run, look in the log for any published entry from the last 3 days without a `check` field and with its time already passed. Run CHECK.md for it inline and include the result in tonight's notification.

## 9. Log and clean-up
- Complete the entry written in step 8 in `log/published.json` (append it now if it is somehow missing):
  - the date, category, slug, title, hook, sources (URLs), the Metricool uuid and the scheduled time
  - `duration_s`
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
