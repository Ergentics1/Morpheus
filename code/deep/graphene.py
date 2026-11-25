import mpmath as mp, numpy as np, json, math
from common import *
from lattice import VOLT, LAT, flip
mp.mp.dps=40
res={}
w=lambda x: mp.expj(2*mp.pi*x/12)
# (a) honeycomb tight-binding: A-site = major root r, B-site = minor root; bonds r->r, r+4, r+9
bonds=sorted({(V[b][0]-V[a][0])%12 for a,b,o,s in EDGES if V[a][1]=='M'})
res['major_to_minor_cell_offsets']=bonds
# (b) A^2 on major triads = 3I + Cayley(Z12,{±3,±4,±5}) (note Tonnetz)
A=np.zeros((24,24))
for a,b,o,s in EDGES: A[a,b]+=1
A2=A@A; maj=[IX[(r,'M')] for r in range(12)]
B=A2[np.ix_(maj,maj)]-3*np.eye(12)
T=np.zeros((12,12))
for r in range(12):
    for d in (3,4,5,7,8,9): T[r,(r+d)%12]=1
res['honeycomb_squared_is_note_tonnetz']=bool(np.allclose(B,T))
# (c) twisted adjacency with torus voltages: spectrum = graphene band at shifted momenta
def At(al,be):
    M=mp.zeros(24,24)
    for (a,b,o,s),(du,dv) in zip(EDGES,VOLT): M[a,b]+=mp.expj(al*du+be*dv)
    return M
def topev(al,be): return max(mp.re(x) for x in mp.eighe(At(al,be))[0])
# step-phase twist equals u-twist with phi=-12 theta  (W=-u): compare spectra
def Astep(th):
    M=mp.zeros(24,24)
    for (a,b,o,s) in EDGES: M[a,b]+=mp.expj(th*s)
    return M
ok=0
for th in [mp.mpf('0.07'),mp.mpf('0.2'),mp.pi/12]:
    e1=sorted(mp.re(x) for x in mp.eighe(Astep(th))[0]); e2=sorted(mp.re(x) for x in mp.eighe(At(-12*th,0))[0])
    ok+= max(abs(x-y) for x,y in zip(e1,e2))<1e-30
res['step_twist_equals_u_flux']=f'{ok}/3'
# (d) covariance of (u,v) per step: -Hessian of log rho at 0
def logrho(al,be):
    l=topev(al,be); return mp.log((l+mp.sqrt(l**2-8))/2)
h=mp.mpf('1e-6')
f0=logrho(0,0)
Huu=(logrho(h,0)-2*f0+logrho(-h,0))/h**2
Hvv=(logrho(0,h)-2*f0+logrho(0,-h))/h**2
Huv=(logrho(h,h)-logrho(h,-h)-logrho(-h,h)+logrho(-h,-h))/(4*h**2)
res['cov_per_step']={'uu':mp.nstr(-Huu,12),'vv':mp.nstr(-Hvv,12),'uv':mp.nstr(-Huv,12)}
res['cov_identify']={k:str(mp.identify(-x)) for k,x in (('uu',Huu),('vv',Hvv),('uv',Huv))}
# check vs census2 (m=18) empirical
C2=json.load(open('../melodic_primes/voice/census2.json'))
for m in ('14','16','18'):
    tot=sum(n for uv,W,pt,hm,d,n in C2[m]); Euu=sum(n*uv[0]**2 for uv,W,pt,hm,d,n in C2[m])/tot
    Evv=sum(n*uv[1]**2 for uv,W,pt,hm,d,n in C2[m])/tot; Euv=sum(n*uv[0]*uv[1] for uv,W,pt,hm,d,n in C2[m])/tot
    res['empirical_cov_over_m_'+m]=[round(Euu/int(m),5),round(Evv/int(m),5),round(Euv/int(m),5)]
# (e) Ramanujan cap in the Brillouin zone: area fraction with |Delta|<=2sqrt2
N=600; cnt=0
for i in range(N):
    for j in range(N):
        a=2*math.pi*i/N; b=2*math.pi*j/N
        if abs(1+complex(math.cos(a),math.sin(a))+complex(math.cos(b),math.sin(b)))<=2*math.sqrt(2): cnt+=1
res['BZ_fraction_RH_ok']=cnt/N**2
# exact: |Delta|^2 = 3+2cos a+2cos b+2cos(a-b) > 8 cap
# (f) Dirac point: twisted spectrum contains 0 exactly at phi=2pi/3 (u-flux)
res['min_abs_eig_at_u_flux_2pi/3']=mp.nstr(min(abs(x) for x in mp.eighe(At(2*mp.pi/3,0))[0]),5)
res['untwisted_has_no_zero_eig']=bool(min(abs(np.linalg.eigvalsh(A)))>0.5)
# (g) voice (Kekule) colouring: colour of a move = coset (2a+b mod 3) of the moving vertex, on the plane;
#     every pedal hexagon uses only two colours; colouring does not descend to the torus (period (4,-4) shifts coset)
res['period_vector_coset_shift']=[(2*4-4)%3,(2*0+3)%3]
hexok=True
for n0 in range(12):
    # walk around hexagon of triads containing n0 starting at major triad with root n0 using alternating moves that keep n0
    c=(n0,'M'); t=LAT[c]; cols=[]; prev=None
    for step in range(6):
        o=next(o for o in 'PLR' if o!=prev and n0 in tri(OPS[o](c)))
        t2=flip(t,o); mv=next(iter(t-t2)); cols.append((2*mv[0]+mv[1])%3)
        c=OPS[o](c); t=t2; prev=o
    hexok&= len(set(cols))==2 and all(cols[i]!=cols[i+1] for i in range(5))
res['pedal_hexagons_bicoloured']=hexok
json.dump(res,open('graphene.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
