#!/usr/bin/env python3
from __future__ import annotations

import argparse,csv,glob,json,pathlib,re,tarfile,collections

PICO=("P","I","C","O")

def runs_from_bio(labels):
    spans=[]
    open_type=None; start=None
    invalid_i=0
    for i,label in enumerate(labels+["O"]):
        if label=="O":
            if open_type is not None:
                spans.append((start,i,open_type))
                open_type=None; start=None
            continue
        if "-" not in label:
            raise ValueError(f"invalid BIO label {label}")
        pref,typ=label.split("-",1)
        if typ not in PICO:
            raise ValueError(f"unexpected PICO type {typ}")
        if pref=="B":
            if open_type is not None:
                spans.append((start,i,open_type))
            open_type=typ; start=i
        elif pref=="I":
            if open_type==typ:
                continue
            # Source-compatible rule: invalid I does NOT create a new entity.
            invalid_i+=1
            if open_type is not None:
                spans.append((start,i,open_type))
                open_type=None; start=None
        else:
            raise ValueError(f"unexpected prefix {pref}")
    return spans,invalid_i

def audit_bids_native(path):
    docs=[]; toks=[]; labs=[]; invalid_total=0; counts=collections.Counter()
    started=False
    def flush():
        nonlocal toks,labs,invalid_total
        if not started: return
        if not toks:
            return
        spans,inv=runs_from_bio(labs)
        invalid_total+=inv
        for _,_,c in spans: counts[c]+=1
        docs.append({"tokens":len(toks),"spans":len(spans)})
        toks=[]; labs=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            flush(); started=True; continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        parts=line.split("\t")
        if len(parts)!=2: raise ValueError("BIDS train line not 2-column")
        toks.append(parts[0]); labs.append(parts[1])
    flush()
    if len(docs)!=400: raise RuntimeError(f"expected 400 EBM_mod train docs got {len(docs)}")
    return {
      "documents":len(docs),
      "span_counts":dict(sorted(counts.items())),
      "invalid_initial_or_type_mismatched_I_fragments":invalid_total,
      "total_spans":sum(counts.values())
    }

def audit_evidence(root):
    result={}
    for fn in ("500RCT-CoNLL.tsv","140EBMNLP-CoNLL.tsv"):
        docs=collections.defaultdict(list)
        with open(root/fn,encoding="utf-8",newline="") as f:
            for row in csv.reader(f,delimiter="\t"):
                if not row: continue
                if len(row)!=5: raise ValueError(f"{fn}: malformed row")
                token,pmid,start,end,label=row
                if label not in {"B-Outcome","I-Outcome","O"}:
                    raise ValueError(f"{fn}: unexpected label {label}")
                docs[pmid].append((token,int(start),int(end),label))
        spans=0; invalid_i=0
        for pmid,rows in docs.items():
            labels=[{"B-Outcome":"B-O","I-Outcome":"I-O","O":"O"}[x[3]] for x in rows]
            ss,inv=runs_from_bio(labels)
            invalid_i+=inv; spans+=len(ss)
            # Validate monotonic released offsets; do not reconstruct text.
            last=-1
            for _,s,e,_ in rows:
                if s<0 or e<=s or s<last: raise ValueError(f"{fn}: bad offsets")
                last=s
        result[fn]={
          "documents":len(docs),
          "outcome_spans":spans,
          "invalid_I_fragments":invalid_i,
          "training_role":"AUXILIARY_O_ONLY"
        }
    return result

def audit_trialsieve(root):
    p=root/"data/processed_for_modeling.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    split=collections.Counter(); tags=collections.Counter(); train_docs=0; heldout_test=0; bad=0
    for d in data:
        sp=str(d.get("split",""))
        split[sp]+=1
        if sp=="test":
            heldout_test+=1
            continue
        if sp not in {"train","validation"}:
            raise ValueError(f"unexpected TrialSieve split {sp}")
        train_docs+=1
        text=d.get("text","")
        for s in d.get("spans",[]):
            st=int(s["start"]); en=int(s["end"]); tag=str(s["tag"])
            if st<0 or en<=st or en>len(text): bad+=1
            tags[tag]+=1
    if bad: raise RuntimeError(f"TrialSieve invalid spans={bad}")
    if len(tags)!=20: raise RuntimeError(f"TrialSieve train/val tag count={len(tags)}")
    if train_docs!=1371 or heldout_test!=238:
        raise RuntimeError(f"TrialSieve split mismatch trainval={train_docs} test={heldout_test}")
    return {
      "canonical_documents":len(data),
      "train_validation_documents_admitted":train_docs,
      "test_documents_excluded":heldout_test,
      "split_counts":dict(sorted(split.items())),
      "admitted_span_tag_count":len(tags),
      "admitted_span_counts":dict(sorted(tags.items())),
      "nonstudydrug_maps_to_C":False,
      "training_role":"AUXILIARY_NATIVE_20_TYPE"
    }

def audit_pico(root):
    d=root/"pico_corpus_brat_annotated_files"
    types=collections.Counter(); spans=0; docs=0; bad=0
    for txt in sorted(d.glob("*.txt")):
        ann=txt.with_suffix(".ann")
        if not ann.exists(): raise RuntimeError("PICO text missing ann")
        text=txt.read_text(encoding="utf-8",errors="replace")
        docs+=1
        for line in ann.read_text(encoding="utf-8",errors="replace").splitlines():
            if not line.startswith("T"): continue
            parts=line.split("\t")
            if len(parts)<2: bad+=1; continue
            meta=parts[1].split()
            if len(meta)<3: bad+=1; continue
            typ=meta[0]
            # BRAT can technically support discontinuous spans with ';'.
            if ";" in parts[1]:
                # Keep native provenance but first-campaign contiguous head cannot train this row.
                continue
            try: st=int(meta[1]); en=int(meta[2])
            except: bad+=1; continue
            if st<0 or en<=st or en>len(text): bad+=1; continue
            types[typ]+=1; spans+=1
    if docs!=1011: raise RuntimeError(f"PICO corpus docs {docs}")
    if bad: raise RuntimeError(f"PICO malformed/invalid spans {bad}")
    if len(types)!=26: raise RuntimeError(f"PICO type count {len(types)}")
    return {
      "documents":docs,
      "contiguous_spans_admitted":spans,
      "native_type_count":len(types),
      "native_type_counts":dict(sorted(types.items())),
      "collapsed_to_four_class":False,
      "training_role":"AUXILIARY_NATIVE_26_TYPE"
    }

def condense_binary(labels):
    spans=[]; start=None
    for i,x in enumerate(labels+["0"]):
        active=str(x)!="0"
        if active and start is None: start=i
        if not active and start is not None:
            spans.append((start,i)); start=None
    return spans

def audit_original_ebm(archive,work):
    work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive,"r:gz") as tf: tf.extractall(work,filter="data")
    tops=[p for p in work.rglob("annotations") if p.is_dir()]
    if not tops: raise RuntimeError("EBM annotations root not found")
    # Select extraction root that contains aggregated/starting_spans.
    top=None
    for p in tops:
        if (p/"aggregated"/"starting_spans").exists():
            top=p.parent; break
    if top is None: raise RuntimeError("EBM starting_spans root not found")
    docs_dir=top/"documents"
    out={}
    test_files_touched=0
    for pio in ("participants","interventions","outcomes"):
        train_dir=top/"annotations"/"aggregated"/"starting_spans"/pio/"train"
        test_dir=top/"annotations"/"aggregated"/"starting_spans"/pio/"test"/"gold"
        if not train_dir.exists() or not test_dir.exists():
            raise RuntimeError(f"missing EBM dirs for {pio}")
        files=sorted(train_dir.glob("*.ann"))
        spans=0; invalid_len=0; pmids=set()
        for ann in files:
            pmid=ann.stem.split("_")[0]
            tok=docs_dir/f"{pmid}.tokens"
            if not tok.exists(): raise RuntimeError(f"missing tokens {pmid}")
            labels=ann.read_text().split()
            tokens=tok.read_text(encoding="utf-8",errors="replace").split()
            if len(labels)!=len(tokens):
                invalid_len+=1; continue
            spans+=len(condense_binary(labels)); pmids.add(pmid)
        if invalid_len: raise RuntimeError(f"EBM {pio} train length mismatches={invalid_len}")
        # Never read test/gold contents; count directory entries only.
        test_count=sum(1 for _ in test_dir.glob("*.ann"))
        out[pio]={
          "train_documents":len(pmids),
          "train_annotation_files":len(files),
          "train_spans":spans,
          "expert_test_files_reserved_not_read":test_count
        }
    return {"elements":out,"training_role":"AUXILIARY_NATIVE_P_I_O","expert_test_content_read":False}

def synthetic_contract():
    spans,inv=runs_from_bio(["B-P","I-P","O","I-I","O","B-C","I-C"])
    if spans!=[(0,2,"P"),(5,7,"C")] or inv!=1:
        raise RuntimeError("source-compatible BIO fixture failed")
    return {"source_compatible_B_start_fixture":True,"invalid_I_does_not_create_entity":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--trialsieve",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--ebm",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    result={
      "state":"FEDERATION_ADAPTER_EXECUTABLE_PREFLIGHT_PASS",
      "synthetic_contract":synthetic_contract(),
      "native_EBM_NLP_mod":audit_bids_native(a.bids/"data/EBM-NLPmod/fold1/train.txt"),
      "EvidenceOutcomes":audit_evidence(a.evidence),
      "TrialSieve":audit_trialsieve(a.trialsieve),
      "PICO_Corpus":audit_pico(a.pico),
      "Original_EBM_NLP":audit_original_ebm(a.ebm/"ebm_nlp_2_00.tar.gz",a.work/"ebm"),
      "benchmark_test_metrics_computed":False,
      "AD_COVID_test_labels_read":False,
      "EBM_expert_test_contents_read":False,
      "raw_examples_emitted":False
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
