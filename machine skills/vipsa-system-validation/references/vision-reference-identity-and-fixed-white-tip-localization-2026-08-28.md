# Vision-reference identity and fixed-white tip localization (2026-08-28)

## Claim correction

A 10-trial camera-guided test used a selected pad centre `(789.899, 537.592)` px as a fixed image target. Later explicit tip localization identified the sharp visible apex near `(687, 527)` px. Because these coordinates differed by about 103 px in X, the first result validates **return-to-image-coordinate repeatability**, not pad-to-tip alignment accuracy.

The user confirmed that the sharp rightmost visible apex is the physical probe-contact reference.

## Durable validation rules

1. Detect and overlay the actual visible apex before defining a pad-to-tip target.
2. Never substitute image centre, nearest-pad centre, probe-body centre, or a verbal “on top of” relationship for the visible apex.
3. If the intended contact point is ambiguous, obtain user confirmation on an overlay before motion.
4. Numerically compare apex and pad-target coordinates before naming a test “alignment.”
5. A pad returned to a fixed pad coordinate is a return-to-coordinate repeatability result unless that coordinate is verified to equal the physical contact reference.
6. Confirm probe retraction/clearance before any lateral OpenFlexure or Zaber movement.

## Verified fixed-configuration detector

Under Camera 1 at 1920×1080 and normal all-white maximum illumination:

- 30 frames at 1 frame/s, with camera, focus, probe, sample, and illumination fixed.
- Manual apex: `(687, 527)` px with estimated ±2 px uncertainty.
- ROI: `x=0:730`, `y=450:620`; grayscale threshold `<115`.
- Select the foreground component touching the left boundary with area >1000 px.
- Apex X is the rightmost component column; apex Y is the median over the rightmost three columns.
- Detection 30/30; mean `(687.00, 528.05)` px.
- Y repeatability SD 0.201 px (0.367 µm with installed Camera 1 Y scale).
- Difference from the single manual annotation: 1.05 px (1.92 µm), within its stated uncertainty.

This is configuration-specific. Revalidate after probe translation, ROI/focus changes, different pad fields, and illumination changes. Absolute accuracy needs multiple independent manual annotations.

## Lighting topology and firmware limit

ViPSA has one individually addressable RGBA LED strip coiled inside a 3D-printed conduit, not separate left/right lights. Current firmware exposes only:

- `on`: all white, maximum intensity
- `off`
- `red`
- `green`
- `rainbow`

Do not invent intensity sweeps, left/right lights, spatial patterns, or per-LED test conditions until live firmware capabilities expose them. Defer expanded controlled-illumination validation until those controls exist.
