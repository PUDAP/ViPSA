# Compound ViPSA pre-move then contact approach (2026-06-30)

Use this reference when the user gives a chained mechanical sequence followed by `approach`, for example: `move stage down by 40 steps, move zaber stage x by 5000, then move stage down by 25 steps, then approach`.

## Operational pattern

- Treat the request as one executable chain; do not split into separate confirmations when the operations are explicit and the active ViPSA defaults are already established.
- Preserve the user’s wording for directions:
  - `stage down N steps` maps to `stage.move_z_by(height=-N, feedrate=450)` under the current user convention.
  - `zaber stage x by N` maps to `zaber.move_x_by(distance=N, units=None)` unless the user specified units.
- Before mechanical moves, put electrical instruments in a safe state:
  - `keithley-2450.set_output(enabled=false)`
  - `keithley-707b.open_all()`
  - lights off before electrical approach unless the user asked to keep them on.
- Capture readbacks after each pre-move:
  - `stage.get_current_position()` after each Z move.
  - `zaber.get_current_position(units=None)` after Zaber moves.
- Then run the default contact approach loop with the existing ViPSA defaults unless the user supplied parameters:
  - `test_voltage=0.01 V`
  - `lower=1e-8 A`, `upper=1e-7 A`
  - `read_compliance=1e-6 A`
  - approach forward `+Z`, commonly `0.5` stage steps per coarse increment and `0.25` for trim.

## Reporting rule

Report the full chain as verified facts: each requested move, key readbacks, approach status, final current, final stage position, and cleanup.

If contact jumps from pA/no-contact into over-current and trimming drops it back to pA/open-like without landing in the target current window, do **not** call it contacted. Report it as `not stabilized` / `snap-in/snap-out`, and say it ended in the safer weak/open-like state.

## Cleanup

Always end by verifying:

- Keithley output off.
- 707B `open_all()` succeeded.
- `keithley-707b.get_closed_channels()` returns `nil`.
- Relevant machines are idle when practical: `keithley-2450`, `keithley-707b`, `stage`, `zaber`, and `light`.
