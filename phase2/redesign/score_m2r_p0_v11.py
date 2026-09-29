#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

def load(p):return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def norm(s):return " ".join((s or "").strip().split())
def ratio(a,b):return a/b if b else None
def match(p,g):return norm(p)==norm(g)

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("blind");ap.add_argument("key");ap.add_argument("pred");ap.add_argument("--out",default="M2R_P0_DEV_RESULTS.json");args=ap.parse_args()
    B={x["case_id"]:x for x in load(args.blind)};K={x["case_id"]:x for x in load(args.key)};P={x["case_id"]:x for x in load(args.pred)}
    if not(set(B)==set(K)==set(P)):raise SystemExit("ID mismatch")
    ec=ech=gt=gh=ct=cfp=rt=rh=pt=pm=inv=0
    dt=Counter();dh=Counter()
    for cid in sorted(B):
        cand=B[cid]["candidate"];k=K[cid];pred=P[cid].get("mandatory_errors",[]);gold=k.get("gold_errors",[])
        if k["family"]=="CLEAN_TARGET_CONTEXT":
            ct+=1;cfp+=int(bool(pred))
        else:
            ec+=1;gt+=len(gold);hits=set()
            for i,g in enumerate(gold):
                for d in g["dimensions"]:dt[d]+=1
                if any(match(x.get("surface"),g["surface"]) for x in pred):
                    hits.add(i)
                    for d in g["dimensions"]:dh[d]+=1
            if hits:ech+=1
            gh+=len(hits)
            if k["family"]=="EXPERT_REINSERTED_RESIDUAL":
                rt+=1;rh+=int(bool(hits))
        for x in pred:
            pt+=1;s=x.get("surface","")
            inv+=int(s not in cand)
            pm+=int(any(match(s,g["surface"]) for g in gold))
    drec={d:{"n":dt[d],"hit":dh[d],"recall":ratio(dh[d],dt[d])} for d in sorted(dt)}
    orth=drec.get("ORTHOGRAPHY",{"n":0,"recall":None})
    nonorth=True
    for d in ["MORPHOLOGY","SYNTAX","LEXICAL"]:
        x=drec.get(d,{"n":0,"recall":None})
        if x["n"]>=20 and x["recall"]<.70:nonorth=False
    crr=ratio(ech,ec);gelr=ratio(gh,gt);cfpr=ratio(cfp,ct);csrr=ratio(rh,rt);cp=ratio(pm,pt);ir=ratio(inv,pt)
    gate={"cfpr_le_0_05":cfpr<=.05,"crr_ge_0_85":crr>=.85,"gelr_ge_0_80":gelr>=.80,"csrr_ge_0_90":csrr>=.90,"orth_recall_ge_0_95_if_n20":orth["n"]<20 or orth["recall"]>=.95,"nonorth_major_recall_ge_0_70_if_n20":nonorth,"invalid_surface_rate_le_0_02":ir is not None and ir<=.02}
    res={"status":"PASS" if all(gate.values()) else "FAIL","n_total":len(B),"error_contexts":ec,"clean_contexts":ct,"context_residual_recall":crr,"gold_error_localization_recall":gelr,"clean_false_positive_rate":cfpr,"controlled_single_residual_recall":csrr,"claim_precision":cp,"invalid_surface_rate":ir,"dimension_recall":drec,"gate":gate,"p1_allowed_if_fail":True,"confirmation_opened":False,"holdout_opened":False}
    Path(args.out).write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n");print(json.dumps(res,ensure_ascii=False,indent=2))
