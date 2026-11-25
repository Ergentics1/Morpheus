"""Cerednik-Drinfeld test. For D=2p, the 2-adic reduction graph of the Shimura curve X_0^D(N) is the bipartite graph on
two copies of Cl(O_N) (Eichler order of level N in the definite algebra B_{p,inf}) with adjacency the Brandt matrix B(2)
(Ribet 1990). Its spectrum is +-{3} u +-{a_2(f) : f in S_2(Gamma_0(pN))^{p-new}} (Eichler / Jacquet-Langlands).
We enumerate all (p,N) whose curve has genus 13, and test whether the spectrum can equal the chord graph's."""
import cypari2, json, itertools, math, sympy as sp
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
def kron(a,q): return int(sp.jacobi_symbol(a%q,q)) if q>2 else {1:1,3:-1,5:-1,7:1}.get(a%8,0) if a%2 else 0
def leg(d,q):  # Kronecker (d/q) for d in {-3,-4}, q prime
    if q==2: return 0 if d==-4 else -1     # (-4/2)=0, (-3/2)=-1
    if d==-4: return 0 if q==2 else (1 if q%4==1 else -1)
    if q==3: return 0
    return 1 if q%3==1 else -1
def data(p,N):
    D=2*p; fN=sp.factorint(N)
    phiD=(2-1)*(p-1); psi=N
    for q in fN: psi=psi*(q+1)//q
    e2=1;e3=1
    for q in (2,p): e2*=1-leg(-4,q); e3*=1-leg(-3,q)
    for q in fN: e2*=1+leg(-4,q); e3*=(0 if (q==3 and fN[q]>=2) else 1+leg(-3,q))
    g=sp.Rational(1)+sp.Rational(phiD*psi,12)-sp.Rational(e2,4)-sp.Rational(e3,3)
    return g,e2,e3,psi
cands=[]
for p in sp.primerange(3,400):
    for N in range(1,400,2):
        if math.gcd(N,p)!=1: continue
        g,e2,e3,psi=data(p,N)
        if g==13: cands.append(dict(p=p,N=N,e2=e2,e3=e3,torsion_free=(e2==0 and e3==0),mass=sp.Rational((p-1)*psi,12)))
print('genus-13 curves X_0^{2p}(N):',[(c['p'],c['N'],'free' if c['torsion_free'] else f"e2={c['e2']},e3={c['e3']}") for c in cands])
x=sp.symbols('x')
target=sp.expand((x**2-1)**3*(x**2-5)**2*(x**2-3)**2*(x**4-4*x**2+1)**2)   # nontrivial part of chord graph charpoly
def t2poly(M):
    mf=pari(f'mfinit([{M},2],0)'); d=int(pari.mfdim(mf))
    if d==0: return sp.Integer(1),0
    cp=pari(f'charpoly(mfheckemat(mfinit([{M},2],0),2))'); return sp.sympify(str(cp).replace('^','**')),d
out=[]
for c in cands:
    p,N=c['p'],c['N']; tot=sp.Integer(1); dim=0
    for Mp in sp.divisors(p*N):
        if Mp%p: continue
        f,d=t2poly(Mp); mult=len(sp.divisors(p*N//Mp)); tot*=f**mult; dim+=d*mult
    tot=sp.expand(tot)
    # graph charpoly of the bipartite double: prod over eigen a of (x^2-a^2)  ->  compare with target
    sym=sp.expand(sp.resultant(tot.subs(x,sp.Symbol('y')),sp.Symbol('y')**2-x**2,sp.Symbol('y'))) if dim else 1
    # sym(x) = prod (x^2 - a_i^2) up to sign
    sym=sp.Poly(sym,x); sym=sp.expand(sym.as_expr()/sym.LC())
    match=sp.expand(sym-target)==0
    fac=sp.factor(tot)
    c.update(dim_pnew=dim,T2_charpoly=str(fac),spectrum_matches=bool(match))
    print(p,N,'free' if c['torsion_free'] else 'torsion','dim',dim,'T2:',fac,'MATCH' if match else '')
    out.append({k:(str(v) if isinstance(v,sp.Basic) else v) for k,v in c.items()})
json.dump(out,open('shimura.json','w'),indent=1)
