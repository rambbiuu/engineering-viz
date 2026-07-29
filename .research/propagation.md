# Radio Propagation Physics — reference sheet for the interactive teaching tool

Every number below is either (a) read directly off a cited page of the IE4155 course PDFs,
(b) read directly out of a cited ITU-R Recommendation, or (c) **computed this session** from a
cited formula/table by the scripts listed in §7. Nothing here is recalled from memory.

## 0. Source index

| Tag | Document | How it was read |
|---|---|---|
| `[P1-4 pN]` | `C:\Users\yongw\Downloads\IE4155 Lecture AY2024-25 Part 1-4 (1).pdf` (31 pp) | text layer + page renders |
| `[6B pN]` | `C:\Users\yongw\Downloads\IE4155 Part 6B Slide version (1).pdf` (42 pp) | image-only; pages rendered to PNG at 100 dpi and read |
| `[6C pN]` | `C:\Users\yongw\Downloads\IE4155 Part 6C AY24-25.pdf` (34 pp) | text layer + page renders (equations are images) |
| `[P.676-13]` | ITU-R P.676-13 (08/2022) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.676-13-202208-I!!PDF-E.pdf` | downloaded, text extracted |
| `[P.838-3]` | ITU-R P.838-3 (03/2005) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf` | downloaded, text extracted |
| `[P.526-15]` | ITU-R P.526-15 (10/2019) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.526-15-201910-S!!PDF-E.pdf` | downloaded, text extracted |
| `[P.372-17]` | ITU-R P.372-17 (08/2024) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.372-17-202408-I!!PDF-E.pdf` | downloaded, text extracted |
| `[P.617-5]` | ITU-R P.617-5 (08/2019) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.617-5-201908-S!!PDF-E.pdf` | downloaded, text extracted |
| `[P.368-10]` | ITU-R P.368-10 (08/2022) `https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.368-10-202208-I!!PDF-E.pdf` | downloaded, text extracted |
| `[Hum]` | S. V. Hum, *Ionospheric Propagation*, ECE422 notes, U. Toronto — `https://www.waves.utoronto.ca/prof/svhum/ece422/notes/20c-ionosphere.pdf` | downloaded, text extracted |

---

## 1. Formulas — explicit, with units and symbol definitions

### 1.1 Free-space loss

Physical chain `[P1-4 p.6-7]`:

```
P_F  = P_T / (4 π d²)                W/m²      power flux density from an isotropic radiator
G    = 4 π A_e / λ²                  -          antenna gain / effective aperture relation
A_e  = λ² / (4π)   for G = 1         m²         effective aperture of an isotropic antenna
P_R / P_T = λ² / (4 π d)²            -
```

Loss in dB:

```
A_FS = 20 log10( 4 π d / λ )                         dB      [P1-4 p.7]
```

Engineering forms (identical, different units):

```
A_FS(dB) = 32.44 + 20 log10 f(MHz) + 20 log10 d(km)
A_FS(dB) = 92.4  + 20 log10 f(GHz) + 20 log10 d(km)          [P1-4 p.7, the 92.4 form is the one printed]
```

Exact constants are **32.4478** and **92.4478** (= 20 log10(4π·10⁹/c) with c = 2.99792458×10⁸ m/s).
Using 32.44 / 92.4 costs 0.04 dB — verified by direct computation this session, e.g. 900 MHz at 4 km:
103.57 dB (32.44 form) vs 103.53 dB (92.4 form).

Symbols: `d` path length, `λ` wavelength, `f` frequency, `P_T`/`P_R` transmit/receive power,
`A_e` effective aperture, `G` gain (linear).

> **Slide error to not reproduce.** `[P1-4 p.7]` states the loss is "proportional to `d`" and
> "proportional to frequency `F`". The *loss ratio* goes as `d²` and `f²`; only the **dB** value
> goes as `20 log d` and `20 log f`. The visualisation must not repeat the slide's wording.

Worked values computed this session from the formula above:

| f | d | A_FS |
|---|---|---|
| 150 MHz | 1 km | 75.96 dB |
| 900 MHz | 4 km | 103.57 dB |
| 2 GHz | 300 km | 148.00 dB |
| 12 GHz | 36 000 km (GEO) | 205.15 dB |
| 28 GHz | 200 m | 107.40 dB |

`[P1-4 p.26]` says satellite links suffer "approximately 40 dB more" free-space loss than terrestrial;
that is a statement about the *distance ratio* (36 000 km vs ~360 km → 40 dB), not a separate loss term.

### 1.2 Radio horizon with the 4/3 earth

```
d1 = sqrt( 12.75 · k · H1 )  = sqrt( 17 · H1 )   for k = 4/3
d2 = sqrt( 12.75 · k · H2 )  = sqrt( 17 · H2 )   for k = 4/3
d  = d1 + d2                                      (LOS grazes the earth)
```
`d1, d2, d` in **km**, `H1, H2` in **metres**, `k` dimensionless `[P1-4 p.11]`.

Origin: `d = sqrt(2 · k · a · H)` with `a = 6371 km`; `2a/1000 = 12.742 ≈ 12.75`, and `12.75 × 4/3 = 17.0`.

Computed this session:

| H | k = 1 (true earth) | k = 4/3 |
|---|---|---|
| 2 m | 5.05 km | 5.83 km |
| 10 m | 11.29 km | 13.04 km |
| 30 m | 19.56 km | 22.58 km |
| 100 m | 35.71 km | 41.23 km |
| 300 m | 61.85 km | 71.41 km |
| 1 000 m | 112.92 km | 130.38 km |
| 10 000 m (airliner) | 357.07 km | 412.31 km |

### 1.3 Earth bulge and effective-earth factor k

```
B = d1 d2 / (2 k a)                                MKS units              [6B p.26]
B(m) = d1(km) · d2(km) / (12.75 · k)                                       [6B p.26, p.27]
```
`B` = height of the earth's bulge above the chord, at the point `d1` from one end and `d2` from the other.

Effective antenna heights on a curved earth (reduce curved geometry to the plane-earth model) `[6B p.23-24]`:

```
h'1(m) = h1(m) − d1(km)² / (12.75 k)
h'2(m) = h2(m) − d2(km)² / (12.75 k)
```

Refractivity → k `[6B p.32-34]`:

```
N  = (n − 1) × 10⁶                    typically N ≈ 350 at the surface, n ≈ 1.00035
N  = 77.6 P/T + 3.75×10⁵ e/T²         P, e in mb (hPa), T in K
1/a_e = 1/(k a) = 1/a + (dN/dh)×10⁻⁶
k  = [ 1 + 6370 (dN/dh) × 10⁻⁶ ]⁻¹ = [ 1 + (dN/dh)/157 ]⁻¹
```

Median `dN/dh = −40 N-units/km` → `a_e = 8500 km` → `k = 4/3` `[6B p.34]`.

Regimes `[6B p.36]`:

| Regime | k | dN/dh (N/km) | Bulge |
|---|---|---|---|
| Sub-refraction | 4/3 > k > 0 | > −40 | larger than normal |
| Normal | 4/3 (≈50 % of time) | −40 | reference |
| Super-refraction | ∞ > k > 4/3 | −157 < dN/dh < −40 | smaller than normal |
| Flat earth | k = ∞ | −157 | zero |
| Ducting | 0 > k > −∞ | < −157 | concave (a_e < 0) |

Bulge computed this session (mid-path, `d1 = d2 = d/2`):

| Path length | k = 2/3 | k = 1 | k = 4/3 |
|---|---|---|---|
| 10 km | 2.94 m | 1.96 m | 1.47 m |
| 20 km | 11.76 m | 7.84 m | 5.88 m |
| 50 km | 73.53 m | 49.02 m | 36.76 m |
| 100 km | 294.12 m | 196.08 m | 147.06 m |

This is the quantitative reason `[6C p.33]` gives: k is irrelevant at 10 km and dominant at 100 km.

### 1.4 Fresnel zones

Definition of the n-th Fresnel ellipsoid `[6C p.7-8]`, `[P.526-15 eq (1)]`:

```
(TP + PR) − TR = n λ / 2
```

Radius derivation `[6C p.9-10]`, using the binomial expansion `d' ≈ d + r²/(2d)`:

```
n λ / 2 = (r²/2)(1/d1 + 1/d2) = r² d / (2 d1 d2)
```

so

```
r_n = sqrt( n d1 d2 λ / d )                      self-consistent units
F1  = sqrt( d1 d2 λ / d )                        m
F_n = sqrt(n) · F1                                                        [6C p.10-11]
```

Practical form (`d1, d2, d` in km, `F` in **GHz**, `F_n` in **metres**) `[6C p.11]`:

```
F_n = sqrt(n) · 17.3 · sqrt( d1 d2 / (F d) )
```

The 17.3 comes from `sqrt(0.3 × 1000) = 17.32` (λ = 0.3/F GHz metres, km→m conversion).

Note `[6C p.13]`: **all Fresnel zones have equal area**, which is why the alternating +/− pixel
cancellation argument works.

Computed this session (mid-path `d1 = d2 = d/2`):

| f | d = 1 km | d = 10 km | d = 50 km |
|---|---|---|---|
| 100 MHz | F1 = 27.35 m (0.6F1 = 16.41) | 86.50 m (51.90) | 193.42 m (116.05) |
| 900 MHz | 9.12 m (5.47) | 28.83 m (17.30) | 64.47 m (38.68) |
| 2.4 GHz | 5.58 m (3.35) | 17.66 m (10.59) | 39.48 m (23.69) |
| 6 GHz | 3.53 m (2.12) | 11.17 m (6.70) | 24.97 m (14.98) |
| 18 GHz | 2.04 m (1.22) | 6.45 m (3.87) | 14.42 m (8.65) |
| 38 GHz | 1.40 m (0.84) | 4.44 m (2.66) | 9.92 m (5.95) |
| 80 GHz | 0.97 m (0.58) | 3.06 m (1.83) | 6.84 m (4.10) |

### 1.5 Knife-edge diffraction, J(ν)

Diffraction parameter (equivalent forms) `[P.526-15 eq (26)-(29)]`:

```
ν = h sqrt( (2/λ)(1/d1 + 1/d2) )
ν = θ sqrt( 2 / (λ (1/d1 + 1/d2)) )      (θ = diffraction angle, rad, < ~0.2 rad)
ν = sqrt( 2 h θ / λ )                    (sign of h and θ)
ν = sqrt( 2 d / λ ) · α1 α2              (sign of α1, α2)
```
`h` = height of the obstacle top **above** the T–R straight line (negative if below), `d1`,`d2` the
distances from each end to the obstacle, `d` the path length, all in self-consistent units.

Course notes form `[6C p.22]`, in terms of obstruction `O` (= negative clearance) and `F1`:

```
ν = sqrt(2) · (O / F1)
```
Equivalent, since `F1 = sqrt(λ d1 d2/d)` and `ν = h sqrt(2(d1+d2)/(λ d1 d2)) = h √2 / F1`.

Exact loss `[P.526-15 eq (30)]`:

```
J(ν) = −20 log10 ( sqrt( (1 − C(ν) − S(ν))² + (C(ν) − S(ν))² ) / 2 )      dB
```
with `C(ν)`, `S(ν)` the Fresnel cosine/sine integrals.

Approximation `[P.526-15 eq (31)]`, valid **ν > −0.78**:

```
J(ν) ≈ 6.9 + 20 log10 ( sqrt( (ν − 0.1)² + 1 ) + ν − 0.1 )               dB
```

`[6C p.22]` prints the same expression but states the validity limit as **ν ≥ −0.7**.
**Both are given here; ITU says −0.78.** (Practical difference: the ITU limit is where J(ν) crosses
0 dB. Computed this session: J(−0.78) = 0.00 dB, J(−0.70) = 0.54 dB.)

Computed this session from eq (31):

| ν | J(ν) |
|---|---|
| −0.78 | 0.00 dB (formula's zero crossing / lower validity bound) |
| −0.70 | 0.54 dB |
| −0.50 | 1.96 dB |
| 0.00 (grazing) | **6.03 dB** |
| +0.50 | 10.29 dB |
| +1.00 | 13.93 dB |
| +2.00 | 19.04 dB |
| +3.00 | 22.42 dB |

Two benchmarks the notes state and this computation confirms:
- **Grazing (C = 0, ν = 0) → 6 dB loss** `[6C p.21]`, computed 6.03 dB.
- **Clearance ≥ 0.6 F1 → diffraction loss negligible** `[6C p.21]`; the exact break-even is
  0.577 F1 `[6C p.29]` — computed: C = 0.577 F1 gives ν = −0.816, J = −0.23 dB;
  C = 0.6 F1 gives ν = −0.849, J = −0.44 dB (i.e. very slightly *above* free space).
  `[P.526-15 §2.3, §2.5]` independently uses "60 % of the first Fresnel zone radius" as the LOS/diffraction
  boundary.

Worked example `[6C p.20]`: 150 MHz, d = 1 km, obstacle at mid-path, h1 = h2 = 27 m, obstacle 21 m.
`F1 = 17.3 sqrt(0.5×0.5 / (0.15×1)) = 22.33 m`; clearance C = 6 m; `C/F1 = 0.27`.
The slide reads **−2.7 dB off Figure C.5**. Computing eq (31) with ν = −√2(0.27) = −0.382
gives **2.86 dB**. Report both — the ~0.15 dB gap is graph-reading error, and it is a good
teaching moment about why a curve read by eye is not a computation.

### 1.6 Two-ray plane-earth model

Geometry and path difference `[6B p.6-9]`:

```
Δd = d[1 + ((h2−h1)/d)²]^½ − d[1 + ((h2+h1)/d)²]^½
   → |Δd| = 2 h1 h2 / d                            m      (binomial expansion, h/d << 1)
ΔΦ = (2π/λ) Δd = 4 π h1 h2 / (λ d)                 rad
```

Vector sum with ground reflection coefficient `R = |R| ∠φ`; for small grazing angle ψ,
`R ≈ −1` i.e. `|R| = 1`, `φ = 180°` `[6B p.10]`:

```
Resultant (voltage, normalised to the direct ray) = 1 + R·exp[ j(ΔΦ + 180°) ]
|E/E0| = 2 |sin(ΔΦ/2)| = 2 |sin( 2 π h1 h2 / (λ d) )|                     [6B p.11]
```

Nulls when `ΔΦ = n·360°` (even Fresnel zones), maxima at odd zones `[6B p.14]`.

**Breakpoint distance** (first and last maximum of the lobing pattern, where `ΔΦ/2 = π/2`):

```
d_b = 4 h1 h2 / λ                                   m
```
This is the standard breakpoint; it is *implied* by `[6B p.11]` but is **not printed in the slides** —
derive it, do not cite the deck for it. Beyond `d_b` the sine argument is small and the model
collapses to the far-field asymptote `[6B p.13]`:

```
sin θ ≈ θ  ⟹  |E/E0| = 4 π h1 h2 / (λ d)      [< 1, so it is a LOSS]
gain due to plane-earth reflection = 20 log10( 4 π h1 h2 / (λ d) )   dB
```

Combined with free-space `20 log d`, total loss `∝ 40 log d`, i.e. **received power ∝ d⁻⁴**
`[6B p.16-17]`. Equivalent closed form (algebra from the two slides):

```
L_plane-earth(dB) = 40 log10 d − 20 log10 h1 − 20 log10 h2      (d, h1, h2 in the same unit)
```

Path exponent summary `[6B p.19]`: n = 2 LOS no reflection; n = 4 LOS with ground reflection;
n > 4 obstructed LOS.

Worked check computed this session against the slide's own example `[6B p.16]`
(900 MHz, λ = 0.3331 m, h1 = 40 m, h2 = 1.5 m, d = 4 km):
- `ΔΦ = 0.5659 rad = 32.4°` — matches the slide's "2π×0.09 (small angle − 32.4°)".
- Exact `|E/E0| = 2 sin(ΔΦ/2) = 0.5584` → **−5.06 dB** relative to free space.
- Small-angle form `4πh1h2/(λd) = 0.5659` → **−4.95 dB**. (0.11 dB error at 32°.)
- `40 log d − 20 log h1 − 20 log h2 = 108.52 dB`; free space 103.53 dB + 5.06 dB = 108.59 dB. Consistent.

Breakpoints computed this session:

| f | h1 | h2 | λ | d_b = 4h1h2/λ |
|---|---|---|---|---|
| 150 MHz | 27 m | 27 m | 1.999 m | 1.46 km |
| 900 MHz | 40 m | 1.5 m | 0.333 m | 0.72 km |
| 900 MHz | 30 m | 1.5 m | 0.333 m | 0.54 km |
| 1800 MHz | 30 m | 1.5 m | 0.167 m | 1.08 km |
| 2.4 GHz | 10 m | 2 m | 0.125 m | 0.64 km |
| 28 GHz | 10 m | 1.5 m | 0.0107 m | 5.60 km |

### 1.7 Secant law and MUF

Plasma / critical frequency `[Hum eq (15)]`:

```
f_c = 9 sqrt( N_max )        Hz, with N_max in electrons/m³
```
(e.g. N_max = 1.0×10¹² e/m³ → f_c = 9 MHz.)

Secant law `[Hum eq (17)]`:

```
f_ob = f_c · sec( θ_i )  = MUF
```
`θ_i` = angle of incidence at the layer, measured **from the local vertical at the reflection point**.

Flat-earth obliquity factor `[Hum eq (18)]`:

```
sec θ_i = sqrt( (D / (2 h0))² + 1 )
```
`D` = ground range of one hop, `h0` = virtual reflection height.

**Spherical-earth obliquity factor** (correct for D ≳ 1000 km; derive, do not use the flat form):

```
γ = D / (2 R_e)                            central half-angle, rad
r = R_e / (R_e + h0)
tan θ_i = r sin γ / (1 − r cos γ)
elevation angle at the ground  β = 90° − θ_i − γ
```

Maximum single-hop skip distance `[Hum eq (19)]`:

```
d_max = 2 sqrt( 2 K R_e h0 )
```
with `K R_e = 8497 km` for the F layer this gives **d_max = 4516 km** `[Hum p.6]`.

Virtual heights `[Hum Table 1]`:

| Layer | Daytime | Nighttime |
|---|---|---|
| F2 | 250–400 km | — |
| F1 | 200–250 km | — |
| F (merged) | — | 300 km |
| E | 110 km | 110 km |

Obliquity factors computed this session (R_e = 6371 km):

| h0 | D | sec θ (flat) | sec θ (spherical) | θ_i | elevation β |
|---|---|---|---|---|---|
| 300 km | 500 km | 1.30 | 1.29 | 39.3° | 48.4° |
| 300 km | 1000 km | 1.94 | 1.86 | 57.4° | 28.1° |
| 300 km | 2000 km | 3.48 | 2.82 | 69.2° | 11.8° |
| 300 km | 3000 km | 5.10 | **3.28** | 72.3° | 4.3° |
| 110 km | 1000 km | 4.65 | 3.98 | 75.5° | 10.1° |
| 110 km | 2000 km | 9.15 | 5.38 | 79.3° | 1.7° |

The spherical value 3.28 at 3000 km is the physical basis of the operational parameter
**M(3000)F2** and of the rule of thumb "MUF ≈ 3 × f_c"
(`https://en.wikipedia.org/wiki/Maximum_usable_frequency`, retrieved this session, which also gives
the optimum working frequency as 80–90 % of MUF). **The flat-earth form over-predicts badly
(5.10 vs 3.28 at 3000 km) — the tool must use the spherical form.**

MUF computed this session (F2, h0 = 300 km):

| foF2 | D = 1000 km (sec 1.86) | D = 2000 km (sec 2.82) | D = 3000 km (sec 3.28) |
|---|---|---|---|
| 3 MHz | 5.6 MHz | 8.4 MHz | 9.8 MHz |
| 5 MHz | 9.3 MHz | 14.1 MHz | 16.4 MHz |
| 7 MHz | 13.0 MHz | 19.7 MHz | 23.0 MHz |
| 10 MHz | 18.6 MHz | 28.2 MHz | 32.8 MHz |
| 12 MHz | 22.3 MHz | 33.8 MHz | 39.4 MHz |

**foF2 day vs night.** foF2 is *measured*, not predicted, and swings with solar cycle, season and
latitude. Representative published mid/low-latitude figures found this session (web search, multiple
ionosonde studies): daytime maxima 13:00–15:00 LT, pre-dawn minima; one study reports daytime
≈ 8.2 MHz vs nighttime ≈ 4.4 MHz; another reports ≈ 5 MHz day falling to ≈ 2 MHz night at solar
minimum; seasonal monthly means 5–11 MHz. **A safe teaching range is ~3–5 MHz at night and
~7–12 MHz by day at mid-latitudes, higher at solar maximum.** Label it as a range, not a constant.
`[Hum p.5]` bounds the usable oblique MUF: "less than 40 MHz, and can be as low as 25–30 MHz in
periods of low solar activity."

Supporting mechanism from the course notes `[P1-4 p.21, p.25]`: D layer absorbs MF/lower-HF by day
and **disappears at night**, F1 and F2 merge at night into a single layer at approximately **250 km**
(`[Hum Table 1]` says 300 km — note the discrepancy). Lower launch angle → better chance of
refraction back to earth `[P1-4 p.23]`.

### 1.8 Troposcatter

`[P1-4 p.17-19]` is qualitative: Tx power up to ~10 kW, dish diameters up to 120 ft (36.6 m),
"a few hundred kilometres" without repeaters, 2/4/8-order frequency, space, angle and polarisation
diversity, bandwidth limited to "several MHz" by frequency-selective multipath fading, and the loss
increases with **scatter angle** and with **frequency**.

Quantitative model `[P.617-5 Annex 1 §4.1]`:

```
θ_e = d × 10³ / (k a)                        mrad     (a = 6370 km, k = 4/3 unless known)
θ   = θ_e + θ_t + θ_r                        mrad     scatter angle; θ_t, θ_r = horizon angles
L_c = 0.07 exp[ 0.055 (G_t + G_r) ]          dB       aperture-to-medium coupling loss
F   = 0.18 N_0 exp(−h_s/h_b) − 0.23 dN       dB       h_b = 7.35 km global-mean scale height
L_bs(p) = F + 22 log10 f + 35 log10 θ + 17 log10 d + L_c − Y_p     dB
Y_50 = 0
```
`d` km, `f` **MHz**, `θ` mrad, `G` dBi, `N_0` sea-level surface refractivity, `dN` refractivity
lapse rate through the lowest 1 km, `h_s` surface height (km).

Computed this session (N_0 = 350, dN = −40, h_s = 0, smooth-earth horizon angles = 0, p = 50 %):

| d | f | G_t = G_r | θ | L_c | L_bs(50 %) | free space | excess over FS |
|---|---|---|---|---|---|---|---|
| 150 km | 900 MHz | 35 dBi | 17.7 mrad | 3.3 dB | **221.1 dB** | 135.0 dB | 86.1 dB |
| 200 km | 2 GHz | 40 dBi | 23.6 mrad | 5.7 dB | **237.7 dB** | 144.4 dB | 93.2 dB |
| 300 km | 900 MHz | 40 dBi | 35.3 mrad | 5.7 dB | **239.2 dB** | 141.0 dB | 98.2 dB |
| 300 km | 2 GHz | 40 dBi | 35.3 mrad | 5.7 dB | **246.8 dB** | 148.0 dB | 98.9 dB |
| 500 km | 2 GHz | 45 dBi | 58.9 mrad | 9.9 dB | **262.5 dB** | 152.4 dB | 110.1 dB |
| 500 km | 5 GHz | 45 dBi | 58.9 mrad | 9.9 dB | **271.3 dB** | 160.4 dB | 110.9 dB |

Note `L_c`: **doubling antenna gain does not buy you 2× gain** — going from 35 to 45 dBi per end
adds 20 dB of gain but 6.6 dB of coupling loss. That is the aperture-to-medium coupling loss, and it
is the single most surprising fact about troposcatter for a student.

Slow fading: hourly-median transmission loss is approximately **log-normal with σ ≈ 4–8 dB**
depending on climate; fast fading over ≤ 5 min is approximately **Rayleigh** `[P.617-5 §4]`.

### 1.9 Received-signal-vs-distance regime picture

`[P1-4 p.10, Fig. 3]` and `[6B p.18, Fig. B.4]` — the master diagram the tool should reproduce:
three regions, referenced to the free-space value, as the receiver moves away at fixed antenna
heights: **LOS region** (interference lobing, ~d⁻² envelope) → **diffraction / shadow region**
(loss increasing rapidly) → **troposcatter region** (very high but slowly varying loss).

---

## 2. Realistic numbers per band

Band edges and mechanisms from `[P1-4 p.29-31]`; wavelengths computed this session from
λ = c/f, c = 2.99792458×10⁸ m/s. Ranges are order-of-magnitude teaching figures — sources noted.

| Band | Frequency | Wavelength (λ at low → high edge) | Dominant mechanism | Typical usable range | What limits it |
|---|---|---|---|---|---|
| **VLF** | 3–30 kHz | 99 931 → 9 993 m | Earth–ionosphere waveguide `[P1-4 p.29]` | Global (many 1000s km); submarine comms, OMEGA navigation `[P1-4 p.29]` | Enormous antennas, ~100 Hz of usable bandwidth; waveguide mode attenuation |
| **LF** | 30–300 kHz | 9 993 → 999 m | Surface (ground) wave `[P1-4 p.29]` | "Stable transmission distance up to 1500 km" `[P1-4 p.29]`; LORAN, beacons | Ground conductivity; bandwidth (a few kHz); antenna efficiency |
| **MF** | 300–3000 kHz | 999 → 100 m | Surface wave (short range) + sky wave (long range at night) `[P1-4 p.29-30]` | ~50–160 km over average land by day; >1000 km at night by E/F-layer sky wave `[P1-4 p.25]`, web-search consensus | **D-layer absorption by day** `[P1-4 p.25]`; fading where ground wave and sky wave interfere `[P1-4 p.25]` |
| **HF** | 3–30 MHz | 100 → 10 m | Sky wave (ionospheric) `[P1-4 p.30]` | 3–6 MHz continental, 6–30 MHz inter-continental; single F2 hop up to ~4500 km `[Hum p.6]`, multi-hop worldwide | MUF above (penetration) and LUF below (absorption); bandwidth only "several kHz" `[P1-4 p.28]`; solar/diurnal variability |
| **VHF** | 30–300 MHz | 9.99 → 1.00 m | Space wave: LOS + diffraction `[P1-4 p.30]` | Radio horizon: ~40 km from 100 m, ~130 km from 1000 m (k = 4/3, computed §1.2); TV Band I/III, FM Band II | Earth curvature/horizon; terrain diffraction loss; ~40 MHz upper bound for ionospheric return `[Hum p.5]` |
| **UHF** | 300–3000 MHz | 999 → 100 mm | Space wave `[P1-4 p.30]`; troposcatter to ~500 km at 5 GHz `[P1-4 p.30]` | Cellular cells 0.5–30 km; d⁻⁴ two-ray regime beyond the breakpoint (§1.6) | Ground-reflection cancellation (40 log d), buildings/clutter, Fresnel-zone blockage |
| **SHF** | 3–30 GHz | 100 → 10 mm | Pure LOS `[P1-4 p.31]` | Microwave relay hops typically 10–60 km; earth–space | **Rain attenuation becomes a problem** `[P1-4 p.31]`; path clearance / k-factor fading; needs unobstructed 0.6 F1 |
| **EHF** | 30–300 GHz | 10 → 1 mm | LOS only `[P1-4 p.31]` | ~0.2–5 km terrestrial; satellite-to-satellite links `[P1-4 p.31]` | **Rain attenuation significant** `[P1-4 p.31]`; the 60 GHz O₂ band (14.7 dB/km, §3) and 183 GHz H₂O band (28.3 dB/km) |
| Optical/FSO | > 300 GHz | < 1 mm | LOS `[P1-4 p.31]` | Hundreds of m to a few km | "Visibility important" `[P1-4 p.31]` — fog, not rain, dominates |

Satellite band shorthand `[P1-4 p.26]`: L/C (Inmarsat), C-band 4/6 GHz (INTELSAT), Ku 11/14 GHz,
Ka 20/30 GHz; GEO altitude ~36 000 km. `[P1-4 p.27]` notes Ku-band in Singapore is severely
attenuated by tropical rain while the same band is used routinely in temperate regions — the
tool should make this a live comparison, not a footnote.

---

## 3. Gaseous attenuation reference points

**Computed this session** with a full implementation of the `[P.676-13]` Annex 1 line-by-line model
(equations 1–9, spectroscopic Tables 1 and 2 transcribed from pp. 8–10 of the Recommendation).
Conditions are the Recommendation's own reference case `[P.676-13 §1, p.3]`:
**p_tot = 1013.25 hPa, T = 15 °C, water-vapour density ρ = 7.5 g/m³** (and a dry atmosphere for
comparison). Water-vapour partial pressure `e = ρT/216.7 = 9.97 hPa`; dry-air pressure
`p = 1003.28 hPa`.

| f (GHz) | γ_o dry air (dB/km) | γ_w water vapour (dB/km) | **γ total (dB/km)** | dry atmosphere (dB/km) |
|---|---|---|---|---|
| 1 | 0.0053 | 0.0001 | **0.0054** | 0.0054 |
| 10 | 0.0081 | 0.0059 | **0.0140** | 0.0081 |
| 22 | 0.0129 | 0.1755 | **0.1884** | 0.0130 |
| 35 | 0.0312 | 0.0690 | **0.1003** | 0.0315 |
| 60 | 14.5021 | 0.1536 | **14.6557** | 14.6511 |
| 77 | 0.0956 | 0.2485 | **0.3441** | 0.0962 |
| 100 | 0.0330 | 0.4210 | **0.4540** | 0.0332 |
| 200 | 0.0135 | 2.8509 | **2.8643** | 0.0137 |

Extra points from the same computation (useful for drawing the curve correctly):

| f (GHz) | γ total (dB/km) | note |
|---|---|---|
| 5 | 0.0086 | |
| 12 | 0.0180 | Ku |
| 20 | 0.1088 | rising edge of the H₂O line |
| **22.235** | **0.1933** | **H₂O line centre** `[P.676-13 Table 2]` |
| 30 | 0.0929 | window between H₂O and O₂ |
| 40 | 0.1294 | |
| 50 | 0.3820 | O₂ band starting |
| 57 | 10.1168 | |
| **60** | **14.6557** | **O₂ band peak region** |
| 61 | 15.0421 | |
| 70 | 0.5062 | falling off the O₂ band |
| 94 | 0.4044 | window |
| **118.75** | **1.9436** | **isolated O₂ line** `[P.676-13 Table 1]` |
| 140 | 0.9155 | window |
| **183.31** | **28.2599** | **strong H₂O line** `[P.676-13 Table 2]` |
| 300 | 5.2031 | |

Structural facts to teach, straight from `[P.676-13 §1, pp.3-6]`:
- The 60 GHz feature is **not one line**: "near 60 GHz, many oxygen absorption lines merge together
  at sea-level pressures to form a single, broad absorption band". Table 1 lists **37 individual O₂
  lines between 50.474 and 68.960 GHz**. At altitude the pressure broadening drops and the individual
  lines resolve (their Fig. 2, 0/5/10/15/20 km).
- The 22.235 GHz feature **is** a single water-vapour line, and it is weak — 0.19 dB/km, only ~14×
  the dry-air value at that frequency. It is a bump, not a wall.
- The 183.31 GHz water line is 150× stronger than the 22 GHz line at sea level.
- Below ~10 GHz the dry-air contribution is the non-resonant **Debye spectrum**; above ~100 GHz it is
  pressure-induced **nitrogen** absorption `[P.676-13 §1 eq (8)]`.

---

## 4. Rain attenuation reference points

Model `[P.838-3 eq (1)]`: `γ_R = k · R^α` dB/km, `R` in mm/h. Coefficients read directly from
`[P.838-3 Table 5]`; the products below were **computed this session**.

`[P.838-3 Table 5]` coefficients used:

| f (GHz) | k_H | α_H | k_V | α_V |
|---|---|---|---|---|
| 1 | 0.0000259 | 0.9691 | 0.0000308 | 0.8592 |
| 10 | 0.01217 | 1.2571 | 0.01129 | 1.2156 |
| 22 | 0.1155 | 1.0329 | 0.1170 | 0.9700 |
| 35 | 0.3374 | 0.9047 | 0.3224 | 0.8761 |
| 60 | 0.8606 | 0.7656 | 0.8515 | 0.7486 |
| 77 | 1.1320 | 0.7177 | 1.1276 | 0.7073 |
| 100 | 1.3671 | 0.6815 | 1.3680 | 0.6765 |
| 200 | 1.6378 | 0.6382 | 1.6443 | 0.6343 |

Specific attenuation γ_R (dB/km), horizontal / vertical polarisation:

| f (GHz) | 5 mm/h | 25 mm/h | 50 mm/h | 100 mm/h |
|---|---|---|---|---|
| 1 | 0.000 / 0.000 | 0.001 / 0.000 | 0.001 / 0.001 | 0.002 / 0.002 |
| 10 | 0.092 / 0.080 | 0.696 / 0.565 | 1.664 / 1.312 | 3.976 / 3.047 |
| 22 | 0.609 / 0.557 | 3.210 / 2.656 | 6.568 / 5.202 | 13.439 / 10.190 |
| 35 | 1.447 / 1.321 | 6.207 / 5.409 | 11.620 / 9.928 | 21.754 / 18.222 |
| 60 | 2.951 / 2.841 | 10.117 / 9.477 | 17.200 / 15.923 | 29.242 / 26.754 |
| 77 | 3.593 / 3.520 | 11.406 / 10.988 | 18.758 / 17.941 | 30.849 / 29.292 |
| 100 | 4.094 / 4.064 | 12.260 / 12.072 | 19.663 / 19.295 | 31.536 / 30.838 |
| 200 | 4.574 / 4.564 | 12.777 / 12.668 | 19.886 / 19.662 | 30.950 / 30.520 |

Polarisation mixing for arbitrary tilt τ and elevation θ `[P.838-3 eq (4)-(5)]`:

```
k = [ k_H + k_V + (k_H − k_V) cos²θ cos 2τ ] / 2
α = [ k_H α_H + k_V α_V + (k_H α_H − k_V α_V) cos²θ cos 2τ ] / (2k)      (τ = 45° for circular)
```

Things this table settles:
- **Rain attenuation saturates.** From 100 → 200 GHz at 100 mm/h it goes *down* slightly
  (31.5 → 31.0 dB/km). Above ~100 GHz the raindrops are already large compared to λ and the
  attenuation stops climbing. A monotonically-rising cartoon curve is wrong.
- **Vertical polarisation is always better than horizontal** in rain (flattened drops), and the gap
  is largest in the 10–35 GHz range: at 22 GHz, 100 mm/h, H = 13.4 vs V = 10.2 dB/km — 3.2 dB/km.
- At 1 GHz rain is irrelevant (0.002 dB/km at 100 mm/h). Rain does not "affect all bands a bit".
- 5 mm/h at 10 GHz is 0.09 dB/km. Over a 20 km hop that is 1.8 dB — a rounding error.
  100 mm/h at 35 GHz over the same hop is 435 dB. That ratio is the whole story of mm-wave link design.

Note on `[P1-4 p.27]`: the claim that Ku-band is "severely attenuated by very heavy rain" in the
tropics is quantitatively supported here (12 GHz, tropical rates → several dB/km on a slant path);
the notes give no numbers, so use the P.838 values.

---

## 5. Radio noise (P.372-17) — the floor the link budget sits on

External noise figure `F_a` (dB above kT₀b) for a short vertical lossless grounded monopole
`[P.372-17 §6.1.1 eq (17), Table 1]`:

```
F_am = c − d log10 f        f in MHz, valid 0.3–250 MHz
```

| Environment | c | d |
|---|---|---|
| City (curve A) | 76.8 | 27.7 |
| Residential (curve B) | 72.5 | 27.7 |
| Rural (curve C) | 67.2 | 27.7 |
| Quiet rural (curve D) | 53.6 | 28.6 |
| Galactic noise (curve E) | 52.0 | 23.0 |

Galactic noise up to ~100 MHz `[P.372-17 §4.1 eq (15)]`: `F_am = 52 − 23 log10 f` (f in MHz),
decile deviations 2 dB. Galactic noise is not observed below foF2 and is suppressed up to about
3× foF2 `[P.372-17 §4.1]`.

Computed this session:

| Environment | 0.5 MHz | 1 MHz | 3 MHz | 10 MHz | 30 MHz | 100 MHz | 250 MHz |
|---|---|---|---|---|---|---|---|
| City | 85.1 | 76.8 | 63.6 | 49.1 | 35.9 | 21.4 | 10.4 |
| Residential | 80.8 | 72.5 | 59.3 | 44.8 | 31.6 | 17.1 | 6.1 |
| Rural | 75.5 | 67.2 | 54.0 | 39.5 | 26.3 | 11.8 | 0.8 |
| Quiet rural | 62.2 | 53.6 | 40.0 | 25.0 | 11.4 | −3.6 | −15.0 |
| Galactic | 58.9 | 52.0 | 41.0 | 29.0 | 18.0 | 6.0 | −3.2 |

Decile deviations of man-made noise `[P.372-17 Table 2]`: city ±(11.0 up / 6.7 low) dB in time,
8.4 dB in location; residential (10.6/5.3) and 5.8; rural (9.2/4.6) and 6.8.

Atmospheric (lightning) noise is given only as world charts of `F_am` at 1 MHz per season and
4-hour local-time block `[P.372-17 §5.1, Figs 13a–36a]` — there is no closed-form model. **Do not
invent one.** If the tool needs atmospheric noise, state it is chart-derived and give a range.

Consequence for the visualisation: at HF the receiver's own noise figure is irrelevant — external
noise is 40–60 dB above kT₀. At UHF and above it is the reverse. That crossover, around 100–300 MHz,
is why "more antenna gain" helps at microwave and "a better receiver" does not help at HF.

---

## 6. Ground-wave, path-clearance criteria and other design data

### 6.1 Ground wave
`[P.368-10]` provides no closed-form model — the prediction method is **software distributed with the
Recommendation** (`R-REC-P.368-10-202208-I!!ZIP-E.zip`), valid 10 kHz–30 MHz for a smooth homogeneous
spherical earth with both antennas on/near the surface `[P.368-10 Annex 1]`. Reference source: a short
vertical monopole radiating 1 kW giving 300 mV/m at 1 km. Convert field strength to basic
transmission loss with `[P.368-10 NOTE 1]`:

```
L_b = 142.0 + 20 log10 f(MHz) − E(dB(µV/m))       dB
```

Course-note range statements `[P1-4 p.14, p.29-30]`: surface wave is "a major mode of propagation
up to approximately 2 MHz"; above that, attenuation increases rapidly; for mobile use up to 20 MHz
it gives "ranges of a few kilometres". Seawater supports ground waves well, jungle terrain badly.
Below ~10–20 MHz both antennas sit on the surface so the direct and ground-reflected waves cancel
and **only** the surface wave reaches the receiver `[P1-4 p.14]` — this is the correct explanation
for why the two-ray model is not used at LF/MF.

### 6.2 Path clearance criteria `[6C p.28/p.31]`, sourced to CCIR Rec. 338.4 Appendix II

Ranked most stringent (1) to most relaxed (5) — clearance **and** minimum k must always be quoted
**together** `[6C p.27]`:

1. 0.6 F₁ at k = 2/3, **or** 0 F₁ at k = 1/2 (whichever is worse)
2. 0.6 F₁ at k = 2/3  ← commonly adopted for tropical regions `[6C p.29]`
3. 0.3 F₁ at k = 2/3, **or** 0.6 F₁ at k = 4/3 (worse of)
4. 0 F₁ at k = 2/3, **or** 0.6 F₁ at k = 4/3
5. 0 F₁ at k = 1, **or** 0.6 F₁ at k = 4/3

k may fall to 1/2 in difficult regions (Gulf of Mexico, Red Sea, Persian/Arabian Gulf) `[6C p.30]`.
High-capacity links (≥120 Mb/s or 1200 voice channels) demand the stringent criteria for
99.99 %+ reliability; 2 Mb/s / 24 channels is "low capacity" `[6C p.32]`.

### 6.3 Excessive clearance is also a fault `[6C p.24-26]`
Over a specular surface (sea, lake, flat roof): reflection tangential to an **odd** Fresnel ellipsoid
→ direct and reflected add (up to +6 dB); tangential to an **even** ellipsoid → they cancel (deep
null). The λ/2 geometric path difference plus the 180° reflection phase shift is what flips the sign.
The reflection lobes are visible in `[6C p.19, Fig. C.5 right portion]` and `[6B p.15, Fig. B.3]`.
Design must therefore constrain clearance from **both** sides.

---

## 7. Reproduction — scripts written and run this session

All computed values above come from these files (they re-run in a few seconds and print the tables verbatim):

- `<scratchpad>\p676.py` — full P.676-13 Annex 1 line-by-line model (Tables 1 & 2 transcribed,
  eq 1–9) plus a P.838-3 rain block.
- `<scratchpad>\calc2.py` — troposcatter (P.617-5), horizon, bulge, Fresnel radii, J(ν),
  two-ray/breakpoint.
- `<scratchpad>\calc3.py` — the §3/§4/§5 tables and free-space-loss cross-check.
- `<scratchpad>\muf.py` — spherical-earth MUF obliquity factors.

`<scratchpad>` = `C:\Users\yongw\AppData\Local\Temp\claude\C--Users-yongw-OneDrive-Desktop-Engineering\1d24b8ef-8195-46d6-b3ac-8ba0d34092e4\scratchpad`

Validation anchors that the P.676 implementation reproduces independently-known features of the
Recommendation's own Fig. 1: the 22.235 GHz H₂O line (0.193 dB/km), the merged 60 GHz O₂ band
(14.66 dB/km), the isolated 118.75 GHz O₂ line (1.94 dB/km) and the 183.31 GHz H₂O line
(28.26 dB/km) all land at the correct frequencies with the correct relative magnitudes.

---

## 8. Student misconceptions, and what the visualisation must show to kill each one

**M1. "Free-space loss means space absorbs the signal / higher frequency is absorbed more."**
Free space absorbs nothing. The `20 log f` term comes entirely from the receiving **isotropic
aperture shrinking as λ²** (`A_e = λ²/4π`, `[P1-4 p.6]`) — the flux density `P_T/4πd²` is
frequency-independent.
*Show:* an expanding sphere of constant total power, with a receive aperture that visibly shrinks
as the frequency slider rises. Then flip a switch to "fixed physical aperture (dish)" and show the
frequency dependence **reverses sign** — link gain goes as `f²` when both ends use fixed-size dishes.
That single toggle destroys the misconception permanently.

**M2. "Rain and gas attenuation just rise with frequency."**
They do not. Gas has a 60 GHz wall (14.7 dB/km) with a **window at 94 GHz (0.40 dB/km)** on the
far side; rain **saturates** above ~100 GHz and even falls slightly (31.5 dB/km at 100 GHz vs
31.0 at 200 GHz, 100 mm/h).
*Show:* one log-y plot, 1–300 GHz, with the real computed γ curve — resonances and windows both —
and a rain-rate slider overlaying γ_R. Mark 94 GHz and 140 GHz as windows explicitly, next to
60 GHz and 183 GHz as walls.

**M3. "Fresnel zone = the line of sight. If I can see it, the link is fine."**
The first Fresnel zone is a fat ellipsoid, and 0.6 F₁ of it must be clear.
*Show:* the ellipsoid drawn to scale against the path, with the F₁ number updating live. At
100 MHz over 50 km, F₁ = 193 m — a hill 100 m below the sight line still costs loss. At 38 GHz over
1 km, F₁ = 1.40 m — a lamppost matters. Same physics, four orders of magnitude of consequence.

**M4. "Grazing the obstacle = no loss."**
Grazing costs **6 dB** (`J(0) = 6.03 dB`, computed §1.5) — half the field, because exactly half the
wavefront is blocked.
*Show:* the knife edge sliding through the path with J(ν) plotted live, annotated at ν = 0 → 6 dB,
and the "clearance = 0.577 F₁ → 0 dB" crossing marked. Also show the **ripple above free space**
for ν < −0.78, which is where the diffracted field constructively interferes.

**M5. "More clearance is always better."**
Over water it is not: excessive clearance puts the specular reflection point in an **even** Fresnel
zone and the signal cancels `[6C p.24-26]`. Deep nulls at n = 2, 4, 6 are visible in
`[6C Fig. C.5]` / `[6B Fig. B.3]`.
*Show:* the same path over "sea" vs "forest" (|R| = 1 vs |R| ≈ 0), sweeping antenna height, with
the received level plotted against `√n = C/F₁`. Over sea the answer is a comb of nulls, not a
monotone curve.

**M6. "The earth's radius is 4/3 of the real one" / "k = 4/3 is a constant."**
k is a **median** (about 50 % of the time) derived from `dN/dh = −40 N/km` `[6B p.34-35]`. It swings
from ~1/2 (sub-refraction, bulge doubles) to ∞ (flat earth) to negative (ducting).
*Show:* a k slider from 0.5 to −4/3 that bends the earth profile *and* recomputes the bulge and
clearance live. At d = 100 km the bulge moves from 147 m (k = 4/3) to 294 m (k = 2/3) — the antenna
tower grows by 150 m in front of the student. At d = 10 km nothing visibly happens (1.5 → 2.9 m).
That contrast is the lesson `[6C p.33]`.

**M7. "Path loss follows one exponent — n = 2, or n = 4, take your pick."**
There is a **breakpoint**. Below `d_b = 4h₁h₂/λ` you get interference lobing; above it the ground
reflection is nearly anti-phase and you drop to d⁻⁴.
*Show:* the two-ray curve on log–log axes with `2 sin(2πh₁h₂/λd)` exactly (not the small-angle
approximation), the free-space `d⁻²` asymptote, the `d⁻⁴` asymptote, and a marker at `d_b`. Slide
`h₁` — the breakpoint moves and the whole lobe pattern rescales. At 900 MHz / 40 m / 1.5 m,
`d_b = 0.72 km`; at 28 GHz / 10 m / 1.5 m, `d_b = 5.6 km`.

**M8. "The ionosphere reflects like a mirror."**
It **refracts**; the "reflection height" you draw is a *virtual* height where the extrapolated
straight rays meet, above the true turning point `[Hum Fig. 4]`. And it only returns the signal if
the frequency is below `f_c sec θ_i`.
*Show:* the curved ray inside a shaded layer with the virtual height drawn as a dashed extrapolation,
plus a frequency slider that makes the ray punch through above MUF. Include the launch-angle slider —
lower angle, larger sec θ, higher MUF, longer hop `[P1-4 p.23]`.

**M9. "MUF = 3 × foF2, always."**
The factor is `sec θ_i`, a pure geometry function of hop length and layer height, and the
**flat-earth formula over-predicts it badly**: 5.10 vs 3.28 at D = 3000 km, h = 300 km (§1.7).
*Show:* a hop-length slider driving the spherical-earth sec θ live, next to (greyed out) the naive
flat-earth value, so the divergence is visible. Also show the day/night foF2 swing (~7–12 → ~3–5 MHz)
and the D-layer appearing/disappearing.

**M10. "Troposcatter is just very weak LOS; buy bigger dishes."**
Aperture-to-medium coupling loss `L_c = 0.07 exp[0.055(G_t+G_r)]` eats the gain: going from
35 dBi to 45 dBi per end adds 20 dB gain and 6.6 dB of coupling loss `[P.617-5 eq (3)]`.
*Show:* a link-budget bar chart where dragging antenna gain up grows the gain bar and simultaneously
grows a red L_c bar, with the net moving less than the student expects. Alongside it, the 99 dB
excess over free space at 300 km / 2 GHz — troposcatter is expensive.

**M11. "Reading a value off the textbook graph is the same as computing it."**
The course's own worked example `[6C p.20]` reads −2.7 dB off Fig. C.5 where eq (31) gives
**2.86 dB**.
*Show:* both, side by side, on the same example. This is the single best argument for the tool
existing at all.

---

## 9. DO NOT FAKE — quantities that must be computed from the real formula

Anything in this list, if drawn from an eyeballed curve or a hand-tuned spline, will produce a
visibly wrong teaching artefact. Compute it.

1. **Free-space loss.** `92.4478 + 20 log f(GHz) + 20 log d(km)`. Never a "typical" table.
2. **Gaseous attenuation γ(f).** Must come from `[P.676-13]` Annex 1 line-by-line (Tables 1 & 2,
   eq 1–9) or, if the runtime cannot carry 44 O₂ + 35 H₂O lines, from the §3 computed table
   **interpolated in log γ**. Never from a hand-drawn curve: the 60 GHz band shape, the 94 and
   140 GHz windows and the 118.75 GHz spike are all wrong if sketched. A curve that rises
   monotonically through 60 GHz is disqualifying.
3. **Rain attenuation γ_R.** `k R^α` with `[P.838-3 Table 5]` coefficients per frequency and
   polarisation, plus eq (4)–(5) for tilt/elevation. Never a power law with a single global exponent.
   The **saturation above 100 GHz** and the **H/V split** must both fall out of the real coefficients.
4. **Knife-edge diffraction J(ν).** `[P.526-15 eq (31)]` (or the Fresnel-integral eq (30) if you want
   the ripple for ν < −0.78 correct). The 6.03 dB grazing value and the 0.577 F₁ zero crossing must
   *emerge*, not be pinned by hand.
5. **Fresnel radius F₁.** `17.3 sqrt(d1 d2/(F d))` metres. Any drawing of the ellipsoid must be to
   this scale, or the whole "is the hill in the way?" intuition is broken.
6. **Earth bulge B and effective heights h′.** `d1 d2/(12.75 k)` metres. The k slider must recompute
   this, not scale a preset picture.
7. **Radio horizon.** `sqrt(12.75 k H)` km. Not `sqrt(17H)` hard-coded — that pins k at 4/3 and
   silently kills the k slider.
8. **Two-ray field.** `2 |sin(2π h1 h2/(λ d))|` **exactly**. Do not substitute the small-angle
   `4π h1 h2/(λ d)` form for the lobing region — it is only valid past the breakpoint
   (0.11 dB error already at ΔΦ = 32°, §1.6) and it erases every null.
9. **Breakpoint distance.** `4 h1 h2 / λ`, recomputed whenever f, h1 or h2 changes.
10. **MUF obliquity factor.** Spherical-earth `tan θ_i = r sin γ/(1 − r cos γ)`. The flat-earth
    `sqrt((D/2h)²+1)` may be shown as a *contrast*, never as the answer.
11. **Troposcatter loss.** `[P.617-5 eq (1)–(6)]` including `L_c` and the `35 log θ` term. A single
    "path loss + 100 dB" fudge hides the two things that matter (scatter-angle sensitivity and
    coupling loss).
12. **External noise F_a.** `c − d log f` from `[P.372-17 Table 1]`. Do not invent an atmospheric-noise
    formula — P.372 gives only charts for that; state the range and its source.
13. **Wavelengths.** `λ = c/f` with `c = 2.99792458×10⁸ m/s`, not `3×10⁸` — and never a lookup table
    of "band wavelengths" that quietly rounds.

Corollary: any number the tool displays should be traceable to one of these formulas or to a cited
table row. If a value can only be produced by "it looks about right", it does not belong in a
teaching tool whose entire purpose is to replace eyeballing a graph.

---

## 10. Where the course notes and the ITU references disagree

| Topic | Course notes | ITU / reference | What to do |
|---|---|---|---|
| Knife-edge approximation validity | `ν ≥ −0.7` `[6C p.22]` | `ν > −0.78` `[P.526-15 eq (31)]` | Use −0.78; note the notes' figure. J(−0.78) = 0.00 dB, J(−0.70) = 0.54 dB. |
| Negligible-diffraction clearance | "approximately 0.6 F₁ (0.577 F₁ to be exact)" `[6C p.21, p.29]` | "60 % of the first Fresnel zone radius" `[P.526-15 §2.3, §2.5]` | Agreement. Use 0.6 F₁ as the design rule, 0.577 F₁ as the exact zero-loss point. |
| Free-space constant | 92.4 `[P1-4 p.7]` | 92.4478 exact | 0.04 dB. Use the exact constant; mention the discrepancy once. |
| Free-space scaling wording | "proportional to d… proportional to frequency F" `[P1-4 p.7]` | Loss ratio ∝ d²f² | **Notes are wrong as written.** Show the dB form. |
| Worked diffraction example | 2.7 dB read off Fig. C.5 `[6C p.20]` | eq (31) gives 2.86 dB | Give both; use it as the graph-vs-formula lesson. |
| Earth radius in k formula | a = 6370 km `[6B p.33]`, 12.75 constant implies 6375 km `[6B p.27]` | `[P.617-5 §4]` uses a = 6370 km | Immaterial (<0.1 %). Use 6371 km and note that 12.75 is `2a/1000` rounded. |
| Night F1/F2 merge height | "approximately 250 km" `[P1-4 p.21]` | 300 km `[Hum Table 1]` | Give the range 250–300 km. Virtual height is itself variable. |
| Troposcatter range | "up to 500 km, 5 GHz" `[P1-4 p.30]`; "a few hundred km" `[P1-4 p.17]` | `[P.617-5]` model runs to any d; loss at 500 km / 2 GHz = 262 dB (computed) | Both consistent — 500 km is where the loss stops being affordable, not a physical wall. |
| Rain in Ku-band | qualitative, "severely attenuated" in tropics `[P1-4 p.27]` | `[P.838-3 Table 5]` gives numbers | Use P.838 numbers; the notes give none. |
