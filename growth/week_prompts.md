# Gemini prompts for the week of 2026-11-02

Missing this week: **cat** (character, reel of 2026-11-08) and three object/illustration sheets: **wifi_objects** (2026-11-03), **earth_tunnel_items** (2026-11-06), **cat_eye_night_items** (2026-11-08). Characters are in the first part, object sheets at the end.
Generate in the Gemini app, then add with `python3 library.py add <sheet.png> cat <9 pose names> --tags animal,cat,pet,night --source gemini`.

---

## cat · sheet 1 (movement)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: an ordinary grey tabby house cat with darker grey stripes, a white chest and paws, big green eyes with vertical slit pupils, pink nose, long tail. It is a normal real-world cat walking on four legs: no clothes, no glasses, no bow tie, no accessories, and it must look clearly different from the cat in the reference sheet.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and markings), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 running cycle side view, legs stretched out front and back; 2 running cycle side view, legs gathered under the body; 3 running cycle side view, front legs reaching forward; 4 running cycle side view, back legs pushing off; 5 walking side view, first step; 6 walking side view, second step; 7 standing still, side view; 8 front view, sitting up straight looking at the viewer; 9 lying down, relaxed.
```
Pose names: `run1 run2 run3 run4 walk1 walk2 side front sit`

---

## cat · sheet 2 (acting)

**Attach:** `factory/library/STYLE_REF.png` + the cat's sheet 1 (movement) generated above

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw the SAME grey tabby house cat as in the attached movement sheet (same proportions, stripes, white chest and paws, green eyes with slit pupils), not the cat of the style sheet. No clothes, no glasses, no accessories.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character, full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 happy, eyes half closed, tail up; 2 scared, fur puffed up, back arched; 3 curious, head tilted; 4 eating from the ground, head down; 5 sleeping curled up in a ball; 6 meowing, mouth open; 7 looking back over its shoulder; 8 jumping; 9 alert, ears up, pupils wide and round as in the dark.
```
Pose names: `happy scared curious eat sleep call look_back jump alert`

---

## wifi_objects · object / illustration sheet (reel of 2026-11-03)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: the things in a Wi-Fi comparison, in a plain, neutral, modern look with no brand logos.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no characters, no hands.
Cells, left to right, top to bottom: 1 white Wi-Fi router with two antennas, front three-quarter view; 2 the same router seen from the side; 3 smartphone, front view, blank screen; 4 laptop, open, three-quarter view, blank screen; 5 microwave oven, door closed, front view; 6 microwave oven with the door open and light on; 7 a section of brick wall, front view, as a flat slab; 8 a section of thick concrete wall, front view, as a flat slab; 9 a small round wall clock, no numbers needed.
```
Pose names: `router router_side phone laptop microwave microwave_open wall_brick wall_concrete clock`
Add with: `python3 library.py add <sheet.png> wifi_objects router,router_side,phone,laptop,microwave,microwave_open,wall_brick,wall_concrete,clock --tags object,tech,home --source gemini`

---

## earth_tunnel_items · object / illustration sheet (reel of 2026-11-06)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: a thought experiment about a tunnel straight through the Earth, simple and friendly (not scary).
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no characters, no hands.
Cells, left to right, top to bottom: 1 planet Earth seen from space with simple continents; 2 Earth cut in half showing the layers (crust, mantle, outer core, inner core) as a flat cross-section, with a thin straight tunnel running through the exact centre from top to bottom; 3 a grassy landscape with a round hole in the ground seen from the front at a slight angle, with a few rocks around the rim; 4 a vertical cutaway of a deep tunnel with layered soil and rock on both sides and a faint light at the bottom; 5 a slice of ground showing grass, soil layers and rock, side view; 6 a landscape on the opposite side of the world, drawn upside down, with a round hole in the ground; 7 a big stopwatch showing about 40 minutes (no numbers, just the dial and one hand); 8 a small round pit rim viewed from above, dark inside; 9 a simple compass rose pointing north-south.
```
Pose names: `earth earth_cutaway hole_entry tunnel_cut ground_slice hole_exit_upside stopwatch pit_top compass`
Add with: `python3 library.py add <sheet.png> earth_tunnel_items earth,earth_cutaway,hole_entry,tunnel_cut,ground_slice,hole_exit_upside,stopwatch,pit_top,compass --tags illustration,object,science,earth --source gemini`

---

## cat_eye_night_items · object / illustration sheet (reel of 2026-11-08)

**Attach:** `factory/library/STYLE_REF.png`

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw NEW objects and illustrations: things for a reel about how cats see at night, simple and friendly.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows ONE separate item, at a similar visual size, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no characters, no hands.
Cells, left to right, top to bottom: 1 close-up of a grey cat's eye in normal light, green iris and a narrow vertical slit pupil; 2 close-up of the same cat's eye in the dark, pupil wide and round, iris with a bright yellow-green eyeshine glow; 3 a labelled-free cutaway diagram of a cat's eye showing the lens, the retina and a shiny layer behind it, light rays drawn as thin lines bouncing back (no text); 4 close-up of a human eye in normal light with a round pupil, for comparison; 5 a night bedroom window with curtains and a crescent moon outside; 6 a lit candle in a small holder; 7 a flashlight shining a cone of light to the right; 8 a full moon with soft craters; 9 a pair of glowing eyes only (two bright yellow-green eyes with slit pupils), as if seen in the dark.
```
Pose names: `eye_normal eye_dark eye_cutaway eye_human window_night candle flashlight moon eyes_glow`
Add with: `python3 library.py add <sheet.png> cat_eye_night_items eye_normal,eye_dark,eye_cutaway,eye_human,window_night,candle,flashlight,moon,eyes_glow --tags illustration,object,nature,night,cat --source gemini`
