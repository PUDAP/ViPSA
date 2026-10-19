# Manual grid restart from a specific device after safe Z/Zaber handoff (2026-06-24)

Use this note when a ViPSA grid run is stopped/failed and the user asks for an explicit manual handoff such as: retract Z, move to a specific device, raise Z partway, approach, then restart the grid from that device.

## Durable workflow lesson

Do not hide the whole handoff inside one long opaque grid-runner process. Split the operation into verified phases so the user can trust that the requested physical motions happened before electrical stress starts:

1. Preflight/cleanup: verify the six ViPSA machines (`light`, `stage`, `zaber`, `keithley-2450`, `keithley-707b`, `keysight-b2902b`) are not carrying stale run IDs; force electrical cleanup (`set_output(false)`, `open_all`, `get_closed_channels`) where needed.
2. Archive or clearly mark stale device folders for the restart range. If restarting from device N, do not let old `device_N/DONE.json` cause the runner to skip it.
3. Execute the explicit user-requested motion as its own verified phase:
   - `stage.move_z_by(height=-<retract>, feedrate=450)` for down/retract in the current convention.
   - `zaber.move_x_to` / `move_y_to` to the grid coordinates for the requested device.
   - `stage.move_z_by(height=+<preapproach>, feedrate=450)` for the requested up/pre-approach.
   - Read Zaber position back; stage readback may return `[null, null, null]`, so do not invent a Z coordinate.
4. Turn lights off before electrical approach/measurements unless the user explicitly asks to keep them on. This was an explicit user correction during restart.
5. Run Keithley-guided approach as a separate bounded phase and record `approach.json` before starting DCIV/pulse measurement.
6. Start the grid continuation only after the approach phase is recorded. For the first restarted device, reuse the recorded approach result and do **not** re-run the manual Z/Zaber handoff inside the grid runner.
7. Resume the device-finish reporter only after the continuation process is actually started.

## Pitfalls observed

- A monolithic patched runner produced no stdout while it was doing motion/approach, making it hard to verify progress; split scripts/foreground phases are better for manual handoffs.
- `puda machine reset stage`, `light`, or `zaber` may be unsupported and can temporarily set the machine state to `error`. Recover with a harmless full-metadata protocol: for light, `initialize(startup_command="off")` then `turn_off`; for Zaber/stage, a read-only `get_current_position` can restore idle/start-complete state. Do not store this as "reset is broken"; the durable lesson is the recovery pattern.
- If the standalone approach finishes with weak/open-like current (for example pA/tens of pA after max attempts), report it honestly. If the active run policy says to continue open/weak devices anyway, record that continuation as an explicit policy override rather than implying good contact.

## Reporting standard

Keep the Telegram update concise:

- target device and Zaber readback
- requested Z motions executed
- lights off before measurements
- approach status and final current
- continuation process ID/PID and reporter state
