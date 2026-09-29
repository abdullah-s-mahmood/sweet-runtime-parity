"""Run frozen QALB14 AraBART voter on the third disjoint validation slice. Gold-blind."""
from __future__ import annotations
import importlib.metadata,json,platform,subprocess
from pathlib import Path
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer,BertForTokenClassification,MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.generalization.ortho_validation_common import select_validation_raw_lines,VALIDATION_SEED,SLICE_N
from phase2.generalization.cross_model_common import eventize,write_jsonl,sha_file

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
LICENSE=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/LICENSE.txt"
ART=ROOT/"artifacts"
EVENTS=ART/"VAL_ARABART_Q14_EVENTS.jsonl"
SUMMARY=ART/"VAL_ARABART_Q14_SUMMARY.json"
UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GED_REV="447179dc63d186e4bff09a993e90e73ad622d571"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
GEC_REV="410588a318d988cdcfdbf64cf5745ed4adea0f6a"

def main():
    ART.mkdir(exist_ok=True)
    assert subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()==UPSTREAM_COMMIT
    selected,total,cross_ids,tri_ids=select_validation_raw_lines(RAW)

    dis=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL,revision=GED_REV)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL,revision=GED_REV).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL,revision=GEC_REV)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL,revision=GEC_REV).eval().cpu()

    rows=[];changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[VAL_ARABART_Q14 {n}/{len(selected)}] line={line_id}",flush=True)
        output,_=generate_one(source,dis,ged_tok,ged_model,gec_tok,gec_model)
        changed+=int(output!=source)
        rows.extend(eventize(source,output,line_id,h,"VAL_ARABART_Q14"))

    write_jsonl(EVENTS,rows)
    obj={
      "status":"ORTHO_VALIDATION_ARABART_RAW_COMPLETE","gold_read":False,
      "voter":"ARABART_QALB14","ged_model":GED_MODEL,"ged_revision":GED_REV,
      "gec_model":GEC_MODEL,"gec_revision":GEC_REV,
      "selection_seed":VALIDATION_SEED,"slice_n":SLICE_N,
      "excluded_cross_ids":cross_ids,"excluded_trimodel_ids":tri_ids,
      "selected_line_ids":[i for _,i,_ in selected],
      "selected_line_hashes":[h for h,_,_ in selected],
      "raw_total_lines":total,"changed_lines":changed,"event_rows":len(rows),
      "runtime":{"python":platform.python_version(),"torch":importlib.metadata.version("torch"),
                 "qalb_repo_commit":UPSTREAM_COMMIT},
      "raw_sha256":sha_file(RAW),"license_sha256":sha_file(LICENSE),"qalb15_test_read":False,
    }
    SUMMARY.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in obj.items() if k not in {"selected_line_hashes","excluded_cross_ids","excluded_trimodel_ids"}},ensure_ascii=False))

if __name__=="__main__":main()
