import sympy as sp, json, itertools
x,T,u=sp.symbols('x T u')
res={}
oct_=sp.expand(sp.resultant(x**4-4*x**2+1, T**2-x*T+2, x))
res['octic weil poly']=str(oct_)
res['octic L(u)']=str(sp.expand(oct_.subs(T,1/u)*u**8))
res['octic irreducible over Q']=sp.Poly(oct_,T).is_irreducible
W={'E+ (lam=1)':T**2-T+2,'E- (lam=-1)':T**2+T+2,'S5 (lam=±sqrt5)':T**4-T**2+4,'S3 (lam=±sqrt3)':T**4+T**2+4,'A4 (lam^2=2±sqrt3)':oct_}
# Weil check: all roots |.|=sqrt2
import mpmath as mp
for k,p in W.items():
    rts=sp.Poly(p,T).nroots(n=30)
    # CM field tests: which sqrt(d) lie in Q(pi): p factors over Q(sqrt d)
    sub=[d for d in (-1,-2,-3,-5,-7,-15,-21,-35,2,3,5,6,7,15) if len(sp.factor_list(p,extension=sp.sqrt(d))[1])>1]
    disc=sp.discriminant(p,T)
    res[k]=dict(poly=str(p),weil=all(abs(abs(complex(r))-2**0.5)<1e-20 for r in rts),
                splits_over_Q_sqrt=sub, poly_disc=str(sp.factorint(disc)),
                N1=int(3-sum(complex(r) for r in rts).real) if sp.degree(p,T)==2 else None)
# point counts of curves for the L-polys: for abelian variety A with Weil poly P, #A(F2)=P(1)
for k,p in W.items(): res[k]['#A(F_2)=P(1)']=int(p.subs(T,1))
# brute force elliptic curves over F2: y^2 + a1 xy + a3 y = x^3 + a2 x^2 + a4 x + a6
def count_E(a):
    a1,a2,a3,a4,a6=a; n=1
    for X in (0,1):
        for Y in (0,1):
            if (Y*Y+a1*X*Y+a3*Y-(X**3+a2*X*X+a4*X+a6))%2==0: n+=1
    return n
def smooth(a):
    a1,a2,a3,a4,a6=a
    b2=a1*a1+4*a2; b4=2*a4+a1*a3; b6=a3*a3+4*a6; b8=a1*a1*a6+4*a2*a6-a1*a3*a4+a2*a3*a3-a4*a4
    D=-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
    return D%2!=0
ex={}
for a in itertools.product((0,1),repeat=5):
    if smooth(a):
        tr=3-count_E(a); ex.setdefault(tr,a)
res['elliptic curves over F2 by trace a (example [a1,a2,a3,a4,a6])']={k:list(v) for k,v in sorted(ex.items())}
json.dump(res,open('arith2.json','w'),indent=1,default=str)
for k,v in res.items(): print(k,':',v)
