# Camera 2 snapshot with stale light-run cleanup (2026-06-23)

## Trigger

Use this when a ViPSA camera snapshot request succeeds visually, but normal PUDA light protocols fail during turn-on/turn-off due to NATS protocol-run timeouts or a stale `light` run id.

## Observed useful pattern

- Camera 2 could still be captured from the existing RTSP stream using the OpenCV fallback:
  - URL: `rtsp://172.30.111.161:8554/camera2`
  - Python env: `/home/vipsa/.venvs/align-cv2/bin/python`
  - Output verified as a non-empty JPEG before reporting.
- Normal `puda protocol run` for `light.turn_on` / `light.turn_off` may fail before execution because protocol-run NATS connection selection times out, even while the raw NATS ports are reachable.
- A direct/raw light cleanup can reveal a stale active run via `RUN_ID_MISMATCH`, for example:
  - `cannot start, <stale-run-id> is currently running`
- Completing that exact stale run id on `puda.light.cmd.immediate` can clear the block.
- After the stale run is completed, retry a raw/direct light transaction:
  1. `start` with a fresh run id
  2. queue `turn_off` step 1
  3. `complete` with the fresh run id
  4. require the `turn_off` response to show `status: success` and `data.result: true`

## Reporting rule

If the image was captured and verified, send the `MEDIA:` image even if light control had to use recovery. In the concise status, say that normal light protocol was blocked by a stale PUDA run, the stale run was completed, and `turn_off` then succeeded. Do not hide the recovery path, and do not claim normal protocol light control succeeded.

## Minimal OpenCV capture snippet

```python
import cv2, time
url = "rtsp://172.30.111.161:8554/camera2"
out = "/path/to/camera2_snapshot.jpg"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
end = time.time() + 15
ok = False
while time.time() < end:
    ret, frame = cap.read()
    if ret and frame is not None and frame.size:
        cv2.imwrite(out, frame)
        ok = True
        break
    time.sleep(0.2)
cap.release()
assert ok
```

## Safety note

This is a cleanup fallback after protocol-first light control is blocked. Use direct/raw NATS only for the stale-run completion and final light cleanup verification path; keep the image capture itself read-only via RTSP/OpenCV.
