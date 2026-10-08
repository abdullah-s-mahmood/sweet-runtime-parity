#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

FROZEN_QUERY = r'''(
  "randomized controlled trial"[Publication Type]
  OR "controlled clinical trial"[Publication Type]
  OR randomized[Title/Abstract]
  OR randomised[Title/Abstract]
  OR randomly[Title/Abstract]
  OR placebo[Title/Abstract]
)
AND ("2026/01/01"[Date - Publication] : "2026/09/30"[Date - Publication])
AND english[Language]
AND hasabstract
NOT (animals[MeSH Terms] NOT humans[MeSH Terms])'''

TITLE_LEVENSHTEIN_TRIGGER = 0.90
ABSTRACT_5GRAM_JACCARD_TRIGGER = 0.80
ABSTRACT_5GRAM_CONTAINMENT_TRIGGER = 0.90

REGISTRY_PATTERNS = {
    "NCT": re.compile(r"\bNCT\s*[-:]?\s*(\d{8})\b", re.I),
    "ISRCTN": re.compile(r"\bISRCTN\s*[-:]?\s*(\d{8})\b", re.I),
    "ACTRN": re.compile(r"\bACTRN\s*[-:]?\s*(\d{14})\b", re.I),
    "CHICTR": re.compile(r"\bChiCTR\s*[-:]?\s*([A-Za-z0-9-]+)\b", re.I),
    "CTRI": re.compile(r"\bCTRI\s*[/:-]?\s*([0-9A-Za-z/-]+)\b", re.I),
    "IRCT": re.compile(r"\bIRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b", re.I),
    "UMIN": re.compile(r"\bUMIN\s*[-:]?\s*([A-Za-z0-9-]+)\b", re.I),
    "JRCT": re.compile(r"\bjRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b", re.I),
    "DRKS": re.compile(r"\bDRKS\s*[-:]?\s*(\d{8})\b", re.I),
    "EUCTR": re.compile(r"\b(?:EudraCT|EU\s*CTR)\s*[-:]?\s*([0-9-]+)\b", re.I),
}

def sha256_bytes(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()

def sha256_text(s:str)->str:
    return sha256_bytes(s.encode("utf-8"))

def normalize_match_text(s:str)->str:
    s=unicodedata.normalize("NFKC",s).casefold()
    return " ".join(s.split())

def lexical_tokens(s:str)->list[str]:
    s=normalize_match_text(s)
    return re.findall(r"[^\W_]+",s,flags=re.UNICODE)

def ngrams(tokens:list[str],n:int=5)->set[tuple[str,...]]:
    if len(tokens)<n:
        return set()
    return {tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)}

def levenshtein_distance(a:str,b:str)->int:
    if a==b: return 0
    if len(a)<len(b): a,b=b,a
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(cur[-1]+1, prev[j]+1, prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]

def levenshtein_similarity(a:str,b:str)->float:
    a=normalize_match_text(a); b=normalize_match_text(b)
    if not a and not b: return 1.0
    m=max(len(a),len(b))
    if m==0: return 1.0
    return 1.0-levenshtein_distance(a,b)/m

def fivegram_metrics(a:str,b:str)->tuple[float,float]:
    A=ngrams(lexical_tokens(a)); B=ngrams(lexical_tokens(b))
    if not A or not B:
        return 0.0,0.0
    inter=len(A&B)
    jac=inter/len(A|B)
    cont=max(inter/len(A),inter/len(B))
    return jac,cont

def normalize_doi(x:str|None)->str|None:
    if not x: return None
    s=normalize_match_text(x)
    s=re.sub(r"^(https?://(?:dx\.)?doi\.org/|doi:\s*)","",s)
    return s.strip(" .") or None

def normalize_pmid(x:str|int|None)->str|None:
    if x is None:return None
    s=str(x).strip()
    return s if s.isdigit() else None

def extract_registry_ids(text:str)->set[str]:
    out=set()
    for prefix,pat in REGISTRY_PATTERNS.items():
        for m in pat.finditer(text or ""):
            value=re.sub(r"[\s:]","",m.group(1)).upper()
            out.add(prefix+":"+value)
    return out

def screening_triggers(a:dict,b:dict)->dict:
    triggers=[]
    ap=normalize_pmid(a.get("pmid")); bp=normalize_pmid(b.get("pmid"))
    if ap and bp and ap==bp: triggers.append("EXACT_PMID")
    ad=normalize_doi(a.get("doi")); bd=normalize_doi(b.get("doi"))
    if ad and bd and ad==bd: triggers.append("EXACT_DOI")

    at=normalize_match_text(a.get("title","")); bt=normalize_match_text(b.get("title",""))
    if at and bt and at==bt: triggers.append("EXACT_NORMALIZED_TITLE")
    title_sim=levenshtein_similarity(at,bt) if at or bt else 0.0
    if min(len(lexical_tokens(at)),len(lexical_tokens(bt)))>=5 and title_sim>=TITLE_LEVENSHTEIN_TRIGGER:
        triggers.append("NEAR_TITLE_LEVENSHTEIN")

    aa=a.get("abstract",""); ba=b.get("abstract","")
    aj,ac=fivegram_metrics(aa,ba)
    if aj>=ABSTRACT_5GRAM_JACCARD_TRIGGER: triggers.append("ABSTRACT_5GRAM_JACCARD")
    if ac>=ABSTRACT_5GRAM_CONTAINMENT_TRIGGER: triggers.append("ABSTRACT_5GRAM_CONTAINMENT")

    ra=extract_registry_ids(" ".join([a.get("title",""),aa,a.get("registry_text","")]))
    rb=extract_registry_ids(" ".join([b.get("title",""),ba,b.get("registry_text","")]))
    shared=sorted(ra&rb)
    if shared: triggers.append("SHARED_REGISTRY_ID")

    return {
        "triggers":sorted(set(triggers)),
        "requires_documentary_review":bool(triggers),
        "title_levenshtein_similarity":title_sim,
        "abstract_5gram_jaccard":aj,
        "abstract_5gram_containment":ac,
        "shared_registry_ids":shared,
        "a_registry_ids":sorted(ra),
        "b_registry_ids":sorted(rb),
    }

def validate_retrieval_snapshot(snapshot:dict)->dict:
    if snapshot.get("query") != FROZEN_QUERY:
        raise ValueError("query differs from frozen literal query")
    parent_count=int(snapshot["parent_count"])
    pages=snapshot.get("pages",[])
    if parent_count<0: raise ValueError("negative parent count")
    if not pages and parent_count:
        raise ValueError("nonzero parent count with no pages")
    seen_page_ids=set()
    pmids=[]
    raw_hashes=[]
    for i,p in enumerate(pages):
        idx=int(p["page_index"])
        if idx in seen_page_ids: raise ValueError("duplicate page_index")
        seen_page_ids.add(idx)
        ids=[str(x) for x in p["pmids"]]
        if any(not x.isdigit() for x in ids): raise ValueError("invalid PMID")
        pmids.extend(ids)
        raw=str(p["raw_response"])
        raw_hashes.append(sha256_text(raw))
    unique=sorted(set(pmids),key=lambda x:int(x))
    duplicates=len(pmids)-len(unique)
    if duplicates:
        raise ValueError(f"duplicate PMIDs across pages: {duplicates}")
    if len(unique)!=parent_count:
        raise ValueError(f"retrieval incomplete: unique={len(unique)} parent_count={parent_count}")
    expected_pages=list(range(len(pages)))
    if sorted(seen_page_ids)!=expected_pages:
        raise ValueError("page indices not contiguous from zero")
    return {
        "state":"RETRIEVAL_SNAPSHOT_STRUCTURAL_PASS",
        "query_sha256":sha256_text(FROZEN_QUERY),
        "parent_count":parent_count,
        "unique_pmids":len(unique),
        "first_pmid":unique[0] if unique else None,
        "last_pmid":unique[-1] if unique else None,
        "raw_response_sha256":raw_hashes,
        "pmid_list_sha256":sha256_text("\n".join(unique)+"\n"),
    }

def validate_partitioned_retrieval(parent_count:int, partitions:list[dict])->dict:
    all_pmids=[]
    labels=[]
    for p in partitions:
        label=str(p["label"])
        if label in labels: raise ValueError("duplicate partition label")
        labels.append(label)
        ids=[str(x) for x in p["pmids"]]
        if any(not x.isdigit() for x in ids): raise ValueError("invalid partition PMID")
        if len(ids)!=len(set(ids)): raise ValueError(f"duplicate inside partition {label}")
        all_pmids.extend(ids)
    union=set(all_pmids)
    cross_duplicates=len(all_pmids)-len(union)
    if cross_duplicates:
        raise ValueError("partition overlap detected")
    if len(union)!=int(parent_count):
        raise ValueError("partition union does not reconcile to parent count")
    return {
        "state":"PARTITION_RECONCILIATION_PASS",
        "parent_count":int(parent_count),
        "partition_count":len(partitions),
        "union_count":len(union),
        "partition_labels":labels,
    }

def synthetic_preflight()->dict:
    # Frozen-query full retrieval happy path.
    snap={
        "query":FROZEN_QUERY,
        "parent_count":6,
        "pages":[
            {"page_index":0,"pmids":["101","102","103"],"raw_response":"page0"},
            {"page_index":1,"pmids":["104","105","106"],"raw_response":"page1"},
        ]
    }
    retrieval=validate_retrieval_snapshot(snap)

    # Must fail on incomplete retrieval.
    bad=json.loads(json.dumps(snap)); bad["pages"][1]["pmids"]=["104","105"]
    try:
        validate_retrieval_snapshot(bad)
        raise RuntimeError("incomplete retrieval did not fail")
    except ValueError:
        pass

    # Must fail on query mutation.
    badq=json.loads(json.dumps(snap)); badq["query"]=FROZEN_QUERY+" "
    try:
        validate_retrieval_snapshot(badq)
        raise RuntimeError("query mutation did not fail")
    except ValueError:
        pass

    partition=validate_partitioned_retrieval(6,[
        {"label":"2026-01","pmids":["101","102"]},
        {"label":"2026-02","pmids":["103","104"]},
        {"label":"2026-03","pmids":["105","106"]},
    ])
    try:
        validate_partitioned_retrieval(6,[
            {"label":"A","pmids":["101","102","103"]},
            {"label":"B","pmids":["103","104","105"]},
        ])
        raise RuntimeError("overlapping partitions did not fail")
    except ValueError:
        pass

    exact_a={
        "pmid":"12345678","doi":"10.1000/XYZ.1",
        "title":"Randomized trial of treatment A versus placebo in adults",
        "abstract":"Adults were randomized to treatment A or placebo for twelve weeks and blood pressure was measured.",
        "registry_text":"NCT01234567"
    }
    exact_b={
        "pmid":"12345678","doi":"https://doi.org/10.1000/xyz.1",
        "title":"Randomized trial of treatment A versus placebo in adults",
        "abstract":"Adults were randomized to treatment A or placebo for twelve weeks and blood pressure was measured.",
        "registry_text":"NCT-01234567"
    }
    exact=screening_triggers(exact_a,exact_b)
    required={"EXACT_PMID","EXACT_DOI","EXACT_NORMALIZED_TITLE","NEAR_TITLE_LEVENSHTEIN","ABSTRACT_5GRAM_JACCARD","ABSTRACT_5GRAM_CONTAINMENT","SHARED_REGISTRY_ID"}
    if not required.issubset(set(exact["triggers"])):
        raise RuntimeError(f"missing exact/near triggers {required-set(exact['triggers'])}")

    near_a={
        "title":"A randomized controlled trial of exercise rehabilitation after cardiac surgery",
        "abstract":"Participants after cardiac surgery received supervised exercise rehabilitation three times weekly for twelve weeks with functional capacity assessment.",
        "registry_text":"ISRCTN 12345678"
    }
    near_b={
        "title":"Randomized controlled trial of exercise rehabilitation following cardiac surgery",
        "abstract":"Participants after cardiac surgery received supervised exercise rehabilitation three times weekly for twelve weeks with functional capacity assessment and safety monitoring.",
        "registry_text":"ISRCTN:12345678"
    }
    near=screening_triggers(near_a,near_b)
    if not near["requires_documentary_review"] or "SHARED_REGISTRY_ID" not in near["triggers"]:
        raise RuntimeError("near/trial-family fixture not triggered")

    unrelated_a={
        "pmid":"1","doi":"10.1/a",
        "title":"Vitamin supplementation in pregnancy",
        "abstract":"Pregnant adults received vitamin supplementation and neonatal weight was recorded.",
        "registry_text":"NCT00000001"
    }
    unrelated_b={
        "pmid":"2","doi":"10.1/b",
        "title":"Robotic gait training after stroke",
        "abstract":"Stroke survivors received robotic gait training and walking speed was assessed.",
        "registry_text":"NCT00000002"
    }
    unrelated=screening_triggers(unrelated_a,unrelated_b)
    if unrelated["requires_documentary_review"]:
        raise RuntimeError(f"unrelated fixture triggered: {unrelated['triggers']}")

    if extract_registry_ids("NCT-01234567 ISRCTN:12345678 DRKS 87654321") != {
        "NCT:01234567","ISRCTN:12345678","DRKS:87654321"
    }:
        raise RuntimeError("registry normalization fixture failed")

    return {
        "state":"FRESH_RCT_ACQUISITION_TOOLING_SYNTHETIC_PREFLIGHT_PASS",
        "new_rct_data_used":False,
        "pubmed_contacted":False,
        "protected_data_opened":False,
        "retrieval_snapshot":retrieval,
        "partition_reconciliation":partition,
        "duplicate_trigger_fixture":exact,
        "near_trial_family_fixture":near,
        "unrelated_fixture":unrelated,
        "thresholds":{
            "title_levenshtein":TITLE_LEVENSHTEIN_TRIGGER,
            "abstract_5gram_jaccard":ABSTRACT_5GRAM_JACCARD_TRIGGER,
            "abstract_5gram_containment":ABSTRACT_5GRAM_CONTAINMENT_TRIGGER,
        },
        "warning":"Triggers require documentary human review; absence of a trigger does not prove independence."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight:
        raise SystemExit("Only --synthetic-preflight is authorized before acquisition readiness closure")
    report=synthetic_preflight()
    s=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(s,encoding="utf-8")
    print(s,end="")

if __name__=="__main__":
    main()
