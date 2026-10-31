# Character sheet prompt (Gemini app or ElevenLabs `creative_generate_image`)

Attach `STYLE_REF.png` (the Mr. Whiskerfact sheet) as the style reference. Fill in CHARACTER and the four POSES.

```
Using exactly the same illustration style as the attached cat character sheet (flat 2D cartoon, clean dark brown outlines of the same thickness, flat colours with one soft shade, friendly rounded shapes, cute but not childish), draw a NEW character: CHARACTER.
Make ONE image: a grid of 2 columns x 2 rows of equal square cells. Each cell shows the SAME character, full body, centred, the same size in every cell, fully inside its cell with a margin, on a perfectly flat pure green background (#00FF00). No labels, no text, no borders, no shadows on the ground, no other objects.
Cell 1: POSE1. Cell 2: POSE2. Cell 3: POSE3. Cell 4: POSE4.
```

Then: `python3 library.py add sheet.png <name> <pose1,pose2,pose3,pose4> --tags ... --source gemini|elevenlabs`
Pose names are short slugs (front, side, walk, point, think, scared, happy, ...). Side views face RIGHT (flip in code for left).
