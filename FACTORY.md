# Mr. Whiskerfact: nightly reel factory

This is the run book the scheduled task follows every night. One run makes one reel from idea to published post, without human input.
All public-facing content is in **English**. All design rules live in `factory/brand.py`, so never hard-code colours, fonts, timings or positions in a scene.

## 0. Setup
- Clone this repo and work in `factory/`. Python 3, PIL, numpy, scipy and ffmpeg are expected. Install anything missing with `pip install --break-system-packages`.
- Read `factory/brand.py` fully before writing anything.
- Read `schedule.json` and `log/published.json`.

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
- **Hook:** at most 10 words. **Both lines are fully on screen from frame 0** (use `V.hook_text`), because viewers decide in the first second. The question never appears late, and something in the drawing moves within the first 0.3 s. The engine adds an entry punch at frame 0. The first frame is also the cover, so it must read well on its own. Use the hook style that `growth/experiments.json` assigns today (see step 8).

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
- **Length:** 150–170 words. Brad reads at about 148 words per minute, so the finished video lasts 65–75 s and is **always over 1 minute**. The renderer refuses to render under 61 s.
- **Language:** plain English that is not childish. Name each complex term, then explain it in one sentence.
- **Structure** (see `brand.STRUCTURE`):
  - hook
  - context
  - 2–3 steps
  - the surprising fact
  - a **wrap line that answers the hook**, in the form "So next time you …, now you know. …"
- Never announce the next video.
- Each scene opens with a distinctive first word, so scene cuts can be found in the transcript.

## 5. Voice (ElevenLabs connector)
- Use `creative_generate_speech` with these settings:
  - voice `Dslrhjl3ZpzrctukrQSN` (Brad)
  - model `eleven_v4`
  - flow `Q4RWsQia6pHRGabsab5B`
- Generate the whole script, wrap line included, in **one** call, with `generations_count: 1`. The default of 2 doubles the cost.
- Poll `creative_get_flow_run_status` until it is done. Never repeat a generation call, because each call is charged.
- Download the mp3 from its `storage.googleapis.com` URL to `factory/voice/<slug>_brad.mp3`.
- Save the exact script as `factory/voice/<slug>_script.txt`.
- Tighten the voice first: run `python3 tighten.py voice/<slug>_brad.mp3`. It shortens pauses to about 0.24 s, speeds the voice up by `brand.VOICE_TEMPO` and keeps the original as `_raw.mp3`. Always run it before alignment.
- Get free word timings with local forced alignment: `python3 align.py voice/<slug>_brad.mp3 voice/<slug>_script.txt voice/<slug>_brad_words.json`. Install it first with `NO_PROXY= pip install --break-system-packages pocketsphinx`.
- If a proper name is missing from the dictionary, add its phones to `EXTRA_PHONES`.
- Only if alignment fails, fall back to `creative_transcribe_audio` (about 400 credits).
- If the free tier is "busy", wait about 10 minutes and poll or retry once. If it still fails, go to step 10.
- The slogan audio is fixed: `factory/voice/slogan_brad.mp3`.

## 6. Build the reel
- Use `factory/pyramids.py` as the template: a single file that builds on `voice_reel.VoiceReel`. That module handles scene cuts, subtitles, the outro and the audio mix. Write `factory/<slug>.py` the same way.
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
  - **Close-ups** (cutaways, diagrams, objects): `ST.card(img, CARD)`, the warm cream card. Labels on the card must be dark (`ST.OUTLINE`, or a dark accent such as `(176, 40, 58)`), never the light category colours, and thin elements that sit on the card (hair, lines) must be dark too.
  - **Outdoor, animals, people, history scenes:** `ST.landscape(img, T)` (sunset, layered forests with parallax) or `ST.landscape(img, T, night=True)` (night with twinkling stars). Stand figures on the ground at y≈1330.
  - **Sky, space, cold, mystery:** a night sky (`ST.sky` + `ST.stars`).
  - **Psychedelic moments are rare and only for the truly crazy beat.** Use one only when the fact is genuinely mind-blowing (the twist, the "wait, what?" moment): `ST.wow_moment(img, T, t0, R.cat, "swirl"|"blobs"|"glitch", dur=1.3–1.6)`. Use 0–1 per reel; many reels have none. Never put one behind an explanation, a diagram or labels. It opens as a circle from the centre and closes the same way; it never fades.
  - **The hook cat never overlaps the drawing:** it sits bottom-left below the illustration (`brand.MASCOT["hook"]`). If the hook drawing reaches down there, move the drawing up.
  - **Figures and people:** draw them as clean organic silhouettes (merged shapes, smoothed) in the flat layered style, not as stick or primitive shapes. Animate state changes as one smooth transformation of the same figure (for example, a scalloped fur coat that retracts), not as two figures with an arrow between them.
  - Mix the backdrops so that consecutive scenes don't all look the same, and keep the pace fast (the videoclip's slow rhythm is NOT copied).
- **The style is a REFERENCE, not a template: no two reels may look the same.** What stays fixed is only the identity: outlines, flat colours, layered silhouettes, the cream close-up card, short psychedelic moments, the cat and the outro. Everything else changes with the topic:
  - Pick the world of the topic: `ST.landscape(..., sky_kind=sunset|dawn|dusk|day|storm, terrain=forest|pines|autumn|hills|dunes|waves|city, seed=n)`. A desert reel uses dunes, an ocean reel waves, a history reel its own place, space a starry sky. You can also draw a new backdrop for the topic (a reef, a cave, a street, a lab) in the same flat layered style.
  - Vary the psychedelic moment (`swirl`, `blobs` or `glitch`), where it falls and what it highlights.
  - Vary the compositions: close-up versus wide shot, the side the subject sits on, and silhouettes against the sky versus objects on the card.
  - Before building, read the last 3 log entries' `variants.look` and do NOT repeat the same combination of sky, terrain and psychedelic moment as the previous reel.
  - Record it in the log as `variants.look`, for example `{"skies": ["night","sunset"], "terrains": ["forest"], "wow": ["blobs","swirl"], "card": true}`.
- Close with the outro (outro5, automatic via reel_lib.outro_frame): the new cat (mascot.py) says the slogan inside its circle with phoneme lip-sync, then winks and smiles. Never edit the outro per video.
- **Big, rich drawings:**
  - The main subject must fill the illustration box: at least 60% of its height (about 360 px tall) and 70% of its width. Use a close-up or a cutaway, not a thin strip across the screen.
  - Add a second layer of detail where it helps: texture, small moving parts, labels with leader lines.
  - The engine re-frames each scene automatically (`VoiceReel.autofit`). It scales the drawing up to 1.45× and centres it left of the app buttons, but it cannot make a weak drawing rich, so draw big from the start.
  - Run `preview` and check that no scene shows more empty background than drawing in the band y 760–1370.
- **Nothing may be cut:** keep every drawing of a scene inside the illustration band (y 740–1370). If a drawing crosses the band edge, the engine prints `AVISO encuadre` during `preview` and does not re-frame that scene. Fix the scene (move the element into the band) until no warning appears. Look at the preview for anything cut by the band or by the screen edge.
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
- Render a preview of 6–8 frames and **look at it**. Draw the rectangle x 900–1080, y 900–1700 over the preview frames and check that nothing important falls inside it. Fix any overlapping text, cropped drawings or unreadable colours before the full render.

## 6b. Music composed for this reel (ElevenLabs)
- After the full render, upload the silent cut as `videos/music_src/<slug>_silent.mp4` (commit and push). Then attach it to flow `Q4RWsQia6pHRGabsab5B` with `creative_attach_reference_file` using its raw GitHub URL with the commit hash.
- Run `creative_generate_in_flow` with these settings:
  - `node_type: "video-to-music"`, `model_id: "eleven_video_to_music_v1"`, `generations_count: 1`, `connect_from` the attached node
  - a 2–3 sentence **sound** prompt: genre and mood matching the category and topic, key instruments, tempo, how the energy moves (lift at scene changes, tension before the twist, warm resolution), "instrumental, sparse mid-range so a narrator sits on top"
  - never repeat the call (about 960 credits)
- Download the result to `factory/voice/<slug>_music.mp3`, then run `python3 <slug>.py mux`. The engine uses that file automatically and matches its loudness.
- If music generation fails, publish with the synthesized bed: it's still a valid reel.
- Delete `videos/music_src/*` older than 7 days during clean-up.

## 7. Upload
- Copy the mp4 to `videos/<YYYY-MM-DD>_<slug>.mp4`, then commit and push to `main`.
- Check that `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/videos/<file>` returns 200.

## 8. Publish (Metricool connector)
- Call `createScheduledPost` with `blogId 7740980` and timezone `Europe/Madrid`. It must be a single post with providers tiktok, instagram and youtube.
- **Experiments:** read `growth/experiments.json`. For every test with status `testing`, pick today's option by its `rule`, counting options already used in `log/published.json`. Choose them all before writing the script, because the hook style changes the script.
- **Time:** use the `time_slots` option chosen today, on today's date (Madrid). If the test is `decided`, follow its rule.
- **Special dates:** a themed reel goes in the earliest slot that still falls before the event.
- **Text:** this is the same text for all three networks, and it is also the YouTube description. Write it in this order:
  1. the hook;
  2. one line in today's `caption_style`;
  3. a call to action, rotating these (pick the one used least in the log, and record it as `variants.cta`):
     - "🐱 Follow for more curious facts."
     - "💾 Save this for your next trivia night."
     - "👇 Tag someone who needs to know this.";
  4. one short sources line naming the institutions, for example "Sources: Harvard, Cell (2020)". No URLs;
  5. 3–5 hashtags: `#mrwhiskerfact`, the category, the topic and `#didyouknow`. Add the event hashtag on special dates.
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
  - prompt: "Clone janpc/whiskerfact-videos (attach it with push access if needed), read CHECK.md and follow it for the reel '<title>' (slug <slug>), Metricool uuid <uuid>, scheduled at <ISO time Europe/Madrid>. Never publish or edit posts."
- **Safety net:** at the start of every nightly run, look in the log for any published entry from the last 3 days without a `check` field and with its time already passed. Run CHECK.md for it inline and include the result in tonight's notification.

## 9. Log and clean-up
- Append to `log/published.json`:
  - the date, category, slug, title, hook, sources (URLs), the Metricool uuid and the scheduled time
  - `duration_s`
  - `event` (themed reels only)
  - `variants`, as in `{"time_slot": "20:30", "hook_style": "statement", "caption_style": "teaser"}`. Include `format`, `personality`, `cta` and `look` too. The weekly review needs these to compare results.
- Delete `videos/*.mp4` older than 7 days, then commit and push.

## 10. Notify
- Send one push notification. On success it gives the title, category, scheduled time and duration.
- On failure it gives the step that failed and why. **Never publish a reel that failed a check.**
- **Credits:** the account is on the ElevenLabs Starter plan, which allows commercial use. If a run finds that credits will not cover the next reel, say so in the notification: "Quedan pocos créditos de ElevenLabs para los próximos vídeos."
- If ElevenLabs refuses for lack of credits, do not publish anything. Say exactly that in the notification.
