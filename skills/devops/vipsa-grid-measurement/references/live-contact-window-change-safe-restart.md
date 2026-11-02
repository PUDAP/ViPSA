# Changing the contact-current window during a live grid run

Use this pattern when the user changes the approach/contact-current window while a grid runner is active.

## Safe boundary procedure

1. Determine the active device and phase from the tracked runner output.
2. Stop the runner immediately if the old window must not govern the current approach. Pause automated per-device reporting while active folders may be archived/recreated.
3. Run electrical cleanup through PUDA: both SMU outputs off, 707B `open_all` then verify `get_closed_channels == nil`, lights off. Verify all machines idle and `run_id: null`.
4. Read live stage and Zaber positions. A killed approach can leave the stage at an intermediate Z and may leave a stale run id; clear/recover it before new commands, then re-read position.
5. Archive the active partial device directory rather than deleting or overwriting it.
6. Restart from that same device as a **current-position handoff**: do not repeat lateral movement or blindly apply the normal `-50/+30` travel sequence. Start a fresh bounded approach from the verified live Z unless the user explicitly asks to reuse an already completed approach.
7. Resume the per-device reporter only after the new runner is confirmed active. If a completed device is being overwritten, remove its active path from reporter state so the replacement result is delivered.

## Parameters that must change together

Changing only the displayed lower/upper values is unsafe and ineffective. Update all of:

- `APPROACH_LOWER_A`
- `APPROACH_UPPER_A`
- approach read compliance, which must be greater than the upper bound (with sensible headroom)
- downstream `safe_contact`, `open_weak`, and `over_or_short` classification thresholds
- metadata written into summaries and approach artifacts

Example: for a requested `5e-8` to `5e-7 A` window, a `2e-8 A` read compliance can never observe the window. Use a suitably conservative compliance above `5e-7 A` (for this campaign, `1e-6 A`) and record it explicitly.

## Verification

After restart, require runner output showing the intended first device and fresh approach mode. Confirm the new `approach.json` records the requested bounds and compatible read compliance. Preserve the archived partial folder and previous completed devices.