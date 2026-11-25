exec(open('primes.py').read().split("A=np.zeros")[0])
import sys
sys.setrecursionlimit(100)
cnt=0; words=[]
def dfs(c,vis,w):
    global cnt
    if len(w)==24:
        return
    for k,f in OPS.items():
        if w and w[-1]==k: continue
        d=f(c)
        if len(w)==23:
            if d==(0,'M') and k!=w[0]: cnt+=1; words.append(w+k)
            continue
        if d in vis: continue
        vis.add(d); dfs(d,vis,w+k); vis.remove(d)
dfs((0,'M'),{(0,'M')},'')
print('directed Hamiltonian cycles through C:',cnt)
import json; json.dump(words,open('hamiltonian_words.json','w'))
