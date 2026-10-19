# No-replay quarantine, delivery ordering, and before-INIT recovery

## Routine motion gates versus exceptional clearance

Do not add a camera-based vertical-clearance prerequisite in the middle of an established campaign when the standard retract has:

- a durable COMPLETE motion edge;
- an exact fresh Stage-Z readback; and
- fresh Keithley-output-OFF plus matrix-open verification.

Use side/oblique clearance imaging only when there is an independent reason for uncertainty: a changed retract, stale/missing Z readback, scratch or collision evidence, suspected over-contact, or an explicit operator request. Camera 2 is qualitative, not a micrometre Z sensor. Never repeat a completed retract solely to satisfy a newly introduced image gate.

## Delivery-gated optimizer handshakes

When optimizer ingestion requires proof that a plot/report was actually delivered, a cron agent cannot truthfully acknowledge delivery before its final response is sent.

1. Complete and verify the device result.
2. Save terminal, raw, cleanup, plot, and continuation-handoff manifests.
3. Leave the handshake pending without replay.
4. Deliver the final response and attachments.
5. On the next invocation, verify prior delivery context and acknowledge the exact saved result.
6. Only then permit next-device travel.

Never fabricate a delivery handle early merely to advance the cursor.

## Scheduler timeout with a detached supervisor

A scheduler's in-flight guard may expire while a child device supervisor continues. Treat the scheduler error as an orchestration event, not as proof that acquisition failed.

- Inspect live process ownership and device artifacts.
- If a controller/supervisor is active, do not duplicate or restart it.
- Let it reach a terminal batch/device record.
- Reconcile from saved terminals, ledger, and cleanup evidence.

## Quarantining an uncertain batch

A dispatched batch with uncertain exposure must never be replayed. If the user explicitly authorizes quarantine-and-advance:

- preserve every UNKNOWN intent and its evidence;
- mark the batch scientifically unusable and non-counted;
- resume only at the next non-overlapping cycle labels;
- count only newly verified complete SET+RESET pairs;
- retain physical-stress uncertainty in final classification;
- never use quarantined operations as optimizer observations.

Quarantine authorization is scoped: it does not automatically apply to a later independent fault.

## Before-INIT native faults

A trigger-model configuration/readback fault can be reconciled as zero exposure only when all of the following are proven from saved evidence:

- `complete == false`;
- `segments == []`;
- `output_transitions == {"on": 0, "off_after_on": 0}`;
- all native preproofs are verified with output OFF before and after;
- the proof's deployed-driver hash matches the inspected source; and
- source ordering proves the raised guard occurs before the relevant `:INIT`.

Then:

1. Back up the permanent ledger.
2. Preserve each intent under `unknown_history`.
3. Reconcile only those intents as COMPLETE with zero energy and `candidate_cycle_counted=false`.
4. Clear device UNKNOWN only if no other unresolved intents remain.
5. Keep the recovery record and hashes durable.

Do not apply this rule to transport timeouts after dispatch merely because final cleanup is safe; output OFF afterward does not prove zero prior exposure.

## Precision/readback debugging

For segment-parameter mismatch, capture expected and actual compliance, current range, and NPLC in the error evidence before raising. Compare against documented instrument storage/query precision and supported fixed-range grids. Do not weaken the guard or change an optimizer recipe speculatively. A diagnostic configuration-only rerun is acceptable only when output remains OFF and the guard is independently proven to precede `:INIT`.
