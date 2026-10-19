# Linux/Tailscale both-camera snapshot with temporary PUDA project

Validated end-to-end pattern when the remembered ViPSA project directory is absent:

1. Verify `light` state through the known ViPSA NATS endpoints.
2. Create a temporary PUDA project (`puda init . --name ...`) and use its generated project ID plus the active `puda config list` user metadata in full-metadata protocols.
3. Run and verify a one-command `light.turn_on` protocol.
4. Capture both streams from the currently verified Tailscale MediaMTX host with native Linux `ffmpeg`:
   ```bash
   timeout 35 ffmpeg -hide_banner -loglevel error -y -rtsp_transport tcp \
     -i rtsp://<verified-host>:8554/camera1 \
     -frames:v 1 -update 1 -q:v 2 /tmp/camera1.jpg

   timeout 45 ffmpeg -hide_banner -loglevel error -y -rtsp_transport tcp \
     -i rtsp://<verified-host>:8554/camera2 \
     -frames:v 1 -update 1 -q:v 2 /tmp/camera2.jpg
   ```
5. Verify both JPEGs are non-zero before reporting success.
6. In a cleanup path, run a full-metadata `light.turn_off` protocol and verify `light` is `idle` with `run_id: null`.

## Portable ffmpeg timeout pitfall

Do not assume every ffmpeg build supports `-rw_timeout`. One Linux build rejected it with `Option rw_timeout not found`; retrying with an outer shell `timeout` and no `-rw_timeout` captured both streams successfully. Treat this as an option-compatibility fallback, not evidence that the RTSP stream is down.

## Host freshness

The host used in the successful session was `100.74.20.98`, but it is not a permanent constant. Verify the current host by obtaining a real frame; do not rely on TCP reachability or an old address alone.
