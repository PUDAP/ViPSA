# Manual Z increment followed by low-bias resistance check (2026-06-25)

## Trigger

Use this pattern when the user explicitly combines a microscope-stage Z move with a resistance/contact check, for example:

```text
move z up by 25 steps and check resistance
```

This is a single authorized chain: execute the requested Z move first, then run a non-stressing Keithley/707B resistance diagnostic.

If the user says `measure current` rather than `check resistance`, do not automatically substitute the full multi-bias resistance table. Execute the requested Z move, then run a compact Keithley current measurement at `+0.1 V` by default unless the user specified another bias. See `vipsa-electrical-measurements/references/manual-z-move-then-measure-current-2026-07-01.md`.

## Procedure

1. Verify relevant machines are idle: `stage`, `keithley-2450`, `keithley-707b`, and `light` if relevant.
2. Run a full-metadata PUDA protocol for the requested signed Z move only:
   - User convention: **up = +Z**.
   - Example: `stage.move_z_by(height=25, feedrate=450)`.
3. Verify the motion path:
   - Run a separate `stage.get_current_position()` protocol after the move.
   - Report numeric readback if available; do not treat tracked Z as physical truth if the user/video indicates the motor did not move.
   - If the stage edge was restarted, assume its tracked origin may have reset to `0`. In that case `0 -> +N` confirms only the fresh relative command/readback chain; do not add it to or compare it as an absolute continuation of a pre-restart tracked Z. State this caveat before interpreting contact changes.
   - Do not begin the electrical check if the fresh move response or post-move readback failed.
4. Run a conservative Keithley resistance/contact check:
   - `keithley-2450.set_output(enabled=false)`.
   - `keithley-707b.connect_keithley_smu()`.
   - `keithley-2450.hold_voltage_measure_current(...)` at `0 V`, `+10 mV`, `-10 mV`, `+50 mV`, `-50 mV` with low compliance such as `1e-6 A`.
   - Use `reset=true` on the first read and `reset=false` on subsequent reads when preserving the setup is safe.
5. Cleanup even if parsing fails:
   - `keithley-2450.set_output(enabled=false)`.
   - `keithley-707b.open_all()`.
   - `keithley-707b.get_closed_channels()`; expected safe result is `nil`.
   - Verify machine states return to `idle` with `run_id: null`.
6. Report compactly:
   - Signed Z move and stage readback.
   - Current at each low-bias probe.
   - Paired differential resistance from ±10 mV and ±50 mV when both polarities are available.
   - Contact classification: pA/sub-nA and GΩ-scale = very high resistance/open-like, not a short or low-resistance contact.

## Example observed outcome

After a prior no-contact approach ending at tracked `z=70`, a requested `+25 Z` move succeeded and read back `z=95`. Low-bias reads stayed pA-scale:

- `0 V`: `~6.0e-11 A`
- `+10 mV`: `~6.6e-11 A`
- `-10 mV`: `~5.1e-11 A`
- `+50 mV`: `~9.1e-11 A`
- `-50 mV`: `~2.2e-11 A`

Paired differential estimates were about `1.3–1.4 GΩ`, so the correct concise interpretation was: **still pA-scale / very high resistance; no short / no low-resistance contact**.
