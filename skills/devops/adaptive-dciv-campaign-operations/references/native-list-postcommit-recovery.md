# Native-List Proof and Post-Commit Recovery

Use this procedure when a Keithley 2450 native-list operation is committed to the permanent ledger but the controller fails before receipt writing, metric generation, or compaction.

## Representation rule

The 2450 exposes two distinct representations:

- a stored seven-significant-digit TSP source level (sometimes reflecting binary32 storage or documented source-grid quantization), and
- a six-significant-digit queried/list readback.

Do not validate a modern proof by independently applying host `.6g` rounding to the unrestricted requested voltage. Decimal ties, especially negative values, can differ even when the instrument evidence is internally consistent.

For every index require:

1. list readback equals the recalled source level at query precision;
2. stored TSP level matches the requested value, its binary32 seven-digit encoding, or a documented source-grid level;
3. when using the grid representation, prefer the validated stored level if it lies exactly on the documented grid and its six-significant rendering equals the returned value;
4. output remains OFF before and after proof, native count is exact, and the error queue is clean.

Apply the same rule in both places:

- the edge driver's native-list proof;
- all host/controller receipt validators.

A corrected edge proof is insufficient if a host validator still checks `actual == [float(format(v, '.6g')) ...]` or recomputes grid rounding directly from the unrestricted host request. For modern proofs with `stored_configs`, compare each `raw_readback[i]` with `stored_configs[i].recalled_level_V`. Keep host `.6g` comparison only as a legacy-fixture fallback when per-index stored evidence is absent.

## TDD and deployment sequence

1. Add a minimal regression reproducing the exact negative/positive tie before changing production code.
2. Confirm the test fails for the intended missing behavior.
3. Implement the smallest shared grid-model helper.
4. Run the focused regression and the surrounding controller/executor suite.
5. Restart only the affected edge service so the new module is loaded.
6. Rerun non-exposing native output-OFF proofs and record the new deployment hash.
7. Do not begin candidate stress until exact counts, output `0`, matrix `nil`, and empty errors are verified.

## Post-commit recovery

A missing receipt is not proof of zero exposure. Freeze automatic retries and inspect the exact operation ID in the permanent ledger.

If the operation is `COMPLETE` with full native rows, measured energy, and verified cleanup:

1. verify fresh output OFF, matrix open, and an empty error queue;
2. corroborate operation identity in wire/native evidence;
3. deep-copy the exact ledger operation—never synthesize rows;
4. run the corrected receipt validator against the frozen recipe operation;
5. add only controller metadata such as category, campaign cycle, `reconstructed_from_permanent_ledger=true`, and `no_replay=true`;
6. atomically write the missing receipt;
7. regenerate cycle metrics from the two validated branch receipts;
8. reconcile terminal/progress counters to include the completed branch;
9. compact only after the unique receipt exists;
10. resume at the first genuinely missing cycle/branch.

The compactor must fail closed when a unique external receipt is absent. A compactor failure must never trigger electrical replay.

## Verification checklist

- [ ] Exact ledger operation is COMPLETE.
- [ ] Full native rows and cleanup evidence exist.
- [ ] Output is `0`, matrix is `nil`, errors are empty.
- [ ] Receipt validator uses stored/recalled evidence for modern proofs.
- [ ] Missing receipt is reconstructed from the ledger entry exactly once.
- [ ] Cycle metrics and health-sweep counters are reconciled.
- [ ] Compaction succeeds only after receipt durability.
- [ ] Resume boundary excludes all completed exposure.
