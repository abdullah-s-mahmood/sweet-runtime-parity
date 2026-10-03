from pathlib import Path
import json,sys,collections

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from at0_v2_3_relation_verifier import verify_case

if len(sys.argv)!=3:
    raise SystemExit("usage: replay_v2_2_passes.py V2_2_REPLAY.jsonl OUT.jsonl")
source=Path(sys.argv[1]); out=Path(sys.argv[2])
ledger=json.loads((ROOT/"SOURCE_RELATION_LEDGER.json").read_text(encoding="utf-8"))
rows=[json.loads(x) for x in source.read_text(encoding="utf-8").splitlines() if x.strip()]
passes=[r for r in rows if r.get("disposition")=="PASS_CANDIDATE"]
if len(passes)!=30:
    raise RuntimeError(f"EXPECTED_30_V22_PASS_CANDIDATES_GOT_{len(passes)}")

result=[]
for r in passes:
    text=r.get("candidate_text")
    if not isinstance(text,str) or not text.strip():
        raise RuntimeError(f"MISSING_CANDIDATE_TEXT:{r.get('slot_id')}")
    v=verify_case(r["case_id"],text,ledger)
    result.append({
        "slot_id":r["slot_id"],
        "case_id":r["case_id"],
        "model_slot":r["model_slot"],
        "arm":r["arm"],
        "v2_2_disposition":"PASS_CANDIDATE",
        "v2_3_disposition":v["disposition"],
        "relation_counts":v["relation_counts"],
        "relations":v["relations"],
        "candidate_text":text,
    })

out.parent.mkdir(parents=True,exist_ok=True)
out.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in result),encoding="utf-8")
cnt=collections.Counter(x["v2_3_disposition"] for x in result)
known=next(x for x in result if x["slot_id"]=="MODEL_A-EN01-DIRECT")
summary={
    "gate":"AT0_EN_V2_3_REPLAY_OF_30_V22_PASS_CANDIDATES",
    "new_model_inference":False,
    "input_v2_2_pass_candidates":30,
    "v2_3_dispositions":dict(sorted(cnt.items())),
    "known_en01_modal_drift_disposition":known["v2_3_disposition"],
    "known_en01_no_longer_auto_passes":known["v2_3_disposition"]!="PASS_CANDIDATE",
    "pass_candidate_ids":[x["slot_id"] for x in result if x["v2_3_disposition"]=="PASS_CANDIDATE"],
    "review_ids":[x["slot_id"] for x in result if x["v2_3_disposition"]=="REVIEW"],
    "reject_ids":[x["slot_id"] for x in result if x["v2_3_disposition"]=="REJECT"],
}
sp=out.with_suffix(".summary.json")
sp.write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
if not summary["known_en01_no_longer_auto_passes"]:
    raise SystemExit(2)
