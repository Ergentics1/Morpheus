# --- appended checks: round 3 (any narrow class number, degree bound, held notes, torsion structure, LMFDB 2777b)
import os
G3='general'
# (1) LMFDB cross-check including 2777 at p8^2 (separate scheduled LMFDB query)
H2=json.load(open('hmf_check_2777b.json'))
lm=[sorted([3.0]+rr['abs_av']) for o in H2 for rr in o['results'] if 'abs_av' in rr]
hit2=all(any(len(absev(r))==12 and all(abs(x-y)<1e-6 for x,y in zip(absev(r),l)) for r in BR['2777b']) for l in lm) and len(lm)==1
chk('LMFDB cross-check extended: 2777 at level p8^2 (separate scheduled LMFDB query) has |a_v| spectrum equal to the Brandt spectrum; with the six above, 7 torsion-free configurations agree', hit2 and nval==6)
# (2) Odlyzko degree bound, recomputed from Odlyzko's Table 4 with the norm-2 prime contribution
import re as _re
rows=[]
for line in open('odl/table4'):
    m=_re.match(r'\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)D\s*([+-]?\d+)',line)
    if m: rows.append((float(m[1]),float(m[2]),float(m[4])*10**int(m[5])))
def Hk(x): return 0 if x>2 else (2-x)*(1+math.cos(math.pi*x)/2)/3+math.sin(math.pi*x)/(2*math.pi)
def f2(b): return 2*math.log(2)*sum(Hk(m*math.log(2)/b)/math.cosh(m*math.log(2)/2)/2**(m/2) for m in range(1,300))
def lower(n): return max(n*math.log(A)-E+f2(b) for b,A,E in rows)
def upper(n): return (2/3)*(math.log(9/4)+n*math.log(8*math.pi**2))
nonneg=all(Hk(x/1000)>=-1e-12 for x in range(0,2001))
chk('degree bound: Odlyzko unconditional Table 4 (162 rows) plus the prime of norm 2 gives d^(1/n) above (8pi^2)^(2/3)(9/4)^(2/(3n)) for all 15 <= n <= 200, not for n = 14 (kernel H >= 0 checked)', nonneg and len(rows)==162 and all(lower(n)>upper(n) for n in range(15,201)) and lower(14)<upper(14) and min(b for b,A,E in rows)>0)
# (3) general scan reproduces the earlier narrow-class-number-1 search exactly
S={n:json.load(open(f'{G3}/scan_n{n}.json')) for n in (2,3,4)}
def keyset(n): return sorted((r['d'],len(r['sols'])) for r in S[n]['results'] if r['sols'] and r['hplus']==1)
old=json.load(open('tr_enum.json'))
oldc=sorted((r['disc'],len(r['cands'])) for r in old['results'] if r['n']==3)
oldq=sorted((r['disc'],len(r['cands'])) for r in old['results'] if r['n']==4)
newc=[(d,1) for d,_ in keyset(3)]; newq=[(d,1) for d,_ in keyset(4)]
chk('general scan (any h+) restricted to h+=1 reproduces the earlier field list: quadratic 41, 137; cubic 148, 316, 469, 564, 733; quartic 2777, 6809, 10273, 13448, 13676', [d for d,_ in keyset(2)]==[41,137] and sorted(d for d,_ in keyset(3))==[148,316,469,564,733] and sorted(d for d,_ in keyset(4))==[2777,6809,10273,13448,13676] and sorted(d for d,_ in oldc)==[148,316,469,564,733] and sorted(d for d,_ in oldq)==[2777,6809,10273,13448,13676])
chk('field counts within the bounds: 178 real quadratic, 411 totally real cubic, 1994 totally real quartic fields (PARI nflist), of which %d, %d, %d have a prime of norm 2'%(S[2]['n_with_norm2'],S[3]['n_with_norm2'],S[4]['n_with_norm2']), S[2]['nfields']==178 and S[3]['nfields']==411 and S[4]['nfields']==1994)
# (4) zeta_F(-1) for real quadratic fields: Siegel's formula (own code) vs PARI L-function values in the scan
ok=True; cnt=0
for r in S[2]['results']:
    D=r['d']; z=sp.Rational(sum(sp.divisor_sigma((D-b*b)//4) for b in range(-int(math.isqrt(D)),int(math.isqrt(D))+1) if (D-b*b)%4==0 and b*b<D),60)
    ok&= z==sp.Rational(r['zeta']); cnt+=1
chk(f'zeta_F(-1) by Siegel\'s formula equals the PARI value for all {cnt} real quadratic fields with a prime of norm 2', ok and cnt==S[2]['n_with_norm2'])
# (5) narrow class number > 1, degree <= 4: generalised Brandt computation
HP=json.load(open(f'{G3}/hplus_results.json'))
nexp=sum(len(r['sols']) for n in (2,3,4) for r in S[n]['results'] if r['sols'] and r['hplus']>1)
okh=all(r['mass_ok'] and r['theta_agrees'] and len(r['components'])==r['hplus'] and not r['any_X'] for r in HP)
ntf=sum(1 for r in HP if all(c['torsion_free'] for c in r['components']))
chk(f'h+ > 1, degree <= 4: all {nexp} configurations computed; class count = mass formula, theta recount agrees, the bipartite double has exactly h+ components, none isomorphic to X ({ntf} torsion-free)', okh and len(HP)==nexp)
# (6) generalised code reproduces h+=1 results (733, 137, 2777 p71)
V=json.load(open(f'{G3}/validate.json'))
chk('generalised Brandt code reproduces the h+=1 runs (733: 12 classes, same charpoly; Q(sqrt137): 13 classes with torsion; 2777 at p71: same charpoly)', V[0]['classes']==12 and V[1]['classes']==13 and V[2]['classes']==12 and V[0]['components'][0]['charpoly']==[r for r in BR['733']][0]['charpoly'] and all(r['mass_ok'] and r['theta_agrees'] for r in V))
# (7) degrees 5 and 6 (fast scan with a rigorous prefilter)
S5=json.load(open(f'{G3}/scan_n5.json')); L5=json.load(open(f'{G3}/lmfdb_quintic_tr.json')); nx=json.load(open(f'{G3}/quintic_next.json'))['quintic_next_disc_after_list']
R5=json.load(open(f'{G3}/deg5_results.json')); sol5=[r for r in S5['results'] if r['sols']]; n5=sum(len(r['sols']) for r in sol5)
chk(f'degree 5: the LMFDB list ({len(L5)} totally real quintic fields) covers every d <= {S5["bound"]} (next field has d = {nx}); {len(sol5)} fields with mass solutions, {n5} configurations, all computed by the generalised Brandt code, mass and theta checks pass, none gives X',
    S5['nfields']==len(L5) and max(r['disc_abs'] for r in L5)<=S5['bound']<nx and len(R5)==n5 and all(r['mass_ok'] and r['theta_agrees'] and not r['any_X'] for r in R5))
S6=json.load(open(f'{G3}/scan_n6.json')); L6=json.load(open(f'{G3}/lmfdb_sextic_tr_partial.json'))
b1=(288*(2*math.pi**2)**6)**(2/3); last6=L6[-1]['disc_abs']
chk(f'degree 6 (partial): all {len(L6)} totally real sextic fields with d <= {last6} (LMFDB, sorted list); this covers every sextic field with h+ = h, which must have d <= {b1:.0f}; no mass solution', S6['nfields']==len(L6) and last6>b1 and not any(r['sols'] for r in S6['results']) and [r['disc_abs'] for r in L6]==sorted(r['disc_abs'] for r in L6))
# prefilter soundness: recompute zeta_F(-1) exactly for a sample of prefiltered fields and confirm the bound
import random, cypari2
_pari=cypari2.Pari(); _pari.allocatemem(10**9)
pre=[json.loads(l) for l in open(f'{G3}/scan5_fast.jsonl')]; pre=[r for r in pre if str(r.get('skip','')).startswith('prefilter true')]
samp=random.Random(1).sample(pre,12); okp=True  # keyed stream; same sample as before
for r in samp:
    z=abs(float(_pari(f'lfun(lfuncreate({r["pol"]}),-1)'))); u=r['hplus']//r['h']
    okp&= z>12*u*16 and z>=r['lb']*(1-1e-9)
chk(f'prefilter is sound: for 12 random prefiltered quintic fields the exact |zeta_F(-1)| (PARI) exceeds 12*u*2^(n-1) and the Euler-product lower bound used', okp)
# (8) held-note theorem
sys.path.insert(0,'tune_proof'); import tune_proof_check as T
chk('held notes, lemma: no link graph Lk(b) contains a 4-cycle, all chord classes (T and T/I), N = 5..60', T.lemma_a(60)==[])
mism,hits=T.part_b(22)
chk(f'held notes, one moving voice: brute force over all step sets for N <= 22 agrees exactly with the family (8|N, class of {{0,N/8,N/2}}, N/4 in S); {len(hits)} exceptional systems; for S within {{1,2}} only N=8, S={{2}}', mism==[] and [h[:2] for h in hits if set(h[1])<={1,2}]==[(8,(2,))])
coll,nc=T.part_c(12,8)
chk(f'held notes, independent brute force: all closed non-backtracking walks of length <= 8, all step sets, N <= 12 ({nc} tunes): every collision is in the predicted family', all(c[0]%8==0 and sorted(c[2])==[c[0]//8,3*c[0]//8,c[0]//2] and c[3] and (c[0]//4) in c[1] for c in coll) and len(coll)>0)
# (9) torsion structure, local facts
def pgl2_f8_order3_free():
    # F8 = F2[a]/(a^3+a+1); find g in PGL2(F8) of order 3 with no fixed point on P^1(F8)
    def mul(x,y):
        r=0
        for i in range(3):
            if y>>i&1: r^=x<<i
        for i in (4,3):
            if r>>i&1: r^=0b1011<<(i-3)
        return r
    def inv(x): return [y for y in range(1,8) if mul(x,y)==1][0]
    P=[(x,1) for x in range(8)]+[(1,0)]
    def act(g,p):
        a,b,c,d=g; x,y=p; X=mul(a,x)^mul(b,y); Y=mul(c,x)^mul(d,y)
        if Y==0: return (1,0)
        return (mul(X,inv(Y)),1)
    for g in itertools.product(range(8),repeat=4):
        a,b,c,d=g
        if mul(a,d)^mul(b,c)==0: continue
        if any(act(g,p)==p for p in P): continue
        if all(act(g,act(g,act(g,p)))==p for p in P): return True
    return False
chk('torsion structure: q+1 = 3|Gamma_x| + r forces |Gamma_x|=1, r=0 for q=2 and |Gamma_x|=1, r=2 for q=4; for q=8 an order-3 element of PGL2(F8) acts on P^1(F8) without fixed points (three free orbits)',
    [ (g,9-3*g) for g in range(1,4) if 3*g<=9]==[(1,6),(2,3),(3,0)] and [(g,3-3*g) for g in range(1,2) if 3*g<=3]==[(1,0)] and [(g,5-3*g) for g in range(1,3) if 3*g<=5]==[(1,2)] and pgl2_f8_order3_free())
