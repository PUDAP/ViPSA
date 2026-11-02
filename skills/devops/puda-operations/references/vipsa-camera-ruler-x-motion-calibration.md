# ViPSA camera-ruler X motion calibration

Reusable workflow for calibrating Zaber X and OpenFlexure X against a stage micrometer visible in Camera 1.

- Fit many ruler ticks to derive µm/pixel; do not use a single interval.
- Calibrate Zaber and OpenFlexure separately while holding the other stage fixed.
- Zaber: run repeated signed native-unit excursions, exact inverse returns, optical before/after/return captures, and fit measured displacement versus command through the origin.
- OpenFlexure: quantify reversal slack first; use same-direction preload and separate positive/negative µm-per-step fits. Restore the physical optical anchor before calling `set_zero`; tracked `[0,0,0]` is not physical proof.
- Use broad image registration with non-periodic ruler features to avoid tick aliasing. Do not interpret apparent image-Y shift as cross-axis coupling until ruler/camera rotation is removed.
- Record both RTSP cameras concurrently to MKV stream copies, remux full recordings after stopping, and create a compressed side-by-side accelerated summary. Verify duration and sampled frames.
- On a timeout, inspect the live run ID and edge response before replaying. COMPLETE the exact live run, determine whether motion occurred optically, apply only a known inverse/bounded correction through the driver, verify the anchor, then require `idle` and `run_id: null`.

Preserve raw images, command logs, CSVs, summary JSON, plots, full recordings, accelerated dual-camera video, and a markdown report in one run directory.
