# Candidate tools and suite structure

Curriculum plan for extending `engineering-viz` from 15 tools to ~29, and for
reorganising the flat index into a hub plus seven category pages.

Target learner: undergraduate wireless communications (IE4155 / EE4155 / EE3012).
Every proposal below is scored on two things — is it in the syllabus, and does it
actually need motion or interaction to land? Anything that a static equation or a
table already teaches well is not here.

---

## 1. What the research says

### What was actually checked

Sources reached this session (July 2026):

- **Circles, Sines and Signals** — <https://jackschaedler.github.io/circles-sines-signals/>
  (fetched, introduction page). Explicit design statement from the author: absorb
  information "visually instead of linguistically", and a deliberate decision to
  *avoid* gratuitous interactivity. Structure is roughly 30 short single-idea pages
  (sine and cosine, complex numbers, signals, discrete signals, coordinates, DFT
  introduction, DFT walkthrough). Its standout page animates every arithmetic
  operation of an 8-point DFT one at a time.
- **RF Cafe calculator list** — <http://blog.rfcafe.com/references/calculators/calculator-list.htm>
  (search result summary; the page itself was not fetched). Coverage is
  calculator-shaped: attenuators, path loss, propagation time, cavity resonance,
  filter responses, and a **cascade calculator** for output power, gain, noise
  figure and intermodulation.
- **DSP Illustrations** — <https://dspillustrations.com/pages/posts/misc/the-cyclic-prefix-cp-in-ofdm.html>
  (search result summary). Notebook-and-plot style: derivation, code, static
  matplotlib figures, one concept per page.
- **Falstad applet collection** — <https://www.falstad.com/> (fetch returned HTTP 403;
  only the search-result description was available). Known for real-time field and
  wave simulation with direct dragging.
- **Awesome-explorables** — <https://github.com/blob42/awesome-explorables>, and the
  Wikipedia definition of an explorable explanation: an interactive simulation
  *plus guidance on what to try*, so the reader tests expectations against behaviour.
- Two searches for interactive teaching tools on **multipath delay spread /
  coherence bandwidth** and on **FM Bessel spectra** returned only PDFs, lecture
  notes, patents and MATLAB scripts — no well-known browser explorable for either.

Unverified: I did not open the Falstad applet index, the RF Cafe calculator index,
or the DSP Illustrations topic index directly. Statements about those three rest on
search-result summaries and should be treated as second-hand.

### The four things good tools do

1. **One idea per page, and the page says which idea.** Circles/Sines/Signals never
   mixes two concepts on one canvas. This is already the house pattern in
   `STYLE.md` (numbered `.sec` blocks) — keep it.
2. **Show the mechanism, not just the result.** The DFT walkthrough earns its
   reputation by animating the multiply-and-sum, not by plotting the output. The
   equivalent moves here: animate the *correlator integrating* in CDMA, the *delayed
   copy smearing* into the previous OFDM symbol, the *match walking to the centre*
   of a Smith chart.
3. **Restraint beats knob-count.** The author of the best-regarded piece explicitly
   warns against gratuitous interactivity. Prefer 4–6 sliders that each change
   something visible over 12 that mostly do nothing.
4. **Numbers alongside the picture.** RF Cafe's whole value is that it answers in
   dB and dBm. The `.cards` metric grid already does this; every new tool must land
   a real engineering number (dBm, dB, Erlangs, µs, %) next to the animation.

### Where the market is thin — and the suite should not be

Searches surfaced no widely-used browser explorable for delay spread and coherence
bandwidth, for FM Bessel sidebands, for Erlang B trunking efficiency, or for
handover hysteresis. These are exactly the syllabus topics where equations are
opaque and motion is decisive. They rank highest below.

### Syllabus coverage audit of the existing 15

| Syllabus item | Covered by | Gap |
|---|---|---|
| Propagation mechanisms | radio-propagation | — |
| Path geometry and clearance | fresnel-clearance | — |
| Link performance | link-budget | no noise floor, no fade margin |
| **Fading** | — | **nothing** |
| RF spectrum management | partial (superhet-image) | no channelisation, no selectivity |
| Intermodulation, image rejection | superhet-image | — |
| C/I and interference | cellular-reuse | no adjacent-channel case |
| Cellular reuse, SIR | cellular-reuse | — |
| **Handover, power control, cell splitting, sectorisation** | — | **nothing** |
| **Erlang / trunking** | — | **nothing** |
| **FDMA / TDMA / CDMA / OFDMA** | — | **nothing** |
| AM | modulation | no power budget, no overmodulation |
| **DSBSC / SSB / QAM / FDM** | iq-constellation (QAM only) | **mostly missing** |
| FM and PM | modulation | waveform only |
| **Bessel spectra, Carson's rule** | — | **nothing** |
| **Noise in analog systems** | — | **nothing** |

Seven hard zeroes. The ranking below follows them.

---

## 2. Proposed tools, most valuable first

Each entry: file name, title, category, what it shows, formulas to implement,
controls, why an RF engineer needs it.

---

### 1. `multipath-fading.html` — Multipath, delay spread and fading
**Category:** propagation

Drops a handful of reflected copies onto a direct path and shows the three faces of
the same channel at once: the tap delay profile, the resulting notches in the
frequency response, and the received envelope thrashing up and down as the mobile
drives. Moving the mobile animates all three together, so a deep fade in time and a
notch in frequency are visibly the same event.

**Formulas**
- Two-ray: `Δd ≈ 2·h_t·h_r/d`, `Δφ = 2π·Δd/λ`, `E ∝ |1 + Γ·e^(−jΔφ)|`;
  far-field `Pr = Pt·Gt·Gr·h_t²·h_r²/d⁴`; breakpoint `d_b = 4π·h_t·h_r/λ`
- Tapped delay line `h(τ) = Σ a_k·e^(jθ_k)·δ(τ − τ_k)`;
  `H(f) = Σ a_k·e^(jθ_k)·e^(−j2πf·τ_k)`
- Mean excess delay `τ̄ = Σa_k²τ_k / Σa_k²`; RMS delay spread
  `σ_τ = √(τ²̄ − τ̄²)` with `τ²̄ = Σa_k²τ_k²/Σa_k²`
- Coherence bandwidth `Bc ≈ 1/(5σ_τ)` (0.5 correlation), `1/(50σ_τ)` (0.9)
- Flat vs frequency-selective test: `B_signal` vs `Bc`, and `Ts` vs `σ_τ`
- Doppler `f_d = (v/λ)·cos θ`; max `f_m = v/λ`; coherence time `Tc ≈ 0.423/f_m`
- Rayleigh envelope CDF `P(r ≤ R) = 1 − exp(−R²/2σ²)`; Rician `K = A²/2σ²`
- Level crossing rate `N_R = √(2π)·f_m·ρ·e^(−ρ²)`, average fade duration
  `(e^(ρ²) − 1)/(ρ·f_m·√(2π))`, `ρ = R/R_rms`
- Rayleigh outage for margin M dB: `P = 1 − exp(−10^(−M/10))`

**Controls** — number of taps (2–8) with draggable delay and amplitude per tap;
K-factor slider sweeping LOS → Rician → Rayleigh; mobile speed; carrier frequency;
signal bandwidth; two-ray heights and separation; play/pause the drive.

**Why** — the link budget in the suite predicts a comfortable margin and the radio
still drops. This is the tool that explains the difference: a 30 dB fade lasting a
few milliseconds is invisible in a mean-power calculation, and whether it hits the
whole signal or one part of it depends entirely on `B` vs `Bc`. No well-known
browser explorable does this; it is the largest single gap in the suite.

---

### 2. `noise-figure-sensitivity.html` — Noise figure, cascades and sensitivity
**Category:** receivers

Builds a receive chain block by block — antenna, cable, LNA, filter, mixer, IF amp —
and draws the classic level diagram: wanted signal and noise floor in dBm marching
stage by stage. Dragging the cable in front of the LNA versus behind it moves the
sensitivity number by tens of dB, which is the whole lesson in one gesture.

**Formulas**
- Thermal noise `N_dBm = −174 + 10·log10(B)` at 290 K (from `N = kTB`)
- Noise factor `F = SNR_in/SNR_out`; `NF = 10·log10(F)`
- Friis cascade `F_tot = F₁ + (F₂−1)/G₁ + (F₃−1)/(G₁G₂) + …`
- Passive loss L: `F = L`, `G = 1/L`
- Noise temperature `Te = (F − 1)·290`; `T_sys = T_ant + Te`
- Sensitivity `P_min(dBm) = −174 + NF_tot + 10·log10(B) + SNR_req`
- Cascade gain `G_tot(dB) = ΣG_i`
- Cascade input intercept `1/IIP3_tot = Σ (G_cum,i−1 / IIP3_i)` (linear)
- `SFDR = (2/3)·(IIP3 − N_floor) − SNR_min`

**Controls** — reorderable chain of 4–6 blocks; per-block gain, NF and IIP3;
noise bandwidth; required SNR; antenna noise temperature; toggle between sensitivity
view and dynamic-range view.

**Why** — "LNA first" is a slogan every student repeats and few can quantify. The
level diagram turns Friis from an algebra exercise into a visible staircase, and it
is the missing half of the existing link budget tool: that one gives received power,
this one gives the floor it has to beat. It also closes the loop with
`superhet-image.html` by putting the noise floor and the IM3 products on one axis.

---

### 3. `fm-bessel-spectrum.html` — FM sidebands, Bessel functions and Carson's rule
**Category:** modulation

Sweeps the modulation index and shows the FM line spectrum reorganising itself:
sidebands appearing, the carrier collapsing to nothing at β = 2.405 and coming back
inverted, and the Carson bracket widening. A running power tally shows what fraction
of the total actually sits inside the Carson bandwidth.

**Formulas**
- `s(t) = Ac·cos(2πf_c t + β·sin 2πf_m t)`, `β = Δf/f_m = k_f·A_m/f_m`
- Line spectrum `s(t) = Ac·Σ_n J_n(β)·cos(2π(f_c + n·f_m)t)`
- `J_n(β) = Σ_{m≥0} (−1)^m/(m!(m+n)!)·(β/2)^(2m+n)` — series is fine for β ≲ 15,
  use the recurrence `J_{n−1}(β) + J_{n+1}(β) = (2n/β)·J_n(β)` downward if extended
- Carson `B ≈ 2(Δf + f_m) = 2f_m(β + 1)`; deviation ratio `D = Δf_max/W`
- Power identity `Σ_n J_n²(β) = 1` — display in-band power fraction
- Carrier nulls at the zeros of `J₀`: β = 2.405, 5.520, 8.654
- PM: `β = k_p·A_m`, independent of `f_m` — sweep `f_m` to contrast FM and PM bandwidth
- Narrowband limit check: β ≪ 1 → only `J₀`, `J₁` significant, `B ≈ 2f_m`

**Controls** — β directly, or Δf and f_m separately; FM/PM toggle; carrier amplitude;
Carson bracket on/off; animate β sweeping 0 → 10; overlay time-domain waveform.

**Why** — β is the only knob in FM and its effect on occupied bandwidth is genuinely
non-obvious from the equation. Watching the carrier line vanish at β = 2.405 is the
moment Bessel functions stop being a table in an appendix. The syllabus names this
explicitly and no good interactive version was found.

---

### 4. `multiple-access.html` — FDMA, TDMA, CDMA and OFDMA
**Category:** cellular

Puts the same set of users through one time–frequency–code resource grid four ways
and animates their traffic flowing through it. Guard bands, guard times, ramp-up and
overhead are drawn to scale, so the efficiency tax of each scheme is a visible area
rather than a percentage in a footnote.

**Formulas**
- FDMA: `N = (B_total − 2·B_guard)/B_channel`; efficiency `η = N·B_c/B_total`
- TDMA: frame `T_f`, N slots; `η = (T_f − N·T_guard − T_overhead)/T_f`;
  burst rate `R_burst = N·R_user/η`
- CDMA: processing gain `Gp = W/R = T_b/T_c`, `Gp(dB) = 10·log10(W/R)`;
  pole capacity `N ≈ 1 + Gp/(Eb/N0)_req · (1/(1+f)) · (1/v_factor)` with
  other-cell factor `f` and voice activity `v`
- OFDMA: `Δf = 1/T_u`; resource block = `N_sc × N_sym`; user rate =
  `RB_count · N_sc · log2(M) · R_code / T_sym`
- FDD/TDD: duplex spacing, TDD split ratio, guard period `T_g ≥ 2·d/c`

**Controls** — scheme buttons; user count; guard band and guard time; total
bandwidth; frame length; modulation order; duplex mode; play/pause the traffic
animation.

**Why** — "FDMA splits frequency, TDMA splits time" is memorised universally and
understood rarely. What matters in practice is the overhead each scheme charges and
how it scales with user count — and that is an area on a grid, not a sentence.

---

### 5. `am-dsbsc-ssb.html` — AM, DSBSC, SSB and the cost of the carrier
**Category:** modulation

Puts the four analog schemes side by side in time and frequency, with a power pie
that shows how much of the transmitter goes into the carrier versus the sidebands.
A coherent-detector phase-error slider then shows what suppressing the carrier
actually costs at the receiver.

**Formulas**
- AM `s(t) = A_c[1 + m·cos 2πf_m t]·cos 2πf_c t`, `m = A_m/A_c`
- Power `P_t = P_c(1 + m²/2)`; sideband fraction `η = m²/(2 + m²)`
  (33.3% at m = 1); overmodulation for m > 1 → envelope-detector failure
- DSBSC `s(t) = A_c·m(t)·cos 2πf_c t`; coherent detector output `∝ cos φ`;
  frequency error Δf → beat at `cos(2πΔf·t)`
- SSB `s(t) = m(t)·cos ω_c t ∓ m̂(t)·sin ω_c t` (Hilbert); bandwidth `W` vs `2W`
- QAM: two DSBSC in quadrature; crosstalk from phase error `∝ sin φ`
- FDM: `B_total = N·(W + B_guard)`; show the stacked spectrum
- Envelope detector: `RC` time constant bound `1/f_c ≪ RC ≪ 1/W`

**Controls** — scheme buttons (AM / DSBSC / SSB / QAM / FDM); modulation index m
swept through 1 into overmodulation; detector phase error and frequency error;
message tone or two-tone; carrier frequency; number of FDM channels.

**Why** — the carrier in AM carries zero information and eats two-thirds of the
transmitter at best case. That number should be felt, not recited, and the phase
error penalty is precisely why coherent detection costs money and broadcast AM
never bothered.

---

### 6. `ofdm-subcarriers.html` — OFDM subcarriers and the cyclic prefix
**Category:** modulation

Overlays the sinc spectra of N subcarriers so that each peak sits on every other
one's null, then breaks that orthogonality two ways: a frequency offset that
introduces ICI, and a delayed multipath copy that smears into the previous symbol
until the cyclic prefix is switched on. Overlaying a faded channel shows individual
subcarriers dropping into notches.

**Formulas**
- Subcarrier k: `e^(j2πkΔf·t)` with `Δf = 1/T_u`;
  orthogonality `∫₀^{T_u} e^(j2π(k−l)Δf·t) dt = 0` for k ≠ l
- Per-subcarrier spectrum `sinc((f − kΔf)·T_u)`
- Symbol `x(n) = (1/N)·Σ_k X_k·e^(j2πkn/N)` (IFFT)
- CP: ISI-free when `T_cp > τ_max`; efficiency `η = T_u/(T_u + T_cp)`
- Frequency offset ε (normalised to Δf): wanted amplitude `∝ sinc(ε)`,
  ICI power `≈ 1 − sinc²(ε)`; SNR ceiling from ICI
- PAPR `= max|x(n)|² / mean|x(n)|²`; grows roughly as `10·log10(N)` worst case
- Per-subcarrier gain `H_k = Σ a_i·e^(−j2πkΔf·τ_i)` from the same tap model as tool 1

**Controls** — subcarrier count (8–128); CP length; channel delay spread; carrier
frequency offset; subcarrier modulation order; CP on/off toggle; time/frequency
view switch.

**Why** — the cyclic prefix looks like pure wasted overhead until you watch the
delayed copy stop bleeding across the symbol boundary. And a frequency offset of a
few percent of Δf wrecking the constellation is the concrete reason OFDM systems
spend so much on synchronisation.

---

### 7. `cdma-spreading.html` — Spreading, processing gain and the near-far problem
**Category:** cellular

Multiplies a slow data bit by a fast chip sequence, buries the result below the
noise floor, and then animates the correlator integrating it back out over one bit
period — with the wrong code integrating to zero. Turning off power control lets a
near user's signal swamp a far user's, which is the entire reason CDMA needs fast
closed-loop control.

**Formulas**
- Spread `s(t) = d(t)·c(t)`; `Gp = R_c/R_b = T_b/T_c`; `Gp(dB) = 10·log10(R_c/R_b)`
- Despread correlation `z = (1/T_b)∫₀^{T_b} r(t)·c(t) dt`
- Walsh-Hadamard `H_{2n} = [[H_n, H_n],[H_n, −H_n]]`; synchronous cross-correlation 0
- PN (m-sequence) autocorrelation: `1` at zero lag, `−1/N` elsewhere
- Interference suppression `SIR_out = Gp · SIR_in`
- `Eb/N0 = (P_r/R_b) / (N₀ + Σ_{i≠k} P_i/W)`
- Single-cell capacity `N ≈ 1 + (W/R)/(Eb/N0)_req`, with voice activity and
  other-cell factor as multipliers
- Power control dynamic range needed `= 10·log10((d_far/d_near)^n)`

**Controls** — user count; code assignment per user (Walsh vs PN); near/far power
imbalance in dB; power control on/off; chip rate; noise level; step the correlator
integration or run it.

**Why** — processing gain is why a signal sitting 20 dB below the noise floor is
still perfectly readable, and that is unbelievable until you watch the integral
climb. The near-far demonstration explains an 80 dB power-control requirement that
otherwise sounds like an implementation detail.

---

### 8. `eye-diagram-isi.html` — Pulse shaping, ISI and the eye diagram
**Category:** signals

Shapes a random symbol stream with a raised-cosine filter, overlays hundreds of
traces into an eye, and shows the occupied spectrum next to it. Sliding the roll-off
factor trades spectrum width against eye opening and timing tolerance in real time —
the single most concrete bandwidth-versus-robustness trade in the suite.

**Formulas**
- Raised cosine `H(f)`: flat for `|f| ≤ (1−α)/2T`, cosine roll-off to `(1+α)/2T`
- `h(t) = sinc(t/T)·cos(παt/T)/(1 − (2αt/T)²)`, with the `t = ±T/2α` limit handled
- Root raised cosine split tx/rx (matched filter); `RRC ⊗ RRC = RC`
- Occupied bandwidth `B = (1 + α)/T = (1 + α)·R_s`; spectral efficiency
  `R_b/B = log2(M)/(1 + α)` bit/s/Hz
- Nyquist ISI criterion `Σ_n H(f + n/T) = constant`
- Eye metrics: vertical opening at the optimum instant, horizontal opening
  (jitter tolerance), and noise margin `20·log10(opening/noise_rms)`
- Channel distortion: convolve with a one-pole or two-tap channel

**Controls** — roll-off α (0 → 1); symbol rate; modulation order (2/4/8 level);
channel delay spread or extra pole; timing offset; SNR; trace count.

**Why** — α = 0 is spectrally perfect and practically unbuildable; α = 1 is easy and
wastes half the band. The eye is how a working engineer reads that trade off a scope
in one glance, and it is the bridge between the suite's DSP tools and its RF ones.

---

### 9. `erlang-trunking.html` — Erlang B, blocking and trunking efficiency
**Category:** cellular

Turns offered traffic and channel count into a grade of service, and plots the
blocking curve so the strongly non-linear payoff of a large trunk group is visible.
Splitting the same channels into three sectors, or into more cells, shows capacity
being lost to trunking inefficiency even as SIR improves.

**Formulas**
- Offered traffic `A = λ·H` Erlangs; per user `A_u = λ_u·H`; total `A = U·A_u`
- Erlang B `P_b = (A^C/C!) / Σ_{k=0}^{C} A^k/k!`, computed with the stable recursion
  `B(0, A) = 1`, `B(n, A) = A·B(n−1, A) / (n + A·B(n−1, A))`
- Erlang C (queued) `P_delay = A^C/(A^C + C!·(1 − A/C)·Σ_{k=0}^{C−1}A^k/k!)`;
  average delay `= P_delay·H/(C − A)`
- Trunking efficiency: carried traffic per channel `A/C` at fixed `P_b` as C grows
- Users supported `U = A/A_u`
- Channels per cell `= C_total/N` for reuse factor `N`; sectorisation splits each
  cell's trunk by the sector count

**Controls** — channels C; target grade of service; calls per hour per user; mean
call holding time; sector count (1/3/6); reuse factor N; Erlang B vs Erlang C.

**Why** — this is the counterintuitive one. Sectorisation improves SIR by roughly
4.8 dB and *reduces* capacity through trunking loss, and cell splitting has the same
character. The blocking curve is the only way to see why, and the syllabus asks for
Erlang explicitly.

---

### 10. `handover-power-control.html` — Handover, hysteresis and power control
**Category:** cellular

Drives a mobile along a path between two base stations while plotting both received
signal traces, with shadowing noise on top, and marks every handover event. Turning
hysteresis down produces visible ping-pong; turning it up produces a visible dropped
call at the cell edge. A second mode closes the power-control loop and shows the
interference floor everyone else sees fall as a result.

**Formulas**
- `P_r(d) = P_t + G_t + G_r − [PL(d₀) + 10n·log10(d/d₀)] + X_σ`
  with `X_σ ~ N(0, σ²)` log-normal shadowing
- Handover trigger: switch when `P_r,new > P_r,old + H` sustained for dwell `T`
- Ping-pong rate as a function of H, σ, speed v and the dwell timer
- Drop condition `P_r < P_min` for longer than the drop timer
- Cell splitting: `P_t ∝ R^n`, so halving R cuts required power by `10n·log10(2)` dB
  (12 dB at n = 4)
- Sectorisation: co-channel interferers 6 → 2 for 120°, SIR gain `10·log10(3)` = 4.77 dB
- Closed-loop power control: step size, update rate, dynamic range;
  `SIR = P_r / Σ P_interferers`
- Reuse SIR link back to `cellular-reuse.html`: `SIR = (1/i₀)·(√(3N))^n`

**Controls** — mobile speed and route (draggable); hysteresis margin; dwell timer;
shadowing σ; path loss exponent n; sector count; power control on/off with step size.

**Why** — hysteresis is a genuinely two-sided trade: too little and the mobile
ping-pongs itself to death on signalling load, too much and it holds a dying link
past the point of no return. Only the animated crossing traces with real shadowing
noise make that legible, and this is the largest untouched block of the cellular
syllabus.

---

### 11. `impedance-matching.html` — Impedance, VSWR and the Smith chart
**Category:** antennas

Lets the load impedance be dragged around a Smith chart while VSWR, return loss and
mismatch loss update live, then adds series and shunt components one at a time and
draws the trace walking to the centre. Adding transmission line rotates the point
around the chart, which is the fact the chart exists to make obvious.

**Formulas**
- `Γ = (Z_L − Z₀)/(Z_L + Z₀)`; normalised `z = Z/Z₀`
- `VSWR = (1 + |Γ|)/(1 − |Γ|)`; return loss `RL = −20·log10|Γ|` dB
- Mismatch loss `= −10·log10(1 − |Γ|²)` dB; delivered power fraction `1 − |Γ|²`
- Smith chart: constant-r circles centre `(r/(1+r), 0)` radius `1/(1+r)`;
  constant-x arcs centre `(1, 1/x)` radius `|1/x|`
- Line rotation `Γ(l) = Γ_L·e^(−j2βl)`, `β = 2π/λ`; one full turn per `λ/2`
- Series reactance moves along constant r; shunt susceptance along constant g
  (admittance chart, i.e. Γ → −Γ)
- L-network `Q = √(R_high/R_low − 1)`; matched bandwidth `≈ f₀/Q`
- Component reactances `X_L = 2πfL`, `X_C = −1/(2πfC)` — so retune with frequency

**Controls** — drag the load point (or enter R + jX); Z₀ (50/75 Ω); frequency;
transmission line length in wavelengths; add/remove series-L, series-C, shunt-L,
shunt-C; frequency sweep to show match bandwidth.

**Why** — the Smith chart is a conformal map that is opaque as algebra and obvious
as a drag. Two numbers every RF engineer needs permanently calibrated live here:
VSWR 2:1 costs only 0.5 dB (so stop panicking), and a narrow match falls apart
across the band (so start panicking about Q).

---

### 12. `ber-vs-ebn0.html` — Bit error rate against Eb/N0
**Category:** receivers

Plots BER curves for the common schemes on a log axis and lets the channel switch
between AWGN, Rician and Rayleigh, so the cliff turns into a slope. Adding diversity
branches steepens the slope back, which is the clearest possible statement of what
diversity buys.

**Formulas**
- `Q(x) = 0.5·erfc(x/√2)`; erfc via Abramowitz–Stegun 7.1.26 (7-digit form)
- BPSK and QPSK `P_b = Q(√(2E_b/N₀))`
- M-PSK `P_s ≈ 2Q(√(2E_s/N₀)·sin(π/M))`, Gray-coded `P_b ≈ P_s/log2 M`
- M-QAM `P_s = 4(1 − 1/√M)·Q(√(3E_s/((M−1)N₀)))`
- Non-coherent FSK `P_b = 0.5·e^(−E_b/2N₀)`; DPSK `P_b = 0.5·e^(−E_b/N₀)`
- Rayleigh flat fading, BPSK: `P_b = 0.5(1 − √(γ̄/(1 + γ̄)))`, `γ̄ = E_b/N₀ mean`
- Diversity order L: `P_b ∝ γ̄^(−L)` — plot L = 1, 2, 4
- `E_s/N₀ = (E_b/N₀)·log2 M`; `SNR = (E_b/N₀)·(R_b/B)`
- Required margin = `E_b/N₀` at target BER minus the AWGN value

**Controls** — scheme; channel (AWGN / Rician K / Rayleigh); diversity branches;
coding gain offset in dB; target BER marker; implementation loss.

**Why** — the AWGN curve is a cliff and the Rayleigh curve is a shallow slope, and
that one picture explains why fading links need 20–30 dB more margin or diversity
rather than more transmit power. It is the quantitative partner to the existing
IQ constellation tool, which shows noise but not its cost.

---

### 13. `polarisation-mismatch.html` — Polarisation, tilt and axial ratio
**Category:** antennas

Animates the tip of the E-field vector tracing a line, an ellipse or a circle as the
amplitude ratio and phase difference between two orthogonal components are changed,
and puts a tiltable receive antenna next to it with the polarisation loss factor
computed live. Cross-polarising a linear pair drives the loss off the scale.

**Formulas**
- `E_x = A·cos(ωt)`, `E_y = B·cos(ωt + δ)`; δ = 0 linear, δ = ±90° with A = B circular
- Ellipse tilt `τ = 0.5·atan2(2AB·cos δ, A² − B²)`
- Axial ratio `AR = major/minor`; `AR_dB = 20·log10(AR)`; `AR = 1` (0 dB) circular
- Polarisation loss factor `PLF = |ρ̂_wave · ρ̂_antenna*|²`; `PLF_dB = 10·log10(PLF)`
- Linear-to-linear `PLF = cos²ψ` for tilt ψ
- Linear-to-circular `PLF = 0.5` (3.0 dB), always
- Circular co-sense vs cross-sense: `PLF = ((AR₁·AR₂ + 1)² ) / ((AR₁²+1)(AR₂²+1))`
  form for the co-polar case, and the counter-rotating case for cross
- Cross-polar discrimination `XPD = 10·log10(P_co/P_cross)`

**Controls** — amplitude ratio A/B; phase difference δ (animates the ellipse);
sense of rotation; receive antenna tilt ψ; receive antenna type (linear / RHCP /
LHCP); freeze or run the vector animation.

**Why** — 3 dB lost permanently on a linear-to-circular link and effectively
infinite loss on a cross-polarised pair are two of the most commonly forgotten terms
in a link budget. Watching the field vector rotate is what makes them stick, and it
connects directly to the existing `link-budget.html` and `antenna-basics.html`.

---

### 14. `filter-selectivity.html` — Selectivity, blocking and adjacent channels
**Category:** receivers

Draws a receiver filter response with a wanted signal in the passband and a strong
interferer sitting a channel or two away, then shows what survives to the mixer.
Raising the filter order sharpens rejection and lengthens group delay, which is the
trade a static Bode plot completely hides.

**Formulas**
- Butterworth `|H(f)|² = 1/(1 + (f/f_c)^(2n))`
- Chebyshev I `|H(f)|² = 1/(1 + ε²T_n²(f/f_c))`, `ε² = 10^(ripple_dB/10) − 1`
- Bandpass transform `f → (f/f₀ − f₀/f)·(f₀/BW)`
- Shape factor `SF = BW_60dB/BW_3dB`; `Q = f₀/BW_3dB`
- Group delay `τ_g = −dφ/dω`, computed numerically from the phase response
- Blocking: interferer at the mixer `= P_int − R(Δf)`; desense when this approaches
  the 1 dB compression point `P_1dB`
- Adjacent channel selectivity `ACS = P_int,max − P_wanted` at the target BER;
  protection ratio `C/I_req`
- Cascaded stages: total rejection `= Σ R_i(dB)`; total noise contribution via Friis

**Controls** — filter type (Butterworth / Chebyshev); order 2–10; centre frequency
and bandwidth; passband ripple; interferer offset and level; wanted signal level;
receiver P1dB; group delay view toggle.

**Why** — selectivity is a receiver's only defence against the transmitter next
door, and it is the missing front end of the existing `superhet-image.html`, which
already assumes an image filter exists without ever showing what one costs. The
order-versus-group-delay trade is a real design decision for anyone touching a
modem.

---

## 3. Build order

**Phase 1 (biggest syllabus holes, highest teaching value):** 1 multipath-fading,
2 noise-figure-sensitivity, 3 fm-bessel-spectrum, 4 multiple-access.

**Phase 2 (completes the syllabus):** 5 am-dsbsc-ssb, 6 ofdm-subcarriers,
7 cdma-spreading, 9 erlang-trunking, 10 handover-power-control.

**Phase 3 (rounds out the engineer, not strictly on the syllabus):**
8 eye-diagram-isi, 11 impedance-matching, 12 ber-vs-ebn0,
13 polarisation-mismatch, 14 filter-selectivity.

Shared code worth writing once and copying (the suite has no build step, so copy is
correct): the `Q`/`erfc` pair (tools 1, 12), the tapped-delay-line channel and its
`H(f)` (tools 1, 6, 8), and the Bessel `J_n` series (tool 3 only, but keep it clean).

A caution on `STYLE.md`: it says "formulas must match the course notes in
`.research/*.md`", and no course notes currently exist in that folder — only
`STYLE.md` and this file. Every formula above is standard textbook material stated
from domain knowledge, not read out of the learner's notes. Before implementation,
either drop the course notes into `.research/` or spot-check each tool's constants
against the module handbook — particularly the coherence bandwidth constant
(1/5σ_τ vs 1/50σ_τ), the CDMA capacity form, and the Erlang B convention.

---

## 4. Suite structure: hub plus seven category pages

### Layout

```
index.html                    hub — seven category cards, nothing else
topics/signals.html           one page per category
topics/modulation.html
topics/antennas.html
topics/propagation.html
topics/receivers.html
topics/geolocation.html
topics/cellular.html
tools/*.html                  unchanged, 29 files
```

`topics/` rather than the repo root, because `tools/modulation.html` already exists
and a root-level `modulation.html` next to it would be a permanent source of
confusion. Tool files stay exactly where they are, so every existing link and
bookmark keeps working.

Each tool's back-link changes from `../index.html` to `../topics/<category>.html`,
and each category page carries `← all topics` pointing at `../index.html`. Two
clicks from anywhere to anywhere.

### Category order and descriptions

Ordered as a single narrative: what a signal is, how you load it, how you launch it,
what happens on the way, how you recover it, what it tells you, and how a whole
network shares it.

| # | Category | One-line description | Tools |
|---|---|---|---|
| 1 | **Signals** | What a waveform is actually made of, and what sampling and filtering do to it. | fourier-series, epicycles, sampling-aliasing, **eye-diagram-isi** |
| 2 | **Modulation** | How information is loaded onto a carrier, and what that costs in bandwidth and power. | modulation, iq-constellation, **fm-bessel-spectrum**, **am-dsbsc-ssb**, **ofdm-subcarriers** |
| 3 | **Antennas** | How a current becomes a wave with a shape, a polarisation and an impedance. | antenna-basics, phased-array, **impedance-matching**, **polarisation-mismatch** |
| 4 | **Propagation** | What the path between two antennas does to the signal on the way across. | radio-propagation, fresnel-clearance, link-budget, **multipath-fading** |
| 5 | **Receivers** | How a weak wanted signal survives noise, strong neighbours and imperfect mixers. | superhet-image, **noise-figure-sensitivity**, **ber-vs-ebn0**, **filter-selectivity** |
| 6 | **Geolocation** | What phase and time of arrival tell you about where a transmitter is standing. | phase-interferometry, aoa-triangulation, tdoa |
| 7 | **Cellular** | How one spectrum allocation is shared by many users across many cells. | cellular-reuse, **multiple-access**, **cdma-spreading**, **erlang-trunking**, **handover-power-control** |

Bold entries are new. Final distribution 4 / 5 / 4 / 4 / 4 / 3 / 5 = 29 tools — no
category is thin enough to feel like an afterthought or fat enough to need scrolling.

### Two placement calls worth stating

- **`phase-interferometry` sits in Geolocation, not Antennas.** It shares hardware
  with `phased-array` but answers the opposite question — the array is transmitting
  a beam, the interferometer is inferring a bearing. Group by the question, not the
  hardware, and cross-link the two pages.
- **`multiple-access` and `cdma-spreading` sit in Cellular, not Modulation.** They
  are about sharing a finite resource among users, which is a network problem;
  OFDM's waveform is a modulation problem and stays in Modulation. Cross-link
  `ofdm-subcarriers` from the Cellular page.

### Hub page content

Keep it to one screen. A two-sentence framing paragraph, then seven cards, each with
the category name, the one-line description above, the tool count, and the two or
three headline tool names as plain text (not links — the card is the link). Do not
list all 29 tools on the hub; that is the flat index the reorganisation is meant to
replace. Same `:root` token set and dark-mode override as every tool, so the hub
does not read as a different site.

Category pages get slightly more room: the same header, a short paragraph on what
the category is for and roughly what order to work through it in, then one card per
tool with a one-line "what it teaches" (the `README.md` table already has good
copy for the existing 15 — reuse it verbatim).

`README.md` should keep a single flat table of all 29 with a category column. A repo
readme is a reference, not a curriculum, and grouping it into seven subsections just
makes it harder to Ctrl-F.
