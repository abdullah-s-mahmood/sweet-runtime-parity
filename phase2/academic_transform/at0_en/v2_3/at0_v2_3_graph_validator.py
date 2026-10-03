import json,re,sys,pathlib,collections

def norm(s): return re.sub(r'\s+',' ',s.lower()).strip()
def sentences(s): return re.split(r'(?<=[.!?])\s+',norm(s))

def validate_case(graph_case,text):
    t=norm(text); findings=[]
    def add(c,msg): findings.append({'constraint_id':c['id'],'severity':c['severity'],'message':msg})
    for c in graph_case['constraints']:
        k=c['kind']
        if k=='REQUIRE_ALL_REGEX':
            for p in c['patterns']:
                if not re.search(p,t,re.I): add(c,f'missing required pattern: {p}')
        elif k=='REQUIRE_ANY_GROUP':
            for grp in c['groups']:
                if not any(re.search(p,t,re.I) for p in grp): add(c,f'none matched: {grp}')
        elif k=='FORBID_REGEX':
            for p in c['patterns']:
                if re.search(p,t,re.I): add(c,f'forbidden pattern matched: {p}')
        elif k=='REVIEW_REGEX':
            for p in c['patterns']:
                if re.search(p,t,re.I): add(c,f'review pattern matched: {p}')
        elif k=='SAME_SENTENCE':
            found=False
            for sent in sentences(t):
                if re.search(c['anchor'],sent,re.I) and all(re.search(p,sent,re.I) for p in c['patterns']):
                    found=True; break
            if not found: add(c,'same-sentence binding not satisfied')
        elif k=='ORDERED_REGEX':
            pos=-1; ok=True
            for p in c['patterns']:
                m=re.search(p,t[pos+1:],re.I)
                if not m: ok=False; break
                pos=pos+1+m.end()
            if not ok: add(c,'ordered relation not satisfied')
        else: raise ValueError(k)
    hard=sum(x['severity']=='HARD' for x in findings)
    review=sum(x['severity']=='REVIEW' for x in findings)
    return {'disposition':'REJECT' if hard else ('REVIEW' if review else 'PASS_CANDIDATE'),'hard_findings':hard,'review_findings':review,'findings':findings}

def load_graph(path):
    g=json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    return {x['case_id']:x for x in g['cases']}

if __name__=='__main__':
    graph=load_graph(sys.argv[1])
    rows=[]
    for line in pathlib.Path(sys.argv[2]).read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        r=json.loads(line); out=dict(r)
        if isinstance(r.get('candidate_text'),str) and r['candidate_text'].strip():
            out.update(validate_case(graph[r['case_id']],r['candidate_text']))
        rows.append(out)
    p=pathlib.Path(sys.argv[3])
    p.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows),encoding='utf-8')
    c=collections.Counter(x.get('disposition','UNAVAILABLE') for x in rows)
    print(json.dumps(dict(c),indent=2,sort_keys=True))
