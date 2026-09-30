#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def load(p):return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def norm(s):return " ".join((s or "").strip().split())
def ratio(a,b):return a/b if b else None

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("blind");ap.add_argument("key");ap.add_argument("pred");ap.add_argument("--out",default="M2RV2_P0_RESULTS.json");args=ap.parse_args()
    B={x["case_id"]:x for x in load(args.blind)};K={x["case_id"]:x for x in load(args.key)};P={x["case_id"]:x for x in load(args.pred)}
    if not(set(B)==set(K)==set(P)):raise SystemExit("ID mismatch")
    ec=ech=gt=gh=ct=cfp=st=sh=pt=pm=inv=0
    for cid in sorted(B):
        cand=B[cid]["candidate"];k=K[cid];pred=P[cid].get("mandatory_errors",[]);gold=k.get("gold_errors",[])
        if k["family"]=="CLEAN_QALB_REFERENCE":
            ct+=1;cfp+=int(bool(pred))
        else:
            ec+=1;gt+=len(gold);hits=set()
            for i,g in enumerate(gold):
                if any(norm(x.get("surface"))==norm(g["surface"]) for x in pred):hits.add(i)
            ech+=int(bool(hits));gh+=len(hits)
            if k["family"]=="QALB_ALL_BUT_ONE_STRICT":
                st+=1;sh+=int(bool(hits))
        for x in pred:
            pt+=1;s=x.get("surface","")
            inv+=int(s not in cand)
            pm+=int(any(norm(s)==norm(g["surface"]) for g in gold))
    crr=ratio(ech,ec);gelr=ratio(gh,gt);cfpr=ratio(cfp,ct);srr=ratio(sh,st);cp=ratio(pm,pt);ir=ratio(inv,pt)
    gate={"cfpr_le_0_05":cfpr<=.05,"crr_ge_0_85":crr>=.85,"gelr_ge_0_80":gelr>=.80,"strict_residual_recall_ge_0_90":srr>=.90,"invalid_surface_rate_le_0_02":ir is not None and ir<=.02}
    res={"status":"PASS" if all(gate.values()) else "FAIL","n_total":len(B),"error_contexts":ec,"clean_contexts":ct,"context_residual_recall":crr,"gold_error_localization_recall":gelr,"clean_false_positive_rate":cfpr,"strict_residual_recall":srr,"claim_precision_diagnostic":cp,"invalid_surface_rate":ir,"gold_error_instances":gt,"gold_hits":gh,"predicted_claims":pt,"matched_claims":pm,"gate":gate,"p1_allowed_if_fail":True,"confirmation_opened":False,"holdout_opened":False}
    Path(args.out).write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n");print(json.dumps(res,ensure_ascii=False,indent=2))
