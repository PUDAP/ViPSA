# Reconciliation, OOM Safety, Short Lists, and Split-Run Plots

## Kill-window classification

Reconcile one exact operation identity across:

1. local intent artifact;
2. permanent exposure ledger;
3. native wire request/reply;
4. fresh hardware cleanup/readback.

Classify:

- **Ledger COMPLETE:** reuse; never replay.
- **Native success, ledger missing:** bind the exact reply to the frozen command, verify rows/order/timing, compute energy once, verify cleanup, and create one reconciled COMPLETE receipt.
- **Intent only, no native request and no ledger entry:** record `undispatched=true`, `zero_exposure=true`; do not add a fake exposure entry; execute later with a new operation ID.
- **Rejected before output enable:** preserve the error and output-before proof, record zero exposure, fix the cause, rerun OFF-only proof, and execute only the missing branch.
- **Ambiguous/partial:** retain UNKNOWN and stop.

If SET completed and RESET did not dispatch, resume RESET only. Restore sweep count, completed cycles, periodic health cadence, failure-monitor history, recipe hash, and hard cap.

## Short native lists

Buffer capacity is not stimulus length. For a Keithley 2450 list with fewer than ten points:

```python
buffer_capacity = max(10, len(voltage_values))
```

Keep `voltage_values` unchanged and require exactly its original length in the returned ordered trace. Never pad the waveform with repeated safe-bias points. Regression-test short and normal lists and rerun output-OFF native proof before stress.

## OOM-safe permanent ledgers

Repeated full-JSON load/copy/save can exceed a memory cgroup when raw envelopes and native-integrity blocks are duplicated.

1. Confirm OOM from kernel/cgroup evidence; do not call it a device or instrument fault.
2. Reconcile the last electrical boundary before changing storage.
3. Create an exact compressed ledger archive and SHA-256 hashes of source and archive.
4. Compact only COMPLETE operations.
5. Retain operation ID, state, phase, spec/settings, timestamps, trace/cumulative energy, cleanup, device totals, and reconciliation metadata.
6. Externalize `raw_envelope`, `available_rows`, and `rows` to the exact archive or a uniquely hashed native receipt file; preserve row counts and canonical payload hashes.
7. Verify parseability, operation count, state counts, and device totals before atomic replacement.
8. Run one cycle per fresh process if in-memory receipt growth is also a problem.
9. Incrementally compact newly COMPLETE operations after each cycle. Never compact UNKNOWN entries.

## Split-run and corrected-run plotting

- Aggregate durable per-branch receipt files; do not trust lagging aggregate progress alone.
- Deduplicate operation IDs and require both positive and negative branches before counting a cycle.
- Assert contiguous completed cycles programmatically.
- Preserve commanded-voltage/native-row order.
- Use `Vcmd` versus `log|Imeas|`, one color per cycle, PF/PB/NF/NB line styles, and a cycle colorbar.
- Use logarithmic contrast axis when outliers hide later cycles.
- For contact correction, plot original forming/conditioning plus distinct reconditioning; candidate plot should use the fresh corrected run and exclude superseded pre-correction cycles.
- Save PNG, native-point CSV, contrast CSV, and provenance in the device dataset folder.
- Label live output as a snapshot; regenerate after the terminal cycle.
- Visually inspect a contact sheet before delivery.

## Auto-progress checkpoints

When automatic next-device progression is already authorized, cleanup, retract, absolute travel, alignment, and pre-approach are checkpoints. Continue to the next safe prerequisite and launch preparation when gates pass. Do not report that the campaign stopped at the previous device merely because the next alignment gate had not yet been completed. Stop only for explicit operator stop, unresolved exposure, or a real safety/control/science blocker.
