"""Exact criterion (proved in the notes): with chords free of steps and moves by steps, the departing note at each
move is the unique note of the current chord at step-distance from the arriving note; hence every arrival n_j leaves at
the first later step i with d(n_j,n_i) in S, and the moving voices' notes at every time are read off the tune.
So the tune theorem can only fail through the HELD notes: it fails iff for two different held sets H != H'
(|H|=1 for two moving voices, |H|=2 for one moving voice) the 'link graphs' share a cycle
(a cyclically non-backtracking closed walk valid with both H and H').  We test this exactly for each system."""
import itertools, json, sys
from collections import defaultdict
sys.setrecursionlimit(10000)
def classes(N):
    seen=set(); out=[]
    for a in range(1,N):
        for b in range(a+1,N):
            c=(0,a,b); norm=min(tuple(sorted((x-t)%N for x in c)) for t in range(N))
            if norm not in seen: seen.add(norm); out.append(norm)
    return out
def chords_of(N,c,inv):
    orb=set()
    for t in range(N):
        orb.add(frozenset((x+t)%N for x in c))
        if inv: orb.add(frozenset((-x+t)%N for x in c))
    return orb
def has_cycle(nodes,edges):
    # undirected multigraph without self-loops: cycle iff some component has #edges >= #nodes
    par={v:v for v in nodes}
    def f(v):
        while par[v]!=v: par[v]=par[par[v]]; v=par[v]
        return v
    for (a,b) in edges:
        ra,rb=f(a),f(b)
        if ra==rb: return True
        par[ra]=rb
    return False
def check(N,S,c,inv):
    CH=chords_of(N,c,inv); d=lambda a,b:min((a-b)%N,(b-a)%N)
    if any(d(a,b) in S for C in CH for a in C for b in C if a!=b): return None
    moves=set()
    for C in CH:
        for a in C:
            for s in S:
                for sg in (1,-1):
                    n=(a+sg*s)%N; D=(C-{a})|{n}
                    if len(D)==3 and D in CH: moves.add((C,D,a,n))
    if not moves: return None
    # 2 moving voices, held note h: link graph on pairs
    bad=[]
    for h,h2 in itertools.permutations(range(N),2):
        nodes=set(); edges=set()
        for (C,D,a,n) in moves:
            if h in C and h in D and h!=a:
                P=C-{h}; Q=D-{h}
                if (P|{h2}) in CH and (Q|{h2}) in CH and h2 not in P|Q:
                    nodes|={P,Q}; edges.add(frozenset((P,Q)))
        if h<h2 and has_cycle(nodes,[tuple(e) for e in edges]): bad.append(('two-voice',h,h2)); break
    if not bad:
        for H in itertools.combinations(range(N),2):
            H=frozenset(H)
            for H2 in itertools.combinations(range(N),2):
                H2=frozenset(H2)
                if H2<=H or H2==H: continue
                nodes=set(); edges=set()
                for (C,D,a,n) in moves:
                    if H<=C and H<=D and a not in H and (H2|{a}) in CH and (H2|{n}) in CH and a not in H2 and n not in H2:
                        nodes|={a,n}; edges.add(frozenset((a,n)))
                if has_cycle(nodes,[tuple(e) for e in edges]): bad.append(('one-voice',tuple(H),tuple(H2))); break
            if bad: break
    degs=defaultdict(int)
    for (C,D,a,n) in moves: degs[C]+=1
    return dict(chords=len(CH),deg=sorted(set(degs.values())),ok=not bad,witness=bad[:1])
res=[]
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 40
for N in range(5,NMAX+1):
    for S in ((1,),(1,2)):
        for c in classes(N):
            for inv in (False,True):
                r=check(N,S,c,inv)
                if r is None: continue
                r.update(N=N,S=S,c=c,inv=inv); res.append(r)
                if not r['ok']: print(r,flush=True)
json.dump(res,open('tune_criterion.json','w'))
print('systems',len(res),'ok',sum(r['ok'] for r in res),'fail',sum(not r['ok'] for r in res))
r12=[r for r in res if r['N']==12 and r['S']==(1,2) and r['c']==(0,3,7)]; print('12-TET consonant triads:',r12)
