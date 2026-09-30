#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib, re

ORTH={"OA","OC","OD","OG","OH","OM","ON","OR","OS","OT","OW"}
MORPH={"MI","MT"}

def base_labels(tag):
    out=[]
    for part in tag.split("+"):
        part=part.strip()
        if not part:
            continue
        for pfx in ("REPLACE_","INSERT_","DELETE_"):
            if part.startswith(pfx):
                part=part[len(pfx):]
                break
        if "^" in part:
            part=part.split("^",1)[0]
        if part in {"MERGE","SPLIT","UC","UNK"}:
            out.append(part)
        elif re.fullmatch(r"[A-Z]{2}",part):
            out.append(part)
    return out

def read_blocks(path):
    lines=pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("SOURCE\tTARGET"):
        lines=lines[1:]
    blocks=[]; cur=[]
    for line in lines:
        if not line.strip():
            if cur:
                blocks.append(cur); cur=[]
            continue
        p=line.split("\t")
        if len(p)<3:
            raise SystemExit(f"bad enriched line: {line[:120]!r}")
        cur.append((p[0],p[1],p[2]))
    if cur: blocks.append(cur)
    return blocks

ap=argparse.ArgumentParser()
ap.add_argument("--calibration",required=True)
ap.add_argument("--enriched",required=True)
ap.add_argument("--out-jsonl",required=True)
ap.add_argument("--out-summary",required=True)
ap.add_argument("--pip-freeze",required=True)
args=ap.parse_args()

cases=[json.loads(x) for x in pathlib.Path(args.calibration).read_text(encoding="utf-8").splitlines() if x.strip()]
blocks=read_blocks(args.enriched)
if len(cases)!=6888: raise SystemExit(f"expected 6888 calibration cases, got {len(cases)}")
if len(blocks)!=len(cases): raise SystemExit(f"ARETA block mismatch: {len(blocks)} vs {len(cases)}")

label_tokens=collections.Counter()
label_cases=collections.Counter()
orth_cases=morph_cases=unk_cases=0
rows=[]

for case,block in zip(cases,blocks):
    labels=[]
    token_rows=[]
    for src,tgt,tag in block:
        bs=base_labels(tag)
        labels.extend(bs)
        for b in bs: label_tokens[b]+=1
        token_rows.append({"source":src,"target":tgt,"tag":tag})
    unique=sorted(set(labels))
    for b in unique: label_cases[b]+=1
    has_orth=bool(set(unique)&ORTH)
    has_morph=bool(set(unique)&MORPH)
    has_unk="UNK" in unique
    orth_cases+=int(has_orth); morph_cases+=int(has_morph); unk_cases+=int(has_unk)
    rows.append({
        "case_id":case["case_id"],
        "uid":case["uid"],
        "areta_labels":unique,
        "h2_orthographic_proxy":has_orth,
        "h3_morphology_proxy":has_morph,
        "areta_has_unk":has_unk,
        "token_annotations":token_rows
    })

outp=pathlib.Path(args.out_jsonl)
outp.write_text("\n".join(json.dumps(r,ensure_ascii=False) for r in rows)+"\n",encoding="utf-8")
freeze=pathlib.Path(args.pip_freeze).read_text(encoding="utf-8")
summary={
  "status":"M2H_ARETA_CALIBRATION_ENRICHMENT_COMPLETE",
  "cases":len(cases),
  "areta_blocks":len(blocks),
  "h2_orthographic_proxy_cases":orth_cases,
  "h3_morphology_proxy_cases":morph_cases,
  "unk_cases":unk_cases,
  "label_token_counts":dict(sorted(label_tokens.items())),
  "label_case_counts":dict(sorted(label_cases.items())),
  "orthographic_codes":sorted(ORTH),
  "morphology_codes":sorted(MORPH),
  "classification_note":"ARETA labels are DEVELOPMENT-ONLY diagnostic/proxy labels, not independent gold.",
  "pip_freeze_sha256":hashlib.sha256(freeze.encode()).hexdigest(),
  "integrity":{
    "calibration_only":True,
    "internal_evaluation_opened":False,
    "stress_diagnostic_opened":False,
    "thresholds_tuned":False,
    "verifier_executed":False
  }
}
pathlib.Path(args.out_summary).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
