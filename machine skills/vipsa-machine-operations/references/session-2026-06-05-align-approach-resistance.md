# 2026-06-05 ViPSA align/approach/resistance notes

Reusable details from the session:

- Windows `ffmpeg.exe` invoked from WSL should receive Windows-style output paths (`C:\Users\amdm\AppData\Local\Temp\...jpg`). Passing `/mnt/c/...` directly to the Windows process produced `Permission denied`; using Windows paths and then verifying the equivalent WSL path worked.
- A combined “move stage, align, approach” run can be interrupted mid-sequence. Before resuming, verify live `stage`, `zaber`, `light`, `keithley-2450`, and `keithley-707b` states/positions rather than relying on the planned position from the interrupted script.
- In contact approach, final high-current cleanup may require repeated small trim retractions, not a single trim. In this session the current stayed near compliance for several `-0.1 * step` trims before reaching the target current window. Keep measuring after each trim and stop only when current is inside range or the hard trim guard is reached.
- Resistance checks after approach should continue to use the low-voltage compliance interpretation: if current is near compliance, report likely short/current-limited; otherwise report apparent resistance and cleanup state.
