# Proof ingredients for "the tune determines the prime" + full reconstruction test
import json, sys
from common import *
out={}
CONS={tri(v) for v in V}
# L1: at every triad the three moves move three different notes (voices)
out['L1_moves_biject_voices']=all(len({move(v,o)[1] for o in 'PLR'})==3 for v in V)
# L1': the unique move that moves the just-arrived note back is the inverse move (backtrack)
out['L1b_only_backtrack_moves_arrival']=all(next(o2 for o2 in 'PLR' if move(move(v,o)[0],o2)[1]==move(v,o)[2])==o for v in V for o in 'PLR')
# L4: a 3-set containing two notes 1 or 2 semitones apart is never consonant
out['L4_steps_not_in_triads']=all(all(((x-y)%12) not in (1,2,10,11) for x in T for y in T if x!=y) for T in CONS)
# every step of a move is 1 or 2 semitones
out['steps_are_1_or_2']=all(abs(e[3]) in (1,2) for e in EDGES)
def closed_words(m):
    for w in itertools.product('PLR',repeat=m):
        if all(w[i]!=w[(i+1)%m] for i in range(m)): yield ''.join(w)
def walk(c0,w):
    c=c0; ch=[]; arr=[]
    for o in w:
        c,outn,inn,s=move(c,o); ch.append(c); arr.append(inn)
    return ch,arr
def reconstruct(arr):
    """chords X_i (after move i) from the cyclic tune alone"""
    m=len(arr); X=[None]*m
    same=[ frozenset({arr[i-2],arr[i-1],arr[i]}) not in CONS for i in range(m)]  # voice(i)==voice(i-2)
    if all(same):   # two voices only (pedal): held note h must make a triad with every consecutive pair
        hs=[h for h in range(12) if all(frozenset({arr[i-1],arr[i],h}) in CONS for i in range(m))]
        if len(hs)!=1: return None
        return [frozenset({arr[i-1],arr[i],hs[0]}) for i in range(m)]
    # unroll the cyclic tune on a line (voices may come back permuted, so label locally)
    K=4*m; idx=list(range(-K,m)); vo={-K:0,-K+1:1}
    for i in range(-K+2,m): vo[i]=vo[i-2] if same[i%m] else 3-vo[i-1]-vo[i-2]
    for i in range(m):
        third=3-vo[i]-vo[i-1]; j=i-2
        while vo[j]!=third:
            j-=1
            if j<-K: return None
        X[i]=frozenset({arr[i%m],arr[(i-1)%m],arr[j%m]})
    return X
def minper(seq):
    m=len(seq); return next(d for d in range(1,m+1) if m%d==0 and all(seq[i]==seq[(i+d)%m] for i in range(m)))
MAXM=int(sys.argv[1]) if len(sys.argv)>1 else 14
stats={}
for m in range(6,MAXM+1,2):
    good=0; tot=0; tunes={}; prim_tune=True
    for w in closed_words(m):
        for c0 in V:
            ch,arr=walk(c0,w)
            if ch[-1]!=c0: continue
            if minper(list(zip(ch,w)))<m: continue
            tot+=1
            X=reconstruct(arr)
            if X==[tri(c) for c in ch]: good+=1
            if minper(arr)<m: prim_tune=False
            key=min(tuple(arr[i:]+arr[:i]) for i in range(m))
            tunes.setdefault(key,set()).add(min(tuple(ch[i:]+ch[:i]) for i in range(m)))
    stats[m]=dict(rooted=tot,primes=tot//m,reconstructed=good,distinct_tunes=len(tunes),injective=all(len(s)==1 for s in tunes.values()),tunes_primitive=prim_tune)
    print(m,stats[m],flush=True)
out['reconstruction']=stats
# W=-u lemma: voice height. Tonnetz lattice coords (a,b): pc=7a+4b. flips move a vertex by delta; step must equal -delta_a
FLIPS=[(1,-2),(1,1),(-2,1),(-1,2),(-1,-1),(2,-1)]
out['flip_vectors_in_coset_lattice']=all((2*a+b)%3==0 for a,b in FLIPS)
out['minimal_step_equals_minus_delta_a']=all(((7*a+4*b)-(-a))%12==0 and abs(a)<=2 for a,b in FLIPS)
# each flip type realised with the claimed step: check on the actual lattice for all 24 triads (uses winding.py flip)
src=open('../winding.py').read().split('res={}')[0]; g={}; exec(src,g)
flip=g['flip']; pcl=g['pc']
def lat(c):
    r,q=c; p=((7*r)%12,0)
    return frozenset({p,(p[0]+1,p[1]),(p[0],p[1]+1)}) if q=='M' else frozenset({p,(p[0]+1,p[1]),(p[0]+1,p[1]-1)})
ok=True
for c in V:
    for o in 'PLR':
        t0=lat(c); t1=flip(t0,o); old=next(iter(t0-t1)); new=next(iter(t1-t0))
        d,outn,inn,s=move(c,o)
        ok&= (pcl(old)==outn and pcl(new)==inn and s==-(new[0]-old[0]) and {pcl(x) for x in t1}==tri(d))
out['lattice_flip_step=-delta_a_all_72']=ok
json.dump(out,open('tune.json','w'),indent=1,default=str)
for k,v in out.items():
    if k!='reconstruction': print(k,v)
