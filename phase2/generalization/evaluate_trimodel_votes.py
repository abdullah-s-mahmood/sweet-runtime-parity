"""Evaluate frozen tri-model votes against QALB15 TRAIN gold. Persist hash/ID only."""
from __future__ import annotations
import json
from pathlib import Path
from phase2.generalization.cross_model_common import read_jsonl,read_nonempty_lines,sha_text
from phase2.arabart_audit.build_full_arabart_edit_queue import align,group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
COR=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.cor.no_ids"
FEATURES=ROOT/"artifacts"/"TRIMODEL_VOTE_FEATURES.jsonl"
RUNTIME=ROOT/"artifacts"/"TRIMODEL_VOTE_RUNTIME.json"
OUT=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"

def gold_events(src,cor):
  ops,_=align(src,cor); out=[]
  for g in group_nonkeep(ops):
    ss=[x["src"] for x in g if x["src"]]; oo=[x["out"] for x in g if x["out"]]
    if ss:
      lex=[x["lexical_index"] for x in ss]; span=[min(lex),max(lex)+1]
    else:span=[-1,-1]
    out.append({"span":span,"source":[x["base"] for x in ss],"gold":[x["base"] for x in oo]})
  return out

def overlap(a,b):return a[0]>=0 and b[0]>=0 and max(a[0],b[0])<min(a[1],b[1])

def classify(ev,gold):
  exact=[g for g in gold if g["span"]==ev["source_lexical_span"]]
  for g in exact:
    if g["gold"]==ev["output_bases"]:return "EXACT_GOLD_SUPPORTED",g
  if exact:return "SAME_GOLD_SPAN_DIFFERENT_OUTPUT",exact[0]
  ovs=[g for g in gold if overlap(g["span"],ev["source_lexical_span"])]
  if ovs:return "GOLD_OVERLAP_NONEXACT_SPAN",ovs[0]
  return "NO_GOLD_EDIT_OVERLAP",None

def main():
  rt=json.loads(RUNTIME.read_text(encoding="utf-8")); assert rt["gold_read"] is False
  votes=read_jsonl(FEATURES)
  raw=read_nonempty_lines(RAW); cor=read_nonempty_lines(COR); assert len(raw)==len(cor)
  gold={i:gold_events(raw[i-1],cor[i-1]) for i in rt["selected_line_ids"]}
  policies={"UNANIMOUS_3":"ACCEPT","ARABART_PLUS_ANY_SWEET":"ACCEPT","BOTH_SWEETS":"DIAGNOSTIC"}
  res={}
  for p,decision in policies.items():
    acc=[x for x in votes if x["runtime_decisions"][p]==decision]
    counts={}; audit=[]
    for x in acc:
      cls,g=classify(x,gold[x["line_id"]]); counts[cls]=counts.get(cls,0)+1
      audit.append({
       "vote_id":x["vote_id"],"line_id":x["line_id"],"line_hash":x["line_hash"],
       "source_lexical_span":x["source_lexical_span"],"source_hash":x["source_hash"],"output_hash":x["output_hash"],
       "classification":cls,
       "gold_source_hash":sha_text("\u241f".join(g["source"])) if g else None,
       "gold_output_hash":sha_text("\u241f".join(g["gold"])) if g else None,
      })
    res[p]={"candidate_events":len(acc),"classification_counts":counts,
            "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
            "needs_contextual_review":len(acc)-counts.get("EXACT_GOLD_SUPPORTED",0),
            "event_audit_hashes":audit}
  obj={"status":"PHASE2_TRIMODEL_VOTING_GOLD_COMPARED","runtime_votes_frozen_before_gold":True,
       "population":"fresh QALB15 L2 TRAIN 50-line slice excluding prior 50","policy_results":res,
       "qalb15_test_read":False,"qalb_text_persisted":False}
  OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  dumped=OUT.read_text(encoding="utf-8")
  assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
  print(json.dumps({k:({pk:{kk:vv for kk,vv in pv.items() if kk!="event_audit_hashes"} for pk,pv in v.items()} if k=="policy_results" else v) for k,v in obj.items()},ensure_ascii=False))
if __name__=="__main__":main()
