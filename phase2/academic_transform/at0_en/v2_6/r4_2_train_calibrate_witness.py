#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import random
from dataclasses import dataclass

import numpy as np
import torch
from seqeval.metrics import classification_report
from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

SEED = 20261005
LABELS = ["O", "B-P", "I-P", "B-I", "I-I", "B-C", "I-C", "B-O", "I-O"]
LABEL2ID = {x:i for i,x in enumerate(LABELS)}
ID2LABEL = {i:x for x,i in LABEL2ID.items()}
THRESHOLDS = [0.80, 0.85, 0.90, 0.95]

def sha256_path(path:pathlib.Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def seed_all():
    os.environ["PYTHONHASHSEED"]=str(SEED)
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True, warn_only=True)
    torch.set_num_threads(2)

def read_conll(path:pathlib.Path):
    sentences=[]
    tokens=[]
    tags=[]
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.rstrip("\n")
        if not line.strip():
            if tokens:
                sentences.append((tokens,tags))
                tokens=[]; tags=[]
            continue
        parts=line.split("\t")
        if len(parts)!=2:
            parts=line.rsplit(None,1)
        if len(parts)!=2:
            raise RuntimeError(f"bad CoNLL line in {path}: {line!r}")
        tok,tag=parts
        if tok=="-DOCSTART-":
            if tokens:
                sentences.append((tokens,tags))
                tokens=[]; tags=[]
            continue
        if tag not in LABEL2ID:
            raise RuntimeError(f"unknown label {tag!r}")
        tokens.append(tok)
        tags.append(tag)
    if tokens:
        sentences.append((tokens,tags))
    return sentences

class TokenDataset(torch.utils.data.Dataset):
    def __init__(self, sentences, tokenizer, max_length=256):
        self.sentences=sentences
        self.items=[]
        for tokens,tags in sentences:
            enc=tokenizer(
                tokens,
                is_split_into_words=True,
                truncation=True,
                max_length=max_length,
                padding="max_length",
                return_attention_mask=True,
            )
            word_ids=enc.word_ids()
            label_ids=[]
            prev=None
            for wid in word_ids:
                if wid is None:
                    label_ids.append(-100)
                elif wid!=prev:
                    label_ids.append(LABEL2ID[tags[wid]])
                else:
                    label_ids.append(-100)
                prev=wid
            enc["labels"]=label_ids
            self.items.append({k:torch.tensor(v) for k,v in enc.items()})
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

def word_sequences(logits, labels):
    probs=np.exp(logits-logits.max(axis=-1,keepdims=True))
    probs=probs/probs.sum(axis=-1,keepdims=True)
    pred_ids=logits.argmax(axis=-1)
    gold_all=[]; pred_all=[]; conf_all=[]
    for p,g,pr in zip(pred_ids,labels,probs):
        gt=[]; pt=[]; cf=[]
        for pi,gi,pvec in zip(p,g,pr):
            if gi==-100:
                continue
            gt.append(ID2LABEL[int(gi)])
            pt.append(ID2LABEL[int(pi)])
            cf.append(float(pvec[int(pi)]))
        gold_all.append(gt); pred_all.append(pt); conf_all.append(cf)
    return gold_all,pred_all,conf_all

def raw_metrics_from_logits(logits, labels):
    gold,pred,_=word_sequences(logits,labels)
    rep=classification_report(gold,pred,output_dict=True,zero_division=0)
    per={}
    for cls in ["P","I","C","O"]:
        d=rep.get(cls,{})
        per[cls]={
            "precision":float(d.get("precision",0.0)),
            "recall":float(d.get("recall",0.0)),
            "f1":float(d.get("f1-score",0.0)),
            "support":int(d.get("support",0)),
        }
    macro_f1=sum(per[x]["f1"] for x in per)/4.0
    macro_precision=sum(per[x]["precision"] for x in per)/4.0
    micro=rep.get("micro avg",{})
    return {
        "per_class":per,
        "macro_f1":macro_f1,
        "macro_precision":macro_precision,
        "micro_f1":float(micro.get("f1-score",0.0)),
        "micro_precision":float(micro.get("precision",0.0)),
        "micro_recall":float(micro.get("recall",0.0)),
    }

def compute_metrics(eval_pred):
    m=raw_metrics_from_logits(eval_pred.predictions,eval_pred.label_ids)
    return {
        "macro_f1":m["macro_f1"],
        "micro_f1":m["micro_f1"],
        "macro_precision":m["macro_precision"],
    }

def entities(tags, confidences=None):
    out=[]
    cur=None
    for i,tag in enumerate(tags+["O"]):
        if tag=="O":
            typ=None; pref="O"
        else:
            pref,typ=tag.split("-",1)
        if cur is not None:
            ctyp,start,vals=cur
            if pref=="I" and typ==ctyp:
                if confidences is not None and i<len(confidences):
                    vals.append(confidences[i])
                continue
            conf=min(vals) if vals else 1.0
            out.append((ctyp,start,i,conf))
            cur=None
        if tag!="O":
            vals=[]
            if confidences is not None and i<len(confidences):
                vals=[confidences[i]]
            cur=(typ,i,vals)
    return out

def calibration_metrics(gold_tags,pred_tags,pred_conf,threshold):
    counts={c:{"tp":0,"fp":0,"fn":0,"accepted":0,"gold":0} for c in ["P","I","C","O"]}
    for gt,pt,cf in zip(gold_tags,pred_tags,pred_conf):
        gold={(c,s,e) for c,s,e,_ in entities(gt)}
        pred={(c,s,e):conf for c,s,e,conf in entities(pt,cf) if conf>=threshold}
        for c,s,e in gold:
            counts[c]["gold"]+=1
        for key,conf in pred.items():
            c=key[0]
            counts[c]["accepted"]+=1
            if key in gold: counts[c]["tp"]+=1
            else: counts[c]["fp"]+=1
        for key in gold:
            if key not in pred:
                counts[key[0]]["fn"]+=1
    per={}
    for c,d in counts.items():
        p=d["tp"]/(d["tp"]+d["fp"]) if d["tp"]+d["fp"] else 0.0
        r=d["tp"]/(d["tp"]+d["fn"]) if d["tp"]+d["fn"] else 0.0
        per[c]={**d,"precision":p,"recall":r}
    macro_precision=sum(per[c]["precision"] for c in per)/4.0
    passes=(
        all(per[c]["precision"]>=0.90 for c in per)
        and all(per[c]["precision"]>=0.85 for c in per)
        and all(per[c]["recall"]>=0.20 for c in per)
        and all(per[c]["accepted"]>=10 for c in per)
        and macro_precision>=0.90
    )
    return {"threshold":threshold,"per_class":per,"macro_precision":macro_precision,"passes":passes}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    seed_all()
    args.out.mkdir(parents=True,exist_ok=False)

    train_s=read_conll(args.train)
    dev_s=read_conll(args.dev)
    tokenizer=AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True,use_fast=True)
    cfg=AutoConfig.from_pretrained(
        args.model_dir,
        local_files_only=True,
        num_labels=len(LABELS),
        label2id=LABEL2ID,
        id2label=ID2LABEL,
    )
    model=AutoModelForTokenClassification.from_pretrained(
        args.model_dir,
        from_flax=True,
        local_files_only=True,
        config=cfg,
    )
    train_ds=TokenDataset(train_s,tokenizer)
    dev_ds=TokenDataset(dev_s,tokenizer)

    work=args.out/"trainer"
    ta=TrainingArguments(
        output_dir=str(work),
        seed=SEED,
        data_seed=SEED,
        learning_rate=5e-5,
        weight_decay=0.01,
        warmup_ratio=0.10,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        gradient_accumulation_steps=1,
        num_train_epochs=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        report_to=[],
        disable_tqdm=True,
        save_safetensors=True,
        dataloader_num_workers=0,
    )
    trainer=Trainer(
        model=model,
        args=ta,
        train_dataset=train_ds,
        eval_dataset=dev_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )
    train_result=trainer.train()

    selected=args.out/"selected_model"
    trainer.save_model(selected)
    tokenizer.save_pretrained(selected)
    if not (selected/"model.safetensors").exists():
        raise RuntimeError("final model was not saved as safetensors")

    pred=trainer.predict(dev_ds)
    raw=raw_metrics_from_logits(pred.predictions,pred.label_ids)
    gold,pred_tags,conf=word_sequences(pred.predictions,pred.label_ids)
    calibrations=[calibration_metrics(gold,pred_tags,conf,t) for t in THRESHOLDS]
    chosen=next((x for x in calibrations if x["passes"]),None)
    state="R4_2_WITNESS_CALIBRATED" if chosen else "R4_2_WITNESS_NOT_READY"

    files={}
    for p in sorted(selected.iterdir()):
        if p.is_file():
            files[p.name]={"sha256":sha256_path(p),"bytes":p.stat().st_size}

    summary={
        "state":state,
        "seed":SEED,
        "labels":LABELS,
        "train_sentences":len(train_s),
        "dev_sentences":len(dev_s),
        "training":{
            "max_epochs":10,
            "learning_rate":5e-5,
            "weight_decay":0.01,
            "warmup_ratio":0.10,
            "train_batch_size":8,
            "eval_batch_size":16,
            "gradient_accumulation":1,
            "early_stopping_patience":2,
            "best_model_checkpoint":trainer.state.best_model_checkpoint,
            "best_metric":trainer.state.best_metric,
            "global_step":trainer.state.global_step,
            "train_loss":float(train_result.training_loss),
        },
        "dev_raw_metrics":raw,
        "calibration_candidates":calibrations,
        "chosen_calibration":chosen,
        "selected_model_files":files,
        "guards":{
            "test_files_read":False,
            "factpico_used":False,
            "consumed_60_rct_holdout_used":False,
            "opened_30_rct_diagnostic_used":False,
            "pickle_weight_loaded":False,
            "final_weights_safetensors":True,
        },
        "stop_boundary":"STOP_BEFORE_EBM_COVID_AD_TEST_INFERENCE",
    }
    rawj=json.dumps(summary,sort_keys=True,separators=(",",":")).encode()
    summary["canonical_pre_hash_sha256"]=hashlib.sha256(rawj).hexdigest()
    (args.out/"R4_2_TRAIN_CALIBRATION_SUMMARY.json").write_text(
        json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8"
    )
    print(json.dumps(summary,indent=2,sort_keys=True))
    if chosen is None:
        raise SystemExit(2)

if __name__=="__main__":
    main()
