import json, re, collections, sys
D=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..')+'/'
P=json.load(open(D+'problem_library.json')); M=json.load(open(D+'ma_library.json')); L=json.load(open(D+'practice-log.json'))
def norm(t):
    t=(t or '').lower().replace('&',' and ').replace('2-d','2d')
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',t)).strip()
names={}
ev=collections.defaultdict(list)   # norm topic -> (date, label, pos, wrong, kind)
QRD={'What to Expect':'2026-09-05','ISEE Lower #1':'2026-08-30','ISEE Lower #2':'2026-09-13','ISEE Lower #3':'2026-09-25','ISEE Lower #4':'2026-09-27','ISEE Lower #5':'2026-11-01','ISEE LOWER #6':'2026-11-08','OFFICIAL LOWER':'2026-11-15'}
def short(s): return s.replace('OFFICIAL LOWER','Official').replace('ISEE LOWER #','PT').replace('ISEE Lower #','PT').replace('What to Expect','WTE')
def add(topic,date,label,pos,wrong,kind):
    if not topic: return
    n=norm(topic); names.setdefault(n,topic); ev[n].append((date,label,pos,wrong,kind))
seen=set()
for x in P:
    s=x.get('set_name') or x.get('test_set')
    if s not in QRD or x.get('is_wrong') is None or x.get('is_duplicate_capture'): continue
    k=(s,x.get('question_number'))
    if k in seen: continue
    seen.add(k)
    add(x.get('official_topic'),QRD[s],short(s)+' QR #%s'%x.get('question_number'),x.get('question_number'),x['is_wrong'],'realQR')
MAD={'ISEE LOWER #%d'%i:QRD['ISEE Lower #%d'%i] if i<6 else QRD['ISEE LOWER #%d'%i] for i in range(1,7)}; MAD['OFFICIAL LOWER']=QRD['OFFICIAL LOWER']
seen=set()
for m in M:
    s=m.get('test_set') or ('What to Expect' if 'Expect' in (m.get('source_file') or '') else None)
    if m.get('is_wrong') is None or s is None: continue
    k=(s,m.get('question_number'))
    if k in seen: continue
    seen.add(k)
    add(m.get('official_topic'),MAD.get(s,'2026-09-05'),short(s)+' MA #%s'%m.get('question_number'),m.get('question_number'),m['is_wrong'],'realMA')
for s in L['sets']:
    g=[(k,v) for k,v in s.items() if k.startswith('graded')]
    if g: date=g[0][0].split('_')[1]; wr=set(g[0][1].get('wrong',[]))|set(g[0][1].get('blank',[]) or g[0][1].get('blanks',[]) or [])
    elif 'click_results' in s: date='2026-10-04'; wr=set(s['click_results']['final_wrong'])
    else: continue
    for i,t in enumerate(s['topics'],1): add(t,date,'QR%d #%d'%(s['set_no'],i),i,i in wr,'setQR')
for s in L['ma_sets']:
    g=[(k,v) for k,v in s.items() if k.startswith('graded')]
    if not g: continue
    date=g[0][0].split('_')[1]; wr=set(g[0][1].get('wrong',[]))
    for i,t in enumerate(s['topics'],1): add(t,date,'MA%d #%d'%(s['set_no'],i),i,i in wr,'setMA')
def stats(n):
    e=sorted(ev[n])
    real=[x for x in e if x[4]=='realQR']
    r5=e[-5:]
    lw=[x for x in e if x[3]]
    return dict(topic=names[n], n=len(e), wrong=sum(x[3] for x in e),
        realQR=len(real), realQR_mid=sum(1 for x in real if 13<=x[2]<=25), realQR_last=sum(1 for x in real if x[2]>=26),
        realQR_wrong=sum(x[3] for x in real),
        last_done=e[-1][1]+' ('+e[-1][0][5:]+')', last_wrong=(lw[-1][1]+' ('+lw[-1][0][5:]+')') if lw else '-',
        recent='%d/%d'%(sum(x[3] for x in r5),len(r5)), recent_rate=sum(x[3] for x in r5)/len(r5),
        since_1025='%d/%d'%(sum(x[3] for x in e if x[0]>='2026-10-25'),sum(1 for x in e if x[0]>='2026-10-25')),
        lw_date=lw[-1][0] if lw else '', ld_date=e[-1][0], events=e)
S={n:stats(n) for n in ev}
json.dump({n:{k:v for k,v in s.items()} for n,s in S.items()},open(sys.argv[1] if len(sys.argv)>1 else '/dev/null','w'),indent=1)
cand=[s for s in S.values() if s['realQR_mid']+s['realQR_last']>0]
cand.sort(key=lambda s:(-(s['realQR_last']*2+s['realQR_mid']), s['topic']))
print('%-52s %4s %4s %4s %-22s %-22s %6s %7s'%('topic','mid','last','rqW','last done','last wrong','last5','since10/25'))
for s in cand: print('%-52s %4d %4d %4d %-22s %-22s %6s %7s'%(s['topic'][:52],s['realQR_mid'],s['realQR_last'],s['realQR_wrong'],s['last_done'],s['last_wrong'],s['recent'],s['since_1025']))
