# Direct-NATS duplicate subscriber run-state recovery

Use this when protocol/direct control after an outage shows inconsistent PUDA run state: machine state may be `idle`/`run_id: null`, `START` returns success, but the following queued driver command returns `RUN_ID_MISMATCH` / `expected active run`.

## Interpretation

This is a control-path/run-state issue, usually consistent with duplicate or stale edge subscribers after a network/edge disruption. Do not interpret it as a physical device failure or electrical measurement result.

## Recovery pattern

1. Inspect live machine state for the affected six-machine ViPSA set.
2. If any machine exposes a non-null `run_id`, publish/execute `complete` for that exact run ID or use `puda machine reset <machine_id>` when appropriate.
3. Run conservative cleanup:
   - Keithley output off.
   - Keysight output off.
   - 707B `open_all`, then `get_closed_channels`; expected safe result is `nil`.
   - Light off/initialize off if needed.
4. For direct-NATS fallback after the cleanup, prefer **short per-command transactions** instead of one long shared run ID:
   - fresh UUID run ID
   - `start`
   - one queued driver command
   - `complete`
5. If `start` fails with `cannot start, <old-run-id> is currently running`, complete the old run ID and retry.
6. If the queued command fails with `RUN_ID_MISMATCH` or `expected active run`, retry the whole transaction with a fresh run ID. Do not keep sending commands under the mismatched run ID.
7. Bound each retry attempt for fast machines (stage/light/zaber/707B) so the control loop can detect a hung transaction and cleanup instead of blocking the whole experiment for many minutes.

## Reporting

Report this as `PUDA run-state/control-path recovery` and include verified final safety state. Avoid claiming that a failed queued command physically executed unless its response status is `success` and any needed readback verifies the effect.
