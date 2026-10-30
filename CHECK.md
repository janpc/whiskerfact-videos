# Mr. Whiskerfact: post check

This is a one-shot task that runs about 30 minutes after a reel's scheduled time. It confirms that the reel really went out on every network.

1. Use the Metricool connector `getScheduledPosts` with these values:
   - brandId `7740980`, timezone `Europe/Madrid`, `extendedRange: true`
   - from 3 hours before to 1 hour after the scheduled time
   - Find the post with the given Metricool **uuid**.
2. For each provider (instagram, tiktok, youtube), read `status` and `publicUrl`.
   - **OK:** `PUBLISHED`, or TikTok `AWAITING_CONFIRMATION` with a published id.
   - **Still `PENDING`:** wait about 10 minutes and look once more. A second `PENDING` counts as a failure.
   - **Failure:** anything else (`ERROR`, `FAILED`, missing).
3. Write the result into the reel's entry in `log/published.json`:
   - `"check": {"at": "<ISO time>", "instagram": "...", "tiktok": "...", "youtube": "..."}`
   - the public URLs
   - Commit and push. (Pull first, and edit only that field.)
4. Send one push notification in Spanish:
   - **All OK:** "✅ «<title>» publicado en TikTok, Instagram y YouTube." plus the links.
   - **Any failure:** "⚠️ «<title>» no se publicó en <network>: <detailedStatus>." plus one line on what the owner can do, for example re-connect that network in Metricool or publish it by hand from the Metricool planner. **Never re-publish or edit the post yourself.**
