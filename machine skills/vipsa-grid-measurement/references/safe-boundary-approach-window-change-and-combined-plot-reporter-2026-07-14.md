# Safe-boundary approach-window change + combined per-device plot reports — 2026-07-14

## When this applies

Use this reference for active ViPSA grid continuations where the user changes the approach contact-current window mid-run and wants per-device reports containing a single figure that combines the main device plots.

Concrete session: S1 7×7 overwrite continuation from device 6 was running. User changed the approach window from `1e-9–1e-8 A` to `5e-9–5e-8 A` at `0.1 V` while device 15 was already in progress, and asked for a report with one combined 4-plot figure after every device.

## Approach-window change at safe boundary

1. **Inspect live state first.** Poll the active runner and inspect the active run directory for the `summary.json` whose `status` is `started` and lacks `DONE.json`. Do not assume the previous device in chat is still active.
2. **Do not claim a mid-device threshold change is active.** If a device is already in approach/measurement, schedule the change at the next safe boundary unless the user explicitly asks to abort/retry the current device.
3. **Patch a new continuation runner rather than editing only the running process.** Update all relevant places together:
   - `START_AT_DEVICE=<next traversal device>`
   - `APPROACH_LOWER_A=<new lower>`
   - `APPROACH_UPPER_A=<new upper>`
   - run-summary metadata for `approach.lower_a` / `approach.upper_a`
   - any first-device/manual-handoff branch so a non-device-6 restart follows normal travel/alignment/approach logic, not the old device-6 handoff path.
4. **Compile-check the patched runner** before launching any watcher.
5. **Use a watcher for the safe boundary:** wait for the current device's `DONE.json`, then terminate only the old measurement runner, not monitor crons/reporters.
6. **Cleanup before restart:** turn light off, force Keithley/Keysight outputs off, `keithley-707b.open_all()`, verify `get_closed_channels == nil` when available.
7. **Archive/prune from the restart boundary:** move any pre-created `device_N+` folders into `archive_before_threshold_restart_deviceN_<UTC>`, and prune `summary.partial.json`/`summary.json` entries for devices at/after the boundary.
8. **Start the patched runner as a fresh background process** and write a state file with the new PID, runner path, log path, thresholds, and `START_AT_DEVICE`.
9. **Interpret SIGTERM correctly:** the old runner exiting with code `143`/SIGTERM after the watcher kills it is expected. Verify the new runner PID and the newly-started device summary before reporting failure/success.

## Per-device combined 4-panel figure reporter

When the user asks for a report/figure after every device, create a `no_agent=True` cron reporter that watches new `device_*/DONE.json` files and stays silent when no new device is done. Initialize its state with already-completed device folders to avoid replay.

The combined figure should be a single `combined_4plots.png` with:

1. DCIV `Voltage` vs log `|I|`, preserving row order and segment labels.
2. Approach trace: `net_z` vs log `|I|`, with the approach terminal status in the subplot title.
3. Randomized pulse read currents: scatter-only `read_after_set` and `read_after_reset` vs pulse index.
4. Switching probability: scatter-only `P(switch)` and `reset_high_fraction` vs SET voltage.

The reporter message should be concise:

```text
✅ Device N measurement finished: <status>
👇 approach: <status>, |I|=<...> A, ΔZ=<...>
DCIV: max |I|=<...> A, SET=<...>, RESET=<...>
pulses: trains=<...>, stop=<...>
MEDIA:<absolute path>/combined_4plots.png
```

## Pitfalls

- Do not edit the already-running Python process and imply it changed; running constants are fixed in memory.
- Do not restart from naive numeric order if the run uses serpentine traversal; slice the traversal list at the requested boundary device.
- Do not leave a partial `device_N` folder created by the old runner at the restart boundary. Archive it before launching the patched runner so the fresh device artifacts prove the new threshold was used.
- Do not treat the old process's expected SIGTERM notification as a failed measurement if the watcher deliberately stopped it after a completed device.
- If the combined plot is regenerated from saved CSV/JSON, do not rerun hardware. Plot from artifacts only.
