---
name: adaptive-dciv-campaign-operations
description: "Use for crash-safe adaptive multi-device DCIV campaigns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, dciv, campaign, recovery, ledger, plotting]
    related_skills: [vipsa-electrical-measurements, vipsa-grid-measurement, vipsa-machine-operations]
---

# Adaptive DCIV Campaign Operations

## Scope

Operate multi-device ViPSA campaigns that combine fixed forming/conditioning, externally generated candidate recipes, repeated SET/RESET cycles, permanent-ledger accounting, health reads, crash recovery, and live/final plots.

This skill governs campaign orchestration and recovery. Use the electrical-measurement skill for device physics and the grid/motion skills for navigation and alignment.

## Core rules

1. Validate preparation from both terminal records and the permanent ledger before requesting a recipe.
2. Never replay completed preparation or a completed SET/RESET branch.
3. Qualify frozen native arrays with output OFF before candidate stress.
4. Carry the completed-stress health counter forward from preparation.
5. Use one fresh process per full candidate cycle and compact only durably receipted COMPLETE payloads.
6. Reconcile post-acquisition failures from wire, ledger, native rows, energy, and cleanup evidence before deciding what remains missing.
7. Apply recipe-specific failure only after the minimum cycle count and configured consecutive-failure rule.
8. Treat hard-cap survivors as complete and right-censored, not failed.
9. Plot only full verified cycles. Label active-campaign figures as snapshots through an explicit cycle boundary.
10. Verify output OFF, matrix nil, no unresolved operations, and cleanup before reporting a stop or advancing devices.
11. An explicitly authorized quarantine-and-finish closure is administrative, not a successful measurement or safety reconciliation. Keep original uncertain-exposure operations and device `unknown=true` intact. A later batch may be reconciled as COMPLETE zero-exposure/non-counted only from its exact wire error, OFF preproofs, matched deployed-source hash and demonstrated guard-before-INIT ordering; preserve each original UNKNOWN entry in `unknown_history`. Exclude those COMPLETE entries from verified-cycle counts and scientific observations using explicit non-counted/zero-exposure flags.
12. At administrative campaign closure, compare the actual `devices_consumed` keys, matched completions and scientific records against the requested device range; `initial_cursor=50` does not prove 50 matched devices or successful measurements. Preserve and explicitly report pre-existing bookkeeping gaps rather than silently fabricating consumption/completions. Back up state, hold existing owner/ledger/runner/handshake locks, write manifests and verify the exact targets. Leave continuation paused and do not dispatch the next device. Label saved final cleanup evidence as historical when no fresh hardware readback was performed.
13. For Keithley 2450 fixed current ranges, program the smallest supported native decade range that is **not below** the requested measurement range (10 nA through 1 A), while preserving the exact requested compliance. Never weaken the readback guard to accept a native range below the request. Test boundary cases such as a 10.363149 mA request mapping to the 100 mA range, reload only the affected edge, and verify the loaded code hash plus OFF/open/error state before stress.

## Detailed workflow

For a newly authorized batch whose old launchers contain hard-coded device/pose/point-count assumptions, use `references/fresh-manifest-driven-grid-batch-executor.md`: fresh durable modules, real constructor preflight before motion, single shared owner, camera-reviewed alignment, native-timeline energy partition, and latched failure/no-replay supervision.

See `references/crash-safe-adaptive-dciv-campaigns.md` for:

- preparation-to-optimizer handoff;
- exact native output-OFF proof semantics;
- 2450 six-digit versus stored seven-digit/binary32 representation checks;
- bounded-memory one-cycle controllers and ledger compaction;
- completed-branch receipt reconstruction and no-replay recovery;
- recipe-failure versus right-censored hard-cap stopping;
- race-safe live snapshot and final plotting requirements.

## User-facing behavior

For an authorized automatic screen, continue across devices after each verified terminal state rather than treating one device's stop as the campaign stop. Pause only for an unresolved safety/control/science gate. When asked for plots during a live run, immediately produce a completed-cycle snapshot and state its frozen boundary; regenerate a final plot after the terminal stop.
