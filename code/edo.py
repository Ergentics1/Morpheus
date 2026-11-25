import math, numpy as np, cmath
from general import tonnetz
def best(N,r): return round(N*math.log2(r))
out=[]
for N in range(12,80):
    X=(0,best(N,5/4),best(N,3/2))
    if len(set(X))<3: continue
    V,A=tonnetz(X,N)
    ev=np.linalg.eigvalsh(A.astype(float)); d=A.sum(1).max()
    nt=[abs(e) for e in ev if abs(abs(e)-d)>1e-9]; lam=max(nt)
    mu=(lam+math.sqrt(max(lam*lam-8,0)))/2 if lam>2*math.sqrt(2) else math.sqrt(2)
    out.append((N,X,len(V),round(lam,4),round(math.log(mu)/math.log(2),4)))
for o in out: print(o)
