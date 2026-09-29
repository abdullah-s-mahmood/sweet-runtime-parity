"""LOCAL_EDIT_SEMANTIC_BACKSTOP_PROTOTYPE.

Diagnostic-only semantic backstop over the already-consumed exact-agreement stream.
This runtime stage reads QALB RAW text and frozen agreement events only.
It MUST NOT read gold, manual adjudication, or prior correctness labels.
Persisted outputs contain no QALB text.
"""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

import torch
from huggingface_hub import HfApi
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl, sha_text

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
AGREEMENT=ROOT/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
OUT=ROOT/"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_RUNTIME.json"

MODEL_ID="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
BATCH=12

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def read_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def protected_signature(text):
    return {
        "digits":re.findall(r"[0-9٠-٩]+(?:[.,٫٬][0-9٠-٩]+)*",text),
        "latin":re.findall(r"[A-Za-z][A-Za-z0-9_.+\-/]*",text),
        "citations":re.findall(r"\[[0-9]+\]",text),
        "symbols":[ch for ch in text if ch in "%=<>±"],
    }

def reconstruct(source,row):
    us=units(source)
    span=list(map(int,row["source_lexical_span"]))
    assert span[0]>=0 and span[1]==span[0]+1,span
    i=span[0]
    assert i < len(us),(i,len(us))
    src_unit=us[i]
    out_surfaces=row.get("output_surfaces") or []
    assert len(out_surfaces)==1,out_surfaces
    candidate=source[:src_unit["span"][0]]+out_surfaces[0]+source[src_unit["span"][1]:]

    left=max(0,i-5); right=min(len(us)-1,i+5)
    a=us[left]["span"][0]; b=us[right]["span"][1]
    source_window=source[a:b]
    rel_a=src_unit["span"][0]-a
    rel_b=src_unit["span"][1]-a
    candidate_window=source_window[:rel_a]+out_surfaces[0]+source_window[rel_b:]
    return candidate,source_window,candidate_window

def infer_pairs(model,tok,pairs,max_length):
    results=[]
    ent_id=int(model.config.label2id.get("entailment",0))
    con_id=int(model.config.label2id.get("contradiction",2))
    for start in range(0,len(pairs),BATCH):
        chunk=pairs[start:start+BATCH]
        prem=[x[0] for x in chunk]
        hyp=[x[1] for x in chunk]
        enc=tok(prem,hyp,return_tensors="pt",padding=True,truncation=True,max_length=max_length)
        with torch.no_grad():
            probs=torch.softmax(model(**enc).logits,dim=-1).cpu()
        for p in probs:
            results.append({
                "entailment":float(p[ent_id]),
                "contradiction":float(p[con_id]),
                "neutral":float(1.0-p[ent_id]-p[con_id]),
            })
    return results

def main():
    rows=[
        x for x in read_jsonl(AGREEMENT)
        if x["runtime_decisions"]["EXACT_SINGLE_SUB_AGREEMENT"]=="ACCEPT"
    ]
    assert len(rows)==159,len(rows)
    raw=read_lines(RAW)

    work=[]
    whole_pairs=[]; local_pairs=[]
    for r in rows:
        source=raw[int(r["line_id"])-1]
        expected=r["line_hash"]
        # Cross-model selection hash already includes the registered seed.
        actual=sha_text("phase2-cross-model-agreement-v1|"+source)
        assert actual==expected,(r["line_id"],actual,expected)
        candidate,src_win,cand_win=reconstruct(source,r)
        inv_ok=protected_signature(source)==protected_signature(candidate)
        work.append((r,source,candidate,src_win,cand_win,inv_ok))
        whole_pairs.extend([(source,candidate),(candidate,source)])
        local_pairs.extend([(src_win,cand_win),(cand_win,src_win)])

    tok=AutoTokenizer.from_pretrained(MODEL_ID)
    model=AutoModelForSequenceClassification.from_pretrained(MODEL_ID).eval().cpu()
    whole=infer_pairs(model,tok,whole_pairs,512)
    local=infer_pairs(model,tok,local_pairs,192)
    revision=HfApi().model_info(MODEL_ID).sha

    out=[]
    for idx,(r,source,candidate,src_win,cand_win,inv_ok) in enumerate(work):
        wf=whole[2*idx]; wr=whole[2*idx+1]
        lf=local[2*idx]; lr=local[2*idx+1]
        whole_review=(
            min(wf["entailment"],wr["entailment"])<0.50
            or max(wf["contradiction"],wr["contradiction"])>=0.50
            or not inv_ok
        )
        local_review=(
            min(lf["entailment"],lr["entailment"])<0.50
            or max(lf["contradiction"],lr["contradiction"])>=0.50
            or not inv_ok
        )
        con_review=(
            max(wf["contradiction"],wr["contradiction"],lf["contradiction"],lr["contradiction"])>=0.50
            or not inv_ok
        )
        out.append({
            "agreement_id":r["agreement_id"],
            "line_id":r["line_id"],
            "line_hash":r["line_hash"],
            "source_hash":r["source_hash"],
            "candidate_hash":r["output_hash"],
            "protected_invariants_equal":inv_ok,
            "whole":{
                "source_to_candidate":wf,
                "candidate_to_source":wr,
            },
            "local":{
                "source_to_candidate":lf,
                "candidate_to_source":lr,
            },
            "runtime_decisions":{
                "WHOLE_HISTORICAL_05":"REVIEW" if whole_review else "PASS",
                "LOCAL_HISTORICAL_05":"REVIEW" if local_review else "PASS",
                "CONTRADICTION_ONLY_05":"REVIEW" if con_review else "PASS",
            },
        })

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    policies=list(out[0]["runtime_decisions"])
    counts={p:{
        "PASS":sum(x["runtime_decisions"][p]=="PASS" for x in out),
        "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in out),
    } for p in policies}
    summary={
        "status":"LOCAL_EDIT_SEMANTIC_BACKSTOP_RUNTIME_FROZEN",
        "prototype":"LOCAL_EDIT_SEMANTIC_BACKSTOP_PROTOTYPE",
        "diagnostic_only":True,
        "labels_or_gold_read":False,
        "population":"159 consumed EXACT_SINGLE_SUB_AGREEMENT events",
        "rows":len(out),
        "model_id":MODEL_ID,
        "model_revision":revision,
        "label_mapping":dict(model.config.label2id),
        "decision_counts":counts,
        "features_sha256":file_sha(OUT),
        "qalb_text_persisted":False,
        "qalb15_test_read":False,
        "thresholds_frozen_before_labels":True,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+SUMMARY.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic/QALB text leaked"
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
