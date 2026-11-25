import itertools, json, sys
from collections import defaultdict
exec(open('tune_criterion.py').read().split('def check(')[0])
def check(N,S,c,inv):
    CH=chords_of(N,c,inv); d=lambda a,b:min((a-b)%N,(b-a)%N)
    if any(d(a,b) in S for C in CH for a in C for b in C if a!=b): return None
    steps=[sg*s for s in S for sg in (1,-1)]
    deg={C:sum(1 for a in C for t in steps if (len((C-{a})|{(a+t)%N})==3 and ((C-{a})|{(a+t)%N}) in CH)) for C in CH}
    if max(deg.values())==0: return None
    # two moving voices
    L=defaultdict(set)
    for C in CH:
        for h in C: L[h].add(C-{h})
    bad=[]
    for h in range(N):
        for h2 in range(h+1,N):
            common=L[h]&L[h2]
            if len(common)<3: continue
            edges=[]
            for P in common:
                for a in P:
                    for t in steps:
                        Q=(P-{a})|{(a+t)%N}
                        if len(Q)==2 and Q in common and h not in Q and h2 not in Q: edges.append((P,Q))
            E={frozenset(e) for e in edges}
            if has_cycle(common,[tuple(e) for e in E]): bad.append(('two-voice',h,h2)); break
        if bad: break
    if not bad:
        comp=defaultdict(set)
        for C in CH:
            for H in itertools.combinations(sorted(C),2):
                x=(C-set(H)); comp[frozenset(H)].add(next(iter(x)))
        Hs=[H for H in comp if len(comp[H])>=3]
        for H,H2 in itertools.combinations(Hs,2):
            common=comp[H]&comp[H2]
            if len(common)<3: continue
            E={frozenset((x,(x+t)%N)) for x in common for t in steps if (x+t)%N in common}
            if has_cycle(common,[tuple(e) for e in E]): bad.append(('one-voice',tuple(H),tuple(H2))); break
    return dict(chords=len(CH),deg=sorted(set(deg.values())),ok=not bad,witness=bad[:1])
res=[]; NMAX=int(sys.argv[1])
for N in range(5,NMAX+1):
    for S in ((1,),(1,2)):
        for c in classes(N):
            for inv in (False,True):
                r=check(N,S,c,inv)
                if r is None: continue
                r.update(N=N,S=S,c=c,inv=inv); res.append(r)
                if not r['ok']: print(r,flush=True)
    print('N',N,'done',len(res),flush=True) if N%8==0 else None
json.dump(res,open('tune_criterion_fast.json','w'))
print('systems',len(res),'ok',sum(r['ok'] for r in res),'fail',sum(not r['ok'] for r in res))
