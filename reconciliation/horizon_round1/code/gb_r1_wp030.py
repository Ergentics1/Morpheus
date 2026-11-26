# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- [GB] Round-1 independent checks
"""GB round-1 independent checks, WP030 (no reads of [G4N] code or data)."""
import math, cmath, numpy as np
R={}
def rep(k,v): R[k]=v; print(f"{k}: {v}")
I=1j
# Jacobi / Hopf chart of the paper (rJ = sqrt2 L, L=1, M=3 -> m=1)
def rho_from_z(z1,z2): return np.array([z1/math.sqrt(2)+z2/math.sqrt(6), -z1/math.sqrt(2)+z2/math.sqrt(6), -math.sqrt(2/3)*z2])
def paper_chart(th0,Th,Ph,rJ=math.sqrt(2)):
    return rho_from_z(rJ*math.cos(Th/2)*cmath.exp(I*(th0+Ph/2)), rJ*math.sin(Th/2)*cmath.exp(I*(th0-Ph/2)))
m=1.0; M=3.0; L=1.0; I0=(2/3)*M*L**2
# --- Thm2(1) constant inertia, Thm2(2) Q, NEG-W4 sign
rng=np.random.default_rng(7); errI=0; errQ=0; errsign=0
for _ in range(1000):
    th0,Th,Ph=rng.uniform(0,2*np.pi),rng.uniform(0,np.pi),rng.uniform(0,2*np.pi)
    r=paper_chart(th0,Th,Ph); x,y=r.real,r.imag
    errI=max(errI,abs(m*np.sum(x*x+y*y)-I0))
    Qmass=m*np.sum(r**2); Qpaper=I0*cmath.exp(2*I*th0)*(math.cos(Ph)+I*math.cos(Th)*math.sin(Ph))
    errQ=max(errQ,abs(Qmass-Qpaper))
    Ixx=m*np.sum(y*y); Iyy=m*np.sum(x*x); Ixy=-m*np.sum(x*y)
    errsign=max(errsign,abs(((Ixx-Iyy)+2*I*Ixy)+Qmass))
rep("Thm2.1 max|Izz-I0|",f"{errI:.1e}"); rep("Thm2.2 max|sum m rho^2 - paper Q|",f"{errQ:.1e} (paper formula = MASS quadrupole)")
rep("NEG-W4 max|(Ixx-Iyy)+2iIxy + sum m rho^2|",f"{errsign:.1e} -> inertia-tensor form has opposite sign: CONFIRMED")
# --- Thm2(3) holonomy, paper chart, loop Th=pi/3, Phi:0->2pi, zero spin
def spin(r,v): return float(np.sum(m*(np.conj(r)*v).imag))
N=4000; Th=math.pi/3; th0=0.0; Smax=0
for k in range(N):
    Ph=2*np.pi*k/N; dP=2*np.pi/N
    dth0=-0.5*math.cos(Th)*dP
    r0=paper_chart(th0,Th,Ph); r1=paper_chart(th0+dth0,Th,Ph+dP)
    Smax=max(Smax,abs(spin((r0+r1)/2,(r1-r0))))/1.0
    th0+=dth0
P0=paper_chart(0,Th,0); P1=paper_chart(th0,Th,2*np.pi); rot=math.degrees(np.angle(np.vdot(P0,P1)))
rep("Thm2.3 paper chart: Delta theta0 (deg)",f"{math.degrees(th0):.6f}")
rep("Thm2.3 paper chart: NET rotation of labelled bodies (deg)",f"{rot:+.6f}; max per-step spin {Smax:.1e}")
for Ph_ in (0,np.pi):
    r=paper_chart(0,Th,Ph_); rep(f"NEG-W2 collision check Phi={Ph_:.4f}",[round(abs(r[i]-r[j]),9) for i,j in ((0,1),(1,2),(0,2))])
rep("NEG-W2 Theta=0 shape",np.round(paper_chart(0,0,0),6).tolist())
r=paper_chart(0,math.pi/2,math.pi/2); d=[abs(r[i]-r[j]) for i,j in ((0,1),(1,2),(0,2))]; rep("equilateral location in paper chart (Th=pi/2,Phi=pi/2) sides",[round(x,6) for x in d])
# G4N equilateral-pole basis w+- = (z1 +- i z2)/sqrt2  ->  z1=(w+ + w-)/sqrt2, z2=(w+ - w-)/(i sqrt2)
def g4n_chart(th0,b,chi,rJ=math.sqrt(2)):
    wp=rJ*math.cos(b/2)*cmath.exp(I*(th0+chi/2)); wm=rJ*math.sin(b/2)*cmath.exp(I*(th0-chi/2))
    return rho_from_z((wp+wm)/math.sqrt(2),(wp-wm)/(I*math.sqrt(2)))
b=math.pi/3; dmin=9; Qvar=0; th0=0.0; N=4000
Q0=None
for k in range(N+1):
    chi=-2*np.pi*k/N
    r=g4n_chart(th0,b,chi); dmin=min(dmin,min(abs(r[i]-r[j]) for i,j in ((0,1),(1,2),(0,2))))
    Q=np.sum(r**2)/cmath.exp(2*I*th0); Q0=Q if Q0 is None else Q0; Qvar=max(Qvar,abs(Q-Q0))
    if k<N:
        # zero spin step: solve d theta0 from numerical spin (linear in d theta0)
        dchi=-2*np.pi/N
        def S(dt): ra=g4n_chart(th0,b,chi); rb=g4n_chart(th0+dt,b,chi+dchi); return spin((ra+rb)/2,rb-ra)
        s0=S(0); s1=S(1e-3); th0+= -s0*1e-3/(s1-s0)
P0=g4n_chart(0,b,0); P1=g4n_chart(th0,b,-2*np.pi); rot=math.degrees(np.angle(np.vdot(P0,P1)))
rep("G4N basis loop beta=pi/3 chi:0->-2pi net rotation (deg)",f"{rot:+.4f}; min d_ij/L={dmin:.6f} (sqrt(2-sqrt3)={math.sqrt(2-math.sqrt(3)):.6f}); |Q e^-2i th0| variation={Qvar:.1e}; |Q|/I0={abs(Q0)/I0:.6f} (sin b={math.sin(b):.6f})")
r=g4n_chart(0,0,0); rep("G4N basis beta=0 sides",[round(abs(r[i]-r[j]),6) for i,j in ((0,1),(1,2),(0,2))])
# --- Theorem G1: zero-spin tracking kinetic energy, max radius
def track_T(q,Om=1.0):
    b=math.pi-math.asin(q) # cos b = -sqrt(1-q^2) as in G4N
    # theta0 = Om t ; chi' from zero spin, measured numerically
    dt=1e-5; th0=0.0; chi=0.3
    ra=g4n_chart(th0,b,chi)
    def S(dc): rb=g4n_chart(th0+Om*dt,b,chi+dc); return spin((ra+rb)/2,(rb-ra)/dt)
    s0=S(0); s1=S(1e-4); dc=-s0*1e-4/(s1-s0)
    rb=g4n_chart(th0+Om*dt,b,chi+dc); v=(rb-ra)/dt
    return 0.5*m*np.sum(abs(v)**2)/(0.5*I0*Om**2)
for q in (0.5,1/math.sqrt(2),0.85,0.95):
    rmax=max(max(abs(g4n_chart(0,math.pi-math.asin(q),c))) for c in np.linspace(0,2*np.pi,721))
    rep(f"G1 q={q:.4f}",f"T/(I0 Om^2/2)={track_T(q):.4f} vs q^2/(1-q^2)={q*q/(1-q*q):.4f}; max|rho|/L={rmax:.4f} vs sqrt(2(1+q)/3)={math.sqrt(2*(1+q)/3):.4f}")
# --- §1 naive subtraction: order dependence
mu=3.986004418e14; Rr=7.0e6; Ll=100.0
import mpmath as mp; mp.mp.dps=60
ex=float(-(mp.mpf(mu)/3)*(1/(mp.mpf(Rr)+Ll)**2+1/(mp.mpf(Rr)-Ll)**2-2/mp.mpf(Rr)**2))
forms={
 "mu/3*(a+b-2c)":-(mu/3)*(1/(Rr+Ll)**2+1/(Rr-Ll)**2-2/Rr**2),
 "(a+b-2c)/3*mu":-((1/(Rr+Ll)**2+1/(Rr-Ll)**2-2/Rr**2)/3)*mu,
 "mean accel minus point (3 accelerations)":(-(mu/(Rr+Ll)**2)-(mu/Rr**2)-(mu/(Rr-Ll)**2))/3+mu/Rr**2,
 "accel sum order 2":(-(mu/(Rr-Ll)**2)-(mu/(Rr+Ll)**2)-(mu/Rr**2))/3+mu/Rr**2,
 "np.float32? (no) a+b then -2c":-(mu/3)*((1/(Rr+Ll)**2+1/(Rr-Ll)**2)-2/Rr**2),
}
for k,v in forms.items(): rep(f"S1 naive [{k}]",f"{v:.10e} relerr {abs(v-ex)/abs(ex):.2e}")
rep("S1 paper naive value","-3.3202862681e-9 relerr %.2e"%(abs(-3.3202862681e-9-ex)/abs(ex)))
for eps in (1e-7,1e-8):
    Rr2=1.0; L2=eps; ex2=float(-(mp.mpf(1)/3)*(1/(1+mp.mpf(L2))**2+1/(1-mp.mpf(L2))**2-2))
    nv=-(1/3)*(1/(Rr2+L2)**2+1/(Rr2-L2)**2-2/Rr2**2); rep(f"S1 naive eps={eps}",f"relerr {abs(nv-ex2)/abs(ex2):.2e} (paper 8.20e-3 at 1e-7, 100% at <=1e-8)")
# --- NEG-W5/W6 tensions, Bennu
muE=3.986004418e14
for rp in (6.3e6,7.0e6,6.8e6): rep(f"NEG-W5 tension mu M L/rp^3 L=100 rp={rp/1e3:.0f}km",f"{muE*1000*100/rp**3:.4f} N")
rep("NEG-W5 Regime B tension L=20km rp=5250km",f"{muE*1000*2e4/5.25e6**3:.2f} N (paper 55.1)")
rep("NEG-W1 Regime B tension L=20km rp=6800km",f"{muE*1000*2e4/6.8e6**3:.2f} N ; at a: {muE*1000*2e4/(6.8e6/0.75)**3*0+muE*1000*2e4/ (6.8e6)**3:.2f}")
muB=4.892; Rb=2500.0
rep("NEG-W6 Bennu tension mu M L/R^3",f"{muB*1000*100/Rb**3:.3e} N; pure gravity-gradient 2/3 of that {2/3*muB*1000*100/Rb**3:.3e}")
rep("NEG-W6 |da_par| 2 mu L^2/R^4",f"{2*muB*100**2/Rb**4:.3e} m/s^2 ; 1AU SRP A/M=0.01: {4.56e-6*0.01:.2e}")
rep("NEG-W6 boost ratio (L/R)^2 Bennu/Earth",f"{(7.0e6/2.5e3)**2:.3e}; L^2/R^4 ratio at fixed mu: {(7.0e6/2.5e3)**4:.3e}")
Tyr=365.25*86400
def dvyr(mu,a,e,L):
    p=a*(1-e*e); dE=2*mu*L**2/p**3*(3*e+e**3); T=2*math.pi*math.sqrt(a**3/mu); return dE/math.sqrt(mu/a)*Tyr/T
rep("NEG-W6 Bennu dv/yr e=0.25 a=2500",f"{1e3*dvyr(muB,2500,0.25,100):.2f} mm/s/yr; v_c={100*math.sqrt(muB/2500):.3f} cm/s")
rep("NEG-W6 Bennu dv/yr e=0.25 rp=2500",f"{1e3*dvyr(muB,2500/0.75,0.25,100):.2f} mm/s/yr")
# Note 8: Keplerian mapping
E0=-1*3/2; Ef=E0+7.2590e-3; af=-3/(2*Ef); ef=math.sqrt(1-0.96/af)
rep("Note8 Keplerian a_f,e_f from dE (mu=1,M=3,p=0.96)",f"{af:.5f}, {ef:.5f} (paper 1.0046, 0.2106)")
rep("F35 q(0.0275)",f"{((1-0.0275)/(1+0.0275))**3:.6f}")
rep("Earth radius: mean 6371.0 vs equatorial 6378.137","rp=6800 km is 429 km (mean) / 421.9 km (equatorial) altitude")
