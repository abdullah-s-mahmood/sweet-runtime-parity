"""Compare frozen fresh validation PASS decisions to QALB15 TRAIN gold."""
from __future__ import annotations
import json
from pathlib import Path
from phase2.generalization.cross_model_common import read_jsonl,read_nonempty_lines,sha_text
from phase2.arabart_audit.build_full_arabart_edit_queue import align,group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
COR=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.cor.no_ids"
VOTES=ROOT/"artifacts"/"ORTHO_VALIDATION_VOTE_FEATURES.jsonl"
FEATURES=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_RUNTIME.json"
OUT=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_RESULTS.json"

def gold_events(src,cor):
    ops,_=align(src,cor);out=[]
    for g in group_nonkeep(ops):
        ss=[x["src"] for x in g if x["src"]];oo=[x["out"] for x in g if x["out"]]
        if ss:
            lex=[x["lexical_index"] for x in ss];span=[min(lex),max(lex)+1]
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
    rt=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert rt["labels_or_gold_read"] is False and rt["rule_frozen_before_labels"] is True

    safe={x["vote_id"]:x for x in read_jsonl(FEATURES)}
    vote={x["vote_id"]:x for x in read_jsonl(VOTES)}
    pass_ids=[vid for vid,x in safe.items() if x["runtime_decision"]=="PASS"]

    raw=read_nonempty_lines(RAW);cor=read_nonempty_lines(COR);assert len(raw)==len(cor)
    line_ids=sorted({vote[vid]["line_id"] for vid in pass_ids})
    gold={i:gold_events(raw[i-1],cor[i-1]) for i in line_ids}

    counts={};audit=[]
    for vid in pass_ids:
        ev=vote[vid]
        cls,g=classify(ev,gold[ev["line_id"]]);counts[cls]=counts.get(cls,0)+1
        audit.append({
          "vote_id":vid,"line_id":ev["line_id"],"line_hash":ev["line_hash"],
          "source_lexical_span":ev["source_lexical_span"],
          "source_hash":ev["source_hash"],"output_hash":ev["output_hash"],
          "classification":cls,
          "gold_source_hash":sha_text("\u241f".join(g["source"])) if g else None,
          "gold_output_hash":sha_text("\u241f".join(g["gold"])) if g else None,
        })

    obj={
      "status":"PHASE2_ORTHO_ISOLATED_FRESH_GOLD_COMPARED",
      "runtime_rule_frozen_before_gold":True,
      "population":"third disjoint QALB15 L2 TRAIN 50-line slice",
      "rule_version":"ORTHO_ISOLATED_COMMON_NOUN_V1",
      "pass_events":len(pass_ids),
      "classification_counts":counts,
      "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
      "needs_contextual_review":len(pass_ids)-counts.get("EXACT_GOLD_SUPPORTED",0),
      "event_audit_hashes":audit,
      "final_promotion_decision":"PENDING_CONTEXTUAL_REVIEW" if len(pass_ids)-counts.get("EXACT_GOLD_SUPPORTED",0)>0 else (
        "PASS_FRESH_VALIDATION" if len(pass_ids)>=10 else "UNPROVEN_LOW_COVERAGE"
      ),
      "independent_human_validation":False,
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8");assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
