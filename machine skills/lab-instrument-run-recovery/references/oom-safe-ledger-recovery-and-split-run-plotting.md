# OOM-safe ledger recovery and split-run plotting

## When to use

Use when a long-running instrument campaign is externally killed, its active JSON ledger becomes too large for the process memory limit, or completed cycles span multiple controller executions.

## Reconcile before resuming

1. Treat `SIGKILL`, timeout, or transport loss as an uncertain boundary until intent, permanent ledger, and native wire journal agree.
2. Never infer completion from aggregate `progress.json` alone; it can lag a durable receipt.
3. Classify the last operation:
   - **COMPLETE:** matching successful native reply, exact expected row count, energy charged once, and OFF/open cleanup.
   - **UNDISPATCHED / zero exposure:** local intent may exist, but there is no matching native sweep request and no ledger entry; require fresh output `0`, matrix `nil`, and empty error queue.
   - **UNKNOWN:** evidence is insufficient; stop rather than replay.
4. Resume only at the first proven-undispatched branch. Reuse completed SET/RESET and health receipts without replay.
5. Rebuild failure-monitor history from per-cycle metric files before continuing.

## Diagnose repeated exit -9

Check the kernel journal. If it identifies a memory-cgroup OOM kill, do not label the event an instrument or recipe fault. Identify the active ledger size and the process memory limit.

## Preserve then compact oversized ledgers

1. Create an exact compressed archive of the active ledger before changing it.
2. Record SHA-256 hashes of the source ledger and compressed archive.
3. Compact only `COMPLETE` operations.
4. Preserve operation IDs, state, phase, specification/settings, timestamps, energy/cumulative accounting, cleanup proof, and device totals.
5. Externalize bulky `raw_envelope`, `available_rows`, and `rows` payloads to either:
   - the exact hashed pre-compaction archive; or
   - a unique native receipt file with a verified hash.
6. Store archive/receipt paths, hashes, original item counts, and per-payload canonical hashes in the active ledger.
7. Verify parseability, operation count, state counts, and device totals before atomic replacement.
8. For continued acquisition, run one cycle per fresh process and compact newly COMPLETE operations after each cycle. If killed during a cycle, return to reconciliation rather than replaying.

## Plotting corrected and split executions

- Deliver PNG plots; save native-point and metric CSVs beside them.
- Preparation plot: forming and conditioning on `Vcmd` versus `log|Imeas|`, colored by sweep order.
- Show post-contact-correction reconditioning distinctly.
- Candidate plot: include only cycles with both positive and negative branches. Use PF solid, PB dashed, NF dotted, NB dash-dot and a cycle colorbar.
- Combine split executions by campaign cycle and deduplicate operation IDs.
- Exclude superseded pre-correction cycles when the corrected run restarted at cycle 1.
- Use a logarithmic contrast axis when large outliers make later cycles unreadable.
- Label active-device output as a snapshot with the highest fully completed cycle.
- Verify all declared counts programmatically and inspect a contact sheet before delivery.
