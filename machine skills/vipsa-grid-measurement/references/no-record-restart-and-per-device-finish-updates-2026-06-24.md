# No-record grid restart + per-device finish updates — 2026-06-24

## When this applies

Use this reference for long ViPSA grid runs where the user asks to stop/avoid recording and wants a message after each device measurement finishes.

## No-record correction pattern

If the user says `do not record` during a grid/resume run:

1. Stop the active runner/recorder process first; treat continued video writing as the immediate side effect to halt.
2. Clean up hardware before restart:
   - SMU outputs off (`keithley-2450`, Keysight if used)
   - Keithley 707B `open_all`, verify closed channels `nil` when available
   - light off unless explicitly kept on
   - clear/verify stale `stage` run id if the stopped process left one active
3. Delete newly-created unwanted video artifacts when the request clearly means no recording should remain.
4. Patch the continuation runner so recorder/video threads are disabled entirely before restarting.
5. Verify the restarted process creates no new `camera*_resume*.mp4` files.

Do not merely say recording will be skipped later; act on the live process and verify no files are being produced.

## Per-device finish update monitor pattern

For long background grid runs, create/resume a `cronjob` no-agent script-only monitor that watches for new `device_*/DONE.json` files and prints only when a new device appears. Empty stdout must mean silent/no update.

Recommended state file pattern:

- Store state under `~/.hermes/state/<run-or-campaign>_device_status_monitor.json`.
- Key by absolute run directory and device directory name.
- Initialize `sent` with already-completed `device_*` folders before enabling the monitor, so old device reports are not replayed.
- On each tick, scan `device_*/DONE.json` sorted by device directory and emit exactly one concise update per newly completed device.

Recommended update content:

- `✅ Device N measurement finished: <status>`
- target row/col/x/y if available
- approach summary (`👇`, final current, ΔZ) if `approach.json` contains it
- DCIV summary (Vset, max |I|, flags) if available
- randomized pulse summary (trains/pulses, threshold, V50, best switching probability) if available
- attach a per-device figure as `MEDIA:<absolute path>` when it exists and is non-empty.

For runs where the user asks for a report/figure after **every** device, prefer generating one combined per-device report figure rather than sending several separate plots. A useful 2×2 layout is:

1. DCIV `|I|` vs voltage, preserving sweep row order and segment labels.
2. Approach trace: `|I|` vs net Z steps.
3. Randomized pulse read currents: read-after-SET/read-after-RESET scatter on log scale.
4. Switching probability: `P(switch)` and reset-high fraction vs SET voltage.

Save it as `combined_4plots.png` in each `device_##` folder and attach that file in the monitor message. Keep separate detailed PNGs available, but do not spam them unless the user asks.

Cron setup:

- Prefer `no_agent=True` with the script producing the exact message text.
- Put scripts under `~/.hermes/scripts/`, but pass the scheduler a path relative to that directory (for example `script="vipsa_s1_7x7_device_reporter.py"`), not an absolute path.
- Schedule `every 1m` for near-live updates; Hermes cron duration syntax does not accept `30s`.
- Keep older duplicate reporter jobs paused to avoid duplicate Telegram updates.

## Pitfalls

- Do not restart a long measurement run just to add reporting unless the runner is already stopped or at a safe boundary. A filesystem/DONE-file monitor can be enabled independently.
- Do not report archived device folders as new completions; monitor only the active run directory unless the user asks for archive review.
- If `summary.json` is stale or only says `status: started`, read sidecar files (`approach.json`, `dciv.json`, `randomized_pulse_summary.json`, `DONE.json`) for the actual completion summary.
- For terse status questions, distinguish **current running device** from **last tested/completed device**. Current running is the `device_##/summary.json` with `status: started` and no `DONE.json`/`finished_utc`; last tested is the completed device with the latest `finished_utc`, not necessarily the numerically highest device because serpentine traversal can go `7 → 14 → 13 ...`.
