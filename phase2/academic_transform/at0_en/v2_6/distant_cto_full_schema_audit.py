#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,json,pathlib,re

KNOWN_TYPES={
"drug","other","device","behavioral","procedure","biological",
"dietary supplement","diagnostic test","radiation","genetic","combination product"
}
TYPE_KEY_PAT=re.compile(r"(type|class|semantic|category)",re.I)

def walk_keys(obj,prefix="",key_counter=None,string_values=None):
    if key_counter is None: key_counter=collections.Counter()
    if string_values is None: string_values=collections.Counter()
    if isinstance(obj,dict):
        for k,v in obj.items():
            p=f"{prefix}.{k}" if prefix else str(k)
            key_counter[p]+=1
            if TYPE_KEY_PAT.search(str(k)) and isinstance(v,(str,int,float,bool,type(None))):
                string_values[f"{p}={v}"]+=1
            walk_keys(v,p,key_counter,string_values)
    elif isinstance(obj,list):
        # sample structure, but recurse every dict; scalars aren't exported.
        for v in obj:
            if isinstance(v,(dict,list)):
                walk_keys(v,prefix+"[]",key_counter,string_values)
    return key_counter,string_values

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--file",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    h=hashlib.sha256(); md5=hashlib.md5()
    with open(a.file,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b); md5.update(b)
    if md5.hexdigest()!="e95e3984a9b46e340b90aeed262e12cc":
        raise RuntimeError(f"Zenodo MD5 mismatch {md5.hexdigest()}")

    rows=0; bad_json=0; ids=set(); duplicate_ids=0
    top=collections.Counter(); agg=collections.Counter(); type_like=collections.Counter()
    known_type_value_hits=0
    binary_annotation_lists=0
    nonbinary_annotation_lists=0
    annot_token_total=0
    for line in a.file.open(encoding="utf-8",errors="strict"):
        line=line.strip()
        if not line: continue
        try:d=json.loads(line)
        except Exception:
            bad_json+=1; continue
        rows+=1
        rid=str(d.get("id",""))
        if rid in ids: duplicate_ids+=1
        ids.add(rid)
        for k in d: top[k]+=1
        ag=d.get("aggregate_annot",{})
        if isinstance(ag,dict):
            for k in ag: agg[k]+=1
        kc,sv=walk_keys(d)
        for k,v in sv.items(): type_like[k]+=v
        # Check all primitive strings for exact known type values, without exporting raw text.
        stack=[d]
        while stack:
            x=stack.pop()
            if isinstance(x,dict): stack.extend(x.values())
            elif isinstance(x,list):
                # Annotation vectors in this resource occur as list of 0/1 ints paired with tokens.
                if x and all(isinstance(z,int) and z in (0,1) for z in x):
                    binary_annotation_lists+=1; annot_token_total+=len(x)
                elif x and all(isinstance(z,(int,float,bool)) for z in x):
                    nonbinary_annotation_lists+=1
                stack.extend(v for v in x if isinstance(v,(dict,list,str)))
            elif isinstance(x,str):
                if x.strip().casefold() in KNOWN_TYPES:
                    known_type_value_hits+=1

    subtype_field_present=bool(type_like or known_type_value_hits)
    out={
      "state":"DISTANT_CTO_FULL_SCHEMA_AUDIT_PASS",
      "file_sha256":h.hexdigest(),
      "file_md5":md5.hexdigest(),
      "json_rows":rows,
      "bad_json_rows":bad_json,
      "unique_record_ids":len(ids),
      "duplicate_record_ids":duplicate_ids,
      "top_level_key_counts":dict(sorted(top.items())),
      "aggregate_annot_key_counts":dict(sorted(agg.items())),
      "type_like_scalar_field_occurrences":sum(type_like.values()),
      "known_11_subtype_exact_value_hits":known_type_value_hits,
      "explicit_11_subtype_field_evidence":subtype_field_present,
      "binary_annotation_lists":binary_annotation_lists,
      "nonbinary_numeric_annotation_lists":nonbinary_annotation_lists,
      "binary_annotation_token_positions":annot_token_total,
      "raw_text_emitted":False,
      "record_ids_emitted":False,
      "scientific_training_performed":False,
      "decision_hint":(
        "D5_SEMANTIC_TYPE_SOURCE_EVIDENCE_PRESENT"
        if subtype_field_present else
        "D5_FROZEN_11_WAY_SEMANTIC_TYPE_LABELS_NOT_PRESENT_IN_RELEASED_WEAK_FILE"
      )
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
