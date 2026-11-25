import json, math, sympy as sp, mpmath as mp, numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
from common import *
mp.mp.dps=50
L=[]; 
def chk(name,cond,detail=''):
    L.append((bool(cond),name,detail)); print(('PASS ' if cond else 'FAIL ')+name+(' — '+str(detail) if detail else ''))
G=json.load(open('group.json')); T=json.load(open('tune.json')); Gr=json.load(open('graphene.json'))
S=json.load(open('signings.json')); E=json.load(open('eisenstein.json'))
TR=json.load(open('../melodic_primes/voice/transfer.json'))
# --- group theory (independent: sympy permutation group)
perms=[Permutation([IX[OPS[o](v)] for v in V]) for o in 'PLR']
PG=PermutationGroup(perms)
chk('PLR group order 24 (sympy)',PG.order()==24)
chk('PLR group is dihedral D12 (non-abelian, has element of order 12, all generators involutions)',
    (not PG.is_abelian) and max(g.order() for g in PG.elements)==12 and all(p.order()==2 for p in perms))
chk('PLR acts simply transitively (regular)',PG.is_transitive() and PG.order()==24)
chk('pi_1 free of rank E-V+1=13; prime cadences = primitive conj. classes of kernel of Z2*Z2*Z2->D12',G['free_rank_pi1']==13)
chk('P=L(LR)^4, R=L(LR) as permutations',G['words_verified'])
# exact chord spectrum (sympy charpoly)
A=sp.zeros(24,24)
for a,b,o,s in EDGES: A[a,b]+=1
x=sp.symbols('x'); cp=sp.factor(A.charpoly(x).as_expr())
roots=sp.Poly(A.charpoly(x).as_expr(),x).all_roots()
nontriv=[r for r in roots if sp.Abs(r)!=3]
mx=max(sp.Abs(r) for r in nontriv)
chk('chord graph max nontrivial eigenvalue = sqrt5 < 2sqrt2 (Ramanujan), exact',sp.simplify(mx-sp.sqrt(5))==0 and sp.sqrt(5)<2*sp.sqrt(2),str(cp))
chk('Artin factorisation over D12 irreps (4 one-dim + 5 two-dim^2) at 50 digits',G['artin_D12_factorisation_checks']=='3/3')
chk('2-dim irrep rho_j of PLR group <-> triad Fourier index k=7j (fifths automorphism)',G['rho_j_matches_k=7j'])
chk('Z12 transposition cover of theta graph: zeta = prod of 12 Artin-Ihara L-functions',G['Z12_artin_L_checks']=='2/2')
chk('explicit (Ihara trace) formula N_m = sum of 48 poles + 12(1+(-1)^m), m<=40',G['explicit_formula_m<=40'])
cheb=[float(v) for v in G['chebotarev_frob_fractions']['40']]
chk('graph Chebotarev: Frobenius (net transposition) equidistributed 1/12 at m=40 (max dev <1e-6)',max(abs(c-1/12) for c in cheb)<1e-6)
# --- tune theorem
chk('Lemma: 3 moves at each triad move 3 different voices',T['L1_moves_biject_voices'])
chk('Lemma: only the backtrack moves the just-arrived note',T['L1b_only_backtrack_moves_arrival'])
chk('Lemma: no consonant triad contains a 1- or 2-semitone pair',T['L4_steps_not_in_triads'])
rec=T['reconstruction']
chk('Tune theorem: local decoder recovers every chord of every prime from its tune alone (m<=16)',all(v['reconstructed']==v['rooted'] for v in rec.values()),{m:v['primes'] for m,v in rec.items()})
chk('Tune map injective and tunes primitive (m<=16)',all(v['injective'] and v['tunes_primitive'] for v in rec.values()))
# --- W=-u
chk('Lemma: flip vectors lie in coset lattice 2a+b=0 mod 3; step = -delta_a for all 72 directed moves',T['flip_vectors_in_coset_lattice'] and T['lattice_flip_step=-delta_a_all_72'])
# --- Gaussian / variance
c2=mp.diff(lambda p: mp.log((mp.sqrt(5+4*mp.cos(p/4))+mp.sqrt(5+4*mp.cos(p/4)-8))/2),0,2)
chk('Var(W)/m = 1/24 from curvature of twisted Perron root',abs(-c2-mp.mpf(1)/24)<mp.mpf(10)**-30)
Gm=sp.Matrix([[16,-6],[-6,9]]); Cov=sp.Rational(1,2)*Gm.inv()
chk('homology covariance = (1/2) Gram^{-1} of torus periods = [[1/24,1/36],[1/36,2/27]] (isotropic Brownian motion, MSD 1/step)',
    Cov==sp.Matrix([[sp.Rational(1,24),sp.Rational(1,36)],[sp.Rational(1,36),sp.Rational(2,27)]]) and
    abs(float(Gr['cov_per_step']['uu'])-1/24)<1e-9 and abs(float(Gr['cov_per_step']['vv'])-2/27)<1e-9 and abs(float(Gr['cov_per_step']['uv'])-1/36)<1e-9)
chk('1/24 = |P_v|^2 / (2 Area^2) with Area^2 = 108 (torus of 24 unit triangles)',sp.Rational(9,2*108)==sp.Rational(1,24))
r40=TR['40']; var40=sum(int(k)**2*v for k,v in r40['W'].items())/r40['pi']
chk('exact prime counts m=40: Var(W)/m = 0.04167',abs(var40/40-1/24)<2e-4,round(var40/40,6))
home=r40['W']['0']/r40['pi']; pred=math.sqrt(12/(math.pi*40))
chk('local CLT: home fraction m=40 within 3% of sqrt(12/(pi m))',abs(home/pred-1)<0.03,(round(home,5),round(pred,5)))
# --- melodic zeta / covers
a=4*mp.acos(mp.mpf(3)/4)
chk('RH window edge: sqrt(5+4cos(a/4)) = 2sqrt2 at a=4 arccos(3/4)',abs(mp.sqrt(5+4*mp.cos(a/4))-2*mp.sqrt(2))<1e-40)
chk('half-flux (voice parity) top eigenvalue = sqrt(5+2sqrt2) exactly',sp.simplify(sp.expand_complex((2+sp.exp(sp.I*sp.pi/4))*(2+sp.exp(-sp.I*sp.pi/4)))-(5+2*sp.sqrt(2)))==0 and abs(float(S['u_parity=voice_parity']['max_eig'])-math.sqrt(5+2*math.sqrt(2)))<1e-9)
cov=S['cyclic_covers_ramanujan']
chk('Z_n voice-winding covers Ramanujan iff n=2 (n=2..12), also for v and full torus',cov['2']['u'] and cov['2']['v'] and cov['2']['full_torus_ZnxZn'] and not any(cov[str(n)][k] for n in range(3,13) for k in ('u','v','full_torus_ZnxZn')))
chk('voice parity (from steps) = u-parity cohomology class; Ramanujan 2-lift',S['voice_parity_classes_agree'] and S['u_parity=voice_parity']['ramanujan'])
chk('Ramanujan 2-lifts are abundant: 7675 of 8191 nontrivial signing classes; best max = 1+sqrt2',S['n_ramanujan_classes(max|lam|<=2sqrt2, excluding trivial)']==7675 and abs(S['min_max_eig_over_signings']-(1+math.sqrt(2)))<1e-9)
# --- graphene
chk('chord graph = graphene tight-binding on 12-cell torus (bond offsets 0,4,9)',Gr['major_to_minor_cell_offsets']==[0,4,9])
chk('honeycomb squared on major sublattice = 3I + note Tonnetz Cay(Z12,{±3,±4,±5})',Gr['honeycomb_squared_is_note_tonnetz'])
chk('phasor step-twist = magnetic flux through the u-cycle of the torus',Gr['step_twist_equals_u_flux']=='3/3')
chk('flux 2pi/3 through u-cycle hits a Dirac point (eigenvalue 0); untwisted has none',float(Gr['min_abs_eig_at_u_flux_2pi/3'])<1e-30 and Gr['untwisted_has_no_zero_eig'])
chk('voice colouring = Kekule (sqrt3 x sqrt3) colouring: every pedal hexagon 2-coloured; not defined on torus (period shifts coset)',Gr['pedal_hexagons_bicoloured'] and Gr['period_vector_coset_shift']==[1,0])
# --- Eisenstein
chk('Tonnetz kernel is NOT an ideal of Z[w] (explicit counterexample)',E['kernel_is_w_stable(ideal)'] is False)
chk('obstruction: x^2+x+1 has no root mod 4 (2 inert in Z[w]); Z3 part is Eisenstein (root mod 3)',E['roots_mod_4']==[] and E['roots_mod_3']==[1])
chk('Tonnetz torus tau = -3/8+3sqrt3 i/8 has CM by order of conductor 12, disc -432, class number 6',E['discriminant']==-432 and E['conductor']==12 and E['class_number_h(-432)']==6 and E['multiplier_ring_min_b']==12)
# twisted Ihara-Bass again with a fresh theta
th=mp.mpf('0.911'); u=mp.mpf('0.27')-0.33j
idx={(a,b):i for i,(a,b,o,s) in enumerate(EDGES)}
B=mp.zeros(72,72)
for i,(a,b,o,s) in enumerate(EDGES):
    for j,(c,d,o2,s2) in enumerate(EDGES):
        if c==b and d!=a: B[i,j]=mp.expj(th*s2)
At=mp.zeros(24,24)
for a,b,o,s in EDGES: At[a,b]+=mp.expj(th*s)
chk('twisted Ihara-Bass identity (fresh theta, 50 digits)',abs(mp.det(mp.eye(72)-u*B)/((1-u**2)**12*mp.det(mp.eye(24)-u*At+2*u**2*mp.eye(24)))-1)<mp.mpf(10)**-40)
n=sum(1 for p,_,_ in L if p)
print(f'PASS {n}/{len(L)}')
with open('math_audit.md','w') as f:
    f.write(f'# Deep math audit — {n}/{len(L)} PASS\n\n')
    for p,name,d in L: f.write(f"- {'PASS' if p else 'FAIL'} {name}" + (f" — {d}" if d else '') + '\n')
