#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,json,pathlib

def file_hash(path,algo):
    h=hashlib.new(algo)
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    records=0
    extraction_entries=0
    intervention_types=collections.Counter()
    aggregate_targets=collections.Counter()
    malformed=0
    nct_ids=set()
    annotated_token_positive=0
    annotated_token_total=0

    with open(a.input,encoding="utf-8",errors="strict") as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            try:
                d=json.loads(line)
            except Exception:
                malformed+=1
                continue
            records+=1
            rid=str(d.get("id","")).strip()
            if rid: nct_ids.add(rid)

            ext=d.get("extraction1",{})
            if isinstance(ext,dict):
                for _,e in ext.items():
                    if not isinstance(e,dict): continue
                    extraction_entries+=1
                    typ=str(e.get("intervention_type","")).strip().casefold()
                    if typ: intervention_types[typ]+=1

            agg=d.get("aggregate_annot",{})
            if isinstance(agg,dict):
                for key,val in agg.items():
                    if key.endswith("_pos"): continue
                    if key.endswith("_annot"):
                        aggregate_targets[key]+=1
                        # Short target is annotation vector. Long target is dict of sentence triples.
                        if isinstance(val,list) and val and all(isinstance(x,(int,float,bool)) for x in val):
                            annotated_token_total += len(val)
                            annotated_token_positive += sum(1 for x in val if x)
                        elif isinstance(val,dict):
                            for _,triple in val.items():
                                if isinstance(triple,list) and len(triple)>=2 and isinstance(triple[1],list):
                                    labels=triple[1]
                                    annotated_token_total += len(labels)
                                    annotated_token_positive += sum(1 for x in labels if x)

    types=sorted(intervention_types)
    expected={
      "behavioral","biological","combination product","device","diagnostic test",
      "dietary supplement","drug","genetic","other","procedure","radiation"
    }

    out={
      "state":"DISTANT_CTO_ZENODO_FILE_AUDIT_PASS",
      "zenodo_record":"6497284",
      "doi":"10.5281/zenodo.6497284",
      "file_name":a.input.name,
      "md5":file_hash(a.input,"md5"),
      "sha256":file_hash(a.input,"sha256"),
      "bytes":a.input.stat().st_size,
      "records":records,
      "unique_nct_ids":len(nct_ids),
      "malformed_json_lines":malformed,
      "extraction_entries":extraction_entries,
      "intervention_type_count":len(types),
      "intervention_types":types,
      "intervention_type_counts":dict(sorted(intervention_types.items())),
      "expected_11_type_set_exact_match":set(types)==expected,
      "semantic_type_supervision_available":bool(types),
      "aggregate_annotation_target_keys":dict(sorted(aggregate_targets.items())),
      "aggregate_annotated_token_total":annotated_token_total,
      "aggregate_positive_token_total":annotated_token_positive,
      "output_contains_record_ids":False,
      "output_contains_raw_text":False,
      "weak_supervision_only":True
    }
    if out["md5"]!="e95e3984a9b46e340b90aeed262e12cc":
        raise RuntimeError("Zenodo MD5 mismatch")
    if malformed:
        raise RuntimeError(f"malformed JSON lines: {malformed}")
    if types and not out["expected_11_type_set_exact_match"]:
        raise RuntimeError(f"unexpected nonempty intervention type set: {types}")
    if not types:
        out["state"]="DISTANT_CTO_ZENODO_FILE_AUDIT_PASS_NO_SEMANTIC_TYPES_AVAILABLE"
        out["protocol_consequence"]="D5_11_WAY_WEAK_SEMANTIC_HEAD_MUST_BE_CANCELED_WITHOUT_REPLACEMENT"
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
