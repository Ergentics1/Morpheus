from core import *
N=12; S=[3,-3,4,-4,7,-7]
B=cayley_hashimoto(N,S); Nm=traces(B,30); pi=primes_from_N(Nm)
print('N_m',{m:Nm[m] for m in range(1,9)})
print('pi',{m:pi[m] for m in range(1,13)})
lam=[eig(N,S,k) for k in range(12)]
f2=[abs(sum(complex(math.cos(2*math.pi*k*x/12),math.sin(2*math.pi*k*x/12)) for x in (0,4,7)))**2 for k in range(12)]
print('lam',np.round(lam,4)); print('lam = |f|^2-3 ?',np.allclose(lam,np.array(f2)-3))
print('max nontriv',max(abs(l) for l in lam[1:]),'bound',2*math.sqrt(5))
for m in (10,20,30): print(m,pi[m],'ratio to 5^m/m',pi[m]/(5**m/m))
