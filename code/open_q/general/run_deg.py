"""Run brandt_gen on every mass-formula solution of scan_n{n}.json (any narrow class number)."""
import json, sys
from brandt_gen import *
n=int(sys.argv[1]); outf=f'deg{n}_results.json'
import os
out=json.load(open(outf)) if os.path.exists(outf) else []
done=[tuple(json.dumps(x) for x in r['key']) for r in out]
S=json.load(open(f'scan_n{n}.json'))
for r in S['results']:
    if not r['sols']: continue
    F=Field(r['pol'].replace('x','y'))
    def prime(t):
        p,f,e,g=t
        for P in G.idealprimedec(F.nf,p):
            if int(P[3])==f and int(P[2])==e and str(P[1])==g: return P
        raise ValueError(t)
    for s in r['sols']:
        if tuple(json.dumps(x) for x in [r['pol'],s['v'],s['D'],s['N']]) in done: continue
        v=prime(s['v']); Ds=[prime(t) for t in s['D']]; Ns=[(prime(t),k) for t,k in s['N']]
        rec=run_one(F,Ds,Ns,v,r['pol']); rec['key']=[r['pol'],s['v'],s['D'],s['N']]; rec['d']=r['d']
        out.append(rec); json.dump(out,open(outf,'w'),indent=0)
print('DONE',len(out))
