# OpenCV RTSP snapshot fallback and stale light recovery (2026-06-19)

## When this applies

Use this reference for ViPSA snapshot requests when:

- the user asks to turn lights on and capture both stations/cameras;
- `puda protocol run` rejects a minimal protocol with `user_id is required in the protocol file`;
- light START fails because a stale run id is still attached;
- Windows `ffmpeg.exe` cannot be executed from the current WSL context, but the OpenCV venv can read RTSP streams.

## Protocol metadata requirement

Recent `puda protocol run --file ...` requires full protocol metadata, not just a `commands` array. Use a generated protocol like:

```json
{
  "project_id": "ed111132-ab51-456d-8776-436a2d604378",
  "user_id": "1204c118-ecb8-4a91-abca-26c18c0bff84",
  "username": "vipsa",
  "protocol_id": "<uuid>",
  "description": "light_turn_on_leave_on",
  "created_at": "<utc-iso8601>",
  "commands": [
    {"step_number": 1, "name": "turn_on", "machine_id": "light", "params": {}}
  ]
}
```

The same metadata wrapper applies to recovery protocols.

## Stale light run recovery pattern

If `turn_on` fails with:

```text
START command failed for machine light: cannot start, <run-id> is currently running
```

then:

1. Check state with a bounded command, because `puda machine state light` streams updates continuously:

```bash
timeout 5 puda machine state light
```

2. If stale active run id blocks START, use the existing recovery recipe:

```bash
puda --nats-servers nats://100.109.131.12:4224 machine reset light || true
```

This may leave `state: error` with `run_id: null`; do not treat reset alone as success.

3. Run a full-metadata recovery protocol:

```json
{
  "description": "light_recover_initialize_off",
  "commands": [
    {"step_number": 1, "machine_id": "light", "name": "initialize", "params": {"startup_command": "off"}},
    {"step_number": 2, "machine_id": "light", "name": "turn_off", "params": {}}
  ]
}
```

4. Retry the full-metadata `turn_on` protocol, then capture images. For leave-on requests, do **not** run `turn_off` afterward.

## OpenCV RTSP fallback

If Windows `ffmpeg.exe` cannot be executed from WSL or one-shot ffmpeg capture is otherwise unavailable, use the OpenCV venv that has RTSP/FFmpeg support:

```bash
/home/vipsa/.venvs/align-cv2/bin/python - <<'PY'
import cv2, time, os, datetime
outdir = '/home/vipsa/vipsa-puda-project/runs/light_on_both_snapshots_' + datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
os.makedirs(outdir, exist_ok=True)
urls = {
    'camera1': 'rtsp://172.30.111.161:8554/camera1',
    'camera2': 'rtsp://172.30.111.161:8554/camera2',
}
for name, url in urls.items():
    path = os.path.join(outdir, f'{name}_lights_on.jpg')
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print(name, 'OPEN_FAILED', url)
        continue
    frame = None
    t0 = time.time()
    count = 0
    while time.time() - t0 < 15:
        ret, fr = cap.read()
        if ret and fr is not None and fr.size:
            frame = fr
            count += 1
            if count >= 2:
                break
        else:
            time.sleep(0.1)
    cap.release()
    if frame is None:
        print(name, 'READ_FAILED', url)
    else:
        cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print(name, path, os.path.getsize(path), frame.shape)
print('OUTDIR', outdir)
PY
```

Verify each printed file exists and has non-zero size, then attach both with `MEDIA:`. Finally run `timeout 5 puda machine state light` and verify the edge is `idle`; remember `idle` is command state, not lamp-off proof.
