# Long experimental campaign status and plot delivery

Use these conventions when the user wants an unattended multi-device campaign with concise live reporting.

## Status cadence

- Schedule a recurring update at the requested cadence (15 minutes in the learned workflow).
- Read current process state, newest progress/terminal artifacts, readiness files, and the permanent operation ledger each time; do not repeat stale conversation state.
- Report: last verified completed action, current device and active operation, completed full cycles and stress sweeps, cleanup/fault/blocker state, and next automatic step.
- An `INTENT`, in-flight branch, or fail-closed initial `status: fault` placeholder is not completion. Plot/count only fully completed cycles.

## Visible optimizer coordination

When the user asks for optimizer/Bayesian exchanges in chat, post preparation-complete requests and final-result tells visibly in the current chat. Keep hardware ownership with the executor; the optimizer selects/records recipes only. Do not wait for an extra confirmation between devices when automatic progression was authorized.

## Plot/file delivery preference

- Deliver PNG only by default.
- Save native and summary CSVs in the relevant device/run dataset folder, but do not attach them unless requested.
- Do not generate or send SVG unless explicitly requested.
- Candidate DCIV: commanded voltage vs log `|Imeas|`, acquisition order preserved, one color per cycle, PF solid / PB dashed / NF dotted / NB dash-dot, cycle colorbar, and contrast-vs-cycle panel.
- Forming and conditioning: separate panels with connected native traces and sweep-order colorbars.
- Verify plot legibility before delivery.
