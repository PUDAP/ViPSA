# Reusable editable multipass alignment executable (2026-07-24)

## Canonical artifact

`/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/align.py`

Live execution:

```bash
/home/amdm/.venvs/align-cv2/bin/python \
  /home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/align.py --execute
```

Safety and reuse properties:

- Without `--execute`, prints a dry-run plan and performs no hardware action.
- `--self-test` generates a synthetic dark pad and verifies the detector with no hardware.
- `--input-image PATH` runs detection/annotation only.
- Editable constants define camera/NATS endpoints, 900 px ROI, `21.5` steps/pixel, 5 px tolerance, pass limit, contour gates, settling time, and final light state.
- Physical light and Zaber commands run through validated PUDA protocols.
- Preflights Zaber state, captures a fresh image per pass, detects the nearest valid dark pad, makes bounded X/Y corrections, and captures an independent final verification image.
- Saves source/annotated images, masks, detections, protocol logs, move responses, final states, and `summary.json` under `runs/align_<UTC>/`.
- Reports final Zaber readback and attaches the final annotated image.

## Verified live behavior

A live two-pass run started with nearest-pad offset `(+109.92, -64.40) px` (`127.40 px` distance):

1. Pass 1 moved Zaber `X +2363`, `Y -1385`; readback `X 251860`, `Y 501134`.
2. Pass 2 observed `(-19.25, +2.76) px`, then moved `X -414`, `Y +59`; readback `X 251446`, `Y 501193`.
3. The independent final image measured residual `(+2.41, +1.99) px`, distance `3.12 px`, inside the 5 px tolerance.
4. Zaber, stage, and light controllers were idle with cleared run IDs; lights were left on as configured.

This validates direct signed mapping from pad-center image offset `(px-cx, py-cy)` to native Zaber correction at the calibrated multiplier for this setup. Always retain the fresh-image final verification; command success/readback alone is not optical alignment proof.

## Reporting rule

For terse `align`, execute the canonical script, then report only correction moves, final readback, final pixel residual/tolerance result, controller cleanup, final light state, and the final annotated image. Use 🎯 and avoid dumping contour candidates unless requested.
