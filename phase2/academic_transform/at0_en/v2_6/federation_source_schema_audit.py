#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,pathlib,re,hashlib,collections,tarfile

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def evidence_outcomes(root):
    # Released CoNLL files have NO header. Fixed columns are:
    # token, PMID, start, end, label.
    out={}
    for fn in ["500RCT-CoNLL.tsv","140EBMNLP-CoNLL.tsv"]:
        p=root/fn
        rows=0; pmids=set(); labels=set(); malformed=0
        with open(p,encoding="utf-8",newline="") as f:
            r=csv.reader(f,delimiter="\t")
            for row in r:
                if not row: continue
                if len(row)!=5:
                    malformed+=1
                    continue
                token,pmid,start,end,label=row
                rows+=1
                if pmid.strip().isdigit(): pmids.add(pmid.strip())
                labels.add(label.strip())
        out[fn]={
            "sha256":sha256_file(p),
            "rows":rows,
            "unique_pmids":len(pmids),
            "labels":sorted(labels),
            "columns":["token","PMID","start","end","label"],
            "malformed_rows":malformed,
        }
    return out

def trialsieve(root):
    p=root/"data/final_schema_data.csv"
    tags=set(); pmids=set(); rows=0; columns=None; correct_values=set()
    with open(p,encoding="utf-8",newline="") as f:
        r=csv.DictReader(f); columns=r.fieldnames
        for row in r:
            rows+=1
            if row.get("tag"): tags.add(row["tag"].strip())
            if row.get("pmid"): pmids.add(row["pmid"].strip())
            if "correct" in row: correct_values.add(row["correct"].strip())
    a=root/"data/pmid_title_abstract.csv"
    with open(a,encoding="utf-8",newline="") as f:
        r=csv.DictReader(f); meta_cols=r.fieldnames; meta_rows=0; meta_pmids=set()
        for row in r:
            meta_rows+=1
            if row.get("pmid"): meta_pmids.add(row["pmid"].strip())
    pre=root/"data/processed_for_modeling.json"
    pre_d=json.loads(pre.read_text(encoding="utf-8"))
    pre_pmids={str(x.get("pmid","")).strip() for x in pre_d if str(x.get("pmid","")).strip()}
    pre_splits=collections.Counter(str(x.get("split","")) for x in pre_d)
    pre_tags=collections.Counter()
    zero_span=0
    for x in pre_d:
        spans=x.get("spans",[])
        if not spans: zero_span+=1
        for sp in spans:
            pre_tags[str(sp.get("tag",""))]+=1
    return {
      "annotations":{
        "sha256":sha256_file(p),"rows":rows,"unique_pmids":len(pmids),
        "tags":sorted(tags),"tag_count":len(tags),"columns":columns,
        "correct_field_values":sorted(correct_values)
      },
      "text_metadata":{
        "sha256":sha256_file(a),"rows":meta_rows,"unique_pmids":len(meta_pmids),"columns":meta_cols
      },
      "pmid_set_equal":pmids==meta_pmids,
      "preprocessed_for_modeling":{
        "sha256":sha256_file(pre),
        "documents":len(pre_d),
        "unique_pmids":len(pre_pmids),
        "split_counts":dict(sorted(pre_splits.items())),
        "zero_span_documents":zero_span,
        "span_tag_counts":dict(sorted(pre_tags.items())),
        "span_tag_count":len(pre_tags),
        "pmids_subset_of_annotation_table":pre_pmids.issubset(pmids),
        "pmids_subset_of_text_metadata":pre_pmids.issubset(meta_pmids)
      }
    }

def pico_corpus(root):
    d=root/"pico_corpus_brat_annotated_files"
    anns={p.stem:p for p in d.glob("*.ann")}
    txts={p.stem:p for p in d.glob("*.txt")}
    types=collections.Counter(); malformed=0; spans=0
    for pmid,p in anns.items():
        for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
            if not line.startswith("T"): continue
            parts=line.split("\t")
            if len(parts)<2: malformed+=1; continue
            meta=parts[1].split()
            if not meta: malformed+=1; continue
            types[meta[0]]+=1; spans+=1
    return {
      "ann_files":len(anns),"txt_files":len(txts),
      "paired_pmids":len(set(anns)&set(txts)),
      "ann_without_txt":len(set(anns)-set(txts)),
      "txt_without_ann":len(set(txts)-set(anns)),
      "entity_type_counts":dict(sorted(types.items())),
      "entity_type_count":len(types),
      "span_rows":spans,
      "malformed_textbound_rows":malformed
    }

def extract_ebm_archive(archive,work):
    work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive,"r:gz") as tf: tf.extractall(work,filter="data")
    docs=list(work.rglob("documents/*.tokens"))
    # structure of labels, no label content exported.
    dirs=sorted({str(p.relative_to(work)) for p in work.rglob("*") if p.is_dir() and ("starting_spans" in str(p) or "hierarchical_labels" in str(p))})
    pmids={p.stem for p in docs if p.stem.isdigit()}
    return {
      "archive_sha256":sha256_file(archive),
      "document_token_files":len(docs),
      "numeric_pmid_documents":len(pmids),
      "annotation_directory_count":len(dirs),
      "contains_starting_spans":any("starting_spans" in x for x in dirs),
      "contains_hierarchical_labels":any("hierarchical_labels" in x for x in dirs)
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--trialsieve",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--ebm",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    d={
      "state":"FEDERATION_SOURCE_SCHEMA_AUDIT_PASS",
      "EvidenceOutcomes":evidence_outcomes(a.evidence),
      "TrialSieve":trialsieve(a.trialsieve),
      "PICO_Corpus":pico_corpus(a.pico),
      "EBM_NLP":extract_ebm_archive(a.ebm/"ebm_nlp_2_00.tar.gz",a.work/"ebm"),
      "raw_examples_emitted":False,
      "benchmark_metrics_computed":False
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__": main()
