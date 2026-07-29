# Antennas: patterns, gain, beamwidth, sidelobes, polarisation, VSWR, boresight

Research note for building interactive teaching tools. Every number below is either quoted
from a source (cited inline) or computed in this session (marked `[computed]`, with the exact
defining equation shown so it can be re-derived).

Source shorthand:

- **[P5 p.N]** = `C:\Users\yongw\Downloads\IE4155 Part 5 AY24-25 (1).pdf`, PDF page N (76 pages).
  Extracted with `pdftotext -layout -f 41 -l 64`. Pages 41–64 carry slide footers 40–63,
  so **PDF page N = slide footer N−1**.

Extraction caveat: [P5 p.45] (the gain / effective-area table) loses its column alignment in
text extraction — the numbers arrive as a scrambled block. The reconstruction in §9 was
verified by checking every cell against `G = 4πA_e/λ²`; all six rows close to within the
table's own rounding. The pattern diagrams on [P5 p.43] and [P5 p.46] are bitmaps and
return no text. Maths glyphs (λ, π, superscripts, division bars) are lost throughout, so
every formula below comes from the web sources or from first principles, not from the slide
text, and is cross-checked numerically.

The course notes contain very little antenna theory — essentially two facts (the dish HPBW
rule and the gain/aperture table). Everything else here is web-sourced or computed.

Verification scripts, saved next to this note and re-runnable (`numpy` + `scipy` only):

- `.research\antennas-verify.py` — patterns, directivities, beamwidths, line and circular
  apertures, arrays, scan broadening, grating lobes, VSWR, the course gain table
- `.research\antennas-verify-polarisation.py` — polarisation loss factor, all limiting cases
- `.research\antennas-verify-taper.py` — continuous aperture tapers and discrete array windows

Every value marked `[computed]` below is printed by one of those three scripts. If a build
agent changes a constant, re-run them rather than trusting this document.

---

## 0. Conventions used throughout

- **θ** is measured from the antenna's own axis (the wire, for a dipole). For a vertical
  dipole θ = 90° is the horizon, θ = 0° is straight up along the wire.
- **F(θ)** is the *normalised field* pattern, peak value 1. The *power* pattern is `|F(θ)|²`.
  Half-power (−3 dB) is `|F|² = 0.5`, i.e. `|F| = 1/√2 = 0.7071`.
- Pattern in dB: `20·log10|F|` = `10·log10|F|²`. Both give the same dB number. A tool must
  not apply `20·log10` to a quantity that is already a power.
- **D** = directivity (dimensionless), `G = η·D` where η is radiation efficiency.
  `G(dBi) = 10·log10(G)`. Isotropic gain = 1 = 0 dBi [P5 p.45].
- For a pattern with no φ dependence,
  `D = 2 / ∫₀^π |F(θ)|² sin θ dθ` — this is how every directivity below was computed.

---

## 1. Normalised field patterns

### 1.1 Isotropic radiator

```
F(θ, φ) = 1                     for all θ, φ
D = 1  =  0 dBi                 (exact, by definition)
```

Has no beam, no beamwidth, no sidelobes and no polarisation. It is a reference, not a
buildable antenna. `A_e = λ²/4π`.

### 1.2 Hertzian (infinitesimal / short) dipole

```
F(θ) = sin θ                    0 ≤ θ ≤ π
power pattern = sin²θ
```

Doughnut shaped, null along the wire axis, maximum broadside.

| Quantity | Value | Source |
|---|---|---|
| Directivity | 1.5 exactly | `[computed]` D = 2/∫sin³θ dθ = 2/(4/3) = 1.5; also stated by [Wikipedia — Dipole antenna](https://en.wikipedia.org/wiki/Dipole_antenna) |
| Gain | **1.7609 dBi** | `[computed]` 10·log10(1.5) = 1.76091 |
| HPBW | **90.0°** exactly (edges at θ = 45° and 135°) | `[computed]` sin²θ = 0.5 → θ = 45°, 135° |

The short dipole is the "even a bad antenna is not isotropic" case: 1.76 dBi is the floor,
not zero.

### 1.3 Half-wave dipole — the canonical form

```
            cos( (π/2)·cos θ )
F(θ)  =  ─────────────────────        0 < θ < π
                 sin θ

F(θ) → 0 as θ → 0 or π      (removable 0/0 — see the code note below)
```

This is the exact form the task asks for, and it is what [Wikipedia — Dipole
antenna](https://en.wikipedia.org/wiki/Dipole_antenna) states: "cos((π/2)cos θ)/sin θ".

**Code note (this bites every implementation):** at θ = 0 and θ = π both numerator and
denominator vanish. The true limit is **0**, not 1 and not NaN. Guard it:

```js
const s = Math.sin(theta);
const F = Math.abs(s) < 1e-9 ? 0 : Math.cos(Math.PI / 2 * Math.cos(theta)) / s;
```

| Quantity | Value | Source |
|---|---|---|
| Directivity | **1.640922** | `[computed]` D = 2/∫₀^π F² sin θ dθ |
| Gain | **2.1509 dBi** (quote as **2.15 dBi**) | `[computed]` 10·log10(1.640922) = 2.150880 |
| HPBW | **78.08°** (quote as **78°**); −3 dB edges at θ = 50.96° and 129.04° | `[computed]` solve F² = 0.5 |
| Radiation resistance | **73.1 Ω** | [Wikipedia — Dipole antenna](https://en.wikipedia.org/wiki/Dipole_antenna) |

Wikipedia independently states directivity "1.64" / "2.15 dBi", HPBW "78 degrees" and
"73.1 Ω" — the computed values agree.

The pattern is only slightly narrower than the short dipole (78° vs 90°) but the *shape* is
visibly less round: it is flatter on top and pinches harder toward the wire.

### 1.4 Quarter-wave monopole over a ground plane

Same field expression as the half-wave dipole, but existing **only in the upper
hemisphere**; the ground plane image supplies the missing half.

```
            cos( (π/2)·cos θ )
F(θ)  =  ─────────────────────        0 ≤ θ < π/2      (above the ground plane)
                 sin θ

F(θ)  =  0                            π/2 < θ ≤ π      (below — no radiation)
```

θ measured from the monopole rod (zenith); θ = 90° is along the ground plane.

Because the same input power now fills half the solid angle, directivity **doubles**:

| Quantity | Value | Source |
|---|---|---|
| Directivity | **3.28184** = 2 × 1.640922 | `[computed]` |
| Gain | **5.161 dBi** | `[computed]` 10·log10(3.28184) = 5.16118 |
| Increase over the half-wave dipole | **+3.01 dB** exactly | `[computed]` 10·log10(2) |
| Radiation resistance | **36.5 Ω** (half of 73) | [Wikipedia — Monopole antenna](https://en.wikipedia.org/wiki/Monopole_antenna) |

[Wikipedia — Monopole antenna](https://en.wikipedia.org/wiki/Monopole_antenna) states the
gain "is twice (or in decibels, 3 dB greater than) the gain of an equivalent dipole" and
gives 36.5 Ω.

**Discrepancy to be aware of, do not paper over it:** the Wikipedia dipole page quotes the
quarter-wave monopole as **5.19 dBi**, whereas doubling the exact dipole directivity gives
**5.161 dBi**. Values of 5.15–5.19 dBi all appear in the literature depending on rounding
chain. Use **5.16 dBi** (it is the one that is internally consistent with 2.15 dBi + 3.01 dB)
and, if the tool displays it, note that references vary in the last digit.

All of the above assumes an **infinite, perfectly conducting** ground plane. A real finite
ground plane tilts the peak upward off the horizon and fills in the lower hemisphere — say so
rather than pretending the null below is real.

### 1.5 Uniform line source / rectangular aperture — the sinc form

Uniform illumination over a line of length `L`:

```
           sin u                        π L
F(θ)  =  ─────── ,          u  =  ───────── · sin θ
             u                          λ

F(0) = 1        (limit of sin u / u as u → 0 — guard this in code)
```

For a **rectangular aperture** `L_x × L_y` the two axes separate:

```
F(θ, φ) = [sin u / u] · [sin v / v]

u = (π L_x / λ)·sin θ cos φ          v = (π L_y / λ)·sin θ sin φ
```

**Beware the two sinc conventions.** This is the *unnormalised* `sin(u)/u`. Many libraries
define `sinc(x) = sin(πx)/(πx)`. In that convention `F = sinc( (L/λ)·sin θ )`. Pick one,
state it in a comment, and do not mix them — mixing produces a beam that is π times too
wide or too narrow.

| Quantity | Value | Source |
|---|---|---|
| First null | at `u = π`, i.e. **sin θ = λ/L** | `[computed]` sin u = 0 |
| Null-to-null beamwidth | `2·arcsin(λ/L)` ≈ **114.6·λ/L degrees** for small angles | `[computed]` 2·(180/π) = 114.59 |
| −3 dB half-argument | `u₃ = 1.3915574` (where sin u/u = 1/√2) | `[computed]` |
| **HPBW** | **0.88589 λ/L radians = 50.758 λ/L degrees** | `[computed]` 2·u₃/π = 0.885893 |
| **First sidelobe** | **−13.26 dB** (peak at `u = 4.49341`, the first root of tan u = u) | `[computed]` 20·log10(sin u/u) = −13.2615 |
| Second sidelobe | −17.83 dB (at u = 7.72525) | `[computed]` |
| Directivity, uniform aperture area A | `D = 4πA/λ²` | see §2 |

The famous **0.886** and **−13.2 dB** both come from this one function. The −13.26 dB
sidelobe is a property of the *rectangle* (uniform illumination), not of any particular
antenna — it is the same number for a uniformly-fed slot, a uniformly-fed array, and an
unwindowed FFT.

Corroboration: [Analog Devices — Phased Array Antenna Patterns Part 3](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part3.html)
states uniform illumination "has −13.2 dB first sidelobes" and that the first sidelobe is at
"−13 dBc regardless of the element count due to the sinc function in the array factor"
*(search-result summary — direct fetch timed out, see Sources)*.

### 1.6 N-element uniform linear array — the array factor

```
                 sin( N ψ / 2 )                        2π d
AF(ψ)  =  ───────────────────────── ,        ψ  =  ───────── · sin θ  +  β
                 N · sin( ψ / 2 )                        λ
```

- `N` = number of elements, `d` = element spacing, `β` = progressive inter-element phase.
- Normalised so `AF = 1` at `ψ = 0`. `AF` is a **field** pattern; power is `AF²`.
- **Beam steering:** to put the main beam at `θ₀`, set `β = −(2π d/λ)·sin θ₀`. Then
  `ψ = (2π d/λ)(sin θ − sin θ₀)`, which is zero at `θ = θ₀`.
  [Wikipedia — Phased array](https://en.wikipedia.org/wiki/Phased_array) gives the planar
  form `β_x = −k d_x sin θ₀ cos φ₀`.
- **Total pattern = element pattern × array factor** (pattern multiplication). A tool that
  plots only `AF` and calls it the antenna pattern is wrong at wide angles; say which one is
  being shown.

**Code note:** at `ψ = 0` (and at `ψ = 2πm`) the denominator vanishes. The limit is **1**:

```js
const den = N * Math.sin(psi / 2);
const AF = Math.abs(den) < 1e-9 ? 1 : Math.sin(N * psi / 2) / den;
```

Computed behaviour, `d = λ/2`, broadside `[computed]`:

| N | exact HPBW | `0.886 λ/(N d)` estimate | first sidelobe |
|---|---|---|---|
| 2 | 60.00° | 50.76° | −3.01 dB (a shoulder, not a true sidelobe) |
| 4 | 26.32° | 25.38° | −11.30 dB |
| 8 | 12.80° | 12.69° | −12.80 dB |
| 16 | 6.36° | 6.35° | −13.15 dB |
| 32 | 3.174° | 3.173° | −13.23 dB |
| 64 | 1.586° | 1.586° | −13.25 dB |

Two things a tool must get right from this table:

1. The sidelobe level **converges to −13.26 dB from below** as N grows. It is **not**
   −13.2 dB for small N. At N = 4 it is −11.3 dB. Hard-coding −13.2 for every N is a lie
   the plot itself will contradict.
2. The `0.886 λ/(N d)` formula is a small-angle approximation. It is within 0.5 % for
   N ≥ 16 but **9 % wrong at N = 4** and **18 % wrong at N = 2**. For small arrays, solve
   `AF² = 0.5` numerically instead.

---

## 2. Gain, directivity and effective aperture

### 2.1 The core relation

```
        4 π A_e                              G λ²
G  =  ───────────           ⟺        A_e  =  ───────
          λ²                                  4 π
```

This is the relation printed in the course notes as "Antenna Gain along the direction of
Main Lobe" [P5 p.45] (the λ² and 4π glyphs are lost in extraction; the numeric table on the
same page confirms the form to within its rounding — see §9).

Also confirmed by [Friis equation and antenna effective area — Circuit Design
Inc.](https://www.cdt21.com/design_guide/friis-equation-and-antenna-effective-area/) and
[Friis Transmission Equation — Physics LibreTexts](https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Electromagnetics_II_(Ellingson)/10:_Antennas/10.14:_Friis_Transmission_Equation):
"The relation between effective area A and gain G of an antenna is: G = 4πA/λ²."

Consequences worth putting on screen:

- An **isotropic** antenna has `A_e = λ²/4π`. It is not zero. At 1 GHz that is 0.00716 m².
- `A_e` is an *effective* area, related to the physical aperture by the **aperture
  efficiency**: `A_e = η_ap · A_phys`. A dish at 56 % efficiency [P5 p.45] captures 56 % of
  the power falling on its mouth.
- **Gain rises as f²** for a fixed physical aperture. The same 2 m dish is 24 dBi at 1 GHz
  and 64 dBi at 100 GHz. This is the single most counter-intuitive fact in the course table
  and is worth an explicit animation.

### 2.2 Directivity summary, all six reference antennas

| Antenna | Normalised field pattern | D (linear) | D (dBi) | HPBW |
|---|---|---|---|---|
| Isotropic | `1` | 1 | **0.00** | none |
| Hertzian dipole | `sin θ` | 1.5 | **1.7609** | **90.00°** |
| Half-wave dipole | `cos((π/2)cos θ)/sin θ` | 1.640922 | **2.1509** | **78.08°** |
| λ/4 monopole (∞ ground) | same, upper half only | 3.281845 | **5.1612** | 39.04° in elevation (half of 78.08°, measured from the horizon up) |
| Uniform line source, length L | `sin u / u` | — (see note) | — | **50.758 λ/L degrees** |
| Uniform rectangular aperture A | `(sin u/u)(sin v/v)` | `4πA/λ²` | `10log10(4πA/λ²)` | 50.758 λ/L per axis |
| N-element ULA, `d = λ/2`, uniform | `sin(Nψ/2)/(N sin(ψ/2))` | ≈ N (broadside) | `≈ 10log10 N` | **≈ 0.886 λ/(N d) rad** |

All values in the D and dBi columns `[computed]`.

Note on the line source: a 1-D line source has no directivity on its own — directivity needs
a 2-D aperture. Quote `4πA/λ²` only for an aperture with an area.

The `D ≈ N` result for a half-wave-spaced uniform array is the useful mental model: **every
doubling of element count buys 3 dB**, and it costs the beamwidth halving.

---

## 3. Beamwidth

### 3.1 The course dish rule

```
HPBW (degrees)  =  22 / ( F_GHz · D_metres )                    [P5 p.44]
```

Quoted verbatim from the slide: "3dB Antenna Half power Beamwidth ( ) HPBW= 22/(F GHz D
meters) for dish".

### 3.2 The general aperture rule

```
HPBW (degrees)  ≈  70 · λ / D
```

[Search-result summary](https://prepp.in/question/the-approximate-3-db-beam-width-for-a-parabolic-an-6846c1f2e4d5b7dc0489462d):
"θ ≈ 70λ/D … for a 'typical' parabolic antenna, K = 70 when θ is in degrees. However, the
'70' constant actually varies from 65 to 75 depending on design." The constant depends on
aperture efficiency and feed illumination taper — see §4, where the taper table shows exactly
why (a cosine taper widens the beam by 1.34×).

### 3.3 How the two rules relate — do not claim they are identical

With `λ = 0.3 / F_GHz` metres:

```
70 λ / D  =  70 × 0.3 / (F_GHz · D_m)  =  21 / (F_GHz · D_m)
```

So the course's `22` corresponds to a constant of **73.3 λ/D**, and the two rules differ by
**22/21 = 1.048, i.e. the course rule is always 4.8 % wider**. `[computed]`

| f | D | `22/(F·D)` (course) | `70λ/D` |
|---|---|---|---|
| 1 GHz | 2.0 m | **11.00°** | 10.50° |
| 6 GHz | 1.2 m | **3.06°** | 2.92° |
| 12 GHz | 0.6 m | **3.06°** | 2.92° |
| 14 GHz | 3.0 m | **0.52°** | 0.50° |

All `[computed]`. Both are rules of thumb for a *tapered* real dish; neither is the
diffraction limit. The theoretical **uniform circular aperture** value is **58.96 λ/D**
`[computed]`, §3.6 — a real dish is always wider than that because its feed
under-illuminates the rim. That gap between 58.96 and 70 is precisely the taper penalty of
§4, and it is worth showing the two side by side.

A tool should let the user pick which constant is in use and show both, rather than silently
choosing one.

### 3.6 Uniform circular aperture (a dish) — different constants from the line source

A circular aperture of diameter D is **not** the sinc case. Its pattern is the Airy function:

```
            2 J₁(u)                       π D
F(θ)  =  ───────────── ,        u  =  ───────── · sin θ         J₁ = Bessel, first kind
                u                          λ

F(0) = 1        (limit — guard it)
```

| Quantity | Value | Source |
|---|---|---|
| −3 dB half-argument | `u₃ = 1.61634` | `[computed]` |
| **HPBW** | **1.0290 λ/D rad = 58.96 λ/D degrees** | `[computed]` 2·u₃/π |
| First null | `u = 3.83171` → sin θ = **1.22 λ/D** | `[computed]` first zero of J₁ |
| **First sidelobe** | **−17.57 dB** (at u = 5.1356) | `[computed]` |

**This is the trap in dish tools.** The famous **−13.26 dB** sidelobe belongs to the
*rectangular / line* aperture. A **circular** aperture — every parabolic dish in the course
— has a **−17.6 dB** first sidelobe even with perfectly uniform illumination, and its first
null is at 1.22 λ/D, not λ/D. Using −13.26 dB for a dish is wrong by 4.3 dB.

(Some references quote the circular HPBW as 1.02 λ/D = 58.4°; the exact Airy FWHM is
1.0290 λ/D = 58.96°. The 1.02 is a rounding, not a different model.)

### 3.4 Array beamwidth, including scan broadening

```
                      0.886 · λ
HPBW  ≈  ───────────────────────────────       radians
              N · d · cos θ_scan

              50.76 · λ
       =  ─────────────────────────            degrees
            N · d · cos θ_scan
```

The `1/cos θ_scan` factor is the **projected aperture**: viewed from θ_scan off broadside,
an aperture of length `L` looks only `L·cos θ_scan` long, so the beam it makes is
correspondingly wider. [MathWorks — arrayscanloss](https://www.mathworks.com/help/radar/ref/arrayscanloss.html)
names this directly: "beam broadening due to the reduced projected array area in the beam
direction."

Accuracy of the `1/cos` model, checked against the exact array factor `[computed]`,
N = 16, d = λ/2, broadside HPBW = 6.359°:

| scan angle | exact HPBW | `HPBW₀/cos θ` | model error |
|---|---|---|---|
| 0° | 6.359° | 6.359° | 0.00 % |
| 30° | 7.349° | 7.342° | 0.09 % |
| 45° | 9.025° | 8.993° | 0.36 % |
| 60° | **12.993°** | 12.717° | 2.2 % |

The `1/cos` law is excellent to 45° and starts to under-predict past 60°. If a tool scans
past 60° it should compute the exact edges rather than scale the broadside value.

**Exact array HPBW** (use when N is small or the scan is wide): solve
`AF²(ψ₃) = 0.5` for `ψ₃ ∈ (0, 2π/N)`, then

```
HPBW  =  arcsin( sin θ_scan + ψ₃·λ/(2π d) )  −  arcsin( sin θ_scan − ψ₃·λ/(2π d) )
```

Guard both `arcsin` arguments to [−1, 1]; past a certain scan the −3 dB edge runs off the
visible region and the beam is clipped by the horizon, not by the array.

### 3.5 Scan loss

Broadening is only half of the story. The gain also falls, from two causes:
[MathWorks — arrayscanloss](https://www.mathworks.com/help/radar/ref/arrayscanloss.html):
"The first effect is the beam broadening due to the reduced projected array area in the beam
direction. The second effect is a reduction of the effective aperture area of the individual
array elements at off-broadside angles."

Standard model: `G(θ) = G₀ · cos^n(θ_scan)`, with **n between 2 and 3, default 2.5**
(MathWorks). `n = 1` is the pure projected-aperture case; the extra comes from the element
pattern. Scan loss in dB = `10·n·log10(cos θ_scan)`. A tool must state which `n` it used.

---

## 4. Sidelobes and tapering

### 4.1 The uniform baseline

A uniformly illuminated aperture gives the **maximum possible gain** for its size — and the
**worst sidelobes**: **−13.26 dB** first sidelobe, `[computed]` (§1.5). That is a fixed
property of the rectangle function; it does not improve with a bigger aperture, only the
beam gets narrower while the sidelobe stays 13.26 dB down.

### 4.2 The trade

Tapering the illumination — feeding the edges of the aperture less than the centre —
suppresses sidelobes, and pays for it in **three** currencies at once:

1. **Wider main beam** (broadening factor > 1)
2. **Lower gain** (taper loss, sometimes called aperture-efficiency loss)
3. Slightly harder feed network

Continuous line source, illumination `g(x)` over `|x| ≤ L/2`, all values `[computed]` with
`taper2.py`:

| Taper `g(x)` | 1st sidelobe | HPBW coefficient (deg × λ/L) | broadening | aperture eff. η_ap | taper loss |
|---|---|---|---|---|---|
| **uniform** `1` | **−13.26 dB** | **50.76** | 1.000 | 1.0000 | 0.00 dB |
| cos on −10 dB pedestal | −20.06 dB | 59.10 | 1.164 | 0.9273 | 0.33 dB |
| **cosine** `cos(πx/L)` | **−23.00 dB** | 68.12 | 1.342 | 0.8106 | 0.91 dB |
| triangular `1−2\|x\|/L` | −26.52 dB | 73.09 | 1.440 | 0.7500 | 1.25 dB |
| **cosine² (Hann)** | **−31.47 dB** | 82.54 | 1.626 | 0.6667 | 1.76 dB |
| cosine³ | −39.30 dB | 95.02 | 1.872 | 0.5764 | 2.39 dB |
| Hamming `0.54+0.46cos(2πx/L)` | −44.04 dB | 74.66 | 1.471 | 0.7338 | 1.34 dB |

Definitions used, so a build agent can reproduce the table exactly:

```
F(u)   = ∫ g(x) · cos(2π u x) dx        over x ∈ [−1/2, 1/2]   (x in units of L)
u      = (L/λ)·sin θ
η_ap   = | ∫ g dx |²  /  ∫ |g|² dx                (aperture / taper efficiency)
taper loss (dB) = −10·log10(η_ap)
D      = (4πA/λ²) · η_ap
```

Discrete N = 32 array, `d = λ/2`, standard windows, `[computed]`:

| Window | 1st sidelobe | HPBW | broadening | taper loss |
|---|---|---|---|---|
| uniform | −13.23 dB | 3.170° | 1.000 | 0.00 dB |
| Chebyshev (−30 dB design) | −30.00 dB | 3.890° | 1.227 | 0.58 dB |
| Taylor (−30 dB, n̄ = 5) | −30.20 dB | 4.014° | 1.266 | 0.68 dB |
| Hamming | −41.76 dB | 4.757° | 1.501 | 1.44 dB |
| Hann | −31.47 dB | 4.997° | 1.576 | 1.63 dB |
| Blackman | −58.13 dB | 6.070° | 1.915 | 2.51 dB |

**The lesson to teach:** Chebyshev and Taylor sit clearly above the cosine-family curve —
they reach −30 dB sidelobes for only 0.6–0.7 dB of gain and 23–27 % broadening, where a
cosine² taper spends 1.76 dB and 63 % broadening to get −31 dB. Taper choice is a genuine
optimisation, not a slider with a single right answer. Chebyshev gives *equal* sidelobes
everywhere (all at exactly −30 dB); Taylor lets the far-out lobes decay, which is usually
preferred in practice.

Corroboration from [Analog Devices — Phased Array Antenna Patterns Part 3](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part3.html)
*(search-result summary only)*: "Tapering provides a method to reduce antenna sidelobes at
some expense to the antenna gain and main lobe beamwidth"; cosine taper quoted as "−23 dB
sidelobes, 0.9 dB gain loss, 1.3× beamwidth increase" — which matches the computed row
(−23.00 dB, 0.91 dB, 1.342×) to all quoted digits.

### 4.3 Why this matters operationally

The course frames sidelobes as an **interference** problem, not an aesthetic one: for
multi-hop microwave links "the interfering signals would be transmitted off the main-lobe
i.e. the sidelobes. The side-lobe levels are lower, depending on the angular distance away
from the main-lobe" [P5 p.57], and one of the listed remedies for raising C/I is to "reduce
antenna side-lobe ratios for microwave antennas" [P5 p.53]. A tool should connect the
taper slider to a C/I readout, not just to a prettier plot.

---

## 5. Grating lobes

### 5.1 The condition

Grating lobes are extra full-strength main beams. They appear when the array factor's
argument advances by a full 2π between adjacent elements, so widely spaced elements can no
longer tell one direction from another. They occur at

```
sin θ_g  =  sin θ_scan  ±  m · λ/d ,        m = ±1, ±2, …
```

A grating lobe is real only if `|sin θ_g| ≤ 1` (inside "visible space"). Setting the m = 1
lobe exactly at the horizon gives the design rule:

```
   d              1
 ─────   <   ──────────────────
   λ           1 + |sin θ_scan|
```

[Search-result summary](https://arxiv.org/pdf/2001.04556): "the relation between the
attainable grating lobe-free scan angle Θ and the corresponding maximal distance d between
the radiating elements is: d < λ · 1/(1 + sin Θ). This relation is referred to as the 'λ/2
condition'."

### 5.2 The numbers

Maximum spacing for a grating-lobe-free scan `[computed]`:

| scan angle | max `d/λ` |
|---|---|
| 0° (broadside only) | **1.0000** |
| 30° | **0.6667** |
| 45° | **0.5858** |
| 60° | **0.5359** |
| 90° (full hemisphere) | **0.5000** |

Read the other way — how far a given spacing can scan before a grating lobe enters visible
space `[computed]`:

| `d/λ` | max grating-lobe-free scan |
|---|---|
| 0.5 | no grating lobe at any scan angle |
| 0.6 | **41.81°** |
| 0.7 | **25.38°** |
| 1.0 | 0° (a grating lobe sits exactly on the horizon at broadside) |
| 1.5 | grating lobe already inside visible space at broadside |

**This is why half-wavelength spacing is the default in every phased array.** It is the
largest spacing that is safe for *any* scan angle. Bigger spacing buys narrower beams and
fewer elements for the same aperture — and it is used deliberately in limited-scan arrays —
but it caps the scan range.

**The mistake to avoid:** "grating lobes appear when d > λ" is true only at broadside.
A `d = 0.7λ` array is perfectly clean at broadside and grows a grating lobe the moment it
steers past 25°. The scan dependence is the entire point of the teaching tool.

---

## 6. Polarisation

### 6.1 The three cases

- **Linear (LP)** — "the E-field stays along a single line". Vertical (VP) and horizontal
  (HP) are the two used in the course [P5 p.52].
- **Circular (CP)** — "the E-field rotates in a circle"; needs two orthogonal components of
  **equal magnitude, 90° out of phase**. Right-hand (RHCP) or left-hand (LHCP) by rotation
  sense.
- **Elliptical** — two perpendicular components "out of phase by 90 degrees but not equal in
  magnitude".

All three quoted from [antenna-theory.com — Polarization](https://www.antenna-theory.com/basics/polarization.php).

### 6.2 Axial ratio

```
AR  =  major axis / minor axis    (linear, ≥ 1)
AR(dB)  =  20·log10(AR)
```

"the ratio of the major and minor axis amplitudes"; circular polarisation is AR = 1.0
(0 dB), linear polarisation is AR = ∞ [antenna-theory.com](https://www.antenna-theory.com/basics/polarization.php).

| AR (dB) | AR (linear) |
|---|---|
| 0 | 1.000 (perfect circular) |
| 1 | 1.122 |
| **3** | **1.4125** (the usual spec limit for a "CP" antenna) |
| 6 | 1.995 |
| 20 | 10.00 |
| ∞ | ∞ (linear) |

`[computed]` — `AR = 10^(AR_dB/20)`. Note **20·log10**, not 10 — axial ratio is an
amplitude ratio.

### 6.3 Polarisation loss factor (PLF)

Two linear antennas at relative tilt φ:

```
PLF  =  cos² φ                 loss(dB) = −10·log10(cos² φ) = −20·log10|cos φ|
```

[antenna-theory.com](https://www.antenna-theory.com/basics/polarization.php): "PLF = cos²(φ),
where φ is the angle between their radiated E-fields."

General elliptical case (this is the one a tool needs to be honest about axial ratio):

```
                4·AR₁·AR₂  +  (AR₁²−1)(AR₂²−1)·cos(2Δτ)
PLF  =  ½  +  ────────────────────────────────────────────
                     2 · (AR₁² + 1) · (AR₂² + 1)
```

`AR` linear ≥ 1, **negated for opposite rotational sense**; `Δτ` = tilt-angle difference.
Verified against all four limiting cases `[computed]` with `pol.py`: two aligned LP → 1;
LP at 90° → 0; CP against LP → exactly 0.5; co-sense CP pair → 1; counter-sense CP pair → 0.

### 6.4 Cross-polarisation loss table

Linear-to-linear `[computed]`:

| tilt φ | PLF | loss |
|---|---|---|
| 0° | 1.0000 | **0.00 dB** |
| 10° | 0.9698 | 0.13 dB |
| 20° | 0.8830 | 0.54 dB |
| 30° | 0.7500 | **1.25 dB** |
| **45°** | **0.5000** | **3.01 dB** |
| 60° | 0.2500 | 6.02 dB |
| 80° | 0.0302 | 15.21 dB |
| 85° | 0.0076 | 21.19 dB |
| 89° | 0.000305 | 35.16 dB |
| 90° | 0 | ∞ (infinite in theory) |

### 6.5 The 3 dB linear-to-circular case

```
LP antenna  ↔  CP wave     PLF = 0.5     loss = 3.01 dB     always
```

[antenna-theory.com](https://www.antenna-theory.com/basics/polarization.php): the loss is
"0.5 (−3dB), **no matter what the angle the LP antenna is rotated to**."

That rotation-independence is the whole engineering point of CP: you give up 3 dB and in
exchange the link stops caring about the orientation of the other end. It is why GPS,
satellite uplinks and tumbling-spacecraft telemetry use CP.

Real antennas are never perfectly circular, and the imperfection shows up as a **ripple
about the 3 dB figure** — this is what axial ratio is actually for `[computed]`:

| CP antenna's AR | loss against a pure LP wave | ripple about 3.01 dB |
|---|---|---|
| 0 dB (perfect CP) | 3.01 dB flat | ±0.00 dB |
| 0.5 dB | 2.77 – 3.27 dB | ±0.25 dB |
| 1 dB | 2.54 – 3.54 dB | ±0.50 dB |
| 2 dB | 2.12 – 4.12 dB | ±1.00 dB |
| **3 dB** | **1.76 – 4.76 dB** | **±1.50 dB** |
| 6 dB | 0.97 – 6.97 dB | ±3.00 dB |

Clean pattern worth stating in the tool: **the ripple in dB is exactly half the axial ratio
in dB.** A 3 dB AR antenna swings ±1.5 dB as the linear source rotates.

Two nominally-CP antennas of the same sense, both with axial ratio AR `[computed]`:

| both antennas' AR | worst-case loss |
|---|---|
| 1 dB | 0.06 dB |
| 2 dB | 0.23 dB |
| 3 dB | **0.51 dB** |
| 6 dB | 1.93 dB |

CP-to-CP is very forgiving; CP-to-LP is not. Do not use one number for both.

### 6.6 In the course

Orthogonal polarisation is listed as an interference-reduction measure: "Antenna
cross-polarization discrimination [if polarization of Link1 and Link2 are orthogonal e.g.
Link1 transmits on vertical polarization (VP) and Link2 transmit on horizontal polarization
(HP)]" [P5 p.52], and "Use orthogonal polarization antenna" [P5 p.53]. "A receiving antenna
on horizontal polarization (HP) will receive lower signals from a transmitter on an
orthogonal polarization [vertical polarization (VP)]" [P5 p.53].

**Do not draw this as infinite rejection.** Real cross-polarisation discrimination (XPD) is
typically 25–35 dB, limited by antenna imperfection and by rain depolarisation — not by the
`cos²(90°) = 0` of the ideal formula. The 89° row above (35 dB) is roughly where a real
system sits, and it corresponds to 1° of misalignment. Present XPD as a finite,
specification-driven number.

---

## 7. VSWR, return loss, reflection coefficient, mismatch loss

### 7.1 The exact relationships

```
Γ  =  ( Z_L − Z₀ ) / ( Z_L + Z₀ )            complex reflection coefficient

           1 + |Γ|                                 VSWR − 1
VSWR  =  ───────────           ⟺        |Γ|  =  ───────────
           1 − |Γ|                                 VSWR + 1

Return Loss (dB)      =  −20 · log10 |Γ|   =  −20·log10[ (VSWR−1)/(VSWR+1) ]
|Γ|                   =  10^( −RL_dB / 20 )
Reflected power (%)   =  100 · |Γ|²
Transmitted power (%) =  100 · ( 1 − |Γ|² )
Mismatch Loss (dB)    =  −10 · log10( 1 − |Γ|² )
```

Every one of these is printed verbatim on the [Marki Microwave return-loss/VSWR conversion
table](https://markimicrowave.com/tools/return-loss-to-vswr.pdf) (fetched and text-extracted;
its footer block reads `Γ = 10^(−Return Loss/20)`, `Return Loss (dB) = −20 log |Γ|`,
`VSWR = (1+|Γ|)/(1−|Γ|)`, `Γ = (VSWR−1)/(VSWR+1)`, `Mismatch Loss (dB) = 10 log(1−Γ²)`,
`Reflected Power (%) = 100·Γ²`, `Through Power (%) = 100(1−Γ²)`). The return-loss form is
independently confirmed by [Electronics Notes — VSWR & Return
Loss](https://www.electronics-notes.com/articles/antennas-propagation/vswr-return-loss/vswr-return-loss-conversion-table.php):
"Return Loss = −20 log10 ( VSWR − 1 / VSWR + 1 ) dB".

**Sign convention:** return loss is quoted as a **positive** number of dB (a *loss*). Some
instruments display it negative (as `S11` in dB). A bigger positive return loss is a better
match. A tool must pick one and label it; the two conventions differ by a minus sign and
this is the single most common confusion on the topic.

### 7.2 The table — REQUIRED, use these exact values

All `[computed]` from the equations above with `verify_ant.py`:

| VSWR | \|Γ\| | Return loss (dB) | Power reflected (%) | Mismatch loss (dB) |
|---|---|---|---|---|
| **1.0** | 0.0000 | **∞** (perfect match) | **0.00** | **0.000** |
| **1.5** | 0.2000 | **13.98** | **4.00** | **0.177** |
| **2.0** | 0.3333 | **9.54** | **11.11** | **0.512** |
| **3.0** | 0.5000 | **6.02** | **25.00** | **1.249** |
| **5.0** | 0.6667 | **3.52** | **44.44** | **2.553** |
| 10.0 | 0.8182 | 1.74 | 66.94 | 4.807 |

Cross-check against the Marki table, which is indexed the other way (by integer return
loss): its RL = 14 dB row reads `Γ = 0.200, mismatch loss 0.176 dB, reflected 3.98 %,
through 96.02 %` — matching the VSWR = 1.5 row above (RL 13.98 dB) to the rounding.
Its RL = 6 dB row reads `Γ = 0.501, mismatch loss 1.256 dB, reflected 25.12 %` — matching
the VSWR = 3.0 row.

*(Note for anyone re-extracting the Marki PDF: the VSWR column in the `pdftotext` dump is
shifted by one row relative to the return-loss column. The Γ, mismatch-loss and reflected-power
columns are aligned correctly. Verify by `VSWR = (1+Γ)/(1−Γ)` before trusting a row.)*

### 7.3 The three numbers people confuse

- **Return loss** is about the *reflected* wave: how far down the reflection is.
- **Mismatch loss** is about the *transmitted* wave: how much of your power failed to get in.
- They are **not** the same number and not the negative of each other. VSWR 2.0 is
  **9.54 dB return loss** but only **0.51 dB mismatch loss** — 11 % of the power comes back,
  yet the link only loses half a dB.

This is why VSWR 2.0 is a routine, acceptable antenna specification. A student who thinks
VSWR 2 costs 9.5 dB will over-design every match they ever build. Put both columns on
screen simultaneously.

Caveat to state: mismatch loss as computed here ignores what happens to the reflected power
after it returns — in a real system it can re-reflect off the source, produce ripple, or
damage the PA. Mismatch loss is the *best case*.

---

## 8. Boresight

### 8.1 The two boresights

- **Mechanical (reference) boresight** — a direction defined by the *physical structure*:
  the mounting flange, an optical alignment reference, the geometric axis of the dish. It is
  what a telescope or a dial indicator can see. It does not move when you change frequency
  or steer the beam.
- **Electrical (electromagnetic) boresight** — the direction the *beam* actually points: the
  peak of the main lobe, or, in a monopulse/tracking antenna, the null of the difference
  pattern. This is what the RF actually does.

### 8.2 Boresight error

> "The antenna is said to be 'boresighted' when the electromagnetic axis and the mechanical
> axis are parallel. The angular discrepancy between the electromagnetic axis and the
> mechanical axis is called the 'boresight error'; a 'boresight measurement' is a measurement
> of this angle."

— [Doren Hess, *Antenna Boresighting*, NSI-MI Technologies](https://www.nsi-mi.com/-/media/project/oneweb/oneweb/nsi/files/technical-papers/1987/antenna-boresighting.pdf)
(fetched and text-extracted; the same sentence appears in both Section I-A and Section II-A
of the paper).

The IEEE definition is the same idea stated formally: boresight error is the angular
deviation of the electrical boresight from the reference boresight
*(search-result summary — IEEE Std 145/149 not fetched directly)*.

### 8.3 What it means in practice

Causes: manufacturing tolerance in the reflector or feed, feed displacement, **radome
refraction** (a radome bends the wavefront and the beam appears to come from the wrong
direction — this is the classic radome boresight error), thermal distortion, mounting
sag, and in a phased array, phase-shifter quantisation and calibration drift.

Consequences a tool can show concretely:

- **Pointing loss.** If the beam is off by δ and the HPBW is θ₃, the loss is roughly
  `12·(δ/θ₃)² dB` (the standard Gaussian main-lobe approximation, exact at the −3 dB point
  where it returns 3 dB). A 0.5° error on a 1° beam costs 3 dB. The narrower the beam, the
  more brutal the error — which is exactly the trade against §3.
- **Tracking bias.** A radar with boresight error reports the target at the wrong angle even
  when perfectly locked, because the *electrical* null it tracks is not on the *mechanical*
  axis the encoder reads.
- **Calibration.** Boresighting is the alignment procedure that measures this angle so it can
  be corrected in software; the NSI paper describes measuring it with an autocollimator and
  a pattern null.

Do not conflate boresight error with **beam squint** (beam direction changing with
frequency) or with **scan error**. They are different mechanisms; a tool that lumps them
together teaches the wrong debugging instinct.

---

## 9. The course gain / effective-area table [P5 p.45]

Reconstructed from the scrambled text extraction and verified cell by cell against
`G = 4πA_e/λ²`. The slide compares the same antennas at two wavelengths.

Footnotes on the slide, verbatim: "*Assumed for parabolic disc, = 56% efficiency."
"# Units are absolute values. To convert to decibels 10 log10(G) so Isotropic Gain = 1 = 0
dBi."

| Antenna | λ = 30 cm: A_e (m²) | G | G (dBi) `[computed]` | λ = 3 mm: A_e (m²) | G | G (dBi) `[computed]` |
|---|---|---|---|---|---|---|
| Isotropic | 0.007 | 1 | 0.00 | 7.2 × 10⁻⁷ | 1 | 0.00 |
| Infinitesimal dipole or loop | 0.011 | 1.5 | 1.76 | 1.1 × 10⁻⁶ | 1.5 | 1.76 |
| Half-wave dipole | 0.012 | 1.64 | 2.15 | 1.2 × 10⁻⁶ | 1.64 | 2.15 |
| Horn | 2.54 | 349 | 25.43 | 2.54 | 3.5 × 10⁶ | 65.44 |
| Parabolic* | 1.76 | 244 | 23.87 | 1.76 | 2.4 × 10⁶ | 63.80 |
| Turnstile | 0.008 | 1.15 | 0.61 | 8.2 × 10⁻⁷ | 1.15 | 0.61 |

Consistency check `[computed]`, `4π/λ²` = 139.626 m⁻² at 30 cm and 1.3963 × 10⁶ m⁻² at 3 mm:

| Antenna | A_e implied by G at 30 cm | table A_e | agreement |
|---|---|---|---|
| Isotropic | 0.007162 | 0.007 | ✓ rounding |
| Inf. dipole / loop | 0.010744 | 0.011 | ✓ rounding |
| Half-wave dipole | 0.011746 | 0.012 | ✓ rounding |
| Horn | 2.4995 | 2.54 | **1.6 % off** |
| Parabolic | 1.7475 | 1.76 | **0.7 % off** |
| Turnstile | 0.008236 | 0.008 | ✓ rounding |

The two aperture antennas are internally inconsistent by 1–2 % — the slide's stated `A_e`
and stated `G` do not close exactly. **Reproduce the slide's numbers when teaching the
course, but derive from `G = 4πA_e/λ²` when computing anything new, and say which you used.**

The parabolic row decodes cleanly: 56 % efficiency and `A_e = 1.76 m²` implies a physical
area of 3.14 m², i.e. a **2.0 m dish**. `[computed]` `A_e = 0.56·π·1² = 1.7593 m²`,
`G = 4π(1.7593)/0.09 = 245.6 = 23.90 dBi` — which is the table's 244 to within its rounding.
And the §3.3 example above is that same 2 m dish at 1 GHz: HPBW = 11.0°.

The horn and parabolic rows keep the **same physical aperture at both frequencies**, which
is why their gain rises by exactly 40 dB (a factor of 10⁴ = (100 GHz / 1 GHz)²) while the
wire antennas do not move at all. That contrast is the single best teaching moment on the
page.

---

## 10. VALIDATION TABLE — a build agent must reproduce every one of these

Test the code against these before shipping. Tolerances are the last quoted digit unless
stated.

### Patterns and directivity

| # | Check | Expected |
|---|---|---|
| V1 | Hertzian dipole directivity | 1.5000 (±0.001) |
| V2 | Hertzian dipole gain | 1.761 dBi (±0.01) |
| V3 | Hertzian dipole HPBW | 90.00° (±0.05) |
| V4 | Half-wave dipole directivity | 1.6409 (±0.001) |
| V5 | **Half-wave dipole gain** | **2.15 dBi** (±0.01) |
| V6 | **Half-wave dipole HPBW** | **78.08°** (±0.1); edges 50.96° / 129.04° |
| V7 | Half-wave dipole `F(θ)` at θ = 0 and π | exactly 0, not NaN, not 1 |
| V8 | Half-wave dipole `F(90°)` | exactly 1 |
| V9 | λ/4 monopole directivity | 3.2818 (±0.002) |
| V10 | λ/4 monopole gain | 5.16 dBi (±0.02) — accept 5.15–5.19 if the source is cited |
| V11 | Monopole gain minus dipole gain | 3.01 dB (±0.01) |
| V12 | Monopole field for θ > 90° | exactly 0 |
| V13 | Isotropic directivity | 1.000 = 0.00 dBi |

### Aperture and array

| # | Check | Expected |
|---|---|---|
| V14 | Uniform line source `F(u)` at u = 0 | exactly 1 (not NaN) |
| V15 | Uniform line source first null | u = π, i.e. sin θ = λ/L |
| V16 | Uniform line source HPBW coefficient | 0.8859 λ/L rad = **50.76 λ/L degrees** (±0.05) |
| V17 | **Uniform aperture first sidelobe** | **−13.26 dB** (±0.02), peak at u = 4.4934 |
| V18 | Uniform aperture second sidelobe | −17.83 dB (±0.05) |
| V18a | Uniform **circular** aperture HPBW | **58.96 λ/D degrees** (±0.05) |
| V18b | Uniform **circular** aperture first sidelobe | **−17.57 dB** (±0.05) — NOT −13.26 |
| V18c | Uniform circular aperture first null | sin θ = **1.22 λ/D** (±0.005) |
| V19 | Array factor at ψ = 0 | exactly 1 (not NaN) |
| V20 | ULA N = 32, d = λ/2, broadside HPBW | 3.174° (±0.01) |
| V21 | ULA N = 32 first sidelobe | −13.23 dB (±0.05) |
| V22 | ULA N = 4 first sidelobe | **−11.30 dB** (±0.05) — must NOT be −13.2 |
| V23 | ULA N = 8 first sidelobe | −12.80 dB (±0.05) |
| V24 | ULA N = 16 first sidelobe | −13.15 dB (±0.05) |
| V25 | ULA directivity, d = λ/2, uniform | ≈ N (within 5 % for N ≥ 8) |

### Scan, grating lobes, beamwidth

| # | Check | Expected |
|---|---|---|
| V26 | N = 16, d = λ/2, HPBW at 0° scan | 6.359° (±0.01) |
| V27 | same, scan 45° | 9.025° exact / 8.993° by 1/cos (±0.02) |
| V28 | same, scan 60° | 12.993° exact / 12.717° by 1/cos (±0.03) |
| V29 | Grating-lobe-free max `d/λ` at 30° scan | 0.6667 (±0.0005) |
| V30 | Grating-lobe-free max `d/λ` at 45° scan | 0.5858 (±0.0005) |
| V31 | Grating-lobe-free max `d/λ` at 60° scan | 0.5359 (±0.0005) |
| V32 | Max scan for `d/λ` = 0.6 | 41.81° (±0.05) |
| V33 | Max scan for `d/λ` = 0.7 | 25.38° (±0.05) |
| V34 | `d/λ` = 0.5 at any scan | no grating lobe in visible space |
| V35 | Dish HPBW, 2 m at 1 GHz, course rule | 11.00° |
| V36 | same, 70λ/D rule | 10.50° |
| V37 | Ratio of the two dish rules | 1.048 at every f and D |

### Tapering

| # | Check | Expected |
|---|---|---|
| V38 | Cosine taper first sidelobe | −23.00 dB (±0.1) |
| V39 | Cosine taper aperture efficiency | 0.8106 → 0.91 dB taper loss (±0.02) |
| V40 | Cosine taper broadening | 1.342× (±0.01) |
| V41 | Cosine² (Hann) first sidelobe | −31.47 dB (±0.1) |
| V42 | Cosine² aperture efficiency | 0.6667 → 1.76 dB (±0.02) |
| V43 | Triangular taper first sidelobe | −26.52 dB (±0.1) |
| V44 | Triangular aperture efficiency | 0.7500 exactly |
| V45 | Uniform taper efficiency | 1.0000, 0.00 dB loss |

### Polarisation

| # | Check | Expected |
|---|---|---|
| V46 | LP/LP aligned | 0.00 dB |
| V47 | LP/LP at 30° | 1.25 dB |
| V48 | **LP/LP at 45°** | **3.01 dB** |
| V49 | LP/LP at 60° | 6.02 dB |
| V50 | **LP antenna, CP wave, any rotation** | **3.01 dB, constant** |
| V51 | Co-sense CP pair, both perfect | 0.00 dB |
| V52 | Counter-sense CP pair, both perfect | infinite (guard the display) |
| V53 | AR = 3 dB CP antenna vs LP wave | 1.76 – 4.76 dB, ripple ±1.50 dB |
| V54 | AR = 1 dB CP antenna vs LP wave | 2.54 – 3.54 dB, ripple ±0.50 dB |
| V55 | Ripple in dB vs AR in dB | ripple = AR/2 exactly |
| V56 | Two co-sense AR = 3 dB antennas, worst case | 0.51 dB (±0.01) |
| V57 | AR = 3 dB in linear | 1.4125 (uses 20·log10, not 10) |

### VSWR

| # | Check | Expected |
|---|---|---|
| V58 | VSWR 1.0 | Γ = 0, RL = ∞, 0.00 % reflected, ML = 0.000 dB |
| V59 | **VSWR 1.5** | **Γ = 0.2000, RL = 13.98 dB, 4.00 %, ML 0.177 dB** |
| V60 | **VSWR 2.0** | **Γ = 0.3333, RL = 9.54 dB, 11.11 %, ML 0.512 dB** |
| V61 | **VSWR 3.0** | **Γ = 0.5000, RL = 6.02 dB, 25.00 %, ML 1.249 dB** |
| V62 | **VSWR 5.0** | **Γ = 0.6667, RL = 3.52 dB, 44.44 %, ML 2.553 dB** |
| V63 | Round trip VSWR → Γ → RL → Γ → VSWR | returns the input to 6 decimal places |

### Gain / aperture

| # | Check | Expected |
|---|---|---|
| V64 | Isotropic effective aperture at 1 GHz | 0.007162 m² (= λ²/4π) |
| V65 | Half-wave dipole A_e at 1 GHz | 0.011746 m² |
| V66 | 2 m dish, 56 % efficiency, 1 GHz | A_e = 1.759 m², G = 245.6 = 23.90 dBi |
| V67 | Same dish at 100 GHz | G rises by exactly 40.00 dB |
| V68 | `G = 4πA_e/λ²` round trip | A_e → G → A_e returns the input |

---

## 11. DO NOT FAKE

Things that must be **computed from the formulas above**, never eyeballed, hard-coded,
approximated silently, or copied from an adjacent tool.

**Patterns**

1. **Do not use `sin θ` for the half-wave dipole.** It is `cos((π/2)cos θ)/sin θ`. The two
   look similar at a glance and differ by 12° of beamwidth. If the tool is about the
   half-wave dipole, the difference *is* the lesson.
2. **Do not give the half-wave dipole a directivity of 1.5.** That is the *short* dipole.
   1.6409 / 2.15 dBi.
3. **Do not return NaN at the pattern singularities.** θ = 0, θ = π for the dipole;
   u = 0 for the sinc; ψ = 0 and ψ = 2πm for the array factor. All three have finite limits
   (0, 1, 1 respectively). A single NaN blanks an entire canvas.
4. **Do not draw the monopole radiating below its ground plane**, and do not claim the null
   below is perfect for a finite ground plane — say the plane is idealised as infinite.
5. **Do not mix `20·log10` and `10·log10`.** Field patterns take 20; power patterns take 10.
   Applying 20 to a power gives a plot that is exactly twice as deep in dB and looks
   plausible, which is what makes it dangerous.
6. **Do not mix the two sinc conventions** (`sin u/u` vs `sin πx/πx`) within one file.

**Beamwidth**

7. **Do not compute HPBW as half the null-to-null beamwidth.** For the uniform line source
   that gives 57.3 λ/L instead of the correct 50.76 λ/L — 13 % wrong. Solve `|F|² = 0.5`.
8. **Do not claim `22/(F·D)` and `70λ/D` agree.** They differ by 4.8 % always. Show both or
   name the one in use.
9. **Do not present either dish rule as exact.** The constant runs 65–75 depending on the
   feed taper; the underlying physics is §4.
10. **Do not apply `0.886 λ/(Nd)` to small arrays.** It is 9 % wrong at N = 4 and 18 % wrong
    at N = 2. Solve for the −3 dB points numerically below N ≈ 16.
11. **Do not forget `1/cos θ_scan`** when a beam is steered, and do not trust it past 60°
    (2.2 % error there and growing).

**Sidelobes and arrays**

12. **Do not hard-code −13.2 dB as the first sidelobe of every array.** It is the N → ∞
    limit. N = 4 gives −11.3 dB, N = 8 gives −12.8 dB. Compute it.
13. **Do not apply the −13.26 dB figure to a tapered aperture.** Tapering is defined by
    changing that number; quoting it alongside a taper slider is self-contradicting.
13a. **Do not apply the −13.26 dB figure to a circular aperture / dish.** That number is the
    *rectangular* aperture. A uniform circular aperture is **−17.57 dB** with its first null
    at 1.22 λ/D and HPBW 58.96 λ/D. Using the line-source constants for a dish is wrong by
    4.3 dB in sidelobe level and 16 % in beamwidth.
14. **Do not show sidelobe suppression without its cost.** Every taper row has a beamwidth
    penalty *and* a gain penalty. A tool that shows only the sidelobes going down teaches
    that tapering is free, which is the opposite of the lesson.
15. **Do not plot the array factor alone and label it "the antenna pattern."** The real
    pattern is element pattern × array factor. Either include the element pattern or label
    the plot "array factor".
16. **Do not claim grating lobes only appear for `d > λ`.** That is broadside only. The
    condition is `d/λ < 1/(1+|sin θ_scan|)`, and the scan dependence is the entire point.
17. **Do not let a grating lobe render outside visible space.** Only `|sin θ_g| ≤ 1` is real.

**Polarisation**

18. **Do not use 10·log10 for axial ratio.** AR is an amplitude ratio: `20·log10`.
19. **Do not treat cross-polar rejection as infinite.** The ideal formula says ∞ at 90°;
    real XPD is 25–35 dB. Displaying "∞ dB" or a division by zero is a bug and a
    misconception at once.
20. **Do not use one number for CP-to-LP and CP-to-CP mismatch.** A 3 dB AR costs ±1.5 dB
    against a linear wave and only 0.51 dB against another CP antenna of the same sense.
21. **Do not make the 3 dB linear/circular loss depend on rotation angle.** It is exactly
    3.01 dB at every angle; that invariance is the reason CP exists.

**VSWR**

22. **Do not confuse return loss with mismatch loss.** VSWR 2.0 is 9.54 dB return loss and
    0.51 dB mismatch loss. Conflating them overstates the penalty by nearly 9 dB.
23. **Do not display return loss without stating the sign convention.** Positive-as-loss or
    negative-as-S11 — pick one, label it.
24. **Do not display ∞ or NaN for VSWR = 1.** Guard it and print "perfect match" or "—".
25. **Do not round `Γ` before computing the rest of the chain.** Compute from VSWR each time;
    rounding Γ to two decimals moves the return loss by tenths of a dB.

**Boresight**

26. **Do not treat mechanical and electrical boresight as the same axis.** The whole concept
    is the angle between them.
27. **Do not conflate boresight error with beam squint or with steering error.** Different
    causes, different fixes.

**General**

28. **Do not state gain where directivity was computed.** `G = η·D`. Every directivity in
    this document assumes η = 1; a real antenna is 50–70 % efficient (and the course's dish
    is 56 % [P5 p.45]). If a tool prints "gain", it must either apply an efficiency or say
    it is assuming a lossless antenna.
29. **Do not silently switch between the course table's numbers and derived numbers.** The
    slide's horn and parabolic rows do not close on `G = 4πA_e/λ²` to better than 1.6 %
    (§9). Say which source a displayed number came from.
30. **Do not guard `arcsin` by clamping without saying so.** When a steered beam edge runs
    past the horizon, the beam is genuinely clipped — that is physics worth drawing, not an
    edge case to hide.

---

## 12. Quick reference card

```
--- patterns (normalised field, peak 1) ---
isotropic            F = 1                                        D = 1      = 0.00 dBi
Hertzian dipole      F = sin θ                                    D = 1.5    = 1.76 dBi   HPBW 90.00°
half-wave dipole     F = cos((π/2)cos θ)/sin θ                    D = 1.6409 = 2.15 dBi   HPBW 78.08°
λ/4 monopole         same, 0 ≤ θ < π/2, else 0                    D = 3.2818 = 5.16 dBi
uniform line source  F = sin u / u,  u = (πL/λ) sin θ             HPBW = 50.76 λ/L deg    SLL1 = −13.26 dB
rect aperture        F = (sin u/u)(sin v/v)                       D = 4πA/λ²
circular aperture    F = 2J₁(u)/u,  u = (πD/λ) sin θ              HPBW = 58.96 λ/D deg    SLL1 = −17.57 dB
  (a dish is CIRCULAR: −17.57 dB and null at 1.22 λ/D, not the line-source −13.26 dB)
N-element ULA        F = sin(Nψ/2)/(N sin(ψ/2))
                     ψ = (2πd/λ) sin θ + β ,  β = −(2πd/λ) sin θ₀
limits to guard      dipole θ→0,π ⇒ 0 ;  sinc u→0 ⇒ 1 ;  AF ψ→0 ⇒ 1

--- gain and aperture ---
G     = 4 π A_e / λ²             A_e = G λ² / (4π)        A_e = η_ap · A_phys
G(dBi)= 10 log10 G               G = η · D
isotropic A_e = λ²/4π            fixed aperture ⇒ G ∝ f²

--- beamwidth ---
dish (course)   HPBW = 22 / (F_GHz · D_m)              deg      [P5 p.44]
dish (general)  HPBW = 70 λ / D  = 21/(F_GHz·D_m)      deg      (constant 65–75)
dish (uniform)  HPBW = 58.96 λ / D                     deg      (theoretical floor)
uniform line    HPBW = 0.886 λ/L rad = 50.76 λ/L       deg
ULA             HPBW = 0.886 λ / (N d cos θ_scan)      rad      (N ≥ 16)
scan loss       G(θ) = G₀ cos^n θ_scan ,  n ≈ 2 … 3 (default 2.5)
pointing loss   ≈ 12 (δ / HPBW)²                       dB

--- sidelobes / taper ---
uniform      −13.26 dB   HPBW ×1.000   taper loss 0.00 dB   η_ap 1.000
cosine       −23.00 dB   HPBW ×1.342   taper loss 0.91 dB   η_ap 0.811
triangular   −26.52 dB   HPBW ×1.440   taper loss 1.25 dB   η_ap 0.750
cosine²      −31.47 dB   HPBW ×1.626   taper loss 1.76 dB   η_ap 0.667
Taylor −30   −30.20 dB   HPBW ×1.266   taper loss 0.68 dB   (N=32 array)
Chebyshev −30 −30.00 dB  HPBW ×1.227   taper loss 0.58 dB   (N=32 array)
η_ap = |∫g dx|² / ∫|g|² dx        taper loss dB = −10 log10 η_ap

--- grating lobes ---
sin θ_g = sin θ_scan ± m λ/d ,  real only if |sin θ_g| ≤ 1
free of grating lobes:   d/λ  <  1 / (1 + |sin θ_scan|)
   θ_scan  0°→1.000   30°→0.667   45°→0.586   60°→0.536   90°→0.500
   d/λ 0.5 → any scan   0.6 → 41.81°   0.7 → 25.38°   1.0 → 0°

--- polarisation ---
AR = major/minor (≥1)            AR(dB) = 20 log10 AR      3 dB ⇒ 1.4125
LP↔LP     PLF = cos²φ            45° ⇒ 3.01 dB    30° ⇒ 1.25 dB    60° ⇒ 6.02 dB
LP↔CP     PLF = 0.5 = 3.01 dB    independent of rotation
general   PLF = ½ + [4·AR₁AR₂ + (AR₁²−1)(AR₂²−1)cos2Δτ] / [2(AR₁²+1)(AR₂²+1)]
          (negate one AR for opposite sense)
AR X dB CP antenna vs LP wave ⇒ 3.01 ± X/2 dB
real cross-pol discrimination (XPD) 25–35 dB, never ∞

--- match ---
Γ    = (Z_L−Z₀)/(Z_L+Z₀)          |Γ| = (VSWR−1)/(VSWR+1)
VSWR = (1+|Γ|)/(1−|Γ|)            |Γ| = 10^(−RL/20)
RL(dB)  = −20 log10 |Γ|
%refl   = 100 |Γ|²                %through = 100 (1−|Γ|²)
ML(dB)  = −10 log10 (1 − |Γ|²)
  VSWR  1.0  1.5    2.0    3.0    5.0
  RL dB  ∞   13.98  9.54   6.02   3.52
  %refl  0   4.00   11.11  25.00  44.44
  ML dB  0   0.177  0.512  1.249  2.553

--- boresight ---
mechanical boresight = physical/optical reference axis
electrical boresight = actual beam peak (or monopulse difference null)
boresight error      = angle between them
causes: manufacturing, feed offset, radome refraction, thermal, phase quantisation
```

---

## Sources

Course PDF (read via `pdftotext -layout`; pattern diagrams on pp. 43 and 46 are bitmaps and
return no text):

- `C:\Users\yongw\Downloads\IE4155 Part 5 AY24-25 (1).pdf` — 76 pages; antenna material on
  pp. 42–46 and 52–57. HPBW dish rule [p.44], gain/effective-area table [p.45],
  polarisation as an interference remedy [pp.52–53], sidelobes and dog-legging [pp.56–57].

Web (fetched and read directly):

- [Dipole antenna — Wikipedia](https://en.wikipedia.org/wiki/Dipole_antenna) — half-wave
  pattern form, 1.64 / 2.15 dBi, 78°, 73.1 Ω; short dipole sin θ, 1.5, 90°
- [Monopole antenna — Wikipedia](https://en.wikipedia.org/wiki/Monopole_antenna) — 3 dB over
  the dipole, 36.5 Ω, image-plane argument
- [Phased array — Wikipedia](https://en.wikipedia.org/wiki/Phased_array) — progressive phase
  steering `β_x = −k d_x sin θ₀ cos φ₀`
- [Polarization of Plane Waves — antenna-theory.com](https://www.antenna-theory.com/basics/polarization.php)
  — LP/CP/elliptical definitions, axial ratio, `PLF = cos²φ`, the 3 dB LP↔CP result
- [Effective Aperture — antenna-theory.com](https://www.antenna-theory.com/basics/aperture.php)
  — concept only; the equation on that page is an image and did not extract
- [Return Loss to VSWR Conversion Table — Marki Microwave (PDF)](https://markimicrowave.com/tools/return-loss-to-vswr.pdf)
  — all five match formulas verbatim plus the full 1–40 dB table (VSWR column is row-shifted
  in text extraction; see §7.2)
- [VSWR to Return Loss Conversion Table & Formulas — Electronics Notes](https://www.electronics-notes.com/articles/antennas-propagation/vswr-return-loss/vswr-return-loss-conversion-table.php)
  — independent confirmation of the return-loss formula
- [Doren Hess, *Antenna Boresighting* — NSI-MI Technologies (PDF)](https://www.nsi-mi.com/-/media/project/oneweb/oneweb/nsi/files/technical-papers/1987/antenna-boresighting.pdf)
  — the quoted definition of boresight error and the measurement procedure
- [arrayscanloss — MathWorks](https://www.mathworks.com/help/radar/ref/arrayscanloss.html)
  — the two scan-loss mechanisms, cos^n law with n ≈ 2–3
- [Continuous Arrays, ECE422 — University of Toronto (PDF)](https://www.waves.utoronto.ca/prof/svhum/ece422/notes/16-continuous.pdf)
  — fetched, but Greek and symbol glyphs are stripped by extraction; used only as
  corroboration that HPBW ≈ half the null-to-null beamwidth for a line source

Web (search-result summaries only — quoted text **not verified at source**):

- [Phased Array Antenna Patterns Part 3: Sidelobes and Tapering — Analog Devices](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part3.html)
  *(direct fetch timed out twice; mirrors at mwrf.com and theengineer.co.uk returned HTTP 403)*
  — the −13.2 dB uniform sidelobe and the cosine-taper trade figures
- [Phased Array Antenna Patterns Part 1 — Analog Devices](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part1.html)
  *(direct fetch timed out twice)*
- [Theory and Simulation of Metasurface Lenses for Extending the Angular Scan Range of Phased Arrays — arXiv](https://arxiv.org/pdf/2001.04556)
  — the `d < λ/(1 + sin Θ)` grating-lobe condition
- [Approximate −3 dB beamwidth for a parabolic antenna — prepp.in](https://prepp.in/question/the-approximate-3-db-beam-width-for-a-parabolic-an-6846c1f2e4d5b7dc0489462d)
  — the 70λ/D rule and the 65–75 spread of the constant
- [Friis equation and antenna effective area — Circuit Design Inc.](https://www.cdt21.com/design_guide/friis-equation-and-antenna-effective-area/)
  and [Friis Transmission Equation — Physics LibreTexts](https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Electromagnetics_II_(Ellingson)/10:_Antennas/10.14:_Friis_Transmission_Equation)
  — `G = 4πA/λ²`
- [Antenna Array Considerations for Calibration — NATO STO EN-SET-337 (PDF)](https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SET-337/EN-SET-337-03.pdf)
  *(direct fetch returned HTTP 403)*
- [VSWR to Return Loss Conversion Chart — everything RF](https://www.everythingrf.com/tech-resources/vswr)
  *(direct fetch returned HTTP 403)*

Not consulted, but the authoritative print references if a discrepancy needs settling:
Balanis, *Antenna Theory: Analysis and Design*; Mailloux, *Phased Array Antenna Handbook*;
IEEE Std 145 (antenna definitions) and IEEE Std 149 (test procedures).
