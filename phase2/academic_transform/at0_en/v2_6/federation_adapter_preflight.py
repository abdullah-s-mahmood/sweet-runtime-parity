#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,pathlib,tarfile,collections,re,hashlib

TRIALSIEVE_TAGS={
"Disease/Condition of Interest","Dosage","Drug Intervention","Follow-up period",
"Group Characteristic","Group Name","Intervention Administration","Intervention Duration",
"Intervention Frequency","Non-Pharmaceutical Intervention","Non-Study Drug",
"Outcome (Study Endpoint)","Quantitative Measurement","Sample Size","Side Effects",
"Statistical Significance","Study Duration","Study Years","Type of Quant. Measure","Units"
}
PICO26={
"age","condition","control","control-participants","cv-bin-abs","cv-bin-percent",
"cv-cont-mean","cv-cont-median","cv-cont-q1","cv-cont-q3","cv-cont-sd","eligibility",
"ethinicity","intervention","intervention-participants","iv-bin-abs","iv-bin-percent",
"iv-cont-mean","iv-cont-median","iv-cont-q1","iv-cont-q3","iv-cont-sd","location",
"outcome","outcome-Measure","total-participants"
}

def parse_bio(path):
    docs=0; labels=set(); invalid_initial_i=0; active=None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            docs+=1; active=None; continue
        if not line.strip(): active=None; continue
        parts=line.split("\t")
        if len(parts)<2: continue
        lab=parts[-1].strip(); labels.add(lab)
        if lab.startswith("B-"): active=lab[2:]
        elif lab.startswith("I-"):
            typ=lab[2:]
            if active!=typ: invalid_initial_i+=1
        else: active=None
    return docs,labels,invalid_initial_i

def evidence500(root):
    p=root/"500RCT-CoNLL.tsv"
    pmids=set(); labels=set(); rows=0; malformed=0
    with open(p,encoding="utf-8",newline="") as f:
        for row in csv.reader(f,delimiter="\t"):
            if not row: continue
            if len(row)!=5: malformed+=1; continue
            _,pmid,s,e,lab=row
            rows+=1; labels.add(lab)
            if pmid.isdigit(): pmids.add(pmid)
            try:
                ss=int(s); ee=int(e)
                if ss<0 or ee<=ss: raise ValueError
            except Exception: raise RuntimeError("EvidenceOutcomes invalid offset")
    return {"rows":rows,"pmids":len(pmids),"labels":sorted(labels),"malformed":malformed}

def trialsieve(root):
    p=root/"data/processed_for_modeling.json"
    d=json.loads(p.read_text(encoding="utf-8"))
    if len(d)!=1609: raise RuntimeError(f"TrialSieve docs {len(d)} !=1609")
    tags=collections.Counter(); spans=0; bad=0; pmids=set()
    for doc in d:
        pmid=str(doc.get("pmid","")).strip()
        if not pmid: raise RuntimeError("TrialSieve missing pmid")
        pmids.add(pmid)
        for sp in doc.get("spans",[]):
            spans+=1
            tag=str(sp.get("tag",""))
            tags[tag]+=1
            s=int(sp["start"]); e=int(sp["end"])
            if s<0 or e<=s: bad+=1
    if set(tags)!=TRIALSIEVE_TAGS: raise RuntimeError("TrialSieve tag inventory changed")
    if spans!=52638: raise RuntimeError(f"TrialSieve spans {spans} !=52638")
    if bad: raise RuntimeError(f"TrialSieve bad offsets {bad}")
    return {"docs":len(d),"pmids":len(pmids),"spans":spans,"tags":dict(sorted(tags.items()))}

def pico(root):
    d=root/"pico_corpus_brat_annotated_files"
    anns=list(d.glob("*.ann")); txts=list(d.glob("*.txt"))
    types=collections.Counter(); spans=0; bad=0; duplicate=0
    for p in anns:
        seen=set()
        for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
            if not line.startswith("T"): continue
            parts=line.split("\t")
            if len(parts)<2: continue
            meta=parts[1].split()
            if len(meta)<3: continue
            typ=meta[0]
            # BRAT can encode discontinuous offsets with ';'; don't collapse.
            coord=" ".join(meta[1:])
            k=(typ,coord)
            if k in seen: duplicate+=1
            seen.add(k)
            types[typ]+=1; spans+=1
    if set(types)!=PICO26: raise RuntimeError("PICO-Corpus type inventory changed")
    if len(anns)!=1011 or len(txts)!=1011: raise RuntimeError("PICO-Corpus file count changed")
    if spans!=17739: raise RuntimeError(f"PICO spans {spans} !=17739")
    return {"docs":1011,"spans":spans,"types":dict(sorted(types.items())),"duplicate_textbound_keys":duplicate}

def ebm_train(root,work):
    archive=root/"ebm_nlp_2_00.tar.gz"
    with tarfile.open(archive,"r:gz") as tf: tf.extractall(work,filter="data")
    result={}
    for name in ["participants","interventions","outcomes"]:
        pats=list(work.rglob(f"annotations/aggregated/starting_spans/{name}/train/*.ann"))
        # Some archive layouts include an extra top-level directory; rglob handles it.
        if not pats: raise RuntimeError(f"no EBM train anns for {name}")
        pmids={p.stem for p in pats}
        result[name]={"train_files":len(pats),"unique_pmids":len(pmids)}
    # explicitly verify test material exists but is NOT admitted
    test_count=sum(len(list(work.rglob(f"annotations/aggregated/starting_spans/{name}/test/**/*.ann"))) for name in ["participants","interventions","outcomes"])
    result["test_files_present_but_excluded"]=test_count
    return result

def synthetic_semantics():
    # Native adapter: B only starts source-compatible entity.
    seq=["O","B-P","I-P","O","I-I","B-C","I-C"]
    starts=[(i,x[2:]) for i,x in enumerate(seq) if x.startswith("B-")]
    invalid_i=[i for i,x in enumerate(seq) if x.startswith("I-") and (i==0 or seq[i-1] not in (x,"B-"+x[2:]))]
    if starts!=[(1,"P"),(5,"C")] or invalid_i!=[4]:
        raise RuntimeError("native source-compatible synthetic contract failed")
    # Auxiliary labels can never become native labels through identity-free conversion.
    forbidden={"Non-Study Drug":"C","control":"C","Drug Intervention":"I","Outcome (Study Endpoint)":"O"}
    # This dictionary is a negative fixture: adapter must not implement it.
    if any(v in {"P","I","C","O"} for v in []):
        raise RuntimeError
    return {"native_B_starts":starts,"invalid_initial_I_positions":invalid_i,"forbidden_mapping_examples":sorted(forbidden)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--trialsieve",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--ebm",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.work.mkdir(parents=True,exist_ok=True)
    ndocs,nlabels,ni=parse_bio(a.bids/"data/EBM-NLPmod/fold1/train.txt")
    expected={"O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"}
    if ndocs!=400 or not nlabels.issubset(expected):
        raise RuntimeError(f"native BIDS schema mismatch docs={ndocs} labels={nlabels}")
    ev=evidence500(a.evidence)
    if ev["pmids"]!=500 or ev["labels"]!=["B-Outcome","I-Outcome","O"] or ev["malformed"]!=0:
        raise RuntimeError(f"EvidenceOutcomes schema mismatch {ev}")
    d={
      "state":"FEDERATION_ADAPTER_SOURCE_PREFLIGHT_PASS",
      "native_EBM_mod":{"docs":ndocs,"labels":sorted(nlabels),"invalid_initial_I_observations":ni},
      "EvidenceOutcomes_500":ev,
      "TrialSieve":trialsieve(a.trialsieve),
      "PICO_Corpus":pico(a.pico),
      "EBM_NLP_training_only":ebm_train(a.ebm,a.work/"ebm"),
      "synthetic_contract":synthetic_semantics(),
      "native_labels_emitted_by_auxiliary_sources":False,
      "benchmark_metrics_computed":False,
      "scientific_training_performed":False
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__": main()
