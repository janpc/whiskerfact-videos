# Character sheets (Gemini app, or ElevenLabs `creative_generate_image`)

Each character has TWO sheets of 3 × 3 poses: 1 = movement, 2 = acting.
Attach `STYLE_REF.png` (the Mr. Whiskerfact sheet) as the style reference. For sheet 2, also attach that character's sheet 1, so it stays the same character.

## Base prompt (fill in CHARACTER and the 9 cells)
```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: CHARACTER.
Make ONE image: a grid of 3 columns × 3 rows of equal square cells. Each cell shows the SAME character (same proportions, colours and clothes), full body, at the same scale in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no ground, no shadows, no other objects. Side views always face RIGHT.
Cells, left to right, top to bottom: 1 ... 2 ... 3 ... 4 ... 5 ... 6 ... 7 ... 8 ... 9 ...
```

## Person, sheet 1 (movement): pose names
walk1, walk2, walk3, walk4, side, front, three_quarter, sit, jump
Cells: 1-4 "walking cycle side view: 1 contact (legs apart, right foot forward), 2 down (knees bent), 3 passing (legs together), 4 up (on toes)"; 5 "standing still, side view"; 6 "standing still, front view, arms relaxed"; 7 "three-quarter view"; 8 "sitting on the ground"; 9 "jumping with joy".

## Person, sheet 2 (acting): pose names
talk, point, think, happy, scared, surprised, wave, cold, shrug
Cells (all front view): 1 "talking, mouth open, one hand gesturing"; 2 "pointing up, explaining"; 3 "thinking, hand on chin"; 4 "very happy, big smile"; 5 "scared, hands up"; 6 "surprised, mouth open"; 7 "waving hello"; 8 "shivering with cold, arms crossed"; 9 "shrugging".

## Animal (four legs), sheet 1 (movement): pose names
run1, run2, run3, run4, walk1, walk2, side, front, sit
Cells: 1-4 "running cycle side view (gallop: 1 legs stretched, 2 legs gathered under body, 3 front legs reaching, 4 back legs pushing)"; 5-6 "walking side view, two steps"; 7 "standing still side view"; 8 "front view"; 9 "sitting or lying down".

## Animal, sheet 2 (acting): pose names
happy, scared, curious, eat, sleep, call, look_back, jump, alert
Cells: 1 "happy"; 2 "scared, fur/feathers puffed"; 3 "curious, head tilted"; 4 "eating"; 5 "sleeping curled up"; 6 "making its sound, mouth open"; 7 "looking back over its shoulder"; 8 "jumping"; 9 "alert, ears up".
(Birds, fish and other non-walking animals: replace the cycle with their own one, e.g. fly1-fly4 wings up/mid/down/mid, swim1-swim4 tail positions.)

## After generating
`python3 library.py add sheet.png <name> <9 pose names, '-' for a bad cell> --tags person|animal,<more> --source gemini|elevenlabs`
