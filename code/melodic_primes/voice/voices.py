import itertools, collections, json, sys
NM=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
def tri(c):
    r,q=c; return {r%12,(r+(4 if q=='M' else 3))%12,(r+7)%12}
def P(c): r,q=c; return (r,'m' if q=='M' else 'M')
def R(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def L(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
OPS={'P':P,'L':L,'R':R}
def cname(c): return NM[c[0]]+('' if c[1]=='M' else 'm')
def step(c,op):
    d=OPS[op](c); a=tri(c); b=tri(d)
    out=(a-b).pop(); inn=(b-a).pop(); s=(inn-out)%12
    s = s if s<=6 else s-12
    assert abs(s) in (1,2)
    return d,out,inn,s
def walk(c0,w):
    r,q=c0
    voices=[r, r+(4 if q=='M' else 3), r+7]   # lifted pitches (root,third,fifth)
    start=list(voices); c=c0; steps=[]; arr=[]; mover=[]
    for op in w:
        c,out,inn,s=step(c,op)
        i=[j for j in range(3) if voices[j]%12==out]; assert len(i)==1; i=i[0]
        voices[i]+=s; steps.append(s); arr.append(inn); mover.append(i)
    return c,start,voices,steps,arr,mover
def perm(start,end):
    # sigma[i]=j : voice i ends on the pitch class voice j started on
    return tuple([ [j for j in range(3) if (start[j]-e)%12==0][0] for e in end])
def ptype(s):
    fixed=sum(1 for i in range(3) if s[i]==i)
    return {3:'id',0:'3-cycle',1:'swap'}[fixed]
def minper(seq):
    m=len(seq)
    for d in range(1,m+1):
        if m%d==0 and all(seq[i]==seq[(i+d)%m] for i in range(m)): return d
def canon(seq):
    m=len(seq); return min(tuple(seq[i:]+seq[:i]) for i in range(m))
def closed_words(m):
    for w in itertools.product('PLR',repeat=m):
        if any(w[i]==w[(i+1)%m] for i in range(m)): continue
        yield ''.join(w)
