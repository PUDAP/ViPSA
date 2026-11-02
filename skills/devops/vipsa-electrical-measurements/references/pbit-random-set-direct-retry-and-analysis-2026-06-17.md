# P-bit-like random SET-voltage pulse test: direct retry + analysis lessons (2026-06-17)

Use this when running a stochastic/p-bit-style ViPSA pulse experiment with randomized `SET -> read -> RESET -> read` trials and the normal `puda protocol run` path is blocked, but the user explicitly wants the pulse test retried after the relevant edge is running.

## Experiment pattern

- Generate a CSV before hardware execution with one row per pulse.
- Trial shape: `SET`, `read_after_set`, `RESET`, `read_after_reset`.
- For the tested p-bit screen, SET voltages were `0.20..0.90 V` in `0.05 V` increments, `25` repeats per SET voltage, randomized trial order, `0.1 V` read, `10 ms` pulse width, `10 uA` compliance.
- Preserve columns sufficient to reconstruct trials: pulse index, trial order/index, repeat index per voltage, phase, voltage, set voltage, pulse width, compliance, measured current, abs current, compliance flag.

## Direct-NATS retry pattern when protocol runner cannot connect cleanly

Protocol-first remains the default. If `puda protocol run` fails due to a protocol-runner/NATS routing issue after the user has fixed/restarted the edge and explicitly asks to retry, a direct core-NATS fallback can execute the same command sequence safely:

1. Connect to the known ViPSA NATS servers, often trying `4223` before `4224`/`4222` if the CLI is routing through a stale endpoint.
2. Subscribe to both immediate and queue response subjects for `keysight-b2902b` and `keithley-707b`.
3. Send `start` to both machines with a fresh shared `run_id`; accept only success or the known same-run duplicate-start mismatch.
4. Command sequence:
   - `keysight-b2902b.set_output(enabled=False)`
   - `keithley-707b.connect_keysight_smu()`
   - one or more `keysight-b2902b.run_voltage_pulse_train(...)` commands
   - `keysight-b2902b.set_output(enabled=False)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`
   - `complete` for both machines
5. Always run cleanup attempts in `finally`: Keysight output off, 707B open_all, get_closed_channels, complete.

## Chunk long pulse trains

A single 1500-voltage payload can cause direct-NATS flush/response problems or oversized practical responses. Chunk long lists while keeping the route open:

- Example chunk: `50` full trials = `200` pulses per `run_voltage_pulse_train` command.
- Concatenate the returned current lists in the same order as the original CSV rows.
- Verify the parsed current count equals the CSV pulse-row count before analysis.

## Current parsing pitfall

Keysight/SMU responses may include aliases for the same reading, e.g. both `I_meas (A)` and `Current (A)`. Do not count both. When recursively parsing returned payloads, prefer one current field per reading, in order such as:

1. `I_meas (A)`
2. `Current (A)`
3. `current_A`
4. `current`
5. `I`

If parsed current count is exactly double the expected pulse count, suspect alias double-counting before rerunning hardware.

## Thresholding and probability analysis

For p-bit switching probability, do not blindly use a k-means threshold on all read currents. If zero/noise-floor points exist, k-means may only separate noise-floor readings from measurable sub-nA readings and make almost every read look switched.

Recommended analysis:

1. Plot histogram of `log10(abs(read current))` for `read_after_set` and `read_after_reset` separately.
2. Compute a discriminating threshold between the two read distributions, e.g. ROC/Youden threshold: maximize `TPR_SET - FPR_RESET` using `read_after_set` as positives and `read_after_reset` as negatives.
3. Report the threshold quality: classification accuracy, SET true-positive fraction, RESET false-positive fraction. If distributions overlap strongly, say the threshold is weak and probabilities are threshold-dependent.
4. Probability per SET voltage: `P_switch(V) = count(read_after_set_abs >= threshold) / attempts`.
5. Also report/reset sanity: reset-high fraction per voltage. High reset-high fractions mean RESET is not reliably returning to HRS.

## Sigmoid fit

Fit the binomial logistic model:

```text
P(switch | Vset) = 1 / (1 + exp(-(beta0 + beta1 * Vset)))
```

Report:

- `beta0`
- `beta1_per_v`
- standard errors when available
- `V50 = -beta0 / beta1`
- fitted probability overlay on measured binomial probabilities

Caution: if the measured probabilities saturate at all 0 or all 1, or the threshold is not physically meaningful, the sigmoid beta values may be numerically fit but scientifically weak. Label this explicitly.

## Reporting standard

Include:

- raw pulse CSV path
- classified read CSV path
- probability CSV path
- summary JSON path
- plot PNG/PDF paths
- compliance-hit count
- cleanup verification: Keysight output off, 707B open all, closed channels `nil`
- whether read distributions were cleanly bimodal or overlapping
