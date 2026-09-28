"""Build a passage-clustered quality adjudication queue from official development outputs.

This does not decide whether edits are correct. It makes the 41 unique passage outputs
reviewable without pretending 150 target rows are independent passages.
"""
import argparse, collections, difflib, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def opcodes(a,b):
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

def non_keep(stage):
    return sum(1 for x in stage.get("raw_labels",[]) if x!="K*")

def non_keep_details(stage):
    subs=stage.get("subwords",[])
    labels=stage.get("raw_labels",[])
    conf=stage.get("top1_confidence",[])
    out=[]
    for i,(sub,label) in enumerate(zip(subs,labels)):
        if label=="K*":
            continue
        out.append({
            "subword_index":i,
            "subword":sub,
            "label":label,
            "top1_confidence":conf[i] if i < len(conf) else None,
        })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw",type=Path,default=ROOT/"artifacts/OFFICIAL_DEVELOPMENT_RAW.jsonl")
    ap.add_argument("--diag",type=Path,default=ROOT/"artifacts/TARGET_RECOVERY_V2.json")
    ap.add_argument("--queue",type=Path,default=ROOT/"PHASE2_ADJUDICATION_QUEUE.jsonl")
    ap.add_argument("--summary",type=Path,default=ROOT/"PHASE2_ADJUDICATION_QUEUE_SUMMARY.json")
    args=ap.parse_args()

    rows=[json.loads(x) for x in args.raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    diag=json.loads(args.diag.read_text(encoding="utf-8"))
    states={x["case_id"]:x["stages"] for x in diag["cases"]}
    assert len(rows)==150 and len({r["passage_id"] for r in rows})==41

    groups=collections.defaultdict(list)
    for r in rows:
        groups[r["passage_id"]].append(r)

    queue=[]
    state_totals=collections.Counter()
    for pid in sorted(groups,key=lambda x:int(x) if str(x).isdigit() else str(x)):
        rs=groups[pid]
        first=rs[0]
        source=first["source"]
        outputs={
            "nopnx_iteration_1":first["nopnx_iteration_1"]["output"],
            "nopnx_iteration_2":first["nopnx_iteration_2"]["output"],
            "pnx_only":first["pnx_only"]["output"],
            "full":first["full_pnx_iteration_1"]["output"],
        }
        targets=[]
        for r in sorted(rs,key=lambda x:x["target_start"]):
            st={k:v["state"] for k,v in states[r["case_id"]].items()}
            state_totals[st["full"]]+=1
            targets.append({
                "case_id":r["case_id"],
                "target_id":r["target_id"],
                "category_hint":r["category_hint"],
                "target_span":[r["target_start"],r["target_end"]],
                "target_error":r["target_error"],
                "target_correction":r["target_correction"],
                "single_target_reference":r["reference"],
                "states":st,
            })

        item={
            "passage_id":pid,
            "source":source,
            "outputs":outputs,
            "source_to_outputs":{
                name:opcodes(source,out) for name,out in outputs.items()
            },
            "model_non_keep_label_counts":{
                "nopnx_iteration_1":non_keep(first["nopnx_iteration_1"]),
                "nopnx_iteration_2_incremental":non_keep(first["nopnx_iteration_2"]),
                "pnx_only":non_keep(first["pnx_only"]),
                "full_pnx_incremental":non_keep(first["full_pnx_iteration_1"]),
            },
            "model_non_keep_edits":{
                "nopnx_iteration_1":non_keep_details(first["nopnx_iteration_1"]),
                "nopnx_iteration_2_incremental":non_keep_details(first["nopnx_iteration_2"]),
                "pnx_only":non_keep_details(first["pnx_only"]),
                "full_pnx_incremental":non_keep_details(first["full_pnx_iteration_1"]),
            },
            "targets":targets,
            "review_flags":{
                "has_target_changed_other":any(t["states"]["full"]=="TARGET_CHANGED_OTHER" for t in targets),
                "has_recovered_target":any(t["states"]["full"].startswith("RECOVERED_") for t in targets),
                "has_preserved_error":any(t["states"]["full"]=="ERROR_PRESERVED_LOCAL" for t in targets),
                "full_output_differs_from_source":outputs["full"]!=source,
            },
            "adjudication_contract":{
                "target_changed_other":"Decide SUPPORTED_ALTERNATIVE / WRONG_CORRECTION / REVIEW_REQUIRED.",
                "collateral_edits":"Decide SUPPORTED_CORRECTION / ACCEPTABLE_ALTERNATIVE / UNNECESSARY_EDIT / INCORRECT_EDIT / REVIEW_REQUIRED.",
                "warning":"Nahw single-target references are not fully corrected passages; do not score full-string exact match as gold."
            }
        }
        queue.append(item)

    args.queue.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in queue)+"\n",encoding="utf-8")
    summary={
        "status":"READY_FOR_QUALITY_ADJUDICATION",
        "passage_clusters":len(queue),
        "target_rows":len(rows),
        "full_target_states":dict(state_totals),
        "passages_with_target_changed_other":sum(x["review_flags"]["has_target_changed_other"] for x in queue),
        "passages_with_recovered_target":sum(x["review_flags"]["has_recovered_target"] for x in queue),
        "passages_with_preserved_error":sum(x["review_flags"]["has_preserved_error"] for x in queue),
        "all_full_outputs_differ_from_source":all(x["review_flags"]["full_output_differs_from_source"] for x in queue),
        "primary_review_unit":"passage_id",
    }
    args.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"adjudication_queue_summary":summary},ensure_ascii=False))

if __name__=="__main__":
    main()