# Contact approach to endurance handoff note

Session learning from a ViPSA contact-change workflow:

- User requested a relative Z move, then contact approach, then the original optimized Keysight endurance test.
- A `stage.move_z_by(height=-10)` moved the stage from about Z `-62.9` to `-72.9`.
- The subsequent contact approach used `+Z` as forward and detected contact after 19 coarse `+1` moves, ending around Z `-54.9`.
- Keithley contact looked measurable (`~2.3 nA` at `0.01 V`, about `4.4 MΩ`) and was inside the chosen approach thresholds.
- However, the immediately following Keysight endurance test at `±1.5 V`, `0.1 V` read, `10 ms`, `10 µA` compliance hit compliance on the low-voltage reads and was stopped after the first 100-cycle batch.

Reusable handoff rule:

- A successful Keithley contact approach only means the contact is inside the approach window; it does not guarantee that a previous pulse-endurance recipe is still safe.
- After significant Z motion or approach, use a batched endurance runner with explicit safety stops and be prepared to stop after the first batch if low-voltage reads are compliance-limited.
- In reports, distinguish: "approach succeeded" from "endurance condition is safe". If endurance read pulses are at compliance, report likely over-contact/short and cleanup.
