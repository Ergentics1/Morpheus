"""General mass scan for item (1): any narrow class number, degrees 2-4 (PARI nflist, complete),
degree 5 from a supplied field list. Condition (torsion-free component of genus 13, Nv=2):
   2^(1-n) |zeta_F(-1)| prod_{p|D''}(Np-1) prod_{p^e||N} Np^(e-1)(Np+1) = 12 u,  u = h+/h,
with v a prime of norm 2, v not dividing D''N, |D''| = n mod 2. Field bound: rd <= (8 pi^2)^(2/3) (9/4)^(2/(3n))."""
import cypari2, json, math, sys
pari=cypari2.Pari(); pari.allocatemem(4*10**9); pari.set_real_precision(60)
def bound(n): return int(((9/4)*(8*math.pi**2)**n)**(2/3))+1
def fields(n):
    B=bound(n); ng={2:1,3:2,4:5}[n]
    return [str(p) for g in range(1,ng+1) for p in pari(f'nflist([{n},{g}],[1,{B}],0)')]
def solve(pol,n):
    K=pari(f'bnfinit({pol},1)')
    pr2=pari(f'[pr|pr<-idealprimedec({K},2),pr.f==1]')
    if len(pr2)==0: return None
    d=int(pari(f'({K}).disc')); h=int(pari(f'({K}).no')); hp=int(pari(f'bnrclassno({K},[1,vector({n},i,1)])'))
    z=pari(f'lfun(lfuncreate({pol}),-1)'); zr=pari(f'bestappr({z},10^15)')
    assert abs(float(pari(f'({z})-({zr})')))<1e-35, (pol,z)
    u=hp//h; T=pari(f'12*{u}*2^({n}-1)/abs({zr})')
    rec=dict(pol=pol,n=n,d=d,h=h,hplus=hp,u=u,zeta=str(zr),T=str(T),n2=len(pr2),sols=[])
    if pari.denominator(T)!=1: return rec
    T=int(T)
    P=pari(f'L=List();forprime(p=2,{T+1},foreach(idealprimedec({K},p),pr,if(pr.p^pr.f<={T+1},listput(L,[pr.p,pr.f,pr.e,pr.gen[2]]))));Vec(L)')
    primes=[(int(a[0]),int(a[1]),int(a[2]),str(a[3])) for a in P]
    norms=[p**f for p,f,e,g in primes]
    for vi,(p,f,e,g) in enumerate(primes):
        if not(p==2 and f==1): continue
        avail=[j for j in range(len(primes)) if j!=vi]; out=[]
        def rs(i,val,Ds,Ns):
            if val==T:
                if len(Ds)%2==n%2: out.append(([primes[j] for j in Ds],[(primes[j],k) for j,k in Ns]))
                return
            if i==len(avail): return
            j=avail[i]; q=norms[j]; rs(i+1,val,Ds,Ns)
            if T%(val*(q-1))==0: rs(i+1,val*(q-1),Ds+[j],Ns)
            k=1
            while val*q**(k-1)*(q+1)<=T:
                if T%(val*q**(k-1)*(q+1))==0: rs(i+1,val*q**(k-1)*(q+1),Ds,Ns+[(j,k)])
                k+=1
        rs(0,1,[],[])
        for Ds,Ns in out: rec['sols'].append(dict(v=primes[vi],D=Ds,N=Ns))
    return rec
if __name__=='__main__':
    n=int(sys.argv[1]); src=sys.argv[2] if len(sys.argv)>2 else None
    pols=json.load(open(src)) if src else fields(n)
    res=[]
    for i,pol in enumerate(pols):
        r=solve(pol,n)
        if r: res.append(r)
        if r and r['sols']: print(r['d'],r['h'],r['hplus'],r['zeta'],r['T'],len(r['sols']),flush=True)
    json.dump(dict(n=n,bound=bound(n),nfields=len(pols),n_with_norm2=len(res),results=res),open(f'scan_n{n}.json','w'),indent=0)
    print('n',n,'bound',bound(n),'fields',len(pols),'with norm-2 prime',len(res),'with solutions',sum(1 for r in res if r['sols']),'h+>1 among them',sum(1 for r in res if r['sols'] and r['hplus']>1))
