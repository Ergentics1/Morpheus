"""Independent verification: two genus-5 curves over F2 (canonical complete intersections of three quadrics in P^4,
taken from Dragutinovic's census) whose L-polynomials are (1-u+2u^2)*octic and (1+u+2u^2)*octic.
We recount points over F_{2^n}, n=1..5, with our own GF(2^n) arithmetic, and check smoothness (Jacobian criterion) by
Groebner bases over F2 on the five affine charts (an ideal containing 1 on every chart = no singular point over F2-bar)."""
import numpy as np, itertools, sympy as sp, json
IRR={1:0b11,2:0b111,3:0b1011,4:0b10011,5:0b100101}
def tables(n):
    q=2**n; M=np.zeros((q,q),dtype=np.int64)
    for a in range(q):
        for b in range(q):
            r=0; x=a; y=b
            while y:
                if y&1: r^=x
                y>>=1; x<<=1
                if x>>n&1: x^=IRR[n]
            M[a,b]=r
    return M
MON=[(i,j) for i in range(5) for j in range(i,5)]   # lexicographic X,Y,Z,T,U
def count(Qs,n):
    q=2**n; M=tables(n); tot=0
    # projective points: first nonzero coordinate = 1
    for lead in range(5):
        rest=4-lead
        grids=np.array(list(itertools.product(range(q),repeat=rest)),dtype=np.int64).reshape(-1,rest) if rest else np.zeros((1,0),dtype=np.int64)
        P=np.zeros((len(grids),5),dtype=np.int64); P[:,lead]=1; P[:,lead+1:]=grids
        ok=np.ones(len(P),dtype=bool)
        for Qc in Qs:
            val=np.zeros(len(P),dtype=np.int64)
            for c,(i,j) in zip(Qc,MON):
                if c: val^=M[P[:,i],P[:,j]]
            ok&=(val==0)
        tot+=int(ok.sum())
    return tot
X,Y,Z,T,U=sp.symbols('X Y Z T U'); V=[X,Y,Z,T,U]
def poly(Qc): return sum(c*V[i]*V[j] for c,(i,j) in zip(Qc,MON))
def smooth(Qs):
    F=[poly(Qc) for Qc in Qs]; J=sp.Matrix([[sp.diff(f,v) for v in V] for f in F])
    minors=[J.extract([0,1,2],list(cols)).det() for cols in itertools.combinations(range(5),3)]
    for k in range(5):
        sub={V[k]:1}
        G=sp.groebner([sp.expand(g.subs(sub)) for g in F+minors],*[v for v in V if v!=V[k]],modulus=2,order='grevlex')
        if not (len(G.exprs)==1 and G.exprs[0]==1): return False
    return True
def Lpoly(N,g=5,q=2):
    u=sp.symbols('u'); s=[q**n+1-N[n-1] for n in range(1,g+1)]; e=[sp.Integer(1)]
    for k in range(1,g+1): e.append(sp.Rational(sum((-1)**(i-1)*e[k-i]*s[i-1] for i in range(1,k+1)),k))
    c=[(-1)**k*e[k] for k in range(g+1)]
    return sp.expand(sum(c[k]*u**k for k in range(g+1))+sum(q**(k-g)*c[2*g-k]*u**k for k in range(g+1,2*g+1)))
u=sp.symbols('u'); OCT=1+4*u**2+9*u**4+16*u**6+16*u**8
CURVES={'A':[(0,0,0,1,0,1,1,0,0,1,1,0,0,0,0),(0,0,1,0,1,1,0,1,0,0,1,1,1,1,1),(1,1,1,0,1,1,1,1,0,1,0,1,0,0,1)],
        'B':[(0,0,0,1,0,1,1,0,0,1,1,0,0,0,0),(0,0,0,1,1,0,0,0,1,0,0,1,0,0,0),(1,1,1,0,1,1,0,0,1,1,0,1,0,1,1)]}
out={}
for name,Qs in CURVES.items():
    N=[count(Qs,n) for n in range(1,6)]; L=Lpoly(N)
    sm=smooth(Qs)
    out[name]=dict(quadrics=[str(sp.expand(poly(Qc))) for Qc in Qs],N=N,L=str(sp.factor(L)),smooth=sm,
       is_L1_times_octic=sp.expand(L-(1-u+2*u**2)*OCT)==0,is_L1p_times_octic=sp.expand(L-(1+u+2*u**2)*OCT)==0)
    print(name,out[name],flush=True)
json.dump(out,open('genus5_verify.json','w'),indent=1)
