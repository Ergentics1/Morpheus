# exhaustive: all homomorphisms psi: Z[w] -> Z12 whose up-triangles are consonant triads (Tonnetz-type);
# which kernels are ideals of Z[w], of Z[zeta12]-type, or modules over orders Z+fZ[w]?
import json, itertools, math
res={}
CONS={frozenset({r%12,(r+4)%12,(r+7)%12}) for r in range(12)}|{frozenset({r%12,(r+3)%12,(r+7)%12}) for r in range(12)}
sols=[]
for a in range(12):
    for b in range(12):
        # psi(m+n w)=a m + b n ; up triangle 0,1,-w^2=1+w ; down triangle 0, 1+w, w
        up={0,a%12,(a+b)%12}; dn={0,(a+b)%12,b%12}
        if frozenset(up) in CONS and frozenset(dn) in CONS and math.gcd(math.gcd(a,b),12)==1:
            sols.append((a,b))
res['n_tonnetz_homs']=len(sols)
def kernel(a,b): return [(m,n) for m in range(-24,25) for n in range(-24,25) if (a*m+b*n)%12==0]
def preserves(a,b,c,d,ker):  # multiplication by c+dw
    return all((a*(c*m-d*n)+b*(c*n+d*m-d*n))%12==0 for m,n in ker)
conds=set(); ideal=False
for a,b in sols:
    ker=kernel(a,b)
    f=min(d for d in range(1,13) if preserves(a,b,0,d,ker))
    conds.add(f); ideal|= preserves(a,b,0,1,ker)
res['multiplier ring conductors over all Tonnetz homs']=sorted(conds)
res['any kernel an ideal of Z[w]']=ideal
res['Phi12 = x^4-x^2+1 roots mod 4, mod 3']=([x for x in range(4) if (x**4-x*x+1)%4==0],[x for x in range(3) if (x**4-x*x+1)%3==0])
res['x^2+1 roots mod 4 (Z4 as Z[i]-quotient?)']=[x for x in range(4) if (x*x+1)%4==0]
res['x^2+x+1 roots mod 4']=[x for x in range(4) if (x*x+x+1)%4==0]
# norm-12 ideals: Z[w]: only (2)(sqrt-3): quotient F4 x F3 ; Z[zeta12]: residue degrees f(2)=2 (N=4), f(3)=2 (N=9) -> no norm 12
res['norm-12 ideals Z[zeta12]']='none (prime norms above 2,3 are 4 and 9)'
# order of conductor 2: Z[sqrt-3]; is there a cyclic Z12 quotient ring? need x^2+3=0 mod 12 solvable
res['x^2+3=0 mod 12 roots (Z[sqrt-3] cyclic quotient)']=[x for x in range(12) if (x*x+3)%12==0]
res['x^2+3=0 mod 4 roots']=[x for x in range(4) if (x*x+3)%4==0]
# period lattice quadratic form and theta coefficients
Q=lambda u,v: 16*u*u-12*u*v+9*v*v
from collections import Counter
th=Counter(Q(u,v) for u in range(-20,21) for v in range(-20,21))
res['period form 16u^2-12uv+9v^2 theta coeffs n<=40']={n:th[n] for n in sorted(th) if n<=40}
# reduce form
a,b,c=16,-12,9
while True:
    if a>c or (a==c and b<0): a,c=c,a; b=-b
    if abs(b)>a or b==-a:
        k=(a-b)//(2*a); b,c=b+2*k*a, a*k*k+b*k+c; continue
    if a>c: continue
    break
res['reduced period form']=(a,b,c); res['disc']=b*b-4*a*c
json.dump(res,open('quotients.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
