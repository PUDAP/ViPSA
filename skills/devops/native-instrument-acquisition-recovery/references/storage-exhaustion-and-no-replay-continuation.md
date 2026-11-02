# Storage exhaustion: preserve exposure and resume the exact missing boundary

## Failure mechanism

An acquisition controller can finish native operations but fail while persisting a journal. Its saved status, UNKNOWN flag and cleanup flag may all be stale. In the observed implementation, `safe()` saved `cleanup_verified=False` before sending OFF/open, so ENOSPC in the finalizer prevented cleanup commands entirely. A Python process exit or entry into `finally` did not establish electrical safety.

## Exercised recovery sequence

1. Inspect surviving acquisition processes before taking ownership. Independently command output OFF and matrix open; require successful output `0`, channels `nil`, error queue empty and real mechanical readbacks. Do not move the stage to compensate for missing controller state.
2. If the normal evidence disk cannot accept writes, use an explicitly identified available filesystem for the emergency command journal. Temporary-memory evidence is not a durable archive: copy and verify it on persistent storage once space is available. Discover exact native command parameters; the direct navigation transport's Zaber query required `units: null`, while a higher-level wrapper supplied this automatically.
3. Restore storage without discarding scientific evidence. Only delete media within the user's authorized scope; retain metadata, databases, claims, native request/reply files and raw CSV data. Before deletion, save path, size and SHA-256. Lossless compression of derived CSVs is another option: compare the decompressed stream hash with the original before retiring an uncompressed duplicate.
4. Inspect pin manifests BEFORE deleting rendered media. Historical validators may pin plots as well as executable/data sources. Authorized deletion can otherwise block future imports. A retirement manifest does not restore the original bytes and must not become a generic missing-file/hash waiver. Any additive retirement contract must be confined to explicitly authorized media paths with matching historical digests; native receipts, code and CSV dependencies must remain strict. Prefer a designed retirement contract over ad hoc loader edits.
5. Audit every saved electrical/control receipt and all native START/command/COMPLETE exchanges, binding command, parameters, run ID, response success and exact raw bytes. Reject duplicate IDs, extra/unreturned wire directories and unjournaled electrical exposure. Reconstruct pose changes, first forming qualification, preparation order, complete candidate cycles, metrics and cumulative measured energy.
6. In this case, 50 candidate cycles were complete. The last saved INTENT was a harmless position readback whose raw reply and lifecycle were complete. The due cycle50 health operation had no route/acquisition dispatch. Reconcile that readback in an additive assessment; preserve the original journal unchanged. Do not classify the entire interruption as zero exposure.
7. Create a separate continuation output and durable claim. Bind the immutable source journal, recipe/compiler digest, native evidence inventory, original claims, current navigation completion, inherited cycles/failure state/energy and exact landed pose. Start with the outstanding health operation, then only cycles51 onward up to the original cap. Never repeat preapproach, forming, preparation, completed cycles or motion.
8. Obtain fresh owned OFF/open/error/pose/driver/sole-edge checks. Continuation readiness must explicitly describe an already-stressed device; do not present a copied `fresh_unstressed=true` context as evidence. Preserve the full readiness receipt and use an isolated validator/worker namespace, not edits to historical modules.
9. Narrow the backend to exact remaining electrical operation keys and parameters plus harmless controls. Reject motion, explicit output-ON, forming/preparation identities, stale readiness, reused output/claims and duplicate acquisition keys. Check free-space reserve before every new acquisition and ensure cleanup itself can still be journaled.

## Verification actually reached

A retained fixture outside the production tree exercised the unchanged native transport with a fake connector and a recorded healthy health-row payload, proving the due health operation advances exactly once while inherited cycles remain50. Duplicate acquisition, motion, forming and stale readiness were rejected. Fixture write guards were relocated only in isolated test function globals.

The live continuation then passed fresh readiness and the due cycle50 health check, and dispatched cycles51–60 with `RUNNING_CONTINUATION` and `unknown=false`. This establishes a tested resume boundary, not proof that the whole campaign or cap100 completed.

## Reporting and orchestration lessons

State completed exposure, what remains uncertain, independently verified cleanup, and the actual resumed phase/run ID. A spawned process is not an acquisition receipt. Do not let a stale offline-only child restriction create a self-handoff when the parent is the authorized hardware owner. Existing continuous-campaign authorization does not require repeated permission requests, but never overrides uncertainty, no-replay or hardware safety gates.
