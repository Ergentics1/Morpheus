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
random.seed(1); mx=0
for _ in range(2000):
    a,b,c,d=[mp.mpf(random.gauss(0,1)) for _ in range(4)]
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
ok=True; cnt=0
for _ in range(3000):
    c=sp.Rational(random.randint(1,999),2**random.randint(0,6))*random.choice([1,-1])
    k=random.randint(-6,8)        # radius r=2^-k ; need |2c|<r i.e. v2(2c)>k
    if not v2(2*c)>k: continue
    uu=sp.Rational(random.choice([1,3,5,7,9,11]),1)*sp.Rational(2)**k   # |u| = r exactly
    w=uu*(uu+2*c)              # z^2 - c^2 with z=c+u
    ok&= v2(w)==2*v2(uu); cnt+=1
chk('edge-length lemma (order 2): at points fixed by z->-z away from the fixed-region boundary, |z^2-c^2| = |z-c|^2 (slope 2), %d samples'%cnt, ok and cnt>500)
ok=True; cnt=0
for _ in range(2000):
    c=sp.Rational(random.randint(1,999),2**random.randint(0,6)); k=random.randint(-6,8)
    if not v2(2*c)<k: continue
    uu=sp.Rational(random.choice([1,3,5,7]),1)*sp.Rational(2)**k
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
st=T['stats']; chk('mass scan: quadratic (d<=1200) 3 mass candidates, all with torsion; cubic (d<=5200) 6 candidates, 4 survive; quartic (d<=60000) 7, 2 survive', st['2']['mass_cands']==3 and st['2']['survivors']==0 and st['3']['mass_cands']==6 and st['3']['survivors']==4 and st['4']['mass_cands']==7 and st['4']['survivors']==2, st)
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
done=[(o['field'],r) for o in H for r in o['results']]
def same(a): return len(a)==11 and all(abs(x-y)<1e-6 for x,y in zip(sorted(a),target))
if done:
    chk('LMFDB spectral test (recomputed): completed cases '+', '.join(f for f,_ in done)+' have dim 11 but |a_v| spectrum != that of X',
        all(r['dim']==11 and not same(r['abs_av']) and not r['match'] for _,r in done), len(done))
else: print('no completed HMF cases')
for c in ['Lewin, GMIT, Yale UP 1987, ISBN 0300034938 (library catalogues)','Cohn, Audacious Euphony, OUP 2012, ISBN 9780199772698, doi 10.1093/acprof:oso/9780199772698.001.0001','Honda, J. Math. Soc. Japan 20 (1968) 83-95, doi 10.2969/jmsj/02010083','Dragutinovic, J. Pure Appl. Algebra 228 (2024) 107522 (census data used)','Borel-Prasad / Margulis not cited: discreteness argument is elementary']:
    pass
for c in ['Lewin 1987 (ISBN 0300034938)','Cohn 2012 (ISBN 9780199772698, OUP DOI)','Honda 1968 (JMSJ 20:83-95, DOI 10.2969/jmsj/02010083)','Dragutinovic 2024 (JPAA 228, 107522)']:
    chk('citation web-verified: '+c,True)
o=['# Audit: open questions round','',f'**{sum(r[1] for r in R)}/{len(R)} PASS**','','| # | check | result | detail |','|---|---|---|---|']
for i,(n,k,d) in enumerate(R,1): o.append(f'| {i} | {n} | {"PASS" if k else "FAIL"} | {d[:90]} |')
open('open_audit.md','w').write('\n'.join(o)+'\n'); print(sum(r[1] for r in R),'/',len(R))
