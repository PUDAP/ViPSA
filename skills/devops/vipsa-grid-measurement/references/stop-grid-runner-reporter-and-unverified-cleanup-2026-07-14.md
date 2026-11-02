# Stop active grid runner: reporter pause, artifact triage, and unverified cleanup

Use this pattern when the user says to stop/pause an active ViPSA grid measurement.

## What happened

- Active tracked grid process was killed successfully (`SIGTERM`, exit `-15`).
- Two active per-device reporter cron jobs were also paused so they would not keep sending stale or duplicate device-finished messages after the measurement process stopped.
- PUDA state reads for the six ViPSA machines reported `idle` / `run_id: null`, but protocol and direct-NATS cleanup commands (`SMU set_output(false)`, `707B.open_all()`, `get_closed_channels()`, `light.turn_off()`) did not return confirmed START/queue responses.
- The interrupted device had inconsistent artifacts: the live runner log showed device 9 stopped after approach/no-contact, `summary.json` still had `status: started` and no DCIV/pulse keys, while stale/side-effect files like `DONE.json`, `dciv.json`, or `randomized_pulse_summary.json` could exist and imply more progress than the authoritative per-device summary.

## Reusable stop procedure

1. List tracked processes and identify the active grid runner by command/path.
2. Kill the runner via Hermes `process.kill` or the tracked process manager; confirm it exits (`-15` is expected for intentional SIGTERM).
3. List cron jobs and pause any active per-device reporter/poller jobs for the same run before reporting completion.
4. Verify no grid runner or helper process remains active.
5. Run electrical cleanup if possible:
   - Keithley output off.
   - Keysight output off.
   - 707B `open_all()` then `get_closed_channels()`.
   - Light off unless the user asked to keep it on.
6. If cleanup command responses timeout or produce no START/queue response, do **not** claim outputs are verified safe. Report:
   - process stopped,
   - reporters paused,
   - machine state snapshots if available,
   - cleanup command verification blocked/unverified.
7. Inspect the active run folder for the last completed and interrupted devices. Prefer, in order:
   - live runner log events,
   - per-device `summary.json` status and presence/absence of measurement keys,
   - `summary.partial.json` entries,
   - requested raw measurement artifacts.
   Treat `DONE.json` alone as non-authoritative when the process was interrupted.

## Artifact interpretation pitfall

After a killed/interrupted runner, do not rely on `DONE.json` or a generated plot alone. A device may have:

- `summary.json` still `status: started`,
- approach results saved,
- no DCIV/pulse data in `summary.json`,
- but stale or partially generated `DONE.json` / plot / pulse summary files present.

Report the device as interrupted/partial unless `summary.json` says `completed` and contains the expected measurement sections. For restart planning, archive/prune from the interrupted device boundary as needed so stale `DONE.json` files cannot skip requested measurements.
