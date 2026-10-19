# Stage Z move and position readback split-protocol pattern (2026-06-24)

Context: After a paused ViPSA grid run, the user requested a simple stage-Z retreat: “move z stage down by 5 steps”.

Working command path:

1. Verify PUDA env is `bears` and `stage` is idle.
2. Generate a full-metadata PUDA protocol for a single physical move:
   - `stage.move_z_by(height=-5, feedrate=450)` for “down 5 steps” using the user's convention: Down = negative Z/backward.
3. Run from `/home/vipsa/vipsa-puda-project` with ViPSA NATS override if needed.
4. Verify final `stage` state with `timeout 3 puda ... machine state stage`.
5. If numeric position is needed, use a fresh separate protocol containing only `stage.get_current_position()`.

Observed pitfall:

A two-step protocol combining:

1. `move_z_by(height=-5, feedrate=450)`
2. `get_current_position()`

had the physical move succeed, but the second command failed with:

```text
Run ID mismatch: expected active run, got <same run id>
```

The protocol runner then completed the machine. A fresh one-command `get_current_position()` protocol succeeded immediately afterward.

Reporting standard:

- If `move_z_by` response status is `success`, report the signed move as executed even if the subsequent readback step failed.
- Still verify `stage` returns to `idle` with `run_id: null`.
- If the separate position read returns `[null, null, null]`, say the driver returned no numeric X/Y/Z readback rather than inventing a Z coordinate.
- Keep the report concise: signed motion, command success, final state, and whether numeric readback was available.
