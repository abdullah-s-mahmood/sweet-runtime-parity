#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib
from r43_contextual_pair_preflight import parse_train, spans_for_sentence

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def source_loader_examples(path):
    """Faithful to source utils_ner.read_examples_from_file for ordinary EBM-NLPmod lines."""
    examples=[]; words=[]; labels=[]; rows=[]
    raw=path.read_text(encoding="utf-8").splitlines(keepends=True)
    for lineno,line in enumerate(raw,1):
        if line.startswith("-DOCSTART-") or line=="" or line=="\n" or (line.startswith("###") and line.endswith("$$$\n")):
            if words:
                examples.append((words,labels)); words=[]; labels=[]
            continue
        splits=line.split()
        if not splits:
            # Only true blank lines are caught above.
            continue
        word=splits[0]
        label=splits[-1].replace("\n","") if len(splits)>1 else "O"
        words.append(word); labels.append(label)
        if line.startswith("\t"):
            rows.append({"line":lineno,"raw":line.rstrip("\n"),"source_loader_word":word,"source_loader_label":label})
    if words: examples.append((words,labels))
    return examples,rows

def bstart_counts_from_examples(examples):
    cnt=collections.Counter()
    entities=[]
    for ei,(words,labels) in enumerate(examples):
        i=0
        while i<len(labels):
            lab=labels[i]
            if lab.startswith("B-"):
                typ=lab[2:]; j=i+1
                while j<len(labels) and labels[j]==f"I-{typ}": j+=1
                cnt[typ]+=1; entities.append((ei,typ,i,j))
                i=j
            else: i+=1
    return cnt,entities

def external_eval_gold_stream(path):
    """Gold stream equivalent to source predict-file -> evaluate.py load_combined_bio path under perfect predictions.
    Normal token rows contribute gold; blank lines contribute O; DOCSTART and empty-token rows have <3 tab columns
    after prediction-file formatting/strip and therefore are ignored by load_combined_bio.
    """
    gold=[]; ignored=collections.Counter()
    raw=path.read_text(encoding="utf-8").splitlines(keepends=True)
    for lineno,line in enumerate(raw,1):
        if line.strip()=="":
            gold.append("O"); continue
        if line.startswith("-DOCSTART-"):
            ignored["DOCSTART"]+=1; continue
        if line.startswith("###") and line.rstrip("\n").endswith("$$$"):
            continue
        # Prediction writer appends one predicted column to the original line.
        predline=line[:-1]+"\tPRED\n" if line.endswith("\n") else line+"\tPRED"
        cols=predline.strip().split("\t")
        if len(cols)<3:
            ignored["TOO_FEW_COLS"]+=1
            continue
        gold.append(cols[-2].split()[0])
    return gold,ignored

def bstart_counts_flat(labels):
    cnt=collections.Counter(); i=0
    while i<len(labels):
        lab=labels[i]
        if lab.startswith("B-"):
            typ=lab[2:]; j=i+1
            while j<len(labels) and labels[j]==f"I-{typ}": j+=1
            cnt[typ]+=1; i=j
        else:i+=1
    return cnt

def current_counts(train):
    docs,empty,bad=parse_train(train)
    if bad: raise RuntimeError(bad[:3])
    cnt=collections.Counter(); cont=collections.Counter(); continuation_rows=[]
    for di,doc in enumerate(docs):
        for si,(tokens,tags) in enumerate(doc):
            spans,bio_bad,continuation=spans_for_sentence(doc,si)
            if bio_bad: raise RuntimeError((di,si,bio_bad[:2]))
            for c,s,e in spans: cnt[c]+=1
            if continuation:
                typ=continuation["tag"][2:]; cont[typ]+=1
                continuation_rows.append({"document":di,"sentence":si,"class":typ,
                  "previous_sentence_last_tag":continuation["previous_sentence_last_tag"],
                  "surface_preview":" ".join(tokens[:12])})
    return docs,empty,cnt,cont,continuation_rows

def empty_contexts(path):
    lines=path.read_text(encoding="utf-8").splitlines()
    out=[]
    for i,line in enumerate(lines):
        if line.startswith("\t"):
            ctx=[]
            for j in range(max(0,i-2),min(len(lines),i+3)):
                ctx.append({"line":j+1,"text":lines[j]})
            out.append({"line":i+1,"raw":line,"context":ctx})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--source-utils",type=pathlib.Path,required=True)
    ap.add_argument("--source-evaluate",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    assert sha(a.train)==TRAIN_SHA
    utiltxt=a.source_utils.read_text(encoding="utf-8")
    evtxt=a.source_evaluate.read_text(encoding="utf-8")
    assert 'splits = line.split()' in utiltxt and 'labels.append("O")' in utiltxt
    assert 'line.strip().split(sep_tag)' in evtxt and "if label.startswith( 'B-' )" in evtxt

    examples,empty_loader_rows=source_loader_examples(a.train)
    loader_cnt,_=bstart_counts_from_examples(examples)
    eval_gold,eval_ignored=external_eval_gold_stream(a.train)
    eval_cnt=bstart_counts_flat(eval_gold)
    docs,empty_removed,our_cnt,cont_cnt,cont_rows=current_counts(a.train)
    classes=["P","I","C","O"]
    fmt=lambda c:{k:int(c[k]) for k in classes}
    result={
      "state":"R43_SOURCE_PIPELINE_SEMANTICS_PARITY_V2_COMPLETE",
      "train_sha256":TRAIN_SHA,
      "source_utils_sha256":sha(a.source_utils),
      "source_evaluate_sha256":sha(a.source_evaluate),
      "source_loader":{"examples":len(examples),"entity_B_start_counts":fmt(loader_cnt),
                       "empty_token_rows_reinterpreted":empty_loader_rows},
      "source_external_evaluator":{"gold_stream_items":len(eval_gold),"entity_B_start_counts":fmt(eval_cnt),
                                   "ignored_rows":dict(eval_ignored)},
      "current_parser":{"documents":len(docs),"entity_counts":fmt(our_cnt),
                        "removed_empty_surface_counts":empty_removed,
                        "continuation_segments":fmt(cont_cnt),"continuation_total":sum(cont_cnt.values())},
      "delta_current_minus_source_external":{k:int(our_cnt[k]-eval_cnt[k]) for k in classes},
      "delta_current_minus_source_loader":{k:int(our_cnt[k]-loader_cnt[k]) for k in classes},
      "empty_token_raw_contexts":empty_contexts(a.train),
      "continuation_rows":cont_rows,
      "interpretation_rules":{
        "source_training_loader":"Empty-token rows are split() into a pseudo-word equal to the label string and assigned label O when only one field remains.",
        "source_external_evaluator":"External -lf path ignores prediction-file rows with fewer than 3 tab-separated columns; entities start only at B-*.",
        "current_parser":"Drops empty surface rows and materializes valid cross-example initial I-X as a local continuation entity.",
        "decision":"Do not train a new model until one canonical semantic contract is prospectively frozen and legacy/source scores are reported under their own semantics."
      },
      "guards":{"TRAIN_only":True,"DEV":False,"TEST":False,"other_folds":False,"training":False}
    }
    (a.out/"R43_SOURCE_PIPELINE_SEMANTICS_PARITY_V2.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
