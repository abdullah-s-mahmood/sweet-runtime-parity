#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, random, os
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer, BertModel

from r43_independent_context_signal_probe import parse_train, examples_for_docs
from r43_stage_b_h0_h1_diagnostic import H0, H1, C2I, CLASSES

SEED=42

def htxt(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def seed_all():
    os.environ["PYTHONHASHSEED"]=str(SEED)
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True,warn_only=True); torch.set_num_threads(2)

def encode_sentence(model,tok,tokens):
    enc=tok(tokens,is_split_into_words=True,return_tensors="pt",truncation=True,max_length=256)
    with torch.no_grad(): h=model(**enc).last_hidden_state[0]
    wids=enc.word_ids(); seen=set(); pos=[]
    for j,w in enumerate(wids):
        if w is not None and w not in seen:
            seen.add(w); pos.append(j)
    if len(pos)!=len(tokens): raise RuntimeError("sentence truncation")
    return h[pos].cpu().float()

def build_raw(docs,rows,model,tok):
    cache={}
    X=torch.empty((len(rows),5,768),dtype=torch.float32)
    pe=torch.zeros(len(rows),dtype=torch.bool)
    ne=torch.zeros(len(rows),dtype=torch.bool)
    w=torch.empty(len(rows),dtype=torch.long)
    y=torch.empty(len(rows),dtype=torch.long)
    for i,(di,si,s,e,label,kind) in enumerate(rows):
        key=(di,si)
        if key not in cache: cache[key]=encode_sentence(model,tok,docs[di][si][0])
        h=cache[key]; n=h.shape[0]
        X[i,0]=h[s]; X[i,1]=h[e-1]; X[i,2]=h[s:e].mean(0)
        if s>0: X[i,3]=h[s-1]
        else: X[i,3].zero_(); pe[i]=True
        if e<n: X[i,4]=h[e]
        else: X[i,4].zero_(); ne[i]=True
        w[i]=e-s; y[i]=C2I[label]
    return X,pe,ne,w,y

def forward(m,X,pe,ne,w): return m(X[:,0],X[:,1],X[:,2],X[:,3],X[:,4],pe,ne,w)

def train(cls,X,pe,ne,w,y):
    seed_all(); m=cls()
    opt=torch.optim.AdamW(m.parameters(),lr=1e-3,weight_decay=.01)
    bs=64; total=10*((len(y)+bs-1)//bs); step=0
    sched=torch.optim.lr_scheduler.LambdaLR(opt,lambda z:max(0.0,1-z/max(1,total)))
    for ep in range(10):
        g=torch.Generator().manual_seed(SEED+ep)
        order=torch.randperm(len(y),generator=g)
        m.train()
        for st in range(0,len(y),bs):
            ix=order[st:st+bs]; opt.zero_grad()
            loss=nn.CrossEntropyLoss()(forward(m,X[ix],pe[ix],ne[ix],w[ix]),y[ix])
            loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(),1.0)
            opt.step(); sched.step(); step+=1
    return m

def metrics(m,X,pe,ne,w,y):
    m.eval()
    with torch.no_grad():
        logits=forward(m,X,pe,ne,w); prob=torch.softmax(logits,dim=-1); pred=prob.argmax(-1)
    per={}; f1s=[]
    for i,c in enumerate(CLASSES):
        tp=int(((pred==i)&(y==i)).sum()); fp=int(((pred==i)&(y!=i)).sum()); fn=int(((pred!=i)&(y==i)).sum())
        p=tp/(tp+fp) if tp+fp else 0.; r=tp/(tp+fn) if tp+fn else 0.; f=2*p*r/(p+r) if p+r else 0.
        per[c]={"precision":p,"recall":r,"f1":f,"support":int((y==i).sum())}; f1s.append(f)
    return {"accuracy":float((pred==y).float().mean()),"macro_f1":sum(f1s)/len(f1s),"per_class":per}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False); seed_all()
    if sha(a.train)!="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e": raise RuntimeError("train mismatch")
    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226": raise RuntimeError("manifest mismatch")
    fit=[]
    for e in m["entries"]:
        if e["partition"]=="FIT": fit.extend(e["documents"])
    fit=sorted(fit)
    ranked=sorted(fit,key=lambda d:htxt(f"{SEED}|R43_CONTEXT_PROBE|{d}"))
    eval_docs=set(ranked[:64]); train_docs=set(ranked[64:])
    docs=parse_train(a.train)
    tr=examples_for_docs(docs,train_docs); ev=examples_for_docs(docs,eval_docs)

    base=BertModel.from_pretrained(a.model_dir,from_flax=True,local_files_only=True); base.eval()
    tok=AutoTokenizer.from_pretrained(a.model_dir,local_files_only=True,use_fast=True)
    Xt,pet,net,wt,yt=build_raw(docs,tr,base,tok)
    Xe,pee,nee,we,ye=build_raw(docs,ev,base,tok)
    # No learned feature normalization; H0/H1 exact architecture sees frozen contextual vectors directly.
    h0=train(H0,Xt,pet,net,wt,yt)
    h1=train(H1,Xt,pet,net,wt,yt)
    m0=metrics(h0,Xe,pee,nee,we,ye); m1=metrics(h1,Xe,pee,nee,we,ye)

    out={
      "state":"R43_INDEPENDENT_BASE_H0_H1_PROBE_COMPLETE",
      "scope":"FIT_ONLY_EXPLORATORY_NON_DECISION",
      "probe_split":{"train_documents":256,"eval_documents":64,
        "train_doc_sha256":htxt(json.dumps(sorted(train_docs))),
        "eval_doc_sha256":htxt(json.dumps(sorted(eval_docs)))},
      "examples":{"train":len(yt),"eval":len(ye)},
      "H0":m0,"H1":m1,
      "delta_H1_minus_H0":{"accuracy":m1["accuracy"]-m0["accuracy"],"macro_f1":m1["macro_f1"]-m0["macro_f1"],
        "per_class_f1":{c:m1["per_class"][c]["f1"]-m0["per_class"][c]["f1"] for c in CLASSES}},
      "parameter_counts":{"H0":sum(p.numel() for p in h0.parameters()),"H1":sum(p.numel() for p in h1.parameters())},
      "guards":{"stage_a_outputs_used":False,"select_used":False,"historical_dev_used":False,"test_used":False,
        "other_folds_used":False,"factpico_used":False,"consumed_60_rct_used":False},
      "interpretation_rule":"EXPLORATORY_ONLY; DOES_NOT_MODIFY_FROZEN_STAGE_B"
    }
    (a.out/"R43_INDEPENDENT_BASE_H0_H1_PROBE.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
