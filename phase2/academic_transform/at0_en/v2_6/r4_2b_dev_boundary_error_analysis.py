#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import AutoTokenizer, BertForTokenClassification, Trainer, TrainingArguments

from r4_2b_source_aligned_train_calibrate_witness import TokenDataset, read_conll, word_sequences

EXPECTED_DEV_SHA256 = "3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a"
EXPECTED_MODEL_SHA256 = "3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c"
THRESHOLDS = [0.80, 0.85, 0.90, 0.95]
ENTITY_TYPES = ["P", "I", "C", "O"]
SEED = 42

def sha256_path(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def tag_type(tag):
    return "OUTSIDE" if tag=="O" else tag.split("-",1)[1]

def entity_spans(tags, confidences=None):
    out=[]; cur=None; n=len(tags)
    for i in range(n+1):
        tag="O" if i==n else tags[i]
        if tag=="O": pref,typ="O",None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            if pref=="I" and typ==cur["type"]:
                if confidences is not None: cur["confs"].append(float(confidences[i]))
                continue
            confs=cur.pop("confs")
            if confs:
                cur["min_conf"]=float(min(confs))
                cur["mean_conf"]=float(sum(confs)/len(confs))
                cur["geom_conf"]=float(math.exp(sum(math.log(max(x,1e-12)) for x in confs)/len(confs)))
            else:
                cur["min_conf"]=cur["mean_conf"]=cur["geom_conf"]=1.0
            cur["end"]=i; out.append(cur); cur=None
        if tag!="O":
            cur={"type":typ,"start":i,"confs":[] if confidences is None else [float(confidences[i])]}
    return out

def overlap(a,b):
    return max(0,min(a["end"],b["end"])-max(a["start"],b["start"]))

def iou(a,b):
    ov=overlap(a,b)
    if not ov: return 0.0
    return ov/((a["end"]-a["start"])+(b["end"]-b["start"])-ov)

def exact(a,b):
    return a["type"]==b["type"] and a["start"]==b["start"] and a["end"]==b["end"]

def exact_span(a,b):
    return a["start"]==b["start"] and a["end"]==b["end"]

def best_overlap(ent,candidates,same_type=None):
    xs=[]
    for x in candidates:
        if same_type is True and x["type"]!=ent["type"]: continue
        if same_type is False and x["type"]==ent["type"]: continue
        ov=overlap(ent,x)
        if ov:
            xs.append((iou(ent,x),ov,-(abs(ent["start"]-x["start"])+abs(ent["end"]-x["end"])),x))
    if not xs: return None
    xs.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)
    return xs[0][3]

def classify_pred(pred,golds):
    for g in golds:
        if exact(pred,g): return "EXACT_CORRECT",g
    for g in golds:
        if exact_span(pred,g) and pred["type"]!=g["type"]: return "TYPE_ERROR_EXACT_BOUNDARY",g
    g=best_overlap(pred,golds,True)
    if g is not None: return "BOUNDARY_ERROR_SAME_TYPE",g
    g=best_overlap(pred,golds,False)
    if g is not None: return "TYPE_AND_BOUNDARY_ERROR",g
    return "SPURIOUS",None

def classify_gold(gold,preds):
    for p in preds:
        if exact(gold,p): return "EXACT_MATCH",p
    for p in preds:
        if exact_span(gold,p) and gold["type"]!=p["type"]: return "TYPE_ERROR_EXACT_BOUNDARY",p
    p=best_overlap(gold,preds,True)
    if p is not None: return "BOUNDARY_ERROR_SAME_TYPE",p
    p=best_overlap(gold,preds,False)
    if p is not None: return "TYPE_AND_BOUNDARY_ERROR",p
    return "OMITTED",None

def boundary_pattern(pred,gold):
    ds=pred["start"]-gold["start"]; de=pred["end"]-gold["end"]
    if ds==0 and de==0: return "EXACT"
    if ds==0: return "RIGHT_CONTRACTION" if de<0 else "RIGHT_EXTENSION"
    if de==0: return "LEFT_CONTRACTION" if ds>0 else "LEFT_EXTENSION"
    if ds>0 and de<0: return "BOTH_CONTRACTION"
    if ds<0 and de>0: return "BOTH_EXTENSION"
    return "MIXED_SHIFT"

def qstats(vals):
    if not vals:
        return {"n":0,"min":None,"q25":None,"median":None,"q75":None,"max":None,"mean":None}
    a=np.asarray(vals,dtype=float)
    return {"n":int(a.size),"min":float(a.min()),"q25":float(np.quantile(a,.25)),
            "median":float(np.quantile(a,.5)),"q75":float(np.quantile(a,.75)),
            "max":float(a.max()),"mean":float(a.mean())}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)

    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True,warn_only=True); torch.set_num_threads(2)

    dev_sha=sha256_path(args.dev)
    model_sha=sha256_path(args.model_dir/"model.safetensors")
    if dev_sha!=EXPECTED_DEV_SHA256: raise RuntimeError(f"frozen dev hash mismatch: {dev_sha}")
    if model_sha!=EXPECTED_MODEL_SHA256: raise RuntimeError(f"R4.2B model hash mismatch: {model_sha}")
    if (args.model_dir/"pytorch_model.bin").exists(): raise RuntimeError("pickle model forbidden")

    dev_s=read_conll(args.dev)
    tokenizer=AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True,use_fast=True)
    model=BertForTokenClassification.from_pretrained(args.model_dir,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in model.parameters()): raise RuntimeError("non-finite model")
    ds=TokenDataset(dev_s,tokenizer)

    pa=TrainingArguments(output_dir=str(args.out/"predict_tmp"),per_device_eval_batch_size=8,
                         report_to=[],disable_tqdm=True,dataloader_num_workers=0,seed=SEED)
    pr=Trainer(model=model,args=pa,tokenizer=tokenizer).predict(ds)
    gold_tags,pred_tags,pred_conf=word_sequences(pr.predictions,pr.label_ids)

    token_confusion=defaultdict(Counter)
    pred_counts=Counter(); gold_counts=Counter()
    pred_by_class={c:Counter() for c in ENTITY_TYPES}
    gold_by_class={c:Counter() for c in ENTITY_TYPES}
    boundary_by_class={c:Counter() for c in ENTITY_TYPES}
    conf_by_class_cat={c:defaultdict(list) for c in ENTITY_TYPES}
    all_preds=[]; sentence_records=[]

    for si,((tokens,_),gt,pt,cf) in enumerate(zip(dev_s,gold_tags,pred_tags,pred_conf)):
        for gtag,ptag in zip(gt,pt): token_confusion[tag_type(gtag)][tag_type(ptag)]+=1
        golds=entity_spans(gt); preds=entity_spans(pt,cf)
        lp=[]; lg=[]
        for p in preds:
            cat,g=classify_pred(p,golds)
            pred_counts[cat]+=1; pred_by_class[p["type"]][cat]+=1
            conf_by_class_cat[p["type"]][cat].append(p["min_conf"])
            rec={**p,"category":cat,"text":" ".join(tokens[p["start"]:p["end"]]),
                 "sentence":" ".join(tokens),"gold_overlap":None,"sentence_index":si}
            if g is not None:
                rec["gold_overlap"]={"type":g["type"],"start":g["start"],"end":g["end"],
                    "text":" ".join(tokens[g["start"]:g["end"]]),"iou":iou(p,g),
                    "boundary_pattern":boundary_pattern(p,g)}
                if cat=="BOUNDARY_ERROR_SAME_TYPE":
                    boundary_by_class[p["type"]][boundary_pattern(p,g)]+=1
            lp.append(rec); all_preds.append(rec)
        for g in golds:
            cat,p=classify_gold(g,preds)
            gold_counts[cat]+=1; gold_by_class[g["type"]][cat]+=1
            rec={**g,"category":cat,"text":" ".join(tokens[g["start"]:g["end"]]),
                 "sentence":" ".join(tokens),"pred_overlap":None,"sentence_index":si}
            if p is not None:
                rec["pred_overlap"]={"type":p["type"],"start":p["start"],"end":p["end"],
                    "text":" ".join(tokens[p["start"]:p["end"]]),"min_conf":p.get("min_conf"),
                    "iou":iou(g,p)}
            lg.append(rec)
        sentence_records.append({"sentence_index":si,"tokens":tokens,
                                 "predicted_entities":lp,"gold_entities":lg})

    threshold_breakdown={}
    for t in THRESHOLDS:
        bc={}
        for c in ENTITY_TYPES:
            accepted=[r for r in all_preds if r["type"]==c and r["min_conf"]>=t]
            cats=Counter(r["category"] for r in accepted)
            tp=cats.get("EXACT_CORRECT",0); n=len(accepted)
            bc[c]={"accepted":n,"exact_tp":tp,"precision":tp/n if n else 0.0,
                   "breakdown":dict(sorted(cats.items()))}
        threshold_breakdown[str(t)]=bc

    confidence_summary={c:{cat:qstats(vals) for cat,vals in sorted(conf_by_class_cat[c].items())}
                        for c in ENTITY_TYPES}
    high=[r for r in all_preds if r["category"]!="EXACT_CORRECT" and r["min_conf"]>=.95]
    high.sort(key=lambda r:(-r["min_conf"],r["type"],r["sentence_index"],r["start"]))

    report={
      "analysis":"R4_2B_DEV_ONLY_BOUNDARY_ERROR_ANALYSIS_V1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "source_run_id":37409097042,"source_artifact_id":11397202598,
      "source_artifact_digest":"sha256:45d204d5f073aa5ecc5944dc49bee88be5bb677e0160b8c17720f2250de6fa71",
      "model_safetensors_sha256":model_sha,"dev_sha256":dev_sha,"dev_sentences":len(dev_s),
      "guards":{"dev_only":True,"training_performed":False,"thresholds_changed":False,
                "test_files_read":False,"factpico_used":False,
                "consumed_60_rct_holdout_used":False,"opened_30_rct_diagnostic_used":False},
      "predicted_entity_error_counts":dict(sorted(pred_counts.items())),
      "predicted_entity_error_by_class":{c:dict(sorted(pred_by_class[c].items())) for c in ENTITY_TYPES},
      "gold_entity_outcome_counts":dict(sorted(gold_counts.items())),
      "gold_entity_outcome_by_class":{c:dict(sorted(gold_by_class[c].items())) for c in ENTITY_TYPES},
      "boundary_patterns_by_class":{c:dict(sorted(boundary_by_class[c].items())) for c in ENTITY_TYPES},
      "confidence_by_class_and_category":confidence_summary,
      "threshold_false_positive_breakdown":threshold_breakdown,
      "token_type_confusion":{g:dict(sorted(row.items())) for g,row in sorted(token_confusion.items())},
      "high_confidence_error_count_ge_0_95":len(high),
      "high_confidence_error_examples_ge_0_95":high[:60],
      "all_sentence_records":sentence_records,
      "interpretation_boundary":"DIAGNOSTIC_ONLY_NO_GATE_OR_THRESHOLD_CHANGE",
      "next_decision":"CLASSIFY_DOMINANT_DEV_ERROR_MECHANISM_BEFORE_ANY_NEW_TRAINING"
    }
    canonical=json.dumps(report,sort_keys=True,separators=(",",":")).encode()
    report["canonical_pre_hash_sha256"]=hashlib.sha256(canonical).hexdigest()
    (args.out/"R4_2B_DEV_BOUNDARY_ERROR_ANALYSIS.json").write_text(
        json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    md=["# R4.2B Dev-only Boundary Error Analysis","",
        f"- Source run: `{report['source_run_id']}`",
        f"- Model SHA-256: `{model_sha}`",f"- Dev SHA-256: `{dev_sha}`",
        "- Scope: frozen dev only; no training; no test/holdout access; no threshold changes.","",
        "## Predicted entity outcomes"]
    md += [f"- {k}: {v}" for k,v in sorted(pred_counts.items())]
    md += ["","## By predicted class"]
    for c in ENTITY_TYPES:
        md += [f"### {c}"]+[f"- {k}: {v}" for k,v in sorted(pred_by_class[c].items())]
    md += ["","## Threshold false-positive mechanism"]
    for t in THRESHOLDS:
        md.append(f"### threshold {t:.2f}")
        for c in ENTITY_TYPES:
            x=threshold_breakdown[str(t)][c]
            md.append(f"- {c}: accepted={x['accepted']}, exact_tp={x['exact_tp']}, precision={x['precision']:.6f}, breakdown={x['breakdown']}")
    md += ["","## Boundary patterns"]
    for c in ENTITY_TYPES: md.append(f"- {c}: {dict(boundary_by_class[c])}")
    md += ["",f"## High-confidence errors (min entity confidence >=0.95): {len(high)}","",
           "Diagnostic evidence only; does not authorize gate/threshold changes or test inference.",""]
    (args.out/"R4_2B_DEV_BOUNDARY_ERROR_ANALYSIS.md").write_text("\n".join(md),encoding="utf-8")

    print(json.dumps({"state":"DEV_ONLY_BOUNDARY_ANALYSIS_COMPLETE",
      "predicted_entity_error_counts":dict(pred_counts),
      "high_confidence_error_count_ge_0_95":len(high),
      "threshold_0_95":threshold_breakdown["0.95"],
      "canonical_pre_hash_sha256":report["canonical_pre_hash_sha256"]},indent=2,sort_keys=True))

if __name__=="__main__":
    main()
