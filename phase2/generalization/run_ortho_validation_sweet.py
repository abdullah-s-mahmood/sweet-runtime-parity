"""Run one frozen SWEET voter on the third disjoint validation slice. Gold-blind."""
from __future__ import annotations
import importlib.metadata,json,os,platform,subprocess,sys
from pathlib import Path
import torch
from transformers import BertTokenizer,BertForTokenClassification

from phase2.generalization.ortho_validation_common import select_validation_raw_lines,VALIDATION_SEED,SLICE_N
from phase2.generalization.cross_model_common import eventize,write_jsonl,sha_file

ROOT=Path(__file__).resolve().parents[2]
UP_QALB=ROOT/"upstream"/"arabic-gec"
UP_SWEET=ROOT/"upstream"/"text-editing"
RAW=UP_QALB/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
LICENSE=UP_QALB/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/LICENSE.txt"
ART=ROOT/"artifacts"
QALB_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
SWEET_COMMIT="4d552ca3ae98029550f27fc52aa1b22883e16e61"

def main():
    model_id=os.environ["SWEET_MODEL_ID"]
    revision=os.environ["SWEET_MODEL_REVISION"]
    voter=os.environ["SWEET_VOTER_NAME"]
    prefix=os.environ["SWEET_OUTPUT_PREFIX"]
    ART.mkdir(exist_ok=True)
    assert subprocess.check_output(["git","-C",str(UP_QALB),"rev-parse","HEAD"],text=True).strip()==QALB_COMMIT
    assert subprocess.check_output(["git","-C",str(UP_SWEET),"rev-parse","HEAD"],text=True).strip()==SWEET_COMMIT

    sys.path.insert(0,str(UP_SWEET.resolve()))
    from gec.tag import rewrite

    tok=BertTokenizer.from_pretrained(model_id,revision=revision)
    model=BertForTokenClassification.from_pretrained(model_id,revision=revision).eval().cpu()

    selected,total,cross_ids,tri_ids=select_validation_raw_lines(RAW)
    rows=[]; changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[{voter} {n}/{len(selected)}] line={line_id}",flush=True)
        words=source.split()
        encoded=tok(words,return_tensors="pt",is_split_into_words=True)
        with torch.no_grad():
            logits=model(**encoded).logits[0]
            _,labels=torch.softmax(logits,dim=-1).max(-1)
        ids=encoded["input_ids"][0].tolist()
        subwords=tok.convert_ids_to_tokens(ids[1:-1])
        edits=[model.config.id2label[int(v)] for v in labels[1:-1]]
        assert len(edits)==len(subwords)
        output=rewrite(subwords=[subwords],edits=[edits])[0][0]
        changed+=int(output!=source)
        rows.extend(eventize(source,output,line_id,h,prefix))

    events=ART/f"{prefix}_EVENTS.jsonl"
    summary=ART/f"{prefix}_SUMMARY.json"
    write_jsonl(events,rows)
    obj={
      "status":"ORTHO_VALIDATION_SWEET_RAW_COMPLETE","gold_read":False,
      "voter":voter,"model_id":model_id,"model_revision":revision,
      "selection_seed":VALIDATION_SEED,"slice_n":SLICE_N,
      "excluded_cross_ids":cross_ids,"excluded_trimodel_ids":tri_ids,
      "selected_line_ids":[i for _,i,_ in selected],
      "selected_line_hashes":[h for h,_,_ in selected],
      "raw_total_lines":total,"changed_lines":changed,"event_rows":len(rows),
      "runtime":{"python":platform.python_version(),"torch_distribution":importlib.metadata.version("torch"),
                 "sweet_commit":SWEET_COMMIT,"qalb_repo_commit":QALB_COMMIT},
      "raw_sha256":sha_file(RAW),"license_sha256":sha_file(LICENSE),"qalb15_test_read":False,
    }
    summary.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in obj.items() if k not in {"selected_line_hashes","excluded_cross_ids","excluded_trimodel_ids"}},ensure_ascii=False))

if __name__=="__main__":main()
