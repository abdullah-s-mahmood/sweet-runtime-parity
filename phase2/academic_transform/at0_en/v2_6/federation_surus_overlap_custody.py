#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,importlib.util,json,pathlib,tarfile,collections

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def semicolon_rows(path):
    with open(path,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f,delimiter=";"))

def csv_rows(path,delimiter=","):
    with open(path,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f,delimiter=delimiter))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",type=pathlib.Path,required=True)
    ap.add_argument("--surus",type=pathlib.Path,required=True)
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--ebm",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--trialsieve",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    mapmod=load_module(a.project/"phase2/academic_transform/at0_en/v2_6/federation_ebm_pmid_mapping_custody.py","mapmod")
    targetmod=load_module(a.project/"phase2/academic_transform/at0_en/v2_6/federation_public_target_pmid_custody.py","targetmod")

    # SURUS
    srows=semicolon_rows(a.surus/"data/dataset/article.csv")
    surus_all={str(r.get("PubmedID","")).strip() for r in srows if str(r.get("PubmedID","")).strip()}
    surus_indomain={str(r["PubmedID"]).strip() for r in srows if r.get("Dataset")=="Indomain"}
    surus_ood=surus_all-surus_indomain
    if len(surus_all)!=523: raise RuntimeError(f"SURUS PMIDs expected 523 got {len(surus_all)}")

    # Protected historical EBM mapping.
    a.work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm/"ebm_nlp_2_00.tar.gz","r:gz") as tf: tf.extractall(a.work/"ebm_extract",filter="data")
    originals=mapmod.find_original_tokens(a.work/"ebm_extract")
    mod_docs=mapmod.parse_mod_docs(a.bids/"data/EBM-NLPmod/fold1/train.txt")
    mapped_rows=mapmod.map_docs(mod_docs,originals)
    mapped={x["document_index"]:x["pmid"] for x in mapped_rows if x["accepted"]}
    m=json.loads(a.r44_manifest.read_text())
    hist={
      "DESIGN":{mapped[i] for i in m["design_documents"] if i in mapped},
      "VERIFY_INTERNAL":{mapped[i] for i in m["verify_internal_documents"] if i in mapped},
      "OLD_SELECT":{mapped[i] for i in m["excluded_old_select_documents"] if i in mapped},
    }

    # Other public sources.
    pico={p.stem for p in (a.pico/"pico_corpus_brat_annotated_files").glob("*.txt") if p.stem.isdigit()}
    evidence=set()
    for fn in ["500RCT-CoNLL.tsv","140EBMNLP-CoNLL.tsv"]:
        with open(a.evidence/fn,encoding="utf-8",newline="") as f:
            for row in csv.reader(f,delimiter="\t"):
                if len(row)==5 and row[1].strip().isdigit(): evidence.add(row[1].strip())
    trial=json.loads((a.trialsieve/"data/processed_for_modeling.json").read_text())
    trial_trainval={str(x.get("pmid","")).strip() for x in trial if x.get("split") in ("train","validation") and str(x.get("pmid","")).strip()}

    # Resolve AD/COVID exact normalized titles again inside custody; emit counts only.
    targets={}
    cache={}
    for corpus in ("AD","COVID-19"):
        docs,test_hashes=targetmod.load_target_unique(a.bids,corpus)
        resolved={}
        reasons=collections.Counter()
        for hh,blocks in sorted(docs.items()):
            title=targetmod.extract_title(blocks)
            if not title: reasons["NO_TITLE"]+=1; continue
            nt=targetmod.norm_title(title)
            if nt not in cache:
                cache[nt]=targetmod.resolve_title(title)
                import time; time.sleep(.36)
            pmid,reason=cache[nt]; reasons[reason]+=1
            if pmid: resolved[hh]=pmid
        targets[corpus]={
          "whole":set(resolved.values()),
          "test":{resolved[h] for h in test_hashes if h in resolved},
          "resolved_whole":len(resolved),
          "resolved_test":sum(h in resolved for h in test_hashes),
          "reasons":dict(reasons)
        }

    def compare(s):
        out={}
        for k,v in hist.items(): out[k]=len(s&v)
        out["PICO_CORPUS"]=len(s&pico)
        out["EVIDENCEOUTCOMES"]=len(s&evidence)
        out["TRIALSIEVE_TRAIN_VALIDATION"]=len(s&trial_trainval)
        for corpus,t in targets.items():
            out[f"{corpus}_RESOLVED_WHOLE"]=len(s&t["whole"])
            out[f"{corpus}_RESOLVED_TEST"]=len(s&t["test"])
        return out

    out={
      "state":"FEDERATION_SURUS_OVERLAP_CUSTODY_AUDIT_PASS",
      "surus":{"all":523,"indomain":len(surus_indomain),"ood":len(surus_ood)},
      "historical_mapped_coverage":{k:len(v) for k,v in hist.items()},
      "target_resolution":{k:{"resolved_whole":v["resolved_whole"],"resolved_test":v["resolved_test"],"reasons":v["reasons"]} for k,v in targets.items()},
      "overlap_counts":{
        "SURUS_ALL":compare(surus_all),
        "SURUS_INDOMAIN":compare(surus_indomain),
        "SURUS_OOD":compare(surus_ood)
      },
      "pmid_values_emitted":False,
      "protected_ids_emitted":False,
      "raw_text_emitted":False,
      "limitations":[
        "PMID equality is not full trial-family identity.",
        "AD/COVID title resolution remains partial.",
        "Historical EBM mapping remains partial.",
        "Any SURUS inclusion must still use per-fold family decontamination."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
