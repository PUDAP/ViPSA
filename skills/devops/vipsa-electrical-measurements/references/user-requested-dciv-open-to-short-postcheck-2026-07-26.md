# User-requested DCIV from open-like state and post-sweep short check (2026-07-26)

## Trigger

The live device repeatedly measured open/very-high-resistance-like at low bias (~1.4 GΩ, pA–tens of pA) after approach attempts. The user then explicitly requested a DCIV sweep:

```text
0 -> +1 -> 0 -> -2 -> 0 V
step size 0.05 V
requested delay 0.001 s
SET-side compliance 0.01 mA = 10 µA
RESET-side compliance 0.1 mA = 100 µA
```

## Durable lessons

1. If the user explicitly requests the stress recipe after an open-like diagnostic, treat that as authorization to run the sweep, but preserve the open/weak-contact precondition in metadata and final wording.
2. Turn lights off before the electrical sweep unless explicitly told otherwise.
3. Build the sweep as non-duplicated branch segments for exactly 121 points:
   - PF: `0 -> +1.0` inclusive at `0.05 V`
   - PB: `+0.95 -> 0`
   - NF: `-0.05 -> -2.0`
   - NB: `-1.95 -> 0`
4. Apply SET compliance to PF/PB and RESET compliance to NF/NB.
5. Report the inter-point delay as **requested/commanded** delay; do not imply the Keithley physically achieved 1 ms spacing unless buffer timestamps verify it.
6. Always do a post-sweep low-bias resistance check if the device state may have changed. In this concrete case the sweep itself did not hit the 10 µA/100 µA compliance limits and max sweep current was only ~1.3 nA, but the immediate post-sweep `check resistance` was pinned at the 1 µA read compliance at ±10 mV/±50 mV, so the device/contact had become conductive/short-like. Report that transition directly as a post-sweep state, not as a contradiction of the sweep compliance summary.
7. For compliance-limited low-bias reads, report resistance as a bound (`≤ ~10 kΩ at 10 mV`, `≤ ~50 kΩ at 50 mV`) rather than a precise ohmic resistance.

## Concrete reporting fields

For the DCIV run:

```text
shape: 0 -> +1 -> 0 -> -2 -> 0 V
points: 121
SET compliance: 1e-5 A
RESET compliance: 1e-4 A
requested delay: 0.001 s
max_abs_sweep_current: ~1.32e-9 A
SET compliance hits: 0
RESET compliance hits: 0
pre +10 mV read: ~3.6e-11 A
post +10 mV read inside DCIV protocol: ~5.1e-11 A
cleanup: Keithley output off, 707B open/nil, machines idle/null
```

For the immediate follow-up resistance check:

```text
+10 mV: ~+1e-6 A at 1 µA read compliance
-10 mV: ~-1e-6 A at 1 µA read compliance
classification: conductive / compliance-limited / short-like
resistance bounds: R <= ~10 kΩ at 10 mV; R <= ~50 kΩ at 50 mV
```

## Plotting fallback

If matplotlib is unavailable in the active Python, do not rerun hardware. Save CSV/JSON first, then either regenerate the plot in a plotting-capable venv or write a simple SVG from the saved CSV that preserves row order and segment colors.
