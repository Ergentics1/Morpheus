import itertools, collections, math, json
N=12; S=[3,-3,4,-4,5,-5]
NM=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
def primes(m):
    seen=set(); out=[]
    for w in itertools.product(S,repeat=m):
        if sum(w)%N: continue
        if any((w[i]+w[(i+1)%m])%N==0 for i in range(m)): continue
        # primitive as graph walk: no proper prefix of length d|m with sum 0 and w = prefix^(m/d)
        if any(m%d==0 and sum(w[:d])%N==0 and w==w[:d]*(m//d) for d in range(1,m)): continue
        for v in range(N):
            key=min(((v+sum(w[:i]))%N,w[i:]+w[:i]) for i in range(m))
            if key in seen: continue
            seen.add(key); out.append(key)
    return out
res={}
for m in range(3,8):
    P=primes(m)
    # transposition stabilizer
    S_=set(P); sym=0; ex_sym=None; ex=None
    for v,w in P:
        st=sum(1 for t in range(1,N) if min(((v+t+sum(w[:i]))%N,w[i:]+w[:i]) for i in range(m))==(v,w))
        if st: sym+=1; ex_sym=ex_sym or (v,w)
        else: ex=ex or (v,w)
    def mel(p):
        v,w=p; s=[NM[v]]; 
        for x in w: v=(v+x)%N; s.append(NM[v])
        return '-'.join(s)
    res[m]=dict(total=len(P),symmetric=sym,free=len(P)-sym)
    print(m,len(P),'symmetric (limited transposition):',sym,'| ex free',mel(ex),'| ex sym',mel(ex_sym) if ex_sym else None,flush=True)
json.dump(res,open('tonnetz_classes.json','w'))
