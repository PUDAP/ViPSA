# Integrated ViPSA motion calibration

Use this reference for installed Zaber/OpenFlexure X--Y calibration with Camera 1 and a physical ruler.

## Validated pattern

1. Retract the probe and keep the non-tested stage fixed.
2. Place a traceable scale in the sample plane. A 1 cm scale divided into 100 parts has 100 um divisions.
3. Calibrate Camera 1 independently in X and Y by rotating the scale 90 degrees. Fit pixel coordinate versus division index; report um/pixel and fit residual. Do not assume square pixels.
4. Save `before`, `after`, and `return` images for every excursion. Use full-frame phase correlation and the matching axis scale.
5. Test both directions separately. Always attempt exact inverse rollback in `finally` when net commanded motion is nonzero.
6. Split long experiments into bounded per-distance runners that append CSV rows, so completed batches survive command/NATS delays.
7. Verify final PUDA state (`idle`, `run_id: null`) and optical return. OpenFlexure `[0,0,0]` after `set_zero` is a tracked reference, not an absolute physical origin.

## Observed installed-system behavior (2026-08-26)

At the ruler calibration focus and 1920x1080 stream:

- Camera X 1.8223 um/px; Camera Y 1.8246 um/px.
- Zaber X 0.099155 um/native unit; mean/max return error 1.04/2.07 um.
- Zaber Y 0.099427 um/native unit; mean/max return error 11.11/13.79 um.
- OpenFlexure X, same-direction preloaded: +1.837 and -1.498 um/step; approximately five steps of reversal deadband.
- OpenFlexure Y, correctly directed commands >=5 steps: +1.445 and -1.563 um/step.
- Two-step OpenFlexure moves were not reliable open-loop displacement. One negative-Y command produced a wrong-sign response; reject sign-inconsistent image motion and recover optically.

Values depend on focus, resolution, optics, scale plane, load, gearing, and mounting. Recalibrate after any of those change. Do not overwrite a pad-alignment steps/pixel calibration obtained at another focus with ruler-derived values.

## Interpretation and reporting

- Zaber sub-1% scale error supports coarse-to-fine operation, not blind pad landing.
- Report OpenFlexure direction and preload history; one bidirectional value hides gearbox behavior.
- Do not label apparent orthogonal image motion as cross-axis coupling until ruler/camera rotation is removed.
- Keep wrong-sign events visible because they justify deterministic sign checks.
- Main manuscript: camera scale/FOV and stage summary tables in Hardware; full method/results/plots in Validation; tolerance interpretation in Discussion; backlash/anomalies in Limitations.
- Supplement/repository: raw CSV, images, logs, scripts, reports, and videos.

For dual-camera evidence, record RTSP H.264 to recoverable MKV files with stream copy, remux to MP4 afterward, and optionally generate a compressed side-by-side accelerated summary for chat delivery.
