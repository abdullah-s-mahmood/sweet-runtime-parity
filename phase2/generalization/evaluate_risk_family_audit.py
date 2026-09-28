"""Evaluate frozen risk-family assignments using prior hash-only adjudication."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEAT=ROOT/"artifacts"/"RISK_FAMILY_FEATURES.jsonl"
MAN=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_MANUAL_REVIEW.json"
RESULT=ROOT/"PHASE2_RISK_FAMILY_AUDIT_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rows=jl(FEAT)
    man=json.loads(MAN.read_text(encoding="utf-8"))
    manual={x["agreement_id"]:x for x in man["items"]}
    labels={}
    for r in rows:
        x=manual.get(r["agreement_id"])
        labels[r["agreement_id"]]=(
            {"class":x["manual_class"],"severity":x["severity"]}
            if x else {"class":"SUPPORTED_CORRECTION","severity":"LOW"}
        )

    fams={}
    for r in rows:
        f=r["risk_family"]
        d=fams.setdefault(f,{
            "total":0,"SUPPORTED_CORRECTION":0,"SUPPORTED_ALTERNATIVE":0,
            "WRONG_CORRECTION":0,"PARTIAL_CORRECTION":0,"UNNECESSARY_EDIT":0,
            "high_or_critical_wrong":0
        })
        d["total"]+=1
        lab=labels[r["agreement_id"]]
        d[lab["class"]]=d.get(lab["class"],0)+1
        if lab["class"]=="WRONG_CORRECTION" and lab["severity"] in ("HIGH","CRITICAL"):
            d["high_or_critical_wrong"]+=1

    candidates=[]
    for f,d in fams.items():
        supported=d["SUPPORTED_CORRECTION"]+d["SUPPORTED_ALTERNATIVE"]
        unsafe=d["WRONG_CORRECTION"]+d["PARTIAL_CORRECTION"]+d["UNNECESSARY_EDIT"]
        d["supported"]=supported
        d["unsafe"]=unsafe
        d["supported_precision"]=supported/d["total"] if d["total"] else None
        d["candidate_for_fresh_validation"]=bool(
            d["total"]>=10 and
            d["WRONG_CORRECTION"]==0 and
            d["PARTIAL_CORRECTION"]==0 and
            d["UNNECESSARY_EDIT"]==0
        )
        if d["candidate_for_fresh_validation"]:candidates.append(f)

    result={
        "status":"PHASE2_RISK_FAMILY_AUDIT_EVALUATED",
        "exploratory_only":True,
        "runtime_families_materialized_before_labels_loaded":True,
        "rows":len(rows),
        "pre_registered_min_family_size":10,
        "family_results":dict(sorted(fams.items())),
        "candidate_families_for_fresh_validation":sorted(candidates),
        "promotion_rule":"No family is promoted from this consumed slice. Candidate families, if any, must be frozen and evaluated unchanged on fresh disjoint evidence.",
        "qalb15_test_read":False,
    }
    RESULT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
