import json,urllib.request,time,math,os,subprocess
B=int(((9/4)*(8*math.pi**2)**6)**(2/3))+1
st='fetch6_state.json'
out,off=(json.load(open(st)) if os.path.exists(st) else ([],0))
while True:
    url=f"https://www.lmfdb.org/api/nf_fields/?degree=i6&r2=i0&_format=json&_fields=label,coeffs,disc_abs&_sort=disc_abs&_offset={off}"
    d=None
    for k in range(60):
        try: d=json.loads(subprocess.run(['curl','-s','-m','90',url],capture_output=True,text=True).stdout); break
        except Exception as e: time.sleep(min(300,20*(k+1)))
    if d is None: raise SystemExit('fetch failed at offset %d'%off)
    rows=d['data']
    if not rows: break
    out+=rows; off+=len(rows); json.dump([out,off],open(st,"w")); time.sleep(4)
    if rows[-1]['disc_abs']>B: break
out=[r for r in out if r['disc_abs']<=B]
print(B,len(out),out[-1],flush=True)
json.dump(out,open('lmfdb_sextic_tr.json','w'))
json.dump(['+'.join(f'({c})*x^{i}' for i,c in enumerate(r['coeffs'])) for r in out],open('sextic_pols.json','w'))
