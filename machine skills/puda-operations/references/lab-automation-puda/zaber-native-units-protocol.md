# Zaber native-units protocol via PUDA

Session-derived example for moving a PUDA-connected Zaber stage by native units/microsteps.

## Discovery

Useful commands:

```bash
puda machine list
puda machine commands zaber
puda machine state zaber
```

Observed Zaber command signatures included:

```text
move_x_by(self, distance: float, units=None) -> None
move_y_by(self, distance: float, units=None) -> None
get_current_position(self, units=None) -> dict[str, float]
```

The machine state endpoint returned an idle state before motion:

```json
{"state": "idle"}
```

## Native units / microsteps

For a request like "move 500 microsteps", use native units by passing JSON `null` for `units`:

```json
{"distance": 500, "units": null}
```

Do **not** pass `"mm"` unless the user explicitly asked for millimeters.

## Minimal protocol shape

```json
{
  "project_id": "<project uuid>",
  "protocol_id": "<new uuid>",
  "user_id": "<user uuid>",
  "username": "vipsa",
  "description": "Move Zaber X axis by +500 microsteps/native units, then read current position in native units.",
  "timestamp": "<UTC ISO timestamp>",
  "commands": [
    {
      "step_number": 1,
      "name": "move_x_by",
      "machine_id": "zaber",
      "params": {"distance": 500, "units": null}
    },
    {
      "step_number": 2,
      "name": "get_current_position",
      "machine_id": "zaber",
      "params": {"units": null}
    }
  ]
}
```

Validate then run:

```bash
puda protocol validate --file protocols/<uuid>.json
puda protocol run --file protocols/<uuid>.json
```

## Success evidence to report

A successful run reports:

- protocol created metadata
- `Run ID: <uuid>`
- `Command ... succeeded: move_x_by`
- response with `"status": "success"`
- readback command response containing `data`, e.g. `{ "x": ..., "y": ... }`

Always include the exact run ID and readback data in the final user response.
