# What we have learned

Written by the weekly review. Newest first. Each entry: date, what was compared, numbers, conclusion, and what changed.

## 2026-11-09 — first weekly review

**Data.** 7 public reels in Metricool (29 Oct – 6 Nov); `cat_night_vision` (8 Nov) is under 48 h and not in Metricool yet. Snapshot: `growth/metrics/2026-11-09.json`.
- Watch % comes from **Instagram only** (`IGRE24` ÷ length). TikTok watch metrics (`TKPO13/15/16`) come back null, and YouTube returns no per-video rows (`YTVV` empty, `YTVP` only lists the 4 October Shorts with null metrics). Instagram retention (`IGRE27`) is null too.
- Followers: Instagram 12 (7 Nov), TikTok 2 (7 Nov), YouTube 7 subscribers (9 Nov).
- Country data: Metricool has none for Instagram or YouTube yet; TikTok countries asked to the owner (pending).

| Video | Length | Window | IG watch % | IG views | 3-s rate | Eng/100 | TikTok views |
|---|---|---|---|---|---|---|---|
| dolphins (base) | 62.6 s | final | 40.7 | 1591 | 63.3 | 4.27 | 0 |
| pyramids (base) | 80.7 s | final | **44.8** | 337 | 55.3 | 1.78 | 0 |
| goosebumps (base) | 62.9 s | final | **13.9** | 190 | 43.5 | 2.63 | 1 |
| vampire_bats (base) | 70.4 s | final | 35.6 | 1543 | 60.8 | 3.24 | 1 |
| hottest_planet (base) | 75.2 s | final | 34.0 | 1406 | 59.3 | 2.28 | 905 |
| wifi_bands (base) | 85.6 s | early (134 h) | 29.5 | 2506 | 57.7 | 2.99 | 310 |
| earth_tunnel (B1 variant) | 86.2 s | early (62 h) | 28.9 | 189 | 52.7 | 2.12 | 278 |

**Baseline** (median watch % of the 5 last base videos with final figures): **35.6 %** (40.7, 44.8, 13.9, 35.6, 34.0).

**Batch B1-hook-style** (statement vs question): 0 of 3 videos with final figures. Early read, provisional: earth_tunnel 28.9 % = −19 % vs baseline (just inside the ±20 % band), at 86 s, one of the two longest videos. No verdict; nothing changed in the tests.

**TikTok mode:** every reel so far is `manual` (or predates the field); no `api` posts to compare yet.

**Hypotheses (not rules):**
- *Length:* the two longest reels (85–86 s) have the lowest watch % apart from goosebumps (29–30 % vs 34–45 % for 63–81 s). Too few videos to separate length from topic or hook.
- *Goosebumps outlier:* 13.9 % watch and 43.5 % 3-s rate, the weakest hook hold of all. It is the only `body` topic so far.
- *Baseline is mixed:* 3 of the 5 baseline reels (dolphins, pyramids, goosebumps) already used a statement hook according to the log. The B1 comparison is therefore statement vs a mostly-statement baseline, which makes a >20 % gap hard to reach. Flagged for the owner; thresholds unchanged.
- *TikTok reach:* the 4 reels of 29–31 Oct got 0–1 TikTok views, while everything from 1 Nov gets 280–900. Looks like the new account was not distributed in its first days (or those posts are restricted). `hottest_planet` shows up on TikTok although the log's post-check recorded an auto-publish error.
- *Instagram reach is volatile:* 190–2,500 views with similar 3-s rates; earth_tunnel has only 189 IG views at 62 h. Views are not used for verdicts.

**Changed:** `experiments.json` → `batch.reads` with this early read. No test status changed.

_Channel started on 2026-10-29._
