import mpmath as mp, json, math, sympy
mp.mp.dps=80
def fk(X,k,N): return abs(sum(mp.e**(2j*mp.pi*k*x/N) for x in X))
def counts(X,N,M):
    lams=[]
    for k in range(N): f=fk(X,k,N); lams+= [f,-f]
    V=2*N; E=3*N
    def Nm(m):
        s=mp.mpf(0)
        for l in lams:
            d=mp.sqrt(mp.mpc(l*l-8)); mu1=(l+d)/2; mu2=(l-d)/2; s+=mu1**m+mu2**m
        s+= (E-V)*(1+(-1)**m)
        return int(mp.nint(mp.re(s)))
    Ns={m:Nm(m) for m in range(1,M+1)}
    pi={m:sum(int(sympy.mobius(m//d))*Ns[d] for d in sympy.divisors(m))//m for m in Ns}
    return Ns,pi,lams
out={}
for N,X in ((12,(0,4,7)),(53,(0,17,31)),(31,(0,10,18))):
    Ns,pi,l=counts(X,N,160)
    err={m: float((pi[m]-mp.mpf(2)**(m+1)/m)/(mp.mpf(2)**(m/2)/m)) for m in range(6,161,2)}
    lam2=max(float(abs(x)) for x in l if abs(abs(x)-3)>1e-20)
    print(N,'lam2',round(lam2,5),'pi6..14',[pi[m] for m in range(6,15,2)],'maxnorm err m<=60',round(max(abs(err[m]) for m in err if m<=60),2),'m=100',round(err[100],1),'m=160',round(err[160],1))
    out[N]=dict(pi={m:str(pi[m]) for m in pi},err=err,lam2=lam2)
json.dump(out,open('explicit.json','w'))
# check 12 vs exact matrix counts
pc=json.load(open('prime_counts.json'))['pi']
print('match matrix', all(int(out[12]['pi'][m])==pc[str(m)] for m in range(1,61)))
