---
name: vipsa-vision-alignment
description: Build and run ViPSA camera-based alignment procedures, especially contact-pad/probe-tip alignment from camera 1 images using OpenCV preprocessing, ROI cropping, thresholding, and contour detection.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, camera, opencv, alignment, contours, roi]
    related_skills: [vipsa-image-capture, vipsa-machine-operations, puda-operations, puda-env]
---

# ViPSA Vision Alignment

## Session references

- `references/align-then-leave-lights-on-2026-06-12.md` — alignment variant where the user explicitly wants lights left on; final cleanup should call `light.turn_on()` and verify idle states.
- `references/terse-lights-on-align-leave-on-2026-06-19.md` — terse “turn lights on and align” means run standard pad alignment and leave lights on; patch both normal and `finally` cleanup paths to final `turn_on()`.


## Overview

Use this skill when the user asks to implement, modify, or run a ViPSA `align` procedure involving camera images, contact pads, probe tips, ROI extraction, thresholding, or contour detection.

This skill complements `vipsa-image-capture`: use that skill for the physical camera/light acquisition step, then use this skill for image-processing stages.

## Required companion skills

Load and follow these before physical acquisition or PUDA side effects:

- `vipsa-image-capture`
- `vipsa-machine-operations`
- `puda-operations`
- `puda-env`

## Environment setup

Use OpenCV (`cv2`) for image processing when the user asks for OpenCV logic. Because the WSL Python environment is PEP 668 managed, install into a venv instead of system Python:

```bash
python3 -m venv /home/vipsa/.venvs/align-cv2
/home/vipsa/.venvs/align-cv2/bin/python -m pip install --upgrade pip
/home/vipsa/.venvs/align-cv2/bin/python -m pip install opencv-python-headless
```

Do not permanently encode missing-package failures as limitations. If `cv2` is absent, install it in the venv and rerun.

## Standard align procedure shape

### Step 0 — capture camera 1

Capture a fresh camera 1 image through the lighted snapshot workflow:

1. Turn light on.
2. Capture one frame from camera 1.
3. Turn light off in a cleanup/finally path.
4. Verify light state is `idle`.
5. Save/display the captured image.

### Step 1 — crop ROI and optionally rotate

The latest user-preferred Step 1 output is:

- From the current camera 1 frame, crop a `900x900px` square ROI in the center of the image.
- Use OpenCV (`cv2`) rather than ffmpeg for this stage.
- Rotation center is reported as `(830, 460)`.
- Rotation is `0°` unless the user changes it.

Implementation pattern:

```python
import cv2

frame = cv2.imread(input_image, cv2.IMREAD_COLOR)
(h, w) = frame.shape[:2]

roi_size = 900
cx, cy = w // 2, h // 2
startX = max(0, cx - roi_size // 2)
endX = min(w, startX + roi_size)
startY = max(0, cy - roi_size // 2)
endY = min(h, startY + roi_size)

# Re-adjust if the image is smaller or a boundary clipped the ROI.
startX = max(0, endX - roi_size)
startY = max(0, endY - roi_size)

cropped_image = frame[startY:endY, startX:endX]
(ch, cw) = cropped_image.shape[:2]

center = (830, 460)
rotation_degrees = 0
rotation_matrix = cv2.getRotationMatrix2D(center, rotation_degrees, 1.0)
rotated_frame = cv2.warpAffine(cropped_image, rotation_matrix, (cw, ch))
```

For a `1920x1080` camera 1 frame, this gives ROI bounds `x=510..1410`, `y=90..990`, output size `900x900`.

### Step 2 — dark contact-pad mask on cropped ROI

The current contact pads appear as **black/dark squares on a lighter background**. For reliable pad detection, prefer a dark-response mask over raw Otsu thresholding. Use the Step 1 `900x900` ROI as BGR input:

```python
import cv2
import numpy as np

def get_dark_pad_mask(roi_bgr) -> np.ndarray:
    gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)

    # Estimate slow-varying illumination/background.
    background = cv2.GaussianBlur(gray, (0, 0), 45)

    # Dark pads become bright in this response image.
    dark_response = cv2.subtract(background, gray)
    dark_response = cv2.normalize(
        dark_response, None, 0, 255, cv2.NORM_MINMAX
    ).astype(np.uint8)

    _, mask = cv2.threshold(
        dark_response, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
    return mask
```

If the user explicitly asks to reproduce their older Otsu step, preserve that code path, but note that the dark-response mask is better for black pads under uneven illumination.

### Step 3 — contact-pad contours ranked by center distance

Find contours from the Step 2 dark-pad mask and rank pad candidates by Euclidean distance from the Step 1 ROI center. For the standard `900x900` ROI, the center is `(450, 450)`.

Core pipeline:

1. `cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
2. Filter by square-ish dark-pad properties:
   - area roughly `1000..15000`
   - aspect ratio roughly `0.55..1.45`
   - extent at least `0.35`
   - nonzero contour moment
3. Compute centroid from moments.
4. Compute `distance = hypot(cX - roi_center_x, cY - roi_center_y)`.
5. Sort ascending; the nearest pad is the Step 4 target.

Use the full `900x900` ROI for pad detection rather than a tight `340x280` center crop; the smaller crop can miss most pads or the nearest usable pad.

### Step 4 — move Zaber to center nearest pad

Given ROI center `(cx, cy)`, nearest pad centroid `(px, py)`, and multiplier `M` steps/pixel:

```python
shift_x_px = cx - px  # positive means image/pad should shift right
shift_y_px = cy - py  # positive means image/pad should shift down

# User convention:
# - to shift image/pad right, move Zaber X by negative steps
# - to shift image/pad up, move Zaber Y by positive steps
zaber_x_steps = round(-shift_x_px * M)
zaber_y_steps = round(-shift_y_px * M)
```

Use `move_x_by(distance=zaber_x_steps, units=None)` and `move_y_by(distance=zaber_y_steps, units=None)` for native-step moves unless the user explicitly asks for millimetres. The user revised the alignment multiplier from `30` to `25`; use the latest requested multiplier in the active procedure.

After moving, read back Zaber position, capture a fresh camera 1 image, rerun the same pad-detection pipeline on the fresh image, and report the residual offset in pixels. If the residual is already only a few pixels and the user has not requested another correction pass, stop there and proceed to the next requested gate (for example approach-parameter confirmation) rather than over-iterating. If the residual remains significant (>~10 px), run a bounded second correction using the observed before→after pixel response from the first move rather than blindly repeating the nominal multiplier; see `references/residual-verified-multipass-pad-alignment-2026-06-23.md`.

See `references/align-dark-pad-centering.md` for the full session-derived implementation notes, robust detection snippet, and example values. See `references/session-2026-06-05-preapproach-pad-align.md` for a concrete pre-approach sequence with coarse Z/Zaber movement, alignment move, recapture, final residual computation, and handoff to approach parameters. See `references/pre-move-pad-align-handoff-2026-06-10.md` for a chained pre-move + pad-alignment handoff where a ~4.6 px residual was treated as aligned before approach, while still attaching the post-correction image.

## Chained pre-approach alignment workflow

When the user requests a combined sequence such as “move Z down, move Zaber X, align the contact pad, then ask for approach parameters,” execute the physical pre-moves first, then run the standard camera-1 contact-pad alignment, then stop for approach parameters. Do not merge the later approach/DCIV steps into the alignment report unless the user has already supplied those parameters.

Recommended sequence:

1. Preflight `stage`, `zaber`, and `light` state.
2. Apply the requested Z-only `stage.move_z_by(height=<signed steps>)` and Zaber native move(s) (`units: null`). Preserve the user’s sign convention; do not substitute a remembered or prior-session step count.
3. Capture camera 1 with the lighted snapshot workflow.
4. Run the 900×900 center ROI dark-pad detector and compute the native Zaber correction using the current multiplier (usually `25` steps/px unless the user changes it).
5. Apply both Zaber X and Y corrections with `units: null`.
6. Recapture camera 1 and rerun the detector as verification. Report the final pixel offset from center, final Zaber readback, and final image attachment. If the final offset is only a few pixels, treat it as aligned unless the user requested tighter tolerance.
7. Ask for the next-step parameters (for example approach parameters) only after alignment verification is complete.

## Probe-tip separation / annotation from a photo

Use this subsection when the user asks to “separate,” identify, or mark the probe tip in a microscope/camera image rather than run a full motion alignment.

1. Treat the dark square contact pad and the tapered probe as distinct objects: the contact pad is a roughly square dark feature; the probe tip is usually a brown/metal tapered feature entering from an image edge and terminating near the pad.
2. If the image is already available in context, use vision to estimate the tip first, then create a marked-up image with OpenCV/Pillow so the user gets a visual artifact, not just coordinates.
3. Run OpenCV scripts with `/home/vipsa/.venvs/align-cv2/bin/python` when available; the default Hermes Python may not have `cv2`. If the venv is missing, create/install it using the Environment setup commands above rather than treating missing `cv2` as a blocker.
4. Report concise full-image pixel coordinates `(x, y)` for the estimated tip and attach the annotated output via `MEDIA:/absolute/path`.
5. Prefer a visible overlay convention: orange/yellow line or contour for the probe taper/body; red dot/circle for the estimated probe tip; optional label text. Avoid confusing the overlay with the dark pad itself.

See `references/probe-tip-separation.md` for a compact example workflow and annotation conventions.

## Qualitative photometric stereo from `circle` light videos

Use this subsection when the user asks to estimate depth/relief from a camera-1 video captured while the light controller runs `circle`.

1. Treat `circle` as a rough rotating multi-light sequence: it sends 3 illumination waves around the optical path.
2. Read the video with OpenCV and detect the active illumination window from frame mean brightness. Do not automatically use the full MP4 if it includes dark pre/post-roll.
3. Sample frames in the active window and fit a simple per-pixel sinusoidal lighting model such as `I(t)=a+bx*cos(theta)+by*sin(theta)`, with `theta` spanning 3 rotations unless a better frame-to-LED timing map is available.
4. Estimate qualitative gradients from normalized lighting coefficients (`bx/a`, `by/a`), suppress low-albedo/noisy pixels, smooth, and integrate with Frankot-Chellappa for a relative relief surface.
5. Generate a sampled-frame montage, depth colormap, overlay on the mean frame, and—when the user asks to “plot this in 3D”—a rendered 3D surface view plus a plane-subtracted/local-relief 3D view.
6. Save the numeric relative-depth arrays (`.npy`) alongside the PNGs so later analysis can reuse the surface instead of recomputing from video.
7. Interpret as qualitative surface relief only. The contact-pad bumps can be visibly detected when the FOV contains pads; if the FOV is over the glass/substrate edge with no pads, report that the proxy mostly reflects slide edge/probe/illumination-gradient structure rather than pad bumps. Sign/magnitude are not trustworthy without calibration.

For details, caveats, 3D plotting notes, and the baseline needed for quantitative work, see `references/qualitative-photometric-stereo-from-circle-video-2026-06-09.md`.

## Reporting style

The user often supplies procedure modifications and expects direct execution plus concise verification. Use the 🎯 emoji to mark align/alignment reports. After each step, report:

- what input image/ROI was used
- key dimensions/bounds/parameters
- whether the operation succeeded
- generated image attachments via `MEDIA:/absolute/path`
- important caveats only when they affect correctness (for example, Step 3 intentionally does not use Step 2 Otsu output)

For qualitative photometric stereo reports, explicitly say that the heatmap is relative surface relief, not calibrated metric depth, and mention whether contact-pad bumps/local relief are visible.

Avoid long explanations unless the user asks for rationale.

## Vision-guided contact approach

A hybrid electrical + camera-1 deflection contact approach is implemented at:

```bash
/home/vipsa/vipsa-puda-project/tools/vision_guided_approach.py
```

It uses OpenCV template matching to track the probe-tip ROI and a nearby fixed sample/background ROI, subtracts global drift, and uses relative tip deflection as a soft/hard contact signal alongside Keithley current. The script is no-motion by default (`calibrate`/`monitor`); actual Z motion requires `execute --execute`. Use an explicitly configured output directory or the current patched script, because an older version could complete execution but fail while writing `summary.json` when `args.outdir` was a `PosixPath`. See `references/vision-guided-contact-approach-2026-06-09.md` for current ROI defaults, thresholds, commands, and verified no-motion tracking output.

## References

- `references/vision-guided-contact-approach-2026-06-09.md` — implemented hybrid electrical + visual deflection approach script, safety gate, ROI defaults, and no-motion calibration output.
- `references/align-session-2026-06-05.md` — concrete procedure evolution and observed parameters from the session where Step 1/2/3 were defined.
