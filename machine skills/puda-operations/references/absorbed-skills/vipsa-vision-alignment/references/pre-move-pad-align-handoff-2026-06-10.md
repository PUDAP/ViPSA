# Pre-move + camera pad alignment handoff to approach (2026-06-10)

## Context

A chained workflow requested:

- stage Z down by 35 steps
- Zaber Y by -5000 native steps
- camera-1 contact-pad alignment
- send aligned picture
- then electrical approach and gated measurements

## Observed successful alignment details

After requested pre-moves, camera-1 dark-pad detector on the 900x900 center ROI found the nearest pad:

- initial pad offset from ROI center: ~12.7 px
- correction multiplier: 25 native Zaber steps/px
- commanded correction:
  - Zaber X: `+103` native steps
  - Zaber Y: `-300` native steps
- final residual pad offset: ~4.63 px

This is close enough to hand off to approach unless the user asks for tighter tolerance.

## Useful pattern for chained requests

When the user includes both pre-moves and later electrical steps:

1. Execute only the user-specified pre-moves first.
2. Capture camera 1 with light on/off cleanup.
3. Run the standard 900x900 ROI dark-pad detector.
4. Apply one Zaber correction with multiplier 25 unless user changes it.
5. Recapture and attach the verified aligned image.
6. If residual is a few pixels, proceed to the next requested gate (approach/short-check). Do not over-iterate alignment by default.

## Reporting

Keep the alignment section concise:

```text
🎯 Alignment:
- Initial pad offset: 12.7 px
- Applied Zaber correction: X +103, Y -300 native steps
- Final pad offset: 4.63 px → aligned
MEDIA:/path/to/after_annotated.jpg
```

## Pitfall

Do not treat the later electrical chain as permission to skip image attachment. The user explicitly asked to send a picture after movement/alignment, so attach the post-correction annotated image before or alongside the electrical outcome.
