import re,csv,difflib,sys
gaps={};sec=None
for l in open('CAVT_GAPS.md'):
    if l.startswith('## '): sec=l[3:6]
    m=re.match(r'\| (\d+) \| ([^|]+)\|',l)
    if sec in('3.1','3.2','3.3') and m: gaps[int(m.group(1))]=(sec,m.group(2).strip())
T={int(r['cavt_no']):r['title'] for r in csv.DictReader(open('raw/cavt/cavt_entries.csv'))}
L=open('raw/cavt/cavt.md').read().split('\n')
END=int(sys.argv[1])
def norm(x): return re.sub(r'^[\W\dIlOo]{0,6}[.,:]?\s*','',x.strip()).lower()
C=[(i,norm(l)) for i,l in enumerate(L) if 1200<i<END and 3<len(l.strip())<120]
cands={}
for n in range(1,278):
    t=T[n].lower(); tp=re.sub(r'\s*\(.*','',t)
    cs=[]
    for i,r in C:
        a=difflib.SequenceMatcher(None,r[:len(t)+3],t).quick_ratio()
        if a<0.6: continue
        s=max(difflib.SequenceMatcher(None,r[:len(t)+3],t).ratio(), difflib.SequenceMatcher(None,r[:len(tp)],tp).ratio()-0.05)
        if s>0.7: cs.append((i,s))
    cands[n]=cs
# DP: longest weighted increasing chain
best={}  # line->(score,prev)
chain=[(1200,0.0,None)]  # list of states (line,score,backptr)
states=[(1200,0,None,0)]
for n in range(1,278):
    new=[]
    for i,s in cands[n]:
        p=max((st for st in states if st[0]<i),key=lambda st:st[1],default=None)
        if p: new.append((i,p[1]+s,p,n))
    states=states+new
end=max(states,key=lambda st:st[1]); starts={}
while end and end[3]: starts[end[3]]=end[0]; end=end[2]
ks=sorted(starts)
print('located',len(ks),file=sys.stderr)
pat=re.compile(r"\b[Cc]odd?\.?:?\s+(?:[e€c]\s+)?([A-Z][\w'.-]+(?: \(?[\w'.-]+\)?){0,2}, [^;:]{1,90}?(?:\b\d{1,5}[a-z]?\b|\b[IVXLivxl]+\.?,? (?=fol\.)))")
out=[]
for k,(sec,t) in sorted(gaps.items()):
    if k not in starts: print('UNLOCATED',k,t,file=sys.stderr);continue
    j=ks.index(k); e=starts[ks[j+1]] if j+1<len(ks) else END
    txt=' '.join(l for l in L[starts[k]:e] if not l.startswith('<!--'))
    txt=re.sub(r'-\s+(?=[a-z])','',txt)
    hits=[h.strip() for h in pat.findall(txt) if not re.search(r'p\. \d|\b1[6-9]\d\d\b|\b20\d\d\b',h)]
    hits=[h for h in dict.fromkeys(hits) if not re.search(r'[A-ZÄÂÖÜÉ]{4,}| in [A-Z]',h)]
    if hits: out.append((k,sec,t,hits))
for k,sec,t,h in out: print(f"{k}\t{sec}\t{t}\t{len(h)}\t{'; '.join(h[:3])}")
print(len(out),'of',len(gaps),file=sys.stderr)
