"""Extension of the Cerednik-Drinfeld test to Gamma_H(N) level structures (H subgroup of (Z/N)^x containing -1):
reduction graph = bipartite graph with biadjacency the 2-Brandt operator B on the Gamma_H Brandt module; B is normal,
so the graph spectrum is +-|eigenvalues| = +-{3} u +-{|a_2(f)|}, f in S_2(Gamma_H(pN))^{p-new} (all even chars trivial on H)."""
import cypari2, sympy as sp, itertools, math, json, numpy as np
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
import importlib, sys, io
_o=sys.stdout; sys.stdout=io.StringIO(); from shimura import data, leg; sys.stdout=_o
TARGET=sorted([1,1,1,5**.5,5**.5,3**.5,3**.5]+[2*math.cos(math.pi/12)]*2+[2*math.cos(5*math.pi/12)]*2)
def units(N): return [a for a in range(1,N) if math.gcd(a,N)==1]
def subgroups_with_minus1(N):
    U=units(N); out=set()
    for gens in itertools.chain.from_iterable(itertools.combinations(U,r) for r in range(0,3)):
        H={1,N-1}; ch=True
        while ch:
            ch=False
            for a in list(H):
                for g in list(gens)+list(H):
                    b=a*g%N
                    if b not in H: H.add(b); ch=True
        out.add(frozenset(H))
    return out
res=[]
for p in sp.primerange(3,150):
    for N in range(3,150,2):
        if math.gcd(N,p)!=1: continue
        psi=N
        for q in sp.factorint(N): psi=psi*(q+1)//q
        if 144%((p-1)*psi): continue
        U=units(N); 
        for H in subgroups_with_minus1(N):
            idx=len(U)//len(H)
            if idx==1 or (p-1)*psi*idx!=144: continue
            g0,e2,e3,_=data(p,N)
            bad2=any((u*u+1)%N==0 for u in H); bad3=any(((u**3-1)%N==0 or (u**3+1)%N==0) and u not in (1,N-1) for u in H)
            free=(e2==0 or not bad2) and (e3==0 or not bad3)
            res.append((p,N,sorted(H),idx,free))
print('Gamma_H candidates with 24 components:',[(r[0],r[1],r[3],'free' if r[4] else 'torsion') for r in res])
def absa2(p,N,H):
    vals=[]
    for Mp in sp.divisors(p*N):
        if Mp%p: continue
        mult=len(sp.divisors(p*N//Mp)); G=pari(f'znstar({Mp},1)')
        for chi in pari.chargalois(G) if False else []: pass
        # enumerate all characters mod Mp via Conrey labels, keep those trivial mod p-part, trivial on H (mod N), even
        for a in units(Mp):
            c=pari(f'znconreychar(znstar({Mp},1),{a})')
            ok=True
            for u in units(Mp):
                v=float(pari(f'chareval(znstar({Mp},1),{c},{u})'))  # value as fraction of 1 (exponent)
                q=Mp//p if Mp%p==0 else Mp
                # u ≡ 1 mod q (the N part) must give trivial value (character is trivial on p-part)
                if u%(q if q>1 else 1)==1 % (q if q>1 else 1) and abs(v-round(v))>1e-9: ok=False;break
                if (q>1 and (u%q) in H) and abs(v-round(v))>1e-9: ok=False;break
            if not ok: continue
            mf=pari(f'mfinit([{Mp},2,Mod({a},{Mp})],0)'); d=int(pari.mfdim(mf))
            if d==0: continue
            # one representative per Galois orbit of characters; evaluate all embeddings
            o=int(pari(f'charorder(znstar({Mp},1),{c})'))
            orbit=sorted({pow(a,j,Mp) for j in range(1,o+1) if math.gcd(j,o)==1})
            if a!=orbit[0]: continue
            M=pari.mfheckemat(mf,2); cp=pari.charpoly(M)
            cpl=pari.liftall(cp)
            for j in range(1,max(o,1)+1):
                if math.gcd(j,o)!=1: continue
                z=pari(f'exp(2*Pi*I*{j}/{o})')
                P=pari.substvec(cpl,['t'],[z]) if o>2 else pari.substvec(cpl,['t'],[z])
                ev=[abs(complex(r)) for r in pari.polroots(P)]
                vals+= ev*mult
    return sorted(vals)
out=[]
for p,N,H,idx,free in res:
    v=absa2(p,N,set(H)); ok=len(v)==11 and np.allclose(v,TARGET,atol=1e-6)
    print(p,N,'idx',idx,'free' if free else 'torsion','#|a2|',len(v),[round(x,4) for x in v],'MATCH' if ok else '')
    out.append(dict(p=p,N=N,H=H,index=idx,torsion_free=free,abs_a2=v,match=bool(ok)))
json.dump(out,open('shimura_H.json','w'),indent=1)
