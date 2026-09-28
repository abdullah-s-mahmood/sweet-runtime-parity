"""Validate a frozen FINAL_ALIF event policy on a deterministic ZAEBUC-v1.0 TRAIN slice.

Runtime stage reads raw TRAIN only. Gold/corrected text is forbidden here.
"""
from __future__ import annotations
import hashlib,json,platform,subprocess
from pathlib import Path
import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer,BertForTokenClassification,MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.arabart_audit.build_full_arabart_edit_queue import align,group_nonkeep
from phase2.full_event_acceptance.run_full_event_acceptance_gate import token_features

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.raw"
OUT=ROOT/"artifacts"/"ZAEBUC_TRAIN_FINAL_ALIF_RUNTIME_EVENTS.jsonl"
SUM=ROOT/"artifacts"/"ZAEBUC_TRAIN_FINAL_ALIF_RUNTIME.json"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
SEED="phase2-final-alif-v1"
N=30

def file_sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def choose(lines):
    ranked=[]
    for i,line in enumerate(lines,1):
        h=hashlib.sha256((SEED+"|"+line).encode("utf-8")).hexdigest()
        ranked.append((h,i,line))
    ranked.sort()
    return ranked[:N]

def build_events(source,generated,line_id,selection_hash):
    ops,total=align(source,generated)
    rows=[]
    for k,g in enumerate(group_nonkeep(ops),1):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        kinds=[x["op"] for x in g]
        typ=kinds[0] if len(g)==1 else "COMPLEX"
        if srcs:
            sa=min(x["span"][0] for x in srcs);sb=max(x["span"][1] for x in srcs)
            span=[sa,sb];st=source[sa:sb]
            li=[x["lexical_index"] for x in srcs]; lspan=[min(li),max(li)+1]
        else:
            span=[0,0];st="";lspan=[-1,-1]
        paired=len(srcs)==len(outs) and len(srcs)>0
        tf=[token_features(a["surface"],b["surface"]) for a,b in zip(srcs,outs)] if paired else []
        sub_only=bool(kinds) and all(x=="SUB" for x in kinds)
        all_final=paired and bool(tf) and all(x["final_alif_add"] for x in tf)
        event_cost=sum(float(x["cost"]) for x in g)
        main=(
            paired and sub_only and all_final and len(tf)<=3
            and event_cost<=0.60
        )
        single=(
            paired and sub_only and len(tf)==1 and all_final
            and event_cost<=0.25
        )
        rows.append({
            "event_id":f"ZTR-{line_id:03d}-{k:03d}",
            "original_line_id":line_id,
            "selection_hash":selection_hash,
            "event_type":typ,
            "primitive_ops":kinds,
            "source_span":span,
            "source_lexical_span":lspan,
            "source_text":st,
            "source_words":[x["surface"] for x in srcs],
            "source_bases":[x["base"] for x in srcs],
            "output_words":[x["surface"] for x in outs],
            "output_bases":[x["base"] for x in outs],
            "event_cost":event_cost,
            "passage_alignment_cost":total,
            "runtime_decisions":{
                "FINAL_ALIF_EVENT_ONLY":"ACCEPT" if main else "REVIEW",
                "FINAL_ALIF_SINGLE_ONLY":"ACCEPT" if single else "REVIEW",
            },
            "final_alif_features":{
                "paired":paired,"substitution_only":sub_only,
                "changed_token_count":len(tf),"all_final_alif_add":all_final
            }
        })
    return rows

def main():
    ROOT.joinpath("artifacts").mkdir(exist_ok=True)
    commit=subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()
    if commit!=UPSTREAM_COMMIT:raise RuntimeError(commit)
    lines=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    selected=choose(lines)

    dis=BERTUnfactoredDisambiguator.pretrained()
    gt=AutoTokenizer.from_pretrained(GED_MODEL)
    gm=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    ct=AutoTokenizer.from_pretrained(GEC_MODEL)
    cm=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    events=[];changed=0
    for n,(h,idx,src) in enumerate(selected,1):
        print(f"[ZAEBUC TRAIN {n}/{N}] original_line={idx}",flush=True)
        gen,_=generate_one(src,dis,gt,gm,ct,cm)
        changed+=int(gen!=src)
        events.extend(build_events(src,gen,idx,h))

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in events)+"\n",encoding="utf-8")
    counts={}
    for e in events:
        for p,d in e["runtime_decisions"].items():
            counts[p+":"+d]=counts.get(p+":"+d,0)+1
    obj={
        "status":"ZAEBUC_TRAIN_FINAL_ALIF_RUNTIME_COMPLETE",
        "development_generalization_only":True,
        "selection_seed":SEED,
        "selected_lines":N,
        "total_raw_lines":len(lines),
        "selected_line_ids":[x[1] for x in selected],
        "selected_hashes":[x[0] for x in selected],
        "raw_sha256":file_sha(RAW),
        "raw_blob_sha_git":"dedcfb04ccaf8cef147881b51dc6ddd092656c5a",
        "upstream_commit":commit,
        "changed_selected_lines":changed,
        "runtime_events":len(events),
        "decision_counts":counts,
        "gold_read_by_runtime":False,
        "zaebuc_test_read":False,
        "nun_family_auto_accept":False,
        "model_stack":{"ged":GED_MODEL,"gec":GEC_MODEL},
        "python":platform.python_version(),"torch":torch.__version__,
    }
    SUM.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":
    main()
