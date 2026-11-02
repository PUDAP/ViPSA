# TE probing: negative current as open-circuit signature (2026-06-29)

## Trigger

Use this note when interpreting ViPSA electrical data collected while probing from the **top electrode (TE)**, especially Keysight/Keithley read currents after SET/read pulse trains or low-bias contact checks.

## Session correction

The user corrected the interpretation after a Keysight retention retest with compliance increased to `1e-4 A`:

> when probing from TE negative currents usually mean open circuit

The measured trace had a `+0.8 V` SET pulse followed by `100 × +0.1 V` reads at `50 ms` with `1e-4 A` compliance. Currents were stable around `-6 to -7 nA`. A naive `R = |V/I|` interpretation suggested `~14–16 MΩ`, but the user clarified that for TE probing this polarity/sign is normally an open-circuit indicator, not retained LRS.

## Rule

When probing from TE:

- Treat negative currents during positive low-bias reads as **open/poor-contact likely** unless corroborated.
- Do **not** report negative nA/pA reads as stable conduction or retained LRS simply because their magnitude is above pA.
- Do **not** convert to a positive resistance and present it as an ohmic conductive state without a warning.
- Prefer wording such as: `negative TE-probe current; likely open/poor contact, not valid retained conductive state`.

## What corroboration would be needed

Before calling the device conductive/LRS, seek at least one of:

1. Paired-bias reads (`0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`) with sign and magnitude scaling consistently with applied voltage.
2. Contact diagnostics showing the probe is mechanically/electrically coupled.
3. A post-read trace with the expected polarity for the probing configuration.
4. Independent Keithley low-bias confirmation after Keysight pulse routing.

## Reporting pattern

If a future trace resembles the session case, report concisely:

```text
Completed, but TE-probe read currents are negative (~X nA), which we treat as open/poor-contact likely. I am not counting this as retained LRS/conduction. Cleanup verified: output off, 707B open/nil.
```

If the earlier wording overclaimed conduction, explicitly correct it:

```text
Reinterpreting with the TE-sign rule: the stable negative reads indicate likely open circuit, not a stable ~R conductive state.
```
