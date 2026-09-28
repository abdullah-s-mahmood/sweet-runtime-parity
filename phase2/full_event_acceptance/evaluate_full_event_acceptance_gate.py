"""Evaluate frozen full edit-event runtime decisions using development labels.

Runtime decisions are already materialized before this script reads adjudication.
"""
from __future__ import annotations
import json,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_FEATURES.jsonl"
LABELS=ROOT/"PHASE2_ARABART_FULL_EDIT_ADJUDICATION.jsonl"
OLD_FEATURES=ROOT/"PHASE2_INDEPENDENT_ACCEPTANCE_FEATURES.jsonl"
REV_QUEUE=ROOT/"PHASE2_ARABART_EDIT_ADJUDICATION_QUEUE.jsonl"
REV_RESULTS=ROOT/"PHASE2_ARABART_REVERSE_ACCEPTANCE_RESULTS.json"
OUT=ROOT/"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def supported(c):
    return c in ("SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE")

def summarize(rows,policy):
    acc=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT"]
    rev=[x for x in rows if x["runtime_decisions"][policy]=="REVIEW"]
    rej=[x for x in rows if x["runtime_decisions"][policy]=="REJECT"]
    classes={}
    for x in acc:
        c=x["label"]["event_class"]; classes[c]=classes.get(c,0)+1
    supp=sum(supported(x["label"]["event_class"]) for x in acc)
    wrong=sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in acc)
    partial=sum(x["label"]["event_class"]=="PARTIAL_CORRECTION" for x in acc)
    high_wrong=sum(
        x["label"]["event_class"]=="WRONG_CORRECTION"
        and x["label"]["severity"] in ("HIGH","CRITICAL")
        for x in acc
    )
    total_supported=sum(supported(x["label"]["event_class"]) for x in rows)
    return {
        "policy":policy,
        "accepted":len(acc),"review":len(rev),"rejected":len(rej),
        "accepted_classes":classes,
        "accepted_supported":supp,
        "accepted_wrong":wrong,
        "accepted_partial":partial,
        "accepted_high_or_critical_wrong":high_wrong,
        "supported_precision":supp/len(acc) if acc else None,
        "supported_coverage_within_full_events":supp/total_supported if total_supported else None,
        "accepted_event_ids":[x["arabart_event_id"] for x in acc],
    }

def word_spans(text):
    return [(m.start(),m.end(),m.group()) for m in re.finditer(r"\S+",text)]

def word_index_for_span(text,span):
    a,b=map(int,span)
    for i,(x,y,_) in enumerate(word_spans(text)):
        if max(a,x)<min(b,y):
            return i
    return None

def prior_accept_keys():
    old=jl(OLD_FEATURES)
    old_keys=set()
    for x in old:
        if x["runtime_decisions"]["EXACT_LOCAL_AGREEMENT"]=="ACCEPT":
            old_keys.add((int(x["passage_id"]),int(x["word_index"]),x["source_word"],x["candidate_result_word"]))

    revq=jl(REV_QUEUE)
    rr=json.loads(REV_RESULTS.read_text(encoding="utf-8"))
    rev_ids=set(rr["policy_results"]["STRUCTURAL_TYPED"]["accepted_ids"])
    rev_keys=set()
    for x in revq:
        if x["arabart_edit_id"] in rev_ids:
            rev_keys.add((int(x["passage_id"]),int(x["word_index"]),x["source_word"],x["arabart_word"]))
    return old_keys,rev_keys

def incremental_analysis(rows,policy):
    old_keys,rev_keys=prior_accept_keys()
    acc=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT" and supported(x["label"]["event_class"])]
    duplicated=[]; incremental=[]
    for x in acc:
        isdup=False; sources=[]
        if len(x["source_words"])==1 and len(x["arabart_words"])==1:
            idx=word_index_for_span(x["source_passage"],x["source_span"])
            k=(int(x["passage_id"]),idx,x["source_words"][0],x["arabart_words"][0])
            if k in old_keys:
                isdup=True; sources.append("EXISTING_EXACT_LOCAL")
            if k in rev_keys:
                isdup=True; sources.append("ARABART_REVERSE")
        rec={
            "arabart_event_id":x["arabart_event_id"],
            "passage_id":x["passage_id"],
            "source_text":x["source_text"],
            "arabart_words":x["arabart_words"],
            "event_type":x["event_type"],
            "duplicate_sources":sources,
        }
        (duplicated if isdup else incremental).append(rec)
    return {
        "accepted_supported_events":len(acc),
        "duplicated_with_current_local_accept_path":len(duplicated),
        "incremental_event_units":len(incremental),
        "incremental_events":incremental,
        "note":"Incremental event units are not directly identical to local-edit counts; multiword events can contain multiple token corrections."
    }

def main():
    feats=jl(FEATURES)
    labels_raw=jl(LABELS)
    lm={x["arabart_event_id"]:{
        "event_class":x["pass2"]["event_class"],
        "severity":x["pass2"]["severity"],
    } for x in labels_raw}
    assert len(feats)==106 and len(lm)==106
    rows=[]
    for x in feats:
        y=dict(x)
        # source_passage is needed only after decisions, for duplicate accounting
        labrow=next(z for z in labels_raw if z["arabart_event_id"]==x["arabart_event_id"])
        y["source_passage"]=labrow["source_passage"]
        y["label"]=lm[x["arabart_event_id"]]
        rows.append(y)

    policies=list(rows[0]["runtime_decisions"])
    results={p:summarize(rows,p) for p in policies}

    destructive=[x for x in rows if x["features"]["narrow_destructive"]]
    result={
        "status":"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_DEVELOPMENT_EVALUATED",
        "runtime_decisions_materialized_before_labels":True,
        "rows":len(rows),
        "supported_or_alternative_rows":sum(supported(x["label"]["event_class"]) for x in rows),
        "wrong_rows":sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in rows),
        "policy_results":results,
        "feature_diagnostics":{
            "narrow_destructive_rows":len(destructive),
            "narrow_destructive_wrong":sum(x["label"]["event_class"]=="WRONG_CORRECTION" for x in destructive),
            "narrow_destructive_supported":sum(supported(x["label"]["event_class"]) for x in destructive),
            "typed_eligible_rows":sum(x["features"]["structural_typed_eligible"] for x in rows),
            "typed_eligible_supported":sum(
                x["features"]["structural_typed_eligible"] and supported(x["label"]["event_class"])
                for x in rows
            ),
            "typed_eligible_wrong":sum(
                x["features"]["structural_typed_eligible"] and x["label"]["event_class"]=="WRONG_CORRECTION"
                for x in rows
            ),
        },
        "incremental_analysis":incremental_analysis(rows,"EVENT_STRUCTURAL_TYPED"),
        "limitations":[
            "This is repeatedly inspected development evidence, not sealed/generalization evidence.",
            "Rules were motivated by this development stream and must be validated on disjoint data before freeze.",
            "Event-level units and prior local-edit units are not numerically interchangeable.",
            "Same-agent adjudication is not independent human validation.",
            "This gate does not replace scientific/semantic/document safety layers."
        ]
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
