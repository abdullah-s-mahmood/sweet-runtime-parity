"""Analyze selective gate with existing DEVELOPMENT edit adjudication.

No new linguistic labels are created. This is retrospective development
measurement only; new selective outputs still require Work adjudication.
"""
import collections,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]; ART=ROOT/"artifacts"
ADJ=ROOT/"PHASE2_SURGICAL_APPLIED_EDIT_ADJUDICATION.jsonl"


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def quality(rows):
    c=collections.Counter(x["classification"] for x in rows)
    s=c["SUPPORTED_CORRECTION"]+c["SUPPORTED_ALTERNATIVE"]
    return {"edits":len(rows),"supported":s,"wrong":c["WRONG_CORRECTION"],"partial":c["PARTIAL_CORRECTION"],"unnecessary":c["UNNECESSARY_EDIT"],"review_required":c["REVIEW_REQUIRED"],"supported_precision":s/len(rows) if rows else None,"classes":dict(c)}


def burden(rows,pids):
    by=collections.defaultdict(list)
    for x in rows: by[int(x["passage_id"])].append(x)
    c=collections.Counter(); detail=[]
    for pid in pids:
        cls={x["classification"] for x in by.get(pid,[])}
        if not cls: st="UNCHANGED"
        elif "WRONG_CORRECTION" in cls: st="REJECT"
        elif cls & {"PARTIAL_CORRECTION","UNNECESSARY_EDIT","REVIEW_REQUIRED"}: st="REVIEW_REQUIRED"
        else: st="AUTO_ACCEPT_CANDIDATE"
        c[st]+=1; detail.append({"passage_id":pid,"status":st,"classes":sorted(cls),"retained_edits":len(by.get(pid,[]))})
    return {"counts":dict(c),"passages":detail}


def main():
    raw=json.loads((ART/"SELECTIVE_SURGICAL_GATE_RAW.json").read_text(encoding="utf-8"))
    ged=json.loads((ART/"SELECTIVE_GED_LOCALIZATION.json").read_text(encoding="utf-8"))
    adj=read_jsonl(ADJ)
    amap={(int(x["passage_id"]),int(x["edit_index"])):x for x in adj}
    pids=sorted(int(x) for x in raw["passages"])
    variants={}
    names=list(raw["variant_summaries"])
    for name in names:
        retained=[]; missing=[]
        for pid_s,p in raw["passages"].items():
            pid=int(pid_s)
            for ei in p["gate_meta"][name]["applied_indices"]:
                a=amap.get((pid,int(ei)))
                if a is None: missing.append({"passage_id":pid,"edit_index":ei})
                else: retained.append(a)
        q=quality(retained)
        q["burden_proxy"]=burden(retained,pids)
        q["missing_adjudication_keys"]=missing
        q["automated_exact_target_recovery"]=raw["variant_summaries"][name]["exact_target_recoveries"]
        q["automated_exact_target_recovery_rate"]=raw["variant_summaries"][name]["exact_target_recovery_rate"]
        q["changed_passages"]=raw["variant_summaries"][name]["changed_passages"]
        variants[name]=q

    # How GED partitions the already operation-approved candidates.
    base=[]
    for pid_s,p in raw["passages"].items():
        pid=int(pid_s)
        allowed=set(p["gate_meta"]["op_aware"]["applied_indices"])
        for e in p["baseline_candidate_edits"]:
            if int(e["edit_index"]) not in allowed: continue
            a=amap[(pid,int(e["edit_index"]))]
            base.append({**a,"zaebuc_error":e["ged"]["zaebuc"]["is_error"],"qalb14_error":e["ged"]["qalb14"]["is_error"]})
    parts={
        "zaebuc_non_uc":quality([x for x in base if x["zaebuc_error"]]),
        "zaebuc_uc":quality([x for x in base if not x["zaebuc_error"]]),
        "qalb14_non_uc":quality([x for x in base if x["qalb14_error"]]),
        "qalb14_uc":quality([x for x in base if not x["qalb14_error"]]),
        "ged_union":quality([x for x in base if x["zaebuc_error"] or x["qalb14_error"]]),
        "ged_intersection":quality([x for x in base if x["zaebuc_error"] and x["qalb14_error"]]),
    }

    result={
        "status":"DEVELOPMENT_SELECTIVE_GATE_ANALYSIS",
        "not_sealed":True,
        "label_source":"Existing same-agent surgical edit adjudication; no new linguistic labels.",
        "variants":variants,
        "ged_partition_of_operation_aware_candidates":parts,
        "ged_localization_summary":ged["summary"],
        "scientific_stress_summary":raw["scientific_stress_summary"],
        "rules":[
            "Automated exact target recovery is diagnostic, not final target quality.",
            "Burden is a proxy from prior edit labels; Work must adjudicate new outputs before freeze.",
            "GED non-target predictions are not counted as false positives because Nahw local targets are not exhaustive.",
            "No selective policy is frozen from this development run."
        ]
    }
    p=ART/"SELECTIVE_GATE_ANALYSIS.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"selective_gate_analysis":{k:{"edits":v["edits"],"supported":v["supported"],"wrong":v["wrong"],"partial":v["partial"],"unnecessary":v["unnecessary"],"precision":v["supported_precision"],"exact_target_recovery":v["automated_exact_target_recovery"],"changed_passages":v["changed_passages"],"burden":v["burden_proxy"]["counts"]} for k,v in variants.items()},"ged_localization":ged["summary"]},ensure_ascii=False))


if __name__=="__main__":
    main()
