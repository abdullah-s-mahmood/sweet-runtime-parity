#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
import torch
from transformers import AutoConfig, AutoTokenizer, BertForSequenceClassification, DataCollatorWithPadding

from r4_2c_boundary_consensus_train import (
    SEED, MAX_SPAN_WIDTH_WORDS, EXPECTED_TRAIN_SHA, EXPECTED_CONVERTED_SHA,
    read_conll, spans_from_tags, convert_safe_base, seed_all, sha256_path
)

def choose(pool,key):
    if not pool:
        return None
    h=int(hashlib.sha256(key.encode("utf-8")).hexdigest(),16)
    return pool[h % len(pool)]

def overlaps(a,b,c,d):
    return max(a,c) < min(b,d)

def build_examples(sentences):
    positives=[]
    pos_keys=set()
    for si,(tokens,tags) in enumerate(sentences):
        for typ,s,e in spans_from_tags(tags):
            if e-s > MAX_SPAN_WIDTH_WORDS:
                raise RuntimeError(f"gold width exceeds {MAX_SPAN_WIDTH_WORDS}")
            k=(si,s,e)
            if k in pos_keys:
                raise RuntimeError(f"duplicate positive boundary {k}")
            pos_keys.add(k)
            positives.append({"sentence_index":si,"start":s,"end":e,"label":1,"kind":"VALID","type":typ})

    hard_selected=[]
    nonover_selected=[]
    for p in positives:
        si,s,e=p["sentence_index"],p["start"],p["end"]
        tokens=sentences[si][0]
        golds=spans_from_tags(sentences[si][1])
        gold_bounds={(gs,ge) for _,gs,ge in golds}
        key=f"{si}|{p['type']}|{s}|{e}|{SEED}"

        raw=[(s-1,e),(s+1,e),(s,e-1),(s,e+1)]
        pool=[]
        for a,b in raw:
            if a<0 or b>len(tokens) or b<=a: continue
            if b-a>MAX_SPAN_WIDTH_WORDS: continue
            if (a,b) in gold_bounds: continue
            pool.append((a,b))
        pick=choose(pool,key+"|BOUNDARY_SHIFT")
        if pick is not None:
            hard_selected.append((si,pick[0],pick[1]))

        w=e-s
        pool2=[]
        if 0 < w <= MAX_SPAN_WIDTH_WORDS and w <= len(tokens):
            for a in range(0,len(tokens)-w+1):
                b=a+w
                if (a,b) in gold_bounds: continue
                if any(overlaps(a,b,gs,ge) for _,gs,ge in golds): continue
                pool2.append((a,b))
        pick2=choose(pool2,key+"|NON_OVERLAP")
        if pick2 is not None:
            nonover_selected.append((si,pick2[0],pick2[1]))

    hard_unique=sorted(set(hard_selected))
    nonover_unique=sorted(set(nonover_selected))
    invalid_keys=set(hard_unique)|set(nonover_unique)
    collisions=invalid_keys & pos_keys
    if collisions:
        raise RuntimeError(f"positive/negative collision: {sorted(collisions)[:5]}")

    examples=list(positives)
    for si,s,e in hard_unique:
        examples.append({"sentence_index":si,"start":s,"end":e,"label":0,"kind":"BOUNDARY_SHIFT"})
    for si,s,e in nonover_unique:
        examples.append({"sentence_index":si,"start":s,"end":e,"label":0,"kind":"NON_OVERLAP"})

    canon=[]
    for x in sorted(examples,key=lambda z:(z["label"],z["sentence_index"],z["start"],z["end"],z["kind"])):
        si,s,e=x["sentence_index"],x["start"],x["end"]
        canon.append({
            "sentence_index":si,"start":s,"end":e,"label":x["label"],"kind":x["kind"],
            "tokens":sentences[si][0][s:e],
        })
    digest=hashlib.sha256(json.dumps(canon,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()
    return examples,{
        "positive_count":len(positives),
        "hard_boundary_selected_raw":len(hard_selected),
        "hard_boundary_unique":len(hard_unique),
        "nonoverlap_selected_raw":len(nonover_selected),
        "nonoverlap_unique":len(nonover_unique),
        "invalid_unique":len(invalid_keys),
        "total_examples":len(examples),
        "positive_negative_collisions":len(collisions),
        "dataset_sha256":digest,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    seed_all()

    if sha256_path(args.train)!=EXPECTED_TRAIN_SHA:
        raise RuntimeError("train hash mismatch")

    sentences=read_conll(args.train,expected_empty_surface_tag_counts={"O":5,"I-I":5,"I-P":6,"I-O":1})
    examples,counts=build_examples(sentences)

    converted=args.out/"converted_base"
    tok,converted_sha=convert_safe_base(args.model_dir,converted)
    if converted_sha!=EXPECTED_CONVERTED_SHA:
        raise RuntimeError("converted base mismatch")

    max_wp=0
    for x in examples:
        span=sentences[x["sentence_index"]][0][x["start"]:x["end"]]
        enc=tok(span,is_split_into_words=True,truncation=False)
        max_wp=max(max_wp,len(enc["input_ids"]))
        if len(enc["input_ids"])>256:
            raise RuntimeError(f"validity example >256 wordpieces: {len(enc['input_ids'])}")

    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=2,
        id2label={0:"INVALID",1:"VALID"},label2id={"INVALID":0,"VALID":1})
    model=BertForSequenceClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    coll=DataCollatorWithPadding(tokenizer=tok,return_tensors="pt")

    pos=[x for x in examples if x["label"]==1][:4]
    neg=[x for x in examples if x["label"]==0][:4]
    smoke=pos+neg
    feats=[]
    for x in smoke:
        span=sentences[x["sentence_index"]][0][x["start"]:x["end"]]
        enc=tok(span,is_split_into_words=True,truncation=False)
        enc["labels"]=x["label"]
        feats.append(enc)
    batch=coll(feats)
    opt=torch.optim.AdamW(model.parameters(),lr=2e-5,weight_decay=.01)
    loss=model(**batch).loss
    if not torch.isfinite(loss):
        raise RuntimeError("validity smoke loss non-finite")
    loss.backward()
    good=any(p.grad is not None and torch.isfinite(p.grad).all() and torch.count_nonzero(p.grad)>0 for p in model.parameters())
    if not good:
        raise RuntimeError("validity gradients invalid")
    opt.step()

    result={
        "state":"R4_2D_SPAN_VALIDITY_PREFLIGHT_PASS",
        "counts":counts,
        "max_wordpieces_with_specials":max_wp,
        "validity_threshold":0.50,
        "validity_model":{"num_labels":2,"epochs":3,"learning_rate":2e-5,"weight_decay":.01,"batch":16,"seed":SEED},
        "smoke_loss":float(loss.detach()),
        "finite_gradients":True,
        "converted_base_sha256":converted_sha,
        "frozen_component_identities":{"r4b_model_sha256":"3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c","r4_2c_boundary_model_sha256":"a56a24572ffd59b93c71e7b68b4ceb63f52ee17e6247fa5f4f857b826de788ae","r4_2c_type_model_sha256":"d531a61cf76e38cfec307e53a95382fbf3cb107d4a7b0d3677a1304b7f30b8a0"},
        "guards":{
            "train_only":True,
            "dev_read":False,
            "test_files_read":False,
            "factpico_used":False,
            "consumed_holdout_used":False,
            "scientific_full_training_performed":False,
        }
    }
    (args.out/"R4_2D_SPAN_VALIDITY_PREFLIGHT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
