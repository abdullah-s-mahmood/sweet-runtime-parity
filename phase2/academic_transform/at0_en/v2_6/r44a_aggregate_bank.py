#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib

CLASSES=["P","I","C","O"]
EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"

def sha_file(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def sha_text(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifacts-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    m=json.loads(a.manifest.read_text())
    ms=m.pop("manifest_sha256",None)
    if ms!=EXPECTED_MANIFEST_SHA or sha_text(json.dumps(m,sort_keys=True,separators=(",",":")))!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError("manifest mismatch")
    expected={int(x["fold"]):set(x["documents"]) for x in m["oof_folds"]}
    if set(expected)!=set(range(5)):raise RuntimeError("fold IDs mismatch")

    summaries={}
    banks={}
    for p in a.artifacts_root.rglob("R44A_FOLD_*_SUMMARY.json"):
        s=json.loads(p.read_text()); f=int(s["fold"])
        if f in summaries:raise RuntimeError(f"duplicate fold summary {f}")
        summaries[f]=s
    for p in a.artifacts_root.rglob("R44A_FOLD_*_CANDIDATES.jsonl"):
        f=int(p.name.split("_")[2])
        if f in banks:raise RuntimeError(f"duplicate fold bank {f}")
        banks[f]=p
    if set(summaries)!=set(range(5)) or set(banks)!=set(range(5)):
        raise RuntimeError(f"incomplete fold artifacts summaries={sorted(summaries)} banks={sorted(banks)}")

    all_rows=[]; seen_docs=set(); seen_candidates=set()
    tax=collections.Counter(); targets=collections.Counter(); predtypes=collections.Counter()
    total_gold=collections.Counter(); coord=collections.Counter(); typed=collections.Counter()
    bio_viol=0; fold_table=[]
    model_ids=[]
    total_candidates=0; goldless_candidates=0
    for f in range(5):
        s=summaries[f]
        if s.get("state")!="R44A_FOLD_COMPLETE":raise RuntimeError(f"fold {f} state")
        if s.get("r44_manifest_sha256")!=EXPECTED_MANIFEST_SHA:raise RuntimeError(f"fold {f} manifest")
        if set(s["heldout_document_ids"])!=expected[f]:raise RuntimeError(f"fold {f} heldout IDs mismatch")
        if seen_docs & expected[f]:raise RuntimeError("heldout doc overlap")
        seen_docs |= expected[f]
        if s["candidate_bank"]["sha256"]!=sha_file(banks[f]):raise RuntimeError(f"fold {f} bank physical hash")
        g=s["guards"]
        must={"design_only_training":True,"heldout_fold_used_for_training":False,
              "training_artifact_contains_verify_internal":False,"training_artifact_contains_old_r43_select":False,
              "verify_internal_used":False,"old_r43_select_used":False,"historical_dev_read":False,
              "test_read":False,"other_folds_read":False,"factpico_used":False,
              "consumed_60_rct_holdout_used":False,"head_training":False}
        for k,v in must.items():
            if g.get(k)!=v:raise RuntimeError(f"fold {f} guard {k} {g.get(k)} != {v}")
        count=0
        with banks[f].open() as fh:
            for line in fh:
                r=json.loads(line); count+=1
                if int(r["fold"])!=f or int(r["document"]) not in expected[f]:raise RuntimeError("bank row fold/doc mismatch")
                key=(r["document"],r["sentence"],r["start"],r["end"],r["b_type"])
                if key in seen_candidates:raise RuntimeError(f"duplicate candidate across bank {key}")
                seen_candidates.add(key); all_rows.append(r)
        if count!=s["candidate_bank"]["rows"]:raise RuntimeError(f"fold {f} bank row count mismatch")
        met=s["candidate_bank"]["metrics"]
        total_candidates+=met["candidate_count"];goldless_candidates+=met["goldless_candidate_count"]
        tax.update(met["taxonomy"]);targets.update(met["target_counts"]);predtypes.update(met["predicted_type_counts"])
        bio_viol+=met["BIO_violation_count"]
        for c in CLASSES:
            q=met["per_class"][c]
            total_gold[c]+=q["gold"];coord[c]+=q["coordinate_available"];typed[c]+=q["typed_B_available"]
        model_ids.append({"fold":f,"B":s["models"]["B_CANDIDATE"]["model_sha256"],
                          "BOUNDARY":s["models"]["C_BOUNDARY"]["model_sha256"],
                          "B_steps":s["models"]["B_CANDIDATE"]["global_step"],
                          "BOUNDARY_steps":s["models"]["C_BOUNDARY"]["global_step"],
                          "B_loss":s["models"]["B_CANDIDATE"]["train_loss"],
                          "BOUNDARY_loss":s["models"]["C_BOUNDARY"]["train_loss"]})
        fold_table.append({"fold":f,"heldout_documents":len(expected[f]),
                           "candidate_metrics":met,"models":model_ids[-1]})
    if seen_docs!=set(m["design_documents"]):raise RuntimeError("aggregate DESIGN coverage mismatch")

    all_rows.sort(key=lambda r:(r["fold"],r["document"],r["sentence"],r["start"],r["end"],r["b_type"]))
    bankout=a.out/"R44A_OOF_CANDIDATE_BANK.jsonl"
    with bankout.open("w") as fh:
        for r in all_rows:fh.write(json.dumps(r,sort_keys=True)+"\n")
    per={}
    for c in CLASSES:
        g=total_gold[c]
        per[c]={"gold":int(g),"coordinate_available":int(coord[c]),"typed_B_available":int(typed[c]),
                "coordinate_recall_ceiling":coord[c]/g if g else 0.0,
                "typed_B_recall":typed[c]/g if g else 0.0}
    typed_total=sum(typed.values());coord_total=sum(coord.values());gold_total=sum(total_gold.values())
    summary={
      "state":"R44A_OOF_BANK_COMPLETE",
      "r44_manifest_sha256":EXPECTED_MANIFEST_SHA,
      "design_documents":len(seen_docs),"folds":5,
      "candidate_bank_sha256":sha_file(bankout),"candidate_rows":len(all_rows),
      "aggregate":{
        "gold_total":int(gold_total),"candidate_count":int(total_candidates),
        "coordinate_available_total":int(coord_total),"typed_B_available_total":int(typed_total),
        "native_typed_precision":typed_total/total_candidates if total_candidates else 0.0,
        "native_typed_recall":typed_total/gold_total if gold_total else 0.0,
        "native_typed_f1":(2*(typed_total/total_candidates)*(typed_total/gold_total)/
                           ((typed_total/total_candidates)+(typed_total/gold_total)))
                           if typed_total and total_candidates and gold_total else 0.0,
        "coordinate_precision":coord_total/total_candidates if total_candidates else 0.0,
        "coordinate_recall":coord_total/gold_total if gold_total else 0.0,
        "per_class":per,"target_counts":dict(targets),"taxonomy":dict(tax),
        "predicted_type_counts":dict(predtypes),"goldless_candidate_count":int(goldless_candidates),
        "BIO_violation_count":int(bio_viol)
      },
      "fold_results":fold_table,"model_identities":model_ids,
      "guards":{"complete_design_coverage":True,"zero_fold_overlap":True,
                "verify_internal_used":False,"old_r43_select_used":False,
                "head_training":False,"threshold_selection":False},
      "stop_boundary":"STOP_BEFORE_R44B_HEAD_TRAINING_OR_VERIFY_INTERNAL_ACCESS",
      "next_action":"ADVERSARIAL_AUDIT_REAL_OOF_BANK_THEN_FREEZE_R44B_PROTOCOL"
    }
    (a.out/"R44A_OOF_BANK_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":main()
