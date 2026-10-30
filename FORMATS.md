# Mr. Whiskerfact: formats

Each reel uses one format. They share the brand rules (colours, hook from frame 0, subtitles, outro) but have different structures, so the channel never looks like one template repeated. The nightly run chooses the format with the `format` test in `growth/experiments.json`.

| Format | Hook on screen (frame 0) | Structure |
|---|---|---|
| **explainer** | "Why do we get goosebumps?" | hook → context → 2–3 numbered steps → surprising fact → wrap ("now you know") |
| **myth** | "MYTH OR FACT? Goldfish have a 3-second memory." | the belief, stated big → a stamp appears (MYTH / FACT / HALF TRUE) after a 1 s beat → where the belief comes from → what the evidence shows (2 steps) → the real answer → wrap |
| **versus** | "Cheetah vs pronghorn: who wins a marathon?" | split screen: two sides with matching drawings → 3 rounds (each a stat or property, a bar or score that grows, one winner per round) → the twist → final score → wrap |
| **what_if** | "What if the Moon disappeared tonight?" | the premise → first minute or hour → first day → long term → what it teaches us about the real world → wrap. Only use effects that published scientists describe, and say "scientists expect" |
| **quiz** | "Pop quiz: which is older, sharks or trees?" | question with 3 options (A, B, C) on screen → "Comment your answer before I tell you" plus a 2-second ticking clock → reveal with stamp → why → wrap |

## Rules
- The `myth` format needs a myth that is really widely believed (demand check), plus a source that addresses the myth directly.
- `versus` must compare like with like, using the same units.
- `quiz` options must all be plausible, and the wrong options must be verifiably wrong.
- `what_if` must never be scary-for-effect or catastrophising. Real disasters and wars belong in neutral `explainer` or `myth` reels, never in hypotheticals.
- Every format keeps the 65–75 s length, the precision check and the hard limits in PERSONALITY.md.
