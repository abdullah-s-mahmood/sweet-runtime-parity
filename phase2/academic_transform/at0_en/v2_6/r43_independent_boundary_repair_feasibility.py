#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib

CLASSES=["P","I","C","O"]
MAX_WIDTH=64
RADIUS=4

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

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
    out=[]; cur=None
    initial_type=None
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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    if sha(a.train)!="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e":
        raise RuntimeError("train hash mismatch")
    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226":
        raise RuntimeError("manifest mismatch")
    fit=set()
    for e in m["entries"]:
        if e["partition"]=="FIT": fit.update(e["documents"])
    docs=parse_train(a.train)

    sent_rows={}
    gold_total=collections.Counter()
    for di in sorted(fit):
        doc=docs[di]
        for si,(ts,ys) in enumerate(doc):
            prev=doc[si-1][1][-1] if si>0 and doc[si-1][1] else None
            gs=spans(ys,prev)
            sent_rows[(di,si)]={"n":len(ts),"gold":gs}
            for c,_,_ in gs: gold_total[c]+=1

    candidates={}
    for key,row in sent_rows.items():
        n=row["n"]; gs=row["gold"]; gold_coords={(s,e):c for c,s,e in gs}
        for c,s,e in gs:
            for ds in range(-RADIUS,RADIUS+1):
                for de in range(-RADIUS,RADIUS+1):
                    if ds==0 and de==0: continue
                    a0=s+ds; b0=e+de
                    if not (0<=a0<b0<=n): continue
                    if b0-a0>MAX_WIDTH: continue
                    if (a0,b0) in gold_coords: continue
                    k=(key[0],key[1],a0,b0)
                    rec=candidates.setdefault(k,{"sources":set(),"sentence":key})
                    rec["sources"].add((c,s,e))
    # Dedup and analyze nearest-gold target ambiguity.
    stats=collections.Counter()
    class_stats={c:collections.Counter() for c in CLASSES}
    delta_hist=collections.Counter()
    ambiguous_examples=[]
    for (di,si,a0,b0),rec in candidates.items():
        gs=sent_rows[(di,si)]["gold"]
        if not gs: continue
        dists=[(abs(a0-s)+abs(b0-e),c,s,e) for c,s,e in gs]
        mind=min(x[0] for x in dists)
        nearest=[x for x in dists if x[0]==mind]
        stats["candidates"]+=1
        stats[f"nearest_distance_{mind}"]+=1
        if len(nearest)==1:
            stats["unique_nearest"]+=1
            _,c,s,e=nearest[0]
            ds=s-a0; de=e-b0
            delta_hist[(ds,de)]+=1
            class_stats[c]["unique_nearest"]+=1
            class_stats[c][f"distance_{mind}"]+=1
            for lim in (1,2,4):
                if max(abs(ds),abs(de))<=lim:
                    stats[f"repairable_within_pm{lim}"]+=1
                    class_stats[c][f"repairable_within_pm{lim}"]+=1
        else:
            stats["nearest_tie_ambiguous"]+=1
            if len(ambiguous_examples)<30:
                ambiguous_examples.append({"document":di,"sentence":si,"candidate":[a0,b0],
                    "nearest":[{"distance":d,"class":c,"start":s,"end":e} for d,c,s,e in nearest]})

        source_types={x[0] for x in rec["sources"]}
        if len(source_types)==1: stats["single_source_type"]+=1
        else: stats["multi_source_type"]+=1

    # Composite repairability.
    comp=collections.Counter()
    for (di,si),row in sent_rows.items():
        gs=row["gold"]; gold_coords={(s,e) for _,s,e in gs}
        seen=set()
        for i,(c1,s1,e1) in enumerate(gs):
            for j,(c2,s2,e2) in enumerate(gs):
                if i==j: continue
                for a0,b0 in ((s1,e2),(s2,e1)):
                    if not (0<=a0<b0<=row["n"]) or b0-a0>MAX_WIDTH or (a0,b0) in gold_coords: continue
                    if (a0,b0) in seen: continue
                    seen.add((a0,b0)); comp["total"]+=1
                    dists=[(abs(a0-s)+abs(b0-e),c,s,e) for c,s,e in gs]
                    mind=min(x[0] for x in dists)
                    near=[x for x in dists if x[0]==mind]
                    if len(near)==1:
                        comp["unique_nearest"]+=1
                        d,c,s,e=near[0]
                        ds=s-a0; de=e-b0
                        for lim in (1,2,4):
                            if max(abs(ds),abs(de))<=lim: comp[f"repairable_within_pm{lim}"]+=1
                    else: comp["ambiguous"]+=1

    out={
      "state":"R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_COMPLETE",
      "scope":"FIT_ONLY_EXPLORATORY_NON_DECISION",
      "fit_documents":len(fit),
      "gold_counts":dict(gold_total),
      "radius":RADIUS,
      "candidate_stats":dict(stats),
      "class_stats":{c:dict(v) for c,v in class_stats.items()},
      "top_offset_targets":[{"delta_start":k[0],"delta_end":k[1],"count":v} for k,v in delta_hist.most_common(30)],
      "ambiguous_nearest_examples":ambiguous_examples,
      "composite_stats":dict(comp),
      "guards":{"stage_a_outputs_used":False,"select_used":False,"historical_dev_used":False,"test_used":False,
                "other_folds_used":False,"factpico_used":False,"consumed_60_rct_used":False},
      "interpretation_rule":"EXPLORATORY_ONLY; DOES_NOT_MODIFY_FROZEN_STAGE_B"
    }
    (a.out/"R43_BOUNDARY_REPAIR_FEASIBILITY.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
