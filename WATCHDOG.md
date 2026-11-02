# Mr. Whiskerfact: morning watchdog

A daily scheduled task, around 09:38 Madrid. It checks that the nightly factory really scheduled today's reel. It is read-only: it never renders, publishes, edits posts or spends ElevenLabs credits.

1. Read `schedule.json` and `log/published.json`.
2. **Was today a publishing day?** Apply FACTORY.md step 1, but **ignore log entries dated today** (Europe/Madrid), so a reel already made tonight doesn't hide the answer. If today was not a publishing day, stop silently: no commit, no notification.
3. **Is there a reel for today?**
   - Log: is there an entry dated today?
   - Metricool: `getScheduledPosts` with brandId `7740980`, timezone `Europe/Madrid`, today 00:00 to 23:59, `extendedRange: false`. Is there a post with a video for today, for Instagram/YouTube and for TikTok?
4. **Result:**
   - **Both found:** stop silently. Everything is fine.
   - **Nothing in Metricool:** send a push notification in Spanish: "⚠️ Hoy tocaba vídeo y no hay nada programado en Metricool. La fábrica de esta noche no terminó." Add the last commit time of the repo and, if there is one, the slug of any half-made reel in `factory/out/` or `factory/voice/` from today.
   - **In Metricool but no log entry:** send: "⚠️ El vídeo de hoy está programado (<time>) pero la fábrica no dejó registro ni comprobación. Revísalo en un chat." Do not write the log yourself.
   - **Only one of the two Metricool posts exists** (Instagram/YouTube or TikTok): say which one is missing.
5. Never commit anything: this task only reads and notifies.
