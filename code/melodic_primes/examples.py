NM=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']; S={3,4,5,7,8,9}
def chk(mel):
    p=[NM.index(x) for x in mel.split('-')]; st=[(b-a)%12 for a,b in zip(p,p[1:])]; m=len(st)
    ok=p[0]==p[-1] and all(s in S for s in st) and all((st[i]+st[(i+1)%m])%12 for i in range(m)) and not any(m%d==0 and st==st[:d]*(m//d) and sum(st[:d])%12==0 for d in range(1,m))
    print(mel,'len',m,'PRIME' if ok else 'no')
for x in ['C-E-G-C','C-E-Ab-C','C-Eb-F#-A-C','C-E-G-Eb-C','C-E-A-F-C','C-G-E-A-F-C','C-E-G-B-Ab-F-C','C-E-G-E-C']: chk(x)
