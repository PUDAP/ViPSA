# Approach retry after a grid runner advanced devices

## Trigger

Use when a grid run stopped or advanced after device N, but the conversation is still discussing an earlier device and the user tersely says “move Z … and retry approach.”

## Critical target-identity gate

1. Read the live Zaber X/Y and compare it with the canonical grid positions plus recorded alignment corrections.
2. Inspect the most recent per-device summaries/logs to identify the physically aligned device.
3. Resolve the conversational referent from the reply chain. A reply about device 6 normally refers to device 6 even if the interrupted runner had already aligned device 7.
4. If the conversational target and live physical device differ, **do not move Z or approach**. State the mismatch and ask whether to return safely to the discussed device or operate on the live device. This ambiguity changes which hardware action is safe and is not suitable for a default assumption.
5. If returning to another device is authorized: electrical cleanup → safe Z travel retract → absolute Zaber X/Y move using the grid/alignment artifact → verified readback → requested pre-move/approach.

## Repeated approach correction

When the user says no `-50` retract between subsequent attempts, carry the next bounded approach forward from the verified current Z. Do not insert a generic or attempt-sized gross retract between failed blocks. Preserve only contact-safety behavior: minimum-step negative trim after over-current/overshoot, hard bounds, and a safe travel retract before any X/Y movement.

## Reporting

State the physical device actually operated on, pre-move Z, requested pre-move, approach-only travel, final Z/current/window result, and cleanup. Never let a large manual pre-advance count as approach travel or contact evidence.
