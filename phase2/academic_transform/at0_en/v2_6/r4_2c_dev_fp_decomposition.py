#!/usr/bin/env python3
import argparse, json, pathlib
from collections import Counter, defaultdict
import numpy as np
import torch
from transformers import AutoTokenizer, BertForTokenClassification, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding

from r4_2c_boundary_consensus_train import (
    THRESHOLDS, BOUNDARY_GENERATION_THRESHOLD, MAX_SPAN_WIDTH_WORDS,
    SPAN_CLASSES, SPAN2ID, EXPECTED_R4B_MODEL_SHA,
    read_conll, spans_from_tags, R4BDataset, BoundaryDataset, CandidateSpanDataset,
    predicted_entities, word_r4b_predictions, boundary_probs, sha256_path
)

def overlap(a,b,c,d):
    return max(a,c) < min(b,d)

def qstats(vals):
    if not vals:
        return {"n":0}
    a=np.array(vals,dtype=float)
    return {
        "n":int(len(a)),
        "min":float(np.min(a)),
        "q25":float(np.quantile(a,.25)),
        "median":float(np.median(a)),
        "q75":float(np.quantile(a,.75)),
        "max":float(np.max(a)),
        "mean":float(np.mean(a)),
    }

def classify_fp(c, golds):
    typ,s,e=c["type"],c["start"],c["end"]
    if any(gs==s and ge==e and gt!=typ for gt,gs,ge in golds):
        return "DIFFERENT_CLASS_EXACT_BOUNDARY"
    if any(gt==typ and overlap(s,e,gs,ge) for gt,gs,ge in golds):
        return "SAME_CLASS_WRONG_BOUNDARY_OVERLAP"
    if any(overlap(s,e,gs,ge) for gt,gs,ge in golds):
        return "DIFFERENT_CLASS_WRONG_BOUNDARY_OVERLAP"
    return "SPURIOUS_NO_OVERLAP"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    ap.add_argument("--r4b-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--boundary-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--span-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)

    dev=read_conll(args.dev, expected_empty_surface_tag_counts={})
    gold=[set(spans_from_tags(tags)) for _,tags in dev]

    # Boundary model predictions.
    btok=AutoTokenizer.from_pretrained(args.boundary_model_dir,local_files_only=True,use_fast=True)
    bmodel=BertForTokenClassification.from_pretrained(args.boundary_model_dir,local_files_only=True)
    bdev=BoundaryDataset(dev,btok)
    barg=TrainingArguments(output_dir=str(args.out/"boundary_predict"),per_device_eval_batch_size=8,report_to=[],disable_tqdm=True)
    bp=Trainer(model=bmodel,args=barg,tokenizer=btok).predict(bdev)
    start_probs,end_probs=boundary_probs(bp.predictions,bdev)

    # Frozen R4.2B candidates.
    if sha256_path(args.r4b_model_dir/"model.safetensors") != EXPECTED_R4B_MODEL_SHA:
        raise RuntimeError("R4B model hash mismatch")
    rtok=AutoTokenizer.from_pretrained(args.r4b_model_dir,local_files_only=True,use_fast=True)
    rmodel=BertForTokenClassification.from_pretrained(args.r4b_model_dir,local_files_only=True)
    rdev=R4BDataset(dev,rtok)
    rarg=TrainingArguments(output_dir=str(args.out/"r4b_predict"),per_device_eval_batch_size=8,report_to=[],disable_tqdm=True)
    rp=Trainer(model=rmodel,args=rarg,tokenizer=rtok).predict(rdev)
    seqs=word_r4b_predictions(rp.predictions,rdev)
    candidates=[]
    for si,(tags,conf) in enumerate(seqs):
        for e in predicted_entities(tags,conf):
            e["sentence_index"]=si
            candidates.append(e)

    # Frozen span classifier predictions on exact frozen candidates.
    stok=AutoTokenizer.from_pretrained(args.span_model_dir,local_files_only=True,use_fast=True)
    smodel=BertForSequenceClassification.from_pretrained(args.span_model_dir,local_files_only=True)
    cds=CandidateSpanDataset(candidates,dev,stok)
    coll=DataCollatorWithPadding(tokenizer=stok,return_tensors="pt")
    sarg=TrainingArguments(output_dir=str(args.out/"span_predict"),per_device_eval_batch_size=16,report_to=[],disable_tqdm=True)
    sp=Trainer(model=smodel,args=sarg,tokenizer=stok,data_collator=coll).predict(cds)
    sprobs=1.0/(1.0+np.exp(-sp.predictions))

    enriched=[]
    for idx,c in enumerate(candidates):
        typ,si,s,e=c["type"],c["sentence_index"],c["start"],c["end"]
        g=gold[si]
        exact_same=(typ,s,e) in g
        exact_boundary_any=any(gs==s and ge==e for gt,gs,ge in g)
        starts={gs for gt,gs,ge in g}
        ends={ge for gt,gs,ge in g}
        start_gold=s in starts
        end_gold=e in ends
        same=float(sprobs[idx][SPAN2ID[typ]])
        other=max(float(sprobs[idx][j]) for j in range(len(SPAN_CLASSES)) if j!=SPAN2ID[typ])
        row={
            **c,
            "exact_same":exact_same,
            "exact_boundary_any_class":exact_boundary_any,
            "fp_kind":None if exact_same else classify_fp(c,g),
            "start_prob":float(start_probs[si][s]),
            "end_prob":float(end_probs[si][e-1]),
            "pair_min":float(min(start_probs[si][s],end_probs[si][e-1])),
            "span_same_class_prob":same,
            "span_other_max_prob":other,
            "start_matches_any_gold_boundary":start_gold,
            "end_matches_any_gold_boundary":end_gold,
            "individually_plausible_jointly_invalid":bool(
                start_probs[si][s] >= BOUNDARY_GENERATION_THRESHOLD
                and end_probs[si][e-1] >= BOUNDARY_GENERATION_THRESHOLD
                and not exact_boundary_any
            ),
            "gold_boundary_cross_pair":bool(start_gold and end_gold and not exact_boundary_any),
        }
        enriched.append(row)

    out={
        "state":"R4_2C_DEV_FP_DECOMPOSITION_COMPLETE",
        "candidate_count":len(enriched),
        "boundary_generation_threshold":BOUNDARY_GENERATION_THRESHOLD,
        "thresholds":{},
        "guards":{
            "dev_only":True,
            "scientific_training_performed":False,
            "test_files_read":False,
            "factpico_used":False,
            "consumed_holdout_used":False,
            "thresholds_changed":False,
        }
    }

    for t in THRESHOLDS:
        acc=[]
        for r in enriched:
            if r["r4b_conf"] < t: continue
            if r["end"]-r["start"] > MAX_SPAN_WIDTH_WORDS or r["end"]<=r["start"]: continue
            if r["start_prob"] < BOUNDARY_GENERATION_THRESHOLD: continue
            if r["end_prob"] < BOUNDARY_GENERATION_THRESHOLD: continue
            if r["span_same_class_prob"] < t: continue
            if r["span_other_max_prob"] >= t: continue
            acc.append(r)
        tp=[r for r in acc if r["exact_same"]]
        fp=[r for r in acc if not r["exact_same"]]
        by_class={}
        for cls in SPAN_CLASSES:
            ca=[r for r in acc if r["type"]==cls]
            ct=[r for r in ca if r["exact_same"]]
            cf=[r for r in ca if not r["exact_same"]]
            by_class[cls]={
                "accepted":len(ca),"tp":len(ct),"fp":len(cf),
                "precision":len(ct)/len(ca) if ca else 0.0,
                "fp_kinds":dict(Counter(r["fp_kind"] for r in cf)),
                "joint_invalid_fp":sum(r["individually_plausible_jointly_invalid"] for r in cf),
                "cross_pair_fp":sum(r["gold_boundary_cross_pair"] for r in cf),
            }
        out["thresholds"][str(t)]={
            "accepted":len(acc),"tp":len(tp),"fp":len(fp),
            "precision":len(tp)/len(acc) if acc else 0.0,
            "fp_kinds":dict(Counter(r["fp_kind"] for r in fp)),
            "joint_invalid_fp":sum(r["individually_plausible_jointly_invalid"] for r in fp),
            "cross_pair_fp":sum(r["gold_boundary_cross_pair"] for r in fp),
            "per_class":by_class,
            "score_stats":{
                "tp_pair_min":qstats([r["pair_min"] for r in tp]),
                "fp_pair_min":qstats([r["pair_min"] for r in fp]),
                "tp_span_same":qstats([r["span_same_class_prob"] for r in tp]),
                "fp_span_same":qstats([r["span_same_class_prob"] for r in fp]),
                "tp_r4b_conf":qstats([r["r4b_conf"] for r in tp]),
                "fp_r4b_conf":qstats([r["r4b_conf"] for r in fp]),
            }
        }

    # Global FP mechanism over all 404 candidates, independent of acceptance.
    all_fp=[r for r in enriched if not r["exact_same"]]
    out["all_candidates_fp_mechanism"]={
        "fp_count":len(all_fp),
        "fp_kinds":dict(Counter(r["fp_kind"] for r in all_fp)),
        "joint_invalid_count":sum(r["individually_plausible_jointly_invalid"] for r in all_fp),
        "cross_pair_count":sum(r["gold_boundary_cross_pair"] for r in all_fp),
    }

    (args.out/"R4_2C_DEV_FP_DECOMPOSITION.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
