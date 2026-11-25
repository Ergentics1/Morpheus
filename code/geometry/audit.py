import json, sys
sys.path.insert(0,'../deep'); from common import V, IX, OPS
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
rows=[]
for f in ('schottky','sandpile','tower','curvesF2'):
    for n,ok,d in json.load(open(f+'.json'))['audit']: rows.append((f,n,ok))
for n,ok in json.load(open('gon_check.json')): rows.append(('gon_check',n,ok))
rows.append(('recheck_g6','independent recount: genus-6 curve y^2+(x^6+x^5+x^4+x^3+1)y=x^13+x^3+x has L=(1-3u^2+4u^4)(octic)',json.load(open('recheck_g6.json'))['ok']))
G=nx.Graph(); [G.add_edge(IX[v],IX[OPS[s](v)]) for v in V for s in 'PLR']
rows.append(('audit','|Aut(X)|=24 => Aut(C)=N(K)/K = D12 (the T/I group) exactly',sum(1 for _ in GraphMatcher(G,G).isomorphisms_iter())==24))
S=json.load(open('shimura_multi.json'))
free=[s for s in S if s['e2']==0 and s['e3']==0]
rows.append(('shimura','all torsion-free genus-13 CD curves X_0^D(N), 2|D, have dim S2^{D/2-new}=11 (Brandt class number 12 consistency)',all(len(s['abs_a2'])==11 for s in free)))
rows.append(('shimura',f'none of the {len(S)} genus-13 CD curves X_0^D(N) (2|D, any number of primes) has the chord-graph spectrum',not any(s['match'] for s in S)))
H=json.load(open('shimura_H.json'))
rows.append(('shimura',f'none of the {len(H)} Gamma_H level structures with 24 components has the chord-graph spectrum',not any(h['match'] for h in H)))
rows.append(('shimura','torsion-free Gamma_H cases have 11 forms (consistency)',all(len(h['abs_a2'])==11 for h in H if h['torsion_free'])))
out=['# math_audit (geometry round)','',f'**{sum(r[2] for r in rows)}/{len(rows)} checks pass**','','| # | script | check | result |','|---|---|---|---|']
for i,(f,n,ok) in enumerate(rows,1): out.append(f'| {i} | {f} | {n} | {"PASS" if ok else "FAIL"} |')
open('math_audit.md','w').write('\n'.join(out)+'\n'); print(sum(r[2] for r in rows),'/',len(rows))
