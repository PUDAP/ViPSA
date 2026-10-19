---
name: vipsa-grid-measurement
description: "Use when traversing or generating ViPSA device grid CSVs for multi-device measurements with Zaber XY motion, safe Z travel moves, alignment/contact approach, and per-device electrical test sequences."
version: 1.0.0
author: Shreyas Pethe + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, grid, zaber, stage, alignment, approach, electrical-measurement]
    related_skills: [vipsa-machine-operations, vipsa-electrical-measurements, vipsa-vision-alignment]
---

> Reference: `references/manual-earlier-device-retest-then-interrupted-boundary-resume.md` covers the case where the operator manually returns to an already processed earlier device before resuming: treat that live device as a one-device gated retest, then jump to the true interrupted serpentine boundary, preserve terminal devices between them, and hard-stop the runner on route/cleanup failure.
>
> Reference: `references/current-device-grid-run-and-stop-cleanup-2026-06-18.md` covers current-device grid generation, row-major CSV vs serpentine traversal, dual-camera recording, and stop/abort cleanup.
>
> Reference: `references/midrun-switch-to-literature-pbit-protocol-2026-07-31.md` covers switching an active grid run to the literature-derived p-bit protocol for subsequent devices: stop the old runner/reporter, verify cleanup, preserve previous-protocol results, restart from the interrupted device, and treat old SIGTERM notifications as expected rather than active-run failures.
>
> Reference: `references/grid-resume-preflight-and-electrical-hard-stop.md` covers safe current-device resumes after manual Z changes and electrical-edge outages: require a real 707B `open_all`/`nil` transaction before launch, hard-stop the entire runner on route/cleanup failure before travel, reconcile unexpected next-device retracts after a failed launch, archive failed artifacts, and reset reporter dedupe before retry.

# ViPSA Grid Measurement

Reference: `references/no-skip-grid-restart-stale-done-cleanup-2026-06-30.md` covers user-requested no-skip grid restarts/re-measurements: convert measurement gates to record-only only when explicitly overridden, archive stale `DONE.json` device folders for the restart range before launching, and verify fresh device artifacts so old completion sentinels cannot silently skip requested measurements.

Reference: `references/fresh-current-pad-substrate-7x7-handoff-2026-07-23.md` covers launching a fresh substrate 7×7 run “from here”: use live Zaber X/Y as device 1, preserve the already-aligned lateral position, enforce the 50–500 nA gate at the same 10 mV bias used for contact, retract in bounded −0.25 Z increments if initially over-window, verify fresh device-1 artifacts, and audit cloned runners for stale substrate/start-device/camera/resume metadata before launch.

Reference: `references/current-device-grid-launch-contact-gate-safety-2026-07-24.md` adds the critical live-handoff rule: reuse an in-window current-device contact without invoking a generic full approach, retract to verified optical clearance before any alignment recheck after possible contact/over-current, emit approach progress, audit cloned metadata, and install a stateful per-device reporter.

Reference: `references/no-skip-grid-resume-manual-handoff-2026-07-01.md` covers explicit “do not skip measurements” / “re-do from device N” continuation and manual contact/stage-zero handoff: make contact gates record-only unless there is a hard instrument fault, preserve completed devices while forcing the requested remeasurement, reuse verified manual contact for the first resumed device without retract/realign/reapproach, and monitor tee-wrapped runners via log/device artifacts.

Reference: `references/manual-s1-7x7-device6-overwrite-continuation-2026-07-14.md` covers a concrete manual positioned-device overwrite continuation: turn lights off, archive/prune old device 6+ artifacts, set an explicit serpentine boundary instead of using `DONE.json` filtering, run first-device approach in place without re-aligning or moving Zaber/stage, then continue the S1 7x7 grid measurement from device 6 with fresh artifacts.

Reference: `references/manual-aligned-approached-device-boundary-resume-2026-07-23.md` covers the later class of continuation where the named boundary device has already been moved to its absolute grid target, aligned, and approached outside the runner: preserve and deduplicate valid pre-boundary summaries, slice the actual serpentine order at the exact named device, record skipped/backfill decisions, reuse normalized standalone handoff artifacts without duplicate motion/alignment/approach, run fresh health before stress, and enable one stateful per-device reporter. For re-measurements that recreate an already-reported `device_N` path, invalidate that path in reporter state so the replacement result is delivered exactly once.

Reference: `references/named-device-resume-after-explicit-z-retract.md` covers “move Z down N steps and continue from device M”: use live Zaber X/Y plus the grid map—not the last partial folder—to identify the physical device; execute cleanup, Z motion, and before/after readbacks in a standalone PUDA protocol; preserve an already aligned live X/Y offset; approach from the verified retracted Z without an automatic pre-approach move that partially undoes the user’s retract; retain earlier standalone partial summaries; and install one stateful reporter for the full continuation.

Reference: `references/stop-and-return-to-completed-device-approach-retry-2026-07-23.md` covers stopping mid-device, preserving completed/partial artifacts, cleaning up and pausing reporters, safely returning by absolute grid coordinates to a prior completed device, running one isolated bounded approach retry without overwriting the original device record, and reporting a contact-window result honestly when it is pinned at read compliance.

Reference: `references/interrupted-grid-retry-and-set-no-reset-pulse-continuation-2026-07-25.md` extends that class with stale-run recovery after killing an active command, safe return to the prior device's recorded aligned absolute X/Y, a strict-window bounded retest that preserves the interrupted next-device partial, and the user-required pulse branch: when DCIV observes SET without RESET, run exactly five RESET-read pairs at the strongest configured RESET voltage, save the reads, and continue randomized pulsed measurements while retaining independent compliance safety checkpoints.

Reference: `references/stable-narrow-window-three-attempt-resume-2026-07-25.md` covers a live policy change to stable 1–10 nA contact: require three consecutive low-bias reads, use two bounded +0.5-step attempts followed by one bounded +1-step attempt, retract each failed attempt's exact positive net Z before retry/travel, archive interrupted-device artifacts, resume from verified aligned absolute X/Y, and emit a concise update after every finished device.

Reference: `references/current-position-overwrite-continuation-after-standalone-approach.md` covers “continue from this device and overwrite” after manual motion or standalone approach: identify the physical boundary from live Zaber X/Y rather than stale narrative state, archive canonical boundary-and-later folders in serpentine order, prune summaries and reporter dedupe state together, recover/revalidate over-contact before stress, compile/assert the cloned runner, and require a fresh boundary `device_start` before reporting success.

Reference: `references/live-nearest-device-finalized-electrical-grid-launch-2026-07-31.md` covers launching the finalized electrical grid protocol from the live contacted device when the device number is not named: use live Zaber X/Y only to identify the nearest saved-grid boundary, preserve the first device’s live aligned/probed offset, verify/recover contact before stress, run exactly one finalized DCIV cycle before randomized pulses, and install a stateful per-device reporter.

Reference: `references/nearest-device-from-live-zaber-and-grid-csv-2026-07-29.md` covers answering “closest device according to grid runner”: query live Zaber X/Y, compare against the relevant `grid_positions.csv`, and report nearest device with target, offset, and distance rather than inferring from stale folders or narrative state.

Reference: `references/live-nearest-device-previous-sequence-device10-handoff-2026-07-29.md` covers live nearest-device identification from Zaber X/Y, treating a user-named previous/next sequence device as authoritative, and the safe cleanup → Z-safe-retract → absolute Zaber move → align → `+40` pre-approach → bounded approach handoff.

Reference: `references/current-device-single-dciv-cycle-grid-pulses-2026-07-27.md` covers current-device single-device testing with grid electrical logic when the user explicitly requests **one DCIV cycle then randomized pulses** and forbids extra reset sweeps: approach/stabilize the current contact, override the grid DCIV reset ladder to a single `0 -> +0.6 -> 0 -> -0.75 -> 0` cycle, then run the grid randomized pulse helper; clearly distinguish forbidden extra DCIV reset sweeps from the grid pulse helper’s five `RESET -> read` fallback pairs after SET-without-RESET.

Grid travel/approach sequence correction for all future grid measurements unless the user explicitly overrides: use `stage.move_z_by(-50)` → `zaber.move_x_to(target_x)` → `zaber.move_y_to(target_y)` → vision `align` → `stage.move_z_by(+40)` → electrical `approach`. Do **not** do the older `+30` pre-approach before alignment.

**Campaign-specific override — `optimization_sub_2` (Pratap CsFAPbI/C60 8×8):** The user explicitly changed adjacent serpentine device transitions to live-position-relative **Z−100 after finishing contact → absolute Zaber target from `eligible_grid.csv` and optical tip/pad alignment → Z+80 → bounded +10 V/100 µA forming-as-approach at the pre-approach height, then Z+5 and a fresh forming/check only while no credible contact is established**. Preserve output-off/matrix-open verification and a visible safe travel gap before XY; verify each stage readback before another move and never replay ambiguous motion. A forming compliance flag alone is not proof of contact: require sustained response and an unclamped post-forming low-bias response with contact-dependent voltage scaling; stop forward motion on read clamp, collision/overcontact signature, hard stage limit, failed instrument/position gate, or a bounded approach ceiling. Record every attempted Z/forming/read, retire a no-contact site rather than advancing without bound. This override does not change other grids' default −50/+40 rule. **Already-retracted handoff:** from live Z−150 at completed (2,8), last verified contact Z−70, the probe is already retracted by 80; add only Z−20 (to −170) to reach the requested −100-from-contact travel height, then move/align (2,7), Z+80 to −90, and begin forming checks. Never issue a second full −100 from −150; recompute and gate against fresh live readbacks if the operator moves Z. See `references/grid-travel-align-then-zplus40-2026-07-28.md`, `references/grid-sequence-correction-and-device16-contact-gate-2026-07-27.md`, and `references/grid-default-post-align-z40-and-current-device-handoff-2026-07-28.md` for current-device handoffs: explicit Z move (e.g. `+15`/`+20`) → approach in place → continue grid only if stable contact succeeds; if stopped mid-approach, cleanup and report verified safety.

Reference: `references/current-aligned-device-grid-continuation-one-dciv-stall-recovery-2026-07-27.md` covers continuing a grid from a manually aligned/current boundary device with `approach -> exactly 1 DCIV -> randomized pulses`, preserving the live aligned XY offset for the first device, using normal safe travel/alignment only for later devices, and recovering/restarting if a stage/NATS stall leaves a busy run id before approach artifacts are written.

Reference: `references/skip-untested-current-device-continue-next-2026-07-27.md` covers conditional skips like “if device N has not been tested, skip it and move on”: verify no DCIV/pulse artifacts exist, stop/cleanup the active runner, mark the current device `skipped_untested_by_user`, compute the next device from serpentine order, and restart with normal travel/alignment logic for that next device rather than reusing the skipped device’s current-handoff path.

Reference: `references/retrofit-standalone-current-device-results-into-grid.md` covers saving standalone current-device DCIV/randomized-pulse artifacts into an ongoing grid run after identifying the nearest grid device from live Zaber X/Y: archive stale canonical folders, normalize artifacts into `device_N`, update run summaries, then continue from the next serpentine device with a reporter.

Reference: `references/manual-current-device-result-backfill-and-next-device-continuation-2026-07-27.md` covers the concrete S9 pattern for assigning standalone current-device measurements to device 15, archiving stale `device_15`/`device_16`, preserving device 15 in run summaries, launching from next serpentine device 16, pausing the reporter on stop, and using stage abort/readback to clear a stale run after SIGTERM.

Reference: `references/safe-boundary-approach-window-change-and-combined-plot-reporter-2026-07-14.md` covers active-grid approach-window changes and per-device reporting: schedule threshold changes at the next DONE boundary, patch constants and metadata in a fresh continuation runner, cleanup/archive/prune before restart, treat the old runner's SIGTERM as expected, and send a single combined 4-panel figure after each newly completed device.

Reference: `references/live-contact-window-change-safe-restart.md` covers the immediate mid-device variant when the old window must stop applying now: terminate and cleanup, recover/read live positions, archive the partial device, restart that device as a current-position fresh-approach handoff, and update lower/upper bounds, compatible read compliance, downstream contact classifications, metadata, and reporter state together.

Reference: `references/no-contact-full-reapproach-before-measurement.md` covers the user-corrected max-attempt policy: after `no_contact_after_max`, preserve attempt 1, re-check alignment, perform one complete bounded approach again, repeat post-approach health, and only then apply the configured persistent-no-contact measurement gate. For live runners, stop/cleanup/archive/restart from the exact current device because already-running Python code will not inherit patched control flow.

Reference: `references/strict-contact-gating.md` defines the stronger class-level gate: evaluate the numeric final `|I|`, redo one complete bounded approach after any out-of-window result, and never run DCIV/pulses unless the final contact current is within the requested window. If both bounded attempts fail, record a contact-gate skip rather than continuing electrical stress or approaching indefinitely.

Reference: `references/stop-grid-runner-reporter-and-unverified-cleanup-2026-07-14.md` covers immediate user-requested grid stops: kill the tracked runner, pause active reporter cron jobs, verify no process remains, attempt electrical cleanup, report cleanup as unverified if START/queue responses time out despite idle state snapshots, and treat interrupted-device artifacts (`DONE.json`, plots, pulse summaries) as non-authoritative unless `summary.json` is completed with expected measurement sections.

Reference: `references/verified-stop-after-strict-contact-skip-2026-07-25.md` covers the successful-cleanup variant: reconcile buffered full-process output against per-device summaries, distinguish completed/skipped/interrupted devices, run bounded per-command abort/output-off/open-all/light-off/stage-abort cleanup, verify all six machines idle/null, and explain strict-window skips from attempt currents and stability evidence without misclassifying weak contact as device failure.

Reference: `references/explicit-redo-boundary-and-pause-unverified-cleanup-2026-07-01.md` covers a later correction: when the user names a redo boundary device, that device number is authoritative and must not be replaced by “first missing `DONE.json`”; archive/prune from the requested traversal boundary, patch `START_AT_DEVICE` and skip filters so the requested device actually starts, and when pausing report cleanup as unverified if PUDA/NATS state/control responses time out.

Reference: `references/done-json-error-artifact-triage-2026-07-01.md` covers retrospective triage after a runner writes `DONE.json` in a `finally` block: count valid measurements by `summary.status == "completed"` plus real electrical artifacts, not by `DONE.json` existence alone; a NATS/connection failure can create many stale `DONE.json` error sentinels that must be archived or skipped around before restart.

## Overview

Use this skill for **grid measurement** workflows: generating or consuming a CSV of device positions, moving the Zaber X/Y stages through the devices, safely handling Z travel height, aligning/contacting each device, and running a user-specified electrical test sequence at each device.

The grid CSV encodes absolute Zaber X/Y positions that place each device under the probe tip, or in the camera frame such that the device to test lies to the left of the center/probe location.

## When to Use

Use this skill when the user asks for any of:

- grid measurement
- measuring many devices from a grid CSV
- creating a grid CSV from current Zaber position plus row/column spacing
- traversing devices row-wise or serpentine
- running DCIV/resistance/pulse tests across a device array

Also load and follow:

- `vipsa-machine-operations` for Zaber, stage-Z, approach, and PUDA safety rules.
- `vipsa-electrical-measurements` for resistance, DCIV, pulse, optimization, and cleanup conventions.
- `vipsa-vision-alignment` when alignment is required before approach.

## Grid CSV Format

The CSV should contain three columns:

```text
device_number,x,y
```

Where:

- `device_number` is a sequential integer device identifier.
- `x` is the absolute Zaber X position.
- `y` is the absolute Zaber Y position.

The `x` and `y` values are **absolute Zaber stage positions**, not relative moves. They are calculated so that moving Zaber to those absolute positions brings the target device into the correct test location under/near the probe.

Use native Zaber units unless the user explicitly requests millimetres.

## Creating a Grid CSV

If the user does not provide a CSV and asks you to make one, collect these inputs:

1. `x_distance`: distance between successive pads/devices in X.
2. `y_distance`: distance between successive pads/devices in Y.
3. `rows`: number of grid rows.
4. `columns`: number of grid columns.

Then:

1. Read the current Zaber X/Y position with `zaber.get_current_position(units=None)`.
2. Treat this current position as the grid origin for device 1.
3. Generate device numbers sequentially **first along each row, then row by row down the columns**.
4. Save the CSV with columns `device_number,x,y`.

Formula for row-major numbering:

```python
device_number = row * columns + column + 1
x = origin_x + column * x_distance
y = origin_y + row * y_distance
```

Where `row` and `column` are zero-indexed.

Example: `rows=3`, `columns=3`, `x_distance=5000`, `y_distance=5000`, origin `(x=100, y=100)`:

```csv
device_number,x,y
1,100,100
2,5100,100
3,10100,100
4,100,5100
5,5100,5100
6,10100,5100
7,100,10100
8,5100,10100
9,10100,10100
```

## Serpentine Traversal Order

Even though CSV numbering is row-major, physical traversal should be **serpentine** to reduce long travel moves:

- First row: left to right.
- Move down in the same column.
- Next row: right to left.
- Repeat.

For the 3x3 example above, traverse in this order:

```text
1, 2, 3, 6, 5, 4, 7, 8, 9
```

Implementation rule:

```python
for row in range(rows):
    row_devices = devices[row*columns : (row+1)*columns]
    if row % 2 == 1:
        row_devices = list(reversed(row_devices))
    traverse(row_devices)
```

If a CSV is provided, infer rows/columns only when possible. If the grid shape is ambiguous, ask the user for rows/columns or traversal order before moving hardware.

## Per-Device Protocol

For each device in the serpentine traversal:

1. **Check whether electrical contact is already made.**
   - Use a non-stressing contact/read check such as a low-voltage Keithley read if needed.
   - If contact is already valid, skip alignment and approach unless the user asks for re-alignment.
2. **If contact is not made, align.**
   - Use the ViPSA vision alignment workflow.
   - Use the 🎯 emoji in concise alignment reports.
3. **Perform approach.**
   - Use the established Keithley-guided approach defaults unless the user gave different parameters.
   - Use the 👇 emoji in concise approach/contact reports.
4. **Run the user-specified test sequence.**
   - The test sequence may include resistance checks, one or more DCIV sweeps, pulse measurements, pulse optimization, or custom electrical workflows.
   - Preserve per-device metadata and save per-device artifacts.
   - If the sequence is conditional, encode each gate explicitly. Example: resistance check first to reject already-shorted devices; DCIV/forming only if not shorted; pulse optimization only if DCIV shows a good SET; long endurance/pulse train only if the device remains alive after the optimization screen.
   - **SET-without-RESET continuation:** when DCIV records `set_detected=true` and `reset_detected=false`, run exactly five `RESET → read` pairs at the strongest configured RESET voltage, save all five read currents, select that RESET voltage, and continue randomized `SET → read → RESET → read` measurements. Do not make successful RESET calibration a prerequisite for entering the pulse loop in this branch. Keep independent pulse/read-compliance checks and cleanup-on-exit safety stops.
5. **Move to the next device.**
   - Force electrical cleanup first: SMU outputs off and 707B open/nil.
   - **Hard-stop the whole grid if output-off, 707B routing, `open_all`, or `get_closed_channels == nil` cannot be verified.** Do not let a per-device exception handler mark an error and continue into Stage/Zaber travel with unknown routing.
   - Move the microscope stage Z to the safe travel height: `stage.move_z_by(height=-50, feedrate=450)` unless the user explicitly overrides the amount.
   - Move Zaber X/Y to the next device’s absolute `x,y` position.
   - Perform vision alignment at this safe/retracted optical position.
   - After alignment, run the pre-approach Z move: `stage.move_z_by(height=+40, feedrate=450)` unless the user explicitly overrides the amount.
   - Then perform electrical contact check/approach.

Session reference: `references/grid-trial-electrical-sequence-2026-06-06.md` captures a concrete 3x3 grid run pattern with device 1 skipped, permanent top-level folder naming, safe Z retract/pre-approach distances, and a resistance → DCIV/forming → bounded pulse optimization → endurance gate sequence.

Session reference: `references/from-here-3x3-grid-pulse-plotting-2026-06-07.md` captures a concrete “from here” 3x3 grid pattern: current Zaber X/Y as origin, explicit approach-current thresholds, tracked background run startup, and scatter-only pulse plotting when the user says not to connect datapoints.

Session reference: `references/dual-camera-grid-run-poller-2026-06-18.md` captures a concrete long 3×3 grid pattern with dual-camera full-process recording, current-device direct approach when not initially in contact, safe Z retract/pre-approach moves between devices, per-device summary plots even for skipped devices, and a `no_agent` poller that sends each graph after the device finishes plus final videos at completion.

Session reference: `references/adaptive-per-device-reporting-and-recorder-deps-2026-06-22.md` captures an adaptive long-grid continuation pattern: send each completed device plot immediately, analyze failures, append a project logbook entry, and tweak the next-device protocol at a safe boundary. It also records the recorder dependency guard for OpenCV-based video threads (`opencv-python-headless`) so video setup issues are separated from electrical measurement status.

Session reference: `references/grid-open-weak-contact-plus1-retry-2026-06-18.md` captures the user-corrected grid-run policy: do not skip a grid device solely because approach/health is open-like or weak-contact; move stage Z forward/up by `+1` step and retry/run the requested measurements, while preserving hard short/over-current safety gates.

Session reference: `references/8x8-align-approach-form-random-sigmoid-grid-2026-06-22.md` captures an 8×8 current-origin grid workflow with 5000-native-unit X/Y spacing, serpentine traversal, align → approach → conservative forming DCIV, and randomized SET-voltage pulse probability measurement with analysis checkpoints every 100 pulses and no separate pulse-health check unless requested.

Session reference: `references/soft-approach-grid-resume-and-contact-edge-dciv-2026-06-22.md` captures how to resume an interrupted grid from an unfinished device after prior devices look pre-shorted: inspect whether the resume device was already aligned/contacted, use a softer 1–20 nA approach window with 0.25 Z steps, and if first DCIV looks like no contact, move Z +0.25 and rerun DCIV once.

Session reference: `references/per-device-live-analysis-logbook-adaptive-tweaks-2026-06-22.md` captures the user-requested pattern for long grid runs: send each device plot/analysis immediately after that device finishes, append failures and artifact links to `project.md`, and adapt subsequent device protocol settings based on observed failure modes such as DCIV compliance-limited shorts or pulse compliance flags.

Session reference: `references/grid-overcontact-override-and-p-switch-reanalysis-2026-06-23.md` captures a full 8×8 continuation where the user explicitly overrode overcontact/short-like skip gates: still run reset-pre-sweep, DCIV, and pulsing; record override flags; verify serpentine resume order; and reanalyze completed randomized-pulse data using a `read_after_set` distribution-derived threshold instead of Youden J when requested.

Session reference: `references/grid-resume-stale-data-and-duplicate-subscriber-recovery-2026-06-24.md` captures the restart-from-device workflow after outage/stale data: reset/cleanup all ViPSA machines, delete stale device folders and partial summaries from the restart device onward, classify killed-process H.264 recorder warnings correctly, and patch resume runners to use bounded fresh per-command start→command→complete retries when duplicate/stale subscribers produce `RUN_ID_MISMATCH` despite idle machine state.

Session reference: `references/electrical-fidelity-preserving-speedups-and-contact-z-surface-2026-06-23.md` captures the user-corrected speedup policy for long ViPSA grid runs: do not compromise electrical fidelity by reducing DCIV/pulse/reset/logging; speed up only non-electrical overhead such as approach prediction, adaptive mechanical Z steps, selective alignment, stateful cleanup, async plotting, and contact-Z surface analysis.

Session reference: `references/batch-substrate-8x8-forming-randomized-5000-train-2026-06-23.md` captures a probabilistic-computing substrate workflow where data must be separated by batch/substrate, an 8×8 current-origin grid uses 5000-native-unit spacing, safe Z retraction is 40 steps, pre-approach is +20 Z steps, alignment occurs after each device move, approach uses +0.5 steps with 0.25-step trim, DCIV is adaptive (`0→+1→+1.5→0` plus reset/recovery branches), and randomized SET-voltage pulse probability measurement with analysis checkpoints every 100 pulses and no separate pulse-health check unless requested. For restarting this class of run from a currently probed device while overwriting stale later records, see `references/restart-8x8-from-current-device-overwrite-boundary-2026-06-24.md`: archive/prune device folders and summary entries beyond the requested boundary, patch the runner not to skip stale `DONE.json`, and keep the batch/substrate hierarchy intact.

Session reference: `references/device-n-no-recording-restart-and-updates-2026-06-24.md` captures the specific pattern for “start with device N, no video recording” after a stopped/idle continuation: distinguish monitor crons from measurement processes, patch `START_AT_DEVICE=N`, keep recording disabled, initialize per-device reporter state to avoid duplicate old reports, start a tracked background runner, and verify `device_N/summary.json` plus no new camera video files.

Session reference: `references/no-record-restart-and-per-device-finish-updates-2026-06-24.md` captures two live-run operating patterns: when the user says `do not record`, stop the active recorder/runner, delete unwanted new video artifacts, patch recorder threads out before restart, and verify no new video files; when the user asks for updates after each device finishes, enable a no-agent cron monitor that watches new `device_*/DONE.json` files, uses a state file to avoid replay, and sends concise summaries plus `MEDIA:device_plot.png` attachments.

Session reference: `references/live-grid-restart-smu-busy-check-and-travel-z-update-2026-06-24.md` captures a live restart pattern when `puda machine state` hangs but the user asks to check whether SMUs are busy before continuing: use short fresh direct PUDA/NATS `START` probes on Keithley/Keysight/707B, force SMU outputs off and 707B `open_all`, patch safe travel Z values in both runner logic and summary metadata after loading old partial summaries, archive the partial current-device folder, restart as a tracked background process, and verify the new device summary/artifacts plus no new videos when recording is disabled.

Session reference: `references/grid-resume-stale-data-and-per-command-run-recovery-2026-06-24.md` captures a post-outage restart workflow: stop the stale process, reset/cleanup all ViPSA machines, delete stale device folders and prune `summary.partial.json` from the requested restart point onward, then resume with fresh per-command `START → command → COMPLETE` transactions and retries when duplicate/stale edge subscribers produce `RUN_ID_MISMATCH` even after a successful START.

Session reference: `references/retrospective-grid-electrical-logic-recall-2026-06-26.md` captures how to answer retrospective questions like “what was the electrical testing logic for the last grid measurement”: inspect the actual run folder and latest runner/resume script, report contact/DCIV/pulse gates with exact numerical parameters, and explicitly note any mismatch between run summary metadata and executed code.

Session reference: `references/s3-grid-pause-and-failure-analysis-2026-06-26.md` captures an S3 8x8 current-device grid pause/analysis pattern: implement pause-after-current-device with a watcher, kill after current `finished_utc`, cleanup/verify outputs and 707B `nil`, mark any pre-created next-device summary as `paused_before_measurement`, clear `idle` machines with stale non-null `run_id`, and analyze early devices by separating short-like/compliance-pinned failures from weak-contact/permanent-HRS failures.

Session reference: `references/s1-8x8-current-device-dciv0p8-randomized-10000-2026-06-30.md` captures an S1 fresh 8x8 current-device campaign pattern: current Zaber X/Y as device-1 origin, align+approach even for the first device, DCIV `0→0.8→0→-1.0 V` at 20 mV with SET/RESET compliance `1e-5/1e-4 A`, randomized `SET-read-RESET-read` pulses with `0.2–1.0 V` levels, `50` attempts/level/block, `500`-pulse chunks up to `10000` pulses/device, `-50/+30` Z travel, fixed run-directory handoff to a no-agent per-device reporter, and the blind-replacement pitfall where changing pulse-count text can accidentally alter 5000-native-unit grid spacing.

Session reference: `references/live-grid-next-device-parameter-change-2026-06-30.md` captures the safe-boundary patch/restart pattern for active long grid runs when the user changes electrical parameters mid-run: distinguish “re-do current device” from “from the next device,” wait for the current device `DONE.json` when appropriate, patch runner constants and metadata together (e.g. compliance and reset-side voltage), cleanup/verify SMU/707B state, archive stale restart folders, prune partial summaries, restart as a tracked process, and log the boundary in `project.md`.

Session reference: `references/failure-prevention-restart-from-device14-2026-06-30.md` captures a failure-prevention restart from a stale unfinished grid device: back up and patch the runner, keep the user-specified `0.5` approach step while tightening the target to `1e-9–1e-8 A`, add post-approach and post-DCIV health checks, lighten pre-characterization DCIV and SET pulse stress, reduce chunks to `100` pulses, archive stale `device_N`, prune summaries by serpentine traversal order, compile, launch tracked, and verify fresh device summary plus no unwanted camera recording.

Session reference: `references/one-by-one-protocol-optimization-after-overforming-2026-06-30.md` captures the adaptive optimization pattern when grid devices show protocol-induced overforming or short pulse lifetime: inspect completed-device metrics, apply only one class of change at a DONE boundary, preserve cleanup/archive/prune hygiene, account for serpentine traversal vs numeric device order, and progress through softer approach → stronger pulse reset → gentler SET pulse stress only if each prior change fails.

Session reference: `references/contact-gated-open-failure-mitigation-2026-06-26.md` captures the follow-up implementation pattern for avoiding device 4/5-style failures: add multi-bias low-compliance contact diagnostics, offset/paired-bias classification, bounded `+0.25 Z` rescue, skip higher-compliance retries when contact remains open-like/no-voltage-scaling, and skip randomized pulses when DCIV/contact diagnostics never show meaningful coupling.

Session reference: `references/device6-plus-safety-gated-continuation-2026-06-26.md` captures the stricter continuation implemented after the first five S3 devices: from device 6 onward, low-bias short-like/contact-compliance is a hard skip for DCIV/pulses, DCIV is branch-by-branch with post-branch low-bias gates, reset is initially capped near `-1.0 V` at `1 µA`, high-compliance reset-pre/recovery sweeps are disabled, and pulses only run when `dciv.pulse_allowed` is true.

Session reference: `references/no-skip-dciv-pulse-override-after-safety-gated-resume-2026-06-26.md` captures the follow-up user correction: when the user explicitly says not to skip DCIV/pulses, stop the safety-gated runner, archive/prune stale skipped device folders from the restart boundary, patch a new continuation runner so contact/safety gates become record-only metadata, keep safer electrical limits unless changed, and rerun from the requested device with DCIV and randomized pulses always attempted.

Session reference: `references/no-skip-restart-stale-done-skip-recovery-2026-06-30.md` captures a no-skip restart pitfall: pruning summaries is not enough if stale `device_N/DONE.json` folders remain after the restart boundary. Archive stale per-device folders or patch the runner's `DONE.json` filter to honor `START_AT_DEVICE`; if a run already skipped stale folders, stop at a safe device boundary, archive the skipped/partial folders, prune summaries, and restart so no requested measurements are skipped.

Session reference: `references/overwrite-restart-from-device-boundary-2026-06-26.md` captures the explicit-overwrite restart pattern: stop the active runner, cleanup/verify electrical safety, delete device folders from the requested boundary onward, prune `summary.partial.json` to preserve only pre-boundary devices, patch `START_AT_DEVICE` and preserved-device sets, ensure contact gates use current threshold constants, compile, launch, and verify fresh first-device artifacts.

## Electrical-Fidelity-Preserving Speedups

When the user asks to make long ViPSA grid runs faster, first ask whether the electrical protocol may change. If the user wants full electrical fidelity, do **not** propose reducing DCIV resolution, pulse count, SET-voltage list, repeats, reset-pre sweeps, compliance logging, or electrical checkpoints as the default speedup path.

Instead optimize only non-electrical overhead:

- Predict contact Z from prior devices / row medians, then still validate with the same low-bias contact check before stress.
- Use adaptive mechanical Z approach: larger steps while clearly open/noise-floor, then the established minimum fine step near the contact-current target.
- Use selective vision alignment: first device of each row, row transitions, large correction, weak/no-contact, or abnormal contact check; otherwise rely on grid X/Y plus electrical validation.
- Keep strict cleanup at travel/device boundaries and on exceptions, but avoid redundant route/output calls inside stable phases when state is known.
- Move plotting/reporting and video encoding out of the measurement loop so raw electrical acquisition proceeds immediately after writing per-device artifacts.
- Build a contact-Z height surface from per-device summaries to support future predictive pre-approach without changing electrical measurements.

See `references/electrical-fidelity-preserving-speedups-and-contact-z-surface-2026-06-23.md` for the detailed session pattern and contact-Z plotting recipe.

- If prior device contacts show a clear corner-to-corner Z gradient, treat the substrate as tilted and speed the *mechanical* approach with a Z-plane calibration, not by reducing electrical measurements. For the first four outside-corner calibration measurements, use extra-cautious travel: force electrical cleanup and move microscope stage Z down/back by **100 steps** before each corner-to-corner Zaber X/Y move; then fit `Z_contact = aX + bY + c`, pre-approach only to `Z_pred - safety_margin`, and always run a live low-bias contact check before any stress. See `references/tilted-substrate-z-plane-precalibration-2026-06-23.md`.

## Manual restart from a positioned device

When restarting an interrupted grid from a user-specified device after manual Z/Zaber instructions, do not bury the full handoff inside one long opaque runner. First reconcile the **live** Zaber X/Y against the saved grid and the named boundary; do not infer the physical device from the newest partial folder. Archive or move stale `device_N+` folders (or patch the runner not to skip them), execute the requested Z motion and any required Zaber absolute travel as separately verified PUDA protocol phases, turn lights off before electrical approach and measurements unless explicitly overridden, run a bounded standalone approach and save `approach.json`, then launch the continuation runner from that device. If live X/Y is already the aligned named device, preserve that aligned offset: do not snap back to nominal CSV X/Y. When the user explicitly requested a Z retract before continuing, approach from the verified retracted Z instead of automatically adding the generic pre-approach move and partially undoing the retract. For the first restarted device, reuse the recorded handoff/approach result instead of repeating motion, alignment, or approach. Preserve earlier standalone partial summaries as interrupted history even if they were never appended to `summary.partial.json`. See `references/manual-positioned-grid-restart-2026-06-24.md` and `references/named-device-resume-after-explicit-z-retract.md`.

If the user pauses an active grid to revisit a completed/current device with changed approach thresholds or parameters, keep the grid paused, patch the continuation runner constants/metadata at the safe boundary, move back to the target device with explicit safe-Z/Zaber/pre-approach steps, and run a standalone retry artifact. For manual retests of already-completed devices, create a distinct retest folder rather than overwriting the original unless explicitly requested, stop active runner/supervisor processes first, cleanup/verify SMU outputs off and 707B `nil`, move by recorded absolute Zaber target, run the requested approach override, and keep the normal grid paused until the user explicitly resumes. Beware helper functions that parse `devdir.name.split('_')[-1]` as a numeric device number; timestamped retest folders can break pulse helpers, so pass an explicit device number or use a temporary numeric symlink and rewrite summary paths back to the real retest folder. See `references/manual-retest-completed-device-with-custom-approach-2026-06-30.md`. If the user changes approach parameters while also preserving a no-skip DCIV/pulse override, follow `references/no-skip-grid-restart-device6-updated-approach-2026-06-26.md`: stop the active runner, cleanup/verify outputs off and 707B `nil`, archive stale restart-device folders, prune partial summaries from the restart boundary, patch both runner logic and metadata for the new parameters (e.g. `0.5` Z step, `0.25` trim/fine step, `120` max attempts), and verify fresh restart artifacts before reporting. If the user authorizes extra approach range beyond the primary max, record primary-max and extra-step budgets separately and only report failure after the combined budget is exhausted; downstream no-contact gates must also recognize the new terminal status. For overwrite-boundary restarts such as “rerun all devices from device 7 and overwrite existing data,” follow `references/restart-overwrite-boundary-and-extended-approach-retry-2026-06-26.md`: stop/cleanup the active runner, delete `device_N+` folders, prune `summary.partial.json` to devices before `N`, patch `START_AT_DEVICE=N` using serpentine traversal index, and verify fresh `device_N/summary.json`. If the retry script stalls during a stage move, recover with `stage.abort_motion()`, stage position readback, SMU output-off, `707B.open_all()`, and full idle/null verification before reporting. See `references/manual-device-retry-extended-approach-2026-06-24.md`.

## Safe Movement Rules

- Zaber X/Y grid positions are absolute positions. Use `move_x_to(position, units=None)` and `move_y_to(position, units=None)` unless the user explicitly requests relative moves.
- For native units, encode `units: null` in PUDA protocol parameters.
- Do not use `units: "mm"` unless the user explicitly requested millimetres.
- Before every Zaber travel move between devices, raise stage Z to the safe travel height first.
- If scratches, uncertain clearance, stale Stage-Z tracking, or a newly changed travel-retract amount is involved, do not trust the commanded/readback delta alone: capture an illuminated side/oblique view after retraction and verify a visible probe–substrate gap before any lateral Zaber motion. Hard-stop if clearance cannot be verified.
- After reaching the next Zaber X/Y position, perform vision alignment first at safe/retracted Z, then run only the planned `+40` pre-approach Z move before electrical approach. Do not blindly return to the previous contact Z.
- Do not move microscope stage X/Y as part of grid traversal; grid traversal uses Zaber X/Y. Microscope `stage` movement is Z-only unless the user explicitly asks for stage X/Y motion.
- Always keep SMU outputs off and 707B open during travel moves.

## Contact Check Logic

Before alignment/approach at a device, determine whether the probe is already in contact:

- If a recent valid contact/read exists for the current device and no travel occurred, contact may already be made.
- If uncertain, do a low-voltage Keithley check with conservative compliance.
- If low-bias current is within the intended contact window, skip alignment and approach.
- When defining or changing a contact window, set the approach read compliance above the requested upper bound with conservative headroom; otherwise the requested window may be physically unobservable. Patch downstream `safe_contact`, `open_weak`, and `over_or_short` thresholds and summary metadata from the same constants rather than leaving stale hard-coded limits.
- If the configured policy requires a retry after `no_contact_after_max`, treat it as a full second approach **before** DCIV/pulses: save attempt 1 separately, re-check alignment when safe, rerun the bounded approach, replace downstream `app`/contact classification with attempt 2, and repeat post-approach health. Only after attempt 2 may persistent-no-contact diagnostics, skips, or explicit no-skip overrides apply. Do not let a higher-voltage diagnostic or stale attempt-1 health substitute for the required re-approach.
- **Strict-window precedence:** if the user says to enforce a contact window or not measure until current is inside it, that instruction supersedes earlier no-skip/record-only overrides. Gate on the final numeric `abs(I_contact)` **and any requested stability criterion**, not an approach status label or later DCIV response. A robust stability criterion is three consecutive low-bias reads inside the window at one unchanged Z position; save those reads and gate downstream work on an explicit `stable_contact_confirmed` field. Execute exactly the user-configured number and step sizes of bounded attempts. For this user's subsequent approach retries, continue from the verified current Stage-Z by default and **do not insert a gross `-50` or attempt-sized retract between failed blocks**; preserve minimum-step negative safety trims after over-current/overshoot. Before any X/Y travel, perform and verify the configured safe travel retract so approach depth does not carry into lateral motion. After all configured attempts fail, block DCIV/pulses and record `skipped_contact_not_in_window`; do not approach indefinitely. See `references/strict-contact-gating.md`, `references/stable-narrow-window-three-attempt-resume-2026-07-25.md` (whose inter-attempt retract recipe is superseded by this later user correction), and `vipsa-machine-operations/references/discussed-device-vs-live-device-approach-retry.md`.
- If current is pA/noise-floor, unstable, or outside the contact window, run alignment and/or approach.
- If low-bias current is compliance-limited, report likely short/over-contact and ask before stressing further, unless the user explicitly gave a safety-stop policy.
- If an approach returns `in_window` at or effectively equal to its configured read compliance, report that the **contact criterion was reached at compliance** and that the uncapped current is unknown. Do not present the compliance-clamped number as a precise physical current or as proof of stable contact from repeated uncapped reads.
- User-corrected grid policy: for grid runs, open/weak-contact or pA/noise-floor after approach is not by itself a skip condition. Run a multi-bias low-compliance contact diagnostic first; if it is voltage-responsive or plausibly high-HRS, continue. If it remains open-like/no-voltage-scaling, move microscope stage Z forward/up by the run's configured bounded contact-edge retry amount (minimum valid step is usually `+0.25`) and repeat the diagnostic. Only run the requested stress measurements after the diagnostic/rescue shows meaningful coupling, unless the user explicitly overrides the gate. Preserve hard stops for short-like/over-current/read-compliance-limited conditions.
- If prior devices in the same run look pre-shorted or over-contacted, soften the next approach instead of continuing with the normal contact window. A validated soft continuation pattern is: precheck at `0 V`, `+10 mV`, `-10 mV`; target `1–20 nA` at `10 mV`; use minimum valid `0.25` stage-Z steps; and lower approach read compliance to about `200 nA`.
- When resuming from an interrupted device, inspect the previous run folder. If alignment exists but `approach.json` is missing, the device was aligned but not contacted: reuse the alignment context only if no movement invalidated it, run a live pre-contact check, then approach if needed. Do not blindly retract/lower or redo XY movement before the live check.
- When the user explicitly asks to restart from device N and delete/overwrite stale data, stop any active runner first, cleanup/verify all six ViPSA machines, then remove/archive device folders and partial-summary entries from the restart boundary onward while preserving completed devices before that boundary. For serpentine traversal, compute the boundary by traversal order, not by naive numeric `device_number >= N`, unless those are equivalent. **The named device N is authoritative**: do not substitute “first missing `DONE.json`” or any earlier unfinished folder for the user's requested redo boundary. Preserve earlier unfinished folders as partial unless the user explicitly asks to backfill them now. **Do not only prune summaries**: stale `device_N/DONE.json` folders after the restart boundary can cause a resume runner to skip measurements even when the user said to re-do them. Archive those stale folders or patch the runner's `DONE.json` skip filter to honor `START_AT_DEVICE`; if the mistake is discovered mid-run, stop at a safe device-finished boundary and restart after archiving skipped folders. After outage-related `RUN_ID_MISMATCH`, use fresh per-command transactions with retry rather than one shared long-lived run id; see `references/grid-resume-stale-data-and-per-command-run-recovery-2026-06-24.md`, `references/overwrite-restart-from-device-boundary-2026-06-26.md`, `references/no-skip-restart-stale-done-skip-recovery-2026-06-30.md`, and `references/explicit-redo-boundary-and-pause-unverified-cleanup-2026-07-01.md`.
- If DCIV after a soft/contact-edge approach shows no meaningful current (for example `max |I| < 5 nA`), run a multi-bias contact diagnostic and a bounded `+0.25` Z rescue before deciding whether a retry is meaningful. Rerun the same-compliance DCIV only if the diagnostic becomes voltage-responsive or plausibly high-HRS/contacted. If it remains open-like/no-voltage-scaling, skip higher-compliance retries and randomized pulses unless explicitly overridden; higher compliance does not fix missing contact and creates misleading stress artifacts. If the DCIV is instead compliance-limited/short-like, stop before pulse testing unless explicitly authorized.
- When the user explicitly overrides skip gates with wording like `do not skip running DCIV/Pulses`, do not leave the safety-gated runner in place. Stop it, archive/prune stale skipped device folders from the restart boundary, patch a no-skip continuation where contact/safety gates become record-only metadata, compile/verify the runner, and resume so DCIV and randomized pulses are attempted for each device while preserving diagnostic warnings and conservative electrical limits.
- Current explicit user override for this 8x8 randomized-pulse grid: even if a device shows overcontact/short-like behavior, still perform DCIV; run an additional reset-only sweep before normal DCIV when overcontact/short-like; and do not skip pulsing solely because DCIV is compliance-limited. Record the override in per-device summaries and plots/logbook entries.

## Pulse Plotting Requirements

When a grid run includes pulse/endurance data:

- Default to clearly labeled per-device plots and whole-grid summaries.
- If the user says not to connect datapoints, enforce scatter-only plotting in code: use `scatter(...)` or `plot(..., linestyle='None', marker='o')`.
- Do not use implicit line plots such as `plot(x, y)` or connected marker styles like `'-o'` for pulse data when scatter-only was requested.
- Treat plotting style requests as part of the measurement deliverable, not cosmetic commentary after the run.

## Measurement Output Expectations

For batch/substrate campaigns, organize the top-level output by durable experiment hierarchy before the run starts, for example `data/probabilistic_computing/batch_<N>/substrate_<S>/runs/<run_name_timestamp>/`, and include `batch` and `substrate` in the run-level summary metadata.

For each device, save or report:

- `device_number`
- target `x,y`
- actual Zaber readback after move
- whether alignment was performed
- whether approach was performed
- final contact/read current and resistance if measured
- electrical test artifacts: CSV/JSON/plots
- cleanup state after the device
- any flags such as open-like, short-like, compliance-limited, good switching, failed approach, skipped, or aborted

For the whole grid, produce a summary table or CSV with one row per device.

## End-of-Run Aggregation and Reporting

After a long grid run completes, do not stop at “process completed.” Actively inspect the run directory and produce the finished artifact package:

1. Read the final per-device summary JSON/CSV and extract compact, user-relevant metrics: completed devices, DCIV/forming yield, best pulse ratio/device, endurance batch counts, short/open/over-contact flags, and skipped/failed reasons.
2. Generate or verify whole-grid category plots when data exists, typically:
   - approach/contact traces for all devices
   - forming/DCIV curves for all devices
   - pulse-optimization read states
   - endurance read states
   - summary metrics/bar plots
3. Make plotting scripts robust: create output directories before writing manifests/stdout files, and write a small plot manifest that maps plot category names to absolute file paths.
4. Verify artifacts before reporting: confirm plot files exist and are non-empty, read back the summary CSV/JSON, check final cleanup (`get_closed_channels() == nil` when available), and report final Zaber/stage positions.
5. Deliver the plots as media attachments and keep the text concise: one summary, a short per-device metric list, cleanup/final-position state, then attachments.

## Common Pitfalls

0. **Delaying or misclassifying per-device reports.**
   - When the user asks for a graph/update after every device measurement, treat per-device delivery as part of the measurement loop.
   - A parent-session `watch_patterns` notification is not a durable per-device reporter: it can disappear when the session closes and cannot reliably deduplicate restarted devices. For unattended runs, use a stateful no-agent cron/poller keyed by run directory + device number, pause it on stop, and verify it is recurring before launch.
   - For long background grid runs, create a stateful poller that watches for `device_XX/DONE.json`, but always parses `summary.json` before wording the update. `DONE.json` is only a terminal-event signal, not proof that electrical measurement occurred.
   - Use status-specific wording: `completed` with expected DCIV/pulse sections means **measurement completed**; `skipped_contact_not_in_window` means **device processed but measurement skipped**; `started` without `finished_utc` means **interrupted/in progress**. Never summarize a range such as “devices 1–5 completed” from `DONE.json` count alone.
   - A skipped-device update should state the final contact current, the required window, and explicitly say that no DCIV/pulses were run. A completed-device update may include contact, DCIV SET/RESET, pulse counts, and the plot. Then identify the currently running device from the newest `status: started` summary without `DONE.json`.
   - If the user asks to analyze and tweak after each device, the poller/loop should also parse the new `summary.json`, append a timestamped failure/tweak entry to `project.md`, and update the next-device protocol at a safe boundary when the failure mode is actionable.
   - Keep a persistent report-state file keyed by run directory and device number so plots/logbook entries are not duplicated after restarts. Pause this reporter immediately when the user stops the runner.
   - For unattended/headless runners, force a non-interactive Matplotlib backend (`MPLBACKEND=Agg` or `matplotlib.use("Agg")`) before importing `pyplot`. A GUI backend can fail with `TclError: couldn't connect to display`, leave `summary.plot`/`DONE.plot` null, and silently prevent media delivery even though the electrical measurement completed. Reporter fallback should regenerate a missing `device_plot.png` headlessly from saved CSV/JSON before sending the update.
   - For a recurring cron reporter, use an explicitly recurring schedule such as `every 1m` and verify the created job says `repeat: forever`; a duration-like `1m` may create a one-shot job.
   - Before launching `python ... | tee <log>`, create the log file's parent directory in the shell *before* the pipeline starts. A runner-side `OUT.mkdir(...)` occurs too late because `tee` opens its output concurrently and may fail even though the measurement continues.

0a. **Letting optional video recording obscure electrical progress or user intent.**
   - If recorder threads use OpenCV (`cv2`), verify the dependency before launching a long recorder-enabled run or make recording optional.
   - Missing recorder dependencies should be reported as a video-recording/setup issue, not as a failed electrical measurement if the device loop and PUDA commands continue.
   - A known setup fix is `python3 -m pip install opencv-python-headless`, followed by a direct `import cv2` verification in the same Python environment used to run the grid script.
   - If the user says `do not record`, immediately stop the active recorder/runner, remove newly-created unwanted video files when appropriate, patch the continuation runner so recording cannot restart, and verify no new `camera*_resume*.mp4` files are created.

0b. **Treating process termination as a completed stop.**
   - `process.kill` / SIGTERM only stops the tracked runner. It does **not** prove the SMU outputs are off, the 707B is open, the light is off, reporters are paused, or all run IDs are cleared.
   - A shell pipeline such as `python runner.py 2>&1 | tee run.log` can leave the Python child or another pipeline member alive after the tracked shell/session is killed. After stopping, search for the runner script name and relevant child processes, terminate the whole remaining process tree/group if present, and repeat the check until no match remains. Prefer launching long hardware runners without an unnecessary shell pipeline, or launch them in a process group whose full lifecycle can be controlled.
   - Delayed `watch_patterns` messages may arrive after a stop and can contain genuine device-finished output buffered before or produced by an orphaned child. Treat them as notifications requiring reconciliation—not proof that the run restarted or remains stopped. Re-check live processes, compare per-device `summary.json` timestamps/statuses against traversal order, identify the first `status: started` device, then run/verify cleanup before reporting.
   - The latest process poll/preview can be stale even without an orphan: a long runner may have completed/skipped several devices while the visible preview still shows an earlier `device_start`. After termination, read the full process log and reconcile it with every new per-device summary before stating the last completed or interrupted device.
   - After a terse `stop`, immediately pause/stop the reporter, kill the runner and any surviving children, run the full six-machine cleanup, inspect the interrupted device summary, and verify outputs off, `get_closed_channels() == nil`, light off, and relevant machines `idle` with `run_id: null` before saying the grid is safely stopped.
   - Never answer only `Operation interrupted.` after killing the runner. If cleanup cannot be verified, say **runner stopped; hardware cleanup unverified** and name the blocker. See `references/stop-grid-runner-reporter-and-unverified-cleanup-2026-07-14.md`.

1. **Confusing numbering with traversal.**
   - CSV numbering is row-major: `1,2,3,4,5,6,...`.
   - Physical traversal is serpentine: e.g. `1,2,3,6,5,4,7,8,9`.

2. **Treating CSV X/Y as relative moves.**
   - They are absolute Zaber positions.

3. **Moving Zaber before raising Z.**
   - Always raise microscope stage Z to safe travel height before X/Y travel.

- Blindly lowering back to contact Z.
   - Lower only to a safe pre-approach height, then approach.
   - Historical contact-Z or fitted-plane predictions are *estimates*, not proof of clearance. After predictive pre-approach, immediately run a live 10 mV contact check. If it is already above the soft window or at approach compliance, retract/cleanup and report over-contact or short-like rather than continuing forward.

4a. **Treating `DONE.json` as proof of completion.**
   - Some runners write `DONE.json` from a `finally` block even when `summary.json` has `status: "error"`.
   - After NATS/connection failures, the remaining traversal devices can be rapidly marked with `DONE.json` plus `ConnectionClosedError()` without approach/DCIV/pulse artifacts.
   - After an intentional stop/SIGTERM, the interrupted device can have mixed artifacts: `DONE.json`, plots, or pulse-summary files may exist while `summary.json` still says `status: "started"` and lacks DCIV/pulse sections. Prefer live runner logs plus `summary.json` status/sections over `DONE.json` alone when reporting the stop point.
   - For retrospective status and restart decisions, count valid measurements by per-device `summary.status == "completed"` and requested artifact presence. Archive or bypass stale error/interrupted `DONE.json` folders before restarting so requested devices are not silently skipped. See `references/done-json-error-artifact-triage-2026-07-01.md` and `references/stop-grid-runner-reporter-and-unverified-cleanup-2026-07-14.md`.

4b. **Misreading killed-process notifications during restarts.**
   - When a stale/background grid process is intentionally killed, Hermes may later receive a completion notification with exit code `-15` (SIGTERM). Do not treat that as the active run failing. Poll the currently active process ID, inspect device `DONE.json` files, and verify live machine states before reporting status.

4b. **Duplicate/stale PUDA subscribers after NATS/internet disruption.**
   - A machine can return `START success` but then reject the queued command with `RUN_ID_MISMATCH` because a stale/duplicate subscriber handled one side of the transaction. For resume scripts, prefer short bounded retries of fresh `start → one command → complete` transactions per machine command, complete any visible stale run IDs, and verify machine states (`idle`, `run_id: null`) before restarting from the first unfinished device.

5. **Skipping contact validation after moving devices.**
   - Each new device needs at least contact verification before electrical stress.

6. **Leaving SMU routed/output-on during travel.**
   - Before movement, force SMU outputs off and open the 707B.

7. **Using millimetres accidentally.**
   - Use native units (`units: null`) unless the user explicitly asks for `mm`.

## Verification Checklist

Before starting grid traversal:

- [ ] CSV exists or has been generated and saved.
- [ ] Grid shape and serpentine traversal order are known.
- [ ] Safe Z raise distance and pre-approach lower distance are known or confirmed.
- [ ] The electrical test sequence is defined.
- [ ] PUDA env and ViPSA machines are responsive.
- [ ] SMU outputs are off and 707B is open before the first move.

For each device:

- [ ] Moved to the correct absolute Zaber X/Y.
- [ ] Contact checked or approach completed.
- [ ] Requested tests executed or safely skipped with reason.
- [ ] Artifacts saved with device number in filenames/metadata.
- [ ] If per-device live reporting was requested: sent `device_plot.png` as `MEDIA:`, summarized analysis/failure classification, recorded a `project.md` log entry, and decided whether the next-device protocol needs a safety/quality tweak.
- [ ] Cleanup verified before travel to next device.

At the end:

- [ ] SMU outputs off.
- [ ] 707B open all and `get_closed_channels() == nil`.
- [ ] Stage/Zaber final positions reported.
- [ ] Grid summary saved and reported.
