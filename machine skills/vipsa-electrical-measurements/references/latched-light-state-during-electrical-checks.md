# Latched light-state override during electrical checks

## Trigger

The user explicitly says to keep the ViPSA lights on until they explicitly say to turn them off.

## Rule

Treat this as a latched operational override, not a one-command preference. Until the user explicitly requests lights off:

1. Do not send `light.turn_off()` before or after terse resistance checks or other low-bias electrical diagnostics.
2. Preserve the light state while still performing normal electrical cleanup: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, and final machine-state checks.
3. Mark the run metadata/report as measured with lights kept on; optical illumination can affect pA-scale/high-HRS measurements, so comparisons with dark measurements should identify lighting condition.
4. Report that lights remain on after cleanup. Do not say a `light` machine state of `idle` proves lamp output; `idle` only confirms command execution state. Ground the retained lamp state in the last verified `turn_on` response plus the absence of any subsequent off command, or use camera evidence if actual optical state must be reverified.
5. The latch ends only when the user explicitly asks to turn the lights off. After that, return to the ordinary lights-off electrical default unless a new override is given.

## Implementation pattern

Electrical runners should expose an explicit switch such as `KEEP_LIGHT_ON=1` or a boolean argument. When set, skip only the light-off command; do not weaken SMU/switch cleanup or compliance limits.

## Reporting

Use concise wording such as:

> Resistance: ~1.5 GΩ under illumination. Keithley output off, 707B channels nil, all machines idle. Lights were kept on and remain on per your instruction.
