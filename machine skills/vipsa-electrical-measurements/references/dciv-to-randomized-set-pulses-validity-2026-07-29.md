# DCIV → randomized SET-pulse validity and interpretation (2026-07-29)

## Trigger

Use this when the user shows or describes a ViPSA memristor dataset where DCIV is followed by randomized SET-voltage pulse testing, and asks whether the data is valid or how to interpret RESET/endurance/sigmoid results.

## User correction / interpretation rule

The protocol can be scientifically valid even when RESET is imperfect or only partially successful.

The intended protocol class is:

```text
DCIV characterization
→ randomized SET-voltage pulse sequence until device failure / stopping criterion
```

The pulsed test serves two purposes simultaneously:

1. **Endurance:** how many SET/read/RESET/read attempts or pulse trains the device survives before degradation, stuck state, hard short, open, or loss of useful separation.
2. **Sigmoid/probability data:** switching probability as a function of randomly sampled SET voltage, derived from read-after-SET / read-after-RESET states.

## Reporting guidance

- Do not reject the entire dataset solely because RESET is weak/unsuccessful.
- Label RESET quality explicitly: `reset_successful`, `partial_reset`, `weak_reset`, `stuck_SET`, `reset_failed`, etc.
- Separate **valid pulse-endurance evidence** from **clean bipolar-switching evidence**.
- For sigmoid extraction, state the classifier/threshold basis and whether RESET/read-state separation is strong enough for a meaningful probability curve.
- If RESET is partially unsuccessful, the sigmoid may still be useful but should be labeled as conditional on a degraded/biased state trajectory, not an ideal independent SET probability.
- Continue preserving raw reads and pulse index order; do not force a clean textbook SET/RESET interpretation onto messy but usable data.

## Suggested concise wording

```text
This is valid pulsed switching data: the DCIV establishes the starting device behavior, then the randomized SET-voltage pulse train provides both endurance information and P(switch | Vset) / sigmoid data. RESET is weak/partially unsuccessful, so I would not call it clean bipolar endurance, but the pulse run is still scientifically useful if we label the RESET quality and failure mode explicitly.
```
