"""Score consumed QALB15 evidence with frozen fine-tuned external CAD model. No labels here."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np,torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cad_qalb14_data_common import target_window

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
MODEL=ROOT/"artifacts/cad_model/CAD_FINETUNED_MODEL"; SUMMARY=ROOT/"artifacts/cad_model/PHASE2_CAD_FINETUNED_TRAINING_SUMMARY.json"
THIRD=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"; THIRD_A=ROOT/"artifacts/third_arabart/VAL_ARABART_Q14_EVENTS.jsonl"
OLD=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"; OLD_A=ROOT/"artifacts/old_arabart/TRI_ARABART_Q14_EVENTS.jsonl"
OUT=ROOT/"PHASE2_CAD_FINETUNED_CONSUMED_FEATURES.jsonl"; RUNTIME=ROOT/"PHASE2_CAD_FINETUNED_CONSUMED_RUNTIME.json"

def jl(p):return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def fsha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def lines(p):return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def emap(path,wanted):
 out={}
 for e in jl(path):
  sp=e.get("source_lexical_span") or [-1,-1]
  if e.get("primitive_ops")==["SUB"] and len(e.get("source_bases") or [])==1 and len(e.get("output_bases") or [])==1:
   k=(int(e["line_id"]),tuple(map(int,sp)),e["source_hash"],e["output_hash"])
   if k in wanted:out[k]=e
 return out

def items():
 third=[x for x in jl(THIRD) if x["runtime_decision"]=="PASS"];assert len(third)==14
 tk={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in third};te=emap(THIRD_A,tk);assert len(te)==14
 guard=jl(OLD);old=[x for x in guard if x["runtime_decisions"]["ORTHO_MORPH_COMMON_NOUN_V1"]=="PASS"];strict={x["vote_id"] for x in guard if x["runtime_decisions"]["ORTHO_ISOLATED_COMMON_NOUN_V1"]=="PASS"}
 assert len(old)==36 and len(strict)==19
 ok={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in old};oe=emap(OLD_A,ok);assert len(oe)==36
 out=[]
 for pop,recs,evs,ss in [("THIRD_V1_14",tk,te,set()),("EARLIER_ORTHO_MORPH_36",ok,oe,strict)]:
  for k,f in sorted(recs.items()):out.append((pop,f,evs[k],f["vote_id"] in ss))
 return out

def main():
 s=json.loads(SUMMARY.read_text(encoding="utf-8"));assert s["external_feasibility_criterion_met"] is True
 tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,use_fast=True);model=AutoModelForSequenceClassification.from_pretrained(MODEL,local_files_only=True).eval().cpu()
 threshold=float(s["acceptance_threshold"]);raw=lines(RAW);rows=[]
 with torch.no_grad():
  for pop,f,e,strict in items():
   text=raw[int(f["line_id"])-1];ws=text.split();wi=int(units(text)[int(f["source_lexical_span"][0])]["whitespace_word_index"])
   src=(e.get("source_surfaces") or [None])[0];cand=(e.get("output_surfaces") or [None])[0];assert ws[wi]==src
   cw=list(ws);cw[wi]=cand;sw=target_window(ws,wi);tw=target_window(cw,wi)
   enc=tok(sw,tw,truncation=True,max_length=96,return_tensors="pt")
   p=float(torch.softmax(model(**enc).logits,dim=-1)[0,1])
   rows.append({"population":pop,"vote_id":f["vote_id"],"line_id":int(f["line_id"]),"line_hash":f["line_hash"],"source_lexical_span":f["source_lexical_span"],"source_hash":f["source_hash"],"output_hash":f["output_hash"],"strict_v1_member":bool(strict),"source_window_hash":sha(sw),"candidate_window_hash":sha(tw),"accept_probability":p,"runtime_decision":"PASS" if p>=threshold else "REVIEW"})
 OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
 counts={}
 for pop in sorted({x["population"] for x in rows}):
  pr=[x for x in rows if x["population"]==pop];counts[pop]={"rows":len(pr),"pass":sum(x["runtime_decision"]=="PASS" for x in pr),"review":sum(x["runtime_decision"]=="REVIEW" for x in pr),"strict_v1_rows":sum(x["strict_v1_member"] for x in pr),"strict_v1_pass":sum(x["strict_v1_member"] and x["runtime_decision"]=="PASS" for x in pr)}
 rt={"status":"PHASE2_CAD_FINETUNED_CONSUMED_FEATURES_FROZEN","external_model_frozen":True,"current_labels_read":False,"qalb15_corrected_read":False,"qalb15_test_read":False,"qalb_text_persisted":False,"acceptance_threshold":threshold,"rows":len(rows),"population_counts":counts,"features_sha256":fsha(OUT)}
 RUNTIME.write_text(json.dumps(rt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");assert not any("\u0600"<=c<="\u06ff" for c in (OUT.read_text(encoding="utf-8")+RUNTIME.read_text(encoding="utf-8")))
 print(json.dumps(rt,ensure_ascii=False))
if __name__=="__main__":main()
