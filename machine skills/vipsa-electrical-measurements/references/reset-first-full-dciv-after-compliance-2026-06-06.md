# Reset-first full DCIV after compliance-limited forming

Session pattern from 2026-06-06 ViPSA memristor work.

## Context

After contact approach, a conservative positive forming branch (`0 -> +0.80 V`, `100 nA` compliance) became compliance-limited almost immediately. The user then explicitly requested a whole DCIV but with an additional negative/reset side first.

## Reusable workflow

When the user explicitly requests a full DCIV despite an earlier compliance-limited branch, do not silently keep the earlier branch-safety stop as the end condition. Instead:

1. Verify machines are idle and force Keithley output off.
2. Route DUT to Keithley via `keithley-707b.connect_keithley_smu()`.
3. Take a low-bias pre-read, e.g. `+10 mV`, and record current/resistance.
4. Run an extra reset side first:
   - `RESET_PRE_NF`: `0 -> -Vneg`
   - `RESET_PRE_NB`: `-Vneg -> 0`
5. Then run the whole DCIV cycle:
   - `PF`: `0 -> +Vpos`
   - `PB`: `+Vpos -> 0`
   - `NF`: `0 -> -Vneg`
   - `NB`: `-Vneg -> 0`
6. Preserve branch labels in CSV/JSON/plot; do not sort points by voltage.
7. Take a low-bias post-read.
8. Cleanup and verify: Keithley output off, 707B `open_all`, `get_closed_channels() == nil`, final machine states idle.

## Example parameters used

- Step: `50 mV`
- Positive side: `+0.80 V`, `100 nA` compliance
- Negative/reset side: `-1.50 V`, `500 nA` compliance
- Return/readback branches: `100 nA` compliance
- Low-bias read: `+10 mV`, `1 uA` compliance

## Safety / interpretation rule

If the user has explicitly asked for a full sweep, compliance hits alone should be reported as measurement outcome rather than used as an automatic stop, provided the current remains within the requested compliance/safety envelope. Keep a hard danger guard for unexpectedly high current, instrument faults, or measured-voltage collapse outside the planned compliance behavior.

Report per-branch row counts and compliance-hit counts. In the observed run, the reset-first side did not recover HRS: pre/post `+10 mV` reads were both about `0.49 uA` (~`20 kOhm`), and most points on all branches were compliance-limited.
