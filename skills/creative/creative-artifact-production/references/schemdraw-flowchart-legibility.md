# Schemdraw Flowcharts: Legibility and Export Pattern

Use this reference when creating workflow/decision flowcharts with Python `schemdraw`, especially when the source content has many gates, side paths, or long labels.

## Durable workflow

1. Generate a real artifact script, not just an image by hand. Keep the source script next to the rendered outputs.
2. Render SVG first with `schemdraw.Drawing(file=...)`; SVG preserves text/editability and is the source of truth.
3. Convert SVG to PNG for chat delivery when needed. If available, use `cairosvg.svg2png(...)`; otherwise deliver the SVG and explain that PNG export was skipped.
4. Verify the PNG visually before final delivery. Look specifically for:
   - text overflow outside shapes
   - cropped labels at canvas edges
   - crossing arrows that obscure labels
   - too-small font from trying to fit too much prose
   - black/transparent background surprises in chat previews
5. Deliver both paths when useful: PNG for viewing, SVG for editing/reuse, plus the script path.

## Layout lessons

- For dense technical workflows, a **single-column vertical flow** with explicit “gate action” boxes is often more readable than a traditional branched flowchart.
- Do not put long paragraphs inside diamond decision shapes. Use short question diamonds (`CONTACT RESULT?`, `MORE DEVICES?`) followed by rectangular action boxes that spell out the outcomes.
- Avoid long side-branch arrows when labels are verbose; they easily cross the main flow and make the chart unreadable. If branches are semantically important but visually crowded, summarize them in the next action box.
- Use light fills and a white PNG background for Telegram/readability. Dark title bars are fine, but avoid black page backgrounds unless explicitly requested.
- Prefer ASCII-safe symbols in diagram text if the rendering path may not have full emoji/math glyph support. Replace arrows like `→` with `to` when glyphs render as boxes.

## Minimal export skeleton

```python
import schemdraw
import schemdraw.flow as flow

OUT_SVG = 'workflow.svg'
OUT_PNG = 'workflow.png'

with schemdraw.Drawing(file=OUT_SVG, show=False) as d:
    d.config(unit=1.0, fontsize=8)
    start = flow.Terminal(w=10, h=1.2).label('START')
    d += start
    step = flow.Process(w=10, h=1.3).label('DO WORK')
    d += flow.Arrow().at(start.S).to(step.N)
    d += step

try:
    import cairosvg
    cairosvg.svg2png(url=OUT_SVG, write_to=OUT_PNG, output_width=1800, background_color='white')
except Exception as e:
    print('PNG conversion skipped:', e)
```

## When summarizing a scientific/engineering workflow

For workflows reconstructed from prior runs, distinguish:

- the operational sequence (`cleanup -> move -> align -> approach`)
- the decision gates (`contact?`, `safe to stress?`, `DCIV outcome?`)
- the data/artifact outputs (`CSV`, `summary.json`, plots)
- the adaptive rule (`only change protocol at safe DONE boundaries`)

This makes the chart useful as a reusable procedure rather than a one-off session narrative.
