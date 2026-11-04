# Mr. Whiskerfact: weekly review

This is the run book for the weekly scheduled task. It reads the metrics, learns what works and adjusts the tests the nightly factory runs.
It never changes the brand rules (`factory/brand.py`) or the run book's quality rules. It only edits `growth/` and sends the owner a summary in Spanish.

## 1. Collect
- Clone `janpc/whiskerfact-videos` and read `log/published.json`, `growth/experiments.json` and `growth/insights.md`.
- Use the Metricool connector `getAnalyticsDataByMetrics` with brandId `7740980`, from the channel start (2026-10-29) to today. Request these metrics:
  - **TikTok:** `TKPO02` (date and time), `TKPO05` (description), `TKPO07` views, `TKPO08` likes, `TKPO09` comments, `TKPO10` shares, `TKPO13` full-watch rate, `TKPO15` average watch time, `TKPO16` For You share.
  - **Instagram Reels:** `IGRE02`, `IGRE03`, `IGRE23` views, `IGRE11` reach, `IGRE24` average watch time, `IGRE27` retention, `IGRE28` 3-second view rate, `IGRE12` saves, `IGRE21` shares.
  - **YouTube:** `YTVV02`, `YTVV17` title, `YTVV06` views, `YTVV08` average view duration, `YTVV09` likes, `YTVV11` comments.
  - **Follower growth:** if available, list the evolution metrics with `getAnalyticsAvailableMetrics` and pick follower counts.
- **TikTok mode (manual vs api):** compare views of reels with `variants.tiktok_mode` `manual` against `api`. If API posts get views comparable to manual ones in 2+ tests, suggest to the owner going back to automatic TikTok.
- **Audience country:** Metricool doesn't give TikTok viewer countries. Ask the owner in the notification, once a month, for the top viewer countries from TikTok Studio, and note them in `growth/insights.md`. Use Instagram/YouTube country data if Metricool lists it. Goal: check that an English channel from a Spanish account reaches English-speaking viewers.
- Match each row to its log entry by publish time, title or description.
- **Measurement windows** (`protocol.windows` in `experiments.json`): under 48 h old, ignore. From 48 h to 7 days old, record an **early read** (never decisive; only for the notification). At 7 days or more, record the **final figures**, which are the only ones used for verdicts. Store `age_h` next to every figure, because Metricool totals are cumulative.
- Save a dated snapshot to `growth/metrics/<YYYY-MM-DD>.json`.

## 2. Score
- For each video and network, compute:
  - views
  - **watch % = average watch time ÷ video length** (YouTube `YTVV08`, TikTok `TKPO15`, Instagram `IGRE24`)
  - full-watch rate, or retention on Instagram
  - (likes + comments + shares + saves) ÷ views, and shares per 100 views
- **Main score = watch %**, averaged over the networks the video went to. Views tell us how far it went, but they depend on algorithm luck, so they are reported and never decide a test. Because longer videos tend to have a lower watch %, always write the video length next to the figure.
- **TikTok mode** (`variants.tiktok_mode`) is a separate side test: compare it on TikTok views only. TikTok views of `api` posts must not drag the batch result down; the main score is watch %, not views.

## 3. Learn
`growth/experiments.json` holds one running `batch` (one variable, 3 videos) and the `protocol` with the thresholds. Never change the thresholds from here.
- **Baseline:** median watch % of the last 5 videos with role `base` or `control` (using final figures).
- **Per video of the batch** (role `variant`, final figures only): compute its watch % versus the baseline, as a percentage difference.
- **Close the batch** only when all 3 videos have final figures:
  - **Success** (variant beats the baseline by more than 20% in at least 2 of 3): set the test `status` to `decided`, make the variant its new `control` (it becomes the default for every video), move the batch to `history` with the numbers, and write the rule in `learned`.
  - **Failure** (worse by more than 20% in at least 2 of 3): `decided`, the control stays; move to `history`.
  - **Inconclusive** (anything else): say "inconclusive", not "it does not work". Reopen the same test once with a new batch id (`B1b-...`). If the second batch is also inconclusive, close it as "no detectable difference" and keep the control.
  - Then set the next batch from `queue` (one variable, new id, hypothesis in one sentence), put its test in `testing` and every other test in `fixed`. The Monday plan assigns the videos.
- **Early read:** while a batch is running, mention in the notification how each finished video is doing at 48 h, flagged as provisional.
- **Content patterns:** look for patterns across category, format, topic type and video length. Write them in `insights.md` as hypotheses, never as rules, and never change a test because of them. Format varies on purpose; note it if it clearly explains a result.
- **Off-limits:** the voice, the mascot, the colours, the outro and the verification rules. Suggest changes to those to the owner instead.
- Add a dated entry at the top of `growth/insights.md` with the numbers behind each conclusion. Commit and push.

## 4. Notify
- Send one push notification in Spanish, at most 5 short lines:
  - videos analysed
  - the best and worst video of the week by watch %, and why
  - the running batch: variable, how many of its 3 videos have final figures, and the early read or the verdict (adopted, discarded or inconclusive)
  - what changed in the tests
  - one suggestion for the owner, if any
- If no videos are old enough or Metricool returns no data yet, say so in one line and change nothing.
