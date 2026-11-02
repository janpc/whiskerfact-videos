# Gemini prompts for the week of 2026-11-02

Missing characters: **cat** (reel of 2026-11-08, "Myth or fact: cats can see in total darkness").
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
