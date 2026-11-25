import sys; sys.argv=[sys.argv[0]]
from voices import *
sys.path.insert(0,'../..')
import importlib.util
src=open('../../winding.py').read().split('res={}')[0]; g={}; exec(src,g)
flip,trans,wind,pcl=g['flip'],g['trans'],g['wind'],g['pc']
def lat(c):
    r,q=c; p=((7*r)%12,0)
    if q=='M': return frozenset({p,(p[0]+1,p[1]),(p[0],p[1]+1)})
    return frozenset({p,(p[0]+1,p[1]),(p[0]+1,p[1]-1)})
starts=[(r,q) for r in range(12) for q in 'Mm']
MAXM=int(sys.stdin.readline() or 16)
res={}
for m in range(6,MAXM+1,2):
    C=collections.Counter(); lines=collections.Counter(); per=0; tot=0; bad=0
    for w in closed_words(m):
        for c0 in starts:
            c,start,end,steps,arr,mover=walk(c0,w)
            if c!=c0: continue
            chords=[c0]; cc=c0
            for op in w[:-1]: cc=OPS[op](cc); chords.append(cc)
            if minper(list(zip(chords,w)))<m: continue
            tot+=1
            t0=lat(c0); t=t0
            for op in w: t=flip(t,op)
            u,v=wind(trans(t0,t))
            W=sum(steps)//12; sig=perm(start,end); disp=tuple(e-s for s,e in zip(start,end))
            # claims
            rho={0:(0,1,2),1:None,2:None}
            C[(u,v,W,ptype(sig),disp==(0,0,0),tuple(sorted(disp)))]+=1
            lines[canon(arr)]+=1
            if minper(arr)<m: per+=1
    print('m',m,'pi',tot//m,'pitchline classes',len(lines),'max mult',max(lines.values())//m if lines else 0,'periodic lines',per)
    agg=collections.Counter()
    for k,n in C.items(): agg[k]+=n
    for k in sorted(agg): print('   (u,v)=%s W=%d perm=%s home=%s disp=%s : %s'%((k[0],k[1]),k[2],k[3],k[4],k[5],agg[k]//m))
    res[m]=[[list(k[:2]),k[2],k[3],k[4],list(k[5]),n//m] for k,n in agg.items()]
    sys.stdout.flush()
json.dump(res,open('census2.json','w'))
