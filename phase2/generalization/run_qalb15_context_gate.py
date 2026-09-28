"""QALB-2015 L2 DEV context-aware structural runtime.

Reads RAW only. Gold/corrected text is not opened here.
No QALB text is intended for persistence in the project repository.
"""
from __future__ import annotations
import hashlib,json,subprocess
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/dev/QALB-2015-L2-Dev.sent.no_ids"
LICENSE=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/LICENSE.txt"
ART=ROOT/"artifacts"
EVENTS=ART/"QALB15_CONTEXT_RUNTIME_EVENTS.jsonl"
SUMMARY=ART/"QALB15_CONTEXT_RUNTIME_SUMMARY.json"

UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
SEED="phase2-qalb15-l2-context-v1"
SLICE_N=100

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def choose(lines):
    scored=[]
    for i,s in enumerate(lines,1):
        scored.append((sha_text(SEED+"|"+s),i,s))
    scored.sort()
    return scored[:min(SLICE_N,len(scored))]

def safe_morph(a):
    if not a:return None
    return {k:a.get(k) for k in ("pos","num","per","asp","mod","cas","stt","gen","vox")}

def build_events(source,generated,trace,line_id,line_hash):
    ops,total=align(source,generated)
    rows=[]
    for gi,g in enumerate(group_nonkeep(ops),1):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        kinds=[x["op"] for x in g]
        if srcs:
            lex=[x["lexical_index"] for x in srcs]
            lex_span=[min(lex),max(lex)+1]
        else:
            lex_span=[-1,-1]

        morph=[]
        for x in srcs:
            wi=x["whitespace_word_index"]
            diag=trace["morphology"][wi] if wi < len(trace["morphology"]) else None
            morph.append(safe_morph(diag.get("analysis") if diag else None))

        src_bases=[x["base"] for x in srcs]
        out_bases=[x["base"] for x in outs]
        cost=sum(float(x["cost"]) for x in g)
        paired=(len(src_bases)==len(out_bases) and len(src_bases)>0)
        sub_only=bool(kinds) and all(x=="SUB" for x in kinds)
        final_alif_each=paired and all(o==s+"ا" for s,o in zip(src_bases,out_bases))
        single=paired and len(src_bases)==1
        pos=(morph[0] or {}).get("pos") if single else None

        waw_alif_verb=(
            single and sub_only and cost<=0.25
            and src_bases[0].endswith("و")
            and out_bases[0]==src_bases[0]+"ا"
            and pos=="verb"
        )
        accusative_single=(
            single and sub_only and cost<=0.25
            and not src_bases[0].endswith("و")
            and out_bases[0]==src_bases[0]+"ا"
        )
        generic_final_alif=(
            paired and len(src_bases)<=3 and sub_only and cost<=0.60
            and final_alif_each
        )

        rows.append({
            "event_id":f"Q15D-{line_id:05d}-{gi:03d}",
            "line_id":line_id,
            "line_hash":line_hash,
            "source_lexical_span":lex_span,
            "event_type":kinds[0] if len(kinds)==1 else "COMPLEX",
            "primitive_ops":kinds,
            "event_cost":cost,
            "passage_alignment_cost":total,
            "source_bases":src_bases,
            "candidate_bases":out_bases,
            "source_bases_sha256":sha_text("\u241f".join(src_bases)),
            "candidate_bases_sha256":sha_text("\u241f".join(out_bases)),
            "source_morph":morph,
            "features":{
                "single_token":single,
                "substitution_only":sub_only,
                "all_final_alif_add":final_alif_each,
                "waw_alif_verb_only":waw_alif_verb,
                "accusative_alif_single":accusative_single,
                "generic_final_alif":generic_final_alif,
            },
            "runtime_decisions":{
                "WAW_ALIF_VERB_ONLY":"ACCEPT" if waw_alif_verb else "REVIEW",
                "ACCUSATIVE_ALIF_SINGLE":"DIAGNOSTIC" if accusative_single else "REVIEW",
                "FINAL_ALIF_GENERIC":"DIAGNOSTIC" if generic_final_alif else "REVIEW",
                "NUN_FAMILY":"REVIEW",
            }
        })
    return rows

def main():
    ART.mkdir(exist_ok=True)
    commit=subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()
    assert commit==UPSTREAM_COMMIT,(commit,UPSTREAM_COMMIT)
    assert RAW.exists() and LICENSE.exists()

    lines=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    selected=choose(lines)

    disambig=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    rows=[];changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[QALB15 L2 DEV {n}/{len(selected)}] line_id={line_id}",flush=True)
        generated,trace=generate_one(source,disambig,ged_tok,ged_model,gec_tok,gec_model)
        changed+=int(generated!=source)
        rows.extend(build_events(source,generated,trace,line_id,h))

    EVENTS.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    counts={}
    for p in ("WAW_ALIF_VERB_ONLY","ACCUSATIVE_ALIF_SINGLE","FINAL_ALIF_GENERIC"):
        key="ACCEPT" if p=="WAW_ALIF_VERB_ONLY" else "DIAGNOSTIC"
        counts[p]=sum(x["runtime_decisions"][p]==key for x in rows)

    safe_summary={
        "status":"QALB15_CONTEXT_RUNTIME_COMPLETE",
        "development_generalization_only":True,
        "upstream_repo":"CAMeL-Lab/arabic-gec",
        "upstream_commit":commit,
        "corpus":"QALB-2015 L2 DEV deterministic raw-only 100-line slice",
        "raw_file_git_blob_sha":"b9e5d7e4eed4da221c6360d9dfac697d0b2ffd95",
        "raw_file_sha256":sha_file(RAW),
        "license_file_sha256":sha_file(LICENSE),
        "selection_seed":SEED,
        "selected_line_ids":[i for _,i,_ in selected],
        "selected_line_hashes":[h for h,_,_ in selected],
        "selected_lines":len(selected),
        "changed_lines":changed,
        "runtime_events":len(rows),
        "policy_candidate_counts":counts,
        "gold_read_by_runtime":False,
        "qalb15_test_read":False,
        "qabl_text_persisted_to_repo":False,
        "model_stack":{"ged":GED_MODEL,"gec":GEC_MODEL}
    }
    SUMMARY.write_text(json.dumps(safe_summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in safe_summary.items() if k not in ("selected_line_hashes",)},ensure_ascii=False))

if __name__=="__main__":
    main()
