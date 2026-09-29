#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

BASE="https://huggingface.co/datasets/khaled44/arabigee-data/resolve/main"

def H(s): return hashlib.sha256(str(s).encode()).hexdigest()
def norm(s): return " ".join((s or "").strip().split())
def partition(cid):
    v=int(H(f"M2R-V1|{cid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")
def dl(name,path):
    for u in (f"{BASE}/{name}?download=true",f"{BASE}/data/{name}?download=true"):
        try:
            urllib.request.urlretrieve(u,path)
            if path.stat().st_size>20:return
        except: pass
    raise RuntimeError(name)
def positions(text,surface):
    out=[]; p=0
    while surface:
        i=text.find(surface,p)
        if i<0:break
        out.append(i); p=i+max(1,len(surface))
    return out

work=Path("upstream/arabigee");work.mkdir(parents=True,exist_ok=True)
for f in ["annotations.csv","contexts_nopnx.csv"]: dl(f,work/f)
with open(work/"annotations.csv",encoding="utf-8-sig",newline="") as f: anns=list(csv.DictReader(f))
with open(work/"contexts_nopnx.csv",encoding="utf-8-sig",newline="") as f: ctx=list(csv.DictReader(f))
by=defaultdict(list)
for a in anns: by[str(a["context_id"])].append(a)

cnt=Counter(); samples=[]
for c in ctx:
    cid=str(c["context_id"])
    if partition(cid)!="DEVELOPMENT": continue
    aa=by.get(cid,[])
    pairs=[];seen=set()
    for a in aa:
        e=norm(a.get("erroneous_word"));t=norm(a.get("target_word"))
        if e and e!=t and (e,t) not in seen:
            seen.add((e,t));pairs.append((e,t,a.get("error_id"),a.get("pair_id")))
    if len(pairs)<2: continue
    cnt["multi_pair_contexts"]+=1
    src=norm(c["src_context"]); tgt=norm(c["target_context"])
    maps=[]
    bad=False
    for e,t,eid,pid in pairs:
        ps=positions(src,e)
        maps.append((e,t,ps,eid,pid))
        if len(ps)==0: cnt["surface_missing_contexts"]+=1; bad=True; break
        if len(ps)>1: cnt["surface_nonunique_contexts"]+=1; bad=True; break
    if bad:
        if len(samples)<8:
            samples.append({"context_id":cid,"reason":"surface_missing_or_nonunique","src":src,"target":tgt,"pairs":[{"e":x[0],"t":x[1],"positions":x[2],"error_id":x[3],"pair_id":x[4]} for x in maps]})
        continue
    spans=sorted((ps[0],ps[0]+len(e),e,t) for e,t,ps,_,_ in maps)
    if any(spans[i][1]>spans[i+1][0] for i in range(len(spans)-1)):
        cnt["overlap_contexts"]+=1
        if len(samples)<8:samples.append({"context_id":cid,"reason":"overlap","src":src,"target":tgt,"pairs":pairs})
        continue
    text=src
    for a,b,e,t in sorted(spans,reverse=True):
        text=text[:a]+t+text[b:]
    built=norm(text)
    if built!=tgt:
        cnt["full_reconstruction_mismatch"]+=1
        if len(samples)<8:
            samples.append({"context_id":cid,"reason":"full_reconstruction_mismatch","src":src,"target":tgt,"built":built,"pairs":[{"e":e,"t":t} for e,t,_,_,_ in maps]})
        continue
    cnt["reconstructable"]+=1

summary={"status":"M2R_ABO_DIAGNOSTIC","development_only":True,"counts":dict(cnt),"sample_count":len(samples)}
Path("M2R_ABO_DIAGNOSTIC_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
Path("M2R_ABO_DIAGNOSTIC_DEV_SAMPLES.json").write_text(json.dumps(samples,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
