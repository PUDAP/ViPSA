# BO namespace execution-contract dry validation

Use after freezing a later optimizer batch and before any hardware command.

1. Import the exact candidate controller that will execute against the new namespace.
2. Instantiate its initial-ledger and segment constructors against Candidate 1.
3. Assert manifest compatibility fields such as `batch_id`, recipe identity, proposal row, binding index, source hashes, preparation-terminal hash, and final pose.
4. Assert the authorized policy change exactly (for example cap 300) while batch size, health cadence, failure rule, and no-replay policy remain unchanged.
5. Assert exact SET/RESET point counts and total native points per batch.
6. Audit every case variant of cloned identity strings (`device51`, `Device51`, `DEVICE51`) plus paths and structured IDs. Require zero stale prior-device identifiers before dispatch.

A syntax check alone is insufficient: it does not discover missing manifest fields or stale uppercase audit labels. Fix the durable manifest/controller contract and rerun this dry validation; never weaken the runtime checks.