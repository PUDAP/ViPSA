# ViPSA contact approach: step-size 1 and cleanup guard notes (2026-06-10)

This reference records reusable details from a live Keithley-guided ViPSA contact approach using PUDA one-command protocols.

## Context

User requested: `Perform approach with step size 1` after a 10 mV resistance check showed ~57.7 pA / ~173 MΩ.

Use the established defaults unless the user overrides them:

- `test_voltage = 0.01 V`
- `lower_current_threshold = 1e-8 A`
- `upper_current_threshold = 1e-7 A`
- `current_compliance = 10 * upper = 1e-6 A`
- `settle_s = 0.2`
- forward approach direction: `+Z`
- requested `step_size = 1`

## Execution pattern that worked

Run as an outer Python orchestrator that sends one-command PUDA protocols and parses each response; do not encode the loop as one static protocol.

Sequence:

1. Verify `keithley-2450`, `keithley-707b`, and `stage` are idle.
2. `keithley-2450.set_output(false)`.
3. `keithley-707b.connect_keithley_smu()`.
4. Loop:
   - `keithley-2450.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=1, reset=true only on first read)`.
   - If `abs(I) >= 1e-8`, contact is detected.
   - Otherwise `stage.move_z_by(height=+1, feedrate=450)` and wait `settle_s`.
5. If current is already in `[1e-8, 1e-7]`, no retract/fine moves are needed.
6. Read final `stage.get_current_position()`.
7. Always cleanup with an explicit validated cleanup protocol:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`
   - verify states for `keithley-2450`, `keithley-707b`, and `stage`.

## Observed outcome

- Contact remained at pA level for 32 `+Z` moves.
- Contact detected on coarse read 33.
- Final/stabilized current was `7.39e-8 A` at 10 mV, inside the 10–100 nA target window.
- Approximate resistance was `~135 kΩ`.
- Final stage position readback was `[0, 0, 82]`.
- Cleanup: Keithley output off, 707B closed channels `nil`, and all three machines idle.

These numbers are session-specific; do not assume future devices contact after the same travel.

## Pitfalls learned

- Keep cleanup independent and explicit. If the approach orchestrator cleanup helper has a bug or an exception path, immediately run a separate validated cleanup protocol before reporting final success.
- Do not command final trim moves smaller than the hardware-supported minimum. The ViPSA stage Z minimum commanded move is `0.25` steps; replace any legacy `0.1 * step_size` final retract with bounded `0.25`-step trim/re-read loops.
- Suppress per-step Telegram updates for the approach loop; report final contact status, travel count/net Z, final current, final position, and cleanup verification.
