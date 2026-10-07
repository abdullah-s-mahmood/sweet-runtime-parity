#!/usr/bin/env python3
from __future__ import annotations

import argparse, collections, hashlib, json, math, pathlib

CLASSES=["NONE","P","I","C","O"]
POS_CLASSES=["P","I","C","O"]
THRESHOLDS=[0.80,0.85,0.90,0.95]
GOLD_DENOMS={"P":271,"I":829,"C":115,"O":677}
EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_ATTEMPT_ID="R44B_B1_DEV_J0J1_ATTEMPT_1"

def sha256_path(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def canonical_manifest_sha(m):
    q=dict(m); q.pop("manifest_sha256",None)
    return sha256_text(json.dumps(q,sort_keys=True,separators=(",",":")))

def read_jsonl(p):
    return [json.loads(x) for x in pathlib.Path(p).read_text().splitlines() if x.strip()]

def write_jsonl(p,rows):
    with pathlib.Path(p).open("w",encoding="utf-8") as f:
        for r in rows:f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def write_json(p,obj):
    pathlib.Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")

def row_key(r):
    return (int(r["outer_fold"]),int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),str(r["b_type"]))

def require_exactly_one(items,label):
    items=list(items)
    if len(items)!=1: raise RuntimeError(f"missing/duplicate output {label}: {len(items)}")
    return items[0]

def ensure_unique_rows(rows,label):
    seen=set()
    for r in rows:
        k=row_key(r)
        if k in seen: raise RuntimeError(f"duplicate output row {label}/{k}")
        seen.add(k)
    return seen

def probvec(r):
    p=[float(r["p_"+c]) for c in CLASSES]
    if any(not math.isfinite(x) or x<0.0 or x>1.0 for x in p): raise RuntimeError("nonfinite/out-of-range probability")
    if abs(sum(p)-1.0)>1e-5: raise RuntimeError(f"probability sum {sum(p)}")
    return p

def predict_label_and_conf(r):
    p=probvec(r); i=max(range(5),key=lambda j:p[j])
    return CLASSES[i],p[i]

def threshold_metrics(rows,t):
    accepted=collections.Counter(); tp=collections.Counter(); errors=collections.Counter()
    for r in rows:
        pred,conf=predict_label_and_conf(r)
        if pred=="NONE" or conf < t: continue  # frozen >= comparison
        accepted[pred]+=1
        if str(r["target"])==pred: tp[pred]+=1
        else: errors[pred]+=1
    per={}
    for c in POS_CLASSES:
        a=accepted[c]; z=tp[c]
        per[c]={
            "accepted":a,"tp":z,"fp":a-z,
            "precision":(z/a if a else 0.0),
            "recall":z/GOLD_DENOMS[c],
            "gold_denominator":GOLD_DENOMS[c],
            "class_gate":bool(a>=10 and a>0 and z/a>=0.90 and z/GOLD_DENOMS[c]>=0.20),
        }
    macro=sum(per[c]["precision"] for c in POS_CLASSES)/4.0
    passed=all(per[c]["class_gate"] for c in POS_CLASSES) and macro>=0.90
    return {"threshold":t,"per_class":per,"macro_precision":macro,"passed":passed,
            "accepted_total":sum(accepted.values()),"tp_total":sum(tp.values())}

def choose_lowest_passing(rows):
    metrics=[threshold_metrics(rows,t) for t in THRESHOLDS]
    passing=[m for m in metrics if m["passed"]]
    return metrics,(passing[0]["threshold"] if passing else None)

def brier(rows):
    vals=[]
    for r in rows:
        p=probvec(r); y=str(r["target"])
        vals.append(sum((p[i]-(1.0 if CLASSES[i]==y else 0.0))**2 for i in range(5)))
    return sum(vals)/len(vals)

def reliability_and_ece(rows,bins=10):
    out=[]; total=len(rows); ece=0.0
    for b in range(bins):
        lo=b/bins; hi=(b+1)/bins
        bucket=[]
        for r in rows:
            pred,conf=predict_label_and_conf(r)
            if (conf>=lo and (conf<hi or (b==bins-1 and conf<=hi))):
                bucket.append((pred==str(r["target"]),conf))
        n=len(bucket)
        acc=sum(int(x[0]) for x in bucket)/n if n else None
        mc=sum(x[1] for x in bucket)/n if n else None
        if n: ece+=(n/total)*abs(acc-mc)
        out.append({"bin":b,"lo":lo,"hi":hi,"count":n,"accuracy":acc,"mean_confidence":mc})
    return out,ece

def risk_coverage(rows):
    eligible=[]
    for r in rows:
        pred,conf=predict_label_and_conf(r)
        if pred!="NONE": eligible.append((conf,pred==str(r["target"])))
    eligible.sort(key=lambda x:x[0],reverse=True)
    pts=[]; err=0; total=len(rows)
    for i,(conf,ok) in enumerate(eligible,1):
        err+=0 if ok else 1
        pts.append({"rank":i,"min_confidence":conf,"coverage":i/total,"risk":err/i})
    return pts

def candidate_ap(rows,c):
    scored=sorted(((float(r["p_"+c]),str(r["target"])==c) for r in rows),reverse=True)
    positives=sum(1 for _,y in scored if y)
    if not positives:return {"candidate_positives":0,"average_precision":0.0}
    hit=0; s=0.0
    for rank,(_,y) in enumerate(scored,1):
        if y:
            hit+=1; s+=hit/rank
    return {"candidate_positives":positives,"average_precision":s/positives,
            "candidate_positive_recall_ceiling":positives/GOLD_DENOMS[c]}

def aggregate_head(rows):
    metrics,selected=choose_lowest_passing(rows)
    rel,ece=reliability_and_ece(rows,10)
    return {
        "row_count":len(rows),
        "threshold_metrics":metrics,
        "selected_threshold":selected,
        "passes_any_frozen_threshold":selected is not None,
        "multiclass_brier_mean_sum_squared_5way":brier(rows),
        "ece_top_class_10_equal_width_bins":ece,
        "reliability_bins":rel,
        "risk_coverage_nonNONE_argmax":risk_coverage(rows),
        "per_class_candidate_AP":{c:candidate_ap(rows,c) for c in POS_CLASSES},
    }

def validate_complete(outputs_root,nested_root,manifest):
    got=canonical_manifest_sha(manifest)
    if manifest.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or got!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError("canonical manifest")
    nested=json.loads((nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if nested.get("state")!="R44B_PAIR_AGGREGATE_PASS": raise RuntimeError("nested state")
    folds={int(q["fold"]):set(q["documents"]) for q in manifest["oof_folds"]}
    all_heads={}
    summaries={}
    for head in ["J0","J1"]:
        all_rows=[]; head_summ=[]
        for k in range(5):
            dirs=list(outputs_root.rglob(f"R44B_OUTER_{k}_{head}_SUMMARY.json"))
            probs=list(outputs_root.rglob(f"R44B_OUTER_{k}_{head}_PROBS.jsonl"))
            summary_path=require_exactly_one(dirs,f"{head}/{k}/summary")
            prob_path=require_exactly_one(probs,f"{head}/{k}/probabilities")
            s=json.loads(summary_path.read_text())
            if s.get("state")!="R44B_HEAD_FOLD_COMPLETE" or s.get("head")!=head or int(s.get("outer_fold"))!=k:
                raise RuntimeError(f"summary state {head}/{k}")
            if s.get("attempt_id")!=EXPECTED_ATTEMPT_ID:
                raise RuntimeError(f"attempt identity {head}/{k}: {s.get('attempt_id')}")
            g=s.get("guards",{})
            must_true=["fresh_model_optimizer_scheduler_rng","meta_only_optimizer_updates","evaluation_model_eval","evaluation_no_grad"]
            if not all(g.get(x) is True for x in must_true): raise RuntimeError(f"guard true {head}/{k}")
            must_false=["mechanics_state_reused","verify_internal_used","old_select_used","protected_data_used","threshold_evaluation_performed","calibration_fitted","early_stopping_used","checkpoint_shopping"]
            if any(g.get(x) for x in must_false): raise RuntimeError(f"guard false {head}/{k}")
            if sha256_path(prob_path)!=s.get("probabilities_sha256"): raise RuntimeError(f"prob SHA {head}/{k}")
            ckpt=summary_path.parent/f"R44B_{head}_FINAL_MODEL.safetensors"
            if not ckpt.exists() or sha256_path(ckpt)!=s.get("checkpoint_sha256"):
                raise RuntimeError(f"checkpoint physical SHA {head}/{k}")
            if int(s.get("seed",-1))!=44 or int(s.get("parameter_count",-1)) not in {584631,667836}:
                raise RuntimeError(f"head identity {head}/{k}")
            sch=s.get("schedule",{})
            expected_schedule={"epochs":10,"batch_size":64,"optimizer":"AdamW","lr":0.001,
                               "weight_decay":0.01,"gradient_clip":1.0,
                               "scheduler":"linear_decay_no_warmup","early_stopping":False,
                               "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY","loss":"ordinary_5way_cross_entropy"}
            if any(sch.get(key)!=val for key,val in expected_schedule.items()):
                raise RuntimeError(f"schedule mutation {head}/{k}: {sch}")
            rows=read_jsonl(prob_path)
            evalp=nested_root/f"R44B_OUTER_{k}_EVAL.jsonl"; ev=read_jsonl(evalp)
            if len(rows)!=len(ev) or len(rows)!=int(s["eval_rows"]): raise RuntimeError(f"row count {head}/{k}")
            seen=ensure_unique_rows(rows,f"{head}/{k}")
            for rr,er in zip(rows,ev):
                if rr["head"]!=head or int(rr["outer_fold"])!=k: raise RuntimeError("head/fold provenance")
                rk=row_key(rr); ek=(k,int(er["document"]),int(er["sentence"]),int(er["start"]),int(er["end"]),str(er["b_type"]))
                if rk!=ek or str(rr["target"])!=str(er["target"]): raise RuntimeError(f"eval row identity {head}/{k}")
                probvec(rr)
                if int(rr["document"]) not in folds[k]: raise RuntimeError("fold document")
            all_rows.extend(rows); head_summ.append(s)
        if len(all_rows)!=1942: raise RuntimeError(f"{head} total probability rows {len(all_rows)} != 1942")
        keys=ensure_unique_rows(all_rows,f"{head}/aggregate")
        if len(keys)!=1942: raise RuntimeError(f"{head} aggregate key count")
        all_heads[head]=all_rows; summaries[head]=head_summ
    if set(row_key(r) for r in all_heads["J0"])!=set(row_key(r) for r in all_heads["J1"]):
        raise RuntimeError("J0/J1 population mismatch")
    return all_heads,summaries,got

def decide(head_reports):
    if head_reports["J0"]["selected_threshold"] is not None:
        return {"state":"NOMINATED","head":"J0","threshold":head_reports["J0"]["selected_threshold"],
                "reason":"J0_FIRST_PRECEDENCE_LOWEST_PASSING_THRESHOLD"}
    if head_reports["J1"]["selected_threshold"] is not None:
        return {"state":"NOMINATED","head":"J1","threshold":head_reports["J1"]["selected_threshold"],
                "reason":"J0_FAILED_J1_ESCALATION_LOWEST_PASSING_THRESHOLD"}
    return {"state":"NO_ARCHITECTURE_NOMINATED","head":None,"threshold":None,
            "reason":"NEITHER_HEAD_PASSED_FROZEN_GATES"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outputs-root",type=pathlib.Path,required=True)
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads(a.manifest.read_text())
    heads,summaries,msha=validate_complete(a.outputs_root,a.nested_root,manifest)
    reports={}
    for head,rows in heads.items():
        allp=a.out/f"R44B_{head}_ALL_OUTER_PROBS.jsonl"; write_jsonl(allp,rows)
        reports[head]=aggregate_head(rows)
        reports[head]["probabilities_sha256"]=sha256_path(allp)
        reports[head]["fold_checkpoint_sha256"]=[s["checkpoint_sha256"] for s in summaries[head]]
        reports[head]["fold_probability_sha256"]=[s["probabilities_sha256"] for s in summaries[head]]
    decision=decide(reports)
    report={
        "state":"R44B_HEAD_DEVELOPMENT_AGGREGATE_COMPLETE",
        "attempt_id":EXPECTED_ATTEMPT_ID,
        "interpretation":"DEVELOPMENT_MODEL_SELECTION_EVIDENCE_ONLY",
        "manifest_canonical_sha256":msha,
        "population_rows_per_head":1942,
        "gold_recall_denominators":GOLD_DENOMS,
        "thresholds":THRESHOLDS,
        "threshold_comparison":">=",
        "gate":{"per_class_precision_min":0.90,"per_class_recall_min":0.20,"per_class_accepted_min":10,"macro_precision_min":0.90},
        "diagnostics":{
            "brier":"mean over 1942 candidates of sum_{5 classes}(p-y)^2",
            "ece":"top-class ECE over all 1942 candidates, 10 equal-width bins [0,.1),...,[.9,1]",
            "risk_coverage":"only candidates whose 5-way argmax is non-NONE; cumulative exact-target error risk; coverage denominator=1942",
            "candidate_AP":"one-vs-rest candidate-level AP; recall ceiling uses authoritative gold denominator",
            "diagnostics_do_not_select":True,
        },
        "heads":reports,
        "decision":decision,
        "guards":{
            "verify_internal_used":False,"old_select_used":False,"protected_data_used":False,
            "calibration_fitted":False,"boundary_repair_used":False,"new_thresholds_used":False,
            "score_driven_retry":False,
        },
        "next_action":"FREEZE_COMPLETE_RESULT_AND_STOP_BEFORE_VERIFY_INTERNAL_OR_FINAL_REFIT",
    }
    write_json(a.out/"R44B_HEAD_DEVELOPMENT_AGGREGATE.json",report)
    print(json.dumps({"state":report["state"],"decision":decision,
                      "J0_selected":reports["J0"]["selected_threshold"],
                      "J1_selected":reports["J1"]["selected_threshold"]},indent=2))

if __name__=="__main__":
    main()
