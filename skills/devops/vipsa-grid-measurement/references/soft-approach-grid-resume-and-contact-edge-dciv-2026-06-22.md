# Soft approach grid resume and contact-edge DCIV retry (2026-06-22)

Use this when resuming an interrupted ViPSA grid run after prior devices look pre-shorted or over-contacted.

## Durable lessons

- If several completed devices show early/compliance-limited DCIV or short-like behavior, soften the approach before continuing the grid instead of reusing the normal 10–100 nA contact window.
- A useful soft contact target is **1–20 nA at 10 mV**, with **0.25 stage-Z steps** and a lower Keithley read compliance such as **200 nA** during the approach loop.
- On resume, inspect the previous device folder before acting:
  - If `align_detection.json` / alignment fields exist but no `approach.json` exists, the device was aligned but not contacted. Reuse the alignment context and run a live low-bias contact check before approach.
  - If `approach.json` exists and final current is in the current target window and no travel occurred, contact may already be valid; otherwise rerun a low-bias precheck.
- For the resume device, do **not** blindly retract/lower or redo XY movement before checking live state if the previous run already moved to and aligned that device.
- Run a pre-approach Keithley check at `0 V`, `+10 mV`, and `-10 mV`. Treat pA/sub-nA at 10 mV as open-like/not contacted, not safe contact.
- If the first DCIV after soft contact looks like no/very weak contact (for example `max |I| < 5 nA` across the sweep), move stage Z **+0.25** once and rerun DCIV once. This is the contact-edge retry requested by the user.
- Preserve hard safety gates: if the soft approach or DCIV becomes over-current/compliance-limited/short-like, do not continue to Keysight pulsing without explicit authorization.
- For Keysight `run_voltage_pulse_train`, do **not** pass unsupported `settle_s`; use `voltages`, `current_compliance`, `pulse_width_s`, and `reset` unless live command metadata proves otherwise.

## Implementation notes

Suggested resume summary metadata:

```json
{
  "resume_from_device": 5,
  "previous_run": "/path/to/previous/run",
  "soft_approach": {
    "test_voltage_v": 0.01,
    "window_a": [1e-9, 2e-8],
    "z_step": 0.25,
    "read_compliance_a": 2e-7
  },
  "dciv_contact_edge_retry": {
    "trigger": "max_abs_current_a < 5e-9",
    "z_move": 0.25,
    "max_retries": 1
  }
}
```

Recommended per-device sequence on resume:

1. Verify cleanup and machine idle/open state.
2. Load previous run grid coordinates; filter traversal to unfinished devices.
3. For the first resumed device, reuse existing alignment evidence if present and no later movement invalidated it.
4. Run low-bias pre-contact check.
5. If already in soft window, skip approach; else run soft approach.
6. Run DCIV.
7. If DCIV is no-contact/contact-edge, Z +0.25 and rerun DCIV once.
8. If DCIV is short-like/compliance-limited, skip pulses; otherwise proceed to pulse batches/checkpoints.
