# PEA2PbBr4 p-bit substrate optimization for on-chip simulated annealing

Use when planning or interpreting ViPSA screening of PEA2PbBr4 memristor substrates for stochastic p-bits / simulated annealing.

## Fabrication constraints learned

Current PEA2PbBr4 device process is one-step and should be treated as the fixed baseline unless the user says otherwise:

- spincoat a PEABr + PbBr2 solution mixture in DMF/DMSO
- no antisolvent quench
- anneal at 100 °C; current baseline is 10 min
- deposit a thin PMMA topcoat
- thermally evaporate Ag top electrodes

Currently available fabrication knobs:

- spin speed
- spin acceleration
- DMF:DMSO ratio, discretized as `1:3`, `1:2`, `1:1`, `2:1`, `3:1`
- perovskite concentration: `0.2 M`, `0.4 M`, `0.6 M`, `0.8 M`
- annealing time

Annealing temperature is not currently varied within a batch.

## Device/application objective

The target is not a single best memristor. The target is a substrate population that provides many usable stochastic p-bits for on-chip simulated annealing:

- high usable-device yield
- low short/open fraction
- high sigmoid-fit success rate
- broad but stable distribution of sigmoid slopes `k`
- entropy peaks near usable voltage ranges
- low drift in `k` and midpoint `V0`
- enough endurance for repeated annealing updates

For device-selection-as-temperature-knob, interpret fitted sigmoid slope as inverse effective temperature:

```text
P(1 | V) = 1 / (1 + exp[-k(V - V0)])
T_eff ∝ 1/k
```

Shallow sigmoid = high effective temperature / exploration; steep sigmoid = low effective temperature / exploitation. Frame device selection as **hardware-discrete effective-temperature binning**, ideally paired with electrical knobs for finer dynamic tuning.

## Iterative DOE strategy

Avoid brute-forcing every process parameter at once. Use sequential screening rounds:

### Round 1 — formulation screen

Hold spin speed, spin acceleration, and annealing time at baseline. Screen all 20 solvent/concentration combinations if possible:

```text
5 DMF:DMSO ratios × 4 concentrations
```

Use ViPSA fast maps to rank usable yield, short/open rate, switching candidate fraction, and initial stochastic response.

### Round 2 — spin-condition optimization

Pick the top 3–5 formulations. Vary spin speed and spin acceleration in a compact matrix such as low/high acceleration at low/medium/high speed, plus a baseline replicate. Optimize film uniformity, pinholes, contact yield, and stochastic switching fraction.

### Round 3 — annealing-time refinement

Pick the top 2–3 formulation/spin conditions. Vary annealing time around the 10 min baseline, for example 5/10/20/30 min. Optimize stability, drift, endurance, and entropy without requiring a different annealing temperature.

## ViPSA screening protocol per substrate

Use a two-stage screen.

### Stage A — fast map

For many devices per substrate:

1. move to device
2. align
3. approach
4. quick low-bias resistance check: `0 V`, `±10 mV`, `±50 mV`
5. classify open / short / weak contact / usable / switching candidate

Reject or deprioritize devices that are open, compliance-limited at low bias, or unstable from contact artifacts.

### Stage B — p-bit characterization

For candidate devices:

1. low-bias precheck
2. conservative DC I–V to identify safe voltage range and switching polarity
3. randomized SET pulse train with read-after-write
4. binary thresholding: `state=1` if `I_read > I_threshold`
5. sigmoid fit to `P(1 | V_SET)`
6. entropy calculation: binary entropy and/or log-binned analog-current entropy
7. short endurance / drift test on promising devices
8. cleanup: SMU outputs off, 707B open/nil, lights off unless requested otherwise

Adaptive pulse rule: first find a safe pulse window and approximate stochastic transition, then refine voltage bins around the midpoint. Do not use one fixed pulse range blindly across all substrates.

## Publication-ready outputs

Per substrate save and plot:

- process condition table
- optical/alignment artifacts and device map
- low-bias resistance distribution and classification map
- representative DC I–V loops
- randomized pulse scatter: `I_read vs V_SET`
- current histograms / `P(I | V_SET)`
- sigmoid fits and fit-quality metrics per device
- slope `k` distribution and midpoint `V0` distribution
- entropy vs voltage and maximum entropy map
- endurance/drift: `Δk/k0`, `ΔV0`, failure/compliance fraction
- substrate ranking table and next-batch recommendation

A concise substrate score can combine usable yield, sigmoid success, slope diversity, entropy, endurance, and penalties for short/open/drift/compliance-hit fractions.

## Reporting preference

For live ViPSA runs, keep updates concise by default. Report device-level status changes and final metrics; do not send per-step approach/pulse logs unless the user explicitly asks for verbose output.