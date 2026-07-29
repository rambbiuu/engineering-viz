# Standing user requests — must be honoured by any agent touching these files

These come directly from the repository owner. They override conflicting guidance elsewhere.

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
