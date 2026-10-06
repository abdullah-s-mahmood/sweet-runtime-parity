#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, math, os, pathlib, random
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer, BertModel

SEED=42
CLASSES=["NONE","P","I","C","O"]
C2I={c:i for i,c in enumerate(CLASSES)}
MAX_WIDTH=64

def seed_all():
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True,warn_only=True)

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def htxt(s): return hashlib.sha256(s.encode()).hexdigest()

def parse_train(path):
    docs=[]; doc=[]; toks=[]; tags=[]
    def fs():
        nonlocal toks,tags,doc
        if toks: doc.append((toks,tags)); toks=[]; tags=[]
    def fd():
        nonlocal doc
        fs()
        if doc: docs.append(doc); doc=[]
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if raw.startswith("-DOCSTART-"): fd(); continue
        if raw=="": fs(); continue
        if "\t" in raw: tok,tag=raw.split("\t",1)
        else:
            p=raw.rsplit(None,1)
            if len(p)!=2: raise RuntimeError(raw)
            tok,tag=p
        if tok=="": continue
        toks.append(tok); tags.append(tag)
    fd(); return docs

def spans(tags,prev_last=None):
    out=[]; cur=None; initial_type=None
    if tags and tags[0].startswith("I-"):
        typ=tags[0][2:]
        if prev_last in (f"B-{typ}",f"I-{typ}"): initial_type=typ
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            ct,s=cur
            if pref=="I" and typ==ct: continue
            out.append((ct,s,i)); cur=None
        if tag!="O":
            if i==0 and pref=="I" and initial_type==typ: cur=(typ,0)
            elif pref=="B": cur=(typ,i)
            elif pref=="I": cur=(typ,i)
    return out

def pick(pool,key,n=1):
    return sorted(pool,key=lambda x:htxt(key+"|"+repr(x)))[:n]

def examples_for_docs(docs,doc_ids):
    rows=[]
    for di in sorted(doc_ids):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            prev=doc[si-1][1][-1] if si>0 and doc[si-1][1] else None
            gs=spans(tags,prev)
            gold={(s,e):c for c,s,e in gs}
            for c,s,e in gs:
                rows.append((di,si,s,e,c,"GOLD"))
                # one local
                pool=[]
                for ds,de in [(-2,0),(-1,0),(1,0),(2,0),(0,-2),(0,-1),(0,1),(0,2),
                              (-1,-1),(-1,1),(1,-1),(1,1)]:
                    a,b=s+ds,e+de
                    if 0<=a<b<=len(tokens) and b-a<=MAX_WIDTH and (a,b) not in gold:
                        pool.append((a,b))
                for a,b in pick(pool,f"{SEED}|{di}|{si}|{s}|{e}|LOCAL",1):
                    rows.append((di,si,a,b,"NONE","LOCAL"))
                # one composite
                cp=[]
                for c2,s2,e2 in gs:
                    if (s2,e2)==(s,e): continue
                    for a,b in ((s,e2),(s2,e)):
                        if 0<=a<b<=len(tokens) and b-a<=MAX_WIDTH and (a,b) not in gold:
                            cp.append((a,b))
                for a,b in pick(cp,f"{SEED}|{di}|{si}|{s}|{e}|COMP",1):
                    rows.append((di,si,a,b,"NONE","COMPOSITE"))
                # one bg fallback
                w=e-s; bg=[]
                if 0<w<=MAX_WIDTH:
                    for a in range(0,len(tokens)-w+1):
                        b=a+w
                        if (a,b) in gold: continue
                        if any(max(a,x)<min(b,y) for _,x,y in gs): continue
                        bg.append((a,b))
                for a,b in pick(bg,f"{SEED}|{di}|{si}|{s}|{e}|BG",1):
                    rows.append((di,si,a,b,"NONE","BACKGROUND"))
    # gold precedence + deterministic provenance
    by={}
    for r in rows:
        k=r[:4]
        if k not in by or r[4]!="NONE":
            by[k]=r
    out=list(by.values())
    out.sort(key=lambda r:r[:4])
    return out

def encode_sentence(model,tok,tokens):
    enc=tok(tokens,is_split_into_words=True,return_tensors="pt",truncation=True,max_length=256)
    with torch.no_grad(): h=model(**enc).last_hidden_state[0]
    wids=enc.word_ids()
    first=[]; seen=set()
    for pos,w in enumerate(wids):
        if w is not None and w not in seen:
            seen.add(w); first.append((w,pos))
    if len(first)!=len(tokens): raise RuntimeError("sentence truncation")
    return torch.stack([h[pos] for _,pos in first],dim=0).cpu()

def encode_crop(model,tok,tokens):
    enc=tok(tokens,is_split_into_words=True,return_tensors="pt",truncation=True,max_length=66)
    with torch.no_grad(): h=model(**enc).last_hidden_state[0]
    wids=enc.word_ids()
    pos=[i for i,w in enumerate(wids) if w is not None]
    if not pos: return h[0].cpu()
    return h[pos].mean(dim=0).cpu()

def build_features(docs,rows,model,tok):
    sent_cache={}; crop_cache={}
    Xctx=[]; Xcrop=[]; y=[]; surfaces=[]; kinds=[]
    for idx,(di,si,s,e,label,kind) in enumerate(rows):
        sk=(di,si)
        if sk not in sent_cache:
            sent_cache[sk]=encode_sentence(model,tok,docs[di][si][0])
        wh=sent_cache[sk]; n=wh.shape[0]
        start=wh[s]; end=wh[e-1]; interior=wh[s:e].mean(dim=0)
        prev=wh[s-1] if s>0 else torch.zeros_like(start)
        nxt=wh[e] if e<n else torch.zeros_like(start)
        ctx=torch.cat([start,end,interior,prev,nxt],dim=0)
        toks=docs[di][si][0][s:e]
        surf="\u241f".join(toks)
        if surf not in crop_cache:
            crop_cache[surf]=encode_crop(model,tok,toks)
        Xctx.append(ctx); Xcrop.append(crop_cache[surf]); y.append(C2I[label]); surfaces.append(surf); kinds.append(kind)
    return torch.stack(Xctx),torch.stack(Xcrop),torch.tensor(y),surfaces,kinds

class LinearHead(nn.Module):
    def __init__(self,d): super().__init__(); self.fc=nn.Linear(d,len(CLASSES))
    def forward(self,x): return self.fc(x)

def train_head(X,y):
    seed_all(); m=LinearHead(X.shape[1])
    opt=torch.optim.AdamW(m.parameters(),lr=1e-2,weight_decay=1e-2)
    bs=64
    for epoch in range(20):
        order=torch.arange(len(y))
        for i in range(0,len(y),bs):
            ix=order[i:i+bs]
            opt.zero_grad(); loss=nn.CrossEntropyLoss()(m(X[ix]),y[ix]); loss.backward(); opt.step()
    return m

def metrics(m,X,y,mask=None):
    if mask is not None:
        X=X[mask]; y=y[mask]
    if len(y)==0: return {"n":0}
    with torch.no_grad(): pred=m(X).argmax(dim=1)
    per={}
    f1s=[]
    for i,c in enumerate(CLASSES):
        tp=int(((pred==i)&(y==i)).sum()); fp=int(((pred==i)&(y!=i)).sum()); fn=int(((pred!=i)&(y==i)).sum())
        p=tp/(tp+fp) if tp+fp else 0.; r=tp/(tp+fn) if tp+fn else 0.; f=2*p*r/(p+r) if p+r else 0.
        per[c]={"precision":p,"recall":r,"f1":f,"support":int((y==i).sum())}; f1s.append(f)
    return {"n":len(y),"accuracy":float((pred==y).float().mean()),"macro_f1":sum(f1s)/len(f1s),"per_class":per}

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
    # independent exploratory split inside FIT, frozen by hash of source doc id
    ranked=sorted(fit,key=lambda d:htxt(f"{SEED}|R43_CONTEXT_PROBE|{d}"))
    eval_docs=set(ranked[:64]); train_docs=set(ranked[64:])
    if train_docs & eval_docs: raise RuntimeError("probe split overlap")
    docs=parse_train(a.train)
    tr_rows=examples_for_docs(docs,train_docs); ev_rows=examples_for_docs(docs,eval_docs)

    base=BertModel.from_pretrained(a.model_dir,from_flax=True,local_files_only=True)
    base.eval()
    tok=AutoTokenizer.from_pretrained(a.model_dir,local_files_only=True,use_fast=True)
    Xct,Xcr,yt,st,kt=build_features(docs,tr_rows,base,tok)
    Xce,Xre,ye,se,ke=build_features(docs,ev_rows,base,tok)

    # standardize by probe-train only
    def norm(A,B):
        mu=A.mean(0); sd=A.std(0).clamp_min(1e-6)
        return (A-mu)/sd,(B-mu)/sd
    Xct,Xce=norm(Xct.float(),Xce.float()); Xcr,Xre=norm(Xcr.float(),Xre.float())
    mc=train_head(Xcr,yt); mx=train_head(Xct,yt)

    # ambiguous-surface subset based ONLY on probe-train label multiplicity / entity-vs-NONE conflicts
    labmap=collections.defaultdict(set)
    for surf,lab in zip(st,yt.tolist()): labmap[surf].add(lab)
    amb={s for s,v in labmap.items() if len(v)>1}
    mask=torch.tensor([s in amb for s in se],dtype=torch.bool)

    out={
      "state":"R43_INDEPENDENT_CONTEXT_SIGNAL_PROBE_COMPLETE",
      "scope":"FIT_ONLY_EXPLORATORY_NON_DECISION",
      "probe_split":{"train_documents":len(train_docs),"eval_documents":len(eval_docs),
                     "train_doc_sha256":htxt(json.dumps(sorted(train_docs))),
                     "eval_doc_sha256":htxt(json.dumps(sorted(eval_docs)))},
      "examples":{"train":len(yt),"eval":len(ye),"eval_ambiguous_surface_subset":int(mask.sum())},
      "cropped_probe":{"all_eval":metrics(mc,Xre,ye),"ambiguous_surface_eval":metrics(mc,Xre,ye,mask)},
      "contextual_probe":{"all_eval":metrics(mx,Xce,ye),"ambiguous_surface_eval":metrics(mx,Xce,ye,mask)},
      "delta_context_minus_crop":{
          "macro_f1_all":metrics(mx,Xce,ye)["macro_f1"]-metrics(mc,Xre,ye)["macro_f1"],
          "accuracy_all":metrics(mx,Xce,ye)["accuracy"]-metrics(mc,Xre,ye)["accuracy"],
          "macro_f1_ambiguous":(metrics(mx,Xce,ye,mask).get("macro_f1",0)-metrics(mc,Xre,ye,mask).get("macro_f1",0)) if int(mask.sum()) else None
      },
      "guards":{"stage_a_outputs_used":False,"select_used":False,"historical_dev_used":False,"test_used":False,
                "other_folds_used":False,"factpico_used":False,"consumed_60_rct_used":False},
      "interpretation_rule":"EXPLORATORY_ONLY; DOES_NOT_MODIFY_FROZEN_STAGE_B"
    }
    (a.out/"R43_CONTEXT_SIGNAL_PROBE.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
