"""Analyze Phase 2 Selective Surgical Gate using existing DEVELOPMENT adjudication.

No new linguistic labels are created here. Existing surgical edit adjudication is
joined only to measure which previously adjudicated edits each runtime policy
would retain. New outputs still require Work adjudication before freeze.
"""
from __future__ import annotations
import collections, json, random
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ART=ROOT/"artifacts"
ADJ=ROOT/"PHASE2_SURGICAL_APPLIED_EDIT_ADJUDICATION.jsonl"


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def quality(rows):
    counts=collections.Counter(x["classification"] for x in rows)
    supported=counts["SUPPORTED_CORRECTION"]+counts["SUPPORTED_ALTERNATIVE"]
    return {
        "edits":len(rows),
        "supported":supported,
        "wrong":counts["WRONG_CORRECTION"],
        "partial":counts["PARTIAL_CORRECTION"],
        "unnecessary":counts["UNNECESSARY_EDIT"],
        "review_required":counts["REVIEW_REQUIRED"],
        "supported_precision":supported/len(rows) if rows else None,
        "classes":dict(counts),
    }


def burden(selected, passages_all):
    by=collections.defaultdict(list)
    for x in selected:
        by[x["passage_id"]].append(x)
    counts=collections.Counter()
    detail=[]
    for pid in passages_all:
        rs=by.get(pid,[])
        classes={x["classification"] for x in rs}
        if not rs:
            status="UNCHANGED"
        elif "WRONG_CORRECTION" in classes:
            status="REJECT"
        elif classes & {"PARTIAL_CORRECTION","UNNECESSARY_EDIT","REVIEW_REQUIRED"}:
            status="REVIEW_REQUIRED"
        else:
            status="AUTO_ACCEPT_CANDIDATE"
        counts[status]+=1
        detail.append({"passage_id":pid,"status":status,"retained_edits":len(rs),"classes":sorted(classes)})
    return {"counts":dict(counts),"passages":detail}


def main():
    raw=json.loads((ART/"SELECTIVE_SURGICAL_GATE_RAW.json").read_text(encoding="utf-8"))
    adj=read_jsonl(ADJ)
    adjmap={(int(x["passage_id"]),int(x["edit_index"])):x for x in adj}
    passages=sorted(int(x) for x in raw["passages"].keys())

    variants={}
    # Operation-aware membership is stored by explicit selected list.
    selectors={"op_aware":lambda p,eidx,e: eidx in p["operation_aware_selected_indices"]}
    for name in ("op_aware_ged_non_uc","op_aware_ged_p30","op_aware_ged_p50","op_aware_ged_p70"):
        selectors[name]=lambda p,eidx,e,n=name: bool(e["ged_gate_membership"].get(n,False))

    for name,select in selectors.items():
        retained=[]
        missing=[]
        for pid_s,p in raw["passages"].items():
            pid=int(pid_s)
            for e in p["baseline_candidate_edits"]:
                ei=int(e["edit_index"])
                if not select(p,ei,e):
                    continue
                a=adjmap.get((pid,ei))
                if a is None:
                    missing.append({"passage_id":pid,"edit_index":ei})
                    continue
                retained.append(a)
        q=quality(retained)
        q["burden_proxy"]=burden(retained,passages)
        q["missing_adjudication_keys"]=missing
        q["automated_exact_target_recovery"]=raw["variant_summaries"][name]["exact_target_recoveries"]
        q["automated_exact_target_recovery_rate"]=raw["variant_summaries"][name]["exact_target_recovery_rate"]
        q["changed_passages"]=raw["variant_summaries"][name]["changed_passages"]
        variants[name]=q

    # GED enrichment among the runtime operation-aware candidates only.
    op_candidates=[]
    for pid_s,p in raw["passages"].items():
        pid=int(pid_s)
        for e in p["baseline_candidate_edits"]:
            if int(e["edit_index"]) not in p["operation_aware_selected_indices"]:
                continue
            a=adjmap[(pid,int(e["edit_index"]))]
            op_candidates.append({
                **a,
                "ged_top_label":e["ged"]["ged_top_label"],
                "ged_error_probability":e["ged"]["ged_error_probability"],
            })

    ged_groups={}
    predicates={
        "GED_TOP_NON_UC":lambda x:x["ged_top_label"]!="UC",
        "GED_TOP_UC":lambda x:x["ged_top_label"]=="UC",
        "GED_P_GE_0_30":lambda x:x["ged_error_probability"]>=0.30,
        "GED_P_GE_0_50":lambda x:x["ged_error_probability"]>=0.50,
        "GED_P_GE_0_70":lambda x:x["ged_error_probability"]>=0.70,
    }
    for name,pred in predicates.items():
        ged_groups[name]=quality([x for x in op_candidates if pred(x)])

    result={
        "status":"DEVELOPMENT_SELECTIVE_GATE_ANALYSIS",
        "not_sealed":True,
        "label_source":"Existing same-agent surgical adjudication only; no new linguistic adjudication in this script.",
        "variants":variants,
        "ged_enrichment_on_operation_aware_candidates":ged_groups,
        "ged_published_target_localization":raw["ged_published_target_localization"],
        "scientific_stress_summary":raw["scientific_stress_summary"],
        "interpretation_rules":[
            "Automated exact target recovery is diagnostic and not final quality.",
            "Passage burden is a proxy derived from prior per-edit adjudication, not independent review of new selective outputs.",
            "GED non-target predictions are not false positives because Nahw target extraction is not exhaustive.",
            "No threshold or GED rule may be frozen from this same development set."
        ]
    }
    p=ART/"SELECTIVE_GATE_ANALYSIS.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "selective_gate_analysis":{
            k:{
                "edits":v["edits"],
                "supported":v["supported"],
                "wrong":v["wrong"],
                "partial":v["partial"],
                "unnecessary":v["unnecessary"],
                "supported_precision":v["supported_precision"],
                "exact_target_recovery":v["automated_exact_target_recovery"],
                "changed_passages":v["changed_passages"],
                "burden":v["burden_proxy"]["counts"],
            } for k,v in variants.items()
        },
        "ged_enrichment":ged_groups
    },ensure_ascii=False))


if __name__=="__main__":
    main()
