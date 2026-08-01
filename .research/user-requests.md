# Standing user requests — must be honoured by any agent touching these files

These come directly from the repository owner. They override conflicting guidance elsewhere.

## Every tool — NO SIDE RAIL, single column (owner, 2026-07-29)

"I don't like how you set control to one side and the simulation to the other, totally not
a fan — the previous layout is better." Controls go ABOVE the canvas, full width, always.
The canvas spans the full column below them. Fill a wide screen by letting control blocks
flow into 3–4 columns horizontally (`.rail` = auto-fit minmax(250px, 1fr)), never by
putting them in a sidebar. Container `min(1180px, 94vw)`. Already applied to the 14
restyled tools; any tool restyled later must follow the same shape.

## Every tool — nothing may spill out of its box (owner, 2026-07-29)

"Make sure the words don't spill out of the box, proper spacing and aspect." See the
NO OVERFLOW section of STYLE.md for the required mechanics: measure canvas text with
fitText/clampX before drawing, ≥10px padding inside every canvas box, thin out colliding
tick labels instead of overlapping or shrinking below 12px, flip leader labels near edges;
in HTML use border-box, min-width:0 on every flex/grid child, overflow-wrap:anywhere,
tabular-nums on values, no fixed widths. Run the overflow console check and screenshot at
375 and 1920 before reporting done — a label crossing a border is a defect, not a nitpick.

## Every tool — minimal marks, on canvas AND in navigation (owner, 2026-07-29)

Read `.research/icons.md` (same folder as this file) — mandatory. It covers TWO things:
1. The seven category glyphs used on the hub and category pages (nowhere else).
2. **Canvas hardware marks** — the masts, dishes, handsets and obstacles drawn inside the
   tools. These are what the owner meant by "looks like cartoon". Single thin stroke, no
   fills, geometric and orthographic like a datasheet figure, hardware in text colour with
   only the signal in a series colour, real dimensions labelled with dimension arrows, and
   absolutely no people, vehicles, buildings-with-windows or cute scale props. Follow the
   standard vocabulary table so a mast looks identical in every tool that draws one.

## Every tool — MAXIMUM CUSTOMISATION, MINIMUM WORDS (owner, 2026-07-29, repeated twice)

The owner has now said this twice. Treat it as the highest-priority rule in this file.
"It's a visualisation tool — I want maximum customisation to play with. So far pretty
decent but more will be better." And again: "less wordy."

**More knobs.** Every physical quantity in a tool's model must be adjustable. If the code
contains a hardcoded constant that a real engineer would vary, promote it to a control.
Target 8–14 controls per tool, arranged as: 3–4 primary controls always visible, the rest
inside the collapsed advanced `<details>`. Each control is a range PLUS a number input for
exact entry. Add 3–5 preset buttons naming real cases ("FM broadcast", "GSM 900",
"Wi-Fi 2.4 GHz", "Ka-band satellite") that set several controls at once.

Also make things DRAGGABLE and CLICKABLE on the canvas wherever it makes physical sense —
drag a site, an obstacle, an emitter, a marker — because direct manipulation teaches faster
than a slider. Add a reset control. Where a comparison helps, add a "hold current as
reference" ghost trace so the user can see what changed.

Examples of constants that must become controls: path-loss exponent, antenna heights,
noise figure and gain per stage, temperature, bandwidth, symbol rate, roll-off factor,
number of elements, element spacing, taper level, cluster size, sector count, blocking
target, code length, delay-spread taps, rain rate, k-factor, ionospheric critical
frequency, clock error, bearing accuracy, modulation index, deviation, tone frequency.

**Fewer words.** Enforce the WORD BUDGET in STYLE.md ruthlessly. The controls and the plot
carry the teaching; prose is a fallback, not the medium. If a sentence explains what a
label already says, delete the sentence. No paragraph anywhere outside a collapsed
`<details>` except the 2-sentence intro.

## Every tool — bigger, higher-contrast text (owner, 2026-07-29)

"Make the text bigger, and not grey — white or black." Apply the TEXT LEGIBILITY table in
STYLE.md at token level: 16px body, 28px h1, 14.5px controls, 26px card values, 14px
legends, canvas text never below 12px and scaling with canvas width. Text colours go
near-black on light / near-white on dark; --text-muted is reserved for incidental captions
and must never carry a number or a name. Font family stays the system stack (already Segoe
UI Variable on Windows) but declared explicitly everywhere.

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
