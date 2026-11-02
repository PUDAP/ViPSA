# Manual retract, re-align, and retained-prefix forming recovery

Use this recovery when preparation reaches an authorized Z ceiling without satisfying its forming criterion, cleanup is verified, no operation is UNKNOWN, and the operator explicitly requests a mechanical reset/re-alignment before continuing the same candidate.

## Preconditions

- Pause autonomous continuation and confirm no measurement worker owns the hardware.
- Reconcile the preparation ledger by operation ID. Retain only forming/conditioning sweeps whose latest event is `COMPLETE` with exact native evidence.
- Require `unknown=false`, output OFF, matrix open/`nil`, empty errors, and a verified cleanup record.
- Treat the old Z-limit failure as a preparation boundary, not a candidate failure. Candidate cycles remain zero until preparation completes.

## Recovery sequence

1. **Reconcile position before motion.** Query live Stage/Zaber state and compare it with durable motion records. Never infer position from forming-sweep count.
2. **Execute the operator’s mechanical reset literally.** For an absolute Z request, calculate one signed relative move from fresh readback and require exact target readback. Do not use Stage `reset`/`set_zero`; those redefine logical coordinates.
3. **Align at the requested retracted pose.** Use fresh Camera 1 evidence, preserve same-pad identity, and apply only bounded corrections. Optical alignment does not establish contact.
4. **Control illumination explicitly.** Lights may be on for image capture/alignment, but require an acknowledged `turn_off` immediately before electrical approach/forming unless the operator explicitly latches illumination.
5. **Write an immutable recovery authorization.** Link and hash:
   - the interrupted preparation terminal;
   - retained forming/conditioning counts;
   - the manual retract/motion terminal;
   - the new alignment record and pose;
   - the exact pre-approach move;
   - the next missing forming attempt;
   - the active Z ceiling;
   - `replay_completed_forming=false`.
6. **Gate the executor narrowly.** Accept only the exact device, candidate, prior fault, retained counts, verified cleanup, `unknown=false`, and unchanged evidence hashes. Reject any mismatch.
7. **Resume without double approach.** From the new aligned/retracted pose, execute the authorized pre-approach exactly once. Run the next missing forming attempt immediately at that resulting pose; do **not** also apply the normal inter-attempt `+5` before this first resumed attempt. Apply normal bounded `+5` increments only before subsequent attempts.
8. **Continue normally after forming.** If the criterion passes, finish remaining conditioning, publish aggregate preparation linked to the retained prefix, and start candidate cycles. Keep the old fault/error text as append-only history; the newer verified terminal status supersedes it operationally.

## Regression tests

Test at least:

- exact retained prefix accepted;
- wrong device/candidate/count rejected;
- any UNKNOWN rejected;
- cleanup not verified rejected;
- evidence hash mutation rejected;
- pre-approach occurs once;
- first resumed forming attempt has no additional `+5`;
- completed sweeps are not replayed;
- active Z ceiling remains enforced.

## Verification

Before reporting continuation:

- recovery event is durably `COMPLETE`;
- retained forming indices appear once;
- next missing forming index is the first new electrical intent;
- pre-approach target and live readback match exactly;
- lights are off;
- `unknown=false`;
- candidate cycles remain zero until preparation completes.
