#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,pathlib,unicodedata
from collections import Counter
from transformers import AutoTokenizer

MODELS={
 "BASE":("microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract","d673b8835373c6fa116d6d8006b33d48734e305d",510,256),
 "MODERN":("thomas-sounack/BioClinical-ModernBERT-base","c3648aa87af95837c809e6f0c5f85d08160db437",8190,4096),
 "PICOX":("microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract","f18ff5ec008285849e7c467b2618262b0def6238",510,256),
}

def parse_docs(path:pathlib.Path):
    docs=[]; cur=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started: docs.append(cur)
            cur=[]; started=True; continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        # ONLY source token column is consumed. Labels are ignored.
        cur.append(line.split("\t")[0])
    if started: docs.append(cur)
    if any(not d for d in docs): raise RuntimeError("empty parsed document")
    return docs

def plan_windows(piece_counts,max_content,stride):
    if any(x<=0 for x in piece_counts): raise ValueError("nonpositive piece count")
    if any(x>max_content for x in piece_counts): raise ValueError("single source word exceeds window")
    prefix=[0]
    for x in piece_counts: prefix.append(prefix[-1]+x)
    out=[]; start=0; n=len(piece_counts)
    while start<n:
        end=start; used=0
        while end<n and used+piece_counts[end]<=max_content:
            used+=piece_counts[end]; end+=1
        if end<=start: raise RuntimeError("no progress")
        out.append((start,end,used))
        if end==n: break
        target=prefix[start]+stride
        nxt=start+1
        while nxt<n and prefix[nxt]<target: nxt+=1
        if nxt>=end: nxt=max(start+1,end-1)
        if nxt<=start: raise RuntimeError("stride did not advance")
        start=nxt
    covered=[False]*n
    for s,e,_ in out:
        for i in range(s,e): covered[i]=True
    if not all(covered): raise RuntimeError("coverage failure")
    return out

def tokenize_words(tok,words):
    counts=[]; empty=[]; dig=hashlib.sha256()
    for i,w in enumerate(words):
        enc=tok(w,add_special_tokens=False,return_attention_mask=False,return_token_type_ids=False)
        ids=list(enc["input_ids"])
        if not ids:
            # frozen policy: explicit UNK one piece, do not drop source word
            ids=[tok.unk_token_id]
            empty.append(i)
        counts.append(len(ids))
        dig.update(str(i).encode()); dig.update(b"\0")
        dig.update(w.encode("utf-8")); dig.update(b"\0")
        dig.update(",".join(map(str,ids)).encode()); dig.update(b"\n")
    return counts,empty,dig.hexdigest()

def run_one(tok,docs,max_content,stride):
    doc_stats=[]
    global_digest=hashlib.sha256()
    total_words=0; total_pieces=0; total_windows=0; empty_words=0; oversized=0
    window_hist=Counter()
    for di,words in enumerate(docs):
        counts,empty,dig=tokenize_words(tok,words)
        total_words+=len(words); total_pieces+=sum(counts); empty_words+=len(empty)
        try:
            windows=plan_windows(counts,max_content,stride)
        except ValueError:
            oversized+=1
            raise
        total_windows+=len(windows)
        window_hist[len(windows)]+=1
        global_digest.update(f"{di}|{dig}|{windows}\n".encode())
        doc_stats.append((len(words),sum(counts),len(windows),len(empty)))
    return {
      "documents":len(docs),
      "total_source_words":total_words,
      "total_wordpieces":total_pieces,
      "total_windows":total_windows,
      "tokenizer_empty_source_words":empty_words,
      "oversized_single_word_failures":oversized,
      "documents_by_window_count":{str(k):v for k,v in sorted(window_hist.items())},
      "max_windows_per_document":max(x[2] for x in doc_stats),
      "max_source_words_per_document":max(x[0] for x in doc_stats),
      "max_wordpieces_per_document":max(x[1] for x in doc_stats),
      "fixture_digest_sha256":global_digest.hexdigest(),
      "full_source_word_coverage":True,
      "gold_columns_consumed":False
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    docs=parse_docs(a.train)
    if len(docs)!=400: raise RuntimeError(f"expected 400 docs, got {len(docs)}")
    results={}
    for name,(repo,rev,maxc,stride) in MODELS.items():
        tok=AutoTokenizer.from_pretrained(repo,revision=rev,use_fast=True)
        if not tok.is_fast: raise RuntimeError(f"{name} tokenizer not fast")
        one=run_one(tok,docs,maxc,stride)
        # rerun to prove determinism
        two=run_one(tok,docs,maxc,stride)
        if one!=two: raise RuntimeError(f"{name} tokenization/windowing nondeterministic")
        one.update({
          "repo":repo,"revision":rev,"tokenizer_class":tok.__class__.__name__,
          "vocab_size":len(tok),"max_content":maxc,"stride":stride,
          "deterministic_rerun_equal":True
        })
        results[name]=one
    out={
      "state":"FEDERATION_REAL_TOKENIZER_OFFSET_WINDOWING_PREFLIGHT_PASS",
      "source":"EBM-NLP_mod fold1/train.txt",
      "source_documents":len(docs),
      "scientific_training_performed":False,
      "benchmark_test_used":False,
      "gold_labels_consumed":False,
      "models":results
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
