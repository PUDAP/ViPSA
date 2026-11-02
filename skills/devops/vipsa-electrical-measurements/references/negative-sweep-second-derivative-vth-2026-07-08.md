# Negative-sweep Vth from second derivative (2026-07-08)

Use this when analyzing repeated negative sweeps such as `0 -> -Vmax -> 0` and the user asks for a derivative-based threshold instead of a fixed current-crossing threshold.

## Trigger

- User asks to calculate/recalculate `Vth` with the **2nd derivative**.
- User asks to re-plot Vth and says to put **absolute voltage** on the y-axis.

## Data preparation

1. Load the saved CSV; do **not** rerun hardware just to replot.
2. Keep only negative-voltage rows:
   ```python
   neg = df[df["Voltage (V)"] < 0]
   ```
3. Group by raw `Cycle Number`, but renumber plotted cycles from the real negative sweeps because raw cycle numbers may include setup/contact-check rows.
4. Split each negative sweep at the minimum voltage point:
   - `NF`: first row through min-voltage row (`0 -> -Vmax`)
   - `NB`: remaining rows (`-Vmax -> 0`)
5. Compute the threshold on the **NF branch only** unless the user explicitly asks otherwise.

## 2nd derivative Vth algorithm

For each NF branch:

```python
x = abs(voltage_v)                 # monotonic positive voltage magnitude
y = log10(abs(current_a))          # current magnitude on log scale
y_smooth = moving_average(y, 5)    # small odd window to suppress point noise
first = gradient(y_smooth, x)
second = gradient(first, x)
ignore a few endpoint samples
k = argmax(second)
vth_abs = x[k]
vth_signed_nf = -x[k]
```

Report clearly:

- `vth_abs_V` — preferred for the user’s requested plot y-axis (`|Vth|`)
- `vth_signed_nf_V` — signed negative-forward voltage, useful for traceability
- derivative method and smoothing window

## Plotting rule

For the second/Vth graph requested by the user:

- x-axis: cycle number
- y-axis: `|NF threshold voltage|, |Vth| (V)`
- title should state the criterion: `max 2nd derivative of log10(|I|) vs |V|`
- save the derivative Vth CSV next to the plot and return the PNG via `MEDIA:`

## Caveats

- This differs from fixed-current thresholding such as `first |I| >= 1 mA`; do not mix the two methods without labeling them.
- The result depends on the smoothing window and sampling density.
- Avoid endpoint artifacts by excluding at least 2 points at each end of the derivative array.
