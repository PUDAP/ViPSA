# Per-device live analysis, logbook updates, and adaptive protocol tweaks (2026-06-22)

Context: During an 8x8 ViPSA grid run resumed from device 5, the user explicitly requested plots and analysis after each device finishes, failures added to the logbook, and protocol tweaks based on the observed failure mode.

## Pattern to reuse

1. Treat per-device reporting as part of the measurement loop, not an end-of-run task.
   - When `device_XX/DONE.json` and `summary.json` appear, inspect them immediately.
   - Send `device_plot.png` as `MEDIA:/absolute/path` if present.
   - Include concise analysis: pre-contact status, approach final current/Z, DCIV max `|I|`, compliance hits by PF/PB/NF/NB, pulse count/trials, pulse compliance flags, threshold accuracy/sigmoid fit if present.
2. Maintain a small state file for duplicate suppression, e.g. `runs/.grid_per_device_reported.json`, keyed by `run_dir:device_number`.
3. Append one timestamped line to `project.md` Logs for each device with:
   - failure classification (`open-like`, `short/over-contact`, `DCIV compliance-limited`, `pulse compliance-limited`, `skipped by safety gate`),
   - artifact links to `device_plot.png` and `summary.json`,
   - the chosen protocol tweak for following devices.
4. For long background runs, create a short poller/cron monitor that watches for new completed device directories and reports only new devices. Keep the monitor self-contained because scheduled jobs run without chat context.
5. If a running continuation is using now-known-aggressive settings, do not kill hardware mid-command blindly. First verify/clean up machines when safe, then restart from the next unfinished device with tweaked parameters.

## Adaptive tweak examples from this session

- Device 5: soft approach reached contact-window current (`~1.13 nA` at 10 mV) but DCIV became strongly compliance-limited (`max |I| ~10 µA`, PF/PB/NF/NB hits `15/18/6/4`). Pulses were skipped. Tweak: keep the softer `1–20 nA` approach, reduce positive/forming DCIV compliance from `1 µA` toward `300 nA`, and early-stop PF if `+50–100 mV` is already compliance-limited.
- Device 6: DCIV still showed positive-side compliance hits and the pulse run collected `100 pulses / 25 trials` with heavy pulse compliance flags (`50`). Tweak: lower pulse compliance and cap the randomized SET voltage range for subsequent devices.

## Reporting style

Keep messages compact and hardware-grounded:

- one short device analysis block,
- explicit failure classification,
- explicit protocol tweak,
- `MEDIA:` plot attachment,
- cleanup/restart state only when relevant.

Avoid waiting until the full grid completes when the user asked for per-device plots/analysis.