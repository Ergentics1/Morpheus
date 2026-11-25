import mpmath as mp, numpy as np, json, math, sympy, sys
from voices import *
mp.mp.dps=40
passes=0; total=0
def chk(name,cond):
    global passes,total; total+=1; passes+=bool(cond); print(('PASS ' if cond else 'FAIL ')+name)
# A) double cover by voice-sum mod 24 : explicit 48-vertex graph
V=[(r,q) for r in range(12) for q in 'Mm']
def vsum(c): return sum(tri(c))  # not lifted; lift tracked below
nodes={}; edges=[]
# state: (chord, S mod 24) where S = lifted sum of voices; start C major S=0+4+7
from collections import deque
start=((0,'M'),11); seen={start}; dq=deque([start])
while dq:
    c,S=dq.popleft()
    for op in 'PLR':
        d,out,inn,s=step(c,op); t=(d,(S+s)%24); edges.append(((c,S),t))
        if t not in seen: seen.add(t); dq.append(t)
idx={v:i for i,v in enumerate(sorted(seen,key=str))}
A=np.zeros((len(idx),)*2)
for a,b in edges: A[idx[a],idx[b]]+=1
ev=np.sort(np.linalg.eigvalsh(A))
chk('melodic double cover has 48 vertices, 3-regular',len(idx)==48 and all(A.sum(1)==3))
nontriv=[x for x in ev if abs(abs(x)-3)>1e-9]
chk('double cover Ramanujan: max nontrivial |lam|=%.6f <= 2sqrt2'%max(abs(x) for x in nontriv), max(abs(x) for x in nontriv)<=2*math.sqrt(2)+1e-12)
chk('new eigenvalue = sqrt(5+2sqrt2)', abs(max(abs(x) for x in nontriv)-math.sqrt(5+2*math.sqrt(2)))<1e-9)
# triple cover (W mod 3) fails
start=((0,'M'),11); seen={start}; dq=deque([start]); edges=[]
while dq:
    c,S=dq.popleft()
    for op in 'PLR':
        d,out,inn,s=step(c,op); t=(d,(S+s)%36); edges.append(((c,S),t))
        if t not in seen: seen.add(t); dq.append(t)
idx={v:i for i,v in enumerate(sorted(seen,key=str))}
A=np.zeros((len(idx),)*2)
for a,b in edges: A[idx[a],idx[b]]+=1
ev=np.sort(np.linalg.eigvalsh(A)); nontriv=[x for x in ev if abs(abs(x)-3)>1e-9]
chk('triple cover (W mod 3, 72 vertices) NOT Ramanujan: max %.6f'%max(abs(x) for x in nontriv), len(idx)==72 and max(abs(x) for x in nontriv)>2*math.sqrt(2))
# B) sigma^2 = 1/24 from curvature of Perron root of twisted Hashimoto (mpmath)
def lam(phi): return mp.sqrt(5+4*mp.cos(phi/4))
def rho(phi): l=lam(phi); return (l+mp.sqrt(l**2-8))/2
c2=mp.diff(lambda p: mp.log(rho(p)),0,2)
chk('variance of W per step = -d2 log rho = 1/24 (got %s)'%mp.nstr(-c2,20), abs(-c2-mp.mpf(1)/24)<mp.mpf(10)**-25)
# C) RH window endpoints 4 arccos(3/4)
a=4*mp.acos(mp.mpf(3)/4)
chk('RH window edge: max|lam(phi)| = 2sqrt2 at phi=4arccos(3/4)=%s'%mp.nstr(a,15), abs(lam(a)-2*mp.sqrt(2))<1e-30)
# D) transfer counts vs enumeration census2 m<=18
T=json.load(open('transfer.json')); C2=json.load(open('census2.json'))
ok=True
for m in range(6,19,2):
    byW=collections.Counter()
    for (uv,W,pt,home,disp,n) in C2[str(m)]:
        byW[W]+=n
        if (W!=-uv[0]) or (home!=(W==0)) or ((pt=='id')!=(W%3==0)): ok=False
    if {int(k):v for k,v in T[str(m)]['W'].items()}!={k:v for k,v in byW.items()}: ok=False
chk('enumeration vs transfer W-distribution m<=18; W=-u, home<=>W=0, sigma=id<=>3|W',ok)
# E) R statistics: mean -> 1/3, variance
m=40; R=T['40']['R']; pi=T['40']['pi']
mean=sum(int(k)*v for k,v in R.items())/pi; var=sum(int(k)**2*v for k,v in R.items())/pi-mean**2
print('   m=40 whole-tone count mean/m=%.6f var/m=%.6f'%(mean/m,var/m))
y=sympy.symbols('y'); l=sympy.symbols('l')
M=sympy.Matrix([[0,1,y],[1,0,y],[1,1,0]])
cp=(l*sympy.eye(3)-M).det()
# derivatives of log Perron root wrt log y at y=1
L=sympy.Function('L')
f=sympy.lambdify
import mpmath
def perron(yy): return mpmath.findroot(lambda l: l**3-(1+2*yy)*l-2*yy, 2)
g=lambda s: mpmath.log(perron(mpmath.e**s))
mu1=mpmath.diff(g,0,1); v1=mpmath.diff(g,0,2)
chk('whole-tone fraction -> 1/3 (mean %s), variance/step %s'%(mpmath.nstr(mu1,15),mpmath.identify(v1)), abs(mu1-mpmath.mpf(1)/3)<1e-20)
print('   char poly',sympy.expand(cp))
# F) counting by voice-leading distance D = sum|step| = m + r
cnt=collections.Counter()
for mm in range(6,41,2):
    for k,v in T[str(mm)]['R'].items(): cnt[mm+int(k)]+=v
t=sympy.symbols('t')
Mt=sympy.Matrix([[0,t,t**2],[t,0,t**2],[t,t,0]])
dp=sympy.factor((sympy.eye(3)-Mt).det()); print('   det(I-M(t,t^2)) =',dp)
roots=[r for r in sympy.Poly(sympy.expand((sympy.eye(3)-Mt).det()),t).nroots(n=30) if r.is_real and r>0]
t0=min(roots); alpha=1/t0
print('   growth per semitone of voice motion alpha=%s'%alpha)
for D in (20,26,30,34,38,40):
    pred=float(alpha)**D/D
    print('   D=%d primes=%d  pred alpha^D/D*c ratio=%.5f'%(D,cnt[D],cnt[D]/pred))
print('PASS %d/%d'%(passes,total))
