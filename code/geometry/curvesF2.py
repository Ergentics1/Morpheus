"""Curves over F2: (1) the degree-44 Ihara-Weil polynomial is not the zeta of any curve (point counts); (2) explicit curves
for the factors; (3) exhaustive search of hyperelliptic curves of genus 4..7 over F2 whose L-polynomial contains the
octic 1+4u^2+9u^4+16u^6+16u^8 (the d=12 character stratum)."""
import numpy as np, sympy as sp, numba, json, itertools, math, time
u=sp.symbols('u')
AU=[]
def chk(name,ok,detail=''): AU.append((name,bool(ok),str(detail))); print(('PASS ' if ok else 'FAIL ')+name,detail)
E1=1-u+2*u**2; E2=1+u+2*u**2; S1=4*u**4-u**2+1; S2=4*u**4+u**2+1; O=16*u**8+16*u**6+9*u**4+4*u**2+1
P44=sp.expand(E1**3*E2**3*S1**2*S2**2*O**2)
chk('degree-44 polynomial, P(u)=q^22 u^44 P(1/(qu)) functional equation',sp.degree(P44,u)==44 and sp.expand(u**44*2**22*P44.subs(u,1/(2*u))-P44)==0)
roots=[complex(r) for F_ in (E1,E2,S1,S2,O) for r in sp.Poly(F_,u).nroots(n=30)]
chk('all inverse roots have |alpha|=sqrt2 (Riemann hypothesis holds; it is a q-Weil polynomial)',all(abs(abs(1/r)-2**.5)<1e-9 for r in roots))
def Nn(P,g,n):
    ser=sp.series(-u*sp.diff(P,u)/P,u,0,n+1).removeO()
    return int(2**n+1-ser.coeff(u,n))
N=[Nn(P44,22,n) for n in range(1,13)]
print('N_n of hypothetical genus-22 curve:',N)
chk('N_2=39 > N_6=27: impossible since C(F_4) is a subset of C(F_64) -> no curve over F_2 has this zeta',N[1]==39 and N[5]==27 and N[5]<N[1])
chk('also degree-2 places count: (N_2-N_1)/2 integer and >=0',(N[1]-N[0])%2==0)
# ---------- point counting on hyperelliptic curves y^2+h y = f over F_{2^n}
IRR={1:0b11,2:0b111,3:0b1011,4:0b10011,5:0b100101,6:0b1000011,7:0b10000011}
def tables(n):
    q=2**n; M=np.zeros((q,q),np.int64)
    for a in range(q):
        for b in range(q):
            r=0; x=a; y=b
            while y:
                if y&1: r^=x
                y>>=1; x<<=1
                if x>>n &1: x^=IRR[n]
            M[a,b]=r
    inv=np.zeros(q,np.int64)
    for a in range(1,q):
        for b in range(1,q):
            if M[a,b]==1: inv[a]=b
    tr=np.zeros(q,np.int64)
    for a in range(q):
        s=a; t=a
        for _ in range(n-1): t=M[t,t]; s^=t
        tr[a]=s
    pw=np.zeros((q,32),np.int64)
    for a in range(q):
        pw[a,0]=1
        for i in range(1,32): pw[a,i]=M[pw[a,i-1],a]
    return M,inv,tr,pw
TB={n:tables(n) for n in range(1,8)}
@numba.njit(cache=True)
def count(h,f,g,n,M,inv,tr,pw):
    q=1<<n; N=0
    for x in range(q):
        hx=0; fx=0
        for i in range(g+2):
            if (h>>i)&1: hx^=pw[x,i]
        for i in range(2*g+3):
            if (f>>i)&1: fx^=pw[x,i]
        if hx==0: N+=1
        else:
            z=M[fx,M[inv[hx],inv[hx]]]
            if tr[z]==0: N+=2
    hl=(h>>(g+1))&1; fl=(f>>(2*g+2))&1
    if hl==0: N+=1
    else:
        if (n*fl)%2==0: N+=2
    return N
def pmul(a,b):
    r=0
    while b:
        if b&1: r^=a
        b>>=1; a<<=1
    return r
def pmod(a,m):
    dm=m.bit_length()
    while a and a.bit_length()>=dm: a^=m<<(a.bit_length()-dm)
    return a
def pgcd(a,b):
    while b: a,b=b,pmod(a,b)
    return a
def deriv(a): # char 2 derivative
    r=0;i=1
    while (a>>i):
        if i%2==1 and (a>>i)&1: r|=1<<(i-1)
        i+=1
    return r
def rev(a,d): return int(format(a,'0%db'%(d+1))[::-1],2)
def smooth(h,f,g):
    if h==0: return False
    for H,Fp in ((h,f),(rev(h,g+1),rev(f,2*g+2))):
        if H==0: return False
        dH=deriv(H); dF=deriv(Fp)
        if pgcd(H, pmul(pmul(dH,dH),Fp) ^ pmul(dF,dF))!=1: return False
    return True
def Lpoly(Ns,g):
    # power sums s_n = q^n+1-N_n of inverse roots; L(u)=prod(1-alpha u) via Newton
    s=[2**n+1-Ns[n-1] for n in range(1,g+1)]
    e=[sp.Integer(1)]
    for k in range(1,g+1):
        e.append(sp.Rational(sum((-1)**(i-1)*e[k-i]*s[i-1] for i in range(1,k+1)),k))
    c=[(-1)**k*e[k] for k in range(g+1)]
    full=c+[2**(k)*c[g-k] for k in range(1,g+1)][::-1][::-1]
    coeffs=c[:]+[2**(g-k)*c[2*g-k]*0 for k in range(0)]
    L=sum(c[k]*u**k for k in range(g+1))+sum(2**(k-g)*c[2*g-k]*u**k for k in range(g+1,2*g+1))
    return sp.expand(L)
def curve_L(h,f,g):
    Ns=[count(h,f,g,n,*TB[n]) for n in range(1,g+1)]
    return Lpoly(Ns,g),Ns
# explicit factor curves
tests=[('E1: y^2+xy=x^3+x^2+1',1,0b10,0b1101,E1),('E2: y^2+xy=x^3+1',1,0b10,0b1001,E2),
       ('y^2+(x^2+x)y=x^5+x^3+x^2+x',2,0b110,0b101110,S1),('y^2+(x^2+x+1)y=x^5+x^3+x^2+1',2,0b111,0b101101,S2)]
for name,g,h,f,target in tests:
    L,Ns=curve_L(h,f,g); chk(f'{name}: smooth genus {g}, L = {target}',smooth(h,f,g) and sp.expand(L-target)==0,f'L={L}')
# predicted counts for a genus-4 curve with L = octic (4.2.a_e_a_j)
NO=[Nn(O,4,n) for n in range(1,9)]
print('genus-4 counts for L=octic:',NO)
# search
Opoly=sp.Poly(O,u)
found={}; stats={}
for g in (4,5,6,7):
    t=time.time(); cnt=0; hits=[]
    # representatives of f modulo {t^2+h t}: reduce f by Gaussian elimination against that space
    for h in range(1,1<<(g+2)):
        basis=[]
        for i in range(g+2):
            t_=1<<i; w=pmul(t_,t_)^pmul(h,t_)
            if w>>(2*g+3): continue
            for b in basis: w=min(w,w^b)
            if w: basis.append(w); basis.sort(reverse=True)
        # echelon reduce: canonical representative = min over coset
        piv=[]
        for b in sorted(basis,reverse=True):
            for p_ in piv: b=min(b,b^p_)
            if b: piv.append(b)
        piv.sort(reverse=True)
        lead={b.bit_length()-1:b for b in piv}
        free=[i for i in range(2*g+3) if i not in lead]
        for bits in range(1<<len(free)):
            f=0
            for j,i in enumerate(free):
                if (bits>>j)&1: f|=1<<i
            if not smooth(h,f,g): continue
            cnt+=1
            Ns=[count(h,f,g,n,*TB[n]) for n in range(1,g+1)]
            L=Lpoly(Ns,g)
            if sp.Poly(L,u).rem(Opoly).is_zero: hits.append((h,f,str(sp.factor(L))))
    stats[g]=cnt; found[g]=hits
    print('genus',g,'smooth hyperelliptic models (reduced):',cnt,'hits:',len(hits),round(time.time()-t,1),'s')
    for x in hits[:5]: print('   h=%s f=%s L=%s'%(bin(x[0]),bin(x[1]),x[2]))
chk('no hyperelliptic genus-4 curve over F2 has Jacobian in class 4.2.a_e_a_j',len(found[4])==0)
json.dump(dict(N44=N,N_octic=NO,search_stats=stats,hits={g:found[g] for g in found},audit=AU),open('curvesF2.json','w'),indent=1)
print(sum(a[1] for a in AU),'/',len(AU))
