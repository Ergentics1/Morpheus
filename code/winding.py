import itertools, collections, json, sys
sys.setrecursionlimit(10000)
NAMES=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
def pc(p): return (7*p[0]+4*p[1])%12
C0=frozenset({(0,0),(1,0),(0,1)})
def flip(tri,op):
    s=list(tri)
    for u,v in itertools.combinations(s,2):
        d=(v[0]-u[0],v[1]-u[1])
        kind={ (1,0):'P',(-1,0):'P',(0,1):'R',(0,-1):'R',(1,-1):'L',(-1,1):'L'}.get(d)
        if kind==op:
            w=[x for x in s if x!=u and x!=v][0]
            return frozenset({u,v,(u[0]+v[0]-w[0],u[1]+v[1]-w[1])})
    raise Exception
def run(w,tri=C0):
    for ch in w: tri=flip(tri,ch)
    return tri
def trans(t0,t1):
    a=sorted(t0); b=sorted(t1)
    d=(b[0][0]-a[0][0],b[0][1]-a[0][1])
    assert all((y[0]-x[0],y[1]-x[1])==d for x,y in zip(a,b)),(a,b)
    return d
def wind(d):
    # d = u*(4,-4)+v*(0,3)
    a,b=d; assert a%4==0; u=a//4; vv=b+4*u; assert vv%3==0; return (u,vv//3)
def primes_words(m):
    out=collections.Counter(); ex={}
    for w in itertools.product('PLR',repeat=m):
        if any(w[i]==w[(i+1)%m] for i in range(m)): continue
        t=run(w)
        if {pc(p) for p in t}!={pc(p) for p in C0}: continue
        # same chord => translation
        a=sorted(t);b=sorted(C0)
        # match by pitch class
        d=None
        for x in t:
            pass
        d=trans(C0,t) if sorted(pc(p) for p in sorted(t))==sorted(pc(p) for p in sorted(C0)) else None
        try: d=trans(C0,t)
        except AssertionError: continue
        k=wind(d); out[(k)]+=1; ex.setdefault(k,''.join(w))
    return out,ex
res={}
for m in range(6,15,2):
    c,ex=primes_words(m)
    # words from C, each rooted closed walk; primes count = 24*words/m (all primitive? check later)
    print(m,dict(c),'total words',sum(c.values()))
    print('   examples',ex)
    res[m]={str(k):v for k,v in c.items()}
json.dump(res,open('winding.json','w'))
