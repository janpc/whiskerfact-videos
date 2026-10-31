# Weekly plan (Monday morning, unattended)

Goal: decide the reels of the coming week in advance, so the owner can generate the missing characters in Gemini (free) before the nightly factory needs them.

1. Read `FACTORY.md` (sections 1, 1b, 2), `schedule.json`, `growth/calendar.json`, `growth/topics.md`, `growth/insights.md`, `log/published.json` and `factory/library/index.json`.
2. **Publishing days:** from the rules in `schedule.json` and the log, list the dates in the next 7 days (today included) on which the factory will publish.
3. **One topic per day.** Follow FACTORY step 2 exactly: special dates first, category rotation, demand check, a format from FORMATS.md, and no repeats of past topics. Do a quick plausibility check that each topic has at least two solid sources (full verification happens on the day).
4. **Characters:** for each reel, list the characters it really needs (people, animals) to show the story well. Match each one against the library (by name or tags). A character that is not there is `missing`.
5. **Prompts:** for every missing character, write the two Gemini prompts (movement sheet, acting sheet) to `growth/week_prompts.md`, following `factory/library/PROMPT.md` and the copy-paste format below. Use the right cycle: a walk cycle for people, a run cycle for four-legged animals, flying or swimming for others.
6. Write `growth/week_plan.json` as `[{"date", "topic", "category", "format", "event"?, "characters": [...], "missing": [...]}]`, then commit and push. Edit only `growth/`.
7. **Notification in Spanish, at most 6 lines:** the week's dates and topics in one line each, then "Personajes que faltan: X, Y" (or "No falta ningún personaje"), then "Los prompts están en growth/week_prompts.md o pídemelos en el chat." Never generate images yourself and never spend ElevenLabs credits.

Copy-paste format for `week_prompts.md`: one block per sheet, starting with which images to attach (`STYLE_REF.png`, plus the character's movement sheet when it is an acting sheet), then the full prompt text.
