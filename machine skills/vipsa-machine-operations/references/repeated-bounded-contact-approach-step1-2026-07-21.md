# Repeated bounded contact approach with step size 1 (2026-07-21)

## Trigger

Use this pattern when the user says “try approach again, with 1 step” after a prior bounded approach ended with no contact.

## Durable workflow

- Treat the request as a continuation from the **current stage Z position**, not as a restart from zero.
- Preserve the established approach defaults unless overridden: `+Z`, coarse step `1`, `10 mV` Keithley read, `1 µA` compliance, `10–100 nA` contact window, and `0.25` minimum trim.
- Preflight `light`, `keithley-2450`, `keithley-707b`, and `stage`; all must be idle with `run_id: null` before starting.
- Run a bounded outer-loop approach through one-command PUDA protocols. A practical bound is another 100 coarse moves unless the active procedure specifies a different limit.
- Keep lights off during electrical reads.
- On no contact, stop at the bound rather than continuing indefinitely.
- Report both:
  - incremental travel for this run; and
  - final/cumulative stage position read back from the stage.
- Always clean up: Keithley output off, 707B `open_all`, verify closed channels `nil`, and verify all machines idle / `run_id: null`.

## Session example

A first bounded run moved from Z `0` to `100` with current remaining near `12–19 pA`. The user requested another run with the same step size. The continuation moved another `+100 Z` to `[0, 0, 200]`; current stayed near `12–15 pA`, so status remained `no_contact_after_max`. This is open/high-HRS-like and should not be called contact.

## Reporting pitfall

Do not report only “100 moves” without clarifying whether that is incremental or cumulative. For continuation runs, explicitly state both `+100 this run` and the final stage position (for example `[0, 0, 200]`).
