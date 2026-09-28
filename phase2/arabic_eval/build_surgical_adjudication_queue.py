"""Build a passage-clustered adjudication queue for the source-preserving surgical renderer.

Consumes artifacts/SURGICAL_RENDERER_RESULTS.json produced in the same GitHub Actions run.
Does not change model outputs. It exposes only development evidence for linguistic review.
"""
import argparse, collections, difflib, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def diffs(a,b):
    out=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=="equal":
            continue
        out.append({
            "tag":tag,
            "source_span":[i1,i2],
            "output_span":[j1,j2],
            "source_text":a[i1:i2],
            "output_text":b[j1:j2],
        })
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results",type=Path,default=ROOT/"artifacts/SURGICAL_RENDERER_RESULTS.json")
    ap.add_argument("--targets",type=Path,default=HERE/"DEVELOPMENT_TARGETS.jsonl")
    ap.add_argument("--queue",type=Path,default=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl")
    ap.add_argument("--summary",type=Path,default=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE_SUMMARY.json")
    args=ap.parse_args()

    result=json.loads(args.results.read_text(encoding="utf-8"))
    targets=[json.loads(x) for x in args.targets.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert result["status"]=="DEVELOPMENT_SOURCE_PRESERVING_SURGICAL_PROTOTYPE"
    assert len(targets)==150 and len({x["passage_id"] for x in targets})==41

    by_passage=collections.defaultdict(list)
    for row in targets:
        by_passage[row["passage_id"]].append(row)

    queue=[]
    total_applied=0
    total_suppressed=0
    changed_passages=0
    recovered_counts=collections.Counter()

    for pid in sorted(by_passage,key=lambda x:int(x) if str(x).isdigit() else str(x)):
        rows=by_passage[pid]
        src=rows[0]["source"]
        outputs=result["passage_outputs"][str(pid)] if str(pid) in result["passage_outputs"] else result["passage_outputs"][pid]
        traces=result["passage_traces"][str(pid)] if str(pid) in result["passage_traces"] else result["passage_traces"][pid]

        variants={}
        for v in ("nopnx1","nopnx2","full"):
            out=outputs[v]
            applied=[]
            suppressed=[]
            for stage in traces[v]:
                stage_name=stage["stage"]
                for e in stage.get("applied_edits",[]):
                    applied.append({"stage":stage_name,**e})
                for e in stage.get("suppressed",[]):
                    suppressed.append({"stage":stage_name,**e})
            variants[v]={
                "output":out,
                "output_changed_from_source":out!=src,
                "source_to_output_diffs":diffs(src,out),
                "applied_model_edits":applied,
                "suppressed_hazards":suppressed,
                "applied_edit_count":len(applied),
                "suppressed_hazard_count":len(suppressed),
            }

        if variants["nopnx1"]["output_changed_from_source"]:
            changed_passages+=1
        total_applied+=variants["nopnx1"]["applied_edit_count"]
        total_suppressed+=variants["nopnx1"]["suppressed_hazard_count"]

        tlist=[]
        for row in sorted(rows,key=lambda x:x["target_start"]):
            rec={}
            tr=next(x for x in result["target_rows"] if x["case_id"]==row["case_id"])
            for v in ("nopnx1","nopnx2","full"):
                val=bool(tr[f"{v}_recovered_exact"])
                rec[v]=val
                if val:
                    recovered_counts[v]+=1
            tlist.append({
                "case_id":row["case_id"],
                "target_id":row["target_id"],
                "category_hint":row["category_hint"],
                "target_span":[row["target_start"],row["target_end"]],
                "target_error":row["target_error"],
                "target_correction":row["target_correction"],
                "single_target_reference":row["reference"],
                "recovered_exact":rec,
            })

        queue.append({
            "passage_id":pid,
            "source":src,
            "targets":tlist,
            "variants":variants,
            "primary_architecture_for_adjudication":"nopnx1",
            "adjudication_contract":{
                "applied_edit_classes":[
                    "SUPPORTED_CORRECTION",
                    "SUPPORTED_ALTERNATIVE",
                    "UNNECESSARY_EDIT",
                    "WRONG_CORRECTION",
                    "PARTIAL_CORRECTION",
                    "REVIEW_REQUIRED"
                ],
                "severity":["LOW","MEDIUM","HIGH","CRITICAL"],
                "renderer_rule":"Untouched source surface is preserved exactly; evaluate only actual applied model edits separately from suppressed hazards.",
                "suppressed_hazard_rule":"Do not count suppressed hazards as model-output errors because they were not applied; audit whether any suppressed hazard would have contained a useful correction.",
                "target_rule":"Nahw references are one-location corrections, not fully corrected passages."
            }
        })

    summary={
        "status":"READY_FOR_SURGICAL_QUALITY_ADJUDICATION",
        "passage_clusters":41,
        "target_rows":150,
        "primary_architecture":"nopnx1",
        "nopnx1_exact_target_recoveries":recovered_counts["nopnx1"],
        "nopnx2_exact_target_recoveries":recovered_counts["nopnx2"],
        "full_exact_target_recoveries":recovered_counts["full"],
        "nopnx1_changed_passages":changed_passages,
        "nopnx1_applied_model_edits":total_applied,
        "nopnx1_suppressed_hazards":total_suppressed,
        "scientific_stress_reference":{
            "nopnx1_protected_exact_cases":result["scientific_stress_summary"]["nopnx1"]["protected_exact_cases"],
            "nopnx1_source_exact_unchanged_cases":result["scientific_stress_summary"]["nopnx1"]["source_exact_unchanged_cases"],
            "nopnx1_outputs_with_UNK":result["scientific_stress_summary"]["nopnx1"]["outputs_with_UNK"],
        },
        "review_unit":"passage_id",
        "development_only":True,
        "not_sealed":True,
    }

    args.queue.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in queue)+"\n",encoding="utf-8")
    args.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"surgical_adjudication_queue_summary":summary},ensure_ascii=False))


if __name__=="__main__":
    main()
