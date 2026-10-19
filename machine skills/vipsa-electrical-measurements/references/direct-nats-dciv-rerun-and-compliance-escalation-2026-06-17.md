# Direct-NATS DCIV rerun and SET-compliance escalation (2026-06-17)

## Trigger
Use this note when the user asks to rerun a live ViPSA DCIV sweep on the current device with a changed current compliance, especially after the normal `puda protocol run` path has been unreliable but direct PUDA/NATS transactions are working.

## Reusable workflow

1. Keep the sweep recipe explicit in the report:
   - path used in this session: `0 -> +1 -> 0 -> -1.5 -> 0 V`
   - step: `50 mV`
   - low-bias read probes before and after the sweep at `+10 mV` and `-10 mV`
   - SET/positive compliance is the user-adjusted parameter
   - RESET/negative compliance can stay at the prior recipe unless the user changes it
2. Use the existing direct-NATS command transaction pattern only as a fallback when protocol control has already shown runner/path issues:
   - subscribe to `puda.<machine>.cmd.response.immediate` and `.queue`
   - publish `start` to both `keithley-2450` and `keithley-707b`
   - run `set_output(false)` before routing
   - route with `keithley-707b.connect_keithley_smu()`
   - issue one `hold_voltage_measure_current(...)` per point
   - cleanup inside the same run: `set_output(false)`, `open_all`, `get_closed_channels`
   - publish `complete` for both machines
3. Save partial data before cleanup if an exception occurs. Always run forced cleanup even on failure.
4. Plot from the saved CSV in a matplotlib-capable venv if the live script lacks plotting dependencies; do not rerun the electrical sweep just to regenerate plots.

## Reporting pattern

Report:
- sweep path, step count, collected/planned points
- SET-side and RESET-side compliance values separately
- pre/post low-bias read currents and approximate resistance
- max sweep current
- number of compliance-region points for SET side and RESET side
- largest positive log-current jump and largest negative log-current drop
- cleanup verification: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, and `complete` sent

## Interpretation lesson

Raising SET compliance can make the positive SET-like jump stronger and compliance-limited without producing a retained low-voltage LRS. In this session:
- `300 nA` SET compliance produced a SET-like PF jump near `+0.8 V`, but post-read stayed near `100 pA`.
- Increasing SET compliance to `1e-6 A` produced a stronger PF jump near `+0.75 V` and µA-limited points, but the post-read still relaxed back to ~`100 pA`.

Reusable wording: “Higher SET compliance produced a stronger compliance-limited SET-like transition, but the low-bias post-read still relaxed back to pA/sub-nA scale, so the device is not retaining a strong LRS at the read voltage.”

## Pitfalls

- Do not call compliance-limited SET evidence “good switching” unless the post-read/read-probe state remains separated from the pre-read HRS.
- Do not skip cleanup verification just because the command responses were successful; explicitly inspect/report `get_closed_channels`.
- Do not store one-off run IDs or device-specific conclusion in the skill body; keep those in run artifacts only.