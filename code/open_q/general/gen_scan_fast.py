"""Fast, resumable, parallel version of gen_scan.py for degree 5/6 field lists.
Rigorous prefilter: |zeta_F(-1)| = d^(3/2) zeta_F(2)/(2 pi^2)^n and zeta_F(2) >= its Euler product over p < 2000
(every factor exceeds 1); the mass equation forces |zeta_F(-1)| <= 12 u 2^(n-1) <= 12*4^(n-1).
Fields failing the bound (first with u<=2^(n-1), then with the true u) cannot carry a solution."""
import cypari2, json, math, sys, os
from multiprocessing import Pool
import gen_scan
def work(args):
    pol,n=args
    pari=cypari2.Pari(); pari.allocatemem(10**9); pari.set_real_precision(60)
    gen_scan.pari=pari
    nf=pari(f'nfinit({pol})'); d=int(pari(f'({nf}).disc'))
    if len(pari(f'[pr|pr<-idealprimedec({nf},2),pr.f==1]'))==0: return dict(pol=pol,skip='no norm-2 prime')
    E=float(pari(f'prod(i=1,1,1.)*prodeuler(p=2,2000,prod(j=1,#idealprimedec({nf},p),1/(1-1.0/idealnorm({nf},idealprimedec({nf},p)[j])^2)))'))
    lb=d**1.5*E/(2*math.pi**2)**n
    if lb>12*4**(n-1)*1.000001: return dict(pol=pol,d=d,skip='prefilter u<=2^(n-1)',lb=lb)
    K=pari(f'bnfinit({pol},1)'); h=int(pari(f'({K}).no')); hp=int(pari(f'bnrclassno({K},[1,vector({n},i,1)])'))
    u=hp//h
    if lb>12*u*2**(n-1)*1.000001: return dict(pol=pol,d=d,h=h,hplus=hp,skip='prefilter true u',lb=lb)
    r=gen_scan.solve(pol,n); r['lb']=lb; return r
if __name__=='__main__':
    n=int(sys.argv[1]); pols=json.load(open(sys.argv[2])); ck=f'scan{n}_fast.jsonl'
    done=set()
    if os.path.exists(ck):
        for l in open(ck): done.add(json.loads(l)['pol'])
    todo=[(p,n) for p in pols if p not in done]
    print('todo',len(todo),flush=True)
    with Pool(int(sys.argv[3]) if len(sys.argv)>3 else 6) as P, open(ck,'a') as f:
        for r in P.imap_unordered(work,todo,chunksize=4):
            f.write(json.dumps(r)+'\n'); f.flush()
            if r.get('sols'): print(r['d'],r['h'],r['hplus'],r['zeta'],r['T'],len(r['sols']),flush=True)
    R=[json.loads(l) for l in open(ck)]
    res=[r for r in R if r.get('skip')!='no norm-2 prime']
    full=[r for r in res if 'skip' not in r]
    json.dump(dict(n=n,bound=gen_scan.bound(n),nfields=len(pols),n_with_norm2=len(res),n_prefiltered=len(res)-len(full),results=full),open(f'scan_n{n}.json','w'),indent=0)
    print('n',n,'fields',len(pols),'with norm-2 prime',len(res),'prefiltered',len(res)-len(full),'with solutions',sum(1 for r in full if r['sols']),'h+>1 among them',sum(1 for r in full if r['sols'] and r['hplus']>1))
