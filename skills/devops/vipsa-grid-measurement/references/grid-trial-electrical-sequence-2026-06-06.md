# Grid trial with conditional electrical sequence (2026-06-06)

## Scenario

The user requested a 3x3 grid starting from the current device, native Zaber spacing of `5000` steps in X and Y, skipping measurement of the first/current device, and saving to a permanent folder named `PUDA grid trial 1`.

Requested mechanical settings:

- Grid origin: current Zaber X/Y position at command time.
- CSV numbering: row-major device numbers.
- Physical traversal: serpentine order, e.g. for 3x3 `1,2,3,6,5,4,7,8,9`.
- Skip device 1 measurement but still preserve it in the grid CSV and summary as skipped.
- Safe Z retract before X/Y travel: stage Z `45` steps downwards in the user's convention (safe retract/travel move).
- Partial Z pre-approach at destination: stage Z `20` steps back toward contact before running the established default approach.

Requested per-device electrical sequence:

1. Resistance check first to see if the device is already shorted.
2. If not shorted, run DCIV forming.
3. Only if a good SET is seen, run pulse-train optimization bounded to at most `100` pulses.
4. Only if the device is still alive after optimization, run the longer `500` pulse test.

## Durable workflow lessons

- Treat `skip measuring the first device` as a measurement skip, not a grid omission: include device 1 in `grid.csv`, traversal metadata, and final summary with a skipped status.
- For permanent grid runs, create a stable top-level folder using the exact user-provided name, then a timestamped run subfolder beneath it. Keep `grid.csv` at the top level and per-run summaries/artifacts in the timestamped subfolder.
- Use one row per device in a durable summary CSV and update it as the run progresses. This allows recovery/reporting after long background runs or context compaction.
- For conditional electrical sequences, encode gates explicitly in the runner: shorted resistance check stops further stress; missing/poor SET after DCIV skips pulse optimization; failed/alive check after optimization skips the endurance pulse train.
- Use bounded background execution with a process/session id for long multi-device runs and report the run folder plus live summary CSV path immediately.
- During movement between devices, cleanup electrical state before travel: SMU outputs off and 707B open. Then retract Z, move absolute Zaber X/Y, perform only the partial pre-approach Z move, and let the normal approach routine find contact.

## Reporting pattern

A concise start report should include:

- top-level folder and timestamped run folder;
- grid dimensions, origin, spacing, and traversal order;
- which devices are skipped;
- safe Z retract and pre-approach distances;
- process id/session id if running in the background;
- summary CSV path for live progress.

A final report should include:

- per-device status and reason for any skipped gate;
- final SMU/707B cleanup verification;
- final Zaber/stage readbacks;
- artifact folder paths.
