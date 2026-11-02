# Direct NATS command path + align→approach edge handling (2026-06-09)

## When this applies

Use this note when PUDA protocol routing or `puda machine state` is stale/unreliable during ViPSA operations, but the edge machines are still responsive over NATS. This came up during an align→approach session where `puda protocol run` attempted a stale route while direct commands on the active `100.109.131.12` NATS server still worked.

## Direct command pattern that worked

A direct one-command transaction can bypass the CLI protocol runner:

1. Connect to the active NATS server. Probe `100.109.131.12:4223` and `:4224` if `:4222` behaves oddly; in this session `:4223` was the reliable control port.
2. Subscribe to both response subjects:
   - `puda.<machine>.cmd.response.immediate`
   - `puda.<machine>.cmd.response.queue`
3. Publish `start` to `puda.<machine>.cmd.immediate` with a fresh `run_id`.
4. Publish the desired driver method to `puda.<machine>.cmd.queue` with `step_number: 1`.
5. Wait for the response whose header `run_id` matches and whose command `step_number` is `1`.
6. Publish `complete` to `puda.<machine>.cmd.immediate` with the same `run_id`, even after an error, so the machine does not remain active.

Plain `nc.publish(...)` on the connected NATS client was sufficient for this command path in the session. Do not assume JetStream publish is always required for direct control; verify with a harmless read-only command such as `zaber.get_current_position(units=None)` or `light.turn_on`/`turn_off` when safe.

## Clearing active-run mismatch

If a machine rejects new commands with a message like:

```text
RUN_ID_MISMATCH: cannot start, <old-run-id> is currently running
```

try to clear it by publishing `complete` on `puda.<machine>.cmd.immediate` using the reported currently-running run ID, then verify with a read-only command. This cleared a stuck `stage` active run after a timed-out foreground approach process.

Do not invent or guess the run ID. First probe with a fresh `start`; use the exact currently-running ID reported in the response.

## Align→approach contact-edge behavior observed

During a combined align→approach run:

- Vision alignment finished well, with final pad offset around a few pixels from the ROI center.
- Coarse +Z approach produced pA current until a sudden compliance-level contact at the edge.
- Retracting by repeated valid Z increments found a sharp transition back to pA current.
- A final +0.25 Z step (the minimum hardware-supported Z increment) can jump slightly above the configured upper current threshold.

Operational rule: if the final fine step lands just above `upper_current_threshold`, do one minimum valid retract (`-0.25` Z) and re-read before leaving the tool. Report the final state candidly as “contact edge / safely below contact” rather than a fully stabilized contact if the post-retract current is below the lower threshold.

## Cleanup and reporting standard

After any interrupted or direct-command approach:

- `keithley-2450.set_output(enabled=false)`
- `keithley-707b.open_all()`
- `keithley-707b.get_closed_channels()` expected `nil`
- Verify final `stage.get_current_position()` and `zaber.get_current_position(units=None)` if motion occurred.

Report:

- alignment final offset and annotated image path if available
- final stage/Zaber positions
- whether current is inside threshold, over threshold, or safely below contact
- cleanup evidence (`output off`, `open_all`, closed channels `nil`)
