from __future__ import annotations
import collections, hashlib, importlib.util, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
AT0=HERE.parents[1]
CASES=AT0/"cases.jsonl"
REF=HERE/"GATE_A1_ANCHOR_REFERENCE_V1.jsonl"
EXTRACTOR=HERE/"source_anchor_extractor.py"
OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
PRED=OUT/"GATE_A1_ANCHOR_PREDICTIONS.jsonl"
SUMMARY=OUT/"GATE_A1_ANCHOR_SUMMARY.json"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

spec=importlib.util.spec_from_file_location("a1",EXTRACTOR)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

cases={x["case_id"]:x for x in rows(CASES)}
refs={x["case_id"]:x for x in rows(REF)}
wanted=["EN04","EN05","EN06","EN07","EN09","EN12"]
assert set(refs)==set(wanted)

pred_rows=[]
case_metrics={}
overall_tp=overall_fp=overall_fn=0
provenance_checks=0

for cid in wanted:
    case=cases[cid]
    graph=mod.build_anchor_graph(case)

    assert graph["schema_version"]=="2.4-gate0-v1"
    assert graph["source_identity"]["source_sha256"]==case["source_sha256"]
    assert graph["assertions"]==[]
    assert graph["relations"]==[]
    assert graph["coverage"]["coverage_status"]=="UNKNOWN"

    spans={x["span_id"]:x for x in graph["evidence_spans"]}
    anchors=graph["anchors"]
    assert len(spans)==len(graph["evidence_spans"])
    assert len({x["anchor_id"] for x in anchors})==len(anchors)
    assert set(graph["coverage"]["unowned_anchor_ids"])=={x["anchor_id"] for x in anchors}

    for a in anchors:
        assert a["criticality"]=="MATERIAL"
        assert len(a["evidence_span_ids"])==1
        sid=a["evidence_span_ids"][0]
        assert sid in spans
        sp=spans[sid]
        start,end=sp["char_start"],sp["char_end"]
        assert start is not None and end is not None and 0 <= start < end <= len(case["source_text"])
        exact=case["source_text"][start:end]
        assert exact==sp["quote"]==a["raw"]
        provenance_checks+=1

    pred=collections.Counter((x["anchor_type"],x["raw"]) for x in anchors)
    gold=collections.Counter()
    for e in refs[cid]["expected"]:
        gold[(e["anchor_type"],e["raw"])]+=e["count"]

    tp=sum((pred & gold).values())
    fp=sum((pred-gold).values())
    fn=sum((gold-pred).values())
    overall_tp+=tp; overall_fp+=fp; overall_fn+=fn
    precision=tp/(tp+fp) if tp+fp else 1.0
    recall=tp/(tp+fn) if tp+fn else 1.0
    case_metrics[cid]={
        "gold":sum(gold.values()),"predicted":sum(pred.values()),
        "tp":tp,"fp":fp,"fn":fn,"precision":precision,"recall":recall
    }
    pred_rows.append({
        "case_id":cid,
        "source_sha256":case["source_sha256"],
        "anchors":anchors,
        "evidence_spans":graph["evidence_spans"],
        "metrics":case_metrics[cid],
    })

precision=overall_tp/(overall_tp+overall_fp) if overall_tp+overall_fp else 1.0
recall=overall_tp/(overall_tp+overall_fn) if overall_tp+overall_fn else 1.0
f1=(2*precision*recall/(precision+recall)) if precision+recall else 0.0

status="PASS" if (overall_fp==0 and overall_fn==0 and precision==1.0 and recall==1.0) else "FAIL"

PRED.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in pred_rows),encoding="utf-8")
summary={
    "gate":"AT0_EN_V2_4_GATE_A1_DETERMINISTIC_ANCHORS",
    "status":status,
    "model_inference":False,
    "cases":wanted,
    "gold_anchor_count":overall_tp+overall_fn,
    "predicted_anchor_count":overall_tp+overall_fp,
    "tp":overall_tp,"fp":overall_fp,"fn":overall_fn,
    "precision":precision,"recall":recall,"f1":f1,
    "provenance_exact_span_checks":provenance_checks,
    "all_anchors_unowned_by_design":True,
    "semantic_ownership_assessed":False,
    "case_metrics":case_metrics,
    "hashes":{
        "cases_sha256":sha(CASES),
        "reference_sha256":sha(REF),
        "extractor_sha256":sha(EXTRACTOR),
        "predictions_sha256":sha(PRED),
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
if status!="PASS":
    raise SystemExit(2)
