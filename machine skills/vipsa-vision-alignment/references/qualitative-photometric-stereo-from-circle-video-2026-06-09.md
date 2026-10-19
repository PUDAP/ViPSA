# Qualitative photometric stereo from `circle` light video (2026-06-09)

Use this note when the user asks to estimate qualitative depth/relief from a ViPSA camera-1 video captured while the light controller runs `circle`.

## Context

`circle` drives a sequential illumination wave around the optical path and repeats it 3 times. A camera-1 video of this sequence can be treated as a rough multi-light photometric-stereo dataset, even before calibrated LED geometry is available.

This is **qualitative only** unless LED/objective geometry, LED intensities, flat-field baseline, and camera calibration are known.

## Practical workflow

1. Use the captured camera-1 `circle` MP4. Prefer the exact capture workflow from `vipsa-machine-operations/references/camera1-circle-video-capture-2026-06-09.md`.
2. Read frames with OpenCV.
3. Detect the active illumination window from frame mean brightness rather than blindly using the whole video. In the session example, the video had ~6.1 s total duration, but the useful active lighting was only ~0.13–2.33 s.
4. Sample frames across the active window. For `circle`, model the phase as 3 rotations over the selected frames unless a better frame-to-LED mapping is available.
5. Fit a simple sinusoidal lighting model per pixel:
   - `I(t) = a + bx*cos(theta(t)) + by*sin(theta(t))`
   - `theta(t)` spans `0..2π*3` over the active frames.
6. Estimate qualitative gradients from `bx/a` and `by/a`, suppress low-albedo/noisy pixels, smooth, then integrate with Frankot-Chellappa.
7. Produce at least:
   - sampled active-frame montage
   - depth colormap
   - depth overlay on mean frame
   - if requested, a 3D rendered surface plot of the relative-depth array
   - if requested or if global tilt/illumination dominates, a plane-subtracted 3D surface plot that emphasizes local relief
   - `.npy` files for both the raw relative-depth surface and any plane-subtracted surface
8. Report caveats clearly: sign and magnitude are not reliable without calibration; local pad/edge relief can still be useful.

## 3D plotting add-on

When the user asks “Plot this in 3D” after a qualitative `circle` photometric-stereo run:

1. Reuse the existing relative-depth surface if it was saved; otherwise recompute from the same active video window and save it.
2. Downsample the surface for rendering (for example every 3–8 pixels depending on image size) so matplotlib 3D plotting remains responsive.
3. Render a main 3D surface with a perceptual colormap and labeled axes (`x pixel`, `y pixel`, `relative relief`).
4. Fit and subtract a best-fit plane from valid pixels to create a local-relief surface; render a second 3D plot from that plane-subtracted surface.
5. Save both PNGs and both `.npy` arrays in the same output directory; attach the PNGs and list the numeric array paths.

## Interpretation learned

The resulting heatmap can visibly show contact-pad bumps/raised local relief when contact pads are actually in the field of view. In a later capture, the user clarified that the image was at the edge of the glass slide/substrate where there were no contact pads; in that case, the proxy should be interpreted as mostly probe geometry, slide-edge/substrate boundary relief, and broad illumination gradients rather than missing/failed pad detection.

## Required caveats

- This is not metric depth.
- LED distances/directions relative to the objective/sample plane are required for quantitative estimation.
- Per-LED intensity normalization and flat-field subtraction with a super-flat reference surface are needed before trusting relative height magnitudes.
- Specular highlights, shadows, and dark pad reflectance differences can dominate the estimate.
- The heatmap should be described as qualitative surface relief, not a calibrated 3D profile.

## Baseline needed for future quantitative work

Ask for or measure:

- LED/segment positions relative to objective and sample plane
- objective working distance / camera pixel scale
- per-LED brightness normalization
- flat reference video using the same `circle` sequence
- frame-to-LED/segment timing map
