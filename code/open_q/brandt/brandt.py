"""Brandt graph at a prime v of norm 2 for an Eichler order of level N in the totally definite quaternion
algebra over a totally real field F ramified at all real places and at the finite set D''.
Method: v-neighbour enumeration of right O-ideal classes (lattice arithmetic in PARI's alg* functions),
class equality via the positive definite form Tr_{F/Q}(nrd(x)/nu) on the left transporter (min = n iff equivalent).
Output: number of classes, unit-group orders, mass, Brandt matrix B(v), and whether the bipartite double is the chord graph."""
import cypari2, json, sys, itertools, networkx as nx, numpy as np, sympy as sp
pari=cypari2.Pari(); pari.allocatemem(6*10**9)
G=pari
G('mkalg(nf,D)=alginit(nf,[2,[D,vector(#D,i,1/2)],vector(nf.r1,i,1/2)])')
G('cent(al,nf,a)=algalgtobasis(al,[Mod(a,nf.pol),0]~)')
G('latbasis(al,L)=my(n=matsize(L[1])[1]); vector(n,i,alglatelement(al,L,vectorv(n,j,j==i)))')
G('qval(al,nf,x,nuinv)=nfelttrace(nf,lift(algnorm(al,x))*nuinv)')
G('cntu(al,nf,B,nuinv,n)=my(Gm=gram(al,nf,B,nuinv),d=denominator(Gm),M=qfminim(d*Gm,d*2*n)[3],c=0);for(k=1,#M,my(x=sum(i=1,#B,M[i,k]*B[i]),u=lift(algnorm(al,x))*nuinv,w=nfalgtobasis(nf,u));if(denominator(content(w))==1&&abs(idealnorm(nf,u))==1,c++));c')
G('gram(al,nf,B,nuinv)=my(m=#B,q=vector(m,i,qval(al,nf,B[i],nuinv)));matrix(m,m,i,j,if(i==j,2*q[i],qval(al,nf,B[i]+B[j],nuinv)-q[i]-q[j]))')
def nbrs(al,nf,O,I,piel):
    vI=G.alglatmul(al,piel,I)
    Ib=G('latbasis')(al,I); n=len(Ib)
    Ibm=G.matconcat(Ib); vIb=G.matconcat(G('latbasis')(al,vI))
    C=G.matsolve(Ibm,vIb)
    Cm=G.lift(G.matimage(C*G.Mod(1,2)))
    k=int(G.matsize(Cm)[1]); assert k==n-4, (k,n)
    comp=G.lift(G.matsupplement(Cm*G.Mod(1,2))) if k>0 else G.matid(n)
    compcols=[G.vecextract(comp,f'[{j+1}]') for j in range(k,n)]
    vecs=[a for a in itertools.product([0,1],repeat=4) if any(a)]
    out=[]; seen=set()
    for a,b in itertools.combinations(vecs,2):
        span=frozenset([a,b,tuple((x+y)%2 for x,y in zip(a,b))])
        if span in seen: continue
        seen.add(span)
        els=[]
        for c in (a,b):
            v=G.matrix(n,1)
            for i,ci in enumerate(c):
                if ci: v=v+compcols[i]
            els.append(Ibm*v)
        J=G.alglathnf(al,G.matconcat([vIb]+els))
        if G.alglatsubset(al,G.alglatmul(al,J,O),J): out.append(J)
    return out
def transp(al,J,R):
    """left transporter (R:J)_l = {x : xJ in R}, computed as 2^-m (2^m R : J)_l with 2^m R inside J so that
    PARI's transporter (which returns integral results) is exact. Returns basis and the factor 4^-m for nrd."""
    m=0
    while not G.alglatsubset(al,G('(L,c)->[L[1],L[2]*c]')(R,2**m),J): m+=1
    m+=1
    L=G.alglatlefttransporter(al,J,G('(L,c)->[L[1],L[2]*c]')(R,2**m))
    return G('latbasis')(al,L), G(4)**(-m)
def tpos_gen(bnf,nf,I):
    r=G.bnfisprincipal(bnf,I)
    assert all(int(t)==0 for t in r[0]); g=G.nfbasistoalg(nf,r[1])
    U=[G.nfbasistoalg(nf,u) for u in G('(b)->concat([-1],b.fu)')(bnf)]
    for mask in itertools.product([0,1],repeat=len(U)):
        h=g
        for m,u in zip(mask,U):
            if m: h=h*u
        if all(int(s)==1 for s in G.nfeltsign(nf,h)): return h
    raise ValueError('no totally positive generator')
def chord_graph():
    V=[(r,q) for r in range(12) for q in 'Mm']
    P=lambda c:(c[0],'m' if c[1]=='M' else 'M')
    R=lambda c:((c[0]+9)%12,'m') if c[1]=='M' else ((c[0]+3)%12,'M')
    L=lambda c:((c[0]+4)%12,'m') if c[1]=='M' else ((c[0]+8)%12,'M')
    X=nx.Graph()
    for c in V:
        for f in (P,L,R): X.add_edge(c,f(c))
    return X
def one(nf,bnf,n,Ds,Ns,v,label,maxclasses=60):
    al=G('mkalg')(nf,Ds)
    Nid=G.idealhnf(nf,1)
    for P,e in Ns: Nid=G.idealmul(nf,Nid,G.idealpow(nf,P,e))
    O=G.alglathnf(al,G.algeichlerbasis(al,Nid)) if Ns else G.alglathnf(al,G.matid(4*n))
    pi=G.lift(tpos_gen(bnf,nf,v)); piel=G('cent')(al,nf,pi)
    pol=G('(nf)->nf.pol')(nf)
    reps=[(O,0)]; edges={}; queue=[0]
    def same(J,kJ,R,kR):
        Lb,sc=transp(al,J,R)
        nuinv=G.lift(G.Mod(pi,pol)**(kJ-kR))*sc
        return int(G('cntu')(al,nf,Lb,nuinv,n))>0
    while queue:
        i=queue.pop(0); I,k=reps[i]
        for J in nbrs(al,nf,O,I,piel):
            hit=None
            for j,(R,kR) in enumerate(reps):
                if same(J,k+1,R,kR): hit=j; break
            if hit is None:
                reps.append((J,k+1)); hit=len(reps)-1; queue.append(hit)
            edges[(i,hit)]=edges.get((i,hit),0)+1
        if len(reps)>maxclasses: break
    h=len(reps)
    B=np.zeros((h,h),dtype=int)
    for (i,j),c in edges.items(): B[i,j]+=c
    units=[]
    for R,kR in reps:
        Lb,sc=transp(al,R,R)
        units.append(2*int(G('cntu')(al,nf,Lb,sc,n)))
    # independent second method: Brandt matrix by counting elements of norm pi*nu in transporters (theta coefficients)
    T=np.zeros((h,h),dtype=int)
    for i,(Ii,ki) in enumerate(reps):
        for j,(Ij,kj) in enumerate(reps):
            Lb,sc=transp(al,Ii,Ij)
            nuinv=G.lift(G.Mod(pi,pol)**(ki-kj-1))*sc
            T[j,i]=int(G('cntu')(al,nf,Lb,nuinv,n))
    theta_agrees=bool((T==B).all())
    ev=sorted(np.round(np.linalg.eigvals(B).real,9).tolist())
    simple=all(B[i,j]<=1 for i in range(h) for j in range(h))
    Bd=nx.MultiGraph()
    for i in range(h):
        for j in range(h):
            for _ in range(B[i,j]): Bd.add_edge(('a',i),('b',j))
    iso=simple and h==12 and nx.is_isomorphic(chord_graph(),nx.Graph(Bd))
    rec=dict(field=label,D=[int(G.idealnorm(nf,P)) for P in Ds],N=[(int(G.idealnorm(nf,P)),e) for P,e in Ns],
             v=str(G.idealtwoelt(nf,v)),classes=h,units=units,mass=str(sum(sp.Rational(2,u) for u in units)),
             symmetric=bool((B==B.T).all()),rowsums=sorted(set(B.sum(1).tolist())),B=B.tolist(),eig=ev,
             charpoly=str(sp.factor(sp.Matrix(B).charpoly(sp.Symbol('t')).as_expr())),
             multi_edges=not simple,theta_matrix_agrees=theta_agrees,isomorphic_to_chord_graph=bool(iso))
    print(json.dumps({k:v for k,v in rec.items() if k!='B'}),flush=True)
    return rec
def run(polF,Dnorms,Nspec,label):
    nf=G.nfinit(G(polF)); bnf=G.bnfinit(G(polF),1); n=int(G.poldegree(G(polF)))
    def primes_norm(q):
        p=int(sp.factorint(q).popitem()[0]); return [P for P in G.idealprimedec(nf,p) if int(G.idealnorm(nf,P))==q]
    res=[]
    for Ds in itertools.product(*[primes_norm(q) for q in Dnorms]):
        for Ns in itertools.product(*[primes_norm(q) for q,e in Nspec]):
            used=list(Ds)+list(Ns)
            for v in primes_norm(2):
                if any(G.idealhnf(nf,v)==G.idealhnf(nf,u) for u in used): continue
                res.append(one(nf,bnf,n,list(Ds),list(zip(Ns,[e for q,e in Nspec])),v,label))
    return res
CASES={'733':('y^3-2*y^2-6*y-1',[13],[]),'148':('y^3+y^2-3*y-1',[25],[(5,1)]),'469':('y^3+2*y^2-4*y-1',[4],[(7,1)]),
       '316':('y^3+2*y^2-3*y-2',[37],[]),'2777a':('y^4-26*y^2-8*y+1',[],[(71,1)]),'2777b':('y^4-26*y^2-8*y+1',[],[(8,2)]),
       'q41':('y^2-y-10',[],[(2,1),(5,1)]),'q137':('y^2-y-34',[],[(2,1)]),'564':('y^3+2*y^2-4*y-2',[17],[]),
       '13448':('y^4-7*y^2+2',[],[(5,1)]),'13676':('y^4-1368*y^2-32*y+378752',[],[(5,1)]),'6809':('y^4-20*y^2-8*y+16',[],[(17,1)]),'10273':('y^4-42*y^2-56*y+193',[],[(8,1)]),
       'Q26_9':('y',[13],[(3,2)]),'Q570_1':('y',[3,5,19],[])}
if __name__=='__main__':
    todo=sys.argv[1:] or list(CASES); allres={}
    for k in todo:
        pol,Dn,Nn=CASES[k]; allres[k]=run(pol,Dn,Nn,k)
        json.dump(allres,open('brandt_results.json' if not sys.argv[1:] else 'brandt_'+'_'.join(todo)+'.json','w'),indent=1)
