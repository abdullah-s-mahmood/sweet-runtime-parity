"""Build a blind-ish Work adjudication queue for the selective surgical gate.

The queue intentionally omits prior linguistic adjudication labels so the new
selective outputs can be reviewed on their own merits. Prior files remain in
the repository for later comparison.
"""
import json, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ART=ROOT/"artifacts"
AR=ROOT/"phase2"/"arabic_eval"
sys.path.insert(0,str(AR))
import prototype_surgical_renderer as surg


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    raw=json.loads((ART/"SELECTIVE_SURGICAL_GATE_RAW.json").read_text(encoding="utf-8"))
    dev=read_jsonl(AR/"DEVELOPMENT_TARGETS.jsonl")
    by={}
    for r in dev:
        by.setdefault(r["passage_id"],[]).append(r)

    queue=[]
    for pid in sorted(by,key=lambda x:int(x)):
        p=raw["passages"][str(pid)]
        source=p["source"]
        targets=[]
        for r in sorted(by[pid],key=lambda x:x["target_start"]):
            exact={}
            for name in ("op_aware","op_aware_ged_non_uc","op_aware_ged_p30","op_aware_ged_p50","op_aware_ged_p70"):
                out=raw["passages"][str(pid)]["operation_aware_output"] if name=="op_aware" else None
                if name!="op_aware":
                    # Variant outputs are stored globally in the raw result only via summaries,
                    # so recover them from passage GED metadata by applying selected edits is not
                    # repeated here. The runner persists explicit outputs below in gate_outputs.
                    out=p["gate_outputs"][name]
                exact[name]=bool(surg.target_recovered(r,out))
            targets.append({
                "case_id":r["case_id"],
                "target_id":r["target_id"],
                "category_hint":r["category_hint"],
                "target_span":[r["target_start"],r["target_end"]],
                "target_error":r["target_error"],
                "published_correction":r["target_correction"],
                "published_reference":r["reference"],
                "automated_exact_flags":exact,
            })

        edits=[]
        for e in p["baseline_candidate_edits"]:
            edits.append({
                "edit_index":e["edit_index"],
                "word_index":e["word_index"],
                "source_word":e["source_word"],
                "source_text":e["source_text"],
                "replacement":e["replacement"],
                "label":e["label"],
                "top1_confidence":e["top1_confidence"],
                "operation_family":e["operation_family"],
                "operation_policy_allow":e["operation_policy_allow"],
                "operation_policy_reason":e["operation_policy_reason"],
                "ged":e["ged"],
                "ged_gate_membership":e["ged_gate_membership"],
            })

        queue.append({
            "passage_id":pid,
            "source":source,
            "targets":targets,
            "candidate_edits":edits,
            "outputs":{
                "baseline_surgical_nopnx1":p["baseline_surgical_output"],
                "operation_aware":p["operation_aware_output"],
                **p["gate_outputs"],
            },
            "primary_new_variant":"operation_aware",
            "secondary_ged_variants":[
                "op_aware_ged_non_uc",
                "op_aware_ged_p30",
                "op_aware_ged_p50",
                "op_aware_ged_p70",
            ],
            "review_contract":{
                "do_not_use_prior_labels_in_pass1":True,
                "judge_applied_edits":"SUPPORTED_CORRECTION / SUPPORTED_ALTERNATIVE / PARTIAL_CORRECTION / UNNECESSARY_EDIT / WRONG_CORRECTION / REVIEW_REQUIRED",
                "target_outcomes":"EXACT_SUPPORTED_CORRECTION / SUPPORTED_ALTERNATIVE / PARTIAL_CORRECTION / ERROR_PRESERVED / WRONG_CORRECTION / REVIEW_REQUIRED",
                "warning":"Nahw references are local corrections, not fully corrected passages.",
            },
        })

    q=ROOT/"PHASE2_SELECTIVE_ADJUDICATION_QUEUE.jsonl"
    q.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in queue)+"\n",encoding="utf-8")
    summary={
        "status":"READY_FOR_SELECTIVE_GATE_ADJUDICATION",
        "passage_clusters":41,
        "target_rows":150,
        "primary_variant":"operation_aware",
        "secondary_ged_variants":[
            "op_aware_ged_non_uc","op_aware_ged_p30","op_aware_ged_p50","op_aware_ged_p70"
        ],
        "prior_labels_omitted_from_queue":True,
        "development_only":True,
        "not_sealed":True,
    }
    s=ROOT/"PHASE2_SELECTIVE_ADJUDICATION_QUEUE_SUMMARY.json"
    s.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"selective_adjudication_queue":summary},ensure_ascii=False))


if __name__=="__main__":
    main()
