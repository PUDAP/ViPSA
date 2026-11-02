# Session note: current-device 3x3 grid measurement and stop/cleanup

Use this reference for future ViPSA grid measurement runs where the user asks to run a grid from the current device and/or asks to stop an active run.

## Grid generation from current device

- If no grid CSV is supplied, generate `device_number,x,y` (optionally with row/col metadata) from the current Zaber X/Y readback as device 1/origin.
- Ask for `x_distance`, `y_distance`, `rows`, and `columns` if the user has not already established defaults. In the common ViPSA 3x3 examples, spacing has been 5000 native Zaber units in X and Y.
- CSV/device numbering is row-major, not serpentine:
  - row 0: `1, 2, 3`
  - row 1: `4, 5, 6`
  - row 2: `7, 8, 9`
- Coordinates are absolute Zaber positions. Example with origin `(100,100)` and 5000 spacing:
  - `1,100,100`
  - `2,5100,100`
  - `3,10100,100`
  - `4,100,5100`
  - ...
  - `9,10100,10100`
- Physical traversal is serpentine even though CSV numbering is row-major: `1,2,3,6,5,4,7,8,9` for 3x3.

## Per-device workflow

1. Check if contact is already made. If contact already exists, skip align/approach and go directly to the requested tests.
2. If not contacted: perform 🎯 alignment.
3. Perform 👇 contact approach.
4. Run the requested electrical tests. For the common forming/endurance request:
   - one DCIV sweep to ensure forming,
   - pulse optimization,
   - 1000 pulse endurance at the optimized parameters, preferably in bounded batches with safety gates.
5. Move to the next device:
   - turn SMU outputs off and open the 707B routes,
   - move stage Z down/retract to safe travel height,
   - move Zaber X/Y to the next absolute CSV target,
   - move stage Z down/up toward the device by the pre-approach amount to avoid wasting approach time,
   - repeat contact check/align/approach/tests.

## Camera recording during grid operations

- When the user says to record both stations/cameras during the operation, start both camera streams before the first device and verify the files are growing.
- Use the OpenCV-capable interpreter (`/home/vipsa/.venvs/align-cv2/bin/python` in this environment) for recording code that imports `cv2`.
- Avoid force-killing the recorder if a playable MP4 is required: OpenCV MP4 writers need a clean `writer.release()` for the `moov` atom. If the user asks to stop urgently, comply immediately, then verify whether the MP4s are playable; report honestly if `moov atom not found` and do not send them as valid videos.
- For future long runs, prefer a stop-aware runner that catches SIGTERM/SIGINT, sets a stop flag, releases camera writers, sends PUDA `complete`, and performs electrical cleanup before exiting.

## Stop/abort cleanup pattern

When the user says `stop` during a grid run:

1. Kill/stop the active process promptly.
2. Remove/pause any cron pollers for that run so they do not keep sending stale updates.
3. Run electrical cleanup:
   - `keithley-2450.set_output(false)`
   - `keysight-b2902b.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`; safe result is `nil`.
4. Send `complete`/clear the active run ID for all ViPSA machines if needed.
5. Verify final machine states: `idle` with `run_id: null` for `keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, and `zaber`.
6. Write an abort marker in the run folder with stop time, cleanup status, and any artifact caveats.
7. Report what completed before stop (device count/status), the run folder, cleanup verification, and media playability.
