# all 2^13 Z2 signing classes (2-lifts) of the PLR graph; where the voice-parity signing sits; torus/Z_n covers
import numpy as np, json, math, itertools, networkx as nx
from common import *
from lattice import VOLT
und={}   # undirected edge id: (a,b) with a major
for (a,b,o,s),vt in zip(EDGES,VOLT):
    if V[a][1]=='M': und[(a,b,o)]=(s,vt)
E=list(und.keys())
Gx=nx.Graph(); Gx.add_edges_from([(a,b,{'k':(a,b,o)}) for a,b,o in E])
# NB: no multi-edges? check
assert Gx.number_of_edges()==36
Tr=nx.minimum_spanning_tree(Gx); tree={d['k'] for a,b,d in Tr.edges(data=True)}
cot=[e for e in E if e not in tree]; assert len(cot)==13
def spec(sign):   # sign: dict edge->±1
    M=np.zeros((24,24))
    for (a,b,o) in E: M[a,b]=M[b,a]=sign[(a,b,o)]
    return np.linalg.eigvalsh(M)
R8=2*math.sqrt(2)
# cohomology class of a signing = its values on cycles; normalise to tree-trivial form via potentials
def normalise(sign):
    # find potential p on vertices with sign(e)*p(a)*p(b)=+1 on tree edges
    p={0:1}; stack=[0]
    adj=collections.defaultdict(list)
    for (a,b,o) in tree: adj[a].append((b,(a,b,o))); adj[b].append((a,(a,b,o)))
    while stack:
        x=stack.pop()
        for y,e in adj[x]:
            if y not in p: p[y]=p[x]*sign[e]; stack.append(y)
    return tuple(sign[e]*p[e[0]]*p[e[1]] for e in cot)
results=[]
for bits in itertools.product((1,-1),repeat=13):
    sg={e:1 for e in E}; sg.update(dict(zip(cot,bits)))
    ev=spec(sg); results.append((max(abs(ev)),bits))
mx=np.array([r[0] for r in results])
nontriv=mx[1:] if results[0][1]==(1,)*13 else mx
out={}
out['n_classes']=len(results)
out['n_ramanujan_classes(max|lam|<=2sqrt2, excluding trivial)']=int(sum(1 for r in results if r[1]!=(1,)*13 and r[0]<=R8+1e-12))
out['min_max_eig_over_signings']=float(min(r[0] for r in results))
# named signings
named={}
named['voice_parity_W']={e:(-1)**((und[e][0]*0+0)) for e in E}  # placeholder replaced below
# voice parity: Z2 voltage = u mod 2 (W=-u)
for nm,fn in [('u_parity=voice_parity',lambda s,vt: vt[0]%2),('v_parity',lambda s,vt: vt[1]%2),('u+v_parity',lambda s,vt:(vt[0]+vt[1])%2)]:
    sg={e:(-1)**fn(*und[e]) for e in E}
    named[nm]=sg
# also an independent definition of voice parity from step sums via BFS potentials of lifted voice sum
S={0:11}; order=[0]; adjd=collections.defaultdict(list)
for a,b,o,s in EDGES: adjd[a].append((b,s))
while order:
    x=order.pop()
    for y,s in adjd[x]:
        if y not in S: S[y]=S[x]+s; order.append(y)
named['voice_parity_from_steps']={(a,b,o):(-1)**(((S[a]+und[(a,b,o)][0]-S[b])//12)%2) for (a,b,o) in E}
for nm,sg in named.items():
    ev=spec(sg); m=max(abs(ev)); cls=normalise(sg)
    rank=int(sum(1 for r in results if r[0]<m-1e-12))
    out[nm]=dict(max_eig=float(m),ramanujan=bool(m<=R8+1e-12),class_rank_by_max_eig=rank,trivial_class=cls==(1,)*13)
out['voice_parity_classes_agree']=normalise(named['voice_parity_from_steps'])==normalise(named['u_parity=voice_parity'])
out['distinct_max_eig_values']=len(set(round(x,9) for x in mx))
out['best_signings_max']=sorted(set(round(x,9) for x in mx))[:5]
# Z_n cyclic covers along u, v : nontrivial characters must all be Ramanujan
def maxeig_char(al,be):
    M=np.zeros((24,24),complex)
    for (a,b,o,s),(du,dv) in zip(EDGES,VOLT): M[a,b]+=np.exp(1j*(al*du+be*dv))
    return max(abs(np.linalg.eigvalsh(M)))
cov={}
for n in range(2,13):
    cov[n]={'u':all(maxeig_char(2*math.pi*j/n,0)<=R8+1e-12 for j in range(1,n)),
            'v':all(maxeig_char(0,2*math.pi*j/n)<=R8+1e-12 for j in range(1,n)),
            'full_torus_ZnxZn':all(maxeig_char(2*math.pi*i/n,2*math.pi*j/n)<=R8+1e-12 for i in range(n) for j in range(n) if (i,j)!=(0,0))}
out['cyclic_covers_ramanujan']=cov
json.dump(out,open('signings.json','w'),indent=1,default=str)
for k,v in out.items(): print(k,':',v)
