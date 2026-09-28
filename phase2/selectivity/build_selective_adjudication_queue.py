"""Build Work adjudication queue for Selective Surgical Gate.

Prior linguistic adjudication labels are deliberately omitted from the queue.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]; ART=ROOT/"artifacts"; AR=ROOT/"phase2"/"arabic_eval"
sys.path.insert(0,str(AR))
import prototype_surgical_renderer as surg


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    raw=json.loads((ART/"SELECTIVE_SURGICAL_GATE_RAW.json").read_text(encoding="utf-8"))
    analysis=json.loads((ART/"SELECTIVE_GATE_ANALYSIS.json").read_text(encoding="utf-8"))
    dev=read_jsonl(AR/"DEVELOPMENT_TARGETS.jsonl")
    by={}
    for r in dev: by.setdefault(r["passage_id"],[]).append(r)
    names=list(raw["variant_summaries"])
    queue=[]
    for pid in sorted(by,key=int):
        p=raw["passages"][str(pid)]
        targets=[]
        for r in sorted(by[pid],key=lambda x:x["target_start"]):
            flags={n:bool(surg.target_recovered(r,p["outputs"][n])) for n in names}
            targets.append({
                "case_id":r["case_id"],"target_id":r["target_id"],"category_hint":r["category_hint"],
                "target_span":[r["target_start"],r["target_end"]],
                "target_error":r["target_error"],"published_correction":r["target_correction"],
                "published_reference":r["reference"],"automated_exact_flags":flags
            })
        edits=[]
        for e in p["baseline_candidate_edits"]:
            edits.append({
                "edit_index":e["edit_index"],"word_index":e["word_index"],"source_word":e["source_word"],
                "source_text":e["source_text"],"replacement":e["replacement"],"label":e["label"],
                "top1_confidence":e["top1_confidence"],"operation_family":e["operation_family"],
                "base_policy_allow":e["base_policy_allow"],"base_policy_reason":e["base_policy_reason"],
                "ged":e["ged"],
                "gate_membership":{n:int(e["edit_index"]) in p["gate_meta"][n]["applied_indices"] for n in names}
            })
        queue.append({
            "passage_id":pid,"source":p["source"],"targets":targets,"candidate_edits":edits,
            "outputs":{"baseline_surgical_nopnx1":p["baseline_surgical_output"],**p["outputs"]},
            "primary_new_variant":"op_aware",
            "ged_variants":["ged_zaebuc","ged_qalb14","ged_union","ged_intersection"],
            "review_contract":{
                "pass1_blind_to_prior_labels":True,
                "applied_edit_classes":["SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE","PARTIAL_CORRECTION","UNNECESSARY_EDIT","WRONG_CORRECTION","REVIEW_REQUIRED"],
                "target_classes":["EXACT_SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE","PARTIAL_CORRECTION","ERROR_PRESERVED","WRONG_CORRECTION","REVIEW_REQUIRED"],
                "warning":"Nahw references are local corrections, not fully corrected passages."
            }
        })
    q=ROOT/"PHASE2_SELECTIVE_ADJUDICATION_QUEUE.jsonl"
    q.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in queue)+"\n",encoding="utf-8")
    summary={
        "status":"READY_FOR_SELECTIVE_GATE_ADJUDICATION","passage_clusters":41,"target_rows":150,
        "variants":names,"primary_variant":"op_aware","prior_labels_omitted_from_queue":True,
        "development_only":True,"not_sealed":True,
        "pre_adjudication_proxy":{k:{
            "retained_edits":v["edits"],"supported_from_prior_labels":v["supported"],"wrong_from_prior_labels":v["wrong"],
            "partial_from_prior_labels":v["partial"],"unnecessary_from_prior_labels":v["unnecessary"],
            "supported_precision_proxy":v["supported_precision"],"automated_exact_target_recovery":v["automated_exact_target_recovery"]
        } for k,v in analysis["variants"].items()}
    }
    s=ROOT/"PHASE2_SELECTIVE_ADJUDICATION_QUEUE_SUMMARY.json"
    s.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"selective_adjudication_queue":summary},ensure_ascii=False))


if __name__=="__main__":
    main()
