from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from at0_v2_2_validator import validate

cases={}
for line in (ROOT.parent/"cases.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        x=json.loads(line); cases[x["case_id"]]=x["source_text"]

tests=[]
def add(name,cid,text,expect_pass):
    tests.append((name,cid,text,expect_pass))

# Frozen source self-checks: every source must remain a PASS_CANDIDATE.
for cid,src in sorted(cases.items()):
    add("SOURCE_"+cid,cid,src,True)

# Adversarial mutations.
add("A_EN01_SCOPE","EN01",cases["EN01"].replace("evaluated only for arterial roads during weekday peak periods","evaluated particularly on arterial roads during weekday peak periods"),False)
add("A_EN02_INTERVAL","EN02",cases["EN02"].replace("every 15 minutes","every 30 minutes"),False)
add("A_EN03_CAUSAL","EN03",cases["EN03"].replace("reported a 12% decrease when messages were batched","demonstrated a 12% decrease due to message batching"),False)
add("A_EN03_MECHANISM_CONFLATION","EN03","Studies A, B, C, and D yielded contrasting findings regarding the impact of edge aggregation on latency and energy consumption. Study A reported lower latency after edge aggregation, whereas Study B observed no latency reduction under sparse traffic. Study C focused on energy consumption and reported a 12% decrease when messages were batched. Study D found that batching increased delay during emergency bursts. Together, these studies examine different operating conditions and should not be summarized as a single consistent effect.",False)
add("A_EN04_CIT_SWAP","EN04",cases["EN04"].replace("[CIT_SYN_01]","[TMP]").replace("[CIT_SYN_02]","[CIT_SYN_01]").replace("[TMP]","[CIT_SYN_02]"),False)
add("A_EN04_WEAKEN","EN04",cases["EN04"].replace("Adaptive signal timing reduced mean queue length","Adaptive signal timing was associated with a reduction in mean queue length"),False)
add("A_EN05_HEDGE","EN05",cases["EN05"].replace("may reflect","reflects"),False)
add("A_EN05_CAUSE","EN05",cases["EN05"].replace("does not establish that beacon density causes the reduction","establishes that beacon density causes the reduction"),False)
add("A_EN06_SWAP","EN06",cases["EN06"].replace("42.0 s","TMP").replace("51.5 s","42.0 s").replace("TMP","51.5 s"),False)
add("A_EN07_SEED","EN07",cases["EN07"].replace("seed 17","seed 19"),False)
add("A_EN08_CAUSE","EN08",cases["EN08"].replace("does not demonstrate that reducing occupancy will cause","demonstrates that reducing occupancy will cause"),False)
add("A_EN09_BIND","EN09",cases["EN09"].replace("U_i is utilization and D_i is normalized deadline pressure","U_i is normalized deadline pressure and D_i is utilization"),False)
add("A_EN10_RATE","EN10",cases["EN10"].replace("every 30 s","every 60 s"),False)
add("A_EN11_DUP","EN11",cases["EN11"].replace("rejects duplicate reports","accepts duplicate reports"),False)
add("A_EN12_RETUNE","EN12",cases["EN12"].replace("rather than from retuning the controller","because the controller is retuned"),False)

rows=[]
for name,cid,text,expect_pass in tests:
    got=validate(cid,cases[cid],text)["disposition"]
    ok=(got=="PASS_CANDIDATE") if expect_pass else (got!="PASS_CANDIDATE")
    rows.append({"test":name,"case_id":cid,"expected":"PASS_CANDIDATE" if expect_pass else "NOT_PASS","observed":got,"status":"PASS" if ok else "FAIL"})

out=ROOT/"AT0_EN_V2_2_VALIDATOR_TEST_RESULTS.json"
out.write_text(json.dumps({"total":len(rows),"passed":sum(r["status"]=="PASS" for r in rows),"failed":sum(r["status"]=="FAIL" for r in rows),"results":rows},indent=2)+"\n",encoding="utf-8")
print(out.read_text())
if any(r["status"]=="FAIL" for r in rows): raise SystemExit(1)
