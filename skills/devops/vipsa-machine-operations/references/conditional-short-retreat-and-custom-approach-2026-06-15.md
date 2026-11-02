# Conditional short/perma-SET retreat and custom contact approach — 2026-06-15

Use this for user requests that chain electrical health logic with mechanical recovery, or ask for a deliberate Z pre-move followed by Keithley-guided contact approach using custom thresholds.

## Conditional short/perma-SET retreat pattern

When the user says: "check device health; if shorted/perma-SET then move Z down by N and move Zaber by M steps":

1. Do the electrical health check first. Do **not** move stage/Zaber unless the short/perma-SET condition is actually met.
2. Use low-bias Keithley reads through the 707B with conservative read compliance:
   - `0 V`, `±10 mV`, `±50 mV` by default.
   - Include `±100 mV` if the user asks to increase the probing voltage.
3. Classify `short/perma-SET` only if low-voltage reads are high or compliance-limited. pA/sub-nA reads are high-resistance / weak-contact-like and should not trigger mechanical retreat.
4. If condition is met and the user gave explicit motion values, execute exactly those moves:
   - Stage Z down = negative signed `stage.move_z_by(height=-N, feedrate=450)` in the current ViPSA convention.
   - Zaber native/microstep move should keep `units: null` unless the user explicitly requests millimetres; require axis/direction if not specified.
5. Cleanup electrical route regardless of whether motion occurs.

## Custom pre-move + approach pattern

When the user says: "move Z down by N steps and perform approach" with explicit approach parameters:

1. Execute the pre-move first: down means signed negative Z (`height=-N`).
2. Then route DUT to Keithley and run the outer-loop approach script, not a single static protocol.
3. Use the user-specified values exactly:
   - `test_voltage`
   - `step_size`
   - `lower_current_threshold`
   - `upper_current_threshold`
4. Compliance can be `10 * upper_current_threshold`, capped conservatively if needed.
5. Approach forward is +Z in the user's current convention.
6. Coarse loop: measure at `test_voltage`; if `abs(I) <= lower`, move `+step_size` and remeasure.
7. If `abs(I) > upper`, retract using the minimum reliable stage increment (`-0.25` Z) and remeasure until below upper or a hard limit.
8. After apparent contact, wait/stabilize and remeasure. If it falls below lower, fine-approach using `+0.25` Z increments; do not command smaller increments.
9. Final trim from over-upper should also use bounded `-0.25` Z increments, because the hardware cannot execute smaller Z increments reliably.
10. Report:
    - pre-move position
    - number and size of approach increments
    - final position
    - final current at the requested probe voltage
    - whether the final current lies within the requested current window
    - cleanup status and idle machines.

## Concrete observed example

A user requested:

```text
move z down by 10 steps and perform approach
step size = 0.5 steps
lower = 5e-10 A
upper = 5e-8 A
contact voltage = 50 mV
```

The safe execution was:

```text
pre-move: stage.move_z_by(height=-10)
then approach: +0.5 Z coarse increments at 50 mV
contact stabilized after 12 forward increments
final current ≈ 3.65e-9 A at 50 mV
final status: inside requested 5e-10 to 5e-8 A window
cleanup: Keithley output off, 707B open_all, closed_channels nil, machines idle
```

This example reinforces that a large deliberate down pre-move can be followed by a bounded +Z approach and that the result should be reported as concise verified hardware state, not a plan.
