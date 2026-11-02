# Activation yield versus electrical-recipe performance

Use this note for prospective device-grid optimization where forming/contact and conditioning are irreversible prerequisites for assigned DC-IV or pulse recipes.

## Core separation

Pre-assign each device's role and recipe before testing. A device evaluates its assigned electrical recipe only after it crosses the declared activation feasibility gate.

If clean forming or conditioning fails:

- preserve the recipe assignment;
- record `recipe_withheld_activation_failure`;
- include the device in activation-yield and spatial analyses;
- exclude it from recipe-effect estimates;
- do not silently replace it or relax activation gates just to obtain recipe data.

Several consecutive activation failures do not prove that the assigned recipes failed. Continue independent prospective assignments unless a campaign-level yield stop was declared in advance.

## Forming/contact feasibility

- Use the lowest forming tier while coupling remains below the predefined meaningful-current threshold.
- Advance only the bounded mechanical variable during weak coupling.
- Unlock higher electrical tiers only after meaningful coupling without clean forming.
- Sustained compliance without large pre-compliance collapses is required; compliance attainment alone is insufficient.
- Repeated multi-order current collapses indicate unstable contact/filament formation and block conditioning.

## Conditioning feasibility

Require a prospective consecutive-pair rule combining direction, minimum state-separation ratio, and maximum variability. Apply thresholds literally; do not round a near miss into success. Passing conditioning demonstrates short-window state separation, not endurance or retention.

## Autonomous campaign behavior

When the user authorizes continuous testing:

1. Preserve raw/partial data and cleanup evidence.
2. Update the campaign wiki after every device, including withheld recipes.
3. Adapt only at safe boundaries and within approved limits.
4. Continue without routine pauses.
5. Report in chat only successful or scientifically interesting results, with focused plots and cautious explanations.

Focused plots should separate forming progression, accepted/failed forming traces, state reads, and ratio/stability metrics instead of overlaying every sweep into an unreadable figure.
