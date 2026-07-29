import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

d = np.degrees

def hpbw(F, th_peak, lo, hi):
    g = lambda t: F(t) - 0.5
    a = brentq(g, lo, th_peak); b = brentq(g, th_peak, hi)
    return d(b - a), d(a), d(b)

print("=== HERTZIAN / SHORT DIPOLE  (power ~ sin^2 th) ===")
Fh = lambda t: np.sin(t)**2
D_h = 2/quad(lambda t: Fh(t)*np.sin(t), 0, np.pi)[0]
print("D =", D_h, "->", 10*np.log10(D_h), "dBi")
print("HPBW (deg, edges) =", hpbw(Fh, np.pi/2, 1e-6, np.pi-1e-6))

print("\n=== HALF-WAVE DIPOLE ===")
def Fd(t):
    s = np.sin(t)
    return 0.0 if abs(s) < 1e-12 else (np.cos(np.pi/2*np.cos(t))/s)**2
D_d = 2/quad(lambda t: Fd(t)*np.sin(t), 0, np.pi)[0]
print("D =", D_d, "->", 10*np.log10(D_d), "dBi")
print("HPBW (deg, edges) =", hpbw(Fd, np.pi/2, 1e-6, np.pi-1e-6))
print("monopole D = 2*D_d =", 2*D_d, "->", 10*np.log10(2*D_d), "dBi")

print("\n=== UNIFORM LINE SOURCE  (sin u / u)^2,  u = (pi L/lam) sin th ===")
u3 = brentq(lambda u: (np.sin(u)/u)**2 - 0.5, 1e-9, np.pi)
k = 2*u3/np.pi
print("u_3dB =", u3, "  HPBW ~", k, "*lam/L rad =", d(k), "*lam/L deg")
us = brentq(lambda u: np.tan(u)-u, np.pi+1e-9, 1.5*np.pi-1e-9)
print("1st sidelobe at u =", us, "  level =", 10*np.log10((np.sin(us)/us)**2), "dB")
print("2nd sidelobe u=", brentq(lambda u: np.tan(u)-u, 2*np.pi+1e-9, 2.5*np.pi-1e-9),
      "level =", 10*np.log10((np.sin(brentq(lambda u: np.tan(u)-u, 2*np.pi+1e-9, 2.5*np.pi-1e-9))/brentq(lambda u: np.tan(u)-u, 2*np.pi+1e-9, 2.5*np.pi-1e-9))**2), "dB")

print("\n=== N-ELEMENT ULA  AF = sin(N psi/2)/(N sin(psi/2)) ===")
def AF2(psi, N):
    den = N*np.sin(psi/2)
    return 1.0 if abs(den) < 1e-12 else (np.sin(N*psi/2)/den)**2
for N in (2,4,8,16,32,64):
    p3 = brentq(lambda p: AF2(p,N)-0.5, 1e-9, 2*np.pi/N)
    ps = np.linspace(2*np.pi/N*1.0001, 3*np.pi/N, 40000)
    v = np.array([AF2(p,N) for p in ps]); i = int(np.argmax(v))
    print(f"N={N:3d} psi3={p3:.6f} HPBW(d=lam/2,bs)={2*d(np.arcsin(p3/np.pi)):8.3f} deg"
          f"  0.886lam/(Nd)={d(0.886/(N*0.5)):8.3f}  1stSLL={10*np.log10(v[i]):.3f} dB")

print("\n=== SCAN BROADENING (N=16, d=lam/2) ===")
N=16; dl=0.5
p3 = brentq(lambda p: AF2(p,N)-0.5, 1e-9, 2*np.pi/N)
bw0 = 2*d(np.arcsin(p3/(2*np.pi*dl)))
print("broadside HPBW =", bw0)
for ts in (0,30,45,60):
    t=np.radians(ts)
    f=lambda th: AF2(2*np.pi*dl*(np.sin(th)-np.sin(t)),N)-0.5
    a=brentq(f, t-0.6, t); b=brentq(f, t, t+0.8)
    print(f"scan={ts:2d}: exact={d(b-a):7.3f}  bw0/cos={bw0/np.cos(t):7.3f}  ratio={d(b-a)/(bw0/np.cos(t)):.4f}")

print("\n=== GRATING LOBES ===")
for dl in (0.5,0.6,0.7,1.0,1.5):
    x = 1/dl - 1
    print(f"d/lam={dl}: GL-free max scan = {'none (>=90 deg, no GL in vis. space)' if x>=1 else f'{d(np.arcsin(x)):.2f} deg'}")
for ts in (0,30,45,60,90):
    print(f"scan {ts:2d} deg -> d/lam < {1/(1+np.sin(np.radians(ts))):.4f}")

print("\n=== VSWR TABLE ===")
print("VSWR |G|      RL(dB)   %refl   ML(dB)")
for v in (1.0,1.5,2.0,3.0,5.0,10.0):
    g=(v-1)/(v+1); rl = float('inf') if g==0 else -20*np.log10(g)
    print(f"{v:5.1f} {g:.4f}  {rl:8.3f} {100*g*g:7.2f}  {-10*np.log10(1-g*g):.4f}")

print("\n=== POLARISATION ===")
for a in (0,30,45,60,90):
    p=np.cos(np.radians(a))**2
    print(f"tilt {a:2d}: PLF={p:.4f} -> {(-99 if p==0 else 10*np.log10(p)):.3f} dB")
print("lin<->circ PLF=0.5 ->", 10*np.log10(0.5), "dB")
for ar_db in (0,1,3,6):
    r=10**(ar_db/20); e=2*r/(1+r*r)
    print(f"AR={ar_db} dB: CP-CP same sense best/worst = {10*np.log10(0.5*(1+e)):+.3f} / {10*np.log10(0.5*(1-e)):+.3f} dB rel. isotropic-pol")

print("\n=== G = 4 pi Ae / lam^2 (course table) ===")
for lam,lab in ((0.3,'30cm'),(0.003,'3mm')): print(lab,"4pi/lam^2 =",4*np.pi/lam**2)
for n,G in (("isotropic",1.0),("inf dipole/loop",1.5),("half-wave dipole",1.64),
            ("horn",349),("parabolic",244),("turnstile",1.15)):
    print(f"  {n:17s} G={G:7.2f} {10*np.log10(G):7.2f} dBi  Ae(30cm)={G*0.09/(4*np.pi):.4g}  Ae(3mm)={G*9e-6/(4*np.pi):.4g}")
print("2 m dish 56% eff: Ae =", 0.56*np.pi*1.0**2, " G@1GHz =", 4*np.pi*(0.56*np.pi)/0.09,
      "=", 10*np.log10(4*np.pi*(0.56*np.pi)/0.09), "dBi")
print("horn Ae from G=349:", 349*0.09/(4*np.pi), " G@100GHz for same Ae:", 4*np.pi*(349*0.09/(4*np.pi))/9e-6)
print("parab Ae from G=244:", 244*0.09/(4*np.pi), " G@100GHz:", 4*np.pi*(244*0.09/(4*np.pi))/9e-6)

print("\n=== DISH HPBW ===")
print("70*lam/D, lam=0.3/F_GHz -> k/(F*D), k =", 70*0.3)
print("course 22/(F*D) == ", 22/0.3, "* lam/D")
for F,D in ((1,2),(6,1.2),(12,0.6),(14,3.0)):
    print(f"F={F} D={D}: 22/(FD)={22/(F*D):.3f}  70lam/D={70*(0.3/F)/D:.3f}  21/(FD)={21/(F*D):.3f}")

print("\n=== UNIFORM CIRCULAR APERTURE (dish): F = 2 J1(u)/u ===")
from scipy.special import j1, jn_zeros
from scipy.optimize import minimize_scalar
u3c = brentq(lambda u: (2*j1(u)/u)**2 - 0.5, 1e-9, 2.0)
print("u3 =", u3c, " HPBW =", 2*u3c/np.pi, "lam/D rad =", d(2*u3c/np.pi), "lam/D deg")
z = jn_zeros(1, 3)
print("first null u =", z[0], "-> sin th =", z[0]/np.pi, "lam/D")
r = minimize_scalar(lambda u: -(2*j1(u)/u)**2, bounds=(z[0], z[1]), method='bounded')
print("first sidelobe u =", r.x, " level =", 10*np.log10((2*j1(r.x)/r.x)**2), "dB")
