# Durable intent / ledger / wire reconciliation

Use this pattern when a controller is killed, times out, or exits between operation boundaries. The process exit code and in-memory/progress JSON are not authoritative by themselves.

## Evidence precedence

Reconcile the same operation identity across four layers:

1. **Local intent artifact** — proves only that orchestration planned an operation.
2. **Permanent exposure ledger** — proves what the adapter durably committed and charged.
3. **Raw wire journal** — proves which machine command was actually requested and what native reply returned.
4. **Fresh hardware cleanup/readback** — proves the current safe state, not historical exposure.

Compare exact operation ID, phase, frozen parameters/list, native run ID, expected point count, response status, and cleanup evidence. Do not infer execution merely because a progress file contains an operation ID.

## Three common kill windows

### A. Native operation and ledger complete; progress copy missing

Evidence:

- permanent ledger entry is `COMPLETE`;
- exact native row count and energy are present;
- operation cleanup is verified;
- progress JSON lacks the receipt or still shows the prior cycle.

Action: reuse the ledger receipt, regenerate missing cycle metrics if needed, and resume at the next undispatched branch. Never repeat the completed stress.

### B. Native success reply exists; ledger commit missing

Evidence:

- exact intent exists;
- wire journal contains a successful native response for the frozen command/list;
- ledger lacks the operation or remains pre-completion;
- complete native rows can be parsed and matched exactly;
- fresh output-off/matrix-open/error-free readback succeeds.

Action: compute sampled energy once from the recovered native rows, add one evidence-backed reconciled `COMPLETE` ledger receipt, preserve the native envelope/run ID and reconciliation basis, and resume after that operation. Do not replay it.

If the reply is partial, malformed, or cannot be bound uniquely to the intent, classify possible partial stress as UNKNOWN instead of fabricating completion.

### C. Intent exists, but hardware dispatch never occurred

Evidence:

- local intent exists;
- operation ID is absent from the permanent ledger;
- the complete wire journal has no matching machine sweep request/reply after that intent;
- the prior operation's cleanup is verified;
- fresh output-off/matrix-open/error-free readback succeeds.

Action: record a separate `undispatched=true`, `zero_exposure=true` reconciliation artifact. Do not insert a fake exposure ledger entry. Resume the missing branch with a **new** operation ID. This is not replay because no hardware exposure occurred.

Count prior same-polarity native run IDs/commands when useful to prove the missing ordinal (for example, 17 negative sweeps exist and no 18th negative request exists).

## Native pre-output rejection

A driver can reject a command during output-OFF native proof/configuration. To classify zero exposure, preserve the exact error response and prove it occurred before `OUTP ON`, with output-before readback `0`, no trace rows/energy, operation cleanup, and independent final cleanup. Mark the failed intent as zero exposure without charging energy; retry only after the defect is fixed and a fresh OFF-only proof passes.

## Continuation state

A continuation controller must explicitly restore:

- stress-sweep counter, including preparation sweeps;
- completed-cycle count;
- due health-read cadence;
- failure-monitor history reconstructed from saved per-cycle metrics;
- reused completed receipt IDs;
- the zero-exposure/undispatched reconciliation path;
- the same frozen recipe and hard cycle cap.

If a cycle's SET completed but RESET did not dispatch, resume RESET only, calculate that cycle's metric from the reused SET plus new RESET, then continue with the next full cycle.

## Verification before launch

- all historical ledger operations are `COMPLETE`;
- device-level `unknown` is false;
- exact recipe/hash and native OFF proofs still match;
- output is `0`, matrix is `nil`/empty, instrument errors are empty;
- live pose/routing still match the intended device;
- continuation script compiles and asserts the expected boundary/counts.

## Reporting language

State separately:

- what physically completed;
- what was only intended;
- what was reconciled from wire evidence;
- what was proven undispatched/zero exposure;
- what will resume next;
- that completed stress will not be replayed.
