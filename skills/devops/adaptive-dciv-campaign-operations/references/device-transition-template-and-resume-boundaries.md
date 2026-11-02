# Safe device-transition templating in continuous DCIV campaigns

Use when deriving the next device's travel, alignment, preparation, candidate, health, and supervisor controllers from a prior device.

## Validate semantic identity, not just filenames

Before execution, assert all of the following together:

- device number and canonical `device_id` mapping;
- recipe `source_row`, manifest binding index, candidate ID, and recipe hash;
- nominal and aligned X/Y;
- starting, clearance, pre-approach, and expected final Z;
- branch point-count assertions and total native points per batch;
- output directory, ledger path, operation-ID prefix, and dispatch label;
- health and supervisor script paths.

Search for the previous device in all case forms, including uppercase console constants. Cosmetic stale labels do not change scientific identity, but they damage auditability and should be rejected before dispatch.

## Motion-boundary recovery

A compound travel controller may complete retraction and then fail on a later machine START. Decode the wire journal and inspect persistent stage state before retrying. If retraction is confirmed, modify the continuation to accept that exact resume Z and skip the completed move; never blindly replay it.

A preparation attempt can likewise complete a `+40` pre-approach and then fail before the first electrical sweep because of a stale expected-Z constant. If the terminal proves zero sweeps, cleanup verified, and persistent pose confirms the move, start the fresh preparation controller from the new pose and record the pre-approach as reused. Do not repeat the motion.

## Batch restart discipline

A supervisor should not USB-reset the SMU before every batch. Prefer a clean targeted edge restart. If USB reset is genuinely required, verify enumeration before and after it and do not dispatch until the protected edge plus OFF/open/error/pose gates pass.
