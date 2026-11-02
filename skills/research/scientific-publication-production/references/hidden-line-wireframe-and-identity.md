# Hidden-line CAD wireframes and installed-model corrections

Use this reference when an apparatus manuscript includes STL/STEP/native CAD and the author wants clean technical wireframes or corrects which model is actually installed.

## Distinguish the requested render styles

- **Triangle mesh:** shows STL tessellation; usually too visually dense for a paper.
- **Smooth solid:** shaded surface with mesh edges suppressed.
- **Hidden-line wireframe:** pale opaque body plus only visible CAD feature edges. This is the preferred technical-line style when smooth solids look too soft but triangle meshes are cluttered.

If the author asks to see the render first, deliver the standalone preview and wait for approval before compiling the manuscript or rebuilding the bundle.

## Validated PyVista hidden-line pattern

```python
import pyvista as pv

model = pv.read("part.STL").clean()
edges = model.extract_feature_edges(
    boundary_edges=True,
    non_manifold_edges=True,
    feature_edges=True,
    manifold_edges=False,
    feature_angle=28,
)
plotter = pv.Plotter(off_screen=True, window_size=(1200, 900))
# Opaque pale geometry performs hidden-line removal.
plotter.add_mesh(
    model,
    color="#f7fbfd",
    opacity=1,
    smooth_shading=True,
    show_edges=False,
    ambient=0.90,
    diffuse=0.12,
    specular=0,
)
plotter.add_mesh(
    edges,
    color="#183b56",
    line_width=2.0,
    render_lines_as_tubes=True,
)
plotter.set_background("white")
plotter.view_isometric()       # view_xy() for a plate; view_xz() for a clip
plotter.camera.zoom(1.1)
plotter.enable_anti_aliasing("ssaa")
image = plotter.screenshot(return_img=True)
plotter.close()
```

Do **not** use raw `style="wireframe"` for STL publication art: it exposes every triangle edge. Crop with a generous white margin, inspect every panel for clipping, and compile-review the final page at manuscript scale.

## Comparing all holder/model variants

For an “all available models” request:

1. Inventory every STL, STEP, and native-only file family.
2. Render one representative per distinct geometry with consistent camera/style.
3. Convert STEP to temporary STL only for rendering; retain the STEP as authoritative.
4. Clearly label `INSTALLED`, `alternative`, `component`, and `topology review`.
5. List native-only variants that cannot be rendered without proprietary export instead of silently omitting them.
6. Exclude temporary lock files.
7. Verify the enumerated render count against the inventory and package individual renders plus contact sheets and a CSV/JSON index.

## Correcting installed-model identity

The latest explicit author identification supersedes earlier photo inference. Propagate it to:

- manuscript prose, subsection title, captions, and availability statement;
- annotated installed-system photograph;
- figure generator and rendered panels;
- BOM generator and regenerated workbook;
- model audit and comparison-sheet status;
- curated installed STEP/STL/native source files;
- release README, validation report, manifest, and checksums; and
- compiled PDF and archive.

Verify both directions: the corrected identifier is present in the paper and all expected installed formats, while the superseded identifier is absent from the paper and curated installed-file set. It may remain only where explicitly labelled as an alternative.
