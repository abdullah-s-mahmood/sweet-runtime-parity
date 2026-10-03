from __future__ import annotations
import json, pathlib, sys
from collections import Counter

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from at0_v2_3_assertion_graph import validate
sys.path.insert(0,str(ROOT.parent/"v2_2"/"redteam"))
from at0_v2_2_independent_redteam import CASES

SAFE={
"EN01":"Real-time traffic monitoring is performed by urban sensing platforms that continuously acquire observations from roadside devices. Such observations may help identify congestion sooner. Evaluation was confined to arterial roads in weekday peak periods.",
"EN02":"The routing controller ingests bin-fill estimates at 15-minute intervals, dispatches two collection vehicles in a synthetic district, and records travel distance together with missed-overflow events.",
"EN03":"Study A observed reduced latency after edge aggregation, but Study B found no latency reduction under sparse traffic. Study C reported a 12% reduction in energy consumption with message batching, whereas Study D reported increased delay during emergency bursts when batching was used. The evidence therefore varies across operating conditions.",
"EN04":"Mean queue length was reduced by adaptive signal timing in the simulated corridor [CIT_SYN_01]. Packet loss rose when roadside-unit density was lowered in a separate experiment [CIT_SYN_02]. The two results concern distinct subsystems and do not establish one common mechanism.",
"EN05":"Within the evening-window vehicles, greater beacon density correlated with reduced discovery time. This may reflect better neighbor awareness, but causation is not established, and the finding was not tested outside the evening window.",
"EN06":"At 08:00, Group A took 42.0 s and Group B took 51.5 s. At 14:00, Group A took 46.2 s and Group B took 49.8 s. Relative to the 08:00 baseline, Group A's route time rose by 4.2 s.",
"EN07":"Readings more than 60 s old are discarded first. Valid values are then normalized using parameters fixed prior to evaluation. Vehicles lacking position data are excluded from route optimization. The optimizer executes 200 iterations using seed 17, and the selected route is stored without additional tuning.",
"EN08":"Lower channel occupancy correlated with a higher delivery ratio across the tested scenarios, with the strongest relationship in medium-density traffic. Occupancy was not manipulated independently, so the experiment does not establish that lowering occupancy causes a higher delivery ratio in other networks.",
"EN09":"For every task i, the scheduler computes P_i = w_1U_i + w_2D_i. U_i denotes utilization, while D_i denotes normalized deadline pressure. The weights are fixed before the run. Priority becomes larger only when the weighted combination becomes larger, and the equation is not modified during adaptation.",
"EN10":"Each active node contributes one measurement at 30-s intervals, with a timestamp and node identifier stored for every measurement. Analysis groups measurements by node and five-minute window. Missing measurements are not imputed.",
"EN11":"The gateway receives every report, verifies its identifier and timestamp, filters out duplicate reports, and sends accepted reports to storage. The storage service preserves the original timestamp.",
"EN12":"Three traffic-density conditions are evaluated. Reliability is quantified by delivery ratio, and delay is measured as well. Controller parameters remain identical across densities so load-related changes can be distinguished from changes caused by retuning."
}

ATTACKS=[
("H_EN01_scope_synonym","EN01","Urban sensing platforms monitor traffic in real time using continuous roadside observations that can support faster congestion identification. Evaluation covers arterial roads during weekday peaks and also collector roads at midday."),
("H_EN02_vehicle_synonym","EN02","The routing controller receives bin fill estimates every 15 minutes and dispatches three collection trucks in a synthetic district. The older phrase 'two collection vehicles' is retained only for comparison. Travel distance and missed-overflow events are measured."),
("H_EN03_B_decoy","EN03","Study A reported lower latency after edge aggregation. Study B reported a latency reduction under sparse traffic, although the phrase 'no latency reduction under sparse traffic' appeared in the preregistered hypothesis. Study C reported a 12% decrease in energy consumption when messages were batched, and Study D found increased delay during emergency bursts. The effects vary across conditions."),
("H_EN04_citation_reassignment","EN04","Adaptive signal timing reduced mean queue length in the corridor [CIT_SYN_01], and lower roadside-unit density increased packet loss [CIT_SYN_02]. A later sentence reassigns the evidence: [CIT_SYN_01] should support the packet-loss claim and [CIT_SYN_02] the queue-length claim. The findings concern different subsystems."),
("H_EN05_direction_synonym","EN05","During the evening window, higher beacon density was associated with greater discovery time, while an earlier expectation mentioned shorter discovery time. The effect may reflect neighbor awareness, does not establish causation, and was not evaluated outside the evening window."),
("H_EN06_worded_swap","EN06","At 08:00, Group A required fifty-one point five seconds and Group B required forty-two seconds; the numeric labels 42.0 and 51.5 are shown only as legend values. At 14:00, Group A required 46.2 s and Group B 49.8 s. Relative to the 08:00 baseline, Group A increased by 4.2 s."),
("H_EN07_order_paraphrase","EN07","Valid sensor values are normalized using pre-fixed parameters before stale readings older than 60 s are discarded. Vehicles with missing positions are excluded. The optimizer runs 200 iterations with seed 17 and stores the route without further tuning."),
("H_EN08_direction_paraphrase","EN08","Across the scenarios, decreases in channel occupancy coincided with decreases in delivery ratio. The pattern was strongest in medium-density traffic. Occupancy was not independently manipulated, and no causal conclusion is claimed for other networks."),
("H_EN09_operator_unicode","EN09","The scheduler computes P_i = w_1U_i − w_2D_i for every task i. U_i denotes utilization and D_i denotes normalized deadline pressure. The weights are fixed before the run. Larger weighted combinations produce larger priorities, and the equation remains unchanged during adaptation."),
("H_EN10_imputation_synonym","EN10","The procedure collects one measurement every 30 s from each active node and stores its timestamp and node identifier. Analysis groups data by node and five-minute interval. The protocol states that no imputation is performed; nevertheless, missing values are filled synthetically before analysis."),
("H_EN11_duplicate_synonym","EN11","The gateway receives every report, checks its identifier and timestamp, retains duplicate reports rather than discarding them, and forwards accepted reports to storage. Storage records the original timestamp."),
("H_EN12_retune_synonym","EN12","The evaluation includes three traffic densities. Reliability is measured as delivery ratio and delay is measured. The text says parameter values are the same across densities, but the controller is recalibrated separately for each density to optimize performance.")
]

rows=[]
for cid,text in SAFE.items():
    result=validate(cid,CASES[cid]["source_text"],text)
    rows.append({"kind":"SAFE_HOLDOUT","test_id":"SAFE2_"+cid,"case_id":cid,"expected":"PASS_CANDIDATE","observed":result["disposition"],"status":"PASS" if result["disposition"]=="PASS_CANDIDATE" else "FAIL","findings":result["findings"],"text":text})
for tid,cid,text in ATTACKS:
    result=validate(cid,CASES[cid]["source_text"],text)
    rows.append({"kind":"ADVERSARIAL_HOLDOUT","test_id":tid,"case_id":cid,"expected":"NOT_PASS","observed":result["disposition"],"status":"PASS" if result["disposition"]!="PASS_CANDIDATE" else "FAIL","findings":result["findings"],"text":text})

safe=[r for r in rows if r["kind"]=="SAFE_HOLDOUT"]
atk=[r for r in rows if r["kind"]=="ADVERSARIAL_HOLDOUT"]
summary={
"gate":"AT0_EN_V2_3_UNSEEN_HOLDOUT_V1",
"new_model_inference":False,
"verifier_frozen_before_holdout":True,
"safe_total":len(safe),
"safe_pass":sum(r["status"]=="PASS" for r in safe),
"safe_false_positive":sum(r["status"]=="FAIL" for r in safe),
"attacks_total":len(atk),
"attacks_caught":sum(r["status"]=="PASS" for r in atk),
"attacks_escaped":sum(r["status"]=="FAIL" for r in atk),
"escape_rate":sum(r["status"]=="FAIL" for r in atk)/len(atk),
"observed_dispositions":dict(Counter(r["observed"] for r in rows)),
"failed_ids":[r["test_id"] for r in rows if r["status"]=="FAIL"]
}
out=ROOT/"results"; out.mkdir(exist_ok=True)
(out/"AT0_EN_V2_3_UNSEEN_HOLDOUT_V1.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
(out/"AT0_EN_V2_3_UNSEEN_HOLDOUT_V1_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True))
