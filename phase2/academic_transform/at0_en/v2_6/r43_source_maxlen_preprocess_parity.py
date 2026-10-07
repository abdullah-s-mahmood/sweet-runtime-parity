#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib
from transformers import AutoTokenizer

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
VOCAB_SHA="7b36651908a88bc38bda41b728b2a598191e0d3b553cbacf7b1e5f026d5b5b9f"

def sha(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def count_bstarts(lines):
    cnt=collections.Counter(); labels=[]
    for line in lines:
        if not line:
            labels.append("O"); continue
        if line.startswith("-DOCSTART-"): labels.append("O"); continue
        if "\t" not in line: continue
        labels.append(line.split("\t")[-1])
    i=0
    while i<len(labels):
        lab=labels[i]
        if lab.startswith("B-"):
            typ=lab[2:]; j=i+1
            while j<len(labels) and labels[j]==f"I-{typ}": j+=1
            cnt[typ]+=1; i=j
        else: i+=1
    return {c:int(cnt[c]) for c in ["P","I","C","O"]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--tokenizer-dir",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    assert sha(a.train)==TRAIN_SHA
    if (a.tokenizer_dir/"vocab.txt").exists(): assert sha(a.tokenizer_dir/"vocab.txt")==VOCAB_SHA
    tok=AutoTokenizer.from_pretrained(a.tokenizer_dir,local_files_only=True,use_fast=True)

    raw=a.train.read_text(encoding="utf-8").splitlines()
    out=[]
    sent_wp=0; since_prev_b=0; prev_b_n=0
    inserted=[]; removed=[]; wp_max=252
    for idx,line0 in enumerate(raw,1):
        line=line0.rstrip()
        if (not line) or (line.startswith("###") and line.endswith("$$$")):
            out.append(line); sent_wp=0; since_prev_b=0; prev_b_n=0; continue
        parts=line.split("\t")
        word=parts[0]; label=parts[-1]
        wps=tok.tokenize(word); n=len(wps)
        if n==0:
            removed.append({"line":idx,"raw":line,"label":label})
            continue
        if sent_wp+n>wp_max:
            insert_at=len(out)-prev_b_n
            out.insert(insert_at,"")
            inserted.append({"source_line":idx,"insert_at_output_index":insert_at,
                             "word":word,"label":label,"prior_sentence_wp":sent_wp,
                             "carry_entity_wp":since_prev_b,"previous_nonO_count":prev_b_n})
            sent_wp=since_prev_b
        out.append(line); sent_wp+=n
        if label=="O":
            prev_b_n=0; since_prev_b=0
        else:
            prev_b_n+=1; since_prev_b+=n

    raw_blanks=sum(1 for x in raw if x=="")
    out_blanks=sum(1 for x in out if x=="")
    result={
      "state":"R43_SOURCE_MAXLEN_PREPROCESS_PARITY_COMPLETE",
      "train_sha256":TRAIN_SHA,
      "tokenizer_vocab_sha256":sha(a.tokenizer_dir/"vocab.txt"),
      "source_max_len":256,"effective_wordpiece_limit":252,
      "raw_lines":len(raw),"output_lines":len(out),
      "raw_blank_lines":raw_blanks,"output_blank_lines":out_blanks,
      "removed_tokenizer_empty_rows_count":len(removed),
      "removed_rows":removed,
      "inserted_split_count":len(inserted),
      "inserted_splits":inserted,
      "raw_B_start_entity_counts":count_bstarts(raw),
      "postprocess_B_start_entity_counts":count_bstarts(out),
      "interpretation":"Faithful logic to source utils_ner.update_data_to_max_len: max_len-=4, remove tokenizer-empty words, insert blank before prior contiguous non-O block when limit exceeded.",
      "guards":{"TRAIN_only":True,"DEV":False,"TEST":False,"other_folds":False,"training":False}
    }
    (a.out/"R43_SOURCE_MAXLEN_PREPROCESS_PARITY.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
