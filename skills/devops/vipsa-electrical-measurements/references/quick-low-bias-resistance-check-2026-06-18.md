# Quick low-bias resistance check (2026-06-18)

Use this reference for terse live requests like `check resistance` on a current ViPSA DUT when no voltage is specified.

## Default live recipe

- Use the Keithley 2450 routed through the 707B.
- Keep this as a non-stressing low-bias diagnostic, not a forming/DCIV operation.
- Use read compliance `1e-6 A` unless the user requested otherwise.
- Probe these points in one protocol after routing to Keithley:
  - `0 V`
  - `+10 mV`
  - `-10 mV`
  - `+50 mV`
  - `-50 mV`
- Use `settle_s ~= 0.2`, `read_count=3`, and `reset=true` only on the first/zero-bias read.
- Cleanup in the same run or an immediate cleanup protocol:
  - `keithley-2450.set_output(false)`
  - `keithley-707b.open_all()`
  - `keithley-707b.get_closed_channels()`
  - verify Keithley/707B idle.

## Illumination context and repeat checks

- If `check resistance` immediately follows an explicit `turn on lights`, preserve that illumination state unless the user asks for dark resistance. Do not silently turn the lights off; label the result **lights-on / illuminated resistance** and issue no light command during the electrical protocol.
- A PUDA `light` state of `idle` only confirms command execution state, not lamp brightness. When the prior `turn_on()` returned `data.result: true` and no later light command occurred, report that the lights were *left in the previously commanded on state* rather than claiming fresh visual verification.
- For a terse `again`, repeat the exact same bias sequence, compliance, settling, read count, illumination condition, routing, and cleanup so the two estimates are comparable. Save the repeat in a distinct run folder.
- At pA currents, zero-bias offset may dominate naive `V/I`. Prefer paired differential resistance: `R_diff = (V_pos - V_neg) / (I_pos_mean - I_neg_mean)` for both ±10 mV and ±50 mV. Report both estimates and classify open-like/highly resistive only when the paired response is consistent; do not over-interpret one signed current.
- Preserve the requested light state after cleanup. Electrical cleanup still requires Keithley output off, 707B `open_all()`, `get_closed_channels() == nil`, and idle/null verification.

## START-timeout / dormant-edge recovery

If the canonical executable fails before collecting rows with a PUDA START timeout for `keithley-2450` or `keithley-707b`, especially when `machine state` returns stale timestamps from an earlier session, do not treat the stale idle/null KV state as fresh readiness and do not report a resistance result. Use `references/quick-resistance-edge-restart-after-start-timeout-2026-08-03.md`: restart the needed electrical edges, reset stale run IDs, use a proper start/run/complete lifecycle to turn the light off when needed, then retry `/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/quick_resistance_check.py` with the explicit bears NATS override. Report only the successful retry measurement as the check result.

## Reporting pattern

Report the measured current and resistance conservatively:

- If `±10 mV` reaches the `1 µA` compliance limit, report `R <= ~10 kΩ at 10 mV`, not a precise ohmic resistance.
- If `±50 mV` also reaches the same compliance limit, do not infer `50 kΩ` as an actual resistance; call it compliance-limited and use the lower-bias bound.
- If zero-bias offset is comparable to the signal, prefer paired differential resistance from `(+V, -V)` over naive `R = V/I`.
- Classify `~1 µA` at `10 mV` with `1 µA` compliance as definitely conductive and short-like / very low resistance under the low-bias check.

## Example outcome wording

```text
Resistance checked.
- +10 mV: ~1.00 µA, compliance-limited -> R <= ~10 kΩ
- -10 mV: ~-1.00 µA, compliance-limited -> R <= ~10 kΩ
Interpretation: definitely conductive, but short-like / very low resistance. This is a bound, not a clean ohmic value.
Cleanup verified: Keithley output off, 707B open-all nil, machines idle.
```
