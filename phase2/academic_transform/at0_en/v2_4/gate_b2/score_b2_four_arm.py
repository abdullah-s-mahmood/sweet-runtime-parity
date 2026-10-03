from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
B1=HERE.parent/"gate_b1"
A=HERE.parent/"gate_a"

PAIRS=B1/"B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
RAW=HERE/"B2_RAW_TEXT_PAIRS_V1.jsonl"
ALIGNER=B1/"b1_aligner.py"
BRIDGE=HERE/"b2_extraction_bridge.py"
EXTRACTOR=A/"source_assertion_extractor.py"
PROTOCOL=HERE/"B2_DEGRADATION_PROTOCOL_V1.md"
BRIDGE_CONTRACT=HERE/"B2_BRIDGE_CONTRACT_V1.md"

OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
DETAIL=OUT/"B2_FIRST_FOUR_ARM_DETAIL.jsonl"
SUMMARY=OUT/"B2_FIRST_FOUR_ARM_SUMMARY.json"
EXTRACTED=OUT/"B2_FIRST_EXTRACTED_GRAPHS.jsonl"

EXPECTED_ALIGNER_SHA="289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42"
EXPECTED_EXTRACTOR_SHA="32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1"
EXPECTED_PAIRS_SHA="29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca"
EXPECTED_RAW_SHA="afa733aa5e0498706df66acb7005fa7fff891ef39afe9e8b086a463fdf107395"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha(ALIGNER)==EXPECTED_ALIGNER_SHA
assert sha(EXTRACTOR)==EXPECTED_EXTRACTOR_SHA
assert sha(PAIRS)==EXPECTED_PAIRS_SHA
assert sha(RAW)==EXPECTED_RAW_SHA

spec=importlib.util.spec_from_file_location("b1",ALIGNER)
b1=importlib.util.module_from_spec(spec); spec.loader.exec_module(b1)

spec=importlib.util.spec_from_file_location("bridge",BRIDGE)
bridge=importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)

pairs={x["pair_id"]:x for x in rows(PAIRS)}
raws={x["pair_id"]:x for x in rows(RAW)}
assert set(pairs)==set(raws) and len(pairs)==12

ARM_NAMES=["GG","GE","EG","EE"]

def has_critical_uncertainty(graph):
    return any(
        a["criticality"]=="CRITICAL" and a["confidence_status"]!="CERTAIN"
        for a in graph["assertions"]
    ) or any(
        r["criticality"]=="CRITICAL" and r["confidence_status"]!="CERTAIN"
        for r in graph["relations"]
    )

def score_arm(records):
    total=len(records)
    correct=sum(x["predicted_outcome"]==x["expected_outcome"] for x in records)
    safe=[x for x in records if x["expected_outcome"]=="PASS_CANDIDATE"]
    adv=[x for x in records if x["expected_outcome"]=="REJECT"]
    rev=[x for x in records if x["expected_outcome"]=="REVIEW"]

    safe_accept=sum(x["predicted_outcome"]=="PASS_CANDIDATE" for x in safe)
    false_reject=sum(x["predicted_outcome"]=="REJECT" for x in safe)
    adv_accept=sum(x["predicted_outcome"]=="PASS_CANDIDATE" for x in adv)
    review_preserved=sum(x["predicted_outcome"]=="REVIEW" for x in rev)
    uncertainty_promoted=sum(
        x["predicted_outcome"]=="PASS_CANDIDATE" and x["has_critical_input_uncertainty"]
        for x in records
    )

    by_shape=collections.defaultdict(lambda:{"correct":0,"total":0})
    by_family=collections.defaultdict(lambda:{"correct":0,"total":0})
    for x in records:
        ok=x["predicted_outcome"]==x["expected_outcome"]
        by_shape[x["mapping_shape"]]["total"]+=1
        by_shape[x["mapping_shape"]]["correct"]+=int(ok)
        by_family[x["scenario_class"]]["total"]+=1
        by_family[x["scenario_class"]]["correct"]+=int(ok)

    return {
        "pair_count":total,
        "pair_correct":correct,
        "pair_accuracy":correct/total,
        "safe_total":len(safe),
        "safe_accept_count":safe_accept,
        "safe_accept_rate":safe_accept/len(safe),
        "faithful_false_rejection_count":false_reject,
        "adversarial_total":len(adv),
        "material_adversarial_acceptance_count":adv_accept,
        "adversarial_acceptance_rate":adv_accept/len(adv),
        "dangerous_critical_false_preserve_count":adv_accept,
        "review_total":len(rev),
        "review_preserved_count":review_preserved,
        "review_preservation_rate":review_preserved/len(rev) if rev else 1.0,
        "critical_uncertainty_promotion_count":uncertainty_promoted,
        "mapping_shape_performance":dict(by_shape),
        "scenario_performance":dict(by_family),
        "wrong_pair_ids":[x["pair_id"] for x in records if x["predicted_outcome"]!=x["expected_outcome"]],
    }

details=[]
extracted_rows=[]
invalid=[]
arm_records={x:[] for x in ARM_NAMES}

for pid in sorted(pairs):
    p=pairs[pid]; r=raws[pid]
    try:
        # Independent extractions. Candidate extraction receives only candidate text.
        es=bridge.extract_and_bridge(
            r["source_text"],
            f"{pid}-SRC",
            f"{pid}-EXTRACTED-SOURCE",
        )
        ec=bridge.extract_and_bridge(
            r["candidate_text"],
            f"{pid}-CAND",
            f"{pid}-EXTRACTED-CANDIDATE",
        )
        extracted_rows.append({
            "pair_id":pid,
            "source_graph":es,
            "candidate_graph":ec,
        })
    except Exception as exc:
        invalid.append({"pair_id":pid,"error":repr(exc)})
        continue

    arm_graphs={
        "GG":(p["source_graph"],p["candidate_graph"]),
        "GE":(p["source_graph"],ec),
        "EG":(es,p["candidate_graph"]),
        "EE":(es,ec),
    }

    per_pair={"pair_id":pid,"expected_outcome":p["expected_outcome"],"arms":{}}
    for arm,(sg,cg) in arm_graphs.items():
        pred=b1.align_pair({"pair_id":pid,"source_graph":sg,"candidate_graph":cg})
        rec={
            "pair_id":pid,
            "scenario_class":p["scenario_class"],
            "mapping_shape":p["mapping_shape"],
            "expected_outcome":p["expected_outcome"],
            "predicted_outcome":pred["predicted_outcome"],
            "has_critical_input_uncertainty":has_critical_uncertainty(sg) or has_critical_uncertainty(cg),
        }
        arm_records[arm].append(rec)
        per_pair["arms"][arm]={
            "predicted_outcome":pred["predicted_outcome"],
            "assertion_alignment":pred["assertion_alignment"],
            "relation_alignment":pred["relation_alignment"],
        }
    details.append(per_pair)

EXTRACTED.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in extracted_rows),encoding="utf-8")
DETAIL.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in details),encoding="utf-8")

if invalid:
    status="INVALID_B2_EVALUATION"
    metrics={arm:score_arm(arm_records[arm]) if arm_records[arm] else None for arm in ARM_NAMES}
else:
    metrics={arm:score_arm(arm_records[arm]) for arm in ARM_NAMES}
    gg=metrics["GG"]
    if not (
        gg["pair_accuracy"]==1.0
        and gg["safe_accept_rate"]==1.0
        and gg["material_adversarial_acceptance_count"]==0
        and gg["review_preservation_rate"]==1.0
    ):
        status="INVALID_B2_EVALUATION"
    else:
        ee=metrics["EE"]
        safety_ok=(
            ee["material_adversarial_acceptance_count"]==0
            and ee["dangerous_critical_false_preserve_count"]==0
            and ee["review_preservation_rate"]==1.0
            and ee["critical_uncertainty_promotion_count"]==0
        )
        usability_ok=(
            ee["safe_accept_rate"]>=0.80
            and ee["pair_accuracy"]>=11/12
            and ee["faithful_false_rejection_count"]<=1
        )
        if not safety_ok:
            status="FAIL_B2_SAFETY"
        elif not usability_ok:
            status="MIXED_B2_REPAIR_REQUIRED"
        else:
            status="PASS_B2_EXTRACTED_DEVELOPMENT"

def pp(a,b):
    return 100.0*(a-b)

degradation={}
if not invalid:
    gg=metrics["GG"]
    for arm in ["GE","EG","EE"]:
        m=metrics[arm]
        degradation[arm]={
            "pair_accuracy_pp_vs_GG":pp(m["pair_accuracy"],gg["pair_accuracy"]),
            "safe_accept_rate_pp_vs_GG":pp(m["safe_accept_rate"],gg["safe_accept_rate"]),
            "adversarial_acceptance_pp_vs_GG":pp(m["adversarial_acceptance_rate"],gg["adversarial_acceptance_rate"]),
            "review_preservation_pp_vs_GG":pp(m["review_preservation_rate"],gg["review_preservation_rate"]),
        }
    degradation["EE_interaction"]= {
        "pair_accuracy_pp_vs_GE":pp(metrics["EE"]["pair_accuracy"],metrics["GE"]["pair_accuracy"]),
        "pair_accuracy_pp_vs_EG":pp(metrics["EE"]["pair_accuracy"],metrics["EG"]["pair_accuracy"]),
        "safe_accept_rate_pp_vs_GE":pp(metrics["EE"]["safe_accept_rate"],metrics["GE"]["safe_accept_rate"]),
        "safe_accept_rate_pp_vs_EG":pp(metrics["EE"]["safe_accept_rate"],metrics["EG"]["safe_accept_rate"]),
    }

summary={
    "gate":"AT0_EN_V2_4_B2_EXTRACTED_GRAPH_DEGRADATION",
    "status":status,
    "development_only":True,
    "model_inference":False,
    "invalid_bridge_records":invalid,
    "arms":metrics,
    "degradation_percentage_points":degradation,
    "ee_hard_gates":{
        "material_adversarial_acceptance_zero": (not invalid and metrics["EE"]["material_adversarial_acceptance_count"]==0),
        "dangerous_critical_false_preserve_zero": (not invalid and metrics["EE"]["dangerous_critical_false_preserve_count"]==0),
        "ambiguous_pair_review_preserved": (not invalid and metrics["EE"]["review_preservation_rate"]==1.0),
        "critical_uncertainty_promotion_zero": (not invalid and metrics["EE"]["critical_uncertainty_promotion_count"]==0),
        "faithful_safe_acceptance_min_80": (not invalid and metrics["EE"]["safe_accept_rate"]>=0.80),
        "pair_accuracy_min_11_of_12": (not invalid and metrics["EE"]["pair_accuracy"]>=11/12),
        "faithful_false_rejection_max_1": (not invalid and metrics["EE"]["faithful_false_rejection_count"]<=1),
    },
    "hashes":{
        "aligner_sha256":sha(ALIGNER),
        "extractor_sha256":sha(EXTRACTOR),
        "bridge_sha256":sha(BRIDGE),
        "pairs_sha256":sha(PAIRS),
        "raw_pairs_sha256":sha(RAW),
        "protocol_sha256":sha(PROTOCOL),
        "bridge_contract_sha256":sha(BRIDGE_CONTRACT),
        "extracted_graphs_sha256":sha(EXTRACTED),
        "detail_sha256":sha(DETAIL),
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
