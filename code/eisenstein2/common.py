import itertools, collections, math
NM=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
V=[(r,q) for r in range(12) for q in 'Mm']; IX={v:i for i,v in enumerate(V)}
def tri(c): r,q=c; return frozenset({r%12,(r+(4 if q=='M' else 3))%12,(r+7)%12})
def P(c): r,q=c; return (r,'m' if q=='M' else 'M')
def R(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def L(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
OPS={'P':P,'L':L,'R':R}
def cname(c): return NM[c[0]]+('' if c[1]=='M' else 'm')
def move(c,op):
    d=OPS[op](c); a,b=tri(c),tri(d); out=next(iter(a-b)); inn=next(iter(b-a))
    s=(inn-out)%12; s=s if s<=6 else s-12
    return d,out,inn,s
EDGES=[(IX[v],IX[OPS[o](v)],o,move(v,o)[3]) for v in V for o in 'PLR']   # 72 directed edges
