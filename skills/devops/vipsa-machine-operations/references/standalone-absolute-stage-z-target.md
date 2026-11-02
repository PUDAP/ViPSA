# Standalone absolute Stage-Z target via relative PUDA motion

Use this pattern when the user gives an absolute microscope-stage Z target such as `move z stage to Z = 20`.

## Why

The ViPSA `stage` driver exposes `get_current_position()` and relative `move_z_by(height, feedrate=450)`, but no general `move_z_to` method. Therefore, implement an absolute target by measuring the live position and calculating one relative delta.

## Procedure

1. Verify `stage` is `idle` with `run_id: null`.
2. Run a **read-only, full-metadata PUDA protocol** containing only `stage.get_current_position()`.
3. Parse the returned `[x, y, z]` and compute:

   ```text
   delta_z = requested_target_z - live_z
   ```

4. Confirm `delta_z` is representable at the stage's minimum `0.25`-step resolution. Do not silently round a nonrepresentable target; ask the user or state the nearest valid values.
5. Generate and validate a one-command, full-metadata PUDA protocol:

   ```json
   {
     "step_number": 1,
     "name": "move_z_by",
     "machine_id": "stage",
     "params": {"height": 120.5, "feedrate": 450}
   }
   ```

6. Run the move protocol. Do not combine the position readback into the same run.
7. Run a fresh, separate `get_current_position()` protocol and require the reported Z to equal the requested target within stage resolution.
8. Verify final `stage` state is `idle` with `run_id: null`.
9. Report only the previous Z, signed delta, verified final Z, and final state. Do not mention stage X/Y unless they changed.

## Safety and pitfalls

- Use the user's established sign convention: positive `height` is Z up/forward; negative is Z down/backward.
- Never use `disconnect()` to reach zero; it has unrelated connection side effects and itself moves the stage.
- Do not use `go_to_zero()` for arbitrary targets.
- If the initial position read returns nulls, do not guess a delta or move.
- If the motion command is interrupted, do not repeat it blindly. Re-read position first and reconcile the actual delta.
- A successful command/readback verifies the controller's tracked position. If the user reports contradictory observed physical motion, treat tracked Z as untrusted and stop further motion.

## Verified example

A live read returned `Z = -100.5`. For requested target `Z = 20`, the computed move was `+120.5`. The `move_z_by` response succeeded, a separate read returned exactly `Z = 20`, and final stage state was idle/null.
