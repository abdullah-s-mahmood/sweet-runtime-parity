#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from collections import Counter,defaultdict

CAL=Path("M2H_CALIBRATION_V1.jsonl")
ARETA=Path("upstream/arabic-gec/areta/m2h_calibration.areta.txt")
ENRICHED=Path("upstream/arabic-gec/areta/m2h_calibration.areta.enriched.tsv")

ORTH={"OH","OT","OA","OW","ON","OS","OG","OC","OR","OD","OM","OO"}
MORPH={"MI","MT","MO"}
SYNTAX={"XC","XF","XG","XN","XT","XM","XO"}
BOUNDARY={"MG","SP"}

def base_codes(label:str):
    out=set()
    for part in label.split("+"):
        x=part.strip()
        if not x: continue
        x=re.sub(r"^(REPLACE_|INSERT_|DELETE_)","",x)
        x=re.sub(r"\^(2|\*)$","",x)
        if x:
            out.add(x)
    return sorted(out)

rows=[json.loads(x) for x in CAL.read_text(encoding="utf-8").splitlines() if x.strip()]
groups=[]
cur=[]
for line in ARETA.read_text(encoding="utf-8",errors="replace").splitlines():
    if not line.strip():
        groups.append(cur);cur=[]
        continue
    p=line.split("\t")
    if len(p)<3:
        raise SystemExit(f"Malformed ARETA row: {line[:120]}")
    cur.append({"raw":p[0],"correct":p[1],"label":p[2],"codes":base_codes(p[2])})
if cur: groups.append(cur)
while groups and not groups[-1]:
    groups.pop()

if len(groups)!=len(rows):
    raise SystemExit(f"Sentence-group mismatch ARETA={len(groups)} CAL={len(rows)}")

case_out=[]
label_counts=Counter()
code_counts=Counter()
orth_cases=morph_cases=syntax_cases=boundary_cases=unk_cases=0

for rec,g in zip(rows,groups):
    labels=[]
    codes=set()
    has_unk=False
    for t in g:
        labels.append(t["label"])
        label_counts[t["label"]]+=1
        for c in t["codes"]:
            codes.add(c);code_counts[c]+=1
        if t["label"]=="UNK" or "UNK" in t["codes"]:
            has_unk=True
    flags={
        "orthographic":bool(codes & ORTH),
        "morphology_primary":bool(codes & {"MI","MT"}),
        "morphology_any":bool(codes & MORPH),
        "syntax":bool(codes & SYNTAX),
        "boundary":bool(codes & BOUNDARY),
        "contains_unk":has_unk
    }
    orth_cases+=flags["orthographic"]
    morph_cases+=flags["morphology_primary"]
    syntax_cases+=flags["syntax"]
    boundary_cases+=flags["boundary"]
    unk_cases+=flags["contains_unk"]
    case_out.append({
        "case_id":rec["case_id"],
        "uid":rec["uid"],
        "split":rec["split"],
        "line_no":rec["line_no"],
        "areta_codes":sorted(codes),
        "flags":flags,
        "token_annotations":g
    })

Path("M2H_CALIBRATION_ARETA_ENRICHMENT_V1.jsonl").write_text(
    "\n".join(json.dumps(x,ensure_ascii=False) for x in case_out)+"\n",
    encoding="utf-8"
)

summary={
    "record_id":"M2H_CALIBRATION_ARETA_ENRICHMENT_V1",
    "status":"READY",
    "cases":len(case_out),
    "sentence_groups":len(groups),
    "case_strata":{
        "orthographic":orth_cases,
        "morphology_primary_MI_or_MT":morph_cases,
        "syntax":syntax_cases,
        "boundary_MG_or_SP":boundary_cases,
        "contains_UNK":unk_cases
    },
    "code_counts":dict(sorted(code_counts.items())),
    "raw_label_counts":dict(label_counts.most_common()),
    "integrity":{
        "calibration_only":True,
        "internal_evaluation_opened":False,
        "stress_diagnostic_opened":False,
        "confirmation_opened":False,
        "holdout_opened":False,
        "a7ta_reserved_opened":False,
        "reserved_nahw_opened":False,
        "qalb15_test_opened":False
    },
    "scientific_role":"DIAGNOSTIC_STRATIFICATION_ONLY_NOT_INDEPENDENT_GOLD"
}
Path("M2H_CALIBRATION_ARETA_SUMMARY_V1.json").write_text(
    json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(summary,ensure_ascii=False,indent=2))
