# No-skip DCIV/pulse override after a safety-gated grid resume (2026-06-26)

Use when a long ViPSA grid continuation was patched to skip DCIV/pulses on open/weak/short-like contact gates, and the user explicitly corrects that policy with wording like: **"do not skip running DCIV/Pulses"**.

## Durable workflow lesson

The user may prefer the electrical sequence to run on every device even when contact diagnostics classify the device as open-like, weak-contact, over-contacted, or short-like. In that case:

1. Stop the active safety-gated runner at a safe boundary if it would continue skipping devices.
2. Cleanup/verify hardware before patching/restarting:
   - SMU outputs off.
   - 707B open/all channels nil when possible.
   - ViPSA machines idle or deliberately busy only from the known active runner.
3. Archive stale device folders from the restart boundary onward, especially folders already marked `DONE.json` with skipped DCIV/pulse summaries.
4. Prune `summary.partial.json` / `summary.json` device entries from the restart boundary onward, preserving completed earlier devices.
5. Generate a no-skip continuation runner rather than mutating the old safety-gated runner in place.
6. Patch the runner so contact/safety gates are **record-only flags**, not blockers:
   - Record `open_weak`, `over_or_short`, `open_contact_rescue`, and `gate_flags_record_only` in the device summary.
   - Always call `dciv(...)` after approach/rescue diagnostics.
   - Set `dciv.pulse_allowed = true` under the explicit user override.
   - Always call `randomized_sigmoid_pulse(...)` after DCIV cleanup.
7. Keep the safer electrical limits unless the user changes them:
   - Keithley DCIV compliance around `1 µA`.
   - Reset branch capped near `-1.0 V` initially.
   - Pulse compliance around `10 µA`.
   - Reset pulse around `-1.0 V`.
8. Verify the patched script by compiling it and searching for the override markers before launching.
9. Start the patched runner as a tracked background process with notify-on-complete.
10. Verify restart by reading the new `device_N/summary.json` and checking for fresh `started` status plus later DCIV/pulse artifacts.

## Important distinction

This is not the same as silently deciding that unsafe devices are safe. The correct behavior is:

- Preserve diagnostics and warnings in the artifacts.
- Make the override explicit in `summary.json`, `dciv.json`, and run metadata.
- Continue the user-requested DCIV and pulse sequence despite gates that would normally skip.

## Example summary fields

```json
"user_override_no_skip_dciv_pulses": {
  "instruction": "do not skip running DCIV/Pulses",
  "safe_contact_from_gates": false,
  "open_weak": true,
  "over_or_short": false,
  "note": "Contact/safety gates are recorded as flags only; DCIV and randomized pulse train are still attempted."
}
```

For `dciv.json`:

```json
{
  "pulse_allowed": true,
  "safety_stop": false,
  "gate_flags_record_only": ["open_like_health_before_dciv"],
  "policy": "USER OVERRIDE no-skip: DCIV branches and randomized pulses are attempted; gates are recorded only; Keithley compliance 1uA and reset cap -1.0V retained"
}
```
