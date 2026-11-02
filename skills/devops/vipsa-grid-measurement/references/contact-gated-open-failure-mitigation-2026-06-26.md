# Contact-gated open/weak failure mitigation for S3 grid resumes (2026-06-26)

## Context
During an S3 8x8 probabilistic-computing grid run, early devices split into two failure regimes:

- devices 1–2: short-like / compliance-limited / reset failure
- devices 3–5: weak/no-contact or permanent-HRS-like, with pA/sub-nA to sub-nA currents and no meaningful DCIV/pulse coupling

The user asked to implement practical mitigations, not just discuss them.

## Durable workflow lesson
For open/weak-contact devices, do **not** blindly convert pA/no-contact into a full DCIV + pulse run just because the older grid policy allowed an open/weak override. First distinguish poor mechanical/electrical contact from a true high-HRS/off-state response.

## Recommended implementation pattern

1. Add a multi-bias Keithley contact diagnostic before stress when approach ends open/weak or `no_contact_after_max`:
   - `0 V`
   - `+10 mV`, `-10 mV`
   - `+50 mV`, `-50 mV`
   - `+100 mV`, `-100 mV`
   - optionally `+200 mV`, `-200 mV`, `+500 mV`, `-500 mV`
   - low read compliance, e.g. `1e-6 A`

2. Use zero-offset and paired-bias behavior:
   - calculate zero-bias offset
   - compare `I(+V)-I(0)` and `I(-V)-I(0)`
   - compute paired differential resistance when possible
   - classify as voltage-responsive only when signal rises above noise/offset in a stable way

3. Classify the result:
   - `valid_contact_or_high_hrs_response`: measurable voltage response or `max |I| >= ~5e-9 A`
   - `weak_voltage_scaled_response`: weak but coherent response around `~1e-9 A`
   - `open_like_no_voltage_scaling`: pA/sub-nA with no voltage scaling
   - `short_like_or_read_compliance`: low-bias read reaches compliance

4. If still open-like, run a bounded contact rescue:
   - move microscope stage Z forward/up by the minimum valid step, usually `+0.25`
   - repeat the diagnostic
   - stop after a small budget, e.g. 2–3 increments

5. Only run DCIV if the diagnostic/rescue shows voltage-responsive contact or a plausible high-HRS response. If it remains open-like/no-voltage-scaling, save the diagnostic artifacts and skip DCIV/pulses.

6. If DCIV itself finishes with `max |I| < ~5e-9 A`, run the same diagnostic/rescue before deciding whether another same-compliance DCIV retry is meaningful.

7. Do **not** automatically escalate to higher DCIV compliance on a no-voltage-scaling open-like device. Higher compliance does not fix missing contact and can create misleading stress artifacts.

8. Gate randomized SET-read-RESET-read pulses:
   - run pulses only if DCIV/contact diagnostic shows meaningful coupling
   - otherwise mark pulses as skipped: `DCIV/contact diagnostic never showed meaningful coupling; randomized pulses would not be physically meaningful`

## Relationship to older open/weak override policy
Older grid runs had a user-corrected policy to avoid skipping devices solely because approach was weak/open-like: move Z forward and try the requested measurement. This S3 mitigation refines that policy: the Z rescue is still attempted, but it is paired with a multi-bias diagnostic and a skip gate when contact remains invalid. Preserve explicit user overrides if the user says to run despite invalid contact, but record the override clearly.

## Artifacts to save per device

- `contact_diag_initial.json`
- `contact_diag_after_z_plus_<n>.json`
- `open_contact_rescue.json`
- summary fields such as:
  - `open_contact_rescue.status`
  - `open_contact_rescue.valid_for_stress`
  - `open_weak_gate`
  - pulse skip reason if applicable

## Verification
Before considering the runner patched:

- Run `python3 -m py_compile <runner.py>`.
- Confirm the resume script points to the existing run directory if resuming, not a new timestamped folder.
- Confirm `START_AT_DEVICE` matches the intended resume boundary.
- Confirm completed devices before the resume boundary are preserved in `summary.partial.json` or explicitly archived/pruned by policy.
