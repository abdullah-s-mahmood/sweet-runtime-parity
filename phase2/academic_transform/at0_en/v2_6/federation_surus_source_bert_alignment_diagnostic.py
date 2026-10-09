#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import pathlib
import platform
import re

import transformers
import tokenizers
import huggingface_hub
from transformers import AutoTokenizer

MODEL_ID="google-bert/bert-base-uncased"
REVISION="86b5e0934494bd15c9632b12f734a8a67f723594"


def read_semicolon(path):
    with open(path,encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))


def safe_int(v):
    try:return int(str(v).strip())
    except Exception:return None


def stable_tokenizer_signature(tok):
    special={
      "cls_token":tok.cls_token,
      "sep_token":tok.sep_token,
      "pad_token":tok.pad_token,
      "unk_token":tok.unk_token,
      "mask_token":tok.mask_token,
      "model_max_length":tok.model_max_length,
      "vocab_size":tok.vocab_size,
      "padding_side":tok.padding_side,
      "truncation_side":tok.truncation_side,
    }
    return hashlib.sha256(json.dumps(special,sort_keys=True,default=str).encode()).hexdigest(),special


def punct_split(text):
    return " ".join(re.findall(r"\w+|[^\w\s]",text,flags=re.UNICODE))


def released_pair_to_zero_based_half_open(ts,te,base,end_mode,special_shift):
    if ts is None or te is None:return None
    a=ts-base-special_shift
    if end_mode=="inclusive":
        b=te-base-special_shift+1
    else:
        b=te-base-special_shift
    if a<0 or b<=a:return None
    return a,b


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION,use_fast=True,trust_remote_code=False)
    if not getattr(tok,"is_fast",False):
        raise RuntimeError("fast tokenizer required for offset mapping")
    sig,special=stable_tokenizer_signature(tok)

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}
    anns_by_article=collections.defaultdict(list)
    for r in anns:
        anns_by_article[str(r["ArticleID"]).strip()].append(r)

    variants=[]
    for base_index in (0,1):
        for end_mode in ("inclusive","exclusive"):
            for special_shift in (0,1):
                variants.append((base_index,end_mode,special_shift))

    exact_pair_counts=collections.Counter()
    exact_pair_counts_aligned_only=collections.Counter()
    raw_text_counts=collections.Counter()
    punct_text_counts=collections.Counter()
    invalid_pair_counts=collections.Counter()
    start_delta=collections.Counter()
    end_delta=collections.Counter()
    char_boundary=collections.Counter()
    source_tokenization=collections.Counter()
    by_dataset=collections.defaultdict(collections.Counter)
    by_eval=collections.defaultdict(collections.Counter)
    by_label=collections.defaultdict(collections.Counter)

    total=0
    raw_exact=0
    mismatch=0
    aligned_rows=0

    for art_id,rows in anns_by_article.items():
        art=article_by_id[art_id]
        abstract=str(art.get("Abstract") or "")
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()

        enc=tok(
            abstract,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
            return_attention_mask=False,
            return_token_type_ids=False,
        )
        offsets=[tuple(map(int,x)) for x in enc["offset_mapping"]]
        source_tokenization["articles"]+=1
        source_tokenization["total_wordpieces"]+=len(offsets)
        source_tokenization["max_wordpieces"]=max(source_tokenization["max_wordpieces"],len(offsets))

        starts=collections.defaultdict(list)
        ends=collections.defaultdict(list)
        for i,(s0,e0) in enumerate(offsets):
            if e0>s0:
                starts[s0].append(i)
                ends[e0].append(i)

        for r in rows:
            total+=1
            ann=str(r.get("Text") or "")
            s=safe_int(r.get("Start")); e=safe_int(r.get("End"))
            ts=safe_int(r.get("TokenStart")); te=safe_int(r.get("TokenEnd"))
            lid=str(r.get("LabelID") or "").strip()

            is_raw=(s is not None and e is not None and 0<=s<e<=len(abstract) and abstract[s:e]==ann)
            if is_raw: raw_exact+=1
            else: mismatch+=1

            derived_pairs=[]
            if s is not None and e is not None:
                for i in starts.get(s,[]):
                    for j in ends.get(e,[]):
                        if i<=j:
                            derived_pairs.append((i,j+1))
            aligned=bool(derived_pairs)
            if aligned:
                aligned_rows+=1
                char_boundary["ALIGNS_TO_BERT_BASE_UNCASED_WORDPIECE_BOUNDARIES"]+=1
            else:
                char_boundary["NOT_ALIGNED_TO_BERT_BASE_UNCASED_WORDPIECE_BOUNDARIES"]+=1

            for base_index,end_mode,special_shift in variants:
                key=f"BASE{base_index}_{end_mode.upper()}_SPECIALSHIFT{special_shift}"
                pair=released_pair_to_zero_based_half_open(ts,te,base_index,end_mode,special_shift)
                if pair is None or pair[1]>len(offsets):
                    invalid_pair_counts[key]+=1
                    continue

                a0,b0=pair
                if aligned and pair in derived_pairs:
                    exact_pair_counts[key]+=1
                    exact_pair_counts_aligned_only[key]+=1
                    by_dataset[key][dom]+=1
                    by_eval[key][ev]+=1
                    by_label[key][lid]+=1
                elif aligned:
                    # summarize distance from the first exact char-derived pair.
                    da=a0-derived_pairs[0][0]
                    db=b0-derived_pairs[0][1]
                    start_delta[(key,da)]+=1
                    end_delta[(key,db)]+=1

                chosen=[x for x in offsets[a0:b0] if x[1]>x[0]]
                if not chosen:
                    continue
                cs,ce=chosen[0][0],chosen[-1][1]
                raw=abstract[cs:ce]
                if raw==ann:
                    raw_text_counts[key]+=1
                if punct_split(raw)==ann:
                    punct_text_counts[key]+=1

    def top_delta(counter,key):
        arr=[(delta,count) for (k,delta),count in counter.items() if k==key]
        arr.sort(key=lambda x:(-x[1],abs(x[0]),x[0]))
        return [{"delta":d,"count":c} for d,c in arr[:30]]

    out={
      "state":"FEDERATION_SURUS_SOURCE_BERT_BASE_UNCASED_ALIGNMENT_DIAGNOSTIC_V5_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "source_tokenizer_rationale":"SURUS publication explicitly describes BERT tokenizer and links bert-base-uncased. This immutable HF revision predates the first public preprint; the publication itself did not pin a tokenizer revision.",
      "tokenizer":{
        "model_id":MODEL_ID,
        "revision":REVISION,
        "class":type(tok).__name__,
        "signature_sha256":sig,
        "specials":special,
      },
      "runtime":{
        "python":platform.python_version(),
        "transformers":transformers.__version__,
        "tokenizers":tokenizers.__version__,
        "huggingface_hub":huggingface_hub.__version__,
      },
      "total_annotations":total,
      "raw_abstract_half_open_exact":raw_exact,
      "raw_text_mismatch_rows":mismatch,
      "source_tokenization_stats":dict(source_tokenization),
      "released_char_boundary_alignment":dict(char_boundary),
      "released_char_boundary_aligned_rows":aligned_rows,
      "candidate_index_conventions":[
        {
          "key":f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}",
          "base":b,
          "end_semantics":m,
          "special_token_shift":s,
          "exact_released_token_pair_matches_char_span":int(exact_pair_counts.get(f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}",0)),
          "invalid_index_rows":int(invalid_pair_counts.get(f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}",0)),
          "raw_reconstructed_text_equals_annotation_text":int(raw_text_counts.get(f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}",0)),
          "punct_split_reconstructed_text_equals_annotation_text":int(punct_text_counts.get(f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}",0)),
          "top_start_index_deltas_vs_char_derived":top_delta(start_delta,f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}"),
          "top_end_index_deltas_vs_char_derived":top_delta(end_delta,f"BASE{b}_{m.upper()}_SPECIALSHIFT{s}"),
        }
        for b,m,s in variants
      ],
      "exact_pair_matches_by_dataset":{k:dict(sorted(v.items())) for k,v in by_dataset.items()},
      "exact_pair_matches_by_eval_type":{k:dict(sorted(v.items())) for k,v in by_eval.items()},
      "exact_pair_matches_by_label_id":{k:dict(sorted(v.items(),key=lambda x:int(x[0]))) for k,v in by_label.items()},
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "source_repair_authorized":False,
      "interpretation":"Read-only source-tokenizer reconstruction diagnostic. A high exact convention match would support, but not alone prove, original released TokenStart/TokenEnd semantics. No protocol change or training is authorized."
    }

    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
