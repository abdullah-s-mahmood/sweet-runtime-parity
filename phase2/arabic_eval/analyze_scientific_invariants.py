"""Check exact preservation of project-authored scientific protected spans.
These 12 cases are NON_HUMAN_GOLD and do not contribute to GEC accuracy.
"""
import argparse, json, collections
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw",type=Path,default=ROOT/"artifacts/OFFICIAL_SCIENTIFIC_STRESS_RAW.jsonl")
    ap.add_argument("--output",type=Path,default=ROOT/"artifacts/SCIENTIFIC_INVARIANT_RESULTS.json")
    args=ap.parse_args()

    rows=[json.loads(x) for x in args.raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows)==12
    stages={
        "nopnx_iteration_1": lambda r:r["nopnx_iteration_1"]["output"],
        "nopnx_iteration_2": lambda r:r["nopnx_iteration_2"]["output"],
        "pnx_only": lambda r:r["pnx_only"]["output"],
        "full": lambda r:r["full_pnx_iteration_1"]["output"],
    }
    cases=[]
    summary={}
    for row in rows:
        item={"case_id":row["case_id"],"category":row["category"],"protected":row["protected"],"stages":{}}
        for name,getout in stages.items():
            out=getout(row)
            missing=[p for p in row["protected"] if p not in out]
            item["stages"][name]={
                "output":out,
                "output_changed_from_source":out!=row["source"],
                "protected_all_present_exact":not missing,
                "missing_protected":missing,
            }
        cases.append(item)

    for name in stages:
        preserved=sum(x["stages"][name]["protected_all_present_exact"] for x in cases)
        changed=sum(x["stages"][name]["output_changed_from_source"] for x in cases)
        broken=[x["case_id"] for x in cases if not x["stages"][name]["protected_all_present_exact"]]
        summary[name]={
            "cases":12,
            "all_protected_exactly_preserved_cases":preserved,
            "protected_preservation_rate":preserved/12,
            "outputs_changed_from_source":changed,
            "protected_break_cases":broken,
        }

    result={
        "status":"PROJECT_AUTHORED_NON_HUMAN_GOLD_SCIENTIFIC_STRESS",
        "accuracy_denominator":False,
        "summary":summary,
        "cases":cases,
    }
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"scientific_invariants":summary},ensure_ascii=False))

if __name__=="__main__":
    main()
