#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib

CLASSES=["P","I","C","O"]
SEED=42

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def htxt(x): return hashlib.sha256(x.encode("utf-8")).hexdigest()

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
    out=[]; cur=None; init=None
    if tags and tags[0].startswith("I-"):
        typ=tags[0][2:]
        if prev_last in (f"B-{typ}",f"I-{typ}"): init=typ
    for i in range(len(tags)+1):
        tag="O" if i==len(tags) else tags[i]
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur is not None:
            ct,s=cur
            if pref=="I" and typ==ct: continue
            out.append((ct,s,i)); cur=None
        if tag!="O":
            if i==0 and pref=="I" and init==typ: cur=(typ,0)
            elif pref=="B": cur=(typ,i)
            elif pref=="I": cur=(typ,i)
    return out

def pick(pool,key):
    if not pool: return None
    return min(pool,key=lambda x:htxt(key+"|"+repr(x)))

def key_surface(tokens,s,e): return "\u241f".join(tokens[s:e])
def key_ctx(tokens,s,e,w):
    a=max(0,s-w); b=min(len(tokens),e+w)
    left=tokens[a:s]; mid=tokens[s:e]; right=tokens[e:b]
    return "\u241f".join(left)+"\u241e"+"\u241f".join(mid)+"\u241e"+"\u241f".join(right)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    if sha(a.train)!="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e":
        raise RuntimeError("train mismatch")
    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226":
        raise RuntimeError("manifest mismatch")
    fit=set()
    for e in m["entries"]:
        if e["partition"]=="FIT": fit.update(e["documents"])
    docs=parse_train(a.train)

    rows=[]
    for di in sorted(fit):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            prev=doc[si-1][1][-1] if si>0 and doc[si-1][1] else None
            gs=spans(tags,prev); gold={(s,e):c for c,s,e in gs}
            for c,s,e in gs:
                rows.append({"doc":di,"sent":si,"s":s,"e":e,"label":c,"tokens":tokens,"kind":"GOLD"})
                # same frozen-style lightweight negative families: one local, one composite, one bg
                local=[]
                for ds,de in [(-2,0),(-1,0),(1,0),(2,0),(0,-2),(0,-1),(0,1),(0,2),(-1,-1),(-1,1),(1,-1),(1,1)]:
                    x,y=s+ds,e+de
                    if 0<=x<y<=len(tokens) and y-x<=64 and (x,y) not in gold: local.append((x,y))
                p=pick(local,f"{SEED}|{di}|{si}|{s}|{e}|L")
                if p:
                    x,y=p; rows.append({"doc":di,"sent":si,"s":x,"e":y,"label":"NONE","tokens":tokens,"kind":"LOCAL"})
                comp=[]
                for c2,s2,e2 in gs:
                    if (s2,e2)==(s,e): continue
                    for x,y in ((s,e2),(s2,e)):
                        if 0<=x<y<=len(tokens) and y-x<=64 and (x,y) not in gold: comp.append((x,y))
                p=pick(comp,f"{SEED}|{di}|{si}|{s}|{e}|C")
                if p:
                    x,y=p; rows.append({"doc":di,"sent":si,"s":x,"e":y,"label":"NONE","tokens":tokens,"kind":"COMPOSITE"})
                w=e-s; bg=[]
                for x in range(0,len(tokens)-w+1):
                    y=x+w
                    if (x,y) in gold: continue
                    if any(max(x,gs0)<min(y,ge0) for _,gs0,ge0 in gs): continue
                    bg.append((x,y))
                p=pick(bg,f"{SEED}|{di}|{si}|{s}|{e}|B")
                if p:
                    x,y=p; rows.append({"doc":di,"sent":si,"s":x,"e":y,"label":"NONE","tokens":tokens,"kind":"BG"})

    # gold precedence
    bycoord={}
    for r in rows:
        k=(r["doc"],r["sent"],r["s"],r["e"])
        if k not in bycoord or r["label"]!="NONE": bycoord[k]=r
    rows=list(bycoord.values())

    def conflict_summary(keyfn):
        d=collections.defaultdict(set); ex=collections.defaultdict(list)
        for r in rows:
            k=keyfn(r); d[k].add(r["label"])
            if len(ex[k])<8: ex[k].append({"doc":r["doc"],"sent":r["sent"],"label":r["label"],"kind":r["kind"]})
        bad={k:v for k,v in d.items() if len(v)>1}
        labelpairs=collections.Counter()
        for v in bad.values(): labelpairs["/".join(sorted(v))]+=1
        return {
            "unique_keys":len(d),
            "conflicting_keys":len(bad),
            "conflicting_key_rate":len(bad)/len(d) if d else 0,
            "label_set_counts":dict(labelpairs),
            "examples":[{"key":k,"labels":sorted(bad[k]),"occurrences":ex[k]} for k in list(sorted(bad))[:30]]
        }

    out={
      "state":"R43_INDEPENDENT_CONTEXT_LOCALITY_AUDIT_COMPLETE",
      "scope":"FIT_ONLY_EXPLORATORY_NON_DECISION",
      "fit_documents":len(fit),"examples":len(rows),
      "surface_only":conflict_summary(lambda r:key_surface(r["tokens"],r["s"],r["e"])),
      "context_pm1":conflict_summary(lambda r:key_ctx(r["tokens"],r["s"],r["e"],1)),
      "context_pm2":conflict_summary(lambda r:key_ctx(r["tokens"],r["s"],r["e"],2)),
      "context_pm4":conflict_summary(lambda r:key_ctx(r["tokens"],r["s"],r["e"],4)),
      "full_sentence_plus_coords":conflict_summary(lambda r:"\u241f".join(r["tokens"])+f"\u241d{r['s']}:{r['e']}"),
      "guards":{"stage_a_outputs_used":False,"select_used":False,"historical_dev_used":False,"test_used":False,
                "other_folds_used":False,"factpico_used":False,"consumed_60_rct_used":False},
      "interpretation_rule":"EXPLORATORY_ONLY; DOES_NOT_MODIFY_FROZEN_STAGE_B"
    }
    (a.out/"R43_CONTEXT_LOCALITY_AUDIT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
