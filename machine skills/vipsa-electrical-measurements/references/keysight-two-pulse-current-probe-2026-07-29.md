# Keysight two-pulse current probe: RESET pulse then read pulse (2026-07-29)

## Trigger
Use when the user asks to “measure current once” at a stress/reset pulse and then at a low read pulse using Keysight, without requesting a long pulse train.

## Pattern
1. Route the DUT to Keysight via 707B (`connect_keysight_smu`) and ensure both SMUs are output-off before routing.
2. Use `keysight-b2902b.run_voltage_pulse_train` with a two-voltage list, not a DC sweep:
   ```json
   {"voltages": [-1.5, 0.1], "current_compliance": 1e-5, "pulse_width_s": 0.01, "acquire_delay_s": 0.001, "current_autorange": true, "reset": true}
   ```
   If the user supplies pulse width/compliance, preserve those values; otherwise state the assumptions concisely.
3. Save `responses.json`, a compact CSV of returned pulse rows, and a summary JSON under a run directory.
4. Report both commanded and measured voltage/current. For compliance-limited pulses, measured voltage may collapse far from the commanded voltage; do not say the full stress voltage was delivered.
5. Cleanup: Keysight output off, 707B `open_all`, verify `get_closed_channels == nil`, and final machine states idle/null.

## Concrete result that motivated this note
For requested `-1.5 V` then `+0.1 V` with assumed `10 ms`, `10 µA` compliance:
- `-1.5 V` command measured about `-0.100 V`, `-10.0 µA`: current compliance hit; voltage collapsed.
- `+0.1 V` command measured about `+0.097 V`, `+10.0 µA`: read pulse also hit compliance.

Wording: “Both pulses hit current compliance; the -1.5 V pulse did not deliver full voltage.”
