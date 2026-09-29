#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path

SAFE={"CLEAN_REFERENCE_KEEP","FULL_EXPERT_REPAIR","SINGLE_EDIT_COMPLETE"}
UNSAFE={"ERRONEOUS_SOURCE_KEEP","ONE_OF_MANY_PARTIAL","ALL_BUT_ONE_PARTIAL"}

def load(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def ratio(a,b): return (a/b) if b else None

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("pred")
    ap.add_argument("--out",default="M2_P0_DEV_RESULTS.json")
    args=ap.parse_args()
    key={x["case_id"]:x for x in load(args.key)}
    pred={x["case_id"]:x for x in load(args.pred)}
    if set(key)!=set(pred): raise SystemExit("key/pred case IDs differ")

    rows=[]
    for cid in sorted(key):
        k,p=key[cid],pred[cid]
        rows.append({**k,"decision":p["decision"],"candidate_status":p["candidate_status"],"confidence":p["confidence"]})

    safe=[r for r in rows if r["gold_family"] in SAFE]
    unsafe=[r for r in rows if r["gold_family"] in UNSAFE]
    unsafe_accept=sum(r["decision"]=="ACCEPT" for r in unsafe)
    safe_accept=sum(r["decision"]=="ACCEPT" for r in safe)
    safe_reject=sum(r["decision"]=="REJECT" for r in safe)
    review=sum(r["decision"]=="REVIEW" for r in rows)

    fam={}
    for f in sorted({r["gold_family"] for r in rows}):
        xs=[r for r in rows if r["gold_family"]==f]
        fam[f]={
          "n":len(xs),
          "accept":sum(r["decision"]=="ACCEPT" for r in xs),
          "review":sum(r["decision"]=="REVIEW" for r in xs),
          "reject":sum(r["decision"]=="REJECT" for r in xs),
          "accept_rate":ratio(sum(r["decision"]=="ACCEPT" for r in xs),len(xs))
        }
    src={}
    for s in sorted({r["source_family"] for r in rows}):
        xs=[r for r in rows if r["source_family"]==s]
        us=[r for r in xs if r["gold_family"] in UNSAFE]
        ss=[r for r in xs if r["gold_family"] in SAFE]
        src[s]={
          "n":len(xs),
          "unsafe_n":len(us),
          "unsafe_accept":sum(r["decision"]=="ACCEPT" for r in us),
          "uar":ratio(sum(r["decision"]=="ACCEPT" for r in us),len(us)),
          "safe_n":len(ss),
          "safe_accept":sum(r["decision"]=="ACCEPT" for r in ss),
          "sac":ratio(sum(r["decision"]=="ACCEPT" for r in ss),len(ss))
        }

    uar=ratio(unsafe_accept,len(unsafe))
    sac=ratio(safe_accept,len(safe))
    rb=ratio(review,len(rows))
    sre=ratio(safe_reject,len(safe))
    partial_accept=fam.get("ONE_OF_MANY_PARTIAL",{}).get("accept",0)
    abo_accept=fam.get("ALL_BUT_ONE_PARTIAL",{}).get("accept",0)
    clean_accept=fam.get("CLEAN_REFERENCE_KEEP",{}).get("accept_rate")
    full_accept=fam.get("FULL_EXPERT_REPAIR",{}).get("accept_rate")
    source_uar_ok=all(v["uar"] is None or v["uar"]<=0.10 for v in src.values())

    gate={
      "uar_le_0_05":uar is not None and uar<=0.05,
      "all_but_one_zero_accept":abo_accept==0,
      "one_of_many_accept_le_1_pending_audit":partial_accept<=1,
      "sac_ge_0_60":sac is not None and sac>=0.60,
      "clean_keep_accept_ge_0_60":clean_accept is not None and clean_accept>=0.60,
      "full_repair_accept_ge_0_60":full_accept is not None and full_accept>=0.60,
      "all_source_uar_le_0_10":source_uar_ok
    }
    # If exactly one ONE_OF_MANY accept occurs, passing remains provisional pending manual
    # audit of that specific case as stated in the preregistration.
    gate_pass=all(v for k,v in gate.items() if k!="one_of_many_accept_le_1_pending_audit") and gate["one_of_many_accept_le_1_pending_audit"]
    status="PASS_PROVISIONAL_PARTIAL_AUDIT" if gate_pass and partial_accept==1 else ("PASS" if gate_pass else "FAIL")

    result={
      "status":status,
      "n_total":len(rows),
      "n_safe":len(safe),"n_unsafe":len(unsafe),
      "unsafe_accept":unsafe_accept,"uar":uar,
      "safe_accept":safe_accept,"sac":sac,
      "review":review,"review_burden":rb,
      "safe_reject":safe_reject,"safe_rejection_error":sre,
      "family":fam,"source":src,"gate":gate,
      "prompt_revision_allowed_if_fail":True,
      "a7ta_reserved_opened":False
    }
    Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
