---
name: vipsa-electrical-measurements
description: "Use when executing, parsing, plotting, or interpreting ViPSA electrical measurements on memristor devices: DCIV sweeps, split-compliance sweeps, pulse trains, resistance/read-probe measurements, compliance behavior, Vset/Vreset, ON/OFF, quality flags, and high-throughput device/substrate summaries."
version: 1.0.0
author: Shreyas Pethe + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, memristor, electrical-measurement, dciv, pulse, compliance, analysis]
    related_skills: [vipsa-machine-operations, puda-operations, puda-data, puda-report]
---

# Electrical Measurement Skills for Memristor Characterization

## Scope

This skill describes how the agent should understand, execute, parse, plot, and reason about **electrical measurements on memristor devices**.

This file is intentionally limited to the electrical layer only. It does **not** describe positioning, optical alignment, Z-approach, probe contact search, grid navigation, stage motion, or sample-holder geometry. Those belong in separate positioning/navigation skills.

The electrical layer assumes that the probe is already on the target device and that electrical contact is either already valid or has been verified by another layer.

---

## 1. What a Memristor Is

A memristor, or resistive switching memory device, is a two-terminal device whose resistance depends on its electrical history. In a typical vertical stack, the device consists of:

```text
Top electrode / active material / bottom electrode
```

For the current materials context, the active layer may be a halide perovskite film, and the device may use metal electrodes such as Ag or Au. The electrical behavior is usually studied using DC voltage sweeps and voltage pulse protocols.

The key device states are:

```text
HRS = high-resistance state
LRS = low-resistance state
```

The device can switch between these states under applied voltage.

Typical switching terminology:

```text
SET   = transition from HRS to LRS
RESET = transition from LRS to HRS
```

In many perovskite memristors, switching can be stochastic, gradual, volatile, partially irreversible, or cycle-dependent. The agent should not assume ideal textbook switching unless the data clearly shows it.

---

## 2. Why Electrical Measurements Are Done

The purpose of electrical measurements is to determine whether a device:

1. Conducts safely within compliance limits.
2. Shows resistive switching.
3. Has a measurable SET and/or RESET event.
4. Has useful ON/OFF ratio.
5. Retains HRS/LRS states sufficiently for the experiment.
6. Shows stochastic switching behavior useful for probabilistic devices or p-bit style operation.
7. Survives repeated cycling or pulsing without permanently shorting or becoming open.

For high-throughput characterization, the agent should treat each device as one statistical sample. The goal is not only to find one good curve, but to quantify distributions across devices, cycles, substrates, and process conditions. For PEA2PbBr4 p-bit substrates intended for on-chip simulated annealing, use `references/pea2pbbr4-bayesian-substrate-optimization-2026-07-31.md`: optimize the population for usable yield, sigmoid success, slope/effective-temperature coverage, entropy, endurance, and drift using simultaneous mixed-variable DOE plus batch Bayesian optimization over solvent ratio, concentration, spin speed, spin acceleration, and annealing time. For the canonical literature-derived electrical protocol for stochastic p-bits, use `references/canonical-pbit-electrical-protocol-literature-review-2026-07-31.md`: contact-gated randomized SET-read-RESET-read pulse trains, `P(1|V_SET)` sigmoid fitting, entropy, drift/endurance, and high-throughput vs publication-depth measurement tiers. For converting an in-progress ViPSA grid to that protocol, use `references/literature-pbit-grid-protocol-conversion-2026-07-31.md`: strict contact gate, `0 -> +0.8 -> 0 -> -1.0 -> 0 V` candidate DCIV, randomized `RESET -> READ_RESET -> SET(random V_SET) -> READ_SET`, and labeled degraded handling after SET-without-RESET.

---

## 3. Main Electrical Measurement Types

The relevant electrical measurement types are:

```text
DCIV sweep
Pulse measurement
Resistance/read-probe measurement
```

### 3.1 DCIV Sweep

A DCIV sweep applies a sequence of voltages and measures current at each voltage point. It is used to observe resistive switching behavior and extract quantities such as Vset, Vreset, ON current, OFF current, and ON/OFF ratio.

A common sweep shape is:

```text
0 V -> +Vmax -> 0 V -> -Vmin -> 0 V
```

or equivalently:

```text
positive forward segment
positive backward segment
negative forward segment
negative backward segment
```

### 3.2 Split DCIV Sweep

The electrical driver may split the sweep into positive and negative branches with different compliance values.

A two-way split may use:

```text
positive compliance = pos_compl
negative compliance = neg_compl
```

A four-way split may use:

```text
positive forward compliance  = compliance_pf
positive backward compliance = compliance_pb
negative forward compliance  = compliance_nf
negative backward compliance = compliance_nb
```

This is useful because SET and RESET may require different current limits depending on polarity and sweep direction.

For branch-specific user requests, preserve the branch names in the data products and final report:

```text
PF = positive forward, 0 -> +Vmax
PB = positive backward, +Vmax -> 0
NF = negative forward/reset branch, 0 -> -Vmin
NB = negative backward, -Vmin -> 0
```

For adaptive forming/grid DCIV code, keep reset-side sweep targets strictly negative. If an adaptive update relaxes the reset endpoint by adding a positive increment (for example `neg_up["to_v"] + 0.2`), normalize the result before constructing the sweep and again at the start of the DCIV builder. A reset target of `0`, `+0.05`, or `+0.1 V` can collapse or omit normal `NF`/`NB` reset branches while leaving only positive/forming branches in the CSV. Preserve the invariant `reset_v < 0` for reset-side branches and verify the next generated DCIV has non-empty `NF` and `NB` segments. Concrete patch/verification pattern: `references/adaptive-reset-voltage-negative-guard-2026-06-25.md`.

When the user requests an inter-point delay, report it as the commanded/requested delay and, if instrument buffer timestamps exist, also report the measured point spacing by branch. Do not imply a requested millisecond delay was physically achieved unless timestamps confirm it; Keithley buffer timing can be orders of magnitude slower than the commanded delay and may differ by segment.

When the user explicitly says **“no dwell,”** set native-list `delay_s` to exactly `0.0` and remove every explicit per-point sleep. Do not retain or report a previously requested nominal sweep rate whose calculation depended on nonzero dwell (for example, `50 mV` steps plus `1 s/point` must not remain labeled `0.05 V/s` after dwell becomes zero). NPLC integration, autoranging, native acquisition, and command overhead still take real time but are not programmed dwell; preserve instrument timestamps so this distinction remains auditable. For an exact signed Z move followed by a zero-dwell repetition, including fresh-directory retry classification and per-attachment delivery verification, use `references/z-increment-zero-dwell-dciv-retry-and-delivery.md`.

For sub-millisecond dwell requests, preserve the user's units literally and do not silently reinterpret milliseconds as seconds. A Keithley 2450 native-list request with `delay_s=1e-6` (user wording `0.001 ms`) has been observed to remain busy until the driver's 600 s VISA timeout and return no trace records. Treat such a timeout as uncertain partial stress: force output off, open/verify the 707B, recover the trace buffer only if records remain, and never repeat the branch automatically. Require explicit authorization before retrying with a supported dwell such as `1 ms` or `0 s`; report commanded dwell separately from measured point spacing.

For user-facing reports after a live ViPSA DCIV run, include cleanup verification alongside the plot and raw data: SMU output off, 707B channels open, and final machine states.

For requests such as “when was the latest DCIV generated?” or “send the generated artifacts,” use `references/latest-dciv-artifact-discovery-and-handoff.md`. It distinguishes database entries from locally orchestrated artifact-only runs, defines authoritative run versus file timestamps, selects the plot/combined CSV/summary manifest, and requires explicit Telegram target resolution plus per-file delivery verification.

For Keysight low-bias resistance checks, if the coordinated Keysight+707B protocol loses START state after routing, use the split-protocol control workaround documented in `vipsa-machine-operations/references/keysight-resistance-split-protocol-start-loss-2026-06-24.md`: route/setup separately, run a Keysight-only read, force Keysight output off in its own protocol, then 707B-only `open_all`/`get_closed_channels`. Compute resistance from measured voltage/current when available (`R = V_meas / I_meas`) and still report cleanup verification.

For Keithley `hold_voltage_measure_current` interleaved reads, a valid response may contain `I_meas (A)` while `V_meas (V)` is `None`. Treat the current as valid and preserve the raw record; for a constant-bias **read row only**, use the commanded hold voltage as voltage provenance. Continue to require a real measured-voltage field for sweep rows. If this parser shape blocks a multi-cycle run after completed stress, verify cleanup, recover completed operations from raw responses, and resume at the first missing operation rather than repeating the completed sweep/read history.

Session reference: `references/dciv-split-compliance-2026-06-05.md` captures concrete four-way-compliance sweep report patterns, timing pitfalls, and interpretation language for compliance-limited SET/RESET behavior.

For separate one-device yield screens that specify high-voltage forming plus SET/RESET cycles and a slow sweep rate, use `references/single-device-yield-form-set-reset-slow-sweep.md`. It covers the low-bias HRS/contact gate, dedicated side-project artifacts, nominal-rate timing, branch-specific compliance, and the critical rule to execute each `0 → endpoint → 0` operation as one native list so output re-enable does not create an abrupt endpoint step. If the user explicitly says to run the specified yield sequence **regardless of contact**, treat that as a one-run override rather than verified contact: record the fresh open/weak-contact precheck and exact authorization, recover uncertain switch-routing state before launch, use a fresh run directory, and distinguish **queued/started** from **completed/verified**. Follow `references/explicit-contact-gate-override-and-queued-yield-run.md`.

For an electrical-only DCIV runner, own only the machines actually commanded. Do not include stage, Zaber, light, or a second SMU merely to gather metadata or because a shared helper has a broad default machine list: a stale nonessential edge can abort the run before the first cycle. Use task-specific cleanup for the owned electrical pair, preserve the last verified mechanical readback with provenance, and retry into a fresh directory only after confirming zero completed cycles and safe electrical state. See `references/minimal-machine-ownership-dciv-and-high-hrs-gate.md`.

For interpreting and plotting a compliance-limited forming rerun, use `references/compliance-limited-forming-rerun-and-line-plot-interpretation.md`. It covers commanded-versus-measured voltage collapse, connected-line artifacts, forward/return separation, non-virgin forming terminology, and the three-panel diagnostic that distinguishes device switching from plotting or source-list faults.

Session reference: `references/post-approach-dciv-plot-recovery-2026-06-05.md` captures the post-approach “1 cycle like the previous one” recipe and a recovery pattern for when the electrical sweep/cleanup succeeded but plotting failed because system Python lacked `matplotlib`: do not rerun the sweep; regenerate plots from the saved JSON/CSV in a plotting-capable venv and verify row-count sanity fields.

### 3.3 Pulse Measurement

A pulse measurement applies a programmed sequence of voltage pulses and measures the current or resistance response. It is used for:

```text
endurance testing
stochastic switching probability
read/write protocols
sigmoid P(switch | V) extraction
```

For timed voltage-list p-bit tests, reject an apparent sigmoid when `read_after_SET` is nearly a deterministic linear function of the immediately preceding SET amplitude or when same-bias reads flip sign according to the preceding pulse polarity. Quantify this with signed-current plots and a linear-fit $R^2$. A 0→1 probability step created by Otsu slicing of voltage-correlated settling bands is not stochastic switching. Treat it as likely capacitive/settling or response-alignment contamination; validate with an inserted 0 V relaxation interval and delayed/repeated read sampling before any further long run. Use a reset-first trial (`RESET -> read_after_RESET -> SET(random V) -> read_after_SET`) or prove that the preceding train's final RESET initializes the next trial. Compute Otsu from `read_after_SET` only, classify `read_after_SET >= threshold` as switched, use `read_after_RESET` only to validate/reset-gate the starting state, and exclude or retry trials whose reset read is not in the initialized state. Group valid switched counts by randomized SET voltage and fit a binomial logistic sigmoid. Also plot/fit early, middle, and late subsets; reject the p-bit sigmoid if probability is flat versus voltage, RESET initialization fails, state direction is inverted, or the apparent switching occurs only in a contiguous cycle window.

For random SET-voltage / p-bit-like pulse train experiments, use the workflow note in `references/pbit-like-random-set-pulse-gating-2026-06-17.md`: repeat a live low-bias probe, branch short-like devices through reset-only DCIV first, skip pulsing on open-like pA/sub-nA contacts, generate the randomized SET-read-RESET-read CSV before hardware execution, and plot probabilities only from real read-current data. For the direct retry, chunked Keysight pulse execution, current-field parsing, ROC/Youden thresholding, and sigmoid beta reporting pattern, see `references/pbit-random-set-direct-retry-and-analysis-2026-06-17.md`. If the user asks for a simpler/non-Youden threshold, use `references/p-switch-read-after-set-distribution-threshold-2026-06-23.md`: choose the threshold from the `read_after_set` current distribution only (e.g. log-current Otsu split), then recompute `P_switch`, reset-high fractions, and sigmoid fits. If the user describes the intended protocol as `DCIV -> pulses with random SET voltages until failure`, treat the pulsed test as providing both endurance and sigmoid/probability data; an imperfect RESET does not automatically invalidate the dataset, but RESET quality and degraded-state bias must be labeled explicitly. See `references/dciv-to-randomized-set-pulses-validity-2026-07-29.md` and `references/dciv-random-set-pulses-valid-weak-reset-2026-07-29.md`. For grid-integrated randomized sigmoid pulse runs where the user says to stop/check every 100 pulses and “just analyse the data,” follow `references/randomized-sigmoid-pulse-checkpoints-2026-06-22.md`: chunk by 100 pulses, analyze accumulated pulse read data at each checkpoint, and do not insert separate Keithley health checks unless explicitly requested. For probabilistic-computing substrate campaigns that request a forming DCIV followed by ≥5000 randomized SET-read-RESET-read trains, follow `references/adaptive-forming-to-randomized-5000-train-pulses-2026-06-23.md`: extract Vset from the forming DCIV, generate SET voltages from 0.2 V to Vset+0.2 V in 0.05 V steps, use 10 ms pulses, handle stuck-SET recovery with a 10 s wait plus five RESET pulses, and preserve partial/raw data if the full train cannot finish. For resumed grid campaigns that continue from the **current manually approached device**, use `references/grid-resume-current-device-handoff-z-policy-2026-06-25.md`: distinguish the first handoff device, which may skip normal `-60/+30` travel and approach, from later devices that use the standard safe-retract/pre-approach Z sequence; report both normal Z policy and handoff exceptions when asked.

A typical pulse protocol may include:

```text
read pulse
write pulse
read pulse
reset pulse
read pulse
```

or a sequence of repeated SET/RESET attempts at different voltages.

---

## 4. Compliance Current

Compliance current is a safety limit on the current allowed through the device. It prevents catastrophic breakdown, hard shorts, or electrode damage.

The agent should understand that compliance is not just a software parameter; it changes device physics. Higher compliance can create stronger or more irreversible filaments, while lower compliance may prevent switching or produce weak LRS states.

Typical compliance fields are:

```text
pos_compl       positive sweep compliance
neg_compl       negative sweep compliance
compliance_pf   positive forward compliance
compliance_pb   positive backward compliance
compliance_nf   negative forward compliance
compliance_nb   negative backward compliance
```

When four-way compliance is not explicitly supplied, the default logic is:

```text
compliance_pf = pos_compl
compliance_pb = pos_compl
compliance_nf = neg_compl
compliance_nb = neg_compl
```

The agent should preserve these values in metadata for later analysis.

---

## 5. DCIV Data Expectations

A saved DCIV sweep usually contains a sequence of voltage-current pairs.

Expected core columns may include:

```text
Voltage
Current
```

Possible variants include:

```text
V
I
voltage_v
current_a
Voltage (V)
Current (A)
```

The agent should normalize column names during analysis, but should not silently discard raw column names. If possible, keep both the original and normalized forms.

A DCIV curve should be treated as an ordered sequence. Do not sort purely by voltage, because the hysteresis depends on sweep direction. The row order matters.

The agent should infer sweep segments from row order and voltage trajectory, for example:

```text
segment 1: 0 -> positive maximum
segment 2: positive maximum -> 0
segment 3: 0 -> negative maximum
segment 4: negative maximum -> 0
```

---

## 6. Pulse Data Expectations

A pulse measurement may contain columns such as:

```text
time
voltage
current
resistance
pulse_index
step_index
state
```

Different instruments and drivers may save different column names. The agent should identify which columns are present before assuming a format.

For pulse-based stochastic switching analysis, useful derived quantities include:

```text
pre-pulse resistance
post-pulse resistance
state transition flag
switching probability at each pulse voltage
number of attempts
number of successful switches
```

---

## 7. Metadata Expectations

Every electrical measurement should preserve metadata. This matters because the same current-voltage curve can mean different things depending on compliance, sweep path, read voltage, pulse width, and instrument settings.

Important DCIV metadata:

```text
sample_no
device_no
step_no
SMU model/address
sweep_path
pos_compliance_a
neg_compliance_a
compliance_pf_a
compliance_pb_a
compliance_nf_a
compliance_nb_a
sweep_delay_s
acquire_delay_s
wait_time_s
use_4way_split
include_read_probe
read_probe_mode
current_autorange
contact_current
Z_pos, if supplied by outer layer
protocol_context
```

Important pulse metadata:

```text
sample_no
device_no
step_no
SMU model/address
pulse_path
compliance_a
pulse_width_s
set_acquire_delay_s
current_autorange
pulse_mode
sigmoid_manifest_path
contact_current
Z_pos, if supplied by outer layer
protocol_context
```

The agent should not analyze a curve in isolation when relevant metadata is available.

---

## 8. How to Plot a Memristor DCIV Curve

The standard diagnostic plot is current versus voltage:

```text
x-axis: Voltage (V)
y-axis: Current magnitude |I| (A), usually on log scale
```

Use `abs(current)` for log-scale plotting because current can be positive or negative. The signed current should still be preserved for interpretation.

Recommended default plot:

```text
plot commanded Voltage vs abs(Current)
y-axis log scale
connect points in measurement order
place PF, PB, NF, and NB together on one shared axis (never separate subplots unless the user explicitly asks)
use a distinct color/style for each branch
label axes clearly
include sample/device/cycle information in title when available
```

When plotting repeated DCIV cycles, overlay every cycle on that same shared semilog axis while preserving the four branch identities. Assign **one color per cycle** and use that exact color for all four PF/PB/NF/NB segments of that cycle; distinguish branches with line styles and include a cycle colorbar plus branch-style legend. This makes cycle-to-cycle variation visible. Do not replace the one-axis all-branch graph with a 2×2 branch panel.

Example Python-style pseudocode:

```python
voltage = df[voltage_column]
current = df[current_column]

current_abs = abs(current)
current_abs = replace_zero_or_negative_for_log_plot(current_abs)

plot(voltage, current_abs, marker='o', line=True)
set_yscale('log')
set_xlabel('Voltage (V)')
set_ylabel('|Current| (A)')
set_title('Device DCIV: log current scale')
```

Important plotting rule:

```text
Do not sort the points by voltage before plotting.
```

Sorting destroys the sweep hysteresis.

### 8.1 Handling Zero or Negative Current for Log Plots

For log-scale plotting, the agent should use current magnitude:

```text
I_plot = abs(I)
```

If `I_plot` contains zeros, replace them only for plotting with a small positive floor. Do not overwrite the raw data.

A reasonable plot-only floor is:

```text
floor = smallest positive measured |I| / 10
```

or, if no positive current exists:

```text
floor = 1e-15 A
```

This should be described as a visualization step, not a data correction.

### 8.2 Recommended Plot Variants

For debugging and interpretation, the agent may generate several plot variants:

```text
1. Voltage vs signed current on linear scale
2. Voltage vs |current| on log scale
3. Voltage vs signed current on symmetric-log scale
4. Point index vs voltage
5. Point index vs current
6. Segment-colored DCIV plot
```

The most useful first plot for memristors is usually:

```text
Voltage vs |Current| with logarithmic y-axis
```

User plotting preference is measurement-class-specific:

- For retention, pulse-cycle, ON/OFF screening, grid screening, and candidate-comparison plots, use **scatter/markers only** by default; do not connect points unless explicitly requested.
- For **single-device DCIV and forming/SET/RESET sweeps**, default to **connected lines with no dot markers**, preserving acquisition order and keeping each operation/branch distinguishable. Reuse this line style on reruns unless the user asks otherwise.

Never sort either plot class by voltage. Connected DCIV traces can visually bridge abrupt compliance-limited state transitions; treat those segments as links between sampled states, not proof that every intermediate point was physically traversed.

---

## 9. How to Plot Sweep Segments

When the sweep has multiple branches, the agent should preserve branch identity.

Possible segment labels:

```text
PF = positive forward
PB = positive backward
NF = negative forward
NB = negative backward
```

A four-segment sweep can be plotted as:

```text
PF: 0 -> +Vmax
PB: +Vmax -> 0
NF: 0 -> -Vmin
NB: -Vmin -> 0
```

In a segment-colored plot:

```text
x-axis = Voltage
 y-axis = |Current| on log scale
one line per segment
legend = segment name
```

The agent should not assume every sweep has exactly four segments. It should inspect the voltage path.

---

## 10. Reading a DCIV Curve

For the user's CsFAPbI3/Pratap campaign, score a SET transition primarily from positive-forward (PF) versus positive-backward (PB) hysteresis at comparable *measured* voltage; a positive-side compliance hit is expected and can support a stable SET transition, but a compliance plateau alone is not proof. Score RESET from negative-forward (NF) versus negative-backward (NB) separation: it may be gradual and need not hit compliance or show a sharp drop. Save the full ordered traces and compare branches only where measured voltages actually overlap without read/stress clamp. Independent post-branch reads still quantify retained states and short/read-limit safety, but do not impose an absolute clean-HRS cutoff as the sole gate for exploratory hysteresis repeats when the user explicitly asks to screen them. Treat qualified retention/endurance claims separately from within-sweep switching.

When interpreting a DCIV curve, the agent should look for:

```text
initial resistance state
sudden current increase
hysteresis between forward and backward branches
current saturation at compliance
RESET-like current decrease
irreversible jumps or hard shorts
open-circuit/noise-floor behavior
asymmetry between positive and negative polarities
cycle-to-cycle drift
```

A likely SET event appears as:

```text
current increases sharply over a small voltage interval
current may hit compliance
subsequent branch remains more conductive
```

A likely RESET event appears as:

```text
current decreases sharply or gradually
subsequent branch returns to a less conductive state
```

However, in perovskite memristors, RESET may be absent, weak, hidden by compliance, or replaced by irreversible degradation. The agent should avoid overclaiming RESET unless the data clearly supports it.

---

## 11. Extracting ON/OFF Ratio

ON/OFF ratio compares low-resistance and high-resistance current or resistance states.

Using current at a read voltage:

```text
ON/OFF = |I_LRS| / |I_HRS|
```

Using resistance:

```text
ON/OFF = R_HRS / R_LRS
```

The log ON/OFF ratio is often more stable:

```text
log10_ONOFF = log10(ON/OFF)
```

The agent should report whether ON/OFF was computed from:

```text
sweep current
read-probe current
resistance file
pulse read states
```

Do not mix these sources silently.

---

## 12. Extracting Vset and Vreset

Vset is the voltage at which the device switches from HRS to LRS.

For the user's repeated PEA DCIV analysis, extract Vset from the **PF branch** as the voltage where the **second derivative of the lightly smoothed `log10(|I|)` versus commanded voltage peaks**. Report smoothing, voltage window, and edge exclusion explicitly; do not substitute first compliance voltage for Vset. Preserve first-compliance voltage as a separate compliance-onset metric when useful.

```text
1. Select PF only and preserve acquisition order.
2. Compute log10(|I|) using a plot/analysis floor without modifying raw current.
3. Apply light smoothing (for example Savitzky–Golay) to suppress pA-floor noise.
4. Compute the second derivative versus commanded voltage.
5. Exclude derivative filter edges and select the maximum positive second-derivative peak as Vset.
6. Apply sanity checks:
   - transition occurs on PF
   - not just instrument noise or a filter-edge artifact
   - current rises materially around the candidate
   - record confidence/quality separately from the extracted value
7. Do not equate a PF second-derivative peak with proven resistive SET until displacement/ionic-current contributions are checked. A simple capacitor should produce a direction-dependent current proportional to $dV/dt$ and approximately scale with sweep rate. Validate candidate SET with multiple sweep rates and delayed fixed-bias reads after a 0 V relaxation interval; if the current decays with settling time or scales with ramp rate, label the threshold as capacitive/ionic-contaminated rather than a retained resistance transition.
```

Vreset is the voltage where the device transitions from LRS to HRS. It may appear as a sharp or gradual current decrease.

For perovskite devices, the agent should be cautious:

```text
If no clear RESET is visible, report Vreset as not detected rather than forcing a value.
```

---

## 13. Recognizing Common Device Outcomes

### 13.1 Good Bipolar Switching

```text
clear SET event
clear RESET event
repeatable hysteresis
reasonable ON/OFF ratio
no permanent short
no permanent open
```

### 13.2 SET-Only or Irreversible Switching

```text
clear current jump into LRS
no later RESET
subsequent current remains high
possible permanent filament formation
```

This is common in fragile devices or when compliance/current/voltage is too aggressive.

### 13.3 No Switching

```text
current changes smoothly with voltage
no significant hysteresis
no sharp state transition
ON/OFF close to 1
```

### 13.4 Shorted Device

```text
high current at low voltage
little hysteresis
resistance already low before forming
may immediately hit compliance
```

### 13.5 Open or Poor Contact

```text
current near noise floor
large scatter
no meaningful voltage dependence
apparent infinite resistance
```

The electrical layer can identify this electrically, but should not decide mechanical corrective action. That belongs to contact/positioning logic.

When probing from the **top electrode (TE)**, negative measured currents—especially stable negative nA/pA reads during positive read pulses—are usually an **open-circuit / poor-contact signature**, not evidence of a retained conductive state. Do not convert those negative reads into a positive resistance and call them LRS/conductive unless corroborated by contact diagnostics, voltage scaling, polarity-consistent paired-bias behavior, or another validated measurement. See `references/te-negative-current-open-circuit-2026-06-29.md` for the session correction and reporting pattern.

When post-approach current is pA/sub-nA at a single low voltage, do **not** immediately label it open and do **not** immediately run forming/DCIV. Distinguish open/poor contact from a true very-high-resistance HRS with a non-stressing contact diagnostic:

1. Measure small-bias reads at multiple voltages such as `0 V`, `±10 mV`, `±50 mV`, and optionally `±100 mV` with low compliance.
2. If those remain pA/sub-nA, add a guarded higher-voltage diagnostic probe such as `±200 mV` at the same low compliance; optionally escalate to `±500 mV` only when it is below the intended forming/sweep region and contextually safe. This distinguishes true lost/open contact from a device that is simply in an ideal very-high-HRS/off state.
3. Check whether current scales consistently with voltage and has stable sign.
4. If ambiguous, run a Z-sensitivity check using tiny forward Z increments (`+0.25` or `+0.5` in the current ViPSA +Z-forward convention) with a low-voltage read after each step.
5. Stop and cleanup if any diagnostic probe reaches compliance or measured voltage collapses.

For grid-integrated open/weak-contact failures, see `vipsa-grid-measurement/references/contact-gated-open-failure-mitigation-2026-06-26.md`: before treating pA/sub-nA current as permanent HRS or running higher-compliance retries, run multi-bias low-compliance diagnostics with offset/paired-bias classification. If bounded `+0.25 Z` rescue still shows no voltage scaling, skip higher-compliance DCIV retries and randomized pulse trains unless explicitly overridden; pulse probabilities from no-coupling traces are not physically meaningful.

For continuation after several early devices fail or look short/open/over-reset, use `references/branch-by-branch-dciv-safety-gate-2026-06-26.md`: pre-stress multi-bias health, positive branch with post-read gate, reset branch capped near `-1.0 V`/`1 µA` with abrupt-jump hard stop, no automatic high-compliance reset recovery, and `pulse_allowed` gating before randomized pulses. If the user explicitly overrides this with wording like `do not skip running DCIV/Pulses`, convert these gates to record-only metadata rather than blockers: still save low-bias/contact flags, compliance hits, and warnings, but set the continuation logic to attempt DCIV branches and randomized pulses while retaining the safer compliance and reset-voltage caps unless the user changes them.

### 13.6 Degrading Device

```text
current increases irreversibly across cycles
ON/OFF ratio collapses
SET voltage drifts strongly
RESET disappears
```

---

## 14. High-Throughput Interpretation Rules

The agent should reason statistically across many devices.

Useful aggregation levels:

```text
cycle-level
measurement-level
device-level
substrate-level
batch-level
process-condition-level
```

A single device may not represent the substrate. The agent should prefer summaries such as:

```text
median ON/OFF
working device fraction
yield fraction
Vset distribution
Vreset distribution
cycle survival fraction
stochastic candidate fraction
fragile device fraction
```

For high-throughput workflows, the agent should avoid conclusions based only on one visually attractive DCIV curve.

During a running or recently completed grid trial, if the user asks for “devices done so far,” select completed devices from the trial summary and include only those with saved measurement files. For a single summary image of DCIV curves, preserve sweep row order, plot `Voltage` vs log-scale `|Current|`, label devices clearly, save the figure into the run folder, and return it as a media attachment. Do not rerun electrical measurements just to regenerate plots from already-saved CSV/JSON data.

---

## 15. Suggested Electrical Quality Flags

For each measurement, the agent may assign flags:

```text
valid_measurement
contact_like_current
open_like
short_like
switching_detected
set_detected
reset_detected
compliance_hit
hard_short_after_set
large_noise
read_probe_available
metadata_complete
```

These flags are not final scientific conclusions. They are screening labels to help organize analysis.

---

## 16. Suggested Device-Level Metrics

For each device, compute or store:

```text
number_of_cycles
number_of_valid_cycles
valid_fraction
switching_fraction
set_detected_fraction
reset_detected_fraction
median_Vset
IQR_Vset
median_Vreset
IQR_Vreset
median_log10_ONOFF
max_log10_ONOFF
late_cycle_survival
fragile_flag
short_flag
open_flag
```

For stochastic pulse experiments, compute:

```text
pulse_voltage
number_of_attempts
number_of_switches
P_switch
V50
sigmoid_slope
state_retention_after_read
```

---

## 17. Suggested Substrate-Level Metrics

For a substrate, useful summaries include:

```text
working_device_fraction
median_device_log10_ONOFF
median_device_Vset
IQR_device_Vset
stochastic_candidate_fraction
fragile_device_fraction
shorted_device_fraction
open_device_fraction
cycle_survival_score
```

For process optimization, substrate-level metrics are usually more useful than individual cycle metrics.

---

## 18. Safety and Sanity Rules for Electrical Analysis

The agent should be conservative when interpreting electrical data.

Rules:

```text
Do not force Vset or Vreset if no clear transition exists.
Do not treat noise-floor current as meaningful switching.
Do not overwrite raw current values when preparing log plots.
Do not sort DCIV points by voltage before plotting.
Do not compare ON/OFF ratios from different methods without labeling the method.
Do not ignore compliance current; it strongly affects switching.
Do not assume RESET exists just because the voltage polarity is reversed.
Do not call a device good based only on one successful cycle.
Do not call a substrate bad based only on one failed device.
```

Compliance-ladder stop rule: when running iterative DCIV compliance escalation, stop further escalation as soon as the completed cycle plot visibly shows a clear SET-RESET transition, especially if the user confirms it. Do not require a post-read heuristic to agree before stopping; visual sweep-shape evidence plus user confirmation is sufficient to halt additional stress. After stopping, force SMU outputs off, open/verify the 707B, and mark the run summary as stopped by user/clear transition rather than continuing to the next compliance level.

---

## 19. Preferred DCIV Plotting Function Behavior

A plotting helper should do the following:

```text
INPUT:
    path to sweep file or dataframe
    optional metadata
    optional output path

STEPS:
    load data
    identify voltage column
    identify current column
    preserve row order
    compute abs_current for plotting only
    replace zero abs_current values with plot floor only
    plot voltage vs abs_current
    use log y-axis
    label voltage in V
    label current in A
    include sample/device/step information if available
    optionally save figure

OUTPUT:
    plotted figure
    optional saved image path
```

Pseudocode:

```text
FUNCTION plot_dciv_log_current(data, metadata=None):

    voltage_column = find voltage column
    current_column = find current column

    voltage = data[voltage_column]
    current = data[current_column]

    abs_current = absolute value of current

    IF abs_current contains positive values:
        floor = minimum positive abs_current / 10
    ELSE:
        floor = 1e-15

    abs_current_for_plot = replace zeros in abs_current with floor

    create figure
    plot voltage vs abs_current_for_plot in original row order
    set y-axis to logarithmic scale
    set x-axis label to "Voltage (V)"
    set y-axis label to "|Current| (A)"
    set title using metadata if available
    show or save figure
```

---

## 20. Preferred DCIV Analysis Function Behavior

A DCIV analysis helper should do the following:

```text
INPUT:
    sweep dataframe
    optional resistance/read-probe dataframe
    optional metadata

STEPS:
    identify voltage/current columns
    clean only for analysis copies
    segment sweep by voltage trajectory
    detect compliance hits
    estimate ON/OFF ratio
    attempt Vset detection
    attempt Vreset detection
    assign quality flags
    return metrics and flags

OUTPUT:
    dictionary or row with extracted metrics
```

Pseudocode:

```text
FUNCTION analyze_dciv(data, resistance_data=None, metadata=None):

    voltage = extract voltage column
    current = extract current column
    abs_current = abs(current)
    log_current = log10(abs_current with safe floor)

    segments = infer sweep segments from voltage trajectory

    compliance_hit = detect whether current approaches compliance limit

    set_candidate = find sharp positive transition in log_current
    reset_candidate = find sharp negative transition in log_current

    onoff_ratio = estimate from read-probe data if available
    otherwise estimate from sweep data at comparable read voltage

    flags = assign quality flags

    RETURN:
        Vset
        Vreset
        ON/OFF
        log10_ONOFF
        compliance_hit
        flags
```

---

## 20.1 Same-device DC-IV recipe optimization

For rapid ON/OFF and endurance parameter screening on relatively uniform devices, test **multiple bounded SET/RESET recipes on each contact-qualified device** before consuming one device per recipe, when the user wants same-device comparisons. Interleave a repeated anchor, record recipe order/cumulative stress, use identical low-bias read timing, and reinitialize the HRS after each candidate; compare other devices afterward for order effects and held-out reproducibility. A forming-compliance event or unclamped read is not an eligibility gate by itself: require correct state direction, retained separation, and credible contact-dependent paired-bias response before escalating to multi-recipe or endurance tests. If a fresh site has same-sign offset-dominated reads after SET/RESET and bounded contact checks, stop rather than assigning its noise-floor ratios to candidate recipes. Thirty cycles may be a checkpoint; when explicitly requested, endurance continues to confirmed failure or the declared 500 full-IV-sweep cap.

## 20.1a Explicit energy-budget override during an in-place endurance run

When the user explicitly authorizes exceeding an energy budget and continuing to device failure, distinguish **branch-energy warnings**, **cumulative sampled-energy ceilings**, and **unknown/nonfinite energy accounting**. An existing branch-only waiver does not waive a cumulative ceiling. Implement the authorized cumulative override at both the pre-dispatch and post-operation guards, scoped to the current device and exact authorization; keep measured energy accumulating and preserve prior ceiling-exceeded flags as history. Do not reset the energy ledger, globally remove guard code, or silently change frozen voltage lists/compliance/timing. Retain native-data, owner, routing, control, unknown-exposure and cleanup gates. Record any changed cycle-limit policy explicitly rather than leaving stale maximum-cycle metadata. An energy-budget waiver does not implicitly waive a separately specified campaign-stage cycle cap: run to confirmed failure **or that cap**, whichever comes first. Verify initial-design, BO and confirmation caps separately with the optimizer; do not extrapolate a current-device until-failure override to every candidate. A cap survivor is right-censored, not a device failure. For a live uncapped controller, pause at a verified operation boundary, preserve completed branches, and restart with a tested finite cycle range plus a pre-dispatch cap guard; editing the running Python source alone does not change its loaded loop.

If a budget guard fires **after a complete native sweep**, inspect the native response, complete point/index order, commanded-list identity, finite measured V/I/time, timing monotonicity, recomputed sampled energy, already-charged amount and verified cleanup. A narrow evidence-backed reconciliation can acknowledge that executed sweep without replaying it or erasing its original UNKNOWN/fault entry. Resume at the next missing operation, not the beginning of the cycle. In a DCIV-only run, carry the every-tenth-sweep health counter forward, including any preparation sweeps already included by the original controller; a due health read is not a restoration of routine interleaved reads.

Existing historical reconciliations may themselves require the device-level unknown flag to be false. After proving the sole new budget-only stop, validate those prior proofs against a **read-only preview** of the reconciled device state, then mutate the live unknown flag only if every other exposure remains resolved. Do not bypass an unproved UNKNOWN. Test absent/wrong-device authorization, continued energy accumulation, unknown/control blocking, partial-trace rejection, and no completed-SET replay before starting the replacement controller. Verify the resumed operation and ledger readback before claiming continuation succeeded. Device-failure monitoring must be stated explicitly and distinguished from irreversible destruction; a SET-side compliance hit alone is not failure.

## 20.2 Preferred Pulse-Optimization Screening Workflow

When a user asks to optimize pulse conditions for one live memristor device, use short conservative screening batches rather than immediately running long endurance tests. Keep the previously safe compliance unless the user asks to change it. Recommended live workflow:

1. Verify the pulse SMU and switch are idle, force SMU output off, and route the DUT to the Keysight SMU.
2. If the absolute read currents are pA/sub-nA, the traces look oscillatory, SET/RESET reads are only weakly separated, or the user suspects open contact, pause pulse optimization and run a Keithley low-voltage contact check first. Do not optimize or endurance-test an apparent switching signal that may be contact noise.
3. Test candidate `SET-read-RESET-read` pulse trains in small batches (for example 30–100 cycles) and save one CSV per candidate.
4. Start from conditions close to the last safe test and escalate one variable at a time: voltage amplitude first in small steps, then pulse width at a voltage that did not hit compliance. Avoid escalating both amplitude and width simultaneously.
5. After every candidate compute read-after-SET and read-after-RESET distributions, median ratio, fraction of cycles with ratio ≥ 5, read-current maxima, and stress compliance-hit fraction.
6. Stop on a good screen if median read ratio is clearly separated (typical first-pass criterion: median ratio ≥ 5 with at least half the cycles ≥ 5) **and** the absolute read currents are credible for contact. Stop on a safety screen if read current rises into likely-short territory, any read pulse hits compliance, or a large fraction of SET/RESET stress pulses hit compliance.
7. Always cleanup: SMU output off, 707B `open_all`, verify `get_closed_channels` is nil/no channels, and report final machine states.
8. After any Z/contact approach or other mechanical contact change, treat the previously optimized endurance condition as untrusted until re-screened. Run the endurance test in bounded batches (for example 100 cycles) with a safety stop if low-voltage read pulses hit compliance, if max read current rises into likely-short territory, or if stress compliance-hit fraction is high. A read pulse at/near compliance at `+0.1 V` should be reported as likely short/over-contact and should stop the run rather than continuing to the full target count.

Do not call a higher-amplitude condition "optimized" merely because stress pulses hit compliance; require separated low-voltage read states. Do not call nA/pA-scale alternating read states robust RRAM switching until contact has been verified. Do not continue long endurance after contact approach if read currents are already compliance-limited; cleanup and report the safety stop.

Session reference: `references/pulse-open-contact-check-2026-06-05.md` captures a concrete case where apparent Keysight pulse switching was later supported as poor/open contact by a Keithley contact check.

Session reference: `references/post-approach-endurance-safety-2026-06-05.md` captures a concrete case where a Keithley approach produced measurable nA contact, but the subsequent Keysight endurance run immediately hit read/stress compliance and had to stop after the first 100-cycle safety batch.

Session reference: `references/dciv-filament-recovery-pulse-handoff-2026-06-05.md` captures a case where apparent SET-only / lack-of-reset behavior was not a permanent hard short: conservative low-SET-compliance DCIV recovered clean SET/RESET, but Keysight pulse handoff produced only weak nA-scale read separation. Use it for filament-recovery searches and for wording that distinguishes completed endurance from robust optimized switching.

Session reference: `references/conservative-dciv-forming-safety-stop-2026-06-06.md` captures a post-approach conservative forming attempt where even a `0 -> +0.60 V` branch at `100 nA` compliance became compliance-limited from `+0.05 V` onward with measured-voltage collapse. For future conservative forming requests, run low-compliance branches incrementally, inspect after each branch, and stop/cleanup instead of completing the planned full sweep if the device is already short-like or over-contacted. The reference also records a PUDA `command_log` recovery pattern: filter measurement command rows rather than assuming the last response is data.

Session reference: `references/reset-first-full-dciv-after-compliance-2026-06-06.md` captures the follow-up case where the user explicitly requested a whole DCIV despite prior compliance-limited forming, with an additional negative/reset side first. In that case, preserve the user's requested branch order (`RESET_PRE_NF/NB` before `PF/PB/NF/NB`) and treat planned compliance hits as reportable outcomes rather than automatic branch stops, while keeping a hard danger guard and full cleanup.

Session reference: `references/pulse-overstress-reset-first-dead-check-2026-06-06.md` captures a pulse-optimization safety stop followed by a user-requested reset-first “DEAD dead” DCIV check. Use it for the distinction between literally open/hard-shorted and “effectively cooked for useful switching”: low-bias reads can recover to measurable non-compliance-limited `~180–230 kΩ` while most low-compliance DCIV branches remain compliance-limited and reset fails to recover a clean HRS.

Session reference: `references/pulse-reset-read-compliance-limited-resistance-2026-06-10.md` captures a single `-2 V`, `1 ms` Keysight reset pulse followed by paired Keithley low-bias resistance reads. Use it when reset pulses and follow-up reads both hit compliance: report the low-bias resistance as a compliance-limited upper/lower bound such as `≤10 kΩ at 10 mV with 1 µA read compliance`, not as a clean ohmic resistance, and avoid interpreting larger-bias differential values when the current is clamped at the same read limit.

Session reference: `references/consecutive-reset-read-compliance-delivery-2026-07-24.md` covers short user-requested `RESET -> read` sequences such as ten `-2.5 V / +0.1 V` pairs: count pairs versus physical pulses explicitly, precheck contact, execute one lifecycle-managed PUDA pulse list with cleanup, and report commanded versus measured RESET voltage whenever current compliance prevents full voltage delivery. Do not label compliance-limited negative stress as successful RESET without lower-current read-state evidence.

Session reference: `references/keysight-two-pulse-current-probe-2026-07-29.md` covers terse Keysight requests to measure current once at a stress/reset pulse and then once at a read pulse, using a two-point `run_voltage_pulse_train`, saving returned rows, reporting commanded vs measured voltage/current, and labeling voltage collapse/current-compliance hits explicitly.

Session reference: `references/pulse-optimization-open-like-health-and-read-compliance-stop-2026-06-18.md` captures a live pulse-optimization screen where the Keithley health check was open-like/sub-nA, a bounded Keysight candidate screen was run, and the highest numerical ratio occurred only when +0.1 V read currents reached the `10 µA` pulse compliance. Use it for the reporting distinction between **highest observed ratio** and **best safer candidate**, and for plotting actual read-after-SET/read-after-RESET currents across pulse candidates.

Session reference: `references/post-approach-resistance-and-split-dciv-2026-06-06.md` captures a post-approach `0.01 V` resistance/contact check and a user-specified `0→+1→0→-2→0 V` split-compliance Keithley DCIV recipe. Use it for concise contact-quality wording (`~80.9 kΩ` at 10 mV = real/slightly strong contact, not open/short) and for the exact 121-point non-duplicated segment construction plus plot-regeneration sanity fixes.

Session reference: `references/z-increment-then-dciv-precheck-2026-06-09.md` captures the workflow for user requests like “move Z up by 1 step and then run a DCIV”: execute the requested signed Z move, run a 10 mV low-bias Keithley precheck before stressing, abort if short-like, otherwise run the established 121-point `0→+1→0→-2→0 V` split-compliance DCIV, save CSV/JSON/plot artifacts, and verify electrical cleanup and idle states. If the Z move is rejected or cannot be verified because of PUDA/NATS `RUN_ID_MISMATCH` or control-path failures, do not run the DCIV at the old contact; report the chain as blocked/no confirmed motion/no confirmed electrical stress. See `references/z-increment-dciv-blocked-run-id-mismatch-2026-06-10.md` for the blocked-run wording and safety rule.

Session reference: `references/z-minstep-then-custom-dciv-2026-06-22.md` captures the minimum valid `+0.25` Z contact-improvement step followed by a user-specified `0→+1→0→-1.5→0 V` split-compliance DCIV (`1e-6 A` positive/SET, `1e-5 A` negative/reset), including the 101-point non-duplicated segment construction, concise reporting fields, cleanup verification, and the rule to regenerate plots from saved CSV/JSON in a temporary plotting venv rather than rerunning hardware if plotting libraries are missing.

Session reference: `references/current-device-manual-high-compliance-dciv-after-retract-2026-07-27.md` captures a current-device manual DCIV after a stopped grid run and safe Z retract: run a low-bias precheck before high-compliance stress, build the 101-point `0→+1→0→-1.5→0 V` sweep with user-requested SET/RESET compliances, handle stale `idle`/non-null run IDs via the ViPSA machine recovery reference, preserve blocked attempts separately from successful retries, and report open-like/high-HRS results without overclaiming SET/RESET.

Session reference: `references/low-bias-resistance-offset-differential-2026-06-09.md` captures a quick Keithley resistance check pattern for pA/sub-nA currents where zero-bias offset is comparable to the 10 mV read. If a single low-bias read is only tens of pA, follow with a non-stressing `0 V`, `±10 mV`, `±50 mV` diagnostic and report differential resistance from paired biases as more meaningful than naive `R = V/I`, while still verifying `set_output(false)`, `open_all`, `get_closed_channels == nil`, and idle states.

**Manual-contact override for pristine HRS:** if the pA/GΩ trace would be classified automatically as `open_or_very_high_resistance_like`, but the user independently confirms physical probe contact and identifies the state as pristine HRS, preserve the automatic label only as `automated_signal_only_classification` and make the final classification `pristine_HRS_contact_confirmed`. Report paired differential estimates at ±10 mV and ±50 mV, retain zero-bias/current evidence, and state that contact was manually confirmed rather than electrically proven. If the device belongs to a named project, move generic quick-check output into that project’s canonical `runs/` root, patch `outdir`/project/context metadata, and append the linked run to `project.md` before reporting the final path. See `references/manual-contact-confirmed-pristine-hrs-resistance.md`.

**Contact-identifiability guard (supersedes absolute-current contact gates):** pA magnitude, polarity reversal, approximately linear paired-bias conductance, and optical overlap/forward sliding are evidence, not independent proof of electrical contact. Instrument, matrix, cable, or probe leakage may share those signatures. Do not impose a universal 1 nA (or other absolute-current) contact floor for high-HRS devices. At fixed Z, acquire repeated independent dark batches at 0, ±10 mV and ±50 mV with low compliance and actual trace-buffer measured voltage/current/time; compare paired conductance and offsets against matrix-open batches with identical settings. A matrix-open reference characterizes only the upstream SMU/matrix-input path, not the full probe/cable open condition. Even a statistically significant routed-minus-matrix-open conductance requires a matched routed, probe-lifted reference to identify physical-contact-dependent conduction. Report batch-level confidence intervals and settling sensitivity; do not pool correlated readings as independent replicates. Keep outputs off before route changes, verify closed-channel sets and cleanup nil, and stop on compliance/voltage collapse/control failure. Diagnostic bias lists are not authorization for forming, stress pulses, or mechanical motion.

**Reusable high-HRS contact marker:** when the user says pristine-device HRS is naturally very high, never gate contact on pA/GΩ magnitude alone. Prefer a device-like paired-bias signature: zero-bias offset smaller than the differential response, current following bias polarity at a sufficient safe voltage, `ΔI` scaling approximately with the voltage-window ratio, and similar differential resistance across bias pairs. Treat same-sign currents dominated by zero-bias offset as electrically open-like. Repeat this diagnostic after DCIV; pre-run manual contact confirmation does not automatically prove retained post-run coupling. If the postcheck becomes offset dominated, report that electrical coupling is no longer confirmed without claiming the probe physically moved. Concrete thresholds, worked examples, metadata, and reporting language are in `references/high-hrs-contact-marker-and-post-dciv-recheck.md`.

Session reference: `references/alive-vs-shorted-low-bias-check-2026-06-09.md` captures the concise alive-vs-shorted check after stress: use paired low-bias Keithley reads (`0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`), classify no-compliance sub-nA/GΩ behavior as `not hard-shorted; very high resistance/open-like`, and always verify Keithley output off plus 707B open-all cleanup.

Session reference: `references/post-dciv-low-bias-health-and-100mv-resistance-2026-06-15.md` captures the follow-up after an aggressive/override DCIV where low-bias reads relaxed back to pA/sub-nA: if asked for `100 mV` resistance, measure `0 V`, `+100 mV`, and `-100 mV`, report naive and offset-corrected resistances, and prefer paired differential resistance when zero-bias offset is comparable to the signal.

Session reference: `references/post-dciv-health-gate-before-repeat-cycles-2026-06-14.md` captures the conditional repeat-cycle gate after a DCIV/forming sweep: if a device that previously showed tens of nA at a 10 mV post-read later relaxes back to pA/~0.1 nA low-bias reads, classify it as weak/open-like or not-retained and do not run requested repeat DCIV cycles under “if the device is working” wording. It also records the one-order-lower compliance mapping from `+1e-4/-1e-3 A` to `+1e-5/-1e-4 A` and the required cleanup/reporting standard.

Session reference: `references/quick-low-bias-resistance-check-2026-06-18.md` captures the default for terse live requests like `check resistance`: run a Keithley/707B low-bias diagnostic at `0 V`, `±10 mV`, and `±50 mV` with `1 µA` read compliance, compute naive/offset/paired estimates, and report compliance-limited `10 mV` reads as resistance bounds such as `R <= ~10 kΩ` rather than precise ohmic values. Verify that the parsed sample count equals the commanded `read_count`; select one canonical structured current field instead of concatenating overlapping aliases. **Canonical executable:** for every terse `check resistance`, `quick resistance check`, or `again` request in an active ViPSA context, execute `/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/quick_resistance_check.py`. It runs the PUDA protocol, saves protocol logs/CSV/summary under `runs/quick_resistance_check_<UTC>/`, computes paired differential resistance at ±10 mV and ±50 mV, and verifies Keithley output-off plus 707B open/nil cleanup. Important light-control pitfall: the canonical script currently sends **no** light commands and reports `light_policy: unchanged`; it does not actually preserve or restore illumination by itself. If lights were previously left on, turn them off before electrical routing unless the user has explicitly latched illumination, leave them off after cleanup by default, and explicitly tell the user that the prior lamp state changed. If an illuminated check was already run unintentionally, immediately turn lights off and repeat the same canonical low-bias check; use the dark repeat as the main decision result and preserve both run dirs. See `references/quick-resistance-after-lights-on-dark-repeat-2026-07-28.md`. If local JetStream NATS recovery is active, pass the explicit override `--nats-servers nats://127.0.0.1:4222` rather than relying on project/default PUDA config, because project-local config may still point at `bears`. For repeated terse checks, compare against the immediately previous run and call out whether the pA/GΩ or compliance-limited state is reproducible. **Explicit latch override:** if the user says to keep the lights on until explicitly told to turn them off, preserve that state across later resistance/electrical checks—skip light-off commands, retain all SMU/707B cleanup, label the measurement as illuminated, and report that lights remain on. See `references/latched-light-state-during-electrical-checks.md`. If a routine check changes by several orders of magnitude relative to adjacent checks—especially pA/GΩ to compliance-limited µA—and the `0 V` current is also anomalously large, report the first result but immediately repeat the same low-bias sequence before calling the new state stable or authorizing stress. If the repeat returns to HRS/open-like behavior, classify the first event as transient short-like/compliance-limited rather than a confirmed stable LRS/short; preserve both runs. See `references/repeat-confirm-transient-short-like-low-bias-2026-07-22.md`. For a confirmed adjacent-run transition from repeated illuminated pA/GΩ checks to reproducible dark compliance-limited µA reads—with high zero-bias current, resistance-bound wording, and the rule not to infer optical causality from timing alone—see `references/paired-low-bias-compliance-transition-confirmation-2026-07-24.md`. For an explicitly requested higher-bias resistance point followed by a low-bias cross-check, use `references/high-bias-vs-low-bias-resistance-crosscheck-2026-07-22.md`: label method and bias, report read-to-read drift/range, do not force agreement between nonlinear high-bias and paired low-bias resistance, and parse one canonical current field per measurement to avoid duplicate samples. For the exact repeated-read protocol shape, see `references/explicit-voltage-resistance-check-repeated-reads-2026-07-22.md`. Session reference: `references/offset-dominated-resistance-before-approach-2026-07-01.md` captures the case where all small-bias currents match the zero-bias offset, making paired/offset-corrected resistance meaningless; report open-like/high-resistance for that diagnostic, but do not skip a later explicit `approach` request—re-read live and gate motion from the fresh approach current.

For chained manual requests that combine a stage Z move and a resistance check, execute the authorized Z move first, verify stage readback separately, then run the same low-bias Keithley/707B diagnostic and cleanup. If the local PUDA edge accepts a stale/delayed START after restart, complete the stale run id and verify the motion did not occur before retrying; do not run the resistance check until the Z move has a successful fresh `move_z_by` response plus readback. The machine-control details are in `vipsa-machine-operations/references/manual-z-increment-then-resistance-check-2026-06-25.md` and `vipsa-machine-operations/references/local-vipsa-edge-restart-stale-run-recovery-2026-07-27.md`.

Session reference: `references/override-negative-first-dciv-2026-06-15.md` captures the user-authorized override pattern for running a DCIV despite a prior health-gate concern: preserve the requested negative-first path (`0 -> -Vmax -> 0 -> +Vmax -> 0`), explicitly record that normal health gating was bypassed by user authorization, keep hard cleanup/idle verification, and report post-read compliance-limited low-voltage states as short-like/resistance bounds rather than precise ohmic values. For an explicit user-requested `0 -> +1 -> 0 -> -2 -> 0 V`, 50 mV step, 1 ms requested-delay sweep from an initially open-like/pA state, use `references/user-requested-dciv-open-to-short-postcheck-2026-07-26.md`: execute the requested recipe with the open-like precondition recorded, turn lights off, build 121 non-duplicated points, and run/report a post-sweep resistance check because the device can become read-compliance-limited/short-like even when the sweep itself did not hit stress compliance.

Session reference: `references/post-approach-default-dciv-compliance-limited-2026-06-15.md` captures a plain post-approach “run a DCIV sweep” request using the established `0→+1→0→-2→0 V`, 121-point split-compliance recipe, plus compliance-limited branch reporting and the plotting recovery pattern of creating a temporary matplotlib/pandas venv from saved CSV/JSON without rerunning the sweep.

Session reference: `references/post-revisit-grid-device-dciv-2026-06-23.md` captures a post-revisit grid-device DCIV after predictive/fractional Z pre-approach: use the recent grid-style `0→+1→0→-1.5→0 V`, 101-point, 50 mV, split-compliance recipe (`300 nA` positive, `10 µA` negative), report branch compliance-hit counts and cleanup, and do not change electrical fidelity in response to early compliance hits unless a hard safety fault occurs.

Session reference: `references/approach-to-dciv-no-contact-gate-2026-06-18.md` captures the chained “perform approach and run one DCIV sweep” safety gate: the DCIV is authorized only after approach establishes real contact. If bounded approach remains open/weak-contact (for example tens of pA/sub-nA at 10 mV after the configured Z range), skip DCIV, cleanup (`set_output(false)`, `open_all`, closed channels `nil`), verify idle states, and report the no-contact blocker concisely. If this chain starts with camera snapshots, first complete the requested image capture and send verified `MEDIA:` attachments, then turn lights off before electrical approach unless the user explicitly says otherwise; see `vipsa-image-capture/references/snapshot-before-electrical-chain-2026-06-22.md`.

Session reference: `references/direct-nats-dciv-rerun-and-compliance-escalation-2026-06-17.md` captures a direct-NATS fallback DCIV workflow for rerunning the current device with changed SET compliance after protocol-run issues: start Keithley/707B, route to Keithley, run one `hold_voltage_measure_current` per point, save partial data before cleanup, plot from saved CSV if needed, and report that stronger compliance-limited SET-like jumps do not imply retained LRS unless post-read probes remain separated.

Session reference: `references/multilevel-set-retention-2026-06-17.md` captures the Keithley + 707B workflow for SET-pulse retention and multi-level SET tests: route once, apply `run_voltage_pulse_train` SET pulses at increasing compliances, take timed `0.1 V` read traces for up to 100 s, distinguish requested compliance from actual pulse current, plot log-scale read-current decay, and always report whether low-bias reads show retained LRS or remain baseline pA/sub-nA.

Session reference: `references/keysight-single-set-100read-retention-2026-06-29.md` captures the Keysight + 707B version of a quick retention check: one SET pulse followed by 100 low-bias reads in a single `run_voltage_pulse_train` voltage list, direct-NATS reliability notes for the advertised-route outage, stale-run `complete` recovery before retry, expected 101 returned currents, CSV/plot products, and concise interpretation of pA/sub-nA reads as no strong retained filament under the requested pulse condition.

Session reference: `references/z-increment-repeat-randomized-3400-pulse-no-bimodal-2026-06-30.md` captures the explicit user-authorized pattern for `stage +1 Z` followed by rerunning the exact same 3400-pulse randomized Keysight SET-read-RESET-read train in `100`-cycle chunks. Important pitfall: if all 3400 hardware points are returned but the read-after-SET distribution is unimodal/no-switch, do not let an unconditional two-component threshold/sigmoid helper mark the measurement failed. Analyze the saved CSV with `bimodal_available=false`, use any previous bimodal threshold only as a clearly labeled consistency reference, generate scatter-only plots plus a no-bimodal histogram, and report TE negative nA positive-read currents as open / very-high-HRS / poor-contact-like rather than LRS conduction.

Session reference: `references/manual-z-move-then-measure-current-2026-07-01.md` captures the distinction between a terse `measure current` request and a full `check resistance` diagnostic after a manual Z move. For unspecified-bias `measure current`, default to a compact Keithley current read at `+0.1 V` with conservative compliance; reserve the multi-bias `0 V`, `±10 mV`, `±50 mV` table for resistance/open-vs-short diagnostics.

Session reference: `references/fixed-voltage-randomized-pulse-10000-budget-2026-06-30.md` captures fixed-range randomized pulse probability runs where the SET-voltage levels are specified directly rather than derived from Vset: generate balanced randomized SET-read-RESET-read blocks with `50` attempts per voltage level, run in fixed total-pulse chunks such as `500` pulses (`125` trains), stop at device failure or a user-specified pulse budget such as `10000` pulses, derive `P(switch)` from read-after-SET/read-after-RESET distributions while labeling weak/unimodal threshold fallbacks, and preserve partial artifacts plus chunk-level recovery/stop reasons.

Session reference: `references/extended-fixed-range-randomized-pulses-and-read-histogram-2026-07-27.md` captures an explicit extended current-device run with SET voltages `0.40–0.80 V` in `0.05 V` steps, 10,000 physical pulses / 2,500 trains, checkpointed weak SET/RESET separation reporting, and the follow-up plotting pattern for a bounded pulse-index read-current scatter plus log-binned histogram. Use `MPLBACKEND=Agg` for headless matplotlib plot generation.

For short current-device fixed budgets, use `references/current-device-fixed-range-randomized-1000-pulses-2026-07-24.md`: make pulse-count semantics explicit (`1000` total physical pulses means `250` four-pulse SET-read-RESET-read trains), treat a separate `+0.1 V` value as the read bias, detect and stop stale concurrent runners, precheck contact, balance random levels even when counts do not divide evenly, checkpoint every 100 physical pulses, separate stress- from read-compliance flags, and require direction-aware RESET-state separation before calling the result robust switching. For a current-device pulse measurement requested immediately after a DCIV SET-like transition, use `references/post-dciv-fixed-range-randomized-pulses-local-2026-07-27.md`: choose SET levels around/below the observed Vset, keep explicit local NATS overrides if historical runners point at stale servers, recover missing Python plotting/NATS deps with `uv run --with ...` rather than rerunning hardware, and if every tested voltage switches report saturation (`threshold below tested range`) rather than a meaningful sigmoid V50.

Session reference: `references/inverted-set-reset-pulse-distributions-2026-07-23.md` covers nominal SET reads falling below nominal RESET reads, polarity-swapped physical behavior, and the critical classifier failure where an assumed SET-high ROC threshold degenerates to `P(switch)=1` and `reset_high_fraction=1`. Require directional separation and mark inverted distributions invalid under the original state convention rather than reporting 100% switching.

Session reference: `references/keysight-set-reset-endurance-500cycle-compliance-drift-2026-06-29.md` captures a Keysight + 707B 500-cycle `SET-read-RESET-read` endurance measurement pattern using one long `run_voltage_pulse_train` voltage list (`[+1 V, +0.05 V, -1 V, +0.05 V] * cycles`), parsing read-after-SET/read-after-RESET phases, plotting read currents and ratios, and reporting upward drift/read-compliance hits as over-conductive or short-like behavior rather than robust SET/RESET endurance.

Session reference: `references/safe-onoff-pulse-optimization-and-scatter-2026-06-29.md` captures a safe ON/OFF optimization screen after over-conductive endurance drift: use short reset-first candidate batches, lower read voltage/read compliance, asymmetric SET/RESET compliance only in small batches, stop on low-bias read-compliance hits, and report that the largest numerical ratio is not trustworthy if it occurs in an unsafe/read-limited candidate. It also records the user's preference for scatter-only electrical pulse/retention plots.

Session reference: `references/dciv-until-good-then-pulse-screen-2026-06-06.md` captures a bounded “run DCIV until good SET/RESET, then pulse” handoff. Use it for the safe candidate escalation order, the practical SET/RESET scoring criteria, and the important wording distinction: a good SET/RESET-looking DCIV can still produce weak pulse read separation, so the pulse condition should be reported as not optimized unless low-voltage read states are clearly separated.

Session reference: `references/reset-compliance-escalation-dciv-and-legible-plotting-2026-06-08.md` captures a `0→+1→-2→0 V` reset-compliance escalation workflow: keep SET/read compliance conservative, increase RESET compliance first, use low-voltage post-SET and post-RESET read probes as the deciding evidence, and stop on perma-set-like reads pinned near SET compliance. It also records the user-facing plotting lesson: ViPSA DCIV plots must be legible and should use real plotting/SVG text rather than crude bitmap-font previews unless clearly labeled as rough.

Session reference: `references/high-hrs-contact-edge-reset-compliance-escalation-2026-06-10.md` captures a high-HRS/contact-edge reset search: after paired low-bias checks and a minimal `+0.25 Z` contact step, escalate RESET compliance up to a declared ceiling while using post-SET/post-RESET read probes to decide state. Important interpretation rule: a steep negative-branch current drop is not a valid sharp RESET unless the device was clearly in LRS immediately before it; compliance-clamped branches and modest read-probe contrast should be reported as partial recovery/ambiguous reset, not clean RESET.

Session reference: `references/bounded-dciv-forming-no-coupling-2026-06-10.md` captures a follow-up “best DCIV to properly form the filament” attempt when the device/contact remained weakly coupled. Use a bounded forming screen (`0→+1.2→0→-2.0→0 V`, SET compliance `300 nA` then `1 µA`, RESET compliance `30 µA` then `100 µA`) and stop/cleanup if currents remain only pA–nA with no compliance approach and ~1× low-bias read-probe change. In that case recommend small contact improvement (e.g. `+0.25 Z` plus low-bias check) rather than blind voltage/current escalation.

Session reference: `references/chained-align-approach-short-gate-before-forming-2026-06-10.md` captures a full gated chain: physical pre-moves, camera pad alignment, Keithley Z approach, low-bias short gate, then forming/pulse eligibility. Important rule: even if approach lands in the 10–100 nA window at 10 mV, run a multi-bias short gate before forming; if ±100 mV reaches the low read-compliance limit (e.g. 1 µA), classify as short-like/over-contacted, skip forming DCIV and Keysight pulses, and cleanup/verify idle.

Session reference: `references/direct-contact-check-fallback-and-open-like-read-2026-06-13.md` captures a low-bias contact check where the normal PUDA protocol runner duplicated START on the 707B; a direct core-NATS fallback measured `~6.9e-11 A` at `10 mV` and verified `open_all`/`nil` channels. Use it for concise wording that pA-scale current after approach means **not in contact / very weak contact** relative to the `10–100 nA` target, and load `vipsa-machine-operations/references/direct-contact-check-protocol-runner-duplicate-start-2026-06-13.md` for the machine-control fallback details.

Session reference: `references/compliance-limited-contact-check-2026-06-12.md` captures the follow-up contact-status check after over-contact/retraction: a 10 mV read that hits `1 µA` compliance means contact is definitely present but short-like/over-contacted; report apparent resistance as a bound such as `≤ ~10 kΩ`, not a precise ohmic value, and do not continue to forming/pulsing without explicit authorization.

Session reference: `references/low-compliance-health-sweep-after-approach-2026-06-12.md` captures a guarded low-compliance DCIV health check after approach: run PF first, stop before PB/NF/NB if `+0.05`–`+0.10 V` is already compliance-limited, report short-like/over-contacted with resistance bounds, and recover CSV/plots from saved PUDA outputs rather than rerunning if post-processing fails.

Session reference: `references/grid-trial-live-updates-and-combined-dciv-2026-06-06.md` captures live-update etiquette and combined plotting for an in-progress ViPSA grid trial: suppress repetitive per-step approach loop updates, still report coarse travel/electrical/status events, and generate a single multi-device DCIV PNG for completed devices by preserving row order and plotting log `|I|` per PF/PB/NF/NB segment.

Session reference: `references/saved-grid-device-dciv-plotting-2026-06-23.md` captures the single-device saved-CSV plotting pattern for requests like "Plot the DCIV for device 1": do not rerun hardware, parse `device_##/dciv.csv`, preserve row order and segment names, plot log `|I|` with compliance reference lines plus a point-index voltage subplot, use a plotting-capable venv/stdlib CSV fallback if pandas is missing, and return the PNG via `MEDIA:` with concise sanity fields.

Session reference: `references/negative-sweep-cycle-plot-threshold-2026-07-08.md` captures saved-CSV analysis for repeated negative sweeps such as `0 -> -3 V -> 0`: remove positive-voltage/contact-check rows, renumber real sweep cycles when raw `Cycle Number` includes setup/contact reads, split NF/NB at the minimum voltage point, plot NF solid and NB dashed with a cycle color gradient, and extract NF threshold voltage vs cycle using an explicit current-crossing criterion with log-current interpolation. If the user asks for derivative-based `Vth`, use `references/negative-sweep-second-derivative-vth-2026-07-13.md`: compute NF `Vth` from the max second derivative of `log10(|I|)` vs `|V|` after light smoothing, save signed voltage separately if needed, and plot `|Vth|` on the y-axis.

Do not call a higher-amplitude condition "optimized" merely because stress pulses hit compliance; require separated low-voltage read states. Do not call nA/pA-scale alternating read states robust RRAM switching until contact has been verified. Do not continue long endurance after contact approach if read currents are already compliance-limited; cleanup and report the safety stop.

A pulse analysis helper should do the following:

```text
INPUT:
    pulse dataframe
    optional metadata

STEPS:
    identify pulse voltage/current/resistance columns
    identify read states before and after write pulses
    classify state transitions
    count switching successes and failures
    compute P_switch at each voltage
    fit or summarize sigmoid if enough data exists

OUTPUT:
    pulse metrics and switching probability table
```

Pseudocode:

```text
FUNCTION analyze_pulse_switching(pulse_data, metadata=None):

    identify pulse index, voltage, current, resistance columns

    for each pulse attempt:
        determine pre-pulse state
        determine post-pulse state
        classify whether switching occurred

    group by pulse voltage:
        attempts = count pulses
        switches = count successful transitions
        P_switch = switches / attempts

    IF enough voltage levels and attempts exist:
        fit sigmoid P(switch | V)
        extract V50 and slope

    RETURN switching probability table and fit parameters
```

---

## 22. Electrical Measurement Vocabulary

Use the following vocabulary consistently:

```text
sweep          DC voltage ramp or stepped voltage sequence
pulse          time-domain voltage stimulus
read probe     low-voltage measurement used to estimate state
compliance     current limit during electrical stress
HRS            high-resistance state
LRS            low-resistance state
SET            HRS -> LRS transition
RESET          LRS -> HRS transition
forming        first creation of conductive pathway
ON/OFF ratio   contrast between LRS and HRS
Vset           voltage where SET occurs
Vreset         voltage where RESET occurs
cycle          repeated sweep or switching attempt
endurance      ability to survive repeated cycles
retention      ability to preserve state over time
stochasticity  probabilistic switching behavior under repeated stimuli
```

---

## 23. What the Agent Should Prioritize

When looking at a memristor electrical dataset, the agent should prioritize:

```text
1. Is the measurement electrically valid?
2. Is the device open, shorted, noisy, or switching?
3. Is SET visible?
4. Is RESET visible?
5. What is the ON/OFF ratio?
6. Was compliance reached?
7. Did the device degrade or become permanently LRS?
8. Are the results repeatable across cycles?
9. Are the results repeatable across devices?
10. What substrate-level or process-level conclusion is supported?
```

The agent should prefer cautious, evidence-based language. For example:

```text
"This curve shows a SET-like transition near +0.8 V."
```

is better than:

```text
"The device definitely SETs at +0.8 V."
```

unless the transition is clear and reproducible.

---

## 23.1 Direction-aware pulse-state sanity check

Before interpreting pulse switching probability, verify the direction of read-state separation at the identical read bias. If nominal `read_after_set` current is systematically lower than nominal `read_after_reset` current, keep command-role labels distinct from physical SET/RESET states: do not force a high-after-SET ROC/Youden classifier and do not report degenerate `P(switch)=1` plus `reset_high_fraction=1` as successful switching. Corroborate polarity with DCIV, then either analyze an explicitly labeled inverted-state hypothesis or mark `inverted/no valid SET-RESET separation`. See `references/inverted-set-reset-pulse-distributions-2026-07-23.md`.

## Output-state capability mismatch guard

Live PUDA `machine commands` metadata can advertise `get_output` while the active Keithley edge rejects it as `Unknown or restricted command`. Inspect the actual active driver source and saved rejection; do not invent a getter or mistake `query_reading` (`:READ?`, acquisition) for `:OUTP?`. A private `_query` is not an exposed command. Do not modify/restart an edge without authorization. Where the user explicitly authorizes the established fallback, require a successful `set_output(False)` response, successful matrix `open_all`, and successful explicit `get_closed_channels == nil`/empty-list readback. Label `output_off_command_acknowledged=true` and `output_off_verified=false` (no independent output-state readback), rather than silently claiming verification. Preserve failed attempt artifacts; prove zero stress from the command ledger before retrying into a fresh directory. Preserve/drain preflight error queue only at that proven zero-stress boundary and require a fresh empty queue before stress.

## Native 2450 list and function-response precision

Keithley 2450 native list replies can differ from unquantized requested floats because source programming has range-dependent resolution (official 2450 datasheet, Voltage Specifications, SOURCE column: 20 mV/500 nV, 200 mV/5 µV, 2 V/50 µV, 20 V/500 µV, 200 V/5 mV). Do not use source accuracy or a generic voltage tolerance to bless a list, and do not assume six-significant-digit equality against unrestricted requests. Preserve exact requested upload tokens, cumulative count/error evidence, and every ordered native value. Capture actual source function/range/AUTO and consistent sweep setup while output is OFF. For AUTO configurations, `:SOUR:CONF:LIST:QUER? "VoltCustomSweepList", <index>, SEM` may say `smu.source.range is not used`; an authorized OFF-only configuration recall followed by `:SOUR:VOLT:RANG?` establishes the actual per-index range without guessing the 105-percent switching boundary. Recall changes configuration, so hold exclusive instrument ownership, prove OFF before every recall, restore the safe final-zero configuration, and reverify compliance/readback/cleanup before enabling output. Keep full proof bounded and retain it once rather than duplicating it on every trace row.

TSP configuration levels can render seven significant digits, including observed binary32 storage effects, while SCPI list/level queries render six. Avoid double rounding TSP text from seven to six digits: corroborate each representation separately against captured native evidence using deterministic encoding checks, not an arbitrary tolerance. Manufacturer source-resolution specifications do not themselves document all storage/rounding rules. Qualify the complete frozen SET and RESET arrays live with output OFF and preserve any failed proof before deployment or stress. `:SENS:FUNC?` can return `"CURR:DC"` after setting `"CURR"`; accept those explicit DC-current aliases while rejecting voltage, resistance, and AC-current functions. A rejection demonstrably before output enable is not an executed READ; preserve its UNKNOWN history with an evidence-backed zero-exposure reconciliation and resume at the missing operation, never replay completed stress.

## Continuous compliance readback encoding guard

For the continuous trigger-model path, a compliance such as requested `0.01291064093426287 A` may legitimately read back as the six-significant-digit SCPI token `0.0129106`. A `math.isclose(..., rel_tol=1e-6)` comparison can reject this before output enable, even though the existing native OFF-list proof accepts the encoding. Check the exact returned Decimal against the deterministic six-significant encoding of the preserved `.17g` upload token (ROUND_HALF_UP); never round a differing returned token into acceptance or broaden an accuracy tolerance. Keep finite-value, current-range and NPLC guards intact. Apply and regression-test the same rule in the downstream continuous receipt validator before stress, otherwise successful acquisition may fault after exposure. Test neighboring tokens, extra trailing nonzero digits, nonfinite values, bad ranges/NPLC and full runner receipts. Preserve original UNKNOWN/fault records and reconcile zero exposure only from a verified before-INIT exception, OFF-list proofs, exact loaded driver identity, output transition evidence and cleanup—not zero records alone. A same-candidate retry needs explicit recovery registration with a fresh request/execution identity, retained fault history, and unchanged bot-confirmed arrays/settings; normal new-candidate publication deliberately rejects previously acknowledged candidates.

## Continuous-trigger configuration-list recovery

On the verified Keithley 2450 firmware 1.7.5b, a dual-list `:TRIG:BLOC:CONF:NEXT <block>, "sourceList", "measureList"` was observed to compile with the first list recorded twice, despite an empty configuration-error queue. Native `:TRIG:BLOC:LIST?` exposed the duplication; execution then stopped with error 2761 (configuration-list types must differ) at that block, before the output-ON block, leaving zero buffer records. Two separate single-list CONFIG_NEXT blocks read back correctly in an output-OFF comparison. Validate exact list identities and block/branch targets before INIT, and inspect runtime error queue plus `:TRIG:STAT?` before reducing failure to a trace-count mismatch. Zero trace records alone never prove zero exposure; reconcile only with preserved trigger program, failed-block evidence, output ordering and cleanup.

Continuous-batch receipts require batch-specific validation, not a single-sweep validator that assumes local sample indices, per-row native-list proof or independently restarted timestamps. Preserve native raw trace windows and status fields once, link each segment to its exact proof and global trace slice, and validate all ordered points. Partition sampled energy along the complete native timeline: first-sample rectangle once at batch start, then trapezoids including segment boundaries once. Do not add each segment's first absolute timestamp as a new rectangle. Regression-test the actual runner-to-adapter-to-driver receipt shape before hardware execution.

## Native low-bias list buffer guard

The live 2450 driver allocates trace-buffer capacity equal to list length; the instrument requires capacity >=10. Short 3/5-point diagnostics can leave error 4920 even if rows return. Dedicated low-bias runners should pad to >=10 points at the final safe bias, preserve all returned rows, and gate on all repeats. Inspect and preserve the error queue before motion. Driver `SENS:CURR:PROT` may yield -113 on 2450; `SOUR:VOLT:ILIM` is the applicable voltage-source limit. Do not dismiss unfamiliar errors or modify/restart the edge during contact approach. An error-blocked preflight is not an executed approach.

## 24. Explicit Non-Scope Items

The following are intentionally not included in this skill:

```text
stage movement
Zaber movement
OpenFlexure control
optical alignment
contact approach
probe landing
safe retraction
grid navigation
sample-holder collision avoidance
slot-to-device coordinate transforms
robot loading/unloading
```

Those should be handled by separate skills that call the electrical measurement layer only after the device is electrically ready to measure.
