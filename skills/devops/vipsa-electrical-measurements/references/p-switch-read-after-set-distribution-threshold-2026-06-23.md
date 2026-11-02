# P-switch reanalysis using read-after-SET distribution threshold (2026-06-23)

Use this when the user asks to recompute randomized SET-voltage `P_switch` without a Youden-J/ROC threshold.

## Context

In an 8×8 ViPSA randomized SET-voltage pulse grid, the original analysis chose the read-current threshold by comparing `read_after_set` vs `read_after_reset` currents with Youden's J statistic. The user requested a simpler one-sided threshold: use the distribution of all `read_after_set` currents only, then recompute `P_switch` and sigmoid fits.

## Durable workflow

For each device:

1. Load `randomized_pulse_results.csv`.
2. Select rows where `role == "read_after_set"` and `abs_current_a > 0`.
3. Work in log current space: `x = log10(abs_current_a)`.
4. Choose a threshold from the `read_after_set` distribution only.
   - Practical simple choice used successfully: Otsu-style threshold on the sorted/log histogram or sorted unique log-current values, maximizing between-cluster separation.
   - If the distribution is degenerate/unimodal and no split is meaningful, fall back to a median/log-median threshold and label it clearly as a fallback.
5. Convert threshold back to amps: `threshold_a = 10 ** log_threshold`.
6. For each SET voltage:
   - `attempts = count(read_after_set rows at that SET voltage)`
   - `switches = count(read_after_set abs_current_a >= threshold_a)`
   - `P_switch = switches / attempts`
7. Keep `read_after_reset` only as a sanity/quality check:
   - `reset_high_fraction = count(read_after_reset abs_current_a >= threshold_a) / reset_reads`
   - A high `reset_high_fraction` means high `P_switch` may reflect stuck-high/poor reset rather than clean stochastic SET.
8. Fit a sigmoid to the recomputed probabilities:
   - `P(V) = 1 / (1 + exp(-slope * (V - V50)))`
   - Report `V50`, slope, weighted RMSE, and weighted R² where meaningful.
   - Weight points by attempts per voltage.

## Reporting pattern

Report two rankings if useful:

- **Best mathematical fits**: sorted by low weighted RMSE / high R².
- **Best clean-ish candidates**: require enough trials, increasing sigmoid, lower compliance-hit count, and reasonable `reset_high_fraction`.

Do not overstate `P_switch` as true switching probability when:

- threshold is near noise floor,
- many read pulses hit compliance,
- reset reads often remain above threshold,
- sigmoid fit is good only because probabilities saturate trivially at 0 or 1.

## Minimal Python helper snippets

```python
import numpy as np

def otsu_log_threshold(read_after_set_abs_currents):
    vals = np.array([v for v in read_after_set_abs_currents if v and v > 0], dtype=float)
    logs = np.log10(vals)
    xs = np.sort(np.unique(logs))
    if len(xs) < 2:
        return float(10 ** np.median(logs)), "median_fallback"
    best = None
    for t in (xs[:-1] + xs[1:]) / 2:
        low, high = logs[logs < t], logs[logs >= t]
        if len(low) == 0 or len(high) == 0:
            continue
        w0, w1 = len(low) / len(logs), len(high) / len(logs)
        between = w0 * w1 * (np.mean(low) - np.mean(high)) ** 2
        if best is None or between > best[0]:
            best = (between, t)
    return float(10 ** best[1]), "otsu_log_read_after_set"
```

```python
def p_switch_table(rows, threshold_a):
    out = []
    for sv in sorted({float(r["set_voltage_v"]) for r in rows if r["role"] == "read_after_set"}):
        rs = [r for r in rows if r["role"] == "read_after_set" and float(r["set_voltage_v"]) == sv]
        rr = [r for r in rows if r["role"] == "read_after_reset" and float(r["set_voltage_v"]) == sv]
        switches = sum(float(r["abs_current_a"]) >= threshold_a for r in rs)
        reset_high = sum(float(r["abs_current_a"]) >= threshold_a for r in rr)
        out.append({
            "set_voltage_v": sv,
            "attempts": len(rs),
            "switches": switches,
            "p_switch": switches / len(rs) if rs else None,
            "reset_reads": len(rr),
            "reset_high": reset_high,
            "reset_high_fraction": reset_high / len(rr) if rr else None,
        })
    return out
```
