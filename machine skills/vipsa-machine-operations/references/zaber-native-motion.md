# Zaber native-unit / microstep motion via PUDA

Use this note when the user asks for Zaber movement in **microsteps** or **native units**.

## Key lesson

For the ViPSA `zaber` machine, PUDA exposes Zaber motion methods with optional `units`:

- `move_x_by(distance, units=None)`
- `move_y_by(distance, units=None)`
- `move_x_to(position, units=None)`
- `move_y_to(position, units=None)`
- `get_current_position(units=None)`

When `units` is omitted/null and the controller default is `None`, the edge uses native controller units. Treat user wording like “microsteps” as a request for `units: null`, not `"mm"`.

## Safe workflow

1. Verify the machine is present and idle:
   ```bash
   puda machine list
   puda machine state zaber
   puda machine commands zaber
   ```
2. If the user only says “move 500 microsteps” without an axis/direction, ask for axis and sign. Current Zaber exposes only X/Y methods, not Z.
3. Create a protocol with the relative move and a follow-up native-position read.
4. Validate before running.
5. Run the protocol and report command status plus returned position.

## Protocol template: X +500 microsteps

```json
{
  "description": "Move Zaber X axis by +500 microsteps/native units, then read current position in native units.",
  "commands": [
    {
      "step_number": 1,
      "name": "move_x_by",
      "machine_id": "zaber",
      "params": {
        "distance": 500,
        "units": null
      }
    },
    {
      "step_number": 2,
      "name": "get_current_position",
      "machine_id": "zaber",
      "params": {
        "units": null
      }
    }
  ]
}
```

Populate the project/user/protocol metadata to match the active PUDA project before validating/running.

## Reporting format

Keep Telegram reports concise:

- Axis/direction/distance/unit basis: e.g. `X +500 microsteps/native units`
- PUDA method: e.g. `move_x_by(distance=500, units=null)`
- Status: `success` or exact failure message
- Follow-up position payload: e.g. `x: ..., y: ...`

Avoid persisting transient run IDs in SKILL.md; session-specific run IDs can be mentioned only in the user reply when useful.
