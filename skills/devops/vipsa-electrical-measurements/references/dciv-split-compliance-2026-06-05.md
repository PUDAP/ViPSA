# DCIV split-compliance run pattern — 2026-06-05

Session-specific reference for future ViPSA memristor DCIV sweeps where the user requests a one-cycle path with different compliance on each branch.

## Request pattern

User requested one-cycle DCIV sweeps on the current contacted device with a path like:

```text
0 -> +1 -> 0 -> -2 -> 0 V
step = 0.05 V
requested time between measurements = 0.001 s
```

Two compliance variants appeared in the session:

```text
Variant A:
PF compliance = 10 uA
PB compliance = 10 uA
NF compliance = 1 mA
NB compliance = 10 uA

Variant B:
PF compliance = 1 uA
PB compliance = 1 uA
NF compliance = 0.1 mA
NB compliance = 1 uA
```

## Useful execution/reporting pattern

1. Treat this as a four-branch split-compliance sweep, not just positive/negative compliance.
2. Preserve branch labels in output and plot:
   - `PF`: positive forward, `0 -> +Vmax`
   - `PB`: positive backward, `+Vmax -> 0`
   - `NF`: negative forward/reset branch, `0 -> -Vmin`
   - `NB`: negative backward, `-Vmin -> 0`
3. Avoid duplicating the vertex row at segment boundaries unless the protocol explicitly calls for it. For `0 -> +1 -> 0 -> -2 -> 0` with 0.05 V steps and no duplicate vertices, expect `21 + 20 + 40 + 40 = 121` points.
4. Report both requested timing and measured instrument timing when buffer timestamps are available. In these runs, a requested `0.001 s` inter-point delay produced much longer physical spacing:
   - one run showed actual median spacing around `0.085 s`
   - the lower-compliance run showed around `0.10 s` for PF/PB/NF and around `0.50 s` for NB
   Future reports should never imply the requested millisecond delay was physically achieved unless timestamps confirm it.
5. Plot `Voltage` vs `|Current|` on log scale with one line per segment and legend entries containing branch name and compliance when space allows. Attach raw CSV as well as the plot when possible.
6. Inference should explicitly separate compliance-limited behavior from true switching. If many points sit at compliance, use cautious language: "SET-like", "possible partial reset", "return toward HRS-like current", or "strong compliance-limited conduction" rather than definitive Vset/Vreset claims.
7. Include cleanup verification in the final report: SMU output off, 707B channels open, and final machine states.

## Interpretation lessons from these runs

A curve can look like a transition while mostly reflecting current-limit behavior. In the higher-compliance run:

- Positive forward hit `10 uA` compliance almost immediately after the first point.
- Negative forward mostly hit `1 mA` compliance.
- Negative backward returned near `10 uA` compliance but dropped to a few microamps near zero.

The concise inference was: electrically conductive, not open; possible rapid forming/SET near the start of PF; no clean RESET transition; possible partial reset after the high-compliance negative branch; not clean bipolar switching in that single cycle.

In the lower-compliance follow-up:

- PF showed a sharp SET-like jump near `+0.35 V` from roughly `2.4e-10 A` to the `1 uA` limit.
- PB remained mostly at the `1 uA` limit.
- NF stayed below `0.1 mA` compliance with a maximum around `1.36e-5 A`.
- NB returned toward low-current/HRS-like behavior near 0 V, around `10^-11` to `10^-10 A`.

The concise inference was: clear SET-like switching with strong ON/OFF contrast; likely reset/recovery after the negative loop, but no sharply resolved RESET event in the NF branch. Do not overstate RESET just because the final current is low.