"""Run official SWEET NoPnx iteration-1 on a raw-only QALB15 L2 TRAIN slice.

No corrected/gold text is opened.
"""
from __future__ import annotations
import json,platform,subprocess,sys,time,resource
from pathlib import Path

import torch
from transformers import BertTokenizer,BertForTokenClassification

from phase2.generalization.cross_model_common import (
    select_raw_lines,eventize,write_jsonl,sha_file,SEED,SLICE_N
)

ROOT=Path(__file__).resolve().parents[2]
UP_QALB=ROOT/"upstream"/"arabic-gec"
UP_SWEET=ROOT/"upstream"/"text-editing"
RAW=UP_QALB/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
LICENSE=UP_QALB/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/LICENSE.txt"
MODEL=ROOT/"models"/"cross_sweet_nopnx"
ART=ROOT/"artifacts"
EVENTS=ART/"CROSS_SWEET_EVENTS.jsonl"
SUMMARY=ART/"CROSS_SWEET_SUMMARY.json"

QALB_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
SWEET_COMMIT="4d552ca3ae98029550f27fc52aa1b22883e16e61"
MODEL_SHA="584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6"

def main():
    ART.mkdir(exist_ok=True)
    assert subprocess.check_output(["git","-C",str(UP_QALB),"rev-parse","HEAD"],text=True).strip()==QALB_COMMIT
    assert subprocess.check_output(["git","-C",str(UP_SWEET),"rev-parse","HEAD"],text=True).strip()==SWEET_COMMIT
    assert sha_file(MODEL/"pytorch_model.bin")==MODEL_SHA
    assert platform.python_version().startswith("3.10."),platform.python_version()
    assert torch.__version__.startswith("1.12.1"),torch.__version__

    sys.path.insert(0,str(UP_SWEET.resolve()))
    from gec.tag import rewrite

    tok=BertTokenizer.from_pretrained(str(MODEL),local_files_only=True)
    model=BertForTokenClassification.from_pretrained(str(MODEL),local_files_only=True).eval().cpu()

    selected,total_lines=select_raw_lines(RAW)
    rows=[];changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[SWEET CROSS {n}/{len(selected)}] line={line_id}",flush=True)
        words=source.split()
        encoded=tok(words,return_tensors="pt",is_split_into_words=True)
        with torch.no_grad():
            logits=model(**encoded).logits[0]
            probs=torch.softmax(logits,dim=-1)
            maxprob,labels=probs.max(-1)
        ids=encoded["input_ids"][0].tolist()
        subwords=tok.convert_ids_to_tokens(ids[1:-1])
        edits=[model.config.id2label[int(v)] for v in labels[1:-1]]
        assert len(edits)==len(subwords)
        rewritten=rewrite(subwords=[subwords],edits=[edits])
        output=rewritten[0][0]
        changed+=int(output!=source)
        rows.extend(eventize(source,output,line_id,h,"SWEET"))

    write_jsonl(EVENTS,rows)
    summary={
        "status":"CROSS_SWEET_RAW_RUNTIME_COMPLETE",
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
            "model_sha256":MODEL_SHA,
            "sweet_commit":SWEET_COMMIT,
            "qalb_repo_commit":QALB_COMMIT,
            "stage":"NoPnx iteration 1 only"
        },
        "raw_sha256":sha_file(RAW),
        "license_sha256":sha_file(LICENSE),
        "qalb15_test_read":False,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="selected_line_hashes"},ensure_ascii=False))

if __name__=="__main__":
    main()
