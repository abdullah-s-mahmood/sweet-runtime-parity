from __future__ import annotations
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def jread(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def dump(p,obj):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8'); os.replace(t,p)
def dumpjl(p,rows):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+'.tmp'); t.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows),encoding='utf-8'); os.replace(t,p)
def cases(): return [json.loads(x) for x in (ROOT/'cases.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
def ctx(c):
 return {'case_id':c['case_id'],'mode':c['mode'],'source_text':c['source_text'],'revision_need':c['revision_need'],'protected_challenge':c['protected_challenge'],'content_units':[{'id':f'CU{i+1}','text':x} for i,x in enumerate(c['content_units'])],'protected_spans':c.get('protected_spans',[]),'adjacent_context':c.get('adjacent_context'),'authorized_scope':{'source_sha256':c['source_sha256'],'scope':'TARGET_PARAGRAPH_ONLY','immutable_adjacent_context':True},'length_policy':{'soft_min_ratio':.85,'soft_max_ratio':1.15},'required_output':{'status':'REVISE|KEEP|REVIEW','revised_paragraph':'string|null','content_unit_mapping':'array','protected_status':'array','uncertainty':'array'}}
def prompt(c,stage,plan=None):
 s=(ROOT/'prompts'/f'{stage}.md').read_text(encoding='utf-8')+'\n\nINPUT\n'+json.dumps(ctx(c),ensure_ascii=False,indent=2)
 if stage=='PLAN': s+='\n\nReturn JSON only: {"status":"PLAN|REVIEW","operations":[],"uncertainty":[]}'
 if stage=='REALIZE': s+='\n\nPLAN\n'+json.dumps(plan or {},ensure_ascii=False,indent=2)
 return s
def parse(raw):
 s=raw.strip()
 if s.startswith('~~~'): s=s.split('\n',1)[1].rsplit('~~~',1)[0].strip()
 if s.startswith('```'): s=s.split('\n',1)[1].rsplit('```',1)[0].strip()
 try: return json.loads(s)
 except Exception:
  a,b=s.find('{'),s.rfind('}')
  if a>=0 and b>a: return json.loads(s[a:b+1])
  raise
def infer(cli,model,p,maxn,seed):
 cmd=[str(cli),'-m',str(model),'--jinja','-cnv','--single-turn','--no-display-prompt','--temp','0','--seed',str(seed),'-c','4096','-n',str(maxn),'-p',p]
 t=time.time(); r=subprocess.run(cmd,capture_output=True,text=True,timeout=1200); dt=time.time()-t
 if r.returncode: raise RuntimeError('LLAMA_EXIT_'+str(r.returncode)+':'+r.stderr[-1200:])
 return r.stdout.strip(),{'elapsed_seconds':round(dt,3),'stderr_tail':r.stderr[-2000:]}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--llama-cli',required=True); ap.add_argument('--model-a',required=True); ap.add_argument('--model-b',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
 cfg=jread(ROOT/'config.json'); mm=jread(ROOT/'MODEL_MANIFEST.json'); cs=cases(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
 assert cfg['schema_version']=='2.1.0' and len(cs)==12 and len(mm['models'])==2 and cfg['live_slots']==48 and cfg['max_logical_calls']==72 and cfg['execution_concurrency']==1 and float(cfg['authorized_cost_ceiling'])==0
 paths={'MODEL_A':Path(a.model_a),'MODEL_B':Path(a.model_b)}
 for m in mm['models']:
  got=sha(paths[m['slot']]); assert got==m['artifact_sha256'],(m['slot'],got)
 rows=[{'slot_id':f"{m['slot']}-{c['case_id']}-{arm}",'model_slot':m['slot'],'case_id':c['case_id'],'arm':arm,'status':'NOT_RUN','logical_calls':0} for m in mm['models'] for c in cs for arm in ('DIRECT','PLANNED')]
 req=[]; resp=[]; calls=0; dumpjl(out/'slots.jsonl',rows)
 dump(out/'identity.json',{'config_sha256':sha(ROOT/'config.json'),'model_manifest_sha256':sha(ROOT/'MODEL_MANIFEST.json'),'cases_sha256':sha(ROOT/'cases.jsonl'),'model_artifacts':{m['slot']:m['artifact_sha256'] for m in mm['models']},'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID')})
 for m in mm['models']:
  mp=paths[m['slot']]
  for c in cs:
   for arm in ('DIRECT','PLANNED'):
    sid=f"{m['slot']}-{c['case_id']}-{arm}"; row=next(x for x in rows if x['slot_id']==sid)
    try:
     if arm=='DIRECT':
      stages=[('DIRECT',prompt(c,'DIRECT'),cfg['per_request_max_output_tokens']['DIRECT'])]
     else:
      pp=prompt(c,'PLAN'); raw,meta=infer(Path(a.llama_cli),mp,pp,cfg['per_request_max_output_tokens']['PLAN'],cfg['generation']['seed']); calls+=1; req.append({'slot_id':sid,'stage':'PLAN','prompt':pp}); resp.append({'slot_id':sid,'stage':'PLAN','raw':raw,'runtime':meta}); plan=parse(raw)
      if plan.get('status')!='PLAN': row.update(status='PLAN_REVIEW_OR_FAILED',logical_calls=1); dumpjl(out/'slots.jsonl',rows); dumpjl(out/'requests.jsonl',req); dumpjl(out/'responses.jsonl',resp); continue
      stages=[('REALIZE',prompt(c,'REALIZE',plan),cfg['per_request_max_output_tokens']['REALIZE'])]
     for st,p,mx in stages:
      raw,meta=infer(Path(a.llama_cli),mp,p,mx,cfg['generation']['seed']); calls+=1; req.append({'slot_id':sid,'stage':st,'prompt':p}); resp.append({'slot_id':sid,'stage':st,'raw':raw,'runtime':meta}); parse(raw)
     row.update(status='COMPLETE_RAW',logical_calls=1 if arm=='DIRECT' else 2)
    except Exception as e:
     row.update(status='FAILED',error=f'{type(e).__name__}:{e}',logical_calls=row.get('logical_calls',0))
     dumpjl(out/'slots.jsonl',rows); dumpjl(out/'requests.jsonl',req); dumpjl(out/'responses.jsonl',resp)
     if isinstance(e,(RuntimeError,subprocess.TimeoutExpired)): raise
    dumpjl(out/'slots.jsonl',rows); dumpjl(out/'requests.jsonl',req); dumpjl(out/'responses.jsonl',resp)
    if calls>cfg['max_logical_calls']: raise RuntimeError('CALL_CEILING')
 dump(out/'backend_summary.json',{'logical_calls':calls,'slots':48,'complete_raw':sum(x['status']=='COMPLETE_RAW' for x in rows),'failed':sum(x['status']=='FAILED' for x in rows),'plan_review_or_failed':sum(x['status']=='PLAN_REVIEW_OR_FAILED' for x in rows),'additional_monetary_cost_usd':0.0})
 print((out/'backend_summary.json').read_text())
if __name__=='__main__': main()
