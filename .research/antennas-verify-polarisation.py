import numpy as np
INF = 1e12  # stands in for linear polarisation (AR -> infinity)

def PLF(AR1, AR2, dtau_deg):
    """Balanis/Milligan polarisation loss factor. AR linear >=1; negate one AR for
    opposite rotational sense. dtau = tilt-angle difference (deg)."""
    t = np.radians(2*dtau_deg)
    return 0.5 + (4*AR1*AR2 + (AR1**2-1)*(AR2**2-1)*np.cos(t)) / (2*(AR1**2+1)*(AR2**2+1))

def dB(x): return -99.0 if x <= 0 else 10*np.log10(x)

print("--- sanity checks ---")
print("LP/LP aligned      :", PLF(INF,INF,0),   dB(PLF(INF,INF,0)))
print("LP/LP 45 deg       :", PLF(INF,INF,45),  dB(PLF(INF,INF,45)))
print("LP/LP 90 deg       :", PLF(INF,INF,90),  dB(PLF(INF,INF,90)))
print("LP/LP 30 deg       :", PLF(INF,INF,30),  dB(PLF(INF,INF,30)))
print("LP/LP 60 deg       :", PLF(INF,INF,60),  dB(PLF(INF,INF,60)))
print("CP/LP              :", PLF(1,INF,0),     dB(PLF(1,INF,0)))
print("CP/CP same sense   :", PLF(1,1,0),       dB(PLF(1,1,0)))
print("CP/CP opp sense    :", PLF(1,-1,0),      dB(PLF(1,-1,0)))

print("\n--- imperfect CP antenna receiving a PURE LINEAR wave (ripple about 3 dB) ---")
for ar_db in (0,0.5,1,2,3,6):
    a = 10**(ar_db/20)
    best  = PLF(a, INF, 0)     # wave aligned with ellipse major axis
    worst = PLF(a, INF, 90)    # aligned with minor axis
    print(f"AR={ar_db:4.1f} dB (={a:.4f}): loss {dB(best):+.3f} dB to {dB(worst):+.3f} dB "
          f"(mean 3.01, ripple +/-{(dB(best)-dB(worst))/2:.3f} dB)")

print("\n--- two nominally-CP antennas, both AR = X dB, SAME sense ---")
for ar_db in (0,0.5,1,2,3,6):
    a = 10**(ar_db/20)
    print(f"AR={ar_db:4.1f} dB: best {dB(PLF(a,a,0)):+.3f} dB, worst {dB(PLF(a,a,90)):+.3f} dB")

print("\n--- cross-pol discrimination: LP wave vs LP antenna at tilt ---")
for t in (0,10,20,30,45,60,80,85,89,90):
    print(f"  tilt {t:3d} deg: PLF={np.cos(np.radians(t))**2:.6f} -> {dB(np.cos(np.radians(t))**2):+.3f} dB")

print("\n--- axial ratio <-> ellipse ---")
for ar_db in (0,1,3,6,10,20,40):
    a=10**(ar_db/20); print(f"AR={ar_db:4.1f} dB = {a:.4f} linear (major/minor axis ratio)")
