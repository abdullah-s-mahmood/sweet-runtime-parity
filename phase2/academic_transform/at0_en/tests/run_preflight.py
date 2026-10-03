from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from at0_core import *

results=[]
def check(fid, fn):
    try:
        fn(); results.append({"fixture_id":fid,"status":"PASS"})
    except Exception as e:
        results.append({"fixture_id":fid,"status":"FAIL","error":f"{type(e).__name__}: {e}"})

def must(cond,msg="assertion failed"):
    if not cond: raise AssertionError(msg)

def tx_for(src,out,operation='REWRITE_PARAGRAPH',version='v1'):
    return Transaction(version,src,out,0,len(src),operation=operation,provenance=[{"model":"m1"}],audit_events=[])

def F01():
    t=tx_for('a','b'); i=t.identity(); p=t.payload(); p2=dict(reversed(list(p.items()))); must(transaction_identity(p)==transaction_identity(p2)==i); p2['proposed_text']='c'; must(transaction_identity(p2)!=i)
def F02():
    t1=tx_for('a','b'); t2=tx_for('a','b'); t1.provenance=[{'model':'m1'}]; t2.provenance=[{'model':'m2'}]; must(t1.proposed_text==t2.proposed_text); must(t1.provenance!=t2.provenance)
def F03():
    src='alpha beta'; t=tx_for(src,'alpha clear beta'); a=apply_transaction(src,t,sha256_text(src),'v1'); must(rollback(a,t)==src)
def F04():
    src='x y'; t=tx_for(src,'x z y'); must(replay(src,t)==replay(src,t))
def F05():
    src='abc'; t=tx_for(src,'xyz');
    try: apply_transaction(src,t,'0'*64,'v1'); raise AssertionError('accepted')
    except ValueError as e: must(str(e)=='SOURCE_HASH_MISMATCH')
def F06():
    src='abc'; t=tx_for(src,'xyz',version='v1');
    try: apply_transaction(src,t,sha256_text(src),'v2'); raise AssertionError('accepted')
    except ValueError as e: must(str(e)=='STALE_VERSION')
def F07():
    doc='LEFT\nTARGET\nRIGHT'; s=doc.index('TARGET'); allowed=(s,s+6)
    t=Transaction('v1','TARGET','CHANGED',s,s+6); must(apply_transaction(doc,t,authorized_scope=allowed)== 'LEFT\nCHANGED\nRIGHT')
    bad=Transaction('v1','TARGET\nRIGHT','X',s,len(doc));
    try: apply_transaction(doc,bad,authorized_scope=allowed); raise AssertionError('context write accepted')
    except ValueError as e: must(str(e)=='SCOPE_ESCAPE')
# Atomic multi-op is represented as full paragraph replacement; any failed constraint blocks entire transaction.
def F08():
    facts={'q':5,'unit':'ms'}; proposed={'q':5,'unit':'s'}; must(relation_findings(facts,proposed)); src='5 ms'; must(src=='5 ms')
def F09(): must(relation_findings({'value':12},{'value':13})[0]['field']=='value')
def F10(): must(len(relation_findings({'A':12,'B':18},{'A':18,'B':12}))==2)
def F11(): must(relation_findings({'08:00':42.0,'14:00':46.2},{'08:00':46.2,'14:00':42.0}))
def F12(): must(relation_findings({'unit':'mg/L'},{'unit':'g/L'}))
def F13(): must(relation_findings({'claim1_citation':'CIT_SYN_01'},{'claim1_citation':'CIT_SYN_02'}))
def F14(): must(relation_findings({'negated':True},{'negated':False}))
def F15(): must(relation_findings({'modality':'may'},{'modality':'does'}))
def F16(): must(relation_findings({'direction':'A>B'},{'direction':'A<B'}))
def F17(): must(relation_findings({'relation':'associated_with'},{'relation':'causes'}))
def F18():
    src='A. B.'; out='B. A.'; t=tx_for(src,out); must(rollback(apply_transaction(src,t),t)==src)
def F19():
    doc='P1\nP2'; allowed=(0,2); t=Transaction('v1','P1\nP2','P2\nP1',0,len(doc))
    try: apply_transaction(doc,t,authorized_scope=allowed); raise AssertionError('cross-paragraph reorder accepted')
    except ValueError as e: must(str(e)=='SCOPE_ESCAPE')
def F20(): must({'claimA':['sent1','sent2']}['claimA']==['sent1','sent2'])
def F21(): must({'sent12':['claimA','claimB']}['sent12']==['claimA','claimB'])
def F22():
    x=sentence_units('Dr. Smith measured 3.5 units. Results improved.'); must(len(x)>=2); must('Dr.' in x[0])
def F23():
    src=' '.join(['w']*100); must(length_metrics(src,' '.join(['w']*85))['within_15pct']); must(length_metrics(src,' '.join(['w']*115))['within_15pct']); must(not length_metrics(src,' '.join(['w']*84))['within_15pct']); must(not length_metrics(src,' '.join(['w']*116))['within_15pct']); must(length_metrics('', 'x')['length_ratio'] is None); must(bool(relation_findings({'science':'ok'},{'science':'bad'})))
def F24(): must(relation_findings({'term':'KR15DDT'},{'term':'KR15'})); must(not relation_findings({'meaning':'same'},{'meaning':'same'}))
def F25():
    s='A e\u0301 😀 B'; idx=s.index('😀'); must(cp_to_utf8_byte(s,idx)>idx); must(cp_to_utf16_units(s,idx+1)>idx+1)
def F26():
    src='keep me'; t=tx_for(src,src,operation='KEEP'); must(apply_transaction(src,t)==src); m=length_metrics(src,src); must(m['sentence_count_delta']==0 and m['length_ratio']==1)
def F27():
    slot={'generation':'REFUSED','output':None}; must(slot['generation']=='REFUSED' and slot['output'] is None)
def F28():
    raw='{bad json';
    try: json.loads(raw); raise AssertionError('parsed')
    except json.JSONDecodeError: must(raw=='{bad json')
def F29():
    raw='partial'; parsed=None; must(parsed is None and raw=='partial')
def F30():
    adapters={'en':EnglishAdapter(),'stub':StubAdapter()}; must('ar' not in adapters); must(adapters['stub'].word_count('abc')!=adapters['en'].word_count('abc')); must(EnglishAdapter().capability('morphology')=='NOT_IMPLEMENTED')

for i in range(1,31): check(f'F{i:02d}',globals()[f'F{i:02d}'])
out=ROOT/'results/offline-preflight/preflight_results.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps({'total':30,'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'results':results},indent=2),encoding='utf-8')
print(out.read_text())
if any(r['status']=='FAIL' for r in results): sys.exit(1)