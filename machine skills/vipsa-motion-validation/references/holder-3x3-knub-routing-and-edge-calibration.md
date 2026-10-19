# 3×3 holder geometry, knub-safe traversal, and edge calibration

## Installed physical frame

For the installed `multi_holder_regular`, do not assume CAD-local axes match the machine/holder convention. The physical frame used by the operator is the CAD frame rotated 90° anticlockwise:

```text
X_physical = -Y_CAD
Y_physical =  X_CAD
```

The longer holder edge is physical X. Slot numbering is row-major in the operator view: Slot 1 is top-left and Slot 9 is bottom-right.

The model has twelve knub positions. Copper tape used for bottom contact can protrude at substrate corners; do not classify such a protrusion as a substrate or holder edge.

## Route planning is sequence-dependent

Do not freeze one universal S1→S9 route. Generate the route from the requested measurement order.

For every candidate route:

1. Use the installed physical coordinate transform, not CAD-local labels.
2. Model all twelve installed knubs as obstacles and inflate them by an explicit XY safety margin.
3. Retract before lateral motion.
4. Prefer orthogonal segments through known inter-row/inter-column transfer lanes.
5. Prohibit diagonal shortcuts unless their complete swept envelope is collision-checked.
6. Validate the actual probe/shank envelope in a dry run; a top-view tip-only path is insufficient proof of clearance.

The supplied knub STEP has an approximately 10 mm × 8 mm footprint in the corrected physical frame. A 2 mm per-side inflated keep-out left 5 mm minimum clearance on the validated example route, but this margin must be recomputed for any new sequence.

## Holder-edge calibration workflow

When the operator manually aligns one edge approximately:

1. Wait for the explicit “aligned” handoff.
2. Record exact Zaber X/Y and OpenFlexure Z before any move.
3. Verify the probe/sample is retracted, Keithley output is off, and the 707B is open.
4. Capture Camera 1 at the aligned edge and Camera 2 for layout context.
5. Camera 2 holder-layout frames may be more informative with illumination off; after capture, restore and verify the user-requested final light state.
6. Move toward the requested edge in bounded increments and capture a fresh frame after every increment.
7. Use coarse-to-fine refinement: coarse overlapping scan to bracket the edge, then smaller steps to select the reference.
8. Treat copper-tape protrusions separately from the structural edge.
9. Preserve the full signed move history, exact readbacks, edge bracket, chosen reference, and images.
10. Stitch or montage overlapping Camera 1 frames as a broad stage-coordinate view, but label it honestly if it is not a photogrammetrically seamless reconstruction.

## Critical pitfall: midpoint assumptions

Approximate alignment of a right/left edge does **not** establish that the current point is the midpoint of that edge. Never jump by half the CAD span to infer top or bottom. This can overshoot substantially.

Instead, follow the operator’s sign instruction and scan until a fresh image visibly brackets the structural edge. If the image is too defocused to distinguish structure from tape, use a light-off Camera 2 overview and ask for/accept operator confirmation rather than inventing an edge coordinate.

## Current reach limitation

At Zaber X = 0, a small strip along the holder’s physical left side is inaccessible. Its width is not yet calibrated. Mark it as schematic/un-calibrated in diagrams; do not assign a numerical dead-zone width until the dedicated calibration is completed.
