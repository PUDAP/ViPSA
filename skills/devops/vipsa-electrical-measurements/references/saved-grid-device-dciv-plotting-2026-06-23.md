# Saved grid-device DCIV plotting from completed run folders (2026-06-23)

## Trigger
Use when the user asks to plot a DCIV for a completed device in an in-progress or recently completed ViPSA grid run, e.g. "Plot the DCIV for device 1".

## Workflow
1. Do **not** rerun electrical hardware measurements. Plot from the existing saved `device_##/dciv.csv` or `dciv.json`.
2. Preserve sweep row order. Do not sort by voltage.
3. Use voltage vs `abs(current)` on a log y-axis as the primary plot.
4. If the CSV has a `segment` column, plot one line per segment and keep the original segment names in the legend.
5. Add compliance reference lines when a `compliance_a` column exists.
6. Add a small point-index vs voltage subplot when helpful, so the user can see the actual sweep path and branch ordering.
7. Save the generated plot into the device folder with a clear filename such as `device_01_dciv_plot.png` and return it via `MEDIA:`.

## Robust plotting fallback
If the default Python lacks pandas or matplotlib, do not stop and do not rerun the measurement. Use an existing plotting-capable environment (for example the ViPSA/OpenCV venv if it has matplotlib), and parse the CSV with Python stdlib `csv` if pandas is missing.

Minimal pattern:

```python
import csv, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p = Path('/path/to/device_01')
rows = []
with (p / 'dciv.csv').open() as f:
    for r in csv.DictReader(f):
        rows.append({
            'point_index': int(r['point_index']),
            'segment': r.get('segment', 'sweep'),
            'voltage_v': float(r['voltage_v']),
            'current_a': float(r['current_a']),
            'abs_current_a': abs(float(r.get('abs_current_a') or r['current_a'])),
            'compliance_a': float(r['compliance_a']) if r.get('compliance_a') else float('nan'),
        })

positives = [r['abs_current_a'] for r in rows if r['abs_current_a'] > 0]
floor = min(positives) / 10 if positives else 1e-15
segments = []
for r in rows:
    if not segments or segments[-1] != r['segment']:
        segments.append(r['segment'])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), dpi=180,
                               gridspec_kw={'height_ratios': [3, 1.15]},
                               constrained_layout=True)
for seg in segments:
    rs = [r for r in rows if r['segment'] == seg]
    ax1.plot([r['voltage_v'] for r in rs],
             [r['abs_current_a'] if r['abs_current_a'] > 0 else floor for r in rs],
             marker='o', markersize=2.5, linewidth=1.2, label=seg)
    ax2.plot([r['point_index'] for r in rs], [r['voltage_v'] for r in rs],
             marker='.', markersize=2.5, linewidth=1.0, label=seg)

ax1.set_yscale('log')
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel('|Current| (A), log scale')
ax1.grid(True, which='both', alpha=0.25)
ax1.legend(fontsize=7, ncol=3)

for c in sorted({round(r['compliance_a'], 12) for r in rows if math.isfinite(r['compliance_a'])}):
    ax1.axhline(c, color='gray', linestyle='--', linewidth=0.7, alpha=0.35)

ax2.set_xlabel('Point index')
ax2.set_ylabel('Voltage (V)')
ax2.grid(True, alpha=0.25)

out = p / 'device_01_dciv_plot.png'
fig.savefig(out, bbox_inches='tight')
print(out)
```

## Reporting
Keep the reply concise and attach the image. Include a few sanity fields only:
- point count
- max `|I|`
- compliance-near point count, if computed
- segment names

Example:

```text
Plotted Device 1 DCIV from saved data.
- Points: 182
- Max |I|: 25 µA
- Compliance-near points: 89
- Segments: PF1, PF2, PB, NF, NB, RESET_RECOVERY

MEDIA:/.../device_01_dciv_plot.png
```
