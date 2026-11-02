# Electrical-fidelity-preserving speedups and contact-Z surface plotting (2026-06-23)

Context: After a long 8×8 ViPSA grid continuation, the user asked how to speed future runs up, then explicitly corrected the optimization target: **do not compromise anything on the electrical side**. Preserve DCIV resolution, reset-pre logic, compliance logging, voltage set, repeats, and full randomized pulse measurements unless the user explicitly asks otherwise.

## Durable workflow correction

When asked to speed up a grid run and the electrical protocol is scientifically important, optimize only the non-electrical parts unless the user explicitly authorizes electrical simplification.

Do **not** propose as defaults:

- fewer DCIV points / coarser DCIV steps
- fewer pulse trials or SET voltages
- lower repeat count
- skipping reset-pre sweeps that are part of the current protocol
- skipping compliance-heavy devices solely to save time
- early-stopping electrical measurements
- reduced electrical logging

Instead, separate the run into two layers:

1. **Layer 1: find/contact/position the device quickly and safely**
2. **Layer 2: run the fixed electrical protocol unchanged**

## Non-electrical bottlenecks observed

Measured from the prior continuation summary:

- Wall time about 7.7 h for 53 completed devices.
- Mean per device about 8.7 min; median about 7.4 min.
- Slowest cases were mostly approach/search dominated, especially no-contact-after-max devices.
- Non-electrical overhead sources:
  - long 0.25-step contact approach loops from far above contact
  - full vision alignment on every device
  - conservative safe retract / partial relower before every X/Y travel
  - repeated route/output cleanup commands inside stable phases
  - per-device plotting/reporting blocking the measurement loop
  - video capture/encoding if not decoupled from PUDA command execution

## Preferred speedup tactics when electrical fidelity is fixed

- **Adaptive mechanical approach, same final electrical criterion**
  - Keep the target contact window and Keithley safety reads unchanged.
  - Use larger Z steps only while clearly open/noise-floor, then switch to 0.25-step fine approach near contact.
  - Example policy: far open -> +1 or +2 steps; intermediate -> +0.5; near target -> +0.25.

- **Predictive contact-Z pre-approach**
  - Record final contact Z, row/column, net approach steps, and final contact current.
  - Use previous device / row median contact Z to lower closer to expected contact height while preserving a safety margin.
  - Still run the same low-bias contact check before any electrical stress.

- **Adaptive vision alignment**
  - Full align first device of each row, after row transitions, after failed/weak contact, after large correction, or when low-bias contact check is abnormal.
  - Otherwise use grid-predicted X/Y and let the electrical contact check decide whether alignment is needed.

- **Stateful cleanup**
  - Keep strict cleanup before X/Y travel, after each device, on exceptions, before switching SMUs, and before COMPLETE.
  - Avoid redundant route/output commands only when software state says the route/output state is already correct.

- **Async plotting/reporting**
  - Measurement loop writes raw artifacts and `DONE.json` then immediately proceeds.
  - Separate watcher/poller generates and sends plots so plotting does not block the next device.

- **Decoupled recording**
  - Start video recording once; run it in a separate thread/process.
  - Recording should drop frames rather than block PUDA measurement commands.

## Contact Z-height surface plot pattern

To visualize whether predictive contact-Z is feasible, plot final contact stage-Z versus Zaber X/Y from per-device `summary.json` files:

- X/Y source: `summary.target.x`, `summary.target.y` in native Zaber units.
- Contact Z source: `summary.approach.stage_position.result[2]`.
- If `open_weak_override.stage_position_after_plus1.result[2]` exists, use that as the final Z actually used for subsequent electrical measurements.
- Save a CSV with device, row, col, X, Y, contact Z, adjusted/final Z, approach status, and final contact current.
- Generate both:
  - 3D triangulated surface (`plot_trisurf`) labeled by device number.
  - Top-down contour (`tricontourf`) labeled by device number.

This plot supports mechanical speedup decisions without changing the electrical protocol.
