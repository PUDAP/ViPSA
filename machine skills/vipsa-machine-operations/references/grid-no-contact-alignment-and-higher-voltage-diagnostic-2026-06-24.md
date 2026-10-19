# Grid no-contact fallback: alignment recheck + sequential higher-voltage diagnostic

Use this when a long ViPSA grid/resume run reaches `no_contact_after_max` during Keithley-guided approach and the user wants future devices handled more aggressively before declaring open/no-contact.

## Trigger

- Active grid/resume runner is processing multiple devices.
- Approach result for a device is `no_contact_after_max` or equivalent: maximum allowed Z travel was reached while current stayed at pA/sub-nA/open-like levels.
- User asks to apply the behavior "for devices now onwards" or similar.

## Operational pattern

1. Stop or pause the active runner at a safe boundary if code changes are required.
2. Preserve completed device folders and archive only the incomplete current-device folder, if needed, before restarting from that device.
3. Patch the continuation runner so future `no_contact_after_max` cases perform:
   - a visual/alignment recheck step before accepting no-contact,
   - a guarded low-current higher-voltage contact diagnostic,
   - then the existing open/weak-contact handling.
4. Keep camera/video recording disabled if the user previously said `do not record` / `stop recording`.
5. Restart the continuation runner from the first unfinished device and verify a fresh `summary.json`/started marker is created.

## Suggested Keithley diagnostic ladder

Use a conservative read compliance such as `1e-6 A` and short settle/read settings appropriate for the existing runner. Suggested sequential biases:

- `0 V`
- `+0.01 V`
- `+0.05 V`
- `+0.10 V`
- `+0.20 V`
- `+0.50 V`

Record the result per device, for example in `higher_voltage_contact_check.json`, including voltage, measured current, compliance status if available, and the classification used by the runner.

## Safety and reporting

- Treat this as a diagnostic, not permission to form or stress the device indefinitely.
- Force Keithley output off and 707B open/nil in cleanup paths.
- If higher-voltage reads reveal a sudden current jump, classify as contact/alignment-dependent or weak contact rather than silently proceeding as open.
- If current remains pA/sub-nA with no voltage dependence, classify as open/no-contact or HRS beyond measurement sensitivity.
- Report the restart PID/session, first device restarted, and whether new video artifacts were avoided when recording was disabled.
