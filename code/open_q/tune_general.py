"""Open question: does the tune theorem hold for every parsimonious triadic system in N-TET whose moves are steps
and whose chords contain no steps?  System = (N, step set S, a 3-note set class c closed under T or T/I).
Chords: all transpositions (and inversions) of c; requirement: no two notes of a chord differ by an element of +-S.
Moves: one note moves by +-s (s in S) and the result is again a chord.  Tune of a closed walk = sequence of arriving notes.
Test: is (rooted, cyclically non-backtracking closed walk) -> tune injective, for all walks of length <= L?"""
import itertools, json, sys
from collections import defaultdict
def classes(N):
    seen=set(); out=[]
    for a in range(1,N):
        for b in range(a+1,N):
            c=frozenset({0,a,b})
            norm=min(tuple(sorted((x-t)%N for x in c)) for t in range(N))
            if norm in seen: continue
            seen.add(norm); out.append(norm)
    return out
def build(N,S,c,inv):
    orb=set()
    for t in range(N):
        orb.add(frozenset((x+t)%N for x in c))
        if inv: orb.add(frozenset((-x+t)%N for x in c))
    ch=sorted(orb,key=sorted)
    dist=lambda a,b: min((a-b)%N,(b-a)%N)
    for C in ch:
        if any(dist(a,b) in S for a in C for b in C if a!=b): return None
    idx={C:i for i,C in enumerate(ch)}; adj=[[] for _ in ch]
    for C in ch:
        for a in C:
            for s in S:
                for sg in (1,-1):
                    n=(a+sg*s)%N; D=(C-{a})|{n}
                    if len(D)==3 and D in idx: adj[idx[C]].append((idx[D],a,n))
    return ch,adj
def test(ch,adj,L,cap=6_000_000):
    work=0
    for m in range(2,L+1):
        seen={}
        for s0 in range(len(ch)):
            stack=[(s0,(),(s0,),None,None)]
            while stack:
                v,tune,path,last,first=stack.pop(); work+=1
                if work>cap: return ('capped',m-1)
                if len(tune)==m:
                    if v!=s0: continue
                    if last[0]==first[1] and last[1]==first[0] and last[2]==first[3] and last[3]==first[2]: continue
                    w0=seen.get(tune)
                    if w0 is not None and w0!=path: return ('collision',m,tune,w0,path)
                    seen[tune]=path; continue
                for (w,a,n) in adj[v]:
                    mv=(v,w,a,n)
                    if last and last[0]==w and last[1]==v and last[2]==n and last[3]==a: continue
                    stack.append((w,tune+(n,),path+(w,),mv,first or mv))
    return ('ok',L)
def path_of(s): return None
res=[]
for N in range(5,int(sys.argv[1]) if len(sys.argv)>1 else 25):
    for S in ((1,),(1,2)):
        for c in classes(N):
            for inv in (False,True):
                g=build(N,S,c,inv)
                if g is None: continue
                ch,adj=g
                degs=sorted({len(a) for a in adj})
                if max(degs)==0: continue
                L=12 if max(degs)<=3 else (9 if max(degs)<=4 else 7)
                r=test(ch,adj,L)
                res.append(dict(N=N,S=S,c=c,inv=inv,chords=len(ch),deg=degs,result=r))
                if r[0]!='ok': print(N,S,c,'TI' if inv else 'T',len(ch),degs,r,flush=True)
json.dump(res,open('tune_general.json','w'))
print('systems tested',len(res),'ok',sum(r['result'][0]=='ok' for r in res),'collisions',sum(r['result'][0]=='collision' for r in res),'capped',sum(r['result'][0]=='capped' for r in res))
