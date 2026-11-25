from core import *
import json
mp.mp.dps=50
R={}
# explicit formula for note Tonnetz
lam=[mp.mpf(sum(mp.cos(2*mp.pi*k*s/12) for s in (3,-3,4,-4,5,-5))) for k in range(12)]
def Nf(m):
    s=mp.mpf(0)
    for l in lam:
        d=mp.sqrt(mp.mpc(l*l-20)); s+=((l+d)/2)**m+((l-d)/2)**m
    return mp.re(s)+24*(1+(-1)**m)
Nm=traces(cayley_hashimoto(12,[3,-3,4,-4,5,-5]),20)
print('explicit formula ok', all(abs(Nf(m)-Nm[m])<1e-20 for m in range(1,21)))
th=sorted(set(round(float(mp.degrees(mp.acos(l/(2*mp.sqrt(5))))),3) for l in lam[1:]))
print('note-Tonnetz zero angles',th)
# (d) exact zeta correspondence chord vs note
def chi(x): return mp.fprod([x-l for l in lam])
def zc_inv(u): # chord dual Tonnetz, 3-regular, |E|-|V|=12, eig ±|f_k|, |f|^2=lam+3
    return (1-u**2)**12*mp.fprod([(1+2*u**2)**2-u**2*(l+3) for l in lam])
def zn_inv(v): return (1-v**2)**24*mp.fprod([1-v*l+5*v**2 for l in lam])
u=mp.mpf('0.21'); x=(1+u**2+4*u**4)/u**2
ok1=abs(zc_inv(u)/((1-u**2)**12*u**24*chi(x))-1)<1e-30
v=mp.findroot(lambda v:(1+5*v**2)/v-x,0.1)
ok2=abs(zn_inv(v)/((1-v**2)**24*v**12*chi(x))-1)<1e-30
print('zeta correspondence: Z_chord^-1(u)/((1-u^2)^12 u^24) = Z_note^-1(v)/((1-v^2)^24 v^12) when (1+5v^2)/v=(1+u^2+4u^4)/u^2:',ok1 and ok2)
# major-triad two-step graph == note Tonnetz
def P(c): r,q=c; return (r,'m' if q=='M' else 'M')
def Rr(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def L(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
two=set()
for f in (P,L,Rr):
    for g in (P,L,Rr):
        if f is g: continue
        two.add((g(f((0,'M')))[0])%12)
print('two-step neighbours of C major (roots):',sorted(two),'== {3,4,5,7,8,9}')
# (b) stepwise census
cen={}
for N in range(5,61):
    for nm,S in (('steps ±1,±2',[1,-1,2,-2]),('steps ±1,±2,±3',[1,-1,2,-2,3,-3])):
        if len(set(s%N for s in S))<len(S): continue
        l,b=ramanujan(N,S); cen.setdefault(nm,[]).append((N,l<=b+1e-12))
for nm,v in cen.items():
    print(nm,'RH-pass N:',[N for N,ok in v if ok],' largest:',max(N for N,ok in v if ok))
# note-Tonnetz census across EDOs: best major triad, and any shape
def best(N,r): return round(N*math.log2(r))
passN=[];anyN=[]
for N in range(7,101):
    a,b=best(N,5/4),best(N,3/2); S=[a,-a,b-a,-(b-a),b,-b]
    if len(set(s%N for s in S))==6:
        l,bd=ramanujan(N,S)
        if l<=bd+1e-12: passN.append(N)
    found=False
    for a in range(1,N):
        for b in range(a+1,N):
            S=[a,-a,b,-b,b-a,-(b-a)]
            if len(set(s%N for s in S))!=6 or math.gcd(math.gcd(a,b),N)!=1: continue
            l,bd=ramanujan(N,S)
            if l<=bd+1e-12: found=True; break
        if found: break
    if found: anyN.append(N)
print('note Tonnetz (best major triad) RH-pass N:',passN)
print('note Tonnetz any connected 3-interval shape passes, N:',anyN[-8:],'largest',max(anyN))
# diatonic & pentatonic step graphs
for nm,N,S in (('diatonic Z7 seconds+thirds',7,[1,-1,2,-2]),('pentatonic Z5 ±1,±2 (=K5)',5,[1,-1,2,-2]),('chromatic Z12 ±1,±2',12,[1,-1,2,-2]),('chromatic Z12 ±1',12,[1,-1])):
    l,b=ramanujan(N,S); print(nm,'lam2=%.4f bound=%.4f'%(l,b), 'PASS' if l<=b+1e-12 else 'FAIL')
B=cayley_hashimoto(7,[1,-1,2,-2]); Nd=traces(B,14); print('diatonic seconds/thirds primes',{m:v for m,v in primes_from_N(Nd).items() if v})
B=cayley_hashimoto(12,[1,-1,2,-2]); Nd=traces(B,16); print('chromatic ±1,±2 primes',{m:v for m,v in primes_from_N(Nd).items() if v})
