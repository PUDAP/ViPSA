# Negative voltage sweep cycle plotting and NF threshold extraction

Use this reference when the user provides a CSV containing repeated negative voltage sweeps, for example `0 -> -3 V -> 0`, and asks for NF/NB plotting, removal of positive-voltage data, or threshold voltage vs cycle.

## Workflow

1. Load the CSV with pandas and inspect actual columns. Common columns are `Voltage (V)`, `Current (A)`, and `Cycle Number`.
2. Remove positive-voltage data before analysis. If the task is strictly negative sweeps, filter `Voltage (V) < 0`; if 0 V points are meaningful for the user's plot, use `<= 0` and state the choice.
3. Treat row order as measurement order. Do not sort by voltage.
4. If the raw `Cycle Number` column interleaves contact checks or setup reads, do not assume it equals physical cycle count. Identify real sweep blocks by sufficient row count and a minimum voltage near the requested endpoint, then renumber those blocks as `cycle_no = 1..N`.
5. Split each negative sweep at the first/minimum voltage point:
   - `NF`: start of negative sweep through the minimum voltage point (`0 -> -Vmax`); plot as a solid line.
   - `NB`: rows after the minimum voltage point through return toward zero (`-Vmax -> 0`); plot as a dashed line.
6. Use a color gradient across successive cycles. Use the same color for NF/NB of the same cycle; branch identity is line style.
7. For negative currents on a log plot, plot `abs(Current)` and label the axis `|Current| (A)`. Preserve signed current in output CSV and optionally make a separate signed-current plot if useful.
8. Save machine-readable outputs:
   - cleaned/split CSV with `cycle_no`, `branch`, and `abs_current_A`
   - threshold CSV with `cycle_no`, raw cycle identifier if available, threshold criterion, and extracted `vth_nf_V`

## Threshold voltage extraction from NF

If the user does not specify a threshold definition, use a clearly stated practical default: first NF crossing of `|I| >= 1e-3 A` with log-current interpolation between adjacent points. Put the threshold criterion in the plot title and final response.

```python
threshold_current_A = 1e-3
crossing_idx = np.flatnonzero(nf['Current (A)'].abs().to_numpy() >= threshold_current_A)
if len(crossing_idx):
    k = int(crossing_idx[0])
    if k == 0:
        vth = float(nf['Voltage (V)'].iloc[k])
    else:
        v1, v2 = nf['Voltage (V)'].iloc[k-1], nf['Voltage (V)'].iloc[k]
        i1, i2 = nf['Current (A)'].abs().iloc[k-1], nf['Current (A)'].abs().iloc[k]
        x1, x2, xt = np.log10(i1), np.log10(i2), np.log10(threshold_current_A)
        vth = float(v1 + (xt - x1) * (v2 - v1) / (x2 - x1))
else:
    vth = np.nan
```

## Plotting details

- Use `matplotlib.use('Agg')` before importing `pyplot` in headless environments.
- Use a perceptually ordered colormap such as `viridis` and add a cycle-number colorbar.
- Include legend proxies for line styles: `NF` solid and `NB` dashed.
- Return requested plots via `MEDIA:` and include concise sanity fields: detected cycles, retained rows, threshold criterion, and output CSV paths.

## Pitfalls

- Raw `Cycle Number` may include short 0 V / positive contact-check blocks; filter and renumber actual negative sweeps.
- Do not plot signed negative currents directly on a logarithmic y-axis.
- Do not silently invent a threshold criterion. If not specified, state the default (for example `|I| >= 1 mA`).
- Do not rerun measurements to regenerate plots when the CSV already contains the needed data; analyze saved data only.