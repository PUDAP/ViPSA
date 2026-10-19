# Negative-sweep Vth via second derivative and absolute-voltage plot (2026-07-13)

Trigger: user asks to replace a fixed current-threshold Vth with a derivative-based Vth for repeated negative sweeps and to plot absolute voltage on the y-axis.

Validated method for repeated `0 -> -Vmax -> 0` sweeps:

1. Keep only real negative-voltage sweep rows (`Voltage (V) < 0`), dropping setup/contact-check rows.
2. Group by raw `Cycle Number`, then renumber valid sweeps sequentially if raw cycle numbers include setup/readback rows.
3. Split each negative sweep at the minimum voltage:
   - `NF`: from near `0` down to the most negative voltage.
   - `NB`: from the most negative voltage back toward `0`.
4. For Vth extraction, use `NF` only unless the user asks otherwise.
5. Convert to absolute-voltage domain:

```python
x = abs(Voltage_V)
y = log10(abs(Current_A))
```

6. Smooth `y` lightly before differentiating (validated: 5-point moving average).
7. Compute numerical derivatives vs `x`:

```python
d1 = np.gradient(y_smooth, x)
d2 = np.gradient(d1, x)
```

8. Define `|Vth|` as the `x` where `d2` is maximum, excluding a small number of edge points to avoid endpoint artifacts.
9. Plot threshold versus cycle with **absolute voltage on the y-axis**: `cycle_no` on x, `|Vth| (V)` on y. Store signed NF voltage separately as `vth_signed_nf_V = -abs_vth` if needed.

Reporting language:

- Say this is a **2nd-derivative maximum of log-current vs |voltage|**, not the previous 1 mA crossing criterion.
- Include smoothing/window details because derivative-based Vth can shift with smoothing and sampling density.
- For user-facing plots, label the axis clearly as `|NF threshold voltage|, |Vth| (V)`.

Pitfall: do not keep plotting negative signed voltage on the y-axis after the user asks for absolute voltage; save signed values in CSV/metadata but show `|Vth|` in the graph.