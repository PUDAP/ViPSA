# Manual device revisit with absolute Stage-Z target then approach (2026-06-30)

## Context

During a paused ViPSA grid run, the user requested an explicit physical handoff:

1. Move Stage Z down by 10 steps.
2. Move Zaber to a previous grid device (device 14).
3. Bring Stage Z up/to an explicit absolute tracked height (`z = -19.75`).
4. Run the standard Keithley-guided contact approach.

## Durable workflow lesson

When the user gives an explicit **absolute Stage-Z height** before approach, treat it as a verified pre-approach target, not a relative up/down amount:

1. Force electrical safe state before motion:
   - `keithley-2450.set_output(false)`
   - `keysight-b2902b.set_output(false)`
   - `keithley-707b.open_all()`
   - `light.turn_off()` before electrical work unless explicitly kept on
2. Read current Stage Z.
3. Execute the requested preliminary relative safe move, e.g. `stage.move_z_by(height=-10, feedrate=450)`.
4. Read Stage Z again.
5. Move Zaber to the target device's absolute grid coordinates recovered from the saved device summary (`target.x`, `target.y`) using native-unit `move_x_to` and `move_y_to`.
6. Compute the Stage-Z delta to the requested absolute target:
   ```text
   dz = target_z - current_z
   stage.move_z_by(height=dz, feedrate=450)
   ```
7. Read Stage Z back and require it to be close to the requested absolute target before approach. If the readback is missing or outside tolerance, stop rather than approaching from an unverified height.
8. Run the normal bounded Keithley approach separately from this handoff, then cleanup and verify.

## Approach reporting rule

If the approach starts at the requested absolute pre-approach Z but remains pA/sub-nA after the bounded max attempts, report `no_contact_after_max` honestly and do not imply contact just because the Stage Z moved a large positive distance. Include:

- initial Z, post-safe-retract Z, requested absolute pre-approach Z, verified pre-approach readback;
- target device Zaber X/Y and readback;
- approach net Z travel and final Stage-Z readback;
- final current relative to the 10–100 nA target window;
- cleanup: SMU outputs off, 707B `get_closed_channels == nil`, light off, all machines idle/null.

## Concrete verified pattern

A representative run used:

```text
initial stage z: 100.5
safe move: -10 -> z 90.5
target device: 14, zaber x=39174, y=489294
absolute pre-approach target: z=-19.75
delta to target after safe move: -110.25
approach: +90.0 coarse + +5.0 fine = +95.0 net
final z: 75.25
final current: ~3.6e-11 A
status: no_contact_after_max
```

This teaches the workflow and reporting pattern only; do not reuse the numeric coordinates or Z values unless they are recovered from the current run artifacts or explicitly requested.
