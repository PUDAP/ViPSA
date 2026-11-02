# Grid open/weak-contact +1 Z retry override (2026-06-18)

## Context

During a long ViPSA 3×3 grid measurement run, the initial runner skipped requested electrical phases when an approach ended open/weak-contact. The user corrected this policy:

> Do not skip the devices in case they are showing open/weak contact. Just move the z stage up by 1 step and retry the measurements.

## Durable workflow lesson

For user-requested ViPSA grid measurements, treat open/weak-contact as a retryable grid condition, not an automatic skip:

1. Finish the normal bounded approach and record the final current/status.
2. If the result is open/weak-contact or below the contact window, move microscope `stage` Z forward/up by `+1` step.
3. Re-run the requested measurement sequence for that device rather than marking it skipped solely because of weak/open contact.
4. If a later device-health check is still open-like but not short-like, apply the same `+1` Z retry once and retry the health/measurement path.
5. Keep hard safety gates: do **not** ignore over-current, short-like, read-compliance-limited, measured-voltage-collapse, or instrument-fault conditions.
6. Record the override in the per-device summary, including before-current/status and stage position after the +1 move.

## Implementation notes

- This is a grid-run policy. It should not override single-device approach→DCIV chains where the user has not requested this behavior.
- The existing ViPSA convention is `+Z` = forward/up/protraction toward contact.
- Do not spam every approach loop step to the user; report device-level status and plots.
- If a running grid process has the old skip policy, stop it cleanly, cleanup outputs/routes, recover machine states, then resume from unfinished devices with the new policy recorded in the run summary.
