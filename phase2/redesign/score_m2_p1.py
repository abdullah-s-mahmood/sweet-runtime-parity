#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

SAFE={"CLEAN_REFERENCE_KEEP","FULL_EXPERT_REPAIR","SINGLE_EDIT_COMPLETE"}
UNSAFE={"ERRONEOUS_SOURCE_KEEP","ONE_OF_MANY_PARTIAL","ALL_BUT_ONE_PARTIAL"}

def load(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def ratio(a,b): return a/b if b else None

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("pred")
    ap.add_argument("--out",default="M2_P1_DEV_RESULTS.json")
    args=ap.parse_args()
    K={x["case_id"]:x for x in load(args.key)}
    P={x["case_id"]:x for x in load(args.pred)}
    if set(K)!=set(P): raise SystemExit("key/pred IDs differ")
    rows=[{**K[c],"decision":P[c]["decision"],"candidate_status":P[c]["candidate_status"],"confidence":P[c]["confidence"]} for c in sorted(K)]
    safe=[r for r in rows if r["gold_family"] in SAFE]
    unsafe=[r for r in rows if r["gold_family"] in UNSAFE]
    fam={}
    for f in sorted({r["gold_family"] for r in rows}):
        xs=[r for r in rows if r["gold_family"]==f]
        a=sum(r["decision"]=="ACCEPT" for r in xs)
        fam[f]={"n":len(xs),"accept":a,"review":sum(r["decision"]=="REVIEW" for r in xs),"reject":sum(r["decision"]=="REJECT" for r in xs),"accept_rate":ratio(a,len(xs))}
    src={}
    for s in sorted({r["source_family"] for r in rows}):
        xs=[r for r in rows if r["source_family"]==s]
        us=[r for r in xs if r["gold_family"] in UNSAFE]; ss=[r for r in xs if r["gold_family"] in SAFE]
        ua=sum(r["decision"]=="ACCEPT" for r in us); sa=sum(r["decision"]=="ACCEPT" for r in ss)
        src[s]={"n":len(xs),"unsafe_n":len(us),"unsafe_accept":ua,"uar":ratio(ua,len(us)),"safe_n":len(ss),"safe_accept":sa,"sac":ratio(sa,len(ss))}
    ua=sum(r["decision"]=="ACCEPT" for r in unsafe); sa=sum(r["decision"]=="ACCEPT" for r in safe)
    uar=ratio(ua,len(unsafe)); sac=ratio(sa,len(safe))
    review=sum(r["decision"]=="REVIEW" for r in rows)
    safe_reject=sum(r["decision"]=="REJECT" for r in safe)
    one=fam.get("ONE_OF_MANY_PARTIAL",{}).get("accept",0)
    abo=fam.get("ALL_BUT_ONE_PARTIAL",{}).get("accept",0)
    clean=fam.get("CLEAN_REFERENCE_KEEP",{}).get("accept_rate")
    full=fam.get("FULL_EXPERT_REPAIR",{}).get("accept_rate")
    source_ok=all(v["uar"] is None or v["uar"]<=0.10 for v in src.values())
    gate={
      "uar_le_0_05":uar is not None and uar<=0.05,
      "all_but_one_zero_accept":abo==0,
      "one_of_many_accept_le_1_pending_audit":one<=1,
      "sac_ge_0_60":sac is not None and sac>=0.60,
      "clean_keep_accept_ge_0_60":clean is not None and clean>=0.60,
      "full_repair_accept_ge_0_60":full is not None and full>=0.60,
      "all_source_uar_le_0_10":source_ok
    }
    passed=all(gate.values())
    status="PASS_PROVISIONAL_PARTIAL_AUDIT" if passed and one==1 else ("PASS" if passed else "FAIL")
    result={
      "status":status,"n_total":len(rows),"n_safe":len(safe),"n_unsafe":len(unsafe),
      "unsafe_accept":ua,"uar":uar,"safe_accept":sa,"sac":sac,
      "review":review,"review_burden":ratio(review,len(rows)),
      "safe_reject":safe_reject,"safe_rejection_error":ratio(safe_reject,len(safe)),
      "family":fam,"source":src,"gate":gate,
      "further_prompt_revision_allowed":False,
      "a7ta_reserved_opened":False
    }
    Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
