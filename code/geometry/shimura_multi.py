"""All Cerednik-Drinfeld curves X_0^D(N) with 2|D, D=2m, m odd squarefree with an odd number of primes (so B_{m,inf} definite),
genus 13. Reduction graph at 2 = bipartite double of the 2-Brandt graph of level N in B_{m,inf}; its spectrum is
+-3 and +-a_2(f), f in S_2(Gamma_0(mN))^{m-new}. Compare with the chord graph."""
import cypari2, sympy as sp, math, json, numpy as np, itertools
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
TARGET=sorted([1,1,1,5**.5,5**.5,3**.5,3**.5]+[2*math.cos(math.pi/12)]*2+[2*math.cos(5*math.pi/12)]*2)
def leg(d,q):
    if q==2: return 0 if d==-4 else -1
    if d==-4: return 1 if q%4==1 else -1
    if q==3: return 0
    return 1 if q%3==1 else -1
cands=[]
P=list(sp.primerange(3,400))
for r in (1,3,5):
    for ps in itertools.combinations(P,r):
        phi=math.prod(q-1 for q in ps)
        if phi>12*14: continue
        m=math.prod(ps)
        for N in range(1,600,2):
            if math.gcd(N,m)!=1: continue
            fN=sp.factorint(N); psi=N
            for q in fN: psi=psi*(q+1)//q
            if phi*psi>12*40: continue
            e2=1;e3=1
            for q in (2,)+ps: e2*=1-leg(-4,q); e3*=1-leg(-3,q)
            for q in fN: e2*=1+leg(-4,q); e3*=(0 if (q==3 and fN[q]>=2) else 1+leg(-3,q))
            g=sp.Rational(1)+sp.Rational(phi*psi,12)-sp.Rational(e2,4)-sp.Rational(e3,3)
            if g==13: cands.append((ps,N,e2,e3))
print(len(cands),'genus-13 CD curves (2|D):')
out=[]
for ps,N,e2,e3 in cands:
    m=math.prod(ps); vals=[]
    for Mp in sp.divisors(m*N):
        if Mp%m: continue
        mf=pari(f'mfinit([{Mp},2],0)')
        if int(pari.mfdim(mf))==0: continue
        cp=pari.charpoly(pari.mfheckemat(mf,2))
        vals+= [abs(float(pari.real(z))) for z in pari.polroots(cp)]*len(sp.divisors(m*N//Mp))
    vals=sorted(vals); ok=len(vals)==11 and np.allclose(vals,TARGET,atol=1e-6)
    print('D=',2*m,ps,'N=',N,'torsion-free' if e2==e3==0 else f'e2={e2},e3={e3}','#',len(vals),[round(v,3) for v in vals],'MATCH' if ok else '')
    out.append(dict(D=2*m,primes=ps,N=N,e2=e2,e3=e3,abs_a2=vals,match=bool(ok)))
json.dump(out,open('shimura_multi.json','w'),indent=1)
print('any match:',any(o['match'] for o in out))
