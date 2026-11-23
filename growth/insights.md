# What we have learned

Written by the weekly review. Newest first. Each entry: date, what was compared, numbers, conclusion, and what changed.

## 2026-11-23 — weekly review

**Data.** 13 public reels in Metricool (29 Oct – 21 Nov). `first_thanksgiving` (21 Nov, base) is 38 h old: stored, not scored. `lightning_vs_sun` (23 Nov, third B2-length variant) goes out tonight 20:30. Snapshot: `growth/metrics/2026-11-23.json`.
- Watch % still comes from **Instagram only** (`IGRE24` ÷ length). TikTok `TKPO13/15/16` null; YouTube `YTVV` empty. `IGRE27` null.
- Followers: Instagram 15 → 16 (14 → 21 Nov), **TikTok 4 → 10 (jump on 21 Nov, the day of the Thanksgiving reel: 664 TikTok views at 38 h, best since hottest_planet)**, YouTube 8 → 8.
- Country: Instagram `IGDP01/02` still returns no rows; nothing for YouTube. TikTok countries still pending from the owner (next monthly ask ~7 Dec).
- TikTok `api` mode: api reels 239–664 views (mammoth_quiz 265, moon_earth_view 239, overnight_charging 270, first_thanksgiving 664) vs manual bone_vs_steel 271 → no warning.

| Video | Length | Role | Window (age) | IG watch % | Avg watch | IG views | 3-s skip | Eng/100 | TikTok views |
|---|---|---|---|---|---|---|---|---|---|
| earth_tunnel | 86.2 s | B1 variant | final (399 h) | 28.7 | 24.8 s | 192 | 47.0 | 2.08 | 281 |
| cat_night_vision | 73.3 s | B1 variant | final (350 h) | **36.5** | 26.7 s | 1270 | **32.9** | **4.96** | 251 |
| mammoth_quiz | 78.4 s | B1 variant | final (279 h) | 27.9 | 21.9 s | 1503 | 38.3 | 2.40 | 265 |
| bone_vs_steel | 79.9 s | base | final (231 h) | 21.7 | 17.3 s | 140 | 46.8 | 2.86 | 271 |
| moon_earth_view | 56.2 s | B2 variant (00:30) | early (154 h) | **17.0** | 9.5 s | 193 | 59.2 | 2.07 | 239 |
| overnight_charging | 54.8 s | B2 variant | early (110 h) | 30.2 | 16.5 s | 694 | 40.1 | 2.74 | 270 |
| first_thanksgiving | 74.3 s | base | too early (39 h) | (40.3) | 29.9 s | 1416 | 26.1 | 2.97 | 664 |

Older reels barely moved since 16 Nov (all final; see snapshot).

**Baseline** (last 5 base/control with final figures: goosebumps, vampire_bats, hottest_planet, wifi_bands, bone_vs_steel): watch % **29.5** (13.8, 35.3, 34.0, 29.5, 21.7) — down from 34.0 because bone_vs_steel replaced pyramids. For B2: median IG views **1,408**, median 3-s skip **42.3 %**.

**Batch B1-hook-style — closed: inconclusive.** 3 of 3 final: earth_tunnel −2.7 %, cat_night_vision **+23.7 %**, mammoth_quiz −5.4 % vs 29.5 %. Only 1 of 3 beyond +20 %, none below −20 % (against the old 34.0 baseline it is −15.6 / +7.4 / −17.9: same verdict). Not "statement doesn't work": no detectable difference yet. Moved to `history`; `B1b-hook-style` queued for the one repeat, after `time_slots` (the owner put that first on 15 Nov). `hook_style` stays fixed at `question`.

**Batch B2-length (short vs standard) — now the running batch, 0 of 3 final.** Early read, provisional: moon_earth_view 193 IG views (−86 % vs 1,408), skip 59.2 % (worse than 42.3); overnight_charging 694 views (−51 %), skip 40.1 % (better). Both are >20 % below on views → if this holds at 7 days it is a **failure** (2 of 3). moon_earth_view also went out at 00:30, so it mixes two variables. lightning_vs_sun goes out tonight; it only reaches 7 days after 30 Nov 20:30, so the verdict most likely comes on 7 Dec.

**Best / worst by watch % (final figures).** Best: cat_night_vision, 36.5 % of 73 s (lowest skip 32.9 %, top engagement). Worst final: bone_vs_steel, 21.7 % of 80 s, 46.8 % skip, 140 views. Worst overall (early): moon_earth_view, 17.0 % of 56 s, 59.2 % skip.

**Hypotheses (not rules):**
- *3-s skip rate predicts Instagram reach* — still holds on the high side: every reel with skip ≥ 44.9 % has 140–338 views (5 reels). Reels with skip ≤ 42.3 % have 1,270–2,521 views (6 final reels), but overnight_charging (40.1 %, early) has only 694 — the line may be fuzzier than "below 42 % → 1,300+".
- *"People watch ~25 s whatever the length" is NOT holding for short reels:* the two short reels average 9.5 s and 16.5 s, against 17–36 s (mostly 22–27 s) for the standard reels. Shorter reels seem to lose seconds, not just add percentage. Two early reads only.
- *`body` topics hook worst:* now with final figures for both (goosebumps 57.1 %, bone_vs_steel 46.8 % skip; 140–192 views). Still only 2 videos.
- *Myth format does well:* overnight_charging (myth) is the better of the two short reels (40.1 % skip, 3 saves). Three myth reels, all with skip ≤ 40.1 %.
- *Themed / seasonal reels travel:* first_thanksgiving has the lowest skip ever (26.1 %) and 1,416 IG views in 38 h, plus the TikTok follower jump; vampire_bats (Halloween) also did well. Early and only 2 cases.
- *TikTok* stays flat at 240–310 except for hottest_planet (907) and first_thanksgiving (664) — both quiz format.

**Changed:** `experiments.json` → B1-hook-style closed (inconclusive) and moved to `history`; `next_batch` B2-length moved into `batch` with its 2026-11-23 early read; `B1b-hook-style` added to `queue` (2nd, after time_slots); `hook_style.note` updated. Status of every test unchanged (length testing, the rest fixed).

## 2026-11-16 — weekly review

**Data.** 10 public reels in Metricool (29 Oct – 13 Nov). `moon_earth_view` (16 Nov, first B2-length variant) is scheduled for tonight 20:30 and not published yet. Snapshot: `growth/metrics/2026-11-16.json`.
- Watch % still comes from **Instagram only** (`IGRE24` ÷ length). TikTok `TKPO13/15/16` null; YouTube `YTVV` empty, `YTVP` only the 4 October Shorts with null metrics. `IGRE27` null. `IGRE30` (3-s skip rate) now stored per reel.
- Followers: Instagram 13 → 15 (9 → 14 Nov), TikTok 3 → 4 (9 → 14 Nov), YouTube 7 → 8 subscribers (9 → 16 Nov).
- Country: Metricool returns no Instagram country rows (`IGDP`) and nothing for YouTube. TikTok countries asked to the owner on 9 Nov: still pending (next monthly ask around 7 Dec).
- TikTok `api` mode: mammoth_quiz (api) 265 views at 110 h vs 251–281 for the manual reels of the same weeks → no warning.

| Video | Length | Role | Window (age) | IG watch % | Avg watch | IG views | 3-s skip | Eng/100 | TikTok views |
|---|---|---|---|---|---|---|---|---|---|
| dolphins | 62.6 s | base | final | 40.7 | 25.5 s | 1592 | 36.7 | 4.27 | 0 |
| pyramids | 80.7 s | base | final | 44.8 | 36.1 s | 337 | 44.7 | 1.78 | 0 |
| goosebumps | 62.9 s | base | final | 13.8 | 8.7 s | 191 | 56.8 | 2.62 | 1 |
| vampire_bats | 70.4 s | base | final | 35.4 | 24.9 s | 1552 | 39.5 | 3.22 | 1 |
| hottest_planet | 75.2 s | base | final | 34.0 | 25.6 s | 1407 | 40.7 | 2.27 | 907 |
| wifi_bands | 85.6 s | base | final (302 h) | 29.5 | 25.2 s | 2518 | 42.3 | 3.06 | 310 |
| earth_tunnel | 86.2 s | B1 variant | final (230 h) | 28.8 | 24.9 s | 191 | 47.3 | 2.09 | 281 |
| cat_night_vision | 73.3 s | B1 variant | final (182 h) | **36.5** | 26.8 s | 1268 | **32.8** | **4.97** | 251 |
| mammoth_quiz | 78.4 s | B1 variant | early (110 h) | 27.9 | 21.9 s | 1502 | 38.3 | 2.46 | 265 |
| bone_vs_steel | 79.9 s | base | early (62 h) | **21.5** | 17.2 s | 139 | 47.2 | 2.88 | 271 |

**Baseline** (median watch % of the last 5 base/control videos with final figures: pyramids, goosebumps, vampire_bats, hottest_planet, wifi_bands): **34.0 %** (44.8, 13.8, 35.4, 34.0, 29.5). For B2-length: median IG views **1,407**, median 3-s skip **42.3 %** (same 5 videos).

**Batch B1-hook-style** (statement vs question): **2 of 3** with final figures. earth_tunnel −15.3 % (final), cat_night_vision +7.4 % (final), mammoth_quiz −17.9 % (early, provisional). Not closed yet (mammoth_quiz reaches 7 days on 18 Nov), but with two finals already inside ±20 % neither success nor failure is reachable: it will close as **inconclusive** next review. Per the protocol that means one repeat (B1b) — to be scheduled after B2-length so there is still one variable at a time.

**Batch B2-length** (short vs standard): 0 of 3 published (first variant goes out tonight). Nothing to read.

**Best / worst of the week (by watch %).** Best: cat_night_vision, 36.5 % of 73 s, with the lowest 3-s skip so far (32.8 %) and the highest engagement (4.97/100). Worst: bone_vs_steel, 21.5 % of 80 s (early, 62 h), 47.2 % skip and 139 IG views.

**Hypotheses (not rules):**
- *3-s skip rate predicts Instagram reach* — holds on all 10 reels: skip ≤ 42.3 % → 1,268–2,518 views (6 reels); skip ≥ 44.7 % → 139–337 views (4 reels). No reel sits between 42.3 and 44.7.
- *People watch ~25 s whatever the length:* 8 of 10 reels have an average watch of 22–27 s for lengths 63–86 s, so watch % falls with length. Exceptions: goosebumps (8.7 s) and pyramids (36.1 s). Supports the B2-length reasoning; B2 will test it.
- *`body` topics hook worst:* both body reels (goosebumps 56.8 %, bone_vs_steel 47.2 %) have the highest skip rates and the lowest views. Only 2 videos, and bone_vs_steel is still early.
- *Myth format does well:* the two myth reels (vampire_bats, cat_night_vision) both have skip < 40 %, 1,250+ views and 3.2–5.0 eng/100. Two videos only.
- *Hook style looks irrelevant so far:* statement hooks range 13.8–44.8 %, question hooks 21.5–35.4 %; the spread inside each group is larger than between them.
- *TikTok views are flat* at 250–310 per reel since 3 Nov regardless of the Instagram result; hottest_planet (907) is still the only breakout.

**Changed:** `experiments.json` → `batch.reads` (2026-11-16 read, 2 of 3 final) and `next_batch.reads` (0 of 3). No test status changed.

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
