# exact weighted traces N_m(z^stepsum, y^#R) by DP over (chord,lastop); independent of enumeration code
import numpy as np, json, sympy, collections, math
NMs=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
# independent re-implementation of moves with explicit voice motion
def triad(r,q): return [r%12,(r+4)%12,(r+7)%12] if q=='M' else [r%12,(r+3)%12,(r+7)%12]
MOV={('M','P'):(lambda r:((r)%12,'m'), -1),('m','P'):(lambda r:(r%12,'M'),+1),
     ('M','L'):(lambda r:((r+4)%12,'m'),-1),('m','L'):(lambda r:((r+8)%12,'M'),+1),
     ('M','R'):(lambda r:((r+9)%12,'m'),+2),('m','R'):(lambda r:((r+3)%12,'M'),-2)}
# sanity: step equals the moved pitch-class difference
for r in range(12):
    for q in 'Mm':
        for o in 'PLR':
            f,s=MOV[(q,o)]; r2,q2=f(r); a=set(triad(r,q)); b=set(triad(r2,q2))
            assert len(a&b)==2 and (list(b-a)[0]-list(a-b)[0]-s)%12==0
V=[(r,q) for r in range(12) for q in 'Mm']; ix={v:i for i,v in enumerate(V)}
MAXM=40; OFF=2*MAXM; NS=4*MAXM+1
N={}  # m -> array [stepsum+OFF, r]
tot={m:np.zeros((NS,MAXM+1),dtype=object) for m in range(1,MAXM+1)}
for q0 in 'Mm':
  for o0 in 'PLR':
    # start on directed edge leaving (0,q0) via o0; count walks returning to same directed edge
    f,s=MOV[(q0,o0)]; v1=f(0)
    state={ (v1,o0): {(s,1 if o0=='R' else 0):1} }
    for m in range(1,MAXM+2):
        # closing: current state (v,o) equals start edge's head & op means walk of m edges returned when v==v1 and o==o0
        if (v1,o0) in state:
            if m>1:
              for (ss,rr),c in state[(v1,o0)].items():
                ss2=ss-s; rr2=rr-(o0=='R')   # remove the duplicated first edge
                tot[m-1][ss2+OFF,rr2]+=c
        new=collections.defaultdict(lambda: collections.defaultdict(int))
        for (v,o),poly in state.items():
            for o2 in 'PLR':
                if o2==o: continue
                f2,s2=MOV[(v[1],o2)]; w=f2(v[0])
                d=new[(w,o2)]
                for (ss,rr),c in poly.items(): d[(ss+s2,rr+(o2=='R'))]+=c
        state=new
for m in tot: tot[m]*=12   # transposition symmetry
Nm={m:int(sum(tot[m].flatten())) for m in tot}
pc=json.load(open('../../prime_counts.json'))
assert all(Nm[m]==int(pc['N'][str(m)]) for m in range(1,MAXM+1)), 'trace mismatch'
print('unweighted traces match prime_counts.json for m<=40')
def subs_pow(arr,k):
    out=np.zeros_like(arr)
    for i in range(NS):
        for r in range(MAXM+1):
            if arr[i,r]:
                j=(i-OFF)*k+OFF; out[j,r*k]+=arr[i,r]
    return out
PI={}
for m in range(1,MAXM+1):
    acc=np.zeros((NS,MAXM+1),dtype=object)
    for d in sympy.divisors(m):
        mu=sympy.mobius(m//d)
        if mu: acc=acc+int(mu)*subs_pow(tot[d],m//d)
    assert all(x%m==0 for x in acc.flatten())
    PI[m]=acc//m
pi_tot={m:int(sum(PI[m].flatten())) for m in PI}
assert all(pi_tot[m]==int(pc['pi'][str(m)]) for m in PI)
print('prime totals match')
res={}
for m in range(6,MAXM+1,2):
    byW=collections.Counter(); byR=collections.Counter()
    for i in range(NS):
        for r in range(MAXM+1):
            c=PI[m][i,r]
            if c:
                assert (i-OFF)%12==0; byW[(i-OFF)//12]+=int(c); byR[r]+=int(c)
    res[m]=dict(pi=pi_tot[m],W=dict(sorted(byW.items())),R=dict(sorted(byR.items())))
json.dump(res,open('transfer.json','w'),indent=0)
for m in (6,8,10,12,14,16,18,20,24,30,40):
    r=res[m]; home=r['W'].get(0,0)
    meanR=sum(k*v for k,v in r['R'].items())/r['pi']
    varW=sum(k*k*v for k,v in r['W'].items())/r['pi']
    pred_home=math.sqrt(12/(math.pi*m))
    print(m,'pi',r['pi'],'home(W=0)',home,'frac %.5f pred %.5f'%(home/r['pi'],pred_home),'varW/m %.5f (1/24=%.5f)'%(varW/m,1/24),'meanR/m %.5f'%(meanR/m), 'W', {k:v for k,v in r['W'].items() if abs(k)<=3})
