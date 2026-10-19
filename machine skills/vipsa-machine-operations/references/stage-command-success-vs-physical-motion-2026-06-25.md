# Stage Z command success vs physical motor movement

Session lesson: PUDA `stage.move_z_by(...)` can return `response.status: success` and `stage.get_current_position()` can update the tracked Z value even when the user observes that the Z motor did not physically move.

## Trigger

Use this when:

- The user says the stage motor is not moving after successful Z commands.
- Video or direct visual observation contradicts PUDA success/readback.
- PUDA edge state timestamps are stale or START commands begin timing out after edge restart.

## Operational rule

Do **not** claim confirmed physical Z motion from PUDA response/readback alone when physical evidence contradicts it. Report the split explicitly:

- PUDA command response: succeeded/failed.
- Tracked/readback Z: value if available, but mark it as internal/tracked.
- Physical motion: unconfirmed or contradicted by observation.

If the user reports no motor movement, stop further motion unless the user explicitly asks to keep trying. Run read-only diagnostics first:

```bash
puda env current
timeout 5 puda machine state stage
puda machine commands stage
```

Then try a fresh one-command `get_current_position()` protocol only if needed. Avoid stacking additional Z moves based on stale tracked coordinates.

## Likely hardware checks to suggest

- Z motor power / driver enable.
- Loose motor cable.
- Coupler/lead screw slipping.
- Arduino/stage controller connected but motor output disabled or faulted.

## Reporting standard

Example:

```text
No confirmed physical Z motion.
PUDA `move_z_by(height=-20)` failed at START / or returned success, but observed motor movement contradicts it.
Tracked Z readback is <value> but should not be trusted as physical confirmation right now.
Stage state: idle, run_id null/stale timestamp.
```
