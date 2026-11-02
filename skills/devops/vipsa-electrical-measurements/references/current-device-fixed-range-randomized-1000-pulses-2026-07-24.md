# Current-device fixed-range randomized 1000-pulse run (2026-07-24)

Use this note for terse requests such as: “run 1000 randomized pulses at this device with -2 V reset, 0.1 V read, and 0.3–0.8 V SET in 0.05 V steps.”

## Durable workflow

1. **Resolve pulse-count semantics before constructing the plan.** The established primitive is `SET -> read -> RESET -> read`, four physical pulses per train. If the user says “1000 pulses,” default to **1000 total physical pulses = 250 trains**, but state that interpretation in the run metadata and final report. If they clearly mean 1000 SET attempts/cycles, generate 4000 physical pulses instead.
2. Treat `+0.1 V` as the low-bias **read** when it appears beside a separate SET range. Preserve role labels (`set`, `read_after_set`, `reset`, `read_after_reset`) in both plan and results; do not silently call the read a SET pulse.
3. Before starting, check for stale or concurrent electrical runners. Stop a stale runner before issuing a new pulse train, then force SMU outputs off and open the 707B. Do not run two current-device experiments concurrently.
4. Run the canonical low-bias Keithley/707B check first. A stable paired-bias voltage-scaled response can support proceeding as high-HRS/weak but measurable contact; preserve the precheck artifact path in the pulse summary.
5. Build an approximately balanced randomized plan over all discrete SET levels. When the train count is not divisible by the number of levels, cycle through shuffled complete level blocks and truncate the last block; this yields attempt counts differing by at most one.
6. Execute Keysight trains in **100-physical-pulse checkpoints** (25 four-pulse trains). Save the complete plan before hardware execution and rewrite partial result CSV/checkpoint metadata after every chunk.
7. Distinguish compliance by role:
   - Any `read_after_set` or `read_after_reset` near compliance is a hard safety stop.
   - Stress-pulse compliance flags are important degradation/overdrive evidence, but isolated stress hits do not by themselves require aborting a user-requested fixed budget when read pulses remain below compliance and no instrument fault occurs.
8. Always cleanup in `finally`: Keysight output off, Keithley output off, 707B `open_all`, verify closed channels are nil, and verify final electrical machine states are idle.

## Analysis and reporting

- Report requested/completed **physical pulses and trains** separately.
- Report stress-compliance and read-compliance hit counts separately.
- Use scatter-only plots for pulse read-current screening and probability summaries.
- Before interpreting `P(switch)`, apply the direction-aware state sanity check from `references/inverted-set-reset-pulse-distributions-2026-07-23.md`. A high SET-high fraction is not robust switching when RESET reads remain high or distributions strongly overlap.
- When RESET-high fraction is large, say that the requested RESET did not consistently restore the low-current state; do not call the resulting ROC threshold or sigmoid a clean probabilistic transfer curve.
- Return the scatter plot as media and provide artifact paths for plan CSV, result CSV, probability CSV, and summary JSON.

## Concrete session outcome

A run using `SET=0.30..0.80 V` in `0.05 V` steps, `read=+0.10 V`, `RESET=-2.0 V`, `2 ms`, and `100 uA` compliance completed 1000/1000 physical pulses (250 trains) in ten 100-pulse chunks. It produced 18 stress-pulse compliance flags and zero read-pulse compliance flags. The RESET-read distribution remained substantially high/overlapping, so the correct interpretation was full budget completion with inconsistent reset-state recovery—not robust clean switching.
