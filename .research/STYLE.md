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
5. **(REMOVED — owner rejected guided tours; do not add them.)** ~~A guided tour.~~ A row of numbered step buttons that *drive the controls themselves*
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

## INSTRUMENT LOOK — the owner's aesthetic ruling (2026-07-29)

The owner's words: the diagrams "look like cartoon — I want it professional, bigger, more
customisable. The whole point is to let a new engineer play with it; keep explanations
short; ADHD people must understand at one look."

**Professional means measurement instrument, not illustration.** The reference aesthetic
is a MATLAB figure, an oscilloscope graticule, a spectrum-analyser screen, a datasheet
plot. Concretely:

- Every plot gets a real graticule: fine gridlines (0.5px, `--grid`), labelled tick marks
  with units on BOTH axes, an axis line (`--axis`). Never a floating curve on blank space.
- Line discipline: data series 1.5–2px crisp; grids 0.5px; annotations 1px. No thick
  rounded doodle strokes, no blob shapes, no hand-drawn wobble, no decorative curves.
- Physical scenes (masts, antennas, receivers) are drawn as **dimensioned technical line
  drawings** — thin strokes, dimension arrows with values ("30 m"), like a datasheet
  mechanical figure. Never cute: no stick figures, no rounded cars, no smiley scale props.
- Typography on canvas: 10–12px, tabular numerals, sentence case, sparing. Key value
  annotated at the exact feature it describes with a thin leader line.
- Colour: data uses the series palette; structure stays neutral. No pastel fills except
  faint (≤0.12 alpha) region shading that encodes meaning (a band, a zone, an uncertainty).

**Bigger.** Page `max-width: 980px`. Primary canvas of each tool at least 420px tall;
secondary canvases at least 300px. The plot is the page's hero, not a thumbnail between
paragraphs.

**More customisable, still glanceable.** Every primary physical quantity is adjustable:
pair each important slider with a number input for exact entry; add preset buttons for
recognisable real cases (e.g. "FM broadcast", "GSM", "Wi-Fi"). Extra parameters live in
the collapsed advanced `<details>` — the first screen keeps at most 3–4 controls.

**One-look comprehension (ADHD rule).** Each tool has ONE hero readout: the current key
number, large (28px+), with a coloured state badge when a threshold matters ("Aliased",
"Below sensitivity", "Link OK"). A newcomer must get the story from: title → hero number →
annotated plot, without reading a paragraph.

**Fill the screen — every aspect ratio (owner, 2026-07-29).** The owner: "on my laptop
there's a lot of empty space; on a phone it's different — make it work on all aspect
ratios." A fixed narrow centred column is a defect. Rules:

- Page container: `width: min(1500px, 94vw)` — wide screens get a wide page.
- Canvas sizing: never a fixed pixel height. Use CSS `aspect-ratio` with clamps, e.g.
  `aspect-ratio: 21/9; min-height: 320px; max-height: 62vh;` for hero canvases. The JS
  `fit()` helper already follows CSS size — keep drawing everything relative to the
  measured width/height so the drawing scales, and re-derive label positions from w/h,
  never from hardcoded pixel offsets that only work at one size.
- **NO SIDE RAIL. The owner rejected it explicitly (2026-07-29): "I don't like how you set
  control to one side and the simulation to the other — the previous layout is better."**
  The page is ALWAYS a single column: header, then controls, then the canvas full width
  below, then legend, cards and collapsed details. Never place controls beside the plot.
- Reclaim wide-screen space by making the CONTROLS flow horizontally, not by moving them
  aside: `.rail` is a grid of `repeat(auto-fit, minmax(250px, 1fr))`, so control blocks sit
  in 3–4 columns across the top on a laptop and collapse to one column on a phone. The hero
  readout, preset rows and tour rows span all columns (`grid-column: 1 / -1`).
- Container is `width: min(1180px, 94vw)` — wide enough to fill a laptop without stretching
  a single column of text to an unreadable line length.
- Side-by-side canvas *pairs* are still fine where two views are meant to be compared
  (`.cv-pair`, two columns above 900px). That is content, not chrome.
- Test mentally at 375, 768, 1366 and 1920 wide: no horizontal scroll ever, no canvas
  that shrinks its text into illegibility, no dead margins wider than the content.

**Typography hygiene (owner, 2026-07-29).** The basics must be ironed flat:

- Sentence case everywhere: headings, buttons, card labels, canvas labels, badges. No
  Title Case, no ALL-CAPS words (acronyms like FM, SNR, QPSK keep their natural caps).
- Formulas must look typeset, not typed: real `<sub>`/`<sup>` (f<sub>s</sub>,
  E<sub>b</sub>/N<sub>0</sub>, 10<sup>−3</sup>), italic single-letter variables, true
  minus U+2212 (−) never a hyphen, multiplication as · or ×, proper Greek glyphs (λ, β,
  θ, σ), and units upright with a space (3.6 dB, 15 kHz). On canvas, follow the same
  conventions with unicode sub/superscripts where needed.
- Numbers: tabular numerals, thousands separated with a thin space (1 500 km), one
  consistent decimal precision per quantity.

## NO OVERFLOW — owner ruling, 2026-07-29. Text must never escape its box.

"Make sure the words don't spill out of the box, and have proper spacing and aspect."
Nothing may render outside its container at ANY viewport width or control value. This is a
correctness requirement, not a polish item — a label crossing its border is a defect.

### On canvas

Never call `fillText` without knowing the box it must fit. Add these kit helpers and use
them for every string that is not a short axis tick:

```js
// Shrink to fit, then ellipsise as a last resort. Returns the font size used.
function fitText(g, text, maxW, baseSize, minSize) {
  let s = baseSize;
  g.font = fnt(s);
  while (g.measureText(text).width > maxW && s > minSize) { s -= 0.5; g.font = fnt(s); }
  if (g.measureText(text).width > maxW) {
    let t = text;
    while (t.length > 1 && g.measureText(t + '…').width > maxW) t = t.slice(0, -1);
    return { text: t + '…', size: s };
  }
  return { text: text, size: s };
}

// Word-wrap into a box, vertically centred, never exceeding maxLines.
function textInBox(g, text, x, y, w, h, opts) { /* measure per word, break, clamp */ }

// Clamp a draw position so the drawn string stays inside [pad, w-pad] for any textAlign.
function clampX(g, x, text, align, w, pad) {
  const tw = g.measureText(text).width;
  const half = align === 'center' ? tw / 2 : align === 'right' ? tw : 0;
  return Math.min(Math.max(x, pad + (align === 'right' ? tw : align === 'center' ? tw / 2 : 0)),
                  w - pad - (align === 'left' ? tw : align === 'center' ? tw / 2 : 0));
}
```

Hard rules:
- Every canvas box gets **≥ 10px internal padding**; text never touches a border or an axis.
- Axis tick labels: if adjacent labels would collide, thin them out (draw every 2nd or 5th)
  rather than shrinking below the 12px floor or letting them overlap.
- `leader()` labels flip to the opposite side of the feature when within 1 label-width of an
  edge, and stack vertically if two would occupy the same spot.
- The last tick label on an axis must not be clipped by the canvas edge — reserve room for
  half its width in the plot box.
- Rotated axis titles use `translate`+`rotate`, and the rotated extent counts toward the
  margin reservation.
- After any change to a drawing, re-check at the **narrowest** supported canvas: text that
  fits at 1400px often collides at 360px.

### In HTML

- `*, *::before, *::after { box-sizing: border-box; }` — non-negotiable.
- Every grid and flex child that contains text carries `min-width: 0;` — without it a long
  word forces the track wider than its container. This is the single most common cause of
  the horizontal scrollbar.
- Text containers get `overflow-wrap: anywhere;`. Card values additionally get
  `font-variant-numeric: tabular-nums;` so a changing number does not resize its box.
- Never a fixed `width` on anything holding text; use `min-width`/`max-width` so it can
  shrink.
- Buttons and labels: `white-space: nowrap` ONLY where the string is short and fixed;
  otherwise let it wrap.
- Consistent internal padding: cards `1rem 1.25rem`, control rows `0.5rem 0`, details
  blocks `0.75rem 1rem`. Do not vary these per tool.
- The page must never scroll horizontally. Verify with
  `document.documentElement.scrollWidth <= window.innerWidth` at 375, 768, 1366 and 1920.

### Verification, required before any agent reports done

```js
// paste in the console; must return an empty array
[...document.querySelectorAll('*')].filter(e => {
  const r = e.getBoundingClientRect();
  return r.width && (r.right > document.documentElement.clientWidth + 1 || r.left < -1);
}).map(e => e.tagName + '.' + e.className);
```
Plus: screenshot at 375 and 1920 and LOOK for text crossing a border, colliding labels, or a
value pushed outside its card.

## TEXT LEGIBILITY — owner ruling, 2026-07-29. Overrides the kit if they disagree.

The owner: "make the text bigger, and not grey — white or black." Current pages use 13–14px
body text and grey secondary text; both are too small and too washed out. Fix at the token
level so every tool inherits it.

**Font family.** Keep the system stack — on Windows it already resolves to Segoe UI
Variable, the same family as the surrounding app, so the family was never the problem.
Declare it explicitly and identically everywhere:

```css
--font-sans: system-ui, -apple-system, "Segoe UI Variable Text", "Segoe UI", Roboto,
             "Helvetica Neue", Arial, sans-serif;
--font-mono: ui-monospace, "Cascadia Mono", "SF Mono", Menlo, Consolas, monospace;
```

**Sizes — these are minimums, not suggestions.**

| Role | Old | Required |
|---|---|---|
| Body / prose | 14px | **16px**, `line-height: 1.65` |
| Intro `.sub`, prose under headings | 14px | **15.5px** |
| h1 | 22px | **28px** |
| Section heading `.sec` | 14px | **16px** |
| Control labels, buttons, inputs | 13px | **14.5px** |
| Card label `.hd` | 13px | **14px** |
| Card value `.big` | 21–22px | **26px** |
| Card footnote `.ft` | 12px | **13px** |
| Legend line | 12.5px | **14px** |
| Hero value | — | **36px** |
| Canvas: axis tick labels | 10–11px | **12px** |
| Canvas: annotations, series labels | 10.5–11px | **13px** |
| Canvas: absolute floor | — | **12px, never smaller** |

Canvas text scales with the canvas: use `Math.max(12, Math.round(w / 62))` for annotations
and `Math.max(12, Math.round(w / 78))` for tick labels, so a wide plot gets larger type
rather than the same small type in more space.

**Colour — kill the grey.** Body and every label a reader needs are near-black on light and
near-white on dark. `--text-muted` is reserved for genuinely incidental text (a units suffix,
a "schematic" caption) and must never carry meaning. Replace the palette's text tokens with:

```css
/* light */
--text-primary:   #14181d;   /* near black — body, labels, card values */
--text-secondary: #2f3742;   /* dark slate, NOT grey — prose, axis labels */
--text-muted:     #5c6672;   /* incidental only */
/* dark */
--text-primary:   #f2f5f8;   /* near white */
--text-secondary: #d4dae1;
--text-muted:     #9aa5b1;
```

Canvas rule: axis tick labels, series labels and annotations use `--text-primary` or
`--text-secondary`. Never `--text-muted` for anything that carries a number or a name.
Contrast must clear 7:1 for body text and 4.5:1 for the smallest canvas label, in both
themes. If a label is hard to read on a screenshot, it is a defect.

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
