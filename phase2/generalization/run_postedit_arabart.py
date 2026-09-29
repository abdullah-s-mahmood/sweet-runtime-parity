"""Second-pass frozen AraBART QALB14 voter over jointly corrected lines."""
from __future__ import annotations
import json,os
from pathlib import Path
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer,BertForTokenClassification,MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.generalization.cross_model_common import eventize,write_jsonl

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
CONS=ART/"consensus"/"POSTEDIT_CONSENSUS_LINES.jsonl"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    ged_rev=os.environ["GED_MODEL_REVISION"]
    gec_rev=os.environ["GEC_MODEL_REVISION"]
    dis=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL,revision=ged_rev)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL,revision=ged_rev).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL,revision=gec_rev)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL,revision=gec_rev).eval().cpu()
    rows=[]
    data=jl(CONS)
    for n,x in enumerate(data,1):
        source=x["corrected_text"]
        print(f"[POSTEDIT ARABART {n}/{len(data)}] line={x['line_id']}",flush=True)
        output,_=generate_one(source,dis,ged_tok,ged_model,gec_tok,gec_model)
        rows.extend(eventize(source,output,int(x["line_id"]),x["line_hash"],"TRI_ARABART_Q14_POST"))
    write_jsonl(ART/"TRI_ARABART_Q14_POSTEDIT_EVENTS.jsonl",rows)
    print(json.dumps({"status":"POSTEDIT_ARABART_COMPLETE","lines":len(data),"events":len(rows)}))

if __name__=="__main__":
    main()
