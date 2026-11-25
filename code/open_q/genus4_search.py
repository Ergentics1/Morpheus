"""Exhaustive: is there a genus-4 curve over F2 with L(u) = 1+4u^2+9u^4+16u^6+16u^8 (point counts 3,13,9,21)?
Hyperelliptic genus-4 models were searched earlier (none). A non-hyperelliptic genus-4 curve is canonically Q cap K in P^3,
Q in {x0x1+x2x3, x0x1+x2^2+x2x3+x3^2, x0x1+x2^2} up to PGL4(F2), K a cubic (mod Q*linear: 16 free coefficients).
We count points over F_{2^n} (n=1..4) for all 3*2^16 pairs, then test smoothness of any survivors."""
import numpy as np, itertools, sympy as sp, json
IRR={1:0b11,2:0b111,3:0b1011,4:0b10011}
def mt(n):
    q=2**n; M=np.zeros((q,q),dtype=np.int64)
    for a in range(q):
        for b in range(q):
            r=0;x=a;y=b
            while y:
                if y&1: r^=x
                y>>=1;x<<=1
                if x>>n&1: x^=IRR[n]
            M[a,b]=r
    return M
V=list(range(4)); CUB=[m for m in itertools.combinations_with_replacement(range(4),3)]  # 20 monomials
QUADS={'hyp':lambda P,M:M[P[:,0],P[:,1]]^M[P[:,2],P[:,3]],
       'ell':lambda P,M:M[P[:,0],P[:,1]]^M[P[:,2],P[:,2]]^M[P[:,2],P[:,3]]^M[P[:,3],P[:,3]],
       'cone':lambda P,M:M[P[:,0],P[:,1]]^M[P[:,2],P[:,2]]}
# monomials divisible by x0*x1 are redundant modulo Q (x0x1 = rest of Q): keep the 16 cubic monomials not divisible by x0*x1
KEEP=[m for m in CUB if not (0 in m and 1 in m)]
assert len(KEEP)==16
TARGET=[3,13,9,21]
cand={}
for qn,Qf in QUADS.items():
    alive=np.ones(2**16,dtype=bool)
    coeffs=((np.arange(2**16)[:,None]>>np.arange(16))&1).astype(np.uint8)
    for n in range(1,5):
        q=2**n; M=mt(n); pts=[]
        for lead in range(4):
            rest=3-lead
            g=np.array(list(itertools.product(range(q),repeat=rest)),dtype=np.int64).reshape(-1,rest) if rest else np.zeros((1,0),dtype=np.int64)
            P=np.zeros((len(g),4),dtype=np.int64); P[:,lead]=1; P[:,lead+1:]=g; pts.append(P)
        P=np.vstack(pts); P=P[Qf(P,M)==0]
        vals=np.zeros((16,len(P)),dtype=np.int64)
        for k,(a,b,c) in enumerate(KEEP): vals[k]=M[M[P[:,a],P[:,b]],P[:,c]]
        bits=((vals[:,:,None]>>np.arange(n))&1).reshape(16,-1).astype(np.uint8)   # 16 x (pts*n)
        idx=np.nonzero(alive)[0]
        R=(coeffs[idx].astype(np.int32)@bits.astype(np.int32))&1      # value bits
        zero=(R.reshape(len(idx),len(P),n).sum(axis=2)==0).sum(axis=1)
        alive[idx[zero!=TARGET[n-1]]]=False
        print(qn,'n',n,'survivors',int(alive.sum()),flush=True)
    cand[qn]=np.nonzero(alive)[0].tolist()
X=sp.symbols('x0:4')
def smooth(qn,c):
    Q={'hyp':X[0]*X[1]+X[2]*X[3],'ell':X[0]*X[1]+X[2]**2+X[2]*X[3]+X[3]**2,'cone':X[0]*X[1]+X[2]**2}[qn]
    K=sum(((c>>k)&1)*X[a]*X[b]*X[d] for k,(a,b,d) in enumerate(KEEP))
    if K==0: return False
    F=[Q,K]; J=sp.Matrix([[sp.diff(f,v) for v in X] for f in F])
    minors=[J.extract([0,1],list(cc)).det() for cc in itertools.combinations(range(4),2)]
    for k in range(4):
        G=sp.groebner([sp.expand(g.subs(X[k],1)) for g in F+minors],*[v for v in X if v!=X[k]],modulus=2,order='grevlex')
        if not (len(G.exprs)==1 and G.exprs[0]==1): return False
    return True
res={qn:[c for c in cs if smooth(qn,c)] for qn,cs in cand.items()}
print('smooth genus-4 curves with the octic as L-polynomial:',{k:len(v) for k,v in res.items()})
json.dump(dict(point_count_survivors={k:len(v) for k,v in cand.items()},smooth=res),open('genus4_search.json','w'))
