# Randomized SET-voltage sigmoid pulse checkpoints during grid runs (2026-06-22)

## Trigger

Use this note when the user asks for randomized pulse measurements to obtain a sigmoid switching-probability curve, especially as one phase inside a grid run.

## Workflow lesson

For this specific class of ViPSA experiment, the user requested that pulsed testing stop/check every `100` pulses by analyzing the pulse data itself, with no separate health check. The correct loop is:

1. Generate the randomized pulse plan before hardware execution.
2. Execute pulse rows in `100`-pulse chunks while keeping the Keysight route active if safe.
3. After each chunk, analyze only the accumulated pulse read data:
   - `read_after_set` and `read_after_reset` median/read distributions.
   - Maximum low-voltage read current.
   - Compliance flags on read pulses.
   - ROC/Youden threshold separating SET-read and RESET-read distributions when possible.
   - `P(switch | Vset)` per SET voltage.
4. Stop on safety evidence from pulse reads: read current near compliance, likely short/over-contact, instrument fault, or nonsensical/missing return counts.
5. Do not run a separate Keithley health check between pulse chunks unless explicitly requested; it adds extra routing/stress and violates the user's requested “just analyse the data” rule for this workflow.

## Practical defaults from the session

- SET voltage range: `0.30..1.10 V` in `0.10 V` steps.
- Repeats: `10` per SET voltage for a live grid-compatible screen.
- Trial phases: `SET`, `read_after_set`, `RESET`, `read_after_reset`.
- Read voltage: `+0.1 V`.
- Reset voltage: `-1.5 V`.
- Pulse width: `5 ms`.
- Compliance: `10 µA`.
- Checkpoint size: `100` pulses.

Tune these based on current device and prior failures: avoid overly aggressive SET/RESET voltages after compliance-limited DCIV; stop early if read pulses approach compliance.

## Current parser pitfall

SMU response dictionaries can contain multiple aliases for the same reading. During pulse-current parsing, accept at most one current value per reading dictionary, preferring:

1. `I_meas (A)`
2. `Current (A)`
3. `current_A`
4. `current`
5. `I`

Double-counting aliases can make current-count validation fail or silently misalign pulse rows with readings.