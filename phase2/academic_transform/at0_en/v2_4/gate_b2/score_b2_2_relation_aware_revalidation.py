from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import pathlib
import re

HERE=pathlib.Path(__file__).resolve().parent
B1=HERE.parent/"gate_b1"
GA=HERE.parent/"gate_a"

PAIRS=B1/"B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
RAW=HERE/"B2_RAW_TEXT_PAIRS_V1.jsonl"
ALIGNER=B1/"b1_aligner.py"
A1_PATH=GA/"source_anchor_extractor.py"
A2_PATH=GA/"source_assertion_extractor.py"
RA_PATH=HERE/"b2_2_relation_aware_extractor.py"
PROTOCOL=HERE/"B2_DEGRADATION_PROTOCOL_V1.md"
BOUNDARY=HERE/"B2_1_FINAL_REPAIR_BOUNDARY_V1.md"

OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
DETAIL=OUT/"B2_2_REVALIDATION_DETAIL.jsonl"
SUMMARY=OUT/"B2_2_REVALIDATION_SUMMARY.json"
EXTRACTED=OUT/"B2_2_REVALIDATION_GRAPHS.jsonl"
AUDIT=OUT/"B2_2_REPRESENTATION_AUDIT.jsonl"

EXPECTED_ALIGNER_SHA="289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42"
EXPECTED_A2_SHA="32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1"
EXPECTED_PAIRS_SHA="29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca"
EXPECTED_RAW_SHA="afa733aa5e0498706df66acb7005fa7fff891ef39afe9e8b086a463fdf107395"

def rows(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(ALIGNER)==EXPECTED_ALIGNER_SHA
assert sha(A2_PATH)==EXPECTED_A2_SHA
assert sha(PAIRS)==EXPECTED_PAIRS_SHA
assert sha(RAW)==EXPECTED_RAW_SHA

# Guard against development-label leakage into the extraction prototype.
ra_source=RA_PATH.read_text(encoding="utf-8")
for forbidden in [
    "B1-P01","B1-P02","B1-P03","B1-P04","B1-P05","B1-P06",
    "B1-P07","B1-P08","B1-P09","B1-P10","B1-P11","B1-P12",
    "expected_outcome","gold_alignment","gold_relation_alignment"
]:
    assert forbidden not in ra_source, forbidden

def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

b1=loadmod("b1",ALIGNER)
a1=loadmod("a1audit",A1_PATH)
ra=loadmod("ra",RA_PATH)

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

def a1_case(case_id,text):
    return {"case_id":case_id,"source_text":text,"source_sha256":hashlib.sha256(text.encode("utf-8")).hexdigest()}

def anchor_projection(graph):
    evidence={e["span_id"]:e for e in graph["evidence_spans"]}
    out=[]
    for a in graph["anchors"]:
        spans=[]
        for sid in a["evidence_span_ids"]:
            e=evidence[sid]
            spans.append((e["char_start"],e["char_end"],e["quote"]))
        out.append((
            a["anchor_type"],a["raw"],a["normalized"],a["quantity_kind"],tuple(spans)
        ))
    return out

def audit_extracted_graph(graph,text,side_id):
    failures=[]
    checks=0

    # Independent A1 rerun: the B2.2 wrapper must preserve the frozen deterministic anchors/provenance.
    direct=a1.build_anchor_graph(a1_case(side_id,text))
    embedded=graph["a2_graph"]
    checks+=1
    if anchor_projection(direct)!=anchor_projection(embedded):
        failures.append("A1_ANCHOR_OR_PROVENANCE_REGRESSION")

    assertion_ids={a["id"] for a in graph["assertions"]}

    for a in graph["assertions"]:
        checks+=1
        if a["evidence"] not in text:
            failures.append(f"ASSERTION_EVIDENCE_NOT_EXACT:{a['id']}")

        # Supported equation coefficient->variable bindings must be visibly present.
        if a["predicate"]=="DEFINE" and re.search(r"[A-Za-z]_[A-Za-z0-9]+\s*=",a["evidence"]):
            for k,v in a.get("bindings",{}).items():
                if re.fullmatch(r"[A-Za-z]_[A-Za-z0-9]+",str(k)):
                    checks+=1
                    if str(k) not in a["evidence"] or str(v) not in a["evidence"]:
                        failures.append(f"EQUATION_BINDING_UNSUPPORTED:{a['id']}:{k}->{v}")

        # Numeric owner/value bindings must have direct textual witnesses.
        if "value" in a.get("bindings",{}):
            checks+=1
            val=format(a["bindings"]["value"],"g") if isinstance(a["bindings"]["value"],float) else str(a["bindings"]["value"])
            if val not in a["evidence"]:
                failures.append(f"VALUE_BINDING_UNSUPPORTED:{a['id']}:{val}")

    for rel in graph["relations"]:
        checks+=1
        ev=rel["evidence"]
        if ev not in text:
            failures.append(f"RELATION_EVIDENCE_NOT_EXACT:{rel['id']}")

        if rel["type"]=="CITES":
            checks+=1
            if rel["from"] not in assertion_ids or not re.fullmatch(r"CIT_[A-Za-z0-9_]+",rel["to"]) or rel["to"] not in ev:
                failures.append(f"CITATION_RELATION_UNSUPPORTED:{rel['id']}")
        elif rel["type"]=="PRECEDES":
            checks+=1
            if rel["from"] not in assertion_ids or rel["to"] not in assertion_ids or "precedes" not in ev.lower():
                failures.append(f"PRECEDES_RELATION_UNSUPPORTED:{rel['id']}")
        elif rel["type"]=="DISTINCT_FROM":
            checks+=1
            if rel["from"] not in assertion_ids or rel["to"] not in assertion_ids or "different subsystems" not in ev.lower():
                failures.append(f"DISTINCT_RELATION_UNSUPPORTED:{rel['id']}")
        else:
            failures.append(f"UNAUDITED_RELATION_TYPE:{rel['type']}")

    return {
        "side_id":side_id,
        "checks":checks,
        "failures":failures,
        "pass":not failures,
        "assertion_count":len(graph["assertions"]),
        "relation_count":len(graph["relations"]),
        "a1_anchor_count":len(direct["anchors"]),
    }

def score_arm(records):
    total=len(records)
    correct=sum(r["predicted_outcome"]==r["expected_outcome"] for r in records)
    safe=[r for r in records if r["expected_outcome"]=="PASS_CANDIDATE"]
    adv=[r for r in records if r["expected_outcome"]=="REJECT"]
    rev=[r for r in records if r["expected_outcome"]=="REVIEW"]

    safe_accept=sum(r["predicted_outcome"]=="PASS_CANDIDATE" for r in safe)
    false_reject=sum(r["predicted_outcome"]=="REJECT" for r in safe)
    adv_accept=sum(r["predicted_outcome"]=="PASS_CANDIDATE" for r in adv)
    review_preserved=sum(r["predicted_outcome"]=="REVIEW" for r in rev)
    uncertainty_promoted=sum(
        r["predicted_outcome"]=="PASS_CANDIDATE" and r["has_critical_input_uncertainty"]
        for r in records
    )

    by_shape=collections.defaultdict(lambda:{"correct":0,"total":0})
    by_family=collections.defaultdict(lambda:{"correct":0,"total":0})
    for r in records:
        ok=r["predicted_outcome"]==r["expected_outcome"]
        by_shape[r["mapping_shape"]]["total"]+=1
        by_shape[r["mapping_shape"]]["correct"]+=int(ok)
        by_family[r["scenario_class"]]["total"]+=1
        by_family[r["scenario_class"]]["correct"]+=int(ok)

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
        "wrong_pair_ids":[r["pair_id"] for r in records if r["predicted_outcome"]!=r["expected_outcome"]],
    }

details=[]
graphs=[]
audits=[]
arm_records={arm:[] for arm in ARM_NAMES}
invalid=[]

for pid in sorted(pairs):
    p=pairs[pid]
    raw=raws[pid]
    try:
        source_ex=ra.relation_aware_extract(raw["source_text"],f"{pid}-SRC")
        cand_ex=ra.relation_aware_extract(raw["candidate_text"],f"{pid}-CAND")

        sa=audit_extracted_graph(source_ex,raw["source_text"],f"{pid}-SRC")
        ca=audit_extracted_graph(cand_ex,raw["candidate_text"],f"{pid}-CAND")
        audits.extend([sa,ca])
        if not sa["pass"] or not ca["pass"]:
            invalid.append({"pair_id":pid,"source_audit":sa,"candidate_audit":ca})

        graphs.append({
            "pair_id":pid,
            "source_graph":source_ex,
            "candidate_graph":cand_ex,
        })
    except Exception as exc:
        invalid.append({"pair_id":pid,"exception":repr(exc)})
        continue

    arm_graphs={
        "GG":(p["source_graph"],p["candidate_graph"]),
        "GE":(p["source_graph"],cand_ex),
        "EG":(source_ex,p["candidate_graph"]),
        "EE":(source_ex,cand_ex),
    }

    per={"pair_id":pid,"expected_outcome":p["expected_outcome"],"arms":{}}
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
        per["arms"][arm]={
            "predicted_outcome":pred["predicted_outcome"],
            "assertion_alignment":pred["assertion_alignment"],
            "relation_alignment":pred["relation_alignment"],
        }
    details.append(per)

EXTRACTED.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in graphs),encoding="utf-8")
DETAIL.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in details),encoding="utf-8")
AUDIT.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in audits),encoding="utf-8")

metrics={arm:(score_arm(arm_records[arm]) if arm_records[arm] else None) for arm in ARM_NAMES}
audit_checks=sum(a["checks"] for a in audits)
audit_failures=sum(len(a["failures"]) for a in audits)

if invalid or len(details)!=12:
    status="INVALID_B2_2_REVALIDATION"
else:
    gg=metrics["GG"]
    gg_ok=(
        gg["pair_accuracy"]==1.0
        and gg["safe_accept_rate"]==1.0
        and gg["material_adversarial_acceptance_count"]==0
        and gg["review_preservation_rate"]==1.0
    )
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
    if not gg_ok or audit_failures:
        status="INVALID_B2_2_REVALIDATION"
    elif not safety_ok:
        status="FAIL_B2_2_SAFETY"
    elif not usability_ok:
        status="MIXED_B2_2_REPAIR_REQUIRED"
    else:
        status="PASS_B2_EXTRACTED_DEVELOPMENT"

def pp(cur,base):
    return 100.0*(cur-base)

baseline={
    "GG":{"pair_accuracy":1.0,"safe_accept_rate":1.0,"adversarial_acceptance_rate":0.0},
    "GE":{"pair_accuracy":5/12,"safe_accept_rate":0.0,"adversarial_acceptance_rate":0.0},
    "EG":{"pair_accuracy":6/12,"safe_accept_rate":0.2,"adversarial_acceptance_rate":0.0},
    "EE":{"pair_accuracy":4/12,"safe_accept_rate":0.0,"adversarial_acceptance_rate":0.0},
}

delta={}
for arm in ARM_NAMES:
    if metrics[arm]:
        delta[arm]={
            "pair_accuracy_pp_vs_canonical_b2":pp(metrics[arm]["pair_accuracy"],baseline[arm]["pair_accuracy"]),
            "safe_accept_rate_pp_vs_canonical_b2":pp(metrics[arm]["safe_accept_rate"],baseline[arm]["safe_accept_rate"]),
            "adversarial_acceptance_pp_vs_canonical_b2":pp(metrics[arm]["adversarial_acceptance_rate"],baseline[arm]["adversarial_acceptance_rate"]),
        }

summary={
    "gate":"AT0_EN_V2_4_B2_2_RELATION_AWARE_REVALIDATION",
    "status":status,
    "development_only":True,
    "model_inference":False,
    "pair_count":len(details),
    "representation_audit":{
        "side_count":len(audits),
        "checks":audit_checks,
        "failures":audit_failures,
        "all_sides_pass":audit_failures==0 and len(audits)==24,
    },
    "arms":metrics,
    "delta_vs_canonical_b2_percentage_points":delta,
    "ee_progression_gates":{
        "adversarial_acceptance_zero":not invalid and metrics["EE"]["material_adversarial_acceptance_count"]==0,
        "dangerous_critical_false_preserve_zero":not invalid and metrics["EE"]["dangerous_critical_false_preserve_count"]==0,
        "critical_uncertainty_promotion_zero":not invalid and metrics["EE"]["critical_uncertainty_promotion_count"]==0,
        "ambiguous_pair_review_preserved":not invalid and metrics["EE"]["review_preservation_rate"]==1.0,
        "safe_acceptance_min_80":not invalid and metrics["EE"]["safe_accept_rate"]>=0.80,
        "pair_accuracy_min_11_of_12":not invalid and metrics["EE"]["pair_accuracy"]>=11/12,
        "faithful_false_rejection_max_1":not invalid and metrics["EE"]["faithful_false_rejection_count"]<=1,
        "gg_hard_gates_100":not invalid and metrics["GG"]["pair_accuracy"]==1.0,
        "representation_audit_clean":audit_failures==0 and len(audits)==24,
    },
    "strong_adoption_targets":{
        "extracted_graph_pair_accuracy":0.95,
        "authentic_safe_acceptance":0.90,
        "automatic_pass_selective_precision":0.99,
        "adversarial_automatic_acceptance":0.0,
        "critical_silent_errors":0,
    },
    "hashes":{
        "aligner_sha256":sha(ALIGNER),
        "a2_sha256":sha(A2_PATH),
        "relation_aware_extractor_sha256":sha(RA_PATH),
        "pairs_sha256":sha(PAIRS),
        "raw_pairs_sha256":sha(RAW),
        "protocol_sha256":sha(PROTOCOL),
        "repair_boundary_sha256":sha(BOUNDARY),
        "graphs_sha256":sha(EXTRACTED),
        "detail_sha256":sha(DETAIL),
        "audit_sha256":sha(AUDIT),
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
