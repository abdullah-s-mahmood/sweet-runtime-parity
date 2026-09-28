"""Phase 2 — target-agnostic reverse acceptance gate for AraBART-only local edits.

DEVELOPMENT ONLY.

Runtime step reads generation-time evidence only. It MUST NOT read:
- Nahw target overlap/correction/explanation fields;
- PHASE2_ARABART_EDIT_ADJUDICATION.jsonl;
- any human correctness label.

It emits frozen ACCEPT/REVIEW/REJECT decisions. Evaluation happens in a separate script.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
QUEUE=ROOT/"PHASE2_ARABART_EDIT_ADJUDICATION_QUEUE.jsonl"
FULL=ROOT/"PHASE2_ARABART_FULL_EDIT_ADJUDICATION_QUEUE.jsonl"
OUT=ROOT/"PHASE2_ARABART_REVERSE_ACCEPTANCE_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_ARABART_REVERSE_ACCEPTANCE_RUNTIME.json"

def jl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def strip_marks_punct(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)!="Mn"
        and ch!="\u0640"
        and ch not in "،؛:,.!?؟\"'()[]{}"
    )

def levenshtein(a,b):
    A=list(a); B=list(b)
    d=list(range(len(B)+1))
    for i,ca in enumerate(A,1):
        prev=d[0]; d[0]=i
        for j,cb in enumerate(B,1):
            old=d[j]
            d[j]=min(d[j]+1,d[j-1]+1,prev+(0 if ca==cb else 1))
            prev=old
    return d[-1]

HAMZA=set("أإؤئءآ")

def complex_spans():
    # Geometry only. Never inspect target/reference fields.
    out={}
    for r in jl(FULL):
        if r.get("event_type")!="COMPLEX":
            continue
        out.setdefault(int(r["passage_id"]),[]).append(tuple(map(int,r["source_span"])))
    return out

def overlaps(a,b):
    a1,a2=a; b1,b2=b
    return max(a1,b1)<min(a2,b2)

def runtime_features(r,complex_by_passage):
    src=strip_marks_punct(r["source_word"])
    out=strip_marks_punct(r["arabart_word"])
    dist=levenshtein(src,out)
    src_n=src.count("ن"); out_n=out.count("ن")

    ta_to_ha=src.endswith("ة") and out.endswith("ه")
    maq_to_ya=src.endswith("ى") and out.endswith("ي")

    # Conservative medial-hamza loss: do not treat ambiguous initial hamzat-wasl
    # changes as a hard veto.
    src_internal=sum(ch in HAMZA for ch in src[1:])
    out_internal=sum(ch in HAMZA for ch in out[1:])
    internal_hamza_loss=src_internal>out_internal

    one_n_insert=(dist==1 and out_n==src_n+1)
    one_n_delete=(dist==1 and src_n==out_n+1)
    case_alif_add=(out==src+"ا")
    structural_positive=one_n_insert or one_n_delete or case_alif_add

    span=tuple(map(int,r["source_word_span"]))
    is_complex_member=any(overlaps(span,x) for x in complex_by_passage.get(int(r["passage_id"]),[]))

    hard_veto=[]
    if ta_to_ha: hard_veto.append("TA_MARBUTA_TO_HA")
    if maq_to_ya: hard_veto.append("ALIF_MAQSURA_TO_YA")
    if internal_hamza_loss: hard_veto.append("INTERNAL_HAMZA_LOSS")

    ged=r.get("ged") or {}
    ged_error=float(ged.get("error_probability",0.0))
    alignment_cost=float(r.get("alignment_cost",1.0))

    return {
        "source_norm":src,
        "output_norm":out,
        "edit_distance":dist,
        "alignment_cost":alignment_cost,
        "ged_label":ged.get("label"),
        "ged_error_probability":ged_error,
        "ta_marbuta_to_ha":ta_to_ha,
        "alif_maqsura_to_ya":maq_to_ya,
        "internal_hamza_loss":internal_hamza_loss,
        "one_n_insert":one_n_insert,
        "one_n_delete":one_n_delete,
        "case_alif_add":case_alif_add,
        "structural_positive":structural_positive,
        "complex_event_member":is_complex_member,
        "hard_vetoes":hard_veto,
    }

def decisions(f):
    if f["hard_vetoes"]:
        structural="REJECT"
        structural_ged="REJECT"
    elif f["complex_event_member"]:
        # A decomposed one-word edit cannot be auto-applied when the full
        # generator event is multiword. Evaluate the complete event separately.
        structural="REVIEW"
        structural_ged="REVIEW"
    elif f["structural_positive"] and f["alignment_cost"]<=0.25:
        structural="ACCEPT"
        structural_ged="ACCEPT" if f["ged_error_probability"]>=0.50 else "REVIEW"
    else:
        structural="REVIEW"
        structural_ged="REVIEW"

    hard_only="REJECT" if f["hard_vetoes"] else "REVIEW"
    return {
        "HARD_VETO_ONLY":hard_only,
        "STRUCTURAL_TYPED":structural,
        "STRUCTURAL_TYPED_PLUS_GED50":structural_ged,
    }

def main():
    rows=jl(QUEUE)
    assert len(rows)==67, len(rows)
    csp=complex_spans()
    out=[]
    counts={}
    for r in rows:
        # Explicitly copy only runtime-safe fields. Do not propagate target fields.
        safe={
            "arabart_edit_id":r["arabart_edit_id"],
            "passage_id":int(r["passage_id"]),
            "word_index":int(r["word_index"]),
            "source_word":r["source_word"],
            "arabart_word":r["arabart_word"],
        }
        f=runtime_features(r,csp)
        d=decisions(f)
        x={**safe,"features":f,"runtime_decisions":d}
        out.append(x)
        for p,v in d.items():
            counts[p+":"+v]=counts.get(p+":"+v,0)+1

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    summary={
        "status":"PHASE2_ARABART_REVERSE_ACCEPTANCE_RUNTIME_COMPLETE",
        "development_only":True,
        "rows":len(out),
        "gold_or_human_labels_read":False,
        "nahw_target_fields_read":False,
        "decision_counts":counts,
        "hard_veto_rows":sum(bool(x["features"]["hard_vetoes"]) for x in out),
        "complex_member_rows":sum(x["features"]["complex_event_member"] for x in out),
        "structural_positive_rows":sum(x["features"]["structural_positive"] for x in out),
        "policy_definitions":{
            "HARD_VETO_ONLY":"Reject only explicit destructive orthographic patterns; otherwise review.",
            "STRUCTURAL_TYPED":"Accept only narrow N-restoration/removal or simple accusative-alif addition with safe local alignment; hard veto rejects; complex-event members review.",
            "STRUCTURAL_TYPED_PLUS_GED50":"Same structural policy, but ACCEPT additionally requires GED error_probability >= 0.50."
        },
        "limitations":[
            "Rules were motivated by repeatedly inspected development evidence and are not an independent production estimate.",
            "Initial hamza changes are deliberately not hard-vetoed because hamzat-al-wasl corrections can be valid.",
            "Complex-event members are never auto-applied as isolated one-word edits."
        ]
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
