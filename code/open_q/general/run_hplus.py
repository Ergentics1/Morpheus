"""Run brandt_gen on every mass-formula solution with narrow class number > 1 (from scan_n2/3/4.json)."""
import json, sys
from brandt_gen import *
done={}
try: done={json.dumps(r['key']):r for r in json.load(open('hplus_results.json'))}
except Exception: pass
out=list(done.values())
for n in (2,3,4):
    S=json.load(open(f'scan_n{n}.json'))
    for r in S['results']:
        if not r['sols'] or r['hplus']==1: continue
        F=Field(r['pol'].replace('x','y'))
        def prime(t):
            p,f,e,g=t
            for P in G.idealprimedec(F.nf,p):
                if int(P[3])==f and int(P[2])==e and str(P[1])==g: return P
            raise ValueError(t)
        for s in r['sols']:
            key=[r['pol'],s['v'],s['D'],s['N']]
            if json.dumps(key) in done: continue
            v=prime(s['v']); Ds=[prime(t) for t in s['D']]; Ns=[(prime(t),k) for t,k in s['N']]
            rec=run_one(F,Ds,Ns,v,r['pol']); rec['key']=key; rec['d']=r['d']
            out.append(rec); json.dump(out,open('hplus_results.json','w'),indent=0)
print('DONE',len(out))
