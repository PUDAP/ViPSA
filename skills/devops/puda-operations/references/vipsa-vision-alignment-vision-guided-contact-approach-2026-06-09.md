# Vision-guided contact approach implementation (2026-06-09)

Use when adding or running the ViPSA hybrid contact approach that combines Keithley current feedback with camera-1 probe-tip deflection tracking.

## Implemented artifact

Script:

```bash
/home/vipsa/vipsa-puda-project/tools/vision_guided_approach.py
```

Run with the OpenCV venv:

```bash
/home/vipsa/.venvs/align-cv2/bin/python tools/vision_guided_approach.py <mode> [options]
```

Default config:

```bash
/home/vipsa/vipsa-puda-project/config/vision_guided_approach_camera1.json
```

## Safety gate

The script is no-motion unless explicitly run as:

```bash
/home/vipsa/.venvs/align-cv2/bin/python tools/vision_guided_approach.py execute --execute
```

Modes `calibrate` and `monitor` only operate lights/camera and do not move Z or bias the DUT.

## Current ROI defaults

From camera-1 frame with probe tip near `(704, 538)` full-frame pixels:

```json
{
  "tip_roi": [585, 495, 145, 90],
  "background_roi": [745, 480, 125, 115],
  "search_radius_px": 45,
  "soft_threshold_px": 1.0,
  "hard_threshold_px": 3.0,
  "min_template_score": 0.45
}
```

- Red tip ROI covers the probe apex/body near the tip.
- Yellow background ROI is on a nearby fixed contact pad/sample texture, not on the probe, and is used to subtract global camera/sample drift.

## Algorithm

For each approach iteration:

1. Measure current with Keithley at low voltage.
2. Capture camera 1 frame with light on.
3. Template-match the probe-tip ROI and fixed background ROI against the baseline.
4. Compute relative deflection:

```text
relative tip motion = tip template displacement - background template displacement
```

5. Decision priority:

```text
if abs(current) > upper_current_threshold:
    retract by high_current_retract_z
    switch to fine mode
elif lower_current_threshold <= abs(current) <= upper_current_threshold:
    accept contact
elif visual_deflection >= hard_threshold_px:
    retract by visual_hard_retract_z and stop
elif visual_deflection >= soft_threshold_px:
    switch to fine mode
else:
    continue approach
```

6. Motion step is `coarse_step_size` until fine mode, then `fine_step_size`.

Defaults:

```text
test_voltage = 0.01 V
lower_current_threshold = 1e-8 A
upper_current_threshold = 1e-7 A
coarse_step_size = +1.0 Z
fine_step_size = +0.1 Z
settle_delay = 0.2 s
max_attempts = 50
high_current_retract_z = 0.5
visual_hard_retract_z = 0.5
```

## Verified no-motion calibration

Command run successfully:

```bash
/home/vipsa/.venvs/align-cv2/bin/python tools/vision_guided_approach.py calibrate --monitor-frames 2 --monitor-interval 0.5
```

Output showed stable tracking over two no-motion frames:

```text
tip_score ~= 0.998
background_score ~= 0.995
relative_deflection_px = 0.0
visual_state = none
light final state = idle
```

Annotated ROI image was saved under `/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_vision_guided_approach_*/vision_monitor_annotated.jpg`.

## Running recommendations

Before first live execution, run `calibrate` or `monitor` and inspect the annotated ROI image. If the probe/camera field has shifted, update ROI options:

```bash
--tip-roi x,y,w,h --background-roi x,y,w,h
```

Start conservative:

```bash
/home/vipsa/.venvs/align-cv2/bin/python tools/vision_guided_approach.py execute --execute \
  --coarse-step-size 0.5 --fine-step-size 0.05 \
  --soft-threshold-px 1.0 --hard-threshold-px 3.0
```

Do not run X/Y motion while landed. If visual hard deflection fires, it retracts and stops rather than continuing to search electrically.
