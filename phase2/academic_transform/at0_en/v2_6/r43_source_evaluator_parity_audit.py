#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, pathlib, hashlib, collections
from r43_contextual_pair_preflight import parse_train, spans_for_sentence

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def load_module(path):
    spec=importlib.util.spec_from_file_location("source_evaluate",path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--source-evaluate",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    assert sha(a.train)==TRAIN_SHA

    src=load_module(a.source_evaluate)
    flat=src.load_bio(str(a.train),sep_tag="\t")
    source=src.load_spans(flat,eval_type="ner")
    source_counts={c:len(source.get(c,[])) for c in ["P","I","C","O"]}

    docs,empty,bad=parse_train(a.train)
    if bad: raise RuntimeError(bad[:3])
    ours=collections.Counter(); continuation=collections.Counter(); rows=[]
    for di,doc in enumerate(docs):
        for si,(tokens,tags) in enumerate(doc):
            spans,bio_bad,cont=spans_for_sentence(doc,si)
            if bio_bad: raise RuntimeError((di,si,bio_bad[:2]))
            for c,s,e in spans: ours[c]+=1
            if cont:
                typ=cont["tag"][2:]
                continuation[typ]+=1
                rows.append({"document":di,"sentence":si,"class":typ,
                             "first_tag":cont["tag"],
                             "previous_sentence_last_tag":cont["previous_sentence_last_tag"],
                             "surface_preview":" ".join(tokens[:min(12,len(tokens))])})
    ours_counts={c:int(ours[c]) for c in ["P","I","C","O"]}
    delta={c:ours_counts[c]-source_counts[c] for c in source_counts}

    result={
      "state":"R43_SOURCE_EVALUATOR_PARITY_AUDIT_COMPLETE",
      "train_sha256":TRAIN_SHA,
      "source_evaluate_sha256":sha(a.source_evaluate),
      "source_official_counts":source_counts,
      "current_parser_counts":ours_counts,
      "delta_current_minus_source":delta,
      "continuation_segments_current_parser":dict(continuation),
      "continuation_total":sum(continuation.values()),
      "continuation_rows":rows,
      "empty_surface_rows_removed":empty,
      "interpretation":{
        "source_rule":"Official load_spans starts entities only at B-*; blank lines become O via load_bio.",
        "current_rule":"spans_for_sentence treats valid sentence-initial I-X following same-type prior-sentence final tag as an example-local continuation segment/entity.",
        "risk":"Entity inventory/evaluation semantics differ unless delta is zero. Must freeze one semantics before future training/evaluation."
      },
      "guards":{"TRAIN_only":True,"DEV":False,"TEST":False,"other_folds":False,"training":False}
    }
    (a.out/"R43_SOURCE_EVALUATOR_PARITY.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
