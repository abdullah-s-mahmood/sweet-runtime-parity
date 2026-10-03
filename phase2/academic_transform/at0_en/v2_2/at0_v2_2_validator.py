import json,re,sys,pathlib,collections

CAUSAL_STRENGTH = [r'\bdue to\b', r'\bcaus(?:e|es|ed|ing)\b', r'\bdemonstrat(?:e|es|ed|ing)\b', r'\bprove[sd]?\b', r'\bensure[sd]?\b', r'\battribut(?:e|ed|able)\b', r'\bguarantee[sd]?\b', r'\bas (?:a )?consequence of\b']
NOVEL_ASSERTIVE = [r'\baccuracy\b',r'\brelevance\b',r'\befficien(?:t|cy)\b',r'\btraffic management\b',r'\bemerging issues\b',r'\bcrucial\b',r'\bprecise tracking\b']

def norm(s):
    return re.sub(r'\s+',' ',s.lower()).strip()

def has(text,*patterns):
    t=norm(text)
    return all(re.search(p,t,re.I) for p in patterns)

def anyp(text,patterns):
    t=norm(text)
    return any(re.search(p,t,re.I) for p in patterns)

def sentence_with(text, anchor):
    for sent in re.split(r'(?<=[.!?])\s+',norm(text)):
        if anchor.lower() in sent:
            return sent
    return ''

def finding(code,severity,msg): return {'code':code,'severity':severity,'message':msg}

def common_review(source,out):
    fs=[]
    s,o=norm(source),norm(out)
    for p in CAUSAL_STRENGTH:
        if re.search(p,o,re.I) and not re.search(p,s,re.I):
            fs.append(finding('CLAIM_STRENGTHENING_CANDIDATE','REVIEW',f'new strong/causal cue: {p}'))
    for p in NOVEL_ASSERTIVE:
        if re.search(p,o,re.I) and not re.search(p,s,re.I):
            fs.append(finding('NEW_INFORMATION_CANDIDATE','REVIEW',f'novel assertive phrase: {p}'))
    return fs

def req(fs,cond,code,msg,severity='HARD'):
    if not cond: fs.append(finding(code,severity,msg))

def validate(case_id, source, out):
    fs=common_review(source,out)
    t=norm(out)
    if case_id=='EN01':
        req(fs, has(t,r'traffic',r'real[- ]?time'),'EN01_MONITOR','traffic real-time monitoring not clearly preserved')
        req(fs, has(t,r'roadside',r'(collect|observation)'),'EN01_ROADSIDE','roadside collection claim missing')
        req(fs, has(t,r'congestion',r'(faster|rapid|quick)'),'EN01_CONGESTION','faster congestion identification claim missing')
        req(fs, has(t,r'arterial roads',r'weekday peak') and anyp(t,[r'\bonly\b',r'\blimit(?:ed|s)?\b',r'\brestrict(?:ed|s)?\b',r'\bfocus\b',r'\bexclusive(?:ly)?\b']),'EN01_SCOPE','restricted evaluation scope not clearly preserved')
    elif case_id=='EN02':
        req(fs, anyp(t,[r'15\s*(?:minutes?|min\b)']),'EN02_INTERVAL','15-minute interval missing')
        req(fs, anyp(t,[r'\btwo\s+collection vehicles?\b',r'\b2\s+collection vehicles?\b']),'EN02_VEHICLES','two collection vehicles missing')
        req(fs, 'synthetic district' in t,'EN02_DISTRICT','synthetic district missing')
        req(fs, 'travel distance' in t,'EN02_DISTANCE','travel distance metric missing')
        req(fs, anyp(t,[r'missed[- ]overflow']),'EN02_OVERFLOW','missed-overflow metric missing')
        if anyp(t,[r'\bnovel\b',r'\bfirst\b',r'state[- ]of[- ]the[- ]art',r'\boutperform']):
            fs.append(finding('UNSUPPORTED_NOVELTY','HARD','novelty/superiority claim introduced'))
    elif case_id=='EN03':
        req(fs, has(t,r'study a',r'(lower|reduc)\w* latency',r'edge aggregation'),'EN03_A','Study A relation missing')
        req(fs, 'study b' in t and 'sparse traffic' in t and bool(re.search(r'(?:no|does not|did not).{0,40}latency.{0,40}(?:reduc|improv)',t)),'EN03_B','Study B relation missing')
        req(fs, has(t,r'study c',r'12\s*%',r'(energy|consumption)',r'batch'),'EN03_C','Study C relation missing')
        req(fs, has(t,r'study d',r'batch',r'(increase|increased)\w* delay',r'emergency'),'EN03_D','Study D relation missing')
        req(fs, anyp(t,[r'not (?:uniformly )?consistent',r'different operating conditions',r'vary across']),'EN03_CONTRAST','non-uniform overall effect missing','REVIEW')
        if re.search(r'study c.{0,100}(demonstrat|due to)',t):
            fs.append(finding('EN03_C_STRENGTHENED','HARD','Study C reporting relation strengthened toward demonstration/causation'))
        # The source binds edge aggregation only to Study A. A summary that scopes Studies C/D under edge aggregation conflates mechanisms.
        lead=t.split('study a',1)[0]
        if 'edge aggregation' in lead and any(x in lead for x in ['study c','study d','studies a, b, c','studies a,b,c']):
            fs.append(finding('EN03_MECHANISM_CONFLATION','HARD','edge aggregation was generalized to studies whose source mechanism is message batching'))
    elif case_id=='EN04':
        req(fs,'[cit_syn_01]' in t,'EN04_CIT1','CIT_SYN_01 missing')
        req(fs,'[cit_syn_02]' in t,'EN04_CIT2','CIT_SYN_02 missing')
        req(fs, has(t,r'queue length',r'(reduc|lower)'),'EN04_QUEUE','queue-length claim missing')
        if re.search(r'(?:associated|association|correlated|correlation).{0,60}(?:reduc|lower).{0,50}queue length|queue length.{0,50}(?:associated|association|correlated|correlation)',t):
            fs.append(finding('EN04_ASSERTION_WEAKENED','HARD','asserted queue-length reduction was weakened to association'))
        req(fs, has(t,r'packet loss',r'(increase|higher)',r'(density|roadside|rsu)'),'EN04_PACKET','packet-loss/density relation missing')
        s1=sentence_with(t,'[cit_syn_01]'); s2=sentence_with(t,'[cit_syn_02]')
        req(fs, bool(s1) and bool(re.search(r'queue length',s1)) and bool(re.search(r'(reduc|lower)',s1)),'EN04_CIT1_LINK','CIT_SYN_01 not linked to queue-length reduction')
        req(fs, bool(s2) and bool(re.search(r'packet loss',s2)) and bool(re.search(r'(increase|higher)',s2)),'EN04_CIT2_LINK','CIT_SYN_02 not linked to packet-loss increase')
        req(fs, anyp(t,[r'different subsystems?',r'distinct subsystems?']),'EN04_DISTINCT','different-subsystem distinction missing','REVIEW')
    elif case_id=='EN05':
        req(fs,'evening' in t,'EN05_POP','evening-window restriction missing')
        req(fs, has(t,r'beacon density',r'(associat|correlat)',r'(shorter|reduc)\w* discovery'),'EN05_ASSOC','association claim missing or strengthened')
        req(fs, anyp(t,[r'\bmay\b.{0,80}(awareness|neighbor)',r'(awareness|neighbor).{0,80}\bmay\b']),'EN05_HEDGE','may/uncertainty on neighbor-awareness explanation missing')
        req(fs, anyp(t,[r'does not (?:establish|demonstrate|prove).{0,80}caus',r'cannot (?:establish|demonstrate|prove).{0,80}caus',r'not.*causal']),'EN05_CAUSAL_NEG','non-causality statement missing')
        req(fs, anyp(t,[r'not (?:evaluated|assessed|tested) outside',r'outside the evening window.{0,40}not']),'EN05_OUTSIDE','not-evaluated-outside restriction missing')
    elif case_id=='EN06':
        for val in ['42.0','51.5','46.2','49.8','4.2']:
            req(fs,val in t,f'EN06_VAL_{val}',f'value {val} missing')
        req(fs,'08:00' in t and '14:00' in t,'EN06_TIMES','time identities missing')
        req(fs,'group a' in t and 'group b' in t,'EN06_GROUPS','group identities missing')
        s08=sentence_with(t,'08:00'); s14=sentence_with(t,'14:00')
        req(fs, bool(re.search(r'group a.{0,45}42\.0|42\.0.{0,25}(?:for )?group a',s08)) and bool(re.search(r'group b.{0,45}51\.5|51\.5.{0,25}(?:for )?group b',s08)),'EN06_BIND_0800','08:00 values are not bound to the correct groups')
        req(fs, bool(re.search(r'group a.{0,45}46\.2|46\.2.{0,25}(?:for )?group a',s14)) and bool(re.search(r'group b.{0,45}49\.8|49\.8.{0,25}(?:for )?group b',s14)),'EN06_BIND_1400','14:00 values are not bound to the correct groups')
        req(fs, anyp(t,[r'(increase|increased|rose).{0,50}4\.2',r'4\.2.{0,50}(increase|increased|rose)']),'EN06_DELTA','4.2-second increase relation missing')
        req(fs,'08:00' in t and 'baseline' in t,'EN06_BASELINE','08:00 baseline relation missing','REVIEW')
        if re.search(r'performance (?:increased|improved)',t):
            fs.append(finding('EN06_PERFORMANCE_DIRECTION','REVIEW','ambiguous performance direction introduced for increased time'))
    elif case_id=='EN07':
        req(fs, anyp(t,[r'(discard|reject|remove)\w*.{0,50}(older than|over) 60\s*(?:s|seconds?)',r'60\s*(?:s|seconds?).{0,50}(discard|reject|remove)']),'EN07_60S','discard >60s step missing')
        req(fs, has(t,r'normaliz',r'fixed (?:before|prior to) (?:evaluation|the evaluation|run|the run)'),'EN07_FIXED','normalization with pre-fixed parameters missing')
        req(fs, bool(re.search(r'(?:exclude|excluded).{0,50}(?:missing|lacking) position|(?:missing|lacking) position.{0,50}excluded',t)),'EN07_EXCLUDE','missing-position exclusion missing')
        req(fs,'200' in t and '17' in t and 'seed' in t,'EN07_REPRO','200 iterations / seed 17 missing')
        req(fs, anyp(t,[r'without (?:further|additional) tuning',r'no (?:further|additional) tuning',r'not.*(?:further|additional) tun']),'EN07_NOTUNE','no-further-tuning condition missing')
    elif case_id=='EN08':
        req(fs, has(t,r'channel occupancy',r'(associat|correlat)',r'delivery ratio'),'EN08_ASSOC','association relation missing')
        req(fs, has(t,r'(strongest|most pronounced)',r'medium[- ]density'),'EN08_MEDIUM','medium-density condition missing')
        req(fs, has(t,r'(not|did not)',r'(manipulat|controlled?)',r'occupancy'),'EN08_MANIP','non-manipulation condition missing')
        req(fs, anyp(t,[r'does not (?:demonstrate|establish|prove)',r'cannot (?:demonstrate|establish|prove|conclude)',r'not.*causal']),'EN08_NOCAUSE','no-causal-conclusion statement missing')
        req(fs, anyp(t,[r'other networks?',r'generaliz']),'EN08_GENERAL','other-network/generalization restriction missing','REVIEW')
    elif case_id=='EN09':
        for token in ['p_i','w_1','u_i','w_2','d_i']:
            req(fs,token in t,f'EN09_EQ_{token}',f'equation token {token} missing')
        req(fs,bool(re.search(r'u_i\s+(?:is|represents?|denotes?)\s+utilization|u_i\s*,?\s*(?:which\s+)?(?:represents?|denotes?)\s+utilization|utilization\s*\(\s*u_i\s*\)',t)),'EN09_U','U_i meaning missing or misbound')
        req(fs,bool(re.search(r'd_i\s+(?:is|represents?|denotes?)\s+normalized deadline pressure|d_i\s*,?\s*(?:which\s+)?(?:represents?|denotes?)\s+normalized deadline pressure|normalized deadline pressure\s*\(\s*d_i\s*\)',t)),'EN09_D','D_i meaning missing or misbound')
        req(fs,bool(re.search(r'weights?.{0,80}fixed (?:before|prior to)',t)),'EN09_WEIGHTS','pre-fixed weights missing')
        req(fs,anyp(t,[r'equation.{0,80}(?:not changed|unchanged|not modified|remains unchanged)',r'(?:not changed|unchanged|not modified|remains unchanged).{0,80}equation']),'EN09_UNCHANGED','equation unchanged during adaptation missing')
    elif case_id=='EN10':
        req(fs, anyp(t,[r'one measurement every 30\s*(?:s|seconds?)',r'every 30\s*(?:s|seconds?)']),'EN10_RATE','30-second measurement rate missing')
        req(fs,'active node' in t,'EN10_ACTIVE','active-node scope missing')
        req(fs,'timestamp' in t and 'node identifier' in t,'EN10_META','timestamp/node identifier missing')
        req(fs,'node' in t and anyp(t,[r'five[- ]minute',r'5[- ]minute']),'EN10_GROUP','node/five-minute grouping missing')
        req(fs,anyp(t,[r'no imputation',r'not imputed',r'imputation is not']),'EN10_IMPUTE','no-imputation condition missing')
    elif case_id=='EN11':
        req(fs,has(t,r'gateway',r'receiv',r'report'),'EN11_RECEIVE','gateway receive step missing')
        req(fs,'identifier' in t,'EN11_ID','identifier check missing')
        req(fs,'timestamp' in t,'EN11_TS','timestamp check/storage missing')
        req(fs,has(t,r'reject',r'duplicate'),'EN11_DUP','duplicate rejection missing')
        req(fs,has(t,r'forward',r'(accepted|valid)',r'storage'),'EN11_FORWARD','forward accepted reports missing')
        req(fs,has(t,r'storage',r'original timestamp'),'EN11_ORIG','original timestamp storage missing')
    elif case_id=='EN12':
        req(fs,anyp(t,[r'three traffic densit',r'3 traffic densit']),'EN12_DENS','three traffic densities missing')
        req(fs,has(t,r'reliability',r'delivery ratio'),'EN12_REL','reliability=delivery ratio missing')
        req(fs,'delay' in t,'EN12_DELAY','delay metric missing')
        req(fs,bool(re.search(r'parameter.{0,50}(?:same|fixed|remain(?:s|ed)? unchanged).{0,60}densit|(?:same|fixed).{0,30}parameter.{0,60}densit',t)),'EN12_FIXED','same parameter values across densities missing')
        req(fs,anyp(t,[r'rather than.{0,60}retun',r'not.{0,60}retun',r'distinguish.{0,60}retun',r'isolate.{0,60}retun']),'EN12_RETUNE','load-vs-retuning purpose missing','REVIEW')
        if re.search(r'ensure\w*.{0,100}attribut',t):
            fs.append(finding('EN12_ATTRIBUTION_STRENGTH','HARD','fixed parameters strengthened to guaranteed attribution'))
    hard=sum(f['severity']=='HARD' for f in fs)
    review=sum(f['severity']=='REVIEW' for f in fs)
    disp='REJECT' if hard else ('REVIEW' if review else 'PASS_CANDIDATE')
    return {'disposition':disp,'hard_findings':hard,'review_findings':review,'findings':fs}

def extract_context(prompt):
    marker='\n\nINPUT\n'
    if marker not in prompt: return None
    s=prompt.split(marker,1)[1]
    if '\n\nPLAN\n' in s: s=s.split('\n\nPLAN\n',1)[0]
    return json.loads(s)

def word_count(s): return len(re.findall(r'\S+',s or ''))

def extract_candidate(slot):
    p=slot.get('parsed_output')
    if isinstance(p,dict):
        if p.get('status') in {'REVISE','KEEP','REVIEW'}:
            return p.get('status'),p.get('revised_paragraph'),'V21_SCHEMA_VALID'
        ro=p.get('required_output')
        if isinstance(ro,dict) and isinstance(ro.get('revised_paragraph'),str):
            return ro.get('status','UNKNOWN'),ro.get('revised_paragraph'),'DIAGNOSTIC_NESTED_REQUIRED_OUTPUT'
        if isinstance(p.get('revised_paragraph'),str):
            return p.get('status','UNKNOWN'),p.get('revised_paragraph'),'DIAGNOSTIC_TOPLEVEL_INCOMPLETE'
    return None,None,'NO_AUDITABLE_FINAL_TEXT'

def audit(artifact_dir):
    root=pathlib.Path(artifact_dir)
    slots=[json.loads(x) for x in (root/'slots.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    reqs=[json.loads(x) for x in (root/'requests.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    cases={}
    for r in reqs:
        if r.get('stage')=='DIRECT':
            c=extract_context(r['prompt']); cases[c['case_id']]=c
    rows=[]
    for s in slots:
        c=cases[s['case_id']]
        status,text,extraction=extract_candidate(s)
        row={'slot_id':s['slot_id'],'model_slot':s['model_slot'],'case_id':s['case_id'],'arm':s['arm'],'v21_status':s['status'],'candidate_extraction':extraction,'candidate_status':status}
        if isinstance(text,str) and text.strip():
            v=validate(s['case_id'],c['source_text'],text)
            sw,ow=word_count(c['source_text']),word_count(text)
            row.update(candidate_text=text,source_words=sw,output_words=ow,length_ratio=round(ow/sw,4) if sw else None,**v)
        elif status=='REVIEW' and extraction=='V21_SCHEMA_VALID':
            row.update(disposition='REVIEW_ESCALATED',hard_findings=0,review_findings=1,findings=[finding('MODEL_ESCALATED_REVIEW','REVIEW','model declined to revise and escalated')])
        elif status=='KEEP' and extraction=='V21_SCHEMA_VALID':
            row.update(disposition='PASS_KEEP',hard_findings=0,review_findings=0,findings=[])
        else:
            row.update(disposition='UNAVAILABLE',hard_findings=0,review_findings=0,findings=[])
        rows.append(row)
    return rows

if __name__=='__main__':
    rows=audit(sys.argv[1])
    out=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else pathlib.Path('AT0_EN_V2_2_OFFLINE_AUDIT.jsonl')
    out.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf-8')
    c=collections.Counter(r['disposition'] for r in rows)
    ex=collections.Counter(r['candidate_extraction'] for r in rows)
    per=collections.Counter((r['model_slot'],r['arm'],r['disposition']) for r in rows)
    summary={'slots':len(rows),'dispositions':dict(c),'candidate_extraction':dict(ex),'by_model_arm':{'|'.join(k):v for k,v in sorted(per.items())}}
    sp=out.with_suffix('.summary.json'); sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2,sort_keys=True))
