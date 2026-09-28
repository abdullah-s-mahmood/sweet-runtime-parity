"""Run the frozen QALB14 AraBART generator and frozen full-event gate on ZAEBUC-v1.0 Arabic DEV.

GENERALIZATION DEVELOPMENT ONLY.
This runtime stage reads only ZAEBUC raw DEV input. It does not read corrected
DEV text, M2 gold, Nahw targets, or project adjudication labels.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, subprocess
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep
from phase2.full_event_acceptance.run_full_event_acceptance_gate import event_features, decisions

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/dev/dev.sent.raw"
LIC=UP/"data/gec/ZAEBUC-v1.0/LICENCE.txt"
OUT=ROOT/"artifacts"/"ZAEBUC_DEV_RUNTIME_EVENTS.jsonl"
RUN=ROOT/"artifacts"/"ZAEBUC_DEV_RUNTIME_SUMMARY.json"

GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def build_events(text,generated,line_id):
    ops,total=align(text,generated)
    groups=group_nonkeep(ops)
    rows=[]
    for k,g in enumerate(groups,1):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        kinds=[x["op"] for x in g]
        typ=kinds[0] if len(g)==1 else "COMPLEX"
        if srcs:
            sa=min(x["span"][0] for x in srcs); sb=max(x["span"][1] for x in srcs)
            src_span=[sa,sb]; src_text=text[sa:sb]
            lex=[x["lexical_index"] for x in srcs]
            lex_span=[min(lex),max(lex)+1]
        else:
            pos=0
            idx=ops.index(g[0])
            for prev in reversed(ops[:idx]):
                if prev["src"]:
                    pos=prev["src"]["span"][1];break
            src_span=[pos,pos];src_text="";lex_span=[-1,-1]
        base_event={
            "event_id":f"ZDEV-{line_id:03d}-{k:03d}",
            "line_id":line_id,
            "event_type":typ,
            "primitive_ops":kinds,
            "source_span":src_span,
            "source_lexical_span":lex_span,
            "source_text":src_text,
            "source_words":[x["surface"] for x in srcs],
            "source_bases":[x["base"] for x in srcs],
            "output_words":[x["surface"] for x in outs],
            "output_bases":[x["base"] for x in outs],
            "event_cost":sum(float(x["cost"]) for x in g),
            "passage_alignment_cost":total,
        }
        # event_features expects the same AraBART field names as the development queue.
        ef_input={
            "source_words":base_event["source_words"],
            "arabart_words":base_event["output_words"],
            "primitive_ops":base_event["primitive_ops"],
            "event_cost":base_event["event_cost"],
        }
        feat=event_features(ef_input)
        base_event["features"]=feat
        base_event["runtime_decisions"]=decisions(feat)
        rows.append(base_event)
    return rows

def main():
    ROOT.joinpath("artifacts").mkdir(exist_ok=True)
    commit=subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()
    if commit!=UPSTREAM_COMMIT: raise RuntimeError(f"upstream pin mismatch {commit}")
    if not RAW.exists() or not LIC.exists(): raise RuntimeError("ZAEBUC raw/license missing")

    lines=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines: raise RuntimeError("ZAEBUC DEV raw empty")

    disambig=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    rows=[]; changed=0
    for i,source in enumerate(lines,1):
        print(f"[ZAEBUC DEV {i}/{len(lines)}]",flush=True)
        generated,_=generate_one(source,disambig,ged_tok,ged_model,gec_tok,gec_model)
        changed+=int(generated!=source)
        rows.extend(build_events(source,generated,i))

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    counts={}
    for x in rows:
        for p,d in x["runtime_decisions"].items():
            counts[p+":"+d]=counts.get(p+":"+d,0)+1
    summary={
        "status":"ZAEBUC_DEV_GENERALIZATION_RUNTIME_COMPLETE",
        "development_generalization_only":True,
        "external_corpus":"ZAEBUC-v1.0 Arabic DEV",
        "external_license":"CC BY-NC-SA 4.0",
        "upstream_repo":"CAMeL-Lab/arabic-gec",
        "upstream_commit":commit,
        "raw_blob_sha_git":"690dc49ea3b278d7d5c1ebcdec2bbb7468bc7bd5",
        "raw_sha256":sha256(RAW),
        "license_sha256":sha256(LIC),
        "raw_lines":len(lines),
        "changed_lines":changed,
        "event_rows":len(rows),
        "runtime_decision_counts":counts,
        "gold_read_by_runtime":False,
        "model_stack":{"ged":GED_MODEL,"gec":GEC_MODEL},
        "python":platform.python_version(),
        "torch":torch.__version__,
        "test_split_read":False,
        "rules_frozen_before_gold":True,
    }
    RUN.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
