# Quick resistance check after lights-on: dark repeat pattern (2026-07-28)

Context: user first asked `turn on lights`, then `quick check resistance`, then `Approach`.

Reusable lesson:

- The canonical quick-resistance script at `/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/quick_resistance_check.py` does **not** itself control the light; its summary says `light_policy: unchanged; this script sends no light commands`.
- Therefore, when the previous conversational/light state is lights-on and the user has not explicitly latched illumination, explicitly turn the light off **before** running the electrical quick check.
- If a check was accidentally run while illuminated, immediately turn lights off, repeat the same canonical low-bias check, preserve both run directories, and report the dark repeat as the decision result while noting that the lamp state changed.
- Do not infer optical causality from one illuminated-vs-dark pair; just report reproducibility/change.

Observed dark repeat example:

- Biases: `0 V`, `±10 mV`, `±50 mV`; compliance `1e-6 A`; 3 reads per bias.
- Dark repeat means were pA-scale: `0 V ~31 pA`, `+10 mV ~39 pA`, `-10 mV ~25 pA`, `+50 mV ~67 pA`, `-50 mV ~-2.8 pA`.
- Paired differential estimates at `±10 mV` and `±50 mV` were both about `1.4 GΩ`.
- Classification: `open_or_very_high_resistance_like`, not shorted.
- Cleanup: Keithley idle/output off, 707B open/nil, light idle/off.

Reporting pattern:

```text
Quick resistance check complete with lights off.
Estimated differential resistance: ~X GΩ.
Classification: open / very-high-resistance-like, not shorted.
Cleanup verified: Keithley output off; 707B open/nil; Keithley + 707B idle/null; lights now off/idle.
```