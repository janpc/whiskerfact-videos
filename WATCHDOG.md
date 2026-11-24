# Mr. Whiskerfact: morning watchdog

A daily scheduled task, around 09:38 Madrid. It checks that the nightly factory really scheduled today's reel. It is read-only: it never renders, publishes, edits posts or spends ElevenLabs credits.

1. Read `schedule.json` and `log/published.json`.
2. **Was today a publishing day?** Apply FACTORY.md step 1, but **ignore log entries dated today** (Europe/Madrid), so a reel already made tonight doesn't hide the answer. If today was not a publishing day, stop silently: no commit, no notification.
3. **Is there a reel for today?**
   - Log: is there an entry dated today?
   - Buffer: connector `list_posts` for organization `6b0492eb2977e5ad81690395`, `dueAt` from today 00:00 to 23:59 (Europe/Madrid), no status filter. Is there a post with a video for each of the three channels (TikTok `6b0493c48541f09ecb7bc60a`, YouTube `6b04939e8541f09ecb7bc487`, Instagram `6b04934b8541f09ecb7bc0e7`)? (Until 23/11/2026 the reels were in Metricool, brandId `7740980`; that no longer applies.)
4. **Result:**
   - **Both found:** stop silently. Everything is fine.
   - **Nothing in Buffer:** send a push notification in Spanish: "⚠️ Hoy tocaba vídeo y no hay nada programado en Buffer. La fábrica de esta noche no terminó." Add the last commit time of the repo and, if there is one, the slug of any half-made reel in `factory/out/` or `factory/voice/` from today.
   - **In Buffer but no log entry:** send: "⚠️ El vídeo de hoy está programado (<time>) pero la fábrica no dejó registro ni comprobación. Revísalo en un chat." Do not write the log yourself.
   - **A network is missing from today's posts** (Instagram, TikTok or YouTube): say which one.
5. Never commit anything: this task only reads and notifies.
