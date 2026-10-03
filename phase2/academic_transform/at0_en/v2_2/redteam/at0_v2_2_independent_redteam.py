from __future__ import annotations
import json
import pathlib
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from at0_v2_2_validator import validate

CASES_PATH = pathlib.Path(__file__).resolve().parents[2] / "cases.jsonl"
CASES = {
    x["case_id"]: x
    for x in (
        json.loads(line)
        for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
}

SAFE = {
    "EN01": "Urban sensing platforms monitor traffic in real time by continuously collecting observations from roadside devices. These observations can support faster identification of congestion. This study evaluates the platform only on arterial roads during weekday peak periods.",
    "EN02": "This study evaluates a routing controller that receives bin fill estimates every 15 minutes, dispatches two collection vehicles in a synthetic district, and measures travel distance and missed-overflow events.",
    "EN03": "Study A reported lower latency after edge aggregation, whereas Study B observed no latency reduction under sparse traffic. Study C reported a 12% decrease in energy consumption when messages were batched, while Study D found that batching increased delay during emergency bursts. The findings arise under different operating conditions and are not uniformly consistent.",
    "EN04": "Adaptive signal timing reduced mean queue length in the simulated corridor [CIT_SYN_01]. A separate experiment found that packet loss increased when roadside-unit density was reduced [CIT_SYN_02]. The findings concern different subsystems and should not be treated as evidence for the same mechanism.",
    "EN05": "Among vehicles observed during the evening window, higher beacon density was associated with shorter discovery time. The result may reflect improved neighbor awareness, but the experiment does not establish that beacon density causes the reduction. The finding was not evaluated outside the evening window.",
    "EN06": "At 08:00, Group A completed the route in 42.0 s, compared with 51.5 s for Group B. At 14:00, Group A required 46.2 s, while Group B required 49.8 s. Relative to the 08:00 baseline, Group A's time increased by 4.2 s.",
    "EN07": "The controller first discards readings older than 60 s. It then normalizes valid sensor values using parameters fixed before evaluation. Vehicles with missing position data are excluded from route optimization. The optimizer runs for 200 iterations with seed 17, after which the selected route is stored without further tuning.",
    "EN08": "Across the tested scenarios, lower channel occupancy was associated with higher delivery ratio, and the association was strongest in medium-density traffic. Because channel occupancy was not independently manipulated, the result does not establish a causal conclusion or generalize to other networks.",
    "EN09": "The scheduler computes P_i = w_1U_i + w_2D_i for every task i. U_i represents utilization and D_i represents normalized deadline pressure. The weights are fixed before the run, and the equation remains unchanged during adaptation.",
    "EN10": "The procedure collects one measurement every 30 s from each active node and stores the timestamp and node identifier with every measurement. The analysis groups measurements by node and five-minute interval. No imputation is performed for missing measurements.",
    "EN11": "The gateway receives each report, checks its identifier and timestamp, rejects duplicate reports, and forwards accepted reports to the storage service. The storage service records the original timestamp.",
    "EN12": "The evaluation includes three traffic densities. Reliability is measured as delivery ratio, and delay is also measured. The controller uses the same parameter values across all densities to determine whether performance changes occur under different loads rather than because of controller retuning.",
}

ATTACKS = [
    # EN01 — scope and modality.
    ("EN01_scope_negation", "EN01",
     "Urban sensing platforms monitor traffic in real time using continuous observations from roadside devices, which can support faster congestion identification. This study evaluates not only arterial roads during weekday peak periods but also local roads and off-peak periods."),
    ("EN01_modal_strengthening", "EN01",
     "Urban sensing platforms monitor traffic in real time through continuous observations from roadside devices. These observations identify congestion faster. This study evaluates the platform only on arterial roads during weekday peak periods."),

    # EN02 — relation binding, not lexical presence.
    ("EN02_interval_decoy", "EN02",
     "The controller receives bin fill estimates every 30 minutes and dispatches two collection vehicles in a synthetic district. A separate 15-minute logging interval is used for diagnostics. Travel distance and missed-overflow events are measured."),
    ("EN02_vehicle_count_decoy", "EN02",
     "The controller receives bin fill estimates every 15 minutes and dispatches three collection vehicles in a synthetic district. The phrase two collection vehicles refers only to an earlier pilot configuration. Travel distance and missed-overflow events are measured."),

    # EN03 — direction and mechanism binding.
    ("EN03_energy_direction", "EN03",
     "Study A reported lower latency after edge aggregation, whereas Study B observed no latency reduction under sparse traffic. Study C reported a 12% increase in energy consumption when messages were batched. Study D found that batching increased delay during emergency bursts. These studies cover different operating conditions and are not uniformly consistent."),
    ("EN03_mechanism_conflation", "EN03",
     "Studies A, B, C, and D describe the impact of edge aggregation on latency and energy consumption. Study A reported lower latency after edge aggregation, Study B observed no latency reduction under sparse traffic, Study C reported a 12% decrease in energy consumption when messages were batched, and Study D found increased delay during emergency bursts when batching was used. The effects are not uniformly consistent across operating conditions."),

    # EN04 — citation binding and same-mechanism contradiction.
    ("EN04_citation_swap_same_sentence", "EN04",
     "Adaptive signal timing reduced mean queue length in the simulated corridor [CIT_SYN_02], while packet loss increased when roadside-unit density was reduced [CIT_SYN_01]. These findings concern different subsystems and should not be treated as evidence for the same mechanism."),
    ("EN04_same_mechanism_contradiction", "EN04",
     "Adaptive signal timing reduced mean queue length in the simulated corridor [CIT_SYN_01]. Packet loss increased when roadside-unit density was reduced [CIT_SYN_02]. Although these findings concern different subsystems, they should be treated as evidence for the same mechanism."),

    # EN05 — direction and contradiction under retained negation words.
    ("EN05_direction_decoy", "EN05",
     "Among vehicles observed during the evening window, higher beacon density was associated with longer discovery time; a prior hypothesis had predicted shorter discovery time. The result may reflect improved neighbor awareness, but the experiment does not establish causation. The finding was not evaluated outside the evening window."),
    ("EN05_causality_contradiction", "EN05",
     "Among vehicles observed during the evening window, higher beacon density was associated with shorter discovery time. The result may reflect improved neighbor awareness. Contrary to the statement that the experiment does not establish that beacon density causes the reduction, the experiment establishes that causal relationship. The finding was not evaluated outside the evening window."),

    # EN06 — direction and relation binding under lexical decoys.
    ("EN06_delta_negated", "EN06",
     "At 08:00, Group A required 42.0 s and Group B 51.5 s. At 14:00, Group A required 46.2 s and Group B 49.8 s. Relative to the 08:00 baseline, Group A decreased by 4.2 s; it did not increase by 4.2 s."),
    ("EN06_group_swap_decoy", "EN06",
     "At 08:00, the reported result assigns 51.5 s to Group A and 42.0 s to Group B; the labels '42.0 s for Group A' and '51.5 s for Group B' appear only in a legend. At 14:00, Group A required 46.2 s and Group B 49.8 s. Relative to the 08:00 baseline, Group A increased by 4.2 s."),

    # EN07 — order and exclusion contradiction.
    ("EN07_order_reversal", "EN07",
     "The controller first normalizes valid sensor values using parameters fixed before evaluation and then discards readings older than 60 s. Vehicles with missing position data are excluded from route optimization. The optimizer runs for 200 iterations with seed 17, after which the route is stored without further tuning."),
    ("EN07_exclusion_negation", "EN07",
     "The controller first discards readings older than 60 s and then normalizes valid values using parameters fixed before evaluation. Vehicles with missing position data are not excluded from route optimization; saying they are excluded from route optimization is incorrect. The optimizer runs for 200 iterations with seed 17, after which the route is stored without further tuning."),

    # EN08 — association direction and explicit causal contradiction.
    ("EN08_direction_reversal", "EN08",
     "Across the tested scenarios, higher channel occupancy was associated with higher delivery ratio. This pattern was strongest in medium-density traffic. Channel occupancy was not independently manipulated, and the result does not establish a causal conclusion or generalize to other networks."),
    ("EN08_causality_contradiction", "EN08",
     "Across the tested scenarios, lower channel occupancy was associated with higher delivery ratio, strongest in medium-density traffic. Although channel occupancy was not independently manipulated and the text says the result does not demonstrate causation, the experiment demonstrates that reducing occupancy will cause higher delivery ratio in other networks."),

    # EN09 — exact equation identity and comparison direction.
    ("EN09_operator_change", "EN09",
     "The scheduler computes P_i = w_1U_i - w_2D_i for every task i. U_i represents utilization and D_i represents normalized deadline pressure. The weights are fixed before the run, and this equation remains unchanged during adaptation."),
    ("EN09_priority_direction", "EN09",
     "The scheduler computes P_i = w_1U_i + w_2D_i for every task i. U_i represents utilization and D_i represents normalized deadline pressure. The weights are fixed before the run. A task obtains a larger priority when the weighted combination becomes smaller; the equation remains unchanged during adaptation."),

    # EN10 — measurement-rate binding and imputation contradiction.
    ("EN10_rate_decoy", "EN10",
     "The procedure collects one measurement every 60 s from each active node; 30 s is only the timestamp resolution. It stores the timestamp and node identifier with every measurement, groups measurements by node and five-minute interval, and performs no imputation for missing measurements."),
    ("EN10_imputation_contradiction", "EN10",
     "The procedure collects one measurement every 30 s from each active node and stores the timestamp and node identifier. The analysis groups measurements by node and five-minute interval. The statement 'No imputation is performed' is no longer true because missing measurements are imputed."),

    # EN11 — negation of duplicate rejection and timestamp retention.
    ("EN11_duplicate_negation", "EN11",
     "The gateway receives each report, checks the report identifier and timestamp, and does not reject duplicate reports; the phrase 'rejects duplicate reports' describes the previous design. Accepted reports are forwarded to storage, which records the original timestamp."),
    ("EN11_timestamp_negation", "EN11",
     "The gateway receives each report, checks its identifier and timestamp, rejects duplicates, and forwards accepted reports to storage. The storage service does not record the original timestamp; the requirement to record the original timestamp was removed."),

    # EN12 — parameter and metric negation.
    ("EN12_parameter_negation", "EN12",
     "The evaluation includes three traffic densities, with reliability measured as delivery ratio and delay measured. It is false that the controller uses the same parameter values across all densities: the controller is retuned for each density. The same parameter values phrase is retained only for comparison, rather than from retuning the controller."),
    ("EN12_delay_negation", "EN12",
     "The evaluation includes three traffic densities. Reliability is measured as delivery ratio, but delay is not measured. The controller uses the same parameter values across all densities to determine whether performance changes arise under different loads rather than from retuning the controller."),
]

def run():
    rows = []
    for case_id, text in SAFE.items():
        src = CASES[case_id]["source_text"]
        result = validate(case_id, src, text)
        rows.append({
            "kind": "SAFE_CONTROL",
            "test_id": f"SAFE_{case_id}",
            "case_id": case_id,
            "expected": "PASS_CANDIDATE",
            "observed": result["disposition"],
            "escaped": False,
            "false_positive": result["disposition"] != "PASS_CANDIDATE",
            "findings": result["findings"],
            "text": text,
        })

    for test_id, case_id, text in ATTACKS:
        src = CASES[case_id]["source_text"]
        result = validate(case_id, src, text)
        rows.append({
            "kind": "ADVERSARIAL",
            "test_id": test_id,
            "case_id": case_id,
            "expected": "NOT_PASS",
            "observed": result["disposition"],
            "escaped": result["disposition"] == "PASS_CANDIDATE",
            "false_positive": False,
            "findings": result["findings"],
            "text": text,
        })

    safe = [r for r in rows if r["kind"] == "SAFE_CONTROL"]
    attacks = [r for r in rows if r["kind"] == "ADVERSARIAL"]
    summary = {
        "gate": "AT0_EN_V2_2_INDEPENDENT_REDTEAM_V1",
        "new_model_inference": False,
        "safe_controls": len(safe),
        "safe_controls_pass_candidate": sum(r["observed"] == "PASS_CANDIDATE" for r in safe),
        "safe_control_false_positives": sum(r["false_positive"] for r in safe),
        "adversarial_tests": len(attacks),
        "adversarial_caught_not_pass": sum(r["observed"] != "PASS_CANDIDATE" for r in attacks),
        "adversarial_escaped_pass_candidate": sum(r["escaped"] for r in attacks),
        "escape_rate_on_constructed_attacks": (
            sum(r["escaped"] for r in attacks) / len(attacks) if attacks else None
        ),
        "observed_dispositions": dict(Counter(r["observed"] for r in rows)),
        "escaped_test_ids": [r["test_id"] for r in attacks if r["escaped"]],
        "safe_false_positive_ids": [r["test_id"] for r in safe if r["false_positive"]],
    }

    out_dir = pathlib.Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    detail_path = out_dir / "AT0_EN_V2_2_INDEPENDENT_REDTEAM_V1.jsonl"
    summary_path = out_dir / "AT0_EN_V2_2_INDEPENDENT_REDTEAM_V1_SUMMARY.json"
    detail_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows),
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    run()
