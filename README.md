# Engineering visualisation tools

Small, self-contained interactive simulators for building engineering intuition. Each tool is a single HTML file with no dependencies — open it in any browser, or visit the hosted version via GitHub Pages.

## Tools

| Tool | What it teaches |
|---|---|
| [4-antenna phase interferometry](tools/phase-interferometry.html) | Direction finding with an unequally spaced array: phase differences, wrapping, ambiguity resolution, and a working phases-to-angle solver |
| [Phased-array beam pattern](tools/phased-array.html) | The reverse direction: phase-steering a beam, beamwidth vs aperture, sidelobes and grating lobes |
| [Fourier series builder](tools/fourier-series.html) | Stack sine harmonics into square, triangle, and sawtooth waves; amplitude spectrum, convergence, and the Gibbs effect |
| [Spinning circles draw your wave](tools/epicycles.html) | The Fourier series as rotating circles (epicycles) tracing time-domain shapes |
| [Sampling and aliasing](tools/sampling-aliasing.html) | The Nyquist rule: undersample a sine and a low-frequency ghost fits the same samples |
| [Modulation playground](tools/modulation.html) | AM, FM, OOK, FSK, BPSK, QPSK side by side — amplitude, frequency, and phase as information carriers |
| [IQ constellation explorer](tools/iq-constellation.html) | BPSK to 16QAM constellations under noise, phase offset, and frequency offset |
| [AoA triangulation](tools/aoa-triangulation.html) | Two to five bearing lines cross-fixing an emitter, with bearing-error wedges |
| [TDoA geolocation](tools/tdoa.html) | Three to five time-synced sites, hyperbolic position curves crossing at the emitter |
| [Antenna basics](tools/antenna-basics.html) | Dipole, monopole, patch, Yagi, horn, dish and array: physical form, radiation, beam pattern, gain, HPBW, front-to-back, and mechanical vs electrical boresight |
| [HF, VHF and how radio waves travel](tools/radio-propagation.html) | Ground wave, sky wave, and line of sight against a live day/night ionosphere with skip zones and the MUF |

## Run locally

Open `index.html` (or any file in `tools/`) in a browser. That's it.
