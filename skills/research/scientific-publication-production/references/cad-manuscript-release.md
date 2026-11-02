# CAD-heavy apparatus manuscript release pattern

This reference records a validated pattern for revising an apparatus paper whose source bundle includes CAD, printable meshes, a draft BOM, figures, and a strict upload-size limit.

## Correction batching

When the author says corrections will be supplied one at a time:

1. Keep a correction ledger without touching the manuscript.
2. Answer conceptual questions provisionally while preserving the wait state.
3. After explicit authorization, patch the manuscript, figure generator, BOM generator, workbook, README, and bundle in one coordinated pass.
4. Search the final source for every superseded term and claim.

This avoids inconsistent intermediate states such as corrected prose with stale tables or regenerated figures omitted from the archive.

## Smooth solid-object rendering

A triangle mesh may be the available geometry, while the paper needs a CAD-like solid presentation. Render it without triangle edges and keep topology validation separate.

```python
import pyvista as pv

plotter = pv.Plotter(off_screen=True, window_size=(1200, 900))
model = pv.read("part.STL")
plotter.add_mesh(
    model,
    color="#8db6d1",
    smooth_shading=True,
    show_edges=False,
    pbr=True,
    metallic=0.04,
    roughness=0.58,
)
plotter.set_background("white")
plotter.view_isometric()       # or view_xy() for a holder top view
plotter.camera.zoom(1.25)
plotter.enable_anti_aliasing("ssaa")
image = plotter.screenshot(return_img=True)
plotter.close()
```

Quality gates:

- no visible triangle-edge network;
- holes, recesses, and modified regions remain legible;
- neutral lighting does not hide geometry;
- object fills its panel without clipping;
- labels remain readable at compiled-page scale;
- caption says parts use independent visual scales when applicable.

Do not describe the geometry as watertight because it looks solid. Validate STL topology independently (parse, dimensions, watertightness, winding consistency, degenerate triangles) and retain the report.

## Using old presentations safely

A development presentation can be useful for:

- hierarchy and exploded-layout concepts;
- camera angle and composition;
- part names that need verification;
- identifying which subsystem needs a dedicated figure.

It is not automatically reliable evidence for:

- installed revision identity;
- model numbers;
- calibrated resolution or accuracy;
- speed limits;
- costs; or
- current holder geometry.

Use the composition while redrawing labels and replacing obsolete geometry. Do not include the original deck in a public bundle if it contains stale claims that could be mistaken for current specifications.

## Unknown camera plus reused optics

For an installed camera whose exact model is unresolved:

- describe it as a USB digital microscope or other confirmed generic class;
- state that the make/model is unconfirmed;
- list a possible vendor model only as a candidate;
- do not import the candidate's sensor size, pixel pitch, frame rate, or optical magnification;
- report the measured stream resolution, object-plane sampling, and field of view instead; and
- identify reused optics by system provenance when individual lens models are unknown.

If working distance changes with substrate thickness and refocusing, explain that dependency and omit a fixed table value.

## Performance-matched minimum optics

A minimum optical configuration should match assembled performance, not brand or nominal megapixels. Specify an acceptance target such as:

- object-plane sampling in micrometres per pixel;
- field of view at a stated stream resolution;
- visible probe-tip and pad contrast;
- rigid mounting;
- clearance across the expected substrate-thickness range;
- controllable exposure; and
- reliable programmatic acquisition.

Require a calibration-scale image after assembly to verify the target.

## Draft BOM language

Use all of the following when many prices are unresolved:

- workbook title includes `Draft`;
- blank price cells mean unresolved, not zero;
- price basis and source URL are explicit;
- currency conversion is not invented;
- reused/custom/model-unspecified items stay outside claimed totals;
- manuscript cost rows say `Pricing incomplete; see draft BOM`; and
- no partial subtotal is presented as the full or minimum configuration cost.

Internal formula subtotals may remain useful if the workbook note says they cover only rows explicitly marked for inclusion and must not be cited as system costs.

## Release verification

A reliable bundle builder should derive figure filenames from `\\includegraphics`, copy the freshly compiled PDF rather than a stale build directory, include the bibliography explicitly, and fail on missing files.

Before delivery, verify:

1. clean compilation succeeded;
2. affected and continuation pages were rendered and visually reviewed;
3. stale hardware names and superseded cost claims have zero matches in the authoritative source;
4. workbook sheets were rendered and checked;
5. archive CRC test passed;
6. expected corrected phrases are present inside the archive;
7. forbidden stale phrases are absent;
8. text credential/connection-string scan passed; and
9. archive byte size is below the strict upload limit.
