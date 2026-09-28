"""Contextual contradiction diagnostic for frozen cross-model agreement events.

Reads:
- frozen gold-blind cross-model agreement features from workflow artifact;
- QALB15 TRAIN raw text only.

Does NOT read:
- QALB corrected/gold text;
- manual review labels;
- QALB TEST.

Diagnostic only. No production promotion.
"""
from __future__ import annotations
import hashlib,json,re,unicodedata
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer,BertForTokenClassification

from phase2.acceptance.run_arabart_candidate_generator import ged_labels_for_words

ROOT=Path(__file__).resolve().parents[2]
AG=ROOT/"artifacts"/"agreement"/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
RAW=ROOT/"upstream"/"arabic-gec"/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
OUT=ROOT/"artifacts"/"CONTEXTUAL_CONTRADICTION_FEATURES.jsonl"
SUM=ROOT/"artifacts"/"CONTEXTUAL_CONTRADICTION_RUNTIME.json"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
EXPECTED_AGREEMENT_SHA="d66a5ab3c6b9e1527b7a1a59ddce0f843a864281e70106cacd58d00315741c4c"

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def strip_marks(s):
    return "".join(ch for ch in unicodedata.normalize("NFC",s) if unicodedata.category(ch)!="Mn" and ch!="ـ")

def is_punc_or_symbol(ch):
    return unicodedata.category(ch)[0] in {"P","S"}

def base(s):
    return "".join(ch for ch in strip_marks(s) if not is_punc_or_symbol(ch) and not ch.isspace())

def units(text):
    out=[]
    for wi,m in enumerate(re.finditer(r"\S+",text)):
        b=base(m.group(0))
        if b:
            out.append({"lexical_index":len(out),"whitespace_word_index":wi,"surface":m.group(0),"base":b})
    return out

def replace_event(source,event):
    words=source.split()
    us=units(source)
    a,b=map(int,event["source_lexical_span"])
    selected=us[a:b]
    outs=list(event["output_surfaces"])
    if len(selected)!=len(outs) or not selected:
        raise RuntimeError(("event replacement geometry mismatch",event["agreement_id"]))
    edited=[]
    for u,new in zip(selected,outs):
        wi=int(u["whitespace_word_index"])
        words[wi]=new
        edited.append(wi)
    return " ".join(words),edited

def morph_view(text,disambig):
    words=text.split()
    dis=disambig.disambiguate(words)
    model_words=[]
    diag=[]
    for src,d in zip(words,dis):
        if d.analyses:
            an=d.analyses[0].analysis
            diac=an.get("diac",src)
            model_words.append(dediac_ar(diac))
            diag.append({
                "has_analysis":True,
                "source":an.get("source"),
                "pos":an.get("pos"),
                "lex":an.get("lex"),
                "num":an.get("num"),
                "per":an.get("per"),
                "asp":an.get("asp"),
                "mod":an.get("mod"),
                "gen":an.get("gen"),
            })
        else:
            model_words.append(dediac_ar(src))
            diag.append({"has_analysis":False,"source":None,"pos":None,"lex":None,"num":None,"per":None,"asp":None,"mod":None,"gen":None})
    return model_words,diag

def main():
    if sha_file(AG)!=EXPECTED_AGREEMENT_SHA:
        raise RuntimeError("Frozen agreement features SHA mismatch")
    raw=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    events=[x for x in read_jsonl(AG) if x["runtime_decisions"]["EXACT_SINGLE_SUB_AGREEMENT"]=="ACCEPT"]
    assert len(events)==159,len(events)

    dis=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()

    rows=[]
    for n,e in enumerate(events,1):
        line=raw[int(e["line_id"])-1]
        candidate,edited=replace_event(line,e)
        model_words,morph=morph_view(candidate,dis)
        labels,details=ged_labels_for_words(model_words,ged_tok,ged_model)
        edited_ged=[details[i] for i in edited]
        edited_morph=[morph[i] for i in edited]
        ged_contradiction=any(x["label"]!="UC" for x in edited_ged)
        no_morph=any(not x["has_analysis"] for x in edited_morph)
        backoff=any((x.get("source")=="backoff" or (x.get("pos")=="noun_prop" and x.get("source")!="lex")) for x in edited_morph)
        rows.append({
            "agreement_id":e["agreement_id"],
            "line_id":e["line_id"],
            "line_hash":e["line_hash"],
            "source_lexical_span":e["source_lexical_span"],
            "source_hash":e["source_hash"],
            "candidate_hash":e["output_hash"],
            "edited_whitespace_indices":edited,
            "edited_ged":[{"word_index":x["word_index"],"label":x["label"],"score":x["score"]} for x in edited_ged],
            "edited_morph":edited_morph,
            "features":{
                "ged_contradiction":ged_contradiction,
                "no_contextual_morph_analysis":no_morph,
                "backoff_or_nounprop_fallback":backoff,
            },
            "runtime_decisions":{
                "GED_CONTRADICTION":"REVIEW" if ged_contradiction else "KEEP_ACCEPT",
                "GED_OR_NO_MORPH":"REVIEW" if (ged_contradiction or no_morph) else "KEEP_ACCEPT",
            }
        })
        print(f"[{n}/{len(events)}] {e['agreement_id']}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    summary={
        "status":"CONTEXTUAL_CONTRADICTION_RUNTIME_FROZEN",
        "diagnostic_only":True,
        "gold_or_manual_labels_read":False,
        "agreement_features_sha256":sha_file(AG),
        "rows":len(rows),
        "ged_contradiction_rows":sum(x["features"]["ged_contradiction"] for x in rows),
        "no_morph_rows":sum(x["features"]["no_contextual_morph_analysis"] for x in rows),
        "backoff_rows":sum(x["features"]["backoff_or_nounprop_fallback"] for x in rows),
        "decision_counts":{
            p:{
                "KEEP_ACCEPT":sum(x["runtime_decisions"][p]=="KEEP_ACCEPT" for x in rows),
                "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in rows),
            } for p in ("GED_CONTRADICTION","GED_OR_NO_MORPH")
        },
        "qalb15_test_read":False,
    }
    SUM.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
