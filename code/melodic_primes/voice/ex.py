from voices import *
import sympy, json, math
def show(c0,w):
    c,start,end,steps,arr,mover=walk(c0,w); assert c==c0
    chords=[c0]; cc=c0
    for op in w: cc=OPS[op](cc); chords.append(cc)
    # voice threads
    vs=[list(start)]; v=list(start)
    for i,s in zip(mover,steps): v=list(v); v[i]+=s; vs.append(v)
    thr=['-'.join(NM[x[j]%12] for x in vs) for j in range(3)]
    return dict(word=w,chords='-'.join(cname(x) for x in chords),melody='-'.join(NM[a] for a in arr),steps=steps,
        voices_moving=''.join(str(i+1) for i in mover),threads=thr,disp=[e-s for s,e in zip(start,end)],W=sum(steps)//12)
E={}
E['hexagon C-Cm-Ab-Fm-F-Am']=show((0,'M'),'PLRPLR')
E['hexatonic']=show((0,'M'),'PLPLPL')
E['octatonic']=show((0,'M'),'PRPRPRPR')
E['winding PRLRLRLR']=show((0,'M'),'PRLRLRLR')
# pedal (2-voice) primes and sequences census
for m in range(6,19,2):
    ped=0; seq=collections.Counter(); voicesets=collections.Counter(); contours=set()
    for w in closed_words(m):
        for c0 in [(r,q) for r in range(12) for q in 'Mm']:
            c,start,end,steps,arr,mover=walk(c0,w)
            if c!=c0: continue
            chords=[c0]; cc=c0
            for op in w[:-1]: cc=OPS[op](cc); chords.append(cc)
            if minper(list(zip(chords,w)))<m: continue
            voicesets[len(set(mover))]+=1
            p=minper(steps)
            if p<m:
                # transposition between chord 0 and chord p
                k=(chords[p][0]-chords[0][0])%12 if chords[p][1]==chords[0][1] else None
                seq[(p,k)]+=1
            contours.add(canon(steps))
    print(m,'voices used',{k:v//m for k,v in voicesets.items()},'sequential (motif len, transposition):',{k:v//m for k,v in seq.items()},'distinct contours',len(contours),flush=True)
json.dump(E,open('examples.json','w'),indent=1)
for k,v in E.items(): print(k,v)
