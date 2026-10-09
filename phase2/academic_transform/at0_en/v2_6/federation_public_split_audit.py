#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, unicodedata
from pathlib import Path
from itertools import combinations

CORPORA=("AD","COVID-19")
FOLDS=range(1,6)
ROLES=("train","dev","test")

def h(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def parse_docs(path:Path):
    docs=[]
    cur=[]
    started=False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.rstrip("\n")
        if line.startswith("-DOCSTART-"):
            if started:
                docs.append(tuple(cur))
            cur=[]
            started=True
            continue
        if not started:
            continue
        if not line.strip():
            continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"):
            continue
        cols=line.split("\t")
        token=cols[0] if cols else ""
        # Text-only fingerprint: ignore all annotation columns.
        cur.append(token)
    if started:
        docs.append(tuple(cur))
    if any(len(d)==0 for d in docs):
        raise ValueError(f"empty document in {path}")
    return docs

def norm_doc(tokens):
    s=" ".join(tokens)
    s=unicodedata.normalize("NFC",s)
    s=" ".join(s.split())
    return s

def fingerprints(path):
    docs=parse_docs(path)
    fps=[h(norm_doc(d)) for d in docs]
    return docs,fps

def digest_set(xs):
    return h("\n".join(sorted(set(xs)))+"\n")

def overlap(a,b):
    return len(set(a)&set(b))

def audit(source:Path):
    file_stats={}
    fp={}
    for corpus in CORPORA:
        fp[corpus]={}
        for fold in FOLDS:
            fp[corpus][fold]={}
            for role in ROLES:
                path=source/f"data/{corpus}/fold{fold}/{role}.txt"
                docs,fps=fingerprints(path)
                fp[corpus][fold][role]=fps
                file_stats[f"{corpus}/fold{fold}/{role}"]={
                    "document_count":len(fps),
                    "unique_document_count":len(set(fps)),
                    "duplicate_document_count":len(fps)-len(set(fps)),
                    "membership_digest_sha256":digest_set(fps),
                    "file_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                }

    fold_role_overlap={}
    for corpus in CORPORA:
        for fold in FOLDS:
            key=f"{corpus}/fold{fold}"
            fold_role_overlap[key]={
                "train_dev":overlap(fp[corpus][fold]["train"],fp[corpus][fold]["dev"]),
                "train_test":overlap(fp[corpus][fold]["train"],fp[corpus][fold]["test"]),
                "dev_test":overlap(fp[corpus][fold]["dev"],fp[corpus][fold]["test"]),
            }

    test_overlap={}
    for corpus in CORPORA:
        mat={}
        for i in FOLDS:
            mat[str(i)]={}
            for j in FOLDS:
                mat[str(i)][str(j)]=overlap(fp[corpus][i]["test"],fp[corpus][j]["test"])
        union=set()
        total=0
        for i in FOLDS:
            union |= set(fp[corpus][i]["test"])
            total += len(fp[corpus][i]["test"])
        test_overlap[corpus]={
            "pairwise_overlap_matrix":mat,
            "sum_test_documents_across_folds":total,
            "unique_test_documents_across_folds":len(union),
            "test_union_digest_sha256":digest_set(union),
        }

    whole={}
    for corpus in CORPORA:
        union=set()
        for fold in FOLDS:
            for role in ROLES:
                union |= set(fp[corpus][fold][role])
        whole[corpus]={
            "unique_documents_across_all_files":len(union),
            "whole_membership_digest_sha256":digest_set(union)
        }

    cross_ad_covid=0
    ad=set(); cv=set()
    for fold in FOLDS:
        for role in ROLES:
            ad |= set(fp["AD"][fold][role]); cv |= set(fp["COVID-19"][fold][role])
    cross_ad_covid=len(ad&cv)

    # Compare benchmark corpora to the known exposed EBM-NLP_mod fold1 TRAIN text universe.
    ebm_path=source/"data/EBM-NLPmod/fold1/train.txt"
    _,ebm=fingerprints(ebm_path)
    ebmset=set(ebm)
    exposure_overlap={}
    for corpus in CORPORA:
        all_test=set()
        all_all=set()
        for fold in FOLDS:
            all_test |= set(fp[corpus][fold]["test"])
            for role in ROLES:
                all_all |= set(fp[corpus][fold][role])
        exposure_overlap[corpus]={
            "unique_test_text_overlap_with_ebm_mod_fold1_train":len(all_test & ebmset),
            "whole_corpus_text_overlap_with_ebm_mod_fold1_train":len(all_all & ebmset),
        }

    # Labels are never returned; only source files are parsed internally to identify text columns.
    return {
        "state":"FEDERATION_PUBLIC_SPLIT_TEXT_FINGERPRINT_AUDIT_PASS",
        "source_commit_expected":"bc4b878773192f38b2600ec830ca4208b82f7dc0",
        "output_contains_raw_text":False,
        "output_contains_gold_labels":False,
        "fingerprint_basis":"NFC whitespace-collapsed first-column source tokens; annotation columns ignored",
        "file_stats":file_stats,
        "within_fold_role_overlap":fold_role_overlap,
        "cross_fold_test_overlap":test_overlap,
        "whole_corpus":whole,
        "ad_covid_text_overlap":cross_ad_covid,
        "overlap_with_known_exposed_ebm_mod_fold1_train":exposure_overlap,
        "limitations":[
            "Text equality is not trial-family identity.",
            "No PMID/DOI/registry identifiers are recovered by this audit.",
            "Zero text-hash overlap does not certify benchmark independence.",
            "Protected VERIFY_INTERNAL membership is not opened or identified here."
        ]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    d=audit(a.source)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
