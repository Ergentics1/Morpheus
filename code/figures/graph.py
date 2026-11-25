"""Chord graph data for the visuals: triads, moves, levels of the Z/12 garage, layouts, the Bruhat-Tits tree."""
import numpy as np, math, json, sys
NAMES=['C','D♭','D','E♭','E','F','F♯','G','A♭','A','B♭','B']
V=[(r,q) for r in range(12) for q in 'Mm']
def P(c): r,q=c; return (r,'m' if q=='M' else 'M')
def R(c): r,q=c; return ((r+9)%12,'m') if q=='M' else ((r+3)%12,'M')
def L(c): r,q=c; return ((r+4)%12,'m') if q=='M' else ((r+8)%12,'M')
OPS={'P':P,'L':L,'R':R}
VOLT={'P':4,'L':0,'R':1}
COL={'P':'#ffc857','L':'#2ec4b6','R':'#ff5d8f'}
def name(c): return NAMES[c[0]]+('' if c[1]=='M' else 'm')
BYNAME={name(c):c for c in V}
def level(c):
    r,q=c
    return (5*r)%12 if q=='M' else (5*(r-4))%12
EDGES=[]
for c in V:
    if c[1]=='M':
        for s in 'PLR': EDGES.append((c,OPS[s](c),s))
def clock_pos(c,cx=960,cy=590,RM=380,Rm=250):
    j=level(c)
    if c[1]=='M': a=math.radians(90-30*j); r=RM
    else: a=math.radians(90-30*j-13); r=Rm
    return np.array([cx+r*math.cos(a),cy+r*math.sin(a)])
def garage_pos(c,tau,cx=960,cy=590,h=56,dx=170):
    j=level(c); x=cx-dx if c[1]=='M' else cx+dx
    return np.array([x,cy+(j-5.5)*h*tau])
def bez(p0,p1,ctrl,n=24):
    t=np.linspace(0,1,n)[:,None]; return (1-t)**2*p0+2*(1-t)*t*ctrl+t**2*p1
# Bruhat-Tits tree as reduced words in {P,L,R}
def tree(depth=6):
    words=[()]; fr=[()]
    for _ in range(depth):
        fr=[w+(s,) for w in fr for s in 'PLR' if not w or w[-1]!=s]; words+=fr
    return words
def act(c,w):
    for s in w: c=OPS[s](c)
    return c
def tree_pos(w,cx=960,cy=590,step=78):
    # radial layout: sector of a word
    if not w: return np.array([cx,cy])
    a0,a1=-90.0,270.0; lo,hi=a0,a1
    first='PLR'.index(w[0]); lo=a0+120*first; hi=lo+120
    for k in range(1,len(w)):
        opts=[s for s in 'PLR' if s!=w[k-1]]; i=opts.index(w[k]); mid=(lo+hi)/2
        lo,hi=(lo,mid) if i==0 else (mid,hi)
    a=math.radians((lo+hi)/2); r=step*len(w)**0.92
    return np.array([cx+r*math.cos(a),cy+r*math.sin(a)])
def fk(k): w=np.exp(2j*np.pi/12); return sum(w**(k*e) for e in VOLT.values())
def wilson(seed):
    rng=np.random.default_rng(seed); nb={c:[OPS[s](c) for s in 'PLR'] for c in V}
    intree={V[0]}; parent={}
    for v in V:
        u=v; nxt={}
        while u not in intree: nxt[u]=nb[u][rng.integers(3)]; u=nxt[u]
        u=v
        while u not in intree: parent[u]=nxt[u]; intree.add(u); u=nxt[u]
    return [(a,b) for a,b in parent.items()]
