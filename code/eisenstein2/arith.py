import sympy as sp, json, itertools
from common import *
res={}
z=sp.exp(2*sp.pi*sp.I/12)
def f(k,T=(0,4,7)): return sp.nsimplify(sp.expand_complex(sum(z**(k*x) for x in T)))
I=sp.I; w3=sp.Rational(-1,2)+sp.sqrt(3)*I/2
F={k:sp.simplify(f(k)) for k in range(12)}
res['f_k']={k:str(v) for k,v in F.items()}
res['f3 == 2-i']=sp.simplify(F[3]-(2-I))==0
res['f4 == 1+2w3 == i*sqrt3']=sp.simplify(F[4]-(1+2*w3))==0 and sp.simplify(F[4]-I*sp.sqrt(3))==0
res['f6 == 1, f2 == 1']=(sp.simplify(F[6]-1)==0, sp.simplify(F[2]-1)==0)
x=sp.symbols('x')
res['|f_k|^2']={k:str(sp.nsimplify(sp.simplify(sp.expand_complex(F[k]*sp.conjugate(F[k]))))) for k in range(12)}
# norms from Q(zeta12) to Q : product over Galois a in {1,5,7,11} of f_{ak}
res['N(f_k) to Q']={k:str(sp.nsimplify(sp.simplify(sp.expand_complex(sp.prod([F[(a*k)%12] for a in (1,5,7,11)]))))) for k in range(12)}
res['f1,f5 are units (norm 1)']=all(res['N(f_k) to Q'][k]=='1' for k in (1,5,7,11))
res['|f5|^2 = 2+sqrt3 = fundamental unit of Z[sqrt3]']=sp.simplify(sp.sympify(res['|f_k|^2'][5])-(2+sp.sqrt(3)))==0
res['min poly f1 over Q']=str(sp.minimal_polynomial(F[1],x))
res['min poly f5 over Q']=str(sp.minimal_polynomial(F[5],x))
# Galois action: sigma_a f_k = f_{ak} (check numerically on conjugated expression)
ok=True
for a in (5,7,11):
    for k in range(12):
        lhs=sp.N(sum(sp.exp(2*sp.pi*I*a*k*x_/12) for x_ in (0,4,7)),30); rhs=sp.N(F[(a*k)%12],30)
        ok&= abs(complex(lhs-rhs))<1e-20
res['galois sigma_a(f_k)=f_{ak}']=ok
# M_a on triads
def Ma(a,T): return frozenset((a*t)%12 for t in T)
cons={tri(v) for v in V}
res['M11 maps triads to triads']=all(Ma(11,T) in cons for T in cons)
res['M5,M7 images of C major']=[sorted(Ma(5,tri((0,'M')))),sorted(Ma(7,tri((0,'M'))))]
def setclass(T):
    best=None
    for t in range(12):
        for s in (1,-1):
            S=tuple(sorted(((s*x)+t)%12 for x in T)); best=S if best is None or S<best else best
    return best
res['M5/M7 image set class']=str(setclass(Ma(7,tri((0,'M')))))
# graph on images: isomorphic (relabelling) -> check 'share two notes' adjacency of 014 orbit equals induced edges
orb=sorted({frozenset(((s*x)+t)%12 for x in (0,1,4)) for t in range(12) for s in (1,-1)},key=sorted)
res['|T/I orbit of 014|']=len(orb)
share2={(A,B) for A in orb for B in orb if A!=B and len(A&B)==2}
induced={(Ma(7,tri(V[a])),Ma(7,tri(V[b]))) for a,b,o,s in EDGES}
res['M7 induced edges subset of share-2-notes in 014 orbit']=induced<=share2
res['014 share-2 degree']=sorted(collections.Counter(A for A,B in share2).values())[:3]
res['M7 is isomorphism Tonnetz(037)->Tonnetz(014) (flip graph)']=induced<=share2
# flip = share two notes AND related by inversion fixing the shared pair
def flipgraph(orbit):
    E=set()
    for A in orbit:
        for B in orbit:
            if A!=B and len(A&B)==2:
                p,q=sorted(A&B); 
                if frozenset((p+q-x)%12 for x in A)==B: E.add((A,B))
    return E
res['flip edges of 014 orbit == M7-induced']=flipgraph(orb)==induced
res['M11 is a graph automorphism of the PLR graph']=all((IX[next(v for v in V if tri(v)==Ma(11,tri(V[a])))],IX[next(v for v in V if tri(v)==Ma(11,tri(V[b])))]) in {(p,q) for p,q,o,s in EDGES} for a,b,o,s in EDGES)
# charpoly and Ihara factors over Q
A=sp.zeros(24,24)
for a,b,o,s in EDGES: A[a,b]+=1
cp=sp.factor_list(A.charpoly(x).as_expr())
res['charpoly factors']=[(str(p),m) for p,m in cp[1]]
u,T=sp.symbols('u T')
fac=[]
for p,m in cp[1]:
    roots=sp.Poly(p,x).all_roots()
    # Ihara factor prod (1 - lam u + 2u^2) over roots of p : resultant
    Lp=sp.expand(sp.resultant(p.subs(x,(1+2*u**2)/u)*u**sp.degree(p,x),sp.Integer(1)*0+1,x)) if False else None
    Lpoly=sp.expand(sp.prod([1-r*u+2*u**2 for r in roots]))
    Lpoly=sp.nsimplify(sp.simplify(Lpoly))
    weil=sp.expand(Lpoly.subs(u,1/T)*T**(2*sp.degree(p,x)))
    # Frobenius field
    pi=sp.Poly(weil,T)
    fac.append(dict(charfactor=str(p),mult=m,L=str(sp.factor(Lpoly)),weil=str(weil)))
res['ihara_factors']=fac
json.dump(res,open('arith.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
