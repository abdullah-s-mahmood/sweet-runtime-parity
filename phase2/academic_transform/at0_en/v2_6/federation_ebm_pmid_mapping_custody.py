#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib, re, tarfile, unicodedata

def lexicalize_tokens(tokens):
    s=" ".join(tokens)
    s=unicodedata.normalize("NFKC",s).casefold()
    return re.findall(r"[a-z0-9]+",s)

def parse_mod_docs(path:pathlib.Path):
    docs=[]; cur=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started: docs.append(cur)
            cur=[]; started=True; continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        cur.append(line.split("\t")[0])
    if started: docs.append(cur)
    return docs

def find_original_tokens(root:pathlib.Path):
    files=list(root.rglob("*.tokens"))
    out={}
    for p in files:
        stem=p.stem
        if not stem.isdigit(): continue
        toks=p.read_text(encoding="utf-8",errors="replace").split()
        lex=lexicalize_tokens(toks)
        if len(lex)>=7:
            out[stem]=lex
    return out

def ngrams(seq,n=7):
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

def map_docs(mod_docs, originals, n=7):
    inv=collections.defaultdict(set)
    for pmid,toks in originals.items():
        # set prevents repeated ngram within one original from inflating votes.
        for g in set(ngrams(toks,n)):
            inv[g].add(pmid)

    rows=[]
    for di,doc in enumerate(mod_docs):
        lex=lexicalize_tokens(doc)
        grams=set(ngrams(lex,n))
        counts=collections.Counter()
        for g in grams:
            for pmid in inv.get(g,()):
                counts[pmid]+=1
        ranked=counts.most_common()
        best=ranked[0][1] if ranked else 0
        second=ranked[1][1] if len(ranked)>1 else 0
        best_ids=[p for p,v in ranked if v==best] if best else []
        coverage=best/max(1,len(grams))
        # Conservative provenance mapping rule:
        # substantial exact 7-gram evidence + margin + unique best.
        accepted=(len(best_ids)==1 and best>=12 and (best-second)>=6 and coverage>=0.12)
        rows.append({
            "document_index":di,
            "accepted":accepted,
            "pmid":best_ids[0] if accepted else None,
            "best_shared_7grams":best,
            "second_shared_7grams":second,
            "coverage":coverage,
            "unique_best":len(best_ids)==1,
            "mod_7gram_count":len(grams)
        })
    return rows

def hist(vals,bins):
    out={}
    for lo,hi in bins:
        out[f"[{lo},{hi})"]=sum(lo<=x<hi for x in vals)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mod-train",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--ebm-archive",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm_archive,"r:gz") as tf:
        tf.extractall(a.work,filter="data")
    originals=find_original_tokens(a.work)
    mod_docs=parse_mod_docs(a.mod_train)
    if len(mod_docs)!=400: raise RuntimeError(f"expected 400 mod docs, got {len(mod_docs)}")
    if len(originals)<4000: raise RuntimeError(f"too few original EBM documents: {len(originals)}")
    rows=map_docs(mod_docs,originals)
    m=json.loads(a.r44_manifest.read_text())
    groups={
      "DESIGN":set(m["design_documents"]),
      "VERIFY_INTERNAL":set(m["verify_internal_documents"]),
      "OLD_SELECT":set(m["excluded_old_select_documents"]),
      "ALL_FOLD1_TRAIN":set(range(400))
    }
    stats={}
    for name,inds in groups.items():
        rr=[rows[i] for i in sorted(inds)]
        accepted=[x for x in rr if x["accepted"]]
        pmids=[x["pmid"] for x in accepted]
        stats[name]={
          "documents":len(rr),
          "accepted_unique_pmid_mappings":len(set(pmids)),
          "accepted_documents":len(accepted),
          "ambiguous_or_unmatched_documents":len(rr)-len(accepted),
          "accepted_fraction":len(accepted)/len(rr) if rr else 0.0,
          "duplicate_accepted_pmid_assignments":len(pmids)-len(set(pmids)),
          "best_shared_7gram_histogram":hist([x["best_shared_7grams"] for x in rr],[(0,1),(1,6),(6,12),(12,25),(25,50),(50,100),(100,10**9)]),
          "coverage_histogram":hist([x["coverage"] for x in rr],[(0,.05),(.05,.12),(.12,.25),(.25,.5),(.5,.75),(.75,1.01)])
        }
    # Never emit PMID values.
    accepted_all=[x for x in rows if x["accepted"]]
    duplicate_assignments=len(accepted_all)-len({x["pmid"] for x in accepted_all})
    out={
      "state":"FEDERATION_EBM_MOD_TO_ORIGINAL_PMID_MAPPING_FEASIBILITY_PASS",
      "original_ebm_documents_found":len(originals),
      "mod_documents":len(mod_docs),
      "mapping_rule":{
        "ngram_n":7,
        "min_best_shared_ngrams":12,
        "min_best_minus_second":6,
        "min_coverage":0.12,
        "unique_best_required":True
      },
      "groups":stats,
      "all_400":{
        "accepted_documents":len(accepted_all),
        "accepted_fraction":len(accepted_all)/400,
        "duplicate_accepted_pmid_assignments":duplicate_assignments
      },
      "output_contains_pmids":False,
      "output_contains_protected_text":False,
      "output_contains_gold_labels":False,
      "limitations":[
        "Accepted mappings are provenance links based on exact lexical 7-gram evidence, not semantic model predictions.",
        "Unmatched/ambiguous records remain unresolved and must not be assumed independent.",
        "This audit does not itself map AD/COVID to PMID."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
