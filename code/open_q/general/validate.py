import json,sys; sys.argv=[sys.argv[0]]
from brandt_gen import *
out=[]
for pol,Dn,Nn in [('y^3-2*y^2-6*y-1',[13],[]),('y^2-y-34',[],[(2,1)]),('y^4-26*y^2-8*y+1',[],[(71,1)])]:
    F=Field(pol)
    def pn(q): p=int(sp.factorint(q).popitem()[0]); return [P for P in G.idealprimedec(F.nf,p) if int(G.idealnorm(F.nf,P))==q]
    Ds=[pn(q)[0] for q in Dn]; Ns=[(pn(q)[0],e) for q,e in Nn]
    used=[G.idealhnf(F.nf,P) for P in Ds+[P for P,e in Ns]]
    v=[P for P in pn(2) if G.idealhnf(F.nf,P) not in used][0]
    out.append(run_one(F,Ds,Ns,v,pol))
json.dump(out,open('validate.json','w'),indent=0)
