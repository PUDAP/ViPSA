# Exact user-edited SVG integration and manuscript cleanup

## Source fidelity

When the author provides edited figure files and says to use them, treat those files as authoritative. Do not redraw, reflow, relabel, or otherwise improve them unless explicitly asked.

1. Inspect ZIP paths for traversal before extraction.
2. Validate SVG XML and record dimensions/viewBox.
3. Copy the exact SVG bytes into the manuscript source directory.
4. Render a PNG only as a preview/LaTeX compatibility derivative; retain the SVG as the editable source.
5. Verify byte equality between the extracted authoritative SVG and manuscript copy.
6. Point LaTeX to the derivative PNG while naming the user-edited SVG in the release bundle.
7. If a wide exact figure is illegible in portrait, place the unchanged figure on a landscape page rather than redesigning it.
8. Compile, locate captions by PDF text extraction, render affected pages, and inspect page-scale legibility/clipping.

SVG attachments may not preview in chat even when valid. Deliver the PNG preview and optionally a ZIP containing SVG+PNG rather than calling the SVG corrupt.

## Removing unfinished-work language

When an author requests removal of text describing what remains:

- scan for `TODO`, placeholders, `future work`, `pending`, `not yet`, `incomplete`, `remains required`, repository/DOI placeholders, author placeholders, and acknowledgement placeholders;
- remove task-list and promise language rather than fabricating missing values;
- convert genuine evidence gaps into present-tense scope statements (for example, `no holder-wide success rate is claimed`);
- replace incomplete cost promises with a defensible statement that no total cost is claimed when reused/custom hardware prevents one;
- remove empty sections after deleting placeholders;
- rescan source programmatically and verify zero matches before compiling.

## Calibration insertion pattern

Replace manuscript placeholders such as `the electrical path should be tested` with measured methods/results only after actual integrated calibration. Include:

- matrix-open and routed-open baselines;
- short-path result;
- reference-resistor table;
- open-conductance correction at high resistance;
- closure acceptance and preserved excluded trials;
- cleanup state;
- distinction between functional integrated validation and accredited traceability.
