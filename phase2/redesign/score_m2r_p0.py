#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path

def load(p): return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def norm(s): return " ".join((s or "").strip().split())
def ratio(a,b): return a/b if b else None

def gold_matches(pred_surface,gold_surface):
    return norm(pred_surface)==norm(gold_surface)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("blind"); ap.add_argument("key"); ap.add_argument("pred")
    ap.add_argument("--out",default="M2R_P0_DEV_RESULTS.json")
    args=ap.parse_args()
    B={x["case_id"]:x for x in load(args.blind)}
    K={x["case_id"]:x for x in load(args.key)}
    P={x["case_id"]:x for x in load(args.pred)}
    if not (set(B)==set(K)==set(P)): raise SystemExit("ID mismatch")

    error_contexts=0; error_context_hits=0
    gold_total=0; gold_hit=0
    clean_total=0; clean_fp=0
    abo_total=0; abo_hit=0
    pred_total=0; pred_match=0; invalid_surface=0
    dim_total=Counter(); dim_hit=Counter()
    fam=defaultdict(lambda:Counter())
    conf=defaultdict(lambda:Counter())

    for cid in sorted(B):
        cand=B[cid]["candidate"]; k=K[cid]; p=P[cid]
        gold=k.get("gold_errors",[])
        preds=p.get("mandatory_errors",[])
        pfam=k["family"]; fam[pfam]["n"]+=1
        if pfam=="CLEAN_TARGET_CONTEXT":
            clean_total+=1
            if preds: clean_fp+=1
        else:
            error_contexts+=1
            gold_total+=len(gold)
            matched_gold=set()
            for gi,g in enumerate(gold):
                for d in g.get("dimensions",[]): dim_total[d]+=1
                if any(gold_matches(pr.get("surface"),g.get("surface")) for pr in preds):
                    matched_gold.add(gi)
                    for d in g.get("dimensions",[]): dim_hit[d]+=1
            if matched_gold: error_context_hits+=1
            gold_hit+=len(matched_gold)
            if pfam=="ALL_BUT_ONE_RESIDUAL":
                abo_total+=1
                if matched_gold: abo_hit+=1

        for pr in preds:
            pred_total+=1
            s=pr.get("surface","")
            if s not in cand:
                invalid_surface+=1
            ismatch=any(gold_matches(s,g.get("surface")) for g in gold)
            if ismatch: pred_match+=1
            conf[pr.get("confidence","UNKNOWN")]["n"]+=1
            conf[pr.get("confidence","UNKNOWN")]["match"]+=int(ismatch)

    crr=ratio(error_context_hits,error_contexts)
    gelr=ratio(gold_hit,gold_total)
    cfpr=ratio(clean_fp,clean_total)
    ncwr=ratio(abo_hit,abo_total)
    cp=ratio(pred_match,pred_total)
    invalid_rate=ratio(invalid_surface,pred_total)
    drec={d:{"n":dim_total[d],"hit":dim_hit[d],"recall":ratio(dim_hit[d],dim_total[d])} for d in sorted(dim_total)}
    orth=drec.get("ORTHOGRAPHY",{"n":0,"recall":None})
    major_nonorth_ok=True
    for d in ["MORPHOLOGY","SYNTAX","LEXICAL"]:
        x=drec.get(d,{"n":0,"recall":None})
        if x["n"]>=20 and x["recall"]<0.70: major_nonorth_ok=False

    gate={
      "cfpr_le_0_05":cfpr is not None and cfpr<=0.05,
      "crr_ge_0_85":crr is not None and crr>=0.85,
      "gelr_ge_0_80":gelr is not None and gelr>=0.80,
      "ncwr_ge_0_90":ncwr is not None and ncwr>=0.90,
      "orth_recall_ge_0_95_if_n20":orth["n"]<20 or orth["recall"]>=0.95,
      "nonorth_major_recall_ge_0_70_if_n20":major_nonorth_ok,
      "invalid_surface_rate_le_0_02":invalid_rate is not None and invalid_rate<=0.02
    }
    result={
      "status":"PASS" if all(gate.values()) else "FAIL",
      "n_total":len(B),
      "error_contexts":error_contexts,
      "clean_contexts":clean_total,
      "context_residual_recall":crr,
      "gold_error_localization_recall":gelr,
      "clean_false_positive_rate":cfpr,
      "near_complete_withheld_recall":ncwr,
      "claim_precision":cp,
      "invalid_surface_rate":invalid_rate,
      "dimension_recall":drec,
      "gate":gate,
      "further_prompt_revision_allowed_if_fail":True,
      "confirmation_opened":False,
      "holdout_opened":False
    }
    Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
