# S3 8x8 grid pause + early-device failure analysis (2026-06-26)

## Context

During an S3 8x8 probabilistic-computing grid run, the user requested:

- start from the current manually approached device;
- preserve prior grid electrical logic except:
  - reset side never runs positive voltages;
  - SET side strictly `PF: 0 -> +1 V` and `PB: +1 -> 0 V`;
  - if initial DCIV `max |I| < 5e-9 A`, classify `possible permanent HRS / poor contact`, move stage Z `+0.5`, retry same DCIV, then if still low retry higher-compliance DCIV as `DCIV_RETRY_*` with positive `1e-5 A` and negative `1e-4 A`.

The run was paused after device 5 completed.

## Pause-after-current-device pattern

When the user asks to "pause after finishing current device" during a running grid:

1. Identify the active runner PID and current device by reading newest `device_*/summary.json` with `status: started` and no `finished_utc`.
2. Start a small watcher that polls that current device summary until `finished_utc` appears or status becomes terminal.
3. Immediately terminate the runner after the current-device summary is complete, before the next device can perform motion/electrical work.
4. Run cleanup after terminating the runner:
   - `keithley-2450.set_output(false)`
   - `keysight-b2902b.set_output(false)`
   - `light.turn_off()`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` and require `nil`
5. Verify all six ViPSA machines are `idle` with `run_id: null`.

### Pitfall: next-device summary pre-created

The runner may create `device_N+1/summary.json` immediately after finishing the current device, before the watcher kills it. If that next folder only contains `summary.json` and no alignment/approach/DCIV/pulse artifacts, mark it explicitly as `paused_before_measurement` rather than leaving `status: started`. This prevents future resume/analysis code from treating it as an interrupted measured device.

### Pitfall: `idle` with non-null `run_id`

After killing the runner, a motion machine can report `state: idle` but still carry a non-null stale `run_id`. Treat `idle + run_id != null` as not fully clean. Complete that exact run id on the machine's immediate subject (or use the established stale-run cleanup path), then re-read state and require `run_id: null` before reporting pause complete.

## Early-device analysis pattern

For a paused grid, analyze only completed devices with saved measurement artifacts. Do not include a `paused_before_measurement` next-device placeholder.

Useful per-device fields:

- approach status and final approach current;
- `open_weak_override` / `over_short_override` flags;
- DCIV `precheck_10mV_current_a`, `pre_short_like`, `max_abs_current_a`, `vset_v`, `set_detected`, `reset_detected`, events, compliance-hit counts;
- randomized pulse trains collected, compliance-hit count, threshold, read-after-SET and read-after-RESET medians/quantiles, reset-high fraction, sigmoid fit status.

Interpretation rules from S3 devices 1–5:

- Devices with low-voltage precheck near read compliance and DCIV/pulse compliance hits are short-like or over-formed. If read-after-SET and read-after-RESET are both pinned at compliance, do not call stochastic switching.
- Devices with `no_contact_after_max`, approach current around `1e-10 A`, and DCIV `max |I| < 5e-9 A` after same-compliance and higher-compliance retries should be reported as `possible permanent HRS / poor contact`; apparent pulse probabilities from nA-scale read offsets are not reliable evidence of memristive switching.
- If SET-like DCIV exists but RESET is absent and pulse read distributions overlap strongly, report marginal/failed operation rather than a working probabilistic device.
- Apparent high `P_switch` is suspect when reset-high fraction is also high or when the DCIV never established meaningful conductive coupling.

## Recommended safe-boundary adaptation

Before continuing from the next unmeasured device after this failure mix, add a compact Keithley low-bias contact diagnostic (`0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`) before full DCIV/pulses:

- pA/sub-nA: perform a small `+0.25` or `+0.5` Z contact-improvement step and repeat diagnostic before stress.
- near read compliance at `10 mV`: retract slightly / treat as over-contacted or short-like.
- stable middle-range voltage-scaled current: proceed with full DCIV/pulse.
