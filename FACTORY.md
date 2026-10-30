# Mr. Whiskerfact: nightly reel factory

This is the run book the scheduled task follows every night. One run makes one reel from idea to published post, without human input.
All public-facing content is in **English**. All design rules live in `factory/brand.py`, so never hard-code colours, fonts, timings or positions in a scene.

## 0. Setup
- Clone this repo and work in `factory/`. Python 3, PIL, numpy, scipy and ffmpeg are expected. Install anything missing with `pip install --break-system-packages`.
- Read `factory/brand.py` fully before writing anything.
- Read `schedule.json` and `log/published.json`.

## 1. Is today a publishing day?
- `schedule.json` holds two fields: `daily_first` (5) and `then_every_days` ([2, 3]).
- Count the published entries in `log/published.json`. Entries with a `note` that contains "test" don't count.
- While that count is below `daily_first`, publish every day.
- After that, the gap since the last published reel must reach the next value in `then_every_days`, taken in turn (2, then 3, then 2…). That gives about 12–13 reels a month, which the ElevenLabs Starter credits cover with composed music.
- A themed reel for a special date may break this rhythm by one day.
- If today is not a publishing day, stop quietly: no notification, no commit.

## 2. Topic
- **Special dates first:** read `growth/calendar.json`. Make a themed reel today if both of these are true:
  - an event falls within the next 7 days;
  - fewer than that event's `reels` themed videos are already in the log (field `event`).
- A themed reel can use any category that fits.
- Publish it no later than 14:00 Madrid on the event day. Never publish one after the event.
- **Category:** otherwise, the next one in `brand.ROTATION` after the last *regular* (non-themed) log entry.
- **Topic:** an evergreen curiosity in that category that is not already in the log. It must be phrased as a question a curious adult would stop scrolling for.
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
- Close with the "gafas" outro: the narrated slogan, with the wink after the words.
- **Big, rich drawings:**
  - The main subject must fill the illustration box: at least 60% of its height (about 360 px tall) and 70% of its width. Use a close-up or a cutaway, not a thin strip across the screen.
  - Add a second layer of detail where it helps: texture, small moving parts, labels with leader lines.
  - The engine re-frames each scene automatically (`VoiceReel.autofit`). It scales the drawing up to 1.45× and centres it left of the app buttons, but it cannot make a weak drawing rich, so draw big from the start.
  - Run `preview` and check that no scene shows more empty background than drawing in the band y 760–1370.
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

## 7. Upload
- Copy the mp4 to `videos/<YYYY-MM-DD>_<slug>.mp4`, then commit and push to `main`.
- Check that `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/videos/<file>` returns 200.

## 8. Publish (Metricool connector)
- Call `createScheduledPost` with `blogId 7740980` and timezone `Europe/Madrid`. It must be a single post with providers tiktok, instagram and youtube.
- **Experiments:** read `growth/experiments.json`. For every test with status `testing`, pick today's option by its `rule`, counting options already used in `log/published.json`. Choose them all before writing the script, because the hook style changes the script.
- **Time:** use the `time_slots` option chosen today, on today's date (Madrid). If the test is `decided`, follow its rule.
- **Special dates:** a themed reel goes in the earliest slot that still falls before the event.
- **Text:** the hook, then one line in today's `caption_style`, then 3–5 hashtags: `#mrwhiskerfact`, the category, the topic and `#didyouknow`. Add the event hashtag on special dates.
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

## 9. Log and clean-up
- Append to `log/published.json`:
  - the date, category, slug, title, hook, sources (URLs), the Metricool uuid and the scheduled time
  - `duration_s`
  - `event` (themed reels only)
  - `variants`, as in `{"time_slot": "20:30", "hook_style": "statement", "caption_style": "teaser"}`. The weekly review needs these to compare results.
- Delete `videos/*.mp4` older than 7 days, then commit and push.

## 10. Notify
- Send one push notification. On success it gives the title, category, scheduled time and duration.
- On failure it gives the step that failed and why. **Never publish a reel that failed a check.**
- **Credits:** the account is on the ElevenLabs Starter plan, which allows commercial use. If a run finds that credits will not cover the next reel, say so in the notification: "Quedan pocos créditos de ElevenLabs para los próximos vídeos."
- If ElevenLabs refuses for lack of credits, do not publish anything. Say exactly that in the notification.
