import numpy as np, itertools, json, sympy, cmath, math
exec(open('primes.py').read().split("print('N_m'")[0])
# adjacency eigenvalues vs |f_k|
ev=np.sort(np.linalg.eigvalsh(A.astype(float)))
f=lambda X,k,N=12: abs(sum(cmath.exp(2j*math.pi*k*x/N) for x in X))
fk=[f((0,4,7),k) for k in range(12)]
print('fk',np.round(fk,4))
print('eig match', np.allclose(np.sort(fk+[-x for x in fk]),ev))
th=[math.acos(fk[k]/(2*math.sqrt(2))) for k in range(1,12)]
print('theta deg',np.round(np.degrees(th),3))
def Nform(m):
    return 2**m+(-2)**m+1+(-1)**m+12*(1+(-1)**m)+sum((1+(-1)**m)*2*2**(m/2)*math.cos(m*t) for t in th)
print('explicit formula check',[ (m,Nm[m],round(Nform(m))) for m in range(2,31,2)])
pi={m: sum(sympy.mobius(m//d)*Nm[d] for d in sympy.divisors(m))//m for m in Nm}
for m in range(6,61,2):
    main=2**(m+1)/m
    print(m,pi[m], round(pi[m]/main,6), 'err/(2^(m/2)/m)=',round((pi[m]-main)/(2**(m/2)/m),3))
