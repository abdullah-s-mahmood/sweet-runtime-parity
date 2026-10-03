from pathlib import Path
import json,sys,ast

ROOT=Path(__file__).resolve().parent
AT0=ROOT.parent
V22=AT0/"v2_2"
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(V22/"redteam"))
from at0_v2_3_relation_verifier import verify_case
from at0_v2_2_independent_redteam import SAFE, ATTACKS

ledger=json.loads((ROOT/"SOURCE_RELATION_LEDGER.json").read_text(encoding="utf-8"))
rows=[]

for cid,text in SAFE.items():
    r=verify_case(cid,text,ledger)
    rows.append({"kind":"SAFE","test_id":"SAFE_"+cid,"case_id":cid,"expected":"PASS_CANDIDATE","observed":r["disposition"],"status":"PASS" if r["disposition"]=="PASS_CANDIDATE" else "FAIL","relations":r["relations"]})

for tid,cid,text in ATTACKS:
    r=verify_case(cid,text,ledger)
    rows.append({"kind":"ADVERSARIAL","test_id":tid,"case_id":cid,"expected":"NOT_PASS","observed":r["disposition"],"status":"PASS" if r["disposition"]!="PASS_CANDIDATE" else "FAIL","relations":r["relations"]})

# Anti-overfit static gate: no case-id branch literals are permitted in verifier source.
src=(ROOT/"at0_v2_3_relation_verifier.py").read_text(encoding="utf-8")
for cid in [f"EN{i:02d}" for i in range(1,13)]:
    if cid in src:
        rows.append({"kind":"ANTI_OVERFIT","test_id":"NO_CASE_LITERAL_"+cid,"case_id":cid,"expected":"ABSENT","observed":"PRESENT","status":"FAIL","relations":[]})

summary={
 "gate":"AT0_EN_V2_3_RELATION_GRAPH_DEVELOPMENT_GATE",
 "new_model_inference":False,
 "safe_total":sum(r["kind"]=="SAFE" for r in rows),
 "safe_pass":sum(r["kind"]=="SAFE" and r["status"]=="PASS" for r in rows),
 "attack_total":sum(r["kind"]=="ADVERSARIAL" for r in rows),
 "attacks_caught":sum(r["kind"]=="ADVERSARIAL" and r["status"]=="PASS" for r in rows),
 "attack_escapes":[r["test_id"] for r in rows if r["kind"]=="ADVERSARIAL" and r["status"]=="FAIL"],
 "anti_overfit_failures":[r["test_id"] for r in rows if r["kind"]=="ANTI_OVERFIT" and r["status"]=="FAIL"],
 "total_checks":len(rows),
 "passed":sum(r["status"]=="PASS" for r in rows),
 "failed":sum(r["status"]=="FAIL" for r in rows),
}
(ROOT/"V2_3_DEVELOPMENT_GATE_DETAIL.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"V2_3_DEVELOPMENT_GATE_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
if summary["safe_pass"]!=12 or summary["attacks_caught"]!=24 or summary["anti_overfit_failures"]:
    raise SystemExit(2)
