---
name: vipsa-image-capture
description: Use when the user asks to get image, capture image, acquire image, take snapshot, or display camera images from ViPSA camera 1, camera 2, both cameras, or both ViPSA stations. Turn the light on, capture requested camera frame(s), then set/verify the user-requested final light state (default off; leave on if explicitly requested) and display image(s) in chat.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, camera, image-capture, lights]
    related_skills: [vipsa-machine-operations, puda-operations]
---

# ViPSA Image Capture

## Overview

Use this skill for ViPSA image-acquisition requests. The standard procedure is:

0. Resolve and probe a live camera source for every requested stream **before illumination**. Prefer bounded `ffprobe` checks against local MediaMTX, then the currently verified reachable host. Do not leave the sample lit while OpenCV spends ~30 seconds opening a dead RTSP endpoint.
1. Turn the ViPSA light on unless the user explicitly requests otherwise.
   - For long video/process captures, do **not** assume the light must remain on for the recording. If the user says the light is not needed during video capture, record without forcing/maintaining illumination; only use light commands required for a specific visual step.
2. Capture one frame from the requested camera(s): camera 1, camera 2, or both. If the user says both ViPSA “stations,” treat that as both camera streams/stations (`camera1` and `camera2`).
3. Return the light to the user-requested final state:
   - default: turn the light off in a cleanup/finally path;
   - if the user says to leave lights on afterward, do **not** run cleanup `turn_off`; verify the `turn_on` command succeeded and the light edge is idle after the command.
   - if the capture is immediately followed by electrical approach, resistance check, DCIV, or pulsing, treat the snapshot illumination as temporary and turn the light off before the electrical phase unless the user explicitly requests otherwise.
4. Verify the final light machine execution state is `idle` and report the intended final lamp state (left on vs turned off).
5. Deliver according to the active interface: use `MEDIA:/absolute/path/to/image.jpg` in messaging-platform chat; in CLI, report the local path or, when explicitly requested, send it through the configured messaging transport. See `references/cli-capture-to-telegram-delivery.md`.

Latest-message guard: if a context-compaction handoff or previous background task mentions an unrelated older objective (for example device health, DCIV, or an align-demo video), ignore it unless the latest user explicitly asks for that task. A fresh image-capture request must complete the image workflow and send fresh media attachments, not drift into stale electrical/status/video reporting, old todos, or old run-directory artifacts. See:

- `references/latest-user-capture-request-handoff-pitfall-2026-06-16.md`
- `references/latest-user-after-compaction-image-capture-pitfall-2026-06-18.md`
- `references/opencv-rtsp-snapshot-and-light-recovery-2026-06-19.md` — full-metadata PUDA protocols, stale light recovery, and OpenCV RTSP fallback when Windows ffmpeg execution is unavailable.
- `references/camera2-snapshot-stale-light-direct-cleanup-2026-06-23.md` — camera 2 RTSP/OpenCV capture plus direct/raw stale-light-run completion and verified `turn_off` recovery when normal protocol light control is blocked.
- `references/snapshot-before-electrical-chain-2026-06-22.md` — combined snapshot → approach/DCIV chain: capture/send both images, turn lights off before electrical approach by default, then apply the approach→DCIV contact gate.

## Trigger phrases

Use this skill when the user says things like:

- “get image”
- “capture image”
- “acquire image”
- “take snapshot”
- “take a picture”
- “show camera 1” / “show camera 2” / “show both cameras”

## Inputs

- `camera`: one of:
  - `1` / `camera 1`
  - `2` / `camera 2`
  - `both` / unspecified when the user asks for plural images

If the user does not specify a camera and the request is singular, use both only if that is the established default in the current context; otherwise ask a short clarification.

## Outputs

- On a messaging-platform session, display one or two image files with `MEDIA:` attachments.
- On Telegram, when the user explicitly asks to **send the images/GIFs** or retries after attachments did not render, verify every file is non-empty, then make the response attachment-focused: emit each `MEDIA:/absolute/path` on its own bare line, outside code fences, with little or no intervening prose. Do not merely list filenames or describe where the artifacts are stored. Include GIFs as `.gif` attachments; if the platform still does not render one, provide an MP4 fallback in addition to the original GIF.
- On a CLI session, do **not** emit `MEDIA:` in the final response because it renders as literal text. Report the verified absolute path and a local viewer command such as `xdg-open <path>`.
- If the CLI user explicitly asks to send the captured file to Telegram, send it to the configured Telegram home chat using `send_message(target="telegram", message="...\nMEDIA:/absolute/path.jpg")`. If the messaging tool is absent from the current cached CLI session, use the configured standalone Hermes sender without exposing the bot token. Require `success: true` and a Telegram `message_id` before reporting delivery. See `references/cli-capture-to-telegram-delivery.md`.
- A concise status line confirming the final light state requested by the user: default turned off/idle, or explicitly left on with the light edge verified idle after `turn_on`.

## Required companion skills

Before operating, load and follow:

- `vipsa-machine-operations`
- `puda-operations`

If the image capture is part of an `align` procedure, contact-pad/probe-tip alignment, ROI preprocessing, thresholding, or contour detection, also load `puda-operations` and follow its **ViPSA Vision Alignment** subsection for the OpenCV processing stages. The older standalone `vipsa-vision-alignment` package has been archived into that umbrella; do not stop just because a separate `vipsa-vision-alignment` skill is not installed.

## Procedure

### 0. Resolve the live stream source before turning on the light

Probe every requested camera path with bounded `ffprobe` before illumination. When publishers and MediaMTX are local, try `rtsp://127.0.0.1:8554/camera1` and `/camera2` first; otherwise test the currently verified reachable host. Require codec/width/height metadata for all requested streams. Discover publisher mappings when labels are uncertain, but report the MediaMTX path labels unless physical identities were freshly verified. Do not execute an older capture helper merely because it worked previously: inspect its hard-coded RTSP URLs and Python interpreter first, and require the preflight probe to succeed against the **same URLs the helper will open**. Patch or parameterize the helper before turning on the light when its endpoint is stale. See `references/local-docker-mediamtx-both-camera-snapshots.md`.

### 1. Verify PUDA and light state

Work from the PUDA project directory:

```bash
cd /home/vipsa/vipsa-puda-project
puda env current
puda machine state light
```

Expected active environment is `bears`. Do not expose NATS connection strings or credentials in the user reply.

### 2. Turn the light on

Run a one-command PUDA protocol. Current PUDA CLI requires full protocol metadata (`project_id`, `user_id`, `username`, `protocol_id`, description/timestamp) around the commands; a bare `{"commands": [...]}` file may validate but then fail at run time with `user_id is required in the protocol file`. Generate the UUID/timestamp per run and include the light command:

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

Validate before running:

```bash
puda protocol validate --file /tmp/<protocol>.json
puda protocol run --file /tmp/<protocol>.json
```

The response should show `status: success` and `data.result: true`.

If START fails because `light` is already active on a stale run id (`cannot start, <run-id> is currently running`), do not pretend light control succeeded. Follow the light recovery procedure in `vipsa-machine-operations/references/light-stuck-active-recovery-and-camera-release-2026-06-10.md`: check state, clear/reset if requested/appropriate, recover with `initialize(startup_command="off")` + `turn_off()`, verify idle, then retry the snapshot light-on protocol. If recovery is not authorized or fails, still capture only if the user explicitly wants the camera frame anyway, and report that light control was blocked.

### 3. Capture frames from requested camera(s)

Prefer the existing MediaMTX RTSP streams, because the cameras may already be in use by the livestream DirectShow/ffmpeg processes.

Known working capture pattern from WSL using Windows ffmpeg:

```bash
FF='/mnt/c/Users/amdm/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'

# Camera 1
"$FF" -hide_banner -y -rtsp_transport tcp \
  -i rtsp://172.30.111.161:8554/camera1 \
  -frames:v 1 -update 1 -q:v 2 \
  'C:\Users\amdm\AppData\Local\Temp\vipsa_snapshot_lit_camera1.jpg'

# Camera 2
"$FF" -hide_banner -y -rtsp_transport tcp \
  -i rtsp://172.30.111.161:8554/camera2 \
  -frames:v 1 -update 1 -q:v 2 \
  'C:\Users\amdm\AppData\Local\Temp\vipsa_snapshot_lit_camera2.jpg'
```

When invoking **Windows `ffmpeg.exe` from WSL**, pass the output filename as a Windows path (`C:\Users\...\Temp\file.jpg`), not as `/mnt/c/...`. A WSL `/mnt/c/...` output path can be interpreted by the Windows process as a literal/invalid Windows-side path and fail with `Permission denied`. After capture, verify the corresponding WSL path:

```text
/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_snapshot_lit_camera1.jpg
/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_snapshot_lit_camera2.jpg
```

Verify each requested image exists and has non-zero size before reporting success.

### 4. Set the requested final light state

Default cleanup is to turn the light off. However, if the user explicitly asks to leave lights on afterward, do **not** send `turn_off`; instead verify the `turn_on` command succeeded and final `puda machine state light` is `idle` (command complete). Remember: `idle` is the PUDA edge execution state, not proof the lamp is off.

If the normal project directory is missing but the light machine is reachable, use the PUDA temporary-project fallback from `puda-operations/references/temp-project-protocol-run-fallback-2026-07-08.md` rather than stopping at the stale path: `puda init . --name light-run ...`, generate full-metadata `turn_off`, run it from the temp project with the active NATS override, then verify `puda machine state light`.

Default/off cleanup path, even if capture fails:

```json
{
  "commands": [
    {"step_number": 1, "name": "turn_off", "machine_id": "light", "params": {}}
  ]
}
```

Then verify:

```bash
timeout 5 puda machine state light
```

Report if light cleanup fails; do not silently ignore it. For leave-on requests, report that lights were left on and that the light edge is idle after the successful `turn_on`. Use a bounded `timeout` because `puda machine state` streams updates continuously and can otherwise hang the turn.

## Implementation notes

- Direct DirectShow capture from the physical devices can fail with “device already in use” when livestream ffmpeg processes are active. Use RTSP/TCP snapshots from MediaMTX first.
- Camera 1 RTSP stream has been observed as `1920x1080` H.264.
- Camera 2 RTSP stream has been observed as `1280x720` or `1920x1080` H.264 at a lower frame rate; it may take a few seconds to produce the first frame. If `ffprobe` sees a healthy low-frame-rate stream but a 15–25 second snapshot times out, retry once with a bounded 75–80 second timeout because a long GOP can delay the first decodable keyframe. See `references/local-docker-mediamtx-both-camera-snapshots.md`.
- Include `-update 1` with ffmpeg image output to avoid sequence-pattern warnings.
- Native Linux ffmpeg builds may reject `-rw_timeout` with `Option rw_timeout not found`. Retry without that input option and bound the whole command with shell `timeout`; do not misclassify an option-compatibility error as an unavailable camera stream. For a verified both-camera workflow that also creates a temporary PUDA project when the remembered project path is missing, see `references/linux-tailscale-both-camera-snapshot-temp-project-2026-07-24.md`.
- When the user asks for current Tailscale livestream addresses or screenshots, verify the live host before answering; do not blindly reuse old script constants. A recent verified Tailscale RTSP host was `100.74.20.98` with `rtsp://100.74.20.98:8554/camera1` and `/camera2`, while older `100.67.251.110` was stale in that session. Use `ffprobe` or an actual frame capture as proof, not only an HTTP/WebRTC page. See `references/tailscale-rtsp-snapshot-host-2026-07-17.md`.
If RTSP on `172.30.111.161` fails, inspect the active MediaMTX process/config and current paths API before trying DirectShow:
  ```bash
  curl -s http://127.0.0.1:9997/v3/paths/list
  ps -ef | grep -Ei 'mediamtx|ffmpeg|camera' | grep -v grep
  ```

### 3b. OpenCV RTSP fallback

If Windows `ffmpeg.exe` cannot be executed from the current WSL context, or one-shot ffmpeg capture is otherwise unavailable, fall back to OpenCV RTSP capture with `/home/vipsa/.venvs/align-cv2/bin/python`. See `references/opencv-rtsp-snapshot-and-light-recovery-2026-06-19.md` for a known-good script. The important checks are: open each `rtsp://172.30.111.161:8554/cameraN` stream with `cv2.VideoCapture(..., cv2.CAP_FFMPEG)`, read up to 15 seconds for a real frame, write JPEGs under the run directory, and verify non-zero file sizes before sending.

### 3c. Docker container-network RTSP fallback

If host-side RTSP URLs return connection refused but the `mediamtx` Docker container is running and logs show `camera1` / `camera2` paths online, capture from inside the MediaMTX container network namespace instead of declaring the stream down:

```bash
docker run --rm --network container:mediamtx \
  -v /home/vipsa/vipsa-puda-project/runs/tmp_capture:/out \
  linuxserver/ffmpeg:latest \
  -hide_banner -y -rtsp_transport tcp \
  -i rtsp://127.0.0.1:8554/camera1 \
  -frames:v 1 -update 1 -q:v 2 \
  /out/camera1.jpg
```

Then verify and process/attach the WSL path under the mounted output directory. Use this as an alignment snapshot source when host RTSP ports are not published. Full notes: `references/docker-container-network-rtsp-capture-2026-06-22.md`.

### 3d. Local V4L2 fallback

If RTSP/MediaMTX camera paths are unavailable, stale, or return 404/no frames, do not stop after a failed RTSP attempt. Try direct local V4L2 capture before reporting failure. A validated fallback is documented in `references/local-v4l2-both-camera-fallback-2026-07-13.md`: turn lights on, capture camera 1 from `/dev/video0` and camera 2 from `/dev/video2` with OpenCV `cv2.CAP_V4L2`, then turn lights off and verify `light` idle / `run_id: null`. Report the actual source device for each attached image. Treat `/dev/video1` and `/dev/video3` as possible non-capturing companion nodes unless live probing proves otherwise.

## 4. Set the requested final light state

For camera 1 only:

```text
Done — light on → camera 1 frame captured → light off/idle.

Camera 1:
MEDIA:/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_snapshot_lit_camera1.jpg
```

For both cameras:

```text
Done — light on → both frames captured → light off/idle.

Camera 1:
MEDIA:/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_snapshot_lit_camera1.jpg

Camera 2:
MEDIA:/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_snapshot_lit_camera2.jpg
```

## Camera 2 bottom-right environment gauge

Camera 2 snapshots may include a digital environmental gauge in the bottom-right corner. The user clarified that:

- The large main number (for example `27.8`) is the **temperature**.
- The far-right bottom number beginning with `55...` is the **humidity level**.

When the user asks for these values, or asks to add environmental readings to a run, capture/read the camera 2 frame, inspect or crop the bottom-right gauge, and write the extracted values into the run metadata/summary JSON with clear keys such as:

```json
{
  "environment_gauge_source": "camera2_bottom_right",
  "temperature_c": 27.8,
  "humidity_percent": 55.0,
  "environment_gauge_confidence": "main temperature clear; humidity partially visible/low confidence if blurred"
}
```

Do not fabricate uncertain digits. If the humidity or temperature is partially cut off or blurred, record the readable prefix and a confidence note rather than inventing the missing digits.

## Verification checklist

- [ ] Requested camera(s) identified: 1, 2, or both. “Both stations” means both camera streams/stations.
- [ ] `puda env current` checked.
- [ ] Light `turn_on` succeeded before capture.
- [ ] Requested image file(s) exist and have non-zero size.
- [ ] If the user asked for environmental gauge values, camera 2 bottom-right gauge was inspected and temperature/humidity were added to run metadata with confidence notes.
- [ ] Final light state handled according to user request: default `turn_off` attempted, or explicit leave-on honored by skipping `turn_off`.
- [ ] Final `puda machine state light` is `idle`.
- [ ] Image(s) attached in chat with `MEDIA:`.
