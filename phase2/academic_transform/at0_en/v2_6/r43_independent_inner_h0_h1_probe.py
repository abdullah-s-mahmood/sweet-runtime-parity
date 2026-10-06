#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, os, pathlib, random
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer, BertModel

from r43_contextual_pair_preflight import parse_train, span_maps, static_negative_candidates
from r43_stage_b_h0_h1_diagnostic import H0,H1,head_forward,seed_all

SEED=42
CLASSES=["NONE","P","I","C","O"]
C2I={c:i for i,c in enumerate(CLASSES)}
EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_SPLIT_SHA="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226"

def sha(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def htxt(s): return hashlib.sha256(s.encode()).hexdigest()
def dump(p,o):
    pathlib.Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def make_examples(docs,docset):
    gm,pos=span_maps(docs,docset)
    neg=static_negative_candidates(docs,docset,gm,pos)
    bg_by_source={}
    for r in neg["background_reserved_raw"]:
        s,e,t=r["source"]
        bg_by_source[(r["document"],r["sentence"],s,e,t)]=r
    rows=list(pos)
    for r in neg["static_unique"]:
        rows.append({"document":r["document"],"sentence":r["sentence"],"start":r["start"],"end":r["end"],
                     "label":"NONE","kind":"STATIC"})
    # Independent probe has no native Stage-A B errors; fill the prospectively defined slot with fallback only.
    for p in pos:
        k=(p["document"],p["sentence"],p["start"],p["end"],p["label"])
        r=bg_by_source.get(k)
        if r is not None:
            rows.append({"document":r["document"],"sentence":r["sentence"],"start":r["start"],"end":r["end"],
                         "label":"NONE","kind":"BACKGROUND_FALLBACK"})
    # exact gold precedence / coordinate dedup
    by={}
    for r in rows:
        k=(r["document"],r["sentence"],r["start"],r["end"])
        if k not in by or r["label"]!="NONE": by[k]=r
    return [by[k] for k in sorted(by)]

def sentence_rows(docs,docset):
    return [(di,si,tokens) for di in sorted(docset) for si,(tokens,tags) in enumerate(docs[di])]

def encode_context(model,tok,docs,docset):
    cache={}
    model.eval()
    rows=sentence_rows(docs,docset)
    with torch.no_grad():
        for st in range(0,len(rows),8):
            ch=rows[st:st+8]
            enc=tok([x[2] for x in ch],is_split_into_words=True,padding=True,truncation=True,max_length=256,return_tensors="pt")
            h=model(**enc).last_hidden_state
            for bi,(di,si,tokens) in enumerate(ch):
                wids=enc.word_ids(batch_index=bi); seen=set(); pos=[]
                for j,w in enumerate(wids):
                    if w is not None and w not in seen:
                        seen.add(w); pos.append(j)
                if len(pos)!=len(tokens): raise RuntimeError(f"truncation {di}/{si}")
                cache[(di,si)]=h[bi,pos,:].detach().cpu().float()
    return cache

def tensors(rows,cache):
    n=len(rows); X=torch.empty(n,5,768); pe=torch.zeros(n,dtype=torch.bool); ne=torch.zeros(n,dtype=torch.bool)
    w=torch.empty(n,dtype=torch.long); y=torch.empty(n,dtype=torch.long)
    z=torch.zeros(768)
    for i,r in enumerate(rows):
        h=cache[(r["document"],r["sentence"])]
        s,e=r["start"],r["end"]
        X[i,0]=h[s]; X[i,1]=h[e-1]; X[i,2]=h[s:e].mean(0)
        if s: X[i,3]=h[s-1]
        else: X[i,3]=z; pe[i]=True
        if e<len(h): X[i,4]=h[e]
        else: X[i,4]=z; ne[i]=True
        w[i]=e-s; y[i]=C2I[r["label"]]
    return X,pe,ne,w,y

def train(cls,X,pe,ne,w,y):
    seed_all(); m=cls(); opt=torch.optim.AdamW(m.parameters(),lr=1e-3,weight_decay=.01)
    bs=64; total=10*math.ceil(len(y)/bs); sched=torch.optim.lr_scheduler.LambdaLR(opt,lambda s:max(0,1-s/max(1,total)))
    seed_all()
    for ep in range(10):
        g=torch.Generator().manual_seed(SEED+ep); order=torch.randperm(len(y),generator=g)
        m.train()
        for st in range(0,len(y),bs):
            ix=order[st:st+bs]; opt.zero_grad()
            loss=nn.CrossEntropyLoss()(head_forward(m,X[ix],pe[ix],ne[ix],w[ix]),y[ix])
            loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(),1.0); opt.step(); sched.step()
    return m

def metrics(m,X,pe,ne,w,y):
    m.eval()
    with torch.no_grad(): pred=head_forward(m,X,pe,ne,w).argmax(1)
    per={}; fs=[]
    for i,c in enumerate(CLASSES):
        tp=int(((pred==i)&(y==i)).sum()); fp=int(((pred==i)&(y!=i)).sum()); fn=int(((pred!=i)&(y==i)).sum())
        p=tp/(tp+fp) if tp+fp else 0.; r=tp/(tp+fn) if tp+fn else 0.; f=2*p*r/(p+r) if p+r else 0.
        per[c]={"precision":p,"recall":r,"f1":f,"support":int((y==i).sum())}; fs.append(f)
    return {"accuracy":float((pred==y).float().mean()),"macro_f1":sum(fs)/len(fs),"per_class":per}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False); seed_all()
    if sha(a.train)!=EXPECTED_TRAIN_SHA: raise RuntimeError("train mismatch")
    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!=EXPECTED_SPLIT_SHA: raise RuntimeError("manifest mismatch")
    fit=[]
    for e in m["entries"]:
        if e["partition"]=="FIT": fit.extend(e["documents"])
    fit=sorted(fit)
    ranked=sorted(fit,key=lambda d:htxt(f"{SEED}|R43_INNER_H0H1|{d}"))
    ev=set(ranked[:64]); tr=set(ranked[64:])
    docs,empty,bad=parse_train(a.train)
    if bad: raise RuntimeError(str(bad[:3]))
    tr_rows=make_examples(docs,tr); ev_rows=make_examples(docs,ev)

    base=BertModel.from_pretrained(a.model_dir,from_flax=True,local_files_only=True); base.eval()
    tok=AutoTokenizer.from_pretrained(a.model_dir,local_files_only=True,use_fast=True)
    cache=encode_context(base,tok,docs,tr|ev)
    Xt,pet,net,wt,yt=tensors(tr_rows,cache); Xe,pee,nee,we,ye=tensors(ev_rows,cache)

    h0=train(H0,Xt,pet,net,wt,yt); h1=train(H1,Xt,pet,net,wt,yt)
    m0=metrics(h0,Xe,pee,nee,we,ye); m1=metrics(h1,Xe,pee,nee,we,ye)
    out={
      "state":"R43_INDEPENDENT_INNER_H0_H1_PROBE_COMPLETE",
      "scope":"FIT_ONLY_EXPLORATORY_NON_DECISION",
      "inner_split":{"train_documents":len(tr),"eval_documents":len(ev),
                     "train_doc_sha256":htxt(json.dumps(sorted(tr))),
                     "eval_doc_sha256":htxt(json.dumps(sorted(ev)))},
      "examples":{"train":len(yt),"eval":len(ye)},
      "H0":m0,"H1":m1,
      "delta_H1_minus_H0":{"accuracy":m1["accuracy"]-m0["accuracy"],"macro_f1":m1["macro_f1"]-m0["macro_f1"]},
      "guards":{"stage_a_outputs_used":False,"select_used":False,"historical_dev_used":False,
                "test_used":False,"other_folds_used":False,"factpico_used":False,
                "consumed_60_rct_used":False},
      "interpretation_rule":"EXPLORATORY_ONLY; DOES_NOT_MODIFY_FROZEN_STAGE_B"
    }
    dump(a.out/"R43_INDEPENDENT_INNER_H0_H1_PROBE.json",out)
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
