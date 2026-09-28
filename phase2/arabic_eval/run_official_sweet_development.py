"""Run ONLY in the established official PyTorch/Transformers environment.
No network/model download. Input is a development-only JSONL and local weight folders.
"""
import argparse,json,time,hashlib,resource,sys,platform,subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ART=ROOT/'artifacts'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--nopnx',type=Path,default=ROOT/'models/nopnx');ap.add_argument('--pnx',type=Path,default=ROOT/'models/pnx');ap.add_argument('--gec-repo',type=Path,default=ROOT/'upstream/text-editing');ap.add_argument('--input',type=Path,default=HERE/'DEVELOPMENT_TARGETS.jsonl');ap.add_argument('--stress-input',type=Path,default=HERE/'SCIENTIFIC_STRESS_CASES.jsonl');ap.add_argument('--output',type=Path,default=ART/'OFFICIAL_DEVELOPMENT_RAW.jsonl');args=ap.parse_args()
 ART.mkdir(parents=True,exist_ok=True)
 git_commit=subprocess.check_output(['git','-C',str(args.gec_repo),'rev-parse','HEAD'],text=True).strip()
 assert git_commit=='4d552ca3ae98029550f27fc52aa1b22883e16e61',('CAMeL source commit mismatch',git_commit)
 pins={'nopnx':'584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6','pnx':'195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3'}
 for name in pins:
  folder=getattr(args,name)
  assert all((folder/x).is_file() for x in ('pytorch_model.bin','config.json','vocab.txt','tokenizer_config.json','special_tokens_map.json')),(name,'missing local model file')
  assert sha(folder/'pytorch_model.bin')==pins[name],(name,'weight hash mismatch')
 sys.path.insert(0,str(args.gec_repo.resolve()))
 import torch,transformers
 from transformers import BertTokenizer,BertForTokenClassification
 from gec.tag import rewrite
 assert platform.python_version().startswith('3.10.'),f'Expected established Python 3.10; got {platform.python_version()}'
 assert torch.__version__.startswith('1.12.1'),torch.__version__
 assert transformers.__version__=='4.30.0',transformers.__version__
 models={}
 for name in ('nopnx','pnx'):
  folder=getattr(args,name)
  tok=BertTokenizer.from_pretrained(str(folder),local_files_only=True)
  model=BertForTokenClassification.from_pretrained(str(folder),local_files_only=True).eval().cpu()
  assert model.classifier.weight.shape[0]==len(model.config.id2label)
  models[name]=(tok,model)
 def once(text,name):
  tok,model=models[name];words=text.split();start=time.perf_counter()
  encoded=tok(words,return_tensors='pt',is_split_into_words=True)
  with torch.no_grad():logits=model(**encoded).logits[0];probs=torch.softmax(logits,dim=-1);maxprob,labels=probs.max(-1)
  ids=encoded['input_ids'][0].tolist();subwords=tok.convert_ids_to_tokens(ids[1:-1]);raw=[model.config.id2label[int(v)] for v in labels[1:-1]]
  assert len(raw)==len(subwords)
  result=rewrite(subwords=[subwords],edits=[raw]);output=result[0][0]
  return {'input':text,'subwords':subwords,'input_ids':ids,'raw_labels':raw,'raw_label_ids':labels[1:-1].tolist(),'top1_confidence':maxprob[1:-1].tolist(),'output':output,'rewrite_non_applicable':result[2],'elapsed_seconds':time.perf_counter()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 records=[json.loads(l) for l in args.input.read_text().splitlines() if l.strip()]
 assert len(records)==150 and len({x['passage_id'] for x in records})==41
 assert len({x['target_id'] for x in records})==150 and all(x['case_id'].startswith('NAHW-DEV-') for x in records)
 cache={}
 def stages(src):
  if src not in cache:
   n1=once(src,'nopnx');n2=once(n1['output'],'nopnx');p_only=once(src,'pnx');p_full=once(n2['output'],'pnx')
   cache[src]=(n1,n2,p_only,p_full)
  return cache[src]
 temp=args.output.with_suffix(args.output.suffix+'.tmp')
 with temp.open('w') as f:
  for rec in records:
   src=rec['source'];reused=src in cache;n1,n2,p_only,p_full=stages(src)
   row={'case_id':rec['case_id'],'target_id':rec['target_id'],'source':src,'reference':rec['reference'],'target_start':rec['target_start'],'target_end':rec['target_end'],'target_error':rec['target_error'],'target_correction':rec['target_correction'],'passage_id':rec['passage_id'],'category_hint':rec['category_hint'],'provenance':{'publication_source':rec['publication_source'],'source_url':rec['source_url'],'doi':rec['doi'],'license_or_usage_basis':rec['license_or_usage_basis'],'human_vs_synthetic':rec['human_vs_synthetic']},'nopnx_iteration_1':n1,'nopnx_iteration_2':n2,'pnx_only':p_only,'full_pnx_iteration_1':p_full,'passage_inference_reused':reused,'baselines':{'input_no_correction':src},'runtime':{'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,'execution':'OFFICIAL_PYTORCH_RUNTIME','rewrite':'gec.tag.rewrite','local_weights':pins,'gec_commit':git_commit,'gec_tag_sha256':sha(args.gec_repo/'gec/tag.py')}}
   f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush()
 temp.replace(args.output)
 stress=[json.loads(l) for l in args.stress_input.read_text().splitlines() if l.strip()]
 assert len(stress)==12 and all(x['human_gold_status']=='NON_HUMAN_GOLD' for x in stress)
 with (ART/'OFFICIAL_SCIENTIFIC_STRESS_RAW.jsonl').open('w') as f:
  for rec in stress:
   n1,n2,p_only,p_full=stages(rec['source'])
   f.write(json.dumps({'case_id':rec['case_id'],'source':rec['source'],'human_gold_status':'NON_HUMAN_GOLD','protected':rec['protected'],'category':rec['category'],'nopnx_iteration_1':n1,'nopnx_iteration_2':n2,'pnx_only':p_only,'full_pnx_iteration_1':p_full},ensure_ascii=False)+'\n')
 manifest={'status':'COMPLETE','target_count':len(records),'unique_passage_count':len({x['passage_id'] for x in records}),'scientific_stress_count':len(stress),'runtime':{'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,'gec_commit':git_commit},'model_sha256':pins,'input_sha256':sha(args.input),'stress_input_sha256':sha(args.stress_input),'raw_sha256':sha(args.output),'stress_raw_sha256':sha(ART/'OFFICIAL_SCIENTIFIC_STRESS_RAW.jsonl')}
 (ART/'OFFICIAL_DEVELOPMENT_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (ART/'OFFICIAL_DEVELOPMENT_RUN_LOG.txt').write_text(f"Official development run complete: {len(records)} targets in 41 passage groups; 12 NON_HUMAN_GOLD stress cases.\nPython {platform.python_version()}, torch {torch.__version__}, transformers {transformers.__version__}, CAMeL {git_commit}.\nRaw SHA-256 {manifest['raw_sha256']}\n")
 print(json.dumps({'completed':len(records),'output':str(args.output),'sha256':sha(args.output),'official_runtime':True}))
if __name__=='__main__':main()
