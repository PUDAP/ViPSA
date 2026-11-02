# Batch/substrate-separated 8×8 forming + randomized pulse grid (2026-06-23)

Use this reference when the user starts a probabilistic-computing substrate grid and gives batch/substrate identity plus a detailed adaptive electrical sequence.

## Data organization

- Save high-throughput probabilistic-computing data separated by both batch and substrate, e.g.:
  - `data/probabilistic_computing/batch_<N>/substrate_<S>/runs/<run_name_timestamp>/`
- Put per-device artifacts under `device_XX/` and include batch/substrate in top-level `summary.json` metadata.
- Preserve `grid_positions.csv`, `grid_row_major.json`, `summary.partial.json`, per-device `summary.json`, and raw CSV/JSON/plots for DCIV and pulses.

## Grid/navigation defaults from this session

- Current substrate: S2; current batch: 1.
- Grid is `8 × 8` devices starting from the current device as device 1.
- Use standard native Zaber spacing: `x_step = 5000`, `y_step = 5000`.
- Generate row-major device numbering, but physically traverse serpentine.
- Between devices:
  1. Force electrical cleanup first: both SMU outputs off, 707B `open_all`, verify no closed channels when available.
  2. Pre-move safe microscope-stage Z retraction: `-40` steps.
  3. Move Zaber X/Y to the next absolute grid coordinate using native units (`units: null`).
  4. Move microscope-stage Z up/forward by `+20` steps before approach.
  5. Perform optical alignment after moving to the next device.
  6. Approach with `+0.5` Z increments; final trim/backtracking uses minimum valid `0.25` steps.

## Electrical sequence per device

1. Run adaptive single DCIV/forming first:
   - Forming path requested: `0 → +1.0 → +1.5 → 0`, then reset side and back to `0`.
   - Start compliance: SET/positive side `1e-6 A`; reset/negative side `1e-5 A`.
   - If the device is already shorted at low-bias precheck, run a truncated lower-voltage RESET sweep first at +1 order of magnitude reset compliance.
   - If negative-forward sweep shows a sudden upward current jump, reduce the reset-side voltage magnitude for following devices.
   - If no RESET is detected, add a reset-side recovery sweep with higher compliance.
   - If apparent permanent HRS/no meaningful current, first verify contact by moving stage Z up/forward only `+0.5` once, then retry/escalate compliance as requested.

2. If DCIV succeeds enough to extract/estimate a SET voltage, switch to Keysight for randomized pulse trains:
   - Generate randomized SET-read-RESET-read trains.
   - SET-voltage list: `0.2 V` to `Vset + 0.2 V` in `0.05 V` increments.
   - Pulse duration: `10 ms`.
   - Pulse compliance initial target: `10e-5 A` (`1e-4 A`).
   - If DCIV leaves the device in SET/LRS, send five RESET pulses before the randomized train.
   - Continue until at least `5000` trains are collected or the device becomes permanently stuck in SET.
   - If stuck in SET, wait `10 s`, send five consecutive RESET pulses, then continue if recovered.

## Contact/approach adaptation

- If multiple devices show open/weak contact, raise/increase the lower approach threshold at a safe boundary.
- If multiple devices show overcontact/short/scratching risk, lower/decrease the upper approach threshold at a safe boundary.
- Keep electrical fidelity intact: do not reduce DCIV resolution, pulse count, randomized voltage list, compliance logging, or reset-pre/recovery logic to speed the run unless the user explicitly authorizes electrical-protocol changes.

## Reporting

- For long runs, start as a tracked background process with notify-on-complete.
- Report the run folder, process/session ID, first-device status, and the encoded batch/substrate path.
- Avoid spamming individual approach-loop reads; report device-level phases and per-device completion artifacts instead.
