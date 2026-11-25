"""Tropical / Berkovich side: Laplacian, critical (sandpile) group = Neron component group of J(C), spanning trees,
cycle-pairing (period valuation) matrix, Baker-Norine divisorial gonality."""
import sys, json, itertools, math, time
sys.path.insert(0,'../deep'); from common import V, IX, OPS, cname
import numpy as np, sympy as sp, cypari2, numba
pari=cypari2.Pari()
n=24; A=np.zeros((n,n),dtype=np.int64)
for v in V:
    for s in 'PLR': A[IX[v],IX[OPS[s](v)]]+=1
Lap=3*np.eye(n,dtype=np.int64)-A
AU=[]
def chk(name,ok,detail=''): AU.append((name,bool(ok),str(detail))); print(('PASS ' if ok else 'FAIL ')+name,detail)
snf=[int(x) for x in pari.matsnf(pari.matrix(n,n,[int(x) for x in Lap.flatten()]))]
inv=sorted([d for d in snf if d not in (0,1)])
print('SNF invariant factors (nontrivial):',inv)
kappa=int(sp.Matrix(Lap[1:,1:]).det())
chk('spanning trees kappa = det reduced Laplacian = 156,008,448 = 2^15 3^2 23^2',kappa==156008448 and sp.factorint(kappa)=={2:15,3:2,23:2},sp.factorint(kappa))
chk('|critical group| = product of invariant factors = kappa',math.prod(inv)==kappa)
chk('one zero invariant factor (connected)',snf.count(0)==1)
# Fourier product formula: kappa = (1/24) * prod over nonzero Laplacian eigenvalues = (1/24)*6*prod_{k!=0}(9-|f_k|^2)
w=np.exp(2j*np.pi/12); fk=[1+w**k+w**(4*k) for k in range(12)]   # exponents {0,1,4} of L,R,P in L rho^j form
prod=6*np.prod([9-abs(f)**2 for f in fk[1:]])/24
chk('Fourier: kappa = (1/24)*6*prod_{k=1..11}(9-|f_k|^2)',abs(prod-kappa)<1e-3*kappa,round(prod.real))
chk('23^2 comes from k=1,11 and 5,7: (9-(2-sqrt3))(9-(2+sqrt3)) = 46',abs((9-abs(fk[1])**2)*(9-abs(fk[5])**2)-46)<1e-9)
# Sylow structure
syl={p:sorted([sp.multiplicity(p,d) for d in inv if d%p==0],reverse=True) for p in (2,3,23)}
print('Sylow exponents',syl)
# cycle pairing matrix on fundamental cycles
C0=(0,'M'); rep={C0:None}; order=[C0]; par={}
for t in order:
    for s in 'PLR':
        u=OPS[s](t)
        if u not in rep: rep[u]=1; par[u]=t; order.append(u)
edges=[]; eidx={}
for v in V:
    for s in 'PLR':
        u=OPS[s](v); e=tuple(sorted((IX[v],IX[u])))
        if e not in eidx: eidx[e]=len(edges); edges.append(e)
tree={tuple(sorted((IX[u],IX[par[u]]))) for u in par}
def path_to_root(v):
    p=[v]
    while v!=C0: v=par[v]; p.append(v)
    return p
def chain(path):  # oriented edge vector
    x=np.zeros(len(edges),dtype=np.int64)
    for a,b in zip(path,path[1:]):
        i,j=IX[a],IX[b]; e=tuple(sorted((i,j))); x[eidx[e]]+= 1 if i<j else -1
    return x
cyc=[]
for e in edges:
    if e in tree: continue
    a,b=V[e[0]],V[e[1]]
    pa=path_to_root(a); pb=path_to_root(b)
    cyc.append(chain([b,a])+chain(pa)-chain(pb))   # b->a then a->root, minus b->root
Cy=np.array(cyc); Q=Cy@Cy.T
chk('13 fundamental cycles',len(cyc)==13)
# boundary zero check
B=np.zeros((n,len(edges)),dtype=np.int64)
for k,(i,j) in enumerate(edges): B[i,k]-=1; B[j,k]+=1
chk('cycles are closed (boundary 0)',not (B@Cy.T).any())
detQ=int(sp.Matrix(Q).det())
chk('det(cycle pairing Q) = kappa (tropical Jacobian volume^2 = spanning trees)',detQ==kappa)
snfQ=sorted([int(x) for x in pari.matsnf(pari.matrix(13,13,[int(x) for x in Q.flatten()])) if int(x)!=1])
chk('coker Q = critical group (same invariant factors)',snfQ==inv,snfQ)
chk('diag of Q = cycle lengths (6 or 8 here)',set(np.diag(Q))<= {6,8,10,12},sorted(set(np.diag(Q))))
# Gonality (Baker-Norine): smallest d with a degree-d divisor of rank>=1. Vertex-transitive => WLOG D = v0 + E.
nbr=np.array([[IX[OPS[s](v)] for s in 'PLR'] for v in V],dtype=np.int64)
@numba.njit(cache=True)
def reduce_q(D,q,nbr):
    # D effective away from q; return q-reduced divisor (Dhar burning + firing the unburnt set)
    n=D.shape[0]
    while True:
        burnt=np.zeros(n,np.bool_); burnt[q]=True
        cnt=np.zeros(n,np.int64)  # burning edges incoming
        stack=[q]
        while len(stack)>0:
            x=stack.pop()
            for k in range(3):
                y=nbr[x,k]
                if not burnt[y]:
                    cnt[y]+=1
                    if cnt[y]>D[y]:
                        burnt[y]=True; stack.append(y)
        if burnt.all(): return D
        # fire unburnt set
        for x in range(n):
            if not burnt[x]:
                for k in range(3):
                    y=nbr[x,k]
                    if burnt[y]: D[x]-=1; D[y]+=1
@numba.njit(cache=True)
def rank_ge1(D,nbr):
    n=D.shape[0]
    for q in range(n):
        E=D.copy()
        E=reduce_q(E,q,nbr)
        if E[q]<1: return False
    return True
@numba.njit(cache=True)
def search(d,nbr,n):
    # enumerate multisets of size d-1 (nondecreasing index tuples), D = e_0 + sum
    idx=np.zeros(d-1,np.int64)
    count=0
    while True:
        D=np.zeros(n,np.int64); D[0]+=1
        for t in range(d-1): D[idx[t]]+=1
        count+=1
        if rank_ge1(D,nbr): return count, D
        # next multiset
        t=d-2
        while t>=0 and idx[t]==n-1: t-=1
        if t<0: return count, np.zeros(n,np.int64)
        idx[t]+=1
        for u in range(t+1,d-1): idx[u]=idx[t]
gon=None; witness=None
for d in range(2,10):
    t=time.time(); cnt,D=search(d,nbr,n)
    found=D.sum()>0
    print('degree',d,'checked',cnt,'found' if found else 'none',round(time.time()-t,1),'s')
    if found: gon=d; witness=[cname(V[i])+('' if D[i]==1 else f'x{D[i]}') for i in range(n) if D[i]]; break
chk('divisorial gonality computed by exhaustive search',gon is not None,f'gon={gon}, witness={witness}')
# independent re-check of the witness rank with a slow pure-python chip-firing (no numba)
def red_py(D,q):
    D=list(D)
    while True:
        burnt={q}; cnt=[0]*n; st=[q]
        while st:
            x=st.pop()
            for y in nbr[x]:
                if y not in burnt:
                    cnt[y]+=1
                    if cnt[y]>D[y]: burnt.add(y); st.append(y)
        if len(burnt)==n: return D
        for x in range(n):
            if x not in burnt:
                for y in nbr[x]:
                    if y in burnt: D[x]-=1; D[y]+=1
Dw=np.zeros(n,dtype=np.int64)
for s in witness:
    nm,_,m=s.partition('x'); Dw[[i for i in range(n) if cname(V[i])==nm][0]]+=int(m) if m else 1
chk('witness has rank>=1 (pure-python recheck)',all(red_py(Dw,q)[q]>=1 for q in range(n)))
chk('Baker specialisation: gon(X) > 2  =>  the Mumford curve C is not hyperelliptic',gon>2)
json.dump(dict(snf=inv,kappa=kappa,sylow=syl,Q=Q.tolist(),gonality=gon,witness=witness,audit=AU),open('sandpile.json','w'),indent=1)
print(sum(a[1] for a in AU),'/',len(AU))
