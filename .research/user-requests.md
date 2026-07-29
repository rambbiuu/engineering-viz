# Standing user requests — must be honoured by any agent touching these files

These come directly from the repository owner. They override conflicting guidance elsewhere.

## Every tool — naming and consistency sweep (owner, 2026-07-29)

Catch and fix the small stale-naming bugs:

- No hardcoded count in a name or copy when that count is adjustable. "4-antenna phase
  interferometry" is stale — make the interferometer's element count configurable
  (2–6 antennas, unequal spacings editable as now, default the current 4) and rename the
  tool "Phase interferometry". Same rule everywhere: if a tool lets you pick N, nothing on
  the page or in any other page's link text may claim a fixed N.
- One term per concept across the whole suite: "site" (not station/mast/receiver site
  mixed), "emitter" (not target/transmitter mixed, except where transmitter is the
  physically correct word), "element" for array antennas, "geolocation" never "DF".
- Every page's <title>, its h1, and every card/link that points at it must use the same
  name. Cross-references in prose ("your 4-antenna interferometer", "your 2–18 GHz…")
  must be checked against what the linked tool actually is now.
- Filenames stay as they are (links depend on them); only display names change.

## Every tool — fill all aspect ratios + typography hygiene (owner, 2026-07-29)

No fixed narrow column: page width min(1500px, 94vw); canvases sized with CSS
aspect-ratio (not fixed px heights) so laptop, ultrawide and phone all fill naturally;
wide screens get a controls rail beside the canvas or side-by-side canvas pairs, phones
stack. No horizontal scroll at any width. AND: iron out the basics — sentence case
everywhere (no stray caps), formulas typeset properly (real sub/superscripts, italic
variables, true minus −, ·, Greek glyphs, units with a space). Details in STYLE.md
"Fill the screen" and "Typography hygiene".

## Every tool — instrument look, bigger, customisable (owner, 2026-07-29)

The diagrams must not look like cartoons. Professional = MATLAB-figure / oscilloscope
aesthetic per the INSTRUMENT LOOK section of STYLE.md: graticule grids with labelled ticks
and units, thin precise strokes, dimensioned technical drawings instead of cute scenes,
980px page width, primary canvas ≥420px tall, slider+number-input pairs, real-world preset
buttons, one large hero readout with a state badge. Explanations stay short — the page
must be understandable at one look from title + hero number + annotated plot.

## aoa-triangulation.html — add a graph section

Below the map, add a numbered graph section: **fix error vs range**. X axis: distance from
the site network, 0 to ~12 km. Y axis: position uncertainty in metres. One curve per current
bearing-accuracy setting (cross-range error ≈ 2·R·tan(σ_bearing)), redrawn live when the
accuracy slider moves. Mark the current emitter's actual range and its uncertainty with a
dot and leader label so the map and the graph visibly agree. Lesson the graph must carry:
an angle error is a *distance* error that grows linearly with range — double the range,
double the miss.

## tdoa.html — add a graph section

Below the map, add a numbered graph section: **timing error becomes position error**.
X axis: clock/timestamp error between sites, 0 to 3 µs. Y axis: position error in metres
(c·Δt, so ~300 m per µs). Straight line with the axis labelled in both µs and the
equivalent km. Mark 1 µs → ~300 m with a leader label. Optionally a second marked point at
10 ns → 3 m (GPS-class sync). Lesson: TDoA trades the AoA family's phase-calibration
problem for a clock-synchronisation problem, and this line is the exchange rate.

## Every tool — minimum wording (owner's rule, 2026-07-29)

"It's a visualisation tool, so minimum words." Always-visible prose is capped by the WORD
BUDGET section of STYLE.md: 2-sentence intro, ≤10-word section explainers, swatch+≤6-word
legend lines, ≤14-word tour narration. Glossaries, worked examples and any longer
explanation are collapsed inside `<details>`. Definitions appear on tap/hover, not inline.
Tools already built with heavy prose (e.g. sampling-aliasing.html) must be trimmed to this
budget during remediation — cut the words, keep the mechanisms.

## Both tools

- The graph updates live with the relevant slider; it is not a static illustration.
- Follow the house style: numbered `.sec` heading, canvas, "what am I looking at" bullets
  beneath (per the beginner scaffolding in STYLE.md).
- Terminology: the suite says "geolocation", not "DF" / "direction finding" — the owner
  asked for this wording explicitly.
- Site/receiver count stays selectable on the AoA tool (2–5 sites, draggable); do not
  regress that.
