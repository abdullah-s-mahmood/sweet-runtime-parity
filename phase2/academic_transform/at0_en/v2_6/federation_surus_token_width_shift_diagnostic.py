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


def signature(tok):
    d={
      "cls_token":tok.cls_token,"sep_token":tok.sep_token,"pad_token":tok.pad_token,
      "unk_token":tok.unk_token,"mask_token":tok.mask_token,
      "model_max_length":tok.model_max_length,"vocab_size":tok.vocab_size,
      "padding_side":tok.padding_side,"truncation_side":tok.truncation_side,
    }
    return hashlib.sha256(json.dumps(d,sort_keys=True,default=str).encode()).hexdigest(),d


def regex_tokens(text):
    return [(m.group(0),(m.start(),m.end())) for m in re.finditer(r"\w+|[^\w\s]",text,flags=re.UNICODE)]


def derive_pair(tokens,s,e):
    if s is None or e is None:return None
    starts={}
    ends={}
    for i,(_,off) in enumerate(tokens):
        a,b=off
        if b>a:
            starts.setdefault(a,[]).append(i)
            ends.setdefault(b,[]).append(i)
    for i in starts.get(s,[]):
        for j in ends.get(e,[]):
            if i<=j:return (i,j+1)
    return None


def top(counter,n=40):
    return [{"value":k,"count":v} for k,v in counter.most_common(n)]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION,use_fast=True,trust_remote_code=False)
    if not tok.is_fast: raise RuntimeError("fast tokenizer required")
    sig,special=signature(tok)
    pre=tok.backend_tokenizer.pre_tokenizer

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}
    anns_by_article=collections.defaultdict(list)
    for r in anns:
        anns_by_article[str(r["ArticleID"]).strip()].append(r)

    seg_names=("BERT_PRETOKENIZER","REGEX_WORD_PUNCT")
    stats={name:collections.Counter() for name in seg_names}
    shift_hist={name:collections.Counter() for name in seg_names}
    shift_hist_raw_exact={name:collections.Counter() for name in seg_names}
    shift_hist_raw_mismatch={name:collections.Counter() for name in seg_names}
    article_shift_sets={name:collections.defaultdict(set) for name in seg_names}
    article_match_counts={name:collections.Counter() for name in seg_names}
    article_aligned_counts={name:collections.Counter() for name in seg_names}
    label_width_match={name:collections.Counter() for name in seg_names}
    label_width_miss={name:collections.Counter() for name in seg_names}
    dataset_width_match={name:collections.Counter() for name in seg_names}
    dataset_width_miss={name:collections.Counter() for name in seg_names}
    eval_width_match={name:collections.Counter() for name in seg_names}
    eval_width_miss={name:collections.Counter() for name in seg_names}

    total=0
    raw_exact_total=0

    for art_id,rows in anns_by_article.items():
        art=article_by_id[art_id]
        abstract=str(art.get("Abstract") or "")
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()

        segs={
          "BERT_PRETOKENIZER":[(t,(int(o[0]),int(o[1]))) for t,o in pre.pre_tokenize_str(abstract)],
          "REGEX_WORD_PUNCT":regex_tokens(abstract),
        }

        for r in rows:
            total+=1
            ann=str(r.get("Text") or "")
            s=safe_int(r.get("Start")); e=safe_int(r.get("End"))
            ts=safe_int(r.get("TokenStart")); te=safe_int(r.get("TokenEnd"))
            lid=str(r.get("LabelID") or "").strip()
            raw_exact=(s is not None and e is not None and 0<=s<e<=len(abstract) and abstract[s:e]==ann)
            if raw_exact: raw_exact_total+=1

            if ts is None or te is None:
                for name in seg_names: stats[name]["INVALID_RELEASED_TOKEN_INDEX"]+=1
                continue

            inc_width=te-ts+1
            exc_width=te-ts

            for name in seg_names:
                pair=derive_pair(segs[name],s,e)
                if pair is None:
                    stats[name]["CHAR_SPAN_NOT_ALIGNED_TO_SOURCE_UNIT"]+=1
                    continue
                stats[name]["CHAR_SPAN_ALIGNED_TO_SOURCE_UNIT"]+=1
                article_aligned_counts[name][art_id]+=1
                a0,b0=pair
                derived_width=b0-a0

                if inc_width==derived_width:
                    stats[name]["INCLUSIVE_WIDTH_MATCH"]+=1
                    article_match_counts[name][art_id]+=1
                    shift=ts-a0
                    shift_end=te-(b0-1)
                    if shift!=shift_end:
                        raise RuntimeError("inclusive width equality without equal endpoint shift")
                    shift_hist[name][shift]+=1
                    article_shift_sets[name][art_id].add(shift)
                    if raw_exact: shift_hist_raw_exact[name][shift]+=1
                    else: shift_hist_raw_mismatch[name][shift]+=1
                    label_width_match[name][lid]+=1
                    dataset_width_match[name][dom]+=1
                    eval_width_match[name][ev]+=1
                else:
                    stats[name]["INCLUSIVE_WIDTH_MISS"]+=1
                    label_width_miss[name][lid]+=1
                    dataset_width_miss[name][dom]+=1
                    eval_width_miss[name][ev]+=1

                if exc_width==derived_width:
                    stats[name]["EXCLUSIVE_WIDTH_MATCH"]+=1
                else:
                    stats[name]["EXCLUSIVE_WIDTH_MISS"]+=1

    article_summaries={}
    for name in seg_names:
        single=multi=zero=0
        dominant_cover_num=0
        dominant_cover_den=0
        unique_shift_hist=collections.Counter()
        for art_id in article_by_id:
            shifts=article_shift_sets[name].get(art_id,set())
            unique_shift_hist[len(shifts)]+=1
            if len(shifts)==0:
                zero+=1
            elif len(shifts)==1:
                single+=1
            else:
                multi+=1

        # Exact dominant coverage requires a second lightweight pass through recorded
        # aggregate information unavailable by shift/article pair; report structural
        # single/multi counts only, not an invented approximation.
        article_summaries[name]={
          "articles_zero_inclusive_width_matches":zero,
          "articles_single_observed_shift":single,
          "articles_multiple_observed_shifts":multi,
          "unique_shift_count_per_article_histogram":{str(k):v for k,v in sorted(unique_shift_hist.items())},
        }

    out={
      "state":"FEDERATION_SURUS_TOKEN_WIDTH_LOCAL_SHIFT_DIAGNOSTIC_V7_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "tokenizer":{
        "model_id":MODEL_ID,"revision":REVISION,"class":type(tok).__name__,
        "signature_sha256":sig,"specials":special,"pretokenizer_class":type(pre).__name__,
      },
      "runtime":{
        "python":platform.python_version(),"transformers":transformers.__version__,
        "tokenizers":tokenizers.__version__,"huggingface_hub":huggingface_hub.__version__,
      },
      "total_annotations":total,
      "raw_text_exact_rows":raw_exact_total,
      "segmenter_stats":{k:dict(v) for k,v in stats.items()},
      "inclusive_width_shift_histogram_top40":{k:top(v) for k,v in shift_hist.items()},
      "inclusive_width_shift_histogram_raw_exact_top40":{k:top(v) for k,v in shift_hist_raw_exact.items()},
      "inclusive_width_shift_histogram_raw_mismatch_top40":{k:top(v) for k,v in shift_hist_raw_mismatch.items()},
      "article_shift_structure":article_summaries,
      "width_match_by_label_id":{k:dict(sorted(v.items(),key=lambda x:int(x[0]))) for k,v in label_width_match.items()},
      "width_miss_by_label_id":{k:dict(sorted(v.items(),key=lambda x:int(x[0]))) for k,v in label_width_miss.items()},
      "width_match_by_dataset":{k:dict(sorted(v.items())) for k,v in dataset_width_match.items()},
      "width_miss_by_dataset":{k:dict(sorted(v.items())) for k,v in dataset_width_miss.items()},
      "width_match_by_eval_type":{k:dict(sorted(v.items())) for k,v in eval_width_match.items()},
      "width_miss_by_eval_type":{k:dict(sorted(v.items())) for k,v in eval_width_miss.items()},
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "repair_authorized":False,
      "interpretation":"Read-only width/shift diagnostic. It tests whether released token spans preserve source-unit span width despite shifted/local absolute indices. No source repair, exclusion, protocol change, or training is authorized."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
