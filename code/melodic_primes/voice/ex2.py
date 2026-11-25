from voices import *
exec(open('ex.py').read().split('E={}')[0])
import json
d=show((0,'M'),'RL'*12); print(d)
d2=show((0,'M'),'LR'*12); print(d2['W'],d2['disp'],d2['melody'])
e=json.load(open('examples.json')); e['circle RL^12']=d; json.dump(e,open('examples.json','w'),indent=1)
