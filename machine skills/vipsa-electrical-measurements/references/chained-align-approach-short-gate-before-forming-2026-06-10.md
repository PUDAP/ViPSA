# Chained align → approach → short gate before forming/pulses (2026-06-10)

## Context

User requested a full chained ViPSA workflow:

1. Move stage Z down by 35 steps.
2. Move Zaber Y by -5000 native steps.
3. Perform camera alignment and send a picture.
4. Approach electrically.
5. Check whether the device is shorted.
6. If not shorted, run conservative DCIV forming.
7. If reset succeeds by post-DCIV resistance, discuss Keysight SET-read-RESET-read pulse values before running pulses.

## Useful workflow pattern

Treat this as a gated chain, not a single unconditional script:

1. Execute requested physical pre-moves with PUDA protocol.
2. Run camera-1 dark-pad alignment and attach the verified image.
3. Run Keithley-guided Z approach using the established 10 mV / 10-100 nA window unless the user supplies different parameters.
4. Always run a low-bias short/contact check before forming:
   - `0 V`
   - `±10 mV`
   - `±50 mV`
   - optionally `±100 mV`
   - low read compliance, e.g. `1e-6 A`
5. If low-bias reads are short-like or compliance-limited, stop and cleanup. Do not run forming DCIV and do not proceed to Keysight pulses.
6. Only if the short gate passes, run the conservative forming DCIV.
7. Only if reset is successful by post-DCIV low-bias read resistance/contrast, stop and discuss pulse values before running Keysight pulses.

## Concrete observed safety-stop criterion

A device that approached cleanly at 10 mV can still be over-contacted/short-like at slightly higher low-bias reads.

Observed after approach:

- Contact read at `10 mV`: `8.12e-8 A` (~123 kΩ), within the 10-100 nA approach window.
- Short-gate reads:
  - `+10 mV`: `1.06e-7 A` (~94.4 kΩ)
  - `+50 mV`: `6.42e-7 A`
  - `+100 mV`: `9.88e-7 A`
  - `-100 mV`: `-1.00e-6 A`
- The `±100 mV` reads reached the `1 µA` read-compliance limit.

Interpretation/reporting used:

- Classify as `short-like / over-contacted`.
- Skip forming DCIV.
- Skip Keysight pulse pattern.
- Cleanup electrical routing and verify all machines idle.

## Reporting pattern

Report the chain as a gated stop, not as a failure:

```text
Chain stopped at the short-check safety gate.

Approach/contact was achieved, but low-bias ±100 mV reads reached the 1 µA read-compliance limit, so I classified the device as short-like/over-contacted and skipped forming DCIV and pulses.
```

Include:

- alignment image path
- final alignment residual
- approach final current/resistance and Z position
- short-gate read currents
- explicit statement that forming/pulses were skipped by safety gate
- cleanup verification: Keithley off, 707B open/nil closed channels, machines idle

## Pitfall

Do not use the approach-window current alone as permission to form. A contact current near 80 nA at 10 mV can be acceptable for approach but still become compliance-limited at ±100 mV. The short gate is the decision point for forming/pulse eligibility.
