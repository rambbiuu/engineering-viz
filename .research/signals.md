# Signals, Modulation and Noise — Reference Sheet for Interactive Teaching Tools

Source-of-truth notes for a build agent. Every formula and number below is traced to a
specific PDF page or URL. Nothing here is from memory.

## 0. How to read the citations

| Tag | File |
|---|---|
| `[W1 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_LD_Week1_V4.0.pdf` |
| `[W2 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_LectureNotes_Week2 (1).pdf` |
| `[W3 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week3.pdf` |
| `[W5 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week5.pdf` |
| `[W6 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week6.pdf` |
| `[W7 pN]` | `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week7.pdf` (extra; used only for §5 noise/SNR) |

`pN` is the **PDF page number**, which in all six files equals the slide number printed in
the footer. Course: NTU EE3012 / IM3002 Communication Principles, A/Prof Guan Yong Liang.

**Extraction note.** `pdftotext` on these PDFs silently drops every math glyph (the equation
fonts carry no ToUnicode map — verified: line 199 of the Week 5 text dump reads
`"  =  cos[ + sin]"`). All formulas below were read from **rendered page images** (PyMuPDF
at 110 dpi), not from the text layer. Do not trust any text-layer extraction of these files.

---

## 1. Formulas, with units and symbol definitions

### 1.1 Symbol table (used throughout)

| Symbol | Meaning | Unit |
|---|---|---|
| `t` | time | s |
| `f` | frequency | Hz |
| `ω = 2πf` | angular frequency | rad/s |
| `A_c` | carrier amplitude | V |
| `f_c` | carrier frequency | Hz |
| `ω_c = 2πf_c` | carrier angular frequency | rad/s |
| `φ`, `θ` | phase | rad |
| `m(t)`, `s(t)` | message / modulating signal | V |
| `A_m` | message amplitude (single tone) | V |
| `f_m` | message frequency (single tone) | Hz |
| `w`, `W_i` | message bandwidth | Hz |
| `k_p` | phase sensitivity | rad/V |
| `k_f` | frequency sensitivity | Hz/V |
| `Δf` | peak frequency deviation | Hz |
| `Δφ` | phase deviation | rad |
| `β` | modulation index (= peak phase deviation) | rad (dimensionless) |
| `η` | noise two-sided PSD is `η/2` | W/Hz |
| `S_v(f)` | power spectral density of `v(t)` | W/Hz |

### 1.2 Fourier transform and the FT pairs the course uses

Definition `[W1 p12]`:

```
F.T. of v(t) = ∫_{-∞}^{∞} v(t) · exp(-j2πft) dt
```

Fourier spectrum = plot of the FT on both positive and negative frequency axes. In this
course "spectrum" means **amplitude** spectrum unless stated otherwise `[W1 p14]`.

Pair 1 `[W1 p12]`:
```
cos(2π f_c t)  ⟷  ½[ δ(f − f_c) + δ(f + f_c) ]
```
Spectrum: two impulses of height ½ at ±f_c.

Pair 2 `[W1 p13]` (`sinc(x) ≜ sin(πx)/(πx)`, stated explicitly on that slide):
```
rect(t/T)  ⟷  T · sinc(f T)
```
Time: unit-height gate from −T/2 to +T/2. Frequency: peak `T` at f = 0, zeros at ±1/T, ±2/T.

Pair 3 `[W1 p13]`:
```
Λ(t/T)  ⟷  T · sinc²(f T)
```
Time: unit-height triangle from −T to +T. Frequency: peak `T` at 0, zeros at ±1/T, ±2/T.

### 1.3 Filtering and bandwidth

`[W1 p15]`:
```
Y(f) = H(f) · X(f)
```
`H(f)` = filter transfer function (gain vs frequency), `X(f)` = FT of input, `Y(f)` = FT of output.

- Ideal lowpass: passes all `|f| < f_1`, rejects beyond `[W1 p16]`.
- Ideal bandpass: passes `f_1 ≤ |f| ≤ f_2` `[W1 p17]`.
- **Bandwidth** = range of *positive* frequency occupied by a spectrum `[W1 p18]`.

### 1.4 Signal power (two domains)

`[W1 p19]`, time domain:
```
mean{v²(t)} = (1/T_0) ∫_{-T_0/2}^{T_0/2} |v(t)|² dt        [W]
```
`T_0` = repetition period of `v(t)`; the overbar means time-average.

Frequency domain:
```
mean{v²(t)} = ∫_{-∞}^{∞} S_v(f) df
```
`S_v(f)` = **power spectral density (PSD)** of `v(t)`, in W/Hz.

Worked example on the same slide: for `v(t) = A cos(2πf_0 t + θ)`,
```
mean{v²(t)} = A²/2      — independent of f_0 and θ; also true for sine.
```

### 1.5 Conventional / full AM (for contrast)

`[W2 p4]`:
```
x(t) = A_c[1 + m·s(t)] cos 2πf_c t = A_c cos 2πf_c t  +  m A_c s(t) cos 2πf_c t
        ↑ carrier                      ↑ sidebands

X(f) = (A_c/2)δ(f − f_c) + (A_c/2)δ(f + f_c)
     + (m A_c/2) S(f − f_c) + (m A_c/2) S(f + f_c)
```
Spectrum occupies `f_c − w … f_c + w` (and mirror), with a discrete carrier line at `f_c`.

AM taxonomy `[W1 p20]`: Conventional/Full AM (analogue broadcast radio) · Suppressed-Carrier
AM (satellite comms) · Single Sideband AM (long-distance telephone) · Vestigial Sideband AM
(analogue broadcast TV) · Quadrature AM (PC modem, wireless LAN, digital TV).

### 1.6 DSBSC-AM and the Modulation Theorem

`[W2 p5]`:
```
x(t) = A_c · s(t) · cos 2πf_c t

X(f) = (A_c/2) [ S(f − f_c) + S(f + f_c) ]          ← Modulation Theorem
```
No carrier line. Sidebands span `f_c − w` to `f_c + w`. `[W2 p9]`: **AM signal BW = 2 × message BW**,
and modulation shifts the spectral centre from 0 to `f_c` while preserving spectral shape.

### 1.7 Coherent (synchronous) demodulation, with the phase-error term

`[W2 p12]` — full derivation, local oscillator with amplitude `A_c'` and phase error `φ`:
```
input:     x(t) = A_c s(t) cos 2πf_c t
internal:  v(t) = A_c' cos(2πf_c t + φ) · x(t)
                = A_c' cos(2πf_c t + φ) · A_c s(t) cos 2πf_c t
                = ½ A_c' A_c s(t) cos φ  +  ½ A_c' A_c s(t) cos(4πf_c t + φ)
                  └── wanted, baseband ──┘  └──── unwanted, at 2f_c ────┘
```
`[W2 p13]` — after a lowpass filter with **BW ≥ BW of s(t)**:
```
v_o(t) = ½ A_c' A_c cos φ · s(t)   = constant × s(t)
```
- `φ = 0` → maximum output.
- `φ = ±π/2` → `v_o(t) = 0`. "This must be avoided."
- General: output amplitude scales as `cos φ`. This is the term an interactive phase-error
  slider must implement — **amplitude ∝ cos φ, not a phase rotation of the recovered signal**
  (for real DSBSC there is only one quadrature; the loss is pure attenuation).

Spectrum picture `[W2 p12]`: `|V(f)|` has a triangle of width `2w` at DC (height doubled)
and copies at `±2f_c` of width `2w`.

Worked example `[W2 p15–p18]`: `s(t) = sinc(t/50)`, `f_c = 70 Hz`.
`x(t) = sinc(t/50) cos(2π70t)`; multiply by `cos(2π70t)`;
`= ½ sinc(t/50) + ½ sinc(t/50) cos(2π·140·t)`; LPF at **1/100 Hz** (the message BW);
output `= ½ sinc(t/50)`.

### 1.8 Frequency translation / mixing

`[W2 p20]`, input `x(t) = s(t) cos 2πf_c t`, local oscillator `cos 2πf_1 t`:
```
v_1(t) = x(t) cos 2πf_1 t
       = (s(t)/2) [ cos 2π(f_c − f_1) t  +  cos 2π(f_c + f_1) t ]
```
`[W2 p21]`, BPF centred at `f_o = f_c − f_1` with bandwidth = BW of `x(t)`:
```
v_2(t) = ½ s(t) cos 2π(f_c − f_1) t = ½ s(t) cos 2πf_o t
```
So a mixer **shifts `f_c` by ±f_1 and halves the amplitude**; the choice of `f_c − f_1` vs
`f_c + f_1` is made by the bandpass filter, not by the multiplier.

### 1.9 FDM: non-overlap design criteria

`[W3 p7]`, three channels, `f_i` = carrier frequency of `x_i(t)`, `W_i` = BW of `s_i(t)`:
```
f_2 − f_1 > W_1 + W_2
f_3 − f_2 > W_2 + W_3
```
Each DSBSC channel occupies `f_i ± W_i`, i.e. an RF width of `2W_i`. Generalisation the
build tool should enforce: **adjacent carriers must satisfy `f_{i+1} − f_i > W_i + W_{i+1}`.**

FDM signal `[W3 p6]`: `x_1(t) + x_2(t) + x_3(t)` where `x_i(t) = s_i(t) cos(2πf_i t)`.
"FDM = AM modulation with different `f_c` + summation."

De-multiplexing `[W3 p8–p9]`: BPF then coherent demod, with
`BPF centre = f_i` and `BPF bandwidth = 2W_i`.

### 1.10 QAM — I/Q modulator and demodulator

Modulator `[W3 p12]`:
```
x_1(t) = A_c s_1(t) cos 2πf_c t      = in-phase (I) signal
x_2(t) = A_c s_2(t) sin 2πf_c t      = quadrature-phase (Q) signal
x(t)   = x_1(t) + x_2(t)
       = A_c s_1(t) cos 2πf_c t + A_c s_2(t) sin 2πf_c t
```
The `sin` branch is generated by a **90° phase shifter** off the same `A_c cos 2πf_c t` carrier.

Demodulator `[W3 p13]`:
```
v_1(t) = x(t) cos 2πf_c t
       = A_c s_1(t) cos²2πf_c t + A_c s_2(t) sin 2πf_c t cos 2πf_c t
       = ½A_c s_1(t) + ½A_c s_1(t) cos 4πf_c t + ½A_c s_2(t) sin 4πf_c t

v_2(t) = x(t) sin 2πf_c t
       = ½A_c s_2(t) − ½A_c s_2(t) cos 4πf_c t + ½A_c s_1(t) sin 4πf_c t
```
After the LPFs (BW = BW of `s_1`, BW of `s_2` respectively) the outputs are
`½A_c s_1(t)` and `½A_c s_2(t)`. Note the cross-terms sit at `2f_c` — **with a perfect
90° reference the two channels do not leak into each other at baseband**; a phase error in
the local carrier is what creates I/Q crosstalk.

Worked example `[W3 p14–p16]`: `s_1 = sinc(t/50)`, `s_2 = sinc²(t/50)`, `f_c = 70 Hz`.
LPF BW for the I arm = **1/100 Hz**, for the Q arm = **1/50 Hz** (each equal to its own
message bandwidth). Outputs `½ sinc(t/50)` and `½ sinc²(t/50)`.

### 1.11 PM and FM: instantaneous phase and frequency

Carrier `[W5 p7]`: `c(t) = A_c cos[2πf_c t + φ]`, with
**PM: `φ → φ_0 + Δφ(t)`** and **FM: `f_c → f_c + Δf(t)`**.

**PM** `[W5 p7]`:
```
φ(t)   = φ_0 + k_p m(t)              φ_0 = initial phase (default 0)
Δφ(t)  = k_p m(t)                    [rad]      k_p in rad/volt
f_PM(t) = A_c cos[ 2πf_c t + k_p m(t) ]
```

**FM** `[W5 p8]`:
```
f_i(t) = f_c + k_f m(t)              Δf(t) = k_f m(t)   [Hz]   k_f in Hz/volt
θ_i(t) = 2π ∫_{-∞}^{t} f_i(τ) dτ = 2π( f_c t + k_f ∫_{-∞}^{t} m(τ) dτ )
f_FM(t) = A_c cos[ 2πf_c t + 2πk_f ∫_{-∞}^{t} m(τ) dτ ]
                                      └── Δφ(t), instantaneous phase deviation ──┘
```

Cross-relations `[W5 p10]` — this table is the exact PM↔FM duality:

| | Phase Modulation | Frequency Modulation |
|---|---|---|
| instantaneous phase deviation | `Δφ(t) = k_p m(t)` | `Δφ(t) = 2π k_f ∫_{-∞}^{t} m(τ)dτ` |
| instantaneous frequency deviation | `Δf(t) = (k_p/2π) · dm(t)/dt` | `Δf(t) = k_f m(t)` |
| peak phase deviation | `β = Δφ(t)\|_max = k_p \|m(t)\|_max` | `β = Δφ(t)\|_max = 2πk_f \|∫m(τ)dτ\|_max` |
| peak frequency deviation | `Δf = (k_p/2π) \|dm(t)/dt\|_max` | `Δf = k_f \|m(t)\|_max` |

Derivation shown in red on that slide: `ω(t) = dφ(t)/dt ⇒ Δω(t) = d/dt Δφ(t) ⇒ 2πΔf(t) = k_p dm/dt`.

Worked FM example `[W5 p9]`: `f_c = 100 Hz`, `k_f = 10 Hz/V`, `m(t)` a two-level staircase
(2 V for 2<t<4, 1 V for 4<t<6). Then `Δf(t)` is 20 Hz then 10 Hz; the FM waveform runs at
100 Hz → 120 Hz → 110 Hz → 100 Hz; `Δφ(t) = 2πk_f∫m` ramps at `40π` then `20π` rad/s and
**holds flat at 120π** afterwards (integrator, so phase never returns to zero).

### 1.12 Single-tone modulation and β for both

Message `m(t) = A_m cos 2πf_m t`.

**PM** `[W5 p11]`:
```
Δφ(t) = k_p m(t) = k_p A_m cos 2πf_m t = β_p cos 2πf_m t
β_p = k_p A_m  = peak phase deviation = modulation index for PM     [rad]
f_PM(t) = A_c cos[2πf_c t + β_p cos 2πf_m t]
```
Note **cosine** inside the PM phase term.

**FM** `[W5 p12]`:
```
Δf(t) = k_f m(t) = k_f A_m cos 2πf_m t = Δf · cos 2πf_m t ,   Δf = k_f A_m   [Hz]
Δφ(t) = 2π∫_0^t Δf(τ)dτ = (Δf/f_m) sin 2πf_m t = β sin 2πf_m t
β = Δf / f_m = k_f A_m / f_m = peak phase deviation = modulation index of FM
f_FM(t) = A_c cos[2πf_c t + β sin 2πf_m t]
```
Note **sine** inside the FM phase term. `β` is dimensionless (rad).

`[W5 p13]`: small β → narrowband FM → less noise suppression; large β → wideband FM →
better noise suppression.

### 1.13 NBFM small-angle expansion

`[W5 p15]`, exact then approximated:
```
f_FM(t) = A_c cos[ω_c t + β sin ω_m t]
        = A_c[ cos ω_c t · cos(β sin ω_m t) − sin ω_c t · sin(β sin ω_m t) ]
```
For narrowband FM or PM, **β ≤ 0.2** (the course's threshold):
```
β sin ω_m t ≪ 1  ⇒  cos(β sin ω_m t) ≈ 1 ,  sin(β sin ω_m t) ≈ β sin ω_m t

f_NBFM(t) ≈ A_c[ cos ω_c t − β sin ω_m t · sin ω_c t ]
          = A_c cos ω_c t + (βA_c/2) cos(ω_c + ω_m)t − (βA_c/2) cos(ω_c − ω_m)t
```
**BW of NBFM = 2 f_m, centred at f_c — same as AM BW** `[W5 p15]`. The distinguishing feature
vs AM: the lower sideband carries a **minus** sign.

### 1.14 WBFM Bessel series

`[W5 p16]` derivation: `e^{jβ sin ω_m t}` is periodic with fundamental `ω_m`, so
```
e^{jβ sin ω_m t} = Σ_{n=-∞}^{∞} C_n e^{jnω_m t} ,     C_n = (1/T)∫_{-T/2}^{T/2} e^{jβ sin ω_m t} e^{-jnω_m t} dt ,  T = 2π/ω_m
with x = ω_m t :   C_n = (1/2π) ∫_{-π}^{π} e^{j(β sin x − n x)} dx = J_n(β)
```
i.e. `C_n` **is** the nth-order Bessel function of the first kind.

`[W5 p17]` result (marked "proof not required"), valid for **any** β (NBFM or WBFM):
```
f_FM(t) = A_c Σ_{n=-∞}^{∞} J_n(β) · cos(ω_c + n ω_m) t
```
Equivalently in Hz `[W5 p20]`: `f_FM(t) = A_c Σ J_n(β) cos[2π(f_c + n f_m)t]`.

Spectrum: lines at `f_c + n f_m` for all integer n, amplitude `A_c |J_n(β)|`
(each real cosine of amplitude `A_c J_n(β)` shows as two half-height impulses at `±(f_c+nf_m)`).

Symmetry `[W5 p18]`:
```
J_{-n}(β) = J_n(β)      for even n
J_{-n}(β) = −J_n(β)     for odd n
```

Power `[W5 p19–p20]`:
```
Power of f_FM(t) = (A_c²/2) Σ_n J_n²(β) = A_c²/2      because Σ_n J_n²(β) = 1
```
**FM is constant-envelope: total power does not depend on β.** β only redistributes power
among the sidebands.

Worked WBFM example `[W5 p19–p20]`: `m(t) = 5cos[2π(8)t]`, `A_c = 100`, `f_c = 10³ Hz`,
`k_f = 8 Hz/V` ⇒ `β = k_f A_m / f_m = (8×5)/8 = 5`.
`f_FM(t) = 100 Σ J_n(5) cos[2π(1000 + 8n)t]`.
Spectrum line amplitudes printed on the slide (as "value/2", i.e. half-height impulses):
`17.76` at 1000 Hz, `32.76` at 992/1008, `4.66` at 984/1016, `36.48` at 976/1024,
`39.12` at 968/1032, `26.11` at 960/1040, `13.10` at 952/1048.
**Independent check (this session): `100·|J_n(5)|` = 17.7597, 32.7579, 4.6565, 36.4831,
39.1232, 26.1141, 13.1049 — matches the slide to all printed digits.**

### 1.15 FM bandwidth: 1% rule and Carson's rule

`[W6 p4]`: an FM signal has infinitely many sidebands, so its true BW is ∞; in practice the
significant sidebands lie in a finite BW. Two approximations: **1% rule** (uses the Bessel
table, more accurate) and **Carson's rule** (convenient, *may under-estimate*).

**1% rule** `[W6 p5]`:
```
If the single-tone FM/PM signal has n' significant sideband frequency PAIRS
with |J_{n'}(β)| ≥ 0.01 ,   then   BW_1% = 2 n' f_m        [Hz]
```
`n'` = the largest order whose Bessel magnitude still reaches 0.01.

**Carson's rule** `[W6 p5]`:
```
BW = 2(β + 1) f_m = 2(Δf + f_m)        [Hz],   with β ≜ Δf / f_m
```
Limits stated on the slide: for `β ≪ 1`, `BW ≈ 2f_m` (agrees with NBFM);
for `β ≫ 1`, `BW ≈ 2βf_m = 2Δf`.

External corroboration: Carson's rule `CBR = 2(Δf + f_m)` contains "all significant sideband
energy (98% or more)", leaving roughly 17 dB of power outside the band —
<https://en.wikipedia.org/wiki/Carson_bandwidth_rule>.

**Computed 1%-rule vs Carson comparison** (computed this session with mpmath, script in §2.4):

| β | n' (largest n with \|J_n(β)\| ≥ 0.01) | BW_1% | Carson BW | Carson under-estimates? |
|---|---|---|---|---|
| 0.2 | 1 | 2·f_m | 2.4·f_m | no |
| 1 | 3 | 6·f_m | 4·f_m | yes |
| 2 | 4 | 8·f_m | 6·f_m | yes |
| 5 | 8 | 16·f_m | 12·f_m | yes |
| 10 | 14 | 28·f_m | 22·f_m | yes |

The `n'` values for β = 5 and β = 10 are confirmed by the course's own Bessel table
`[W5 p18]`: at β = 5 the last entry ≥ 0.010 is n = 8 (0.018), n = 9 is 0.006; at β = 10 the
last is n = 14 (0.012), n = 15 is 0.004.

**Standard FM broadcast numbers** (external): monaural FM broadcast uses peak deviation
**Δf = 75 kHz** with highest audio **f_m = 15 kHz**, giving **β = 75/15 = 5** and
**Carson BW = 2(75 + 15) = 180 kHz**; the FM broadcast band 88–108 MHz is divided into 100
channels of **200 kHz** each, the extra width easing receiver selectivity —
<https://www.fmsystems-inc.com/carsons-rule-calculating-fm-modulation-bandwidth/>,
<https://www.ecfr.gov/current/title-47/chapter-I/subchapter-C/part-73/subpart-B/section-73.201>,
<https://www.allaboutcircuits.com/technical-articles/three-methods-for-estimating-the-transmission-bandwidth-of-fm-signals/>.
Applying the 1% rule to the same case gives `n' = 8` ⇒ **240 kHz**, wider than Carson's
180 kHz — the concrete illustration of "Carson may under-estimate".
For *stereo* FM the highest modulating frequency is 53 kHz (composite baseband), giving
`2(75 + 53) = 256 kHz` — <https://en.wikipedia.org/wiki/Carson_bandwidth_rule>.

### 1.16 NBFM modulator (Armstrong front end)

`[W6 p7]`, direct hardware realisation of the §1.13 expansion
`f_NBFM(t) ≈ A_c[cos ω_c t − β sin ω_m t · sin ω_c t]`:

```
m(t)=A_m cos ω_m t ──► ∫ dt ──►(×)──► (Σ, minus input) ──► f_NBFM(t)
                                ▲              ▲ (plus input)
                       A_c sin ω_c t           │
                                ▲              │
                             [90°] ◄───────────┴──── A_c cos ω_c t  (carrier oscillator)
```
The multiplier + 90°-shifted carrier alone (red box on the slide) is an **NBPM** modulator;
adding the integrator in front makes it NBFM. Same structure generates NBPM signals.

### 1.17 Frequency multiplier and mixer scaling

`[W6 p11]`. **Frequency multiplier (×n)** — a non-linear device of order n:
```
s_out(t) = k_0 + k_1 s_1(t) + … + k_n s_1^n(t)
where s_1(t) is an NBFM signal with carrier f_1 and peak deviation Δf_1
  output carrier frequencies present:  f_1, 2f_1, … n f_1
  output peak deviations present:      Δf_1, 2Δf_1, … n Δf_1
  → filter to keep only n f_1 and n Δf_1
```
**⇒ Both `f_c` and `Δf` are multiplied by n. Since `β = Δf/f_m` and `f_m` is unchanged,
`β` is also multiplied by n.**

**Frequency converter (mixer)** `[W6 p11]`:
```
output carrier freq = input carrier freq ± f_shift
no change in Δf        (⇒ no change in β)
```

This asymmetry is the whole point of the Armstrong indirect method: multipliers buy you β,
mixers reposition the carrier without touching β.

### 1.18 Armstrong indirect method — full worked chain

`[W6 p10]` block diagram: `m(t) → NBFM modulator (f_c1, Δf_1) → frequency multiplier →
mixer (with crystal oscillator f_2) → WBFM (f_c3, Δf_3)`. NBFM stage uses `β ≤ 0.2` to
minimise distortion `[W6 p10]`.

Worked example `[W6 p12–p14]`. Given `f_m = 200 Hz`, `Δf_1 = 25 Hz`, `f_c1 = 200 kHz`;
chain = NBFM mod → ×64 multiplier → mixer with 10.9 MHz crystal → ×48 multiplier → PA.

| stage | `f_c` | `Δf` | `β` |
|---|---|---|---|
| ① NBFM modulator out | 200 kHz | 25 Hz | `25/200 = 0.125` (< 0.2 ✓ NBFM) |
| ② ×64 multiplier | `200k×64 = 12.8 MHz` | `25×64 = 1.6 kHz` | 8 |
| ③ mixer −10.9 MHz | `12.8M − 10.9M = 1.9 MHz` | 1.6 kHz (unchanged) | 8 |
| ④ ×48 multiplier | `1.9M×48 = 91.2 MHz` | `1.6k×48 = 76.8 kHz` | 384 |

Total multiplication `48 × 64 = 3072`, so final `β = 0.125 × 3072 = 384`.
Signals:
```
NBFM:  f_FM(t)   = A_c cos[2π × 200×10³ t + 0.125 sin(2π × 200 t)]
WBFM:  f_WBFM(t) = A_c cos[2π × 91.2×10⁶ t + 384  sin(2π × 200 t)]
```
Design target on the question slide: `80 kHz ≥ Δf ≥ 75 kHz` and `100 MHz ≥ f_c ≥ 90 MHz`;
76.8 kHz and 91.2 MHz both satisfy it. **All four rows of arithmetic re-computed
independently this session and match the slide exactly.**

Direct method `[W6 p9]` for contrast: vary L or C of a tuned oscillator / VCO, with
`f_0 = 1/(2π√(LC))`, so that `f_i(t) = f_c + k_f m(t)` directly.

---

## 2. Bessel table `J_n(β)`, n = 0…8

### 2.1 The table (6 decimal places)

| n | β = 0.2 | β = 1 | β = 2 | β = 5 | β = 10 |
|---|---|---|---|---|---|
| 0 | +0.990025 | +0.765198 | +0.223891 | −0.177597 | −0.245936 |
| 1 | +0.099501 | +0.440051 | +0.576725 | −0.327579 | +0.043473 |
| 2 | +0.004983 | +0.114903 | +0.352834 | +0.046565 | +0.254630 |
| 3 | +0.000166 | +0.019563 | +0.128943 | +0.364831 | +0.058379 |
| 4 | +0.000004 | +0.002477 | +0.033996 | +0.391232 | −0.219603 |
| 5 | +0.000000 | +0.000250 | +0.007040 | +0.261141 | −0.234062 |
| 6 | +0.000000 | +0.000021 | +0.001202 | +0.131049 | −0.014459 |
| 7 | +0.000000 | +0.000002 | +0.000175 | +0.053376 | +0.216711 |
| 8 | +0.000000 | +0.000000 | +0.000022 | +0.018405 | +0.317854 |

Higher-precision values for the ones a build agent is most likely to unit-test:
`J_0(1) = 0.7651976866`, `J_1(1) = 0.4400505857`, `J_0(2) = 0.2238907791`,
`J_0(5) = −0.1775967713`, `J_1(5) = −0.3275791376`, `J_0(10) = −0.2459357645`,
`J_1(10) = 0.0434727462`. (mpmath, 30 dps, this session.)

### 2.2 Source and how it was validated

**Primary source:** computed this session at 30 decimal digits with
[mpmath](https://mpmath.org/doc/current/functions/bessel.html) `mp.besselj`, and cross-checked
against two *independent* implementations:

1. `scipy.special.jv` (SciPy wraps the Cephes/AMOS Fortran routines — a completely different
   algorithm from mpmath's).
2. Direct numerical quadrature of the **defining Bessel integral**
   `J_n(β) = (1/π) ∫_0^π cos(n x − β sin x) dx` via `mp.quad`.

Result: **max absolute disagreement across all 45 entries = 2.3811 × 10⁻¹⁶.**

**Independent printed cross-checks:**

- Published 4-decimal table of `J_0…J_10(β)`, β = 0…5 in steps of 0.1:
  <https://www.statisticshowto.com/wp-content/uploads/2018/09/bessel-tables.pdf>.
  Its β = 0.2 row reads `0.9900 0.0995 0.0050 0.0002 0.0000 …`; its β = 1 row
  `0.7652 0.4401 0.1149 0.0196 0.0025 0.0002 …`; its β = 2 row
  `0.2239 0.5767 0.3528 0.1289 0.0340 0.0070 0.0012 0.0002 …`; its β = 5 row
  `-0.1776 -0.3276 0.0466 0.3648 0.3912 0.2611 0.1310 0.0534 0.0184 0.0055 0.0015`.
  **Every one of these agrees with the table above when rounded to 4 dp.** (This table stops
  at β = 5, so it does not cover β = 10.)
- The course's own 3-decimal Bessel table `[W5 p18]` covers β = 0.1, 0.2, 0.5, 1, 2, 5, 8, 10.
  Its β = 10 column reads `−0.246, 0.043, 0.255, 0.058, −0.220, −0.234, −0.014, 0.217, 0.318`
  for n = 0…8 — **identical to the table above rounded to 3 dp, all nine entries.**
  Its β = 0.2, 1, 2, 5 columns likewise agree at 3 dp.
- The Week 5 WBFM spectrum slide `[W5 p20]` prints `100·|J_n(5)|` as
  17.76 / 32.76 / 4.66 / 36.48 / 39.12 / 26.11 / 13.10 — matching `100×` the β = 5 column
  above to 4 significant digits.

Reproduce (exact command run this session):
```python
import mpmath as mp; mp.mp.dps = 30
[[mp.besselj(n, b) for b in (0.2,1,2,5,10)] for n in range(9)]
```

### 2.3 Sanity properties a build agent must reproduce

- `J_n(0) = 0` for all `n ≥ 1`, `J_0(0) = 1` (the published table's β = 0 row is `1 0 0 0 …`).
- `J_{-n}(β) = (−1)^n J_n(β)` `[W5 p18]`.
- For small β, `J_n(β) ≈ (β/2)^n / n!` — visible in the β = 0.2 column collapsing to zero by n = 4.
- **Naive forward recurrence `J_{n+1} = (2n/β)J_n − J_{n−1}` is numerically unstable upward**
  for `n > β`; it will blow up in the β = 0.2 and β = 1 columns. Use a series/`Math`-library
  implementation or downward (Miller) recurrence.

### 2.4 Validation scripts written this session

`C:\Users\yongw\AppData\Local\Temp\claude\C--Users-yongw-OneDrive-Desktop-Engineering\1d24b8ef-8195-46d6-b3ac-8ba0d34092e4\scratchpad\bessel.py`
`…\bessel2.py` (three-way agreement + table emitter)
`…\checks.py` (1%-rule `n'`, Carson comparison, Armstrong arithmetic)
These are scratch files, not part of the repo; copy the logic rather than the paths.

---

## 3. The sum rule `Σ J_n²(β) = 1`, with a worked check

### 3.1 Statement

Course form `[W5 p18]`:
```
Σ_{n=-∞}^{∞} J_n²(β) = 1        for every β
```
Because `J_{-n}² = J_n²`, the one-sided form is:
```
J_0²(β) + 2 Σ_{n=1}^{∞} J_n²(β) = 1
```
This is **DLMF equation 10.23.3**, a special case of Neumann's addition theorem —
<https://dlmf.nist.gov/10.23> (quoted there as `J_0²(z) + 2 Σ_{k=1}^∞ J_k²(z) = 1`).

Physical meaning `[W5 p19–p20]`: the FM signal's total power is
`(A_c²/2) Σ_n J_n²(β) = A_c²/2`, independent of β — FM has a constant envelope, so the
modulation index only *redistributes* power across sidebands, never changes the total.

### 3.2 Worked check at β = 1 (computed this session)

| n | `J_n(1)` | `J_n²(1)` | weight (1 for n=0, 2 otherwise) | running total |
|---|---|---|---|---|
| 0 | +0.765198 | 0.58552750 | 0.58552750 | 0.58552750 |
| 1 | +0.440051 | 0.19364452 | 0.38728904 | 0.97281654 |
| 2 | +0.114903 | 0.01320281 | 0.02640562 | 0.99922216 |
| 3 | +0.019563 | 0.00038272 | 0.00076545 | 0.99998761 |
| 4 | +0.002477 | 0.00000613 | 0.00001227 | 0.99999987 |
| 5 | +0.000250 | 0.00000006 | 0.00000012 | 1.00000000 |
| 6–8 | ~0 | ~0 | ~0 | 1.00000000 |

Converged to 1.000000 by n = 5.

### 3.3 Worked check at β = 5 (computed this session)

| n | `J_n(5)` | `J_n²(5)` | weighted | running total |
|---|---|---|---|---|
| 0 | −0.177597 | 0.03154061 | 0.03154061 | 0.03154061 |
| 1 | −0.327579 | 0.10730809 | 0.21461618 | 0.24615680 |
| 2 | +0.046565 | 0.00216831 | 0.00433662 | 0.25049342 |
| 3 | +0.364831 | 0.13310183 | 0.26620365 | 0.51669707 |
| 4 | +0.391232 | 0.15306276 | 0.30612552 | 0.82282259 |
| 5 | +0.261141 | 0.06819438 | 0.13638877 | 0.95921136 |
| 6 | +0.131049 | 0.01717377 | 0.03434754 | 0.99355890 |
| 7 | +0.053376 | 0.00284904 | 0.00569808 | 0.99925698 |
| 8 | +0.018405 | 0.00033875 | 0.00067750 | 0.99993449 |

Truncating at n = 8 gives **0.99993449** — i.e. 99.993 % of the power. Full sum to n = 200
gives 1.000000000000000.

### 3.4 Truncation error a build tool must respect

Truncating the series at `|n| ≤ 8` (computed this session):

| β | `J_0² + 2Σ_{n=1}^{8} J_n²` | power missing |
|---|---|---|
| 0.2 | 1.000000000000 | ~0 |
| 1 | 1.000000000000 | ~0 |
| 2 | 0.999999999987 | 1.3e−11 |
| 5 | 0.999934485643 | 6.6e−5 |
| 10 | 0.703181785967 | **29.7 %** |

**At β = 10 you must sum to at least n ≈ 14–16, not 8.** A safe rule for a plotting tool:
sum to `n_max ≥ β + 6·β^{1/3} + 10` or simply until the running total exceeds `1 − 10⁻⁶`.

---

## 4. Noise

### 4.1 SNR — definition

Course definitions `[W7 p12]`:
```
Input SNR  (before demodulation):
  S_i/N_i = (mean power of the modulated signal) / (mean power of noise within the signal's BW)
          = (A_c²/2) / (η · B_FM)

Output SNR (after demodulation):
  S_0/N_0 = (mean power of message signal after demodulation) / (mean power of noise)
```
Both are **power ratios** (dimensionless); expressed in dB as `10·log10(S/N)`.
`η` is defined by "white noise `w(t)` with power spectral density `η/2`" `[W7 p11]`, i.e.
`η/2` is the **two-sided** PSD in W/Hz and `η` is the one-sided PSD. Note that the input-noise
power is `η·B_FM` — the two-sided density `η/2` integrated over both the positive and negative
bands of total width `2B_FM`.

Key structural point for a teaching tool: **SNR is bandwidth-dependent.** Widening the receiver
BW admits proportionally more noise power without admitting more signal power, so `S_i/N_i`
falls as `1/B`.

Worked FM result `[W7 p12, p15, p16]`:
```
S_0 = mean{(2πk_f m(t))²} = 4π²k_f² · mean{m²(t)}
N_0 = 8π²η f_m³ / (3A_c²)
S_0/N_0 = 3A_c²k_f² mean{m²(t)} / (2η f_m³)

single tone, m(t)=A_m cos ω_m t, Δf = A_m k_f, mean{m²} = A_m²/2, β = Δf/f_m :
        S_0/N_0 = 3 A_c² β² / (4 η f_m)
```
Since `BW = 2(β+1)f_m`, output SNR grows as **BW²** — the quantitative statement of "FM trades
bandwidth for noise performance" `[W7 p16]`. FM's threshold: below about **10 dB input SNR**
the capture effect occurs and the demodulator fails `[W7 p21 area, text dump line 371]`.

### 4.2 PSD — what it is

`[W1 p19]`: `S_v(f)` is the **power spectral density** of `v(t)`, defined by
```
mean{v²(t)} = ∫_{-∞}^{∞} S_v(f) df
```
Units: W/Hz. It is the distribution of average power over frequency; the area under it is the
total average power. It carries **no phase information**, so it does not determine `v(t)`.

White noise: `S_w(f) = η/2` for all `f` (flat, two-sided) `[W7 p11]`. After an ideal bandpass
filter of width `B_FM` centred at `f_c`, the noise PSD is `η` over `|f| ≤ B_FM/2` in the
equivalent-baseband description `[W7 p14]`.

Filtering transforms PSD as `S_out(f) = |H(f)|² S_in(f)` — used explicitly at `[W7 p14]`:
```
S_{n_0}(ω) = (1/A_c²) S_{n_s}(ω) |H(ω)|²   with H(ω)=jω (the discriminator differentiates)
           = (1/A_c²) ω² S_{n_s}(ω) = (1/A_c²) ω² η       for |f| ≤ B_FM/2
```
⇒ **parabolic** output-noise PSD `[W7 p15]`: differentiation in the FM discriminator emphasises
high-frequency noise, which is why FM receivers use de-emphasis. Integrating the parabola over
the post-detection LPF of width `f_m`:
```
N_0 = 2∫_0^{f_m} S_{n_0}(f) df = 8π²η f_m³ / (3A_c²)
```
— the `f_m³` is the signature of a parabolic noise PSD.

### 4.3 Why bandpass noise splits into I and Q components of equal power

Course statement `[W7 p13]`:
```
n(t) = n_c(t) cos ω_c t − n_s(t) sin ω_c t          (in-phase / quadrature form)
     = r(t) cos[ω_c t + v(t)]                        (envelope / phase form)
```
with the phasor diagram on that slide showing `r(t)` as the resultant of `n_c(t)` along the
carrier axis and `n_s(t)` at 90°.

**Why the split exists.** After the receiver's bandpass filter the noise occupies only
`f_c ± B/2`. Any such bandpass process can be written exactly as two *lowpass* processes
(bandwidth `B/2`) riding on quadrature carriers — this is the same I/Q decomposition as QAM
(§1.10), applied to noise instead of data.

**Why the two components carry equal power.** For white noise the PSD is *symmetric about
`f_c`* after an ideal symmetric bandpass filter. Under that symmetry the two quadratures are
statistically indistinguishable — there is no preferred phase reference in the noise — so:

- `E[n_c(t)] = E[n_s(t)] = E[n(t)] = 0`
- `E[n_c²] = E[n_s²] = E[n²]` — **each component has the same total power as the bandpass
  noise itself** (not half of it; the factor is recovered by the `cos`/`sin` averaging of ½
  when they are re-modulated back up to `f_c`).
- `E[n_c(t)·n_s(t)] = 0` — uncorrelated; if `n(t)` is Gaussian they are independent Gaussians.
- `S_{n_c}(f) = S_{n_s}(f) = S_n(f − f_c) + S_n(f + f_c)` over `|f| ≤ B/2`, zero elsewhere.
- Consequently the envelope `r(t) = √(n_c² + n_s²)` is **Rayleigh** distributed and the phase
  `v(t)` is uniform on `[0, 2π)`.

External corroboration of the property list (equal means and variances, uncorrelatedness,
Gaussian preservation, and the PSD relation `G_x(f) = G_y(f) = G_n(f−f_c) + G_n(f+f_c)` for
`f_c − B/2 < |f| < f_c + B/2`): <https://www.brainkart.com/article/Narrow-Band-Noise_13140/>.
The course uses exactly this in `S_{n_s}(ω) = η for |f| ≤ B_FM/2` `[W7 p14]`.

Small-noise FM result that follows `[W7 p13]`: for `A_c ≫ r(t)`, the demodulated phase is
`ρ(t) ≈ φ(t) + (r(t)/A_c) sin[v(t) − φ(t)]`; with no message, `ρ(t) ≈ n_s(t)/A_c`, so the
discriminator output noise is `n_0(t) = dρ/dt = (1/A_c)·d n_s(t)/dt`. **Only the quadrature
component `n_s` reaches the output of an FM detector** — the in-phase component perturbs
amplitude, which the limiter removes. That is the mechanism behind FM's noise advantage.

### 4.4 Matched filter (external research)

For a known pulse `s(t)` of duration `T` in additive white Gaussian noise of two-sided PSD
`N_0/2`, the filter that maximises the SNR at the sampling instant `t = T` is the **matched
filter**, the time-reversed (and conjugated) copy of the pulse:
```
h(t) = s(T − t)          (up to an arbitrary gain constant)
```
and the resulting peak SNR is
```
SNR_max = 2E / N_0 ,     E = ∫_0^T s²(t) dt   (pulse energy, J)
```
It depends **only on the pulse energy, not on the pulse shape**.
Sources: <https://courses.grainger.illinois.edu/ece361/sp2011/Newlectures/Lecture04.pdf>,
<http://web.mit.edu/16.36/2006directory/lectures/Lectures89.pdf>,
<https://www.sciencedirect.com/topics/mathematics/matched-filter>.
Equivalent implementation: correlate the received waveform with `s(t)` over `[0,T]` and sample
at `T` — a correlator and a matched filter give identical outputs at the sampling instant.

### 4.5 Raised-cosine pulse shaping and ISI (external research)

Nyquist's zero-ISI criterion: the *end-to-end* response (transmit filter × channel × receive
filter) must be zero at every symbol instant other than its own. The raised-cosine response is
the standard family that satisfies it.
Source: <https://en.wikipedia.org/wiki/Raised-cosine_filter>, <https://en.wikipedia.org/wiki/Root-raised-cosine_filter>.

Frequency response (`β` = roll-off, `0 ≤ β ≤ 1`; `T` = symbol period, s):
```
H(f) = 1                                                      |f| ≤ (1−β)/(2T)
H(f) = ½[ 1 + cos( (πT/β)( |f| − (1−β)/(2T) ) ) ]    (1−β)/(2T) < |f| ≤ (1+β)/(2T)
H(f) = 0                                                      otherwise
```

Impulse response:
```
h(t) = (1/T) sinc(t/T) · cos(πβt/T) / [ 1 − (2βt/T)² ]        general
h(t) = (π/4T) sinc(1/(2β))                                     at t = ±T/(2β)   (removable singularity)
```

Bandwidth:
```
baseband BW = (R_s/2)(1 + β)        RF/passband BW = R_s(1 + β)      R_s = 1/T  (symbol rate, baud)
excess bandwidth fraction = β
```
`β = 0` → ideal brick wall, `h(t) = (1/T) sinc(t/T)`: minimum bandwidth `R_s/2` but the tails
decay only as `1/t`, so timing error causes severe ISI.
`β = 1` → "pure raised cosine", `H(f) = ½[1 + cos(πfT)]` for `|f| ≤ 1/T`: double the minimum
bandwidth, fastest-decaying tails, most tolerant of timing error.

**Split filtering.** To get the matched-filter SNR benefit *and* zero ISI, put a root-raised-
cosine (RRC) filter at both the transmitter and the receiver; their cascade is the raised
cosine. An RRC alone is **not** ISI-free — the standard student trap.

### 4.6 Eye diagram (external research)

Source: <https://en.wikipedia.org/wiki/Eye_pattern>.
Construction: slice the received waveform into symbol periods (unit intervals) using the
recovered clock and overlay them on one time axis, accumulating into a 2-D histogram.

| Feature | What it measures |
|---|---|
| Eye **height** (vertical opening at the sampling instant) | noise margin — how much noise voltage can be added before a decision error |
| Eye **width** (horizontal opening) | timing-jitter margin |
| Widest point of the eye | the **optimum sampling instant** |
| Slope of the transitions at the crossings | sensitivity to timing error (steeper = more tolerant) |
| Eye **closure** | intersymbol interference and/or noise |

ISI closes the eye vertically and smears the crossings horizontally. An open eye = minimal
distortion. Interactive tools should let the user vary roll-off `β`, timing offset and SNR and
show the eye responding to each.

---

## 5. DO NOT FAKE — checklist for the build agent

1. **Do not hard-code Bessel values you did not verify.** Use the §2.1 table as ground truth,
   and unit-test your implementation against **all 45 entries** to 6 dp before shipping a
   spectrum plot. If your `J_n` is wrong, every FM spectrum, every 1%-rule bandwidth and
   every power sum silently becomes wrong-but-plausible.
2. **Do not use upward recurrence for `J_n`.** `J_{n+1} = (2n/β)J_n − J_{n−1}` is unstable for
   `n > β` and will produce garbage in the β = 0.2 and β = 1 columns. Test the β = 0.2 column
   explicitly: `J_4(0.2)` must be `+0.000004`, not `1e+12`.
3. **Do not truncate the Bessel sum at a fixed small n.** At β = 10, `|n| ≤ 8` captures only
   **70.3 %** of the power (§3.4). Sum until the running total exceeds `1 − 10⁻⁶`, or to
   `n_max ≥ β + 6β^{1/3} + 10`.
4. **Do not claim `Σ J_n² = 1` in a UI without computing it.** Show the running total; it is
   the single best self-check that the Bessel implementation and the spectrum plot agree.
5. **Do not let FM total power change with β.** If your animated spectrum's total power moves
   when the user drags β, the implementation is wrong — FM is constant-envelope
   (`Power = A_c²/2` always, `[W5 p20]`).
6. **Do not confuse the two bandwidth rules.** Carson = `2(β+1)f_m`, 1% rule = `2n'f_m` with
   `|J_{n'}(β)| ≥ 0.01`. They differ (§1.15 table): at β = 5 they are `12f_m` vs `16f_m`.
   Label whichever you draw. Never present Carson as exact.
7. **Do not swap sin and cos in the single-tone phase term.** FM is
   `cos[ω_c t + β sin ω_m t]`, PM is `cos[ω_c t + β_p cos ω_m t]` `[W5 p11, p12]`.
   Getting this backwards makes PM and FM look identical.
8. **Do not model the coherent-demodulator phase error as a rotation.** For DSBSC the effect
   is an amplitude scale `cos φ`, going to **zero** at `φ = ±90°` `[W2 p13]`. For QAM the
   phase error additionally couples I into Q; do not show QAM crosstalk in the DSBSC demo or
   vice versa.
9. **Do not draw the NBFM lower sideband with a plus sign.** The expansion is
   `+ (βA_c/2)cos(ω_c+ω_m)t − (βA_c/2)cos(ω_c−ω_m)t` `[W5 p15]` — the minus is what
   distinguishes NBFM from AM, which otherwise has the same spectrum.
10. **Do not let a multiplier change `f_m`, and do not let a mixer change `Δf`.** Multiplier:
    `f_c` and `Δf` (hence `β`) both ×n. Mixer: `f_c` shifts by ±`f_shift`, `Δf` and `β`
    unchanged `[W6 p11]`. Every Armstrong-chain simulator gets this wrong at least once.
11. **Do not treat the FM instantaneous phase as returning to zero.** `Δφ(t)` is the *integral*
    of the message; after a finite pulse the phase holds at a constant offset `[W5 p9]`.
12. **Do not claim the plotted "instantaneous frequency" of an FM waveform is measurable by
    counting zero crossings** for large β — it is a model quantity, valid when `f_m ≪ f_c`.
13. **Do not use `sinc(x) = sin(x)/x`.** This course defines `sinc(x) = sin(πx)/(πx)`
    `[W1 p13]`. Mixing the two conventions shifts every null in every spectrum plot by π.
14. **Do not violate the FDM non-overlap criterion silently.** If the user picks carriers with
    `f_{i+1} − f_i ≤ W_i + W_{i+1}`, show the overlap and say demultiplexing will fail
    `[W3 p7]` — do not just draw pretty non-overlapping boxes regardless of the inputs.
15. **Do not claim a root-raised-cosine filter alone is ISI-free.** Only the *cascade* of TX
    and RX RRC (= raised cosine) satisfies the Nyquist criterion (§4.5).
16. **Do not report SNR without stating the bandwidth it is measured in.** `S_i/N_i` depends on
    `B` `[W7 p12]`; an SNR number with no reference bandwidth is meaningless.
17. **Do not assert that bandpass noise splits into I and Q of *half* the power each.** Each
    quadrature component has the **same** variance as the bandpass noise (§4.3).
18. **Do not extract text from these PDFs with `pdftotext` and trust it.** The math glyphs have
    no Unicode mapping and vanish silently; render the pages instead (§0).
19. **Do not invent Bessel values for β not in the §2.1 table.** Compute them; if the tool
    can't, restrict the slider to the validated β values and say so.
20. **Do not present the FM broadcast numbers loosely.** Mono: `Δf = 75 kHz`, `f_m = 15 kHz`,
    `β = 5`, Carson `= 180 kHz`, channel allocation `= 200 kHz` (88–108 MHz, 100 channels).
    Stereo composite baseband goes to 53 kHz, giving Carson `= 256 kHz`. These are different
    numbers for different cases — do not blend them.

---

## 6. Numbers verified in this session (for regression tests)

| Claim | Value | How verified |
|---|---|---|
| max disagreement mpmath vs scipy vs Bessel integral, 45 entries | 2.3811e−16 | computed |
| `Σ_{|n|≤8} J_n²(5)` | 0.99993449 | computed |
| `Σ_{|n|≤8} J_n²(10)` | 0.703181785967 | computed |
| `Σ_{|n|≤200} J_n²(β)`, all five β | 1.000000000000000 | computed |
| 1%-rule `n'` at β = 0.2, 1, 2, 5, 10 | 1, 3, 4, 8, 14 | computed; n'(5)=8 and n'(10)=14 confirmed against `[W5 p18]` |
| `100·J_n(5)` for n = 0…6 | −17.7597, −32.7579, +4.6565, +36.4831, +39.1232, +26.1141, +13.1049 | computed; matches `[W5 p20]` |
| Armstrong chain: β₁, f_c2, Δf₂, f_c3, Δf₃, f_c4, Δf₄, β₄ | 0.125, 12.8 MHz, 1.6 kHz, 1.9 MHz, 1.6 kHz, 91.2 MHz, 76.8 kHz, 384 | computed; matches `[W6 p13, p14]` |
| FM broadcast mono β and Carson BW | 5, 180 kHz | computed from Δf=75k, f_m=15k; corroborated externally |
| FM broadcast mono 1%-rule BW | 240 kHz | computed (n'=8 × 2 × 15 kHz) |

**Not verified in this session** (recorded as external claims, not observations):
the "98 % of sideband energy / ~17 dB outside the band" figure for Carson's rule; the FCC
200 kHz channel-allocation figure; the matched-filter `2E/N₀` result; the raised-cosine and
eye-diagram statements in §4.5–4.6. Each is cited to its URL above and was not independently
derived or numerically checked here.
