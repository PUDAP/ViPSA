# Canonical p-bit electrical testing protocol — focused literature-review notes (2026-07-31)

## Trigger
Use when designing or explaining electrical measurements for stochastic devices / memristive p-bits / simulated-annealing substrates, especially PEA2PbBr4 ViPSA campaigns.

## Literature-derived consensus
Across p-bit and stochastic-device papers, the canonical electrical characterization is:

1. Apply a controllable electrical input.
2. Repeatedly sample a stochastic binary output.
3. Compute output probability vs input.
4. Fit a sigmoid/logistic transfer curve.
5. Report tunability, entropy/randomness, speed/stability, and device-to-device statistics.

For memristive devices, the closest canonical protocol is repeated `initialize/reset -> write/SET pulse -> low-bias read` trials over a randomized or swept pulse-amplitude/width set, converting read current into a binary state and extracting `P(state=1 | V_SET)`.

## Representative prior-study measurements

### p-bit / stochastic MTJ work
- Camsari/Sutton/Datta, *p-Bits for probabilistic spin logic* (Applied Physics Reviews 2019; arXiv:1809.04028): defines p-bits as tunable binary stochastic neurons with tanh/sigmoid response.
- Borders et al., *Integer factorization using stochastic magnetic tunnel junctions* (Nature 2019): demonstrates stochastic MTJ p-bits for probabilistic computing.
- Daniel et al., *Experimental demonstration of an on-chip p-bit core based on stochastic MTJs and 2D MoS2 transistors* (Nat. Commun. 2024; arXiv:2308.10989): measures time-domain MTJ resistance fluctuations, extracts dwell times, identifies 50/50 bias point, measures p-bit core output vs input voltage, and reports sigmoidal/tunable output. Supplementary notes: output sampled 200 times per input voltage for the integrated p-bit; MTJ randomness at 50/50 was binarized and tested with NIST suite.
- Li et al., *Stochastic p-Bits Based on Spin-Orbit Torque Magnetic Tunnel Junctions* (arXiv:2306.02780): initializes MTJ state, applies voltage pulses, reads resistance after pulses, measures switching probability vs pulse amplitude and pulse width, fits sigmoid, reports `V50`, `P=20/50/80%`, `ΔVc = V80 - V20`, `Q = ΔVc / Vc(P=50%)`, and NIST SP800-22 randomness tests.
- Ota et al., *Voltage-insensitive stochastic magnetic tunnel junctions with double free layers* (arXiv:2405.20665): characterizes stochastic MTJs using random telegraph noise, relaxation/dwell time ratios `τAP/τP`, 50/50 field, bias-voltage dependence, and autocorrelation/relaxation-time stability.

### Organic/memristive p-bit work
- *Polymer-based probabilistic bits for thermodynamic computing* (arXiv:2509.21372): reports a memristive device in a voltage divider + comparator p-bit primitive. Measures `P1` vs `Voffset` at multiple `VDD`, uses 5000 measurements per `(VDD,Voffset)` point, fits logistic curves, reports slope/steepness `k` and midpoint `V°`, shows running-average convergence over ~2000 cycles, and separately performs randomized pulsed I-V (`-3 V` to `+3 V`, 180 ms square pulses, 100 ms grounding) with log-binned current distributions, discrete Shannon entropy `Hdisc(I|V)`, and `Neff = 2^H`.
- Resistive-switching probability literature (e.g. IEEE EDL 2011 *Reset Switching Probability of Resistive Switching Devices*, DOI `10.1109/LED.2011.2109933`) commonly reports SET/RESET probability vs pulse amplitude/width, cumulative switching probability, and distributions/variability.

## What authors commonly report

| Category | Canonical reported quantities |
|---|---|
| Transfer curve | `P(1)` or `P_switch` vs input voltage/current/field/pulse amplitude/width |
| Sigmoid fit | logistic fit, slope `k`/β, midpoint `V50`/`V0`, `Pmin`, `Pmax`, fit quality |
| Tunability | `ΔV20-80`, `V50`, dynamic range, pinning near 0/1 |
| Time-domain stochasticity | raw resistance/current/output trace, binary bitstream, running average of `P1` |
| Speed/correlation | dwell times, autocorrelation/relaxation time, pulse-width dependence |
| Randomness | NIST SP800-22, autocorrelation, bit bias, XOR/bias correction if used |
| Entropy | binary entropy `H(p)`, analog/discrete entropy `Hdisc(I|V)`, `Neff` |
| Stability | endurance cycles, drift in `k`, `V50`, read-current distributions, stuck states |
| Scalability | device-to-device distributions, usable yield, short/open/stuck fractions |

## High-throughput compatibility with ViPSA

### Good high-throughput measurements
- Low-bias resistance/contact map (`0 V`, `±10 mV`, `±50 mV`) with Keithley + 707B.
- Open/short/usable classification.
- One conservative DCIV/forming map on candidate devices.
- Randomized SET-read-RESET-read pulse trains with Keysight + 707B.
- Automated `P(1|V_SET)`, sigmoid fit, binary entropy, current-distribution entropy.
- Device/substrate-level p-bit ranking: usable yield, sigmoid success rate, slope distribution, entropy distribution, compliance/stuck fraction.

### Medium throughput / candidate-only
- Full voltage × pulse-width probability phase diagrams.
- Dense `≥100–500` attempts per voltage bin.
- `≥5000` total trains/device.
- Retention/delay sweeps and blockwise drift analysis.

### Low throughput / late validation
- Long NIST randomness tests.
- Temperature-dependent stochasticity.
- Mechanistic spectroscopy/ER-EIS/dielectric measurements.

## Widely reported ViPSA-adapted protocol

Name: **contact-gated randomized SET-read-RESET-read p-bit characterization**.

Per device:

```text
A. Cleanup / dark setup
   lights off
   Keithley output off
   Keysight output off
   707B open_all -> get_closed_channels == nil

B. Contact/read gate, Keithley
   read: 0 V, +10 mV, -10 mV, +50 mV, -50 mV
   read compliance: 1 µA
   read_count: 3
   settle: 0.2 s

C. Classify
   pA/sub-nA, no voltage scaling -> open/weak contact; do not pulse
   stable nA-scale, voltage-scaled -> candidate
   compliance at ±10 mV -> short-like/over-contact; skip p-bit train unless explicitly overriding
   high zero-bias current or abrupt orders-of-magnitude change -> repeat low-bias check before calling stable

D. Conservative DCIV/forming for candidates
   0 -> +0.6..+1.0 V -> 0 -> -0.75..-1.5 V -> 0
   step: 20-50 mV
   positive compliance: 0.3-1 µA
   negative/reset compliance: 1-10 µA
   run post-DCIV low-bias health; stop if read-compliance-limited/short-like

E. Randomized pulse train, Keysight
   preferred train: RESET -> READ_RESET -> SET(random V_SET) -> READ_SET
   voltage list: [V_RESET, V_READ, V_SET, V_READ] * N
   V_READ: +0.05 V or +0.1 V
   V_SET: initially 0.2-1.0 V or 0.2 to Vset+0.2 V, step 0.05 V
   V_RESET: negative voltage selected from DCIV, often -1.0 to -2.0 V
   pulse width: 10 ms first pass
   pulse compliance: start conservatively; 10 µA maximum unless known safe

F. Analysis
   use read_after_set current distribution
   threshold into state=0/1 (fixed current, log-Otsu, ROC/Youden if reset reliable, or labeled fallback)
   compute P1(V_SET)
   fit P1 = Pmin + (Pmax-Pmin)/(1+exp[-k(V_SET-V50)])
   report k, V50, Pmin/Pmax, ΔV20-80, fit quality, attempts/bin
   compute H_binary(V) = -p log2(p) - (1-p) log2(1-p)
   optionally log-bin analog read currents to compute Hdisc(I|V) and Neff=2^H
   split into blocks to report drift in k/V50 and compliance/stuck fraction

G. Cleanup
   Keysight output off
   Keithley output off
   707B open_all and verify nil
   final machine states idle/run_id:null when available
```

## Screening vs publication depth

For grid/high-throughput screening:
- Run contact gate on all devices.
- Run DCIV + short randomized pulse screen only on usable candidates.
- Use ~20-50 attempts per SET level.

For publication candidates:
- Use dense bins near `V50`.
- Use `≥100-500` attempts per voltage bin.
- Use `≥5000` total trains/device.
- Report blockwise drift/endurance and entropy.
- Add NIST/randomness tests only after a device produces a clean, long, unbiased or bias-corrected bitstream.

## Interpretation rules for PEA2PbBr4 ViPSA devices
- A useful p-bit candidate is not merely high-current or compliance-limited; require a voltage-tunable probability curve from low-bias read states.
- Devices already compliance-limited at `±10 mV` should normally be treated as short-like/over-contacted and skipped for long p-bit pulse trains unless the user explicitly requests record-only failure data.
- Open/weak pA reads with no voltage scaling should not be pulsed for probability claims; probabilities would reflect contact noise/no coupling.
- Weak/no RESET does not automatically invalidate data, but must be explicitly labeled; if SET occurs without RESET, run exactly five RESET-read pairs at strongest configured RESET voltage before continuing randomized pulses only if the user/protocol permits degraded-state data.
- If nominal read_after_SET is lower than read_after_RESET, do not force a SET-high classifier; label inverted/no-valid-state-separation unless an explicit inverted convention is adopted.

## Publication-ready substrate-level outputs
Report across devices/substrates:

```text
usable yield
open fraction
short fraction
sigmoid-success fraction
distribution of k / effective-temperature bins
distribution of V50
distribution of Hmax and V_Hmax
compliance/stuck fraction
drift/endurance summaries
best high-T / medium-T / low-T candidate devices
```

This supports the framing: device-to-device sigmoid-slope variation provides hardware-discrete effective-temperature bins for simulated annealing, while pulse/read parameters provide dynamic fine tuning.
