import cypari2, math, itertools, json
pari=cypari2.Pari(); pari.allocatemem(10**9)
def zm1(D):
    s=0
    for b in range(-int(math.isqrt(D)),int(math.isqrt(D))+1):
        if (b-D)%2==0 and b*b<D: s+=pari.sigma((D-b*b)//4)
    return pari(s)/60
# sanity vs lfun
for D in (5,8,17):
    print(D,zm1(D),pari(f'lfun(lfuncreate(x^2-{D}),-1)'))
def fund(D):
    return pari.isfundamental(D)
res=[]
for D in range(5,705):
    if not fund(D): continue
    if not (D%8==1 or D%4==0): continue
    K=pari.bnfinit(f'x^2-{D}' if D%4==0 else f'x^2-x-{(D-1)//4}',1)
    h=int(pari.bnf_get_no(K)) if hasattr(pari,'bnf_get_no') else int(K[7][0][0])
    hp=int(pari.bnrinit(K,pari('[1,[1,1]]'))[4][0]) if False else int(pari(f'bnrclassno({K},[1,[1,1]])')) if False else None
    res.append((D,h))
print(len(res))
