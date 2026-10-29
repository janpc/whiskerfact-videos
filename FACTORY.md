# Mr. Whiskerfact: nightly reel factory

This is the run book the scheduled task follows every night. One run makes one reel from idea to published post, without human input.
All public-facing content is in **English**. All design rules live in `factory/brand.py`, so never hard-code colours, fonts, timings or positions in a scene.

## 0. Setup
- Clone this repo and work in `factory/`. Python 3, PIL, numpy, scipy and ffmpeg are expected. Install anything missing with `pip install --break-system-packages`.
- Read `factory/brand.py` fully before writing anything.
- Read `schedule.json` and `log/published.json`.

## 1. Is today a publishing day?
- `schedule.json` holds two fields: `daily_until` (a date) and `then_every_days` (default 2).
- Up to and including `daily_until`, publish every day.
- After that date, publish only if at least `then_every_days` days have passed since the last entry in `log/published.json`.
- If today is not a publishing day, stop quietly: no notification, no commit.

## 2. Topic
- **Category:** the next one in `brand.ROTATION` after the category of the last log entry.
- **Topic:** an evergreen curiosity in that category that is not already in the log. It must be phrased as a question a curious adult would stop scrolling for.
- **Hook:** at most 10 words, on screen from frame 0. Either the question itself, or a surprising statement followed by the question.

## 3. Verify
- Every fact in the script must be confirmed by **two independent, reliable sources**, for example a university, a museum, NASA or NOAA, a peer-reviewed review, or Britannica.
- Prefer recent sources and check that the fact is still current.
- Record both URLs for each claim. If a claim can't be confirmed twice, cut it.

## 4. Script
- **Length:** 165–195 words, so the finished video lasts 65–75 s and is **always over 1 minute**. The renderer refuses to render under 61 s.
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
- Generate the whole script, wrap line included, in **one** call.
- Poll `creative_get_flow_run_status` until it is done. Never repeat a generation call, because each call is charged.
- Download the mp3 from its `storage.googleapis.com` URL to `factory/voice/<slug>_brad.mp3`.
- Get word timings with `creative_transcribe_audio` (eleven_scribe_v1), connected from that node, and save them as `[[word, start, end], …]` in `factory/voice/<slug>_brad_words.json`.
- If the free tier is "busy", wait about 10 minutes and poll or retry once. If it still fails, go to step 10.
- The slogan audio is fixed: `factory/voice/slogan_brad.mp3`.

## 6. Build the reel
- Use `factory/dolphins.py` (scenes and drawings) and `factory/dolphins_voice.py` (voice sync, subtitles and mix) as templates. Write `factory/reels/<slug>.py` and `factory/reels/<slug>_voice.py`.
- The illustrations must be simple vector shapes drawn with PIL that show the real mechanism.
- Keep the rhythm rules:
  - something changes at least every 2 s
  - each scene lasts 3–7 s
  - a visual punch about every 10 s
  - every animation has its sound effect
- The background uses the category colour (`brand.bg_for`). Subtitles appear word by word with the voice.
- Close with the "gafas" outro: the narrated slogan, with the wink after the words.
- Render a preview of 6–8 frames and **look at it**. Fix any overlapping text, cropped drawings or unreadable colours before the full render.

## 7. Upload
- Copy the mp4 to `videos/<YYYY-MM-DD>_<slug>.mp4`, then commit and push to `main`.
- Check that `https://raw.githubusercontent.com/janpc/whiskerfact-videos/main/videos/<file>` returns 200.

## 8. Publish (Metricool connector)
- Call `createScheduledPost` with `blogId 7740980` and timezone `Europe/Madrid`. It must be a single post with providers tiktok, instagram and youtube.
- **Time:** use `getBestTimeToPostByNetwork` for tiktok for today. Pick the highest-value hour between 13:00 and 22:00 that is at least 30 min from now.
- **Text:** the hook, one short line, then 3–5 hashtags: `#mrwhiskerfact`, the category, the topic, `#didyouknow`.
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
- Append to `log/published.json` the date, category, slug, title, hook, sources (URLs), the Metricool uuid and the scheduled time.
- Delete `videos/*.mp4` older than 7 days, then commit and push.

## 10. Notify
- Send one push notification. On success it gives the title, category, scheduled time and duration.
- On failure it gives the step that failed and why. **Never publish a reel that failed a check.**
