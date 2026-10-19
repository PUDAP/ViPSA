# High-HRS contact-edge reset-compliance escalation (2026-06-10)

## When to use

Use this reference for live ViPSA cases where a device is electrically alive but very high resistance / open-like after approach, and the user asks to search for a proper DCIV reset by moving to the contact edge and escalating reset compliance.

## Concrete workflow that worked safely

1. Start with non-stressing paired low-bias Keithley reads (`0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`) to rule out a hard short and distinguish very-high-HRS from pure open contact.
2. If low-bias current is stable but tiny and the user wants more contact, advance Z only in the minimum current ViPSA increment (`+0.25` in the current +Z-forward convention), then rerun the same low-bias check.
3. For DCIV reset-compliance search:
   - keep SET compliance conservative first (example: `100 nA`),
   - include low-voltage post-SET and post-RESET read probes (example: `+100 mV`) as the deciding state evidence,
   - step RESET compliance upward (`1 µA`, `3 µA`, `10 µA`, `30 µA`, `100 µA`) rather than jumping immediately,
   - if SET remains weak, repeat with a modestly stronger SET compliance (example: `300 nA`) while still bounding RESET compliance.
4. Stop at the declared safety ceiling rather than continuing automatically (example ceiling: `100 µA` reset compliance).
5. Always cleanup and verify: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, and stage/Zaber/SMU/switch idle.

## Interpretation lessons

- A reset-like drop is **not** a valid sharp RESET unless the device was clearly in LRS immediately before it. In the reference session, the largest drop was ~2 decades near `-2.10 -> -2.15 V`, but the pre-reset state was not clearly LRS, so it was reported as an invalid/ambiguous reset-like feature rather than a clean RESET.
- ON/OFF contrast from read probes is useful but not sufficient to call a proper reset if the reset branch is mostly compliance-clamped. In the reference session, `SET=300 nA`, `RESET=1 µA` gave post-SET `+100 mV ≈ 2.23e-7 A` and post-RESET `+100 mV ≈ 1.45e-8 A` (~15x), but the branch did not show a clean visible rupture transition.
- If higher reset compliance mostly produces compliance-limited current instead of a well-defined current collapse, report that plainly: the device can be pushed more conductive and partly recovered, but no clean/sharp reset was found under this sweep family.
- End-state matters: report final low-voltage state. In the reference session final post-reset `+100 mV` returned near `3.9e-10 A`, i.e. high-resistance again, despite no clean reset transition.

## Reporting pattern

Keep the user-facing summary concise and evidence-first:

- contact/Z position change;
- compliance escalation sequence and ceiling;
- best reset-like candidate and why it did or did not qualify;
- best read-probe ON/OFF contrast if any;
- final state;
- artifact paths/plot media;
- cleanup verification.

Avoid claiming success from a visually steep negative-branch drop unless both pre-reset LRS and post-reset HRS are supported by low-voltage read probes or branch history.