# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- [GB] Round-1 independent checks
"""GB round-1 independent checks, WP031-WP035 (from scratch; no [G4N] code/data reads)."""
import math, numpy as np, mpmath as mp, sympy as sp
from scipy.special import gammaincc
from scipy.integrate import solve_ivp
def rep(k,v): print(f"{k}: {v}")
# ================= WP034 =================
# NEG-W19: 106-bit subtraction emulated with mpmath prec=106 (DD-class mantissa) vs cancellation-free f64
for s in (1e16,1e17,1e20,1e33,1e77):
    mp.mp.prec=106
    S=mp.mpf(s); th=2/S; pi=+mp.pi
    reLi=pi**2/6-th*(2*pi-th)/4
    d106=S**3*(reLi/(2*S**2)-pi**2/(12*S**2))
    mp.mp.prec=300; ex=-mp.pi/2+1/(2*mp.mpf(s))
    f64=-math.pi/2+1/(2*s)
    mp.mp.prec=53; S5=mp.mpf(s); th5=2/S5; pi5=+mp.pi; naive=S5**3*((pi5**2/6-th5*(2*pi5-th5)/4)/(2*S5**2)-pi5**2/(12*S5**2))
    rep(f"WP034 NEG-W19 s={s:.0e}",f"53-bit closed-form {float(naive):+.4f} | 106-bit closed-form {float(d106):+.6f} relerr {abs(float((d106-ex)/ex)):.2e} | cancel-free f64 relerr {abs((f64-float(ex))/float(ex)):.1e}")
mp.mp.prec=53
# NEG-W20 / Theorem G5 from the definitions in WP034 (Eq. 5.23 + Counterexample 2)
A,B,C,c,sst=sp.symbols('A B C c s_star',positive=True)
de=4*sp.exp(-sst/2)/(1+c)
num_DO=2*2*sp.exp(-sst/2)*A          # <Psi|Delta_eta O|Psi>, Delta_eta O = -2 O
norm=(A+B)+c*(A+C)                    # |S0|=A+B (C_b|0>=|0>), |S1|=A+C (C_b|1>=e^{-s*/2}|1>)
Z=sp.simplify((num_DO-de/2*norm).subs(sp.exp(-sst/2),sp.sqrt(c)) )
G5=sp.simplify(de.subs(sp.exp(-sst/2),sp.sqrt(c))/2*((A-B)+(A-C)*c))
rep("WP034 G5 Z_P - G5 formula",sp.simplify(Z-G5))
cv=math.exp(-math.pi**2); dv=4*math.exp(-math.pi**2/2)/(1+cv)
rep("WP034 Counterex2 pair M=1e4",f"{dv/2*1e4*(1+cv):.4f} (paper +143.8377); cycle r=5: {dv/2*((1e4)-(3*1e4)+cv*1e4):.4f} (paper -287.6530)")
# Eq (5.24) safety ratio for paired state (s0 = mean area)
p=cv/(1+cv); lhs=dv; rhs=(2/math.pi)*1*math.pi**2*math.sqrt(p*(1-p)); rep("WP034 Eq5.24 RHS/LHS",f"{rhs/lhs:.6f} (pi/2={math.pi/2:.6f})")
rep("WP034 witness 2-2/(r-1)",f"r=5: {2-2/4:.3f}, r=12: {2-2/11:.3f}; dilution (1+c)/(r-1+c) r=4: {(1+cv)/(3+cv):.4f}")
# NEG-W21
rep("WP034 C156 domain",f"u<=0.35 <=> R>=e^(13/7)={math.exp(13/7):.4f}; at R=e u=0.5: e^-u/(1-u)={math.exp(-.5)/.5:.4f}, minus (1+u^2/2)={math.exp(-.5)/.5-1.125:.4f}")
a=math.pi**4/15; b=4/3**0.75*a**0.25
rep("WP034 beta* ratio",f"C=1: {(1+a)/b:.4f}; C=5/pi^4: {(1+a*5/math.pi**4)/(b*(5/math.pi**4)**0.25):.6f}; argmin C=1/(3a)={1/(3*a):.5f} (5/pi^4={5/math.pi**4:.5f})")
rep("WP034 C153 domain","theta in [0.01,0.40] <=> s=2/theta in [5,200]")
rep("WP034 Sen 2013 (fetched arXiv:1205.0971v2, Eqs.1.4-1.5 + text)","C_local=212/45 per ln a (a ~ length): mixed 212/45 ln a = 106/45 ln A; singlet (212/45-3) ln a = 77/90 ln A")
# 106/45 vs 167/90 cross-paper: density implied by WP034 construction
s_=sp.symbols('s',positive=True)
rep("X-PAPER 106/45 vs 167/90","WP034: Tr(C_b^dag C_b)|_{s_b} ~ s_b^(106/45); measure (4 pi s_b)^(-1/2) ds_b => density rho(s) ~ e^s s^(106/45-1/2) => N(s*) ~ e^{s*} s*^(167/90): Z_{D,1}~s*^(257/90)=alpha; WP035 R3: ln N = s + (alpha-1) ln s = s + 167/90 ln s. Both arithmetic correct; they identify different quantities with Sen's mixed-ensemble entropy.")
# ================= WP035 =================
mp.mp.dps=30
z1=mp.zeta(-2,derivative=1)-mp.zeta(0,derivative=1)
rep("WP035 NEG-W22 S^3",f"zeta1'(0)={mp.nstr(z1,12)}; remainder zeta_R'(-2)={mp.nstr(mp.zeta(-2,derivative=1),8)}; exact/|rem|={mp.nstr(z1/abs(mp.zeta(-2,derivative=1)),5)}, dropped/|rem|={mp.nstr(-mp.zeta(0,derivative=1)/abs(mp.zeta(-2,derivative=1)),5)}")
rep("WP035 NEG-W22 S^5 ratios",f"1.757764/0.080113={1.757764018038/0.080113048371:.3f}; 1.837877/0.080113={2*float(-mp.zeta(0,derivative=1))/0.080113048371:.3f}")
volS=lambda n: 2*math.pi**((n+1)/2)/math.gamma((n+1)/2)
ratio=volS(2)*volS(9)**0.25/(volS(4)**2*math.pi)
wy=(9/(8*math.pi**4))*(math.pi**5/(2**4*120))**0.25
rep("WP035 NEG-W24 Lemma8 ratio",f"{ratio:.7f}; 10^(1/4)*alpha_W={10**0.25*wy:.7f}; Vol(D^5)=pi^5/1920 vs Vol(S^9)/160={volS(9)/160:.6f} ({math.pi**5/1920:.6f})")
rep("WP035 NEG-W24 a_e waterfall",f"-5428.8+121269.4-116156.4 = {-5428.8+121269.4-116156.4:.1f} sigma")
rep("WP035 NEG-W23 boundary example","rho(E)=(1+E)^-2 e^{bH E}: Z(bH)=int_0^inf (1+E)^-2 dE = 1 (finite at the abscissa)")
# G6 Gamma(alpha,alpha) checks by sampling-free formulas
for al in (151/45,257/90,167/90):
    rep(f"WP035 G6 alpha={al:.4f}",f"sigma/mean=1/sqrt(a)={1/math.sqrt(al):.5f}, tail={gammaincc(al,al):.4f}, Beta(a,1) RMS={1/math.sqrt(al*(al+2)):.5f}")
# ================= WP031 =================
q=sp.symbols('q',positive=True); psi,w,L_,m_=sp.symbols('psi omega L m',positive=True)
# arm radii breathing r_k^2 = L^2(1+q cos(2psi+phi_k)) ; motoring power = sum of positive parts of T_k rdot_k
qq=0.5; I0=1000*(2e4)**2; om=2.422e-3
Pc=qq/(math.pi*(1-qq**2)**1.5)*I0*om**3
th=np.linspace(0,2*np.pi,200001)[:-1]; ww=om/math.sqrt(1-qq**2); mt=1000/3; Lm=2e4
P=0
for ph in (0,2*np.pi/3,4*np.pi/3):
    r2=Lm**2*(1+qq*np.cos(2*th+ph)); r=np.sqrt(r2); rdot=-qq*Lm**2*ww*np.sin(2*th+ph)/r; T=mt*ww**2*r; P+=np.mean(np.clip(T*rdot,0,None))
rep("WP031 G4 P_circ q=0.5",f"numeric {P:.1f} W vs formula {Pc:.1f} W (G4N 1,392.3); heat x37/110 = {Pc*37/110:.1f} W (G4N 468.3)")
muE=3.986004418e14; rp=6378.137e3+600e3; e=0.25; pp=rp*(1+e); a=rp/(1-e)
dE=2*muE*1000*Lm**2*(3*e+e**3)/pp**3; T=2*math.pi*math.sqrt(a**3/muE)
rep("WP031 P_orb,full",f"{dE/T:.2f} W (G4N 41.19) using WP030 I0=(2/3)ML^2 law; with I0=ML^2 (3 arms of length L) it would be {1.5*dE/T:.2f} W")
Om=math.sqrt(muE*pp)/rp**2; rep("WP031 Omega_max, 2Omega_max",f"{Om:.4e}, {2*Om:.4e} (paper 2.422e-3)")
nu=muE/rp**3; rep("WP031 NEG-W18 T_pk",f"paper mu M L/rp^3 + m L w^2 = {muE*1000*Lm/rp**3+mt*Lm*(2*Om)**2:.2f} N; 2 m L mu/rp^3 + m L w^2 = {2*mt*Lm*nu+mt*Lm*(2*Om)**2:.2f} N")
rep("WP031 NEG-W18 strain",f"0.5271% vs sigma_allow/E = {1.16e9/270e9*100:.4f}%")
mr=math.exp(992.91/(1600*9.80665)); rep("WP031 NEG-W18 Hall",f"wet-1000: {30+1.15*1000*(1-1/mr):.2f} kg; dry-1000 payload: {30+1.15*1000*(mr-1):.2f} kg")
# NEG-W17 point-mass J2 baseline: mu=1, r=1 circular, i=45 deg, J2 R^2 = 0.05, 5 periods, M=3
def j2(t,y,k=0.05):
    x,yv,z=y[:3]; r=math.sqrt(x*x+yv*yv+z*z); f=-1/r**3; c=1.5*k/r**5; zz=5*z*z/r**2
    return [y[3],y[4],y[5], f*x - c*x*(1-zz), f*yv - c*yv*(1-zz), f*z - c*z*(3-zz)]
i0=math.radians(45); y0=[1,0,0,0,math.cos(i0),math.sin(i0)]
sol=solve_ivp(j2,(0,10*math.pi),y0,rtol=1e-12,atol=1e-12)
yE=sol.y[:,-1]; L0=3*np.cross(y0[:3],y0[3:]); L1=3*np.cross(yE[:3],yE[3:])
rep("WP031 NEG-W17 L=0 baseline (my IC: circular r=1, v=1)",f"|dJ_perp|={np.linalg.norm((L1-L0)[:2]):.4f}, |dJ_z|={abs(L1[2]-L0[2]):.1e}, i_end={math.degrees(math.acos(L1[2]/np.linalg.norm(L1))):.4f} deg, d|L|={np.linalg.norm(L1)-np.linalg.norm(L0):+.4f} (G4N 3.0859, 44.3968, -0.0322; paper 3.087)")
# ================= WP032 =================
d=0.1
for Mh in (100.0,):
    m=100.0; Mt=Mh+3*m
    pts=np.array([[L*math.cos(a_),L*math.sin(a_)] for L,a_ in ((1-d,2*math.pi/3),(1-d,4*math.pi/3),(1.0,0.0))]); hub=np.zeros(2)
    com=(m*pts.sum(0))/Mt; Icom=m*np.sum(np.sum((pts-com)**2,1))+Mh*np.sum(com**2)
    ratio=Icom/(3*m); wrat=1/ratio
    proj=np.dot(pts[0]-com,pts[0]/np.linalg.norm(pts[0]))
    rep("WP032 G2 direct",f"I_COM/I0={ratio:.6f} (formula {1-4/3*d+7/12*d*d:.6f}); T'/T0 (radial projection)={wrat**2*proj:.4f} (G4N 1.1987; paper 0.8163)")
rep("WP032 NEG-W7",f"true radial coefficient 9 mu C22 R_B^2/r^4 vs paper 3; with J2: 3C22-J2/2 = {3*0.0058-0.0175/2:.5f}")
x,y=sp.symbols('x y'); U=1/sp.sqrt(x**2+y**2); lap=sp.diff(U,x,2)+sp.diff(U,y,2)
H=[[sp.diff(lap,a1,a2) for a2 in (x,y)] for a1 in (x,y)]; pt={x:sp.Rational(1,2),y:sp.sqrt(3)/2}
Hx=[[sp.nsimplify(sp.simplify(H[i][j].subs(pt))) for j in range(2)] for i in range(2)]
rep("WP032 NEG-W9 planar isotropic triad Hessian ~ Hess(lap_2D U) at L4 (big primary)",f"{Hx} -> xx:yy = 1:{sp.nsimplify(Hx[1][1]/Hx[0][0])}, both positive")
# ================= WP033 =================
def lin_xy(Uxx,Uyy):
    bq=4-Uxx-Uyy; cq=Uxx*Uyy; lam2=np.roots([1,bq,cq]); return float(-min(lam2.real)) if True else None
mu_=0.0121505856; g2=0.1678327510078692; c2=mu_/g2**3+(1-mu_)/(1+g2)**3
def wxy2(dxx,dyy): # center frequency^2 of planar collinear linearisation
    Uxx=1+2*c2+dxx; Uyy=1-c2+dyy; bq=4-Uxx-Uyy; cq=Uxx*Uyy; disc=bq*bq-4*cq; return (bq+math.sqrt(disc))/2
h=1e-6
for name,row in (("x",(8,-4,-4)),("y",(-4,3,1)),("z",(-4,1,3)),("eq",(2,-0.5,-1.5))):
    dw=(wxy2(row[0]*h,row[1]*h)-wxy2(0,0))/h; dz=-row[2]
    rep(f"WP033 G3 sens axis {name}",f"d(w_xy^2)={dw:+.4f}, d(w_z^2)={dz:+.4f}, d(gap)={dw-dz:+.4f}")
rep("WP033 NEG-W11",f"1003.71-1737.4={1003.71-1737.4:.1f} km")
chi=21.59*600/1190; rep("WP033 NEG-W13",f"chi(600)={chi:.3f}, z={80.2*math.log1p(chi)/chi:.2f} cm")
eta=1.617; rr=4*(2+math.sqrt(1+eta))/(3*(math.sqrt(1+eta)+1)**2)
rep("WP033 NEG-W14",f"eta/0.20={eta/0.2:.2f}x, chi/0.15={21.59/0.15:.0f}x, const-g drift={22.72*rr:.2f} m, centrifugal relief={(4.0627e-4)**2*246*math.cos(math.radians(56))**2:.3e} m/s^2 = {(4.0627e-4)**2*246*math.cos(math.radians(56))**2/(4.892/246**2)*100:.1f}% of g")
