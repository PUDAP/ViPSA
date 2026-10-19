# Dual-camera 3×3 grid run with per-device plot delivery (2026-06-18)

## Context

User requested a 3×3 grid measurement starting from the current device, with native Zaber spacing `x=5000`, `y=5000`, safe Z travel handling, full-process video from both camera streams, and per-device plots sent after each device.

## Durable workflow pattern

1. Preflight first:
   - Verify PUDA env and all ViPSA machine states.
   - Verify both RTSP camera streams can be opened/read before starting motion.
   - Cleanup electrical outputs/routes before the first move.
2. Start dual-camera recording before grid traversal:
   - Use in-process OpenCV `VideoCapture`/`VideoWriter` threads for `camera1` and `camera2` when Windows ffmpeg is inconvenient for long recordings.
   - Keep recording until the run `finally` block, then stop writers and verify non-empty MP4s.
3. Generate grid positions from current Zaber origin:
   - Current Zaber X/Y is device 1.
   - CSV numbering is row-major.
   - Physical traversal is serpentine.
4. Apply Z travel handling between devices:
   - Before every Zaber XY travel after the first device, run electrical cleanup, move stage Z by the user-provided safe retract amount, move Zaber to absolute X/Y, then stage Z by the user-provided pre-approach amount.
   - For a first/current device that the user says is not in contact, do **not** blindly retract/protract; approach it directly.
5. For each device:
   - Run contact approach; only run electrical stress if the final current is inside the accepted contact window.
   - Run DCIV, health check, pulse optimization, and 1000-cycle endurance only when preceding gates are safe.
   - Always produce a per-device summary plot, even when measurement phases are skipped; the plot should visibly say what data is missing.
6. Telegram delivery for long runs:
   - If the run will take a long time, start the runner as a tracked background process and create a short `no_agent` cron/script poller.
   - The poller should send each new `device_XX/DONE.json` plot once, and send final camera videos once `summary.json` has `finished_utc` plus verified recording paths.
   - Persist a small sent-state JSON under `~/.hermes/` so the poller does not resend old plots.

## Pitfalls

- Do not wait until the full 3×3 run finishes to send all plots; the user explicitly asked for a graph after every device.
- Do not spam contact-approach loop internals; send device-level completion and plot artifacts.
- Do not run DCIV/pulses on a device whose approach ended below/above the requested contact window; mark measurements skipped for safety and still provide the device plot.
- Stop both camera writers in a `finally` block so partial failures still produce usable process video when possible.
- If the grid request contains conflicting Z wording or values (for example “pre-approach protraction is 15 steps” but “Z stage up 20 steps”), clarify the exact signed Z value before any motion. Treat the user’s clarification as the run parameter and record it in the runner summary.
- If the user explicitly says the current device is not in contact, the first/current device should not receive a safe-retract cycle first. Apply only the confirmed pre-approach/protraction amount before alignment/approach, then let the approach routine find contact.
- For long grid runs launched in the background, do not rely on the main chat context staying alive. Immediately create a `no_agent` cron poller after the runner starts. The poller should discover or hard-code the actual run directory, persist a sent-state JSON under `~/.hermes/`, deliver each `device_XX/DONE.json` plot exactly once, and deliver final videos once `summary.json` contains `finished_utc` and non-empty video paths.
- After starting the runner, verify the process is still running and query PUDA states. It is acceptable and useful to report the active run id and which machine is busy, because this confirms the hardware run is actually underway.
