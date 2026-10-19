# Reusable quick resistance script and confirmed compliance-limited transition (2026-07-24)

## Reusable executable

Use `/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/quick_resistance_check.py` for every terse live request such as `check resistance`, `quick resistance check`, or `again` in an active ViPSA session.

The script runs the paired low-bias Keithley/707B diagnostic at `0 V`, `±10 mV`, and `±50 mV`, saves complete artifacts under `runs/quick_resistance_check_<UTC>/`, leaves the light latch unchanged, and verifies output-off/open-all/idle cleanup.

## Confirmed transition pattern

A sequence of illuminated checks repeatedly measured approximately `1.47–1.53 GΩ` with pA currents. After the lights were explicitly turned off, the next check changed by several orders of magnitude:

- `±10 mV` and `±50 mV` reads all reached the `±1 µA` compliance limit.
- Zero-bias current was anomalously high (`~0.48–0.56 µA`).
- An immediate identical repeat reproduced both the compliance-limited nonzero reads and high zero-bias current.

## Durable handling rule

When an adjacent low-bias result jumps from pA/GΩ to compliance-limited µA:

1. Preserve the first run and immediately execute the same script again before calling the state stable.
2. If the repeat agrees, report a confirmed conductive/compliance-limited, short-like or over-contacted state.
3. Do not average compliance-limited paired-bias values into a precise resistance. At `10 mV` with `1 µA` compliance, report `R ≤ approximately 10 kΩ` as a bound.
4. Report anomalous zero-bias current explicitly because it weakens a simple ohmic interpretation.
5. Do not infer that a light-state change caused the electrical transition merely because it preceded it; report only the temporal association unless controlled A/B measurements establish causality.
6. Keep full electrical cleanup and do not apply additional stress automatically.
