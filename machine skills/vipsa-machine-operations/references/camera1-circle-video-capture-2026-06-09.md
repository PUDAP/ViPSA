# Camera 1 + light `circle` video capture (2026-06-09)

Use this note when the user asks for a tightly sequenced capture of camera 1 while sending `circle` to the ViPSA light controller.

## User-required sequence

When the user says to follow the sequence exactly:

1. Start capturing video from camera 1.
2. Immediately send `circle` to `light`.
3. Wait the requested duration, e.g. 6 seconds.
4. End the capture.
5. Send the video before any processing.

Do not add multi-second pre-roll unless the user asks for it. If a small encoder/RTSP readiness wait is needed to avoid an empty file, keep it minimal and report it explicitly.

## Implementation pattern

- Camera 1 RTSP stream used in this session: `rtsp://172.30.111.161:8554/camera1`.
- Windows ffmpeg from WSL worked when given Windows output paths, then delivered through the equivalent `/mnt/c/...` path.
- Send `circle` via direct NATS/JetStream light commands, not plain `nc.publish`:
  - subscribe to `puda.light.cmd.response.immediate` and `puda.light.cmd.response.queue`
  - publish `start` on `puda.light.cmd.immediate`
  - publish `control_lights(command="circle")` on `puda.light.cmd.queue`
  - publish `complete` on `puda.light.cmd.immediate`
- Verify final `puda machine state light` is `idle`.

## Timing pitfall

Waiting for the `circle` response before starting the 6-second timer changes the requested sequence; the response wait can add ~0.5 s. For exact timing, start the timer immediately after publishing `circle`, collect the response asynchronously, and stop capture at the requested delay.

## MP4/ffmpeg pitfall

Stopping a direct MP4 encode too soon after RTSP startup can produce an empty or near-empty MP4 even with ffmpeg return code 0. Verify non-trivial file size and duration with ffmpeg/ffprobe-style probing before sending.

If exact immediate start produces an empty file, a practical fallback is:

1. Start capture to an intermediate `.ts` file so frames are written continuously.
2. After capture stop, remux/convert the `.ts` to MP4 with `-c copy -movflags +faststart`.
3. Verify the MP4 duration and size before attaching it.

In this session, a direct immediate MP4 run produced a 287-byte empty file, while the verified playable direct MP4 capture had ~6.1 s duration, 1280×720, and non-trivial MB-scale size. Always choose the verified playable artifact, not merely the newest file.

## Reporting standard

Keep the report concise:

- circle status/result
- actual delay between circle publish and stop request if measured
- video resolution/duration/size
- final light state
- `MEDIA:/absolute/path.mp4`

Do not begin photometric/depth processing until after the video has been sent if the user asked to see the video first.
