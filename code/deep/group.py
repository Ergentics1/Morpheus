# 1. PLR group, Coxeter cover, kernel rank, irreps / Artin factorisation, explicit formula
import sympy as sp, mpmath as mp, json
from common import *
mp.mp.dps=50
res={}
perm={o:tuple(IX[OPS[o](v)] for v in V) for o in 'PLR'}
comp=lambda a,b: tuple(a[b[i]] for i in range(24))   # a after b
idp=tuple(range(24))
G={idp}; frontier=[idp]
while frontier:
    nf=[]
    for g in frontier:
        for o in 'PLR':
            h=comp(perm[o],g)
            if h not in G: G.add(h); nf.append(h)
    frontier=nf
res['order']=len(G)
s=comp(perm['L'],perm['R']); t=perm['L']
def pw(g,n):
    out=idp
    for _ in range(n): out=comp(g,out)
    return out
order_s=next(n for n in range(1,25) if pw(s,n)==idp)
res['LR_order']=order_s
res['dihedral_relation']= comp(comp(t,s),t)==pw(s,order_s-1)
res['simply_transitive']= len({g[IX[(0,'M')]] for g in G})==24
res['P_equals_t_s4']= perm['P']==comp(t,pw(s,4)) or perm['P']==comp(pw(s,4),t)
# which convention holds
res['P=L(LR)^4 ?']= perm['P']==comp(t,pw(s,4)); res['R=L(LR)?']= perm['R']==comp(t,s)
# Cayley graph identification: triad g.C <-> g ; neighbours via left mult by P,L,R
# Coxeter: rank of kernel = E - V + 1
res['free_rank_pi1']=36-24+1
# 2-dim irreps rho_j of D12=<s,t>: s->diag(w^j,w^-j), t->[[0,1],[1,0]]
w=lambda x: mp.expj(2*mp.pi*x/12)
def rho(j,word):
    # word: list of 's'/'t' applied as product left->right
    M=mp.eye(2)
    for ch in word:
        X=mp.matrix([[w(j),0],[0,w(-j)]]) if ch=='s' else mp.matrix([[0,1],[1,0]])
        M=M*X
    return M
# express P,L,R as words in s,t (verified as permutations)
words={'L':'t','R':'ts' if res['R=L(LR)?'] else None,'P':'tssss' if res['P=L(LR)^4 ?'] else None}
assert None not in words.values()
def wordperm(wd):
    g=idp
    for ch in wd: g=comp(g, s if ch=='s' else t)
    return g
res['words_verified']=all(wordperm(words[o])==perm[o] for o in 'PLR')
f=lambda k: abs(1+w(4*k)+w(7*k))   # DFT magnitude of major triad {0,4,7}
irr={}
for j in range(1,6):
    Msum=rho(j,words['P'])+rho(j,words['L'])+rho(j,words['R'])
    ev=sorted([mp.re(x) for x in mp.eig(Msum)[0]])
    match=[k for k in range(12) if abs(ev[1]-f(k))<1e-40]
    irr[j]=dict(eig=[mp.nstr(x,20) for x in ev],triad_DFT_index=match)
res['rho_j_to_k']=irr
res['rho_j_matches_k=7j']=all((7*j)%12 in irr[j]['triad_DFT_index'] for j in irr)
# 1-dim reps: t->e1, s->e2 (e2=±1)
one={}
for e1 in (1,-1):
    for e2 in (1,-1):
        val=sum(e1*(e2**words[o].count('s')) for o in 'PLR'); one[(e1,e2)]=val
res['one_dim_sums']={str(k):v for k,v in one.items()}
# Artin factorisation check of det(I-uA+2u^2) at random u
A=mp.zeros(24,24)
for a,b,o,st in EDGES: A[a,b]+=1
ok=0
for u in [mp.mpf('0.3')+0.1j, mp.mpf('-0.21')+0.4j, mp.mpf('0.6')]:
    lhs=mp.det(mp.eye(24)-u*A+2*u**2*mp.eye(24))
    rhs=mp.mpf(1)
    for v in one.values(): rhs*= (1-u*v+2*u**2)
    for j in range(1,6):
        Msum=rho(j,words['P'])+rho(j,words['L'])+rho(j,words['R'])
        rhs*= mp.det(mp.eye(2)-u*Msum+2*u**2*mp.eye(2))**2
    ok+= abs(lhs/rhs-1)<mp.mpf(10)**-40
res['artin_D12_factorisation_checks']=f'{ok}/3'
# Z12 (transposition) abelian cover of theta graph: L(u,chi_k)^{-1}=(1-u^2)*(1-u^2|g_k|^2 ... ) check
ok=0
g=lambda k: 1+w(0)*0+w(0)+w(4*k)+w(9*k)-w(0)   # =1+w^{4k}+w^{9k}
for u in [mp.mpf('0.3')+0.1j, mp.mpf('0.45')]:
    lhs=mp.det(mp.eye(24)-u*A+2*u**2*mp.eye(24))
    rhs=mp.mpf(1)
    for k in range(12): rhs*= (1+2*u**2)**2-u**2*abs(g(k))**2
    ok+= abs(lhs/rhs-1)<mp.mpf(10)**-40
res['Z12_artin_L_checks']=f'{ok}/2'
# explicit (trace) formula N_m = sum over 48 Ihara poles + (E-V)(1+(-1)^m)
pc=json.load(open('../prime_counts.json'))
ev=[mp.re(x) for x in mp.eig(A)[0]]
poles=[]
for l in ev:
    disc=mp.sqrt(l**2-8+0j); poles+= [(l+disc)/2,(l-disc)/2]
ok=all(abs(sum(p**m for p in poles)+12*(1+(-1)**m)-int(pc['N'][str(m)]))<1e-25 for m in range(1,41))
res['explicit_formula_m<=40']=ok
res['nontrivial_poles_on_circle_sqrt2']=all(abs(abs(p)-mp.sqrt(2))<1e-35 for p,l in zip(poles,[x for x in ev for _ in (0,1)]) if abs(abs(l)-3)>1e-20)
res['max_nontrivial_eig']=mp.nstr(max(abs(l) for l in ev if abs(abs(l)-3)>1e-20),25)
# Chebotarev for X -> theta_3 (Galois Z12): fraction of theta primes with Frobenius T_k
# rooted closed nb walks in theta3 of length m with net transposition k : (1/12) sum_chi chi(-k) tr(B_chi^m)
def trB(k,m):
    l=abs(g(k)); out=0
    for sgn in (1,-1):
        lam=sgn*l; d=mp.sqrt(lam**2-8+0j); out+=((lam+d)/2)**m+((lam-d)/2)**m
    return out+ (1)*(1+(-1)**m)   # base theta graph has E-V=1
cheb={}
for m in (12,24,40):
    tot=[mp.re(sum(trB(j,m)*w(-j*k) for j in range(12))/12) for k in range(12)]
    S=sum(tot); cheb[m]=[mp.nstr(x/S,8) for x in tot]
res['chebotarev_frob_fractions']=cheb
json.dump(res,open('group.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
