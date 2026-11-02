# Authorized Z-ceiling and retained-prefix preparation recovery

Use when forming stops at a software Z ceiling, completed sweeps are durable, and the operator authorizes either an exact higher ceiling or a deliberate retract/re-align/re-approach recovery.

## Exact-ceiling continuation

- Preserve every completed forming/conditioning sweep and criterion result; never restart preparation from attempt 1.
- Require `unknown=false`, verified output OFF, matrix open/nil, empty errors, and exact live/persisted pose before any continuation.
- Bind the operator’s verbatim authorization to a versioned, hashed artifact with old/new ceiling, device/candidate scope, retained counts, resume pose, and no-replay policy.
- When the normal increment would overshoot an authorized ceiling, use `min(normal_step, ceiling-current_z)`. Example: from Z268 with a +5 normal step and a Z270 ceiling, issue exactly +2, verify Z270, then run the next missing forming attempt.
- If that attempt fails at the ceiling, stop before another sweep; do not interpret “up to Z270” as permission to exceed it.

## Manual retract, re-align, and preparation rebase

When the operator explicitly requests a large retract followed by alignment and renewed approach:

1. Pause autonomous continuation and prove no measurement worker is active.
2. Force/verify electrical safety, then execute the exact retract with durable motion intent and exact readback.
3. Capture a fresh alignment frame at the retracted pose. If the target pad is partially occluded, register substrate-only ROIs against the last verified same-pad frame rather than chasing a neighboring contour.
4. Seal a new alignment record with same-pad review, residual, pose, image hashes, and `physical_contact_claim=false`.
5. Create a hashed recovery authorization that links the old preparation terminal, manual retract terminal, new alignment, retained sweep counts, next missing attempt, pre-approach delta, ceiling, and light policy.
6. Turn lights OFF before electrical approach/stress.
7. Apply the standard pre-approach from the new baseline, then run the next missing forming attempt immediately. Do **not** add the normal inter-attempt Z increment before that first resumed attempt.
8. Resume normal move-then-sweep increments only after the first resumed attempt.

Worked boundary: three failed forming sweeps at Z270 were retained; the operator commanded Z270→Z0, lights on for inspection, Z0→Z−50, and re-alignment. Recovery used +40 pre-approach to Z−10 and ran attempt 4 there without replay. Later attempts advanced +5; forming succeeded at attempt 6 at Z0, followed by all conditioning sweeps and candidate measurement.

## Lifecycle timeout recovery before motion

A harmless preflight getter can time out because an edge process is absent after START/COMPLETE intent. Treat this as zero exposure only when no motion/stress intent was written and the wire journal proves the command boundary.

- Restart exactly one missing affected edge from its canonical deployment; do not start duplicates.
- Let the edge consume the retained COMPLETE for the exact run, then require `idle` and `run_id=None`.
- For Stage, never use machine reset to clear the lifecycle hold because reset can redefine logical zero. Restarting the absent Stage edge may consume the retained getter COMPLETE while preserving the persisted position.
- Start other missing prerequisite edges before retrying the full preflight to avoid serial timeout discovery.
- Retry only the preflight/recovery entry, never completed motion or electrical exposure.

## Verification and history

Before candidate dispatch, verify aggregate unique COMPLETE operation IDs, retained/new sweep counts, final pose, cleanup, and `unknown=false`. Append-only ledgers may retain an old fault/error string after status becomes `preparation_complete`; preserve it as history, but use current terminal status plus structured proofs for the active state.