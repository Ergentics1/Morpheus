"""Brandt graphs at a prime v of norm 2 for any narrow class number (generalises ../brandt/brandt.py, which needs h+=1).
All right ideal classes of the Eichler order O are enumerated by p-neighbours (v and further degree-one primes),
tracking nrd(I) as an ideal. J ~ R iff nrd(R)/nrd(J) = (g) with g >> 0 and, for some eps in O_F^{x,+}/O_F^{x2},
the form Tr(nrd(x)/(g eps)) takes the value n on the left transporter (R:J). Completeness: the weighted class count
sum 1/[O_l^x:O_F^x] must equal the Eichler mass M. The dual graph of the whole Shimura curve at v is the bipartite
double of B(v) on all classes; each of its connected components is the reduction graph of one geometric component."""
import cypari2, json, sys, itertools, networkx as nx, numpy as np, sympy as sp
sys.path.insert(0,'../brandt')
pari=cypari2.Pari(); pari.allocatemem(6*10**9); G=pari
G('mkalg(nf,D)=alginit(nf,[2,[D,vector(#D,i,1/2)],vector(nf.r1,i,1/2)])')
G('cent(al,nf,a)=algalgtobasis(al,[Mod(a,nf.pol),0]~)')
G('latbasis(al,L)=my(n=matsize(L[1])[1]); vector(n,i,alglatelement(al,L,vectorv(n,j,j==i)))')
G('qval(al,nf,x,nuinv)=nfelttrace(nf,lift(algnorm(al,x))*nuinv)')
G('gram(al,nf,B,nuinv)=my(m=#B,q=vector(m,i,qval(al,nf,B[i],nuinv)));matrix(m,m,i,j,if(i==j,2*q[i],qval(al,nf,B[i]+B[j],nuinv)-q[i]-q[j]))')
G('cntu(al,nf,B,nuinv,n)=my(Gm=gram(al,nf,B,nuinv),d=denominator(Gm),M=qfminim(d*Gm,d*2*n)[3],c=0);for(k=1,#M,my(x=sum(i=1,#B,M[i,k]*B[i]),u=lift(algnorm(al,x))*nuinv,w=nfalgtobasis(nf,u));if(denominator(content(w))==1&&abs(idealnorm(nf,u))==1,c++));c')
from brandt import chord_graph
def lat_ideal_mul(al,nf,I,P):
    a,b=G.idealtwoelt(nf,P)
    return G.alglatadd(al,G.alglatmul(al,G('cent')(al,nf,G.nfbasistoalg(nf,a)),I),G.alglatmul(al,G('cent')(al,nf,G.lift(G.nfbasistoalg(nf,b))),I))
def nbrs(al,nf,O,I,P):
    p=int(G.idealnorm(nf,P)); assert sp.isprime(p)
    pI=lat_ideal_mul(al,nf,I,P)
    Ib=G('latbasis')(al,I); n=len(Ib); Ibm=G.matconcat(Ib); pIb=G.matconcat(G('latbasis')(al,pI))
    C=G.matsolve(Ibm,pIb); Cm=G.lift(G.matimage(C*G.Mod(1,p)))
    k=int(G.matsize(Cm)[1]); assert k==n-4,(k,n)
    comp=G.lift(G.matsupplement(Cm*G.Mod(1,p))) if k>0 else G.matid(n)
    cc=[G.vecextract(comp,f'[{j+1}]') for j in range(k,n)]
    # 2-dim subspaces of F_p^4 in reduced echelon form
    subs=[]
    for i1,i2 in itertools.combinations(range(4),2):
        free=[(r,c) for r,piv in ((0,i1),(1,i2)) for c in range(piv+1,4) if c not in (i1,i2)]
        for vals in itertools.product(range(p),repeat=len(free)):
            M=[[0]*4,[0]*4]; M[0][i1]=1; M[1][i2]=1
            for (r,c),x in zip(free,vals): M[r][c]=x
            subs.append(M)
    assert len(subs)==(p**2+1)*(p**2+p+1)
    out=[]
    for M in subs:
        els=[]
        for row in M:
            v=G.matrix(n,1)
            for i,ci in enumerate(row):
                if ci: v=v+ci*cc[i]
            els.append(Ibm*v)
        J=G.alglathnf(al,G.matconcat([pIb]+els))
        if G.alglatsubset(al,G.alglatmul(al,J,O),J): out.append(J)
    assert len(out)==p+1,(len(out),p)
    return out
def transp(al,J,R):
    m=0
    while not G.alglatsubset(al,G('(L,c)->[L[1],L[2]*c]')(R,2**m),J): m+=1
    m+=1
    L=G.alglatlefttransporter(al,J,G('(L,c)->[L[1],L[2]*c]')(R,2**m))
    return G('latbasis')(al,L), G(4)**(-m)
class Field:
    def __init__(s,pol):
        s.nf=G.nfinit(G(pol)); s.bnf=G.bnfinit(G(pol),1); s.n=int(G.poldegree(G(pol)))
        s.bnr=G.bnrinit(s.bnf,G(f'[1,vector({s.n},i,1)]')); s.pol=G('(nf)->nf.pol')(s.nf)
        U=[G.nfbasistoalg(s.nf,u) for u in G('(b)->concat([-1],b.fu)')(s.bnf)]; s.U=U
        s.eps=[]
        for mask in itertools.product([0,1],repeat=len(U)):
            h=G(1)
            for m,u in zip(mask,U):
                if m: h=h*u
            if all(int(x)==1 for x in G.nfeltsign(s.nf,h)): s.eps.append(G.lift(h))
        s.hplus=int(G('(b)->b.no')(s.bnr)); s.h=int(G('(b)->b.no')(s.bnf))
        assert len(s.eps)==s.hplus//s.h
    def inv(s,x): return G.lift(G.Mod(x,s.pol)**-1)
    def tpos(s,I):
        if any(int(t)!=0 for t in G.bnrisprincipal(s.bnr,I,0)): return None
        r=G.bnfisprincipal(s.bnf,I); g=G.nfbasistoalg(s.nf,r[1])
        for mask in itertools.product([0,1],repeat=len(s.U)):
            h=g
            for m,u in zip(mask,s.U):
                if m: h=h*u
            if all(int(x)==1 for x in G.nfeltsign(s.nf,h)): return G.lift(h)
        raise ValueError
def run_one(F,Ds,Ns,v,label,extra_bound=40,maxcl=200):
    nf,n=F.nf,F.n
    al=G('mkalg')(nf,Ds)
    Nid=G.idealhnf(nf,1)
    for P,e in Ns: Nid=G.idealmul(nf,Nid,G.idealpow(nf,P,e))
    O=G.alglathnf(al,G.algeichlerbasis(al,Nid)) if Ns else G.alglathnf(al,G.matid(4*n))
    # Eichler mass
    z=G(f'bestappr(lfun(lfuncreate({F.pol}),-1),10^15)')
    M=sp.Rational(str(abs(z)))*sp.Rational(2)**(1-n)*F.h
    for P in Ds: M*=int(G.idealnorm(nf,P))-1
    for P,e in Ns: q=int(G.idealnorm(nf,P)); M*=q**(e-1)*(q+1)
    bad=[G.idealhnf(nf,P) for P in Ds]+[G.idealhnf(nf,P) for P,e in Ns]+[G.idealhnf(nf,v)]
    extra=[P for p in sp.primerange(2,14) for P in G.idealprimedec(nf,p) if int(G.idealnorm(nf,P))==p and G.idealhnf(nf,P) not in bad]
    if F.hplus>1:   # make sure some seeding prime has a non-trivial narrow class (to reach the other components)
        more=[P for p in sp.primerange(2,200) for P in G.idealprimedec(nf,p) if int(G.idealnorm(nf,P))==p and G.idealhnf(nf,P) not in bad]
        nontriv=[P for P in more if any(int(t)!=0 for t in G.bnrisprincipal(F.bnr,P,0))]
        extra=nontriv[:3]+[P for P in extra if P not in nontriv[:3]]
    gens=[v]+extra
    reps=[]; nrds=[]; units=[]
    def units_of(R):
        Lb,sc=transp(al,R,R)
        return sum(int(G('cntu')(al,nf,Lb,sc*F.inv(e),n)) for e in F.eps)
    def find(J,nJ):
        for j,(R,nR) in enumerate(zip(reps,nrds)):
            g=F.tpos(G.idealdiv(nf,nR,nJ))
            if g is None: continue
            Lb,sc=transp(al,J,R)
            if any(int(G('cntu')(al,nf,Lb,sc*F.inv(g*e),n))>0 for e in F.eps): return j
        return None
    def add(J,nJ):
        reps.append(J); nrds.append(nJ); units.append(units_of(J)); return len(reps)-1
    add(O,G.idealhnf(nf,1)); edges={}
    done=0
    while True:
        while done<len(reps):            # v-neighbour BFS
            for J in nbrs(al,nf,O,reps[done],v):
                nJ=G.idealmul(nf,nrds[done],v); j=find(J,nJ)
                if j is None: j=add(J,nJ)
                edges[(done,j)]=edges.get((done,j),0)+1
            done+=1
            if len(reps)>maxcl: break
        mass=sum(sp.Rational(1,w) for w in units)
        if mass>=M or len(reps)>maxcl: break
        new=False                         # seed a new v-component by a neighbour at a further prime
        for P in extra:
            for i0 in range(len(reps)):
                for J in nbrs(al,nf,O,reps[i0],P):
                    nJ=G.idealmul(nf,nrds[i0],P)
                    if find(J,nJ) is None: add(J,nJ); new=True; break
                if new: break
            if new: break
        if not new: break
    h=len(reps); mass=sum(sp.Rational(1,w) for w in units)
    B=np.zeros((h,h),dtype=int)
    for (a,b),c in edges.items(): B[a,b]+=c
    # theta check: T[j,i] = #{x : x I_i in I_j, nrd(x) = g eps, (g) = v nrd(I_j)/nrd(I_i)} should equal B[j,i]*w_i
    T=np.zeros((h,h),dtype=int)
    for a in range(h):
        for b in range(h):
            g=F.tpos(G.idealdiv(nf,G.idealmul(nf,v,nrds[b]),nrds[a]))
            if g is None: continue
            Lb,sc=transp(al,reps[a],reps[b])
            T[b,a]=sum(int(G('cntu')(al,nf,Lb,sc*F.inv(g*e),n)) for e in F.eps)
    theta=bool(all(T[b,a]==B[b,a]*units[a] for a in range(h) for b in range(h)))
    D2=nx.MultiGraph(); D2.add_nodes_from([(s,k) for s in 'ab' for k in range(h)])
    for a in range(h):
        for b in range(h):
            for _ in range(B[a,b]): D2.add_edge(('a',a),('b',b))
    comps=[]
    X=chord_graph()
    for cset in nx.connected_components(D2):
        S=D2.subgraph(cset); idx=sorted({k for s,k in cset})
        ws=[units[k] for k in idx]; simple=nx.number_of_edges(S)==nx.number_of_edges(nx.Graph(S))
        iso=bool(len(cset)==24 and simple and all(w==1 for w in ws) and nx.is_isomorphic(X,nx.Graph(S)))
        sub=B[np.ix_(idx,idx)] if len(cset)==2*len(idx) else None
        comps.append(dict(vertices=len(cset),units=ws,torsion_free=all(w==1 for w in ws),simple=simple,
                          charpoly=str(sp.factor(sp.Matrix(sub).charpoly(sp.Symbol('t')).as_expr())) if sub is not None else 'n/a',
                          has_t4_4t2_1=(sub is not None and sp.rem(sp.Matrix(sub).charpoly(sp.Symbol('t')).as_expr(),sp.Symbol('t')**4-4*sp.Symbol('t')**2+1)==0),
                          isomorphic_to_X=iso))
    rec=dict(field=label,hplus=F.hplus,h=F.h,D=[int(G.idealnorm(nf,P)) for P in Ds],N=[(int(G.idealnorm(nf,P)),e) for P,e in Ns],
             v=str(G.idealtwoelt(nf,v)),classes=h,units=units,mass=str(mass),mass_formula=str(M),mass_ok=bool(mass==M),
             theta_agrees=theta,components=comps,any_X=any(c['isomorphic_to_X'] for c in comps))
    print(json.dumps(rec),flush=True)
    return rec
