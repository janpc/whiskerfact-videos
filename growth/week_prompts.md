# Gemini prompts for the week of 2026-11-16

Reels: **2026-11-16** (space, what if: the Moon; already rendered, nothing missing), **2026-11-18** (tech, myth: charging your phone overnight; B2 short variant), **2026-11-21** (history, quiz: what was NOT at the first Thanksgiving; themed, base) and **2026-11-23** (science, versus: lightning vs the Sun; B2 short variant).

Missing, 9 sheets in priority order (by publishing date):
1. **battery_items** (4x4, 18/11) 2. **large_w47** (2x2 LARGE: battery_cutaway, bedroom_night for 18/11; sun_cutaway, thunderstorm for 23/11)
3. **pilgrim_man** (2 sheets, 21/11) 4. **wampanoag_man** (2 sheets, 21/11) 5. **thanksgiving_items** (4x4, 21/11) 6. **large_thanksgiving** (2x2 LARGE: harvest_feast_1621, modern_table, plymouth_1621)
7. **lightning_items** (4x4, 23/11)

Already in the library and reused: young_man, scientist, wifi_objects (phone, clock), moon_items (sun, stopwatch). The thermometer of battery_items is reused on 23/11.
Style reference: object sheets attach **`growth/style_ref_objects_4x4.png`** (a clean 4x4 contact sheet built from the moon_items library crops, made in this plan); character sheets attach `factory/library/STYLE_REF.png` as usual.
Generate in the Gemini app, then add each sheet with the `library.py add` line under its prompt (run from `factory/`; `-` marks an empty cell).

---

## battery_items · object / illustration sheet 4x4 (reel of 2026-11-18)

**Attach:** `growth/style_ref_objects_4x4.png` (clean contact sheet of the moon_items crops; use it instead of `wifi_objects/sheet1.png`)

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a myth-or-fact about charging a smartphone overnight, calm bedtime mood, generic phones with no brand.
Make ONE image: a grid of 4 columns × 4 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. Perfectly flat pure green background (#00FF00). No labels, no text, no numbers, no divider lines, no borders, no shadows, no characters, no hands, no logos.
Cells, left to right, top to bottom: 1 a white USB wall charger plug with a short cable end, three-quarter view; 2 a coiled white charging cable; 3 a generic smartphone lying flat, plugged into a cable, screen showing a green battery icon; 4 a small wooden bedside table with a lamp switched on; 5 a flat rectangular smartphone battery pack (silver pouch cell), three-quarter view; 6 two old-fashioned rechargeable AA batteries, chunky and slightly worn; 7 a 1990s brick mobile phone with a stubby antenna and small screen; 8 a classic glass thermometer with a red liquid column near the top; 9 a small car parked under a blazing sun, heat waves rising, side view facing right; 10 a rectangular portable power bank with four small indicator lights; 11 a big rounded battery icon, full, bright green; 12 the same big battery icon, almost empty, red sliver. Leave the remaining cells empty (flat green).
```
Pose names: `charger_plug charging_cable phone_charging nightstand li_battery nicd_battery old_phone thermometer hot_car power_bank battery_full battery_low`
Add with: `python3 library.py add <sheet.png> battery_items charger_plug,charging_cable,phone_charging,nightstand,li_battery,nicd_battery,old_phone,thermometer,hot_car,power_bank,battery_full,battery_low,-,-,-,- --grid 4x4 --tags object,tech,phone,battery --source gemini`

---

## large_w47 · LARGE items sheet 2x2 (items 1-2 for 2026-11-18, items 3-4 for 2026-11-23)

**Attach:** `growth/style_ref_objects_4x4.png`

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW large illustrations: key illustrations for two reels: inside a phone battery, and lightning versus the Sun.
Make ONE image: a grid of 2 columns × 2 rows of equal square cells. Each cell shows ONE separate item on a perfectly flat pure green background (#00FF00). Draw each item large, filling most of its cell, with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. No divider lines, no numbers, no text, no labels, no borders, no shadows, no logos. Scenes fill their cell inside that margin.
Cells, left to right, top to bottom: 1 a smartphone battery cut open as a friendly diagram: layered sheets rolled inside, with small glowing dots (lithium ions) between two layers; 2 a cosy bedroom at night seen from the side: a bed with a pillow, a bedside table with a phone charging on it, a window with the moon; nobody in the bed; 3 the Sun cut open like a slice: a glowing white-yellow core in the centre, orange and red layers around it, a bright yellow surface with a few spots and a faint glowing corona; 4 a dark thunderstorm cloud over a green field with one bright yellow-white lightning bolt striking the ground.
```
Pose names: `battery_cutaway bedroom_night sun_cutaway thunderstorm`
Add with: `python3 library.py add <sheet.png> large_w47 battery_cutaway,bedroom_night,sun_cutaway,thunderstorm --grid 2x2 --tags illustration,tech,science,large --source gemini`

---

## pilgrim_man · sheet 1 (movement) (reel of 2026-11-21)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: an English colonist man of Plymouth in 1621, historically accurate (NOT the buckle-hat cliche): a brown or dull-green wool doublet, white linen collar, knee breeches, wool stockings, plain leather shoes without buckles, a simple felt hat with a round crown, short beard. Friendly, ordinary farmer look.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and clothes), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 walking cycle side view, contact (legs apart, right foot forward); 2 walking cycle side view, down (knees bent); 3 walking cycle side view, passing (legs together); 4 walking cycle side view, up (on toes); 5 standing still, side view; 6 standing still, front view, arms relaxed; 7 three-quarter view; 8 sitting on the ground; 9 jumping with joy.
```
Pose names: `walk1 walk2 walk3 walk4 side front three_quarter sit jump`
Add with: `python3 library.py add <sheet1.png> pilgrim_man walk1,walk2,walk3,walk4,side,front,three_quarter,sit,jump --tags person,history,thanksgiving,1621 --source gemini`

---

## pilgrim_man · sheet 2 (acting)

**Attach:** `factory/library/STYLE_REF.png` + the pilgrim_man sheet 1 (movement) generated above

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw the SAME character as in the attached movement sheet (same face, proportions, colours and clothes), not the cat of the style sheet. No buckles, no weapons.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character, full body, front view, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects.
Cells, left to right, top to bottom: 1 talking, mouth open, one hand gesturing; 2 pointing up, explaining; 3 thinking, hand on chin; 4 very happy, big smile; 5 scared, hands up; 6 surprised, mouth open; 7 waving hello; 8 shivering with cold, arms crossed; 9 shrugging.
```
Pose names: `talk point think happy scared surprised wave cold shrug`
Add with: `python3 library.py add <sheet2.png> pilgrim_man talk,point,think,happy,scared,surprised,wave,cold,shrug --tags person,history,thanksgiving,1621 --source gemini`

---

## wampanoag_man · sheet 1 (movement) (reel of 2026-11-21)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: a Wampanoag man of 17th-century coastal New England, drawn respectfully and accurately (NOT a Plains feather headdress, NOT a cartoon stereotype): long dark hair tied back with a single small feather at most, deerskin breechcloth and leggings, deerskin moccasins, a deerskin mantle over one shoulder, a simple shell-bead (wampum) necklace. Dignified, friendly, natural face.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and clothes), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 walking cycle side view, contact (legs apart, right foot forward); 2 walking cycle side view, down (knees bent); 3 walking cycle side view, passing (legs together); 4 walking cycle side view, up (on toes); 5 standing still, side view; 6 standing still, front view, arms relaxed; 7 three-quarter view; 8 sitting on the ground; 9 jumping with joy.
```
Pose names: `walk1 walk2 walk3 walk4 side front three_quarter sit jump`
Add with: `python3 library.py add <sheet1.png> wampanoag_man walk1,walk2,walk3,walk4,side,front,three_quarter,sit,jump --tags person,history,thanksgiving,1621,wampanoag --source gemini`

---

## wampanoag_man · sheet 2 (acting)

**Attach:** `factory/library/STYLE_REF.png` + the wampanoag_man sheet 1 (movement) generated above

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw the SAME character as in the attached movement sheet (same face, proportions, colours and clothes), not the cat of the style sheet. No weapons, no war paint, no headdress.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character, full body, front view, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects.
Cells, left to right, top to bottom: 1 talking, mouth open, one hand gesturing; 2 pointing up, explaining; 3 thinking, hand on chin; 4 very happy, big smile; 5 scared, hands up; 6 surprised, mouth open; 7 waving hello; 8 shivering with cold, arms crossed; 9 shrugging.
```
Pose names: `talk point think happy scared surprised wave cold shrug`
Add with: `python3 library.py add <sheet2.png> wampanoag_man talk,point,think,happy,scared,surprised,wave,cold,shrug --tags person,history,thanksgiving,1621,wampanoag --source gemini`

---

## thanksgiving_items · object / illustration sheet 4x4 (reel of 2026-11-21)

**Attach:** `growth/style_ref_objects_4x4.png` (clean contact sheet of the moon_items crops; use it instead of `wifi_objects/sheet1.png`)

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a history quiz about what was really eaten at the 1621 harvest feast in Plymouth, warm autumn colours.
Make ONE image: a grid of 4 columns × 4 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. Perfectly flat pure green background (#00FF00). No labels, no text, no numbers, no divider lines, no borders, no shadows, no characters, no hands, no logos.
Cells, left to right, top to bottom: 1 a live wild turkey, bronze-brown feathers, side view facing right; 2 a modern golden roast turkey on a platter; 3 a white-tailed deer standing, side view facing right; 4 a wild duck (mallard), side view facing right; 5 a whole orange pumpkin with a short stem; 6 a modern pumpkin pie with one slice cut out and a dollop of cream; 7 two ears of multicoloured flint corn with dry husks pulled back; 8 a small pile of wild red cranberries; 9 a few blue-black mussels, two of them open; 10 a single long eel, gently curved; 11 a 17th-century cone-shaped sugar loaf wrapped in blue paper at the base; 12 an old folded letter on parchment with a feather quill and an ink pot, no readable text; 13 a 17th-century wooden sailing ship with three masts and cream sails, side view facing right; 14 a black iron cooking pot hanging over a small open fire; 15 a wooden bowl of thick yellow corn porridge with a wooden spoon. Leave the remaining cells empty (flat green).
```
Pose names: `wild_turkey roast_turkey deer duck pumpkin pumpkin_pie corn_ears cranberries mussels eel sugar_loaf old_letter mayflower cooking_pot corn_porridge`
Add with: `python3 library.py add <sheet.png> thanksgiving_items wild_turkey,roast_turkey,deer,duck,pumpkin,pumpkin_pie,corn_ears,cranberries,mussels,eel,sugar_loaf,old_letter,mayflower,cooking_pot,corn_porridge,- --grid 4x4 --tags object,illustration,history,thanksgiving,food --source gemini`

---

## large_thanksgiving · LARGE items sheet 2x2 (reel of 2026-11-21)

**Attach:** `growth/style_ref_objects_4x4.png`

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW large illustrations: key scenes of the 1621 harvest feast in Plymouth and a modern Thanksgiving table, warm autumn light, no people.
Make ONE image: a grid of 2 columns × 2 rows of equal square cells. Each cell shows ONE separate item on a perfectly flat pure green background (#00FF00). Draw each item large, filling most of its cell, with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. No divider lines, no numbers, no text, no labels, no borders, no shadows, no logos. Scenes fill their cell inside that margin.
Cells, left to right, top to bottom: 1 an outdoor 1621 harvest feast scene with no people: long rough wooden tables on the grass, wooden bowls of corn, roasted venison over an open fire, ducks on a spit, autumn trees behind; 2 a modern Thanksgiving dinner table seen from slightly above: a golden roast turkey, mashed potatoes, cranberry sauce, a pumpkin pie, plates and candles, no people; 3 the small Plymouth village of 1621: a few wooden houses with thatched roofs along a dirt street, a wooden palisade, the sea in the distance. Leave cell 4 empty (flat green).
```
Pose names: `harvest_feast_1621 modern_table plymouth_1621`
Add with: `python3 library.py add <sheet.png> large_thanksgiving harvest_feast_1621,modern_table,plymouth_1621,- --grid 2x2 --tags illustration,history,thanksgiving,large --source gemini`

---

## lightning_items · object / illustration sheet 4x4 (reel of 2026-11-23)

**Attach:** `growth/style_ref_objects_4x4.png` (clean contact sheet of the moon_items crops; use it instead of `wifi_objects/sheet1.png`)

```
Using exactly the same illustration style as the attached reference sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a versus between lightning and the Sun (which is hotter), bright and exciting but not scary.
Make ONE image: a grid of 4 columns × 4 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a clear empty margin of green around it: nothing may touch or cross the edge of its cell. Perfectly flat pure green background (#00FF00). No labels, no text, no numbers, no divider lines, no borders, no shadows, no characters, no hands, no logos.
Cells, left to right, top to bottom: 1 a single bright yellow-white zigzag lightning bolt; 2 a dark grey storm cloud; 3 a fulgurite: a rough branching tube of glassy fused sand; 4 a metal lightning rod on a small roof peak; 5 a tree trunk split down the middle by a lightning strike, a little smoke, no fire; 6 a glowing orange loop of plasma rising from a curved piece of the Sun's surface; 7 a small glowing white-hot ball with soft yellow rays (the Sun's core); 8 an hourglass with glowing star dust instead of sand. Leave the remaining cells empty (flat green).
```
Pose names: `lightning_bolt storm_cloud fulgurite lightning_rod struck_tree solar_prominence sun_core_glow hourglass_space`
Add with: `python3 library.py add <sheet.png> lightning_items lightning_bolt,storm_cloud,fulgurite,lightning_rod,struck_tree,solar_prominence,sun_core_glow,hourglass_space,-,-,-,-,-,-,-,- --grid 4x4 --tags object,illustration,science,lightning,sun --source gemini`

---

Prompts written by the weekly plan of 2026-11-16. Nothing was generated.
