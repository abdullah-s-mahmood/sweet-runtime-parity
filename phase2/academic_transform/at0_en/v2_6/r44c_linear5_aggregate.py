#!/usr/bin/env python3
from __future__ import annotations

import argparse, collections, hashlib, json, math, pathlib

CLASSES=["NONE","P","I","C","O"]
POS=["P","I","C","O"]
THRESHOLDS=[0.80,0.85,0.90,0.95]
GOLD={"P":271,"I":829,"C":115,"O":677}
ATTEMPT_ID="R44C_LINEAR5_L2_DEV_ATTEMPT_1"
EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_CONTEXT_SHA="6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b"
EXPECTED_INDEX_SHA="db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd"

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
        for r in rows: f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def write_json(p,obj):
    pathlib.Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")

def key(r):
    return (int(r["outer_fold"]),int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),str(r["b_type"]))

def eval_key(k,r):
    return (k,int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),str(r["b_type"]))

def probs(r):
    p=[float(r["p_"+c]) for c in CLASSES]
    if any(not math.isfinite(x) or x<0.0 or x>1.0 for x in p): raise RuntimeError("invalid probability")
    if abs(sum(p)-1.0)>1e-10: raise RuntimeError(f"prob sum {sum(p)}")
    return p

def validate_numeric_record(r):
    z=[float(r["logit_"+c]) for c in CLASSES]
    lp=[float(r["logp_"+c]) for c in CLASSES]
    p=probs(r)
    if any(not math.isfinite(x) for x in z+lp): raise RuntimeError("nonfinite logit/logp")
    m=max(z)
    ex=[math.exp(x-m) for x in z]; den=sum(ex)
    sp=[x/den for x in ex]
    slp=[math.log(x) for x in sp]
    if max(abs(a-b) for a,b in zip(sp,p))>1e-10: raise RuntimeError("logit/probability mismatch")
    if max(abs(a-b) for a,b in zip(slp,lp))>1e-10: raise RuntimeError("logit/logp mismatch")
    return p

def argmax_label(r,subset=CLASSES):
    if subset==CLASSES:
        p=probs(r); idx=max(range(5),key=lambda i:p[i]); return CLASSES[idx],p[idx]
    vals=[float(r["p_"+c]) for c in subset]
    idx=max(range(len(subset)),key=lambda i:vals[i]); return subset[idx],vals[idx]

def auc_binary(scores,labels):
    pairs=sorted(zip(scores,labels),key=lambda x:x[0])
    npos=sum(labels); nneg=len(labels)-npos
    if npos==0 or nneg==0: return None
    rank_sum=0.0; i=0; rank=1
    while i<len(pairs):
        j=i+1
        while j<len(pairs) and pairs[j][0]==pairs[i][0]: j+=1
        avg=(rank+(rank+(j-i)-1))/2.0
        rank_sum+=avg*sum(int(y) for _,y in pairs[i:j])
        rank+=j-i; i=j
    return (rank_sum-npos*(npos+1)/2.0)/(npos*nneg)

def ap_grouped(scores,labels):
    groups=collections.defaultdict(lambda:[0,0])
    for s,y in zip(scores,labels):
        groups[float(s)][0]+=int(y); groups[float(s)][1]+=1
    positives=sum(labels)
    if positives==0:return None
    tp=0; total=0; area=0.0; prev_recall=0.0
    for s in sorted(groups,reverse=True):
        pos,n=groups[s]; tp+=pos; total+=n
        recall=tp/positives; precision=tp/total
        area+=(recall-prev_recall)*precision
        prev_recall=recall
    return area

def threshold_metrics(rows,t):
    accepted=collections.Counter(); tp=collections.Counter()
    fp_tax=collections.Counter()
    for r in rows:
        pred,conf=argmax_label(r)
        if pred=="NONE" or conf<t: continue
        accepted[pred]+=1
        if r["target"]==pred:
            tp[pred]+=1
        else:
            fp_tax[r.get("taxonomy","UNKNOWN")]+=1
    per={}
    for c in POS:
        a=accepted[c]; z=tp[c]
        precision=z/a if a else 0.0
        recall=z/GOLD[c]
        per[c]={"accepted":a,"tp":z,"fp":a-z,"precision":precision,"recall":recall,
                "gold_denominator":GOLD[c],
                "class_gate":bool(a>=10 and precision>=0.90 and recall>=0.20)}
    macro=sum(per[c]["precision"] for c in POS)/4.0
    return {"threshold":t,"per_class":per,"macro_precision":macro,
            "accepted_total":sum(accepted.values()),"tp_total":sum(tp.values()),
            "fp_taxonomy":dict(fp_tax),
            "passed":bool(all(per[c]["class_gate"] for c in POS) and macro>=0.90)}

def nll(rows):
    s=0.0
    for r in rows:
        p=probs(r); y=CLASSES.index(r["target"])
        if p[y]<=0.0: return float("inf")
        s-=math.log(p[y])
    return s/len(rows)

def brier(rows):
    out=0.0
    for r in rows:
        p=probs(r)
        out+=sum((p[i]-(1.0 if CLASSES[i]==r["target"] else 0.0))**2 for i in range(5))
    return out/len(rows)

def ece(rows,bins=10):
    rec=[]; total=len(rows); val=0.0
    for b in range(bins):
        lo=b/bins; hi=(b+1)/bins
        bucket=[]
        for r in rows:
            pred,conf=argmax_label(r)
            if conf>=lo and (conf<hi or (b==bins-1 and conf<=hi)):
                bucket.append((pred==r["target"],conf))
        n=len(bucket)
        acc=sum(int(x[0]) for x in bucket)/n if n else None
        mc=sum(x[1] for x in bucket)/n if n else None
        if n: val+=(n/total)*abs(acc-mc)
        rec.append({"bin":b,"lo":lo,"hi":hi,"count":n,"accuracy":acc,"mean_confidence":mc})
    return val,rec

def diagnostics(rows):
    labels=[r["target"]!="NONE" for r in rows]
    vs=[1.0-float(r["p_NONE"]) for r in rows]
    valid=[r for r in rows if r["target"]!="NONE"]
    type_correct=0; b_correct=0; fixes=0; breaks=0
    for r in valid:
        pred,_=argmax_label(r,POS)
        if pred==r["target"]: type_correct+=1
        if r["b_type"]==r["target"]: b_correct+=1
        if r["b_type"]!=r["target"] and pred==r["target"]: fixes+=1
        if r["b_type"]==r["target"] and pred!=r["target"]: breaks+=1
    fold_auc={}
    for k in range(5):
        rr=[r for r in rows if int(r["outer_fold"])==k]
        fold_auc[str(k)]=auc_binary([1.0-float(r["p_NONE"]) for r in rr],[r["target"]!="NONE" for r in rr])
    ev,rel=ece(rows)
    return {
        "outer_fiveway_nll":nll(rows),
        "multiclass_brier":brier(rows),
        "topclass_ece_10_equal_width":ev,
        "reliability_bins":rel,
        "validity_auc_1_minus_pNONE":auc_binary(vs,labels),
        "validity_ap_1_minus_pNONE":ap_grouped(vs,labels),
        "validity_prevalence":sum(labels)/len(labels),
        "per_fold_validity_auc":fold_auc,
        "valid_coordinate_count":len(valid),
        "conditional_type_accuracy":type_correct/len(valid),
        "conditional_type_correct":type_correct,
        "copy_B_conditional_accuracy":b_correct/len(valid),
        "copy_B_correct":b_correct,
        "type_only_fixes_B_errors":fixes,
        "type_only_breaks_correct_B":breaks,
    }

def require_one(xs,label):
    xs=list(xs)
    if len(xs)!=1: raise RuntimeError(f"{label} count {len(xs)}")
    return xs[0]

def validate(outputs_root,nested_root,manifest,
             expected_manifest_sha=EXPECTED_MANIFEST_SHA,
             expected_attempt_id=ATTEMPT_ID,
             expected_rows=1942):
    got=canonical_manifest_sha(manifest)
    if manifest.get("manifest_sha256")!=expected_manifest_sha or got!=expected_manifest_sha:
        raise RuntimeError("manifest")
    nested=json.loads((nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if nested.get("state")!="R44B_PAIR_AGGREGATE_PASS": raise RuntimeError("nested")
    folds={int(q["fold"]):set(q["documents"]) for q in manifest["oof_folds"]}
    allrows=[]; summaries=[]
    for k in range(5):
        sp=require_one(outputs_root.rglob(f"R44C_OUTER_{k}_SUMMARY.json"),f"summary {k}")
        pp=require_one(outputs_root.rglob(f"R44C_OUTER_{k}_PROBS.jsonl"),f"probs {k}")
        ck=require_one(outputs_root.rglob(f"R44C_OUTER_{k}_LINEAR5_MODEL.safetensors"),f"checkpoint {k}")
        sc=require_one(outputs_root.rglob(f"R44C_OUTER_{k}_SCALER.safetensors"),f"scaler {k}")
        s=json.loads(sp.read_text())
        if s.get("state")!="R44C_LINEAR5_FOLD_COMPLETE" or s.get("attempt_id")!=expected_attempt_id or int(s.get("outer_fold"))!=k:
            raise RuntimeError(f"summary identity {k}")
        if int(s.get("feature_dim",-1))!=3918 or int(s.get("parameter_count",-1))!=19595: raise RuntimeError("dimension")
        exact_schedule={
            "l2_coefficient":0.01,"optimizer":"LBFGS","lr":1.0,"history_size":100,
            "line_search_fn":"strong_wolfe","max_iter_per_step":1,"max_eval":25,
            "tolerance_grad":1e-7,"tolerance_change":1e-12,
            "convergence_grad_inf":1e-6,"max_optimizer_steps":1000
        }
        for name,val in exact_schedule.items():
            if s.get(name)!=val: raise RuntimeError(f"schedule mutation {name}: {s.get(name)} != {val}")
        if float(s.get("final_grad_inf",1))>1e-6: raise RuntimeError("convergence")
        if int(s.get("optimizer_steps",0))<1 or int(s.get("optimizer_steps",0))>1000: raise RuntimeError("steps")
        if s.get("manifest_canonical_sha256")!=expected_manifest_sha: raise RuntimeError("fold manifest identity")
        if s.get("context_npy_sha256")!=EXPECTED_CONTEXT_SHA or s.get("context_index_sha256")!=EXPECTED_INDEX_SHA:
            raise RuntimeError("fold context identity")
        osum=nested["outer"][str(k)]
        if s.get("meta_sha256")!=osum["meta_sha256"] or s.get("eval_sha256")!=osum["eval_sha256"]:
            raise RuntimeError("fold bank identity")
        g=s.get("guards",{})
        if not all(g.get(x) is True for x in ["train_scaler_meta_only","eval_inference_fields_stripped"]): raise RuntimeError("positive guard")
        if any(g.get(x) for x in ["eval_loss_computed","eval_gradient_computed","verify_internal_used","old_select_used","protected_data_used","calibration_fitted","boundary_repair_used","hard_negative_weighting","class_weighting","retry_or_restart"]):
            raise RuntimeError("negative guard")
        if sha256_path(pp)!=s["probabilities_sha256"] or sha256_path(ck)!=s["checkpoint_sha256"] or sha256_path(sc)!=s["scaler_sha256"]:
            raise RuntimeError("physical SHA")
        out=read_jsonl(pp)
        ev=read_jsonl(nested_root/f"R44B_OUTER_{k}_EVAL.jsonl")
        if len(out)!=len(ev) or len(out)!=int(s["eval_rows"]): raise RuntimeError("fold population")
        om={key(r):r for r in out}
        if len(om)!=len(out): raise RuntimeError("duplicate output")
        joined=[]
        for er in ev:
            kk=eval_key(k,er)
            if kk not in om: raise RuntimeError(f"missing output {kk}")
            rr=dict(om[kk])
            if int(rr["document"]) not in folds[k]: raise RuntimeError("fold docs")
            for forbidden in ["target","taxonomy","goldless_example"]:
                if forbidden in rr: raise RuntimeError(f"leaked eval metadata {forbidden}")
            validate_numeric_record(rr)
            rr["target"]=str(er["target"])
            rr["taxonomy"]=str(er.get("taxonomy",""))
            rr["goldless_example"]=bool(er.get("goldless_example",False))
            joined.append(rr)
        allrows.extend(joined); summaries.append(s)
    if len(allrows)!=expected_rows or len({key(r) for r in allrows})!=expected_rows:
        raise RuntimeError(f"aggregate rows {len(allrows)}")
    return allrows,summaries,got

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outputs-root",type=pathlib.Path,required=True)
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    m=json.loads(a.manifest.read_text())
    rows,summaries,msha=validate(a.outputs_root,a.nested_root,m)
    allp=a.out/"R44C_LINEAR5_ALL_OUTER_PROBS_WITH_FROZEN_TARGETS.jsonl"
    write_jsonl(allp,rows)
    metrics=[threshold_metrics(rows,t) for t in THRESHOLDS]
    passing=[x for x in metrics if x["passed"]]
    selected=passing[0]["threshold"] if passing else None
    decision={"state":"NOMINATED" if selected is not None else "NO_ARCHITECTURE_NOMINATED",
              "architecture":"R44C_LINEAR5_L2_V1" if selected is not None else None,
              "threshold":selected,
              "reason":"LOWEST_FROZEN_PASSING_THRESHOLD" if selected is not None else "NO_FROZEN_THRESHOLD_PASSED"}
    diag=diagnostics(rows)
    report={
        "state":"R44C_LINEAR5_DEVELOPMENT_AGGREGATE_COMPLETE",
        "attempt_id":ATTEMPT_ID,
        "interpretation":"ADAPTIVE_NESTED_DEVELOPMENT_EVIDENCE_ONLY",
        "population_rows":len(rows),"manifest_canonical_sha256":msha,
        "gold_recall_denominators":GOLD,"thresholds":THRESHOLDS,
        "threshold_comparison":">=",
        "gate":{"per_class_precision_min":0.90,"per_class_recall_min":0.20,
                "per_class_accepted_min":10,"macro_precision_min":0.90},
        "threshold_metrics":metrics,"decision":decision,"diagnostics":diag,
        "historical_descriptive_references":{"J0_validity_auc":0.7328427209613384,
                                              "J0_outer_fiveway_nll":1.210236485360117},
        "fold_optimizer_steps":[int(s["optimizer_steps"]) for s in summaries],
        "fold_final_train_ce":[float(s["final_train_ce"]) for s in summaries],
        "fold_final_penalized_objective":[float(s["final_objective"]) for s in summaries],
        "fold_final_grad_inf":[float(s["final_grad_inf"]) for s in summaries],
        "all_probabilities_sha256":sha256_path(allp),
        "guards":{"verify_internal_used":False,"protected_data_used":False,
                  "calibration_fitted":False,"boundary_repair_used":False,
                  "new_thresholds_used":False,"score_driven_retry":False},
        "next_action":"FREEZE_RESULT_AND_STOP_BEFORE_VERIFY_INTERNAL_OR_ANY_SUCCESSOR_MODEL"
    }
    write_json(a.out/"R44C_LINEAR5_DEVELOPMENT_AGGREGATE.json",report)
    print(json.dumps({"state":report["state"],"decision":decision,
                      "validity_auc":diag["validity_auc_1_minus_pNONE"],
                      "outer_nll":diag["outer_fiveway_nll"]},indent=2))

if __name__=="__main__":
    main()
