#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, re, hashlib, unicodedata

PATTERNS=[
 ("NCT", re.compile(r"\bNCT\s*[-:]?\s*(\d{8})\b",re.I)),
 ("ISRCTN", re.compile(r"\bISRCTN\s*[-:]?\s*(\d{8})\b",re.I)),
 ("ACTRN", re.compile(r"\bACTRN\s*[-:]?\s*(\d{14})\b",re.I)),
 ("CHICTR", re.compile(r"\bChiCTR\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("CTRI", re.compile(r"\bCTRI\s*[/:-]?\s*([0-9A-Za-z/-]+)\b",re.I)),
 ("IRCT", re.compile(r"\bIRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("UMIN", re.compile(r"\bUMIN\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("JRCT", re.compile(r"\bjRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("DRKS", re.compile(r"\bDRKS\s*[-:]?\s*(\d{8})\b",re.I)),
 ("EUCTR", re.compile(r"\b(?:EudraCT|EU\s*CTR)\s*[-:]?\s*([0-9-]+)\b",re.I)),
]

def parse_docs(path:pathlib.Path):
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

def canonical_text(tokens):
    s=" ".join(tokens)
    s=unicodedata.normalize("NFC",s)
    return " ".join(s.split())

def ids(tokens):
    s=canonical_text(tokens)
    out=set()
    for prefix,pat in PATTERNS:
        for m in pat.finditer(s):
            v=re.sub(r"[\s:]","",m.group(1)).upper()
            out.add(prefix+":"+v)
    return out

def digest(items):
    return hashlib.sha256(("\n".join(sorted(items))+"\n").encode()).hexdigest()

def corpus_registry(path):
    docs=parse_docs(path)
    arr=[ids(d) for d in docs]
    union=set().union(*arr) if arr else set()
    return arr,union

def overlap_stats(source_sets,target_sets):
    src_union=set().union(*source_sets) if source_sets else set()
    tgt_union=set().union(*target_sets) if target_sets else set()
    shared=src_union&tgt_union
    src_docs_with=sum(bool(x) for x in source_sets)
    tgt_docs_with=sum(bool(x) for x in target_sets)
    src_docs_shared=sum(bool(x&shared) for x in source_sets)
    tgt_docs_shared=sum(bool(x&shared) for x in target_sets)
    return {
      "source_docs":len(source_sets),
      "target_docs":len(target_sets),
      "source_docs_with_registry_id":src_docs_with,
      "target_docs_with_registry_id":tgt_docs_with,
      "source_unique_registry_ids":len(src_union),
      "target_unique_registry_ids":len(tgt_union),
      "shared_registry_id_count":len(shared),
      "source_docs_touching_shared_id":src_docs_shared,
      "target_docs_touching_shared_id":tgt_docs_shared,
      "shared_id_digest_sha256":digest(shared) if shared else digest(set())
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--public-root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    train_docs=parse_docs(a.train)
    if len(train_docs)!=400: raise RuntimeError(f"expected 400 EBM-NLP_mod docs, got {len(train_docs)}")
    m=json.loads(a.r44_manifest.read_text())
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); old=set(m["excluded_old_select_documents"])
    if len(design)!=256 or len(verify)!=64 or len(old)!=80:
        raise RuntimeError("R44 partition sizes mismatch")
    if design&verify or design&old or verify&old:
        raise RuntimeError("R44 partitions overlap")

    reg=[ids(d) for d in train_docs]
    groups={
      "DESIGN":[reg[i] for i in sorted(design)],
      "VERIFY_INTERNAL":[reg[i] for i in sorted(verify)],
      "OLD_SELECT":[reg[i] for i in sorted(old)],
      "ALL_EBM_MOD_FOLD1_TRAIN":reg
    }

    targets={}
    for corpus in ["AD","COVID-19"]:
        whole_seen={}
        test_seen={}
        for fold in range(1,6):
            for role in ["train","dev","test"]:
                p=a.public_root/f"data/{corpus}/fold{fold}/{role}.txt"
                docs=parse_docs(p)
                for d in docs:
                    key=hashlib.sha256(canonical_text(d).encode()).hexdigest()
                    whole_seen.setdefault(key,ids(d))
                    if role=="test":
                        test_seen.setdefault(key,ids(d))
        targets[f"{corpus}_WHOLE"]=list(whole_seen.values())
        targets[f"{corpus}_TEST_UNION"]=list(test_seen.values())

    comparisons={}
    for gname,gsets in groups.items():
        comparisons[gname]={}
        for tname,tsets in targets.items():
            comparisons[gname][tname]=overlap_stats(gsets,tsets)

    # Cross-target registry overlap is also useful.
    target_cross=overlap_stats(targets["AD_WHOLE"],targets["COVID-19_WHOLE"])

    out={
      "state":"FEDERATION_PROTECTED_REGISTRY_CUSTODY_AUDIT_PASS",
      "output_contains_registry_ids":False,
      "output_contains_raw_text":False,
      "output_contains_gold_labels":False,
      "r44_manifest_sha256":m.get("manifest_sha256"),
      "comparisons":comparisons,
      "ad_covid_cross_registry":target_cross,
      "limitations":[
        "Registry IDs present in text cover only a subset of documents.",
        "Zero shared registry ID does not prove different trial families.",
        "PMID/DOI/title-family linkage is not closed by this audit.",
        "Protected VERIFY_INTERNAL identities are never emitted."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
