#!/usr/bin/env python3
from __future__ import annotations

import argparse, gc, hashlib, json, math, os, pathlib, random, sys, time
from collections import Counter
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import (
    AutoConfig, AutoTokenizer, BertModel, BertForTokenClassification,
    BertForSequenceClassification, DataCollatorWithPadding,
    Trainer, TrainerCallback, TrainingArguments
)

from r43_contextual_pair_preflight import (
    parse_train, spans_for_sentence, LABELS as SPAN_CLASSES
)

SEED=42
BIO_LABELS=["O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"]
BIO2ID={x:i for i,x in enumerate(BIO_LABELS)}
BOUNDARY_LABELS=["OUT","START","END","BOTH","IN"]
BOUNDARY2ID={x:i for i,x in enumerate(BOUNDARY_LABELS)}
SPAN2ID={x:i for i,x in enumerate(SPAN_CLASSES)}

EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_SPLIT_SHA="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226"
EXPECTED_CONVERTED_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"

def now():
    return datetime.now(timezone.utc).isoformat()

def sha256_path(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def seed_all():
    os.environ["PYTHONHASHSEED"]=str(SEED)
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True,warn_only=True)
    torch.set_num_threads(2)

def write_json(path,obj):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,p)

class Progress(TrainerCallback):
    def __init__(self,status_path,module,offset,width,total=16):
        self.path=pathlib.Path(status_path); self.module=module
        self.offset=offset; self.width=width; self.total=total
        self.started=time.time(); self.last=-1; self.latest_loss=None
    def emit(self,state,stage,force=False):
        step=int(state.global_step or 0); totalsteps=int(state.max_steps or 0)
        if not force and step==self.last: return
        frac=step/totalsteps if totalsteps else 0.0
        units=self.offset+self.width*frac
        payload={
            "state":"RUNNING","current_stage":stage,"active_module":self.module,
            "progress_percent":round(100*units/self.total,2),
            "completed_units":round(units,4),"total_units":self.total,
            "current_epoch":float(state.epoch or 0.0),
            "global_step":step,"total_steps":totalsteps or None,
            "latest_loss":self.latest_loss,
            "elapsed_seconds":round(time.time()-self.started,1),
            "last_progress_at":now(),"failure_or_stall_reason":None,
            "next_expected_step":f"CONTINUE_{self.module}"
        }
        write_json(self.path,payload)
        print("PROCESS_STATUS "+json.dumps(payload,sort_keys=True),file=sys.stderr,flush=True)
        self.last=step
    def on_step_end(self,args,state,control,**kwargs):
        if int(state.global_step or 0)%10==0: self.emit(state,"TRAINING")
    def on_log(self,args,state,control,logs=None,**kwargs):
        if logs and isinstance(logs.get("loss"),(int,float)): self.latest_loss=float(logs["loss"])
        self.emit(state,"TRAINING_LOG",True)
    def on_train_end(self,args,state,control,**kwargs):
        self.emit(state,"MODULE_TRAINING_COMPLETE",True)

class TokenDataset(torch.utils.data.Dataset):
    def __init__(self,rows,tokenizer,label_mode):
        self.items=[]
        for tokens,tags,boundary in rows:
            enc=tokenizer(tokens,is_split_into_words=True,truncation=True,max_length=256,
                          padding="max_length",return_attention_mask=True)
            wids=enc.word_ids(); seen=set(); labs=[]; first=[]
            target=tags if label_mode=="bio" else boundary
            mapper=BIO2ID if label_mode=="bio" else BOUNDARY2ID
            for pos,wid in enumerate(wids):
                if wid is None: labs.append(-100)
                elif wid not in seen:
                    seen.add(wid); first.append(pos); labs.append(mapper[target[wid]])
                else: labs.append(-100)
            if len(first)!=len(tokens):
                raise RuntimeError(f"{label_mode} truncation {len(first)} != {len(tokens)}")
            enc["labels"]=labs
            self.items.append({k:torch.tensor(v) for k,v in enc.items()})
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

class SpanDataset(torch.utils.data.Dataset):
    def __init__(self,rows,tokenizer):
        self.items=[]
        for tokens,typ,s,e in rows:
            piece=tokens[s:e]
            if e<=s or e-s>64: raise RuntimeError("bad span width")
            enc=tokenizer(piece,is_split_into_words=True,truncation=False)
            lab=[0.0]*len(SPAN_CLASSES); lab[SPAN2ID[typ]]=1.0
            enc["labels"]=lab
            self.items.append(enc)
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

def boundary_tags(n,spans):
    y=["OUT"]*n
    for _,s,e in spans:
        if e<=s: continue
        if e-s==1: y[s]="BOTH"
        else:
            y[s]="START"; y[e-1]="END"
            for i in range(s+1,e-1): y[i]="IN"
    return y

def convert_base(model_dir,out):
    seed_all()
    base=BertModel.from_pretrained(model_dir,from_flax=True,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in base.parameters()): raise RuntimeError("nonfinite base")
    out=pathlib.Path(out); out.mkdir(parents=True,exist_ok=False)
    base.save_pretrained(out,safe_serialization=True)
    tok=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,use_fast=True)
    tok.save_pretrained(out)
    got=sha256_path(out/"model.safetensors")
    if got!=EXPECTED_CONVERTED_SHA: raise RuntimeError(f"converted base mismatch {got}")
    del base; gc.collect()
    return tok

def train_token(name,converted,ds,out_dir,lr,wd,epochs,batch,status,offset,width):
    seed_all()
    labels=BIO_LABELS if name=="B_CANDIDATE" else BOUNDARY_LABELS
    mapper=BIO2ID if name=="B_CANDIDATE" else BOUNDARY2ID
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=len(labels),
        id2label={i:x for i,x in enumerate(labels)},label2id=mapper)
    model=BertForTokenClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    ta=TrainingArguments(output_dir=str(out_dir/"trainer"),seed=SEED,data_seed=SEED,
        learning_rate=lr,weight_decay=wd,warmup_steps=0,max_grad_norm=1.0,
        lr_scheduler_type="linear",per_device_train_batch_size=batch,
        num_train_epochs=epochs,evaluation_strategy="no",save_strategy="no",
        logging_strategy="steps",logging_steps=10,load_best_model_at_end=False,
        report_to=[],disable_tqdm=True,save_safetensors=True,dataloader_num_workers=0)
    tr=Trainer(model=model,args=ta,train_dataset=ds,tokenizer=AutoTokenizer.from_pretrained(converted,local_files_only=True,use_fast=True),
               callbacks=[Progress(status,name,offset,width)])
    res=tr.train()
    out_dir.mkdir(parents=True,exist_ok=True)
    tr.save_model(out_dir); tr.tokenizer.save_pretrained(out_dir)
    if not (out_dir/"model.safetensors").exists(): raise RuntimeError("missing safetensors")
    got=sha256_path(out_dir/"model.safetensors")
    info={"epochs":epochs,"global_step":int(tr.state.global_step),"train_loss":float(res.training_loss),"model_sha256":got}
    del tr,model; gc.collect()
    return info

def train_type(converted,ds,out_dir,status):
    seed_all()
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=len(SPAN_CLASSES),
        id2label={i:x for i,x in enumerate(SPAN_CLASSES)},label2id=SPAN2ID,
        problem_type="multi_label_classification")
    model=BertForSequenceClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    tok=AutoTokenizer.from_pretrained(converted,local_files_only=True,use_fast=True)
    coll=DataCollatorWithPadding(tokenizer=tok,return_tensors="pt")
    ta=TrainingArguments(output_dir=str(out_dir/"trainer"),seed=SEED,data_seed=SEED,
        learning_rate=2e-5,weight_decay=.01,warmup_steps=0,max_grad_norm=1.0,
        lr_scheduler_type="linear",per_device_train_batch_size=16,
        num_train_epochs=3,evaluation_strategy="no",save_strategy="no",
        logging_strategy="steps",logging_steps=10,load_best_model_at_end=False,
        report_to=[],disable_tqdm=True,save_safetensors=True,dataloader_num_workers=0)
    tr=Trainer(model=model,args=ta,train_dataset=ds,tokenizer=tok,data_collator=coll,
               callbacks=[Progress(status,"C_TYPE",13,3)])
    res=tr.train()
    out_dir.mkdir(parents=True,exist_ok=True)
    tr.save_model(out_dir); tok.save_pretrained(out_dir)
    got=sha256_path(out_dir/"model.safetensors")
    info={"epochs":3,"global_step":int(tr.state.global_step),"train_loss":float(res.training_loss),"model_sha256":got}
    del tr,model; gc.collect()
    return info

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--split-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=False)
    status=args.out/"PROCESS_STATUS.json"

    if sha256_path(args.train)!=EXPECTED_TRAIN_SHA: raise RuntimeError("train hash mismatch")
    manifest=json.loads(args.split_manifest.read_text())
    if manifest.get("manifest_sha256")!=EXPECTED_SPLIT_SHA: raise RuntimeError("split manifest identity mismatch")
    fit_ids=set()
    for e in manifest["entries"]:
        if e["partition"]=="FIT": fit_ids.update(e["documents"])
    if len(fit_ids)!=320: raise RuntimeError(f"FIT doc count mismatch {len(fit_ids)}")

    docs,empty,bad=parse_train(args.train)
    if bad: raise RuntimeError(f"bad source lines {bad[:3]}")
    if len(docs)!=400: raise RuntimeError("document count mismatch")

    token_rows=[]; span_rows=[]; counts=Counter()
    for di in sorted(fit_ids):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            sps,badbio,_=spans_for_sentence(doc,si)
            if badbio: raise RuntimeError(f"BIO issue doc{di} sent{si}: {badbio}")
            btags=boundary_tags(len(tokens),sps)
            token_rows.append((tokens,tags,btags))
            for typ,s,e in sps:
                span_rows.append((tokens,typ,s,e)); counts[typ]+=1

    if len(token_rows)!=1292: raise RuntimeError(f"FIT sentence mismatch {len(token_rows)}")
    if len(span_rows)!=2371: raise RuntimeError(f"FIT span mismatch {len(span_rows)}")
    want={"P":342,"I":1038,"C":144,"O":847}
    if dict(counts)!=want: raise RuntimeError(f"FIT class mismatch {dict(counts)}")

    write_json(status,{"state":"RUNNING","progress_percent":0.0,"current_stage":"INITIALIZING",
        "active_module":"FIT_ANCESTORS","completed_units":0,"total_units":16,
        "last_progress_at":now(),"failure_or_stall_reason":None})

    converted=args.out/"converted_base"
    tok=convert_base(args.model_dir,converted)
    bds=TokenDataset(token_rows,tok,"bio")
    binfo=train_token("B_CANDIDATE",converted,bds,args.out/"b_candidate",5e-5,0.0,10,8,status,0,10)
    del bds; gc.collect()

    bndds=TokenDataset(token_rows,tok,"boundary")
    bndinfo=train_token("C_BOUNDARY",converted,bndds,args.out/"c_boundary",5e-5,.01,3,8,status,10,3)
    del bndds; gc.collect()

    sds=SpanDataset(span_rows,tok)
    tinfo=train_type(converted,sds,args.out/"c_type",status)

    summary={
      "state":"R43_FIT_ANCESTORS_COMPLETE",
      "seed":SEED,
      "train_sha256":EXPECTED_TRAIN_SHA,
      "split_manifest_sha256":EXPECTED_SPLIT_SHA,
      "fit":{"documents":len(fit_ids),"sentences":len(token_rows),"gold_total":len(span_rows),"gold_counts":want},
      "models":{"B_CANDIDATE":binfo,"C_BOUNDARY":bndinfo,"C_TYPE":tinfo},
      "converted_base_sha256":EXPECTED_CONVERTED_SHA,
      "guards":{"fit_only_training":True,"select_used_for_training":False,"historical_dev_read":False,
        "test_read":False,"other_folds_read":False,"factpico_used":False,"consumed_60_rct_holdout_used":False,
        "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY"},
      "next_action":"FREEZE_ANCESTORS_THEN_RUN_FROZEN_H0_VS_H1_SELECT_DIAGNOSTIC"
    }
    write_json(args.out/"R43_FIT_ANCESTORS_SUMMARY.json",summary)
    write_json(status,{"state":"COMPLETED","progress_percent":100.0,"current_stage":"FIT_ANCESTORS_COMPLETE",
        "active_module":"FIT_ANCESTORS","completed_units":16,"total_units":16,
        "last_progress_at":now(),"failure_or_stall_reason":None,
        "next_expected_step":"FREEZE_ANCESTORS_THEN_RUN_FROZEN_H0_VS_H1_SELECT_DIAGNOSTIC"})
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
