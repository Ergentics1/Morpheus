"""Spectral test of the surviving mass candidates against the chord graph X, using LMFDB Hilbert modular form data.
For B' ramified at the real places and D'', Eichler level N, maximal at v (norm 2): by Jacquet-Langlands the Brandt
operator T_v on the 12 classes has eigenvalues {3} and a_v(f), f running over newforms of level M with D''|M|D''N
(multiplicity = number of divisors of D''N/M). X = bipartite double, so we need {|a_v(f)|} = {1,1,1,r5,r5,r3,r3,c1,c1,c2,c2}."""
import json, time, urllib.request, itertools, mpmath as mp, sympy as sp, cypari2
mp.mp.dps=50; pari=cypari2.Pari(); pari.allocatemem(10**9)
import hashlib, os, subprocess
def api(table,q):
    url=f'https://www.lmfdb.org/api/{table}/?{q}&_format=json&_max_count=500'
    fn='cache/'+hashlib.md5(url.encode()).hexdigest()+'.json'
    if os.path.exists(fn): return json.load(open(fn))['data']
    for k in range(12):
        r=subprocess.run(['curl','-s',url],capture_output=True,timeout=90).stdout
        try:
            d=json.loads(r); open(fn,'w').write(json.dumps(d)); time.sleep(8); return d['data']
        except Exception: print('  waiting (rate limit)',flush=True); time.sleep(120)
    raise RuntimeError(url)
c1=2*mp.cos(mp.pi/12); c2=2*mp.cos(5*mp.pi/12)
TARGET=sorted([mp.mpf(1)]*3+[mp.sqrt(5)]*2+[mp.sqrt(3)]*2+[c1]*2+[c2]*2)
CASES=[('3.3.733.1',[13],[]),('3.3.148.1',[25],[(5,1)]),('3.3.469.1',[4],[(7,1)]),('3.3.316.1',[37],[]),('4.4.2777.1',[],[(71,1)]),('4.4.2777.1',[],[(8,2)])]
x,e=sp.symbols('x e')
report=[]
for lab,Dn,Nn in CASES:
    F=api('hmf_fields',f'label={lab}')[0]
    co=api('nf_fields',f'label={lab}')[0]['coeffs']; nf=pari.nfinit(pari.Pol(list(reversed(co)),'y'))
    def I(s):
        N,a,al=s.strip('[]').split(',',2); return pari.idealadd(nf,int(a),pari(al.replace('w','y')))
    primesL=[I(s) for s in F['primes']]
    def prid(P):
        p=int(pari.idealnorm(nf,P)); p=int(sp.factorint(p).popitem()[0])
        for q in pari.idealprimedec(nf,p):
            if pari.idealhnf(nf,q)==pari.idealhnf(nf,P): return q
        raise ValueError
    pridL={}
    nrm=lambda P: int(pari.idealnorm(nf,P))
    v_idx=[i for i,P in enumerate(primesL) if nrm(P)==2]
    def primes_of_norm(q): return [i for i,P in enumerate(primesL) if nrm(P)==q]
    choices=[]
    for Dc in itertools.product(*[primes_of_norm(q) for q in Dn]):
        for Nc in itertools.product(*[primes_of_norm(q) for q,_ in Nn]):
            if len(set(Dc+Nc))<len(Dc+Nc): continue
            for vi in v_idx:
                if vi in Dc+Nc: continue
                choices.append((Dc,Nc,vi))
    # torsion test (maximal orders of F(i), F(sqrt-3) embed => torsion)
    def st(Pi,a):
        R=pari(f'rnfinit(nfinit({pari.Pol(list(reversed(co)),"y")}),x^2+{a})'); pridL.setdefault(Pi,prid(primesL[Pi])); D=pari.rnfidealprimedec(R,pridL[Pi])
        return 1 if len(D)==2 else (0 if int(D[0][2])//int(pridL[Pi][2])==2 else -1)
    out=dict(field=lab,Dnorms=Dn,Nnorms=Nn,results=[])
    hecke={}
    for Dc,Nc,vi in choices:
        tors=False
        for a in (1,3):
            ok=all(st(j,a)!=1 for j in Dc) and all(st(j,a)!=-1 and Nn[k][1]==1 for k,j in enumerate(Nc))
            if ok: tors=True
        rec=dict(Dpp=[F['primes'][j] for j in Dc],N=[(F['primes'][j],Nn[k][1]) for k,j in enumerate(Nc)],v=F['primes'][vi],torsion=tors)
        if tors: out['results'].append(rec); continue
        Dideal=pari.idealhnf(nf,1)
        for j in Dc: Dideal=pari.idealmul(nf,Dideal,primesL[j])
        Nideal=pari.idealhnf(nf,1)
        for k,j in enumerate(Nc): Nideal=pari.idealmul(nf,Nideal,pari.idealpow(nf,primesL[j],Nn[k][1]))
        DN=pari.idealmul(nf,Dideal,Nideal); nDN=nrm(DN)
        vals=[]; dim=0; used=[]
        for Ln in sp.divisors(nDN):
            if Ln % (nrm(Dideal))!=0: continue
            for f in api('hmf_forms',f'field_label={lab}&level_norm=i{Ln}'):
                M=I(f['level_ideal'])
                # D'' | M | DN
                if pari.idealdiv(nf,DN,M,1) is None: pass
                q1=pari.idealadd(nf,M,Dideal); 
                if not (pari.idealhnf(nf,Dideal)==pari.idealhnf(nf,pari.idealadd(nf,Dideal,M)) and True): pass
                divides=lambda A,B: pari.idealhnf(nf,pari.idealadd(nf,A,B))==pari.idealhnf(nf,A)   # B subset A  <=> A | B
                if not (divides(Dideal,M) and divides(M,DN)): continue
                Q=pari.idealdiv(nf,DN,M); mult=int(pari.idealnumdiv(nf,Q)) if hasattr(pari,'idealnumdiv') else None
                if mult is None:
                    fa=pari.idealfactor(nf,Q); mult=1
                    for t in range(len(fa[0])): mult*=int(fa[1][t])+1
                lb=f['label']
                if lb not in hecke: hecke[lb]=api('hmf_hecke',f'label={lb}')[0]
                h=hecke[lb]; pp=sp.Poly(sp.sympify(h['hecke_polynomial'].replace('^','**')),x)
                rts=pp.nroots(n=50) if pp.degree()>1 else [sp.solve(pp.as_expr(),x)[0]]
                ev=sp.sympify(str(h['hecke_eigenvalues'][vi]).replace('^','**'))
                for r in rts: vals+=[abs(sp.N(ev.subs(e,r),50))]*mult
                dim+=f['dimension']*mult; used.append((lb,f['dimension'],mult,str(h['hecke_eigenvalues'][vi]),h['hecke_polynomial']))
        vals=sorted(vals)
        rec.update(dim=dim,forms=used,abs_av=[float(t) for t in vals],
                   match=(dim==11 and all(abs(a-b)<1e-30 for a,b in zip(vals,TARGET))))
        out['results'].append(rec)
    print(json.dumps(out)[:2500],flush=True); report.append(out)
json.dump(report,open('hmf_check.json','w'),indent=1)
print('ANY MATCH:',any(r.get('match') for o in report for r in o['results']))
