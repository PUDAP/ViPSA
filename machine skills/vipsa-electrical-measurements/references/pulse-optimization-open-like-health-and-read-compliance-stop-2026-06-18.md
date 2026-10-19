# Pulse optimization after open-like health check and read-compliance safety stop (2026-06-18)

## Context

A current device had just completed an edge-contact DCIV ladder that produced transient compliance-limited positive-branch events but did not retain a conductive LRS. The user then requested pulse-train optimization for highest `Ron/Roff` ratio and a plot of actual result currents.

## Useful workflow lesson

1. **Run a live Keithley low-bias health check before Keysight pulse optimization**, even if previous DCIV/pulse history exists.
   - Example bias set: `0 V`, `±10 mV`, `±50 mV`, `±100 mV` with `1 µA` read compliance.
   - In this case max low-bias current was only `~1.37e-10 A`, so the device/contact was classified `open_like_very_weak`.

2. **If health is pA/sub-nA open-like, do not run an unbounded optimization sweep.**
   - A conservative single candidate can be useful if the user explicitly asked to pulse, but label it as limited/diagnostic rather than optimized.
   - Small apparent read separation at nA/pA levels can be contact/noise dominated.

3. **If proceeding with bounded candidate screening, score by read pulses, not stress pulses.**
   - Use `SET-read-RESET-read` cycles and compute read-after-SET vs read-after-RESET distributions from actual returned currents.
   - Track: median read-after-SET, median read-after-RESET, median current ratio, per-cycle ratio ≥ 5 count, max read current.

4. **Stop on read-current safety even if the ratio is numerically large.**
   - A high-amplitude candidate `SET +1.4 V`, `RESET -1.8 V`, `1 ms`, `10 µA` compliance produced median current ratio `~1.5e3`, but max read current reached `~1.00e-5 A` near pulse compliance.
   - Report this as likely over-formed / unsafe to continue, not simply “best optimized.”

5. **Also report the best safer candidate.**
   - In the same screen, `SET +1.2 V`, `RESET -1.5 V`, `1 ms` gave a more credible safer contrast: median read-after-SET `~5.9e-8 A`, median read-after-RESET `~3.1e-9 A`, ratio `~19×`, max read current `~5.4e-7 A`.

6. **Always cleanup and verify.**
   - Force Keithley and Keysight outputs off.
   - Run 707B `open_all` and `get_closed_channels`; expected safe result is `nil`.
   - Verify final machine states idle where possible.

## Plot/report pattern

Generate a combined plot with:

- Keithley low-bias health check current vs voltage.
- Median current ratio by candidate.
- All candidate read currents on log scale, preserving actual read-after-SET and read-after-RESET points.
- Best-candidate per-cycle read-after-SET/read-after-RESET traces on log scale.

User-facing wording should distinguish:

- **Highest observed numerical ratio**: may be unsafe if read current reaches compliance.
- **Best safer condition**: lower ratio but below read-current safety limits.

## Key pitfall

Do not call a high-ratio candidate “optimized” when the ratio is caused by SET reads near current compliance. For this class of device, the correct conclusion is often: “highest observed ratio occurred at an unsafe/over-formed condition; use the best safer candidate or improve contact before further optimization.”
