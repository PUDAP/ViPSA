---
name: instrument-campaign-resilience
description: "Use for crash-safe long instrument campaigns."
version: 1.0.0
metadata:
  hermes:
    tags: [lab-automation, campaign, recovery, provenance, ledger, plotting]
    related_skills: [lab-instrument-run-recovery, vipsa-electrical-measurements]
---

# Instrument Campaign Resilience

Use this class-level skill for long, multi-operation laboratory campaigns that must survive process termination, OOM kills, controller handoffs, split executions, contact corrections, or large durable ledgers without replaying stress or losing provenance.

## Core invariants

1. Process state is not exposure truth. Reconcile local intent, permanent ledger, native wire request/reply, and fresh cleanup readback.
2. Never replay a completed or possibly exposed operation.
3. Resume only at an operation proven undispatched/zero exposure, or after reconstructing an exact successful native reply once.
4. Charge measured energy exactly once and preserve health/failure counters across controllers.
5. Archive before compaction; compact only COMPLETE payloads; retain identifiers, state, energy, cleanup, hashes, and recoverable native receipts.
6. Candidate plots contain only fully completed cycles and preserve native acquisition order.
7. An approved auto-progress campaign continues through next-device checkpoints unless a real blocker or operator stop occurs.

## Workflow

1. Freeze retries and inventory artifacts.
2. Classify the last operation from durable evidence.
3. Force and verify output-off/matrix-open/error-free state.
4. Reconcile missing progress or ledger commits without fabricating exposure.
5. Diagnose repeated `-9` from kernel/cgroup evidence before changing instrument logic.
6. If ledger size causes OOM, create a hashed exact archive, atomically compact COMPLETE payloads, and switch to bounded fresh processes.
7. Rebuild controller state from saved metrics and receipts.
8. Generate split-run plots from durable per-operation receipts; assert full contiguous cycles.
9. Verify final cleanup, counts, and artifacts before reporting.

## Reference

- `references/reconciliation-oom-short-lists-and-split-plots.md` — durable kill-window classification, short-list buffer capacity, OOM-safe ledger compaction, one-cycle processes, corrected-run plotting, and auto-progress checkpoints.

## Verification checklist

- [ ] Intent/ledger/wire evidence agrees on the resume boundary.
- [ ] Output off, matrix open, and errors empty before continuation.
- [ ] Completed stress and energy are not replayed or double charged.
- [ ] Exact pre-compaction archive and hashes exist.
- [ ] UNKNOWN operations were not compacted or silently cleared.
- [ ] Fresh controller preserves recipe, cycle, health cadence, failure history, and hard cap.
- [ ] Plots include only complete cycles and retain native CSV/provenance.
- [ ] Approved next-device progression remains active unless genuinely blocked.
