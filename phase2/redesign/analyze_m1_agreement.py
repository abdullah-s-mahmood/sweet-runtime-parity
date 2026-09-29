#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCHEMA=json.loads((HERE/"M1_LABEL_SCHEMA.json").read_text(encoding="utf-8"))
AXES=list(SCHEMA["axes"])

def load(path):
    return {r["m1_case_id"]:r for r in (json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip())}

def kappa(a,b):
    n=len(a)
    if not n: return None
    po=sum(x==y for x,y in zip(a,b))/n
    ca,cb=Counter(a),Counter(b)
    cats=set(ca)|set(cb)
    pe=sum((ca[c]/n)*(cb[c]/n) for c in cats)
    if pe>=1.0: return 1.0 if po==1.0 else None
    return (po-pe)/(1-pe)

def nominal_alpha_two(a,b):
    # Krippendorff nominal alpha via observed pair disagreement and pooled expected disagreement.
    n=len(a)
    if not n: return None
    do=sum(x!=y for x,y in zip(a,b))/n
    pooled=Counter(a+b); N=2*n
    if N<=1: return None
    agree_exp=sum(v*(v-1) for v in pooled.values())/(N*(N-1))
    de=1-agree_exp
    if de==0: return 1.0 if do==0 else None
    return 1-do/de

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("reviewer_a"); ap.add_argument("reviewer_b")
    ap.add_argument("--out",default="M1_AGREEMENT_REPORT.json")
    args=ap.parse_args()
    A,B=load(args.reviewer_a),load(args.reviewer_b)
    ids=sorted(set(A)&set(B))
    report={"status":"M1_PRIMARY_PASS_AGREEMENT","paired_cases":len(ids),"axes":{},"disagreements":[]}
    for axis in AXES:
        aa=[A[i][axis] for i in ids]; bb=[B[i][axis] for i in ids]
        raw=sum(x==y for x,y in zip(aa,bb))/len(ids) if ids else None
        report["axes"][axis]={"raw_agreement":raw,"cohen_kappa_nominal":kappa(aa,bb),"krippendorff_alpha_nominal":nominal_alpha_two(aa,bb)}
    for i in ids:
        diff={axis:[A[i][axis],B[i][axis]] for axis in AXES if A[i][axis]!=B[i][axis]}
        if diff: report["disagreements"].append({"m1_case_id":i,"axes":diff})
    Path(args.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","paired_cases":len(ids),"cases_with_any_disagreement":len(report["disagreements"]),"out":args.out},ensure_ascii=False,indent=2))
