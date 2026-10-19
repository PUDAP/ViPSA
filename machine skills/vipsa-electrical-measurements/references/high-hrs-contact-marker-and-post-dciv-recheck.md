# Distinguishing pristine very-high HRS from a truly open contact

Use this when a user states that pristine devices in the current material system naturally have very high HRS and pA/GΩ readings.

## Core rule

Do not classify contact from resistance magnitude or current magnitude alone. A confirmed pristine HRS can overlap an open route in the pA/GΩ range. Preserve manual contact confirmation as independent evidence and evaluate the paired-bias response.

## Device-like contact marker

From a low-compliance sequence such as `0 V, ±10 mV, ±50 mV`:

- subtract/inspect the zero-bias offset;
- require a reproducible differential slope `ΔI/ΔV`;
- at a sufficiently large safe pair, current should normally follow applied polarity after accounting for offset;
- when the voltage pair grows by 5×, differential current should scale approximately with it for an ohmic HRS;
- differential resistance from the two bias pairs should agree reasonably.

A concrete confirmed-HRS example gave:

- zero-bias current about `−11 pA`;
- `+50 mV: +19.9 pA`, `−50 mV: −39.8 pA`;
- `ΔI(±50 mV) / ΔI(±10 mV) = 4.89` for a 5× voltage increase;
- `Rdiff = 1.638 GΩ` at ±10 mV and `1.675 GΩ` at ±50 mV (2.2% mismatch);
- final classification `pristine_HRS_contact_confirmed` because the user independently confirmed the probe contact.

## Open-like marker

A truly open or electrically uncoupled route is commonly offset/leakage dominated:

- the same current sign persists across positive and negative biases;
- zero-bias offset is comparable to or larger than the paired differential response;
- extracted resistance varies more strongly across voltage pairs;
- repeated stress produces no meaningful current increase or switching.

A representative open-like trace had about `−117 pA` at zero bias, retained negative current at every bias, offset/`ΔI(±50 mV)` ratio `2.24`, and 12.1% resistance-pair mismatch.

## Before and after DCIV

1. Save the precheck and its manual-contact context.
2. Run the requested DCIV only after contact is accepted under the rule above.
3. Repeat the paired-bias diagnostic afterward.
4. Do not carry the pre-run manual confirmation forward automatically. If the postcheck becomes same-sign and offset dominated, label it `post_dciv_offset_dominated_open_like` and say that retained electrical coupling is not confirmed. Do not overclaim that physical contact was lost unless motion or imaging proves it.
5. Link both checks from the DCIV summary and project history.

## Reporting language

Prefer: `The post-test electrical trace is offset-dominated/open-like and does not confirm retained electrical coupling; this alone does not prove physical probe contact was lost.`

Avoid: `The probe lost contact` when only electrical evidence is available.
