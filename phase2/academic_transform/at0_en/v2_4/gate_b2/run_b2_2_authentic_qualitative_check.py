from __future__ import annotations
import importlib.util, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
DATA=HERE/"B2_2_AUTHENTIC_QUALITATIVE_SET_V1.jsonl"
EX=HERE/"b2_2_relation_aware_extractor.py"
OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
DETAIL=OUT/"B2_2_AUTHENTIC_QUALITATIVE_DETAIL.jsonl"
SUMMARY=OUT/"B2_2_AUTHENTIC_QUALITATIVE_SUMMARY.json"

spec=importlib.util.spec_from_file_location("ex",EX)
ex=importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)

rows=[json.loads(x) for x in DATA.read_text(encoding="utf-8").splitlines() if x.strip()]
details=[]
structural_ok=True
unsupported_relation_count=0
certain=uncertain=ambiguous=0

for row in rows:
    g=ex.relation_aware_extract(row["excerpt"],row["id"])
    assert g["assertions"], row["id"]

    # These authentic excerpts intentionally contain no explicit CIT_* target, equation,
    # or explicit "X precedes Y" / different-subsystems relation sentence.
    # Therefore generating such edges would be unsupported overreach.
    bad=[r for r in g["relations"] if r["type"] in {"CITES","PRECEDES","DISTINCT_FROM"}]
    unsupported_relation_count+=len(bad)
    if bad:
        structural_ok=False

    # AUTH-05 discusses math symbols in prose but contains no explicit equation:
    # no equation binding should be invented.
    if row["id"]=="AUTH-05":
        for a in g["assertions"]:
            if any(str(k).startswith("w_") or str(k).startswith("equation") for k in a["bindings"]):
                structural_ok=False

    for a in g["assertions"]:
        if a["confidence_status"]=="CERTAIN": certain+=1
        elif a["confidence_status"]=="UNCERTAIN": uncertain+=1
        else: ambiguous+=1

    details.append({
        "id":row["id"],
        "purpose":row["purpose"],
        "source_title":row["source_title"],
        "assertions":g["assertions"],
        "relations":g["relations"],
        "audit":g["audit"],
    })

DETAIL.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in details),encoding="utf-8")
summary={
    "status":"PASS_STRUCTURAL_QUALITATIVE_CHECK" if structural_ok else "FAIL_STRUCTURAL_QUALITATIVE_CHECK",
    "development_only":True,
    "qualitative_only":True,
    "benchmark":False,
    "numeric_adoption_claim_authorized":False,
    "excerpt_count":len(rows),
    "unsupported_relation_count":unsupported_relation_count,
    "assertion_confidence_counts":{
        "CERTAIN":certain,
        "UNCERTAIN":uncertain,
        "AMBIGUOUS":ambiguous
    },
    "note":"This check only detects obvious overreach/contract blind spots on authentic prose. It is not a performance benchmark."
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
for d in details:
    print("\n###",d["id"],d["source_title"])
    for a in d["assertions"]:
        print("ASSERT",a["confidence_status"],a["subject"],"|",a["predicate"],"|",a["object"])
    for r in d["relations"]:
        print("REL",r["type"],r["from"],"->",r["to"])
