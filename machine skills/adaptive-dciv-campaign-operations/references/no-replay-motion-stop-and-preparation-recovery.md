# No-replay motion, STOP, and preparation recovery

Use this note when a long adaptive DCIV campaign is interrupted between device transitions or during forming/conditioning.

## Preserve completed motion and preparation

- A completed retract, alignment correction, pre-approach, or forming `Z+5` increment is durable evidence; never rerun it as setup.
- Reconcile receipts and the permanent ledger, require zero UNKNOWN electrical operations, and reconstruct completed forming/conditioning counts plus the health counter.
- Verify fresh output OFF, matrix nil, empty errors, terminals, and exact Stage/Zaber pose.
- Resume at the next missing operation only.

## Resolve stale holds from structured evidence

A hold record can retain an early timeout reason while later fields contain successful OFF/open/error/pose readbacks. Compare timestamps and structured responses, then perform a fresh gate before new stress. Do not let stale prose override newer verified state.

## STOP sentinel lifecycle

Inspect a STOP file before honoring or clearing it. Never clear a fresh operator stop or unresolved safety hold. If it encodes a superseded control hold that the user explicitly resolved and all referenced gates now pass, archive it as an audit artifact and clear the active sentinel. A preflight exit caused by that stale STOP proves no hardware command was dispatched; fix the sentinel and rerun the same no-replay recovery.

## Explicit quarantine-and-advance

When post-dispatch UNKNOWN exposure cannot be resolved, an explicit user instruction to finish later candidates may authorize quarantine-and-advance. Record the affected device as infrastructure-fault/incomplete with only verified cycles, retain UNKNOWN intents, exclude them from scientific observations, verify fresh hardware safety, and advance without replay. Do not silently extend the override to unrelated later faults.
