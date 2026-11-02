# Authorized Z-ceiling retained-prefix preparation recovery

Use when a campaign preparation stops at a software Z ceiling after one or more forming sweeps are permanently COMPLETE, and the operator explicitly authorizes a higher numeric ceiling.

## Recovery contract

1. Pause autonomous continuation before inspecting or editing the recovery path.
2. Freeze a versioned authorization artifact with the exact old/new ceiling, scope, device, current verified pose, retained forming/conditioning counts, and `automatic_replay: false`.
3. Preserve the pre-authorization preparation terminal, ledger, latest pointer, and supervisor as append-only backups.
4. Reconcile the retained prefix:
   - every latest operation state is `COMPLETE`;
   - device/preparation `unknown` is false;
   - cleanup proves output `0`, matrix `nil`, and empty errors;
   - live/tracked pose equals the last completed motion readback;
   - no candidate ledger exists unless preparation had already completed.
5. Implement an exact recovery gate, not a generic “retry failed preparation” path. Require the expected device, error label, sweep counts, pose, authorization hash, and no unresolved operations.
6. Resume at the first missing forming attempt. Never repeat pre-approach, completed Z increments, completed forming sweeps, health reads, or conditioning sweeps.
7. If the normal increment would cross the authorized ceiling, use `min(normal_increment, ceiling-current_z)` so the last move lands exactly on the ceiling. Require a positive remaining distance before dispatch; never round past the bound.
8. After a sweep at the ceiling:
   - if forming passes, continue conditioning with no additional forward Z motion;
   - if it fails, stop before another sweep and request a new operator decision (higher bound, preparation failure/skip, or campaign stop).
9. Run offline tests before hardware: exact-prefix acceptance, wrong-device rejection, UNKNOWN rejection, changed-count/pose rejection, successful partial final step, and no-replay behavior.

## Edge/lifecycle recovery during the preflight

A recovery worker must reacquire the global owner and freshly verify OFF/open/errors, protected driver identity, terminals, and exact Stage/Zaber pose before motion. If a harmless getter times out during START/COMPLETE:

- prove the preparation ledger was not changed and no motion/stress was dispatched;
- inspect the wire record and exact run ID;
- reset only a non-Stage machine state when appropriate;
- never call `puda machine reset stage`, because it redefines logical zero;
- if a local edge process is absent, start exactly one canonical edge from its known deployment directory and verify it consumes the retained COMPLETE and returns `idle / run_id=None`;
- verify Stage startup preserves the confirmed persisted coordinates and pending state;
- start missing Zaber/light/matrix edges before repeating the full preflight, avoiding serial zero-exposure failures.

Transient edge absence is not itself a reusable environment claim. The durable lesson is targeted single-edge restoration plus exact retained-run reconciliation, followed by a fresh full gate.

## Reporting

Report retained versus newly executed sweeps, exact Z sequence, forming-attempt result, replay count (must be zero), UNKNOWN state, cleanup proof, active worker, and whether autonomous continuation is paused or enabled. Do not call optical alignment contact and do not count preparation sweeps as candidate cycles.
