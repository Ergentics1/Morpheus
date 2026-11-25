"""Independent checks: (a) pure-python exhaustive search that no degree<=5 divisor has rank>=1;
(b) Chan's criterion: no involution of X has a tree quotient, so the metric graph is not hyperelliptic."""
import sys, json, itertools
sys.path.insert(0,'../deep'); from common import V, IX, OPS, cname
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
n=24; nbr=[[IX[OPS[s](v)] for s in 'PLR'] for v in V]
def red(D,q):
    D=list(D)
    while True:
        burnt={q}; cnt=[0]*n; st=[q]
        while st:
            x=st.pop()
            for y in nbr[x]:
                if y not in burnt:
                    cnt[y]+=1
                    if cnt[y]>D[y]: burnt.add(y); st.append(y)
        if len(burnt)==n: return D
        for x in range(n):
            if x not in burnt:
                for y in nbr[x]:
                    if y in burnt: D[x]-=1; D[y]+=1
def rank1(D): return all(red(D,q)[q]>=1 for q in range(n))
found=False
for d in range(2,6):
    for E in itertools.combinations_with_replacement(range(n),d-1):
        D=[0]*n; D[0]=1
        for e in E: D[e]+=1
        if rank1(D): found=True; print('found',d,D); break
    if found: break
r=[('pure-python: no rank-1 divisor of degree <=5 (vertex-transitivity => contains C)',not found)]
G=nx.Graph(); [G.add_edge(IX[v],IX[OPS[s](v)]) for v in V for s in 'PLR']
invols=[f for f in GraphMatcher(G,G).isomorphisms_iter() if all(f[f[x]]==x for x in range(n)) and any(f[x]!=x for x in range(n))]
trees=0
for f in invols:
    Vo={frozenset((x,f[x])) for x in range(n)}
    Eo={frozenset((frozenset(e),frozenset((f[e[0]],f[e[1]])))) for e in G.edges}
    flipped=sum(1 for (a,b) in G.edges if f[a]==b)//1
    Vp=len(Vo)+flipped; Ep=len(Eo)
    if Vp-Ep==1: trees+=1
r.append((f'Chan criterion: none of the {len(invols)} involutions of X has a tree quotient (metric graph not hyperelliptic)',trees==0))
for a,b in r: print('PASS' if b else 'FAIL',a)
json.dump(r,open('gon_check.json','w'))
