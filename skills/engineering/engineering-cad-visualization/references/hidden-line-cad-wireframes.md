# Clean hidden-line CAD wireframes

Use this pattern for publication figures or comparison sheets built from STL/STEP mechanical models, especially when the user rejects shaded solids or visible triangle meshes.

## Preferred visual style

- Use a **hidden-line technical wireframe**: visible CAD feature edges over a nearly white opaque body.
- Suppress raw STL triangle edges. A literal `style="wireframe"` usually exposes every tessellation triangle and looks like a mesh, not a clean engineering drawing.
- Use a white background, dark high-contrast feature lines, anti-aliasing, and generous crop margins.
- Mark the installed/current variant clearly; distinguish alternatives and topology-review parts without implying they are installed.

## Validated PyVista pattern

```python
import pyvista as pv

mesh = pv.read(path).clean()
edges = mesh.extract_feature_edges(
    boundary_edges=True,
    non_manifold_edges=True,
    feature_edges=True,
    manifold_edges=False,
    feature_angle=28,
)

p = pv.Plotter(off_screen=True, window_size=(1200, 900))
# Opaque pale body provides hidden-line removal.
p.add_mesh(
    mesh,
    color="#f7fbfd",
    opacity=1,
    smooth_shading=True,
    show_edges=False,
    ambient=0.90,
    diffuse=0.12,
    specular=0,
)
p.add_mesh(
    edges,
    color="#183b56",
    line_width=2.0,
    render_lines_as_tubes=True,
)
p.set_background("white")
p.view_isometric()       # or view_xy/view_xz when geometry demands it
p.camera.zoom(1.1)
p.enable_anti_aliasing("ssaa")
image = p.screenshot(return_img=True)
p.close()
```

The opaque body is essential: it occludes feature lines on hidden surfaces while retaining a wireframe-like technical appearance.

## Multi-variant contact sheets

1. Inventory every candidate programmatically before rendering.
2. Group same-stem STL/STEP/SolidWorks files as one design family; select one neutral/mesh export for the render.
3. Render one image per distinct geometry and verify the count against the inventory.
4. Add source filename, dimensions, and status (`INSTALLED`, `alternative`, `component`, `topology review`) to every panel.
5. Add a dedicated inventory panel for native-CAD-only variants that have no STEP/STL export.
6. Exclude temporary lock files such as `~$*.SLDPRT`.
7. State that native SolidWorks-only files require a real SolidWorks/eDrawings export; do not fabricate a render from filenames.

## Verification gates

- Inspect the full contact sheet and representative individual renders.
- Confirm no object or label is clipped.
- Confirm no dense tessellation triangles are visible.
- Confirm the installed/current variant is the one marked as installed.
- Programmatically verify rendered count plus source-only count equals the complete inventoried design-family count.
- Preserve topology warnings separately from visual rendering quality: a clean render does not prove a watertight printable mesh.

## Installed-model correction propagation

When the user corrects which model is physically installed, update all of these in one pass:

- Paper prose and captions
- Figure panel and photograph annotation
- BOM model identity
- Curated STL/STEP/native-CAD release contents
- README, audit report, and checksum manifest
- Comparison-sheet installed/alternative status

Then compile the paper, inspect affected pages, rebuild the archive, test ZIP integrity, and assert programmatically that the superseded model name is absent from the installed release.
