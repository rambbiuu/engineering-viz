# Handoff — continuing this project in any AI assistant

Everything needed to continue is in this repository. No conversation history is required.
This file is the entry point: read it, then read the four spec files it points at.

## What this is

A suite of 28 single-file interactive RF and wireless-communications visualisation tools,
plus a hub and 7 category pages. Each tool is one self-contained `.html` — no build step,
no dependencies, no external requests. Open it in a browser and it works.

Live: https://rambbiuu.github.io/engineering-viz/

## Read these first, in this order

| File | What it is |
|---|---|
| `.research/user-requests.md` | **The owner's standing orders. Highest authority. Overrides everything else.** |
| `.research/STYLE.md` | The full design contract: instrument look, responsive layout, word budget, text sizes and colours, no-overflow mechanics, palette |
| `.research/kit.md` | The shared "instrument kit" — copy-paste CSS block and canvas helper functions every tool uses |
| `.research/icons.md` | The 7 navigation glyphs, and the canvas hardware drawing vocabulary (masts, dishes, handsets) |

Reference material with validated formulas and citations, for when you touch the physics:
`.research/propagation.md`, `link-noise.md`, `signals.md`, `cellular.md`, `antennas.md`.
These were extracted from the owner's course notes (IE4155 / EE4155 / EE3012) and public
ITU-R recommendations. Do not contradict them without checking.

## The owner's rules, in one paragraph

Minimum words — it is a visualisation tool, the plot and the controls teach, prose is a
fallback. Maximum customisation — every physical constant should be a control, 8–14 per
tool, 3–4 visible and the rest collapsed, each a slider plus a number box, with real-world
preset buttons. Professional instrument look, not cartoons — gridded axes with ticks and
units, thin strokes, technical drawings. Big high-contrast text, never grey. Fill every
screen size, no dead margins on a laptop, no horizontal scroll on a phone. Nothing spills
out of its box. Sentence case, typeset formulas.

## Current state, as of commit 3cdfaf2

**Restyled to the kit (14):** am-dsbsc-ssb, antenna-basics, aoa-triangulation, ber-vs-ebn0,
cdma-spreading, cellular-reuse, epicycles, erlang-trunking, eye-diagram-isi,
fm-bessel-spectrum, fourier-series, fresnel-clearance, handover-power-control,
impedance-matching.

**Still on the old style (14):** iq-constellation, link-budget, modulation, multipath-fading,
multiple-access, noise-figure-sensitivity, ofdm-subcarriers, phase-interferometry,
phased-array, polarisation-mismatch, radio-propagation, sampling-aliasing, superhet-image,
tdoa.

To tell them apart: a restyled file contains `--plot-bg` and `class="wrap"`.

## Outstanding work, in priority order

1. **Restyle the remaining 14 tools** to `.research/kit.md`. This is the bulk of the work and
   it is mechanical now that the kit exists: replace the `<style>` block, move to the
   `.wrap` grid layout, swap fixed canvas heights for `.cv-hero` / `.cv-sub`, redraw plots
   through `graticule()`, add the hero readout, add number inputs and presets, apply the
   typography rules.
2. **Early-file consistency sweep.** Tools restyled before the text ruling landed (notably
   `fourier-series.html`) still use 15px body text and the older grey `--text-secondary:
   #55606c`. Every tool must end on 16px body and `--text-primary: #14181d` /
   `#f2f5f8`. A find-and-replace across the token blocks fixes it.
3. **Phase interferometry upgrade.** Make the antenna count configurable 2–6 (default 4,
   unequal spacings editable), then rename it "Phase interferometry" — dropping "4-antenna"
   — in its `<title>`, its `<h1>`, and in the link text on `index.html` and
   `geolocation.html`.
4. **Icons.** Add the 7 category glyphs from `.research/icons.md` to the hub and category
   page headings, plus the favicon line to every page. Currently there are none and browser
   tabs are blank.
5. **Root pages.** `index.html` and the 7 category pages still use the old narrow column and
   old palette; bring them onto the kit tokens and the responsive container.
6. **Canvas hardware sweep.** Replace any remaining cartoon-style scene drawings with the
   vocabulary in `.research/icons.md`.

## How to verify — do not skip this

The owner has explicitly complained about unverified work. Before claiming any file is done:

```bash
# 1. JavaScript must parse (run from the tools/ directory)
for f in *.html; do sed -n '/<script>/,/<\/script>/p' "$f" | sed '1d;$d' > /tmp/c.js; node --check /tmp/c.js || echo "SYNTAX ERROR: $f"; done

# 2. Serve locally, then open pages in a real browser
python -m http.server 8931
```

In the browser, for each page you changed: console must be clean; screenshot at 375, 768,
1366 and 1920 px wide and look at them; check both light and dark colour schemes; drive the
two most important controls to both extremes and confirm no `NaN`, blank canvas, or text
crossing a border. Then run the overflow check from the NO OVERFLOW section of `STYLE.md`.

Recompute at least one number per tool by hand against the `.research/*.md` reference files.
A plausible-looking wrong curve is worse than no tool.

## Notes for a non-Claude assistant

- Everything is plain HTML/CSS/JS in git, so nothing here is tied to a particular model or
  tool. The spec files are the project's memory.
- The `.research/*.md` reference files are large (40–60 KB each). Read the section you need
  rather than the whole file.
- The physics has been verified once already against the course notes; changing a formula
  without re-deriving it is the most likely way to break this project.
- Filenames are load-bearing (pages link to each other). Change display names, not files.
