# Grid default: post-align +40 pre-approach and current-device handoff

Session-derived corrections for ViPSA grid runs and restarts.

## Durable correction

For future grid measurements, the default between-device sequence is:

```text
stage.move_z_by(-50)
zaber.move_x_to(target_x)
zaber.move_y_to(target_y)
align
stage.move_z_by(+40)
approach
```

Do **not** use the older order where the stage pre-approach `+30` happened before vision alignment. Alignment should occur at the safe/retracted optical position; only after alignment should the stage move `+40` before electrical approach.

## Current-device handoff pattern

When the user says the current physical device is a specific grid device and asks to approach it before continuing the grid:

1. Treat the named device as the boundary and archive stale `device_N` artifacts before overwrite.
2. Do not move Zaber or re-align if the user says to operate the current device in place.
3. Apply only the user-requested Z pre-move, e.g. `stage.move_z_by(+15)` or `+20`, then run approach from the verified readback.
4. Save results under the named device folder and update run summary.
5. Continue to subsequent devices only if the contact gate passes; otherwise stop at that device and record `skipped_contact_not_in_window` or equivalent.

## Stop/cleanup during handoff

If a manual current-device approach is stopped mid-run, kill the tracked approach process, run cleanup immediately, and report cleanup verification rather than only saying “operation interrupted.” Required cleanup: Keithley output off/abort, Keysight output off/abort, 707B open + `get_closed_channels == nil`, lights off, stage abort/readback, and all machine states idle/null.
