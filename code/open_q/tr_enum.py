"""Totally real F of degree n<=4 with a prime v of norm 2 and narrow class number 1.
Necessary condition for a torsion-free Cerednik-Drinfeld group G at v with G\\T = X:
  Mass = 2^(1-n)|zeta_F(-1)| prod_{p|D''}(Np-1) prod_{p^e||N} Np^(e-1)(Np+1) = 12,  n+|D''| even, v not dividing D''N,
and for each CM field K=F(sqrt(-1)),F(sqrt(-3)) (F(zeta_7) if F=Q(zeta_7)^+) the maximal order of K must NOT embed,
i.e. NOT[ all p|D'' non-split in K and all p|N exactly once and non-inert in K ] (otherwise torsion certainly exists).
h^+=1 implies totally positive units are squares, so no other CM orders carry extra units."""
import cypari2, json, sys
pari=cypari2.Pari(); pari.allocatemem(4*10**9); pari.set_real_precision(60)
pari('zm1f(f)=my(L=lfuncreate(f)); bestappr(lfun(L,-1),10^8)')
def fields(n,dmax):
    if n==2:
        return [pari(f'polredabs(x^2-{D})') if D%4==0 else pari(f'polredabs(x^2-x-{(D-1)//4})') for D in range(5,dmax+1) if int(pari.isfundamental(D))]
    if n==3: return list(pari(f'nflist("C3",[1,{dmax}],0)'))+list(pari(f'nflist("S3",[1,{dmax}],0)'))
    if n==4:
        out=[]
        for G in ("C4","V4","D4","A4","S4"):
            out+=list(pari(f'nflist("{G}",[1,{dmax}],0)'))
        return out
DMAX={2:1200,3:5200,4:60000}
results=[]; stats={}
for n in (2,3,4):
    Fs=fields(n,DMAX[n]); cnt=dict(total=len(Fs),norm2=0,hplus1=0,integral_target=0,mass_cands=0,survivors=0)
    for f in Fs:
        K=pari.bnfinit(f,1)
        has2=int(pari(f'#[pr|pr<-idealprimedec({K},2),pr.f==1]'))
        if not has2: continue
        cnt['norm2']+=1
        hp=int(pari(f'bnrclassno({K},[1,vector({n},i,1)])'))
        if hp!=1: continue
        cnt['hplus1']+=1
        z=pari(f'zm1f({f})'); d=int(pari.nfdisc(f))
        target=pari(12)*2**(n-1)/abs(z)
        if pari.denominator(target)!=1: continue
        cnt['integral_target']+=1; T=int(target)
        prs=pari(f'my(L=List());forprime(p=2,{T+1},foreach(idealprimedec({K},p),pr,if(pr.p^pr.f<={T+1},listput(L,pr))));Vec(L)')
        v=[i for i in range(len(prs)) if int(prs[i][0])==2 and int(prs[i][3])==1][0]
        avail=[i for i in range(len(prs)) if i!=v]; norms=[int(prs[i][0])**int(prs[i][3]) for i in range(len(prs))]
        cands=[]
        def rs(i,val,Ds,Ns):
            if val==T:
                if (n+len(Ds))%2==0: cands.append((list(Ds),list(Ns)))
                return
            if i==len(avail) or val>T: return
            j=avail[i]; q=norms[j]; rs(i+1,val,Ds,Ns)
            if T%(val*(q-1))==0: rs(i+1,val*(q-1),Ds+[j],Ns)
            e=1
            while val*q**(e-1)*(q+1)<=T:
                if T%(val*q**(e-1)*(q+1))==0: rs(i+1,val*q**(e-1)*(q+1),Ds,Ns+[(j,e)])
                e+=1
        rs(0,1,[],[])
        if not cands: continue
        # CM fields
        As=[1,3]
        if n==3 and d==49: As.append(7)
        nf=pari(f'nfinit(subst({f},x,y))')
        prsy=pari(f'my(nf=nfinit(subst({f},x,y)),L=List());forprime(p=2,{T+1},foreach(idealprimedec(nf,p),pr,if(pr.p^pr.f<={T+1},listput(L,pr))));Vec(L)')
        assert [int(q[0])**int(q[3]) for q in prsy]==norms
        RN={a:pari(f'rnfinit(nfinit(subst({f},x,y)),x^2+{a})') for a in As}
        def st_of(j,a):
            D=pari.rnfidealprimedec(RN[a],prsy[j])
            if len(D)==2: return 1
            # relative ramification index = absolute e in K divided by e(P/p) in F
            return 0 if int(D[0][2])//int(prsy[j][2])==2 else -1
        surv=[]
        for Ds,Ns in cands:
            killed=False
            for a in As:
                ok_all=True
                # need per-prime splitting; compute by matching: same rational prime, same f,e, and test membership of generators
                for j in Ds+[jj for jj,e in Ns]:
                    st=st_of(j,a)
                    st=int(st)
                    if j in Ds:
                        if st==1: ok_all=False
                    else:
                        e=[e for jj,e in Ns if jj==j][0]
                        if e>1 or st==-1: ok_all=False
                if ok_all: killed=True; break
            if not killed: surv.append((Ds,Ns))
        cnt['mass_cands']+=len(cands); cnt['survivors']+=len(surv)
        rec=dict(n=n,disc=d,pol=str(f),zeta=str(z),target=T,cands=[([norms[j] for j in Ds],[(norms[j],e) for j,e in Ns]) for Ds,Ns in cands],
                 survivors=[([norms[j] for j in Ds],[(norms[j],e) for j,e in Ns]) for Ds,Ns in surv])
        results.append(rec); print(rec,flush=True)
    stats[n]=cnt; print(n,cnt,flush=True)
json.dump(dict(stats=stats,results=results),open('tr_enum.json','w'),indent=1)
