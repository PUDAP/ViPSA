# Early-grid contact-threshold adjustment notes

Use this note when the first devices in a ViPSA grid run fail or behave suspiciously during approach/contact detection.

## Durable pattern

If the initial devices show weak/no-contact, over-contact risk, or inconsistent low-bias current before DCIV/pulses:

- Treat the approach/contact threshold window as an experiment parameter, not a fixed constant.
- Prefer a narrow low-current contact window before stressing the DUT. In the June 2026 S3 batch run, the user explicitly requested lowering the contact window to:
  - lower contact threshold: `1e-9 A`
  - upper contact threshold: `1e-8 A`
- Keep approach bounded:
  - small Z steps, e.g. `0.5` step approach increments
  - optional final trim, e.g. `0.25` step
  - a hard max-attempt limit, e.g. `120`
- If restarting mid-grid, preserve completed devices in the actual traversal order and resume from the current device rather than re-running earlier devices.
- Archive partial device folders before rerunning the same device with changed thresholds so old and new artifacts are not mixed.

## Pitfall

Do not silently skip DCIV or pulse sections because a safety gate classified contact as weak/no-contact if the user has explicitly requested that DCIV/pulses still be attempted. Instead, keep conservative electrical limits, clearly label contact quality in the summary, and run the requested downstream sections unless doing so would create an immediate hardware-safety hazard.

## Verification before reporting

Before telling the user the restart/change is active, verify with real state where possible:

- old background runner is terminated or no longer the active one
- relevant machines are idle / cleaned up before restart
- new runner process/session id exists
- active script contains the intended thresholds
- current device summary/artifacts show the expected restart point
