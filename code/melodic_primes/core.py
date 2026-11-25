import numpy as np, sympy, itertools, math, mpmath as mp
def cayley_hashimoto(N,S):
    S=sorted(set(s%N for s in S)); E=[(v,s) for v in range(N) for s in S]; ix={e:i for i,e in enumerate(E)}
    B=np.zeros((len(E),len(E)),dtype=object)
    for (v,s),i in ix.items():
        w=(v+s)%N
        for t in S:
            if (t+s)%N!=0: B[i,ix[(w,t)]]=1
    return B
def traces(B,M):
    P=np.identity(len(B),dtype=object); out={}
    for m in range(1,M+1): P=P.dot(B); out[m]=int(sum(P[i,i] for i in range(len(B))))
    return out
def primes_from_N(Nm): return {m:sum(int(sympy.mobius(m//d))*Nm[d] for d in sympy.divisors(m))//m for m in Nm}
def eig(N,S,k): return sum(math.cos(2*math.pi*k*s/N) for s in S)
def ramanujan(N,S):
    S=[s%N for s in S]; d=len(S); q=d-1
    lam=[eig(N,S,k) for k in range(1,N)]
    nt=[l for l in lam if abs(abs(l)-d)>1e-9]
    return max(abs(l) for l in nt) if nt else 0, 2*math.sqrt(q)
