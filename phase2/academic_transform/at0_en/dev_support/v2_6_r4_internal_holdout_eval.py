#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import urllib.request

HERE=pathlib.Path(__file__).resolve().parent
AT0=HERE.parent
V26=AT0/"v2_6"
MANIFEST_PATH=V26/"AT0_EN_V26_R4_INTERNAL_HOLDOUT_MANIFEST_V1.json"
FACTPICO_HASH_PATH=V26/"FACTPICO_V25_SOURCE_CLUSTER_HASHES_FOR_R4_OVERLAP_V1.json"

def git_blob_sha(raw:bytes)->str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()

def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

manifest=json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
factpico=json.loads(FACTPICO_HASH_PATH.read_text(encoding="utf-8"))

if manifest["manifest_id"]!="AT0_EN_V26_R4_INTERNAL_HOLDOUT_V1":
    raise RuntimeError("Unexpected holdout manifest ID")
if manifest["document_count"]!=60 or len(manifest["documents"])!=60:
    raise RuntimeError("Holdout document count mismatch")
if factpico["source_cluster_count"]!=115 or len(factpico["source_cluster_sha256"])!=115:
    raise RuntimeError("FactPICO source-hash reference count mismatch")

source_commit=manifest["source_commit"]
base=f"https://raw.githubusercontent.com/sociocom/PICO-Corpus/{source_commit}/pico_corpus_brat_annotated_files"
factpico_hashes=set(factpico["source_cluster_sha256"])

# PRE-EXTRACTION OPEN BOUNDARY:
# fetch immutable bytes, verify Git blob identity, hash only, and stop before extractor on overlap.
frozen=[]
overlaps=[]
for d in manifest["documents"]:
    pmid=d["pmid"]
    with urllib.request.urlopen(f"{base}/{pmid}.txt",timeout=30) as resp:
        raw=resp.read()
    blob=git_blob_sha(raw)
    if blob!=d["git_blob_sha1"]:
        raise RuntimeError(f"Git blob mismatch for PMID {pmid}: {blob}")
    raw_sha=hashlib.sha256(raw).hexdigest()
    if raw_sha in factpico_hashes:
        overlaps.append({"pmid":pmid,"raw_sha256":raw_sha})
    frozen.append((pmid,raw,blob,raw_sha))

if overlaps:
    result={
        "evaluation_id":"AT0_EN_V26_R4_INTERNAL_HOLDOUT_V1",
        "state":"BLOCKED_BEFORE_EXTRACTION_FACTPICO_OVERLAP",
        "holdout_document_count":60,
        "factpico_source_hash_count":115,
        "overlap_count":len(overlaps),
        "overlaps":overlaps,
        "extractor_invoked":False,
        "holdout_consumed":False,
    }
    print(json.dumps(result,sort_keys=True,indent=2))
    raise SystemExit(3)

# Only after overlap=0 is text decoded and passed to the frozen extractor.
ra=loadmod("v26_holdout_ra",V26/"gate_b2"/"relation_aware_extractor.py")

docs=[]
total_assertions=0
total_noncertain=0
total_unresolved=0
total_short=0
empty=0
over_envelope=0
docs_noncertain_le_50=0

for pmid,raw,blob,raw_sha in frozen:
    text=raw.decode("utf-8")
    g=ra.relation_aware_extract(text,f"R4-HOLDOUT-{pmid}")
    assertions=g["assertions"]
    noncertain=sum(a["confidence_status"]!="CERTAIN" for a in assertions)
    unresolved=sum(a["predicate"]=="UNRESOLVED" for a in assertions)
    short=sum(len(a["evidence"].strip())<=3 for a in assertions)
    rate=noncertain/len(assertions) if assertions else 1.0
    docs_noncertain_le_50+=int(rate<=0.50)
    empty+=int(not assertions)
    over_envelope+=int(len(assertions)>128)
    total_assertions+=len(assertions)
    total_noncertain+=noncertain
    total_unresolved+=unresolved
    total_short+=short
    # No text/evidence is emitted: only immutable identity and numeric diagnostics.
    docs.append({
        "pmid":pmid,
        "git_blob_sha1":blob,
        "raw_sha256":raw_sha,
        "assertion_count":len(assertions),
        "noncertain_count":noncertain,
        "noncertain_rate":rate,
        "unresolved_count":unresolved,
        "short_evidence_le3":short,
        "over_128":len(assertions)>128,
    })

noncertain_rate=total_noncertain/total_assertions if total_assertions else 1.0
unresolved_rate=total_unresolved/total_assertions if total_assertions else 1.0
docs_le50_rate=docs_noncertain_le_50/60

criteria={
    "short_evidence_zero": total_short==0,
    "empty_documents_zero": empty==0,
    "over_128_documents_zero": over_envelope==0,
    "unresolved_rate_le_0_40": unresolved_rate<=0.40,
    "noncertain_rate_le_0_45": noncertain_rate<=0.45,
    "docs_noncertain_le_50_rate_ge_0_80": docs_le50_rate>=0.80,
}

result={
    "evaluation_id":"AT0_EN_V26_R4_INTERNAL_HOLDOUT_V1",
    "state":"HOLDOUT_CONSUMED_AND_EVALUATED",
    "holdout_consumed":True,
    "extractor_invoked":True,
    "source_repo":"sociocom/PICO-Corpus",
    "source_commit":source_commit,
    "holdout_document_count":60,
    "factpico_source_hash_count":115,
    "factpico_overlap_count":0,
    "frozen_thresholds":{
        "unresolved_rate_max":0.40,
        "noncertain_rate_max":0.45,
        "docs_noncertain_le_50_rate_min":0.80,
        "short_evidence_le3":0,
        "empty_documents":0,
        "over_128_documents":0,
    },
    "aggregate":{
        "total_assertions":total_assertions,
        "noncertain_assertions":total_noncertain,
        "noncertain_rate":noncertain_rate,
        "unresolved_predicates":total_unresolved,
        "unresolved_rate":unresolved_rate,
        "short_evidence_le3":total_short,
        "empty_representation_documents":empty,
        "over_128_assertion_documents":over_envelope,
        "documents_noncertain_le_50pct":docs_noncertain_le_50,
        "documents_noncertain_le_50pct_rate":docs_le50_rate,
    },
    "criteria":criteria,
    "overall_pass":all(criteria.values()),
    "per_document_numeric_diagnostics":docs,
}
canonical=json.dumps(result,sort_keys=True,separators=(",",":"))
result["canonical_result_sha256"]=hashlib.sha256(canonical.encode()).hexdigest()
print(json.dumps(result,sort_keys=True,indent=2))
if not result["overall_pass"]:
    raise SystemExit(2)
