# Schema-bound remaining-navigation recovery

## Validated method

An interrupted grid navigation had a returned clearance move but no lateral dispatch. Recovery eventually completed live with exactly two remaining lateral commands, fresh final position and safe cleanup readbacks, no clearance replay and no cleanup-command replay. Subsequent acquisition was launched; its electrical outcome is not established here.

1. Read the canonical operation and ordered event rows. Distinguish returned motion, missing readback, absent command intent and ambiguous dispatched command. Preserve every original row.
2. Hold both canonical acquisition-owner and navigation-journal locks. Audit historical terminal/native evidence and hash bindings before starting a short-lived continuation validity window.
3. Maintain evidence-change monitoring/read leases and exact journal-prefix checks through dispatch. Full-history proofs must not become unchecked cached booleans.
4. Review actual native discovery catalogs and their exact digest. A copied null digest caused a real launch to stop before motion despite unchanged native catalog bytes. Compare both semantic catalog contents and retained raw/native evidence; do not blindly accept a newly observed hash.
5. After the locked audit and schema review, bind genuine current-user authorization to the unpredictable operation/prefix/schema challenge. The evidence timestamp is the new binding time, not a fabricated timestamp for an older user message. Never label human approval as bot approval.
6. Read fresh independent native position, confirmed stage state, idle/null-run state, output OFF, matrix OPEN and instrument errors. Only then arm the exact unissued lateral commands from the saved plan.
7. Commit durable intent before each dispatch. Preserve timeout/uncertainty latches; never infer permission to retry from an unchanged coordinate or an equal Y target.
8. Verify each returned move and the final safe pose. Validate the strict completion suffix and full historical Store before releasing locks. Only then perform the optical checkpoint, lights-off verification and separately gated acquisition.

## Changed boundaries are new evidence, not retry permission

A schema-rejection launch appended authorization but no motion intent. The next continuation had to recognize that exact authorization-only prefix, preserve its bytes and prove no lateral dispatch before proceeding. Do not erase the append, invent historical position captures or run the previous entrypoint against a different prefix.

## Resource and test orchestration lessons

- The working integration used substantial historical verification before fresh attestation. Slow preflight is not itself a reason to extend the dispatch TTL.
- Multiple full-history fixtures exhausted the shared file-watch budget before reaching their intended fault injection. Serial execution preserved the original monitoring coverage and allowed the actual lock-loss, drift, schema-change, receipt-failure and crash/no-replay cases to pass.
- `ENOSPC` from monitor creation is not necessarily a full disk. Inspect the failing syscall/resource and distinguish watch capacity from filesystem blocks/inodes. The session also independently encountered a full filesystem; both diagnoses mattered.
- Track bounded suites as independent background processes with completion notifications. Persist result batches with atomic replace/fsync. A worker timing out does not mean its tracked test process failed or stopped; inspect that exact process before restarting anything.
- A caught exception can yield shell exit 0. Verify explicit test assertions/results, not just the wrapper status. A diagnostic happy-path success does not replace failure-path tests or a final source-bound freeze.
- Delayed notices from terminated older runs must not overwrite newer verified results. Record the run identity, source snapshot and actual finished case list.

## User-facing workflow

Repeated requests to start are not an invitation to create endless audit-only layers. Fix the identified defect in the existing unfrozen implementation, prepare the exact parent launcher while tests run, and launch only after the required suite and freeze readback pass. Keep updates concise: live or fixture, motion issued or not, exact blocker and actual next running action. Interpret 'remove blockers' as resolving implementation obstacles while retaining native safety checks.
