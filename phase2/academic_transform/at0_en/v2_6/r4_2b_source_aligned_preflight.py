#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import Counter

from transformers import AutoTokenizer

LABELS = ["O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"]

def sha256_path(path:pathlib.Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_conll(path:pathlib.Path):
    sents=[]; toks=[]; tags=[]
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.rstrip()
        if not line or line.startswith("-DOCSTART-") or (line.startswith("###") and line.endswith("$$$")):
            if toks:
                sents.append((toks,tags)); toks=[]; tags=[]
            continue
        parts=line.split("\t")
        if len(parts)!=2:
            parts=line.rsplit(None,1)
        if len(parts)!=2:
            raise RuntimeError(f"bad line: {line!r}")
        tok,tag=parts
        if tag not in LABELS:
            raise RuntimeError(f"unknown label {tag!r}")
        toks.append(tok); tags.append(tag)
    if toks:
        sents.append((toks,tags))
    return sents

def entities(tags):
    out=[]; cur=None
    for i,tag in enumerate(tags+["O"]):
        if tag.startswith("B-"):
            if cur is not None: out.append(cur)
            cur=[tag[2:],i,i+1]
        elif tag.startswith("I-"):
            typ=tag[2:]
            if cur is not None and cur[0]==typ:
                cur[2]=i+1
            else:
                if cur is not None: out.append(cur)
                cur=[typ,i,i+1]
        else:
            if cur is not None:
                out.append(cur); cur=None
    return [tuple(x) for x in out]

def wordpiece_lengths(tokens,tokenizer):
    lens=[]; empty=0
    for tok in tokens:
        n=len(tokenizer.tokenize(tok))
        if n<=0:
            empty+=1; n=1
        lens.append(n)
    return lens,empty

def current_hard_truncation_stats(sentences,tokenizer,max_length=256):
    budget=max_length-tokenizer.num_special_tokens_to_add(pair=False)
    out={
        "content_wordpiece_budget":budget,
        "sentences":len(sentences),
        "sentences_over_budget":0,
        "words_lost":0,
        "entities_total":0,
        "entities_fully_preserved":0,
        "entities_partially_or_fully_lost":0,
        "lost_entities_by_class":Counter(),
        "empty_tokenized_words":0,
    }
    for toks,tags in sentences:
        lens,empty=wordpiece_lengths(toks,tokenizer)
        out["empty_tokenized_words"]+=empty
        if sum(lens)>budget: out["sentences_over_budget"]+=1
        used=0; included=[]
        for n in lens:
            included.append(used < budget)
            used += n
        out["words_lost"]+=sum(1 for x in included if not x)
        ents=entities(tags)
        out["entities_total"]+=len(ents)
        for typ,s,e in ents:
            ok=all(included[i] for i in range(s,e))
            if ok: out["entities_fully_preserved"]+=1
            else:
                out["entities_partially_or_fully_lost"]+=1
                out["lost_entities_by_class"][typ]+=1
    out["lost_entities_by_class"]=dict(sorted(out["lost_entities_by_class"].items()))
    return out

def source_safe_split(sentences,tokenizer,max_length=256):
    budget=max_length-4
    output=[]; empty=0
    for toks,tags in sentences:
        seg_t=[]; seg_g=[]; seg_len=0
        for tok,tag in zip(toks,tags):
            n=len(tokenizer.tokenize(tok))
            if n<=0:
                empty+=1
                continue
            if seg_len+n>budget and seg_t:
                carry_start=len(seg_g)
                j=len(seg_g)-1
                while j>=0 and seg_g[j]!="O":
                    carry_start=j; j-=1
                if carry_start < len(seg_g):
                    carry_t=seg_t[carry_start:]
                    carry_g=seg_g[carry_start:]
                    output.append((seg_t[:carry_start],seg_g[:carry_start]))
                    seg_t=carry_t; seg_g=carry_g
                    seg_len=sum(len(tokenizer.tokenize(x)) or 1 for x in seg_t)
                else:
                    output.append((seg_t,seg_g))
                    seg_t=[]; seg_g=[]; seg_len=0
            seg_t.append(tok); seg_g.append(tag); seg_len+=n
        if seg_t: output.append((seg_t,seg_g))
    output=[x for x in output if x[0]]
    max_wp=max((sum(len(tokenizer.tokenize(t)) or 1 for t in toks) for toks,_ in output),default=0)
    return output,{
        "content_wordpiece_budget":budget,
        "output_sentences":len(output),
        "max_output_wordpieces":max_wp,
        "empty_tokenized_words":empty
    }

def entity_count(sentences):
    c=Counter()
    for _,tags in sentences:
        for typ,_,_ in entities(tags): c[typ]+=1
    return dict(sorted(c.items()))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--dev",type=pathlib.Path,required=True)
    args=ap.parse_args()

    tokenizer=AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True,use_fast=True)
    train=read_conll(args.train)
    dev=read_conll(args.dev)
    train_split,train_split_meta=source_safe_split(train,tokenizer)
    dev_split,dev_split_meta=source_safe_split(dev,tokenizer)

    result={
        "state":"R4_2B_SOURCE_ALIGNED_PREFLIGHT_COMPLETE",
        "source_reference":{
            "repo":"BIDS-Xu-Lab/section_specific_annotation_of_PICO",
            "commit":"bc4b878773192f38b2600ec830ca4208b82f7dc0",
            "files":["PICO_ner.py","run_ner.py","utils_ner.py"]
        },
        "model_revision":"d673b8835373c6fa116d6d8006b33d48734e305d",
        "data_sha256":{"train":sha256_path(args.train),"dev":sha256_path(args.dev)},
        "protocol_delta":{
            "current_v5":{
                "seed":20261005,
                "weight_decay":0.01,
                "warmup_ratio":0.10,
                "eval_batch_size":16,
                "max_epochs":10,
                "early_stopping_patience":2,
                "load_best_model_at_end":True,
                "sequence_handling":"FAST_TOKENIZER_HARD_TRUNCATION_AT_256"
            },
            "published_repo_source_aligned":{
                "seed":42,
                "weight_decay":0.0,
                "warmup_steps":0,
                "eval_batch_size":8,
                "epochs":10,
                "early_stopping":False,
                "load_best_model_at_end":False,
                "sequence_handling":"UPDATE_DATA_TO_MAX_LEN_SAFE_SPLIT_EFFECTIVE_252"
            },
            "unchanged":{
                "learning_rate":5e-5,
                "train_batch_size":8,
                "max_seq_length":256,
                "gradient_accumulation_steps":1
            }
        },
        "train":{
            "input_sentences":len(train),
            "entities_by_class":entity_count(train),
            "current_hard_truncation":current_hard_truncation_stats(train,tokenizer),
            "source_safe_split":train_split_meta,
            "source_split_entities_by_class":entity_count(train_split)
        },
        "dev":{
            "input_sentences":len(dev),
            "entities_by_class":entity_count(dev),
            "current_hard_truncation":current_hard_truncation_stats(dev,tokenizer),
            "source_safe_split":dev_split_meta,
            "source_split_entities_by_class":entity_count(dev_split)
        },
        "guards":{
            "training_run":False,
            "test_files_read":False,
            "factpico_used":False,
            "consumed_60_rct_holdout_used":False,
            "opened_30_rct_diagnostic_used":False
        },
        "decision_rule":"AUTHORIZE_ONE_SOURCE_ALIGNED_DEV_TRAIN_ONLY_IF_PROTOCOL_DELTA_IS_MATERIAL_OR_HARD_TRUNCATION_LOSES_GOLD_ENTITY_CONTENT"
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
