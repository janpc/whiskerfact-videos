# Gemini prompts for the week of 2026-11-23

Reels: **2026-11-23** (science, versus: lightning vs the Sun; already rendered, nothing missing), **2026-11-26** (nature, what if: a dog's nose for one day; base, standard length) and **2026-11-28** (history, explainer: why a week has 7 days; base, standard length).

Missing, 3 sheets in priority order (by publishing date):
1. **nose_items** (4x4, 26/11)
2. **large_w48** (2x2 LARGE: nose_cutaway, brain_compare, dog_sniffing for 26/11; babylon_night_sky for 28/11)
3. **week_items** (4x4, 28/11)

No new characters: the library `dog`, `young_man` and `ancient_person` are reused. Also reused: wifi_objects (clock), moon_items (sun, moon_near), mammoth_quiz_items (sundial).
Style reference: object sheets attach **`growth/style_ref_objects_4x4.png`** (the clean 4x4 contact sheet built from library crops); for `large_w48` also attach `factory/library/dog/sheet1.png` so the sniffing dog is the same dog.
Generate in the Gemini app, then add each sheet with the `library.py add` line under its prompt (run from `factory/`; `-` marks an empty cell).

---

## nose_items · object / illustration sheet 4x4 (reel of 2026-11-26)

**Attach:** `growth/style_ref_objects_4x4.png`

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: what the world would smell like with a dog's nose, a cheerful everyday morning and a walk in town, no brands.
Make ONE image: a grid of 4 columns × 4 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. Perfectly flat pure green background (#00FF00). No labels, no text, no numbers, no divider lines, no borders, no shadows, no characters, no hands, no logos.
Cells, left to right, top to bottom: 1 a brown dog's nose seen from the front, big and shiny, with two comma-shaped nostrils and small side slits; 2 a metal teaspoon heaped with white sugar; 3 a rectangular outdoor swimming pool with lane ropes, seen from above at an angle; 4 a breakfast plate with two fried eggs, bacon strips and toast; 5 a steaming coffee mug; 6 a chocolate bar with the wrapper half peeled back; 7 a single red rose with two leaves; 8 a red fire hydrant; 9 a folded newspaper with only grey lines, no readable text; 10 a trail of three shoe prints in a row, fading from dark to faint; 11 a trail of three paw prints in a row, fading from dark to faint; 12 a bloodhound with long droopy ears, side view facing right; 13 a yellow-green tennis ball; 14 a red dog leash, coiled; 15 an old-fashioned street lamp post; 16 a sandwich with lettuce, cheese and ham.
```
Pose names: `dog_nose_front sugar_spoon swimming_pool breakfast_plate coffee_mug chocolate_bar rose fire_hydrant newspaper shoe_prints paw_prints bloodhound tennis_ball leash lamp_post sandwich`
Add with: `python3 library.py add <sheet.png> nose_items dog_nose_front,sugar_spoon,swimming_pool,breakfast_plate,coffee_mug,chocolate_bar,rose,fire_hydrant,newspaper,shoe_prints,paw_prints,bloodhound,tennis_ball,leash,lamp_post,sandwich --grid 4x4 --tags object,nature,dog,smell --source gemini`

---

## large_w48 · LARGE items sheet 2x2 (items 1-3 for 2026-11-26, item 4 for 2026-11-28)

**Attach:** `growth/style_ref_objects_4x4.png` + `factory/library/dog/sheet1.png` (the channel's brown dog, for cell 3)

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW large illustrations: key illustrations for two reels: how a dog's nose works, and why the week has seven days.
Make ONE image: a grid of 2 columns × 2 rows of equal square cells. Each cell shows ONE separate item on a perfectly flat pure green background (#00FF00). Draw each item large, filling most of its cell, with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. No divider lines, no numbers, no text, no labels, no borders, no shadows, no logos. Scenes fill their cell inside that margin.
Cells, left to right, top to bottom: 1 a friendly side cut-away of a dog's snout and head facing right, like a simple science diagram: air going in at the nostril splits into two paths, one to the lungs and one up into a big curled maze of thin bony scrolls at the back of the nose, coloured soft pink and orange; 2 two brains side by side seen from the side, a small dog brain on the left and a human brain on the right, each with its smell area (the olfactory bulb at the front) coloured bright orange: big on the dog brain, tiny on the human brain; 3 the SAME brown dog as in the attached dog sheet (same colours and proportions), side view facing right, walking with its nose down to the ground, sniffing, tail up, happy and focused; 4 a night scene in ancient Babylon: a stepped mud-brick ziggurat under a deep blue starry sky, a crescent Moon and five bright coloured dots of planets in a gentle arc above it, no people.
```
Pose names: `nose_cutaway brain_compare dog_sniffing babylon_night_sky`
Add with: `python3 library.py add <sheet.png> large_w48 nose_cutaway,brain_compare,dog_sniffing,babylon_night_sky --grid 2x2 --tags illustration,nature,dog,history,large --source gemini`

---

## week_items · object / illustration sheet 4x4 (reel of 2026-11-28)

**Attach:** `growth/style_ref_objects_4x4.png`

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a history explainer about why the week has seven days, from Babylonian sky-watchers to Rome to the French Revolution.
Make ONE image: a grid of 4 columns × 4 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. Perfectly flat pure green background (#00FF00). No labels, no text, no numbers, no divider lines, no borders, no shadows, no characters, no hands, no logos.
Cells, left to right, top to bottom: 1 a small clay tablet with wedge-shaped cuneiform marks (decorative, not readable); 2 a stepped Mesopotamian ziggurat in daylight; 3 a row of four Moon phases: new, first quarter, full, last quarter; 4 the planet Saturn with its rings; 5 the planet Jupiter with its stripes and red spot; 6 the planet Mars, rusty red; 7 the planet Venus, pale creamy yellow with soft clouds; 8 the planet Mercury, small and grey with craters; 9 a modern wall calendar page with a grid of seven columns, empty boxes, no numbers; 10 an ancient Roman bronze coin with the profile of an emperor wearing a laurel wreath; 11 an ancient Roman market stall with amphorae, bread and fruit under a striped awning; 12 a round clock face divided into 10 hours instead of 12, marked only with ten tick marks, no numbers; 13 a large paper calendar sheet with a tricolour blue-white-red ribbon on top and a grid of ten columns, no numbers; 14 a hammock between two palm trees, relaxing weekend mood; 15 an ancient star chart on a rolled-out scroll, with dots of stars joined by thin lines; 16 leave empty (flat green).
```
Pose names: `clay_tablet ziggurat moon_phases saturn jupiter mars venus mercury wall_calendar roman_coin market_stall decimal_clock revolution_calendar weekend_hammock star_chart`
Add with: `python3 library.py add <sheet.png> week_items clay_tablet,ziggurat,moon_phases,saturn,jupiter,mars,venus,mercury,wall_calendar,roman_coin,market_stall,decimal_clock,revolution_calendar,weekend_hammock,star_chart,- --grid 4x4 --tags object,illustration,history,calendar,space --source gemini`
