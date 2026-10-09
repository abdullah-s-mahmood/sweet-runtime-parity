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


def regex_tokens(text):
    return [(m.group(0),(m.start(),m.end())) for m in re.finditer(r"\w+|[^\w\s]",text,flags=re.UNICODE)]


def whitespace_tokens(text):
    return [(m.group(0),(m.start(),m.end())) for m in re.finditer(r"\S+",text)]


def released_pair(ts,te,base,end_mode,special_shift):
    if ts is None or te is None:return None
    a=ts-base-special_shift
    if end_mode=="inclusive":
        b=te-base-special_shift+1
    else:
        b=te-base-special_shift
    if a<0 or b<=a:return None
    return a,b


def derive_pairs(tokens,s,e):
    if s is None or e is None:return []
    starts=collections.defaultdict(list)
    ends=collections.defaultdict(list)
    for i,(_,off) in enumerate(tokens):
        a,b=off
        if b>a:
            starts[a].append(i); ends[b].append(i)
    out=[]
    for i in starts.get(s,[]):
        for j in ends.get(e,[]):
            if i<=j: out.append((i,j+1))
    return out


def joined_text(tokens,a,b):
    return " ".join(t for t,_ in tokens[a:b])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION,use_fast=True,trust_remote_code=False)
    if not tok.is_fast:
        raise RuntimeError("fast tokenizer required")
    sig,special=stable_tokenizer_signature(tok)
    pre=tok.backend_tokenizer.pre_tokenizer

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}
    anns_by_article=collections.defaultdict(list)
    for r in anns:
        anns_by_article[str(r["ArticleID"]).strip()].append(r)

    segmenters=("BERT_PRETOKENIZER","REGEX_WORD_PUNCT","WHITESPACE")
    variants=[]
    for base_index in (0,1):
        for end_mode in ("inclusive","exclusive"):
            for special_shift in (0,1):
                variants.append((base_index,end_mode,special_shift))

    exact_pair=collections.Counter()
    boundary_align=collections.Counter()
    raw_join_match=collections.Counter()
    joined_space_match=collections.Counter()
    invalid=collections.Counter()
    source_counts=collections.Counter()
    start_delta=collections.Counter()
    end_delta=collections.Counter()

    total=0
    raw_exact=0

    for art_id,rows in anns_by_article.items():
        art=article_by_id[art_id]
        abstract=str(art.get("Abstract") or "")

        bert_pre=[(t,(int(off[0]),int(off[1]))) for t,off in pre.pre_tokenize_str(abstract)]
        segs={
          "BERT_PRETOKENIZER":bert_pre,
          "REGEX_WORD_PUNCT":regex_tokens(abstract),
          "WHITESPACE":whitespace_tokens(abstract),
        }
        for name,toks in segs.items():
            source_counts[f"{name}_articles"]+=1
            source_counts[f"{name}_total_tokens"]+=len(toks)
            source_counts[f"{name}_max_tokens"]=max(source_counts[f"{name}_max_tokens"],len(toks))

        for r in rows:
            total+=1
            ann=str(r.get("Text") or "")
            s=safe_int(r.get("Start")); e=safe_int(r.get("End"))
            ts=safe_int(r.get("TokenStart")); te=safe_int(r.get("TokenEnd"))
            if s is not None and e is not None and 0<=s<e<=len(abstract) and abstract[s:e]==ann:
                raw_exact+=1

            for seg_name,toks in segs.items():
                derived=derive_pairs(toks,s,e)
                if derived:
                    boundary_align[seg_name]+=1

                for b,m,shift in variants:
                    vk=f"BASE{b}_{m.upper()}_SPECIALSHIFT{shift}"
                    key=f"{seg_name}::{vk}"
                    pair=released_pair(ts,te,b,m,shift)
                    if pair is None or pair[1]>len(toks):
                        invalid[key]+=1
                        continue
                    a0,b0=pair

                    if derived and pair in derived:
                        exact_pair[key]+=1
                    elif derived:
                        start_delta[(key,a0-derived[0][0])]+=1
                        end_delta[(key,b0-derived[0][1])]+=1

                    cs=toks[a0][1][0]
                    ce=toks[b0-1][1][1]
                    if abstract[cs:ce]==ann:
                        raw_join_match[key]+=1
                    if joined_text(toks,a0,b0)==ann:
                        joined_space_match[key]+=1

    def top_delta(counter,key):
        arr=[(d,c) for (k,d),c in counter.items() if k==key]
        arr.sort(key=lambda x:(-x[1],abs(x[0]),x[0]))
        return [{"delta":d,"count":c} for d,c in arr[:20]]

    results=[]
    for seg_name in segmenters:
        for b,m,shift in variants:
            vk=f"BASE{b}_{m.upper()}_SPECIALSHIFT{shift}"
            key=f"{seg_name}::{vk}"
            results.append({
              "segmenter":seg_name,
              "convention":vk,
              "exact_released_pair_matches_char_span":int(exact_pair.get(key,0)),
              "invalid_index_rows":int(invalid.get(key,0)),
              "raw_reconstructed_slice_equals_annotation_text":int(raw_join_match.get(key,0)),
              "space_joined_tokens_equal_annotation_text":int(joined_space_match.get(key,0)),
              "top_start_delta_vs_char_derived":top_delta(start_delta,key),
              "top_end_delta_vs_char_derived":top_delta(end_delta,key),
            })

    results.sort(key=lambda x:(-x["exact_released_pair_matches_char_span"],-x["space_joined_tokens_equal_annotation_text"],x["segmenter"],x["convention"]))

    out={
      "state":"FEDERATION_SURUS_BERT_PRETOKEN_SOURCE_UNIT_DIAGNOSTIC_V6_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "tokenizer":{
        "model_id":MODEL_ID,
        "revision":REVISION,
        "class":type(tok).__name__,
        "signature_sha256":sig,
        "specials":special,
        "pretokenizer_class":type(pre).__name__,
      },
      "runtime":{
        "python":platform.python_version(),
        "transformers":transformers.__version__,
        "tokenizers":tokenizers.__version__,
        "huggingface_hub":huggingface_hub.__version__,
      },
      "total_annotations":total,
      "raw_text_exact_rows":raw_exact,
      "segmenter_token_stats":dict(source_counts),
      "char_span_boundary_alignment_by_segmenter":{k:int(boundary_align.get(k,0)) for k in segmenters},
      "candidate_results_ranked":results,
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "repair_authorized":False,
      "interpretation":"Read-only source-unit diagnostic. It tests whether released token indices correspond to BERT pre-token, regex word/punctuation, or whitespace units. No result authorizes source repair, row exclusion, protocol change, or training."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
