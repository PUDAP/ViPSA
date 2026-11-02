# Interrupted PUDA stage-motion reconciliation

Use this when a client/terminal interruption occurs while `puda protocol run` is executing a physical stage move.

## Core rule

An interrupted local command is **not evidence that motion failed**. The edge may have already received and completed `move_z_by`. Never blindly repeat the move.

## Recovery workflow

1. Preserve the interrupted run directory and read its artifacts:
   - the last successful pre-move `get_current_position` response;
   - generated motion protocol and signed `height`;
   - motion run output, if any.
2. Inspect live stage state. Treat `idle` with a non-null `run_id` as incomplete/stale cleanup, not as a trustworthy final state.
3. Attempt stale-state cleanup only if needed. `puda machine reset stage` may return `Unknown or restricted command: reset`, transiently set `state:error`, and still clear the stale `run_id`; therefore always re-read state instead of trusting reset exit text alone.
4. Run a **fresh full-metadata read-only protocol** containing only `stage.get_current_position()`.
5. Compare live position against the preserved pre-move position:
   - delta equals requested signed move: motion already completed; do not repeat;
   - delta is zero: motion did not occur; after recovering `idle`/`run_id:null`, execute the original move once;
   - partial/unexpected delta: stop and report; do not guess or automatically complete the remainder without explicit authorization.
6. Require final `stage` state `idle`, `run_id:null` before continuing to alignment or another chained hardware phase.

## Chained move → alignment

If the user requested stage Z motion before visual alignment, reconcile the stage move first. Only after the requested signed delta is verified should the alignment runner capture a fresh camera frame, move Zaber, recapture, verify residual, and set the requested final light state.

## Reporting

Report the preserved pre-position, verified post-position, signed delta, and whether the motion was recovered as already completed. Do not describe local interruption as a failed physical move when readback proves otherwise.
