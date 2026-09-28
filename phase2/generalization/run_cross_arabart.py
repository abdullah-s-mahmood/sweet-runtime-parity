"""Run frozen QALB14 AraBART generator on the same raw-only QALB15 L2 TRAIN slice.

No corrected/gold text is opened.
"""
from __future__ import annotations
import json,platform,subprocess
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer,BertForTokenClassification,MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.generalization.cross_model_common import (
    select_raw_lines,eventize,write_jsonl,sha_file,SEED,SLICE_N
)

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
LICENSE=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/LICENSE.txt"
ART=ROOT/"artifacts"
EVENTS=ART/"CROSS_ARABART_EVENTS.jsonl"
SUMMARY=ART/"CROSS_ARABART_SUMMARY.json"

UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"

def main():
    ART.mkdir(exist_ok=True)
    assert subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()==UPSTREAM_COMMIT
    selected,total_lines=select_raw_lines(RAW)

    dis=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    rows=[];changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[ARABART CROSS {n}/{len(selected)}] line={line_id}",flush=True)
        output,_=generate_one(source,dis,ged_tok,ged_model,gec_tok,gec_model)
        changed+=int(output!=source)
        rows.extend(eventize(source,output,line_id,h,"ARABART"))

    write_jsonl(EVENTS,rows)
    summary={
        "status":"CROSS_ARABART_RAW_RUNTIME_COMPLETE",
        "gold_read":False,
        "corpus":"QALB-2015 L2 TRAIN deterministic raw-only 50-line slice",
        "selection_seed":SEED,
        "slice_n":SLICE_N,
        "raw_total_lines":total_lines,
        "selected_line_ids":[i for _,i,_ in selected],
        "selected_line_hashes":[h for h,_,_ in selected],
        "changed_lines":changed,
        "event_rows":len(rows),
        "runtime":{
            "python":platform.python_version(),
            "torch":torch.__version__,
            "qalb_repo_commit":UPSTREAM_COMMIT,
            "ged_model":GED_MODEL,
            "gec_model":GEC_MODEL
        },
        "raw_sha256":sha_file(RAW),
        "license_sha256":sha_file(LICENSE),
        "qalb15_test_read":False,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="selected_line_hashes"},ensure_ascii=False))

if __name__=="__main__":
    main()
