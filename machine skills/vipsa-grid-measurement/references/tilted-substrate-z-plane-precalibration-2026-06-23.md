# Tilted-substrate Z-plane precalibration for faster ViPSA grid approach

Use this when prior grid contact-Z data shows a clear corner-to-corner gradient and the user wants to speed up approach without reducing electrical fidelity.

## Core idea

Model the substrate as a tilted plane in Zaber X/Y coordinates:

```text
Z_contact_est = a*X + b*Y + c
```

Use this only to shorten the *mechanical search*. Do not reduce the electrical protocol: keep DCIV resolution, pulse voltage list, repeats, reset-pre logic, compliance logging, and checkpoints unchanged unless the user explicitly authorizes electrical changes.

## Four outside-corner calibration points

Before the grid run, probe four points just outside the active grid corners, preferably sacrificial/non-device locations:

- outside top-left
- outside top-right
- outside bottom-left
- outside bottom-right

For these first four measurements, be extra cautious:

1. Force electrical cleanup before motion:
   - Keithley output off
   - Keysight output off
   - 707B `open_all`
   - verify `get_closed_channels == nil` when possible
2. Before each corner-to-corner Zaber X/Y move, move microscope stage Z **down/back by 100 steps** (`stage.move_z_by(height=-100)` using the user's convention Down = Z-).
3. Move Zaber X/Y to the outside-corner coordinate using absolute native-unit moves.
4. Use cautious Keithley-guided approach at low bias:
   - `0.01 V`
   - soft target `1–20 nA`
   - fine Z step `0.25`
   - read compliance around `200 nA`
5. Record Zaber X/Y, contact Z, final current, status, and any over-contact/weak-contact events.
6. After each corner contact, cleanup electrically and again move stage Z down/back by 100 steps before the next X/Y travel.

Do not use the Z-plane prediction until all four calibration points have been collected.

## Fit and use the plane

After four valid corner contacts:

1. Fit `Z_contact_est = a*X + b*Y + c`.
2. For each device, compute `Z_pred` from target Zaber X/Y.
3. Move to a conservative pre-approach height, preferably:

```text
Z_preapproach = Z_pred - safety_margin
```

rather than an ambiguous “80% of the way” expression. Start with a generous margin (e.g. 5–10 Z steps) until the model has been validated.
4. After pre-approach, always perform the same live low-bias Keithley contact check before any electrical stress.
5. If the pre-approach read is already above the soft window or at compliance, immediately retract in minimum valid increments and report over-contact/short-like; do not continue pushing forward.
6. If the read is open/noise-floor, continue the normal fine approach from the pre-approach height.

## Adaptive refinement

Append successful device contact-Z results to the calibration dataset and refit/update the plane or row-local residual correction. Use the plane to reduce mechanical search only; preserve electrical acquisition unchanged.

## Pitfall observed from direct move-to-device test

A prior device's historical contact Z is not always a safe pre-approach target after intervening alignment/motion. In a D52 revisit, moving to a previous contact estimate minus an 8-step margin still produced a 10 mV read at the 200 nA approach compliance and remained compliance-limited after repeated 0.25-step retractions. Therefore:

- Always perform a live low-bias read immediately after any predictive pre-approach.
- Treat compliance-limited current at the pre-approach point as a hard over-contact/short-like stop for the approach phase.
- Retract and cleanup rather than continuing the fine approach loop.
- Consider using a larger initial safety margin for revisits or after long time gaps.
