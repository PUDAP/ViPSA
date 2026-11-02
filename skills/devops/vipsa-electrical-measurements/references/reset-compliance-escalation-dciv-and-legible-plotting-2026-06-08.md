# Reset-compliance escalation DCIV + plotting lesson (2026-06-08)

## Context

User asked for a Keithley-guided approach with `step_size=1`, then a DCIV sweep shaped:

```text
0 -> +1 -> -2 -> 0 V
```

with conservative SET compliance and sequentially increasing RESET compliance until a good RESET appears, because devices were often dying by permanent SET.

## Useful execution pattern

1. Run contact approach first using established ViPSA defaults, but honor the explicit step-size override:
   - `test_voltage=0.01 V`
   - `lower=1e-8 A`, `upper=1e-7 A`
   - `step_size=1`
   - forward `+Z`
2. Proceed to DCIV only if final approach current is stabilized inside the contact window.
3. Keep SET compliance conservative while escalating RESET compliance first. A safe observed plan was:
   - sweep 1: SET `1e-7 A`, RESET `1e-6 A`
   - sweep 2: SET `1e-7 A`, RESET `3e-6 A`
   - sweep 3: SET `1e-7 A`, RESET `1e-5 A`
   - only then consider modest SET-compliance increase if RESET is promising and reads are not already perma-set-like.
4. Construct non-duplicated 121-point path at `0.05 V` pitch:
   - PF: `0 -> +1`
   - RESET_DOWN: continue from `+0.95 -> -2`
   - RETURN: continue from `-1.95 -> 0`
5. After the SET branch and after the RESET/return branch, take low-voltage read probes at `+0.1 V` using the conservative SET/read compliance. Use these read probes for the practical RESET score.
6. Stop escalation when either:
   - good RESET: post-SET read / post-RESET read ratio is clearly separated, e.g. `>= 5x`, and the post-RESET read is well below the SET/read compliance; or
   - safety stop: post-RESET read remains pinned near the SET/read compliance after increasing RESET compliance, indicating perma-set-like behavior.
7. Always cleanup: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, final machine states idle.

## Interpretation wording

If post-SET and post-RESET low-voltage reads are both pinned at the read/SET compliance, report this as:

```text
no RESET detected; perma-set-like safety stop
```

Do not call RESET good just because the negative/reset branch hit a higher compliance. The deciding evidence is separated low-voltage read states after the reset branch.

## Plotting lesson from this session

A quick dependency-free PNG plotter produced ugly blocky labels that the user reasonably questioned. For user-facing ViPSA electrical plots:

- Prefer a real plotting backend (`matplotlib` in a temporary venv is fine) or a clean SVG with normal text labels.
- Do not ship crude bitmap-font plots unless explicitly marked as a rough preview.
- If forced to make a dependency-free preview, keep labels plain, legible, and scientific; avoid compressed/ambiguous titles that look like the wrong language or arbitrary styling.
- The raw CSV/JSON is the primary artifact, but preview plots should still be readable enough for scientific review.
