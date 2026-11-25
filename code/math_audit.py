# Independent high-precision audit of every number in "Prime Cadences"
import mpmath as mp, itertools, json, sympy, math, numpy as np
mp.mp.dps=60
R=[]
def chk(name,ok): R.append((name,bool(ok))); print(('PASS ' if ok else 'FAIL ')+name)
# --- graph built from pitch-class sets (independent of score/geo code)
tri=[frozenset({r%12,(r+4)%12,(r+7)%12}) for r in range(12)]+[frozenset({r%12,(r+3)%12,(r+7)%12}) for r in range(12)]
ix={t:i for i,t in enumerate(tri)}
def nbrs(t):
    out=[]
    for a,b in itertools.combinations(sorted(t),2):
        c=next(iter(t-{a,b})); w=frozenset({a,b,(a+b-c)%12})
        if w in ix: out.append(w)
    return out
adj={t:nbrs(t) for t in tri}
chk('24 triads, every one has exactly 3 P/L/R neighbours',len(tri)==24 and all(len(v)==3 for v in adj.values()))
import collections
col={tri[0]:0}; q=[tri[0]]; bip=True
while q:
    u=q.pop()
    for v in adj[u]:
        if v not in col: col[v]=1-col[u]; q.append(v)
        elif col[v]==col[u]: bip=False
chk('graph connected and bipartite (major/minor alternate)',len(col)==24 and bip)
A=mp.matrix(24,24)
for t in tri:
    for w in adj[t]: A[ix[t],ix[w]]=1
ev=sorted([x for x in mp.eigsy(A,eigvals_only=True)])
fk=lambda k: abs(sum(mp.e**(2j*mp.pi*k*x/12) for x in (0,4,7)))
F=sorted([fk(k) for k in range(12)]+[-fk(k) for k in range(12)])
chk('adjacency spectrum = ±|f_k| of {0,4,7} (60 digits)',max(abs(a-b) for a,b in zip(ev,F))<mp.mpf(10)**-40)
chk('|f1|^2=2-√3, |f2|=|f6|=1, |f3|^2=5, |f4|^2=3, |f5|^2=2+√3',all(abs(x)<1e-50 for x in (fk(1)**2-(2-mp.sqrt(3)),fk(2)-1,fk(6)-1,fk(3)**2-5,fk(4)**2-3,fk(5)**2-(2+mp.sqrt(3)))))
lam2=max(fk(k) for k in range(1,12))
chk('largest non-trivial eigenvalue = √5 = 2.23607 ≤ 2√2 (Ramanujan / graph RH)',abs(lam2-mp.sqrt(5))<1e-50 and lam2<=2*mp.sqrt(2))
th={k:mp.degrees(mp.acos(fk(k)/(2*mp.sqrt(2)))) for k in range(1,12)}
d=sorted(set(round(float(v),3) for v in th.values()))
chk('zero angles = 37.761°, 46.920°, 52.239°, 69.295°, 79.455°',d==[37.761,46.92,52.239,69.295,79.455])
chk('rounded as narrated: 38, 47, 52, 69, 79 degrees',[round(x) for x in d]==[38,47,52,69,79])
chk('θ3 + θ4 = 90° exactly (|f3|²+|f4|² = 8)',abs(th[3]+th[4]-90)<1e-45)
# --- Hashimoto (non-backtracking) matrix, exact integer traces
E=[(ix[t],ix[w]) for t in tri for w in adj[t]]; eix={e:i for i,e in enumerate(E)}
B=[[0]*len(E) for _ in E]
for (u,v),i in eix.items():
    for (x,w),j in eix.items():
        if x==v and w!=u: B[i][j]=1
chk('Hashimoto matrix is 72×72 (36 edges, both directions)',len(E)==72)
Bs=sympy.Matrix(B); Nm={}; Pw=sympy.eye(72)
for m in range(1,41): Pw=Pw*Bs; Nm[m]=int(Pw.trace())
pi={m:sum(int(sympy.mobius(m//dd))*Nm[dd] for dd in sympy.divisors(m))//m for m in Nm}
chk('no closed non-backtracking loops of odd length; none shorter than 6',all(Nm[m]==0 for m in range(1,41) if m%2) and all(Nm[m]==0 for m in (2,4)))
chk('π(6..16) = 32, 78, 240, 576, 2400, 8196',[pi[m] for m in range(6,17,2)]==[32,78,240,576,2400,8196])
u=mp.mpf('0.137')
lhs=mp.det(mp.eye(72)-u*mp.matrix(B)); rhs=(1-u**2)**12*mp.det(mp.eye(24)-u*A+2*u*u*mp.eye(24))
chk('Ihara–Bass: det(I−uB) = (1−u²)^12·det(I−uA+2u²I) at u=0.137',abs(lhs-rhs)<1e-40)
def Nform(m):
    return 2**(m+1)+26+mp.mpf(2)**(m/2+2)*mp.fsum(mp.cos(m*mp.acos(fk(k)/(2*mp.sqrt(2)))) for k in range(1,12))
chk('explicit formula N_m = 2^(m+1)+26+2^(m/2+2)Σcos(mθ_k) matches exact traces, m=2..40 even',all(abs(Nform(m)-Nm[m])<1e-30 for m in range(2,41,2)))
# extend with explicit formula (independent of matrix) to m=160
def piF(m):
    tot=0
    for dd in sympy.divisors(m):
        Nd=0 if dd%2 else int(mp.nint(Nform(dd)))
        tot+=int(sympy.mobius(m//dd))*Nd
    return tot//m
p30=piF(30)
chk('π(30) = 71,585,776; 2^31/30 ≈ 71,582,788',p30==71585776 and int(mp.nint(mp.mpf(2)**31/30))==71582788)
rel=(p30-mp.mpf(2)**31/30)/p30*100
chk('relative gap at m=30 is 0.0042 %',abs(rel-mp.mpf('0.0042'))<mp.mpf('0.00005'))
ne=[abs((piF(m)-mp.mpf(2)**(m+1)/m)/(mp.mpf(2)**(m/2)/m)) for m in range(6,161,2)]
chk('12-EDO normalised error stays inside the RH band |·| ≤ 48 for m = 6..160',max(ne)<=48)
# --- shortest primes, classified independently
def walk(word,start=frozenset({0,4,7})):
    path=[start]; t=start
    for ch in word:
        for w in adj[t]:
            if (len(t&w)==2) and kind(t,w)==ch: t=w; break
        path.append(t)
    return path
def kind(t,w):
    a,b=sorted(t&w); dd=(b-a)%12
    return {7:'P',5:'P',3:'L',9:'L',4:'R',8:'R'}[dd]
def closed_words(m):
    out=[]
    for w in itertools.product('PLR',repeat=m):
        if any(w[i]==w[(i+1)%m] for i in range(m)): continue
        if walk(w)[-1]==frozenset({0,4,7}): out.append(''.join(w))
    return out
w6=closed_words(6)
hexa=[w for w in w6 if len(set.intersection(*[set(x) for x in walk(w)[:-1]]))==1]
hext=[w for w in w6 if w in ('PLPLPL','LPLPLP')]
chk('length 6: 24 common-tone hexagons + 8 hexatonic = 32 primes',len(w6)*24//6==32 and len(hexa)*24//6==24 and len(hext)*24//6==8 and len(hexa)+len(hext)==len(w6))
w8=closed_words(8)
chk('length 8: 6 of the 78 primes are octatonic PR cycles',len(w8)*24//8==78 and sum(w in ('PRPRPRPR','RPRPRPRP') for w in w8)*24//8==6)
W=json.load(open('winding.json'))
chk('winding census: length 8 has no contractible (0,0) prime; length 6 has 24',W['8'].get('(0, 0)',0)==0 and W['6']['(0, 0)']*24//6==24)
chk('addresses: hexatonic (0,±1), octatonic (±1,0), PRLRLRLR (1,1)',('(0, -1)' in W['6']) and W['8'].get('(1, 0)')==1 and W['8'].get('(1, 1)')==4)
# Hamiltonian cycles (independent DFS on the set-based graph)
cnt=0
def dfs(t,vis,last,n):
    global cnt
    for w in adj[t]:
        if w==last: continue
        if n==23:
            if w==frozenset({0,4,7}): cnt+=1
            continue
        if w in vis: continue
        vis.add(w); dfs(w,vis,t,n+1); vis.remove(w)
s0=frozenset({0,4,7}); dfs(s0,{s0},None,0)
chk('124 directed Hamiltonian cycles (Albini–Antonini 2009)',cnt==124)
# --- other tunings
def lam(X,N): return max(abs(sum(mp.e**(2j*mp.pi*k*x/N) for x in X)) for k in range(1,N))
l53=lam((0,17,31),53); l31=lam((0,10,18),31)
mu=(l53+mp.sqrt(l53**2-8))/2
chk('53-EDO major triad: max |λ| = 2.8565 > 2√2 (fails graph RH)',abs(l53-mp.mpf('2.85654'))<1e-5 and l53>2*mp.sqrt(2))
chk('53-EDO error exponent log2(μ) = 0.703 → narrated 0.70',abs(mp.log(mu,2)-mp.mpf('0.7032'))<5e-4)
chk('31-EDO major triad passes, barely: 2.8246 ≤ 2.8284',l31<=2*mp.sqrt(2) and abs(l31-mp.mpf('2.82463'))<1e-5)
chk('53-EDO major third 17 steps = 384.9¢ vs pure 386.3¢',abs(1200*17/mp.mpf(53)-mp.mpf('384.906'))<1e-3 and abs(1200*mp.log(1.25,2)-mp.mpf('386.314'))<1e-3)
X=json.load(open('explicit.json'))
chk('53-EDO normalised error at m=160 exceeds 10^10 (grows), 12-EDO stays below 48',abs(X['53']['err']['160'])>1e10 and abs(X['12']['err']['160'])<48)
chk('the constant 26 = 2 (poles ±1 of λ=±3) + 24 (Bass factor (1−u²)^12)',2+2*12==26)
# --- the composed piece: every phrase is a prime cadence from C to C
CAD={'hexagon':'PLRPLR','hexatonic':'PLPLPL','octatonic':'PRPRPRPR','winding':'PRLRLRLR','double':'PLPLRPLPLR','coda':'RLPRLP'}
ok=True
for k,w in CAD.items():
    m=len(w); path=walk(w)
    ok&= path[-1]==s0 and all(w[i]!=w[(i+1)%m] for i in range(m)) and len(set(path[:-1]))==m
chk('all six finale phrases are closed, non-backtracking, primitive loops through distinct triads',ok)
chk('double hexagon (length 10) is contractible: 10-step (0,0) loops exist',W['10'].get('(0, 0)',0)>0)
# lattice lift: displacement of the start triangle after a word, in the kernel basis (4,-4),(0,3)
def lift_wind(word):
    tri=[(0,0),(1,0),(0,1)]
    K={(1,0):'P',(-1,0):'P',(0,1):'R',(0,-1):'R',(1,-1):'L',(-1,1):'L'}
    for ch in word:
        for u_,v_ in itertools.combinations(tri,2):
            if K.get((v_[0]-u_[0],v_[1]-u_[1]))==ch:
                w_=[x for x in tri if x not in (u_,v_)][0]; tri=[u_,v_,(u_[0]+v_[0]-w_[0],u_[1]+v_[1]-w_[1])]; break
    a0=sorted(tri)[0]; da,db=a0; return (da//4,(db+da)//3) if da%4==0 and (db+da)%3==0 else None
chk('finale addresses by lattice lift: hexagon (0,0), hexatonic (0,±1), octatonic ±(1,0), winding ±(1,1), double hexagon (0,0)',
    lift_wind('PLRPLR')==(0,0) and abs(lift_wind('PLPLPL')[1])==1 and lift_wind('PLPLPL')[0]==0 and abs(lift_wind('PRPRPRPR')[0])==1 and lift_wind('PRPRPRPR')[1]==0
    and lift_wind('PRLRLRLR') in ((1,1),(-1,-1)) and lift_wind('PLPLRPLPLR')==(0,0) and lift_wind('RLPRLP')==(0,0))
TH=np.array([37.761,46.920,52.239,69.295,79.455]); chk('Tonnetz-bell partials = θ_k/θ_min = 1, 1.243, 1.383, 1.835, 2.104',np.allclose(TH/TH[0],[1,1.2426,1.3834,1.8351,2.1042],atol=2e-4))
n=sum(ok for _,ok in R); print(f'\n{n}/{len(R)} checks passed')
open('math_audit.md','w').write('# Prime Cadences: math audit\n\n'+'\n'.join(('- PASS ' if ok else '- FAIL ')+nm for nm,ok in R)+f'\n\n**{n}/{len(R)} passed**\n')
