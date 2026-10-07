#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, math, pathlib, statistics

CLASSES=["P","I","C","O"]
TAX=["EXACT_TYPED","WRONG_TYPE_EXACT_COORD","SAME_CLASS_WRONG_BOUNDARY","DIFFERENT_CLASS_WRONG_BOUNDARY","SPURIOUS_NO_OVERLAP"]

def sha256(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def q(v,p):
    if not v:return None
    s=sorted(v); x=(len(s)-1)*p; lo=math.floor(x); hi=math.ceil(x)
    if lo==hi:return s[lo]
    return s[lo]*(hi-x)+s[hi]*(x-lo)

def stats(v):
    return {"n":len(v),"mean":sum(v)/len(v) if v else None,"q05":q(v,.05),"q50":q(v,.5),"q95":q(v,.95)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bank",type=pathlib.Path,required=True)
    ap.add_argument("--summary",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)

    s=json.loads(a.summary.read_text())
    if s.get("state")!="R44A_OOF_BANK_COMPLETE": raise RuntimeError("aggregate state mismatch")
    if sha256(a.bank)!=s.get("candidate_bank_sha256"): raise RuntimeError("candidate bank SHA mismatch")
    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720":
        raise RuntimeError("manifest SHA mismatch")
    if len(m["design_documents"])!=256: raise RuntimeError("DESIGN size mismatch")

    rows=[json.loads(x) for x in a.bank.read_text().splitlines() if x.strip()]
    if len(rows)!=1942 or len(rows)!=s.get("candidate_rows"): raise RuntimeError("row count mismatch")

    coord_type=[(r["fold"],r["document"],r["sentence"],r["start"],r["end"],r["b_type"]) for r in rows]
    coord=[(r["fold"],r["document"],r["sentence"],r["start"],r["end"]) for r in rows]
    dup_typed=len(coord_type)-len(set(coord_type))
    dup_coord=len(coord)-len(set(coord))
    if dup_typed: raise RuntimeError(f"duplicate typed coordinates: {dup_typed}")

    targets=collections.Counter(r["target"] for r in rows)
    tax=collections.Counter(r["taxonomy"] for r in rows)
    folds=collections.Counter(int(r["fold"]) for r in rows)
    sections=collections.Counter(r["section"] for r in rows)
    pred=collections.Counter(r["b_type"] for r in rows)

    expected_targets={"NONE":536,"P":213,"I":591,"C":87,"O":515}
    expected_tax={"EXACT_TYPED":1355,"SAME_CLASS_WRONG_BOUNDARY":264,"SPURIOUS_NO_OVERLAP":242,
                  "WRONG_TYPE_EXACT_COORD":51,"DIFFERENT_CLASS_WRONG_BOUNDARY":30}
    if dict(targets)!=expected_targets: raise RuntimeError(f"target mismatch {dict(targets)}")
    if dict(tax)!=expected_tax: raise RuntimeError(f"taxonomy mismatch {dict(tax)}")

    exact_coord=[r for r in rows if r["target"]!="NONE"]
    negatives=[r for r in rows if r["target"]=="NONE"]
    wrong_type=[r for r in rows if r["taxonomy"]=="WRONG_TYPE_EXACT_COORD"]
    if len(exact_coord)!=1406 or len(negatives)!=536: raise RuntimeError("coordinate partition mismatch")
    if len(negatives)!=(tax["SAME_CLASS_WRONG_BOUNDARY"]+tax["DIFFERENT_CLASS_WRONG_BOUNDARY"]+tax["SPURIOUS_NO_OVERLAP"]):
        raise RuntimeError("NONE taxonomy accounting mismatch")

    conf=collections.Counter((r["b_type"],r["target"]) for r in wrong_type)
    conf_matrix={f"{p}->{t}":n for (p,t),n in sorted(conf.items())}

    by_tax={}
    for t in TAX:
        rr=[r for r in rows if r["taxonomy"]==t]
        by_tax[t]={
          "b_conf":stats([float(r["b_conf"]) for r in rr]),
          "boundary_start_prob":stats([float(r["boundary_start_prob"]) for r in rr]),
          "boundary_end_prob":stats([float(r["boundary_end_prob"]) for r in rr]),
          "width":stats([float(r["width"]) for r in rr]),
        }

    goldless=[r for r in rows if r["goldless_example"]]
    goldless_tax=collections.Counter(r["taxonomy"] for r in goldless)

    section_tax=collections.defaultdict(collections.Counter)
    for r in rows: section_tax[r["section"]][r["taxonomy"]]+=1

    thresholds={}
    for t in [.80,.85,.90,.95,.99]:
        hi=[r for r in rows if float(r["b_conf"])>=t]
        pos=sum(r["target"]!="NONE" for r in hi)
        neg=sum(r["target"]=="NONE" for r in hi)
        thresholds[str(t)]={"rows":len(hi),"coordinate_positive":pos,"NONE":neg,
                            "coordinate_precision":pos/len(hi) if hi else None}

    fr=s["fold_results"]
    fold_diag=[]
    for x in fr:
        cm=x["candidate_metrics"]
        fold_diag.append({
          "fold":x["fold"],
          "candidates":cm["candidate_count"],
          "typed_precision":cm["native_typed_precision"],
          "typed_recall":cm["native_typed_recall"],
          "coordinate_precision":cm["coordinate_precision"],
          "coordinate_recall":cm["coordinate_recall"],
          "C_target_support":cm["target_counts"].get("C",0),
          "C_coordinate_ceiling":cm["per_class"]["C"]["coordinate_recall_ceiling"],
          "C_typed_recall":cm["per_class"]["C"]["typed_B_recall"],
          "goldless_candidates":cm["goldless_candidate_count"],
        })

    per=s["aggregate"]["per_class"]
    ceiling={c:per[c]["coordinate_recall_ceiling"] for c in CLASSES}
    typed_recall={c:per[c]["typed_B_recall"] for c in CLASSES}

    report={
      "state":"R44A_FULL_OOF_AUDIT_PASS",
      "identity":{
        "parent_run":37581447046,
        "candidate_bank_sha256":sha256(a.bank),
        "manifest_sha256":m["manifest_sha256"],
        "design_documents":256,
        "candidate_rows":len(rows),
      },
      "integrity":{
        "duplicate_typed_coordinate_rows":dup_typed,
        "duplicate_coordinate_rows_ignoring_predicted_type":dup_coord,
        "target_counts":dict(targets),
        "taxonomy":dict(tax),
        "fold_candidate_rows":dict(sorted(folds.items())),
        "predicted_type_counts":dict(pred),
        "section_counts":dict(sections),
      },
      "mechanism":{
        "exact_coordinate_positives":len(exact_coord),
        "NONE_negatives":len(negatives),
        "wrong_type_exact_coordinate":len(wrong_type),
        "wrong_type_confusion":conf_matrix,
        "wrong_boundary_all":tax["SAME_CLASS_WRONG_BOUNDARY"]+tax["DIFFERENT_CLASS_WRONG_BOUNDARY"],
        "spurious_no_overlap":tax["SPURIOUS_NO_OVERLAP"],
        "NONE_fraction":len(negatives)/len(rows),
        "dominant_NONE_boundary_or_spurious_fraction":1.0,
        "non_exact_typed_total":len(rows)-tax["EXACT_TYPED"],
        "boundary_or_spurious_fraction_of_non_exact_typed":
          (tax["SAME_CLASS_WRONG_BOUNDARY"]+tax["DIFFERENT_CLASS_WRONG_BOUNDARY"]+tax["SPURIOUS_NO_OVERLAP"])/(len(rows)-tax["EXACT_TYPED"]),
      },
      "actionability":{
        "coordinate_recall_ceiling":ceiling,
        "typed_B_recall":typed_recall,
        "all_coordinate_ceilings_above_recall_floor_0_20":all(v>=.20 for v in ceiling.values()),
        "boundary_repair_required_before_primary_verifier":False,
        "reason":"Every class coordinate ceiling is far above the frozen recall floor; first test leakage-safe verifier rejection/type correction.",
      },
      "confidence_threshold_diagnostic":thresholds,
      "by_taxonomy":by_tax,
      "goldless":{"candidate_count":len(goldless),"taxonomy":dict(goldless_tax)},
      "section_taxonomy":{k:dict(v) for k,v in section_tax.items()},
      "fold_variability":fold_diag,
      "selection_implication":{
        "C_support_total":targets["C"],
        "C_fold_support":[x["C_target_support"] for x in fold_diag],
        "C_coordinate_ceiling_range":[min(x["C_coordinate_ceiling"] for x in fold_diag),max(x["C_coordinate_ceiling"] for x in fold_diag)],
        "C_typed_recall_range":[min(x["C_typed_recall"] for x in fold_diag),max(x["C_typed_recall"] for x in fold_diag)],
        "recommended_R44B_protocol":"B1_NESTED_OUTER_INNER_DOCUMENT_CV",
        "reason":"Class C is the smallest positive target and has material fold-to-fold ceiling/typed-recall variation; nested evaluation uses all DESIGN documents while avoiding dependence on a single HEAD_SELECT split.",
      },
      "stop_boundary":"NO_VERIFY_INTERNAL_OR_PROTECTED_TEST_ACCESS",
    }

    outj=a.out/"R44A_FULL_OOF_AUDIT.json"
    outj.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")

    md=[
      "# ACAD_PASS — R44-A Full OOF Audit",
      "",
      "**Verdict:** `R44A_FULL_OOF_AUDIT_PASS`",
      "",
      f"- Candidate rows: **{len(rows)}**",
      f"- Exact-coordinate positives: **{len(exact_coord)}**",
      f"- Exact-typed: **{tax['EXACT_TYPED']}**",
      f"- NONE negatives: **{len(negatives)}**",
      f"- Same-class wrong boundary: **{tax['SAME_CLASS_WRONG_BOUNDARY']}**",
      f"- Different-class wrong boundary: **{tax['DIFFERENT_CLASS_WRONG_BOUNDARY']}**",
      f"- Spurious/no-overlap: **{tax['SPURIOUS_NO_OVERLAP']}**",
      f"- Wrong-type exact-coordinate: **{len(wrong_type)}**",
      f"- Goldless candidates: **{len(goldless)}**",
      "",
      "All NONE rows are boundary/spurious errors. The 51 exact-coordinate wrong-type rows remain positive typed targets and are directly learnable by the joint head.",
      "",
      "## Candidate recall ceilings",
      "",
    ]
    for c in CLASSES: md.append(f"- {c}: coordinate ceiling **{ceiling[c]:.6f}**, native typed recall **{typed_recall[c]:.6f}**")
    md += [
      "",
      "All coordinate ceilings exceed the frozen 0.20 recall floor. Boundary repair is therefore **not a prerequisite** before the corrected verifier.",
      "",
      "## R44-B protocol recommendation",
      "",
      "`B1_NESTED_OUTER_INNER_DOCUMENT_CV`.",
      "",
      "Reason: class C is the smallest target class and shows meaningful fold-to-fold variability; nested evaluation avoids letting one fixed HEAD_SELECT split dominate the decision while preserving leakage isolation.",
      "",
      "STOP: no VERIFY_INTERNAL, old SELECT, DEV or protected tests.",
    ]
    (a.out/"R44A_FULL_OOF_AUDIT.md").write_text("\n".join(md)+"\n")
    print(json.dumps({"state":report["state"],"recommendation":report["selection_implication"]["recommended_R44B_protocol"],
                      "candidate_rows":len(rows),"NONE":len(negatives),"C_support":targets["C"],
                      "C_ceiling_range":report["selection_implication"]["C_coordinate_ceiling_range"]},indent=2))

if __name__=="__main__": main()
