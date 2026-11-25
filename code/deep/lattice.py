# lattice lift of the 24 triads; per-edge torus voltages (du,dv)
from common import *
src=open('../winding.py').read().split('res={}')[0]; g={}; exec(src,g)
flip,trans,wind,pcl=g['flip'],g['trans'],g['wind'],g['pc']
def lat(c):
    r,q=c; p=((7*r)%12,0)
    return frozenset({p,(p[0]+1,p[1]),(p[0],p[1]+1)}) if q=='M' else frozenset({p,(p[0]+1,p[1]),(p[0]+1,p[1]-1)})
LAT={v:lat(v) for v in V}
VOLT=[]
for a,b,o,s in EDGES:
    t=flip(LAT[V[a]],o); VOLT.append(wind(trans(LAT[V[b]],t)))
