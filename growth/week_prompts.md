# Gemini prompts for the week of 2026-11-09

Reels this week: **2026-11-11** (history, quiz: when did the last woolly mammoths die out?), **2026-11-13** (body, versus: bone vs steel) and **2026-11-16** (space, what if: standing on the Moon looking back at Earth; rendered in the night of 15→16).
Missing: **woolly_mammoth** (character, 2 sheets, reel of 11/11) **astronaut** (character, 2 sheets, reel of 11/16) and three object/illustration sheets: **mammoth_quiz_items** (11/11), **bone_steel_items** (11/13) and **moon_items** (11/16). Already in the library and reused: ancient_person, early_human, scientist, young_man, wifi_objects (clock), earth_tunnel_items (earth).
Generate in the Gemini app, then add each sheet with the `library.py add` line under its prompt (run from `factory/`).

---

## woolly_mammoth · sheet 1 (movement)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: a woolly mammoth, an adult with long shaggy reddish-brown fur, a high domed head, a sloping back, small furry ears, a long trunk and two long curved ivory tusks. It is a real animal walking on four legs: no clothes, no accessories.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and fur), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 running cycle side view (a heavy trot), front and back legs stretched apart; 2 running cycle side view, legs gathered under the body; 3 running cycle side view, front legs reaching forward; 4 running cycle side view, back legs pushing off; 5 walking side view, first step; 6 walking side view, second step; 7 standing still, side view; 8 front view, trunk hanging down between the tusks; 9 lying down, resting.
```
Pose names: `run1 run2 run3 run4 walk1 walk2 side front sit`
Add with: `python3 library.py add <sheet1.png> woolly_mammoth run1,run2,run3,run4,walk1,walk2,side,front,sit --tags animal,mammoth,ice_age,prehistory --source gemini`

---

## woolly_mammoth · sheet 2 (acting)

**Attach:** `factory/library/STYLE_REF.png` + the woolly mammoth's sheet 1 (movement) generated above

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw the SAME woolly mammoth as in the attached movement sheet (same proportions, reddish-brown shaggy fur, domed head, curved tusks, long trunk), not the cat of the style sheet. No clothes, no accessories.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character, full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 happy, eyes smiling, trunk curled up; 2 scared, fur standing on end, leaning back; 3 curious, head tilted, trunk reaching forward; 4 eating, trunk pulling a tuft of grass to its mouth; 5 sleeping, lying down with eyes closed; 6 trumpeting, trunk raised high, mouth open; 7 looking back over its shoulder; 8 a small playful hop with the front feet off the ground; 9 alert, ears out, trunk raised slightly.
```
Pose names: `happy scared curious eat sleep call look_back jump alert`
Add with: `python3 library.py add <sheet2.png> woolly_mammoth happy,scared,curious,eat,sleep,call,look_back,jump,alert --tags animal,mammoth,ice_age,prehistory --source gemini`

---

## mammoth_quiz_items · object / illustration sheet (reel of 2026-11-11)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a history quiz about when the last woolly mammoths lived, compared with ancient Egypt and Rome.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no shadows, no characters, no hands. Scenes fill their cell, with flat green only in the empty sky.
Cells, left to right, top to bottom: 1 the Great Pyramid of Giza finished, smooth sides, golden sand at its base; 2 the same pyramid half built, with a long mud-brick ramp and stacked stone blocks; 3 a small rocky Arctic island in a dark blue sea with patches of snow and tundra grass (Wrangel Island); 4 a wide icy Ice Age tundra landscape with snow and low hills; 5 a single long curved mammoth tusk, lying flat; 6 a mammoth skeleton standing, side view, as in a museum; 7 an early farm field with a few rows of wheat and a wooden hoe; 8 the Roman Colosseum, front three-quarter view; 9 a large cut stone block on a wooden sledge with ropes.
```
Pose names: `pyramid pyramid_building wrangel_island tundra tusk mammoth_skeleton first_farm colosseum stone_sledge`
Add with: `python3 library.py add <sheet.png> mammoth_quiz_items pyramid,pyramid_building,wrangel_island,tundra,tusk,mammoth_skeleton,first_farm,colosseum,stone_sledge --tags illustration,object,history,mammoth,egypt --source gemini`

---

## bone_steel_items · object / illustration sheet (reel of 2026-11-13)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a friendly comparison between human bone and steel, clean and not gory (no blood, no injuries).
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no characters, no hands.
Cells, left to right, top to bottom: 1 a human thigh bone (femur), ivory white, lying horizontally; 2 the same bone cut in half, showing a hard outer shell and a spongy honeycomb inside; 3 a shiny grey steel bar of the same length, lying horizontally; 4 a steel I-beam girder, three-quarter view; 5 an old-fashioned balance scale, empty, with two pans level; 6 a material-testing press: two thick metal plates squeezing a small sample between them; 7 an X-ray image of a human leg showing the bones in white on a dark blue film; 8 a bone with a thin healed line where a crack has knitted back together, with a small glowing sparkle; 9 a full human skeleton standing, front view, friendly and not spooky.
```
Pose names: `femur femur_section steel_bar steel_beam balance test_press xray_leg bone_healed skeleton`
Add with: `python3 library.py add <sheet.png> bone_steel_items femur,femur_section,steel_bar,steel_beam,balance,test_press,xray_leg,bone_healed,skeleton --tags illustration,object,body,bone,steel --source gemini`

---

## astronaut · sheet 1 (movement) (reel of 2026-11-16)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: a human astronaut in a chunky white spacesuit with light grey joints, a small backpack life-support unit, white gloves and boots, and a round helmet with a gold reflective visor raised enough to show a friendly face. No flags, no patches with text, no logos.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and suit), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 walking cycle side view, contact (legs apart, right foot forward); 2 walking cycle side view, down (knees bent); 3 walking cycle side view, passing (legs together); 4 walking cycle side view, up (on toes); 5 standing still, side view; 6 standing still, front view, arms relaxed; 7 three-quarter view; 8 sitting on the ground; 9 a big floaty low-gravity bunny hop, both feet off the ground.
```
Pose names: `walk1 walk2 walk3 walk4 side front three_quarter sit jump`
Add with: `python3 library.py add <sheet1.png> astronaut walk1,walk2,walk3,walk4,side,front,three_quarter,sit,jump --tags person,astronaut,space,moon --source gemini`

---

## astronaut · sheet 2 (acting)

**Attach:** `factory/library/STYLE_REF.png` + the astronaut's sheet 1 (movement) generated above

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw the SAME astronaut as in the attached movement sheet (same white spacesuit, backpack, gold visor raised showing the face), not the cat of the style sheet. No flags, no logos, no text.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character, full body, front view, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects.
Cells, left to right, top to bottom: 1 talking, mouth open, one hand gesturing; 2 pointing up at the sky, explaining; 3 thinking, glove on the helmet's chin; 4 very happy, big smile; 5 scared, hands up; 6 surprised, mouth open; 7 waving hello; 8 looking up in wonder, head tilted back; 9 shrugging.
```
Pose names: `talk point think happy scared surprised wave look_up shrug`
Add with: `python3 library.py add <sheet2.png> astronaut talk,point,think,happy,scared,surprised,wave,look_up,shrug --tags person,astronaut,space,moon --source gemini`

---

## moon_items · object / illustration sheet (reel of 2026-11-16)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: standing on the Moon and looking back at Earth, calm and full of wonder (not scary).
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no shadows, no characters, no hands, no flags, no logos. Scenes fill their cell; leave the sky of cell 1 flat green so it can be replaced.
Cells, left to right, top to bottom: 1 a grey lunar landscape with craters and gentle hills, low horizon; 2 the full Moon's near side, the familiar face with dark seas (maria); 3 the Moon's far side, lighter and covered in many more craters; 4 a small lunar lander with four legs and gold foil; 5 a single astronaut boot footprint in grey dust, seen from above; 6 a small grey moon rock; 7 a bright yellow-white Sun with short rays; 8 a sandy beach with a high tide line and gentle waves; 9 a small four-wheeled lunar rover, side view facing right.
```
Pose names: `moon_surface moon_near moon_far lander footprint moon_rock sun tide_beach rover`
Add with: `python3 library.py add <sheet.png> moon_items moon_surface,moon_near,moon_far,lander,footprint,moon_rock,sun,tide_beach,rover --tags illustration,object,space,moon --source gemini`
