"""Development evaluator for the gold-independent acceptance gate.

IMPORTANT: unlike run_independent_acceptance_gate.py, this evaluator DOES read
existing human development adjudication labels, but only AFTER runtime decisions
have already been materialized. It never changes those decisions.
"""
from __future__ import annotations

import collections
import json
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
RUNTIME=ART/"INDEPENDENT_ACCEPTANCE_RUNTIME.json"
SURG_LABELS=ROOT/"PHASE2_SURGICAL_APPLIED_EDIT_ADJUDICATION.jsonl"
NORM_LABELS=ROOT/"PHASE2_NORMALIZED_CANDIDATE_ADJUDICATION.jsonl"


def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def canonical_class(stream,row):
    if stream=="SURGICAL":
        c=row["classification"]
    else:
        c=row["candidate_class"]
    if c in ("SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"):
        return "SUPPORTED"
    if c=="PARTIAL_CORRECTION":
        return "PARTIAL"
    if c=="WRONG_CORRECTION":
        return "WRONG"
    if c=="UNNECESSARY_EDIT":
        return "UNNECESSARY"
    if c=="REVIEW_REQUIRED":
        return "REVIEW_REQUIRED"
    return c


def label_maps():
    surg={}
    for x in read_jsonl(SURG_LABELS):
        cid=f"SURG-{int(x['passage_id'])}-{int(x['edit_index'])}"
        surg[cid]={
            "class":canonical_class("SURGICAL",x),
            "raw_class":x["classification"],
            "severity":x.get("severity"),
        }
    norm={}
    for x in read_jsonl(NORM_LABELS):
        norm[x["candidate_id"]]={
            "class":canonical_class("NORMALIZED",x),
            "raw_class":x["candidate_class"],
            "severity":None,
        }
    assert len(surg)==60 and len(norm)==19
    return {**surg,**norm}


def bootstrap_precision(rows,policy,B=4000):
    accepted=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT"]
    if not accepted:
        return None
    pids=sorted({x["passage_id"] for x in rows})
    by=collections.defaultdict(list)
    for x in rows: by[x["passage_id"]].append(x)
    rng=random.Random(20260928)
    vals=[]
    for _ in range(B):
        sample=[]
        for _ in pids:
            pid=rng.choice(pids)
            sample.extend(y for y in by[pid] if y["runtime_decisions"][policy]=="ACCEPT")
        if not sample:
            continue
        vals.append(sum(y["label"]["class"]=="SUPPORTED" for y in sample)/len(sample))
    vals.sort()
    if not vals: return None
    return [vals[int(.025*(len(vals)-1))],vals[int(.975*(len(vals)-1))]]


def summarize(rows,policy):
    acc=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT"]
    rev=[x for x in rows if x["runtime_decisions"][policy]=="REVIEW"]
    rej=[x for x in rows if x["runtime_decisions"][policy]=="REJECT"]
    cc=collections.Counter(x["label"]["class"] for x in acc)
    supported=cc["SUPPORTED"]
    known_bad=sum(
        x["label"]["class"]=="WRONG" and x["label"].get("severity") in ("HIGH","CRITICAL")
        for x in acc
    )
    all_supported=sum(x["label"]["class"]=="SUPPORTED" for x in rows)
    return {
        "policy":policy,
        "accepted":len(acc),
        "review":len(rev),
        "rejected":len(rej),
        "accepted_classes":dict(cc),
        "supported_precision":supported/len(acc) if acc else None,
        "supported_coverage":supported/all_supported if all_supported else None,
        "accepted_wrong_high_or_critical":known_bad,
        "accepted_candidate_ids":[x["candidate_id"] for x in acc],
        "passages_with_accept":len({x["passage_id"] for x in acc}),
        "passage_cluster_bootstrap_95_precision":bootstrap_precision(rows,policy),
    }


def stream_summary(rows,policy,stream):
    a=[x for x in rows if x["stream"]==stream and x["runtime_decisions"][policy]=="ACCEPT"]
    cc=collections.Counter(x["label"]["class"] for x in a)
    return {
        "stream":stream,
        "accepted":len(a),
        "classes":dict(cc),
        "supported_precision":cc["SUPPORTED"]/len(a) if a else None,
    }


def main():
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    labels=label_maps()
    rows=[]
    for x in runtime["rows"]:
        y=dict(x)
        y["label"]=labels[y["candidate_id"]]
        rows.append(y)
    assert len(rows)==79

    policies=list(runtime["policy_definitions"])
    summaries={p:summarize(rows,p) for p in policies}
    streams={p:{
        "SURGICAL":stream_summary(rows,p,"SURGICAL"),
        "NORMALIZED":stream_summary(rows,p,"NORMALIZED"),
    } for p in policies}

    counter_ids=["NORM-38-24-0","NORM-21-9-0","NORM-63-11-0"]
    counter=[]
    for cid in counter_ids:
        x=next(r for r in rows if r["candidate_id"]==cid)
        counter.append({
            "candidate_id":cid,
            "source_word":x["source_word"],
            "candidate_result_word":x["candidate_result_word"],
            "label":x["label"],
            "arabart":x["arabart"],
            "ged":x["ged"],
            "veto_reasons":x["veto_reasons"],
            "runtime_decisions":x["runtime_decisions"],
            "direct_patch":x.get("direct_patch"),
            "morph":x.get("morph"),
        })

    # Baselines from already-fixed runtime-observable signals.
    op_rows=[x for x in rows if x["stream"]=="SURGICAL" and x["operation_aware"]]
    op_cc=collections.Counter(x["label"]["class"] for x in op_rows)
    direct_rows=[x for x in rows if x["stream"]=="NORMALIZED" and x.get("direct_patch") and not x["veto_reasons"]]
    direct_cc=collections.Counter(x["label"]["class"] for x in direct_rows)

    result={
        "status":"PHASE2_INDEPENDENT_ACCEPTANCE_DEVELOPMENT_EVALUATED",
        "runtime_gate_status":runtime["status"],
        "candidate_rows":79,
        "passages":len({x["passage_id"] for x in rows}),
        "labels_loaded_only_after_runtime_decisions":True,
        "policy_results":summaries,
        "stream_results":streams,
        "baselines":{
            "SURGICAL_OPERATION_AWARE":{
                "selected":len(op_rows),
                "classes":dict(op_cc),
                "supported_precision":op_cc["SUPPORTED"]/len(op_rows) if op_rows else None,
            },
            "NORMALIZED_DIRECT_PATCH":{
                "selected":len(direct_rows),
                "classes":dict(direct_cc),
                "supported_precision":direct_cc["SUPPORTED"]/len(direct_rows) if direct_rows else None,
            },
        },
        "known_counterexamples":counter,
        "feature_diagnostics":{
            "arabart_normalized_agreement_supported":sum(x["arabart"]["normalized_local_agreement"] and x["label"]["class"]=="SUPPORTED" for x in rows),
            "arabart_normalized_agreement_wrong":sum(x["arabart"]["normalized_local_agreement"] and x["label"]["class"]=="WRONG" for x in rows),
            "arabart_exact_agreement_supported":sum(x["arabart"]["exact_local_agreement"] and x["label"]["class"]=="SUPPORTED" for x in rows),
            "arabart_exact_agreement_wrong":sum(x["arabart"]["exact_local_agreement"] and x["label"]["class"]=="WRONG" for x in rows),
            "veto_supported":sum(bool(x["veto_reasons"]) and x["label"]["class"]=="SUPPORTED" for x in rows),
            "veto_wrong":sum(bool(x["veto_reasons"]) and x["label"]["class"]=="WRONG" for x in rows),
        },
        "limitations":[
            "All precision/coverage figures are retrospective development estimates using existing same-agent adjudication labels.",
            "The policies themselves were materialized before labels were loaded, but the development population has been repeatedly inspected.",
            "AraBART source-local alignment is coarse and must be improved before a frozen/sealed evaluation.",
            "Passage clustering makes candidate-level independence invalid; clustered bootstrap is diagnostic only.",
        ],
    }

    ART.mkdir(parents=True,exist_ok=True)
    (ART/"INDEPENDENT_ACCEPTANCE_EVALUATION.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"PHASE2_INDEPENDENT_ACCEPTANCE_RESULTS.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"PHASE2_INDEPENDENT_ACCEPTANCE_COUNTEREXAMPLES.json").write_text(json.dumps(counter,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print(json.dumps({
        "status":result["status"],
        "policy_results":summaries,
        "baselines":result["baselines"],
        "feature_diagnostics":result["feature_diagnostics"],
        "known_counterexamples":[{
            "candidate_id":x["candidate_id"],
            "label":x["label"],
            "decisions":x["runtime_decisions"],
            "veto_reasons":x["veto_reasons"],
            "arabart_support":x["arabart"]["normalized_local_agreement"],
        } for x in counter],
    },ensure_ascii=False))


if __name__=="__main__":
    main()
