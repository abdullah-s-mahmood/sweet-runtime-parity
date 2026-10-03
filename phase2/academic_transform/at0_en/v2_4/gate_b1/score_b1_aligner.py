from __future__ import annotations
import collections, hashlib, importlib.util, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
PAIRS=HERE/"B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
ALIGNER=HERE/"b1_aligner.py"
CONTRACT=HERE/"B1_SCORING_CONTRACT_V1.md"
OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
DETAIL=OUT/"B1_FIRST_SCORE_DETAIL.jsonl"
SUMMARY=OUT/"B1_FIRST_SCORE_SUMMARY.json"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

src=ALIGNER.read_text(encoding="utf-8")
assert "gold_alignment" not in src
assert "expected_outcome" not in src
assert "gold_relation_alignment" not in src

spec=importlib.util.spec_from_file_location("b1",ALIGNER)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

pairs=rows(PAIRS)
details=[]
pair_ok=0
critical_gold_total=0
critical_gold_covered=0
critical_status_total=0
critical_status_correct=0
dangerous_false_preserve=0
faithful_safe_rejection=0
material_adversarial_acceptance=0
uncertain_total=0
uncertain_correct=0
evidence_trace_complete=0
evidence_trace_total=0
shape_stats=collections.defaultdict(lambda:{"correct":0,"total":0})
family_stats=collections.defaultdict(lambda:{"correct":0,"total":0})

BAD={"ALTERED","CONTRADICTORY","OMITTED","NEW_INFORMATION"}

def key(m,relation=False):
    if relation:
        return (tuple(sorted(m.get("source_relation_ids",[]))),tuple(sorted(m.get("candidate_relation_ids",[]))))
    return (tuple(sorted(m.get("source_ids",[]))),tuple(sorted(m.get("candidate_ids",[]))))

for p in pairs:
    pred=mod.align_pair(p)
    outcome_ok=(pred["predicted_outcome"]==p["expected_outcome"])
    pair_ok+=int(outcome_ok)
    shape_stats[p["mapping_shape"]]["total"]+=1
    shape_stats[p["mapping_shape"]]["correct"]+=int(outcome_ok)
    family_stats[p["scenario_class"]]["total"]+=1
    family_stats[p["scenario_class"]]["correct"]+=int(outcome_ok)

    if p["expected_outcome"]=="PASS_CANDIDATE" and pred["predicted_outcome"]!="PASS_CANDIDATE":
        faithful_safe_rejection+=1
    if p["expected_outcome"]=="REJECT" and pred["predicted_outcome"]=="PASS_CANDIDATE":
        material_adversarial_acceptance+=1

    pred_a={key(x):x for x in pred["assertion_alignment"]}
    pred_r={key(x,True):x for x in pred["relation_alignment"]}

    assertion_rows=[]
    relation_rows=[]

    for g in p["gold_alignment"]:
        k=key(g)
        found=pred_a.get(k)
        if g["criticality"]=="CRITICAL":
            critical_gold_total+=1
            if found:
                critical_gold_covered+=1
                critical_status_total+=1
                critical_status_correct+=int(found["status"]==g["status"])
        if g["status"]=="UNCERTAIN":
            uncertain_total+=1
            uncertain_correct+=int(bool(found) and found["status"]=="UNCERTAIN")
        if found and found["status"]=="PRESERVED" and g["criticality"]=="CRITICAL" and g["status"] in BAD:
            dangerous_false_preserve+=1
        assertion_rows.append({
            "gold":g,
            "predicted":found,
            "mapping_found":bool(found),
            "status_correct":bool(found) and found["status"]==g["status"]
        })

    for g in p["gold_relation_alignment"]:
        k=key(g,True)
        found=pred_r.get(k)
        if g["criticality"]=="CRITICAL":
            critical_gold_total+=1
            if found:
                critical_gold_covered+=1
                critical_status_total+=1
                critical_status_correct+=int(found["status"]==g["status"])
        if g["status"]=="UNCERTAIN":
            uncertain_total+=1
            uncertain_correct+=int(bool(found) and found["status"]=="UNCERTAIN")
        if found and found["status"]=="PRESERVED" and g["criticality"]=="CRITICAL" and g["status"] in BAD:
            dangerous_false_preserve+=1
        relation_rows.append({
            "gold":g,
            "predicted":found,
            "mapping_found":bool(found),
            "status_correct":bool(found) and found["status"]==g["status"]
        })

    for x in pred["assertion_alignment"]+pred["relation_alignment"]:
        if x["criticality"]=="CRITICAL":
            evidence_trace_total+=1
            se=x.get("source_evidence",[])
            ce=x.get("candidate_evidence",[])
            ok=bool(se or x["status"]=="NEW_INFORMATION") and bool(ce or x["status"]=="OMITTED")
            evidence_trace_complete+=int(ok)

    details.append({
        "pair_id":p["pair_id"],
        "scenario_class":p["scenario_class"],
        "mapping_shape":p["mapping_shape"],
        "expected_outcome":p["expected_outcome"],
        "predicted_outcome":pred["predicted_outcome"],
        "outcome_correct":outcome_ok,
        "assertion_alignment":assertion_rows,
        "relation_alignment":relation_rows,
        "raw_prediction":pred
    })

pair_accuracy=pair_ok/len(pairs)
critical_coverage=critical_gold_covered/critical_gold_total if critical_gold_total else 1.0
critical_status_accuracy=critical_status_correct/critical_status_total if critical_status_total else 1.0
uncertainty_preservation=uncertain_correct/uncertain_total if uncertain_total else 1.0
evidence_trace_rate=evidence_trace_complete/evidence_trace_total if evidence_trace_total else 1.0

hard={
    "dangerous_false_preserve_zero":dangerous_false_preserve==0,
    "pair_outcome_accuracy_100":pair_accuracy==1.0,
    "critical_gold_alignment_coverage_100":critical_coverage==1.0,
    "critical_alignment_status_accuracy_100":critical_status_accuracy==1.0,
    "faithful_safe_pair_rejection_zero":faithful_safe_rejection==0,
    "material_adversarial_acceptance_zero":material_adversarial_acceptance==0,
    "critical_uncertainty_preservation_100":uncertainty_preservation==1.0,
    "critical_evidence_trace_completeness_100":evidence_trace_rate==1.0
}
status="PASS_B1_HUMAN_CORRECT" if all(hard.values()) else "FAIL_B1_HUMAN_CORRECT"

DETAIL.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in details),encoding="utf-8")
summary={
    "gate":"AT0_EN_V2_4_B1_HUMAN_CORRECT_ALIGNMENT",
    "status":status,
    "model_inference":False,
    "pair_count":len(pairs),
    "pair_outcome_correct":pair_ok,
    "pair_outcome_accuracy":pair_accuracy,
    "critical_gold_alignment_total":critical_gold_total,
    "critical_gold_alignment_covered":critical_gold_covered,
    "critical_gold_alignment_coverage":critical_coverage,
    "critical_alignment_status_accuracy":critical_status_accuracy,
    "dangerous_false_preserve_count":dangerous_false_preserve,
    "faithful_safe_pair_rejection_count":faithful_safe_rejection,
    "material_adversarial_acceptance_count":material_adversarial_acceptance,
    "critical_uncertainty_total":uncertain_total,
    "critical_uncertainty_preserved":uncertain_correct,
    "critical_uncertainty_preservation":uncertainty_preservation,
    "critical_evidence_trace_completeness":evidence_trace_rate,
    "mapping_shape_performance":dict(shape_stats),
    "scenario_performance":dict(family_stats),
    "hard_gates":hard,
    "hashes":{
        "aligner_sha256":sha(ALIGNER),
        "pairs_sha256":sha(PAIRS),
        "contract_sha256":sha(CONTRACT),
        "detail_sha256":sha(DETAIL)
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
