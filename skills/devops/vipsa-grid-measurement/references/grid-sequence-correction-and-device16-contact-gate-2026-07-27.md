# Grid sequence correction and device-16 contact gate (2026-07-27)

## Trigger

Use this note for ViPSA grid continuations, especially when resuming from a current/manual handoff device and then continuing to subsequent devices.

## User-corrected default grid travel sequence

The user corrected the default inter-device sequence. For all future grid measurements unless explicitly overridden, use:

```text
stage.move_z_by(-50)
zaber.move_x_to(target_x)
zaber.move_y_to(target_y)
align
stage.move_z_by(+40)
approach
```

Important correction: **do not** do the older `+30` pre-approach before alignment. Alignment happens at the safe/retracted optical position, then the `+40` Z pre-approach happens immediately before electrical approach.

## Current-device handoff with explicit Z move

When the user says a current device is already the boundary device and asks for a manual Z move plus approach before continuing, treat that boundary device specially:

1. Verify no active grid runner is still alive.
2. Archive stale/partial boundary-device artifacts before overwriting, while preserving previous completed devices.
3. Force electrical cleanup and lights off.
4. Do **not** move Zaber or re-align if the user asks to operate the current device in place.
5. Run the explicit stage-Z move first, e.g. `stage.move_z_by(+15)`.
6. Save before/after stage readbacks in the boundary device summary.
7. Run bounded Keithley-guided approach for that device.
8. Only if stable contact is confirmed should the runner execute DCIV/pulses for that device and continue to subsequent devices.
9. If the boundary approach does not reach the required stable current window, save the boundary device as skipped/contact-gated and stop the continuation; do not move to later devices.

## Approach retry behavior

For this user's current narrow contact policy:

- Required contact: three stable reads in `1–10 nA` at `10 mV`.
- Bounded retries: two `+0.5`-step approach blocks, then one `+1.0`-step block.
- Do **not** insert a gross/inter-attempt retract between subsequent approach blocks. Continue from verified current Z, preserving only minimum negative safety trims after over-current.
- If final approach remains pA/sub-nA/no-contact, skip DCIV/pulses and record `skipped_contact_not_in_window`.

## Concrete outcome captured

A device-16 handoff used: cleanup/lights off → current-position Zaber read → stage readback `Z=27.5` → `stage.move_z_by(+15)` → stage readback `Z=42.5` → three bounded approach blocks. The approaches remained pA-scale (`~3e-11 A`) and did not reach the `1–10 nA` stable window, so device 16 was saved as `skipped_contact_not_in_window`; no DCIV/pulses ran; the grid did not continue to later devices. Cleanup verified SMU outputs off, 707B `nil`, machines idle/null, and a final stage readback of `Z=142.5` after final failed-attempt retract.

## Pitfalls avoided

- Do not continue the grid after a boundary-device approach failure simply because the user asked to continue on success; the continuation is conditional on stable approach.
- Do not re-run Zaber travel/alignment on the first current-position boundary device unless the user requests it.
- Do not let stale `DONE.json` or stale partial `device_N` folders skip the requested fresh boundary device; archive/prune/reset reporter state before launch.
- Do not treat a successful software stage readback as physical proof if visual evidence contradicts motion; report only what was verified.
