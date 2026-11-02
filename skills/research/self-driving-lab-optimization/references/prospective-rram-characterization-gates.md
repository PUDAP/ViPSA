# Prospective RRAM characterization gates

Use this reference when optimizing DC-IV or pulse recipes across a device grid with irreversible activation prerequisites.

## Separate feasibility layers

Track these outcomes independently:

1. optical/mechanical alignment validity;
2. clean forming/contact yield;
3. conditioning convergence yield;
4. assigned-recipe characterization;
5. endurance survival;
6. retention and multilevel quality.

If forming or conditioning fails, record the pre-assigned recipe as **withheld/unevaluated**, not failed. Keep the device in activation-yield and spatial analyses, but exclude it from recipe-effect estimates.

## Clean forming and conditioning

- Compliance attainment alone is insufficient: reject forming traces with large pre-compliance current collapses.
- Use the lowest forming tier during weak coupling and unlock higher tiers only after a declared meaningful-current gate.
- Require a prospective consecutive conditioning window with correct state direction, minimum ON/OFF, and maximum spread. Apply the spread threshold literally; do not round a near miss into success.

## Characterization before endurance

After activation passes:

- Run the full declared short characterization block first (five cycles in the validated campaign).
- A characterization cycle is valid only when reads are complete, directionally correct, non-compliance-limited, and ON/OFF meets the prospective floor (`>=2` in the validated campaign).
- Start endurance only if **every** characterization cycle is valid.
- One or two attractive early cycles are not sufficient. If later characterization loses separation, classify the recipe as initially switching but unstable and withhold endurance and retention.
- Run retention only after endurance remains valid, preserving the exact SET/read compliance and no-RESET-between-reads policy.

## Runner and analysis rules

- Preserve the recipe assignment even when it is withheld.
- Never silently substitute another device or relax gates to obtain recipe data.
- Preserve raw operations and resume from the first unexecuted operation after a parser/control-flow failure.
- For constant-bias Keithley reads, valid `I_meas` may coexist with `V_meas=None`; use commanded read voltage with explicit provenance only for hold/read rows.
- Focused plots should separate activation progression, accepted/rejected forming, conditioning reads, and characterization ON/OFF instead of overlaying all sweeps.

## Autonomous reporting

For long campaigns, update the campaign wiki after every device. Report in chat only successful or scientifically interesting results, with a focused plot and cautious explanation; retain routine negative outcomes in the wiki and failure logbook.
