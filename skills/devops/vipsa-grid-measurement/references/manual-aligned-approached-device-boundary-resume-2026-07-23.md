# Resume an S1 grid from a manually aligned/approached named device (2026-07-23)

## Use case

The user explicitly chooses a named device as the new continuation boundary after manually moving to its absolute S1 grid coordinate, aligning it, and running a standalone approach. The active run may contain completed devices before the boundary and may have no active folder for the selected device.

## Correct continuation pattern

1. Treat the named device as authoritative; do not replace it with the first missing or first incomplete device.
2. Verify the selected device's nominal target in S1 `grid_positions.csv` and live handoff readbacks:
   - nominal grid target before alignment,
   - live post-alignment Zaber coordinate,
   - final standalone approach Z,
   - alignment and approach artifact paths.
3. Inspect the active run folder before modification:
   - preserve valid completed devices before the requested traversal boundary,
   - deduplicate old partial-summary entries by `device_number`,
   - archive an existing boundary/later device folder only if one actually exists,
   - do not claim archival when there was nothing to archive.
4. Compute `remaining` from the run's actual serpentine list and slice at the exact boundary index. Record the complete remaining traversal order and explicitly record which numeric devices are intentionally not backfilled.
5. For the first resumed device, do **not** repeat lateral motion, alignment, or approach. Save a handoff record and copy/normalize the standalone alignment/approach results into the device summary and `approach.json`.
6. Run a fresh low-stress post-approach health check. A pA final approach read can still be followed by measurable, voltage-responsive health data; classify from the fresh multi-bias result rather than the single final trim read.
7. Continue the established DCIV/pulse policy. If the campaign has an explicit no-skip override, keep gates as record-only metadata while preserving compliance limits, cleanup, and hard instrument-fault handling.
8. For later devices, resume normal travel: outputs off/707B open → safe Z retract → absolute Zaber X/Y target → bounded pre-approach → align → approach → electrical sequence.
9. Launch as a tracked background process, verify a fresh `device_N/summary.json` with live handoff values, and enable one stateful per-device reporter rather than duplicate reporters.
10. If this is a **re-measurement of a device whose active `device_N` path was already reported**, archive the old active folder before recreating it and invalidate that path in the reporter's `sent` state. A path-keyed reporter otherwise sees the recreated `device_N` as already delivered and silently suppresses the new result. Preserve archived originals outside the active glob watched by the reporter.
11. Do not let a successful single-point approach handoff bypass fresh health logic. If the reused approach hit read compliance or the immediate multi-bias health check is open-like, record the discrepancy and run the campaign's bounded diagnostic/contact-rescue policy before stress rather than claiming stable contact from the handoff alone.

## Concrete handoff

- Boundary: S1 device 22
- Nominal CSV target: `x=24383`, `y=509373`
- Post-alignment live Zaber: `x=24990`, `y=509610`
- Alignment residual: `0.43 px`
- Standalone approach final Z: `168.5`
- Final trim read: `25.4 pA`
- Fresh post-approach health: measurable, max `|I| ≈ 414 nA`, neither open-like nor short-like

This demonstrates why the nominal grid coordinate and post-alignment coordinate must both be preserved and why the first resumed device should reuse, not duplicate, a verified manual handoff.

## Verification checklist

- [ ] Named boundary matches the user's request.
- [ ] Absolute grid target and post-alignment live coordinate are separately recorded.
- [ ] Stage/Zaber handoff is live-read and unchanged before first-device electrical work.
- [ ] Preserved summaries are deduplicated and limited to valid pre-boundary devices.
- [ ] Remaining serpentine order is written to the run summary.
- [ ] First device has fresh health/DCIV/pulse artifacts without duplicate move/alignment/approach.
- [ ] Recreated boundary-device paths were removed from the reporter's sent-state so the re-measurement will be delivered once.
- [ ] A compliance-clamped or single-point handoff was revalidated with fresh multi-bias health/contact logic before stress.
- [ ] Runner remains active after startup and reporter state does not replay old devices.
