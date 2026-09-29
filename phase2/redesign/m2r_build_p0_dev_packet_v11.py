#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

BASE="https://huggingface.co/datasets/khaled44/arabigee-data/resolve/main"
SALT="M2R-P0-DEV-A-V11"

def H(s): return hashlib.sha256(str(s).encode()).hexdigest()
def norm(s): return " ".join((s or "").strip().split())
def rank(*x): return H("|".join(map(str,x)))
def partition(cid):
    v=int(H(f"M2R-V1|{cid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")
def dl(name,path):
    for u in (f"{BASE}/{name}?download=true",f"{BASE}/data/{name}?download=true"):
        try:
            urllib.request.urlretrieve(u,path)
            if path.stat().st_size>20:return
        except Exception: pass
    raise RuntimeError(name)
def dims(a):
    out=[]
    if norm(a.get("orth_code")):out.append("ORTHOGRAPHY")
    if norm(a.get("morph_code")):out.append("MORPHOLOGY")
    if norm(a.get("synt_code")):out.append("SYNTAX")
    if norm(a.get("lex_code")):out.append("LEXICAL")
    return out

work=Path("upstream/arabigee");work.mkdir(parents=True,exist_ok=True)
for f in ["annotations.csv","contexts_nopnx.csv"]:dl(f,work/f)
with open(work/"annotations.csv",encoding="utf-8-sig",newline="") as f:anns=list(csv.DictReader(f))
with open(work/"contexts_nopnx.csv",encoding="utf-8-sig",newline="") as f:ctx=list(csv.DictReader(f))
by=defaultdict(list)
for a in anns:by[str(a["context_id"])].append(a)

dev=[]
reinjected=[]
for c in ctx:
    cid=str(c["context_id"])
    if partition(cid)!="DEVELOPMENT":continue
    src=norm(c["src_context"]);target=norm(c["target_context"]);aa=by.get(cid,[])
    if not src or not target or not aa:continue
    dev.append((cid,c,src,target,aa))
    candidates=[];seen=set()
    for a in aa:
        e=norm(a.get("erroneous_word"));t=norm(a.get("target_word"));ds=dims(a)
        if not e or not t or e==t or not ds:continue
        k=(e,t,tuple(ds))
        if k in seen:continue
        seen.add(k)
        if target.count(t)!=1:continue
        pos=target.find(t)
        cand=target[:pos]+e+target[pos+len(t):]
        cand=norm(cand)
        if e not in cand or cand==target:continue
        candidates.append({"candidate":cand,"surface":e,"replacement":t,"dimensions":ds,"areta_label":norm(a.get("areta_label"))})
    if candidates:
        candidates.sort(key=lambda x:rank(SALT,cid,x["surface"],x["replacement"]))
        reinjected.append((cid,c,src,target,aa,candidates[0]))

reinjected.sort(key=lambda x:rank(SALT,"REINSERT",x[0]))
sel_r=reinjected[:30]
if len(sel_r)<30:raise SystemExit(f"only {len(sel_r)} eligible reinjected cases")
used={x[0] for x in sel_r}

nat=[x for x in dev if x[0] not in used]
nat.sort(key=lambda x:rank(SALT,"NAT",x[0]))
sel_n=nat[:60]
if len(sel_n)<60:raise SystemExit("insufficient natural")
used.update(x[0] for x in sel_n)

clean=[x for x in dev if x[0] not in used]
clean.sort(key=lambda x:rank(SALT,"CLEAN",x[0]))
sel_c=clean[:30]
if len(sel_c)<30:raise SystemExit("insufficient clean")
used.update(x[0] for x in sel_c)

def gold_all(aa):
    out=[];seen=set()
    for a in aa:
        e=norm(a.get("erroneous_word"));t=norm(a.get("target_word"));ds=dims(a)
        if not e or not t or e==t or not ds:continue
        k=(e,t,tuple(ds))
        if k in seen:continue
        seen.add(k)
        out.append({"surface":e,"replacement":t,"dimensions":ds,"areta_label":norm(a.get("areta_label"))})
    return out

rows=[]
for cid,c,src,target,aa in sel_n:
    rows.append(("NATURAL_ERROR_CONTEXT",cid,c,src,gold_all(aa),False))
for cid,c,src,target,aa in sel_c:
    rows.append(("CLEAN_TARGET_CONTEXT",cid,c,target,[],False))
for cid,c,src,target,aa,x in sel_r:
    rows.append(("EXPERT_REINSERTED_RESIDUAL",cid,c,x["candidate"],[{"surface":x["surface"],"replacement":x["replacement"],"dimensions":x["dimensions"],"areta_label":x["areta_label"]}],True))

rows.sort(key=lambda x:rank(SALT,"shuffle",x[1],x[0]))
blind=[];keyrows=[];dc=Counter()
for i,(fam,cid,c,cand,gold,controlled) in enumerate(rows,1):
    case=f"M2R-P0-{i:03d}"
    for g in gold:
        for d in g["dimensions"]:dc[d]+=1
    blind.append({"case_id":case,"candidate":cand})
    keyrows.append({"case_id":case,"context_id":cid,"family":fam,"source_dataset":c.get("source_dataset"),"gold_errors":gold,"controlled_counterfactual":controlled})

fc=Counter(x["family"] for x in keyrows)
if len(blind)!=120 or len({x["context_id"] for x in keyrows})!=120:raise SystemExit("packet uniqueness/size failure")
if fc!={"NATURAL_ERROR_CONTEXT":60,"CLEAN_TARGET_CONTEXT":30,"EXPERT_REINSERTED_RESIDUAL":30}:raise SystemExit(f"family counts {fc}")
if dc["ORTHOGRAPHY"]<20:raise SystemExit(f"orth count {dc['ORTHOGRAPHY']}")
if sum(dc[d] for d in ["MORPHOLOGY","SYNTAX","LEXICAL"])<20:raise SystemExit("nonorth count")
if any(partition(x["context_id"])!="DEVELOPMENT" for x in keyrows):raise SystemExit("partition leak")

Path("M2R_P0_DEV_BLIND.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in blind)+"\n",encoding="utf-8")
Path("M2R_P0_DEV_KEY.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in keyrows)+"\n",encoding="utf-8")
summary={"status":"M2R_P0_V11_PACKET_READY","cases":120,"family_counts":dict(fc),"gold_dimension_instances":dict(dc),"eligible_reinserted_pool":len(reinjected),"development_context_pool":len(dev),"confirmation_exposed":False,"holdout_exposed":False,"salt":SALT}
Path("M2R_P0_PACKET_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
