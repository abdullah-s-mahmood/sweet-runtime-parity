#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from scipy.stats import beta

DOMAIN = "ACAD_PASS_FRESH2026_V1|precision-audit"
ALPHA_PER_CLASS = 0.0125
PRECISION_LOWER_BOUND_MIN = 0.90
MIN_CONTRIBUTING_FAMILIES = 200
CLASSES = ("P","I","C","O")

def clopper_pearson_lower(k:int,n:int,alpha:float=ALPHA_PER_CLASS)->float:
    if not (0 <= k <= n):
        raise ValueError(f"require 0 <= k <= n, got k={k}, n={n}")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0,1)")
    if n == 0 or k == 0:
        return 0.0
    x=float(beta.ppf(alpha,k,n-k+1))
    if not math.isfinite(x) or not (0.0 <= x <= 1.0):
        raise RuntimeError(f"nonfinite/invalid beta quantile: {x}")
    return x

def audit_message(row:dict)->bytes:
    c=str(row["class"])
    if c not in CLASSES:
        raise ValueError(f"unknown class {c}")
    fields=[
        DOMAIN,c,str(row["family_id"]),str(row["document_id"]),
        str(int(row["start"])),str(int(row["end"]))
    ]
    return "|".join(fields).encode("utf-8")

def audit_rank(secret:bytes,row:dict)->bytes:
    if len(secret) != 32:
        raise ValueError("secret must be exactly 256 bits (32 bytes)")
    return hmac.new(secret,audit_message(row),hashlib.sha256).digest()

def select_one_per_class_family(rows:Iterable[dict],secret:bytes)->list[dict]:
    grouped=defaultdict(list)
    seen=set()
    for row in rows:
        c=str(row["class"])
        if c not in CLASSES:
            raise ValueError(f"unknown class {c}")
        start,end=int(row["start"]),int(row["end"])
        if start < 0 or end <= start:
            raise ValueError("invalid coordinates")
        ident=(c,str(row["family_id"]),str(row["document_id"]),start,end)
        if ident in seen:
            raise ValueError(f"duplicate accepted prediction identity {ident}")
        seen.add(ident)
        grouped[(c,str(row["family_id"]))].append(dict(row))
    selected=[]
    for (c,fam),items in sorted(grouped.items()):
        ranked=[]
        for row in items:
            digest=audit_rank(secret,row)
            # hash first; coordinate identity is deterministic tie-breaker.
            tie=(str(row["document_id"]),int(row["start"]),int(row["end"]))
            ranked.append((digest,tie,row))
        ranked.sort(key=lambda x:(x[0],x[1]))
        chosen=dict(ranked[0][2])
        chosen["audit_hmac_sha256"]=ranked[0][0].hex()
        selected.append(chosen)
    return selected

def score_trial_balanced(selected_rows:Iterable[dict])->dict:
    by_class={c:[] for c in CLASSES}
    for row in selected_rows:
        c=str(row["class"])
        if c not in CLASSES:
            raise ValueError(f"unknown class {c}")
        if "correct" not in row:
            raise ValueError("gold correctness must be joined only after selection")
        corr=row["correct"]
        if corr not in (True,False,0,1):
            raise ValueError("correct must be boolean")
        by_class[c].append(bool(corr))
    out={}
    all_pass=True
    for c in CLASSES:
        vals=by_class[c]
        n=len(vals); k=sum(vals)
        lower=clopper_pearson_lower(k,n)
        support=(n>=MIN_CONTRIBUTING_FAMILIES)
        bound=(lower>=PRECISION_LOWER_BOUND_MIN)
        passed=bool(support and bound)
        out[c]={
            "n_contributing_families":n,
            "k_correct":k,
            "point_precision":(k/n if n else None),
            "alpha_one_sided":ALPHA_PER_CLASS,
            "clopper_pearson_lower":lower,
            "support_pass":support,
            "lower_bound_pass":bound,
            "class_pass":passed,
        }
        all_pass = all_pass and passed
    return {
        "estimand":"TRIAL_BALANCED_PRECISION_ONE_ACCEPTED_SPAN_PER_CLASS_PER_FAMILY",
        "simultaneous_familywise_confidence":0.95,
        "bonferroni_classes":4,
        "per_class":out,
        "all_classes_pass":all_pass,
        "warning":"This is not an exact confidence bound for pooled entity-weighted precision."
    }

def synthetic_preflight()->dict:
    # Numerical fixtures from the independent review.
    expected={
        (95,100):0.8772335911610268,
        (190,200):0.9037442005509154,
        (475,500):0.9235837897122915,
    }
    numerical={}
    for (k,n),e in expected.items():
        got=clopper_pearson_lower(k,n)
        if abs(got-e)>5e-13:
            raise RuntimeError(f"CP fixture mismatch {(k,n)} got={got} expected={e}")
        numerical[f"{k}/{n}"]=got

    secret=bytes(range(32))
    rows=[]
    for c in CLASSES:
        for fam in range(1,6):
            for j in range(3):
                rows.append({
                    "class":c,
                    "family_id":f"F{fam:03d}",
                    "document_id":f"D{fam:03d}",
                    "start":10*j+fam,
                    "end":10*j+fam+3,
                    "confidence":0.99-j*0.01, # deliberately unused by selection
                })

    selected1=select_one_per_class_family(rows,secret)
    if len(selected1)!=20:
        raise RuntimeError(f"unexpected selected count {len(selected1)}")

    # Label-blindness: correctness cannot affect selection because it is absent.
    rows_with_fake_labels=[]
    for i,r in enumerate(rows):
        q=dict(r); q["correct"]=(i%2==0)
        rows_with_fake_labels.append(q)
    selected2=select_one_per_class_family(rows_with_fake_labels,secret)
    ids1=[(r["class"],r["family_id"],r["document_id"],r["start"],r["end"],r["audit_hmac_sha256"]) for r in selected1]
    ids2=[(r["class"],r["family_id"],r["document_id"],r["start"],r["end"],r["audit_hmac_sha256"]) for r in selected2]
    if ids1!=ids2:
        raise RuntimeError("selection changed when correctness labels were added")

    # Confidence must also not drive selection.
    rows_conf=[dict(r,confidence=(0.01 if i%2 else 0.999)) for i,r in enumerate(rows)]
    selected3=select_one_per_class_family(rows_conf,secret)
    ids3=[(r["class"],r["family_id"],r["document_id"],r["start"],r["end"],r["audit_hmac_sha256"]) for r in selected3]
    if ids1!=ids3:
        raise RuntimeError("selection changed when confidence changed")

    # Scoring fixtures: 190/200 must pass both support and bound; 95/100 must fail support/bound.
    score_rows=[]
    for c in CLASSES:
        for i in range(200):
            score_rows.append({"class":c,"family_id":f"{c}{i:03d}","correct":i<190})
    score=score_trial_balanced(score_rows)
    if not score["all_classes_pass"]:
        raise RuntimeError("190/200 x 4 should pass frozen trial-balanced gate")

    weak_rows=[]
    for c in CLASSES:
        for i in range(100):
            weak_rows.append({"class":c,"family_id":f"{c}{i:03d}","correct":i<95})
    weak=score_trial_balanced(weak_rows)
    if weak["all_classes_pass"]:
        raise RuntimeError("95/100 x 4 must not pass")

    # Secret sensitivity: changing S should generally change at least one selected identity.
    secret2=hashlib.sha256(secret).digest()
    ids4=[(r["class"],r["family_id"],r["document_id"],r["start"],r["end"])
          for r in select_one_per_class_family(rows,secret2)]
    ids1_short=[x[:5] for x in ids1]
    if ids4==ids1_short:
        raise RuntimeError("synthetic secret-sensitivity fixture did not change any choice")

    return {
        "state":"FRESH_RCT_TRIAL_BALANCED_STATS_SYNTHETIC_PREFLIGHT_PASS",
        "scientific_data_used":False,
        "eval_data_used":False,
        "new_rct_data_used":False,
        "numerical_fixtures":numerical,
        "selection_label_blind":True,
        "selection_confidence_blind":True,
        "secret_domain_separated":True,
        "support_min_families":MIN_CONTRIBUTING_FAMILIES,
        "alpha_per_class":ALPHA_PER_CLASS,
        "lower_bound_min":PRECISION_LOWER_BOUND_MIN,
        "pass_fixture":"190/200_PER_CLASS",
        "fail_fixture":"95/100_PER_CLASS",
        "estimand_warning":"Trial-balanced only; not pooled entity-weighted population precision.",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight:
        raise SystemExit("Only --synthetic-preflight is authorized in readiness stage")
    report=synthetic_preflight()
    s=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(s,encoding="utf-8")
    print(s,end="")

if __name__=="__main__":
    main()
