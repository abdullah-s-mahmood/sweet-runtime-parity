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


MODEL_ID="microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract"
REVISION="d673b8835373c6fa116d6d8006b33d48734e305d"
EXPECTED_TOKENIZER_SIGNATURE="088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81"


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
    sig=hashlib.sha256(json.dumps(special,sort_keys=True,default=str).encode()).hexdigest()
    return sig,special


def punct_split(text):
    # Same fixed label-independent punctuation-spacing diagnostic family as V3.
    return " ".join(re.findall(r"\w+|[^\w\s]",text,flags=re.UNICODE))


def variant_span(offsets,ts,te,name):
    if ts is None or te is None:
        return None
    if name=="ZERO_BASED_INCLUSIVE":
        a,b=ts,te+1
    elif name=="ZERO_BASED_EXCLUSIVE":
        a,b=ts,te
    elif name=="ONE_BASED_INCLUSIVE":
        a,b=ts-1,te
    elif name=="ONE_BASED_EXCLUSIVE":
        a,b=ts-1,te-1
    else:
        raise ValueError(name)
    if a<0 or b<=a or b>len(offsets):
        return None
    # Fast tokenizers may produce zero-length offsets for special-like artifacts.
    chosen=[x for x in offsets[a:b] if x[1]>x[0]]
    if not chosen:
        return None
    return chosen[0][0],chosen[-1][1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    tok=AutoTokenizer.from_pretrained(
        MODEL_ID,revision=REVISION,use_fast=True,trust_remote_code=False
    )
    if not getattr(tok,"is_fast",False):
        raise RuntimeError("fast tokenizer required for offset mapping")
    sig,special=stable_tokenizer_signature(tok)
    if sig!=EXPECTED_TOKENIZER_SIGNATURE:
        raise RuntimeError(f"tokenizer signature mismatch: {sig}")

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}
    anns_by_article=collections.defaultdict(list)
    for r in anns:
        anns_by_article[str(r["ArticleID"]).strip()].append(r)

    variants=[
      "ZERO_BASED_INCLUSIVE",
      "ZERO_BASED_EXCLUSIVE",
      "ONE_BASED_INCLUSIVE",
      "ONE_BASED_EXCLUSIVE",
    ]

    counts={v:collections.Counter() for v in variants}
    residual_counts={v:collections.Counter() for v in variants}
    released_char_boundary_token_match=collections.Counter()
    tokenization_stats=collections.Counter()
    invalid_released_token_indices=collections.Counter()
    by_dataset={v:collections.Counter() for v in variants}
    by_eval={v:collections.Counter() for v in variants}
    by_label={v:collections.Counter() for v in variants}

    total=0
    raw_exact=0
    residual=0

    for art_id,rows in anns_by_article.items():
        art=article_by_id[art_id]
        abstract=str(art.get("Abstract") or "")
        enc=tok(
            abstract,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
            return_attention_mask=False,
            return_token_type_ids=False,
        )
        offsets=[tuple(map(int,x)) for x in enc["offset_mapping"]]
        tokenization_stats["articles_tokenized"]+=1
        tokenization_stats["total_wordpieces"]+=len(offsets)
        tokenization_stats["max_wordpieces"]=max(tokenization_stats["max_wordpieces"],len(offsets))
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()

        # Boundary lookup for released char spans.
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
            else: residual+=1

            if s is not None and e is not None:
                exact_pairs=0
                for i in starts.get(s,[]):
                    for j in ends.get(e,[]):
                        if i<=j: exact_pairs+=1
                if exact_pairs:
                    released_char_boundary_token_match["RELEASED_CHAR_SPAN_ALIGNS_TO_TOKEN_BOUNDARIES"]+=1
                else:
                    released_char_boundary_token_match["RELEASED_CHAR_SPAN_NOT_TOKEN_BOUNDARY_ALIGNED"]+=1

            for v in variants:
                span=variant_span(offsets,ts,te,v)
                if span is None:
                    counts[v]["INVALID_INDEX_RANGE"]+=1
                    if not is_raw:
                        residual_counts[v]["INVALID_INDEX_RANGE"]+=1
                    continue
                ds,de=span
                raw=abstract[ds:de]
                if s==ds and e==de:
                    counts[v]["DERIVED_CHAR_EQUALS_RELEASED_CHAR"]+=1
                    if not is_raw:
                        residual_counts[v]["DERIVED_CHAR_EQUALS_RELEASED_CHAR"]+=1
                else:
                    counts[v]["DERIVED_CHAR_DIFFERS_RELEASED_CHAR"]+=1
                    if not is_raw:
                        residual_counts[v]["DERIVED_CHAR_DIFFERS_RELEASED_CHAR"]+=1

                if raw==ann:
                    counts[v]["DERIVED_RAW_EQUALS_ANNOTATION_TEXT"]+=1
                    by_dataset[v][dom]+=1
                    by_eval[v][ev]+=1
                    by_label[v][lid]+=1
                    if not is_raw:
                        residual_counts[v]["DERIVED_RAW_EQUALS_ANNOTATION_TEXT"]+=1
                elif punct_split(raw)==ann:
                    counts[v]["DERIVED_PUNCT_SPLIT_EQUALS_ANNOTATION_TEXT"]+=1
                    if not is_raw:
                        residual_counts[v]["DERIVED_PUNCT_SPLIT_EQUALS_ANNOTATION_TEXT"]+=1
                else:
                    counts[v]["DERIVED_TEXT_UNEXPLAINED"]+=1
                    if not is_raw:
                        residual_counts[v]["DERIVED_TEXT_UNEXPLAINED"]+=1

    out={
      "state":"FEDERATION_SURUS_PINNED_BIOMEDBERT_TOKEN_ALIGNMENT_DIAGNOSTIC_V4_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "tokenizer":{
        "model_id":MODEL_ID,
        "revision":REVISION,
        "class":type(tok).__name__,
        "signature_sha256":sig,
        "expected_signature_sha256":EXPECTED_TOKENIZER_SIGNATURE,
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
      "raw_mismatch_rows":residual,
      "tokenization_stats":dict(tokenization_stats),
      "released_char_boundary_alignment":dict(released_char_boundary_token_match),
      "token_index_variant_all_rows":{v:dict(c) for v,c in counts.items()},
      "token_index_variant_raw_mismatch_rows_only":{v:dict(c) for v,c in residual_counts.items()},
      "derived_raw_exact_matches_by_dataset":{v:dict(sorted(c.items())) for v,c in by_dataset.items()},
      "derived_raw_exact_matches_by_eval_type":{v:dict(sorted(c.items())) for v,c in by_eval.items()},
      "derived_raw_exact_matches_by_label_id":{v:dict(sorted(c.items(),key=lambda x:int(x[0]))) for v,c in by_label.items()},
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "repair_authorized":False,
      "interpretation":"Read-only pinned-tokenizer alignment diagnostic. No token-index convention, source repair, row exclusion, or training is authorized by this result alone."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
