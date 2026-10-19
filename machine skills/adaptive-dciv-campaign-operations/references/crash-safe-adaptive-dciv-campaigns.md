# Crash-safe adaptive DCIV campaign execution

## 1. Preparation handoff

Before requesting a candidate recipe, verify from both the terminal record and permanent ledger:

- exact forming and conditioning counts;
- health reads due from the completed-stress counter;
- every receipt and ledger operation is `COMPLETE`;
- every operation has verified cleanup;
- device `unknown == false` and no partial receipts exist;
- final live pose matches the preparation terminal record;
- cumulative sampled energy remains recorded (never reset accounting).

Compact only completed operation payloads after their native receipt files are durable. Preserve hashes/references and operation/state counts. Never compact unresolved exposure.

The optimizer request must name the exact preparation terminal path, counts, energy, final pose, minimum-cycle rule, hard cap, global waiver, and `no preparation replay`. Validate both semantic recipe hash and file hash before hardware use.

## 2. Native output-OFF qualification

Qualify the complete frozen SET and RESET arrays while SMU output is OFF. Require:

- exact upload tokens and ordered point counts;
- zero instrument errors during chunked upload;
- list readback matching the recalled source level at the instrument's query precision;
- stored seven-significant TSP level matching the requested value or its explicit binary32 encoding;
- exact compliance representation;
- output `0` before/after and matrix `nil` after cleanup.

Do not compare unrestricted host doubles directly to six-significant query text and do not introduce an arbitrary voltage tolerance. The 2450 can expose six-digit query text and seven-digit/binary32 stored values with different decimal-tie rendering. Corroborate those representations independently.

A proof rejection before output enable is zero candidate exposure. Preserve the failed proof and cleanup evidence, fix the verifier, redeploy/test, and rerun only the OFF-only proof.

## 3. Bounded-memory cycle controller

Use one fresh process per full candidate cycle. At each launch:

1. Verify recipe/readiness/active-request hashes and the no-replay preparation terminal.
2. Recompute the expected ledger prefix from preparation operations, completed full cycles, and health reads due from the carried preparation stress counter.
3. Require all prefix operations `COMPLETE`, device `unknown == false`, output OFF, matrix nil, correct terminals, empty errors, and unchanged pose.
4. Execute SET then RESET exactly once, inserting health reads when the completed-stress counter reaches each tenth sweep.
5. Persist intent before dispatch, native receipt after completion, cycle metrics, terminal status, and cleanup.
6. Compact newly completed payloads only after receipt discovery succeeds.

This bounds RAM even when a JSON ledger grows large and avoids long-lived full-ledger accumulation.

## 4. Post-acquisition failure reconciliation

A controller exception after hardware completion is not permission to replay stress. Resolve in this order:

1. Inspect the wire journal, permanent ledger, native row count/order, energy, and fresh cleanup.
2. If an operation is ledgered `COMPLETE`, has exact native rows, and cleanup is verified, reconstruct its receipt from the permanent ledger and validate it against the frozen operation.
3. Archive/compact that receipt, record explicit `no_replay` reconciliation, and resume at the first missing branch only.
4. If dispatch cannot be disproved and completion cannot be proved, keep exposure unresolved and stop.

Typical recoverable boundaries are: completed SET but missing RESET; completed electrical cycle but failed receipt archival; or process OOM after a ledgered operation. Never restart the whole cycle when one branch is already proven complete.

## 5. Stop semantics

- Do not apply recipe-specific failure before the declared minimum full-cycle count.
- Confirm recipe-specific failure only after the configured consecutive-cycle signal (commonly three), and describe it as failure under that unchanged recipe—not irreversible device death.
- Stop at the hard cap even without failure. A hard-cap survivor is `complete`, **right-censored**, and not a failure.
- Always verify final output OFF, matrix nil, empty unresolved operations, and no cleanup failures.

## 6. Live and final plots

Plot only full cycles for which both SET and RESET receipts are `COMPLETE` with verified cleanup.

For a live request during an active campaign:

- freeze an explicit completed-cycle boundary `N`;
- filter receipt discovery to `cycle <= N` so later completions cannot invalidate regeneration;
- assert the cycle set is exactly `1..N` and both polarities exist for every cycle;
- label the title **snapshot through cycle N**, never `final`;
- retain native-point and contrast CSVs.

For final plots, require a verified stop terminal. Use commanded voltage versus log `|Imeas|`, one color per cycle, PF/PB/NF/NB line styles, a cycle colorbar, and a log-scale contrast panel. Label a hard-cap result as a final survivor/right-censored plot.

## 7. Verification checklist

- Preparation counts and health counter reconcile.
- Recipe semantic/file hashes match the active request.
- OFF-only proofs pass for exact SET/RESET counts.
- Ledger prefix count is computed, not guessed.
- Every plotted cycle has two completed branches.
- No in-progress or intent-only operation is plotted.
- Cleanup and UNKNOWN state are read back after the final operation.
- Snapshot/final wording matches actual campaign state.
