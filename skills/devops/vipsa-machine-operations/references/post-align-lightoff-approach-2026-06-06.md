# Post-alignment light-off Keithley approach (2026-06-06)

Use this reference when the user has just run a ViPSA pad alignment/pre-move sequence, then tersely asks to turn lights off and perform approach.

## Pattern

1. Do not ask for approach parameters if this is the established electrical-contact workflow and no visual probe-deflection plan is required.
2. Turn lights off first with `light.turn_off()` and verify `puda machine state light` is idle.
3. Use Keithley-guided electrical approach defaults:
   - test voltage: `0.01 V`
   - lower current threshold: `1e-8 A`
   - upper current threshold: `1e-7 A`
   - current compliance: `10 * upper = 1e-6 A`
   - settle: `0.2 s`
   - forward direction: `+Z`
   - step: most recently used conservative step, typically `0.5`
4. Set `max_attempts` based on the immediately preceding intentional Z offset, with a bounded margin. Example: after `stage.move_z_by(height=-50)`, use `120` attempts at `0.5` to allow up to `+60` Z travel.
5. Loop measurement-before-motion: measure at `0.01 V`; if `abs(I) > lower`, contact is detected; otherwise move `+Z` by step.
6. If current is over the upper threshold, retract/trim as in the contact-approach workflow. If already within the window, just stabilize and report.
7. Always cleanup: Keithley output off, 707B `open_all`, verify `get_closed_channels() == nil`, and check final states.

## Concrete observed run

After an alignment sequence left stage Z at about `-98.85`, lights were turned off and a `0.5`-step approach was run with `max_attempts=120`.

- Initial current at `+10 mV`: about `5e-11 A` (pA noise floor).
- Contact detected after total `+45.5` Z travel.
- Final current after stabilization: `6.89362e-8 A` at `+10 mV`.
- Final Z readback: about `-53.35`.
- Resistance estimate: about `145 kΩ`.
- No over-current retraction or fine approach was needed.
- Cleanup left Keithley output off, 707B open, closed channels `nil`, and light/stage/Keithley/707B idle.

## Reporting

Use concise 👇 reporting:

- lights off status
- approach direction and step
- start/final Z and total Z travel
- final current and approximate resistance
- whether current is inside target window
- cleanup verification
