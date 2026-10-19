# ViPSA chained stage-Z move then camera alignment (2026-06-29)

Trigger: user asks tersely for a Z-only microscope stage jog followed by alignment, e.g. `move stage down by 10 steps and align`.

Validated workflow:

1. Treat the request as a combined hardware operation: first execute the signed stage Z move, then run the standard camera-1 pad alignment. Do not ask for clarification when axis, direction, step count, and align are explicit.
2. Use PUDA protocol-first stage motion from `/home/vipsa/vipsa-puda-project`:
   - stage down maps to `stage.move_z_by(height=-<steps>, feedrate=450)`.
   - verify stage with a separate one-command `stage.get_current_position()` protocol after the move.
3. Only after successful Z motion/readback, run the standard reusable alignment runner:
   - `/home/vipsa/vipsa-puda-project/runs/run_alignment_now_turn_off.py`
   - camera 1 RTSP
   - centered 900x900 ROI dark-pad detector
   - `25` native Zaber steps per pixel
   - up to two correction passes
   - final verification capture and `final_annotated.jpg`
   - lights off afterward by default.
4. Verify/send the final overlay artifact exists and is non-empty before reporting success.
5. If final `puda machine state` probes time out after all command responses succeeded, report the timeout as a verification limitation, not as proof that the completed move/alignment/light-off failed. Use the command response artifacts as grounding and include the state-probe limitation concisely.

Concise report fields:

- 🎯 aligned status.
- Signed stage Z move and readback, e.g. `height=-10`, `z=-10`.
- Zaber correction moves in native units for each pass.
- Final pixel residual `x/y/dist`.
- Light cleanup command result.
- Any final state-probe blocker.
- Attach the final overlay with `MEDIA:/absolute/path`.

Concrete successful artifact pattern:

- Combined wrapper: `runs/stage_z_down_10_then_align_YYYYMMDD.py`
- Wrapper output dir: `runs/stage_z_down_10_then_align_<timestamp>/summary.json`
- Alignment output dir: `runs/align_now_<timestamp>/summary.json`
- Overlay: `runs/align_now_<timestamp>/final_annotated.jpg`
