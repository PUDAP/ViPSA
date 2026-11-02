# BO batch rebinding, counters, and crash-safe continuation

Use these rules when applying an optimizer-proposed batch to a corrected physical traversal or when a continuous batch loses its client connection.

## Recipe-to-device binding

- Keep the optimizer’s recipe order, candidate IDs, request IDs, full-precision parameters, and source hashes immutable.
- Bind recipe index 1..N to the operator-approved physical traversal 1..N. Do not infer numeric device order from an old handoff when the operator corrected the serpentine order.
- Store a versioned binding manifest with source recipe, physical device, absolute nominal target, candidate/request IDs, source semantic hash, and execution-binding hash.
- Preparation/forming/conditioning are not candidate cycles and must not increment endurance counters.

## Forming and alignment semantics

- “Three consecutive forming signals” means three consecutive qualifying current points in one outbound forming sweep—not three forming sweeps.
- Stop forming on the first sweep that satisfies the outbound criterion; move Z only between failed attempts, with each motion durably journaled.
- Optical alignment may intentionally offset the final XY from the nominal grid coordinate. Validate nominal-target provenance, fresh Camera-1 evidence, aligned pose, and residual ≤ gate; do not require aligned XY to equal nominal XY.
- Record the +85 pre-approach as a separate durable operation after alignment. It does not establish physical contact.

## Candidate and health counters

Maintain separate fields:

- `physical_cycle`: every dispatched slot, including later UNKNOWN ranges;
- `verified_ordinal`: increments only after a complete SET+RESET cycle with native evidence;
- `completed_full_cycles`: count of verified ordinals, used for the 200-cycle cap;
- `unknown_history`: immutable physical ranges and branch IDs;
- zero-exposure administrative attempts: preserved but consume neither physical slots nor verified ordinals.

Health reads occur after each complete ten-cycle candidate batch but are telemetry. The recipe failure criterion is computed from consecutive **candidate-cycle** metrics, not consecutive health results.

## Post-dispatch transport loss

1. Latch the exact physical range and branch operation IDs UNKNOWN immediately.
2. Stop/retire all parent and child controllers before retry logic can run.
3. Search edge logs for a response matching the original run ID and exact command. If complete native evidence exists, reconcile it without replay (see `native-instrument-acquisition-recovery/references/post-dispatch-response-reconciliation.md`).
4. If no completion proof exists, obtain independent OFF/open/errors/pose proof and continue only with new physical labels while retaining verified ordinals.
5. A pre-dispatch owner-lock failure is proven zero exposure: do not consume physical labels and do not let it hide an earlier dispatched operation.

## Executor review pitfalls

Offline tests can be green while encoding wrong science. Review tests against campaign semantics, especially:

- points-within-sweep versus sweeps;
- physical labels versus verified ordinals;
- candidate-cycle failures versus health signals;
- nominal XY versus optically aligned XY;
- existing COMPLETE receipts must be revalidated before reuse;
- one owner lock must cover the entire live controller scope.
