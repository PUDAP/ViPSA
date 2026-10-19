# Post-approach one-cycle DCIV + plot-recovery pattern — 2026-06-05

Use this reference for ViPSA memristor DCIV runs immediately after a Keithley-guided contact approach when the user says “do a DCIV sweep, 1 cycle like the previous one.”

## Reused “previous lower-compliance” sweep

The previous one-cycle lower-compliance recipe was:

```text
Path: 0 -> +1 -> 0 -> -2 -> 0 V
Step: 0.05 V
Requested inter-point delay: 0.001 s
Points without duplicate vertices: 121
PF compliance: 1e-6 A
PB compliance: 1e-6 A
NF compliance: 1e-4 A
NB compliance: 1e-6 A
Instrument: Keithley 2450 through 707B Keithley route
```

Run order:

1. Verify Keithley 2450 and 707B are idle.
2. `keithley-2450.set_output(false)` before routing.
3. `keithley-707b.connect_keithley_smu()`.
4. Sweep four segments with branch-specific compliance and branch labels `PF`, `PB`, `NF`, `NB`.
5. Save raw CSV/JSON before plotting when possible.
6. Cleanup in `finally`: Keithley output off, 707B `open_all`, `get_closed_channels`, final states.
7. Plot voltage vs `|Current|` on log scale in original row order, plus a segment-colored plot.

## Plot-recovery lesson

If the sweep succeeds and cleanup completes but the plotting import fails (for example `ModuleNotFoundError: No module named 'matplotlib'` in system Python), do **not** rerun the electrical sweep just to make the plot. Treat the JSON/CSV as authoritative completed measurement artifacts, then generate plots from the saved JSON/CSV in a plotting-capable venv.

Observed working fallback in this environment:

```bash
/tmp/dciv_plot_venv/bin/python - <<'PY'
import json, math, pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p = pathlib.Path('/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_dciv/<dciv_run>.json')
j = json.loads(p.read_text())
s, rows = j['summary'], j['rows']
v_col = s['columns']['voltage']
i_col = s['columns']['current']
positive = [abs(float(r[i_col])) for r in rows if abs(float(r[i_col])) > 0]
floor = min(positive) / 10 if positive else 1e-15
# full-order plot and segment plot, preserving row order
PY
```

Also verify and, if needed, correct summary sanity fields after recovery:

```text
valid_measurement = (len(rows) == sum(segment_lengths.values()))
```

This can catch a reporting artifact where the printed summary showed `valid_measurement: false` even though the saved rows were complete (`121/121`).

## Reporting standard

Report:

- sweep path, step, requested delay, total point count
- branch compliances
- whether row count matches expected points
- compliance-hit flag and cautious SET/RESET interpretation
- ON/OFF/read-current ratios if computed
- cleanup verification: output off, 707B channels `nil`, final states idle
- attach segment plot and raw CSV

Do not overstate timing; requested `0.001 s` is not proof of physical inter-point timing unless buffer timestamps confirm it.
