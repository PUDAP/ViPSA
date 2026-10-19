# Pulse switching that was actually poor/open contact — 2026-06-05

## Trigger

Use this reference when ViPSA pulse/endurance data on an RRAM/memristor device shows nA/sub-nA read currents, oscillatory or alternating apparent states, weakly separated SET/RESET reads, or the user suspects open contact.

## What happened

A device was tested with Keysight `SET-read-RESET-read` pulse trains. Short screening found apparent SET/RESET read-state separation, and a degradation-allowed endurance run completed 1000 cycles with median read ratio around 5×. The user pointed out that the behavior looked like open-contact oscillation rather than real RRAM switching.

A follow-up Keithley 2450 contact check through the 707B route measured repeated low-voltage currents:

- `0.01 V`: median `4.21e-11 A` (`42 pA`), inferred `~237 MΩ`
- `0.1 V`: median `1.03e-10 A` (`103 pA`), inferred `~967 MΩ`

The contact/current level was pA-scale and non-ohmic/inconsistent with a solid device contact. This supported the user's interpretation that the pulse results should not be treated as robust RRAM switching.

## Durable lesson

Do not interpret apparent pulse read-state separation as switching when the absolute currents are near the pA/nA noise/contact regime. If pulse data looks oscillatory, weak, or suspicious, pause and run a Keithley low-voltage contact check before optimizing pulses or reporting endurance as device behavior.

## Recommended Keithley contact check pattern

1. Verify `keithley-2450`, `keithley-707b`, and the pulse SMU are idle.
2. Force outputs off before routing if practical.
3. Route the DUT to Keithley via 707B.
4. Measure 3–5 repeats at low voltages such as `0.01 V` and `0.1 V` under conservative compliance.
5. Report median/min/max absolute current and inferred resistance for each voltage.
6. Treat pA-scale currents, very high inferred resistance, and non-ohmic resistance changes with bias as open/poor-contact evidence.
7. Cleanup: Keithley output off, 707B `open_all`, confirm no closed channels, and report final machine states.

## Reporting language

Use cautious but direct language:

- "This looks open / poor-contact-like; previous pulse switching should be interpreted cautiously."
- "The data supports your concern that the apparent oscillations may be contact artifacts."
- "Re-contact/re-approach and rerun a short Keithley DC/contact check before further Keysight pulse tests."
