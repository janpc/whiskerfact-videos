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
- Match each row to its log entry by publish time, title or description.
- Ignore videos younger than 72 h, because their numbers are still moving.
- Save a dated snapshot to `growth/metrics/<YYYY-MM-DD>.json`.

## 2. Score
- For each video and network, compute:
  - views
  - average watch time ÷ video length (watch %)
  - full-watch rate, or retention on Instagram
  - (likes + comments + shares + saves) ÷ views
- **Main score:** views × watch %, normalised per network as a rank among our own videos, then averaged across the three networks. Views tell us how far it went; watch % tells us whether it held people.

## 3. Learn
- For each test in `experiments.json` with status `testing`, compare the options using the median main score per option.
- **Declare a winner** only if both are true:
  - every option has at least 4 videos;
  - the best option beats the second by at least 25% on the median.
- If so, set `"status": "decided"` and the winner's weight to 3 (others stay at 1, for occasional re-checks). Write the rule that follows from it.
- **Weights:** while a test is still running, set each option's weight to 1 plus its rank (best = highest). Never drop an option to 0, so it keeps getting explored.
- **Content patterns:** look for patterns across category, topic type and video length. Write them as hypotheses, not rules, unless they clear the same bar as above.
- **New test:** when a test is decided and fewer than 3 tests are running, open one new test. Change one thing only, with two options. Ideas, in rough order:
  - video length (65 s vs 75 s)
  - first word on screen (number vs question)
  - number of hashtags (3 vs 6)
  - a pinned first comment asking a question vs none
  - posting days (weekday vs weekend)
- **Off-limits:** the voice, the mascot, the colours, the outro and the verification rules. Suggest changes to those to the owner instead.
- Add a dated entry at the top of `growth/insights.md` with the numbers behind each conclusion. Commit and push.

## 4. Notify
- Send one push notification in Spanish, at most 5 short lines:
  - videos analysed
  - the best and worst video of the week, and why
  - what changed in the tests
  - one suggestion for the owner, if any
- If no videos are old enough or Metricool returns no data yet, say so in one line and change nothing.
