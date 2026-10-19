# Retrospective Grid Electrical-Logic Recall (2026-06-26)

Use this reference when the user asks what the electrical testing logic was for the *last* or recent ViPSA grid measurement. The lesson is procedural: answer from the actual runner script and summary artifacts, not from the high-level memory of the experiment.

## What to inspect

1. Locate the active/latest run folder under the durable experiment hierarchy, usually:
   - `data/probabilistic_computing/batch_<N>/substrate_<S>/runs/<run_name>/`
2. Read the run-level `summary.json` or `summary.partial.json` for declared parameters and completed-device summaries.
3. Read the actual runner script in `/home/vipsa/vipsa-puda-project/runs/` when available, especially the latest resume/continuation script. The executed code may be more authoritative than stale summary text.
4. If summary metadata and code disagree, report the mismatch explicitly and identify which value was actually used by the runner.

## Example from the last S2 8×8 grid run

Run folder:

```text
/home/vipsa/vipsa-puda-project/data/probabilistic_computing/batch_1/substrate_S2/runs/grid_8x8_batch1_S2_form_randomized_5000_20260623T113438Z
```

Latest restart script inspected:

```text
/home/vipsa/vipsa-puda-project/runs/resume_grid_8x8_batch1_S2_from_device63_resetv_negative_20260625.py
```

### Per-device electrical sequence

1. **Keithley contact approach**
   - Read bias: `0.1 V`
   - Target window: `5e-10 A` to `1e-8 A`
   - Read compliance: `1e-7 A`
   - Forward Z step: `+0.5`
   - Max attempts: `120`
   - Over-current handling: retract in `-0.25` Z steps.
   - Below-lower trim: fine approach in `+0.25` Z steps.

2. **Weak/open contact policy**
   - Weak/open contact was not treated as a skip by itself.
   - The actual runner moved stage Z forward by `+0.5` once and then ran the requested measurements.
   - In this session the run-level summary text still contained an older `+1` note; the code path used `+0.5`. Future retrospective reports should call out such metadata/code mismatches.

3. **Over-contact/short-like policy**
   - Explicit override: still run adaptive DCIV.
   - `dciv()` begins with a low-bias precheck and, if short-like, runs a reset-pre sweep before the main forming path.

### Adaptive forming DCIV logic

Precheck:

```text
+10 mV at 1 µA compliance
pre_short_like = abs(I) >= 9e-7 A
```

If pre-short-like:

```text
RESET_PRE: 0 → -0.8 → 0 V, 50 mV step, 1e-4 A compliance
```

Main DCIV:

```text
0 → +1.0 → +1.5 → 0 → reset_side → 0 V
step = 0.05 V
positive/forming compliance = 1e-6 A
negative/reset compliance = 1e-5 A
initial reset_side = -1.5 V
```

Segments:

```text
PF1: 0 → +1.0 V
PF2: +1.05 → +1.5 V
PB:  +1.45 → 0 V
NF:  -0.05 → reset_v
NB:  reset_v+0.05 → 0 V
```

Detection/adaptation:

- SET detected when the largest log-current jump in `PF1/PF2` is `>= 0.5 log10`; `vset` is the destination voltage of that jump.
- RESET detected when the largest negative log-current jump in `NF` is `<= -0.5 log10`.
- If the negative-forward branch has an upward jump `>= 0.7 log10`, adapt the next device’s reset voltage toward `jump_to_v + 0.2 V`, but keep it strictly negative so `NF/NB` are never empty.
- If no reset is detected, append a `RESET_RECOVERY` sweep: `0 → reset_v → 0` at `1e-4 A` compliance.
- If all DCIV current remains very low (`max |I| < 5e-9 A`), move Z `+0.5` and retry the DCIV path with higher compliance: positive `1e-5 A`, negative `1e-4 A`, labeled `DCIV_RETRY_*`.

### Randomized SET-read-RESET-read pulse logic

- Instrument: Keysight via 707B.
- Target: `5000` trains.
- Per train:
  1. SET pulse at randomized voltage.
  2. Read-after-SET at `+0.1 V`.
  3. RESET pulse at `-1.5 V`.
  4. Read-after-RESET at `+0.1 V`.
- Pulse width: `10 ms`.
- Initial pulse compliance: `1e-4 A`.
- Checkpoint every `100` trains.
- SET voltages: `0.20 V` upward in `0.05 V` steps to `min(1.7 V, Vset + 0.2 V)`. If no Vset exists, default effectively reaches about `1.2 V`.
- If DCIV detected SET, apply five `-1.5 V` reset pulses before the randomized train.

Checkpoint/recovery:

- Compute read-after-SET/read-after-RESET distributions, ROC/Youden threshold, switching probability by SET voltage, and a simple logistic grid fit.
- If recent reset reads stay high above threshold for >95%, classify stuck-SET, wait `10 s`, and apply five reset pulses. Stop after two stuck-SET recoveries.
- If both read-after-SET and read-after-RESET remain below `1e-9 A`, first move Z `+0.5`; if it persists, increase pulse compliance to `3e-4 A`.

## Reporting style

When answering the user, keep it concise but specific:

- Name the inspected run folder and runner script.
- Separate contact/approach, DCIV, and pulse logic.
- Include exact numerical gates and compliance values.
- State whether values came from summary metadata or actual code.
- Avoid rerunning hardware for retrospective questions; use saved artifacts only.
