#!/usr/bin/env python3
import argparse, json, math, pathlib, time
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import (
    AutoConfig, AutoTokenizer, BertForSequenceClassification, BertForTokenClassification,
    DataCollatorWithPadding, Trainer, TrainingArguments
)

from r4_2c_boundary_consensus_train import (
    SEED, THRESHOLDS, BOUNDARY_GENERATION_THRESHOLD, MAX_SPAN_WIDTH_WORDS,
    SPAN_CLASSES, SPAN2ID, EXPECTED_TRAIN_SHA, EXPECTED_DEV_SHA,
    EXPECTED_R4B_MODEL_SHA, EXPECTED_CONVERTED_SHA,
    read_conll, spans_from_tags, R4BDataset, BoundaryDataset, CandidateSpanDataset,
    predicted_entities, word_r4b_predictions, boundary_probs, convert_safe_base,
    seed_all, sha256_path, ProgressCallback, atomic_json_write
)
from r4_2d_span_validity_preflight import build_examples

EXPECTED_R42C_BOUNDARY_SHA="a56a24572ffd59b93c71e7b68b4ceb63f52ee17e6247fa5f4f857b826de788ae"
EXPECTED_R42C_TYPE_SHA="d531a61cf76e38cfec307e53a95382fbf3cb107d4a7b0d3677a1304b7f30b8a0"
EXPECTED_VALIDITY_DATASET_SHA="6038f5dd905271b27ad7be8f86118aa583f5adc06158b3adcbd9a7f02b724461"
VALIDITY_THRESHOLD=0.50

class ValidityDataset(torch.utils.data.Dataset):
    def __init__(self,examples,sentences,tokenizer):
        self.items=[]
        for x in examples:
            span=sentences[x["sentence_index"]][0][x["start"]:x["end"]]
            enc=tokenizer(span,is_split_into_words=True,truncation=False)
            if len(enc["input_ids"])>256:
                raise RuntimeError("validity example exceeds 256 wordpieces")
            enc["labels"]=int(x["label"])
            self.items.append(enc)
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

def qstats(vals):
    if not vals: return {"n":0}
    a=np.array(vals,dtype=float)
    return {"n":len(vals),"mean":float(a.mean()),"median":float(np.median(a)),
            "q25":float(np.quantile(a,.25)),"q75":float(np.quantile(a,.75)),
            "min":float(a.min()),"max":float(a.max())}

def calibrate(dev,candidates,start_probs,end_probs,type_probs,valid_probs):
    gold=[]
    for _,tags in dev:
        gold.append(set(spans_from_tags(tags)))
    results=[]
    for t in THRESHOLDS:
        counts={c:{"tp":0,"fp":0,"fn":0,"accepted":0,"gold":0} for c in SPAN_CLASSES}
        accepted=[set() for _ in dev]
        accepted_rows=[]
        for si,g in enumerate(gold):
            for typ,_,_ in g: counts[typ]["gold"]+=1
        for idx,c in enumerate(candidates):
            typ=c["type"]; si=c["sentence_index"]; s=c["start"]; e=c["end"]
            if c["r4b_conf"]<t: continue
            if e<=s or e-s>MAX_SPAN_WIDTH_WORDS: continue
            if start_probs[si][s]<BOUNDARY_GENERATION_THRESHOLD: continue
            if end_probs[si][e-1]<BOUNDARY_GENERATION_THRESHOLD: continue
            p=type_probs[idx]
            same=float(p[SPAN2ID[typ]])
            if same<t: continue
            if any(float(p[j])>=t for j in range(len(SPAN_CLASSES)) if j!=SPAN2ID[typ]): continue
            if float(valid_probs[idx])<VALIDITY_THRESHOLD: continue
            key=(typ,s,e)
            counts[typ]["accepted"]+=1
            accepted[si].add(key)
            is_tp=key in gold[si]
            if is_tp: counts[typ]["tp"]+=1
            else: counts[typ]["fp"]+=1
            accepted_rows.append((is_tp,float(valid_probs[idx])))
        for si,g in enumerate(gold):
            for key in g:
                if key not in accepted[si]: counts[key[0]]["fn"]+=1
        per={}
        for cls,d in counts.items():
            pr=d["tp"]/(d["tp"]+d["fp"]) if d["tp"]+d["fp"] else 0.0
            rc=d["tp"]/(d["tp"]+d["fn"]) if d["tp"]+d["fn"] else 0.0
            per[cls]={**d,"precision":pr,"recall":rc}
        macro=sum(per[c]["precision"] for c in SPAN_CLASSES)/4.0
        passes=(all(per[c]["precision"]>=.90 for c in SPAN_CLASSES)
                and all(per[c]["recall"]>=.20 for c in SPAN_CLASSES)
                and all(per[c]["accepted"]>=10 for c in SPAN_CLASSES)
                and macro>=.90)
        tpv=[v for ok,v in accepted_rows if ok]
        fpv=[v for ok,v in accepted_rows if not ok]
        results.append({"threshold":t,"per_class":per,"macro_precision":macro,"passes":passes,
                        "validity_score_stats":{"accepted_tp":qstats(tpv),"accepted_fp":qstats(fpv)}})
    return results

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--r4b-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--boundary-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--type-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    seed_all()
    args.out.mkdir(parents=True,exist_ok=False)
    status=args.out/"PROCESS_STATUS.json"
    atomic_json_write(status,{"state":"RUNNING","progress_percent":0.0,
        "current_stage":"INITIALIZING","active_module":"SPAN_VALIDITY_GUARD",
        "completed_units":0,"total_units":4,
        "last_successful_checkpoint":None,"last_progress_at":datetime.now(timezone.utc).isoformat(),
        "next_expected_step":"VERIFY_IDENTITIES_AND_TRAIN","failure_or_stall_reason":None})

    if sha256_path(args.train)!=EXPECTED_TRAIN_SHA: raise RuntimeError("train hash mismatch")
    if sha256_path(args.dev)!=EXPECTED_DEV_SHA: raise RuntimeError("dev hash mismatch")
    if sha256_path(args.r4b_model_dir/"model.safetensors")!=EXPECTED_R4B_MODEL_SHA: raise RuntimeError("R4B model mismatch")
    if sha256_path(args.boundary_model_dir/"model.safetensors")!=EXPECTED_R42C_BOUNDARY_SHA: raise RuntimeError("R4.2C boundary mismatch")
    if sha256_path(args.type_model_dir/"model.safetensors")!=EXPECTED_R42C_TYPE_SHA: raise RuntimeError("R4.2C type mismatch")
    for p in [args.model_dir,args.r4b_model_dir,args.boundary_model_dir,args.type_model_dir]:
        if (p/"pytorch_model.bin").exists(): raise RuntimeError(f"pickle forbidden: {p}")

    train=read_conll(args.train,expected_empty_surface_tag_counts={"O":5,"I-I":5,"I-P":6,"I-O":1})
    dev=read_conll(args.dev,expected_empty_surface_tag_counts={})
    examples,counts=build_examples(train)
    if counts["dataset_sha256"]!=EXPECTED_VALIDITY_DATASET_SHA: raise RuntimeError("validity dataset digest mismatch")
    if counts["positive_count"]!=3011 or counts["invalid_unique"]!=5442 or counts["total_examples"]!=8453:
        raise RuntimeError(f"validity count mismatch {counts}")

    converted=args.out/"converted_base"
    vtok,converted_sha=convert_safe_base(args.model_dir,converted)
    if converted_sha!=EXPECTED_CONVERTED_SHA: raise RuntimeError("converted base mismatch")
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=2,
        id2label={0:"INVALID",1:"VALID"},label2id={"INVALID":0,"VALID":1})
    vmodel=BertForSequenceClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    vds=ValidityDataset(examples,train,vtok)
    coll=DataCollatorWithPadding(tokenizer=vtok,return_tensors="pt")
    vdir=args.out/"validity_trainer"
    vargs=TrainingArguments(output_dir=str(vdir),seed=SEED,data_seed=SEED,
        learning_rate=2e-5,weight_decay=.01,warmup_steps=0,max_grad_norm=1.0,
        lr_scheduler_type="linear",per_device_train_batch_size=16,
        num_train_epochs=3,evaluation_strategy="no",save_strategy="epoch",
        load_best_model_at_end=False,save_total_limit=3,logging_strategy="steps",logging_steps=10,
        report_to=[],disable_tqdm=True,save_safetensors=True,dataloader_num_workers=0)
    vt=Trainer(model=vmodel,args=vargs,train_dataset=vds,tokenizer=vtok,data_collator=coll,
        callbacks=[ProgressCallback(status,"SPAN_VALIDITY_GUARD",0.0,3.0,4.0)])
    tr=vt.train()
    vsel=args.out/"validity_model"
    vt.model.save_pretrained(vsel,safe_serialization=True); vtok.save_pretrained(vsel)
    if any(not torch.isfinite(p).all() for p in vt.model.parameters()): raise RuntimeError("non-finite validity model")

    atomic_json_write(status,{"state":"RUNNING","progress_percent":75.0,
        "current_stage":"FROZEN_DEV_CALIBRATION","active_module":"CONSENSUS_PLUS_VALIDITY",
        "completed_units":3,"total_units":4,"last_successful_checkpoint":str(vsel),
        "last_progress_at":datetime.now(timezone.utc).isoformat(),
        "next_expected_step":"CALIBRATE_EXISTING_THRESHOLD_GRID","failure_or_stall_reason":None})

    # Frozen R4.2C boundary predictions.
    btok=AutoTokenizer.from_pretrained(args.boundary_model_dir,local_files_only=True,use_fast=True)
    bmodel=BertForTokenClassification.from_pretrained(args.boundary_model_dir,local_files_only=True)
    bdev=BoundaryDataset(dev,btok)
    barg=TrainingArguments(output_dir=str(args.out/"boundary_predict"),per_device_eval_batch_size=8,report_to=[],disable_tqdm=True)
    bp=Trainer(model=bmodel,args=barg,tokenizer=btok).predict(bdev)
    start_probs,end_probs=boundary_probs(bp.predictions,bdev)

    # Frozen R4.2B candidates.
    rtok=AutoTokenizer.from_pretrained(args.r4b_model_dir,local_files_only=True,use_fast=True)
    rmodel=BertForTokenClassification.from_pretrained(args.r4b_model_dir,local_files_only=True)
    rdev=R4BDataset(dev,rtok)
    rarg=TrainingArguments(output_dir=str(args.out/"r4b_predict"),per_device_eval_batch_size=8,report_to=[],disable_tqdm=True)
    rp=Trainer(model=rmodel,args=rarg,tokenizer=rtok).predict(rdev)
    seqs=word_r4b_predictions(rp.predictions,rdev)
    candidates=[]
    for si,(tags,conf) in enumerate(seqs):
        for e in predicted_entities(tags,conf):
            e["sentence_index"]=si; candidates.append(e)

    # Frozen R4.2C type probabilities.
    ttok=AutoTokenizer.from_pretrained(args.type_model_dir,local_files_only=True,use_fast=True)
    tmodel=BertForSequenceClassification.from_pretrained(args.type_model_dir,local_files_only=True)
    cds=CandidateSpanDataset(candidates,dev,ttok)
    tcoll=DataCollatorWithPadding(tokenizer=ttok,return_tensors="pt")
    targ=TrainingArguments(output_dir=str(args.out/"type_predict"),per_device_eval_batch_size=16,report_to=[],disable_tqdm=True)
    tp=Trainer(model=tmodel,args=targ,tokenizer=ttok,data_collator=tcoll).predict(cds)
    type_probs=1.0/(1.0+np.exp(-tp.predictions))

    # New validity probabilities on exactly the same candidates.
    vcds=CandidateSpanDataset(candidates,dev,vtok)
    varg2=TrainingArguments(output_dir=str(args.out/"validity_predict"),per_device_eval_batch_size=16,report_to=[],disable_tqdm=True)
    vp=Trainer(model=vt.model,args=varg2,tokenizer=vtok,data_collator=coll).predict(vcds)
    valid_probs=torch.softmax(torch.tensor(vp.predictions),dim=-1).numpy()[:,1]

    cals=calibrate(dev,candidates,start_probs,end_probs,type_probs,valid_probs)
    chosen=next((x for x in cals if x["passes"]),None)
    state="R4_2D_SPAN_VALIDITY_CALIBRATED" if chosen else "R4_2D_SPAN_VALIDITY_NOT_READY"
    summary={
        "experiment":"R4_2D_HARD_NEGATIVE_SPAN_VALIDITY_DEV_ONLY",
        "state":state,"seed":SEED,
        "training":{
            "dataset":counts,
            "epochs":3,"learning_rate":2e-5,"weight_decay":.01,"batch":16,
            "global_step":int(vt.state.global_step),
            "train_metrics":{k:(float(v) if isinstance(v,(int,float)) else v) for k,v in tr.metrics.items()},
        },
        "validity":{"threshold":VALIDITY_THRESHOLD,"model_sha256":sha256_path(vsel/"model.safetensors")},
        "frozen_components":{
            "r4b_model_sha256":EXPECTED_R4B_MODEL_SHA,
            "r4_2c_boundary_model_sha256":EXPECTED_R42C_BOUNDARY_SHA,
            "r4_2c_type_model_sha256":EXPECTED_R42C_TYPE_SHA,
            "converted_base_sha256":EXPECTED_CONVERTED_SHA,
        },
        "candidate_count":len(candidates),
        "threshold_grid":THRESHOLDS,
        "calibration_candidates":cals,
        "chosen_calibration":chosen,
        "guards":{
            "test_files_read":False,"factpico_used":False,"consumed_60_rct_holdout_used":False,
            "opened_30_rct_diagnostic_used":False,"old_threshold_grid_changed":False,
            "validity_threshold_changed":False,"dev_hard_negatives_used_for_training":False,
            "pickle_weight_loaded":False,"final_weights_safetensors":True,
        },
        "stop_boundary":"STOP_BEFORE_EBM_COVID_AD_TEST_INFERENCE",
    }
    atomic_json_write(args.out/"R4_2D_TRAIN_CALIBRATION_SUMMARY.json",summary)
    atomic_json_write(status,{"state":"COMPLETED" if chosen else "COMPLETED_WITH_GATE_FAIL",
        "progress_percent":100.0,"current_stage":"CALIBRATION_COMPLETE","active_module":"CONSENSUS_PLUS_VALIDITY",
        "completed_units":4,"total_units":4,"last_successful_checkpoint":"R4_2D_TRAIN_CALIBRATION_SUMMARY.json",
        "last_progress_at":datetime.now(timezone.utc).isoformat(),
        "next_expected_step":"STOP_AND_REQUEST_EXTERNAL_TEST_AUTHORIZATION" if chosen else "STOP_AND_ANALYZE_R4_2D_DEV_ONLY_FAILURE",
        "failure_or_stall_reason":None if chosen else "FROZEN_DEV_R4_2D_GATE_NOT_MET",
        "witness_state":state})
    print(json.dumps(summary,indent=2,sort_keys=True))
    if chosen is None: raise SystemExit(2)

if __name__=="__main__":
    main()
