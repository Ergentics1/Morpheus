import mpmath as mp, itertools, json, collections
from voices import *
mp.mp.dps=50
V=[(r,q) for r in range(12) for q in 'Mm']; ix={v:i for i,v in enumerate(V)}
E=[]  # directed edges (x,y,op,step)
for v in V:
    for op in 'PLR':
        d,out,inn,s=step(v,op); E.append((ix[v],ix[d],op,s))
eix={(a,b):i for i,(a,b,o,s) in enumerate(E)}
def Bmat(th):
    B=mp.zeros(72,72)
    for i,(a,b,o,s) in enumerate(E):
        for j,(c,d,o2,s2) in enumerate(E):
            if c==b and d!=a: B[i,j]=mp.expj(th*s2)
    return B
def Amat(th):
    A=mp.zeros(24,24)
    for (a,b,o,s) in E: A[a,b]+=mp.expj(th*s)
    return A
out={}
# 1) twisted Ihara-Bass check
ok=0
for th,u in [(mp.mpf('0.137'),mp.mpf('0.31')+0.2j),(mp.mpf('0.5'),mp.mpf('0.6')),(mp.pi/12,mp.mpf('0.2')-0.4j),(mp.mpf(1.234),mp.mpf('0.45')+0.1j)]:
    l=mp.det(mp.eye(72)-u*Bmat(th)); r=(1-u**2)**(72//2-24)*mp.det(mp.eye(24)-u*Amat(th)+2*u**2*mp.eye(24))
    ok+= abs(l/r-1)<mp.mpf(10)**-40
print('twisted Ihara-Bass checks',ok,'/4')
# 2) eigenvalue formula lambda=±|1+w^{4k}+e^{3i th} w^{9k}| (up to k relabel)
w=lambda k: mp.expj(2*mp.pi*k/12)
def formula(th): return sorted([s*abs(1+w(4*k)+mp.expj(3*th)*w(9*k)) for k in range(12) for s in (1,-1)])
def formula2(th): return sorted([s*abs(1+w(4*k)+mp.expj(-3*th)*w(9*k)) for k in range(12) for s in (1,-1)])
ok=0
for th in [mp.mpf('0.137'),mp.mpf('0.5'),mp.pi/12,mp.mpf('1.234')]:
    ev=sorted([mp.re(x) for x in mp.eighe(Amat(th))[0]])
    ok+= max(abs(a-b) for a,b in zip(ev,formula(th)))<1e-40 or max(abs(a-b) for a,b in zip(ev,formula2(th)))<1e-40
print('eigen formula checks',ok,'/4')
# periodicity in theta with period 2pi/12
ev1=sorted(formula(mp.mpf('0.3'))); ev2=sorted(formula(mp.mpf('0.3')+2*mp.pi/12))
print('period 2pi/12:',max(abs(a-b) for a,b in zip(ev1,ev2))<1e-40)
# 3) RH range in phi=12 theta : max |lambda| <= 2 sqrt2
def mx(phi): return max(formula(phi/12))
r8=2*mp.sqrt(2)
f=lambda phi: mx(phi)-r8
# scan
import numpy as np
pts=[mp.mpf(i)/2000*2*mp.pi for i in range(2001)]
vals=[f(p) for p in pts]
sign_changes=[(pts[i],pts[i+1]) for i in range(2000) if (vals[i]>0)!=(vals[i+1]>0)]
roots=[mp.findroot(f,(a+b)/2) for a,b in sign_changes]
print('RH holds (max|lam|<=2sqrt2) for phi in', [mp.nstr(x,15) for x in roots], 'region where f<=0 e.g. phi=pi:', mp.nstr(f(mp.pi),10))
print('max |lam| at phi=pi', mp.nstr(mx(mp.pi),20), ' closed form?', mp.identify(mx(mp.pi)**2))
for phi in [0,mp.pi/3,mp.pi/2,2*mp.pi/3,mp.pi]:
    print(' phi=%s maxlam=%s minpos=%s'%(mp.nstr(phi,5),mp.nstr(mx(phi),12),mp.nstr(min(abs(x) for x in formula(phi/12)),12)))
print('roots/pi',[mp.nstr(x/mp.pi,15) for x in roots], [mp.identify(mp.cos(x/4)) for x in roots])
json.dump(dict(rh_phi_roots=[str(x) for x in roots]),open('mzeta.json','w'))
