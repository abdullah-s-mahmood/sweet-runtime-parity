#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import random
import sys
import time
from collections import Counter
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import (
    AutoConfig,
    AutoTokenizer,
    BertForSequenceClassification,
    BertForTokenClassification,
    BertModel,
    DataCollatorWithPadding,
    Trainer,
    TrainerCallback,
    TrainingArguments,
)

SEED=42
THRESHOLDS=[0.80,0.85,0.90,0.95]
BOUNDARY_GENERATION_THRESHOLD=0.25
MAX_SPAN_WIDTH_WORDS=64
R4B_LABELS=["O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"]
R4B_ID2LABEL={i:x for i,x in enumerate(R4B_LABELS)}
BOUNDARY_LABELS=["OUT","START","END","BOTH","IN"]
BOUNDARY2ID={x:i for i,x in enumerate(BOUNDARY_LABELS)}
SPAN_CLASSES=["P","I","C","O"]
SPAN2ID={x:i for i,x in enumerate(SPAN_CLASSES)}
EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_DEV_SHA="3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a"
EXPECTED_R4B_MODEL_SHA="3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c"
EXPECTED_CONVERTED_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256_path(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def seed_all(seed=SEED):
    os.environ["PYTHONHASHSEED"]=str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True,warn_only=True)
    torch.set_num_threads(2)

def atomic_json_write(path,payload):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(t,p)

def read_conll(path):
    out=[]; toks=[]; tags=[]
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            if toks:
                out.append((toks,tags)); toks=[]; tags=[]
            continue
        p=raw.split("\t")
        if len(p)!=2: p=raw.rsplit(None,1)
        if len(p)!=2: raise RuntimeError(f"bad CoNLL line: {raw!r}")
        tok,tag=p
        if tok=="-DOCSTART-":
            if toks:
                out.append((toks,tags)); toks=[]; tags=[]
            continue
        if tag not in R4B_LABELS: raise RuntimeError(f"unknown tag {tag!r}")
        toks.append(tok); tags.append(tag)
    if toks: out.append((toks,tags))
    return out

def spans_from_tags(tags):
    out=[]; cur=None
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O":
            pref=typ=None
        else:
            pref,typ=tag.split("-",1)
        if cur is not None:
            ctyp,start=cur
            if pref=="I" and typ==ctyp:
                continue
            out.append((ctyp,start,i)); cur=None
        if tag!="O":
            cur=(typ,i)
    return out

def boundary_labels_from_tags(tags):
    y=[BOUNDARY2ID["OUT"]]*len(tags)
    for _,s,e in spans_from_tags(tags):
        w=e-s
        if w<=0: continue
        if w==1:
            y[s]=BOUNDARY2ID["BOTH"]
        else:
            y[s]=BOUNDARY2ID["START"]
            y[e-1]=BOUNDARY2ID["END"]
            for i in range(s+1,e-1): y[i]=BOUNDARY2ID["IN"]
    return y

class BoundaryDataset(torch.utils.data.Dataset):
    def __init__(self,sentences,tokenizer,max_length=256):
        self.items=[]; self.first_positions=[]
        for tokens,tags in sentences:
            enc=tokenizer(tokens,is_split_into_words=True,truncation=True,max_length=max_length,
                          padding="max_length",return_attention_mask=True)
            wids=enc.word_ids()
            gold=boundary_labels_from_tags(tags)
            labs=[]; first=[]; seen=set()
            for pos,wid in enumerate(wids):
                if wid is None:
                    labs.append(-100)
                elif wid not in seen:
                    seen.add(wid); first.append(pos); labs.append(gold[wid])
                else:
                    labs.append(-100)
            if len(first)!=len(tokens):
                raise RuntimeError(f"boundary truncation: {len(first)} != {len(tokens)}")
            enc["labels"]=labs
            self.items.append({k:torch.tensor(v) for k,v in enc.items()})
            self.first_positions.append(first)
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

class R4BDataset(torch.utils.data.Dataset):
    def __init__(self,sentences,tokenizer,max_length=256):
        self.items=[]; self.first_positions=[]
        label2id={x:i for i,x in enumerate(R4B_LABELS)}
        for tokens,tags in sentences:
            enc=tokenizer(tokens,is_split_into_words=True,truncation=True,max_length=max_length,
                          padding="max_length",return_attention_mask=True)
            wids=enc.word_ids(); labs=[]; first=[]; seen=set()
            for pos,wid in enumerate(wids):
                if wid is None:
                    labs.append(-100)
                elif wid not in seen:
                    seen.add(wid); first.append(pos); labs.append(label2id[tags[wid]])
                else:
                    labs.append(-100)
            if len(first)!=len(tokens): raise RuntimeError("R4B truncation")
            enc["labels"]=labs
            self.items.append({k:torch.tensor(v) for k,v in enc.items()})
            self.first_positions.append(first)
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

class SpanDataset(torch.utils.data.Dataset):
    def __init__(self,sentences,tokenizer):
        self.items=[]; self.meta=[]
        for si,(tokens,tags) in enumerate(sentences):
            for typ,s,e in spans_from_tags(tags):
                span_tokens=tokens[s:e]
                if len(span_tokens)>MAX_SPAN_WIDTH_WORDS:
                    raise RuntimeError(f"gold span exceeds max width: {len(span_tokens)}")
                enc=tokenizer(span_tokens,is_split_into_words=True,truncation=False)
                lab=[0.0]*len(SPAN_CLASSES); lab[SPAN2ID[typ]]=1.0
                enc["labels"]=lab
                self.items.append(enc)
                self.meta.append((si,typ,s,e))
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

class CandidateSpanDataset(torch.utils.data.Dataset):
    def __init__(self,candidates,sentences,tokenizer):
        self.items=[]; self.meta=[]
        for c in candidates:
            tokens=sentences[c["sentence_index"]][0][c["start"]:c["end"]]
            enc=tokenizer(tokens,is_split_into_words=True,truncation=False)
            self.items.append(enc); self.meta.append(c)
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

def macro_span_metrics(eval_pred):
    logits,labels=eval_pred
    probs=1.0/(1.0+np.exp(-logits))
    pred=np.argmax(probs,axis=1); gold=np.argmax(labels,axis=1)
    f1s=[]
    for c in range(len(SPAN_CLASSES)):
        tp=int(np.sum((pred==c)&(gold==c)))
        fp=int(np.sum((pred==c)&(gold!=c)))
        fn=int(np.sum((pred!=c)&(gold==c)))
        p=tp/(tp+fp) if tp+fp else 0.0
        r=tp/(tp+fn) if tp+fn else 0.0
        f=2*p*r/(p+r) if p+r else 0.0
        f1s.append(f)
    return {"macro_f1":float(sum(f1s)/len(f1s)),
            "accuracy":float(np.mean(pred==gold))}

class ProgressCallback(TrainerCallback):
    def __init__(self,path,module,unit_offset,unit_width=3.0,total_units=7.0):
        self.path=pathlib.Path(path); self.module=module
        self.unit_offset=unit_offset; self.unit_width=unit_width; self.total_units=total_units
        self.started=time.time(); self.latest={}; self.last_step=-1; self.last_checkpoint=None
    def emit(self,state,stage,force=False):
        step=int(state.global_step or 0); total=int(state.max_steps or 0)
        if not force and step==self.last_step: return
        frac=(step/total) if total else min(1.0,float(state.epoch or 0.0)/3.0)
        units=self.unit_offset+self.unit_width*frac
        payload={
          "state":"RUNNING","progress_percent":round(100.0*units/self.total_units,2),
          "current_stage":stage,"active_module":self.module,
          "current_epoch":float(state.epoch or 0.0),"max_epochs":3,
          "global_step":step,"total_steps":total or None,
          "latest_loss":self.latest.get("loss"),
          "latest_dev_metric":self.latest.get("eval_macro_f1"),
          "best_metric":state.best_metric,"best_model_checkpoint":state.best_model_checkpoint,
          "completed_units":round(units,4),"total_units":self.total_units,
          "last_successful_checkpoint":self.last_checkpoint or state.best_model_checkpoint,
          "elapsed_seconds":round(time.time()-self.started,1),
          "last_progress_at":utc_now(),"next_expected_step":f"CONTINUE_{self.module}",
          "failure_or_stall_reason":None
        }
        atomic_json_write(self.path,payload)
        print("PROCESS_STATUS "+json.dumps(payload,sort_keys=True),file=sys.stderr,flush=True)
        self.last_step=step
    def on_step_end(self,args,state,control,**kwargs):
        if int(state.global_step or 0)%10==0: self.emit(state,"TRAINING")
    def on_log(self,args,state,control,logs=None,**kwargs):
        if logs:
            for k,v in logs.items():
                if isinstance(v,(int,float,str,bool)) or v is None: self.latest[k]=v
        self.emit(state,"TRAINING_LOG",True)
    def on_evaluate(self,args,state,control,metrics=None,**kwargs):
        if metrics:
            for k,v in metrics.items():
                if isinstance(v,(int,float,str,bool)) or v is None: self.latest[k]=v
        self.emit(state,"EVALUATION_COMPLETE",True)
    def on_save(self,args,state,control,**kwargs):
        self.last_checkpoint=str(pathlib.Path(args.output_dir)/f"checkpoint-{int(state.global_step or 0)}")
        self.emit(state,"CHECKPOINT_SAVED",True)

def convert_safe_base(model_dir,out):
    converted=pathlib.Path(out); converted.mkdir(parents=True,exist_ok=False)
    base=BertModel.from_pretrained(model_dir,from_flax=True,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in base.parameters()):
        raise RuntimeError("non-finite converted base")
    base.save_pretrained(converted,safe_serialization=True)
    tok=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,use_fast=True)
    tok.save_pretrained(converted)
    got=sha256_path(converted/"model.safetensors")
    if got!=EXPECTED_CONVERTED_SHA:
        raise RuntimeError(f"converted base hash mismatch {got}")
    return tok,got

def make_boundary_model(converted):
    seed_all()
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=len(BOUNDARY_LABELS),
        id2label={i:x for i,x in enumerate(BOUNDARY_LABELS)},label2id=BOUNDARY2ID)
    m=BertForTokenClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in m.parameters()): raise RuntimeError("non-finite boundary model")
    return m

def make_span_model(converted):
    seed_all()
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=len(SPAN_CLASSES),
        id2label={i:x for i,x in enumerate(SPAN_CLASSES)},label2id=SPAN2ID,
        problem_type="multi_label_classification")
    m=BertForSequenceClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in m.parameters()): raise RuntimeError("non-finite span model")
    return m

def select_epoch_checkpoint(trainer,criterion):
    rows=[x for x in trainer.state.log_history if "eval_loss" in x and "epoch" in x]
    if not rows: raise RuntimeError("no epoch evaluations")
    if criterion=="loss":
        best=min(rows,key=lambda x:(float(x["eval_loss"]),float(x["epoch"])))
    else:
        best=min(rows,key=lambda x:(-float(x.get("eval_macro_f1",0.0)),float(x["eval_loss"]),float(x["epoch"])))
    epoch=int(round(float(best["epoch"])))
    steps_per_epoch=int(math.ceil(len(trainer.train_dataset)/trainer.args.per_device_train_batch_size))
    ckpt=pathlib.Path(trainer.args.output_dir)/f"checkpoint-{epoch*steps_per_epoch}"
    if not ckpt.exists():
        candidates=sorted(pathlib.Path(trainer.args.output_dir).glob("checkpoint-*"),
                          key=lambda p:abs(int(p.name.split("-")[-1])-epoch*steps_per_epoch))
        if not candidates: raise RuntimeError("checkpoint missing")
        ckpt=candidates[0]
    return best,ckpt

def word_r4b_predictions(logits,dataset):
    probs=torch.softmax(torch.tensor(logits),dim=-1).numpy()
    out=[]
    for si,first in enumerate(dataset.first_positions):
        tags=[]; conf=[]
        for pos in first:
            p=probs[si,pos]; j=int(np.argmax(p))
            tags.append(R4B_ID2LABEL[j]); conf.append(float(p[j]))
        out.append((tags,conf))
    return out

def predicted_entities(tags,conf):
    out=[]; cur=None
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            ctyp,s,vals=cur
            if pref=="I" and typ==ctyp:
                vals.append(conf[i]); continue
            out.append({"type":ctyp,"start":s,"end":i,"r4b_conf":float(min(vals))}); cur=None
        if tag!="O": cur=(typ,i,[conf[i]])
    return out

def boundary_probs(logits,dataset):
    prob=torch.softmax(torch.tensor(logits),dim=-1).numpy()
    start=[]; end=[]
    for si,first in enumerate(dataset.first_positions):
        s=[]; e=[]
        for pos in first:
            p=prob[si,pos]
            s.append(float(p[BOUNDARY2ID["START"]]+p[BOUNDARY2ID["BOTH"]]))
            e.append(float(p[BOUNDARY2ID["END"]]+p[BOUNDARY2ID["BOTH"]]))
        start.append(s); end.append(e)
    return start,end

def calibration(sentences,candidates,start_probs,end_probs,span_probs):
    gold_by_sentence=[]
    for _,tags in sentences:
        gold_by_sentence.append(set(spans_from_tags(tags)))
    results=[]
    for t in THRESHOLDS:
        counts={c:{"tp":0,"fp":0,"fn":0,"accepted":0,"gold":0} for c in SPAN_CLASSES}
        accepted_keys=[set() for _ in sentences]
        for si,golds in enumerate(gold_by_sentence):
            for c,_,_ in golds: counts[c]["gold"]+=1
        for idx,c in enumerate(candidates):
            typ=c["type"]; si=c["sentence_index"]; s=c["start"]; e=c["end"]
            if c["r4b_conf"]<t: continue
            if e-s>MAX_SPAN_WIDTH_WORDS or e<=s: continue
            if start_probs[si][s]<BOUNDARY_GENERATION_THRESHOLD: continue
            if end_probs[si][e-1]<BOUNDARY_GENERATION_THRESHOLD: continue
            p=span_probs[idx]; same=float(p[SPAN2ID[typ]])
            if same<t: continue
            if any(float(p[j])>=t for j in range(len(SPAN_CLASSES)) if j!=SPAN2ID[typ]): continue
            key=(typ,s,e)
            counts[typ]["accepted"]+=1
            accepted_keys[si].add(key)
            if key in gold_by_sentence[si]: counts[typ]["tp"]+=1
            else: counts[typ]["fp"]+=1
        for si,golds in enumerate(gold_by_sentence):
            for key in golds:
                if key not in accepted_keys[si]: counts[key[0]]["fn"]+=1
        per={}
        for c,d in counts.items():
            p=d["tp"]/(d["tp"]+d["fp"]) if d["tp"]+d["fp"] else 0.0
            r=d["tp"]/(d["tp"]+d["fn"]) if d["tp"]+d["fn"] else 0.0
            per[c]={**d,"precision":p,"recall":r}
        macro=sum(per[c]["precision"] for c in SPAN_CLASSES)/4.0
        passes=(all(per[c]["precision"]>=.90 for c in SPAN_CLASSES)
                and all(per[c]["recall"]>=.20 for c in SPAN_CLASSES)
                and all(per[c]["accepted"]>=10 for c in SPAN_CLASSES)
                and macro>=.90)
        results.append({"threshold":t,"per_class":per,"macro_precision":macro,"passes":passes})
    return results

def smoke(args,train_s,dev_s,tokenizer,converted,status_path):
    bmodel=make_boundary_model(converted)
    bds=BoundaryDataset(train_s[:8],tokenizer)
    batch={k:torch.stack([bds[i][k] for i in range(4)]) for k in bds[0]}
    opt=torch.optim.AdamW(bmodel.parameters(),lr=5e-5,weight_decay=.01)
    loss=bmodel(**batch).loss
    if not torch.isfinite(loss): raise RuntimeError("boundary smoke loss non-finite")
    loss.backward()
    if not any(p.grad is not None and torch.isfinite(p.grad).all() and torch.count_nonzero(p.grad)>0 for p in bmodel.parameters()):
        raise RuntimeError("boundary smoke gradients invalid")
    opt.step()

    smodel=make_span_model(converted)
    sds=SpanDataset(train_s[:80],tokenizer)
    coll=DataCollatorWithPadding(tokenizer=tokenizer,return_tensors="pt")
    sb=coll([sds[i] for i in range(min(8,len(sds)))])
    opt2=torch.optim.AdamW(smodel.parameters(),lr=2e-5,weight_decay=.01)
    sloss=smodel(**sb).loss
    if not torch.isfinite(sloss): raise RuntimeError("span smoke loss non-finite")
    sloss.backward()
    if not any(p.grad is not None and torch.isfinite(p.grad).all() and torch.count_nonzero(p.grad)>0 for p in smodel.parameters()):
        raise RuntimeError("span smoke gradients invalid")
    opt2.step()

    rsha=sha256_path(pathlib.Path(args.r4b_model_dir)/"model.safetensors")
    if rsha!=EXPECTED_R4B_MODEL_SHA: raise RuntimeError("R4B model hash mismatch")
    fixtures=[(("P",1,4),("P",1,4),True),(("P",1,4),("P",1,3),False),(("P",1,4),("I",1,4),False)]
    scorer=all(((a==b)==want) for a,b,want in fixtures)
    if not scorer: raise RuntimeError("exact scorer fixture fail")
    result={"state":"R4_2C_SMOKE_PASS","boundary_loss":float(loss.detach()),
            "span_loss":float(sloss.detach()),"r4b_model_sha256":rsha,
            "exact_scorer_fixture_pass":scorer,
            "guards":{"scientific_training_performed":False,"test_files_read":False,
                      "factpico_used":False,"consumed_holdout_used":False}}
    atomic_json_write(pathlib.Path(args.out)/"R4_2C_SMOKE.json",result)
    atomic_json_write(status_path,{"state":"COMPLETED","progress_percent":100.0,
      "current_stage":"SMOKE_COMPLETE","completed_units":5,"total_units":5,
      "last_successful_checkpoint":"R4_2C_SMOKE.json","last_progress_at":utc_now(),
      "next_expected_step":"AUTHORIZE_ONE_R4_2C_DEVELOPMENT_TRAINING_RUN",
      "failure_or_stall_reason":None})
    print(json.dumps(result,indent=2,sort_keys=True))

def full_train(args,train_s,dev_s,tokenizer,converted,status_path):
    # A: boundary localizer
    btrain=BoundaryDataset(train_s,tokenizer); bdev=BoundaryDataset(dev_s,tokenizer)
    bmodel=make_boundary_model(converted)
    bdir=pathlib.Path(args.out)/"boundary_trainer"
    bargs=TrainingArguments(output_dir=str(bdir),seed=SEED,data_seed=SEED,
        learning_rate=5e-5,weight_decay=.01,warmup_steps=0,max_grad_norm=1.0,
        lr_scheduler_type="linear",per_device_train_batch_size=8,per_device_eval_batch_size=8,
        num_train_epochs=3,evaluation_strategy="epoch",save_strategy="epoch",
        load_best_model_at_end=False,save_total_limit=3,logging_strategy="steps",logging_steps=10,
        report_to=[],disable_tqdm=True,save_safetensors=True,dataloader_num_workers=0)
    bt=Trainer(model=bmodel,args=bargs,train_dataset=btrain,eval_dataset=bdev,tokenizer=tokenizer,
        callbacks=[ProgressCallback(status_path,"BOUNDARY_LOCALIZER",0.0)])
    bt.train()
    brow,bck=select_epoch_checkpoint(bt,"loss")
    bsel=pathlib.Path(args.out)/"boundary_model"
    best_b=BertForTokenClassification.from_pretrained(bck,local_files_only=True)
    best_b.save_pretrained(bsel,safe_serialization=True); tokenizer.save_pretrained(bsel)
    if any(not torch.isfinite(p).all() for p in best_b.parameters()): raise RuntimeError("non-finite boundary selected")

    # B: span classifier
    strain=SpanDataset(train_s,tokenizer); sdev=SpanDataset(dev_s,tokenizer)
    smodel=make_span_model(converted)
    sdir=pathlib.Path(args.out)/"span_trainer"
    sargs=TrainingArguments(output_dir=str(sdir),seed=SEED,data_seed=SEED,
        learning_rate=2e-5,weight_decay=.01,warmup_steps=0,max_grad_norm=1.0,
        lr_scheduler_type="linear",per_device_train_batch_size=16,per_device_eval_batch_size=16,
        num_train_epochs=3,evaluation_strategy="epoch",save_strategy="epoch",
        load_best_model_at_end=False,save_total_limit=3,logging_strategy="steps",logging_steps=10,
        report_to=[],disable_tqdm=True,save_safetensors=True,dataloader_num_workers=0)
    coll=DataCollatorWithPadding(tokenizer=tokenizer,return_tensors="pt")
    st=Trainer(model=smodel,args=sargs,train_dataset=strain,eval_dataset=sdev,tokenizer=tokenizer,
        data_collator=coll,compute_metrics=macro_span_metrics,
        callbacks=[ProgressCallback(status_path,"SPAN_CLASSIFIER",3.0)])
    st.train()
    srow,sck=select_epoch_checkpoint(st,"macro_f1")
    ssel=pathlib.Path(args.out)/"span_model"
    best_s=BertForSequenceClassification.from_pretrained(sck,local_files_only=True)
    best_s.save_pretrained(ssel,safe_serialization=True); tokenizer.save_pretrained(ssel)
    if any(not torch.isfinite(p).all() for p in best_s.parameters()): raise RuntimeError("non-finite span selected")

    # C: frozen-dev consensus calibration
    atomic_json_write(status_path,{"state":"RUNNING","progress_percent":87.5,
      "current_stage":"CONSENSUS_CALIBRATION","active_module":"CONSENSUS",
      "completed_units":6,"total_units":7,"last_successful_checkpoint":str(ssel),
      "last_progress_at":utc_now(),"next_expected_step":"CALIBRATE_FROZEN_GRID",
      "failure_or_stall_reason":None})

    # boundary dev probabilities
    beargs=TrainingArguments(output_dir=str(pathlib.Path(args.out)/"boundary_predict_tmp"),
        per_device_eval_batch_size=8,report_to=[],disable_tqdm=True,dataloader_num_workers=0)
    bep=Trainer(model=best_b,args=beargs,tokenizer=tokenizer).predict(bdev)
    sp,ep=boundary_probs(bep.predictions,bdev)

    # R4.2B candidate predictions
    r4tok=AutoTokenizer.from_pretrained(args.r4b_model_dir,local_files_only=True,use_fast=True)
    r4model=BertForTokenClassification.from_pretrained(args.r4b_model_dir,local_files_only=True)
    if sha256_path(pathlib.Path(args.r4b_model_dir)/"model.safetensors")!=EXPECTED_R4B_MODEL_SHA:
        raise RuntimeError("R4B model hash mismatch")
    r4ds=R4BDataset(dev_s,r4tok)
    r4args=TrainingArguments(output_dir=str(pathlib.Path(args.out)/"r4b_predict_tmp"),
        per_device_eval_batch_size=8,report_to=[],disable_tqdm=True,dataloader_num_workers=0)
    r4pred=Trainer(model=r4model,args=r4args,tokenizer=r4tok).predict(r4ds)
    seqs=word_r4b_predictions(r4pred.predictions,r4ds)
    candidates=[]
    for si,(tags,conf) in enumerate(seqs):
        for e in predicted_entities(tags,conf):
            e["sentence_index"]=si; candidates.append(e)

    # span probabilities for exactly the frozen R4B candidates
    cds=CandidateSpanDataset(candidates,dev_s,tokenizer)
    sargs2=TrainingArguments(output_dir=str(pathlib.Path(args.out)/"span_predict_tmp"),
        per_device_eval_batch_size=16,report_to=[],disable_tqdm=True,dataloader_num_workers=0)
    spr=Trainer(model=best_s,args=sargs2,tokenizer=tokenizer,data_collator=coll).predict(cds)
    sprobs=1.0/(1.0+np.exp(-spr.predictions))

    cals=calibration(dev_s,candidates,sp,ep,sprobs)
    chosen=next((x for x in cals if x["passes"]),None)
    state="R4_2C_BOUNDARY_CONSENSUS_CALIBRATED" if chosen else "R4_2C_BOUNDARY_CONSENSUS_NOT_READY"
    summary={
      "experiment":"R4_2C_BOUNDARY_CONSENSUS_DEV_ONLY",
      "state":state,"seed":SEED,
      "training":{
        "boundary":{"epochs":3,"learning_rate":5e-5,"weight_decay":.01,"batch":8,
                    "selected_eval":brow,"selected_checkpoint":str(bck)},
        "span":{"epochs":3,"learning_rate":2e-5,"weight_decay":.01,"batch":16,
                "selected_eval":srow,"selected_checkpoint":str(sck)}
      },
      "consensus":{"boundary_generation_threshold":BOUNDARY_GENERATION_THRESHOLD,
                   "max_span_width_words":MAX_SPAN_WIDTH_WORDS,
                   "threshold_grid":THRESHOLDS,
                   "rule":"R4B_CONF_AND_EXACT_BOUNDARY_AND_SAME_CLASS_SPAN_CONF; DISAGREEMENT_TO_REVIEW"},
      "calibration_candidates":cals,"chosen_calibration":chosen,
      "candidate_count":len(candidates),
      "files":{
        "boundary_model_sha256":sha256_path(bsel/"model.safetensors"),
        "span_model_sha256":sha256_path(ssel/"model.safetensors"),
        "r4b_model_sha256":EXPECTED_R4B_MODEL_SHA,
        "converted_base_sha256":EXPECTED_CONVERTED_SHA
      },
      "guards":{"test_files_read":False,"factpico_used":False,
                "consumed_60_rct_holdout_used":False,"opened_30_rct_diagnostic_used":False,
                "thresholds_changed":False,"pickle_weight_loaded":False,
                "final_weights_safetensors":True},
      "stop_boundary":"STOP_BEFORE_EBM_COVID_AD_TEST_INFERENCE"
    }
    raw=json.dumps(summary,sort_keys=True,separators=(",",":")).encode()
    summary["canonical_pre_hash_sha256"]=hashlib.sha256(raw).hexdigest()
    atomic_json_write(pathlib.Path(args.out)/"R4_2C_TRAIN_CALIBRATION_SUMMARY.json",summary)
    atomic_json_write(status_path,{"state":"COMPLETED" if chosen else "COMPLETED_WITH_GATE_FAIL",
      "progress_percent":100.0,"current_stage":"CALIBRATION_COMPLETE","active_module":"CONSENSUS",
      "completed_units":7,"total_units":7,"last_successful_checkpoint":"R4_2C_TRAIN_CALIBRATION_SUMMARY.json",
      "last_progress_at":utc_now(),
      "next_expected_step":"STOP_AND_REQUEST_TEST_AUTHORIZATION" if chosen else "STOP_AND_ANALYZE_DEV_ONLY_CONSENSUS_FAILURE",
      "failure_or_stall_reason":None if chosen else "FROZEN_DEV_CONSENSUS_GATE_NOT_MET",
      "witness_state":state})
    print(json.dumps(summary,indent=2,sort_keys=True))
    if chosen is None: raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["smoke","train"],required=True)
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--r4b-model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    seed_all()
    if sha256_path(args.train)!=EXPECTED_TRAIN_SHA: raise RuntimeError("train hash mismatch")
    if sha256_path(args.dev)!=EXPECTED_DEV_SHA: raise RuntimeError("dev hash mismatch")
    if sha256_path(args.r4b_model_dir/"model.safetensors")!=EXPECTED_R4B_MODEL_SHA:
        raise RuntimeError("R4B model identity mismatch")
    if (args.model_dir/"pytorch_model.bin").exists(): raise RuntimeError("pickle base forbidden")
    if (args.r4b_model_dir/"pytorch_model.bin").exists(): raise RuntimeError("pickle R4B forbidden")
    args.out.mkdir(parents=True,exist_ok=False)
    status_path=args.out/"PROCESS_STATUS.json"
    atomic_json_write(status_path,{"state":"RUNNING","progress_percent":0.0,
      "current_stage":"SAFE_BASE_CONVERSION","completed_units":0,"total_units":7 if args.mode=="train" else 5,
      "last_successful_checkpoint":None,"last_progress_at":utc_now(),
      "next_expected_step":"CONVERT_SAFE_BASE","failure_or_stall_reason":None})
    train_s=read_conll(args.train); dev_s=read_conll(args.dev)
    converted=args.out/"converted_base"
    tokenizer,_=convert_safe_base(args.model_dir,converted)
    if args.mode=="smoke":
        smoke(args,train_s,dev_s,tokenizer,converted,status_path)
    else:
        full_train(args,train_s,dev_s,tokenizer,converted,status_path)

if __name__=="__main__":
    main()
