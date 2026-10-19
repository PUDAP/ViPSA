# Authorized preparation Z-cap extension with retained-prefix recovery

Use when a guarded ViPSA preparation stops at a software Z ceiling, the operator explicitly raises that ceiling, and completed forming/conditioning sweeps must be preserved without replay.

## Authorization and immutable history

1. Record a versioned authorization artifact containing the verbatim operator permission, old/new Z ceilings, batch/device scope, retained counts, exact verified pose, next missing operation, and `automatic_replay: false`.
2. Hash the authorization and make the recovery executor require that exact hash and semantic fields.
3. Preserve the original preparation terminal, ledger, latest pointer, and supervisor record as `*-before-<authorization>-resume.json` artifacts. Do not erase the original fault.
4. Keep recipe/proposal files immutable; a motion-envelope exception is separate from recipe parameters.

## Exact retained-prefix gate

Permit recovery only when all of the following match the authorization:

- fault reason is exactly the prior software Z-ceiling rejection;
- `unknown == false` and prior cleanup is verified;
- completed forming/conditioning/health counts match the retained prefix;
- the latest state for every operation ID is `COMPLETE`;
- the last completed motion readback and tracked Stage state match the authorized resume pose;
- the next missing operation is explicit.

For example, if forming attempts 1–3 and moves through `Z=248` are complete, resume attempt 4 with one guarded `Z+5 -> 253`. Do not repeat pre-approach, attempts 1–3, or their moves.

## Implementation pattern

- Add a narrowly scoped recovery-state validator separate from normal fresh preparation.
- Before any live action, regression-test exact-prefix acceptance plus rejection of UNKNOWN, wrong counts, wrong device, wrong fault, changed authorization bytes, and wrong pose.
- A fresh preparation can use the newly authorized upper bound only after the authorization verifier passes.
- A previously completed or unrelated faulted preparation must still refuse replay.
- The supervisor may call preparation recovery only when `preparation-latest` is not complete; the recovery validator decides whether that state is admissible.
- Append a durable `recovery: COMPLETE` event before the first new move, linking authorization hash, retained counts, resume pose, and next missing attempt.

## Preflight faults are not preparation replay

A recovery worker may fail before writing its recovery event because a harmless OFF/open/pose getter cannot complete its PUDA lifecycle. Classify this as zero new motion/stress only from the wire chronology and unchanged retained ledger/Stage state—not from the exception text alone.

If a required local edge process is absent:

1. Confirm no duplicate process by PID, executable, CWD, and `main.py` argv.
2. Start exactly one canonical edge process from its machine directory and project virtual environment.
3. For ordinary electrical edges, allow the new edge to consume the exact retained COMPLETE and require `idle / run_id=None` afterward.
4. **Never `puda machine reset stage`**: Stage reset redefines logical zero. Restart exactly one Stage edge only when absent; verify that it consumes the retained getter COMPLETE and republishes the same confirmed tracked position.
5. Check all other required local edges before retrying, because a shared gateway/process teardown can leave several absent and otherwise cause serial preflight failures.
6. Retry only the zero-exposure preflight. The retained preparation prefix and next missing operation remain unchanged.

## Verification after recovery begins

Before declaring continuation active, verify from the permanent ledger and tracked Stage file that:

- the recovery event is COMPLETE;
- forming intent indexes contain the old prefix exactly once and then the next attempt;
- the first new completed move starts at the authorized resume pose;
- completed sweep counters increased only for newly acquired sweeps;
- no prior operation was replayed;
- `unknown == false`;
- live Stage Z remains within the newly authorized ceiling.

Keep autonomous next-device continuation paused during reconciliation and edge repair. Re-enable it only after a single recovery worker is alive and the scheduler is guaranteed to remain read-only while that worker runs.
