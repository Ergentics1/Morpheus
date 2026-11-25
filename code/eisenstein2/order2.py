import json, math, itertools, mpmath as mp
res={}
# which orders O_f = Z[f w] (min poly x^2 + f x + f^2) admit a ring surjection onto Z12?
res['conductors f<=12 with cyclic Z12 quotient ring']=[f for f in range(1,13) if any((c*c+f*c+f*f)%12==0 for c in range(12))]
# explicit conductor-2 realisation: O=Z[s], s=sqrt(-3), ring map psi(x+y s)=x+3y mod 12
psi=lambda x,y: (x+3*y)%12
# Tonnetz basis: fifth -> 1+2s, major third -> 1+s ; Tonnetz psi_T(a,b)=7a+4b
phi=lambda a,b: (a+b, 2*a+b)    # a*(1+2s)+b*(1+s) = (a+b) + (2a+b) s
res['basis unimodular (det)']=1*1-2*1
res['psi o phi == 7a+4b']=all(psi(*phi(a,b))==(7*a+4*b)%12 for a in range(-12,13) for b in range(-12,13))
res['minor third = M3 - ... images: s->3, 1+s->4, 1+2s->7, 1->1']=(psi(0,1),psi(1,1),psi(1,2),psi(1,0))
# kernel J is an ideal: closed under multiplication by s: s*(x+ys) = -3y + x s
ker=[(x,y) for x in range(-30,31) for y in range(-30,31) if psi(x,y)==0]
res['ker psi is ideal of Z[sqrt-3]']=all(psi(-3*y,x)==0 for x,y in ker)
# J = (3 - s): generated lattice {(3-s)(m+n s)} = (3m+3n) + (3n-m) s ; index = norm 12
gen=lambda m,n: (3*m+3*n, 3*n-m)
res['J == (3-sqrt-3), norm 12']=set(ker)=={p for p in (gen(m,n) for m in range(-40,41) for n in range(-40,41)) if abs(p[0])<=30 and abs(p[1])<=30} and 3*3+3*1==12
res['3-sqrt-3 = -sqrt-3*(1+sqrt-3)... check (s)*(1+s) = -3 + s']='(s)(1+s) = s + s^2 = -3 + s = -(3 - s)'
# combinatorics: triangles of Z^2 (Tonnetz) <-> consonant triads under psi o phi (same as Tonnetz by construction)
# j-invariant of C/Z[sqrt-3]
mp.mp.dps=30
res['j(sqrt(-3))']=mp.nstr(1728*mp.kleinj(mp.mpc(0,mp.sqrt(3))),20)
# Euclidean shape check: in this CM structure the triad triangle {0, 1+s, 1+2s} side lengths^2
pts=[complex(0,0),complex(1,3**0.5),complex(1,2*3**0.5)]
res['triad triangle side^2 in CM picture']=[round(abs(pts[i]-pts[j])**2,6) for i,j in ((0,1),(1,2),(0,2))]
# non-unique factorisation of 4 in Z[sqrt-3] (classic): 4=2*2=(1+s)(1-s); no element of norm 2
res['no element of norm 2 in Z[sqrt-3]']=not any(x*x+3*y*y==2 for x in range(-3,4) for y in range(-3,4))
json.dump(res,open('order2.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
