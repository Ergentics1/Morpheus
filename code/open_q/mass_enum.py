"""Real quadratic F with a prime v of norm 2; narrow class number 1.
Torsion-free Cerednik-Drinfeld group G with G\\T = X (24 vertices) needs: definite B' over F ramified exactly at
the 2 real places and an even set D'' of finite primes, Eichler level N, v not dividing D''N, with
Mass = (1/2)|zeta_F(-1)| h_F prod_{p|D''}(Np-1) prod_{p^e||N} Np^(e-1)(Np+1) = 12 exactly (all unit indices 1, h(O)=12)."""
import cypari2, math, itertools, json
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
pari('zm1(D)=sum(b=-sqrtint(D),sqrtint(D),if((b-D)%2==0&&b^2<D,sigma((D-b^2)/4),0))/60')
pari('pol(D)=if(D%4==0,x^2-D/4,x^2-x-(D-1)/4)')
out=[]
for D in range(5,1200):
    if not int(pari.isfundamental(D)) or not (D%8==1 or D%4==0): continue
    z=pari(f'zm1({D})')
    K=pari(f'bnfinit(pol({D}),1)')
    h=int(pari(f'({K}).no')); hp=int(pari(f'bnrclassno({K},[1,[1,1]])'))
    target=pari(24)/(z*h)
    rec=dict(D=D,zeta=str(z),h=h,hplus=hp,target=str(target))
    if hp!=1: rec['note']='narrow class number >1 (not treated)'; out.append(rec); continue
    if pari.denominator(target)!=1: rec['cands']=[]; out.append(rec); continue
    T=int(target)
    P=pari(f'K=bnfinit(pol({D}),1); L=List(); forprime(p=2,{T+1},foreach(idealprimedec(K,p),pr,if(pr.p^pr.f<={T+1},listput(L,[pr.p,pr.f,pr.e])))); Vec(L)')
    primes=[(int(a[0]),int(a[1]),int(a[2])) for a in P]
    norms=[(p**f) for p,f,e in primes]
    idx2=[i for i,(p,f,e) in enumerate(primes) if p==2 and f==1]
    if not idx2: continue
    avail=list(range(len(primes))); avail.remove(idx2[0])
    cands=[]
    def rs(i,val,Dset,Nset):
        if val==T:
            if len(Dset)%2==0: cands.append((tuple(norms[j] for j in Dset),tuple((norms[j],e) for j,e in Nset)))
            return
        if i==len(avail) or val>T: return
        j=avail[i]; q=norms[j]
        rs(i+1,val,Dset,Nset)
        if q-1>=1 and T%(val*(q-1))==0: rs(i+1,val*(q-1),Dset+[j],Nset)
        e=1
        while True:
            f=q**(e-1)*(q+1)
            if val*f>T: break
            if T%(val*f)==0: rs(i+1,val*f,Dset,Nset+[(j,e)])
            e+=1
    rs(0,1,[],[])
    rec['cands']=cands; out.append(rec)
    print(D,'h',h,'zeta',z,'target',T,'#cands',len(cands),cands[:8],flush=True)
json.dump(out,open('mass_candidates.json','w'),indent=1)
print('fields with h+=1:',sum(1 for r in out if r['hplus']==1),' h+>1:',[r['D'] for r in out if r['hplus']!=1])
