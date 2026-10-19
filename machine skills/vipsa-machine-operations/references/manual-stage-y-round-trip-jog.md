# Manual Stage-Y Round-Trip Jog

Use this pattern for an explicit request such as “move stage Y by +10 and -10.” It is a microscope-stage X/Y operation, so execute only when the user explicitly names the Y axis.

## Protocol-first sequence

1. Confirm `stage` is `idle` with `run_id: null`.
2. Query live stage commands and confirm `move_y_by(steps)` is exposed.
3. Create and validate one full-metadata PUDA protocol with two sequential commands:

```json
[
  {
    "step_number": 1,
    "name": "move_y_by",
    "machine_id": "stage",
    "params": {"steps": 10}
  },
  {
    "step_number": 2,
    "name": "move_y_by",
    "machine_id": "stage",
    "params": {"steps": -10}
  }
]
```

Preserve the exact order and signs supplied by the user. The PUDA protocol runner automatically sends machine `START` before the command array and `COMPLETE` afterward; do not add fake driver commands named `START` or `COMPLETE` to `commands` unless live protocol schema explicitly requires them.

4. Require a success response for both moves. Do not infer the second move from protocol completion alone.
5. Run a separate read-only `stage.get_current_position()` protocol after the jog; a separate protocol avoids multi-command run-state/readback issues.
6. Verify final `stage` state is `idle` with `run_id: null`.

## Reporting

Report both signed moves, the final `(x, y, z)` readback, net Y displacement, and final stage state. If no pre-move position was captured, do not claim the final coordinate proves a return to the original position; report only that the two successful relative commands algebraically sum to zero. A pre/post comparison is required for a verified physical return. If the user reports that the motor did not visibly move, treat tracked coordinates as untrusted and do not claim physical motion from PUDA responses alone.
