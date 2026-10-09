#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

NATIVE_CLASSES=("P","I","C","O")
TRIALSIEVE_TYPES=(
"Disease/Condition of Interest","Dosage","Drug Intervention","Follow-up period",
"Group Characteristic","Group Name","Intervention Administration","Intervention Duration",
"Intervention Frequency","Non-Pharmaceutical Intervention","Non-Study Drug",
"Outcome (Study Endpoint)","Quantitative Measurement","Sample Size","Side Effects",
"Statistical Significance","Study Duration","Study Years","Type of Quant. Measure","Units"
)
EVIDENCE_LABELS=("B-Outcome","I-Outcome","O")
PICO_TYPES=(
"age","condition","control","control-participants","cv-bin-abs","cv-bin-percent",
"cv-cont-mean","cv-cont-median","cv-cont-q1","cv-cont-q3","cv-cont-sd","eligibility",
"ethinicity","intervention","intervention-participants","iv-bin-abs","iv-bin-percent",
"iv-cont-mean","iv-cont-median","iv-cont-q1","iv-cont-q3","iv-cont-sd","location",
"outcome","outcome-Measure","total-participants"
)
WEAK_TYPES=("Behavioural","Biological","Combination Product","Device","Diagnostic Test","Dietary Supplement","Drug","Genetic","Procedure","Radiation","Other")
class AdapterError(Exception): pass

def adapt_native_picoc(spans):
    out=[]
    for x in spans:
        c=x["class"]
        if c not in NATIVE_CLASSES: raise AdapterError("native four-class adapter rejects non P/I/C/O class")
        out.append(dict(x,task="native_picoc",target=c))
    return out

def adapt_ebm_aux(spans):
    out=[]
    for x in spans:
        c=x["class"]
        if c not in ("P","I","O"): raise AdapterError("original EBM auxiliary adapter allows only P/I/O")
        out.append(dict(x,task="aux_ebm_pio",target=c))
    return out

def adapt_trialsieve(spans):
    out=[]
    for x in spans:
        t=x["type"]
        if t not in TRIALSIEVE_TYPES: raise AdapterError("unknown TrialSieve type")
        out.append(dict(x,task="aux_trialsieve20",target=t))
    return out

def adapt_evidence(tokens):
    out=[]
    for x in tokens:
        lab=x["label"]
        if lab not in EVIDENCE_LABELS: raise AdapterError("unknown EvidenceOutcomes label")
        out.append(dict(x,task="aux_evidence_outcome",target=lab))
    return out

def adapt_pico_corpus(spans):
    out=[]
    for x in spans:
        t=x["type"]
        if t not in PICO_TYPES: raise AdapterError("unknown PICO-Corpus native type")
        out.append(dict(x,task="aux_pico_corpus26",target=t))
    return out

def adapt_weak_mentions(mentions):
    out=[]
    for x in mentions:
        t=x["semantic_type"]
        if t not in WEAK_TYPES: raise AdapterError("unknown weak intervention semantic type")
        if x.get("role") in ("I","C"): raise AdapterError("DISTANT-CTO role promotion to native I/C is forbidden")
        out.append(dict(x,task="weak_intervention_semantic11",target=t))
    return out

def synthetic_preflight():
    native=adapt_native_picoc([
      {"document_id":"n1","start":0,"end":1,"class":"P"},
      {"document_id":"n1","start":2,"end":3,"class":"I"},
      {"document_id":"n1","start":4,"end":5,"class":"C"},
      {"document_id":"n1","start":6,"end":7,"class":"O"}])
    assert [x["target"] for x in native]==list(NATIVE_CLASSES)

    ebm=adapt_ebm_aux([
      {"document_id":"e1","start":0,"end":1,"class":"P"},
      {"document_id":"e1","start":2,"end":3,"class":"I"},
      {"document_id":"e1","start":4,"end":5,"class":"O"}])
    try:
        adapt_ebm_aux([{"document_id":"e2","start":0,"end":1,"class":"C"}]); raise RuntimeError("EBM C accepted")
    except AdapterError: pass

    ts=adapt_trialsieve([
      {"document_id":"t1","start":0,"end":1,"type":"Drug Intervention"},
      {"document_id":"t1","start":2,"end":3,"type":"Non-Study Drug"},
      {"document_id":"t1","start":4,"end":5,"type":"Outcome (Study Endpoint)"}])
    assert all(x["task"]=="aux_trialsieve20" for x in ts)
    assert not any(x.get("native_target") for x in ts)

    ev=adapt_evidence([{"token":"mortality","label":"B-Outcome"},{"token":"rate","label":"I-Outcome"},{"token":"was","label":"O"}])
    assert all(x["task"]=="aux_evidence_outcome" for x in ev)

    pc=adapt_pico_corpus([
      {"document_id":"p1","start":0,"end":1,"type":"control"},
      {"document_id":"p1","start":2,"end":3,"type":"intervention"},
      {"document_id":"p1","start":4,"end":5,"type":"outcome"}])
    assert all(x["task"]=="aux_pico_corpus26" for x in pc)
    assert not any(x.get("native_target") for x in pc)

    weak=adapt_weak_mentions([
      {"document_id":"w1","start":0,"end":1,"semantic_type":"Drug"},
      {"document_id":"w1","start":2,"end":3,"semantic_type":"Procedure"}])
    assert all(x["task"]=="weak_intervention_semantic11" for x in weak)
    try:
        adapt_weak_mentions([{"document_id":"w2","start":0,"end":1,"semantic_type":"Drug","role":"C"}]); raise RuntimeError("weak C role accepted")
    except AdapterError: pass

    failures=0
    tests=[
      (adapt_native_picoc,[{"document_id":"x","start":0,"end":1,"class":"X"}]),
      (adapt_trialsieve,[{"document_id":"x","start":0,"end":1,"type":"Comparator"}]),
      (adapt_evidence,[{"token":"x","label":"B-P"}]),
      (adapt_pico_corpus,[{"document_id":"x","start":0,"end":1,"type":"P"}]),
      (adapt_weak_mentions,[{"document_id":"x","start":0,"end":1,"semantic_type":"Comparator"}])]
    for fn,arg in tests:
        try: fn(arg)
        except AdapterError: failures+=1
    if failures!=5: raise RuntimeError("unknown-schema fail-closed mismatch")

    return {
      "state":"FEDERATION_ADAPTER_SYNTHETIC_PREFLIGHT_PASS",
      "scientific_data_used":False,
      "benchmark_gold_used":False,
      "native_classes":list(NATIVE_CLASSES),
      "original_ebm_aux_classes":["P","I","O"],
      "trialsieve_type_count":len(TRIALSIEVE_TYPES),
      "evidenceoutcomes_labels":list(EVIDENCE_LABELS),
      "pico_corpus_type_count":len(PICO_TYPES),
      "weak_semantic_type_count":len(WEAK_TYPES),
      "forbidden_mapping_checks":{
        "original_ebm_C_rejected":True,
        "trialsieve_nonstudy_drug_to_C_forbidden":True,
        "pico_corpus_26_to_native_forbidden":True,
        "weak_role_to_native_I_C_forbidden":True,
        "unknown_schema_fail_closed":True
      }
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight: raise SystemExit("Only synthetic preflight is authorized")
    d=synthetic_preflight()
    s=json.dumps(d,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(s,encoding="utf-8")
    print(s,end="")
if __name__=="__main__": main()
