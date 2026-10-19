# Contact approach defaults: observed execution pattern

Use this as a compact reference for implementing the ViPSA Keithley + stage contact-approach workflow with the standard defaults.

## Default parameter set

```text
test_voltage = 0.01 V
lower_current_threshold = 1e-8 A
upper_current_threshold = 1e-7 A
step_size = 1
max_attempts = 50
settle_delay = 0.2 s
forward = +Z
current_compliance = 10 * upper_current_threshold = 1e-6 A
```

## Validated orchestration pattern

Run the approach as an outer script that issues one-command PUDA protocols and parses each response, not as a single static protocol. Keep cleanup in a `finally` block.

Sequence:

1. Verify `keithley-2450`, `keithley-707b`, and `stage` are idle.
2. `keithley-2450.set_output(enabled=false)`.
3. `keithley-707b.connect_keithley_smu()`.
4. Coarse loop: measure with `hold_voltage_measure_current(...)`; if `abs(I) <= lower`, move `stage.move_z_by(height=+1)` and settle.
5. If current exceeds `upper`, retract in bounded `-0.5 * step` increments, measuring after each move.
6. Stabilize for `5 * settle_delay`, then remeasure.
7. If current falls below `lower`, fine approach in bounded `+0.25 * step` increments.
8. If fine approach overshoots above `upper`, perform bounded final trim retractions of `-0.1 * step`, measuring after each trim until current is within range.
9. Read `stage.get_current_position()`.
10. Always cleanup: Keithley output off, `keithley-707b.open_all()`, `get_closed_channels()` should return `nil`, and final states should be `idle`.

## Durable pitfall

A fine approach can jump from below threshold to over-current/compliance. Do not report the fine-approach measurement as final if it exceeds the upper threshold; perform the final trim loop and report the post-trim measurement.

## Direct-NATS fallback and snap-in/snap-out behavior — 2026-06-13

If `puda protocol run` fails at START with the Keithley 707B reporting `RUN_ID_MISMATCH` against the same newly-created run id, do not keep retrying the same protocol-runner path. Use the direct PUDA/NATS command pattern from the manual jog panel / direct contact-check fallback:

1. Reset stale machines if needed.
2. Direct core-NATS publish `start` to `keithley-2450`, `keithley-707b`, and `stage`.
3. Treat a 707B START response like `RUN_ID_MISMATCH` where the message contains the same run_id as a duplicate-start artifact, not a true different active run.
4. Send queued commands under that run id: Keithley output off, 707B route, repeated low-bias reads, Z moves, cleanup, then COMPLETE.
5. Always verify `set_output(false)`, `open_all`, `get_closed_channels == nil`, and idle states.

Observed contact behavior can be discontinuous: pA/no-contact over many +Z increments, then a sudden jump to compliance/over-contact, and after a small retract it can fall back to pA. If the minimum reliable Z increment cannot land in the `10–100 nA` target window, report the approach as **not stabilized** and leave the device in the safer open/weak-contact state rather than leaving it compliance-limited.
