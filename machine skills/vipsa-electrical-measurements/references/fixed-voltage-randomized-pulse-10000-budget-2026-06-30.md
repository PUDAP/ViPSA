# Fixed-voltage randomized pulse probability runs in grid campaigns (2026-06-30)

## Trigger
Use when the user asks for randomized pulse measurement over an explicit voltage range and max pulse budget, rather than deriving voltage range from DCIV Vset.

## Protocol shape
- Generate a balanced randomized list of `SET-read-RESET-read` trains.
- SET levels are explicit and inclusive; for the S1 run they were `0.20 V` through `1.00 V` in `0.05 V` increments.
- Each voltage level gets `50` attempts per randomized block.
- Shuffle within a block; repeat blocks until device failure or the user-specified pulse budget.
- Interpret a `10000 pulses` budget as `2500` complete trains when each train has 4 pulses.
- Execute in chunks sized by total pulses. Start with no more than 100 physical voltage slots (25 four-pulse trains) on the current Keysight B2901BL path. A 400-slot native pulse call at 10 ms timed out at `*OPC?` and retained only one trace point; a 400-slot timed voltage-list call also timed out while the recoverable trace still contained the previous successful 100-slot chunk. Before retrying any timeout, call `recover_pulse_trace`, compare recovered source values exactly against the saved plan, and count only the matching completed chunk. Resume from the first unmatched plan row rather than repeating possible stress. The reliable fallback is 100-slot `source_voltage_measure_current` chunks with `delay_s` equal to the requested slot width; label this honestly as timed voltage-list execution rather than native pulse-shape mode.
- Save the plan before execution (`randomized_pulse_plan.csv`) so partial hardware results can be audited against intended pulses.

## Analysis
- Parse all returned currents and require returned current count to match the chunk plan when possible.
- Use read-after-SET and read-after-RESET distributions to derive the switching threshold. If a true two-mode distribution is not visible, record that the distribution is weak/unimodal and label the threshold as a fallback rather than a definitive bimodal split.
- Group by SET voltage to compute attempts, switches, `P_switch`, reset-high count/fraction, and an optional sigmoid fit.
- Preserve chunk checkpoints with medians, max read current, threshold, probabilities, compliance counts, and stop/recovery reason.

## Failure/recovery gates
- Stuck SET: if read-after-RESET remains above threshold for most recent reset reads, wait and apply a small reset-pulse burst; stop after repeated failed recoveries.
- Permanent HRS/open-like: perform the existing contact-nudge recovery once if that is part of the grid workflow, then stop if the next checkpoint remains uncoupled.
- Read compliance/short-like: if low-voltage read currents approach pulse compliance, stop the device early and classify as likely short/over-contact instead of continuing to the full budget.
- Always preserve partial CSV/JSON artifacts and cleanup Keysight output plus 707B routes before travel.
