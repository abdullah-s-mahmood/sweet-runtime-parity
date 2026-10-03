from __future__ import annotations
import hashlib, importlib.util, json, pathlib, re, collections

HERE=pathlib.Path(__file__).resolve().parent
AT0=HERE.parents[1]
GATE0=HERE.parent/"gate0"
CASES=AT0/"cases.jsonl"
GOLD=GATE0/"GATE0_DEV_REFERENCE_V1.jsonl"
SLOTS=HERE/"GATE_A3_SLOT_REFERENCE_V1.jsonl"
EXTRACTOR=HERE/"source_assertion_extractor.py"
DETAIL=HERE/"results"/"GATE_A3_EXTRACTOR_DETAIL.jsonl"
SUMMARY=HERE/"results"/"GATE_A3_EXTRACTOR_SUMMARY.json"
DETAIL.parent.mkdir(exist_ok=True)

EXPECTED_EXTRACTOR_SHA="32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s):
    s=(s or "").lower().replace("−","-").replace("–","-")
    s=re.sub(r"[^a-z0-9_+.%:-]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()

def terms_ok(text, terms):
    t=norm(text)
    return all(norm(x) in t for x in terms)

def evidence_offset(source, evidence):
    first=source.find(evidence)
    assert first>=0, evidence
    second=source.find(evidence,first+1)
    assert second<0, f"non-unique gold evidence: {evidence}"
    return first, first+len(evidence)

def spans_align(gs,ge,ps,pe):
    overlap=max(0,min(ge,pe)-max(gs,ps))
    if overlap<=0:
        return False
    gl=ge-gs; pl=pe-ps
    return overlap/gl>=0.5 or overlap/pl>=0.5 or (ps<=gs and ge<=pe) or (gs<=ps and pe<=ge)

assert sha(EXTRACTOR)==EXPECTED_EXTRACTOR_SHA, (sha(EXTRACTOR),EXPECTED_EXTRACTOR_SHA)

spec=importlib.util.spec_from_file_location("a2",EXTRACTOR)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

cases={x["case_id"]:x for x in rows(CASES)}
gold_records={x["case_id"]:x for x in rows(GOLD)}
slot_ref={x["gold_id"]:x for x in rows(SLOTS)}
wanted=["EN04","EN05","EN06","EN07","EN09","EN12"]
assert set(gold_records)==set(wanted)
all_gold_ids={g["id"] for r in gold_records.values() for g in r["gold_assertions"]}
assert set(slot_ref)==all_gold_ids

gold_map={}
gold_by_case=collections.defaultdict(list)
for cid in wanted:
    src=cases[cid]["source_text"]
    for g in gold_records[cid]["gold_assertions"]:
        s,e=evidence_offset(src,g["evidence"])
        x={**g,"case_id":cid,"span_start":s,"span_end":e}
        gold_map[g["id"]]=x
        gold_by_case[cid].append(x)

preds=[]
pred_by_id={}
pred_to_gold=collections.defaultdict(list)
gold_to_pred=collections.defaultdict(list)

for cid in wanted:
    g=mod.extract_source_assertions(cases[cid])
    em={e["span_id"]:e for e in g["evidence_spans"]}
    for p in g["assertions"]:
        ev=em[p["evidence_span_ids"][0]]
        x={**p,"case_id":cid,"span_start":ev["char_start"],"span_end":ev["char_end"],"evidence_quote":ev["quote"]}
        preds.append(x); pred_by_id[p["assertion_id"]]=x
        for gold in gold_by_case[cid]:
            if spans_align(gold["span_start"],gold["span_end"],x["span_start"],x["span_end"]):
                pred_to_gold[x["assertion_id"]].append(gold["id"])
                gold_to_pred[gold["id"]].append(x["assertion_id"])

gold_covered=[gid for gid in all_gold_ids if gold_to_pred[gid]]
critical_gold=[gid for gid,g in gold_map.items() if g["criticality"]=="CRITICAL"]
critical_covered=[gid for gid in critical_gold if gold_to_pred[gid]]
false_add=[p["assertion_id"] for p in preds if not pred_to_gold[p["assertion_id"]]]
one_to_one=[]
overmerged=[]
for p in preds:
    gids=pred_to_gold[p["assertion_id"]]
    if len(gids)==1 and len(gold_to_pred[gids[0]])==1:
        one_to_one.append(p["assertion_id"])
    elif len(gids)>1:
        overmerged.append(p["assertion_id"])
oversplit=[gid for gid in all_gold_ids if len(gold_to_pred[gid])>1]

CONTEXT_MARKERS={"coreference_subject","shared_context_after_clause_split","embedded_scope"}

field_stats=collections.defaultdict(lambda: [0,0])
detail=[]
critical_silent=[]
error_preds=[]
clean_preds=[]
certain_total=0
certain_clean=0
error_noncertain=0
clean_noncertain=0

context_needed_total=0
context_detected=0
context_independent_total=0
context_false_alarm=0

for p in preds:
    pid=p["assertion_id"]
    gids=pred_to_gold[pid]
    errors=[]
    field_results={}
    involved_critical=any(gold_map[g]["criticality"]=="CRITICAL" for g in gids)

    if not gids:
        errors.append("FALSE_ADDITION")
    elif len(gids)>1:
        errors.append("OVERMERGE")
    elif len(gold_to_pred[gids[0]])>1:
        errors.append("OVERSPLIT")
    else:
        gid=gids[0]
        sr=slot_ref[gid]
        checks={}

        checks["assertion_type"]=(p["assertion_type"]==sr["type"])
        checks["predicate"]=(p["predicate_normalized"] in sr["predicates"])
        checks["polarity"]=(p["polarity"]==sr["polarity"])
        checks["modality"]=(p["modality"]==sr["modality"])
        checks["causality"]=(p["causality"]==sr["causality"])
        checks["subject_terms"]=terms_ok(p["subject"],sr.get("subject_terms",[]))
        checks["object_terms"]=terms_ok(p.get("object"),sr.get("object_terms",[]))
        if "required_population_terms" in sr:
            checks["population"]=terms_ok(" ".join(p.get("population",[])),sr["required_population_terms"])
        if "required_time" in sr:
            checks["time"]=all(x in p.get("temporal_context",[]) for x in sr["required_time"])
        if "required_baseline_terms" in sr:
            checks["baseline"]=terms_ok(" ".join(p.get("baseline",[])),sr["required_baseline_terms"])
        if sr.get("required_scope"):
            checks["scope"]=set(sr["required_scope"]) <= set(p.get("scope_operators",[]))

        for k,v in checks.items():
            field_stats[k][1]+=1
            field_stats[k][0]+=int(v)
            if not v:
                errors.append("SLOT_"+k.upper())
        field_results=checks

        context_flag=bool(CONTEXT_MARKERS & set(p.get("unresolved_slots",[])))
        if sr["context_dependent"]:
            context_needed_total+=1
            context_detected+=int(context_flag)
        else:
            context_independent_total+=1
            context_false_alarm+=int(context_flag)

    clean=not errors
    if clean:
        clean_preds.append(pid)
    else:
        error_preds.append(pid)

    if p["extraction_status"]=="CERTAIN":
        certain_total+=1
        if clean: certain_clean+=1
    else:
        if clean: clean_noncertain+=1
        else: error_noncertain+=1

    silent=False
    if p["extraction_status"]=="CERTAIN" and errors and (involved_critical or not gids):
        silent=True
        critical_silent.append(pid)

    detail.append({
        "prediction_id":pid,
        "case_id":p["case_id"],
        "prediction_status":p["extraction_status"],
        "prediction_type":p["assertion_type"],
        "prediction_subject":p["subject"],
        "prediction_predicate":p["predicate_normalized"],
        "prediction_object":p.get("object"),
        "evidence_quote":p["evidence_quote"],
        "aligned_gold_ids":gids,
        "alignment_count":len(gids),
        "errors":errors,
        "clean":clean,
        "critical_silent_error":silent,
        "field_results":field_results,
        "unresolved_slots":p.get("unresolved_slots",[])
    })

gold_cov=len(gold_covered)/len(all_gold_ids)
critical_cov=len(critical_covered)/len(critical_gold)
false_add_rate=len(false_add)/len(preds)
atomic_rate=len(one_to_one)/len(preds)
certain_precision=certain_clean/certain_total if certain_total else 0.0
error_abstention_recall=error_noncertain/len(error_preds) if error_preds else 1.0
unnecessary_abstention=clean_noncertain/len(clean_preds) if clean_preds else 0.0

field_summary={k:{"correct":v[0],"total":v[1],"accuracy":v[0]/v[1] if v[1] else None} for k,v in sorted(field_stats.items())}

if critical_silent:
    status="FAIL_CRITICAL_SILENT_ERROR"
elif not (critical_cov>=0.95 and gold_cov>=0.90 and false_add_rate<=0.10 and atomic_rate>=0.75 and certain_precision>=0.90 and error_abstention_recall>=0.80):
    status="MIXED_REPAIR_REQUIRED"
else:
    status="PASS_DEVELOPMENT"

DETAIL.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in detail),encoding="utf-8")
summary={
    "gate":"AT0_EN_V2_4_GATE_A3_EXTRACTOR_VALIDATION",
    "status":status,
    "development_only":True,
    "blind_evaluation":False,
    "model_inference":False,
    "extractor_sha256":sha(EXTRACTOR),
    "case_count":len(wanted),
    "gold_assertion_count":len(all_gold_ids),
    "critical_gold_count":len(critical_gold),
    "prediction_count":len(preds),
    "gold_assertion_coverage":gold_cov,
    "critical_gold_coverage":critical_cov,
    "uncovered_gold_ids":sorted(set(all_gold_ids)-set(gold_covered)),
    "false_addition_count":len(false_add),
    "false_addition_rate":false_add_rate,
    "unaligned_prediction_ids":false_add,
    "one_to_one_prediction_count":len(one_to_one),
    "atomic_one_to_one_rate":atomic_rate,
    "overmerged_prediction_ids":overmerged,
    "oversplit_gold_ids":oversplit,
    "field_accuracy":field_summary,
    "context_dependency_detection_recall":context_detected/context_needed_total if context_needed_total else None,
    "context_false_alarm_rate":context_false_alarm/context_independent_total if context_independent_total else None,
    "certain_prediction_count":certain_total,
    "certain_clean_count":certain_clean,
    "certain_precision":certain_precision,
    "error_prediction_count":len(error_preds),
    "clean_prediction_count":len(clean_preds),
    "error_abstention_recall":error_abstention_recall,
    "unnecessary_abstention_rate":unnecessary_abstention,
    "critical_silent_error_count":len(critical_silent),
    "critical_silent_error_ids":critical_silent,
    "thresholds":{
        "critical_gold_coverage_min":0.95,
        "gold_assertion_coverage_min":0.90,
        "false_addition_rate_max":0.10,
        "atomic_one_to_one_rate_min":0.75,
        "certain_precision_min":0.90,
        "error_abstention_recall_min":0.80,
        "critical_silent_errors_max":0
    },
    "hashes":{
        "gold_reference_sha256":sha(GOLD),
        "slot_reference_sha256":sha(SLOTS),
        "detail_sha256":sha(DETAIL)
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
