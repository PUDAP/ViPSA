# Foreground timeout during long per-step contact approach (2026-07-26)

## Trigger

A terse `approach` was run immediately after a verified manual Stage-Z `+50` move. The default electrical approach used many small per-step PUDA protocols:

- `test_voltage_v = 0.01`
- target window `10–100 nA`
- `step_z = +0.5`
- `max_moves = 120`
- cleanup after each read/move: Keithley output off + 707B open/all

Running the Python approach script in a foreground terminal with `timeout=600` timed out before the script's `finally` block completed, despite the hardware loop being near the end.

## Durable lesson

For contact-approach loops that may execute dozens of separate PUDA protocols, do **not** rely on a foreground `terminal(timeout=600)` even if 600 seconds seems sufficient. Use a tracked background terminal process with `notify_on_complete=true`, or reduce the per-run budget, so Hermes can continue after the terminal wrapper limit and the script can complete its own cleanup/final summary.

## Recovery pattern after timeout/interruption

If the foreground wrapper times out or is interrupted:

1. Check for still-running approach/PDUA protocol processes before deciding whether the run is complete.
2. Read the partial `summary.json` to recover:
   - last completed move index
   - net approach Z travel
   - last current and contact status
3. Do not repeat any Z motion blindly.
4. Run explicit recovery cleanup protocols:
   - `keithley-2450.abort_measurement()`
   - `keithley-2450.set_output(enabled=false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`
   - `light.turn_off()` when approach policy turns lights off
   - `stage.get_current_position()`
5. If 707B cleanup START fails with `cannot start, <old-run-id> is currently running` while `puda machine state keithley-707b` shows `idle` with that non-null run id, run `puda machine reset keithley-707b`, verify `idle/run_id:null`, then retry `open_all` + `get_closed_channels`.
6. Report the approach as interrupted/partial if the scripted max-move loop did not formally complete, but still report verified facts: final readback Z, last measured current, and cleanup state.

## Concrete outcome from this session

The approach reached 117 moves (`+58.5` commanded approach travel) before the foreground wrapper timed out. Fresh stage readback after recovery was `z=109`, consistent with the earlier `z=50` start plus approximately `+59`. Current remained pA-scale (`~3.48e-11 A` at 10 mV), far below the 10 nA lower threshold, so it was reported as no contact/very weak contact. Cleanup was verified only after resetting a stale 707B idle+non-null run id and rerunning `open_all`/`get_closed_channels == nil`.
