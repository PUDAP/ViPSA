---
name: vipsa-device-failure-prevention-recovery
description: "Use whenever a ViPSA memristor/DUT shows a new failure mode, breakdown, over-contact, over-reset, perma-set, open-contact, short-like behavior, unexpected compliance behavior, or recovery question. Maintain the linked logbook with causes, prevention, recovery, and recurrence tallies."
version: 1.0.0
author: Shreyas Pethe + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, memristor, failure-analysis, recovery, prevention, logbook]
    related_skills: [vipsa-electrical-measurements, vipsa-machine-operations]
---

# ViPSA Device Failure Prevention & Recovery

## Trigger

Load this skill whenever a ViPSA DUT/device:

- breaks down or appears damaged during DCIV, pulses, approach, or contact checks
- hits compliance unexpectedly
- becomes perma-SET / short-like / over-contacted
- becomes open-like / weak-contact / no meaningful voltage response
- shows a new failure mode or a recurring failure mode
- needs a prevention or recovery strategy after electrical/mechanical stress
- the user asks why a device failed or how to recover it

Also load `vipsa-electrical-measurements` and `vipsa-machine-operations` for live hardware actions.

## Core rule: update the logbook every time

Every time a new device failure mode appears, or a known failure mode recurs with new evidence, update:

- `references/device-failure-logbook.md`

The update must include:

1. Date/session/run artifact path if available.
2. Failure-mode label.
3. Evidence from real data: voltages, currents, compliance, branch, sweep shape, contact/Z state, plots/CSV paths.
4. Immediate classification: e.g. over-reset breakdown, over-contact short-like, open/weak contact, perma-SET, no-retention, compliance-limited false success.
5. What likely caused it, separated into:
   - anecdotal / operational cause
   - speculative mechanistic cause
6. Prevention strategy for next time.
7. Recovery strategy actually attempted or recommended.
8. Outcome: worked, did not work, not yet tried, or inconclusive.
9. Tally update for recurring failure modes.

Do not store secrets, NATS URLs, user IDs, run IDs that look credential-like, or transient irrelevant logs. Use paths to local artifacts and concise numeric evidence.

## Failure-analysis workflow

When a device fails or looks suspicious:

1. Freeze stress escalation.
   - Do not continue a planned sweep/pulse sequence blindly.
   - If live run is still active and danger is evident, stop safely and cleanup.
2. Save/inspect raw data.
   - Preserve sweep row order.
   - Identify branch and voltage where abrupt current jumps/drops occurred.
   - Compare to compliance settings and low-bias read probes.
3. Classify with evidence.
   - Breakdown-like: abrupt current increase on stress branch, sustained high return current, often not a clean RESET/SET.
   - Perma-SET/short-like: low-bias reads pinned near compliance or resistance bound in kΩ–low-MΩ range.
   - Open/weak contact: pA/sub-nA reads with little voltage scaling, noisy sign, no stress response.
   - Contact edge/over-contact: large sensitivity to ±0.25 Z changes; low-bias current jumps or reaches compliance after approach.
   - No-retention: switching-like branch occurs but post-read relaxes back to pA/sub-nA or loses state separation.
4. Choose the least stressful recovery probe first.
   - Low-bias health check before any further forming/reset.
   - Only escalate if low-bias data says device is not hard-shorted and contact is credible.
5. Cleanup and verify.
   - Keithley output off.
   - 707B open_all.
   - closed channels nil/no channels.
   - Relevant machines idle with `run_id: null`.
6. Patch the logbook.

## Default recovery ladder

Use the least aggressive step that can answer the question.

1. Low-bias health check:
   - `0 V`, `±10 mV`, `±50 mV`; optionally `±100 mV`.
   - Low compliance appropriate to context, typically `1e-7` to `1e-6 A`.
2. If short-like / over-contacted:
   - Stop electrical stress.
   - Consider retracting Z by `0.25` step and repeat low-bias health check if contact mechanics are likely the issue.
   - If still short-like, mark device as likely damaged/over-contacted and move on.
3. If open/weak-contact:
   - Do not form blindly.
   - Determine whether the reading followed only a lateral-move **pre-approach**. A pre-approach restores clearance partially and is not proof of contact; pA/GΩ behavior at that point may mean the probe has not landed rather than that the DUT is damaged.
   - Consider a single `+0.25` Z step and repeat low-bias check, or run bounded contact approach if user asks.
   - For the active ViPSA grid policy, use a `50–500 nA` target window at `+10 mV` before DCIV/pulses, with coarse `+0.5 Z` motion while clearly open-like and `0.25 Z` trimming near the contact edge.
   - See `references/post-lateral-preapproach-open-like-contact-recovery.md` for the safe handoff from lateral pre-approach to bounded electrical contact approach.
4. If over-reset/breakdown-like on negative branch:
   - Stop using the damaging voltage/compliance range.
   - Retry only with reduced reset limit and compliance, e.g. cap reset voltage before the observed jump and start reset compliance one order lower.
   - Add a hard stop on abrupt current jump, e.g. >3–5× in one point or entry into µA range if that is unsafe for the device.
5. If perma-SET/no-reset:
   - Use reset-first bounded recovery only if low-bias reads are not already hard shorted.
   - Escalate reset compliance slowly and use post-SET/post-RESET low-bias reads as the deciding evidence, not branch compliance hits.
6. If no-retention:
   - Do not call the condition optimized.
   - Use timed read probes or retention trace before pulses/endurance.

## Prevention rules for future experiments

- Avoid repeating the exact stress condition that caused a failure unless the user explicitly asks.
- For fragile or newly contacted devices, prefer branch-by-branch execution with inspection gates over full blind sweeps.
- Use low-bias reads before and after stress branches.
- Treat low-bias compliance hits as safety stops, not precise resistances.
- Treat a reset branch current surge as breakdown-like unless followed by clean low-bias HRS recovery.
- Distinguish actual recovery from apparent branch features: post-branch read probes decide whether RESET/SET retained.

## Contact-approach continuation after a blocked/failed runner

When contact approach is interrupted, blocked by command/protocol timeouts, or needs to continue after weak/no-contact reads:

1. Do not start a second approach blindly. First identify whether the previous runner is still active or has produced a final summary. If the interrupted protocol may already have applied an electrical sweep, mark its stress history unknown; **do not call a contact gate whose first iteration sweeps that same Z again**. Use an independent low-bias-only read at the current verified Z, then either advance with an explicitly skipped-first/next-Z procedure within the existing bound or retire. Do not infer zero stress merely because the CLI response timed out.
2. Force and verify cleanup before continuation: Keithley output off, Keysight output off if used, 707B `open_all`, closed channels empty/`nil`, light off unless imaging is required, and stale run IDs reset if they block safe commands.
3. If the normal PUDA protocol wrapper is blocked, a direct per-command NATS fallback is acceptable only after cleanup succeeds and only with bounded Z moves plus low-bias reads.
4. Log every fallback move/read into a run directory and `summary.json`, including thresholds, compliance, net Z, final status/error, and cleanup results.
5. While the approach is still running, report the current measured current, target window, net Z, process/session ID, and artifact path. Do not claim contact/completion from intent alone.

See `references/contact-approach-cleanup-and-fallback.md` for session-specific details.

## Bounded approach, over-current guard, and visualization

For a plain live `approach` request after coarse positioning or an open-like resistance check:

1. Use the user-standard `50–500 nA` contact window at `10 mV` unless the active experiment specifies another gate.
2. Approach with bounded `+0.5 Z` steps and a hard attempt limit. Stop forward motion immediately if current exceeds the upper gate or reaches read compliance.
3. Recover an overshoot using guarded retraction with a read after each move; use `0.25 Z` final guard trims around a steep contact edge.
4. Long-running runners may buffer stdout. Verify liveness from the tracked process plus the newest per-read artifact, and report the active phase—not merely a raw read count.
5. After completion, when the approach trajectory is useful or requested, create a scatter-only plot of cumulative net commanded Z versus `|current|` on a logarithmic axis. Separate forward/retract/fine/final-guard phases, shade the contact window, mark compliance, and save matching CSV data.
6. Do not use read index as a substitute for Z displacement; initial reads and extra retractions make the mapping nonuniform.
7. Verify output-off, 707B open/`nil`, lights off by default, and all relevant machines idle before reporting completion.

See `references/bounded-contact-approach-overcurrent-guard-and-plot-2026-07-24.md` for the verified recovery and plotting pattern.

## Early-grid failure prevention

When the first few devices in a grid run fail, show weak/no contact, or look over-contacted, do not just continue with the original approach parameters. Treat early failures as feedback on the contact recipe:

1. Pause or restart safely after cleanup if the run is still active.
2. Archive any partial device folders before re-running the same device with changed thresholds.
3. Preserve completed devices in the real grid traversal order and resume from the next/current device rather than repeating earlier devices.
4. Narrow the contact-detection current window when weak/over-contact behavior suggests the previous threshold was too permissive. A known user-requested conservative window is `1e-9 A` lower threshold and `1e-8 A` upper threshold.
5. Keep Z approach bounded with small increments, optional final trim, and a hard attempt limit.
6. If the user explicitly says not to skip DCIV/pulses, do not let a contact-quality safety gate silently suppress them. Continue with conservative electrical limits, record weak/no-contact honestly, and only refuse/stop for immediate hardware-safety hazards.
7. Before reporting success, verify the old runner stopped, machines cleaned up/are idle, the new runner exists, and the active script or artifacts contain the intended thresholds.

See `references/early-grid-contact-thresholds.md` for the session-specific notes behind this pattern.

## Linked files

- `references/device-failure-logbook.md` — cumulative failure/recovery log and recurrence tallies.
- `references/early-grid-contact-thresholds.md` — notes on adjusting contact thresholds and restarting a grid after early-device failures.
- `references/contact-approach-cleanup-and-fallback.md` — cleanup-first fallback pattern for continuing contact approach after blocked runners/protocol timeouts.
- `references/bounded-contact-approach-overcurrent-guard-and-plot-2026-07-24.md` — bounded `50–500 nA` approach, compliance overshoot recovery, buffered-run progress checks, and cumulative-Z/current plotting.
- `references/post-lateral-preapproach-open-like-contact-recovery.md` — interpret pA/GΩ checks after lateral pre-approach correctly and transition safely into a bounded `50–500 nA` contact approach.
