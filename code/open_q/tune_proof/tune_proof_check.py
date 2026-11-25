"""Checks for the held-note theorem (all N, all step sets S, both symmetry types).
(a) Lemma: the link graph Lk(b) (u~w iff {b,u,w} is a chord) never contains a 4-cycle -- independent of S.
(b) Two-held walks: brute force over all S for small N, compared with the predicted exceptional family
    {T/I class, intervals (x, N/2, z), x != z, 2x and x-z in +-S}.
(c) Independent brute force: all closed non-backtracking walks up to length L, tune collisions, for all S, N<=14."""
import itertools, json, sys
from collections import defaultdict
def classes(N):
    out=[]
    seen=set()
    for x in range(1,N):
        for y in range(1,N-x):
            z=N-x-y
            if z<1: continue
            base=frozenset({0,x,x+y})
            for ti in (False,True):
                ch=set()
                for t in range(N):
                    ch.add(frozenset((a+t)%N for a in base))
                    if ti: ch.add(frozenset((t-a)%N for a in base))
                key=(frozenset(ch),ti)
                if key in seen: continue
                seen.add(key); out.append(dict(x=x,y=y,z=z,ti=ti,chords=ch))
    return out
def lemma_a(Nmax):
    bad=[]
    for N in range(5,Nmax+1):
        for c in classes(N):
            Lk=defaultdict(set)
            for ch in c['chords']:
                if 0 in ch:
                    u,w=sorted(ch-{0}); Lk[u].add(w); Lk[w].add(u)
            V=list(Lk)
            for a,b in itertools.combinations(V,2):
                if len(Lk[a]&Lk[b])>=2: bad.append((N,c['x'],c['y'],c['ti']))
    return bad
def steps_ok(c,S,N):
    pm={s%N for s in S}|{(-s)%N for s in S}
    return all(((u-w)%N) not in pm for ch in c['chords'] for u in ch for w in ch if u!=w), pm
def has_cycle(Vs,adj):
    # undirected graph contains a cycle?
    seen=set()
    for s in Vs:
        if s in seen: continue
        stack=[(s,None)]; seen.add(s); par={s:None}
        while stack:
            v,p=stack.pop()
            for w in adj[v]:
                if w==p: continue
                if w in par: return True
                par[w]=v; seen.add(w); stack.append((w,v))
    return False
def two_held(c,pm,N):
    comp=defaultdict(set)
    for ch in c['chords']:
        for a in ch:
            comp[frozenset(ch-{a})].add(a)
    Q0=[Q for Q in comp if 0 in Q]
    for Q in Q0:
        for Qp in comp:
            if Qp==Q: continue
            W=comp[Q]&comp[Qp]
            adj={a:{b for b in W if (b-a)%N in pm} for a in W}
            if has_cycle(W,adj): return True
    return False
def predicted(c,pm,N):
    """Exceptional family: 8 | N, T/I class of the chord with intervals (N/8, 3N/8, N/2), and N/4 in S."""
    if not c['ti'] or N%8: return False
    if sorted([c['x'],c['y'],c['z']])!=[N//8,3*N//8,N//2]: return False
    return (N//4)%N in pm
def part_b(Nmax):
    mism=[]; hits=[]
    for N in range(5,Nmax+1):
        cl=classes(N); half=list(range(1,N//2+1))
        for r in range(1,len(half)+1):
            for S in itertools.combinations(half,r):
                for c in cl:
                    ok,pm=steps_ok(c,S,N)
                    if not ok: continue
                    a=two_held(c,pm,N); b=predicted(c,pm,N)
                    if a!=b: mism.append((N,S,c['x'],c['y'],c['ti']))
                    if a: hits.append((N,S,(c['x'],c['y'],c['z']),c['ti']))
    return mism,hits
def part_c(Nmax,L):
    coll=[]; ncheck=0
    for N in range(5,Nmax+1):
        cl=classes(N); half=list(range(1,N//2+1))
        for r in range(1,len(half)+1):
            for S in itertools.combinations(half,r):
                for c in cl:
                    ok,pm=steps_ok(c,S,N)
                    if not ok: continue
                    ch=list(c['chords']); E=defaultdict(list)
                    for A in ch:
                        for a in A:
                            for s in pm:
                                B=(A-{a})|{(a+s)%N}
                                if len(B)==3 and B in c['chords']: E[A].append((B,(a+s)%N))
                    tunes=defaultdict(set)
                    def canon(seq):
                        m=len(seq); return min(tuple(seq[i:]+seq[:i]) for i in range(m))
                    for A0 in ch:
                        stack=[(A0,None,[],[A0])]
                        while stack:
                            A,prev,tune,path=stack.pop()
                            if len(tune)>=1 and A==A0 and len(path)>1:
                                # closed; check non-backtracking at the seam
                                if path[1]!=path[-2] or len(path)==2:
                                    if len(path)>2 or True:
                                        cyc=tuple(path[:-1])
                                        tunes[canon(tune)].add(frozenset(canon_c(cyc)))
                            if len(tune)==L: continue
                            for B,nt in E[A]:
                                if B==prev: continue
                                stack.append((B,A,tune+[nt],path+[B]))
                    for t,ws in tunes.items():
                        ncheck+=1
                        if len(ws)>1: coll.append((N,S,(c['x'],c['y'],c['z']),c['ti'],t))
    return coll,ncheck
def canon_c(cyc):
    m=len(cyc); return [cyc[(i) % m] for i in range(m)] and {tuple(cyc[i:]+cyc[:i]) for i in range(m)}
if __name__=='__main__':
    res={}
    res['lemma_a_N<=60_violations']=lemma_a(60)
    mism,hits=part_b(26); res['part_b_N<=26_mismatches']=mism; res['part_b_exceptional_count']=len(hits); res['part_b_examples']=hits[:5]
    res['part_b_hits_with_S_subset_12']=[h for h in hits if set(h[1])<={1,2}]
    print(json.dumps({k:(v if not isinstance(v,list) or len(v)<20 else len(v)) for k,v in res.items()}),flush=True)
    coll,nc=part_c(int(sys.argv[1]) if len(sys.argv)>1 else 12, int(sys.argv[2]) if len(sys.argv)>2 else 8)
    res['part_c_collisions']=coll[:20]; res['part_c_ncollisions']=len(coll); res['part_c_tunes_checked']=nc
    json.dump(res,open('tune_proof_check.json','w'),indent=1,default=str)
    print(json.dumps({k:(v if not isinstance(v,list) or len(v)<20 else len(v)) for k,v in res.items()},default=str))
