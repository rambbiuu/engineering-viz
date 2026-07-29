# Link budgets, receiver noise, and RF front-end impairments

Research note for building interactive teaching tools. Every number below is either quoted
from a source (cited inline) or computed in this session (marked `[computed]` with the exact
inputs shown, so it can be re-derived).

Source shorthand:

- **[6A p.N]** = `C:\Users\yongw\Downloads\IE4155 Part 6A.pdf`, PDF page N (28 pages).
- **[P5 p.N]** = `C:\Users\yongw\Downloads\IE4155 Part 5 AY24-25 (1).pdf`, PDF page N (76 pages).
- **[W4 p.N]** = `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week4.pdf`, PDF page N (17 pages).

Extraction caveat: [6A p.20] (the worked "Link Budget Table (Example)") and [6A p.23] are
bitmap slides — `pdftotext` returns only the title and slide number, no cell values. The
worked example in §2 below is therefore computed from the problem statement on [6A p.19],
not copied from the answer table. Maths glyphs (subscripts, Greek, division bars) are lost
in text extraction throughout; every reconstructed formula below is cross-checked against a
numeric example that the slides do state.

---

## 1. Formulas, with units

### 1.1 dB conventions

| Quantity | Definition | Unit |
|---|---|---|
| `P(dBW) = 10·log10( P / 1 W )` | power referred to 1 watt | dBW |
| `P(dBm) = 10·log10( P / 1 mW )` | power referred to 1 milliwatt | dBm |
| `P(dBm) = P(dBW) + 30` | conversion | — |

Worked identity from the notes: 10 W = 10 dBW = 40 dBm [6A p.4].

Gains/losses are pure ratios, so they are plain **dB**. Antenna gain referred to an isotropic
radiator is **dBi**; isotropic gain = 1 = 0 dBi [P5 p.45].

### 1.2 EIRP — effective isotropic radiated power

```
EIRP = P_T · G_T / L_T                    (linear, watts)
EIRP(dBm) = P_T(dBm) + G_T(dBi) − L_T(dB) (dB form)
```

`L_T` is the total transmit-side loss between the PA output and the antenna port: feeder /
coax / waveguide, filter insertion loss, combiner or duplexer, radome [6A p.5, p.6, p.12].

### 1.3 Friis transmission equation (received power)

```
        P_T · G_T · G_R          P_T · G_T · G_R      ( λ  )^2
P_R = ───────────────────── = ───────────────────  · (─────)
       L_T · L_FSL · L_R           L_T · L_R          (4πd)
```

[6A p.7, eqn (1)]. `P_R` in watts; `λ` and `d` in the same length unit; `G` dimensionless;
`L_T`, `L_R`, `L_FSL` dimensionless loss factors ≥ 1.

dB form, which is what a tool should actually compute:

```
C(dBm) = P_T(dBm) + G_T(dBi) − L_T(dB) − L_FSL(dB) + G_R(dBi) − L_R(dB) − L_impl(dB)
       = EIRP(dBm) − L_FSL(dB) + G_R(dBi) − L_R(dB) − L_impl(dB)
```

`C` is the **unfaded** received carrier level, also written `P_R` [6A p.8]. `L_impl` is
receiver implementation loss — the notes' example carries one ([6A p.19], 2 dB) even though
the block diagram does not name it.

### 1.4 Free space loss (FSL) — both forms

**Physical form** (from the `(λ/4πd)²` term in eqn (1), [6A p.7]):

```
L_FSL = ( 4πd / λ )^2        (dimensionless)
L_FSL(dB) = 20·log10( 4πd / λ ) = 20·log10( 4πdf / c )
```

**Engineering form** [6A p.12]:

```
L_FSL(dB) = 92.4 + 20·log10( f_GHz · d_km )
```

The exact constant is **92.4478** for (GHz, km) and **32.4478** for (MHz, km)
`[computed: 20·log10(4π·10^9·10^3 / 2.99792458e8) = 92.4478]`. The slide rounds to 92.4
[6A p.12]; the (MHz, km) variant `32.44 + 20·log10(f_MHz · d_km)` is the same equation.
Pick one constant, state it in the tool, and stay with it — 92.4 vs 92.45 shifts the answer
by 0.05 dB.

Two other useful identities, both direct consequences: **FSL rises 6.02 dB per doubling of
distance and 6.02 dB per doubling of frequency** (the `20·log10` on each).

### 1.5 Fade margin

```
FM(dB) = C(dBm) − R_T(dBm)
```

where `R_T` is the specified receiver threshold level for a stated performance target — FM
threshold, a minimum S/N, or a BER such as 1×10⁻⁶ [6A p.9, p.10]. When the target is given
as a minimum carrier-to-noise ratio instead, the equivalent statements are:

```
R_T(dBm) = N(dBm) + (C/N)_min(dB)
FM(dB)   = (C/N)_unfaded(dB) − (C/N)_min(dB)
```

**Propagation reliability / availability** is the fraction of time the link stays above
`R_T`; the complementary `P%` (time spent below threshold) is the unavailability
[6A p.15]. Design targets quoted in the notes run 99 % to 99.999 % [6A p.2]. The mapping
from FM to P% needs a fading distribution — the notes use Bullington's worst-month curves
for 30–40 mile LOS paths at 30 MHz / 100 MHz / 300 MHz / 1 GHz / 4 GHz, plus the Rayleigh
reference curve [6A p.15, p.17]. Fading worsens with increasing frequency and increasing
path length [6A p.17]. Do not invent a closed form for these curves; either plot the Rayleigh
case, for which `P(fade > FM) = 10^(−FM/10)` is exact for deep fades, or label the axis
qualitatively.

### 1.6 Carrier-to-noise ratio

```
C/N (dB) = C(dBm) − N(dBm)
```

`C` unfaded received carrier, `N` total receiver noise power in the IF bandwidth [6A p.9].

### 1.7 Eb/No

```
E_b = C · T = C / R           (joules; C in watts, T in s/symbol, R in symbols/s)   [6A p.21]
N_0 = N / B                   (W/Hz; N in watts, B in Hz)                           [6A p.22]

E_b / N_0 = (C/N) · (B/R)                                                           [6A p.22]

E_b/N_0 (dB) = C/N (dB) + 10·log10( B / R )
```

`B` = IF bandwidth at the demodulator input (Hz), `R` = symbol (or bit) rate (symbols/s or
bit/s). The notes call `E_b` "energy per symbol" and `R` "symbol rate" [6A p.21]; the same
algebra holds bit-wise if `R` is the bit rate. `B/R` is dimensionless, so `E_b/N_0` is
dimensionless. Units check: `(J/symbol) / (W/Hz)` = `(W·s) / (W·s)` = 1. ✓

### 1.8 Thermal noise and noise figure

```
N_perfect = k · T_0 · B                   watts   (ideal/noiseless receiver)
N         = k · T_0 · B · F               watts   [6A p.24, eqn (3)]
N(dBW)    = 10·log10(k·T_0·B) + 10·log10(F)       [6A p.24, eqn (4)]
```

- `k` = 1.38×10⁻²³ J/K (Boltzmann) [6A p.24]. CODATA exact value 1.380649×10⁻²³ J/K.
- `T_0` = 290 K, the reference "room temperature" [6A p.24].
- `B` = IF (noise) bandwidth in Hz.
- `F` = noise **factor**, a linear ratio ≥ 1. `NF = 10·log10(F)` in dB. The notes use `F`
  for both and warn explicitly: *"When using the formula - use absolute value before
  converting your result to dB"* [6A p.27].

**Noise temperature form:**

```
F = 1 + T_e / T_0          ⟺        T_e = ( F − 1 ) · T_0        kelvin
```

[6A p.24]. `T_e` is the equivalent input noise temperature.

**Practical dBm form** — this is the one a tool should implement:

```
N(dBm) = −174 + 10·log10( B / 1 Hz ) + NF(dB)
```

Justification of −174 in §5.1.

### 1.9 Friis cascade formula

```
              F_2 − 1     F_3 − 1        F_4 − 1
F_total = F_1 + ─────── + ─────────── + ─────────────── + …
                  G_1       G_1·G_2       G_1·G_2·G_3
```

[6A p.25, eqn (5)]. **All terms linear** — factors and gains, not dB. Convert only at the
end. Equivalent temperature form:

```
T_e,total = T_e1 + T_e2/G_1 + T_e3/(G_1·G_2) + …
```

### 1.10 Passive device rule: F = L

*"for passive devices, e.g. transmission lines, device loss in L is equal to the noise
figure of the device i.e. F = L"* [6A p.26]. In dB: **NF(dB) = insertion loss (dB)**, and the
stage gain is `G(dB) = −L(dB)`.

Two consequences worth building into a tool:

- A chain of passive stages followed by an amplifier collapses exactly:
  `F_total = L_1 · L_2 · F_amp`, i.e. in dB the losses simply add to the amplifier's NF
  `[computed: substitute F_i = L_i, G_i = 1/L_i into §1.9 — the intermediate terms telescope]`.
- A passive **mixer**'s noise figure equals its conversion loss for the same reason: "The
  noise figure of a passive diode mixer equals its conversion loss… A passive mixer with 6 dB
  conversion loss has a 6 dB noise figure (SSB)"
  (<https://rfessentials.com/rf-knowledge-base/what-is-the-noise-figure-of-a-passive-mixer-and-how-does-conversion-loss-factor-/>).

Course-note check on §1.9 + §1.10 [6A p.26–27]: 3 dB cable (L = 2) ahead of an AMPS phone
with F = 4 (6 dB), B = 30 kHz. `F = 2 + (4−1)/(1/2) = 2 + 6 = 8 = 9 dB`. The slide states
exactly this. A tool implementing §1.9 must reproduce `8 → 9.03 dB`.

### 1.11 Receiver sensitivity (the same equation rearranged)

```
P_min(dBm) = −174 + 10·log10(B) + NF(dB) + (C/N)_min or (S/N)_min (dB)
```

"RS = Nfloor + SNRreq (dBm)", with "Nfloor = −174 + 10·log10(BW) + NF + 10·log10(T/290)"
(<https://www.mathworks.com/help/simrf/ug/determine-rf-receiver-specification.html>, via
search result summary). The `10·log10(T/290)` term is zero at the 290 K reference.

### 1.12 Noise in analogue AM (EE3012 track)

White noise has flat two-sided PSD `S_n(f) = η/2` W/Hz and therefore infinite total power
[W4 p.6]. After an ideal BPF of bandwidth `B` centred on `f_0`:

```
σ²_n = 2 · (η/2) · B = η·B        watts        [W4 p.7]
```

Bandpass noise decomposes as `n(t) = n_c(t)·cos(2πf_0 t) − n_s(t)·sin(2πf_0 t)` [W4 p.8],
with `σ²(n_c) = σ²(n_s) = σ²(n) = ηB`; the PSD of `n_c` and `n_s` is `η` over `|f| ≤ B/2`
[W4 p.8, p.15].

Coherent (synchronous) DSB-SC demodulation of `A_c·s(t)·cos(2πf_c t) + n(t)`, LPF to the
message bandwidth [W4 p.10, p.11]:

```
demodulated signal        = A_c·s(t)/2
demodulated signal power  = A_c²·σ²(s) / 4
output noise              = n_c(t)/2
output noise power        = σ²(n_c)/4 = ηB/4

SNR_out = A_c² · σ²(s) / ( η · B )
```

Course-note check [W4 p.12, p.13]: `s(t) = sin(10πt) + sin(20πt)`, carrier `cos(100πt)`
(A_c = 1, f_c = 50 Hz), `η/2 = 10⁻³` W/Hz. Message components at 5 Hz and 10 Hz → DSB
bandwidth `B = 2 × 10 = 20 Hz`. `σ²(s) = ½ + ½ = 1`. Noise power `= 2 × 10⁻³ × 20 = 0.04` W.
`SNR = 1/0.04 = 25 = 13.98 dB`. The slide states 0.04, 25 and 13.98 dB. ✓
`[computed check: 10·log10(25) = 13.979]`

Also from [W4 p.4]: PSD of filtered noise `S_y(f) = |H(f)|²·S_x(f)`; power `= ∫ S(f) df`.

---

## 2. Worked numeric example — end-to-end regression check

Source problem: [6A p.19] ("Q1", NTU campus link). The slide poses the question and leaves
the arithmetic to the student; **all values below are `[computed]` in this session** from the
stated inputs. The answer slide [6A p.20] is a bitmap and could not be read, so treat these
as *my* arithmetic on *the notes'* problem, not as the lecturer's published answer.

### Inputs (verbatim from [6A p.19])

| Symbol | Value | Note |
|---|---|---|
| `f` | 2.45 GHz | |
| `d` | 800 m = 0.8 km | |
| `P_T` | 100 mW | |
| `G_T` | 3 dBi | |
| `G_R` | 0.5 dBi | |
| cable loss, Tx | 2 dB | "2 dB each, at the Rx and Tx" |
| cable loss, Rx | 2 dB | |
| insertion loss, Tx | 1.5 dB | "1.5 dB each at Tx and Rx" |
| insertion loss, Rx | 1.5 dB | |
| `L_impl` | 2 dB | receiver implementation loss |
| `B` | 1.6 MHz | IF bandwidth |
| `NF` | 5 dB | |
| `(C/N)_min` | 9 dB | |

### Constant set used (state this in any tool that reproduces the numbers)

`k·T_0` reference `N_0 = −174.0 dBm/Hz`; FSL constant `92.45` for (GHz, km).

### Every intermediate value

| Step | Expression | Value |
|---|---|---|
| 1 | `P_T(dBm) = 10·log10(100 mW / 1 mW)` | **+20.000 dBm** |
| 2 | `L_T = 2 + 1.5` | **3.500 dB** |
| 3 | `EIRP = 20 + 3 − 3.5` | **+19.500 dBm** (= −10.500 dBW) |
| 4 | `f_GHz · d_km = 2.45 × 0.8` | **1.960** |
| 5 | `20·log10(1.96)` | **5.845 dB** |
| 6 | `L_FSL = 92.45 + 5.845` | **98.295 dB** |
| 7 | `P at Rx antenna port = 19.500 − 98.295 + 0.5` | **−78.295 dBm** |
| 8 | `L_R = 2 + 1.5 + 2 (impl)` | **5.500 dB** |
| 9 | `C = −78.295 − 5.500` | **−83.795 dBm** (= −113.795 dBW) |
| 10 | `10·log10(1.6×10⁶)` | **62.041 dB** |
| 11 | `N = −174 + 62.041 + 5` | **−106.959 dBm** (= −136.959 dBW) |
| 12 | `N_0 = N − 10·log10(B) = −106.959 − 62.041` | **−169.000 dBm/Hz** |
| 13 | `C/N = −83.795 − (−106.959)` | **+23.164 dB** |
| 14 | `R_T = N + (C/N)_min = −106.959 + 9` | **−97.959 dBm** |
| 15 | `FM = C − R_T = −83.795 + 97.959` | **+14.164 dB** |
| 15′ | cross-check `FM = C/N − (C/N)_min = 23.164 − 9` | **+14.164 dB** ✓ |

### Extension: Eb/No at 1.0 Mbit/s on the same link

| Step | Expression | Value |
|---|---|---|
| 16 | `10·log10(B/R) = 10·log10(1.6e6 / 1.0e6)` | **+2.041 dB** |
| 17 | `E_b/N_0 = 23.164 + 2.041` | **+25.205 dB** |
| 17′ | cross-check `E_b = C − 10·log10(R) = −83.795 − 60` | **−143.795 dBm·s**; `E_b/N_0 = −143.795 − (−169.000) = 25.205 dB` ✓ |

### Tolerance and known sensitivity of this example

| If you instead use | C/N becomes | Δ |
|---|---|---|
| FSL const 92.45, `N_0` = −174.0 (**canonical above**) | 23.164 dB | — |
| FSL const 92.4 (slide value), `N_0` = −174.0 | 23.214 dB | +0.05 |
| FSL const 92.4478, `N_0` = −173.975 (k = 1.380649e-23) | 23.141 dB | −0.02 |

`[all computed]`. **Accept any implementation within ±0.1 dB, but the tool must state which
constants it used.** A regression test should assert `abs(C/N − 23.164) < 0.1` and
`abs(FM − 14.164) < 0.1`.

---

## 3. Intermodulation products

### 3.1 Origin

A linear device produces only the input frequencies at its output — no harmonics, no IM
products [P5 p.20]. A weakly non-linear device is modelled as a power series [P5 p.21]:

```
e_out = k1·e_in + k2·e_in² + k3·e_in³ + …
```

With a two-tone input `e_in = e1·sin(2πf1·t) + e2·sin(2πf2·t)` the output contains
[P5 p.22]:

- fundamentals `f1, f2`
- harmonics `n·f1`, `n·f2`
- **intermodulation products `n·f1 ± m·f2`**

**Order = n + m** — "the order of the IP is the number of times each frequency occurs"
[P5 p.22]. Example given: `3f2 − 2f1` is 5th order because f2 occurs 3× and f1 occurs 2×
[P5 p.23].

### 3.2 Product table, orders 2–5

Two-tone case. Numeric column uses **f1 = 900 MHz, f2 = 901 MHz, Δ = f2 − f1 = 1 MHz**
`[all frequencies computed]`. "In band" means the product lands inside a receiver channel
sitting on or next to f1/f2 — the practical test.

| Order | Product (n,m) | Expression | Value (MHz) | Offset from f1 | In band? |
|---|---|---|---|---|---|
| 2 | (1,1) | `f2 − f1` | 1.0 | −899 | no — near DC, `= Δ` |
| 2 | (1,1) | `f1 + f2` | 1801.0 | +901 | no — near 2×f |
| 2 | (2,0) | `2f1` | 1800.0 | +900 | no — 2nd harmonic |
| 2 | (0,2) | `2f2` | 1802.0 | +902 | no |
| **3** | **(2,1)** | **`2f1 − f2`** | **899.0** | **−1 (= −Δ)** | **YES** |
| **3** | **(1,2)** | **`2f2 − f1`** | **902.0** | **+2 (= f2+Δ)** | **YES** |
| 3 | (2,1) | `2f1 + f2` | 2701.0 | +1801 | no |
| 3 | (1,2) | `2f2 + f1` | 2702.0 | +1802 | no |
| 3 | (3,0) | `3f1` | 2700.0 | +1800 | no |
| 3 | (0,3) | `3f2` | 2703.0 | +1803 | no |
| 4 | (2,2) | `2f2 − 2f1` | 2.0 | −898 | no — near DC, `= 2Δ` |
| 4 | (3,1) | `3f1 − f2` | 1799.0 | +899 | no — near 2×f |
| 4 | (1,3) | `3f2 − f1` | 1803.0 | +903 | no |
| 4 | (2,2) | `2f1 + 2f2` | 3602.0 | +2702 | no |
| 4 | (4,0) | `4f1` | 3600.0 | +2700 | no |
| **5** | **(3,2)** | **`3f1 − 2f2`** | **898.0** | **−2 (= −2Δ)** | **YES** |
| **5** | **(2,3)** | **`3f2 − 2f1`** | **903.0** | **+3 (= f2+2Δ)** | **YES** |
| 5 | (4,1) | `4f1 − f2` | 2699.0 | +1799 | no |
| 5 | (1,4) | `4f2 − f1` | 2704.0 | +1804 | no |
| 5 | (3,2) | `3f1 + 2f2` | 4502.0 | +3602 | no |
| 5 | (5,0) | `5f1` | 4500.0 | +3600 | no |

The notes' own listings match this generation rule: 2nd order `f1+f2, f1−f2, f2−f1`;
3rd order `2f1+f2, 2f1−f2, 2f2−f1, f1+2f2`; 4th order `3f2−f1, 3f1−f2` [P5 p.22].

### 3.3 Why odd orders matter and even orders do not

The general result, visible in the table: for closely spaced tones, a product `n·f1 ± m·f2`
sits near `(n ± m)·f`. **Even-order products have `n ± m` even** — they fall near DC or near
2f, 4f, … , far outside the receiver passband, where the RF filter kills them.
**Odd-order products have `n ± m` = ±1** — they fall right back on top of the wanted band and
**no filter can remove them, because they are inside the channel**. The 3rd-order pair sits
one channel spacing outside the two tones; the 5th-order pair sits two spacings out.

Course statement: *"In general, even order IP's may be ignored since they generally fall
outside the frequencies of interest. The amplitude of the IP's decreases as the order
increases, hence 3rd order products have high amplitudes than 5th order products."*
[P5 p.25].

Three-tone case [P5 p.23, p.24] adds the nastiest family of all: `a + b − c`, `a + c − b`,
`c + b − a` — 3rd order, and with unevenly spaced carriers these land essentially anywhere.
4th order: `2a + b − c`, `2b + c − a`, …; 5th order: `2a + b − 2c`, `2a + 2b − c`, ….
"As the number of frequencies is increased, very large numbers of IP's are present; it
increases exponentially with the numbers of input frequencies" [P5 p.24].

### 3.4 Where IM is generated in a real system

Three named mechanisms [P5 p.29, p.30, p.32, p.34]:

1. **Transmitter output stage / antenna.** Tx2's signal is picked up by Tx1's antenna and
   mixes in Tx1's non-linear PA; the products `n·f1 ± m·f2` are re-radiated. If a nearby
   receiver on `f3` has one inside its bandwidth, it is jammed [P5 p.30, Fig 5.6].
2. **Receiver front-end overload.** A high-power transmitter nearby drives the receiver
   input stage non-linear; two external signals `fa`, `fb` then generate `n·fa ± m·fb`
   *inside the receiver* [P5 p.32, Fig 5.7]. This is what IIP3 quantifies.
3. **"Rusty bolt" effect.** Corroded metal on a tower or fence acts as a diode. `f1` and `f2`
   mix in it and the fence radiates the products; interference occurs if
   `f3 = n·f1 ± m·f2` [P5 p.34, Fig 5.8].

### 3.5 Third-order intercept point and the 3:1 slope rule

The defining behaviour: *"A third-order nonlinear product will increase by 3 dB in power when
the input power is raised by 1 dB"* — on a log-log plot, the fundamental has slope 1 and the
IM3 product has slope 3; the extrapolated crossing is the intercept point
(<https://en.wikipedia.org/wiki/Third-order_intercept_point>).

```
OIP3(dBm) = P_out(dBm) + ½ · [ P_out(dBm) − P_IMD3(dBm) ]
IIP3(dBm) = OIP3(dBm) − G(dB)
IIP3(dBm) = P_in(dBm)  + ½ · [ P_out(dBm) − P_IMD3(dBm) ]
```

"OIP3 = Po + 1/2(Po - PIMD)"; "IIP3 = OIP3 - Gain"
(<https://www.rfwireless-world.com/terminology/ip2-ip3-formulas-calculations-significance>).
Same source's worked example: two tones at +10 dBm producing IMD3 at −20 dBm give
`IP3 = +10 + (10 − (−20))/2 = +25 dBm`.

Cascade (referred to output, then to input):

```
1/OIP3_total = 1/(G2·G3·OIP3_1) + 1/(G3·OIP3_2) + 1/OIP3_3      (linear, watts)
IIP3_total   = OIP3_total / (G1·G2·G3)
```

same source. Note the **opposite** structure to Friis noise: for noise the *first* stage
dominates, for IP3 the *last* (highest-level) stage dominates.

**3:1 slope demonstration** — canonical numbers a tool can plot and assert. Amplifier with
`G = 20 dB`, `OIP3 = +20 dBm` (so `IIP3 = 0 dBm`), two equal tones, per-tone powers:

| P_in/tone (dBm) | P_out/tone (dBm) | P_IMD3,out (dBm) = `3·P_out − 2·OIP3` | Δ = P_out − P_IMD3 (dB) |
|---|---|---|---|
| −30 | −10 | −70 | 60 |
| −29 | −9 | −67 | 58 |
| −28 | −8 | −64 | 56 |
| −20 | 0 | −40 | 40 |

`[all computed from P_IMD3 = 3·P_out − 2·OIP3]`. Read the slopes: +1 dB of input moves the
fundamental +1 dB and the IM3 product +3 dB, so **the spurious-free window Δ closes at 2 dB
per 1 dB of drive**. `Δ = 2·(OIP3 − P_out)` exactly, and the lines meet (Δ = 0) at
`P_out = OIP3` — which is why the intercept is a fiction: the device compresses long before.

**Compression relation.** Wikipedia gives the rule of thumb: *"the 1 dB compression point
falls approximately 10 dB below the third-order intercept point"*
(<https://en.wikipedia.org/wiki/Third-order_intercept_point>). For the ideal memoryless cubic
`y = a1·x + a3·x³` the exact figure is **9.64 dB**
`[computed: A²_1dB = 0.1449·|a1/a3| from 1 − 0.75(|a3|/a1)A² = 10^(−1/20);`
`A²_IP3 = (4/3)·|a1/a3|; ratio 9.202 → 10·log10(9.202) = 9.639 dB]`. Use ~10 dB in a tool and
say it is a rule of thumb.

**Spurious-free dynamic range**, if the tool wants a single figure of merit:

```
SFDR(dB) = ⅔ · ( IIP3(dBm) − N_floor(dBm) )        [− (S/N)_min if a demod threshold applies]
```

Example `[computed]`: `IIP3 = 0 dBm`, `NF = 3 dB`, `B = 1.6 MHz` → `N_floor = −174 + 62.041
+ 3 = −108.96 dBm`, `SFDR = ⅔ × 108.96 = 72.6 dB`.

---

## 4. Superheterodyne conversion and the image

### 4.1 The mixer relation

Inputs are the RF signal `f_R` and the local oscillator `f_0`; the mixer being non-linear,
its output contains `f_i = n·f_R + m·f_0` for integer m, n [P5 p.37]. The wanted response is
`m = n = 1`:

```
f_i = | f_R − f_0 |
```

[P5 p.37]. An IF bandpass filter selects it [P5 p.35, p.36].

### 4.2 Image frequency and why it sits 2×IF away

Invert the relation: for a given `f_0` and `f_i`, **two** RF frequencies satisfy it
[P5 p.38]:

```
f_R  = f_0 + f_i          (high-side image / wanted, depending on injection)
f_R' = f_0 − f_i
```

Course example [P5 p.38]: `f_0 = 160.7 MHz`, `f_i = 10.7 MHz` →
`f_R = 10.7 ± 160.7 = 150.0 MHz` **and** `171.4 MHz`. Two possible values of `f_R`. If
171.4 MHz is wanted, 150.0 MHz is the image [P5 p.39].

```
| f_R − f_R' | = 2 · f_i        = 2 × 10.7 = 21.4 MHz    [computed, matches P5 p.38/39]
```

Stated in the notes: *"the mixer is equally responsive to two frequencies which are 2 IF's
apart - one is the desired response, fR and the other is the Image Frequency, fR'"*
[P5 p.39]. Confirmed independently: *"These will be separated from the wanted channel by a
frequency equal to twice the IF"*
(<https://www.electronics-notes.com/articles/radio/radio-receiver-selectivity/image-rejection-response.php>).

The physical reason is that the mixer only sees the *magnitude* of the difference. Both the
signal `f_0 + f_i` and the signal `f_0 − f_i` are exactly `f_i` away from the LO — one above,
one below — so both fold down onto the same IF. The mixer cannot tell them apart; only a
filter **before** the mixer can. Hence: *"This illustrates the importance of pre-selection
filtering before mixing"* [P5 p.39], and *"the RF filter is used to remove fR'"* [P5 p.40].

Important asymmetry, stated in the notes and worth putting in a tool's caption: *"The wanted
signal, fR for the receiver is always there, but the image signal, fR' may not be there"*
[P5 p.40]. The image is only a problem when something is actually transmitting on or near it.

**Half-IF spur** (the (2,2) product, a real second-order impairment on the same block): a
signal at `f_LO ± f_i/2` produces `2·f_spur − 2·f_LO = ± f_i`, landing in the IF.
`[derived from f_i = n·f_R + m·f_0, P5 p.37, with n = m = 2; f_spur = f_LO ± IF/2, i.e. exactly
midway between the wanted RF and the LO]`. It sits only **IF/2** from the wanted channel — a
quarter of the image offset of 2·IF — so it is markedly harder to filter than the image.

### 4.3 High-side vs low-side injection

| | High-side: `f_0 = f_R + f_i` | Low-side: `f_0 = f_R − f_i` |
|---|---|---|
| Image at | `f_R + 2·f_i` (above the wanted signal) | `f_R − 2·f_i` (below) |
| LO tuning ratio over a band | smaller | larger |
| Spectral inversion | yes — `f_IF = f_LO − f_RF`, so rising RF gives falling IF | no — `f_IF = f_RF − f_LO` |
| LO leakage out of the antenna sits | above the wanted band | below the wanted band |

**Worked comparison, AM broadcast band 540–1600 kHz with IF = 455 kHz** `[all computed]`:

- High-side LO: 995 → 2055 kHz, **tuning ratio 2.07 : 1**. Image band 1450 → 2510 kHz.
- Low-side LO: 85 → 1145 kHz, **tuning ratio 13.47 : 1**. Image band −370 → 690 kHz.

A single variable capacitor or varactor cannot cover 13.5 : 1 in frequency (that is 181 : 1
in capacitance). **This is the reason every AM broadcast superhet uses high-side injection.**
The trade is spectral inversion, which is harmless for AM and easily undone in DSP.

Note also `2·IF = 910 kHz` is **less** than the 1060 kHz width of the MW band, so for stations
below about 690 kHz the image falls *inside* the broadcast band — a genuine, well-known
weakness of the 455 kHz IF that a teaching tool should show rather than hide `[computed]`.

**Contrast, FM broadcast 88–108 MHz with IF = 10.7 MHz** `[all computed]`:
`2·IF = 21.4 MHz` **exceeds** the 20 MHz band width, so the image band (109.4 → 129.4 MHz for
high-side) lies entirely outside the FM band and no FM station can ever be another station's
image. This is precisely why 10.7 was chosen. Independent confirmation: *"With a 10.7 MHz IF
frequency, the image is always outside of the FM broadcast band, so strong in-band FM signals
are never found at the image frequency"* (search-result summary of
<https://web.ece.ucsb.edu/~long/ece145b/Introduction_to_Receivers_w11.pdf> and
<https://www.electronics-notes.com/articles/radio/superheterodyne-receiver/design-evolution-trends.php>;
the UCSB PDF itself would not fetch — TLS chain error — so this specific sentence is quoted
from the search engine's summary and is **unverified at source**).

### 4.4 The f_RF / IF ratio rule for single conversion

Direct from the notes [P5 p.39]:

> *"fR / fi ratio should not exceed 10 or 20 for 1 down conversion to avoid extreme
> selectivity requirements."*

The mechanism: the preselector must reject at a fractional offset of `2·IF / f_RF`. Push the
ratio up and that offset shrinks toward the filter's own passband, so the required Q explodes.

| f_RF | IF | f_RF / IF | image offset | as % of f_RF | verdict against the ≤10–20 rule |
|---|---|---|---|---|---|
| 1.07 MHz (MW) | 455 kHz | 2.4 | 910 kHz | 85 % | comfortable |
| 98 MHz (FM) | 10.7 MHz | 9.2 | 21.4 MHz | 22 % | comfortable |
| 150 MHz (VHF) | 10.7 MHz | 14.0 | 21.4 MHz | 14 % | at the limit |
| 900 MHz | 45 MHz | 20.0 | 90 MHz | 10 % | at the limit |
| 2450 MHz | 70 MHz | 35.0 | 140 MHz | 5.7 % | **fails — needs dual conversion** |
| 6000 MHz | 70 MHz | 85.7 | 140 MHz | 2.3 % | **fails badly** |
| 2450 MHz | 10.7 MHz | 229.0 | 21.4 MHz | 0.87 % | **hopeless single-conversion** |

`[all computed]`. This table is the honest answer to "why does a microwave receiver convert
twice": a 6 GHz link cannot reach 70 MHz in one hop under this rule, so it goes 6 GHz → a
first IF in the hundreds of MHz to ~1 GHz → 70 MHz.

### 4.5 Why 455 kHz / 10.7 MHz / 70 MHz specifically

Course statement: *"Commonly used IF frequencies are: 70 MHz, 10.7 MHz and 455 kHz"*
[P5 p.36]. Reasons, from the web sources:

- **455 kHz (AM broadcast, MW/HF).** Chosen when *"high-quality, low-cost ceramic and crystal
  IF filters were manufactured for that band"*; it gives adequate image spacing for the MW
  band with simple front-end tuning, and AM's ~5–10 kHz audio bandwidth is easy to realise
  there with good stability and selectivity. Mechanical and crystal filters *"until the 1960s
  became expensive and performed poorly much above this frequency"*. Low IF ⇒ **excellent
  adjacent-channel selectivity** (narrow fractional bandwidth is cheap), poor image rejection.
- **10.7 MHz (FM broadcast, VHF).** Chosen so that `2·IF = 21.4 MHz` exceeds the 20 MHz FM
  band width, pushing all images out of band (§4.3). Also standard for the 88–108 MHz band's
  200 kHz channel spacing, which a 10.7 MHz ceramic filter handles.
- **70 MHz (microwave, satellite, radar).** *"A common design trend is to use a first IF
  frequency considerably higher than the RF, typically in the range of 35 to 60 MHz (50 MHz
  is common in HF receivers, 70 MHz in microwave receivers), as the high IF makes it possible
  to suppress VHF images with a simple low-pass filter."* High IF ⇒ **easy image rejection**,
  but the IF filter now needs a tiny fractional bandwidth for a given channel, so selectivity
  moves to a second, lower IF.

All three bullets' quoted text: search-result summaries citing
<https://web.ece.ucsb.edu/~long/ece145b/Introduction_to_Receivers_w11.pdf>,
<https://www.quora.com/How-do-I-choose-the-intermediate-frequency-IF-and-why-445-khz>, and
<https://www.electronics-notes.com/articles/radio/superheterodyne-receiver/design-evolution-trends.php>.
**Flagged: the UCSB PDF failed to fetch (TLS certificate chain error) and these quotes were
not verified at the primary source.** The underlying engineering trade — *low IF buys
selectivity, high IF buys image rejection, and you cannot have both in one conversion* — is
however exactly what [P5 p.39] states in the f_RF/IF rule, and that citation is verified.

**The core trade-off, in one line:** raising the IF moves the image further from the wanted
signal (easier RF filter) but makes the IF filter's fractional bandwidth smaller for the same
channel width (harder IF filter). Dual conversion exists to take both wins.

### 4.6 Achievable image rejection with real filters

| Filter type / case | Image rejection | Source |
|---|---|---|
| Typical "good" receiver specification | **> 70 dB** | search summary of <https://www.sciencedirect.com/topics/engineering/image-rejection> |
| SAW filter | *"less than 1-dB ripple in the passband and over 60 dB of rejection in the stopband depending on the bandwidth"* | same |
| Cavity filter, 3 % fractional BW at 6 GHz | *"40+ dB rejection at the image offset"* | same |
| Microstrip filter, same job | *"only 20 dB"* | same |
| General receiver practice | *"Normally it is possible to achieve figures of 60 to 80 dB rejection, and on some receivers figures of 100 dB have been quoted"* | <https://www.electronics-notes.com/articles/radio/radio-receiver-selectivity/image-rejection-response.php> |
| Worked meaning of the number | *"it may be 60 dB at 30 MHz. This means that if signals of the same strength were present on the wanted frequency and the image frequency, then the image signal would be 60 dB lower than the wanted one"* | same |

The last row is the definition a tool should use: **image rejection ratio in dB = the extra
attenuation the front end applies to `f_R'` relative to `f_R`**, so an image signal of level
`P_img` arrives at the IF at `P_img − IRR`. It only causes trouble if
`P_img − IRR > C − (C/I)_required`.

Typical front-end architecture that produces those numbers: *"a RF bandpass filter, usually a
surface acoustic wave (SAW) device, is utilized to perform band selection ahead of the low
noise amplifier (LNA), while a second filter follows the LNA to perform image rejection"*
(search summary, ScienceDirect image-rejection topic page). Two filters, because the first
must be low-loss (it is in front of the LNA and adds directly to NF, §5.4) and the second can
afford loss (it sits behind 15–20 dB of gain).

### 4.7 Related C/I material in the same lecture (for context)

Co-channel and adjacent-channel interference are analysed by the same budget method: compute
the wanted carrier `C` from `P_Tx1`, `G_Tx1` toward Rx1, `G_Rx1` toward Tx1, and distance
`d_w`; compute the interferer `I` from `P_Tx2`, `G_Tx2` *toward Rx1* (a sidelobe, not the
main lobe), `G_Rx1` *toward Tx2*, distance `d_i`, any obstruction, and cross-polar
discrimination [P5 p.52, p.53]. Ways to raise C/I: narrower beamwidths / lower sidelobe
ratios, orthogonal polarisation, natural obstructions, and *"all ratio would be increased if
di/dw is greater"* [P5 p.54]. Dog-legging deliberately breaks a multi-hop microwave chain out
of a straight line so that the repeated frequency arrives only via sidelobes [P5 p.57, p.58].

Dish beamwidth, if a tool needs it: `HPBW(degrees) = 22 / (f_GHz · D_metres)` [P5 p.44].
Antenna gain `G = 4π·A_eff / λ²` [P5 p.45]; parabolic dish assumed 56 % efficient [P5 p.45].

Adjacent-channel: interference exists only where the interferer's emission spectrum overlaps
the wanted receiver's filter response, so the estimate needs both the Tx spectral mask and the
Rx filter shape [P5 p.59, p.60, p.61]. "It is obvious that if the two frequencies are further
apart the adjacent interference level will be lower" [P5 p.62].

Spurious vs harmonic, for a spectrum-mask tool: *"Spurious Emissions are any radiation that is
not required for transmitting the desired information (and not harmonically related to
fundamental frequency)"*; harmonics are the integer multiples [P5 p.18].

---

## 5. Noise: floor, bandwidth, noise figure, cascade dominance

### 5.1 Thermal noise floor per hertz

```
N_0 = k · T_0        W/Hz
```

`[computed]` with k = 1.380649×10⁻²³ J/K and T_0 = 290 K:

```
k·T_0 = 4.0039 × 10⁻²¹ W/Hz
      = 10·log10(4.0039e-21)        = −203.975 dBW/Hz
      = 10·log10(4.0039e-21 / 1e-3) = −173.975 dBm/Hz   →  −174 dBm/Hz
```

Using the notes' rounded k = 1.38×10⁻²³ gives −173.977 dBm/Hz `[computed]` — same to three
figures. Confirmed: *"10 log(kT₀) = 10 log(1.38 × 10⁻²³ × 290) ≈ -174 dBm"*
(<https://www.qsl.net/va3iul/Noise/Understanding%20Noise%20Figure.pdf>, via search summary;
the same value appears in <https://rfessentials.com/resources/rf-glossary/noise-floor/>).

Note **290 K is a definition, not a measurement** — it is the standardised reference for
noise-figure specification (≈ 17 °C / 62 °F), chosen so that kT₀ lands on a round number.
The notes call it "room temperature (290 K)" [6A p.24].

### 5.2 How bandwidth changes it

```
N(dBm) = −174 + 10·log10( B / 1 Hz ) + NF(dB)
```

`10·log10(B)` is the only bandwidth term, so **the noise floor rises 3.01 dB per doubling of
bandwidth and 10 dB per decade** — *"the noise floor increases by 3 dB for every doubling of
bandwidth"* (search summary, RF Essentials noise-floor page). Reference values `[computed]`:

| B | 10·log10(B) | N at NF = 0 dB (dBm) |
|---|---|---|
| 1 Hz | 0.00 | −174.0 |
| 1 kHz | 30.00 | −144.0 |
| 30 kHz (AMPS, [6A p.26]) | 44.77 | −129.2 |
| 200 kHz (GSM, [P5 p.68]) | 53.01 | −121.0 |
| 1 MHz | 60.00 | −114.0 |
| 1.6 MHz (§2 example) | 62.04 | −112.0 |
| 20 MHz | 73.01 | −101.0 |

This is the single most important design lever in the whole budget: **halving the receiver
bandwidth buys 3 dB of link margin for free**, which is exactly why *"Receivers are designed
to have as narrow a bandwidth as possible to receive only the signals transmitted from its
wanted receiver. Any other signal it receives is interference"* [P5 p.49].

### 5.3 What a noise figure physically means

`F` is the factor by which a real device's output noise exceeds that of an ideal noiseless
device of the same gain at the same source temperature — equivalently, the factor by which
the device degrades signal-to-noise ratio:

```
F = SNR_in / SNR_out           (both linear, source at T_0 = 290 K)
NF(dB) = SNR_in(dB) − SNR_out(dB)
```

The notes present it as the multiplier in `N = k·T_0·B·F` [6A p.24, eqn (3)] and give the
temperature equivalence `F = 1 + T_e/T_0` [6A p.24].

Physical readings of `NF = x dB`:

| NF | F (linear) | T_e = (F−1)·290 K | Meaning |
|---|---|---|---|
| 0 dB | 1.00 | 0 K | perfect — impossible |
| 0.5 dB | 1.122 | 35.4 K | very good LNA |
| 1.5 dB | 1.413 | 119.6 K | good LNA |
| 3.0 dB | 1.995 | 288.6 K | device adds as much noise as the source; SNR halves |
| 5.0 dB | 3.162 | 627.1 K | the §2 example receiver |
| 12.0 dB | 15.85 | 4306 K | the no-LNA cascade of §5.4 |

`[T_e column computed from T_e = (10^(NF/10) − 1)·290]`.

The 3 dB row is the intuition anchor: at NF = 3 dB the device injects noise equal to what it
receives, so it throws away exactly half the signal-to-noise ratio.

### 5.4 Why the first stage dominates — with numbers

The notes state the conclusion: *"The first (front) stage of the receiver is the most
important (i.e. should have high gain but low noise)"* [6A p.26]. The reason is structural in
§1.9: stage `i`'s excess noise `(F_i − 1)` is divided by the product of **all preceding
gains**, so once the first stage has 20 dB of gain everything behind it is attenuated by 100×
before it counts.

**Reference cascade** `[all computed from §1.9, linear arithmetic, dB conversion last]`:

| # | Stage | NF (dB) | Gain (dB) | F (lin) | G (lin) | Contribution to F_total (lin) | Share of total |
|---|---|---|---|---|---|---|---|
| 1 | feedline / duplexer | 1.0 | −1.0 | 1.2589 | 0.7943 | 1.25893 | 65.4 % |
| 2 | LNA | 1.5 | +20.0 | 1.4125 | 100.0 | 0.51935 | 27.0 % |
| 3 | passive mixer (CL 7 dB) | 7.0 | −7.0 | 5.0119 | 0.1995 | 0.05051 | 2.6 % |
| 4 | IF amplifier | 4.0 | +30.0 | 2.5119 | 1000.0 | 0.09539 | 5.0 % |
| | **total** | | **+42.0** | | | **F = 1.9242** | **NF = 2.84 dB** |

Read the last two columns. The mixer has a 7 dB noise figure — the worst in the chain — and
contributes **2.6 %** of the total. The 1 dB feedline in front contributes **65 %**. Same
cascade, four experiments:

| Variant | Cascade NF | Δ vs baseline |
|---|---|---|
| **Baseline** (feedline → LNA 1.5/20 → mixer → IF amp) | **2.842 dB** | — |
| Delete the LNA entirely (feedline → mixer → IF amp) | **12.000 dB** | **+9.16 dB** |
| Move the LNA to the mast head, ahead of the feedline | **1.934 dB** | **−0.91 dB** |
| Keep the LNA but drop its gain to 10 dB | **5.102 dB** | **+2.26 dB** |

`[all computed]`. Three teaching points fall straight out:

1. **The LNA buys 9.2 dB of sensitivity** — the whole link budget's worth of margin — purely
   by putting gain in front of the lossy stages.
2. **The no-LNA case comes out at exactly 12.000 dB = 1 + 7 + 4.** That is not a coincidence:
   when every stage before an amplifier is passive, §1.9 collapses to `F = L_1·L_2·F_amp`
   `[derived; verified numerically: 1.2589 × 5.0119 × 2.5119 = 15.849 = 12.000 dB]`, i.e.
   **losses in front of the first gain stage add decibel-for-decibel to the system NF.**
3. **LNA gain matters as much as LNA noise figure.** Dropping G from 20 dB to 10 dB costs
   2.26 dB even though the LNA's own NF never changed. This is the "high gain *and* low noise"
   in [6A p.26].

Point 2 is also the argument for the mast-head LNA and for the two-filter front end of §4.6:
every dB of filter or feeder loss ahead of the first amplifier is a dB of system noise figure.

### 5.5 Realistic component values for tool defaults

| Component | Typical NF | Typical gain | Source |
|---|---|---|---|
| Modern integrated LNA | 0.4 – 1.2 dB | 15 – 25 dB | search summary: *"modern LNAs can achieve noise figures in the 0.4–1.2 dB range with gains typically between 15–25 dB"*; *"typical gain values of LNA range from 10 to 30 dB"*; *"Usually 15–25 dB; enough to overcome downstream noise without saturation"* — <https://www.origin-ic.com/blog/key-low-noise-amplifier-specifications-to-consider/49110>, <https://www.sciencedirect.com/topics/engineering/low-noise-amplifier> |
| LNA design targets | < 1.5 dB (satellite/GPS), < 3 dB (general comms) | | same |
| Published LNA data points | 0.73 dB at 20.4 dB gain; 1.03 dB at 21.45 dB gain; 1.2 dB (diversity Rx module) | | <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11679211/>, <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8704615/> (via search summaries) |
| Passive double-balanced mixer | = conversion loss | −5 to −8 dB (conversion loss 5–8 dB typical; 6–11 dB across all real passive microwave mixers) | <https://rfessentials.com/rf-knowledge-base/what-is-the-noise-figure-of-a-passive-mixer-and-how-does-conversion-loss-factor-/> and search summary of <https://www.sciencedirect.com/topics/engineering/balanced-mixer> |
| RF/IF SAW filter | = insertion loss (§1.10) | −1 to −3 dB typical passband, > 60 dB stopband | §4.6 sources |
| Coax feeder / duplexer | = insertion loss | −0.5 to −3 dB | [6A p.26] uses 3 dB; §2 example uses 2 dB |
| Handset receiver, complete | 5 dB | — | [6A p.19] |
| AMPS phone + 3 dB cable | 9 dB | — | [6A p.27] |

Caveat: every entry sourced to a "search summary" above came from the search engine's
extracted text, not from a page I fetched and read end to end. The two I fetched and read
directly are the electronics-notes image-rejection page and the rfwireless-world IP3 page.
Treat the LNA/mixer numbers as **typical-value guidance for slider ranges, not as
specifications**.

---

## 6. DO NOT FAKE — quantities that must be computed, never drawn by eye

Every item below has a closed form in this document. Drawing it by eye, hard-coding it, or
tuning it until "it looks right" produces a tool that teaches the wrong physics. Each entry
names the formula and a cheap assertion.

1. **Free space loss.** Compute `92.45 + 20·log10(f_GHz·d_km)` (§1.4). Do not draw a
   straight line on a linear distance axis — FSL is linear in `log d`, 6.02 dB per doubling.
   *Assert:* `FSL(2×d) − FSL(d) = 6.02 ± 0.01 dB` for any d.
2. **The dB waterfall in a link budget bar chart.** Every bar segment must be the actual
   `+G` or `−L` in dB, and the running total must land on the computed `C`. Do not scale
   segments for visual balance. *Assert:* the §2 chain sums to −83.795 dBm ± 0.1.
3. **Noise floor `N`.** Compute `−174 + 10·log10(B) + NF` (§1.8, §5.2). Never a fixed pixel
   line. When the bandwidth slider moves, the line must move 3.01 dB per octave.
   *Assert:* `N(2B) − N(B) = 3.01 ± 0.01 dB`.
4. **Cascade noise figure.** Compute via §1.9 **in linear terms** and convert once at the
   end. Adding dB noise figures is the classic wrong answer — it gives 13.5 dB for the §5.4
   baseline instead of the correct 2.84 dB. *Assert:* the §5.4 baseline returns
   2.842 ± 0.01 dB, and the AMPS example [6A p.26–27] returns 9.03 ± 0.01 dB.
5. **Per-stage noise contribution shares** (the 65 / 27 / 2.6 / 5.0 % split of §5.4). These
   are `(F_i − 1)/∏G` divided by `F_total`, not a hand-picked pie chart.
6. **Fade margin.** `C − R_T`, or equivalently `C/N − (C/N)_min` (§1.5). The two routes must
   agree to floating-point precision in the same tool — if they disagree, one of them is
   fabricated. *Assert:* both give 14.164 ± 0.1 for §2.
7. **Eb/No.** `C/N + 10·log10(B/R)` (§1.7). The `B/R` correction is often small (2.04 dB in
   §2) and therefore tempting to drop. Do not drop it.
8. **Image frequency.** `f_R' = f_R ± 2·IF` (§4.2), computed from the current IF and injection
   side. The image marker on a spectrum plot must sit exactly `2·IF` from the wanted marker
   at every slider position. *Assert:* `|f_img − f_RF| = 2·IF` exactly.
9. **LO frequency and tuning ratio.** `f_LO = f_RF ± IF`; ratio = `f_LO,max / f_LO,min` over
   the band (§4.3). *Assert:* MW 540–1600 kHz with 455 kHz IF gives 2.07 high-side and 13.47
   low-side, ±0.01.
10. **Whether the image lands in band.** The test is `2·IF` vs the band width, not a
    judgement call. *Assert:* MW/455 kHz → in-band images exist; FM/10.7 MHz → they do not.
11. **f_RF / IF ratio and the ≤10–20 verdict** (§4.4). Compute the ratio and compare;
    do not label an architecture "single conversion" by intuition.
12. **Intermodulation product frequencies.** Compute `n·f1 ± m·f2` for the actual tone
    frequencies on screen (§3.2). Never place spurs at eyeballed offsets. *Assert:* with
    f1 = 900, f2 = 901 MHz the 3rd-order pair is exactly 899 and 902 MHz.
13. **Which products are in band.** Test each computed product against the actual channel
    edges. Do not assume "odd = in band" — that heuristic is only true for closely spaced
    tones, and a tool with a tone-spacing slider will break it.
14. **IM3 product level and the 3:1 slope.** `P_IMD3 = 3·P_out − 2·OIP3` (§3.5). The IM3
    trace must have slope exactly 3 against input power in dB. *Assert:* a 1 dB input step
    moves the fundamental 1.00 dB and the IM3 3.00 dB, ±0.01.
15. **Intercept point location.** The crossing of the slope-1 and slope-3 lines, solved for,
    not placed. *Assert:* the lines meet at `P_out = OIP3` within 0.01 dB.
16. **Δ (spurious-free window) and SFDR.** `Δ = 2·(OIP3 − P_out)`;
    `SFDR = ⅔·(IIP3 − N_floor)` (§3.5).
17. **Cascade IIP3.** The reciprocal-sum formula in §3.5, in linear watts. It has the
    opposite weighting to Friis noise — do not reuse the noise code.
18. **Image rejection consequence.** The residual image level at the IF is
    `P_img − IRR(dB)`; whether it matters is `P_img − IRR` vs `C − (C/I)_required`
    (§4.6). Compute the comparison, do not colour the bar by hand.
19. **Bandpass noise power and post-demod SNR.** `σ²_n = η·B` and
    `SNR_out = A_c²·σ²(s)/(η·B)` (§1.12). *Assert:* the [W4 p.13] case returns 0.04 W and
    25 (13.98 dB).
20. **Antenna beamwidth**, if drawn: `22/(f_GHz·D_m)` degrees [P5 p.44]. The lobe width on
    screen must follow it.
21. **Anything read off a Bullington/Rayleigh fading curve.** There is no closed form for the
    Bullington curves in these notes [6A p.15, p.16 — p.16 is a bitmap]. Either use the exact
    Rayleigh deep-fade relation `P = 10^(−FM/10)` and say so, or label the axis qualitatively.
    Do not digitise the slide's plot by eye and present the result as a number.

**Meta-rule:** if a tool displays a number, that number must come from an expression in this
document evaluated on the current control state. If it cannot, the tool should not display it.

---

## 7. Quick reference card

```
P(dBm)      = P(dBW) + 30
EIRP        = P_T + G_T − L_T                                    dBm
FSL         = 92.45 + 20·log10(f_GHz · d_km)                     dB      (= 32.45 + 20·log10(f_MHz·d_km))
            = 20·log10(4πd/λ)                                    dB
C           = EIRP − FSL + G_R − L_R − L_impl                    dBm
N           = −174 + 10·log10(B/Hz) + NF                         dBm
C/N         = C − N                                              dB
Eb/No       = C/N + 10·log10(B/R)                                dB
FM          = C − R_T = C/N − (C/N)_min                          dB
N           = k·T_0·B·F         k=1.380649e-23 J/K, T_0=290 K    W
F           = 1 + T_e/T_0        T_e = (F−1)·T_0                 —, K
F_cascade   = F1 + (F2−1)/G1 + (F3−1)/(G1G2) + …                 linear only
F_passive   = L      (NF dB = insertion loss dB)                 —
f_IF        = |f_RF − f_LO|                                      Hz
f_image     = f_RF ± 2·f_IF                                      Hz
f_RF/f_IF   ≤ 10…20 for single conversion
IM products = n·f1 ± m·f2,  order = n+m;  odd orders land in band
P_IMD3      = 3·P_out − 2·OIP3                                   dBm
OIP3        = P_out + ½(P_out − P_IMD3);  IIP3 = OIP3 − G        dBm
IIP3        ≈ P1dB + 9.6 dB  (ideal cubic; ~10 dB rule of thumb) dBm
SFDR        = ⅔·(IIP3 − N_floor)                                 dB
σ²_n        = η·B  ;  SNR_out(DSB coherent) = A_c²·σ²(s)/(η·B)
HPBW        = 22/(f_GHz · D_m)                                   degrees
```

---

## Sources

Course PDFs (read in full via `pdftotext -layout`; bitmap-only slides noted above):

- `C:\Users\yongw\Downloads\IE4155 Part 6A.pdf` — 28 pages
- `C:\Users\yongw\Downloads\IE4155 Part 5 AY24-25 (1).pdf` — 76 pages
- `C:\Users\yongw\Downloads\17S1_EE3012_Lecture Notes_Week4.pdf` — 17 pages

Web (fetched and read directly):

- [Understand Radio Image Rejection & Image Response — Electronics Notes](https://www.electronics-notes.com/articles/radio/radio-receiver-selectivity/image-rejection-response.php)
- [IP2 and IP3: Formulas, Calculations, and Significance — RF Wireless World](https://www.rfwireless-world.com/terminology/ip2-ip3-formulas-calculations-significance)
- [Third-order intercept point — Wikipedia](https://en.wikipedia.org/wiki/Third-order_intercept_point)

Web (search-result summaries only — quoted text **not verified at source**):

- [Understanding Noise Figure (qsl.net/va3iul)](https://www.qsl.net/va3iul/Noise/Understanding%20Noise%20Figure.pdf)
- [Noise Floor — RF Essentials](https://rfessentials.com/resources/rf-glossary/noise-floor/)
- [Passive Mixer Noise Figure and Conversion Loss — RF Essentials](https://rfessentials.com/rf-knowledge-base/what-is-the-noise-figure-of-a-passive-mixer-and-how-does-conversion-loss-factor-/)
- [Introduction to Receivers — UCSB ECE145B](https://web.ece.ucsb.edu/~long/ece145b/Introduction_to_Receivers_w11.pdf) *(direct fetch failed: TLS certificate chain error)*
- [Superhet Design Evolution & Trends — Electronics Notes](https://www.electronics-notes.com/articles/radio/superheterodyne-receiver/design-evolution-trends.php)
- [Image Rejection — ScienceDirect Topics](https://www.sciencedirect.com/topics/engineering/image-rejection)
- [Balanced Mixer — ScienceDirect Topics](https://www.sciencedirect.com/topics/engineering/balanced-mixer)
- [Low Noise Amplifier — ScienceDirect Topics](https://www.sciencedirect.com/topics/engineering/low-noise-amplifier)
- [How to Choose a Low Noise Amplifier — Origin IC](https://www.origin-ic.com/blog/key-low-noise-amplifier-specifications-to-consider/49110)
- [A 0.73 dB Multi-Gain Low Noise Amplifier — PMC11679211](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11679211/)
- [A Low-Band Multi-Gain LNA with 1.2 dB NF — PMC8704615](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8704615/)
- [Determine RF Receiver Specifications — MathWorks](https://www.mathworks.com/help/simrf/ug/determine-rf-receiver-specification.html)
- [How do I choose the intermediate frequency IF — Quora](https://www.quora.com/How-do-I-choose-the-intermediate-frequency-IF-and-why-445-khz)
- [Understanding the Third-Order Intercept Point of a Cascaded System — All About Circuits](https://www.allaboutcircuits.com/technical-articles/understanding-the-third-order-intercept-point-of-a-cascaded-system/) *(direct fetch failed: HTTP 403)*
