#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, pathlib, hashlib, collections, shutil

from r43_contextual_pair_preflight import parse_train, spans_for_sentence

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
LABELS=["P","I","C","O"]

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def build_combined(processed,out):
    # Exact evaluator path used by PICO_ner.py expects token GOLD PRED in one file.
    lines=[]
    for raw in pathlib.Path(processed).read_text(encoding="utf-8").splitlines():
        if raw.startswith("-DOCSTART-"):
            lines.append(raw); continue
        if raw=="":
            lines.append(""); continue
        parts=raw.split()
        if len(parts)>=2:
            token=parts[0]; label=parts[-1].strip()
        else:
            token=parts[0]; label="O"
        lines.append(f"{token}\t{label}\t{label}")
    pathlib.Path(out).write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--source-utils",type=pathlib.Path,required=True)
    ap.add_argument("--source-evaluate",type=pathlib.Path,required=True)
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    assert sha(a.train)==TRAIN_SHA

    u=load_module(a.source_utils,"source_utils")
    ev=load_module(a.source_evaluate,"source_eval")
    processed=a.out/"SOURCE_PREPROCESSED_TRAIN.txt"
    u.update_data_to_max_len(256,str(a.train),str(processed),str(a.model_dir),sep_tag_type="tab")

    combined=a.out/"SOURCE_GOLD_AS_PRED.txt"
    build_combined(processed,combined)
    gold,pred=ev.load_combined_bio(str(combined),"\t")
    src=ev.load_spans(gold,eval_type="ner")
    source_counts={c:len(src.get(c,[])) for c in LABELS}

    # Our parser applied to source-preprocessed data: comparison isolates span semantics.
    docs,empty,bad=parse_train(processed)
    if bad: raise RuntimeError(bad[:10])
    ours=collections.Counter(); continuation=collections.Counter(); cont_rows=[]
    for di,doc in enumerate(docs):
        for si,(tokens,tags) in enumerate(doc):
            ss,bio_bad,cont=spans_for_sentence(doc,si)
            if bio_bad: raise RuntimeError((di,si,bio_bad[:3]))
            for c,s,e in ss: ours[c]+=1
            if cont:
                typ=cont["tag"][2:]; continuation[typ]+=1
                cont_rows.append({"document":di,"sentence":si,"class":typ,
                                  "first_tag":cont["tag"],
                                  "previous_sentence_last_tag":cont["previous_sentence_last_tag"],
                                  "preview":" ".join(tokens[:12])})
    ours_counts={c:int(ours[c]) for c in LABELS}

    # Manual strict B-only span count per blank-delimited sequence, independent check.
    strict=collections.Counter()
    initial_I=collections.Counter()
    nseq=0
    for doc in docs:
        for tokens,tags in doc:
            nseq+=1
            if tags and tags[0].startswith("I-"): initial_I[tags[0][2:]]+=1
            for tag in tags:
                if tag.startswith("B-"): strict[tag[2:]]+=1

    # Compare sequence inventory raw vs source-preprocessed.
    raw_docs,raw_empty,raw_bad=parse_train(a.train)
    raw_seq=sum(len(d) for d in raw_docs)
    proc_seq=sum(len(d) for d in docs)
    raw_tok=sum(len(t) for d in raw_docs for t,_ in d)
    proc_tok=sum(len(t) for d in docs for t,_ in d)

    result={
      "state":"R43_SOURCE_PROTOCOL_PARITY_V2_COMPLETE",
      "train_sha256":TRAIN_SHA,
      "source_utils_sha256":sha(a.source_utils),
      "source_evaluate_sha256":sha(a.source_evaluate),
      "processed_sha256":sha(processed),
      "inventory":{
        "raw_docs":len(raw_docs),"processed_docs":len(docs),
        "raw_sequences":raw_seq,"processed_sequences":proc_seq,
        "raw_tokens_after_current_empty_removal":raw_tok,
        "processed_tokens":proc_tok,
        "raw_empty_surface_rows_removed_by_current_parser":dict(raw_empty),
        "processed_empty_surface_rows":dict(empty)
      },
      "official_combined_evaluator_counts":source_counts,
      "manual_strict_B_counts":{c:int(strict[c]) for c in LABELS},
      "current_parser_on_source_preprocessed_counts":ours_counts,
      "delta_current_minus_official":{c:ours_counts[c]-source_counts[c] for c in LABELS},
      "processed_initial_I_counts":dict(initial_I),
      "current_continuation_segments":dict(continuation),
      "current_continuation_total":sum(continuation.values()),
      "continuation_rows":cont_rows,
      "interpretation":{
        "validity":"Uses source's actual preprocessing function and actual combined-file evaluator path used by PICO_ner.py.",
        "decision":"If official counts equal manual strict-B counts, evaluator reproduction is valid. Any current-parser delta is a real semantics difference caused by continuation handling, not the prior load_bio newline artifact."
      },
      "guards":{"TRAIN_only":True,"DEV":False,"TEST":False,"other_folds":False,"training":False}
    }
    (a.out/"R43_SOURCE_PROTOCOL_PARITY_V2.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": main()
