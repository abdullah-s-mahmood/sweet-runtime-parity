#!/usr/bin/env python3
from __future__ import annotations

import argparse, collections, hashlib, json, math, os, pathlib, random, sys, time
from datetime import datetime, timezone

import numpy as np
import torch
import torch.nn as nn
from safetensors.torch import save_file
from transformers import AutoTokenizer, BertForTokenClassification, BertForSequenceClassification

from r43_contextual_pair_preflight import (
    parse_train, spans_for_sentence, span_maps, static_negative_candidates
)

SEED=42
CLASSES=["NONE","P","I","C","O"]
C2I={x:i for i,x in enumerate(CLASSES)}
BIO_LABELS=["O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"]
BID2={i:x for i,x in enumerate(BIO_LABELS)}
BOUNDARY_LABELS=["OUT","START","END","BOTH","IN"]
BOUNDARY2ID={x:i for i,x in enumerate(BOUNDARY_LABELS)}
THRESHOLDS=[0.80,0.85,0.90,0.95]

EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_SPLIT_SHA="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226"
EXPECTED_STATIC_SHA="1ac4b4dd2ca3c1dbc42b5dc0530cafc93fb289f1646b518e305a3d7c20d5d8d2"

def utc_now(): return datetime.now(timezone.utc).isoformat()
def sha256_path(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def htxt(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def seed_all(seed=SEED):
    os.environ["PYTHONHASHSEED"]=str(seed)
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True,warn_only=True); torch.set_num_threads(2)
def dump(p,o):
    p=pathlib.Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(t,p)
def overlap(a,b,c,d): return max(a,c)<min(b,d)

class H0(nn.Module):
    def __init__(self):
        super().__init__()
        self.proj=nn.ModuleList([nn.Linear(768,128) for _ in range(5)])
        self.edge_prev=nn.Parameter(torch.zeros(768))
        self.edge_next=nn.Parameter(torch.zeros(768))
        self.width=nn.Embedding(64,16)
        self.ff=nn.Linear(656,128)
        self.drop=nn.Dropout(0.1)
        self.out=nn.Linear(128,5)
    def projected(self,start,end,inside,prev,nxt,prev_edge,next_edge,width):
        prev=torch.where(prev_edge[:,None],self.edge_prev[None,:],prev)
        nxt=torch.where(next_edge[:,None],self.edge_next[None,:],nxt)
        xs=[start,end,inside,prev,nxt]
        ps=[m(x) for m,x in zip(self.proj,xs)]
        z=torch.cat(ps+[self.width(width-1)],dim=-1)
        return ps,z
    def forward(self,start,end,inside,prev,nxt,prev_edge,next_edge,width):
        ps,z=self.projected(start,end,inside,prev,nxt,prev_edge,next_edge,width)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        return self.out(h)

class H1(H0):
    def __init__(self):
        super().__init__()
        self.U=nn.Parameter(torch.empty(5,129,129))
        nn.init.xavier_uniform_(self.U)
    def forward(self,start,end,inside,prev,nxt,prev_edge,next_edge,width):
        ps,z=self.projected(start,end,inside,prev,nxt,prev_edge,next_edge,width)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        base=self.out(h)
        ones=torch.ones((start.shape[0],1),dtype=start.dtype,device=start.device)
        sa=torch.cat([ps[0],ones],dim=-1); ea=torch.cat([ps[1],ones],dim=-1)
        bi=torch.einsum("bi,kij,bj->bk",sa,self.U,ea)
        return base+bi

def head_mechanics():
    seed_all()
    batch=8
    xs=[torch.randn(batch,768) for _ in range(5)]
    pe=torch.tensor([True,False,False,True,False,False,False,True])
    ne=~pe
    w=torch.tensor([1,2,3,4,8,16,32,64],dtype=torch.long)
    y=torch.tensor([0,1,2,3,4,0,1,2])
    out={}
    for name,cls,want in [("H0",H0,579461),("H1",H1,662666)]:
        seed_all(); m=cls(); n=sum(p.numel() for p in m.parameters() if p.requires_grad)
        if n!=want: raise RuntimeError(f"{name} params {n}!={want}")
        logits=m(*xs,pe,ne,w); loss=nn.CrossEntropyLoss()(logits,y); loss.backward()
        finite=bool(torch.isfinite(loss) and all(p.grad is None or torch.isfinite(p.grad).all() for p in m.parameters()))
        if logits.shape!=(batch,5) or not finite: raise RuntimeError(f"{name} mechanics fail")
        out[name]={"params":n,"shape":list(logits.shape),"loss":float(loss.detach()),"finite":finite}
    out["difference"]=out["H1"]["params"]-out["H0"]["params"]
    return out

def word_batch(tokenizer,token_lists):
    return tokenizer(token_lists,is_split_into_words=True,padding=True,truncation=True,max_length=256,return_tensors="pt")

def first_positions(enc,batch_i,nwords):
    wids=enc.word_ids(batch_index=batch_i); seen=set(); pos=[]
    for j,w in enumerate(wids):
        if w is not None and w not in seen:
            seen.add(w); pos.append(j)
    if len(pos)!=nwords: raise RuntimeError(f"wordpiece truncation {len(pos)}!={nwords}")
    return pos

def decode_pred_entities(tags,conf):
    out=[]; cur=None
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            ct,s,vals=cur
            if pref=="I" and typ==ct:
                vals.append(conf[i]); continue
            out.append({"type":ct,"start":s,"end":i,"b_conf":float(min(vals))}); cur=None
        if tag!="O": cur=(typ,i,[conf[i]])
    return out

def infer_b(model,tokenizer,sentence_rows,batch_size=8):
    model.eval(); out={}
    with torch.no_grad():
        for st in range(0,len(sentence_rows),batch_size):
            chunk=sentence_rows[st:st+batch_size]
            enc=word_batch(tokenizer,[x["tokens"] for x in chunk])
            logits=model(**enc).logits
            probs=torch.softmax(logits,dim=-1)
            for bi,row in enumerate(chunk):
                pos=first_positions(enc,bi,len(row["tokens"]))
                tags=[]; conf=[]
                for p in pos:
                    v=probs[bi,p]; j=int(torch.argmax(v))
                    tags.append(BID2[j]); conf.append(float(v[j]))
                out[(row["doc"],row["sent"])]=decode_pred_entities(tags,conf)
    return out

def infer_boundary_and_context(model,tokenizer,sentence_rows,batch_size=8):
    model.eval(); probs_out={}; hidden_out={}
    with torch.no_grad():
        for st in range(0,len(sentence_rows),batch_size):
            chunk=sentence_rows[st:st+batch_size]
            enc=word_batch(tokenizer,[x["tokens"] for x in chunk])
            base=model.bert(input_ids=enc["input_ids"],attention_mask=enc["attention_mask"])
            seq=model.dropout(base.last_hidden_state)
            logits=model.classifier(seq); probs=torch.softmax(logits,dim=-1)
            for bi,row in enumerate(chunk):
                pos=first_positions(enc,bi,len(row["tokens"]))
                h=base.last_hidden_state[bi,pos,:].detach().cpu().float()
                p=probs[bi,pos,:].detach().cpu()
                start=(p[:,BOUNDARY2ID["START"]]+p[:,BOUNDARY2ID["BOTH"]]).numpy()
                end=(p[:,BOUNDARY2ID["END"]]+p[:,BOUNDARY2ID["BOTH"]]).numpy()
                key=(row["doc"],row["sent"])
                hidden_out[key]=h
                probs_out[key]={"start":start,"end":end}
    return probs_out,hidden_out

def infer_type(model,tokenizer,items,batch_size=32):
    model.eval(); res=[]
    with torch.no_grad():
        for st in range(0,len(items),batch_size):
            chunk=items[st:st+batch_size]
            spans=[x["tokens"][x["start"]:x["end"]] for x in chunk]
            enc=tokenizer(spans,is_split_into_words=True,padding=True,truncation=True,max_length=66,return_tensors="pt")
            logits=model(**enc).logits
            probs=torch.sigmoid(logits).cpu().numpy()
            res.extend(probs.tolist())
    if len(res)!=len(items): raise RuntimeError("type inference length mismatch")
    return res

def make_sentence_rows(docs,doc_ids):
    rows=[]
    for di in sorted(doc_ids):
        for si,(tokens,tags) in enumerate(docs[di]):
            rows.append({"doc":di,"sent":si,"tokens":tokens,"tags":tags})
    return rows

def gold_by_sentence(docs,doc_ids):
    out={}
    positives=[]
    for di in sorted(doc_ids):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            sps,bad,_=spans_for_sentence(doc,si)
            if bad: raise RuntimeError(f"BIO issue {di}/{si}: {bad}")
            out[(di,si)]={(s,e):c for c,s,e in sps}
            for c,s,e in sps:
                positives.append({"document":di,"sentence":si,"start":s,"end":e,"label":c,"kind":"GOLD","source":(s,e,c)})
    return out,positives

def materialize_final_fit_examples(docs,fit_docs,b_preds):
    goldmap,positives=gold_by_sentence(docs,fit_docs)
    neg=static_negative_candidates(docs,fit_docs,goldmap,positives)

    # Verify the preflight static manifest identity exactly.
    synthetic_manifest={
        "fit_positive_coordinates":[
            {k:p[k] for k in ("document","sentence","start","end","label")} for p in
            sorted(positives,key=lambda x:(x["document"],x["sentence"],x["start"],x["end"],x["label"]))
        ],
        "static_none_coordinates":[
            {k:r[k] for k in ("document","sentence","start","end","kind","provenance")} for r in neg["static_unique"]
        ],
        "reserved_background_fallback":[
            {k:r[k] for k in ("document","sentence","start","end","kind")} for r in neg["background_reserved_unique"]
        ],
        "native_fit_error_slot":"DEFERRED_UNTIL_FIT_ONLY_B_REPLICA_EXISTS; algorithm frozen in design V1"
    }
    got=htxt(json.dumps(synthetic_manifest,sort_keys=True,separators=(",",":")))
    if got!=EXPECTED_STATIC_SHA: raise RuntimeError(f"static manifest parity mismatch {got}")

    # Background fallback raw map retains source association.
    bg_by_source={}
    for r in neg["background_reserved_raw"]:
        di,si=r["document"],r["sentence"]
        s,e,typ=r["source"]
        bg_by_source[(di,si,s,e,typ)]=r

    native_rows=[]
    native_count=0; fallback_count=0
    for p in positives:
        di,si,s,e,typ=p["document"],p["sentence"],p["start"],p["end"],p["label"]
        gm=goldmap[(di,si)]
        gold_triples={(c,a,b) for (a,b),c in gm.items()}
        candidates=[]
        for q in b_preds[(di,si)]:
            qt,qs,qe=q["type"],q["start"],q["end"]
            if (qt,qs,qe) in gold_triples: continue
            ov=overlap(s,e,qs,qe)
            key=htxt(f"{SEED}|{di}|{si}|{typ}|{s}|{e}|{qt}|{qs}|{qe}|NATIVE_FIT_ERROR")
            candidates.append((0 if ov else 1,key,q))
        if candidates:
            candidates.sort(key=lambda x:(x[0],x[1])); q=candidates[0][2]
            qs,qe=q["start"],q["end"]
            true=gm.get((qs,qe))
            native_rows.append({"document":di,"sentence":si,"start":qs,"end":qe,
                "label":true if true is not None else "NONE","kind":"NATIVE_FIT_ERROR","source":(s,e,typ)})
            native_count+=1
        else:
            r=bg_by_source.get((di,si,s,e,typ))
            if r is not None:
                native_rows.append({"document":di,"sentence":si,"start":r["start"],"end":r["end"],
                    "label":"NONE","kind":"BACKGROUND_FALLBACK","source":(s,e,typ)})
                fallback_count+=1

    # Merge with precedence exact gold > NONE; provenance retained.
    rows=[]
    rows.extend(positives)
    for r in neg["static_unique"]:
        rows.append({"document":r["document"],"sentence":r["sentence"],"start":r["start"],"end":r["end"],
                     "label":"NONE","kind":"STATIC_"+"+".join(r["provenance"]),"source":r.get("source")})
    rows.extend(native_rows)

    bycoord={}; prov=collections.defaultdict(set)
    for r in rows:
        k=(r["document"],r["sentence"],r["start"],r["end"])
        prov[k].add(r["kind"])
        if k not in bycoord or r["label"]!="NONE": bycoord[k]=r
    final=[]
    for k in sorted(bycoord):
        r=dict(bycoord[k]); r["provenance"]=sorted(prov[k]); final.append(r)
    manifest=[{k:r[k] for k in ("document","sentence","start","end","label","provenance")} for r in final]
    manifest_sha=htxt(json.dumps(manifest,sort_keys=True,separators=(",",":")))
    return final,manifest_sha,{"native_slots":native_count,"fallback_slots":fallback_count,
                               "static_unique":len(neg["static_unique"]),"positives":len(positives)}

def build_raw_feature_tensor(docs,rows,hidden):
    n=len(rows)
    X=torch.empty((n,5,768),dtype=torch.float32)
    prev_edge=torch.zeros(n,dtype=torch.bool); next_edge=torch.zeros(n,dtype=torch.bool)
    width=torch.empty(n,dtype=torch.long); y=torch.empty(n,dtype=torch.long)
    zero=torch.zeros(768)
    for i,r in enumerate(rows):
        di,si,s,e=r["document"],r["sentence"],r["start"],r["end"]
        h=hidden[(di,si)]; ln=h.shape[0]
        if not (0<=s<e<=ln) or e-s>64: raise RuntimeError("bad feature coordinate")
        X[i,0]=h[s]; X[i,1]=h[e-1]; X[i,2]=h[s:e].mean(0)
        if s>0: X[i,3]=h[s-1]
        else: X[i,3]=zero; prev_edge[i]=True
        if e<ln: X[i,4]=h[e]
        else: X[i,4]=zero; next_edge[i]=True
        width[i]=e-s; y[i]=C2I[r["label"]]
    return X,prev_edge,next_edge,width,y

def head_forward(model,X,pe,ne,w):
    return model(X[:,0],X[:,1],X[:,2],X[:,3],X[:,4],pe,ne,w)

def train_head(cls,X,pe,ne,w,y,name,status_path):
    seed_all(); model=cls()
    want=579461 if name=="H0" else 662666
    got=sum(p.numel() for p in model.parameters() if p.requires_grad)
    if got!=want: raise RuntimeError(f"{name} param mismatch {got}")
    opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=.01)
    bs=64; steps_per_epoch=math.ceil(len(y)/bs); total_steps=10*steps_per_epoch
    scheduler=torch.optim.lr_scheduler.LambdaLR(opt,lambda step:max(0.0,1.0-step/max(1,total_steps)))
    # Reset after model init so dropout RNG is shared prospectively across H0/H1.
    seed_all()
    step=0; latest=None
    for epoch in range(10):
        g=torch.Generator().manual_seed(SEED+epoch)
        order=torch.randperm(len(y),generator=g)
        model.train()
        for st in range(0,len(y),bs):
            ix=order[st:st+bs]
            opt.zero_grad()
            logits=head_forward(model,X[ix],pe[ix],ne[ix],w[ix])
            loss=nn.CrossEntropyLoss()(logits,y[ix]); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
            opt.step(); scheduler.step(); step+=1; latest=float(loss.detach())
            if step%20==0 or step==total_steps:
                dump(status_path,{"state":"RUNNING","current_stage":"HEAD_TRAINING","active_head":name,
                    "progress_percent":round((0 if name=="H0" else 50)+50*step/total_steps,2),
                    "current_epoch":epoch+1,"max_epochs":10,"global_step":step,"total_steps":total_steps,
                    "latest_loss":latest,"last_progress_at":utc_now(),"failure_or_stall_reason":None})
    model.eval()
    return model,{"steps":step,"epochs":10,"final_loss":latest,"parameters":got}

def proposal_items(docs,doc_ids,b_preds):
    items=[]
    for di in sorted(doc_ids):
        for si,(tokens,tags) in enumerate(docs[di]):
            for q in b_preds[(di,si)]:
                items.append({"document":di,"sentence":si,"start":q["start"],"end":q["end"],
                    "type":q["type"],"b_conf":q["b_conf"],"tokens":tokens})
    return items

def attach_evidence(items,boundary_probs,type_probs,hidden,docs):
    if len(items)!=len(type_probs): raise RuntimeError("type probs mismatch")
    rows=[]
    for item,tp in zip(items,type_probs):
        r=dict(item); di,si,s,e=r["document"],r["sentence"],r["start"],r["end"]
        bp=boundary_probs[(di,si)]
        r["start_prob"]=float(bp["start"][s]); r["end_prob"]=float(bp["end"][e-1])
        r["type_probs"]=[float(x) for x in tp]
        rows.append(r)
    return rows

def pair_probs(model,X,pe,ne,w,batch=256):
    vals=[]
    model.eval()
    with torch.no_grad():
        for st in range(0,len(w),batch):
            sl=slice(st,min(len(w),st+batch))
            vals.append(torch.softmax(head_forward(model,X[sl],pe[sl],ne[sl],w[sl]),dim=-1).cpu())
    return torch.cat(vals,dim=0).numpy() if vals else np.zeros((0,5))

def metric_counts(docs,doc_ids,items,pair_p,t):
    gold={}
    counts={c:{"tp":0,"fp":0,"fn":0,"accepted":0,"gold":0} for c in CLASSES[1:]}
    for di in sorted(doc_ids):
        for si,(tokens,tags) in enumerate(docs[di]):
            sps,bad,_=spans_for_sentence(docs[di],si)
            if bad: raise RuntimeError("bad SELECT gold")
            g={(c,s,e) for c,s,e in sps}; gold[(di,si)]=g
            for c,_,_ in g: counts[c]["gold"]+=1
    accepted=collections.defaultdict(set)
    accepted_rows=[]
    for idx,r in enumerate(items):
        typ,s,e=r["type"],r["start"],r["end"]
        if r["b_conf"]<t or r["start_prob"]<.25 or r["end_prob"]<.25 or e-s>64: continue
        tp=np.asarray(r["type_probs"])
        same=float(tp[["P","I","C","O"].index(typ)])
        if same<t: continue
        if any(float(tp[j])>=t for j,c in enumerate(["P","I","C","O"]) if c!=typ): continue
        pp=pair_p[idx]; top=int(np.argmax(pp))
        if CLASSES[top]!=typ or float(pp[top])<t: continue
        k=(typ,s,e); accepted[(r["document"],r["sentence"])].add(k)
        counts[typ]["accepted"]+=1
        ok=k in gold[(r["document"],r["sentence"])]
        counts[typ]["tp" if ok else "fp"]+=1
        accepted_rows.append({"document":r["document"],"sentence":r["sentence"],"type":typ,"start":s,"end":e,
                              "pair_conf":float(pp[top]),"is_tp":ok})
    for key,g in gold.items():
        for c,s,e in g:
            if (c,s,e) not in accepted[key]: counts[c]["fn"]+=1
    per={}
    for c,d in counts.items():
        p=d["tp"]/(d["tp"]+d["fp"]) if d["tp"]+d["fp"] else 0.0
        rr=d["tp"]/(d["tp"]+d["fn"]) if d["tp"]+d["fn"] else 0.0
        per[c]={**d,"precision":p,"recall":rr}
    macro_p=sum(per[c]["precision"] for c in per)/4
    macro_r=sum(per[c]["recall"] for c in per)/4
    passes=all(per[c]["precision"]>=.90 and per[c]["recall"]>=.20 and per[c]["accepted"]>=10 for c in per) and macro_p>=.90
    return {"threshold":t,"per_class":per,"macro_precision":macro_p,"macro_recall":macro_r,"passes":passes,
            "accepted_rows":accepted_rows}

def cstyle_metrics(docs,doc_ids,items,t):
    # same as metric_counts without pair head.
    pair=np.ones((len(items),5),dtype=float)
    for i,r in enumerate(items):
        pair[i,:]=0; pair[i,C2I[r["type"]]]=1.0
    return metric_counts(docs,doc_ids,items,pair,t)

def candidate_ceiling(docs,doc_ids,items):
    gold=collections.Counter(); avail=collections.Counter(); exact_seen=set()
    fp=0
    goldset=collections.defaultdict(set)
    for di in sorted(doc_ids):
        for si,(tokens,tags) in enumerate(docs[di]):
            sps,bad,_=spans_for_sentence(docs[di],si)
            if bad: raise RuntimeError("bad gold")
            for c,s,e in sps: gold[c]+=1; goldset[(di,si)].add((c,s,e))
    for r in items:
        k=(r["type"],r["start"],r["end"]); dk=(r["document"],r["sentence"])
        if k in goldset[dk]:
            if (dk,k) not in exact_seen: avail[r["type"]]+=1; exact_seen.add((dk,k))
        else: fp+=1
    return {"candidate_count":len(items),"candidate_fp":fp,
            "per_class":{c:{"gold":gold[c],"exact_tp_available":avail[c],
                "max_recall":avail[c]/gold[c] if gold[c] else 0.0,
                "support_floor_possible":avail[c]>=10,
                "recall_floor_possible":(avail[c]/gold[c] if gold[c] else 0)>=.20} for c in gold}}

def fp_taxonomy(docs,doc_ids,accepted_rows):
    gold_by=collections.defaultdict(list)
    for di in sorted(doc_ids):
        for si,(tokens,tags) in enumerate(docs[di]):
            sps,bad,_=spans_for_sentence(docs[di],si)
            for c,s,e in sps: gold_by[(di,si)].append((c,s,e))
    cnt=collections.Counter()
    for r in accepted_rows:
        if r["is_tp"]: continue
        typ,s,e=r["type"],r["start"],r["end"]; gs=gold_by[(r["document"],r["sentence"])]
        exact_other=[g for g in gs if g[1]==s and g[2]==e and g[0]!=typ]
        if exact_other: cnt["DIFFERENT_CLASS_EXACT_BOUNDARY"]+=1; continue
        ov=[g for g in gs if overlap(s,e,g[1],g[2])]
        if ov:
            if any(g[0]==typ for g in ov): cnt["SAME_CLASS_WRONG_BOUNDARY_OVERLAP"]+=1
            else: cnt["DIFFERENT_CLASS_WRONG_BOUNDARY_OVERLAP"]+=1
        else: cnt["SPURIOUS_NO_OVERLAP"]+=1
    return dict(cnt)

def bootstrap_docs(docs,doc_ids,items,pair_p,t,reps=2000):
    # Compact document-cluster bootstrap for macro precision/recall only.
    ids=sorted(doc_ids); rng=np.random.default_rng(SEED)
    # Build per-document gold and accepted sufficient statistics.
    base=metric_counts(docs,doc_ids,items,pair_p,t)
    acc_by=collections.defaultdict(list)
    for r in base["accepted_rows"]: acc_by[r["document"]].append(r)
    gold_by_doc={d:collections.Counter() for d in ids}
    for di in ids:
        for si,(tokens,tags) in enumerate(docs[di]):
            sps,bad,_=spans_for_sentence(docs[di],si)
            for c,_,_ in sps: gold_by_doc[di][c]+=1
    vals=[]
    for _ in range(reps):
        sample=rng.choice(ids,size=len(ids),replace=True)
        tp=collections.Counter(); fp=collections.Counter(); gold=collections.Counter()
        for d in sample:
            gold.update(gold_by_doc[d])
            for r in acc_by[d]:
                if r["is_tp"]:
                    tp[r["type"]]+=1
                else:
                    fp[r["type"]]+=1
        ps=[]; rs=[]
        for c in ["P","I","C","O"]:
            p=tp[c]/(tp[c]+fp[c]) if tp[c]+fp[c] else 0.0
            rr=tp[c]/gold[c] if gold[c] else 0.0
            ps.append(p); rs.append(rr)
        vals.append((sum(ps)/4,sum(rs)/4))
    arr=np.asarray(vals)
    return {"replicates":reps,"seed":SEED,
        "macro_precision_q025_q50_q975":[float(x) for x in np.quantile(arr[:,0],[.025,.5,.975])],
        "macro_recall_q025_q50_q975":[float(x) for x in np.quantile(arr[:,1],[.025,.5,.975])]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path)
    ap.add_argument("--split-manifest",type=pathlib.Path)
    ap.add_argument("--b-model",type=pathlib.Path)
    ap.add_argument("--boundary-model",type=pathlib.Path)
    ap.add_argument("--type-model",type=pathlib.Path)
    ap.add_argument("--out",type=pathlib.Path)
    ap.add_argument("--mechanics-only",action="store_true")
    args=ap.parse_args()
    if args.mechanics_only:
        print(json.dumps({"state":"R43_STAGE_B_MECHANICS_PASS","head_mechanics":head_mechanics()},indent=2,sort_keys=True))
        return
    for x in [args.train,args.split_manifest,args.b_model,args.boundary_model,args.type_model,args.out]:
        if x is None: raise SystemExit("missing required arg")
    args.out.mkdir(parents=True,exist_ok=False); seed_all()
    status=args.out/"PROCESS_STATUS.json"
    if sha256_path(args.train)!=EXPECTED_TRAIN_SHA: raise RuntimeError("train hash mismatch")
    manifest=json.loads(args.split_manifest.read_text())
    if manifest.get("manifest_sha256")!=EXPECTED_SPLIT_SHA: raise RuntimeError("split manifest mismatch")
    fit=set(); select=set()
    for e in manifest["entries"]:
        (fit if e["partition"]=="FIT" else select).update(e["documents"])
    if len(fit)!=320 or len(select)!=80 or fit&select: raise RuntimeError("split membership mismatch")
    docs,empty,bad=parse_train(args.train)
    if bad: raise RuntimeError(f"source errors {bad[:3]}")

    # Models are frozen ancestors. Caller/workflow verifies their hashes against Stage-A summary too.
    tok=AutoTokenizer.from_pretrained(args.boundary_model,local_files_only=True,use_fast=True)
    bmodel=BertForTokenClassification.from_pretrained(args.b_model,local_files_only=True)
    boundary=BertForTokenClassification.from_pretrained(args.boundary_model,local_files_only=True)
    tmodel=BertForSequenceClassification.from_pretrained(args.type_model,local_files_only=True)
    for m in (bmodel,boundary,tmodel):
        m.eval()
        if any(not torch.isfinite(p).all() for p in m.parameters()): raise RuntimeError("nonfinite ancestor")

    fit_sent=make_sentence_rows(docs,fit); sel_sent=make_sentence_rows(docs,select)
    dump(status,{"state":"RUNNING","progress_percent":2.0,"current_stage":"ANCESTOR_INFERENCE",
        "last_progress_at":utc_now(),"failure_or_stall_reason":None})

    fit_b=infer_b(bmodel,tok,fit_sent); sel_b=infer_b(bmodel,tok,sel_sent)
    boundary_probs,hidden=infer_boundary_and_context(boundary,tok,fit_sent+sel_sent)
    fit_examples,final_manifest_sha,slot_counts=materialize_final_fit_examples(docs,fit,fit_b)

    # Add tokens to type inference proposal rows.
    fit_props=proposal_items(docs,fit,fit_b); sel_props=proposal_items(docs,select,sel_b)

    # Candidate ceiling is a pre-head stop rule. Do not train H0/H1 when
    # native SELECT proposals cannot mathematically satisfy support/recall.
    ceiling=candidate_ceiling(docs,select,sel_props)
    ceiling_block=any((not d["support_floor_possible"]) or (not d["recall_floor_possible"]) for d in ceiling["per_class"].values())
    if ceiling_block:
        summary={
          "state":"R43_STAGE_B_STOPPED_AT_CANDIDATE_CEILING",
          "decision":"STOP_H0_H1_AS_INSUFFICIENT_CANDIDATE_CEILING",
          "nominated":None,
          "train_sha256":EXPECTED_TRAIN_SHA,
          "split_manifest_sha256":EXPECTED_SPLIT_SHA,
          "candidate_ceiling":ceiling,
          "candidate_ceiling_block":True,
          "ancestor_model_sha256":{
            "B":sha256_path(args.b_model/"model.safetensors"),
            "BOUNDARY":sha256_path(args.boundary_model/"model.safetensors"),
            "TYPE":sha256_path(args.type_model/"model.safetensors")},
          "guards":{"h0_h1_training_performed":False,"select_used_for_training":False,
            "historical_dev_read":False,"test_read":False,"other_folds_read":False,
            "factpico_used":False,"consumed_60_rct_holdout_used":False},
          "stop_boundary":"STOP_AND_REOPEN_CANDIDATE_REPAIR_DESIGN"
        }
        dump(args.out/"R43_STAGE_B_H0_H1_SUMMARY.json",summary)
        dump(status,{"state":"COMPLETED_WITH_CANDIDATE_CEILING_BLOCK","progress_percent":100.0,
            "current_stage":"CANDIDATE_CEILING_STOP","last_progress_at":utc_now(),
            "failure_or_stall_reason":None,"next_expected_step":"REOPEN_CANDIDATE_REPAIR_DESIGN"})
        print(json.dumps(summary,indent=2,sort_keys=True))
        return

    fit_type=infer_type(tmodel,tok,fit_props); sel_type=infer_type(tmodel,tok,sel_props)
    fit_props=attach_evidence(fit_props,boundary_probs,fit_type,hidden,docs)
    sel_props=attach_evidence(sel_props,boundary_probs,sel_type,hidden,docs)

    # Build shared raw contextual cache for H0/H1 training.
    X,pe,ne,w,y=build_raw_feature_tensor(docs,fit_examples,hidden)
    dump(status,{"state":"RUNNING","progress_percent":8.0,"current_stage":"FINAL_MANIFEST_FROZEN",
        "fit_examples":len(fit_examples),"final_manifest_sha256":final_manifest_sha,
        "last_progress_at":utc_now(),"failure_or_stall_reason":None})
    final_manifest=[{k:r[k] for k in ("document","sentence","start","end","label","provenance")} for r in fit_examples]
    dump(args.out/"R43_FINAL_H0_H1_FIT_MANIFEST.json",{"manifest_sha256":final_manifest_sha,"examples":final_manifest})

    h0,h0train=train_head(H0,X,pe,ne,w,y,"H0",status)
    h1,h1train=train_head(H1,X,pe,ne,w,y,"H1",status)
    save_file({k:v.detach().cpu().contiguous() for k,v in h0.state_dict().items()},str(args.out/"H0.safetensors"))
    save_file({k:v.detach().cpu().contiguous() for k,v in h1.state_dict().items()},str(args.out/"H1.safetensors"))

    # SELECT features are only native B proposals.
    sel_feature_rows=[{"document":r["document"],"sentence":r["sentence"],"start":r["start"],"end":r["end"],"label":"NONE"} for r in sel_props]
    Xs,pes,nes,ws,_=build_raw_feature_tensor(docs,sel_feature_rows,hidden)
    p0=pair_probs(h0,Xs,pes,nes,ws); p1=pair_probs(h1,Xs,pes,nes,ws)

    cstyle=[cstyle_metrics(docs,select,sel_props,t) for t in THRESHOLDS]
    # Remove rows to keep baseline compact.
    for x in cstyle: x.pop("accepted_rows",None)

    results={}
    for name,pair,model in [("H0",p0,h0),("H1",p1,h1)]:
        rows=[metric_counts(docs,select,sel_props,pair,t) for t in THRESHOLDS]
        compact=[]
        for rr in rows:
            tax=fp_taxonomy(docs,select,rr["accepted_rows"])
            cr=dict(rr); cr["fp_taxonomy"]=tax; cr.pop("accepted_rows",None); compact.append(cr)
        chosen=next((r for r in compact if r["passes"]),None)
        # retention vs C-style at same t
        retain=[]
        for t,base,rr in zip(THRESHOLDS,cstyle,compact):
            base_tp=sum(base["per_class"][c]["tp"] for c in ["P","I","C","O"])
            head_tp=sum(rr["per_class"][c]["tp"] for c in ["P","I","C","O"])
            base_fp=sum(base["per_class"][c]["fp"] for c in ["P","I","C","O"])
            head_fp=sum(rr["per_class"][c]["fp"] for c in ["P","I","C","O"])
            retain.append({"threshold":t,"tp_retention":head_tp/base_tp if base_tp else 0.0,
                           "fp_rejection":1-head_fp/base_fp if base_fp else 0.0,
                           "base_tp":base_tp,"head_tp":head_tp,"base_fp":base_fp,"head_fp":head_fp})
        matched=None
        for r in reversed(retain):
            if r["tp_retention"]>=.80: matched=r; break
        # Bootstrap at chosen threshold, else t=.90 as fixed descriptive fallback.
        bt=chosen["threshold"] if chosen else .90
        boot=bootstrap_docs(docs,select,sel_props,pair,bt,2000)
        results[name]={"training":h0train if name=="H0" else h1train,
            "threshold_results":compact,"chosen_calibration":chosen,
            "matched_retention_diagnostic":matched,
            "bootstrap_threshold":bt,"bootstrap":boot,
            "model_sha256":sha256_path(args.out/f"{name}.safetensors")}

    # Frozen architecture decision.
    h0c=results["H0"]["chosen_calibration"]; h1c=results["H1"]["chosen_calibration"]
    if ceiling_block:
        decision="STOP_H0_H1_AS_INSUFFICIENT_CANDIDATE_CEILING"
        nominated=None
    elif h0c is None and h1c is None:
        decision="DIAGNOSTIC_NO_ARCHITECTURE_READY"; nominated=None
    elif h0c is not None and h1c is None:
        decision="NOMINATE_H0"; nominated="H0"
    elif h1c is not None and h0c is None:
        decision="NOMINATE_H1"; nominated="H1"
    else:
        # Both pass: H1 must add >=0.02 macro recall while preserving gates.
        if h1c["macro_recall"]-h0c["macro_recall"]>=.02:
            decision="NOMINATE_H1_BY_FROZEN_RECALL_TIEBREAK"; nominated="H1"
        else:
            decision="NOMINATE_H0_BY_FROZEN_COMPLEXITY_TIEBREAK"; nominated="H0"

    summary={
      "state":"R43_STAGE_B_DIAGNOSTIC_COMPLETE",
      "decision":decision,"nominated":nominated,
      "train_sha256":EXPECTED_TRAIN_SHA,"split_manifest_sha256":EXPECTED_SPLIT_SHA,
      "static_manifest_sha256":EXPECTED_STATIC_SHA,"final_fit_manifest_sha256":final_manifest_sha,
      "slot_counts":slot_counts,"candidate_ceiling":ceiling,"candidate_ceiling_block":ceiling_block,
      "cstyle_baseline":cstyle,"heads":results,"head_mechanics":head_mechanics(),
      "ancestor_model_sha256":{
        "B":sha256_path(args.b_model/"model.safetensors"),
        "BOUNDARY":sha256_path(args.boundary_model/"model.safetensors"),
        "TYPE":sha256_path(args.type_model/"model.safetensors")},
      "guards":{"fit_only_head_training":True,"select_used_for_training":False,
        "historical_dev_read":False,"test_read":False,"other_folds_read":False,
        "factpico_used":False,"consumed_60_rct_holdout_used":False,
        "threshold_grid":THRESHOLDS,"encoder_frozen":True,"seed":SEED},
      "stop_boundary":"STOP_BEFORE_HISTORICAL_DEV_OR_PROTECTED_EXTERNAL_TESTS"
    }
    dump(args.out/"R43_STAGE_B_H0_H1_SUMMARY.json",summary)
    dump(status,{"state":"COMPLETED","progress_percent":100.0,"current_stage":"DIAGNOSTIC_COMPLETE",
        "decision":decision,"nominated":nominated,"last_progress_at":utc_now(),
        "failure_or_stall_reason":None,"next_expected_step":"FREEZE_RESULT_AND_STOP"})
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__": main()
