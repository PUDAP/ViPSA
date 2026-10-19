# Paired camera-1 probe-motion verification after a Z jog

Use when the user asks whether the probe tip moved between two microscope captures, especially before/after a stage-Z jog.

## Why raw subtraction is insufficient

Camera compression, focus, illumination, and slight sample translation produce differences even if the probe does not move. Register the **substrate** first, then measure the probe relative to that registered substrate. Keep visual motion distinct from electrical contact.

## Workflow

1. Use the exact two requested frames and verify matching dimensions and nonidentical hashes.
2. Register the after-frame to the before-frame from substrate-only features:
   - mask out the probe-dominated ROI;
   - use SIFT/ORB feature matching;
   - estimate a bounded affine/partial-affine transform with RANSAC;
   - record good-match and inlier counts.
3. Identify the physical probe taper/tip separately in each image. For the usual brown/orange probe, HSV segmentation can seed the connected component entering from the left edge, but visually verify the marker is on the terminal taper—not a pad edge, shadow, or dark contact mark.
4. Report both:
   - raw image-coordinate displacement;
   - displacement after substrate registration (the meaningful probe-versus-device value).
5. Generate user-inspectable artifacts:
   - before/after/registered tip crop panel;
   - substrate-registered color overlay with distinct tip markers;
   - registered absolute-difference heat map;
   - two-frame blink GIF.
6. Attach the comparison panel and blink/overlay in chat. State uncertainty from blur, focus, illumination, and JPEG artifacts. Do not convert pixels to physical distance without a current calibrated scale.

## Interpretation

- A small displacement near the blurred tip-width or segmentation uncertainty is suggestive, not definitive.
- Agreement between the registered overlay, blink GIF, and tip estimates is stronger than one thresholded coordinate.
- Z-stage motion can shift the sample image or focus while the probe remains mechanically fixed; describe what moved **relative to the substrate**, not simply what changed in raw pixels.
- Visual overlap or visible tip motion does not establish electrical contact; use the low-bias electrical gate separately.

## Known-good output shape

Report concise signed `dx`, `dy`, and Euclidean pixel displacement, then attach the visual artifacts. Preserve before/after Z readbacks in the run metadata so the image comparison remains traceable to the actual jog.