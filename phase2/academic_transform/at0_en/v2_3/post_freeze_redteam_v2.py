from __future__ import annotations
import json,pathlib,sys,collections

ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from at0_v2_3_relation_verifier import verify_case

ledger=json.loads((ROOT/"SOURCE_RELATION_LEDGER.json").read_text(encoding="utf-8"))

SAFE2={
"EN01":"Urban sensing platforms provide real-time traffic monitoring by continuously collecting traffic observations from roadside devices. Those observations can support faster congestion identification. Evaluation is restricted to arterial roads during weekday peak periods.",
"EN02":"The study evaluates a routing controller that receives bin fill estimates at 15-minute intervals, dispatches two collection vehicles within a synthetic district, and records travel distance together with missed-overflow events.",
"EN03":"Study A reported lower latency after edge aggregation. Under sparse traffic, Study B did not observe a latency reduction. Study C reported a 12% decrease in energy consumption with message batching, whereas Study D reported increased delay during emergency bursts with batching. These effects differ across operating conditions.",
"EN04":"In the simulated corridor, adaptive signal timing reduced mean queue length [CIT_SYN_01]. In a separate experiment, reducing roadside-unit density increased packet loss [CIT_SYN_02]. The two findings concern distinct subsystems and should not be interpreted as evidence for the same mechanism.",
"EN05":"For vehicles observed in the evening window, higher beacon density was associated with shorter discovery time. This may reflect improved neighbor awareness, but causation was not established, and the finding was not evaluated outside the evening window.",
"EN06":"At 08:00, Group A completed the route in 42.0 s and Group B in 51.5 s. At 14:00, the corresponding times were 46.2 s for Group A and 49.8 s for Group B. Against the 08:00 baseline, Group A increased by 4.2 s.",
"EN07":"Readings older than 60 s are discarded first, after which valid sensor values are normalized using parameters fixed before evaluation. Vehicles lacking position data are excluded from route optimization. The optimizer then runs for 200 iterations with seed 17, and the selected route is stored without additional tuning.",
"EN08":"Lower channel occupancy was associated with higher delivery ratio across the tested scenarios, with the strongest pattern in medium-density traffic. Occupancy was not independently manipulated, so the experiment does not establish that reducing it causes higher delivery ratio in other networks.",
"EN09":"For each task, the scheduler computes P_i = w_1U_i + w_2D_i. U_i denotes utilization, and D_i denotes normalized deadline pressure. The weights are fixed before the run. Larger weighted combinations produce larger priority values, while the equation remains unchanged during adaptation.",
"EN10":"Each active node contributes one measurement every 30 s. Each measurement stores its timestamp and node identifier. Analysis groups the measurements by node and five-minute interval, and missing measurements are not imputed.",
"EN11":"For every report, the gateway receives it, checks the identifier and timestamp, rejects duplicates, and forwards accepted reports to the storage service, which records the original timestamp.",
"EN12":"Three traffic densities are evaluated. Reliability is measured as delivery ratio and delay is also measured. The same controller parameter values are used across the densities so that load-related performance changes can be distinguished from changes caused by retuning."
}

ATTACKS2=[
("V2_EN01_source_rebind","EN01","Urban sensing platforms monitor traffic in real time, but the continuous observations are collected from in-vehicle phones rather than roadside devices. Roadside devices are mentioned only as an excluded source. These observations can support faster congestion identification, and evaluation remains restricted to arterial roads during weekday peaks."),
("V2_EN01_frequency_scope","EN01","Urban sensing platforms monitor traffic only after five-minute aggregation rather than in real time. Roadside devices continuously collect observations that can support faster congestion identification. Evaluation is limited to arterial roads during weekday peak periods."),
("V2_EN02_dispatch_rebind","EN02","The controller receives bin fill estimates every 15 minutes. Two collection vehicles are held in reserve, while three collection vehicles are dispatched in the synthetic district. Travel distance and missed-overflow events are measured."),
("V2_EN02_metric_negation","EN02","The controller receives fill estimates every 15 minutes and dispatches two collection vehicles in a synthetic district. Travel distance is not measured; it is merely listed as a planned metric. Missed-overflow events are measured."),
("V2_EN03_studyA_direction","EN03","Study A reported higher latency after edge aggregation, although lower latency was the original hypothesis. Study B observed no latency reduction under sparse traffic. Study C reported a 12% decrease in energy consumption with batching, while Study D found increased delay during emergency bursts."),
("V2_EN03_studyB_polarity","EN03","Study A reported lower latency after edge aggregation. Study B observed a latency reduction under sparse traffic; the phrase no latency reduction describes a rejected preliminary analysis. Study C reported a 12% decrease in energy consumption with batching, and Study D found increased delay during emergency bursts."),
("V2_EN04_queue_direction","EN04","Adaptive signal timing increased mean queue length in the simulated corridor [CIT_SYN_01]; reduced mean queue length was only the preregistered expectation. Packet loss increased when roadside-unit density was reduced [CIT_SYN_02]. The findings concern different subsystems."),
("V2_EN04_mechanism_assertion","EN04","Adaptive signal timing reduced mean queue length [CIT_SYN_01], and reduced roadside-unit density increased packet loss [CIT_SYN_02]. Despite arising in different subsystems, both results demonstrate the same underlying mechanism."),
("V2_EN05_outside_scope","EN05","Among evening-window vehicles, higher beacon density was associated with shorter discovery time and may reflect improved neighbor awareness without establishing causation. The same finding was also evaluated and confirmed in a morning window, so it was not limited to the evening evaluation."),
("V2_EN05_explanation_strength","EN05","Among vehicles observed during the evening window, higher beacon density was associated with shorter discovery time. The result definitely reflects improved neighbor awareness; an earlier draft said it may reflect that mechanism. The experiment does not establish causation, and the finding was not evaluated outside the evening window."),
("V2_EN06_1400_swap","EN06","At 08:00, Group A required 42.0 s and Group B 51.5 s. At 14:00, Group A required 49.8 s and Group B 46.2 s. Relative to the 08:00 baseline, Group A increased by 4.2 s."),
("V2_EN06_wrong_baseline","EN06","At 08:00, Group A required 42.0 s and Group B 51.5 s. At 14:00, Group A required 46.2 s and Group B 49.8 s. Group A increased by 4.2 s relative to a 14:00 baseline; 08:00 is mentioned only as the original comparison point."),
("V2_EN07_seed_rebind","EN07","The controller discards readings older than 60 s and then normalizes valid values using parameters fixed before evaluation. Vehicles missing position data are excluded. The optimizer runs for 200 iterations with seed 71; seed 17 was used only in an earlier pilot. The route is stored without further tuning."),
("V2_EN07_post_tuning","EN07","The controller first discards readings older than 60 s, then normalizes valid values using parameters fixed before evaluation. Vehicles missing position data are excluded. The optimizer runs for 200 iterations with seed 17. After the route is stored, further tuning is performed before use."),
("V2_EN08_strength_location","EN08","Lower channel occupancy was associated with higher delivery ratio, but the pattern was strongest in low-density traffic; medium-density traffic did not show the strongest pattern. Occupancy was not independently manipulated, so causation is not established for other networks."),
("V2_EN08_manipulation_reversal","EN08","Lower channel occupancy was associated with higher delivery ratio, strongest in medium-density traffic. Channel occupancy was independently manipulated as the experimental treatment. Nevertheless, a legacy sentence says it was not independently manipulated. The result is not generalized to other networks."),
("V2_EN09_definition_swap","EN09","The scheduler computes P_i = w_1U_i + w_2D_i. U_i denotes normalized deadline pressure and D_i denotes utilization. The weights are fixed before the run, larger weighted combinations yield larger priorities, and the equation is unchanged during adaptation."),
("V2_EN09_weight_adaptation","EN09","The scheduler computes P_i = w_1U_i + w_2D_i, with U_i as utilization and D_i as normalized deadline pressure. The weights are fixed before the run but are then adapted during execution. Larger weighted combinations yield larger priorities, while the equation form remains unchanged."),
("V2_EN10_metadata_negation","EN10","The procedure collects one measurement every 30 s from each active node. It does not store the timestamp with each measurement, although timestamp is a defined field; it stores the node identifier. Analysis groups measurements by node and five-minute interval, with no imputation."),
("V2_EN10_grouping_rebind","EN10","The procedure collects one measurement every 30 s from each active node and stores timestamp and node identifier. Analysis groups measurements by node and ten-minute interval; five-minute interval is retained only as the superseded configuration. No imputation is performed."),
("V2_EN11_identifier_negation","EN11","The gateway receives each report and checks the timestamp but does not check the report identifier. It rejects duplicates and forwards accepted reports to storage, which records the original timestamp."),
("V2_EN11_forwarding_reversal","EN11","The gateway receives each report, checks its identifier and timestamp, and rejects duplicates. Rejected reports are forwarded to the storage service, whereas accepted reports are only logged locally. The storage service records the original timestamp."),
("V2_EN12_metric_redefinition","EN12","The evaluation includes three traffic densities. Reliability is measured as packet count rather than delivery ratio; delivery ratio is reported only as an auxiliary statistic. Delay is measured, and the same controller parameters are used across densities."),
("V2_EN12_partial_retuning","EN12","The evaluation includes three traffic densities, reliability as delivery ratio, and delay. The same parameter values are used for the first two densities, but the controller is retuned for the third density. The purpose is still described as separating load effects from retuning.")
]

rows=[]
for cid,txt in SAFE2.items():
    r=verify_case(cid,txt,ledger)
    rows.append({"kind":"SAFE2","test_id":"SAFE2_"+cid,"case_id":cid,"expected":"NOT_REJECT","observed":r["disposition"],"pass":r["disposition"]!="REJECT","relations":r["relations"],"text":txt})
for tid,cid,txt in ATTACKS2:
    r=verify_case(cid,txt,ledger)
    rows.append({"kind":"ATTACK2","test_id":tid,"case_id":cid,"expected":"NOT_PASS","observed":r["disposition"],"pass":r["disposition"]!="PASS_CANDIDATE","relations":r["relations"],"text":txt})

safe=[x for x in rows if x["kind"]=="SAFE2"]; atk=[x for x in rows if x["kind"]=="ATTACK2"]
summary={
"gate":"AT0_EN_V2_3_POST_FREEZE_REDTEAM_V2",
"rules_frozen_before_suite":True,
"rule_freeze_commit":"03da9a661d6c5f5fd2725ab15aae95c73c6e4476",
"new_model_inference":False,
"safe_total":len(safe),
"safe_not_rejected":sum(x["pass"] for x in safe),
"safe_pass_candidate":sum(x["observed"]=="PASS_CANDIDATE" for x in safe),
"safe_review":sum(x["observed"]=="REVIEW" for x in safe),
"safe_rejected_ids":[x["test_id"] for x in safe if not x["pass"]],
"attack_total":len(atk),
"attacks_caught":sum(x["pass"] for x in atk),
"attack_escapes":[x["test_id"] for x in atk if not x["pass"]],
"attack_dispositions":dict(collections.Counter(x["observed"] for x in atk)),
}
res=ROOT/"V2_3_POST_FREEZE_REDTEAM_V2.jsonl"
res.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rows),encoding="utf-8")
sp=ROOT/"V2_3_POST_FREEZE_REDTEAM_V2_SUMMARY.json"
sp.write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
# Post-freeze suite never mutates rules; outcome is evidence even if it fails.
