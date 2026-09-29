"""Second-pass SWEET voter over jointly corrected tri-model lines."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
import torch
from transformers import BertTokenizer,BertForTokenClassification

from phase2.generalization.cross_model_common import eventize,write_jsonl

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"text-editing"
ART=ROOT/"artifacts"
CONS=ART/"consensus"/"POSTEDIT_CONSENSUS_LINES.jsonl"

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    model_id=os.environ["SWEET_MODEL_ID"]
    voter=os.environ["SWEET_VOTER_NAME"]
    prefix=os.environ["SWEET_OUTPUT_PREFIX"]
    revision=os.environ["SWEET_MODEL_REVISION"]
    out_path=ART/f"{prefix}_POSTEDIT_EVENTS.jsonl"
    sys.path.insert(0,str(UP.resolve()))
    from gec.tag import rewrite

    tok=BertTokenizer.from_pretrained(model_id,revision=revision)
    model=BertForTokenClassification.from_pretrained(model_id,revision=revision).eval().cpu()
    rows=[]
    for n,x in enumerate(jl(CONS),1):
        source=x["corrected_text"]
        print(f"[POSTEDIT {voter} {n}] line={x['line_id']}",flush=True)
        words=source.split()
        enc=tok(words,return_tensors="pt",is_split_into_words=True)
        with torch.no_grad():
            logits=model(**enc).logits[0]
            _,labels=torch.softmax(logits,dim=-1).max(-1)
        ids=enc["input_ids"][0].tolist()
        subwords=tok.convert_ids_to_tokens(ids[1:-1])
        edits=[model.config.id2label[int(v)] for v in labels[1:-1]]
        output=rewrite(subwords=[subwords],edits=[edits])[0][0]
        rows.extend(eventize(source,output,int(x["line_id"]),x["line_hash"],prefix+"_POST"))
    write_jsonl(out_path,rows)
    print(json.dumps({"status":"POSTEDIT_SWEET_COMPLETE","voter":voter,"lines":len(jl(CONS)),"events":len(rows)}))

if __name__=="__main__":
    main()
