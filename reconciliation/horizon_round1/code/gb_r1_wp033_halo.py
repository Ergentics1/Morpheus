# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- [GB] Round-1 independent checks
"""GB independent re-run of WP033 §2 halo (paper initial state), 42-ODE STM, Broucke indices, W^u periapsis."""
import numpy as np, math
from scipy.integrate import solve_ivp
mu=0.0121505856; DU=384400.0
def f(t,Y):
    x,y,z,vx,vy,vz=Y[:6]; r1=math.sqrt((x+mu)**2+y*y+z*z); r2=math.sqrt((x-1+mu)**2+y*y+z*z)
    ax=2*vy+x-(1-mu)*(x+mu)/r1**3-mu*(x-1+mu)/r2**3; ay=-2*vx+y-(1-mu)*y/r1**3-mu*y/r2**3; az=-(1-mu)*z/r1**3-mu*z/r2**3
    out=[vx,vy,vz,ax,ay,az]
    if len(Y)>6:
        Phi=np.array(Y[6:]).reshape(6,6)
        def U2(x,y,z):
            H=np.zeros((3,3)); 
            for m_,cx,r in ((1-mu,-mu,r1),(mu,1-mu,r2)):
                d=np.array([x-cx,y,z]); H+=m_*(3*np.outer(d,d)/r**5-np.eye(3)/r**3)
            H[0,0]+=1; H[1,1]+=1; return H
        A=np.zeros((6,6)); A[:3,3:]=np.eye(3); A[3:,:3]=U2(x,y,z); A[3,4]=2; A[4,3]=-2
        out+=list((A@Phi).ravel())
    return out
def CJ(Y):
    x,y,z,vx,vy,vz=Y[:6]; r1=math.sqrt((x+mu)**2+y*y+z*z); r2=math.sqrt((x-1+mu)**2+y*y+z*z)
    return x*x+y*y+2*(1-mu)/r1+2*mu/r2-(vx*vx+vy*vy+vz*vz)
X0=np.array([1.1734236346,0,0.0800,0,-0.1845292585,0]); T=3.36106913
# small differential correction (fix x0, vary z0? -> keep paper z0, vary vy0 and T) to report how close the printed state is to periodic
def half(X):
    ev=lambda t,Y: Y[1]; ev.terminal=True; ev.direction=1 if False else 0
    s=solve_ivp(f,(1e-3,T),X,events=ev,rtol=1e-13,atol=1e-13); return s
Y0=np.concatenate([X0,np.eye(6).ravel()])
s=solve_ivp(f,(0,T),Y0,rtol=1e-13,atol=1e-13)
YT=s.y[:,-1]; M=YT[6:].reshape(6,6)
print("closure |X(T)-X0| =",np.linalg.norm(YT[:6]-X0), " C_J0=",f"{CJ(X0):.8f}"," |dCJ|=",abs(CJ(YT)-CJ(X0)))
K=np.array([[0,1,0],[-1,0,0],[0,0,0]]); Om=np.block([[-2*K,np.eye(3)],[-np.eye(3),np.zeros((3,3))]])
print("||M^T Om M - Om||_inf =",np.abs(M.T@Om@M-Om).max())
tr1=np.trace(M); tr2=np.trace(M@M)
alpha=2-tr1; beta=(alpha**2-(tr2-2))/2  # Broucke: char poly of reciprocal 6x6 with two unit eigenvalues
# reduce: eigenvalues lam: pairs (lam,1/lam): nu=(lam+1/lam)/2
w=np.linalg.eigvals(M); w=w[np.argsort(-abs(w))]
lu=abs(w[0]); nus=sorted({round(((x+1/x)/2).real,6) for x in w if abs(abs(x)-1)>1e-3 or abs(x-1)>1e-2})
print("eigvals:",np.round(w,6)); print("lambda_u=",lu," nu1=(lu+1/lu)/2=",(lu+1/lu)/2)
# nu2 from complex unit-modulus pair
cpx=[x for x in w if abs(abs(x)-1)<1e-3 and abs(x.imag)>1e-3]
if cpx: print("nu2=cos(arg)=",math.cos(abs(np.angle(cpx[0]))), " winding deg/orbit=",math.degrees(abs(np.angle(cpx[0]))))
# W^u from x0 with 1e-4 kick along -v_u (normalised 6-vector) ; also +v_u
vals,vecs=np.linalg.eig(M); vu=np.real(vecs[:,np.argmax(abs(vals))]); vu/=np.linalg.norm(vu)
for sgn in (-1,1):
    def moon(t,Y): return math.sqrt((Y[0]-1+mu)**2+Y[1]**2+Y[2]**2)-1737.4/DU
    moon.terminal=True
    s2=solve_ivp(f,(0,6*T),X0+sgn*1e-4*vu,rtol=1e-12,atol=1e-12,events=moon,dense_output=True,max_step=0.01)
    d=np.sqrt((s2.y[0]-1+mu)**2+s2.y[1]**2+s2.y[2]**2)*DU
    hit=len(s2.t_events[0])>0
    print(f"W^u sign {sgn:+d}: min distance to Moon centre = {d.min():.1f} km; surface impact event: {hit} at t={s2.t[-1]*4.342:.2f} d")
