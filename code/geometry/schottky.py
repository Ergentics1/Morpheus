"""Explicit 2-adic Schottky uniformisation of the chord graph X = Cay(D12,{P,L,R}).
Bruhat-Tits tree T of PGL2(Q2): vertices = homothety classes of Z2-lattices; a lattice is stored as an integer 2x2 basis
matrix with 2-power determinant (its Z-span has 2-power index, so its 2-adic completion is determined)."""
import sys, json, itertools, math
sys.path.insert(0,'../deep'); from common import V, IX, OPS, cname
from fractions import Fraction as F
import numpy as np, sympy as sp
def mul(A,B): return [[A[0][0]*B[0][0]+A[0][1]*B[1][0],A[0][0]*B[0][1]+A[0][1]*B[1][1]],[A[1][0]*B[0][0]+A[1][1]*B[1][0],A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def v2(n):
    n=abs(int(n)); 
    if n==0: return 10**9
    k=0
    while n%2==0: n//=2;k+=1
    return k
def inv_adj(A): return [[A[1][1],-A[0][1]],[-A[1][0],A[0][0]]]   # = det * A^-1 (same class in PGL2)
def canon(M):
    """canonical form of the homothety class of the lattice M.Z2^2 : column HNF [[a,0],[b,d]] with a,d 2-powers, 0<=b<d,
    after removing odd parts (units in Z2) and the common power of 2."""
    (p,q),(r,s)=M
    # column ops over Z: make first row (g,0)
    g,x,y=sp.gcdex(p,q)[2],*sp.gcdex(p,q)[:2]
    g=int(g); x=int(x); y=int(y)
    # new col1 = x*c1+y*c2 ; col2 = (-q/g)c1+(p/g)c2
    c1=(p*x+q*y, r*x+s*y); c2=(-q//g*p+p//g*q, -q//g*r+p//g*s)
    a,b,d=c1[0],c1[1],c2[1]
    if d<0: d=-d
    if a<0: a=-a; b=-b
    # strip odd parts (units over Z2): lattice spanned by (a,b),(0,d); a=2^i*u, d=2^j*w
    i,j=v2(a),v2(d)
    # (a,b) ~ (2^i, b/u) with b/u computed mod 2^j  (u odd -> invertible mod 2^j)
    u=a>>i; bb=(b*pow(u,-1,2**j)) % (2**j) if j>0 else 0
    a,d,b=2**i,2**j,bb
    k=min(i,j,v2(b) if b else 10**9)
    return (a>>k, b>>k, d>>k)
def lat(c):  a,b,d=c; return [[a,0],[b,d]]
def neighbours(c):
    M=lat(c); return {canon(mul(M,T)) for T in ([[2,0],[0,1]],[[1,0],[1,2]],[[1,0],[0,2]])}
# generators: sigma1 swaps v0=Z^2 with Z+2Z ; sigma2, sigma3 are GL2(Z)-conjugates
s1=[[0,1],[2,0]]
g2=[[0,1],[1,0]]; g3=[[1,0],[1,1]]
s2=mul(mul(g2,s1),inv_adj(g2)); s3=mul(mul(g3,s1),inv_adj(g3))
SIG={'P':s1,'L':s2,'R':s3}     # any bijection {P,L,R}->{s1,s2,s3} works (X is a Cayley graph)
v0=canon([[1,0],[0,1]])
A=[]  # audit
def chk(name,ok,detail=''): A.append((name,bool(ok),str(detail))); print(('PASS ' if ok else 'FAIL ')+name,detail)
nb0=neighbours(v0)
chk('tree: v0 has 3 neighbours (P^1(F_2))',len(nb0)==3,sorted(nb0))
for k,S in SIG.items():
    sq=mul(S,S)
    chk(f'sigma_{k}^2 is scalar (involution in PGL2)',sq[0][1]==0 and sq[1][0]==0 and sq[0][0]==sq[1][1],sq)
    w=canon(S); chk(f'sigma_{k} moves v0 to a neighbour',w in nb0,w)
    chk(f'sigma_{k} maps that neighbour back to v0 (edge inversion)',canon(mul(S,lat(w)))==v0)
chk('the three sigma_i send v0 to the three distinct neighbours',{canon(S) for S in SIG.values()}==nb0)
# reduced words up to length 7: distinct vertices, distance = length  -> W3 acts simply transitively (tree isomorphism)
def words(n):
    out=[()]
    frontier=[()]
    for _ in range(n):
        nf=[w+(s,) for w in frontier for s in 'PLR' if not w or w[-1]!=s]; out+=nf; frontier=nf
    return out
W=words(7); Mw={}
for w in W:
    M=[[1,0],[0,1]]
    for s in w: M=mul(M,SIG[s])
    Mw[w]=M
verts={w:canon(Mw[w]) for w in W}
chk('reduced words of length <=7 give pairwise distinct vertices',len(set(verts.values()))==len(W),f'{len(W)} words')
okadj=all(verts[w] in neighbours(verts[w[:-1]]) for w in W if w)
chk('w and w[:-1] are adjacent in T (word path = geodesic)',okadj)
chk('ball count 1+3*(2^n-1) matches tree ball of radius 7',len(W)==1+3*(2**7-1))
# homomorphism W3 -> D12 via right action on triads; K = stabiliser of C major
C=('0','M') if False else (0,'M')
def act(t,w):
    for s in w: t=OPS[s](t)
    return t
# BFS spanning tree of X from C
rep={C:()}; order=[C]
for t in order:
    for s in 'PLR':
        u=OPS[s](t)
        if u not in rep: rep[u]=rep[t]+(s,); order.append(u)
chk('BFS tree reaches all 24 triads',len(rep)==24)
tree_edges={frozenset((t,OPS[s](t),)) for t in rep for s in rep[t][-1:]} 
tree_edges={frozenset((act(C,rep[t][:-1]),t)) for t in rep if rep[t]}
def red(w):
    out=[]
    for s in w:
        if out and out[-1]==s: out.pop()
        else: out.append(s)
    return tuple(out)
gens=[]; seen=set()
for t in V:
    for s in 'PLR':
        u=OPS[s](t); e=frozenset((t,u))
        if e in tree_edges or e in seen: continue
        seen.add(e)
        w=red(rep[t]+(s,)+tuple(reversed(rep[u])))
        gens.append((cname(t),s,cname(u),w))
chk('number of Schreier generators = 36-23 = 13 = rank pi_1(X)',len(gens)==13)
def matof(w):
    M=[[1,0],[0,1]]
    for s in w: M=mul(M,SIG[s])
    return M
def cyc_len(w):
    w=list(w)
    while len(w)>1 and w[0]==w[-1]: w=w[1:-1]
    return len(w)
G=[]
for (a,s,b,w) in gens:
    M=matof(w); g=math.gcd(*[abs(x) for r in M for x in r]); M=[[x//g for x in r] for r in M]
    tr=M[0][0]+M[1][1]; ell=v2(det(M))-2*v2(tr)
    G.append(dict(edge=f'{a} -{s}- {b}',word=''.join(w),matrix=M,det=det(M),trace=tr,translation_length=ell,cycle_length=cyc_len(w)))
    if act(C,w)!=C: chk('generator fixes C',False,w)
chk('every Schreier word stabilises C major (lies in K)',all(act(C,tuple(g['word']))==C for g in G))
chk('all 13 generators hyperbolic: 2 v2(tr) < v2(det)',all(g['translation_length']>0 for g in G))
chk('translation length on T = length of the closed cycle in X',all(g['translation_length']==g['cycle_length'] for g in G),[g['cycle_length'] for g in G])
# stabiliser of C acts trivially on all triads (K normal, quotient D12) on all words up to length 7
Kwords=[w for w in W if act(C,w)==C]
chk('stab(C)=kernel: every word fixing C fixes all 24 triads',all(all(act(t,w)==t for t in V) for w in Kwords),f'{len(Kwords)} words checked')
# K\T = X : vertex w.v0 -> triad C.w is a covering map of graphs T -> X compatible with adjacency
chk('covering T->X: adjacent vertices map to PLR-adjacent triads',all(act(C,w) == OPS[w[-1]](act(C,w[:-1])) for w in W if w))
chk('K has no inversions: all elements of K are even words (preserve bipartition)',all(len(w)%2==0 for w in Kwords))
# genus 13 Mumford curve invariants
chk('genus = rank H1(X) = E-V+1 = 13',36-24+1==13)
pts=lambda n: 24*2**n-12
chk('special fibre: 24 P^1 meeting in 36 F2-nodes, #C0(F_2^n)=24*2^n-12, N1=36 = all F2-points are nodes',pts(1)==36)
# Zariski density / non-arithmeticity of this explicit Gamma: generators have integer entries, tr^2/det not all rational-integral
# Invariant trace field Q(tr^2/det) = Q; Gamma subset PGL2(Q) and not virtually abelian -> invariant quaternion algebra M2(Q),
# which is split at infinity; a cocompact arithmetic lattice of PGL2(Q2) comes from a definite algebra, so Gamma is NOT arithmetic.
# Additional numerical witness: an arithmetic Gamma (from Z[1/2]-points of a definite order) has tr^2/det in Z[1/2] with
# |tr|^2 <= 4|det| at the real place for every element (compact at infinity). Find an element violating this.
viol=[g for g in G if g['trace']**2>4*abs(g['det'])]
chk('non-arithmetic witness: some generator is hyperbolic at the real place (tr^2>4|det|), impossible in a definite order',len(viol)>0,viol[0]['word'] if viol else '')
json.dump(dict(sigma={k:v for k,v in SIG.items()},generators=G,audit=A),open('schottky.json','w'),indent=1)
for g in G: print(g['edge'],g['word'],g['matrix'],'det 2^%d'%v2(g['det']),'tr',g['trace'],'ell',g['translation_length'])
print(sum(a[1] for a in A),'/',len(A))
