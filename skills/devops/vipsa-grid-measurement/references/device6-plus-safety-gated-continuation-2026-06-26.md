# Device 6+ safety-gated continuation after early S3 failures — 2026-06-26

## Context

During the S3 8x8 grid run, devices 1–5 showed failure patterns that made the previous continuation policy too permissive: short-like/compliance-pinned devices were still driven through DCIV/pulses, and reset/recovery used aggressive negative stress. The user asked to implement the prevention strategy and continue from device 6 onward.

## Durable workflow update

For grid continuation after early devices show short-like, weak-contact, or reset-breakdown failures, patch the continuation runner so device N+ uses a strict branch-by-branch safety gate rather than the earlier override policy.

### Pre-stress gate

Before any DCIV stress on each device:

1. Route to Keithley with SMU output off first.
2. Run multi-bias low-compliance reads:
   - `0 V`, `+10 mV`, `-10 mV`, `+50 mV`, `-50 mV`, `+100 mV`, `-100 mV`
   - read compliance around `1e-6 A` or lower if the run is known fragile.
3. If any low-bias read reaches read compliance / looks short-like, skip DCIV and randomized pulses for that device unless the user explicitly overrides.
4. If open-like/no response, run the existing contact diagnostic/rescue flow:
   - multi-bias low-compliance contact diagnostic with offset/paired-bias classification
   - bounded `+0.25 Z` rescue steps
   - skip stress if no voltage-scaled coupling appears.

### DCIV branch policy

Use a gated DCIV instead of a blind full sweep:

1. Positive branch first: `0 → +1.0 → 0`, `1e-6 A` compliance.
2. Post-positive low-bias read at `+10 mV`.
3. Only if still safe, run reset branch capped near `0 → -1.0 → 0`, `1e-6 A` compliance.
4. Stop reset immediately on any of:
   - current jump `>= 0.5 log10` in one step
   - current entering read/stress compliance region
   - unexpected µA-scale current for a fragile device/contact state.
5. Do **not** run high-compliance reset-pre or reset-recovery sweeps automatically after early failures.
6. Use post-branch low-bias reads as the truth for whether the device remains usable.

### Pulse gate

Only run randomized SET-read-RESET-read pulse trains if DCIV returns `pulse_allowed=true`, meaning:

- no safety stop occurred
- there was meaningful coupling (`max |I| >= ~5 nA`)
- SET-like transition was detected without low-voltage short/compliance artifact.

For fragile continuation after early failures, reduce pulse stress initially:

- reset pulse around `-1.0 V` rather than `-1.5 V`
- pulse compliance around `1e-5 A` rather than `1e-4 A`
- stop pulses on permanent-HRS/open-like reads instead of moving Z or increasing compliance inside the pulse loop.

## Implementation pattern

Create a new continuation script rather than mutating the already-running/archived script in-place. In the 2026-06-26 S3 case this produced:

- `runs/resume_grid_8x8_batch1_S3_from_device6_safety_gated_20260626.py`

Key code-level flags/fields to write into per-device summaries:

- `dciv.policy`: e.g. `device6+ safety-gated branch-by-branch; no high-compliance reset recovery`
- `dciv.safety_stop`: boolean
- `dciv.stop_reason`: concise stop reason
- `dciv.pulse_allowed`: boolean
- `over_short_gate`: record that short-like low-bias contact caused a hard skip
- `randomized_pulse.skipped`: include DCIV gate reason when pulses are not run.

## Verification before restart

Before starting the continuation:

1. Compile/check the runner syntax, e.g. `python3 -m py_compile <runner.py>`.
2. Verify all ViPSA machines are visible and idle/null-run when possible.
3. Start the runner as a tracked background process with completion notification.
4. Verify the target restart device summary changes from stale `paused_before_measurement` to fresh `status: started`.
5. Ensure the existing monitor/reporter will emit per-device plot/status updates, or patch it to include the new gate fields (`safety_stop`, `stop_reason`, `pulse_allowed`).

## Pitfall

Do not preserve an older grid policy that says “still run DCIV/pulses on overcontact/short-like devices” when the user has asked to avoid early-device failures. That override is useful only when explicitly requested. For failure-prevention continuation, short-like low-bias/contact-compliance is a hard safety stop.
