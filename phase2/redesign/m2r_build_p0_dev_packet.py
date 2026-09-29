#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

BASE="https://huggingface.co/datasets/khaled44/arabigee-data/resolve/main"
SALT="M2R-P0-DEV-A"

def h(s): return hashlib.sha256(str(s).encode()).hexdigest()
def norm(s): return " ".join((s or "").strip().split())
def rank(*x): return h("|".join(map(str,x)))
def partition(cid):
    v=int(h(f"M2R-V1|{cid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")

def dl(name,path):
    for url in (f"{BASE}/{name}?download=true",f"{BASE}/data/{name}?download=true"):
        try:
            urllib.request.urlretrieve(url,path)
            if path.stat().st_size>20: return
        except Exception:
            pass
    raise RuntimeError(name)

def dim(a):
    out=[]
    if norm(a.get("orth_code")): out.append("ORTHOGRAPHY")
    if norm(a.get("morph_code")): out.append("MORPHOLOGY")
    if norm(a.get("synt_code")): out.append("SYNTAX")
    if norm(a.get("lex_code")): out.append("LEXICAL")
    return out or ["OTHER"]

def locate_unique(text,surface):
    if not surface: return None
    starts=[]; pos=0
    while True:
        i=text.find(surface,pos)
        if i<0: break
        starts.append(i); pos=i+max(1,len(surface))
    return (starts[0],starts[0]+len(surface)) if len(starts)==1 else None

def build_all_but_one(src,target,anns,cid):
    pairs=[]
    seen=set()
    for a in anns:
        e=norm(a.get("erroneous_word")); t=norm(a.get("target_word"))
        if not e or e==t: continue
        k=(e,t)
        if k in seen: continue
        seen.add(k)
        span=locate_unique(src,e)
        if span is None: return None
        pairs.append({"surface":e,"replacement":t,"span":span,"dimensions":dim(a)})
    if len(pairs)<2: return None
    spans=sorted((p["span"][0],p["span"][1]) for p in pairs)
    if any(spans[i][1]>spans[i+1][0] for i in range(len(spans)-1)): return None

    def apply(skip=None):
        text=src
        selected=[(i,p) for i,p in enumerate(pairs) if i!=skip]
        for i,p in sorted(selected,key=lambda z:z[1]["span"][0],reverse=True):
            a,b=p["span"]; text=text[:a]+p["replacement"]+text[b:]
        return norm(text)

    if apply(None)!=target: return None
    wi=int(rank(SALT,cid,"withheld")[:8],16)%len(pairs)
    cand=apply(wi)
    w=pairs[wi]
    if cand.count(w["surface"])!=1: return None
    return cand,w,len(pairs)

work=Path("upstream/arabigee"); work.mkdir(parents=True,exist_ok=True)
for f in ["annotations.csv","contexts_nopnx.csv"]:
    dl(f,work/f)

with open(work/"annotations.csv",encoding="utf-8-sig",newline="") as fh:
    anns=list(csv.DictReader(fh))
with open(work/"contexts_nopnx.csv",encoding="utf-8-sig",newline="") as fh:
    ctx=list(csv.DictReader(fh))

byctx=defaultdict(list)
for a in anns: byctx[str(a["context_id"])].append(a)

dev=[]
abo=[]
for c in ctx:
    cid=str(c["context_id"])
    if partition(cid)!="DEVELOPMENT": continue
    src=norm(c["src_context"]); target=norm(c["target_context"])
    aa=byctx.get(cid,[])
    if not src or not target or not aa: continue
    dev.append((cid,c,src,target,aa))
    x=build_all_but_one(src,target,aa,cid)
    if x is not None: abo.append((cid,c,src,target,aa,x))

abo.sort(key=lambda x:rank(SALT,"ABO",x[0]))
sel_abo=abo[:30]
if len(sel_abo)<30: raise SystemExit(f"only {len(sel_abo)} reconstructable ABO")
used={x[0] for x in sel_abo}

nat=[x for x in dev if x[0] not in used]
nat.sort(key=lambda x:rank(SALT,"NAT",x[0]))
sel_nat=nat[:60]
if len(sel_nat)<60: raise SystemExit("insufficient NAT")
used.update(x[0] for x in sel_nat)

clean=[x for x in dev if x[0] not in used]
clean.sort(key=lambda x:rank(SALT,"CLEAN",x[0]))
sel_clean=clean[:30]
if len(sel_clean)<30: raise SystemExit("insufficient CLEAN")
used.update(x[0] for x in sel_clean)

blind=[]; keyrows=[]; gold_dims=Counter()
def ann_gold(aa):
    out=[]
    seen=set()
    for a in aa:
        e=norm(a.get("erroneous_word")); t=norm(a.get("target_word"))
        if not e or e==t: continue
        k=(e,t,tuple(dim(a)))
        if k in seen: continue
        seen.add(k)
        ds=dim(a)
        for d in ds: gold_dims[d]+=1
        out.append({"surface":e,"replacement":t,"dimensions":ds,"areta_label":norm(a.get("areta_label"))})
    return out

rows=[]
for x in sel_nat:
    cid,c,src,target,aa=x
    rows.append(("NATURAL_ERROR_CONTEXT",cid,c,src,ann_gold(aa),{"controlled":False}))
for x in sel_clean:
    cid,c,src,target,aa=x
    rows.append(("CLEAN_TARGET_CONTEXT",cid,c,target,[],{"controlled":False}))
for x in sel_abo:
    cid,c,src,target,aa,(cand,w,total)=x
    for d in w["dimensions"]: gold_dims[d]+=1
    rows.append(("ALL_BUT_ONE_RESIDUAL",cid,c,cand,[{"surface":w["surface"],"replacement":w["replacement"],"dimensions":w["dimensions"],"areta_label":None}],{"controlled":True,"original_error_pair_count":total}))

rows.sort(key=lambda x:rank(SALT,"shuffle",x[1],x[0]))
for i,(fam,cid,c,candidate,gold,meta) in enumerate(rows,1):
    case=f"M2R-P0-{i:03d}"
    blind.append({"case_id":case,"candidate":candidate})
    keyrows.append({
      "case_id":case,
      "context_id":cid,
      "family":fam,
      "source_dataset":c.get("source_dataset"),
      "gold_errors":gold,
      **meta
    })

if len(blind)!=120 or len(keyrows)!=120: raise SystemExit("packet size failure")
if len({r["context_id"] for r in keyrows})!=120: raise SystemExit("context overlap")
if sum(r["family"]=="ALL_BUT_ONE_RESIDUAL" for r in keyrows)!=30: raise SystemExit("ABO count")
if gold_dims["ORTHOGRAPHY"]<20: raise SystemExit(f"orth gold too small {gold_dims['ORTHOGRAPHY']}")
if sum(gold_dims[d] for d in ["MORPHOLOGY","SYNTAX","LEXICAL"])<20: raise SystemExit("nonorth gold too small")
if any(partition(r["context_id"])!="DEVELOPMENT" for r in keyrows): raise SystemExit("partition leak")

Path("M2R_P0_DEV_BLIND.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in blind)+"\n",encoding="utf-8")
Path("M2R_P0_DEV_KEY.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in keyrows)+"\n",encoding="utf-8")
summary={
  "status":"M2R_P0_PACKET_READY",
  "cases":120,
  "family_counts":dict(Counter(r["family"] for r in keyrows)),
  "unique_context_ids":120,
  "gold_dimension_instances":dict(gold_dims),
  "all_but_one_reconstructable_pool":len(abo),
  "development_context_pool":len(dev),
  "confirmation_exposed":False,
  "holdout_exposed":False,
  "salt":SALT
}
Path("M2R_P0_PACKET_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
