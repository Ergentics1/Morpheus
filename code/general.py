import numpy as np, itertools, math, sympy
def tonnetz(X,N):
    X=tuple(sorted(x%N for x in X))
    orb=set()
    for t in range(N):
        orb.add(frozenset((x+t)%N for x in X)); orb.add(frozenset((-x+t)%N for x in X))
    V=sorted(orb,key=sorted); ix={v:i for i,v in enumerate(V)}
    A=np.zeros((len(V),)*2,int)
    for v in V:
        s=sorted(v)
        for a,b in itertools.combinations(s,2):
            c=[x for x in s if x not in (a,b)][0]
            w=frozenset((a,b,(a+b-c)%N))
            if len(w)==3 and w!=v: A[ix[v],ix[w]]+=1
    return V,A
def counts(A,M=40):
    n=len(A); E=[(u,v) for u in range(n) for v in range(n) for _ in range(A[u,v])]
    # simple graphs only
    eix={e:i for i,e in enumerate(E)}
    B=np.zeros((len(E),)*2,dtype=object)
    for (u,v),i in eix.items():
        for (x,w),j in eix.items():
            if x==v and w!=u: B[i,j]=1
    N={};P=np.identity(len(E),dtype=object)
    for m in range(1,M+1):
        P=P.dot(B); N[m]=int(sum(P[i,i] for i in range(len(E))))
    pi={m:int(sum(sympy.mobius(m//d)*N[d] for d in sympy.divisors(m))//m) for m in N}
    return N,pi
if __name__=='__main__':
  res=[]
  for X in [(0,1,2),(0,1,3),(0,1,4),(0,1,5),(0,1,6),(0,2,4),(0,2,5),(0,2,6),(0,2,7),(0,3,6),(0,3,7),(0,4,8)]:
    V,A=tonnetz(X,12)
    deg=set(A.sum(1)); simple=A.max()<=1
    ev=np.linalg.eigvalsh(A.astype(float))
    d=max(deg)
    nontriv=[abs(e) for e in ev if abs(abs(e)-d)>1e-9]
    lam=max(nontriv) if nontriv else 0
    import networkx as nx
    G=nx.from_numpy_array(A); 
    print(X,len(V),'deg',deg,'simple',simple,'conn',nx.is_connected(G),'lam2=%.4f'%lam,'RH' if lam<=2*math.sqrt(2)+1e-12 else 'FAIL')
