# Safe ON/OFF pulse optimization and scatter-only plotting (2026-06-29)

## Context

A contacted PEA-based ViPSA memristor device showed a useful-looking `+1.0 V` SET retention response only when SET compliance reached around `100 µA`, but a later 500-cycle `SET-read-RESET-read` train drifted upward until some low-bias reads approached/read-hit the same compliance. The user asked to maximize ON/OFF ratio while keeping the device safe.

## Workflow that worked

Use short bounded screening batches rather than another long endurance test:

1. Force Keysight output off and route through the 707B to Keysight.
2. Test short `RESET -> read_HRS -> SET -> read_LRS` candidates.
3. Use a lower read voltage than the previous endurance test when trying to stay safe (for example `+20 mV` instead of `+50/+100 mV`).
4. Start with low/symmetric compliance and short pulses:
   - `SET = +0.8 to +1.0 V`
   - `RESET = -1.2 to -2.0 V`
   - pulse width `5–10 ms`
   - compliance around `10 µA`
   - `20` cycles per candidate is enough for a first screen.
5. If low-compliance screens give only ~1x separation, try asymmetric compliance in very small batches:
   - low-compliance RESET, e.g. `10 µA`
   - low-compliance read, e.g. `1 µA`
   - short SET pulse at the minimum compliance that previously formed, e.g. `50–100 µA`, `5 ms`
   - `10` cycles per candidate.
6. After every candidate compute:
   - median read-after-SET current
   - median read-after-RESET current
   - median ON/OFF ratio = `median(|I_SET_read|) / median(|I_RESET_read|)`
   - cycles with ratio >= 2/5/10
   - max read current
   - read pulses at or near read compliance
   - stress pulse compliance hits
7. Stop immediately if any low-bias read is near compliance. Do not continue to a full endurance test.
8. Always cleanup after every candidate: Keysight output off, 707B `open_all`, and verify `get_closed_channels == nil`.

## Interpretation lessons

- Do **not** call the largest single-cycle ratio the optimized condition if that ratio occurs in a candidate that hit read compliance. Treat it as unsafe/likely over-conductive.
- In this session, low/symmetric `10 µA` screens produced stable positive read currents but only about `1.1–1.2x` median separation.
- Asymmetric `100 µA` short SET + `10 µA` RESET did not produce robust separation; median ratios stayed below or near `1x` for several candidates.
- A `50 µA` SET candidate produced a larger numerical max ratio, but one `+20 mV` read hit the `1 µA` read compliance, so the run was safety-stopped and the ratio was not trusted.
- User-facing conclusion pattern: “No safe high-ON/OFF pulse condition found on this contacted device” is preferred over overclaiming an optimized condition.

## Plotting lesson

The user corrected the plotting style: for these ViPSA electrical pulse/retention screens, use **scatter/markers only** by default. Do not connect dots with lines unless the user explicitly asks for connected traces. This applies especially to retention, pulse-cycle, ON/OFF screening, and candidate-comparison plots where connecting points can visually imply continuity or trends stronger than the measured point sequence supports.
