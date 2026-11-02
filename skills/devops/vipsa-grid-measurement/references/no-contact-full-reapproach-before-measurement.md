# Required full re-approach after max-attempt no-contact

Use this policy when a grid user says that a device must be approached again if the first bounded approach ends with `no_contact_after_max`.

## Required sequence

1. **Do not begin DCIV or pulse measurement after attempt 1 reports `no_contact_after_max`.**
2. Preserve attempt 1 as `approach_attempt_1.json` and retain its current/Z trace in the device summary.
3. Re-check alignment before retry when that can be done safely. Do not silently reuse a stale alignment after lateral travel.
4. Run one complete bounded approach again with the same configured contact window, step sizes, maximum attempts, and a read compliance high enough to observe the window.
5. Preserve the retry separately as `approach_attempt_2.json` / `approach_retry_after_max` and make it the active `approach` result for downstream classification.
6. Repeat the post-approach electrical health check after attempt 2; do not gate measurements using health metadata captured before the retry.
7. Only after attempt 2 finishes may the workflow apply the configured policy for persistent no-contact (stop/skip, diagnostic rescue, or an explicit user-authorized no-skip measurement override).

## Applying this to a live runner

A running Python process will not pick up patched constants or control-flow changes. Apply the policy at a controlled restart boundary:

1. Stop the tracked runner before the old policy starts measurement on the affected device.
2. Pause its per-device reporter.
3. Force both SMU outputs off, open the 707B, turn lights off, and verify cleanup.
4. Recover stale machine ownership if needed and read live stage/Zaber positions.
5. Archive the partial current-device folder; preserve completed devices before the restart boundary.
6. Restart from the exact current device/position. The first resumed operation is the required fresh/retry approach—not lateral movement or immediate measurement.
7. Verify the runner emits the current-device start event, then resume the reporter.

## Contact-window coherence

When changing the window, patch all of these together:

- approach lower and upper bounds;
- read compliance above the upper bound with conservative headroom;
- `safe_contact`, `open_weak`, and `over_or_short` classifications;
- summary metadata and event logs.

For example, a `50–500 nA` window cannot be measured with a `20 nA` read compliance. A `1 µA` read compliance provides enough headroom while still bounding the diagnostic.

## Reporting

Report attempt 1 and attempt 2 independently. If attempt 2 still has no contact, say so directly; do not describe diagnostic voltage response or an explicit no-skip stress override as successful contact.