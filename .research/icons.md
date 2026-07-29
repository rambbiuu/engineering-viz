# Icon set — minimal line marks

Owner's brief: "more minimalistic". These are instrument marks, not illustrations. One
glyph per category; tools inherit their category's glyph. Seven glyphs total for the whole
suite — restraint is the point. Do not invent extra icons, do not use emoji, do not use a
filled or multi-colour icon anywhere.

## Rules

- 24 × 24 viewBox, `fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`,
  `stroke-linecap="round"`, `stroke-linejoin="round"`.
- Inherits text colour through `currentColor` — so it is automatically correct in both
  themes and needs no dark-mode rule.
- Rendered at 20 × 20 in card headers, sitting left of the title with a 10px gap, optically
  aligned to the cap height (`vertical-align: -3px` or flex `align-items: center`).
- Decorative: every inline icon carries `aria-hidden="true"`.
- Never scale a glyph above 24px or below 16px. Never rotate, never fill, never add a
  background plate or circle behind it.
- One stroke weight across the whole set. If a glyph looks busy at 20px, simplify the glyph
  rather than thinning the stroke.

## The seven glyphs

Paste inline. `class="ico"` for sizing.

**signals** — a sine wave, the base object of the whole suite
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12c2.5 0 2.5-7 5-7s2.5 14 5 14 2.5-7 5-7 2.5 3.5 5 3.5"/></svg>
```

**modulation** — a carrier inside its envelope
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12v-3M6.5 12V6M10 12V4M13.5 12V6M17 12v-3M20.5 12v-1M3 12v3M6.5 12v6M10 12v8M13.5 12v6M17 12v3M20.5 12v1" opacity=".55"/><path d="M3 9c3.5-5 7-5 10.5 0S20.5 11 21 11"/></svg>
```

**antennas** — a mast radiating two arcs
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21V8"/><path d="M8.5 8 12 3l3.5 5"/><path d="M6 11.5a8 8 0 0 1 12 0"/><path d="M3.5 15a12 12 0 0 1 17 0"/></svg>
```

**propagation** — a wave crossing the horizon
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 19h20"/><path d="M3 15c4-9 14-9 18 0" stroke-dasharray="3 2.5"/><path d="M5 19V9M19 19v-6"/></svg>
```

**receivers** — signal narrowing through a chain
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 5h20l-7 8v6l-6 2v-8z"/></svg>
```

**geolocation** — two bearings crossing on a fix
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 20 13 6M21 20 11 6"/><circle cx="12" cy="7.5" r="2.5"/></svg>
```

**cellular** — two tessellating cells
```html
<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3 3 6.5v7L9 17l6-3.5v-7z"/><path d="m15 6.5 6 3.5v7l-6 3.5-6-3.5"/></svg>
```

## CSS

```css
.ico { width: 20px; height: 20px; flex: none; color: var(--text-secondary); }
a.card:hover .ico, .cat-head .ico { color: var(--series-1); }
```

Card header markup:
```html
<h2 style="display:flex;align-items:center;gap:10px;"><svg class="ico" …></svg>Signals</h2>
```

## Favicon — every page, tool and root alike

Browser tabs are currently blank. Add this one line to every `<head>`; it is the signals
glyph as an inline data URI, so it needs no file and works offline:

```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230072bd' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M2 12c2.5 0 2.5-7 5-7s2.5 14 5 14 2.5-7 5-7 2.5 3.5 5 3.5'/%3E%3C/svg%3E">
```

## Canvas hardware marks — the antennas, masts and handsets drawn INSIDE tools

These are not icons; they are drawn on canvas by JS. They are also what the owner meant by
"looks like cartoon", so they follow the same discipline as the glyphs above, scaled up.

**Rules, identical across every tool:**

- One stroke weight per drawing: 1.5px for hardware outlines, 1px for detail, 0.5px for
  grid or ground. Never a thick rounded doodle stroke.
- No fills, except a faint (≤ 0.10 alpha) tint to indicate a solid body such as terrain or
  a building. No gradients, no shadows, no rounded blobby corners.
- Geometric and orthographic, like a datasheet mechanical figure. Straight lines meet at
  clean angles; curves are true arcs, not freehand wobble.
- Colour: hardware is `--text-primary` or `--text-secondary`. Only the *signal* uses a
  series colour. A mast is structure, not data — it must not be blue.
- Every piece of hardware that has a real dimension gets a `dimension()` arrow with the
  value ("30 m", "2.4 cm"), not a cute size comparison.
- No human figures, no vehicles, no buildings with windows, no smiling anything. If scale
  must be shown, use a labelled dimension arrow or a scale bar — never a person or a car.
- Proportions are consistent suite-wide: a mast is ~4× taller than wide at its base, a dish
  aperture is drawn as an arc with a straight feed line, a handset is a plain rounded
  rectangle with a single antenna stub and no screen detail.

**Standard vocabulary — same shape in every tool that needs it:**

| Mark | Construction |
|---|---|
| ground / horizon | single 1px line, optional 0.5px hatching below at 45°, ≤ 0.10 alpha |
| mast | vertical line, two short diagonal guy stubs at the base, small crossbar at top |
| dish | arc of ~100° with a straight feed line from the vertex to the focus, plus a short mount line |
| dipole element | one vertical line with a 1px gap at the centre feed point |
| array element | short vertical tick on a common baseline, evenly or unevenly spaced |
| handset / mobile | rounded rectangle, 2:1 tall, one antenna stub, nothing inside |
| base station | mast with three short sector bars at the top |
| receiver / block | plain rectangle with a centred sentence-case label, connected by 1px lines |
| obstacle / knife edge | filled-to-baseline triangle or rectangle at ≤ 0.10 alpha, 1.5px outline |
| satellite | rectangle body with two straight panel lines either side |
| emitter | small filled circle, series colour, with a leader label |

**Motion:** if a wave animates, only the wave moves. Hardware is static. No bobbing, no
pulsing glow, no sparkles.

## Where icons go, and where they do not

- Hub `index.html`: the category glyph in each category card. Yes.
- Category pages: the category glyph once beside the `h1`. Tool cards on that page stay
  text-only — repeating one glyph seven times down a page is noise, not navigation.
- Inside a tool: no icons at all. The plot is the visual; a decorative glyph beside a
  section heading competes with it.
