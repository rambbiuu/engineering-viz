# House style contract for engineering-viz tools

Every tool is ONE self-contained `.html` file in `tools/`. No build step, no external
requests, no CDN, no frameworks. Opens by double-click and works offline.

## THE READER — read this before anything else

The reader is **new to RF and learns visually**. They have never seen a Smith chart, do not
know what dBm means, and cannot read an unlabelled plot. They did not choose to read an
equation; they came here because the equation did not work for them.

A tool that is correct but unreadable to that person has failed. Judge every decision by:
*would someone who has never heard this word understand what they are looking at, without
scrolling away to look something up?*

This means the abstract plot is never the first thing, and never the only thing.

### WORD BUDGET — minimum wording, the owner's explicit rule

These are visualisation tools. The visuals teach; words only point. Prose that explains
what a picture could show is a defect. Hard caps on always-visible text:

- Page intro: **2 sentences maximum, ~35 words**. No second paragraph.
- Section heading explainer: **≤ 10 words**.
- Legend / "what am I looking at" bullet: swatch + **≤ 6 words** ("blue — the real wave").
- Guided-tour narration: **one sentence, ≤ 14 words**.
- Metric card footnote: **≤ 8 words**.
- Closing paragraph: **cut it**, or one sentence inside the collapsed details block.

Everything wordier goes **on demand, collapsed by default**: glossary, worked example,
long explanations, analogies all live inside `<details>`. Jargon gets a dotted-underline
term that shows its definition on tap/hover — never an inline defining sentence.
Prefer a 4-word label drawn on the canvas over any sentence below it. When cutting, keep
the label, cut the explanation of the label.

### Mandatory beginner scaffolding — every tool, no exceptions

1. **Anchor before abstraction.** The first visual must be a recognisable physical picture —
   an antenna on a mast, a wave in the air, a receiver box, two towers on a hill — drawn to
   a human scale, with the parts labelled in words. Only after that may an axes-and-curves
   plot appear. If a tool has only abstract plots, it is not finished.
2. **Define every term on demand, not inline.** Every jargon word (dB, dBm, phase, gain,
   IF, SIR, PSD, bandwidth…) is a dotted-underline term whose plain definition appears on
   tap/hover. The sentence around it stays short and does not restate the definition.
3. **A compact legend under every canvas.** One line per visual element: colour swatch +
   ≤ 6 words. Use the class `.legend-note`. No full sentences.
4. **Label features on the canvas itself**, not only on the axes. Draw a short leader line
   and a few words pointing at the peak, the null, the crossing point, the region that
   matters. A student should be able to screenshot the canvas alone and still follow it.
5. **A guided tour.** A row of numbered step buttons that *drive the controls themselves*
   and narrate what just changed in one sentence ("Step 2 — frequency doubled; notice the
   wave peaks are now half as far apart"). Three to five steps, ending in the interesting
   case. This is the single highest-value feature for a visual learner; do not skip it.
6. **One worked example with real arithmetic** — inside a collapsed `<details>` block.
7. **An everyday analogy where one genuinely fits** — expressed visually if at all possible
   (draw the ocean wave, the strobe-lit wheel), otherwise one short sentence. Do not force it.
8. **A glossary** at the foot of the page inside a collapsed `<details>`, `<dl class="glossary">`.
9. **Progressive disclosure.** Expert-only controls go inside a `<details>` element that is
   collapsed by default, so the first screen is never a wall of sliders.
10. **Prerequisites and next steps.** A single line near the top — "if this is unfamiliar,
    start with <a>…</a>" — and a line at the bottom pointing at the tool that follows.

### Language

Write for someone intelligent who lacks the vocabulary, not for someone slow. Short
sentences. Active voice. Expand every acronym on first use. Prefer "how strong the signal
is" over "received power level" on first mention, then introduce the technical term
alongside it. Never use "simply", "just", "obviously", or "as you can see".

## Reference implementation

Read `tools/link-budget.html` before writing anything. Copy its `<style>` block verbatim
(the `:root` token set plus the `@media (prefers-color-scheme: dark)` override) and its
overall document skeleton. Do not invent a new palette.

## Required structure, in order

1. `<!DOCTYPE html>`, `<html lang="en">`, `<head>` with charset + viewport + `<title>`.
2. The standard `<style>` block (tokens, `body`, `h1`, `.sub`, `.back`, `button`, `.row`,
   `.ctl`, `.sec`, `.cards`, `.card`, `canvas`).
3. `<p style="margin: 0 0 1rem;"><a class="back" href="../index.html">&larr; all tools</a></p>`
4. `<h1>` — the tool name, sentence case.
5. `<p class="sub">` — 2–4 sentences of plain-English framing. Say what the thing IS and why
   an engineer cares, not what the sliders do.
6. Controls: `.row` / `.ctl` blocks with `<input type="range">` and a live readout `<span>`.
   Buttons for discrete choices, `.on` class marks the active one.
7. Numbered sections: `<p class="sec"><b>1 &middot; Title</b> <span>&mdash; one-line explainer</span></p>`
   followed by a `<canvas>`.
8. `.cards` grid of computed metric cards (`.hd` label, `.big` value, `.ft` footnote).
9. A closing `<p class="sub">` — 3–5 sentences of the engineering lesson: what to try, what
   trade-off it demonstrates, what a practitioner does about it.

## Theme and palette — MANDATORY, replaces any earlier palette

The suite follows the operating system setting automatically through
`@media (prefers-color-scheme: dark)`. Light is the primary design target and must look
like a MATLAB figure: white paper, light grey grid, saturated data lines.

Declare BOTH themes as CSS custom properties on `:root` and never hardcode a colour in
JS. Canvas code reads them at draw time with `getComputedStyle(document.documentElement)
.getPropertyValue('--series-1')` and so on, so a theme change needs no code change.

```css
:root {
  /* surfaces — MATLAB figure white */
  --bg: #ffffff;
  --surface-1: #f4f6f8;
  --surface-2: #ffffff;
  --plot-bg: #ffffff;
  --grid: #e4e8ec;
  --grid-strong: #c8ced4;
  --axis: #3c4650;
  /* text */
  --text-primary: #1a1f26;
  --text-secondary: #55606c;
  --text-muted: #869099;
  /* MATLAB default series order — do not reorder, do not substitute */
  --series-1: #0072bd;  /* blue      */
  --series-2: #d95319;  /* orange    */
  --series-3: #edb120;  /* yellow    */
  --series-4: #7e2f8e;  /* purple    */
  --series-5: #77ac30;  /* green     */
  --series-6: #4dbeee;  /* light blue*/
  --series-7: #a2142f;  /* dark red  */
  /* semantic */
  --good: #77ac30;
  --warn: #d95319;
  --bad: #a2142f;
  --border: #dfe4e9;
  --border-strong: #b6bfc8;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16191d;
    --surface-1: #1e2328;
    --surface-2: #232930;
    --plot-bg: #1a1e23;
    --grid: #2c333a;
    --grid-strong: #444d56;
    --axis: #9aa5b1;
    --text-primary: #e9edf1;
    --text-secondary: #b0bac4;
    --text-muted: #7d8791;
    /* brightened so the same series stays recognisably the same colour */
    --series-1: #4da6ff;
    --series-2: #ff8c42;
    --series-3: #ffd24d;
    --series-4: #c77dda;
    --series-5: #9fd356;
    --series-6: #7fd4f5;
    --series-7: #ff6b6b;
    --good: #9fd356;
    --warn: #ff8c42;
    --bad: #ff6b6b;
    --border: #2c333a;
    --border-strong: #49525b;
  }
}
```

Rules that follow from this:
- Assign series colours in order: the first data series is `--series-1`, the second
  `--series-2`, and so on. Where a colour carries meaning across several tools (for example
  one antenna, one signal, one band), keep that mapping consistent between tools.
- Plot areas get `--plot-bg` with a `--grid` gridline and a `--axis` axis line. In light
  mode this reads as a MATLAB figure; do not fill plots with the page background.
- Never a raw grey or black hex for text. Never a colour literal in JS.
- Check both themes before finishing. Any element that vanishes or drops below comfortable
  contrast in either theme is a defect, not a preference.

## Hard rules
- Canvas: use the `fit(c)` devicePixelRatio helper from the reference file. Read colours
  at draw time via `getComputedStyle` so dark mode works. Never hardcode text colour.
- Wrap all JS in an IIFE: `(function () { ... })();`
- Every displayed number goes through `.toFixed(n)`. No raw float artifacts. No `NaN`,
  no `Infinity`, no `undefined` reaching the DOM — guard every division and `asin`.
- Animation: `requestAnimationFrame`, clamp the delta (`Math.min(ts - last, 50)`), and
  respect `matchMedia('(prefers-reduced-motion: reduce)')`.
- Keyboard focus stays visible (`:focus-visible` outline). Label every input.
- No emoji. No `<!-- comments -->` in the HTML body. Sentence case everywhere.
- British-neutral plain English. No exclamation marks. No "simply", "just", "easy".

## Physics rules

- Formulas must match the course notes in `.research/*.md`. Where a model is simplified,
  say so in the closing paragraph — never silently fake it.
- Units on every axis and every card. Prefer engineering units (dBm, dB/km, MHz, km).
- Sliders must span a range where the interesting behaviour actually happens, and the
  default state must already show something worth looking at.
