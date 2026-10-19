# Grid mid-run approach-parameter change (2026-06-24)

Reusable pattern for a long ViPSA grid/resume run when the user changes contact-approach parameters mid-run (for example changing approach read voltage while keeping a specified current window).

## Trigger

Use when a grid continuation runner is already active and the user asks to change approach parameters for remaining devices, such as:

- approach read voltage
- contact-current lower/upper window
- approach read compliance
- step/trim policy

## Safe restart sequence

1. Identify the active tracked runner process and current/partial device from the run directory, not from stale background notifications.
2. Stop the old runner before editing behavior.
3. Immediately force/verify electrical cleanup:
   - Keithley 2450 `set_output(false)`
   - Keysight/B2902 `set_output(false)`
   - Keithley 707B `open_all()`
   - verify `get_closed_channels()` is `nil`/none
4. Patch the continuation runner constants rather than relying on ad-hoc CLI state:
   - `START_AT_DEVICE=<first unfinished/partial device>`
   - approach test voltage constant
   - approach lower/upper current constants
   - read compliance constant; choose a compliance above the upper threshold but still conservative for the diagnostic
   - `approach.json` / summary params must write the same values used by the live read calls
5. Archive any partial folder for the restart device before rerun, especially if it may contain artifacts generated under old approach parameters.
6. Prune `summary.partial.json` for devices at/after the restart device and append a resume event explaining the parameter change. Keep completed devices and artifacts intact.
7. Restart the runner as a tracked background process with completion notification.
8. Verify after restart:
   - new runner PID/session is alive
   - restart device `summary.json` is recreated
   - `approach.json` once present records the new `test_voltage_v`, `lower_a`, `upper_a`, and `read_compliance_a`
   - if the run is configured for no recording, no new `camera*_resume_*.mp4` files appear

## Concrete parameter example

The user requested approach at `0.1 V` while keeping a `1e-10 A` to `1e-8 A` contact window. The continuation runner was patched to constants equivalent to:

```python
APPROACH_TEST_V = 0.1
APPROACH_LOWER_A = 1e-10
APPROACH_UPPER_A = 1e-8
APPROACH_READ_COMPLIANCE_A = 1e-7
```

The active partial device was archived, the summary was pruned from that device onward, and the grid was restarted from the archived device so no device mixes old and new approach settings.

## Reporting standard

Keep the user-facing report concise and verified:

- old runner stopped
- electrical outputs/routes cleaned and verified
- new approach voltage/window/compliance
- restart device
- new tracked session/PID
- partial device archived if applicable
- no-video check if relevant

Do not include NATS, RTSP, or other connection strings in the report or reference; redact them if present in logs.
