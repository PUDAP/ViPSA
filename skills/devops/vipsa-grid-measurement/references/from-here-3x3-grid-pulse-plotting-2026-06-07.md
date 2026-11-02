# From-current-position 3x3 grid with thresholded approach and scatter-only pulse plots

Session pattern captured from a user request to make a 3x3 grid starting at the current Zaber position, perform the grid measurement, use explicit approach thresholds, and plot pulse data without connecting lines.

## Reusable workflow details

- Interpret “from here” as: read current Zaber X/Y and use that absolute position as device 1 / grid origin.
- Generate row-major device numbering, but traverse physically in serpentine order to minimize X/Y travel.
  - For 3x3: `1,2,3,6,5,4,7,8,9`.
- If the user gives approach thresholds, pass them through exactly into the Keithley-guided approach/contact logic.
  - Example thresholds from this session: lower `1e-9 A`, upper `5e-8 A`.
- For pulse plots, honor plotting style requirements in the plotting code itself, not just in the report.
  - “Do not connect the datapoints by a line” means use point markers/scatter only, e.g. Matplotlib `scatter(...)` or `plot(..., linestyle='None', marker='o')`.
  - Do not use `plot(..., '-o')`, default line plots, or any implicit line style for pulse/endurance data when this is requested.
- For long grid runs, start a tracked background process with completion notification and immediately report the run folder, summary CSV path, traversal order, and process/session id.

## Output/reporting pattern

Concise start report should include:

- grid origin/readback
- spacing and shape
- traversal order
- approach thresholds
- pulse plotting style
- background process id
- run folder and live summary CSV path
- current device/status if already known

Concise completion report should be backed by file readback, not just process exit:

- Read final `grid_trial_summary.csv` / `.json` and compute a compact yield summary.
- Report `completed/total`, DCIV good count, best pulse-ratio device, endurance-batch counts, cleanup state, final Zaber, and final stage.
- Attach the all-category plot files after verifying they exist and are non-empty.
- If using a watcher/helper script, create the output directory before redirecting stdout/stderr or writing `plot_manifest.json`; otherwise the watcher can fail after the measurement succeeds.

Example final plot categories from this session:

- `01_approach_traces_all_9_devices.png`
- `02_forming_dciv_all_9_devices.png`
- `03_pulse_optimization_read_states_all_9_devices.png`
- `04_endurance_read_states_all_9_devices.png`
- `05_summary_metrics_all_9_devices.png`
