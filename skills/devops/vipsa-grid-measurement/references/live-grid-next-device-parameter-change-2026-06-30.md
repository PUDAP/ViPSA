# Live grid run: safe-boundary parameter changes for remaining devices (2026-06-30)

Use this pattern when a long ViPSA grid run is already active and the user asks to change an electrical parameter such as compliance current or reset-side voltage **for the next device onward**.

## Trigger phrases

- “increase the compliance to ... and re-do the test”
- “from the next device change the reset side of the sweep to ...”
- “after this device, use ...”
- “restart from device N with ...”

## Pattern

1. Identify the active runner, log file, run directory, current device, and the newest `summary.partial.json` / per-device `DONE.json` state. Do not assume the compacted/session summary is current.
2. Decide the safe boundary:
   - If the user says “re-do the test” for the current device, finish/stop at a safe cleanup point, archive/delete the current partial device folder, prune the partial summary for that device, and rerun that device with the new parameter.
   - If the user says “from the next device,” do **not** interrupt the device in progress mid-measurement. Watch for the current device `DONE.json`, then stop/restart from the next traversal device.
3. Patch the continuation runner constants and metadata together. Examples:
   - compliance change: patch the actual instrument compliance used in `hold_voltage_measure_current` / pulse commands, plus run/device metadata fields.
   - reset-side voltage change: patch the DCIV builder default (e.g. `reset_v=-1.2`), generated negative branch endpoint, path string, and metadata such as `next_reset_voltage_v`.
4. Compile or syntax-check the patched runner before starting a watcher/restart.
5. Use a small watcher script for safe-boundary restarts:
   - wait for the boundary device `DONE.json` or the requested stopped/cleanup state;
   - terminate only the old measurement process, not unrelated monitor crons;
   - force SMU output off and `707B.open_all()`;
   - verify closed channels are nil/no channels;
   - archive/delete stale partial folders from the restart device onward and prune partial summaries;
   - launch the patched runner as a tracked background process.
6. Patch no-agent per-device reporters/cron state only if needed so old devices are not replayed and new plots still arrive.
7. Append a concise `project.md` log entry with UTC time, boundary device, changed parameter values, and watcher/runner filenames.
8. Report verified state concisely: current device, boundary, new parameter values, process/session ID, and what cleanup/restart action the watcher will perform.

## Pitfalls

- Do not blindly replace text like `5000` or `1e-4` across a grid runner; values may also represent grid spacing, pulse budgets, read compliances, or metadata. Patch named constants and specific code paths only.
- Do not claim the new parameter is already in effect on the device currently running unless that device was actually restarted with the patched runner.
- For reset-side changes, preserve the negative sign and verify generated DCIV `NF`/`NB` branches are non-empty.
- Preserve the user's existing approach/contact policy, no-skip overrides, scatter-only plotting preference, and per-device reporter behavior unless the user explicitly changes them.
