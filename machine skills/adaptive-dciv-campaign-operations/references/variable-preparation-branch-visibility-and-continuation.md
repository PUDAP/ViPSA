# Variable preparation, branch visibility, and continue-through-failure

Use this note when cloning an adaptive DCIV controller to a new device, interpreting a plot with an apparently missing polarity, or handling an instruction to keep an autonomous screen moving.

## Derive preparation invariants; never inherit them

Forming-as-approach is variable. A device may require one forming sweep or several, and every tenth completed preparation stress sweep can add a health operation. Therefore a copied controller must derive from the new preparation terminal and ledger:

- `forming_sweeps`, `conditioning_sweeps`, and `completed_sweeps`;
- completed preparation health reads;
- receipt/operation count;
- final pose after all +Z forming attempts;
- candidate-batch ledger baseline.

Do not hard-code a prior device's common values such as 14 stress sweeps, 15 operations, one preparation health read, or its pre-approach pose. Before candidate dispatch assert the new terminal, permanent ledger, and live pose agree. A prerequisite assertion failure before dispatch is zero candidate exposure; correct the derived invariant and restart with fresh IDs only if any intent was created.

## Diagnose an apparently missing SET/RESET side from data

Before blaming the sample or plotting code, inspect the exported native CSV/receipts and report per polarity:

- row count per cycle;
- unique commanded voltages;
- endpoint magnitude and voltage step;
- plot x/y limits and log-floor handling;
- branch labels and line styles.

If `endpoint < step`, a nominal `0 -> endpoint -> 0` branch has only three points and may collapse into a near-vertical sliver at zero when the opposite polarity spans volts. The data is present but physically under-resolved. State its exact location and point count. Only classify a plotting/label bug when the source contains a normal branch that the rendered plot omits or misassigns. A zoom/inset improves visibility but cannot create an uncommanded full sweep.

## “Do not stop” in an autonomous device screen

Interpret continue-through-failure at campaign scope, not as permission to bypass hard safety or frozen scientific stop rules:

- recover transient infrastructure/storage/schema faults and continue from retained evidence without replay;
- when the configured minimum-cycle consecutive failure rule is met, stop that recipe on that device, record it as recipe-specific (not irreversible death), clean up, advance the optimizer, and begin the next device;
- never continue stressing the same DUT past its authorized stop solely to satisfy “do not stop”;
- unresolved UNKNOWN exposure, unverified OFF/open cleanup, ownership conflicts, or unsafe live readback remain fail-closed gates.

## Storage guard

Before long native batches, require enough root-filesystem space for the wire journal, native response, receipts, atomic ledger rewrite, and margin. If ENOSPC occurs after candidate acquisition, preserve completed cycles, prove whether the health intent had zero exposure, remove only disposable caches, reverify safety, and run only the missing health operation under a new identity.
