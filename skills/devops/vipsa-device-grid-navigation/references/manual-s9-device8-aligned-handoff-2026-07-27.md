# Manual S9 device-8 handoff from current device (2026-07-27)

## Trigger
Use when the user is manually traversing S9 and asks to move to device 8 after recent device-7/current-device work, especially with an explicit stage-Z clearance command such as `move z stage down by 10 steps and move to device 8`.

## Key workflow
- Treat `device 8` as a named absolute device request, not as a simple adjacent `+5000` move from the current physical X/Y.
- Start with live readbacks for `stage` and `zaber`.
- Execute the user's explicit Z clearance exactly as requested (`stage.move_z_by(height=-10)` or later requested down amount) instead of stacking the default `-35` grid retract when a fresh safe clearance is being commanded.
- Before lateral motion, force electrical safety:
  - `keithley-2450.set_output(false)`
  - `keysight-b2902b.set_output(false)` when pulsing was just used
  - `keithley-707b.open_all()` and verify `get_closed_channels == nil`
- Prefer the archived aligned device coordinate when present and verified. For S9 device 8, a successful pattern was:
  - nominal from `grid_positions.csv`: `(266765, 491131)`
  - archived pre-align readback: `(266765, 491131)`
  - archived alignment move_native: `(-331, -489)`
  - aligned target: `(266434, 490642)`
- Use absolute native Zaber moves (`move_x_to`, `move_y_to`, `units: null`) to the aligned target, then read back stage and Zaber in a separate verification protocol.

## Reporting pattern
Report compactly:
- Stage Z signed move and readback delta, e.g. `z=-55.75 -> -65.75`.
- Zaber start and final readback.
- Whether target was nominal CSV or archived aligned coordinate.
- 707B `nil` and all relevant final machine states idle/null.

## Pitfall
If an archived `device_08/summary.json` stores `zaber_readback_pre_align` and `alignment.move_native`, compute the aligned absolute coordinate as `pre_align + move_native`. Do not use only the first correction from a contour list, and do not fall back to the row/column grid pitch unless the aligned evidence is absent or stale after remounting.
