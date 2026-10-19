# S1 8x8 current-device grid: fixed DCIV + randomized 10k-pulse protocol (2026-06-30)

## Trigger
Use this reference when starting a fresh substrate/campaign grid from the current physical device with a user-specified electrical recipe and per-device reporting requirement.

## Pattern captured
- Campaign hierarchy: save under `data/probabilistic_computing/batch_1/substrate_S1/runs/<run_name_timestamp>/` and record `batch=1`, `substrate=S1` in run metadata.
- Treat the current Zaber X/Y position as device 1 origin for an 8x8 row-major grid with 5000 native-unit X/Y spacing; traverse physically in serpentine order.
- For the first device, if the user explicitly says to start from this device and asks to align/approach, do not reuse prior manual approach artifacts by default. Run alignment and approach on device 1.
- Between devices: force electrical cleanup, then stage Z safe retract `-50` steps, move Zaber to the next absolute X/Y, stage Z pre-approach `+30` steps, then align and approach.
- Run background measurement with a fixed output folder path computed before launch so the monitor/reporting script and the runner point to the same directory.
- Create a no-agent reporter script/cron that watches `device_*/DONE.json`, de-duplicates via a state file, and sends a concise per-device summary plus `MEDIA:<device_plot.png>` after each completed device.
- Append a project logbook entry at run start with the runner path, output folder, and exact electrical/mechanical parameters.

## Electrical recipe used
- DCIV: `0 -> +0.8 -> 0 -> -1.0 V`, `0.02 V` step.
- SET-side compliance (`PF/PB`): `1e-5 A`.
- RESET-side compliance (`NF`): `1e-4 A`.
- Randomized pulse train: `SET-read-RESET-read`.
  - SET levels: `0.20 V` to `1.00 V`, inclusive, spaced by `0.05 V`.
  - Reset voltage: `-1.0 V`.
  - Read voltage: `+0.1 V`.
  - Pulse width: `10 ms`.
  - Pulse compliance: `1e-4 A`.
  - Balance/randomization: 50 attempts per voltage level per block; shuffle the block; repeat blocks until device failure or `10000` total pulses (`2500` trains).
  - Execute in `500`-pulse chunks (`125` trains per chunk) and analyze after each chunk.
  - Estimate `P(switch | V)` from read-after-SET/read-after-RESET distributions using the existing distribution/ROC/bimodal-style threshold logic; save `switching_probability.csv` and sigmoid fit metadata.
- Device failure/recovery gate: preserve existing recovery behavior (e.g. reset bursts for stuck-SET, small contact nudge for permanent-HRS/open-like cases, stop on read-current near pulse compliance) and preserve partial pulse CSVs.

## Implementation pitfall
When deriving a new runner from an older campaign script, avoid blind global replacements. In this session, changing `5000` in text for a 10k-pulse run could also alter the grid spacing if not corrected. Verify all of these explicitly before launch:
- output path / substrate name
- `x_step` and `y_step` remain `5000`
- generated grid formula uses `col*5000`, `row*5000`
- safe retract/pre-approach are `-50/+30`
- first-device handoff branch is disabled if the new user request says to align and approach
- script compiles (`python3 -m py_compile`) before starting background hardware execution

## Verification before reporting start
- Probe all six ViPSA machines for `idle`/`run_id: null` when available.
- Confirm the background process is still running after launch.
- Confirm the output folder exists and at least `grid_positions.csv`, `grid_row_major.json`, and `device_01/summary.json` appear.
- Confirm alignment artifacts for device 1 appear if alignment has started.
