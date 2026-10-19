# Repeated step-1 approach: abrupt compliance cliff after a prior no-contact block

Use this pattern when a bounded `+Z`, step-size-1 Keithley approach ended `no_contact_after_max` and the user immediately asks to approach again.

## Verified continuation pattern

- Continue from the **current verified Stage-Z**; do not reset, retract, or replay the earlier block.
- Preserve the established electrical recipe unless overridden: `10 mV`, `1 µA` read compliance, `10–100 nA` target, `+Z`, `1`-step coarse motion, `0.25`-step minimum trim, and bounded attempts.
- Capture the pre-block Stage-Z/current so the report can distinguish prior cumulative travel, gross forward travel in this block, safety retraction, and final net travel.

## Sharp contact-cliff outcome

A repeated block starting at Stage-Z `300` stayed near the pA noise floor through Z `358` (`68.7 pA` at `10 mV`), then one additional `+1` step to Z `359` jumped directly to the `1 µA` compliance limit. The standard bounded safety trim performed twenty `-0.25` moves (`-5` total), ending at Z `354`, but every trim read remained near compliance.

Classify this as:

```text
still_over_current_after_trim
```

—not `in_window`, successful contact, or stable resistance.

## Safety/reporting rules

1. Stop the approach when the bounded trim limit is exhausted; do not automatically resume `+Z`, run DCIV, or pulse the device.
2. Do not oscillate indefinitely across a sharp edge or extend the retraction beyond the configured safety bound without a new user decision.
3. Cleanup immediately: Keithley output off, 707B `open_all`, verify closed channels `nil`, lights off, and relevant machines `idle` with `run_id: null`.
4. Report both gross and net motion. In the example: gross forward `+59`, trim `-5`, net `+54`, final Stage-Z `354`.
5. Report the electrical bracket that triggered the stop: last below-threshold current/position and first compliance-limited current/position.
6. A later terse `approach` must not silently continue forward from this unresolved over-current state. Re-read at low bias and require an explicit safe next action (typically further bounded retraction or a contact diagnostic).
