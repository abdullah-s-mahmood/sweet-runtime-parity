"""Phase 2 — Full Edit-Event Acceptance Prototype.

Runtime decisions are target-agnostic and label-free.
This script MUST NOT read Nahw targets as decision features, human adjudication,
or any previous correctness label.

It consumes complete AraBART edit events and emits ACCEPT / REVIEW / REJECT.
"""
from __future__ import annotations
import json, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
QUEUE=ROOT/"PHASE2_ARABART_FULL_EDIT_ADJUDICATION_QUEUE.jsonl"
OUT=ROOT/"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_RUNTIME.json"

PUNCT=set("،؛:,.!?؟\"'()[]{}")

def jl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def norm_token(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)!="Mn"
        and ch!="\u0640"
        and ch not in PUNCT
    )

def lev(a,b):
    A=list(a); B=list(b)
    d=list(range(len(B)+1))
    for i,ca in enumerate(A,1):
        prev=d[0]; d[0]=i
        for j,cb in enumerate(B,1):
            old=d[j]
            d[j]=min(d[j]+1,d[j-1]+1,prev+(0 if ca==cb else 1))
            prev=old
    return d[-1]

def token_features(source,output):
    s=norm_token(source); o=norm_token(output)
    dist=lev(s,o)
    sn=s.count("ن"); on=o.count("ن")

    one_n_insert=(dist==1 and on==sn+1)
    one_n_delete=(dist==1 and sn==on+1)
    final_alif_add=(o==s+"ا")

    # Narrow destructive surface patterns only.
    ta_marbuta_to_ha=(len(s)>0 and len(o)>0 and s[:-1]==o[:-1] and s.endswith("ة") and o.endswith("ه"))
    alif_maqsura_to_ya=(len(s)>0 and len(o)>0 and s[:-1]==o[:-1] and s.endswith("ى") and o.endswith("ي"))

    return {
        "source_norm":s,
        "output_norm":o,
        "edit_distance":dist,
        "one_n_insert":one_n_insert,
        "one_n_delete":one_n_delete,
        "final_alif_add":final_alif_add,
        "structural_positive":one_n_insert or one_n_delete or final_alif_add,
        "ta_marbuta_to_ha":ta_marbuta_to_ha,
        "alif_maqsura_to_ya":alif_maqsura_to_ya,
        "narrow_destructive":ta_marbuta_to_ha or alif_maqsura_to_ya,
    }

def event_features(r):
    src=list(r["source_words"]); out=list(r["arabart_words"])
    paired=(len(src)==len(out) and len(src)>0)
    tf=[token_features(s,o) for s,o in zip(src,out)] if paired else []
    primitive=list(r.get("primitive_ops") or [])
    sub_only=bool(primitive) and all(op=="SUB" for op in primitive)
    no_destructive=paired and not any(x["narrow_destructive"] for x in tf)
    all_structural=paired and bool(tf) and all(x["structural_positive"] for x in tf)
    all_final_alif=paired and bool(tf) and all(x["final_alif_add"] for x in tf)

    structural_typed=(
        paired and sub_only and no_destructive and all_structural
        and float(r.get("event_cost",1.0))<=0.60
    )

    if len(tf)==1:
        structural_strict=(
            sub_only and no_destructive and tf[0]["structural_positive"]
            and float(r.get("event_cost",1.0))<=0.25
        )
    else:
        structural_strict=(
            paired and len(tf)<=2 and sub_only and no_destructive and all_final_alif
            and float(r.get("event_cost",1.0))<=0.60
        )

    narrow_destructive=paired and any(x["narrow_destructive"] for x in tf)

    return {
        "paired_token_count":paired,
        "source_token_count":len(src),
        "output_token_count":len(out),
        "primitive_ops":primitive,
        "substitution_only":sub_only,
        "event_cost":float(r.get("event_cost",1.0)),
        "token_features":tf,
        "narrow_destructive":narrow_destructive,
        "all_structural":all_structural,
        "all_final_alif":all_final_alif,
        "structural_typed_eligible":structural_typed,
        "structural_strict_eligible":structural_strict,
    }

def decisions(f):
    if f["narrow_destructive"]:
        reject="REJECT"
    else:
        reject="REVIEW"

    typed="ACCEPT" if f["structural_typed_eligible"] else reject
    strict="ACCEPT" if f["structural_strict_eligible"] else reject

    return {
        "NARROW_DESTRUCTIVE":reject,
        "EVENT_STRUCTURAL_TYPED":typed,
        "EVENT_STRUCTURAL_STRICT":strict,
    }

def main():
    rows=jl(QUEUE)
    assert len(rows)==106, len(rows)
    out=[]; counts={}
    for r in rows:
        safe={
            "arabart_event_id":r["arabart_event_id"],
            "passage_id":int(r["passage_id"]),
            "event_type":r["event_type"],
            "source_span":r["source_span"],
            "source_text":r["source_text"],
            "source_words":r["source_words"],
            "arabart_words":r["arabart_words"],
        }
        f=event_features(r)
        d=decisions(f)
        x={**safe,"features":f,"runtime_decisions":d}
        out.append(x)
        for p,v in d.items():
            counts[p+":"+v]=counts.get(p+":"+v,0)+1

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    summary={
        "status":"PHASE2_FULL_EDIT_EVENT_ACCEPTANCE_RUNTIME_COMPLETE",
        "development_only":True,
        "rows":len(out),
        "gold_or_human_labels_read":False,
        "nahw_target_fields_used_for_decision":False,
        "decision_counts":counts,
        "typed_eligible_rows":sum(x["features"]["structural_typed_eligible"] for x in out),
        "strict_eligible_rows":sum(x["features"]["structural_strict_eligible"] for x in out),
        "narrow_destructive_rows":sum(x["features"]["narrow_destructive"] for x in out),
        "policy_definitions":{
            "NARROW_DESTRUCTIVE":"Reject only local ta-marbuta->ha or alif-maqsura->ya degradation; otherwise review.",
            "EVENT_STRUCTURAL_TYPED":"Accept substitution-only complete events where every aligned token is one-N insertion/deletion or final-alif addition, event_cost <= 0.60, and no narrow destructive veto fires.",
            "EVENT_STRUCTURAL_STRICT":"For one token use the same structural family with event_cost <= 0.25; for <=2-token multiword events accept only all-final-alif additions."
        },
        "limitations":[
            "Rules were motivated by repeatedly inspected development evidence and are not production estimates.",
            "Hamza corrections, lexical substitutions, speech-act/tense/person changes and word-boundary edits are review-only in this gate.",
            "Scientific Integrity Guard and semantic fidelity verification still run after linguistic candidate acceptance.",
            "No sealed benchmark and no Phase 3."
        ]
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
