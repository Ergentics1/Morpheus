import sys, math, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import graph as Gr
plt.rcParams.update({'font.family':'serif','font.size':9,'mathtext.fontset':'cm'})
STY={'P':dict(color='#b8860b',ls='-',lw=1.3),'L':dict(color='#1f7a72',ls='--',lw=1.1),'R':dict(color='#b0305a',ls=':',lw=1.4)}
def nm(c): return Gr.name(c).replace('♭',r'$\flat$').replace('♯',r'$\sharp$')
# Fig: reduction graph of C (clock layout = circle of fifths levels)
fig,ax=plt.subplots(figsize=(4.2,4.2))
pos=lambda c: Gr.clock_pos(c,cx=0,cy=0,RM=1.0,Rm=0.66)
for u,v,s in Gr.EDGES:
    p,q=pos(u),pos(v); ax.plot([p[0],q[0]],[p[1],q[1]],**STY[s],zorder=1)
for c in Gr.V:
    p=pos(c); ax.add_patch(plt.Circle(p,0.075,fc='white' if c[1]=='M' else '0.85',ec='k',lw=0.6,zorder=2)); ax.text(p[0],p[1],nm(c),ha='center',va='center',fontsize=5.5,zorder=3)
for s in 'PLR': ax.plot([],[],**STY[s],label=s)
ax.legend(loc='lower right',frameon=False,fontsize=7); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.15,1.15); ax.set_ylim(-1.15,1.15)
fig.tight_layout(); fig.savefig('../../paper/figures/reduction_graph.pdf')
# Fig: special fibre of H (two lines) and theta graph
fig,ax=plt.subplots(1,2,figsize=(6.4,2.0),gridspec_kw=dict(width_ratios=[1.6,1]))
xs=np.linspace(-1,1,300); y=0.35*np.sin(xs*np.pi*1.5)
ax[0].plot(xs,y,'k-',lw=1.6); ax[0].plot(xs,-y,'-',color='0.55',lw=1.6)
for k,(s,x) in enumerate(zip('PLR',(-2/3,0,2/3))):
    ax[0].plot(x,0,'o',ms=5,color=STY[s]['color']); ax[0].text(x,-0.17,s,ha='center',va='top',fontsize=9,color=STY[s]['color'])
ax[0].text(-1.05,0.25,'major',ha='right',fontsize=8); ax[0].text(-1.05,-0.25,'minor',ha='right',fontsize=8,color='0.4')
ax[0].set_xlim(-1.5,1.1); ax[0].set_ylim(-0.6,0.6); ax[0].axis('off'); ax[0].set_title(r'special fibre of $H$: $\mathbb{P}^1\cup\mathbb{P}^1$ glued at $\mathbb{P}^1(\mathbb{F}_2)$',fontsize=8)
pM,pm=np.array([0,0.6]),np.array([0,-0.6])
for s,off in (('L',0),('R',0.45),('P',-0.45)):
    t=np.linspace(0,1,40)[:,None]; c=(1-t)**2*pM+2*(1-t)*t*(np.array([off*1.6,0]))+t**2*pm; ax[1].plot(c[:,0],c[:,1],**STY[s]); ax[1].text(off*0.85+0.05,0,s,fontsize=8,color=STY[s]['color'])
for p,n in ((pM,'major'),(pm,'minor')): ax[1].plot(*p,'o',ms=7,mfc='white',mec='k'); ax[1].text(p[0]+0.12,p[1],n,fontsize=8,va='center')
ax[1].set_xlim(-0.9,1.1); ax[1].set_ylim(-0.85,0.85); ax[1].axis('off'); ax[1].set_title(r'dual graph $\Theta$',fontsize=8)
fig.tight_layout(); fig.savefig('../../paper/figures/two_lines.pdf')
# Fig: the Z/12 cover drawn as a 12-level garage
fig,ax=plt.subplots(figsize=(4.0,4.6))
for u,v,s in Gr.EDGES:
    j,i=Gr.level(u),Gr.level(v); jj=i if i>=j else i+12
    ax.plot([0,1],[j,jj],**STY[s],alpha=1 if jj<12 else 0.35)
for c in Gr.V:
    x=0 if c[1]=='M' else 1; ax.plot(x,Gr.level(c),'o',ms=9,mfc='white' if c[1]=='M' else '0.85',mec='k',mew=0.6); ax.text(x,Gr.level(c),nm(c),ha='center',va='center',fontsize=5)
for j in range(12): ax.text(-0.18,j,str(j),ha='right',va='center',fontsize=6,color='0.4')
ax.axhline(11.6,color='0.6',lw=0.5,ls='-'); ax.text(1.12,12.6,'level 12 = level 0',fontsize=6.5,color='0.35',ha='left')
ax.text(-0.18,13.2,'level',fontsize=6.5,color='0.4',ha='right')
ax.set_xlim(-0.45,1.7); ax.set_ylim(-0.7,15.3); ax.axis('off')
ax.text(1.12,8,r'$L:\ +0$'+'\n'+r'$R:\ +1$'+'\n'+r'$P:\ +4$',fontsize=8,va='center')
fig.tight_layout(); fig.savefig('../../paper/figures/cover.pdf'); print('ok')
