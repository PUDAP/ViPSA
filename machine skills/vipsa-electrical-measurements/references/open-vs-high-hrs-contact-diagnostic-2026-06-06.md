# Open contact vs true high-HRS diagnostic (2026-06-06)

Context: after a visually aligned approach with `step_size=0.5`, the approach loop reached the max attempts with only ~`4.7e-11 A` at `0.01 V` (apparent ~`213 MΩ`) and no contact detection. The user pointed out this could be either open/poor contact or a legitimately very high-resistance HRS.

## Durable lesson

Do not immediately run DCIV/forming when the current is pA/sub-nA after an approach. First run a non-stressing contact diagnostic that separates:

- open/poor mechanical contact
- real high-resistance HRS
- short/over-contact

## Recommended diagnostic

1. Turn lights off if the user asks, and verify `light` is idle.
2. Route DUT to Keithley safely:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.connect_keithley_smu()`
3. Measure low-voltage reads at several small biases, for example:
   - `0 V`
   - `+10 mV`, `-10 mV`
   - `+50 mV`, `-50 mV`
   - optionally `+100 mV`, `-100 mV`
   Use low compliance (`100 nA` to `1 µA`).
4. If the small-bias reads stay pA/sub-nA, add a **higher-voltage diagnostic probe** before declaring failed health. This is specifically to separate two cases the user called out:
   - true mechanical open contact from vibration / lost probe contact
   - genuinely very-high-HRS/off-state device, which is an ideal/working off state

   Suggested guarded probe sequence:
   - `+200 mV`, `-200 mV` at the same low read compliance (`100 nA` to `1 µA`)
   - If still ambiguous and the upcoming/previous device recipe already used larger voltages safely, optionally escalate to `+500 mV`, `-500 mV` with the same low compliance, but do not exceed the intended non-forming health-check ceiling without explicit user approval.
5. Interpret and branch:
   - **Case 1 — true open/lost contact likely:** current stays near pA noise floor and does not scale even at the higher-voltage probe. Move `stage` Z **up / forward by +0.25 steps** (the minimum valid ViPSA Z increment), then rerun the same probe sequence. If it remains pA/no-scaling after this retry, treat as failed health/open-like and do not run cycling/stress automatically.
   - **Case 2 — true high-HRS/off-state likely:** small-bias current is pA/sub-nA, but the higher-voltage probe rises clearly above noise and scales with voltage without compliance. Treat the device as electrically alive/working and continue to the next requested operation.
   - current scales roughly with low voltage and has stable sign: likely real high-HRS contact; continue to the next requested operation if otherwise safe.
   - current hits compliance at low or higher diagnostic voltage, or measured voltage collapses: short/over-contact; stop stress and cleanup.
6. If the multi-bias plus higher-voltage result is still ambiguous after the single +0.25 Z retry, run or ask about a broader Z-sensitivity/contact approach workflow rather than blind stress:
   - measure at `+10 mV`
   - move Z forward in tiny increments (`+0.25` or `+0.5`, using the confirmed ViPSA +Z forward convention)
   - remeasure after each step with the same low-voltage/read compliance
   - a sudden current jump with Z indicates contact was not properly made; stable pA/sub-nA current across Z steps suggests still open or extremely high HRS
6. Always cleanup:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should return `nil`
   - verify final machine states.

## Reporting pattern

Keep it concise for the user:

- lights off status if requested
- measured currents at each small bias
- whether current scales with voltage
- any Z increments and current changes
- classification: likely open/poor contact, likely high-HRS, or short/over-contact
- cleanup verification

Do not overclaim high-HRS from a single pA-scale read at one voltage; use multi-bias scaling and/or Z-sensitivity evidence.