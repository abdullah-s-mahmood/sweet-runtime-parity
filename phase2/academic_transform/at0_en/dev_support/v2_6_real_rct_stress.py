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
SRC_COMMIT="482b7d8f135fe6ea424961c2812e8d214c3f4a5f"
BASE=f"https://raw.githubusercontent.com/sociocom/PICO-Corpus/{SRC_COMMIT}/pico_corpus_brat_annotated_files"

SOURCES=[
("10459028","bc806f2e353544a41c57707ce24fd2d6e6d89e5d"),
("10547391","91ee86e2c9135dd107309faffd38f055c462f991"),
("11136837","9b7f448553291474f5433c455c3c64eb60b1bcdd"),
("11283119","2d9ebe52246a70a445e553912c7235bd1e3f8591"),
("12374678","a9360d78bbf61f67aedbde4ebb9457c239ccc539"),
("12377957","7afad18df352dd6fc631bbb3e65060da8788b933"),
("12393819","320baf142eea870492d685503996ffe9306ab0be"),
("12425756","1be62e949a714df38fc92d4f96134fa8ccc5fb2c"),
("12439707","78e5a40d23cce22a06848b95576bf118571b47b1"),
("12540501","16638929745eecc03f4e1928ddff834941762395"),
("12598347","61d2f67806a1daa1b5e9968539a67553f15ebb31"),
("12609560","191598730dfa5a77b790f3649961fa932b024d1e"),
("12621740","42f408259650542bc832d9f9e328e165a1a8f006"),
("12637464","e2abbff6f10de7e35babea9878b13f220bac9485"),
("12697850","e20678dda99a1228dd1b783e090b8ef2976c6f5f"),
("12721239","d077dee508768736a418476c8d385dba03afb482"),
("12775735","9b4ee4b85adbcd50b3d6c3537148cc6920d96f0d"),
("12796608","3a89f396a030673ac37abfcbad275abfd0518c41"),
("12812657","7e204c5bfaf31f5b5e005eb0238df01d312b69c9"),
("12839848","4d41d0df5e5a82c1841925a2f4d4afaea15e9100"),
("12840087","ea5ecfcd8480837febeeac4905c57f4224cfaeb2"),
("12904519","b58767d1478d456629279f434a71d18db0070032"),
("12919237","cae99837d70a4bc9fcb0f7fe33f5f7c713631d65"),
("12926095","e38b2607b7c6a9e2f68b547fea0f0afd6c4c7d50"),
("12957243","38f589cde831f33f870e7ff36cc644a92980994e"),
("14525573","6bd095d2d0378a345591117d154905513fa87f80"),
("14556922","dbb1c9f71ec830439f0cd69939a2018faf246325"),
("14637388","69f3223c5b32ece47ee23c59425e246dac568311"),
("14722733","ecdc30b11e1f1e70e9663ad965faf3124411d648"),
("15014181","9d64392dafb893dc38ce3f6120f65394bec2cdea"),
]

def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ra=loadmod("v26_ra_stress",V26/"gate_b2"/"relation_aware_extractor.py")

def git_blob_sha(raw:bytes)->str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()

docs=[]
total_assertions=0
total_noncertain=0
total_unresolved=0
total_short=0
over_30=0
empty=0
over_envelope=0

for pmid,expected_blob in SOURCES:
    url=f"{BASE}/{pmid}.txt"
    with urllib.request.urlopen(url,timeout=30) as resp:
        raw=resp.read()
    actual_blob=git_blob_sha(raw)
    if actual_blob!=expected_blob:
        raise RuntimeError(f"source blob mismatch PMID={pmid}: {actual_blob}")
    text=raw.decode("utf-8")
    g=ra.relation_aware_extract(text,f"PICO-CORPUS-{pmid}")
    assertions=g["assertions"]
    certain=sum(a["confidence_status"]=="CERTAIN" for a in assertions)
    uncertain=sum(a["confidence_status"]=="UNCERTAIN" for a in assertions)
    ambiguous=sum(a["confidence_status"]=="AMBIGUOUS" for a in assertions)
    noncertain=uncertain+ambiguous
    unresolved=sum(a["predicate"]=="UNRESOLVED" for a in assertions)
    short=sum(len(a["evidence"].strip())<=3 for a in assertions)
    rate=noncertain/len(assertions) if assertions else 1.0
    over_30+=int(rate>0.30)
    empty+=int(not assertions)
    over_envelope+=int(len(assertions)>128)
    total_assertions+=len(assertions)
    total_noncertain+=noncertain
    total_unresolved+=unresolved
    total_short+=short
    docs.append({
        "pmid":pmid,
        "git_blob_sha1":actual_blob,
        "raw_sha256":hashlib.sha256(raw).hexdigest(),
        "assertions":len(assertions),
        "certain":certain,
        "uncertain":uncertain,
        "ambiguous":ambiguous,
        "noncertain_rate":rate,
        "unresolved_predicate":unresolved,
        "short_evidence_le3":short,
        "relation_count":len(g["relations"]),
        "normalization_event_count":len(g["audit"]["normalization_events"]),
        "section_heading_count":len(g["audit"]["section_headings"]),
    })

noncertain_rate=total_noncertain/total_assertions if total_assertions else 1.0
unresolved_rate=total_unresolved/total_assertions if total_assertions else 1.0
doc_over_30_rate=over_30/len(SOURCES)

# Development-only diagnostic rule, frozen before observing this stress result.
R4_NONCERTAIN_THRESHOLD=0.20
R4_UNRESOLVED_THRESHOLD=0.15
R4_DOC_OVER30_THRESHOLD=0.20
r1_incomplete=total_short>0 or empty>0 or over_envelope>0
r4_recommended=(
    not r1_incomplete and (
        noncertain_rate>R4_NONCERTAIN_THRESHOLD
        or unresolved_rate>R4_UNRESOLVED_THRESHOLD
        or doc_over_30_rate>R4_DOC_OVER30_THRESHOLD
    )
)

summary={
    "diagnostic_id":"AT0_EN_V26_REAL_RCT_STRESS_V1",
    "source_dataset":"sociocom/PICO-Corpus",
    "source_commit":SRC_COMMIT,
    "selected_documents":len(SOURCES),
    "factpico_used_for_scoring_or_tuning":False,
    "purpose":"DEVELOPMENT_DIAGNOSTIC_ONLY",
    "aggregate":{
        "total_assertions":total_assertions,
        "noncertain_assertions":total_noncertain,
        "noncertain_rate":noncertain_rate,
        "unresolved_predicates":total_unresolved,
        "unresolved_rate":unresolved_rate,
        "short_evidence_le3":total_short,
        "documents_noncertain_gt_30pct":over_30,
        "documents_noncertain_gt_30pct_rate":doc_over_30_rate,
        "empty_representation_documents":empty,
        "over_128_assertion_documents":over_envelope,
    },
    "frozen_r4_diagnostic_thresholds":{
        "aggregate_noncertain_rate_gt":R4_NONCERTAIN_THRESHOLD,
        "aggregate_unresolved_rate_gt":R4_UNRESOLVED_THRESHOLD,
        "document_fraction_with_noncertain_gt_30pct_gt":R4_DOC_OVER30_THRESHOLD,
    },
    "r1_incomplete":r1_incomplete,
    "r4_recommended":r4_recommended,
    "documents":docs,
}
raw=json.dumps(summary,sort_keys=True,separators=(",",":"))
summary["canonical_summary_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
print(json.dumps(summary,sort_keys=True,indent=2))
