# House style

How every tool in this suite is built. Follow it exactly — the look is
consistent on purpose, and most of these rules exist because something
looked wrong and got fixed.

## What a tool is

One self-contained HTML file in `tools/`. No build step, no dependencies, no
external requests. Open the file and it works.

Add a card for it in `index.html` with a topic tag (Geolocation, Antennas,
Propagation).

## Layout

```css
body { max-width: 760px; margin: 0 auto; padding: 2rem 1rem 4rem;
       line-height: 1.5; font-weight: 600; }
```

- **Controls go above the canvas. Never in a side rail.** This was tried and
  rejected.
- Back link first, then `h1`, then a one-paragraph `.sub` saying what the tool
  is for.
- Then controls, then numbered sections.
- Sections are `1 · Title` followed by a caption. The colon after the title
  comes from `.sec b::after { content: ':' }`, not from a hand-typed dash — a
  literal em dash left a 14 px gap.
- Readout cards last.
- Everything must fit 390 px wide as well as 760. Canvases reduce their own
  detail when narrow rather than overprinting.

## Type

- Body weight is **600**, not 400. The regular weight has to look thick.
- Bold is **700**. Nothing between exists: the font is static, so 450 and 500
  silently snap to 400. Measured, not assumed.
- `h1` 22px/700 · `.sub` 14.5px · `.sec` 14px · `.sec span` 13.5px/600
- `.card .hd` 13.5px · `.card .big` 19–24px/700 tabular-nums · `.card .ft` 13px
- **Sentence case with a capital first letter on every visible string.** That
  includes canvas labels, card values and fallbacks: `None`, `All round`,
  `No 3 dB point` — never lowercase. This has been got wrong repeatedly.

## Colour

CSS custom properties, light and dark, driven by both
`prefers-color-scheme` and `[data-theme]`.

**One Microsoft Office palette per tool, never mixed.** In use so far:

| Tool | Palette |
|---|---|
| phase-interferometry, antenna-pattern | Office |
| aoa-triangulation | Office 2007–2010 |
| tdoa | Median |
| phased-array | Paper |
| link-budget | Marquee |
| propagation | Slipstream |

The emitter is Office red `#C0504D` in every geolocation tool.

Where colour can carry information, make it: in `propagation` the band bar is
coloured by propagation mode, so it matches the legend of the diagram below it
instead of being decoration.

## Canvas drawing spec

Every tool obeys the same scale. Thickness means something: the heavier the
line, the more it is data rather than furniture.

| Element | Width |
|---|---|
| Grid | 0.5 |
| Frame, axis | 1.0 |
| Annotation, scale bar | 1.2 |
| Dashed ray, cursor | 1.4 |
| Data series | 1.8 |

- Tick labels `fnt(12)`, axis titles `fnt(13)`.
- Every tick label sits **10 px clear** of its axis.
- Markers: 5.5 for sites and elements, 6 for the emitter or the selected one.
- `fnt()` carries the 600 weight: `'600 ' + s + 'px ' + var(--font-sans)`.
- `fit()` handles devicePixelRatio; call it at the top of every draw function.
- A readout that would collide with the thing it labels goes to a **corner** of
  the plot instead, right-aligned at `w - r - 4`.

## Drawing the thing itself

A chart is not a visualisation. If the tool is about a physical object, draw
the object.

- **Conductors are filled bars with squared tip caps**, not strokes. Stroked
  lines read as tally marks.
- **Dimensions in wavelengths**, with arrowheads and short witness stubs, the
  label rotated when the dimension line is vertical so it costs no width.
- **Auto-fit**: measure the drawing's bounding box on a first pass, then set the
  scale to fill the canvas whichever way round it is, and draw again. Do not
  scale off `min(w, h)` — a wide canvas goes unused.
- **The span must follow the subject.** A line-of-sight hop is tens of km and a
  sky-wave hop is thousands; a fixed span leaves one of them a pixel wide.
- **Place labels against measured text width**, never a guessed offset. Most
  clipping bugs came from a hardcoded margin.
- Exaggerate where you must (earth curvature, antenna height) and say so on the
  drawing.

## Honesty

- Check every number against a published value before claiming the tool works.
  Dipole 2.15 dBi / 78°, dish 23.9 dBi at 5 λ, free-space loss 100 dB at 1 km
  and 2.4 GHz, thermal floor −108 dBm in 1 MHz at 6 dB NF.
- Say which figures are exact and which are indicative. Ground-wave range
  depends on soil; sky wave depends on the hour and the sunspot number.
- **A clamped trace can state a falsehood.** A ground-wave curve pinned to the
  axis floor read as "still reaches 1 km at 100 GHz". Stop the trace instead.

## Building

- **Hand-build one tool at a time.** Mass production by agents produced 28
  unusable files. State the plan before writing code.
- **Verify by screenshot, and look at it.** Headless Chrome, then read the PNG:

  ```bash
  "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new \
    --disable-gpu --hide-scrollbars --virtual-time-budget=6000 \
    --window-size=900,1500 --screenshot="out.png" "http://localhost:8940/tools/x.html"
  ```

  Measurements alone miss collisions. Parsing cleanly proves nothing.
- To script a tool's controls, load it in an iframe from a probe page in the
  repo root and dispatch `input` events — headless Chrome cannot click.
- For phone width use a **390 px iframe**, not `--window-size=390`: headless
  Chrome ignores `width=device-width` that way and will falsely report overflow.
