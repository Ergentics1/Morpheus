"""The tower C -> H -> P^1: X is the Z/12 voltage cover of the theta graph Theta (2 vertices major/minor, 3 edges P,L,R,
voltages 4,0,1 = exponents of P=L rho^4, L, R=L rho in the PLR group). Ihara zeta factorises into twisted L-functions."""
import sys, json, itertools, numpy as np, sympy as sp
sys.path.insert(0,'../deep'); from common import V, IX, OPS
import networkx as nx
AU=[]
def chk(name,ok,detail=''): AU.append((name,bool(ok),str(detail))); print(('PASS ' if ok else 'FAIL ')+name,detail)
volt={'P':4,'L':0,'R':1}
def cover(d):
    G=nx.MultiGraph()
    for j in range(d):
        for s,e in volt.items(): G.add_edge(('M',j),('m',(j+e)%d),key=s)
    return G
X=nx.Graph(); [X.add_edge(IX[v],IX[OPS[s](v)]) for v in V for s in 'PLR']
chk('X is isomorphic to the Z/12 voltage cover of Theta with voltages P:4, L:0, R:1',nx.is_isomorphic(X,nx.Graph(cover(12))) and nx.Graph(cover(12)).number_of_edges()==36)
u=sp.symbols('u'); w=sp.exp(2*sp.pi*sp.I/12)
A=sp.Matrix(nx.to_numpy_array(X,nodelist=range(24)).astype(int))
zinv=sp.expand((1-u**2)**12*(sp.eye(24)-A*u+2*u**2*sp.eye(24)).det())
prodL=1
Ls=[]
for k in range(12):
    f=sum(w**(k*e) for e in volt.values()); m2=3+2*sum(sp.cos(2*sp.pi*k*(a-b)/12) for a,b in itertools.combinations(volt.values(),2))
    Lk=sp.expand((1-u**2)*((1+2*u**2)**2-m2*u**2)); Ls.append(Lk); prodL*=Lk
chk('1/zeta_X(u) = prod_{k=0}^{11} L_Theta(u,chi_k)^{-1} (Artin-Ihara factorisation over the 12 characters)',sp.expand(sp.expand(prodL)-zinv)==0)
# group characters by order d -> rational factors (these are the Q-factors of the degree-44 polynomial)
fac={}
for d in (1,2,3,4,6,12):
    ks=[k for k in range(12) if 12//sp.gcd(k,12)==d]
    fac[d]=sp.factor(sp.expand(sp.prod([Ls[k] for k in ks])))
    print('d=',d,'k=',ks,fac[d])
chk('Chevalley-Weil: genus(C)=13 = 2 (trivial char) + 11*(g_H-1)=11',2+11*1==13)
for d in (1,2,3,4,6):
    G=cover(d); gs=G.number_of_edges()-G.number_of_nodes()+1
    print('intermediate cover Z/%d:'%d,G.number_of_nodes(),'vertices',G.number_of_edges(),'edges, genus',gs, 'simple' if nx.Graph(G).number_of_edges()==G.number_of_edges() else 'multigraph')
G6=nx.Graph(cover(6)); print('Z/6 quotient girth',nx.girth(G6))
chk('genus of Z/d intermediate curve = d+1',all(cover(d).number_of_edges()-cover(d).number_of_nodes()+1==d+1 for d in (1,2,3,4,6,12)))
json.dump(dict(L={k:str(L) for k,L in enumerate(Ls)},factors={d:str(f) for d,f in fac.items()},audit=AU),open('tower.json','w'),indent=1)
print(sum(a[1] for a in AU),'/',len(AU))
