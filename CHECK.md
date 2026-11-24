# Mr. Whiskerfact: post check

This is a one-shot task that runs about 30 minutes after a reel's scheduled time. It confirms that the reel really went out on every network. Since 24/11/2026 the reels are published with Buffer (one post per network). Reels logged before that date have `metricool_uuid`: for those, the check used the Metricool connector `getScheduledPosts` (brandId `7740980`); they no longer need a check.

1. For each of the three Buffer post ids given in the task (TikTok, Instagram, YouTube), call the Buffer connector `get_post` (never `edit_post` or `delete_post`). Read `status`, `error` and `externalLink`.
   - **OK:** `status: sent`.
   - **Still `scheduled` or `sending`:** wait about 10 minutes and look once more. A second time counts as a failure.
   - **Failure:** `status: error` (read `error.message`), `needs_approval`, `draft`, or the post is missing.
2. **Links:** use `externalLink` as the public URL. For TikTok, if it is empty or looks broken, rebuild it as `https://www.tiktok.com/@mrwhiskerfact/video/<id>` when the id is known.
3. Write the result into the reel's entry in `log/published.json`:
   - `"check": {"at": "<ISO time>", "instagram": "...", "tiktok": "...", "youtube": "..."}`
   - the public URLs
   - Commit and push. (Pull first, and edit only that field.)
4. Send one push notification in Spanish:
   - **All OK:** "✅ «<title>» publicado en TikTok, Instagram y YouTube." plus the links.
   - **Any failure:** "⚠️ «<title>» no se publicó en <network>: <error>." plus one line on what the owner can do, for example re-connect that network in Buffer or publish it by hand from the Buffer queue. **Never re-publish or edit the post yourself.**
