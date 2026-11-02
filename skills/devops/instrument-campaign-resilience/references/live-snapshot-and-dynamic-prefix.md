# Live Plot Snapshots and Dynamic Ledger Prefixes

Use this note when plotting a campaign that is still acquiring, or when adapting a bounded one-cycle controller to a device with a different preparation length or health-read cadence.

## Freeze a completed plotting boundary

Acquisition may finish more cycles while receipts are being discovered. To produce a truthful snapshot:

1. Determine an explicit boundary `N` from verified completed metric files.
2. Discover native receipts, but retain only cycles `<= N` with both SET and RESET in state COMPLETE and cleanup verified.
3. Assert the retained cycle list is exactly contiguous `1..N`; fail rather than silently plotting gaps or later cycles.
4. Label the figure `snapshot through cycle N`, never `final` while the campaign is active.
5. Keep the native-point CSV and per-cycle contrast CSV beside the PNG.
6. After a verified stop or hard cap, regenerate a separately named final plot from the full contiguous cycle set.

A live snapshot is immutable evidence of the stated boundary even if acquisition subsequently advances.

## Derive ledger-prefix expectations per device

Never copy preparation constants from a prior device. Read these from the validated preparation terminal record and recipe health policy:

- `S0`: completed preparation stress sweeps;
- `P0`: preparation ledger-operation count, including preparation health reads;
- health interval and next due stress-sweep boundary.

Before candidate cycle `n`:

- completed candidate writes = `2 * (n - 1)`;
- candidate health reads = scheduled boundaries crossed from `next_due` through `S0 + 2*(n-1)`;
- expected device ledger operations = `P0 + candidate_writes + candidate_health_reads`.

Require every prefix operation COMPLETE, device UNKNOWN false, and exact native proof counts before dispatch. Also derive the live pose and SET/RESET point counts from current device artifacts rather than editing only a device number.

## Post-commit validator/compactor boundary

An electrical branch may be durably COMPLETE before local validation or receipt writing. If the controller then faults:

- inspect the permanent ledger and wire journal before retrying;
- if COMPLETE with native rows and verified cleanup, reconstruct the missing receipt from that exact ledger payload, validate it, mark `no_replay`, and continue at the next missing branch;
- run compaction only after the unique receipt exists;
- compactor receipt-discovery failure is an archival fault, not authorization to replay electrical stress.

## Native list representation

For Keithley list verification, preserve two independent exact checks:

1. recalled source level equals list readback at instrument query precision;
2. stored seven-significant TSP level equals the requested seven-digit encoding or its binary32 seven-digit encoding.

Do not force host-language six-digit rounding to reproduce instrument decimal-tie rendering, and do not replace these checks with a widened voltage tolerance.
