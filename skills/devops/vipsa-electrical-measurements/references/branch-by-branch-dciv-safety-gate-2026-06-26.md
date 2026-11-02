# Branch-by-branch DCIV safety gate after early-device failures — 2026-06-26

## Use case

Use this pattern when prior devices in a run show short-like low-bias reads, open/weak contact, no meaningful voltage coupling, or negative-branch breakdown/over-reset. The goal is to prevent repeating the first-device failure mode on later devices.

## Electrical sequence

### 1. Pre-stress low-bias health

Measure current at:

- `0 V`
- `±10 mV`
- `±50 mV`
- `±100 mV`

Use low read compliance, typically `1e-6 A` or lower.

Classify before stress:

- **Short-like / over-contact:** any low-bias read near compliance. Stop DCIV/pulses unless user explicitly overrides.
- **Open-like / no voltage scaling:** run contact diagnostic and bounded Z rescue before stress; skip stress if unresolved.
- **Measurable / voltage responsive:** proceed to positive branch.

### 2. Positive branch gate

Run only the positive branch first:

- `0 → +1.0 → 0 V`
- compliance around `1e-6 A`

Stop if low-voltage positive points already hit compliance or measured voltage/current indicate short-like behavior.

After the branch, perform a low-bias read, e.g. `+10 mV` at `1e-6 A`. If it is compliance-limited, do not run the reset branch.

### 3. Reset branch gate

For fragile continuation after early failures, do not jump to `-1.5 V / 1e-5 A` or higher-compliance reset recovery. Start with:

- `0 → -1.0 → 0 V`
- reset compliance around `1e-6 A`

Stop reset immediately if:

- current jumps upward by `>= 0.5 log10` in one voltage step
- current reaches `>= 0.9 * compliance`
- current unexpectedly enters the µA range

Record `next_reset_voltage_v` as a less-negative cap for the next device if an upward reset jump appears.

### 4. Post-branch truth criterion

Low-bias read probes after each branch decide whether SET/RESET is meaningful. Do not infer success from stress-branch shape alone.

Set a `pulse_allowed` gate only if:

- no safety stop occurred
- coupling was meaningful, e.g. `max |I| >= ~5 nA`
- SET-like transition was detected without low-voltage compliance artifact.

## Pulse handoff

Only run randomized pulse trains if `pulse_allowed` is true. For fragile continuation after early failures:

- reduce reset pulse from the older `-1.5 V` style to about `-1.0 V`
- reduce pulse compliance from `1e-4 A` to about `1e-5 A`
- do not fix permanent-HRS/open-like pulse reads by moving Z or increasing compliance inside the pulse loop; stop and record the gate closure.

## Reporting fields

Per-device `dciv.json` / `summary.json` should include:

- `safety_stop`
- `stop_reason`
- `pulse_allowed`
- `policy`
- `events[]` with safety stops and contact-rescue outcomes
- `compliance_hits` by segment
- `precheck_10mV_current_a`

## Pitfall

A prior user-authorized override to keep testing overcontact/short-like devices must not leak into failure-prevention runs. Unless explicitly re-authorized, low-bias compliance/short-like contact is a hard stop, not a reason to run reset-pre, DCIV, or pulses.
