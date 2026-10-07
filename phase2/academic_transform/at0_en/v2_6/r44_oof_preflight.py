#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, math, pathlib
from typing import Dict, List, Tuple
from r43_contextual_pair_preflight import parse_train, canonical_doc_tokens, canonical_doc_tags

SEED=44
TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
R43_SPLIT_SHA="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226"
CLASSES=["P","I","C","O"]

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_text(s): return sha_bytes(s.encode("utf-8"))
def file_sha(p): return sha_bytes(pathlib.Path(p).read_bytes())

def source_spans(tags):
    """Source-compatible: only B-X starts an entity; initial I-X never starts one."""
    out=[]; i=0
    while i<len(tags):
        t=tags[i]
        if t.startswith("B-"):
            typ=t[2:]; j=i+1
            while j<len(tags) and tags[j]==f"I-{typ}": j+=1
            out.append((typ,i,j)); i=j
        else:
            i+=1
    return out

def section_assign(doc):
    cur="UNKNOWN"; rows=[]
    for si,(tokens,tags) in enumerate(doc):
        head=[x.lower() for x in tokens[:3]]
        if len(tokens)>=1 and tokens[0].lower()=="title":
            cur="TITLE"
        elif len(tokens)>=1 and tokens[0].lower() in {"methods","method"}:
            cur="METHODS"
        rows.append(cur)
    return rows

def doc_stats(docs,di):
    doc=docs[di]; sec=section_assign(doc)
    cc=collections.Counter(); goldless=0; ntok=0; secct=collections.Counter()
    continuations=[]
    for si,(tokens,tags) in enumerate(doc):
        ntok+=len(tokens); secct[sec[si]]+=1
        sps=source_spans(tags)
        if not sps: goldless+=1
        for c,s,e in sps: cc[c]+=1
        if tags and tags[0].startswith("I-"):
            typ=tags[0][2:]; prev=doc[si-1][1][-1] if si>0 and doc[si-1][1] else None
            if prev in (f"B-{typ}",f"I-{typ}"):
                continuations.append({"sentence":si,"class":typ})
            else:
                continuations.append({"sentence":si,"class":typ,"invalid":True,"previous":prev})
    tokcanon=canonical_doc_tokens(doc); tagcanon=canonical_doc_tags(doc)
    return {
      "document":di,
      "token_sha256":sha_text(tokcanon),
      "token_tag_sha256":sha_text(tokcanon+"\n"+tagcanon),
      "sentences":len(doc),"tokens":ntok,"goldless_sentences":goldless,
      "gold_counts":{c:int(cc[c]) for c in CLASSES},
      "section_counts":{k:int(secct[k]) for k in ["TITLE","METHODS","UNKNOWN"]},
      "continuation_fragments":continuations
    }

def sum_stats(rows):
    c=collections.Counter(); sc=collections.Counter(); docs=0; toks=0; goldless=0; sents=0
    for r in rows:
        docs+=1; toks+=r["tokens"]; goldless+=r["goldless_sentences"]; sents+=r["sentences"]
        c.update(r["gold_counts"]); sc.update(r["section_counts"])
    return {"documents":docs,"sentences":sents,"tokens":toks,"goldless_sentences":goldless,
            "gold_counts":{k:int(c[k]) for k in CLASSES},
            "section_counts":{k:int(sc[k]) for k in ["TITLE","METHODS","UNKNOWN"]}}

def objective_after(cur,row,target,weights=None):
    # scale-normalized squared deviation toward target.
    ncur=dict(cur)
    def val(key,add):
        x=ncur.get(key,0)+add; t=target[key]
        return ((x-t)/max(1.0,t))**2
    score=0.0
    score+=2.0*val("documents",1)
    score+=0.5*val("tokens",row["tokens"])
    score+=0.5*val("goldless_sentences",row["goldless_sentences"])
    for c in CLASSES:
        score+=2.0*val("gold_"+c,row["gold_counts"][c])
    score+=0.25*val("TITLE",row["section_counts"]["TITLE"])
    score+=0.25*val("METHODS",row["section_counts"]["METHODS"])
    return score

def flat_target(rows,fraction):
    s=sum_stats(rows)
    t={"documents":fraction*s["documents"],"tokens":fraction*s["tokens"],
       "goldless_sentences":fraction*s["goldless_sentences"],
       "TITLE":fraction*s["section_counts"]["TITLE"],
       "METHODS":fraction*s["section_counts"]["METHODS"]}
    for c in CLASSES:t["gold_"+c]=fraction*s["gold_counts"][c]
    return t

def subset_objective(rows,target):
    s=sum_stats(rows)
    vals={
      "documents":s["documents"],"tokens":s["tokens"],"goldless_sentences":s["goldless_sentences"],
      "TITLE":s["section_counts"]["TITLE"],"METHODS":s["section_counts"]["METHODS"]}
    for c in CLASSES: vals["gold_"+c]=s["gold_counts"][c]
    score=0.0
    score+=2.0*((vals["documents"]-target["documents"])/max(1.0,target["documents"]))**2
    score+=0.5*((vals["tokens"]-target["tokens"])/max(1.0,target["tokens"]))**2
    score+=0.5*((vals["goldless_sentences"]-target["goldless_sentences"])/max(1.0,target["goldless_sentences"]))**2
    for c in CLASSES:
        score+=2.0*((vals["gold_"+c]-target["gold_"+c])/max(1.0,target["gold_"+c]))**2
    score+=0.25*((vals["TITLE"]-target["TITLE"])/max(1.0,target["TITLE"]))**2
    score+=0.25*((vals["METHODS"]-target["METHODS"])/max(1.0,target["METHODS"]))**2
    return score

def optimize_pair_swaps(chosen,remain,target,seed_tag,max_swaps=1000):
    """Deterministic local optimization of the predeclared balance objective.
    It does not alter seed, target size, target statistics, tolerance or data universe.
    """
    chosen=list(chosen); remain=list(remain)
    current=subset_objective(chosen,target); swaps=[]
    for step in range(max_swaps):
        best=None
        # Exhaustive single pair exchange; deterministic tie-break only.
        for ci,a in enumerate(chosen):
            for ri,b in enumerate(remain):
                candidate=chosen.copy(); candidate[ci]=b
                score=subset_objective(candidate,target)
                if score >= current-1e-15: continue
                tie=sha_text(f"{SEED}|{seed_tag}|SWAP|{a['document']}|{b['document']}")
                rec=(score,tie,ci,ri,a,b)
                if best is None or rec[:2] < best[:2]: best=rec
        if best is None: break
        score,tie,ci,ri,a,b=best
        chosen[ci],remain[ri]=b,a
        swaps.append({"step":step+1,"out_document":a["document"],"in_document":b["document"],
                      "objective_before":current,"objective_after":score,"tie_sha256":tie})
        current=score
    return chosen,remain,{"initial_objective":None,"final_objective":current,
                           "swap_count":len(swaps),"swaps":swaps}

def greedy_subset(rows,n,seed_tag):
    target=flat_target(rows,n/len(rows))
    remain=list(rows); chosen=[]; cur=collections.Counter()
    while len(chosen)<n:
        scored=[]
        for r in remain:
            score=objective_after(cur,r,target)
            tie=sha_text(f"{SEED}|{seed_tag}|{r['token_sha256']}|{r['document']}")
            scored.append((score,tie,r))
        scored.sort(key=lambda x:(x[0],x[1]))
        r=scored[0][2]; chosen.append(r); remain.remove(r)
        cur["documents"]+=1; cur["tokens"]+=r["tokens"]; cur["goldless_sentences"]+=r["goldless_sentences"]
        cur["TITLE"]+=r["section_counts"]["TITLE"]; cur["METHODS"]+=r["section_counts"]["METHODS"]
        for c in CLASSES:cur["gold_"+c]+=r["gold_counts"][c]
    initial=subset_objective(chosen,target)
    chosen,remain,opt=optimize_pair_swaps(chosen,remain,target,seed_tag)
    opt["initial_objective"]=initial
    return chosen,remain,target,opt

def row_values(r):
    x={"documents":1,"tokens":r["tokens"],"goldless_sentences":r["goldless_sentences"],
       "TITLE":r["section_counts"]["TITLE"],"METHODS":r["section_counts"]["METHODS"]}
    for c in CLASSES:x["gold_"+c]=r["gold_counts"][c]
    return x

def rows_counter(rows):
    z=collections.Counter()
    for r in rows:z.update(row_values(r))
    return z

def fold_score(cur,target):
    # Same predeclared balance terms plus penalties for ALREADY-FROZEN hard constraints.
    score=0.0
    weights={"documents":2.0,"tokens":0.5,"goldless_sentences":0.5,"TITLE":0.25,"METHODS":0.25}
    for c in CLASSES:weights["gold_"+c]=2.0
    for key,w in weights.items():
        score+=w*((cur[key]-target[key])/max(1.0,target[key]))**2
    # Existing hard constraints from the first preflight are incorporated as
    # feasibility penalties; their values are NOT changed.
    ccount=cur["gold_C"]
    if ccount<15: score+=1000.0*(15-ccount)**2
    for c in CLASSES:
        dev=abs((cur["gold_"+c]-target["gold_"+c])/max(1.0,target["gold_"+c]))
        if dev>.25: score+=1000.0*(dev-.25)**2
    return score

def optimize_fold_swaps(folds,targets,max_swaps=1000):
    folds=[list(x) for x in folds]
    curs=[rows_counter(x) for x in folds]
    def total_score(): return sum(fold_score(curs[i],targets[i]) for i in range(len(folds)))
    initial=total_score(); current=initial; swaps=[]
    for step in range(max_swaps):
        best=None
        for i in range(len(folds)):
            for j in range(i+1,len(folds)):
                for ai,a in enumerate(folds[i]):
                    av=row_values(a)
                    for bj,b in enumerate(folds[j]):
                        bv=row_values(b)
                        ci=curs[i].copy(); cj=curs[j].copy()
                        ci.subtract(av); ci.update(bv)
                        cj.subtract(bv); cj.update(av)
                        score=current-fold_score(curs[i],targets[i])-fold_score(curs[j],targets[j])
                        score+=fold_score(ci,targets[i])+fold_score(cj,targets[j])
                        if score>=current-1e-15: continue
                        tie=sha_text(f"{SEED}|FOLDSWAP|{i}|{j}|{a['document']}|{b['document']}")
                        rec=(score,tie,i,j,ai,bj,a,b,ci,cj)
                        if best is None or rec[:2]<best[:2]:best=rec
        if best is None:break
        score,tie,i,j,ai,bj,a,b,ci,cj=best
        folds[i][ai],folds[j][bj]=b,a
        curs[i],curs[j]=ci,cj
        swaps.append({"step":step+1,"fold_a":i,"fold_b":j,"out_a":a["document"],"in_a":b["document"],
                      "objective_before":current,"objective_after":score,"tie_sha256":tie})
        current=score
    return folds,{"initial_objective":initial,"final_objective":current,
                  "swap_count":len(swaps),"swaps":swaps}

def assign_folds(rows,k=5):
    targets=[]
    sizes=[len(rows)//k + (1 if i < len(rows)%k else 0) for i in range(k)]
    for i,n in enumerate(sizes):
        frac=n/len(rows); targets.append(flat_target(rows,frac))
    folds=[[] for _ in range(k)]; curs=[collections.Counter() for _ in range(k)]
    # difficult/rare-rich docs first, deterministic.
    def hardness(r):
        rare=4*r["gold_counts"]["C"]+2*r["gold_counts"]["P"]+r["gold_counts"]["I"]+r["gold_counts"]["O"]
        return (-rare,-sum(r["gold_counts"].values()),sha_text(f"{SEED}|FOLDORDER|{r['token_sha256']}"))
    for r in sorted(rows,key=hardness):
        cand=[]
        for i in range(k):
            if len(folds[i])>=sizes[i]: continue
            score=objective_after(curs[i],r,targets[i])
            tie=sha_text(f"{SEED}|FOLDASSIGN|{i}|{r['token_sha256']}")
            cand.append((score,tie,i))
        cand.sort(); i=cand[0][2]
        folds[i].append(r); curs[i].update(row_values(r))
    folds,opt=optimize_fold_swaps(folds,targets)
    return folds,sizes,targets,opt

def deviations(actual,target):
    out={}
    mapping={"documents":actual["documents"],"tokens":actual["tokens"],"goldless_sentences":actual["goldless_sentences"],
             "TITLE":actual["section_counts"]["TITLE"],"METHODS":actual["section_counts"]["METHODS"]}
    for c in CLASSES:mapping["gold_"+c]=actual["gold_counts"][c]
    for k,v in mapping.items():
        t=target[k]; out[k]=(v-t)/max(1.0,t)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--r43-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    if file_sha(a.train)!=TRAIN_SHA: raise RuntimeError("TRAIN SHA mismatch")
    m=json.loads(a.r43_manifest.read_text())
    if m.get("manifest_sha256")!=R43_SPLIT_SHA: raise RuntimeError("R43 manifest SHA mismatch")
    parent_fit=set(); old_select=set()
    for e in m["entries"]:
        (parent_fit if e["partition"]=="FIT" else old_select).update(e["documents"])
    if len(parent_fit)!=320 or len(old_select)!=80 or parent_fit&old_select: raise RuntimeError("parent split mismatch")

    docs,empty,bad=parse_train(a.train)
    if bad or len(docs)!=400: raise RuntimeError(f"source parse mismatch {len(docs)} {bad[:2]}")
    rows=[doc_stats(docs,di) for di in sorted(parent_fit)]
    # No exact-token duplicate may cross anything.
    bytok=collections.defaultdict(list)
    for r in rows: bytok[r["token_sha256"]].append(r["document"])
    dups={h:v for h,v in bytok.items() if len(v)>1}
    if dups: raise RuntimeError(f"parent FIT has duplicate token groups unexpectedly: {dups}")

    verify,design,target,verify_optimization=greedy_subset(rows,64,"VERIFY")
    if len(verify)!=64 or len(design)!=256: raise RuntimeError("DESIGN/VERIFY size")
    folds,sizes,fold_targets,fold_optimization=assign_folds(design,5)

    vstats=sum_stats(verify); dstats=sum_stats(design); pstats=sum_stats(rows)
    vdev=deviations(vstats,target)
    fold_rows=[]
    seen=set()
    for i,fr in enumerate(folds):
        fs=sum_stats(fr); fd=deviations(fs,fold_targets[i])
        if any(r["document"] in seen for r in fr): raise RuntimeError("fold duplicate")
        seen.update(r["document"] for r in fr)
        fold_rows.append({"fold":i,"documents":[r["document"] for r in sorted(fr,key=lambda x:x["document"])],
                          "stats":fs,"deviation_from_target":fd})
    if seen!={r["document"] for r in design}: raise RuntimeError("fold coverage mismatch")

    # Preflight tolerances, conservative for small C.
    if abs(vdev["documents"])>1e-9: raise RuntimeError("verify doc target")
    for c in CLASSES:
        if abs(vdev["gold_"+c])>.15: raise RuntimeError(f"verify {c} imbalance {vdev['gold_'+c]}")
    for fr in fold_rows:
        if fr["stats"]["gold_counts"]["C"]<15: raise RuntimeError(f"fold {fr['fold']} C support too low")
        if max(abs(fr["deviation_from_target"]["gold_"+c]) for c in CLASSES)>.25:
            raise RuntimeError(f"fold class imbalance {fr['fold']}")

    unknown=pstats["section_counts"]["UNKNOWN"]; total_examples=pstats["sentences"]
    section_ok=(unknown/max(1,total_examples))<=.01
    cont=collections.Counter()
    invalid=[]
    for r in rows:
        for x in r["continuation_fragments"]:
            if x.get("invalid"): invalid.append({"document":r["document"],**x})
            else: cont[x["class"]]+=1
    if invalid: raise RuntimeError(f"invalid initial-I in parent FIT: {invalid[:3]}")

    manifest_core={
      "version":"R44_OOF_MANIFEST_V1","seed":SEED,
      "source_train_sha256":TRAIN_SHA,"parent_r43_manifest_sha256":R43_SPLIT_SHA,
      "semantic_contract":"SOURCE_COMPATIBLE_B_START + DOCUMENT_CONTINUITY_METADATA",
      "parent_fit_documents":sorted(parent_fit),"excluded_old_select_documents":sorted(old_select),
      "design_documents":sorted(r["document"] for r in design),
      "verify_internal_documents":sorted(r["document"] for r in verify),
      "oof_folds":fold_rows
    }
    manifest_sha=sha_text(json.dumps(manifest_core,sort_keys=True,separators=(",",":")))
    manifest={**manifest_core,"manifest_sha256":manifest_sha}
    (a.out/"R44_OOF_MANIFEST_V1.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")

    summary={
      "state":"R44_READ_ONLY_PREFLIGHT_PASS",
      "manifest_sha256":manifest_sha,
      "parent_fit_stats":pstats,"design_stats":dstats,"verify_internal_stats":vstats,
      "verify_deviation_from_target":vdev,
      "verify_pair_swap_optimization":verify_optimization,
      "oof_fold_stats":fold_rows,
      "oof_fold_pair_swap_optimization":fold_optimization,
      "section_feature_enabled":section_ok,
      "section_unknown_rate":unknown/max(1,total_examples),
      "continuation_fragments_parent_fit":{c:int(cont[c]) for c in CLASSES},
      "empty_surface_rows_removed_global":empty,
      "duplicate_token_groups_parent_fit":len(dups),
      "guards":{"old_SELECT_excluded":True,"historical_DEV":False,"TEST":False,"other_folds":False,
                "FactPICO":False,"consumed_60_RCT":False,"training":False},
      "next_action":"ADVERSARIAL_REVIEW_R44_PROTOCOL_AND_PREFLIGHT_BEFORE_ANY_TRAINING"
    }
    (a.out/"R44_PREFLIGHT_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__": main()
