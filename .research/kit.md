# Shared instrument kit

The one style block, the one set of canvas helpers, the one page skeleton that every tool in
`tools/` uses. Paste them verbatim. Do not fork them, do not "improve" them locally, do not
invent a parallel palette — 28 tools have to look like one instrument family.

Everything here has been run: the helpers pass an assertion suite over canvas sizes from
1200×500 down to 40×30 (linear and log axes, degenerate ranges, edge-clamped labels), and the
CSS was rendered in a browser at 375, 502, 1200 and 1440 px wide — the rail layout and the
graticule checked in dark, the stacked layout and the scale drawing in light.

Authority order: `user-requests.md` > `STYLE.md` > this file. This file only makes those two
mechanical.

## 0 · How to apply, in order

1. Replace the tool's entire `<style>…</style>` with **block 1**. Delete whatever was there.
2. Rewrap `<body>` in the **block 3** skeleton (`.wrap` > `header.full` + `.rail` + `.stage`).
3. Paste **block 2** as the first thing inside the tool's existing `(function () { … })();`.
4. Rewrite each `draw*()` to start with `fit()` + `theme()` + `graticule()`.
5. Work the **section 4** checklist, then the **section 5** typography table.

Three rules that break the look if you ignore them:

- No colour literal in JS. Ever. Every colour comes from `theme()`.
- No `style="height: 300px"` on a canvas. Use `class="cv-hero"` or `class="cv-sub"`.
- No drawing coordinate is a hardcoded pixel offset. Everything derives from the `w`/`h`
  that `fit()` returned, or from the plot rect that `graticule()` returned.

---

## 1 · The canonical `<style>` block

Paste whole. The only edit permitted is adding a tool-specific class **after** the block, and
only when no existing class does the job.

```html
<style>
:root {
  --bg: #ffffff; --surface-1: #f4f6f8; --surface-2: #ffffff; --plot-bg: #ffffff;
  --grid: #e4e8ec; --grid-strong: #c8ced4; --axis: #3c4650;
  --text-primary: #1a1f26; --text-secondary: #55606c; --text-muted: #869099;
  --series-1: #0072bd; --series-2: #d95319; --series-3: #edb120; --series-4: #7e2f8e;
  --series-5: #77ac30; --series-6: #4dbeee; --series-7: #a2142f;
  --good: #77ac30; --warn: #d95319; --bad: #a2142f;
  --border: #dfe4e9; --border-strong: #b6bfc8;
  --radius: 8px;
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16191d; --surface-1: #1e2328; --surface-2: #232930; --plot-bg: #1a1e23;
    --grid: #2c333a; --grid-strong: #444d56; --axis: #9aa5b1;
    --text-primary: #e9edf1; --text-secondary: #b0bac4; --text-muted: #7d8791;
    --series-1: #4da6ff; --series-2: #ff8c42; --series-3: #ffd24d; --series-4: #c77dda;
    --series-5: #9fd356; --series-6: #7fd4f5; --series-7: #ff6b6b;
    --good: #9fd356; --warn: #ff8c42; --bad: #ff6b6b;
    --border: #2c333a; --border-strong: #49525b;
  }
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--text-primary);
  font-family: var(--font-sans); font-size: 15px; line-height: 1.5;
  font-variant-numeric: tabular-nums; }

.wrap { width: min(1500px, 94vw); margin: 0 auto; padding: 1.4rem 0 4rem;
  display: grid; grid-template-columns: 1fr; gap: 1.4rem; align-items: start; }
.rail, .stage { min-width: 0; }
.rail { display: flex; flex-direction: column; gap: 1rem; }
.stage { display: flex; flex-direction: column; }
@media (min-width: 1100px) {
  .wrap { grid-template-columns: minmax(280px, 340px) 1fr; column-gap: 2rem; }
  .wrap > .full { grid-column: 1 / -1; }
  .rail { position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow-y: auto; }
}

h1 { font-size: 23px; font-weight: 500; margin: 0 0 5px; letter-spacing: -0.01em; }
.sub { font-size: 14px; color: var(--text-secondary); margin: 0 0 6px; max-width: 78ch; }
.prereq { font-size: 13px; color: var(--text-muted); margin: 0; }
.prereq a, .sub a { color: var(--series-1); }
a { color: inherit; }
.back { font-size: 13px; color: var(--text-secondary); text-decoration: none; }
.back:hover { text-decoration: underline; }
.sec { margin: 1.5rem 0 6px; font-size: 14px; }
.sec:first-child { margin-top: 0; }
.sec b { font-weight: 500; }
.sec span { color: var(--text-secondary); font-size: 12.5px; }
.var { font-style: italic; }
.unit { white-space: nowrap; }
.term { border-bottom: 1px dotted var(--border-strong); cursor: help; }

input, button, select { font: inherit; color: inherit; }
button { background: transparent; border: 1px solid var(--border-strong);
  border-radius: var(--radius); padding: 5px 11px; font-size: 13px; cursor: pointer; }
button:hover { background: var(--surface-1); }
button.on { border-color: var(--series-1); color: var(--series-1); background: var(--surface-1); }
input:focus-visible, button:focus-visible, summary:focus-visible, a:focus-visible {
  outline: 2px solid var(--series-1); outline-offset: 2px; }

.hero { background: var(--surface-1); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.8rem 1rem 0.9rem; }
.hero .lbl { font-size: 12.5px; color: var(--text-secondary); }
.hero .val { font-size: 34px; line-height: 1.05; font-weight: 500; margin: 3px 0 0;
  font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.hero .val .u { font-size: 17px; font-weight: 400; color: var(--text-secondary); margin-left: 5px; }
.hero .badge { display: inline-block; margin-top: 8px; font-size: 12px; line-height: 1.6;
  padding: 1px 9px; border-radius: 999px; border: 1px solid var(--border-strong);
  color: var(--text-secondary); background: transparent; }
.hero .badge.good { color: var(--good); border-color: var(--good);
  background: color-mix(in srgb, var(--good) 13%, transparent); }
.hero .badge.warn { color: var(--warn); border-color: var(--warn);
  background: color-mix(in srgb, var(--warn) 13%, transparent); }
.hero .badge.bad { color: var(--bad); border-color: var(--bad);
  background: color-mix(in srgb, var(--bad) 13%, transparent); }
.hero .ft { font-size: 12px; color: var(--text-muted); margin-top: 6px; }

.ctl { display: grid; grid-template-columns: 1fr; gap: 3px; margin-bottom: 0.75rem; }
.ctl label { font-size: 13px; color: var(--text-secondary); }
.ctl .in { display: flex; align-items: center; gap: 8px; }
.ctl input[type=range] { flex: 1 1 60px; min-width: 0; accent-color: var(--series-1); }
.ctl input[type=number] { width: 7ch; padding: 3px 5px; text-align: right;
  font-size: 13px; font-variant-numeric: tabular-nums; background: var(--surface-2);
  color: var(--text-primary); border: 1px solid var(--border-strong); border-radius: 6px; }
.ctl .unit { font-size: 12px; color: var(--text-muted); min-width: 3.4ch; }

.presets { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: 0 0 0.9rem; }
.presets .lbl, .tour .lbl { font-size: 12.5px; color: var(--text-secondary); margin-right: 2px; }
.tour { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: 0 0 0.4rem; }
.tour-note { font-size: 13px; color: var(--text-secondary); margin: 0 0 1rem; min-height: 1.5em; }

canvas { display: block; width: 100%; background: var(--plot-bg);
  border: 1px solid var(--border); border-radius: 6px; }
.cv-hero { aspect-ratio: 21 / 9; min-height: 320px; max-height: 62vh; }
.cv-sub { aspect-ratio: 16 / 7; min-height: 240px; }
.cv-pair { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 900px) { .cv-pair { grid-template-columns: 1fr 1fr; } }

ul.legend-note { list-style: none; margin: 7px 0 0; padding: 0;
  font-size: 12.5px; color: var(--text-secondary); }
ul.legend-note li { display: inline-block; margin: 2px 16px 2px 0; }
.sw { display: inline-block; width: 11px; height: 11px; border-radius: 2px;
  margin-right: 6px; vertical-align: -1px; }
.sw.dash { height: 0; border-top: 2px dashed currentColor; border-radius: 0; vertical-align: 3px; }

.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
.card { background: var(--surface-1); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.7rem 0.85rem; }
.card .hd { font-size: 12.5px; color: var(--text-secondary); }
.card .big { font-size: 21px; font-weight: 500; margin-top: 3px; font-variant-numeric: tabular-nums; }
.card .ft { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

details { border: 1px solid var(--border); border-radius: var(--radius);
  padding: 0.55rem 0.85rem; margin: 1rem 0 0; }
summary { font-size: 13px; color: var(--text-secondary); cursor: pointer; }
details[open] summary { margin-bottom: 0.6rem; }
ol.work { font-size: 13px; color: var(--text-secondary); padding-left: 1.3rem; margin: 0.3rem 0 0; }
ol.work li { margin: 3px 0; }
dl.glossary { font-size: 13px; margin: 0.3rem 0 0; }
dl.glossary dt { font-weight: 500; margin-top: 8px; }
dl.glossary dd { margin: 1px 0 0; color: var(--text-secondary); }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { text-align: right; padding: 5px 8px; border-bottom: 1px solid var(--border); }
th:first-child, td:first-child { text-align: left; color: var(--text-secondary); }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
</style>
```

### Class inventory — what to use for what

| Class | Use |
| --- | --- |
| `.wrap` | Page container. `width: min(1500px, 94vw)`, CSS grid. Everything lives inside it. |
| `header.full` | Back link, `h1`, intro, prerequisite line. Spans both columns on wide screens. |
| `.rail` | Left rail ≥1100 px: hero readout, primary controls, presets, cards. Stacks on top on narrow screens. |
| `.stage` | The canvases and their section headings and legends. |
| `.hero` / `.val` / `.badge` | The one big number. `.badge good` / `warn` / `bad` for the state. |
| `.ctl` | One control: `<label>` + `.in` holding range + number + `.unit`. |
| `.presets` / `.tour` | Button rows. `button.on` marks the active one. |
| `.cv-hero` / `.cv-sub` | Canvas sizing. Never set a height attribute or inline height. |
| `.cv-pair` | Two canvases side by side ≥900 px, stacked below. |
| `.legend-note` / `.sw` | Swatch + ≤6 words per visual element. `.sw.dash` for a dashed line. |
| `.cards` / `.card` | Computed metric cards (`.hd`, `.big`, `.ft`). |
| `.sec` | Numbered section heading: `<b>1 · Title</b> <span>— ≤10-word explainer</span>`. |
| `.var` / `.unit` / `.term` | Italic variable, non-breaking unit, dotted-underline jargon with `title=`. |

Layout behaviour, already handled — do not re-solve it:

- **< 1100 px**: one column, DOM order (header, rail, stage). No horizontal scroll at 375 px.
- **≥ 1100 px**: `minmax(280px, 340px) 1fr`; the rail sticks while the stage scrolls.
- `.cv-hero` is 21:9 clamped to `min-height: 320px` / `max-height: 62vh`; at 1440 px wide that
  is a 982×421 canvas, which satisfies the "primary canvas ≥ 420 px tall" rule.
- `.rail` and `.stage` both carry `min-width: 0` so a wide canvas can never push the grid out.

---

## 2 · Canvas helpers

Paste whole, inside the tool's IIFE, above your drawing code. Dependency-free. Every function
survives a canvas as small as 40×30 without collapsing or throwing.

```html
<script>
(function () {
  /* ============================================================
     engineering-viz shared canvas kit — paste verbatim inside the
     tool's IIFE, above your own drawing code. No dependencies.
     ============================================================ */

  /* --- 1. sizing ------------------------------------------------ */
  function fit(c) {
    const r = c.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(1, r.width), h = Math.max(1, r.height);
    const W = Math.max(1, Math.round(w * dpr)), H = Math.max(1, Math.round(h * dpr));
    if (c.width !== W) c.width = W;
    if (c.height !== H) c.height = H;
    const g = c.getContext('2d');
    g.setTransform(W / w, 0, 0, H / h, 0, 0);
    g.clearRect(0, 0, w, h);
    return [w, h];
  }

  /* --- 2. palette ----------------------------------------------- */
  let _th = null;
  (function () {
    const mq = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
    if (mq && mq.addEventListener) mq.addEventListener('change', function () { _th = null; });
  })();
  function theme() {
    if (_th) return _th;
    const cs = getComputedStyle(document.documentElement);
    const v = n => cs.getPropertyValue(n).trim();
    const fam = v('--font-sans') || 'system-ui, sans-serif';
    const s = [v('--series-1'), v('--series-2'), v('--series-3'), v('--series-4'),
               v('--series-5'), v('--series-6'), v('--series-7')];
    _th = {
      bg: v('--bg'), surface: v('--surface-1'), surface2: v('--surface-2'), plot: v('--plot-bg'),
      grid: v('--grid'), gridStrong: v('--grid-strong'), axis: v('--axis'),
      text: v('--text-primary'), text2: v('--text-secondary'), muted: v('--text-muted'),
      good: v('--good'), warn: v('--warn'), bad: v('--bad'),
      border: v('--border'), borderStrong: v('--border-strong'),
      family: fam, s: s,
      s1: s[0], s2: s[1], s3: s[2], s4: s[3], s5: s[4], s6: s[5], s7: s[6],
      font: function (px, weight) { return (weight ? weight + ' ' : '') + px + 'px ' + fam; }
    };
    return _th;
  }
  theme.clear = function () { _th = null; };

  /* --- 3. numbers ----------------------------------------------- */
  const THIN = ' ', NB = ' ', MINUS = '−';
  const _PFX = [[1e12, 'T'], [1e9, 'G'], [1e6, 'M'], [1e3, 'k'], [1, ''],
                [1e-3, 'm'], [1e-6, 'µ'], [1e-9, 'n'], [1e-12, 'p']];
  const _SCALABLE = /^(m|Hz|s|W|V|A|F|H|Ω|J|N|Pa|bit\/s|b\/s|B\/s|Sa\/s|sps|bd|rad)$/;

  function fmtNum(x, dec) {
    if (x == null || !isFinite(x)) return '—';
    dec = dec == null ? 0 : Math.max(0, Math.min(8, dec));
    const s = Math.abs(x).toFixed(dec);
    const p = s.split('.');
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, THIN);
    const body = p.join('.');
    return (x < 0 && parseFloat(s) !== 0 ? MINUS : '') + body;
  }

  function fmtEng(value, unit, decimals) {
    if (value == null || !isFinite(value)) return '—';
    unit = unit == null ? '' : unit;
    const dec = decimals == null ? 1 : decimals;
    let v = value, u = unit;
    if (unit && _SCALABLE.test(unit) && v !== 0) {
      const a = Math.abs(v);
      for (let i = 0; i < _PFX.length; i++) {
        if (a >= _PFX[i][0] * (1 - 1e-12) || i === _PFX.length - 1) {
          v = v / _PFX[i][0]; u = _PFX[i][1] + unit; break;
        }
      }
    }
    const n = fmtNum(v, dec);
    return u ? n + NB + u : n;
  }

  const _SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻', '−': '⁻', '+': '⁺', 'n': 'ⁿ', 'i': 'ⁱ' };
  const _SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    '-': '₋', '−': '₋', '+': '₊', 'a': 'ₐ', 'e': 'ₑ',
    'h': 'ₕ', 'i': 'ᵢ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ',
    'o': 'ₒ', 'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
    'v': 'ᵥ', 'x': 'ₓ' };
  function sup(str) { return String(str).split('').map(ch => _SUP[ch] || ch).join(''); }
  function sub(str) { return String(str).split('').map(ch => _SUB[ch] || ch).join(''); }

  /* --- 4. ticks ------------------------------------------------- */
  function _niceStep(span, count) {
    span = Math.abs(span); count = Math.max(1, count);
    if (!(span > 0) || !isFinite(span)) return 1;
    const raw = span / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const n = raw / mag;
    const s = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
    return s * mag;
  }
  function _linTicks(min, max, count) {
    if (!isFinite(min) || !isFinite(max)) return [];
    if (max === min) max = min + 1;
    if (max < min) { const t = min; min = max; max = t; }
    const st = _niceStep(max - min, count);
    if (!(st > 0)) return [];
    const out = [];
    for (let v = Math.ceil(min / st - 1e-9) * st, i = 0;
         v <= max + st * 1e-9 && i < 500; v += st, i++) {
      out.push(Math.abs(v) < st * 1e-9 ? 0 : v);
    }
    return out;
  }
  function _logTicks(min, max) {
    const lo = Math.max(Math.min(min, max), 1e-300), hi = Math.max(Math.max(min, max), lo * 10);
    const d0 = Math.floor(Math.log10(lo)), d1 = Math.ceil(Math.log10(hi));
    let major = [], minor = [];
    for (let d = d0; d <= d1 && d - d0 < 40; d++) {
      const base = Math.pow(10, d);
      if (base >= lo * (1 - 1e-9) && base <= hi * (1 + 1e-9)) major.push(base);
      if (d1 - d0 <= 5) for (let m = 2; m <= 9; m++) {
        const v = m * base;
        if (v >= lo * (1 - 1e-9) && v <= hi * (1 + 1e-9)) minor.push(v);
      }
    }
    if (major.length < 3) {
      const keep = minor.filter(v => {
        const m = v / Math.pow(10, Math.floor(Math.log10(v) + 1e-9));
        return Math.abs(m - 2) < 0.01 || Math.abs(m - 3) < 0.01 || Math.abs(m - 5) < 0.01;
      });
      major = major.concat(keep).sort((a, b) => a - b);
      minor = minor.filter(v => major.indexOf(v) < 0);
    }
    return { major: major, minor: minor };
  }
  function _autoDec(step) {
    if (!(step > 0) || !isFinite(step)) return 0;
    let dec = Math.max(0, Math.min(6, -Math.floor(Math.log10(step))));
    const k = Math.pow(10, dec);
    if (Math.abs(step * k - Math.round(step * k)) > 1e-6) dec = Math.min(6, dec + 1);
    return dec;
  }
  function _tickText(v, ax, step) {
    if (ax.fmt) return ax.fmt(v);
    let dec = ax.dec;
    if (dec == null) {
      dec = ax.log ? Math.max(0, Math.min(6, -Math.floor(Math.log10(Math.abs(v) || 1) + 1e-9)))
                   : _autoDec(step);
    }
    return fmtNum(v, dec);
  }
  function _axisTitle(ax) {
    if (ax.title != null) return ax.title;
    if (ax.label) return ax.unit ? ax.label + ' (' + ax.unit + ')' : ax.label;
    return ax.unit || '';
  }
  function _px(v) { return Math.round(v) + 0.5; }

  /* --- 5. graticule --------------------------------------------- */
  function graticule(g, box, xs, ys, opts) {
    opts = opts || {};
    const t = theme();
    const small = Math.min(box.w, box.h) < 280;
    const fs = opts.fontSize || (small ? 9.5 : 11);
    g.save();
    g.font = t.font(fs);

    const xt = xs.log ? _logTicks(xs.min, xs.max)
                      : { major: _linTicks(xs.min, xs.max, Math.max(2, Math.round(box.w / (small ? 62 : 88)))), minor: [] };
    const yt = ys.log ? _logTicks(ys.min, ys.max)
                      : { major: _linTicks(ys.min, ys.max, Math.max(2, Math.round(box.h / (small ? 32 : 46)))), minor: [] };
    const xstep = xt.major.length > 1 ? xt.major[1] - xt.major[0] : (xs.max - xs.min) / 4;
    const ystep = yt.major.length > 1 ? yt.major[1] - yt.major[0] : (ys.max - ys.min) / 4;
    const xlab = v => _tickText(v, xs, xstep), ylab = v => _tickText(v, ys, ystep);

    let ymaxw = 0;
    for (let i = 0; i < yt.major.length; i++) ymaxw = Math.max(ymaxw, g.measureText(ylab(yt.major[i])).width);
    const xTitle = _axisTitle(xs), yTitle = _axisTitle(ys);
    const showY = !!yTitle && box.h >= 150 && box.w >= 220;
    const showX = !!xTitle && box.h >= 120;

    let padL = opts.padL != null ? opts.padL : ymaxw + 9 + (showY ? fs + 6 : 0);
    let padB = opts.padB != null ? opts.padB : fs + 9 + (showX ? fs + 6 : 0);
    let padT = opts.padT != null ? opts.padT : (opts.title ? fs + 13 : Math.max(7, fs * 0.7));
    let padR = opts.padR != null ? opts.padR
      : Math.max(10, (xt.major.length ? g.measureText(xlab(xt.major[xt.major.length - 1])).width / 2 : 0) + 4);
    padL = Math.min(padL, box.w * 0.42); padR = Math.min(padR, box.w * 0.22);
    padT = Math.min(padT, box.h * 0.28); padB = Math.min(padB, box.h * 0.38);

    const x0 = box.x + padL, y0 = box.y + padT;
    const iw = Math.max(12, box.w - padL - padR), ih = Math.max(12, box.h - padT - padB);
    const x1 = x0 + iw, y1 = y0 + ih;

    const lg = v => Math.log10(Math.max(Math.abs(v), 1e-300));
    const xa = xs.log ? lg(xs.min) : xs.min, xb = xs.log ? lg(xs.max) : xs.max;
    const ya = ys.log ? lg(ys.min) : ys.min, yb = ys.log ? lg(ys.max) : ys.max;
    const xd = (xb - xa) || 1, yd = (yb - ya) || 1;
    const X = xs.log ? (v => x0 + (lg(v) - xa) / xd * iw) : (v => x0 + (v - xa) / xd * iw);
    const Y = ys.log ? (v => y1 - (lg(v) - ya) / yd * ih) : (v => y1 - (v - ya) / yd * ih);

    if (opts.fill !== false) { g.fillStyle = t.plot; g.fillRect(x0, y0, iw, ih); }

    g.strokeStyle = t.grid; g.lineWidth = 0.5;
    if (xt.minor.length || yt.minor.length) {
      g.save(); g.globalAlpha = 0.7; g.beginPath();
      for (let i = 0; i < xt.minor.length; i++) { const p = _px(X(xt.minor[i])); if (p > x0 && p < x1) { g.moveTo(p, y0); g.lineTo(p, y1); } }
      for (let i = 0; i < yt.minor.length; i++) { const p = _px(Y(yt.minor[i])); if (p > y0 && p < y1) { g.moveTo(x0, p); g.lineTo(x1, p); } }
      g.stroke(); g.restore();
    }
    g.beginPath();
    for (let i = 0; i < xt.major.length; i++) { const p = _px(X(xt.major[i])); if (p > x0 && p < x1) { g.moveTo(p, y0); g.lineTo(p, y1); } }
    for (let i = 0; i < yt.major.length; i++) { const p = _px(Y(yt.major[i])); if (p > y0 && p < y1) { g.moveTo(x0, p); g.lineTo(x1, p); } }
    g.stroke();

    g.strokeStyle = t.axis; g.lineWidth = 1;
    g.strokeRect(_px(x0), _px(y0), Math.round(iw), Math.round(ih));
    const tk = small ? 3 : 4.5;
    g.beginPath();
    for (let i = 0; i < xt.major.length; i++) {
      const p = _px(X(xt.major[i])); if (p <= x0 || p >= x1) continue;
      g.moveTo(p, y1); g.lineTo(p, y1 - tk); g.moveTo(p, y0); g.lineTo(p, y0 + tk);
    }
    for (let i = 0; i < yt.major.length; i++) {
      const p = _px(Y(yt.major[i])); if (p <= y0 || p >= y1) continue;
      g.moveTo(x0, p); g.lineTo(x0 + tk, p); g.moveTo(x1, p); g.lineTo(x1 - tk, p);
    }
    g.stroke();

    g.fillStyle = t.text2; g.font = t.font(fs);
    g.textAlign = 'center'; g.textBaseline = 'top';
    for (let i = 0; i < xt.major.length; i++) {
      const v = xt.major[i], p = X(v);
      if (p < x0 - 1 || p > x1 + 1) continue;
      const s = xlab(v), half = g.measureText(s).width / 2;
      const cx = Math.min(Math.max(p, box.x + half + 1), box.x + box.w - half - 1);
      g.fillText(s, cx, y1 + 4);
    }
    g.textAlign = 'right'; g.textBaseline = 'middle';
    for (let i = 0; i < yt.major.length; i++) {
      const v = yt.major[i], p = Y(v);
      if (p < y0 - 1 || p > y1 + 1) continue;
      g.fillText(ylab(v), x0 - 6, Math.min(Math.max(p, box.y + fs * 0.6), box.y + box.h - fs * 0.4));
    }

    g.fillStyle = t.muted;
    if (showX) { g.textAlign = 'center'; g.textBaseline = 'bottom'; g.fillText(xTitle, x0 + iw / 2, box.y + box.h - 1); }
    if (showY) {
      g.save(); g.translate(box.x + 2, y0 + ih / 2); g.rotate(-Math.PI / 2);
      g.textAlign = 'center'; g.textBaseline = 'top'; g.fillText(yTitle, 0, 0); g.restore();
    }
    if (opts.title) {
      g.fillStyle = t.text; g.font = t.font(fs + 0.5, '500');
      g.textAlign = 'left'; g.textBaseline = 'bottom'; g.fillText(opts.title, x0, y0 - 4);
    }
    g.restore();

    return {
      X: X, Y: Y, x0: x0, y0: y0, x1: x1, y1: y1,
      x: x0, y: y0, w: iw, h: ih, box: { x: x0, y: y0, w: iw, h: ih },
      fs: fs, xTicks: xt.major, yTicks: yt.major,
      clip: function (gg) { gg.save(); gg.beginPath(); gg.rect(x0, y0, iw, ih); gg.clip(); },
      unclip: function (gg) { gg.restore(); }
    };
  }

  /* --- 6. annotation -------------------------------------------- */
  function _rect(g, opts) {
    if (opts && opts.box) return opts.box;
    const dpr = window.devicePixelRatio || 1;
    return { x: 0, y: 0, w: g.canvas.width / dpr, h: g.canvas.height / dpr };
  }
  function leader(g, x, y, text, opts) {
    opts = opts || {};
    const t = theme(), box = _rect(g, opts);
    const size = opts.size || 11, col = opts.colour || t.text2;
    let dx = opts.dx == null ? 30 : opts.dx, dy = opts.dy == null ? -26 : opts.dy;
    g.save();
    g.font = t.font(size, opts.weight);
    const tw = g.measureText(text).width, tail = 7, pad = 4;
    if (dx >= 0 && x + dx + tail + tw + pad > box.x + box.w) dx = -Math.abs(dx);
    if (dx < 0 && x + dx - tail - tw - pad < box.x) dx = Math.abs(dx);
    if (dy <= 0 && y + dy - size < box.y) dy = Math.abs(dy);
    if (dy > 0 && y + dy + size > box.y + box.h) dy = -Math.abs(dy);
    const dir = dx >= 0 ? 1 : -1;
    let ex = x + dx, ey = y + dy;
    ey = Math.min(Math.max(ey, box.y + size * 0.8), box.y + box.h - size * 0.8);
    let tx = ex + dir * (tail + 2);
    let left = dir > 0 ? tx : tx - tw;
    if (left < box.x + 2) { const s = box.x + 2 - left; ex += s; tx += s; left += s; }
    if (left + tw > box.x + box.w - 2) { const s = left + tw - (box.x + box.w - 2); ex -= s; tx -= s; left -= s; }
    g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 1;
    g.beginPath(); g.moveTo(_px(x), _px(y)); g.lineTo(_px(ex), _px(ey)); g.lineTo(_px(ex + dir * tail), _px(ey)); g.stroke();
    if (opts.dot !== false) { g.beginPath(); g.arc(x, y, opts.dotR || 2.2, 0, Math.PI * 2); g.fill(); }
    if (opts.halo !== false) {
      g.globalAlpha = 0.86; g.fillStyle = t.plot;
      g.fillRect(left - 3, ey - size * 0.78, tw + 6, size * 1.5);
      g.globalAlpha = 1;
    }
    g.fillStyle = col; g.textAlign = dir > 0 ? 'left' : 'right'; g.textBaseline = 'middle';
    g.fillText(text, tx, ey);
    g.restore();
  }

  function _head(g, x, y, dir, s) {
    g.beginPath(); g.moveTo(x, y);
    g.lineTo(x - Math.cos(dir - 0.35) * s, y - Math.sin(dir - 0.35) * s);
    g.lineTo(x - Math.cos(dir + 0.35) * s, y - Math.sin(dir + 0.35) * s);
    g.closePath(); g.fill();
  }
  function dimension(g, x1, y1, x2, y2, text, opts) {
    opts = opts || {};
    const t = theme(), col = opts.colour || t.text2, size = opts.size || 10.5;
    const dxv = x2 - x1, dyv = y2 - y1, len = Math.sqrt(dxv * dxv + dyv * dyv);
    if (!(len > 2)) return;
    const a = Math.atan2(dyv, dxv);
    const nx = -Math.sin(a), ny = Math.cos(a);
    const ah = Math.max(3, Math.min(6, len * 0.22));
    g.save();
    g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 1; g.setLineDash([]);
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
    const wt = Math.max(2.5, Math.min(4, len * 0.12));
    g.beginPath();
    g.moveTo(x1 - nx * wt, y1 - ny * wt); g.lineTo(x1 + nx * wt, y1 + ny * wt);
    g.moveTo(x2 - nx * wt, y2 - ny * wt); g.lineTo(x2 + nx * wt, y2 + ny * wt);
    g.stroke();
    _head(g, x1, y1, a + Math.PI, ah); _head(g, x2, y2, a, ah);
    if (text) {
      let ta = a;
      if (ta > Math.PI / 2 || ta < -Math.PI / 2) ta += Math.PI;
      g.translate((x1 + x2) / 2, (y1 + y2) / 2); g.rotate(ta);
      g.font = t.font(size);
      const tw = g.measureText(text).width;
      const off = len < tw + 14 ? -size * 1.05 : 0;
      g.globalAlpha = 0.88; g.fillStyle = t.plot;
      g.fillRect(-tw / 2 - 3, off - size * 0.75, tw + 6, size * 1.45);
      g.globalAlpha = 1; g.fillStyle = col;
      g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillText(text, 0, off);
    }
    g.restore();
  }

  function band(g, box, a, b, colour, axis) {
    const t = theme();
    const lo = Math.min(a, b), hi = Math.max(a, b);
    g.save();
    g.globalAlpha = 0.10; g.fillStyle = colour || t.warn;
    if (axis === 'y') {
      const p0 = Math.max(lo, box.y), p1 = Math.min(hi, box.y + box.h);
      if (p1 > p0) g.fillRect(box.x, p0, box.w, p1 - p0);
    } else {
      const p0 = Math.max(lo, box.x), p1 = Math.min(hi, box.x + box.w);
      if (p1 > p0) g.fillRect(p0, box.y, p1 - p0, box.h);
    }
    g.restore();
  }

  /* --- 7. technical hardware ------------------------------------ */
  function mast(g, x, groundY, heightPx, label, opts) {
    opts = opts || {};
    const t = theme();
    const h = Math.max(6, heightPx), top = groundY - h;
    const bw = Math.max(2.5, Math.min(13, h * 0.075)), tw = Math.max(1.4, bw * 0.36);
    g.save();
    g.strokeStyle = opts.colour || t.axis; g.fillStyle = opts.colour || t.axis;
    g.setLineDash([]); g.lineWidth = 1;
    g.beginPath();
    g.moveTo(x - bw, groundY); g.lineTo(x - tw, top);
    g.moveTo(x + bw, groundY); g.lineTo(x + tw, top);
    g.stroke();
    if (h > 18) {
      const n = Math.max(1, Math.min(24, Math.round(h / Math.max(11, bw * 2.6))));
      g.lineWidth = 0.7; g.beginPath();
      for (let i = 0; i < n; i++) {
        const f0 = i / n, f1 = (i + 1) / n;
        const w0 = bw + (tw - bw) * f0, w1 = bw + (tw - bw) * f1;
        const y0 = groundY + (top - groundY) * f0, y1 = groundY + (top - groundY) * f1;
        g.moveTo(x - w0, y0); g.lineTo(x + w1, y1);
        g.moveTo(x + w0, y0); g.lineTo(x - w1, y1);
        g.moveTo(x - w1, y1); g.lineTo(x + w1, y1);
      }
      g.stroke();
    }
    const ah = Math.max(5, Math.min(16, h * 0.15));
    g.lineWidth = 1.2; g.beginPath();
    g.moveTo(x, top); g.lineTo(x, top - ah);
    g.moveTo(x - ah * 0.42, top - ah * 0.58); g.lineTo(x + ah * 0.42, top - ah * 0.58);
    g.moveTo(x - ah * 0.28, top - ah * 0.92); g.lineTo(x + ah * 0.28, top - ah * 0.92);
    g.stroke();
    g.lineWidth = 1; g.beginPath();
    g.moveTo(x - bw * 1.6, groundY); g.lineTo(x + bw * 1.6, groundY);
    g.stroke();
    if (label) {
      const side = opts.side === 'right' ? 1 : -1;
      const dx = side * (bw + (opts.gap == null ? 16 : opts.gap));
      g.strokeStyle = t.muted; g.lineWidth = 0.5;
      g.beginPath();
      g.moveTo(x, groundY); g.lineTo(x + dx * 1.15, groundY);
      g.moveTo(x, top); g.lineTo(x + dx * 1.15, top);
      g.stroke();
      dimension(g, x + dx, groundY, x + dx, top, label, { size: opts.size || 10.5 });
    }
    g.restore();
  }

  function dish(g, x, y, r, angle, opts) {
    opts = opts || {};
    const t = theme();
    r = Math.max(4, r);
    const back = angle + Math.PI, spread = 1.05;
    g.save();
    g.strokeStyle = opts.colour || t.axis; g.setLineDash([]);
    g.lineWidth = Math.max(1, Math.min(1.6, r * 0.06));
    g.beginPath(); g.arc(x, y, r, back - spread, back + spread); g.stroke();
    const e0x = x + Math.cos(back - spread) * r, e0y = y + Math.sin(back - spread) * r;
    const e1x = x + Math.cos(back + spread) * r, e1y = y + Math.sin(back + spread) * r;
    g.lineWidth = 0.8;
    g.beginPath();
    g.moveTo(e0x, e0y); g.lineTo(x, y); g.moveTo(e1x, e1y); g.lineTo(x, y);
    g.stroke();
    const f = Math.max(1.6, r * 0.13);
    g.lineWidth = 1.1;
    g.strokeRect(x - f, y - f, f * 2, f * 2);
    const bx = x + Math.cos(back) * r, by = y + Math.sin(back) * r;
    g.beginPath();
    g.moveTo(bx, by); g.lineTo(bx + Math.cos(back) * r * 0.45, by + Math.sin(back) * r * 0.45);
    g.stroke();
    if (opts.axisLine !== false && r > 8) {
      g.strokeStyle = t.muted; g.lineWidth = 0.7; g.setLineDash([4, 3]);
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(angle) * r * 1.1, y + Math.sin(angle) * r * 1.1); g.stroke();
      g.setLineDash([]);
    }
    g.restore();
  }

  /* --- 8. slider + number input --------------------------------- */
  function bindPair(rangeEl, numEl, cb) {
    const lo = parseFloat(rangeEl.min), hi = parseFloat(rangeEl.max);
    numEl.value = rangeEl.value;
    rangeEl.addEventListener('input', function () { numEl.value = rangeEl.value; if (cb) cb(parseFloat(rangeEl.value)); });
    numEl.addEventListener('input', function () {
      const v = parseFloat(numEl.value);
      if (isFinite(v) && v >= lo && v <= hi) { rangeEl.value = v; if (cb) cb(parseFloat(rangeEl.value)); }
    });
    numEl.addEventListener('change', function () {
      let v = parseFloat(numEl.value);
      if (!isFinite(v)) v = parseFloat(rangeEl.value);
      rangeEl.value = Math.min(hi, Math.max(lo, v));
      numEl.value = rangeEl.value;
      if (cb) cb(parseFloat(rangeEl.value));
    });
  }

  /* …the tool's own code goes here… */
})();
</script>
```

### API

**`fit(canvas) → [w, h]`**
Sizes the backing store to `devicePixelRatio`, follows the CSS box (so `aspect-ratio` decides
the shape), clears the canvas and returns CSS pixels. Call it first in every draw function and
scale everything you draw to the returned `w`/`h`.

**`theme() → t`**
Reads every palette token once and caches until the OS theme changes.
`t.bg t.surface t.surface2 t.plot t.grid t.gridStrong t.axis t.text t.text2 t.muted t.good
t.warn t.bad t.border t.borderStrong`; series colours as `t.s1 … t.s7` (and `t.s[0…6]` for
loops); `t.font(px)` / `t.font(px, '500')` builds a canvas font string.
First data series is `t.s1`, second `t.s2`, in order — never pick a colour by taste.

**`graticule(g, box, xs, ys, opts) → P`** — the important one. A plot without it looks like a cartoon.
`box` is the area to lay the plot into, normally `{x: 0, y: 0, w: w, h: h}`.
`xs`/`ys` are `{min, max, unit, label, log, dec, fmt, title}` — `unit` and `label` are what turn
an anonymous curve into a measurement; supply both. `log: true` gives decade majors with 2–9
minors. `opts`: `{title, padL, padR, padT, padB, fontSize, fill}`.
Draws: plot fill, 0.5 px minor and major gridlines, a 1 px frame, inward tick marks on all four
sides, tick labels, and both axis titles (`label (unit)`), the y-title rotated.
Returns `P` with `P.X(value)`, `P.Y(value)`, `P.x0 P.y0 P.x1 P.y1 P.w P.h`, `P.xTicks`,
`P.yTicks`, `P.fs`, and `P.clip(g)` / `P.unclip(g)`. `P` is itself a rect (`P.x P.y P.w P.h`),
so it can be passed straight to `band()` and to `leader({box: P})`.

**`leader(g, x, y, text, opts)`**
Dot at the feature, 1 px leader line with a short tail, label at the end with a halo so it stays
readable over a curve. `opts`: `{box, dx, dy, colour, size, weight, dot, halo, dotR}`.
Pass `box: P` and the label can never leave the plot — it flips side and clamps instead.
Two to four per canvas; label the peak, the null, the crossing, the current operating point.

**`dimension(g, x1, y1, x2, y2, text, opts)`**
Technical dimension line: arrowheads and end ticks, the value on the line, rotated with the line
and kept upright, offset beside the line when the line is too short for the text.
`opts`: `{colour, size}`. This is how a scale drawing gets its "30 m".

**`band(g, box, a, b, colour, axis)`**
Region shading at alpha 0.10, clipped to `box`. `a`/`b` are **pixel** coordinates — use
`P.X(v1), P.X(v2)` for a vertical band, or `P.Y(v1), P.Y(v2)` with `axis: 'y'` for a horizontal
one. The only permitted pastel fill: it must encode a zone, a forbidden region or an uncertainty.

**`mast(g, x, groundY, heightPx, label, opts)`**
Thin-stroke lattice tower: tapered rails, cross bracing, a dipole at the top, a footing, and a
dimensioned height when `label` is given. `opts`: `{side: 'left'|'right', gap, colour, size}`.
`heightPx` is pixels — derive it as `P.Y(0) − P.Y(heightInMetres)` so it scales with the plot.

**`dish(g, x, y, r, angle, opts)`**
Reflector arc, feed struts, feed horn, rear mount, dashed boresight. `angle` is the boresight in
radians, `(x, y)` is the feed. `opts`: `{colour, axisLine}`.

**`fmtEng(value, unit, decimals) → string`**
`fmtEng(1500, 'm', 1)` → `1.5 km`; `fmtEng(1500, 'km', 0)` → `1 500 km` (thin space);
`fmtEng(-3.6, 'dB', 1)` → `−3.6 dB` (true minus, non-breaking unit space);
`fmtEng(2.4e9, 'Hz', 2)` → `2.40 GHz`; `fmtEng(NaN, 'dB', 1)` → `—`.
SI prefixes are applied only to base units (`m Hz s W V A F H Ω J N Pa bit/s b/s B/s Sa/s sps
bd rad`); dB-family units and already-prefixed units are never re-scaled. Use it for every
number that reaches the DOM or the canvas. `fmtNum(x, dec)` is the same without a unit.

**`sup(str)` / `sub(str)`**
Unicode super/subscripts for canvas text: `'10' + sup('-3')` → `10⁻³`, `'f' + sub('s')` → `fₛ`.
Characters with no unicode form (subscript `b c d f g q y z`) pass through unchanged, so write
`'E' + 'b/N' + sub('0')` → `Eb/N₀` on canvas and the proper `E<sub>b</sub>/N<sub>0</sub>` in HTML.

**`bindPair(rangeEl, numEl, cb)`**
Wires a range to its number input in both directions and calls `cb(value)` on every change.
Typing an out-of-range value is clamped on blur, not while typing.

### The canonical draw function

Copy this shape for every canvas.

```js
  function drawLoss() {
    const c = document.getElementById('cLoss'), wh = fit(c), w = wh[0], h = wh[1];
    const g = c.getContext('2d'), t = theme();

    const P = graticule(g, { x: 0, y: 0, w: w, h: h },
      { min: 0.05, max: 100, unit: 'km', label: 'distance', log: true },
      { min: -140, max: -40, unit: 'dBm', label: 'received power' });

    band(g, P, P.Y(-140), P.Y(SENS), t.bad, 'y');      // region that fails

    P.clip(g);                                          // keep curves inside the frame
    g.strokeStyle = t.s1; g.lineWidth = 2;
    g.beginPath();
    for (let px = P.x0; px <= P.x1; px++) {
      const f = (px - P.x0) / P.w;
      const d = Math.pow(10, Math.log10(0.05) + f * (Math.log10(100) - Math.log10(0.05)));
      const y = P.Y(prx(d));
      if (px === P.x0) g.moveTo(px, y); else g.lineTo(px, y);
    }
    g.stroke();
    g.strokeStyle = t.bad; g.lineWidth = 1.4; g.setLineDash([6, 4]);
    g.beginPath(); g.moveTo(P.x0, P.Y(SENS)); g.lineTo(P.x1, P.Y(SENS)); g.stroke();
    g.setLineDash([]);
    P.unclip(g);

    leader(g, P.X(D), P.Y(prx(D)), 'you are here, ' + fmtEng(prx(D), 'dBm', 1),
           { box: P, colour: t.s2 });
    leader(g, P.x1, P.Y(SENS), 'sensitivity ' + fmtEng(SENS, 'dBm', 0),
           { box: P, colour: t.bad, dx: -30, dy: 26 });
  }
```

Scale drawing, same shape — the physical picture the reader meets first:

```js
  function drawScene() {
    const c = document.getElementById('cScene'), wh = fit(c), w = wh[0], h = wh[1];
    const g = c.getContext('2d'), t = theme();
    const P = graticule(g, { x: 0, y: 0, w: w, h: h },
      { min: 0, max: D, unit: 'km', label: 'ground range' },
      { min: 0, max: Math.max(60, H1 * 1.6), unit: 'm', label: 'height' });
    const gy = P.Y(0);

    mast(g, P.X(D * 0.08), gy, gy - P.Y(H1), fmtEng(H1, 'm', 0));
    mast(g, P.X(D * 0.92), gy, gy - P.Y(H2), fmtEng(H2, 'm', 0), { side: 'right' });
    g.strokeStyle = t.s1; g.lineWidth = 1.8;
    g.beginPath(); g.moveTo(P.X(D * 0.08), P.Y(H1)); g.lineTo(P.X(D * 0.92), P.Y(H2)); g.stroke();
    leader(g, P.X(D * 0.5), P.Y((H1 + H2) / 2), 'direct ray', { box: P, dy: -34 });
  }
```

Line discipline, non-negotiable: data 1.5–2 px, gridlines 0.5 px (`graticule` does it),
annotations and hardware 1–1.2 px, dashes `[6, 4]` for thresholds and `[4, 3]` for construction
lines. No shadows, no rounded blob strokes, no gradients, no emoji, no decorative curves.

---

## 3 · The standard page skeleton

Exact order. Anything not on this list does not belong on the first screen.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tool name</title>
<style>
/* ---- block 1, verbatim ---- */
</style>
</head>
<body>
<div class="wrap">

<header class="full">
  <p style="margin: 0 0 0.7rem;"><a class="back" href="../index.html">&larr; all tools</a></p>
  <h1>Tool name</h1>
  <p class="sub">What the thing is, in one sentence. Why an engineer cares, in a second one.</p>
  <p class="prereq">New to decibels? Start with <a href="link-budget.html">link budget</a>.</p>
</header>

<div class="rail">

  <div class="hero">
    <div class="lbl">Fade margin</div>
    <div class="val" id="heroVal">&minus;84.2<span class="u">dBm</span></div>
    <span class="badge good" id="heroBadge">link closes</span>
    <div class="ft" id="heroFt">12.4 dB above the noise floor</div>
  </div>

  <div>
    <div class="ctl">
      <label for="ds">Path length</label>
      <div class="in">
        <input type="range" id="ds" min="0.1" max="60" step="0.1" value="12">
        <input type="number" id="dsN" min="0.1" max="60" step="0.1" aria-label="Path length in kilometres">
        <span class="unit">km</span>
      </div>
    </div>
    <div class="ctl">
      <label for="fq">Frequency</label>
      <div class="in">
        <input type="range" id="fq" min="0.1" max="40" step="0.1" value="2.4">
        <input type="number" id="fqN" min="0.1" max="40" step="0.1" aria-label="Frequency in gigahertz">
        <span class="unit">GHz</span>
      </div>
    </div>
    <div class="ctl">
      <label for="ht">Mast height</label>
      <div class="in">
        <input type="range" id="ht" min="3" max="120" step="1" value="30">
        <input type="number" id="htN" min="3" max="120" step="1" aria-label="Mast height in metres">
        <span class="unit">m</span>
      </div>
    </div>

    <div class="presets">
      <span class="lbl">Presets</span>
      <button type="button" id="pWifi" class="on">Wi-Fi 2.4 GHz</button>
      <button type="button" id="pGsm">GSM 900</button>
      <button type="button" id="pFm">FM broadcast</button>
    </div>
  </div>

  <details>
    <summary>More controls</summary>
    <div class="ctl">
      <label for="nf">Receiver noise figure</label>
      <div class="in">
        <input type="range" id="nf" min="0.5" max="12" step="0.5" value="5">
        <input type="number" id="nfN" min="0.5" max="12" step="0.5" aria-label="Receiver noise figure in decibels">
        <span class="unit">dB</span>
      </div>
    </div>
  </details>

  <div class="cards">
    <div class="card">
      <div class="hd">EIRP</div>
      <div class="big" id="cEirp">&mdash;</div>
      <div class="ft">what leaves the antenna</div>
    </div>
    <div class="card">
      <div class="hd">Free-space loss</div>
      <div class="big" id="cFsl">&mdash;</div>
      <div class="ft" id="cFslFt">&mdash;</div>
    </div>
  </div>

</div>

<div class="stage">

  <div class="tour">
    <span class="lbl">Guided tour</span>
    <button type="button" id="t1">1 &middot; a short hop</button>
    <button type="button" id="t2">2 &middot; go further</button>
    <button type="button" id="t3">3 &middot; add dishes</button>
    <button type="button" id="t0">reset</button>
  </div>
  <p class="tour-note" id="tourNote">Press the steps in order; each one moves the controls.</p>

  <p class="sec"><b>1 &middot; The scene</b> <span>&mdash; two sites, drawn to scale</span></p>
  <canvas id="cScene" class="cv-hero"></canvas>
  <ul class="legend-note">
    <li><span class="sw" style="background:var(--series-1)"></span>direct ray</li>
    <li><span class="sw" style="background:var(--series-2)"></span>ground reflection</li>
    <li><span class="sw" style="background:var(--bad)"></span>shaded &mdash; no clearance</li>
  </ul>

  <p class="sec"><b>2 &middot; Received power vs distance</b> <span>&mdash; where the margin runs out</span></p>
  <canvas id="cLoss" class="cv-sub"></canvas>
  <ul class="legend-note">
    <li><span class="sw" style="background:var(--series-1)"></span>received power</li>
    <li><span class="sw dash" style="color:var(--bad)"></span>sensitivity</li>
  </ul>

  <details>
    <summary>Worked example, with the current numbers</summary>
    <ol class="work" id="work"></ol>
  </details>

  <details>
    <summary>Glossary</summary>
    <dl class="glossary">
      <dt>dBm</dt><dd>Power compared with 1 milliwatt, in dB. 0 dBm = 1 mW.</dd>
    </dl>
  </details>

  <p class="prereq" style="margin-top:1rem">Next: <a href="fresnel-clearance.html">Fresnel clearance</a>.</p>

</div>
</div>

<script>
(function () {
  /* ---- block 2, verbatim ---- */

  const $ = id => document.getElementById(id);
  const S = { d: 12, f: 2.4, h: 30, nf: 5 };

  function drawScene() { /* fit → theme → graticule → mast/dish → leader/dimension */ }
  function drawLoss()  { /* fit → theme → graticule → band → curve → leader */ }

  function update() {
    /* hero + cards + worked example, every number through fmtEng */
    drawScene(); drawLoss();
  }

  bindPair($('ds'), $('dsN'), v => { S.d = v; update(); });
  bindPair($('fq'), $('fqN'), v => { S.f = v; update(); });
  bindPair($('ht'), $('htN'), v => { S.h = v; update(); });
  bindPair($('nf'), $('nfN'), v => { S.nf = v; update(); });
  window.addEventListener('resize', update);
  update();
})();
</script>
</body>
</html>
```

Word budget, enforced (from `STYLE.md`): intro 2 sentences / ~35 words; section explainer ≤10
words; legend line ≤6 words; tour narration ≤14 words; card footnote ≤8 words. Anything longer
goes inside a collapsed `<details>`. No closing essay.

---

## 4 · Migration checklist — converting one existing tool

Work top to bottom. Do not skip step 0.

0. **Read the whole file first**, and note every canvas id, every slider id, and every place a
   colour or a pixel offset is hardcoded. Keep the physics untouched; check any formula you move
   against `.research/propagation.md`, `link-noise.md`, `signals.md`, `cellular.md`, `antennas.md`.
1. **Replace the `<style>` block** with block 1, entire. Delete the old `:root`, the old
   `max-width: 760px` body rule, and any bespoke `.grid2` / `.btnrow` / `.steps` / `.note` rules
   the new block already covers.
2. **Rewrap the body**: `.wrap` > `header.full` + `.rail` + `.stage`. Move the hero readout,
   the 3–4 primary controls, the preset row and the cards into `.rail`; leave section headings,
   canvases and legends in `.stage`. Expert controls go in a collapsed `<details>` in the rail.
3. **Canvas sizing.** Delete every `style="height: NNNpx"` and every `height=` attribute.
   Primary canvas → `class="cv-hero"`; every other → `class="cv-sub"`; two canvases meant to be
   compared → wrap in `<div class="cv-pair">`. Nothing else changes; `fit()` already follows CSS.
4. **Paste block 2** at the top of the IIFE and delete the tool's own `fit`, `axes`, `tag`,
   `dashLine`, `cvv`, `fnt` and any local tick/format helpers. Repoint their call sites:
   `cvv('--series-1')` → `t.s1`, `fnt(11)` → `t.font(11)`, `tag(...)` → `leader(...)`.
5. **Re-derive every drawing constant into fractions.** This is the step that makes the tool
   work at every aspect ratio, and the one most often skipped:
   - `const l = 52, r = 12, t = 14, b = 42;` → delete; `graticule` computes its own margins.
   - `g.fillText(label, 120, 40)` → `g.fillText(label, P.x0 + P.w * 0.18, P.y0 + P.h * 0.12)`,
     or better, `leader(g, P.X(value), P.Y(value), label, { box: P })`.
   - `g.arc(x, y, 5, …)` → `g.arc(x, y, Math.max(2.5, Math.min(6, P.h * 0.014)), …)`.
   - font sizes: `fnt(11)` → `t.font(P.fs)` inside a plot, so small canvases shrink text once,
     consistently.
   - scene geometry: mast heights, ranges and offsets come from `P.X()` / `P.Y()` of real
     physical values, never from `w * 0.5 + 30`.
6. **Rebuild each plot on `graticule`.** Every axis gets `label` and `unit`. Log axes get
   `log: true` instead of hand-rolled `L10` mapping. Delete hand-drawn axis lines and manual
   tick loops.
7. **Annotate.** At least two `leader()` labels per canvas naming the feature that matters, and
   `dimension()` on every physical length in a scale drawing. Replace any cute illustration
   (stick figures, cars, houses, smiley props) with `mast()` / `dish()` / plain thin-stroke
   rectangles.
8. **Controls.** Every primary slider gains a number input and `bindPair()`; the old
   `<span class="v">` readouts are deleted (the number input *is* the readout). Add 3–5 preset
   buttons for recognisable real cases. Keep at most 3–4 controls outside `<details>`.
9. **Hero readout.** One `.hero` with the tool's key number and a `good`/`warn`/`bad` badge
   driven by the real threshold. Update it in the same function that updates the cards.
10. **Numbers and text.** Every number through `fmtEng`/`fmtNum` or `.toFixed(n)`. Then run the
    section 5 table over the whole file, HTML and canvas strings alike.
11. **Trim the words** to the budget. Move analogies, worked examples and glossary into
    collapsed `<details>`. Delete the closing essay paragraph if one survives.
12. **Delete on sight**: the old `:root` palette, `max-width: 760px`/`820px`, fixed canvas
    heights, local `fit`/`axes`/`cvv` copies, `getComputedStyle` calls inside a loop, hardcoded
    hex colours, `Title Case` labels, hyphen-minus in numbers, `.v` readout spans, decorative
    scene props, any second intro paragraph.
13. **Check both themes and four widths** (375, 768, 1366, 1920): no horizontal scroll, no text
    smaller than ~9.5 px, no element that vanishes in one theme, no `NaN`/`undefined`/`Infinity`
    in the DOM at any slider extreme.

---

## 5 · Typography conversion table

Apply to HTML *and* to every string drawn on canvas.

| Find | Replace with | Note |
| --- | --- | --- |
| `-3.5`, `-174 dBm` (hyphen-minus in a number) | `−3.5`, `−174 dBm` (U+2212) | `fmtNum`/`fmtEng` do this for you |
| `1500 km`, `1,500 km` | `1 500 km` (U+2009 thin space) | never a comma |
| `3.6dB`, `15kHz` | `3.6 dB`, `15 kHz` | U+00A0 between number and unit |
| `x`, `*` as multiply | `·` for products, `×` for "times" and ratios (`2 × 2`) | `20·log₁₀(d)` |
| `f_s`, `fs` | `f<sub>s</sub>` / canvas `'f' + sub('s')` → `fₛ` | |
| `Eb/N0`, `Eb/No` | `E<sub>b</sub>/N<sub>0</sub>` / canvas `'Eb/N' + sub('0')` | subscript `b` has no glyph |
| `10^-3`, `1e-3` | `10<sup>−3</sup>` / canvas `'10' + sup('-3')` → `10⁻³` | |
| `lambda`, `theta`, `sigma`, `beta`, `phi`, `mu`, `ohm`, `deg` | `λ θ σ β φ µ Ω °` | µ is U+00B5 |
| `dB/km`, `dBm/Hz` | unchanged, but always with the unit space before them | `−174 dBm/Hz` |
| `d`, `f`, `n`, `k` as variables in prose | `<span class="var">d</span>` (italic) | single letters only; never italicise units |
| `SNR`, `QPSK`, `FM`, `GSM`, `Wi-Fi` | unchanged | acronyms and proper nouns keep their caps |
| `Guided Tour`, `Reset`, `Link OK` | `Guided tour`, `Reset` → `reset`, `Link closes` | sentence case: buttons, badges, labels, headings, canvas text |
| `Tx Power`, `Noise Figure` | `Tx power`, `Noise figure` | first word capitalised only |
| `ALIASED`, `BELOW SENSITIVITY` | `Aliased`, `Below sensitivity` | badges are sentence case, never caps |
| `1.0e-6 s` | `1.0 µs` via `fmtEng(1e-6, 's', 1)` | engineering prefixes, not exponent notation |
| `2.4GHz` in a preset button | `Wi-Fi 2.4 GHz` | presets name the real case |
| `--` / `-` as a dash | `—` (em dash) in `.sec` explainers, `–` in ranges (`10–20 dB`) | |
| `0.30000000004` | `.toFixed(n)` or `fmtEng(…)` | one precision per quantity, everywhere |

Canvas-specific: unicode sub/superscripts available are `₀₁₂₃₄₅₆₇₈₉₊₋` `ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ` and
`⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿⁱ`. Anything else is written plain — do not fake it with a smaller font.

---

## 6 · Self-check before you call a tool done

- Title → hero number → annotated plot tells the story with no paragraph read.
- Every canvas has a graticule with labelled ticks **and units on both axes**, or is a scale
  drawing with dimension arrows.
- Every canvas has ≥2 on-canvas labels with leader lines, and a `.legend-note` beneath.
- Zero colour literals in the JS. `grep` for `#` inside `<script>` returns nothing.
- Zero fixed canvas heights. `grep` for `height:` inside a canvas tag returns nothing.
- Sliders at both extremes: no `NaN`, no `Infinity`, no `undefined`, no overlapping labels.
- Light and dark both checked. 375 px and 1920 px both checked, no horizontal scroll.
- Word budget respected; glossary, worked example and analogy collapsed.
