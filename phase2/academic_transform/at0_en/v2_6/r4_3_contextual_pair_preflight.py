#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, math, pathlib, random
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer

SEED=42
CLASSES=["P","I","C","O"]
LABELS={"O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"}
MAX_WIDTH=64

def htxt(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()

def parse_docs(path):
    docs=[]; doc=[]; toks=[]; tags=[]; empty=collections.Counter(); saw_docstart=False
    def flush_sent():
        nonlocal toks,tags,doc
        if toks:
            doc.append((toks,tags)); toks=[]; tags=[]
    def flush_doc():
        nonlocal doc
        flush_sent()
        if doc:
            docs.append(doc); doc=[]
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            flush_sent(); continue
        p=raw.split("\t")
        if len(p)!=2: p=raw.rsplit(None,1)
        if len(p)!=2: raise RuntimeError(f"bad CoNLL row: {raw!r}")
        tok,tag=p
        if tok=="-DOCSTART-":
            saw_docstart=True; flush_doc(); continue
        if tag not in LABELS: raise RuntimeError(f"unknown tag {tag}")
        if tok=="":
            empty[tag]+=1; continue
        toks.append(tok); tags.append(tag)
    flush_doc()
    if not saw_docstart: raise RuntimeError("no DOCSTART boundaries found")
    if not docs: raise RuntimeError("no documents parsed")
    return docs,dict(sorted(empty.items()))

def spans(tags):
    out=[]; cur=None
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            ct,s=cur
            if pref=="I" and typ==ct: continue
            out.append((ct,s,i)); cur=None
        if tag!="O": cur=(typ,i)
    return out

def doc_stats(doc):
    sc=collections.Counter(); tokens=0; sents=len(doc)
    for ts,ys in doc:
        tokens+=len(ts)
        for c,_,_ in spans(ys): sc[c]+=1
    return {"sentences":sents,"tokens":tokens,"spans":{c:int(sc[c]) for c in CLASSES}}

def doc_token_payload(doc,casefold=False):
    out=[]
    for ts,_ in doc:
        out.append([t.casefold() if casefold else t for t in ts])
    return out

def make_groups(docs):
    exact=collections.defaultdict(list)
    casefold=collections.defaultdict(list)
    for i,d in enumerate(docs):
        exact[htxt(doc_token_payload(d,False))].append(i)
        casefold[htxt(doc_token_payload(d,True))].append(i)
    groups=[]
    for gh,ids in sorted(exact.items()):
        agg={"tokens":0,"sentences":0,"spans":{c:0 for c in CLASSES}}
        for i in ids:
            st=doc_stats(docs[i]); agg["tokens"]+=st["tokens"]; agg["sentences"]+=st["sentences"]
            for c in CLASSES: agg["spans"][c]+=st["spans"][c]
        groups.append({"hash":gh,"doc_ids":ids,"doc_count":len(ids),**agg})
    return groups,exact,casefold

def choose_select(groups):
    n=len(groups); target_n=max(1,round(0.20*n))
    total_tokens=sum(g["tokens"] for g in groups)
    total_spans={c:sum(g["spans"][c] for g in groups) for c in CLASSES}
    targets={"tokens":0.20*total_tokens, **{c:0.20*total_spans[c] for c in CLASSES}}
    chosen=[]; remaining=list(groups)
    cur={"tokens":0,**{c:0 for c in CLASSES}}
    for step in range(target_n):
        best=None
        for g in remaining:
            nxt={"tokens":cur["tokens"]+g["tokens"],**{c:cur[c]+g["spans"][c] for c in CLASSES}}
            err=0.0
            for k in ["tokens"]+CLASSES:
                denom=max(1.0,targets[k])
                err+=((nxt[k]-targets[k])/denom)**2
            # discourage gross overshoot before final steps
            frac=(step+1)/target_n
            expected={k:targets[k]*frac for k in ["tokens"]+CLASSES}
            path_err=sum(((nxt[k]-expected[k])/max(1.0,targets[k]))**2 for k in ["tokens"]+CLASSES)
            tie=hashlib.sha256(f"{SEED}|{g['hash']}".encode()).hexdigest()
            key=(err+0.35*path_err,tie)
            if best is None or key<best[0]: best=(key,g,nxt)
        chosen.append(best[1]); cur=best[2]; remaining.remove(best[1])
    return chosen,remaining,targets

def partition_summary(groups):
    out={"groups":len(groups),"documents":sum(g["doc_count"] for g in groups),
         "sentences":sum(g["sentences"] for g in groups),"tokens":sum(g["tokens"] for g in groups),
         "spans":{c:sum(g["spans"][c] for g in groups) for c in CLASSES}}
    return out

def split_docs(groups):
    return sorted(i for g in groups for i in g["doc_ids"])

def audit_coordinate_labels(docs):
    collisions=[]
    for di,d in enumerate(docs):
        for si,(ts,ys) in enumerate(d):
            seen={}
            for c,s,e in spans(ys):
                key=(s,e)
                if key in seen and seen[key]!=c: collisions.append((di,si,s,e,seen[key],c))
                seen[key]=c
    return collisions

def audit_gold_surface_conflicts(docs):
    surf=collections.defaultdict(set); ids=collections.defaultdict(set)
    for di,d in enumerate(docs):
        for si,(ts,ys) in enumerate(d):
            for c,s,e in spans(ys):
                key=" ".join(ts[s:e])
                surf[key].add(c)
                ids[htxt(ts[s:e])].add(c)
    return {
        "gold_surface_sequences_total":len(surf),
        "surface_sequences_with_multiple_gold_classes":sum(len(v)>1 for v in surf.values()),
        "token_id_proxy_sequences_with_multiple_gold_classes":sum(len(v)>1 for v in ids.values()),
        "examples":[{"surface":k,"classes":sorted(v)} for k,v in sorted(surf.items()) if len(v)>1][:20],
    }

def deterministic_pick(pool,key,n=1):
    if not pool: return []
    ranked=sorted(pool,key=lambda x:hashlib.sha256((key+"|"+repr(x)).encode()).hexdigest())
    return ranked[:n]

def preflight_negatives(docs,fit_ids):
    gold_keys=set(); gold_rows=[]
    for di in fit_ids:
        for si,(ts,ys) in enumerate(docs[di]):
            for c,s,e in spans(ys):
                gold_keys.add((di,si,s,e))
                gold_rows.append((di,si,c,s,e))
    selected_local=[]; selected_comp=[]; fallback_possible=0; neg_surface=collections.defaultdict(set)
    for di,si,c,s,e in gold_rows:
        ts,ys=docs[di][si]; n=len(ts); gs=spans(ys); gb={(a,b) for _,a,b in gs}
        local=set()
        vals=[-2,-1,1,2]
        for ds in vals:
            a=s+ds; b=e
            if 0<=a<b<=n and b-a<=MAX_WIDTH and (a,b) not in gb: local.add((a,b))
        for de in vals:
            a=s; b=e+de
            if 0<=a<b<=n and b-a<=MAX_WIDTH and (a,b) not in gb: local.add((a,b))
        for ds in vals:
            for de in vals:
                a=s+ds; b=e+de
                if 0<=a<b<=n and b-a<=MAX_WIDTH and (a,b) not in gb: local.add((a,b))
        picks=deterministic_pick(sorted(local),f"{SEED}|{di}|{si}|{c}|{s}|{e}|LOCAL",2)
        for a,b in picks:
            selected_local.append((di,si,a,b))
            neg_surface[" ".join(ts[a:b])].add("LOCAL")
        comp=set()
        for _,s1,e1 in gs:
            for _,s2,e2 in gs:
                if (s1,e1)==(s2,e2): continue
                a=s1; b=e2
                if 0<=a<b<=n and b-a<=MAX_WIDTH and (a,b) not in gb: comp.add((a,b))
        picks=deterministic_pick(sorted(comp),f"{SEED}|{di}|{si}|{c}|{s}|{e}|COMPOSITE",1)
        for a,b in picks:
            selected_comp.append((di,si,a,b))
            neg_surface[" ".join(ts[a:b])].add("COMPOSITE")
        w=e-s
        bg=False
        if 0<w<=MAX_WIDTH:
            for a in range(0,n-w+1):
                b=a+w
                if (a,b) in gb: continue
                if any(max(a,x)<min(b,y) for _,x,y in gs): continue
                bg=True; break
        fallback_possible+=int(bg)
    local_unique=set(selected_local); comp_unique=set(selected_comp)
    neg_keys=local_unique|comp_unique
    collisions=neg_keys & gold_keys
    gold_surface=collections.defaultdict(set)
    for di,si,c,s,e in gold_rows:
        ts=docs[di][si][0]; gold_surface[" ".join(ts[s:e])].add(c)
    overlap_surfaces=sorted(set(neg_surface)&set(gold_surface))
    return {
        "gold_positive_coordinates":len(gold_keys),
        "local_selected_raw":len(selected_local),"local_unique":len(local_unique),
        "composite_selected_raw":len(selected_comp),"composite_unique":len(comp_unique),
        "gold_negative_coordinate_collisions":len(collisions),
        "gold_examples_with_length_matched_background_available":fallback_possible,
        "negative_surface_sequences_also_seen_as_gold_surface":len(overlap_surfaces),
        "negative_gold_surface_examples":[{"surface":x,"gold_classes":sorted(gold_surface[x]),"negative_kinds":sorted(neg_surface[x])} for x in overlap_surfaces[:20]],
    }

class H0(nn.Module):
    def __init__(self):
        super().__init__()
        self.proj=nn.ModuleList([nn.Linear(768,128) for _ in range(5)])
        self.edge_prev=nn.Parameter(torch.zeros(768)); self.edge_next=nn.Parameter(torch.zeros(768))
        self.width=nn.Embedding(65,16)
        self.ff=nn.Linear(128*5+16,128); self.out=nn.Linear(128,5); self.drop=nn.Dropout(.1)
    def features(self,xs,width):
        ps=[p(x) for p,x in zip(self.proj,xs)]
        return ps,torch.cat(ps+[self.width(width)],dim=-1)
    def forward(self,xs,width):
        ps,z=self.features(xs,width)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        return self.out(h)

class H1(H0):
    def __init__(self):
        super().__init__(); self.U=nn.Parameter(torch.zeros(5,128,128)); nn.init.xavier_uniform_(self.U)
    def forward(self,xs,width):
        ps,z=self.features(xs,width)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        base=self.out(h)
        s,e=ps[0],ps[1]
        bi=torch.einsum("bi,kij,bj->bk",s,self.U,e)
        return base+bi

def mechanics():
    torch.manual_seed(SEED)
    xs=[torch.randn(8,768) for _ in range(5)]; width=torch.tensor([1,2,3,4,5,8,16,64])
    y=torch.tensor([0,1,2,3,4,0,1,2])
    out={}
    for name,cls in [("H0",H0),("H1",H1)]:
        m=cls(); logits=m(xs,width)
        loss=nn.CrossEntropyLoss()(logits,y); loss.backward()
        finite=bool(torch.isfinite(loss) and all(p.grad is None or torch.isfinite(p.grad).all() for p in m.parameters()))
        out[name]={"params":sum(p.numel() for p in m.parameters() if p.requires_grad),
                   "logit_shape":list(logits.shape),"loss":float(loss.detach()),"finite_backward":finite}
    out["parameter_difference_H1_minus_H0"]=out["H1"]["params"]-out["H0"]["params"]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--tokenizer-dir",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=False)
    raw_sha=hashlib.sha256(args.train.read_bytes()).hexdigest()
    if raw_sha!="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e": raise RuntimeError("TRAIN SHA mismatch")
    docs,empty=parse_docs(args.train)
    groups,exact,casefold=make_groups(docs)
    select,fit,targets=choose_select(groups)
    fit_ids=split_docs(fit); sel_ids=split_docs(select)
    if set(fit_ids)&set(sel_ids): raise RuntimeError("document overlap")
    if set(g["hash"] for g in fit)&set(g["hash"] for g in select): raise RuntimeError("duplicate group overlap")
    coord=audit_coordinate_labels(docs)
    if coord: raise RuntimeError(f"coordinate label collisions: {coord[:5]}")
    surf=audit_gold_surface_conflicts(docs)
    neg=preflight_negatives(docs,fit_ids)
    if neg["gold_negative_coordinate_collisions"]!=0: raise RuntimeError("gold/NONE collision")
    tok=AutoTokenizer.from_pretrained(args.tokenizer_dir,local_files_only=True,use_fast=True)
    max_wp=0; lost=[]
    for di,d in enumerate(docs):
        for si,(ts,ys) in enumerate(d):
            enc=tok(ts,is_split_into_words=True,truncation=False)
            max_wp=max(max_wp,len(enc["input_ids"]))
            # This diagnostic inherits sentence-level max 256; fail if any normalized TRAIN sentence exceeds it.
            if len(enc["input_ids"])>256: lost.append((di,si,len(enc["input_ids"])))
    if lost: raise RuntimeError(f"sentences exceed 256 wordpieces: {lost[:5]}")
    fit_sum=partition_summary(fit); sel_sum=partition_summary(select)
    # Minimum feasibility: SELECT must have enough gold support that >=10 accepted and >=0.20 recall are arithmetically possible.
    blockers=[]
    for c in CLASSES:
        if sel_sum["spans"][c] < 10: blockers.append(f"SELECT_{c}_GOLD_LT_10")
    split_manifest={
      "seed":SEED,"grouping":"EXACT_NORMALIZED_TOKEN_SEQUENCE_WITH_DOCSTART_DOCUMENT_BLOCKS",
      "fit_group_hashes":sorted(g["hash"] for g in fit),
      "select_group_hashes":sorted(g["hash"] for g in select),
      "fit_document_ids":fit_ids,"select_document_ids":sel_ids,
    }
    split_digest=htxt(split_manifest)
    fit_digest=htxt([doc_token_payload(docs[i],False) for i in fit_ids])
    sel_digest=htxt([doc_token_payload(docs[i],False) for i in sel_ids])
    mech=mechanics()
    if not mech["H0"]["finite_backward"] or not mech["H1"]["finite_backward"]: blockers.append("HEAD_MECHANICS_NONFINITE")
    result={
      "state":"R4_3_CONTEXTUAL_PAIR_PREFLIGHT_PASS" if not blockers else "R4_3_CONTEXTUAL_PAIR_PREFLIGHT_BLOCKED",
      "raw_train_sha256":raw_sha,"empty_surface_tag_counts":empty,
      "documents":{"count":len(docs),"exact_duplicate_groups":len(groups),
        "groups_with_exact_duplicates":sum(len(v)>1 for v in exact.values()),
        "documents_in_exact_duplicate_groups":sum(len(v) for v in exact.values() if len(v)>1),
        "casefold_duplicate_groups":len(casefold),
        "groups_with_casefold_duplicates":sum(len(v)>1 for v in casefold.values())},
      "fit":fit_sum,"select":sel_sum,
      "targets":{"select_groups":round(.2*len(groups)),"tokens":targets["tokens"],"spans":{c:targets[c] for c in CLASSES}},
      "digests":{"fit_content_sha256":fit_digest,"select_content_sha256":sel_digest,"split_manifest_sha256":split_digest},
      "coordinate_label_collisions":len(coord),
      "gold_surface_conflict_audit":surf,
      "gold_only_negative_preflight":neg,
      "tokenization":{"max_sentence_wordpieces_with_specials":max_wp,"sentences_over_256":len(lost)},
      "head_mechanics":mech,
      "blockers":blockers,
      "guards":{"train_only":True,"historical_dev_read":False,"test_read":False,"other_folds_read":False,
                "factpico_read":False,"consumed_60_rct_holdout_read":False,"scientific_training_performed":False},
    }
    (args.out/"R4_3_CONTEXTUAL_PAIR_PREFLIGHT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (args.out/"R4_3_TRAIN_INTERNAL_SPLIT_MANIFEST.json").write_text(json.dumps(split_manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    if blockers: raise SystemExit(2)

if __name__=="__main__":
    main()
