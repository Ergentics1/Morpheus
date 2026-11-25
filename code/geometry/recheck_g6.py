# independent pure-python point count (galois-free, using sympy GF(2^n) via polynomial arithmetic) of
# C6: y^2 + (x^6+x^5+x^4+x^3+1) y = x^13 + x^3 + x over F_{2^n}, n=1..6, then L-polynomial
import sympy as sp, json
from sympy import GF, Poly, symbols
X,u=symbols('X u')
IRR={1:X+1,2:X**2+X+1,3:X**3+X+1,4:X**4+X+1,5:X**5+X**2+1,6:X**6+X+1}
def elems(n):
    for i in range(2**n): yield Poly(sum(((i>>k)&1)*X**k for k in range(n)),X,modulus=2)
def red(p,n): return p.rem(Poly(IRR[n],X,modulus=2))
def ev(coeffs,x,n):
    r=Poly(0,X,modulus=2)
    for c in reversed(coeffs): r=red(r*x+Poly(c,X,modulus=2),n)
    return r
h=[1,0,0,1,1,1,1]; f=[0,1,0,1]+[0]*9+[1]
Ns=[]
for n in range(1,7):
    E=list(elems(n)); sq={}
    N=0
    for x in E:
        hx=ev(h,x,n); fx=ev(f,x,n)
        N+=sum(1 for y in E if red(y*y+hx*y+fx,n).is_zero)
    # infinity: weighted model degree g+1=7: h has x^7 coeff 0 -> one point (Y^2 = f_14 = 0 over leading)  
    N+=1
    Ns.append(N)
g=6; s=[2**n+1-Ns[n-1] for n in range(1,g+1)]
e=[sp.Integer(1)]
for k in range(1,g+1): e.append(sp.Rational(sum((-1)**(i-1)*e[k-i]*s[i-1] for i in range(1,k+1)),k))
c=[(-1)**k*e[k] for k in range(g+1)]
L=sp.expand(sum(c[k]*u**k for k in range(g+1))+sum(2**(k-g)*c[2*g-k]*u**k for k in range(g+1,2*g+1)))
print(Ns, sp.factor(L))
ok=sp.expand(L-(4*u**4-3*u**2+1)*(16*u**8+16*u**6+9*u**4+4*u**2+1))==0
print('PASS' if ok else 'FAIL','independent recount of genus-6 curve')
json.dump(dict(N=Ns,L=str(sp.factor(L)),ok=ok),open('recheck_g6.json','w'))
