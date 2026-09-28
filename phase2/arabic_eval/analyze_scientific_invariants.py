"""Check preservation of project-authored scientific protected spans.
These 12 cases are NON_HUMAN_GOLD and do not contribute to GEC accuracy.

Two preservation levels are reported:
- exact: the protected substring is byte-for-byte present;
- whitespace-insensitive: only whitespace differences inside the protected span are ignored.
The second level helps distinguish formatting/tokenization drift from content corruption.
"""
import argparse, json, re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def compact_ws(s):
    return re.sub(r"\s+", "", s)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw",type=Path,default=ROOT/"artifacts/OFFICIAL_SCIENTIFIC_STRESS_RAW.jsonl")
    ap.add_argument("--output",type=Path,default=ROOT/"artifacts/SCIENTIFIC_INVARIANT_RESULTS.json")
    args=ap.parse_args()

    rows=[json.loads(x) for x in args.raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows)==12
    correction_path=HERE/"SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"
    corrections=json.loads(correction_path.read_text(encoding="utf-8"))["corrections"] if correction_path.exists() else {}
    def effective_protected(row):
        return corrections.get(row["case_id"],{}).get("effective_protected",row["protected"])
    stages={
        "nopnx_iteration_1": lambda r:r["nopnx_iteration_1"]["output"],
        "nopnx_iteration_2": lambda r:r["nopnx_iteration_2"]["output"],
        "pnx_only": lambda r:r["pnx_only"]["output"],
        "full": lambda r:r["full_pnx_iteration_1"]["output"],
    }
    cases=[]
    summary={}
    for row in rows:
        protected=effective_protected(row)
        item={"case_id":row["case_id"],"category":row["category"],"source":row["source"],"protected_original":row["protected"],"protected_effective":protected,"stages":{}}
        for name,getout in stages.items():
            out=getout(row)
            missing_exact=[p for p in protected if p not in out]
            compact_out=compact_ws(out)
            missing_compact=[p for p in protected if compact_ws(p) not in compact_out]
            item["stages"][name]={
                "output":out,
                "output_changed_from_source":out!=row["source"],
                "protected_all_present_exact":not missing_exact,
                "protected_all_present_whitespace_insensitive":not missing_compact,
                "missing_exact":missing_exact,
                "missing_whitespace_insensitive":missing_compact,
                "whole_source_whitespace_insensitive_unchanged":compact_ws(out)==compact_ws(row["source"]),
                "contains_UNK":"[UNK]" in out,
            }
        cases.append(item)

    for name in stages:
        exact=sum(x["stages"][name]["protected_all_present_exact"] for x in cases)
        compact=sum(x["stages"][name]["protected_all_present_whitespace_insensitive"] for x in cases)
        changed=sum(x["stages"][name]["output_changed_from_source"] for x in cases)
        exact_break=[x["case_id"] for x in cases if not x["stages"][name]["protected_all_present_exact"]]
        compact_break=[x["case_id"] for x in cases if not x["stages"][name]["protected_all_present_whitespace_insensitive"]]
        whole_compact=sum(x["stages"][name]["whole_source_whitespace_insensitive_unchanged"] for x in cases)
        unk_cases=[x["case_id"] for x in cases if x["stages"][name]["contains_UNK"]]
        summary[name]={
            "cases":12,
            "exact_preserved_cases":exact,
            "exact_preservation_rate":exact/12,
            "whitespace_insensitive_preserved_cases":compact,
            "whitespace_insensitive_preservation_rate":compact/12,
            "outputs_changed_from_source":changed,
            "exact_break_cases":exact_break,
            "content_break_after_ignoring_whitespace_cases":compact_break,
            "whole_source_whitespace_insensitive_unchanged_cases":whole_compact,
            "whole_source_whitespace_insensitive_unchanged_rate":whole_compact/12,
            "UNK_output_cases":unk_cases,
        }

    result={
        "status":"PROJECT_AUTHORED_NON_HUMAN_GOLD_SCIENTIFIC_STRESS",
        "accuracy_denominator":False,
        "interpretation":"Whitespace-insensitive preservation is diagnostic only; it does not prove semantic safety.",
        "summary":summary,
        "cases":cases,
    }
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    broken_details={}
    for name in stages:
        broken_details[name]=[
            {
                "case_id":x["case_id"],
                "category":x["category"],
                "protected_original":x["protected_original"],"protected_effective":x["protected_effective"],
                "output":x["stages"][name]["output"],
                "missing_exact":x["stages"][name]["missing_exact"],
                "missing_whitespace_insensitive":x["stages"][name]["missing_whitespace_insensitive"],
            }
            for x in cases
            if not x["stages"][name]["protected_all_present_exact"]
        ]
    print(json.dumps({"scientific_invariants":summary,"broken_exact_details":broken_details},ensure_ascii=False))

if __name__=="__main__":
    main()