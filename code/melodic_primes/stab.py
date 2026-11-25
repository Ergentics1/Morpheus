import itertools, collections
N=12; S=[3,-3,4,-4,5,-5]
exec(open('classify.py').read().split('res={}')[0])
for m in (3,4,6,8):
    P=primes(m); c=collections.Counter()
    for v,w in P:
        st=1+sum(1 for t in range(1,N) if min(((v+t+sum(w[:i]))%N,w[i:]+w[:i]) for i in range(m))==(v,w))
        c[st]+=1
    print(m,len(P),dict(c),'free/12 =',c[1]/12)
