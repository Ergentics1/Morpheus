import json, math, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','font.size':10,'mathtext.fontset':'cm'})
PC=json.load(open('../prime_counts.json')); TR=json.load(open('../melodic_primes/voice/transfer.json'))
# Fig 1: prime counts and poles
fig,ax=plt.subplots(1,2,figsize=(7.2,2.9))
ms=[m for m in range(6,41,2)]; pi=[int(PC['pi'][str(m)]) for m in ms]
ax[0].semilogy(ms,pi,'o',ms=3.5,label=r'$\pi(m)$ exact'); ax[0].semilogy(ms,[2**(m+1)/m for m in ms],'-',lw=1,label=r'$2^{m+1}/m$')
ax[0].set_xlabel('length $m$'); ax[0].legend(frameon=False); ax[0].set_title('Prime cadences')
ev=[3,-3]+[1]*3+[-1]*3+[math.sqrt(5)]*2+[-math.sqrt(5)]*2+[math.sqrt(3)]*2+[-math.sqrt(3)]*2+[s*2*math.cos(a) for s in (1,-1) for a in (math.pi/12,5*math.pi/12) for _ in range(2)]
P=[]
for l in ev:
    d=np.sqrt(complex(l*l-8)); P+= [(l+d)/4,(l-d)/4]
P=np.array(P); t=np.linspace(0,2*np.pi,400)
ax[1].plot(np.cos(t)/math.sqrt(2),np.sin(t)/math.sqrt(2),'k-',lw=0.6); ax[1].plot(P.real,P.imag,'o',ms=4,mfc='none')
ax[1].plot([1,-1,0.5,-0.5],[0,0,0,0],'x',ms=5,color='C3')
ax[1].set_aspect('equal'); ax[1].set_title(r'poles of $\zeta_X(u)$; circle $|u|=2^{-1/2}$'); ax[1].set_xlim(-1.1,1.1); ax[1].set_ylim(-0.85,0.85)
fig.tight_layout(); fig.savefig('../../paper/figures/counts_poles.pdf')
# Fig 2: W distribution m=40 vs Gaussian
r=TR['40']; W=sorted(int(k) for k in r['W']); tot=r['pi']
fig,ax=plt.subplots(figsize=(3.6,2.8))
ax.bar(W,[r['W'][str(w)]/tot for w in W],color='0.7',label='exact, $m=40$')
xs=np.linspace(-4,4,200); s2=40/24
ax.plot(xs,np.exp(-xs**2/(2*s2))/np.sqrt(2*np.pi*s2),'k-',lw=1,label=r'$\mathcal{N}(0,m/24)$')
ax.set_xlabel(r'voice winding $W$'); ax.legend(frameon=False,fontsize=8); fig.tight_layout(); fig.savefig('../../paper/figures/winding.pdf')
# Fig 3: Riemann window
phi=np.linspace(0,2*np.pi,1000)
k=np.arange(12)[:,None]; w=lambda x: np.exp(2j*np.pi*x/12)
lam=np.abs(1+w(4*k)+np.exp(1j*phi/4)[None,:]*w(9*k)).max(0)
fig,ax=plt.subplots(figsize=(3.6,2.8))
ax.plot(phi,lam,'k-',lw=1); ax.axhline(2*math.sqrt(2),color='C3',lw=0.8,ls='--'); 
a=4*math.acos(0.75); ax.axvspan(a,2*np.pi-a,color='C0',alpha=0.2)
ax.set_xlabel(r'flux $\varphi$'); ax.set_ylabel(r'$\max_k|\lambda_k(\varphi)|$'); ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi]); ax.set_xticklabels(['0',r'$\pi/2$',r'$\pi$',r'$3\pi/2$',r'$2\pi$'])
ax.text(np.pi,2.86,r'$2\sqrt{2}$',ha='center',fontsize=8,color='C3'); fig.tight_layout(); fig.savefig('../../paper/figures/window.pdf')
# Fig 4: Fourier coefficients in C
fk=[sum(np.exp(2j*np.pi*kk*x/12) for x in (0,4,7)) for kk in range(12)]
fig,ax=plt.subplots(figsize=(3.6,3.2))
t=np.linspace(0,2*np.pi,300)
for rr in (1,math.sqrt(3),math.sqrt(5),3): ax.plot(rr*np.cos(t),rr*np.sin(t),color='0.85',lw=0.6)
for kk in (0,1,2,3,4,5,7,8,9,11):
    z=fk[kk]
    c='C3' if kk in (1,5,7,11) else ('C0' if kk in (3,9) else ('C2' if kk in (4,8) else 'k'))
    ax.plot(z.real,z.imag,'o',color=c,ms=5)
    txt=r'$f_2, f_6, f_{10}$' if kk==2 else f'$f_{{{kk}}}$'
    off=(-4,6) if kk==0 else (4,4)
    ax.annotate(txt,(z.real,z.imag),xytext=off,textcoords='offset points',fontsize=7,ha='center' if kk==0 else 'left')
ax.set_aspect('equal'); ax.set_title('triad Fourier coefficients in $\\mathbb{Z}[\\zeta_{12}]$',fontsize=9)
fig.tight_layout(); fig.savefig('../../paper/figures/fourier.pdf')
# Fig 5: honeycomb schematic with hexagon prime and its two moving voices
fig,ax=plt.subplots(figsize=(3.6,3.0))
import itertools
NM=['C','D$\\flat$','D','E$\\flat$','E','F','F$\\sharp$','G','A$\\flat$','A','B$\\flat$','B']
pos=lambda a,b: (a+0.5*b, b*math.sqrt(3)/2)
for a in range(-2,3):
    for b in range(-2,3):
        x,y=pos(a,b)
        for da,db in ((1,0),(0,1),(-1,1)):
            x2,y2=pos(a+da,b+db); ax.plot([x,x2],[y,y2],color='0.8',lw=0.6,zorder=1)
        ax.text(x,y,NM[(7*a+4*b)%12],ha='center',va='center',fontsize=7,bbox=dict(boxstyle='circle,pad=0.15',fc='w',ec='0.5',lw=0.5),zorder=3)
# hexagon around C (0,0): triads containing C
tris=[((0,0),(1,0),(0,1)),((0,0),(1,0),(1,-1)),((0,0),(1,-1),(0,-1)),((0,0),(0,-1),(-1,0)),((0,0),(-1,0),(-1,1)),((0,0),(-1,1),(0,1))]
cent=[np.mean([pos(*v) for v in t],axis=0) for t in tris]
cyc=cent+[cent[0]]
ax.plot([c[0] for c in cyc],[c[1] for c in cyc],'-',color='C3',lw=1.6,zorder=2)
for c in cent: ax.plot(*c,'o',color='C3',ms=3,zorder=2)
ax.set_aspect('equal'); ax.axis('off'); ax.set_title('pedal hexagon C–Cm–A$\\flat$–Fm–F–Am around C',fontsize=8)
fig.tight_layout(); fig.savefig('../../paper/figures/hexagon.pdf')
print('ok')
