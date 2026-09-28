"""Evaluate already-materialized AraBART reverse acceptance decisions.

This script is allowed to read development adjudication labels ONLY after
runtime decisions exist. It never changes runtime decisions.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_ARABART_REVERSE_ACCEPTANCE_FEATURES.jsonl"
LABELS=ROOT/"PHASE2_ARABART_EDIT_ADJUDICATION.jsonl"
OUT=ROOT/"PHASE2_ARABART_REVERSE_ACCEPTANCE_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def supported(c):
    return c in ("SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE")

def summarize(rows,policy):
    acc=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT"]
    rev=[x for x in rows if x["runtime_decisions"][policy]=="REVIEW"]
    rej=[x for x in rows if x["runtime_decisions"][policy]=="REJECT"]
    classes={}
    for x in acc:
        c=x["label"]["event_class"]; classes[c]=classes.get(c,0)+1
    supp=sum(supported(x["label"]["event_class"]) for x in acc)
    total_supported=sum(supported(x["label"]["event_class"]) for x in rows)
    wrong=sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in acc)
    partial=sum(x["label"]["event_class"]=="PARTIAL_CORRECTION" for x in acc)
    high_wrong=sum(x["label"]["event_class"]=="WRONG_CORRECTION" and x["label"]["severity"] in ("HIGH","CRITICAL") for x in acc)
    rejected_wrong=sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in rej)
    total_wrong=sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in rows)
    return {
        "policy":policy,
        "accepted":len(acc),"review":len(rev),"rejected":len(rej),
        "accepted_classes":classes,
        "accepted_supported":supp,
        "accepted_wrong":wrong,
        "accepted_partial":partial,
        "accepted_high_or_critical_wrong":high_wrong,
        "supported_precision":supp/len(acc) if acc else None,
        "supported_coverage_within_arabart_only":supp/total_supported if total_supported else None,
        "wrong_rejection_recall":rejected_wrong/total_wrong if total_wrong else None,
        "accepted_ids":[x["arabart_edit_id"] for x in acc],
    }

def main():
    feats=jl(FEATURES)
    labels_raw=jl(LABELS)
    lm={x["arabart_edit_id"]:{
        "event_class":x["pass2"]["event_class"],
        "severity":x["pass2"]["severity"],
    } for x in labels_raw}
    assert len(feats)==67 and len(lm)==67
    rows=[]
    for x in feats:
        y=dict(x); y["label"]=lm[x["arabart_edit_id"]]; rows.append(y)

    policies=list(rows[0]["runtime_decisions"])
    results={p:summarize(rows,p) for p in policies}
    hard=[x for x in rows if x["features"]["hard_vetoes"]]
    structural=[x for x in rows if x["features"]["structural_positive"] and not x["features"]["hard_vetoes"] and not x["features"]["complex_event_member"] and x["features"]["alignment_cost"]<=0.25]

    result={
        "status":"PHASE2_ARABART_REVERSE_ACCEPTANCE_DEVELOPMENT_EVALUATED",
        "runtime_decisions_materialized_before_labels":True,
        "rows":67,
        "supported_rows":sum(supported(x["label"]["event_class"]) for x in rows),
        "wrong_rows":sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in rows),
        "policy_results":results,
        "feature_diagnostics":{
            "hard_veto_rows":len(hard),
            "hard_veto_wrong":sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in hard),
            "hard_veto_supported":sum(supported(x["label"]["event_class"]) for x in hard),
            "structural_eligible_rows":len(structural),
            "structural_eligible_supported":sum(supported(x["label"]["event_class"]) for x in structural),
            "structural_eligible_wrong":sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in structural),
        },
        "cross_stream_development_comparator":{
            "existing_exact_local_agreement_accepts_supported":23,
            "existing_exact_local_agreement_accepted_wrong":0,
            "arabart_only_structural_typed_accepts_supported":results["STRUCTURAL_TYPED"]["accepted_supported"],
            "arabart_only_structural_typed_accepted_wrong":results["STRUCTURAL_TYPED"]["accepted_wrong"],
            "note":"The 67 AraBART-only rows were defined as new local locations outside the existing 79-candidate population, so accepted supported rows here are incremental at the recorded local locations. This is still repeatedly inspected development evidence."
        },
        "limitations":[
            "All quality labels are same-agent development adjudication, not sealed or independent-human evidence.",
            "The typed rules were motivated by this development population and therefore require disjoint validation before freezing.",
            "Candidate rows are clustered by passage; candidate-level precision must not be interpreted as independent Bernoulli trials.",
            "This gate covers the 67 new one-to-one AraBART substitutions; complete multiword events remain governed by the full-event audit."
        ]
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
