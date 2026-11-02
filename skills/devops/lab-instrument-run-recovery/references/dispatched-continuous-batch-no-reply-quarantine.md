# Dispatched continuous batch with no native reply

Use this pattern when a continuous Keithley batch command was sent, the NATS connection closed, and no native result envelope returned.

## Classification

- A recorded command intent followed by no measurement reply is **not** zero exposure.
- Zero rows, no receipt files, and an empty normalized result do not prove the instrument never executed.
- Preserve every planned branch as `UNKNOWN`; do not count the cycles and do not replay them.
- A later `RUN_ID_MISMATCH` identifying the original active run strengthens the possible-exposure classification rather than clearing it.

## Recovery sequence

1. Stop autonomous scheduling for the affected continuation.
2. Preserve terminal, progress, frozen recipe, execution claim, and the complete wire journal.
3. Decode `raw_b64` wire envelopes programmatically. Confirm whether the measurement command has an intent and whether any matching native reply exists.
4. Verify the matrix independently. A successful `open_all` plus explicit `get_closed_channels == nil` proves matrix state only; it does not prove SMU output state or zero exposure.
5. If the Keithley edge reports stale active-run state, reset only that PUDA machine state. Do not restart NATS.
6. Issue explicit output OFF, matrix open, output readback, matrix readback, and error query. Require real success/readback before further motion or measurement.
7. Keep the affected device's UNKNOWN flag and branch intents permanent when exposure cannot be resolved.
8. Quarantine the device at its last verified cycle boundary. Plot and report only complete nonsuperseded cycles.
9. Continue the broader campaign only after hardware safety is verified, using a fresh device; never replay the ambiguous batch.

## Optimizer/runner bookkeeping

When quarantining an initial-design device:

- acknowledge the result as `infrastructure_unknown_exposure`, not a recipe/device failure;
- set scientific-training acceptance false;
- preserve verified cycle, native-point, and health-check totals separately from UNKNOWN intents;
- append a handshake-history acknowledgement and clear the active handshake atomically with clearing runner pending state and advancing the sequential design cursor;
- record `eligible_for_next_proposal=true` only after hardware safety is verified;
- retain `prior_UNKNOWN_preserved=true`.

## Verified evidence shape

A defensible quarantine record includes:

- exact last verified cycle;
- complete branch and native-point counts before the fault;
- number of UNKNOWN planned branches;
- wire proof: command intent exists, matching native result absent;
- explicit final output `0`, matrix `nil`, and empty instrument error list;
- partial plot/CSV labeled with verified cycles only;
- a statement that the ambiguous batch was neither counted nor replayed.
