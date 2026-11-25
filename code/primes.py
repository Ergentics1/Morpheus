import numpy as np, itertools, math, json, sympy
from functools import lru_cache
# dual Tonnetz: triads as (root,q); P,L,R
def P(c): r,q=c; return (r,'m' if q=='M' else 'M')
def R(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def L(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
OPS={'P':P,'L':L,'R':R}
V=[(r,q) for r in range(12) for q in 'Mm']; ix={v:i for i,v in enumerate(V)}
A=np.zeros((24,24),int)
for v in V:
    for f in OPS.values(): A[ix[v],ix[f(v)]]+=1
E=[(u,v) for u in range(24) for v in range(24) if A[u,v]]; eix={e:i for i,e in enumerate(E)}
B=np.zeros((72,72),dtype=object)
for (u,v),i in eix.items():
    for w in range(24):
        if A[v,w] and w!=u: B[i,eix[(v,w)]]=1
M=sympy.Matrix(B.tolist())
# traces N_m = tr(B^m) exactly with python ints
Bi=[[int(x) for x in row] for row in B.tolist()]
import numpy as np
Bn=np.array(Bi,dtype=object)
Nm={}; Pw=np.identity(72,dtype=object)
for m in range(1,61):
    Pw=Pw.dot(Bn); Nm[m]=int(sum(Pw[i,i] for i in range(72)))
def mob(n): return sympy.mobius(n)
pi={m: sum(mob(m//d)*Nm[d] for d in sympy.divisors(m))//m for m in Nm}
for m in Nm: assert sum(mob(m//d)*Nm[d] for d in sympy.divisors(m))%m==0
print('N_m',{m:Nm[m] for m in range(1,25)})
print('pi(m)',{m:pi[m] for m in range(1,31) if pi[m]})
# words: cyclically reduced words over {P,L,R} trivial on C
def apply(w,c):
    for ch in w: c=OPS[ch](c)
    return c
def words(m):
    out=[]
    for w in itertools.product('PLR',repeat=m):
        if any(w[i]==w[(i+1)%m] for i in range(m)): continue
        if apply(w,(0,'M'))==(0,'M'): out.append(''.join(w))
    return out
for m in (6,8,10,12):
    ws=words(m); print(m,len(ws),'words; 24*len =',24*len(ws),'N_m=',Nm[m])
    # primitive cyclic classes
    cl=set()
    for w in ws:
        rots=[w[i:]+w[:i] for i in range(m)]; c=min(rots)
        if not any(len(w)%d==0 and w==w[:d]*(m//d) for d in range(1,m) ): cl.add(c)
    print('   primitive cyclic word classes:',sorted(cl))
json.dump(dict(N={k:int(v) for k,v in Nm.items()},pi={k:int(v) for k,v in pi.items()}),open('prime_counts.json','w'))
