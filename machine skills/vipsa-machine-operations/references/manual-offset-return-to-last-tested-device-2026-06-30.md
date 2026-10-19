# Manual offset return to last tested device

Use this when the user manually jogs Zaber away from a device and later asks to move back to the last tested device.

## Pattern learned

If the only movement away from the last tested device was a known relative Zaber jog, reconstruct the previous absolute target from the latest verified Zaber readback plus the inverse of that jog.

Concrete example from session:

```text
Latest verified Zaber readback after manual jog: x=37861, y=702673
Manual jog that moved away: X -100, Y -300
Reconstructed last tested device: x=37861+100=37961, y=702673+300=702973
```

## Safe return sequence

1. Keep the calculation explicit in the reply when the user asks for the position.
2. Do **not** imply the return move has executed if only the protocol was generated.
3. If the user asks to return to that position, first perform the requested safe microscope-stage Z retraction/down move before any Zaber X/Y travel.
4. Move Zaber using absolute native-unit commands (`move_x_to`, `move_y_to`) to the reconstructed target rather than another relative inverse jog, unless the user explicitly asks for a relative jog.
5. Read back both stage Z and Zaber X/Y after the move.
6. Report final `idle` / `run_id: null` states for both `stage` and `zaber`.

Verified example sequence:

```json
[
  {"step_number": 1, "machine_id": "stage", "name": "move_z_by", "params": {"height": -20, "feedrate": 450}},
  {"step_number": 2, "machine_id": "zaber", "name": "move_x_to", "params": {"position": 37961, "units": null}},
  {"step_number": 3, "machine_id": "zaber", "name": "move_y_to", "params": {"position": 702973, "units": null}}
]
```

Readback after the verified return example:

```text
stage z = 36.75
zaber x = 37961
y = 702973
stage state: idle, run_id null
zaber state: idle, run_id null
```

## Pitfall

A terse user phrase like “this position” may refer to the position calculated in the previous assistant message, not the current stage/Zaber position. Use the immediately preceding verified calculation as the target, and state the coordinates being used before/while reporting the result.
