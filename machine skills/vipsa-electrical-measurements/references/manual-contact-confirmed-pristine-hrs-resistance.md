# Manually confirmed contact: classify pA/GΩ reads as pristine HRS

## Trigger

Use this when a low-bias ViPSA resistance check produces pA-scale current and an automated classifier returns `open_or_very_high_resistance_like`, but the user has independently confirmed physical contact (for example by manually moving/observing the probe tip) and identifies the device as pristine HRS.

## Rule

Do not discard the raw signal-only classification, but do not present it as the final device classification either.

Record both layers:

```json
{
  "measurement_context": "pristine HRS resistance",
  "manual_contact_confirmed": true,
  "manual_contact_confirmation_note": "User confirmed contact manually by moving the probe tip.",
  "classification": "pristine_HRS_contact_confirmed",
  "automated_signal_only_classification": "open_or_very_high_resistance_like",
  "interpretation_note": "Because contact was manually confirmed, pA-scale current is interpreted as pristine HRS rather than lost/open contact."
}
```

## Resistance reporting

For the standard dark low-bias check at `0 V`, `±10 mV`, and `±50 mV`:

1. Report paired differential resistance separately at ±10 mV and ±50 mV.
2. Report the combined estimate only when both estimates are finite and reasonably consistent.
3. Preserve current samples, zero-bias offset, and the automated classifier in the saved artifact.
4. Do not claim contact was electrically proven by the resistance trace; state that contact was independently/manual-confirmed by the user.
5. Keep the final wording concise: `pristine HRS, contact manually confirmed`, resistance estimates, maximum current magnitude, compliance status, and cleanup.

## Project artifact routing

If the device belongs to a named project, the canonical quick-check script may initially write under a generic `runs/` directory. Before final reporting:

1. Move the complete run directory into the project’s canonical `runs/` root.
2. Update the saved summary’s `outdir` and `project` fields.
3. Add the manual-contact/pristine-HRS annotation above.
4. Append a timestamped linked run entry to that project’s `project.md` using the actual `started_utc` or run timestamp.
5. Verify the final artifact path is the path reported to the user.

## Example interpretation

Paired differential estimates of approximately `1.64 GΩ` at ±10 mV and `1.67 GΩ` at ±50 mV, with currents below `40 pA`, are a valid pristine-HRS baseline when contact is independently confirmed. Without that independent confirmation, the same electrical data remains ambiguous between very-high-HRS and open/weak contact.
