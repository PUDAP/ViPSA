# Align procedure: dark contact-pad detection and Zaber centering

Session-derived workflow for ViPSA contact-pad/probe-tip alignment from camera 1 images.

## Current align pipeline

1. **Capture camera 1 with light on**, then turn light off in cleanup.
2. **Step 1 ROI**: crop a `900x900` square from the image center with OpenCV. For `1920x1080`, bounds are `x=510..1410`, `y=90..990`. Rotation is currently `0°`. The user asked to report rotation center `(830, 460)` even though `0°` is identity.
3. **Step 2 improved pad mask**: contact pads are black/dark squares, so do not threshold as bright objects. Use local background normalization:
   - grayscale
   - large Gaussian blur background estimate, e.g. `sigma=45`
   - `dark_response = background - gray`
   - normalize to `0..255`
   - Otsu threshold on dark response
   - morphology close `(11,11)` then open `(5,5)`
4. **Step 3 contours**: find contours from the dark-pad mask, filter as square-ish pads, then rank by Euclidean distance from the `900x900` ROI center `(450,450)`.
5. **Step 4 centering move**: choose nearest ranked pad; compute the pixel shift needed to bring it to ROI center, then move Zaber using the user-specified multiplier.

## Robust dark-pad contour detection snippet

```python
import cv2
import numpy as np
import math

def detect_dark_pads(roi_bgr):
    gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    roi_center = (w / 2.0, h / 2.0)

    background = cv2.GaussianBlur(gray, (0, 0), 45)
    dark_response = cv2.subtract(background, gray)
    dark_response = cv2.normalize(dark_response, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    _, mask = cv2.threshold(dark_response, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pads = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 1000 or area > 15000:
            continue
        x, y, bw, bh = cv2.boundingRect(cnt)
        aspect = bw / float(bh)
        if not (0.55 <= aspect <= 1.45):
            continue
        extent = area / (bw * bh) if bw * bh else 0
        if extent < 0.35:
            continue
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
        dist = math.hypot(cX - roi_center[0], cY - roi_center[1])
        pads.append({
            "contour": cnt,
            "bbox": (x, y, bw, bh),
            "centroid": (cX, cY),
            "area": area,
            "aspect": aspect,
            "extent": extent,
            "distance_from_center_px": dist,
        })
    return sorted(pads, key=lambda p: p["distance_from_center_px"]), mask
```

## Zaber centering formula

Given ROI center `(cx, cy)`, nearest pad centroid `(px, py)`, and multiplier `M` steps/pixel:

```python
shift_x_px = cx - px  # positive means image/pad must shift right
shift_y_px = cy - py  # positive means image/pad must shift down

# User convention:
# - to shift image/pad right, move Zaber X by negative steps
# - to shift image/pad up, move Zaber Y by positive steps
zaber_x_steps = round(-shift_x_px * M)
zaber_y_steps = round(-shift_y_px * M)
```

Use `units: None` for these native-step Zaber moves unless the user explicitly says millimetres.

## Observed example values

For the tested `900x900` ROI, nearest pad centroid was about `(327.27, 438.77)` and ROI center was `(450,450)`, giving offset `dx=-122.73 px`, `dy=-11.23 px`.

- With multiplier `30`: `move_x_by(-3682)`, `move_y_by(-337)`.
- User later changed multiplier to `25`: `move_x_by(-3068)`, `move_y_by(-281)`.

Always capture a fresh camera 1 image after the move and report Zaber readback plus light cleanup state.
