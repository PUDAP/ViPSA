# Integrated X/Y motion and one-hour drift calibration (2026-08)

Use this reference when converting Camera 1 displacement into physical motion, designing an alignment benchmark, or reporting installed-system stability.

## Camera 1 scale

A 1 cm scale divided into 100 intervals was imaged in the sample plane; each division was 100 µm.

- X orientation: 54.876 px/division; 1.8222873668 µm/px.
- Y orientation (same scale rotated 90°): 54.8066 px/division; 1.8245979869 µm/px.
- Camera 2 is a simple webcam and is unsuitable for absolute micrometre Z calibration. Defer metric Z claims until a suitable external reference is available.

## Installed Zaber results

- X: 0.0991554666 µm/native unit; scale error −0.845%; R² 0.9999979; mean/max return error 1.044/2.067 µm.
- Y: 0.0994265775 µm/native unit; scale error −0.573%; R² 0.9999353; mean/max reversal return error 11.106/13.791 µm.
- Coarse coordinates are nominal locations. The Y reversal offset is acceptable for retaining the target in the camera field but not for blind microscopic-pad landing.
- Compute axis conversion at runtime:
  `native_units_per_pixel = camera_axis_um_per_px / zaber_axis_um_per_native_unit`.
- Do not reuse the older global 21.5 native-units/px constant after this calibration.

## Installed OpenFlexure results

Direction, load, and motion history matter.

- Recalibrated Camera 1 X scale: 54.88009 px per 100 µm; 1.8221543 µm/px; 0.1490 px tick-fit RMS.
- Recalibrated X (10 repeats at 5, 10, and 20 steps per direction; 10-step same-direction preload): +X 1.52079 µm/step, R² 0.9681; −X 1.55891 µm/step, R² 0.9609.
- X directional asymmetry: 2.48%; all 60 full-run responses passed the optical sign/magnitude gate. Response per step remained command-size dependent.
- Nominal tracked X return-to-zero had mean/max optical error 8.23/13.79 µm; bounded cleanup reduced physical X residual to 0.875 µm and left tracked X at −9.
- A prior pad-to-tip operation observed severe X under-response/stall under different loading/history; the new 60/60 acceptance result does not erase that anomaly. Tracked X changes remain insufficient evidence of physical movement.
- Recalibrated Camera 1 Y scale: 54.81887 px per 100 µm; 1.8241895 µm/px; 0.0567 px tick-fit RMS.
- Recalibrated Y (10 repeats at 5, 10, and 20 steps per direction; 10-step same-direction preload): +Y 1.51328 µm/step, R² 0.9845; −Y 1.37266 µm/step, R² 0.8785.
- Y directional asymmetry: 9.75%; 59/60 full-run responses passed the optical sign/magnitude gate. One −10-step response moved in the wrong apparent direction. A separate preflight −5-step command stalled after reversal.
- Nominal tracked return-to-zero was physically poor: mean/max block optical return error 24.12/58.24 µm; final pre-correction Y drift 57.58 µm. Bounded optical cleanup reduced Y residual to 0.917 µm and left tracked position [0, −38, 0].
- Two-step commands are below a robust open-loop range; commands below approximately five steps require explicit optical verification.
- Use Zaber for large travel. Use OpenFlexure only for bounded fine corrections with direction-specific conversions, same-direction preload where practical, and a fresh image after every command.
- Reject wrong-sign, stalled, or magnitude-inconsistent motion; recover in a bounded way and never infer physical return from tracked coordinates alone.

## OpenFlexure Z-to-X/Y coupling (2026-08-31)

With Zaber and OpenFlexure X/Y fixed, five positive and five negative ladders visited commanded Z positions ±1, ±2, ±5, ±10, ±20, and ±50 steps. Camera 1 measured lateral displacement; this is not absolute Z metrology.

- Operator classification: repeats 1–2 are setup/conditioning transients and are excluded from the operational coupling metric. Preserve them in the raw record only: +50/−50 mean radial shift 3.213/3.514 µm; maximum 3.533 µm.
- Operational steady-state result, repeats 3–5: mean radial shift at +50/−50 steps 0.186/0.111 µm; maximum across all tested Z positions 0.235 µm; return mean/max 0.134/0.240 µm; focus ratio 0.975–1.009.
- Final tracked position was restored to [−10, −46, 0]. No X/Y or Zaber movement was commanded.
- Treat conditioned Z-to-X/Y coupling as negligible relative to the current 5 µm positioning tolerance; no fixed X/Y compensation is required from this dataset.
- This remains lateral Camera 1 metrology only, not absolute Z calibration. Continue normal optical verification during precision alignment.

## Combined Zaber-coarse/OpenFlexure-fine benchmark (2026-08-31)

A fixed text fiducial (`1 DIV=0.10mm`) was used after the user confirmed ±0.5 mm physical X/Y clearance. No Z motion was commanded. Gradient phase correlation plus ECC translation refinement registered ten deterministic randomized targets spanning ±500 µm in both image-plane axes.

Control policy:

- Zaber handled residual components above 18 µm, with each command capped at 5000 native units.
- OpenFlexure handled bounded final correction, capped at 12 steps per command.
- Every move was followed by a fresh Camera 1 frame and OpenFlexure sign/magnitude gate.
- Local Zaber pilot gains were 0.09685 µm/unit X and 0.08415 µm/unit Y. Treat the Y discrepancy from the earlier ruler calibration as setup-local and unresolved; optical feedback determined final placement.

Results:

- 10/10 trials passed the predefined ≤5 µm radial criterion.
- Final residual mean/median/P95/max: 1.517/1.416/3.112/3.360 µm.
- Median coarse/fine iterations: 1/1; two trials passed after coarse correction alone.
- Median/max elapsed time before return: 40.85/49.09 s.
- No OpenFlexure sign or magnitude gate failures.
- Raw anchor return mean/median/max: 8.56/10.87/12.55 µm; 7/10 returns required camera correction.
- Final anchor residual: 1.349 µm.
- Final OpenFlexure tracked position after optical anchor correction: [−10, −46, 0]; do not reset it merely to make readback zero.

Interpretation: this validates the hierarchy for one text fiducial, one location, one focus state, and white-maximum illumination. It does not validate blind open-loop positioning, holder-wide accuracy, pad-to-tip alignment, contact, or electrical integrity.

## One-hour stationary drift

Acquisition: 61 Camera 1 frames at one-minute intervals with stages, scale, focus, and illumination unchanged.

Initial full-frame phase correlation had weak response because most of the frame was low texture. Verified analysis used OpenCV ECC translation registration on ROI x=100:1550, y=250:1070 with 5×5 Gaussian blur.

- X net drift: −0.236 µm; peak-to-peak 0.917 µm; SD 0.240 µm.
- Y net drift: −0.033 µm; peak-to-peak 0.433 µm; SD 0.082 µm.
- ECC correlation: 0.898–0.920; median 0.914.
- Interpret as integrated camera-plus-optics-plus-mechanics stability, not isolated stage drift.
- This supports sub-micrometre stationary stability over one hour; multi-hour and holder-position-dependent drift remain outstanding.

## Quantitative alignment benchmark handoff

After motion calibration, use the actual visible probe tip rather than frame centre. Keep the probe retracted and electrical outputs off. Recommended minimum benchmark: centre plus four holder corners × two repeatable lighting conditions × five randomized initial offsets = 50 trials. Save manual and detected tip/pad coordinates, all corrections, fresh verification images, final residual, iterations, time, and failure reason. Define success using a safe inset region of the pad rather than an arbitrary fixed tolerance.