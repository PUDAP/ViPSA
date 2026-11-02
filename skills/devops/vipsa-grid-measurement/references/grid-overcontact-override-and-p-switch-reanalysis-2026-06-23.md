# Grid continuation with overcontact override and post-run P-switch reanalysis (2026-06-23)

## Context

During an 8×8 ViPSA grid continuation, the user explicitly overrode the normal safety/quality gating:

- even if a device shows overcontact/short-like behavior, still perform DCIV;
- run an additional reset-only sweep before normal DCIV when overcontact/short-like;
- do not skip pulsing solely because DCIV is compliance-limited.

The continuation completed the remaining 53 devices and then the user requested a different `P_switch` analysis threshold.

## Durable run-control lessons

- For long grid continuations, verify traversal order before restarting after a tweak. Row-major device numbering and serpentine traversal can diverge; resuming numerically from a device can accidentally jump to the wrong physical next device.
- If changing the continuation policy mid-run, stop the old process at a safe boundary, cleanup/verify all ViPSA machines, then resume from unfinished devices in the correct serpentine order.
- The overcontact override should be recorded in per-device summaries with enough detail to distinguish:
  - safe contact before override,
  - open/weak/contact-edge override,
  - over/short-like override.
- Even when pulsing is not skipped under explicit override, continue to record compliance-hit counts and checkpoint stops; these are quality flags, not skip gates under this override.

## Post-run analysis lessons

When the user asks to recompute `P_switch` after a completed grid run, do not rerun hardware. Reanalyze saved CSV artifacts:

- per-device `randomized_pulse_results.csv`,
- existing device plots and summaries,
- final `summary.json`.

For a non-Youden `P_switch` threshold, use the electrical-measurement reference:

- `vipsa-electrical-measurements/references/p-switch-read-after-set-distribution-threshold-2026-06-23.md`

Recommended output package:

- per-device recomputed `P_switch` CSVs,
- a summary CSV with threshold, `V50`, slope, RMSE/R², compliance hits, and P@selected voltages,
- a plot panel of best sigmoid fits,
- a plot panel showing the `read_after_set` distributions and selected thresholds for top candidates,
- concise ranking of both best mathematical fits and best clean-ish candidates.

## Interpretation pitfall

A good sigmoid fit from a distribution-derived threshold can be mathematically real but scientifically weak if:

- threshold is near noise floor,
- reset reads frequently remain above threshold,
- pulse compliance hits are high,
- the device is overcontacted/short-like,
- probabilities saturate trivially.

Report those caveats directly instead of calling the device a clean stochastic switch.
