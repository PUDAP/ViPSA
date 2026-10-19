# Grid-trial orchestration: mid-run parameter changes and live updates

Session lesson from a 3x3 ViPSA grid trial where devices are traversed with Z safe retract, Zaber XY moves, contact approach, resistance check, DCIV forming, pulse optimization, and optional endurance.

## Mid-run approach-threshold change

If the user asks to change approach thresholds while a long grid trial is running:

1. Do **not** let the old process continue with stale thresholds.
2. Stop the tracked background process cleanly.
3. Immediately run electrical cleanup:
   - `keithley-2450.set_output(false)`
   - `keysight-b2902b.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`; expected safe value is `nil` / no channels.
4. Verify all involved machines are idle before resuming.
5. Start a resume script that loads the existing run summary, preserves terminal device records, drops only non-terminal/in-progress records, updates `summary['params']['approach']`, and continues the same serpentine order from unfinished devices.
6. Add a note in the summary that the threshold change applies only from the resumed/subsequent devices onward.

This avoids mixing stale thresholds with new user instructions and avoids rerunning already-completed devices.

## Live-update preference

When providing live Telegram updates for long grid trials, do **not** spam every approach-loop micro-step. The user explicitly objected to per-step approach updates.

Report these live:
- device-level status changes
- coarse travel / target-device moves
- resistance check start/result
- DCIV start/completion
- pulse optimization/endurance start/completion
- final approach status/result

Suppress or batch these unless explicitly requested:
- `approach read N`
- `approach forward N`
- `approach retract trim N`

A good pattern is a script-only cron updater that tracks newly observed protocol files and summary CSV status changes, but filters approach-loop protocol descriptions before delivery.

## Plotting completed devices during a running grid trial

When asked to plot DCIV curves for completed devices so far:

1. Read the grid summary and include devices with `status == completed` that have a `device_<n>_forming_dciv.csv` file.
2. Preserve measurement order; do not sort by voltage.
3. Plot `Voltage` vs log-scale `|Current|`.
4. Use subplots or a clearly labeled combined image for the completed device set.
5. Save the image in the run folder and return it as `MEDIA:<path>`.
