# Lighted camera snapshots via ViPSA livestream

Use this reference when the user asks to turn ViPSA lights on, capture images from both cameras/stations, then display the images. Default final light state is off, but if the user explicitly says to leave the lights on afterward, preserve that requested final state.

## Durable workflow learned

1. Control the `light` PUDA machine with explicit single-command protocols:
   - `turn_on` before capture.
   - If the user did **not** ask to leave the lights on, attempt `turn_off` in a `finally`/cleanup path after capture, even if camera capture fails.
   - If the user explicitly asked to leave lights on, do **not** run `turn_off`; verify the `turn_on` response succeeded and the light edge is `idle` after the command.
   - Verify final `puda machine state light` is `idle` and separately report the intended lamp state (left on vs turned off).
   - Verify final `puda machine state light` is `idle`.
2. Prefer the existing MediaMTX RTSP streams for snapshots when the cameras are already being streamed by Windows FFmpeg:
   - `rtsp://<wsl-ip-or-host>:8554/camera1`
   - `rtsp://<wsl-ip-or-host>:8554/camera2`
3. Capture single stills with Windows FFmpeg from WSL, using RTSP over TCP and `-update 1` for a single output file:

```bash
FF='/mnt/c/Users/<windows-user>/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-*/bin/ffmpeg.exe'
"$FF" -hide_banner -y -rtsp_transport tcp -i rtsp://<host>:8554/camera1 -frames:v 1 -update 1 -q:v 2 'C:\Users\<windows-user>\AppData\Local\Temp\camera1.jpg'
"$FF" -hide_banner -y -rtsp_transport tcp -i rtsp://<host>:8554/camera2 -frames:v 1 -update 1 -q:v 2 'C:\Users\<windows-user>\AppData\Local\Temp\camera2.jpg'
```

Translate output paths back to `/mnt/c/...` before attaching with `MEDIA:/mnt/c/...`.

## Pitfalls

- Do not try to open DirectShow devices directly if active FFmpeg streamer processes already own the cameras. DirectShow may list devices and options, but still fail with `Could not run graph` / `device already in use` or WinRT `Hardware MFT failed to start streaming due to lack of hardware resources`.
- If RTMP capture from a stream hangs, retry the RTSP endpoint with `-rtsp_transport tcp`; in this session RTSP captured both cameras successfully while RTMP camera2 timed out.
- `-frames:v 1` to a single `.jpg` may warn about missing image sequence; include `-update 1` for a clean single-image write.
- Keep connection strings and any PUDA config secrets redacted in reports; do not expose NATS credentials or `.env` values.

## Verification standard

Report only after confirming:

- `turn_on` returned success.
- Both image files exist and have non-zero size.
- `turn_off` returned success.
- Final light machine state is `idle`.
