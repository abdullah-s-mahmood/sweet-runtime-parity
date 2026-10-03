from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from at0_v2_3_assertion_graph import validate
sys.path.insert(0,str(ROOT.parent/"v2_2"/"redteam"))
from at0_v2_2_independent_redteam import SAFE, ATTACKS, CASES

rows=[]
for cid,text in SAFE.items():
    got=validate(cid,CASES[cid]["source_text"],text)
    expected="REJECT_BENCHMARK_DEFECT" if cid=="EN09" else "PASS_CANDIDATE"
    ok=(got["disposition"]!="PASS_CANDIDATE") if cid=="EN09" else (got["disposition"]=="PASS_CANDIDATE")
    rows.append({"kind":"SAFE_CONTROL","test_id":"SAFE_"+cid,"expected":expected,"observed":got["disposition"],"status":"PASS" if ok else "FAIL","findings":got["findings"]})
for tid,cid,text in ATTACKS:
    got=validate(cid,CASES[cid]["source_text"],text)
    ok=got["disposition"]!="PASS_CANDIDATE"
    rows.append({"kind":"ADVERSARIAL","test_id":tid,"expected":"NOT_PASS","observed":got["disposition"],"status":"PASS" if ok else "FAIL","findings":got["findings"]})
out=ROOT/"results"; out.mkdir(exist_ok=True)
p=out/"AT0_EN_V2_3_KNOWN_EXTERNAL_V1.json"
p.write_text(json.dumps({"total":len(rows),"passed":sum(x["status"]=="PASS" for x in rows),"failed":sum(x["status"]=="FAIL" for x in rows),"benchmark_defects":["SAFE_EN09 omits a scientific relation present in source_text; the frozen EN09 content_units also omit that source relation"],"results":rows},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(p.read_text())
if any(x["status"]=="FAIL" for x in rows): raise SystemExit(2)
