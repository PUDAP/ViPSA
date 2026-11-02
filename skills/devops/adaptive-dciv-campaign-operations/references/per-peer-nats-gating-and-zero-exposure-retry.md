# Per-peer NATS gating and append-only zero-exposure retry

## Why this gate exists

A multi-server NATS configuration can be partially partitioned: one peer may time out, another may show only part of the heartbeat set, and a third may still carry every command required for the next bounded operation. TCP connect and `machine list` are not sufficient health proofs.

## Validated recovery pattern

1. **Prove the failed attempt's boundary.** Decode the wire journal and require that the native stress command was never sent. Confirm no motion/stress dispatch, unchanged persisted pose, zero completed cycles, output OFF, matrix open, and no unresolved earlier UNKNOWN.
2. **Preserve the attempt.** Keep its claim and operation IDs as append-only `ZERO_EXPOSURE`, `zero_exposure=true`, non-counted records. Never delete or relabel it as a successful batch.
3. **Probe peers independently.** For each configured broker peer, use a bounded NATS/application request. TCP acceptance alone does not count. Treat heartbeat membership as advisory.
4. **Require one-peer completeness.** Through the candidate peer, directly verify every edge needed by the next operation: 2450 output OFF/errors/terminals/protected driver and capabilities, 707B open state and routing, exact Zaber readback when motion provenance matters, and the required light command. Read the authoritative persisted OpenFlexure state when that campaign uses it.
5. **Pin only the bounded operation.** If one peer passes the complete direct gate, pin the candidate batch and its mandatory post-batch health check to that peer. Re-evaluate peer suitability at later batch boundaries; do not make the pin a permanent deployment assumption.
6. **Retry with fresh identity.** Use fresh operation/run IDs while preserving the immutable candidate ID, full-precision recipe, recipe hash, preparation proof, physical-cycle boundary, and the prior zero-exposure history.
7. **Fail closed after dispatch.** If transport fails after the native stress command crosses dispatch, mark exposure UNKNOWN unless an exact complete retained native response can be independently reconciled. Never generalize a pre-dispatch retry rule to post-dispatch faults.

## Monitor correction

An all-machines-discovered monitor is too strict when discovery is incomplete but direct commands work. A bounded monitor may wait while no peer passes the direct gate, but it must not issue stress or motion. Retire it as soon as a peer passes the full operation-specific gate; do not make the operator ask why the campaign is still waiting on advisory discovery.

## Lifecycle ambiguity

A redelivered START can yield both `RUN_ID_MISMATCH` and success for the same run ID. Decode replies by machine/run/command/time and inspect process CWD plus parent trees before declaring duplicate edges. If one edge remains but run state is stale and the CLI reset endpoint is unavailable, restart only that affected edge, require idle/null state, and rerun the full direct safety gate.
