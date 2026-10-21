import sys,re
D=sys.argv[1]
def load(f):
    m={};n=None
    for l in open(f"{D}/{f}.tf",encoding='utf8'):
        l=l.rstrip('\n')
        if l.startswith('@') or (n is None and l==''): continue
        if '\t' in l: k,v=l.split('\t',1)
        else: k,v='',l
        if k:
            if '-' in k:
                a,b=map(int,k.split('-'));
                for i in range(a,b+1): m[i]=v
                n=b; continue
            n=int(k)
        else: n=(n or 0)+1
        m[n]=v
    return m
ot=load('otype'); sl=load('oslots'); sc=load('scroll'); fr=load('fragment'); ln=load('line'); fu=load('full'); af=load('after')

def rng(v):
    r=[]
    for p in v.split(','):
        a,_,b=p.partition('-'); r+=range(int(a),int(b or a)+1)
    return r
import bisect
words=sorted((min(rng(sl[n])),n) for n,t in ot.items() if t=='word')
firsts=[w[0] for w in words]
want=set(sys.argv[2].split(','))
for n,t in ot.items():
    if t=='line' and sc.get(n) in want:
        r=rng(sl[n]); lo,hi=min(r),max(r)
        i=bisect.bisect_left(firsts,lo); out=''
        while i<len(words) and firsts[i]<=hi:
            w=words[i][1]; out+=fu.get(w,'')+af.get(w,''); i+=1
        print(sc[n],fr.get(n),ln.get(n),out,sep='\t')
