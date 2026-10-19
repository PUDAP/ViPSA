# User-authorized health-gate override: negative-first DCIV

Session signal: after a guarded health gate indicated weak/open-like behavior, the user explicitly authorized overriding the safety health gate and requested a DCIV with the negative side first and limits `+1 V` and `-1.5 V`.

Use this reference when the user explicitly overrides a prior electrical health gate and asks to continue with a stress sweep anyway.

## Workflow pattern

1. Treat the override as an explicit user authorization for the requested stress operation, but do not drop hard safety/cleanup guards.
2. Preserve the requested branch order exactly. For this case the intended path was:
   `0 -> -1.5 -> 0 -> +1.0 -> 0 V`.
3. Use the user-specified voltage maxima verbatim and report them in the final summary.
4. Record branch/path metadata in raw artifacts so later analysis does not assume the usual positive-first order.
5. Run the requested cycle count if known; otherwise ask only if the cycle count is genuinely missing and not recoverable from context.
6. If health-gate logic is bypassed, say so in the run metadata/final wording rather than implying the device passed normal health screening.
7. Keep normal cleanup mandatory: SMU output off, 707B `open_all`, verify closed channels are nil/no channels, and verify relevant machines idle / `run_id: null`.

## Reporting pattern

Concise final output should include:

- branch path/order, voltage limits, cycle count, point count;
- compliance values used per side/branch;
- max current and compliance-hit counts;
- post-read values and whether they are compliance-limited;
- interpretation using cautious wording such as `short-like / very low resistance under the read limit` when low-voltage post-reads hit read compliance;
- cleanup verification and raw artifact paths.

## Interpretation note

If the post-read at only `10 mV` hits `1 µA` read compliance, do not report a precise resistance. Report a bound/qualitative state, e.g. `<= ~10 kOhm at 10 mV with 1 uA read compliance`, `short-like`, or `very low resistance under the read limit`.
