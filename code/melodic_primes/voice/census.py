from voices import *
from fractions import Fraction
import math
starts=[(r,q) for r in range(12) for q in 'Mm']
res={}
MAXM=int(sys.argv[1]) if len(sys.argv)>1 else 16
examples={}
for m in range(2,MAXM+1,2):
    C=collections.Counter(); pitchlines=set(); contours=set(); tot=0
    plmap=collections.defaultdict(set)
    for w in closed_words(m):
        for c0 in starts:
            c,start,end,steps,arr,mover=walk(c0,w)
            if c!=c0: continue
            # harmonic primitivity: walk (chord sequence) not periodic
            chords=[c0]; cc=c0
            for op in w[:-1]: cc=OPS[op](cc); chords.append(cc)
            hp=minper(list(zip(chords,w)))
            if hp<m: continue
            tot+=1
            sig=perm(start,end); disp=tuple(e-s for s,e in zip(start,end))
            W=sum(steps)//12; assert sum(steps)%12==0
            home=all(d==0 for d in disp)
            ip=minper(steps); pp=minper(arr)
            semis=sum(1 for s in steps if abs(s)==1)
            key=(ptype(sig),home,W,ip<m,pp<m,semis)
            C[key]+=1
            pitchlines.add(canon(arr)); contours.add(canon(steps))
            plmap[canon(arr)].add(canon(list(zip(chords,w))))
            ex=(ptype(sig),home,ip<m)
            if ex not in examples.get(m,{}):
                examples.setdefault(m,{})[ex]=dict(word=w,chords='-'.join(cname(x) for x in chords),arr='-'.join(NM[a] for a in arr),steps=steps,disp=disp,perm=sig)
    agg=lambda f: {k:Fraction(v,m) for k,v in sorted(((kk,sum(vv for key,vv in C.items() if f(key)==kk)) for kk in set(f(key) for key in C)))}
    pi=Fraction(tot,m)
    out=dict(pi=pi,
        perm=agg(lambda k:k[0]), home=agg(lambda k:(k[0],k[1])), W=agg(lambda k:k[2]),
        seq_interval_periodic=agg(lambda k:k[3]), pitchline_periodic=agg(lambda k:k[4]),
        semis=agg(lambda k:k[5]),
        distinct_pitchlines=len(pitchlines), distinct_contours=len(contours),
        pitchline_collisions=sum(1 for v in plmap.values() if len(v)>1))
    print(m,{k:(str(v) if isinstance(v,Fraction) else {str(a):str(b) for a,b in v.items()} if isinstance(v,dict) else v) for k,v in out.items()},flush=True)
    res[m]={k:(str(v) if isinstance(v,Fraction) else {str(a):str(b) for a,b in v.items()} if isinstance(v,dict) else v) for k,v in out.items()}
json.dump(dict(census=res,examples={m:{str(k):v for k,v in d.items()} for m,d in examples.items()}),open('census.json','w'),indent=1)
