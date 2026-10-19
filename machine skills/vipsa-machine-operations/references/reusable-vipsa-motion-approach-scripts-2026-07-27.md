# Reusable ViPSA Stage/Zaber movement and approach scripts — 2026-07-27

Created project-level reusable scripts under `/home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/`:

- `tools/vipsa_move.py` — protocol-first reusable motion utility for Stage-Z and Zaber X/Y.
  - Safe by default: dry-run unless `--execute` is supplied.
  - Stage support is Z-only by design (`--stage-z-by`), preserving the user's no Stage X/Y movement convention.
  - Zaber supports relative (`--zaber-x-by`, `--zaber-y-by`) and absolute (`--zaber-x-to`, `--zaber-y-to`) native-unit or explicit-unit moves.
  - Native Zaber units are encoded as `units: null`; do not convert to mm unless explicitly requested.
  - Reads pre/post positions with separate protocols and writes `summary.json`.
  - Include user-observation caveat: if observed motor motion contradicts PUDA/readback, treat readback as internal/tracked only.

Example commands:

```bash
# Dry-run only
python3 tools/vipsa_move.py --stage-z-by 15 --label z_up15

# Execute Stage-Z up 15 steps
python3 tools/vipsa_move.py --stage-z-by 15 --label z_up15 --execute

# Execute absolute Zaber move in native units after a safe Stage-Z retract
python3 tools/vipsa_move.py --stage-z-by -50 --zaber-x-to 266765 --zaber-y-to 496131 --label to_device15 --execute
```

- `tools/vipsa_approach.py` — protocol-first customizable Keithley-guided contact approach.
  - Safe by default: dry-run unless `--execute` is supplied.
  - Defaults: `10 mV`, `1–10 nA` target window, `1 µA` read compliance, `+0.5` Stage-Z coarse steps, `0.25` trim/fine steps, 3 stability reads.
  - Turns light off before/final by default.
  - Routes through Keithley/707B, logs every read/move to `approach_log.csv`, writes `approach_summary.json`, and performs cleanup (`Keithley off`, `Keysight off`, `707B open/nil`, light off if configured).
  - Enforces minimum Stage-Z step of `0.25`; no Stage X/Y movement.

Example commands:

```bash
# Dry-run default approach plan
python3 tools/vipsa_approach.py --label default_1nA_10nA

# Execute default 1-10 nA approach
python3 tools/vipsa_approach.py --execute --label default_1nA_10nA

# Execute custom approach
python3 tools/vipsa_approach.py --execute --lower 5e-10 --upper 1e-8 --step 1 --max-attempts 100 --label custom_contact
```

Verification performed at creation:

```bash
chmod +x tools/vipsa_move.py tools/vipsa_approach.py
python3 -m py_compile tools/vipsa_move.py tools/vipsa_approach.py
python3 tools/vipsa_move.py --help
python3 tools/vipsa_approach.py --help
python3 tools/vipsa_move.py --stage-z-by 5 --zaber-x-by 100 --label dryrun_test
python3 tools/vipsa_approach.py --lower 1e-9 --upper 1e-8 --step 0.5 --max-attempts 3 --label dryrun_test
```
