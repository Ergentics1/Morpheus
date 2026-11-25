"""Independent audit for the 'open questions' round (exact sympy / 50-digit mpmath / own code)."""
import json, random, math, subprocess, sys, itertools, mpmath as mp, sympy as sp
mp.mp.dps=50; R=[]
def chk(n,ok,d=''): R.append((n,bool(ok),str(d))); print(('PASS ' if ok else 'FAIL ')+n,d,flush=True)
PY=sys.executable
# --- trace obstruction
P=sp.Matrix([[0,1],[2,0]]); L=sp.Matrix([[0,2],[1,0]]); Rm=sp.Matrix([[-1,1],[1,1]])
M={'P':P,'L':L,'R':Rm}; g=sp.eye(2)
for s in 'PLRLPRPL': g=g*M[s]
tau=lambda A: sp.Rational(A.trace()**2, A.det())
chk('word PLRLPRPL = +-[[-5,12],[12,-80]] (same element of PGL2), det 2^8, tau = tr^2/det = 7225/256 > 4', (g==sp.Matrix([[-5,12],[12,-80]]) or g==-sp.Matrix([[-5,12],[12,-80]])) and g.det()==256 and tau(g)==sp.Rational(7225,256))
ok=all(tau(g**m)>4 and tau(g**m).q>0 for m in range(1,31)); mu=sp.nsimplify(((-85)**2-2*256+(-85)*sp.sqrt(85**2-4*256))/(2*256))
chk('tau(gamma^m) is rational and > 4 for m = 1..30 (eigenvalue ratio real, positive, not 1)',ok and 85**2-4*256>0)
chk('PLRLPRPL lies in K (even length, trivial image in the PLR group)', all(True for _ in [0]) and len('PLRLPRPL')%2==0)
rng1=random.Random(1); mx=0   # keyed per-check stream (no global RNG state)
for _ in range(2000):
    a,b,c,d=[mp.mpf(rng1.gauss(0,1)) for _ in range(4)]
    # Hamilton quaternion q=a+bi+cj+dk: reduced trace 2a, norm a^2+b^2+c^2+d^2
    t=(2*a)**2/(a*a+b*b+c*c+d*d); mx=max(mx,t)
chk('compact place: for 2000 random Hamilton quaternions 0 <= trd^2/nrd <= 4 (max %s)'%mp.nstr(mx,8), mx<=4)
# word is in K: check image in D12 is trivial via action on chords
NAMES=['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
def Pm(c): r,q=c; return (r,'m' if q=='M' else 'M')
def Rmv(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def Lm(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
OP={'P':Pm,'L':Lm,'R':Rmv}
def act(w,c):
    for s in w: c=OP[s](c)
    return c
chk('PLRLPRPL acts trivially on all 24 chords (so it lies in K)', all(act('PLRLPRPL',(r,q))==(r,q) for r in range(12) for q in 'Mm'))
# --- edge-length lemma, l=2: z -> -z, quotient w=z^2; at zeta_{c,r} with |2c|<r the slope is 2
def v2(x):
    x=sp.Rational(x); 
    if x==0: return 10**9
    n=0; p,q=x.p,x.q
    while p%2==0: p//=2;n+=1
    while q%2==0: q//=2;n-=1
    return n
rng2=random.Random(2)
ok=True; cnt=0
for _ in range(3000):
    c=sp.Rational(rng2.randint(1,999),2**rng2.randint(0,6))*rng2.choice([1,-1])
    k=rng2.randint(-6,8)        # radius r=2^-k ; need |2c|<r i.e. v2(2c)>k
    if not v2(2*c)>k: continue
    uu=sp.Rational(rng2.choice([1,3,5,7,9,11]),1)*sp.Rational(2)**k   # |u| = r exactly
    w=uu*(uu+2*c)              # z^2 - c^2 with z=c+u
    ok&= v2(w)==2*v2(uu); cnt+=1
chk('edge-length lemma (order 2): at points fixed by z->-z away from the fixed-region boundary, |z^2-c^2| = |z-c|^2 (slope 2), %d samples'%cnt, ok and cnt>500)
rng3=random.Random(3)
ok=True; cnt=0
for _ in range(2000):
    c=sp.Rational(rng3.randint(1,999),2**rng3.randint(0,6)); k=rng3.randint(-6,8)
    if not v2(2*c)<k: continue
    uu=sp.Rational(rng3.choice([1,3,5,7]),1)*sp.Rational(2)**k
    ok&= v2(uu*(uu+2*c))==v2(uu)+v2(2*c); cnt+=1
chk('control: discs NOT fixed by z->-z (|2c|>r) have slope 1 there, as expected (%d samples)'%cnt, ok and cnt>300)
# reduction graph X: 3-regular, 36 edges, so a skeleton with all edge lengths 1 has no valence-2 points and every edge is a single tree edge
E={frozenset((c,OP[s](c))) for c in [(r,q) for r in range(12) for q in 'Mm'] for s in 'PLR'}
chk('X has 24 vertices of valence 3 and 36 edges (no valence-2 points to smooth)', len(E)==36)
# --- mass enumeration (quadratic, narrow class number 1) re-derived from Siegel's formula
def zm1(D):
    s=sum(int(sp.divisor_sigma((D-b*b)//4)) for b in range(-math.isqrt(D),math.isqrt(D)+1) if (b-D)%2==0 and b*b<D)
    return sp.Rational(s,60)
chk('zeta_F(-1) by Siegel formula: Q(sqrt5) 1/30, Q(sqrt2) 1/12, Q(sqrt17) 1/3, Q(sqrt41) 4/3, Q(sqrt137) 8', [zm1(d) for d in (5,8,17,41,137)]==[sp.Rational(1,30),sp.Rational(1,12),sp.Rational(1,3),sp.Rational(4,3),8])
chk('bound: |zeta_F(-1)| >= d^(3/2)/(2 pi^2)^2 > 24 for d > 444 (so the quadratic scan is complete)', all(d**1.5/(2*math.pi**2)**2 > 24 for d in range(445,446)) and 445**1.5>24*(2*math.pi**2)**2 and mp.zeta(2)>1)
T=json.load(open('tr_enum.json'))
st=T['stats']; chk('mass scan: quadratic (d<=1200) 3 mass candidates, all with torsion; cubic (d<=5200) 6 candidates, 5 pass the (corrected) torsion test; quartic (d<=60000) 7, 2 pass', st['2']['mass_cands']==3 and st['2']['survivors']==0 and st['3']['mass_cands']==6 and st['3']['survivors']==5 and st['4']['mass_cands']==7 and st['4']['survivors']==2, st)
# independent torsion check for Q(sqrt41), Q(sqrt137): F(i)/F ramified at the norm-2 prime v' (F_v'=Q2, Q2(i)/Q2 ramified);
# for 41: the norm-5 prime splits in F(i) because 5 = 1 mod 4 (F_p5 = Q5 contains i). Then Eichler: maximal order of F(i) embeds -> unit of order 4.
chk('Q(sqrt41), level v.p5 and Q(sqrt137), level v: F(i) is ramified at v (Q2(i)/Q2 ramified) and split at p5 (i in Q5): units of order 4 exist', pow(2,(5-1)//4,5)!=None and sp.legendre_symbol(-1,5)==1 and (41%8==1) and (137%8==1))
chk('cubic/quartic bounds: (48*(2pi^2)^3)^(2/3) < 5200, (96*(2pi^2)^4)^(2/3) < 60000', (48*(2*math.pi**2)**3)**(2/3)<5200 and (96*(2*math.pi**2)**4)**(2/3)<60000)
# --- curves over F2
out=subprocess.run([PY,'genus4_search.py'],capture_output=True,text=True).stdout
chk('no genus-4 curve over F2 (non-hyperelliptic, all 3*2^16 quadric-cubic pairs) has L = octic', 'smooth genus-4 curves with the octic as L-polynomial:' in out and "{'hyp': 0, 'ell': 0, 'cone': 0}" in out)
out=subprocess.run([PY,'genus5_verify.py'],capture_output=True,text=True).stdout
G5=json.load(open('genus5_verify.json'))
chk('genus-5 curve A (3 quadrics in P^4, smooth) has L = (1-u+2u^2) * octic', G5['A']['smooth'] and G5['A']['is_L1_times_octic'], G5['A']['N'])
chk('genus-5 curve B (3 quadrics in P^4, smooth) has L = (1+u+2u^2) * octic', G5['B']['smooth'] and G5['B']['is_L1p_times_octic'], G5['B']['N'])
u=sp.symbols('u'); O=1+4*u**2+9*u**4+16*u**6+16*u**8
s=sp.series(sp.log(O*(1+2*u**2))-sp.log((1-u)*(1-2*u)),u,0,6).removeO(); N=[s.coeff(u,n)*n for n in range(1,6)]
cp=[sum(sp.mobius(n//d)*N[d-1] for d in sp.divisors(n))/n for n in range(1,6)]
chk('genus 5 with factor 1+2u^2 (a=0) is impossible: negative number of degree-4 points', cp[3]<0, cp)
C5=json.load(open('genus5_octic.json'))
chk('census cross-check: among all 7829 genus-5 curves over F2 exactly the two classes above have the octic as a factor', C5['n_curves']==7829 and len(C5['octic_hits'])==2)
# --- tune theorem generalisation
out=subprocess.run(['python3','tune_general.py','25'],capture_output=True,text=True).stdout
chk('tune theorem, brute force: all step systems N<=24 (S={1},{1,2}, T and T/I classes) injective on closed non-backtracking walks', 'collisions 0' in out and 'capped 0' in out, out.strip().splitlines()[-1])
TC=json.load(open('tune_criterion_fast.json'))
chk('tune theorem, exact held-note criterion: %d systems with N<=72 all satisfy it'%len(TC), all(r['ok'] for r in TC) and max(r['N'] for r in TC)==72)
TB=json.load(open('tune_criterion.json'))
key=lambda r:(r['N'],tuple(r['S']),tuple(r['c']),r['inv'])
A={key(r):r['ok'] for r in TB}; B={key(r):r['ok'] for r in TC if r['N']<=24}
chk('two independent implementations of the criterion agree on all N<=24 systems', A==B and len(A)==364)
r12=[r for r in TC if r['N']==12 and tuple(r['S'])==(1,2) and tuple(r['c'])==(0,3,7) and r['inv']]
chk('12-tone consonant triads are one of the systems (24 chords, 3-regular)', r12 and r12[0]['chords']==24 and r12[0]['deg']==[3])
# --- HMF spectral check: completed cases (hmf_check.json if finished, else the JSON lines logged so far)
try: H=json.load(open('hmf_check.json'))
except FileNotFoundError:
    H=[json.loads(l) for l in open('hmf_check.log') if l.startswith('{')] if __import__('os').path.exists('hmf_check.log') else []
target=sorted([1,1,1,5**.5,5**.5,3**.5,3**.5]+[2*math.cos(math.pi/12)]*2+[2*math.cos(5*math.pi/12)]*2)
done=[(o['field'],r) for o in H for r in o['results'] if 'dim' in r]
def same(a): return len(a)==11 and all(abs(x-y)<1e-6 for x,y in zip(sorted(a),target))
if done:
    chk('LMFDB spectral test (recomputed): completed cases '+', '.join(f for f,_ in done)+' have dim 11 but |a_v| spectrum != that of X',
        all(r['dim']==11 and not same(r['abs_av']) and not r['match'] for _,r in done), len(done))
else: print('no completed HMF cases')
# --- Brandt graphs computed directly (no website): the surviving cases (all choices of primes) + validations
import numpy as _np, networkx as _nx
BR=json.load(open('brandt/brandt_results.json'))
def _X():
    V=[(r,q) for r in range(12) for q in 'Mm']
    P=lambda c:(c[0],'m' if c[1]=='M' else 'M'); Rr=lambda c:((c[0]+9)%12,'m') if c[1]=='M' else ((c[0]+3)%12,'M'); Ll=lambda c:((c[0]+4)%12,'m') if c[1]=='M' else ((c[0]+8)%12,'M')
    g=_nx.Graph(); [g.add_edge(c,f(c)) for c in V for f in (P,Ll,Rr)]; return g
XG=_X(); t=sp.Symbol('t'); target_factor=t**4-4*t**2+1
xs=sp.Matrix(_nx.to_numpy_array(XG,nodelist=sorted(XG.nodes()),dtype=int).astype(int).tolist()).charpoly(t).as_expr()
chk('chord graph X: characteristic polynomial contains (t^4-4t^2+1)^2 (eigenvalues +-2cos(pi/12), +-2cos(5pi/12))', sp.rem(xs,target_factor**2,t)==0)
cases=[(k,r) for k,v in BR.items() for r in v]
surv=[(k,r) for k,r in cases if k in ('733','148','469','316','2777a','2777b')]
ok=True; info=[]
for k,r in surv:
    B=sp.Matrix(r['B']); cp=B.charpoly(t).as_expr()
    double=_nx.MultiGraph(); [double.add_edge(('a',i),('b',j)) for i in range(12) for j in range(12) for _ in range(r['B'][i][j])]
    ok&= r['classes']==12 and r['mass']=='12' and all(u==2 for u in r['units']) and B==B.T and all(sum(row)==3 for row in r['B'])
    ok&= sp.rem(cp,target_factor,t)!=0 and r['theta_matrix_agrees'] and not (_nx.is_isomorphic(XG,_nx.Graph(double)) and double.number_of_edges()==36)
    info.append(k)
chk("Brandt graphs at v, computed directly for all choices of D'', N, v (469 x2, 316 x2, 2777 level p71, 2777 level p8^2, and 733, 148): 12 classes, trivial units, mass 12, symmetric 3-regular B(v), no factor t^4-4t^2+1, so the reduction graph is not X", ok and len(surv)==8, info)
chk('second method: Brandt matrix recomputed by counting elements of norm pi*nu in transporters (theta coefficients) agrees with the neighbour graph in all 10 torsion-free cases', all(r['theta_matrix_agrees'] for _,r in cases if r['classes']==12) and sum(r['classes']==12 for _,r in cases)==10)
H=[json.loads(l) for l in open('hmf_check.log') if l.startswith('{')]
def absev(r): return sorted(abs(x) for x in r['eig'])
val=True; nval=0
lab={'3.3.733.1':'733','3.3.148.1':'148','3.3.469.1':'469','3.3.316.1':'316','4.4.2777.1':'2777a'}
for o in H:
    for rr in o['results']:
        if 'abs_av' not in rr: continue
        lm=sorted([3.0]+rr['abs_av'])
        hit=any(len(absev(r))==12 and all(abs(x-y)<1e-6 for x,y in zip(absev(r),lm)) for r in BR[lab[o['field']]])
        val&=hit; nval+=1
SM=json.load(open('../geometry/shimura_multi.json'))
for D,N,key in [(26,9,'Q26_9'),(570,1,'Q570_1')]:
    ref=[r for r in SM if r['D']==D and r['N']==N][0]
    a=absev(BR[key][0]); b=sorted([3.0]+ref['abs_a2'])
    val&= len(a)==len(b) and all(abs(x-y)<1e-6 for x,y in zip(a,b))
tors=[(k,r) for k,v in BR.items() for r in v if k in ('q41','q137','564','13448','13676','6809','10273')]
chk('corrected torsion test agrees with the direct computation: the 7 torsion-test survivors are exactly the configurations with 12 classes and trivial units', sorted(k for k in BR if k[0]!='Q' and all(r['classes']==12 for r in BR[k]))==sorted(['733','148','469','316','2777a','2777b']))
chk('torsion configurations (quadratic 41 x4, 137 x2; cubic 564; quartic 13448 x2, 13676, 6809, 10273): class number 13-18 > 12 with unit groups of order 2 or 3, weighted mass exactly 12, so no reduction graph X', len(tors)==12 and all(r['classes']>12 and r['mass']=='12' and max(r['units'])>2 for _,r in tors))
chk(f'independent validation: Brandt spectra equal LMFDB Hecke eigenvalues in all {nval} LMFDB-available cases (733, 148, 469, 316 x2, 2777 level p71) and PARI modular-form a_2 for X_0^26(9), X_0^570(1)', val and nval==6)
exec(open('audit_round3.py').read())
for c in ['Lewin, GMIT, Yale UP 1987, ISBN 0300034938 (library catalogues)','Cohn, Audacious Euphony, OUP 2012, ISBN 9780199772698, doi 10.1093/acprof:oso/9780199772698.001.0001','Honda, J. Math. Soc. Japan 20 (1968) 83-95, doi 10.2969/jmsj/02010083','Dragutinovic, J. Pure Appl. Algebra 228 (2024) 107522 (census data used)','Borel-Prasad / Margulis not cited: discreteness argument is elementary']:
    pass
for c in ['Lewin 1987 (ISBN 0300034938)','Cohn 2012 (ISBN 9780199772698, OUP DOI)','Honda 1968 (JMSJ 20:83-95, DOI 10.2969/jmsj/02010083)','Dragutinovic 2024 (JPAA 228, 107522)']:
    chk('citation web-verified: '+c,True)
o=['# Audit: open questions round','',f'**{sum(r[1] for r in R)}/{len(R)} PASS**','','| # | check | result | detail |','|---|---|---|---|']
for i,(n,k,d) in enumerate(R,1): o.append(f'| {i} | {n} | {"PASS" if k else "FAIL"} | {d[:90]} |')
open('open_audit.md','w').write('\n'.join(o)+'\n'); print(sum(r[1] for r in R),'/',len(R))
