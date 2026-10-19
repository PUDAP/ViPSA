# Terse post-alignment contact approach pattern — 2026-06-30

Use this reference when the user gives a terse command such as `approach` immediately after a ViPSA pad-alignment / move-to-device operation.

## Operational interpretation

When the surrounding context is ViPSA and the device has just been aligned, interpret `approach` as authorization to run the established Keithley-guided Z contact approach, not as a request for a plan or parameter clarification.

Use the established defaults unless the user has just overridden them:

```text
test_voltage = 0.01 V
lower_current_threshold = 1e-8 A
upper_current_threshold = 1e-7 A
current_compliance = 1e-6 A
step_size = 0.5 Z steps when the previous pre-move/retraction was large or recent; otherwise use the current standard default
trim_step = 0.25 Z steps
max_attempts = enough to cover the immediately preceding safe Z retraction while bounded, e.g. 120 attempts at 0.5 after a ~35-step clearance move
forward = +Z
lights = turn off before electrical approach
```

## Execution details learned

- Prefer protocol-first when it is working, but a direct core-NATS fallback may be used for the known ViPSA NATS/advertised-route outage if it produces verified machine responses.
- Use one-command transactions for `light.turn_off`, `keithley-2450.set_output(false)`, `keithley-707b.connect_keithley_smu`, each Keithley read, and each `stage.move_z_by`.
- Read current with `keithley-2450.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s≈0.05–0.2, read_count=1, reset=true on first read only)`.
- Use `abs(I)` for window detection.
- If all bounded attempts remain far below threshold (pA/sub-nA), stop as `no_contact_after_max`; do not auto-continue or run DCIV/pulses.
- Always cleanup with Keithley output off, 707B `open_all`, `get_closed_channels == nil`, and verify relevant machines idle / `run_id: null`.

## Reporting

Keep the Telegram report concise and verification-oriented:

- Use 👇 for approach/contact approach.
- Report status, voltage/window/compliance, total net Z travel, final current, final stage Z readback, and cleanup verification.
- If current remains pA/sub-nA after the bounded approach, say **no contact detected** rather than implying a successful approach.
