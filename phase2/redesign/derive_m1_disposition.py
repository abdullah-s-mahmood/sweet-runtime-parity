#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def derive(r):
    reject=(
      r["necessity"]=="UNNECESSARY"
      or r["local_correctness"]=="INCORRECT"
      or r["contextual_correctness"]=="INCORRECT_IN_CONTEXT"
      or r["semantic_fidelity"]=="SEMANTIC_DRIFT"
      or r["scientific_fidelity"]=="VIOLATED"
      or r["protected_invariants"]=="FAIL"
      or r["document_integrity"]=="FAIL"
    )
    if reject: return "REJECT_EDIT"
    review=(
      r["necessity"] in {"OPTIONAL_IMPROVEMENT","AMBIGUOUS_INTENT","INSUFFICIENT_CONTEXT"}
      or r["local_correctness"]=="AMBIGUOUS"
      or r["contextual_correctness"] in {"AMBIGUOUS_READING","INSUFFICIENT_CONTEXT"}
      or r["edit_group_status"] in {"GROUP_REQUIRED_INCOMPLETE","GROUP_BOUNDARY_UNCERTAIN"}
      or r["residual_relation"] in {"RELATED_RESIDUAL","POSSIBLE_RESIDUAL_UNCERTAIN"}
      or r["semantic_fidelity"] in {"AMBIGUOUS","INSUFFICIENT_CONTEXT"}
      or r["scientific_fidelity"] in {"AT_RISK","AMBIGUOUS"}
      or r["ambiguity_author_intent"]!="RESOLVED"
    )
    if review: return "REVIEW_REQUIRED"
    eligible=(
      r["necessity"]=="REQUIRED_ERROR_FIX"
      and r["local_correctness"] in {"CORRECT","VALID_ALTERNATIVE"}
      and r["contextual_correctness"]=="CORRECT_IN_CONTEXT"
      and r["edit_group_status"] in {"ATOMIC_COMPLETE","GROUP_REQUIRED_COMPLETE","NOT_APPLICABLE"}
      and r["residual_relation"] in {"NO_RELEVANT_RESIDUAL","INDEPENDENT_RESIDUAL","OUT_OF_SCOPE"}
      and r["semantic_fidelity"] in {"PRESERVED","CHANGED_BUT_EQUIVALENT"}
      and r["scientific_fidelity"] in {"PRESERVED","NOT_APPLICABLE"}
      and r["protected_invariants"] in {"PASS","NOT_APPLICABLE","NOT_TESTED"}
      and r["document_integrity"] in {"PASS","NOT_APPLICABLE","UNKNOWN"}
    )
    return "ELIGIBLE_FOR_LATER_VERIFIER_STUDY" if eligible else "REVIEW_REQUIRED"

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("adjudicated"); ap.add_argument("--out",default="M1_ADJUDICATED_WITH_DISPOSITION.jsonl")
    args=ap.parse_args()
    rows=[json.loads(x) for x in Path(args.adjudicated).read_text(encoding="utf-8").splitlines() if x.strip()]
    for r in rows: r["derived_disposition"]=derive(r)
    Path(args.out).write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    from collections import Counter
    print(json.dumps(Counter(x["derived_disposition"] for x in rows),ensure_ascii=False,indent=2))
