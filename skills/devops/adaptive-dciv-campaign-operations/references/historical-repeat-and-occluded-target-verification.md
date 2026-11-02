# Historical-repeat and occluded-target verification

## User corrections to preserve

- A terminal probe normally obscures its target. Before declaring alignment blocked, use neighbouring devices as fiducials to reconstruct target position. Occlusion alone is not an error.
- Distinguish row-major device labels from serpentine traversal indices. Establish both labels' row/column and absolute coordinates; two apparently different sequences can describe the same physical route.
- An operator amendment such as retract −100 / pre-approach +85 or a +2.5 post-forming move must be explicit in the policy and handoff. These are scoped amendments, not universal historical defaults. Apply new policies prospectively without replaying completed approach or forming.

## Verified fiducial method

1. Verify fresh output-OFF, matrix-open, error-empty and native stage/XY readbacks. Hold the global owner during capture; illuminate, acquire camera 1, and restore the required light state in finally cleanup. Do not move just to expose a hidden target.
2. Visually identify multiple neighbouring electrode sites at known lattice offsets, preferably spanning both axes. Exclude the hidden target from detection. Inspect partial/low-contrast fiducials rather than trusting their proximity to a predicted position.
3. In the demonstrated ring-electrode view, use local red-minus-blue contrast and normalized annular-template matching around visually selected visible sites. Template radii and seed coordinates are frame-specific, not transferable calibration. Use another detector when electrode appearance changes.
4. Fit image coordinates with an affine lattice, `p = origin + column*u + row*v`. Compute per-fiducial residuals, reject ambiguous or inconsistent site assignments, and estimate the hidden target from its lattice index.
5. Independently mark the actual terminal apex/footprint. Compare it with the inferred target and fresh native grid coordinates. Overlay observed fiducials, inferred centre, apex and residuals; inspect the image before approving.
6. The demonstrated six-site fit had maximum residual 2.21 px; target-to-marked-apex distance was 6.60 px, supporting the target under the terminal footprint without XY correction. These are example results, not universal acceptance thresholds. In particular, fit residual is not a bound on absolute target uncertainty or probe localization error.
7. Save original image/hash, pose proof, observed sites and lattice indices, fitted vectors, residuals, inferred target, independently marked apex, overlay, and assessment in the device-specific navigation context.
8. Approval means geometric target identity only. Do not infer vertical contact, electrical continuity, retained switching, or precise conductive-rim contact from a hidden centre. Actual contact/forming remains governed by the authorized electrical criterion and motion ceilings.

## Exact historical-repeat audit

Compare actual executed requests and receipts, not merely frozen candidate parameters or a later campaign template. Audit:

- forming endpoint, point list, compliance, dwell, ranges, PF/PB acceptance scope, threshold, consecutive-sample and downjump rules;
- attempt ceilings and any divergence between frozen policy and executable ancestry;
- all conditioning operations and extra diagnostic exposures;
- health reads: carry the stress count from forming attempts through conditioning; distinguish after-every-N-sweeps from after-every-N-cycles;
- continuous acquisition mode, zero boundaries, output continuity across segments, integration/range/autozero settings;
- commanded delay versus demonstrated native timestamp spacing;
- mechanical sequence, native coordinates, direction and current authorization;
- energy-policy authority and reference-operational accounting versus demonstrated hardware cutoff.

This session found an 8 V historical forming waveform versus a carried-forward 10 V waveform, and PF-only 90 µA/drop-check acceptance versus PF/PB 95 µA acceptance. Unchanged conditioning and candidate parameters did not make those runs equivalent. Preserve affected histories as non-equivalent comparisons, not silently corrected experiments.

For explicitly requested post-forming motion: journal intent before dispatch, require successful forming and fresh OFF/open proof, enforce absolute ceiling, verify position, then authorize conditioning. Test exactly-once movement, no move on unsuccessful forming, no replay/UNKNOWN handling, and handoff-pose consistency. In this session +2.5 was tested offline before enablement; do not describe that as hardware qualification unless a later real receipt proves it.

## Plotting and continuation

Produce forming/conditioning figures from saved native receipts, preserving acquisition order and source hashes. Include every positive attempt, initial negative sweep and all conditioning pairs; separate health reads and preparation from candidate counters. Use V-command versus log absolute current with PF solid/PB dashed/NF dotted/NB dash-dot. Provide PNG and CSV with attempt/cycle/Z/timestamps. For many attempts use a colour scale, not an unreadable full legend; Matplotlib `cmap(1.0)` reaches the upper colour endpoint, whereas integer `cmap(1)` indexes the lookup table.

Before launching an ordered CLI chain, exercise each entry point's parser and full mocked orchestration, including required execute flags. If a later launcher fails before dispatch, preserve all completed forming/qualification records and resume only the pending stage after inspecting its exact journal and ensuring the original worker has exited. Never launch duplicate hardware owners or replay preparation to repair a CLI error.
