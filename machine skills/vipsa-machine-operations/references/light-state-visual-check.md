# Checking whether the ViPSA light is on

PUDA `puda machine state light` reports machine execution state (`idle`, `active`, etc.) and does **not** expose a durable on/off/color telemetry field for the serial light controller. Treat `idle` only as "not currently running a command", not as proof that the lamp is off or on.

## Practical verification workflow

1. Check PUDA is reachable and the light edge is idle/responding:
   ```bash
   puda env current
   puda machine state light
   puda machine commands light
   ```
2. If the question is simply "is light on now?", use the live camera feed as the observable truth:
   - Preferred interactive check: open the existing MediaMTX WebRTC page for a camera stream, for example `http://127.0.0.1:8889/camera1/`, press play if needed, and visually inspect illumination.
   - A dim, noisy microscope/sample view means the light is likely off; a bright, evenly illuminated view means the light is on.
3. When producing artifacts instead of an answer, capture stills from the already-running MediaMTX streams rather than opening the USB camera device directly, because the streaming containers may already own `/dev/video*`.
4. Report confidence honestly: "PUDA reports the light machine is idle, but it has no on/off telemetry; the camera view looks dark/bright, so the light appears off/on."

## Pitfalls

- Do not infer on/off from `puda machine state light`; it is an execution-state API, not a lamp-state API.
- Do not rely on direct `/dev/video*` access while livestream containers are running; use RTSP/WebRTC/HLS from MediaMTX.
- For Windows `ffmpeg.exe` capture from WSL, use Windows output paths (`C:\\Users\\...\\Temp\\file.jpg`) and then attach/read via the equivalent `/mnt/c/...` path.
