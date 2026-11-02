# Retained-prefix recovery after a user-directed retract and realignment

Use when adaptive preparation reached a guarded Z ceiling without forming, cleanup is verified, and the operator explicitly directs a new mechanical focus/recovery sequence before continuing the same device.

## Validated recovery pattern

1. **Pause autonomous continuation.** Confirm no measurement worker is alive.
2. **Reconcile the stopped preparation.** Require:
   - every latest motion/electrical operation is `COMPLETE`;
   - `unknown=false`;
   - output OFF, matrix `nil`/open, empty errors;
   - exact completed forming/conditioning counts;
   - no candidate ledger/cycles started.
3. **Preserve the stopped terminal and ledger unchanged.** Back them up and hash them. Completed forming sweeps are retained exposure and must never be replayed.
4. **Execute the operator’s mechanical sequence literally, with exact readback after each move.** For an absolute-zero then retract instruction, first move from the live tracked Z to logical Z0, then make the signed retract (for example `-50`). Never use Stage reset/set-zero as a substitute for motion.
5. **Use lights only for optical alignment.** Capture a fresh Camera 1 frame, verify same-device/same-pad lattice identity, and align at the retracted height. If direct contour detection is confused by probe occlusion, register substrate-only ROIs against the last verified aligned frame. Require corroborating shifts and a bounded residual; do not chase a neighboring contour.
6. **Turn lights OFF before electrical approach/forming.** Save the command acknowledgement. The worker should also issue `light.turn_off` immediately before motion/stress.
7. **Create an immutable recovery authorization artifact** binding:
   - the user’s verbatim instruction;
   - stopped terminal/ledger hash and retained counts;
   - manual-move terminal hashes;
   - fresh alignment path/hash and pose;
   - lights-off requirement;
   - pre-approach delta/target;
   - next missing forming-attempt index;
   - maximum authorized Z;
   - `automatic_replay=false`.
8. **Patch/construct a narrowly scoped resume path.** It must accept only the exact device, exact original fault, exact retained counts, verified cleanup/no-UNKNOWN state, and immutable recovery hashes.
9. **Pre-approach once from the new aligned pose.** If standard preparation uses `+40`, apply it once. Resume the next missing forming attempt at that pose **without** the usual additional `+5` that would precede later attempts. Subsequent attempts may use normal bounded `+5` increments.
10. **Verify live execution before re-enabling automation.** Confirm the recovery marker is COMPLETE, retained attempt indices were not replayed, the pre-approach readback is exact, the next missing attempt completed or is running, lights are off, and `unknown=false`.

## Partial final increment at a Z ceiling

If normal `+5` increments would overshoot an explicitly authorized maximum, use the positive remainder once (for example `Z268 -> Z270` via `+2`) and run the next forming attempt there. If it still fails, stop before another attempt. Never round past the authorization.

## Edge/lifecycle recovery during preflight

A harmless getter can time out because the local edge process is absent while START/COMPLETE remains in the durable queue. Treat this as zero exposure only when no preparation ledger event, motion, or electrical command was created.

- Inspect the exact wire run ID.
- Start exactly one replacement process from the canonical edge directory.
- Let it consume the retained COMPLETE and verify `idle`, `run_id=None`.
- For Stage, never use `machine reset`; it can redefine logical zero. Restarting the single edge must preserve and report the persisted confirmed position.
- Check all locally required edges together before retrying so failures do not cascade one edge per preflight.

## Reporting

Report separately:

- retained forming sweeps;
- manual retract and realignment pose/residual;
- lights-off proof;
- pre-approach endpoint;
- next missing attempt number;
- replay count (must be zero);
- UNKNOWN state;
- whether candidate cycles have started.
