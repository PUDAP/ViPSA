# Initial-Screening BO Readiness and Storage Closure

Use this reference when closing a long adaptive DC-IV initial-design campaign after infrastructure faults, retries, administrative dispositions, or disk pressure.

## 1. Fixed-range requests on native instruments

When an SMU accepts only discrete fixed measurement ranges, do not send an arbitrary requested range and then relax the readback guard.

1. Preserve the exact requested compliance and waveform.
2. Map the requested measurement range to the smallest supported native range that is **not below** the request.
3. Reject requests above the instrument maximum.
4. Keep the post-write readback guard strict: finite, at least the requested range within native precision, and no greater than the hardware ceiling.
5. Add a regression at the exact boundary that failed. Example: a 10.363149 mA request must select the 100 mA range, not 10 mA.

This is a safety correction, not permission to alter recipe compliance.

## 2. File provenance versus loaded edge code

A deployment-state command may hash the current file on disk even while a long-running Python edge still executes an older imported module.

After changing protected edge code:

1. Run focused hardware-free tests.
2. Verify output OFF, matrix open, and empty error queue.
3. Restart only the affected edge process; do not restart NATS or unrelated machines.
4. Wait for edge readiness.
5. Query the live deployment hash and capabilities again.
6. Repeat OFF/open/error verification before any routed stress.

Do not infer that a matching on-disk hash proves the running process loaded the change.

## 3. Configuration diagnostics must be non-acquiring by construction

Do not use the full continuous-acquisition command as a “configuration-only” diagnostic. If all guards pass, that command may reach `:INIT` and execute the waveform.

Preferred patterns:

- expose a dedicated validation command that returns before `:INIT`;
- validate supported-range mapping offline with a fake instrument model;
- run output-OFF list/configuration proofs that cannot enable output.

If an acquisition command was accidentally run with the matrix open, preserve the native response as instrument evidence but do not count it as DUT candidate data. Verify output OFF, matrix open, and errors empty before proceeding.

## 4. Zero-exposure reconciliation

A dispatched operation may be reconciled as zero exposure only when exact evidence proves all of the following:

- the saved wire response belongs to the exact operation/batch;
- output-ON transitions are zero;
- executed segments are empty;
- native preproofs show output OFF before and after;
- the deployed-source identity is known;
- source ordering proves the failing guard occurs before `:INIT`;
- terminal cleanup is verified;
- cumulative charged energy remains unchanged.

Reconciliation procedure:

1. Back up the ledger atomically under owner and ledger locks.
2. Preserve the original UNKNOWN entry in `unknown_history`.
3. Mark the reconciled operation COMPLETE with `zero_exposure=true` and `candidate_cycle_counted=false`.
4. Store the wire path, code hash, guard-before-INIT proof, and reason.
5. Clear the device UNKNOWN latch only when no unresolved operation remains.
6. Never reuse the failed operation IDs.

A timeout after dispatch without this complete proof remains UNKNOWN and must not be replayed.

## 5. Scientific completion versus administrative closure

Cursor advancement, a consumed-device key, or an administrative disposition does not prove a valid scientific observation.

At initial-screen closure, reconcile every requested device across:

- proposal/recipe identity;
- runner completion records;
- consumed-device map;
- completion acknowledgement;
- permanent electrical ledger;
- verified full-cycle metrics;
- plot/evidence delivery state;
- optimizer handshake.

Normalize legacy records only from authoritative proposal/result evidence. Preserve administrative-fault history when later evidence supersedes it; do not silently erase the earlier state.

## 6. Canonical retry histories

When a device has multiple complete histories:

1. Use an explicit authoritative completion acknowledgement or final runner execution ID to choose the canonical non-superseded execution.
2. Preserve earlier histories as provenance.
3. Do not average incompatible retries into one metric window.
4. Record the canonical-source rule in the dataset builder and manifest.

## 7. BO-ready data contract

A robust initial-screen package should contain:

- one device-level row per physical recipe/device;
- a cycle-level validity table;
- all requested input parameters exactly as proposed;
- per-polarity valid counts and finite conditional contrast summaries;
- validity rate over the declared comparison window;
- verified-cycle count and explicit failure/right-censor/infrastructure-censor semantics;
- source hashes and a schema describing missingness.

Rules:

- keep every device in the validity model;
- use only physically valid finite ratios for conditional contrast targets;
- keep invalid ratios null—never interpolate or impute them;
- distinguish observed recipe failure, right censoring, and infrastructure censoring;
- preserve device hierarchy; cycles are not independent recipes;
- require exactly one normalized runner record per requested device before declaring bookkeeping complete.

## 8. Evidence-first storage cleanup

When disk pressure follows campaign completion:

1. Pause autonomous continuation and verify no controller owns the campaign.
2. Create a compact closure snapshot containing the live runner, ledger, handshake, reconciliation reports, protected driver/tests, and final optimizer evidence.
3. Compress large JSON snapshots and read them back to verify the original SHA-256.
4. Generate a full campaign SHA-256 manifest after all intended cleanup.
5. Update the wiki with operational lessons and durable evidence paths.
6. Delete coordination trees, task-specific temporary scripts/journals, and regenerable caches only after snapshot verification.
7. For prior-run duplicates, delete only byte-identical stale derivatives (for example, a `.partial` file identical to its finalized sibling), keep one canonical copy, and write a deletion manifest containing paths, hashes, and reclaimed bytes.
8. Preserve small per-run metadata such as grid definitions when removing it would make an independent run non-self-contained.
9. Re-run integrity checks on the closure snapshot, BO archive, wiki link, retained canonical duplicate targets, and final disk state.

Do not delete unique experimental files merely because their names look similar. Hash equality and a retained canonical copy are mandatory.

## Verification checklist

- [ ] Focused driver tests pass.
- [ ] Corrected edge module is actually loaded.
- [ ] Output OFF, matrix open, errors empty.
- [ ] Every zero-exposure reconciliation has guard-before-INIT evidence.
- [ ] Exactly one normalized record exists per requested device.
- [ ] BO validity/contrast/survival tables satisfy their declared row counts.
- [ ] Invalid targets remain null and censoring is explicit.
- [ ] Campaign closure snapshot and full manifest verify.
- [ ] Duplicate deletion manifest verifies retained copies.
- [ ] Autonomous continuation remains paused and the next device was not started.
