# Scheduler and edge-state recovery during adaptive DCIV campaigns

Use this when a transport or PUDA state fault leaves cleanup, exposure, or pose uncertain during a multi-device campaign.

## Verified sequence

1. Pause the autonomous campaign scheduler before recovery so no second controller can race the ledger or hardware.
2. Inventory the interrupted terminal, wire evidence, and permanent ledger. Retain every COMPLETE operation with native rows; never replay it merely because the controller ended in `fault`.
3. Fail closed when OFF/open readback is missing, even if part of cleanup succeeded.
4. For edge-local `RUN_ID_MISMATCH`, keep NATS running. Confirm edge visibility/log output, reset only the affected machine state, then issue fresh harmless cleanup/readback commands.
5. Require fresh SMU output `0`, matrix `nil`, and empty instrument errors before continuation.
6. Read live stage and coarse-stage pose. Do not derive pose from completed sweep count: the next attempt's guarded move may have landed before its electrical sweep began.
7. If the move landed but the sweep has no receipt/rows, resume that same attempt at the live pose and skip its move. Apply the normal increment only on later attempts.
8. Seed the continuation with retained operation IDs, receipts, completed-sweep count, and health counter; use a fresh execution ID for new work.
9. A recovery attempt that stops before motion or acquisition (for example, a fresh-pose mismatch) is diagnostic only. Do not count it as a sweep, branch, health check, or zero-exposure electrical intent.
10. Resume autonomous scheduling only after retained prefix, live pose, permanent ledger, cleanup, and device UNKNOWN state agree.

## Campaign semantics

- A safety pause is a recovery gate, not campaign termination.
- Continue across recipe-specific device failures once their terminal state and cleanup are verified.
- Preserve exact traversal order and advance the optimizer cursor by design-row count, which may differ from the physical device number when traversal jumps (for example `30 → 40`).
