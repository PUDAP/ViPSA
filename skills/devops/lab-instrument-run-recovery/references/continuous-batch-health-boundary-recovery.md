# Continuous-batch health-boundary recovery

Use when a multi-cycle electrical batch finishes all candidate branches but the post-batch health read or its cleanup acknowledgement fails.

## Evidence-first classification

Separate candidate acquisition from the health boundary before deciding what to replay.

1. Verify the batch summary independently:
   - exact expected native point count;
   - all SET/RESET segments present;
   - one output-ON and one final output-OFF transition;
   - native source status ON for every measured candidate point;
   - output-after readback OFF.
2. Verify every candidate operation is `COMPLETE` in the permanent ledger.
3. Inspect the health operation itself:
   - **Measurement completed, cleanup acknowledgement lost:** a successful raw envelope and expected rows exist, but cleanup is unverified. Preserve the measurement. Reconcile only after later batch cleanup and a fresh independent OFF/open/error-free proof.
   - **Failed before hardware action:** no raw envelope, zero rows, and transport-connect/start evidence shows acquisition never began. Record the intent as zero-exposure rather than pretending the health measurement completed. Execute one fresh, separately identified replacement health read after safe-state recovery.
   - **Possible partial exposure:** any ambiguous dispatch or incomplete raw response remains `UNKNOWN`; do not retry without explicit authorization.
4. Never replay the completed candidate batch merely because its post-batch health operation failed.

## Edge recovery

For PUDA/NATS reconnect failures:

- Stop orchestration first.
- Map edge PIDs to their real working directories through `/proc/<pid>/cwd`; generic `main.py` process names are insufficient.
- Restart only affected edge owners. Preserve custom/deployed driver directories (for example, a protected SMU deployment) rather than silently replacing them with the workspace copy.
- Do not restart local NATS when the rig is configured for a remote cluster.
- Require each replacement edge to report fresh subscriptions plus `idle` and `run_id: null`.
- Then run harmless commands: output OFF, matrix `open_all`, output readback `0`, closed-channel readback `nil`, and instrument error query.

## Ledger reconciliation

- Hold the ledger lock and write atomically.
- Preserve the original cleanup/error payload under a reconciliation field.
- Record evidence paths and hashes for the terminal/batch cleanup and fresh independent safety proof.
- Clear the device UNKNOWN flag only after confirming no other UNKNOWN operations remain.
- Keep zero-exposure abandoned intents distinguishable from actual replacement health measurements.

## Finalization

A 100-cycle device may be classified as a right-censored survivor only after:

- all 100 SET/RESET cycles are complete;
- all required health boundaries are satisfied, including any separately identified replacement read;
- final OFF/open/error-free proof succeeds;
- recovery records are included in the aggregate manifest and optimizer acknowledgement.
