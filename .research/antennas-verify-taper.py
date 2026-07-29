import numpy as np
from scipy.optimize import brentq

# Continuous line source length L, illumination g(x), x in [-1/2,1/2] (units of L)
# F(u) = int g(x) cos(2 pi u x) dx ,  u = (L/lam) sin(theta)
X = np.linspace(-0.5, 0.5, 4001)

def make_F(g):
    gx = g(X)
    def F(u):
        u = np.atleast_1d(np.asarray(u, float))
        out = np.empty(u.size)
        for i in range(0, u.size, 500):
            ch = u[i:i+500]
            out[i:i+500] = np.trapezoid(gx*np.cos(2*np.pi*np.outer(ch, X)), X, axis=1)
        return np.abs(out)
    return F, gx

tapers = {
 "uniform":            lambda x: np.ones_like(x),
 "cosine cos(pi x)":   lambda x: np.cos(np.pi*x),
 "cosine^2 (Hann)":    lambda x: np.cos(np.pi*x)**2,
 "cosine^3":           lambda x: np.cos(np.pi*x)**3,
 "triangular":         lambda x: 1-2*np.abs(x),
 "Hamming (0.54)":     lambda x: 0.54+0.46*np.cos(2*np.pi*x),
 "cos on -10dB ped":   lambda x: 0.3162+(1-0.3162)*np.cos(np.pi*x),
}

print(f"{'taper':20s} {'SLL dB':>8s} {'HPBW coef (deg*lam/L)':>22s} {'broaden':>8s} {'eta_ap':>7s} {'taper loss dB':>13s}")
base = None
uu = np.linspace(0.4, 8.0, 12000)
for name, g in tapers.items():
    F, gx = make_F(g)
    F0 = F(0.0)[0]
    u3 = brentq(lambda u: (F(u)[0]/F0)**2 - 0.5, 1e-9, 3.0)
    hp = np.degrees(2*u3)
    if base is None: base = hp
    v = F(uu)/F0
    pk = [i for i in range(1, len(v)-1) if v[i] > v[i-1] and v[i] > v[i+1]]
    sll = 20*np.log10(v[pk[0]])
    eta = np.trapezoid(gx, X)**2 / np.trapezoid(gx**2, X)
    print(f"{name:20s} {sll:8.2f} {hp:22.3f} {hp/base:8.3f} {eta:7.4f} {-10*np.log10(eta):13.2f}")
print("# D = (4 pi A / lam^2) * eta_ap ; HPBW_deg = coef * lam/L")

print("\n=== DISCRETE ARRAY WINDOWS (N=32, d=lam/2) ===")
from scipy.signal.windows import chebwin, taylor
N, dl = 32, 0.5
th = np.linspace(-np.pi/2, np.pi/2, 200001)
n = np.arange(N)-(N-1)/2
S = np.exp(1j*2*np.pi*dl*np.outer(n, np.sin(th)))
wins = {"uniform": np.ones(N), "Hann": np.hanning(N+2)[1:-1], "Hamming": np.hamming(N),
        "Blackman": np.blackman(N), "Chebyshev -30dB": chebwin(N,30),
        "Taylor -30dB nbar=5": taylor(N, nbar=5, sll=30)}
base2 = None
for name, w in wins.items():
    AF = np.abs(w @ S); AF /= AF.max()
    P = 20*np.log10(np.maximum(AF, 1e-12)); i0 = int(np.argmax(AF))
    l = np.where(P[:i0] < -3)[0][-1]; r = i0 + np.where(P[i0:] < -3)[0][0]
    hp = np.degrees(th[r]-th[l])
    if base2 is None: base2 = hp
    pk = [i for i in range(1,len(P)-1) if P[i]>P[i-1] and P[i]>P[i+1] and abs(i-i0)>20]
    eta = w.sum()**2/(N*np.sum(w**2))
    print(f"{name:20s} SLL={max(P[i] for i in pk):7.2f} dB  HPBW={hp:6.3f} deg  "
          f"broaden={hp/base2:.3f}  taper loss={-10*np.log10(eta):5.2f} dB")
