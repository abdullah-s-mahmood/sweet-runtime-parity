#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
import difflib
import html
import json
import pathlib
import re
import unicodedata


def read_semicolon(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def safe_int(v):
    try:
        return int(str(v).strip())
    except Exception:
        return None


def all_occurrences(text, needle):
    if needle == "":
        return []
    out=[]
    p=0
    while True:
        i=text.find(needle,p)
        if i<0:
            return out
        out.append(i)
        p=i+1


def norm_ws(s):
    return re.sub(r"\s+"," ",s).strip()


def norm_nfkc_ws(s):
    return norm_ws(unicodedata.normalize("NFKC",s))


def norm_html_nfkc_ws(s):
    return norm_ws(unicodedata.normalize("NFKC",html.unescape(s)))


def bucket_ratio(r):
    if r>=0.999: return "GE_0.999"
    if r>=0.99: return "0.99_0.999"
    if r>=0.95: return "0.95_0.99"
    if r>=0.90: return "0.90_0.95"
    if r>=0.75: return "0.75_0.90"
    if r>=0.50: return "0.50_0.75"
    return "LT_0.50"


def bucket_count(n):
    if n==0:return "0"
    if n==1:return "1"
    if n<=5:return "2_5"
    if n<=10:return "6_10"
    if n<=25:return "11_25"
    if n<=50:return "26_50"
    if n<=100:return "51_100"
    return "GT_100"


def token_models(abstract, ann, ts, te):
    counts=[]
    toks=list(re.finditer(r"\S+",abstract))
    if ts is None or te is None:
        return counts
    models=[
      ("WS_0_BASED_INCLUSIVE",ts,te+1),
      ("WS_0_BASED_EXCLUSIVE",ts,te),
      ("WS_1_BASED_INCLUSIVE",ts-1,te),
      ("WS_1_BASED_EXCLUSIVE",ts-1,te-1),
    ]
    for name,a,b in models:
        if a is None or b is None or a<0 or b<=a or b>len(toks):
            continue
        s=toks[a].start()
        e=toks[b-1].end()
        if abstract[s:e]==ann:
            counts.append(name)
    return counts


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}

    per_article=collections.defaultdict(lambda:{"total":0,"mismatch":0,"dataset":"","eval":""})
    field_exact=collections.Counter()
    field_norm=collections.Counter()
    mismatch_kind=collections.Counter()
    similarity=collections.Counter()
    len_delta=collections.Counter()
    token_model_counts=collections.Counter()
    label_counts=collections.Counter()
    dataset_counts=collections.Counter()
    eval_counts=collections.Counter()
    unique_offset_delta=collections.Counter()
    unique_occurrence_count=collections.Counter()

    text_fields=["Title","Abstract","Indication","ArticleType"]
    total=0
    mismatch=0

    for r in anns:
        total+=1
        art=article_by_id[str(r["ArticleID"]).strip()]
        ann=str(r.get("Text") or "")
        s=safe_int(r.get("Start"))
        e=safe_int(r.get("End"))
        ts=safe_int(r.get("TokenStart"))
        te=safe_int(r.get("TokenEnd"))
        lid=str(r.get("LabelID") or "").strip()
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()
        abstract=str(art.get("Abstract") or "")

        aid=str(r["ArticleID"]).strip()
        pa=per_article[aid]
        pa["total"]+=1
        pa["dataset"]=dom
        pa["eval"]=ev

        exact=(s is not None and e is not None and 0<=s<e<=len(abstract) and abstract[s:e]==ann)
        if exact:
            continue

        mismatch+=1
        pa["mismatch"]+=1
        label_counts[lid]+=1
        dataset_counts[dom]+=1
        eval_counts[ev]+=1

        # Exact or normalized occurrence anywhere in released text fields.
        any_exact=False
        any_norm=False
        ann_nfkc=norm_nfkc_ws(ann)
        ann_html=norm_html_nfkc_ws(ann)
        for field in text_fields:
            src=str(art.get(field) or "")
            if ann and ann in src:
                field_exact[field]+=1
                any_exact=True
            src_nfkc=norm_nfkc_ws(src)
            src_html=norm_html_nfkc_ws(src)
            if ann_nfkc and ann_nfkc in src_nfkc:
                field_norm[f"{field}:NFKC_WS"]+=1
                any_norm=True
            if ann_html and ann_html in src_html:
                field_norm[f"{field}:HTML_NFKC_WS"]+=1
                any_norm=True

        if any_exact:
            mismatch_kind["EXACT_OCCURRENCE_IN_SOME_RELEASED_FIELD"]+=1
        elif any_norm:
            mismatch_kind["NORMALIZED_OCCURRENCE_IN_SOME_RELEASED_FIELD"]+=1
        else:
            mismatch_kind["NO_OCCURRENCE_IN_RELEASED_TEXT_FIELDS"]+=1

        occ=all_occurrences(abstract,ann)
        unique_occurrence_count[len(occ)]+=1
        if len(occ)==1 and s is not None:
            unique_offset_delta[occ[0]-s]+=1

        if s is not None and e is not None and 0<=s<e<=len(abstract):
            sl=abstract[s:e]
            ratio=difflib.SequenceMatcher(None,sl,ann,autojunk=False).ratio()
            similarity[bucket_ratio(ratio)]+=1
            len_delta[len(ann)-len(sl)]+=1
        else:
            similarity["OFFSET_OUT_OF_BOUNDS"]+=1

        for name in token_models(abstract,ann,ts,te):
            token_model_counts[name]+=1

    affected=[]
    fully=partially=exact_only=0
    mismatch_hist=collections.Counter()
    mismatch_rate_bins=collections.Counter()
    affected_by_dataset=collections.Counter()
    affected_by_eval=collections.Counter()

    for aid,x in per_article.items():
        if x["mismatch"]==0:
            exact_only+=1
            continue
        affected.append((x["mismatch"],x["total"],x["dataset"],x["eval"]))
        affected_by_dataset[x["dataset"]]+=1
        affected_by_eval[x["eval"]]+=1
        if x["mismatch"]==x["total"]:
            fully+=1
        else:
            partially+=1
        mismatch_hist[bucket_count(x["mismatch"])]+=1
        rate=x["mismatch"]/x["total"]
        if rate==1: b="1.00"
        elif rate>=.75:b="0.75_1.00"
        elif rate>=.50:b="0.50_0.75"
        elif rate>=.25:b="0.25_0.50"
        elif rate>=.10:b="0.10_0.25"
        else:b="LT_0.10"
        mismatch_rate_bins[b]+=1

    affected_sorted=sorted(affected,reverse=True)
    top_counts=[{"mismatch_rows":m,"annotation_rows":t,"rate":m/t} for m,t,_,_ in affected_sorted[:40]]

    out={
      "state":"FEDERATION_SURUS_COORDINATE_MISMATCH_ARTICLE_FIELD_DIAGNOSTIC_V2_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "total_articles":len(articles),
      "total_annotations":total,
      "mismatch_rows":mismatch,
      "affected_articles":len(affected),
      "exact_only_articles":exact_only,
      "fully_mismatched_articles":fully,
      "partially_mismatched_articles":partially,
      "affected_articles_by_dataset":dict(sorted(affected_by_dataset.items())),
      "affected_articles_by_eval_type":dict(sorted(affected_by_eval.items())),
      "mismatch_rows_by_dataset":dict(sorted(dataset_counts.items())),
      "mismatch_rows_by_eval_type":dict(sorted(eval_counts.items())),
      "mismatch_rows_by_label_id":dict(sorted(label_counts.items(),key=lambda x:int(x[0]))),
      "per_article_mismatch_count_bins":dict(mismatch_hist),
      "per_article_mismatch_rate_bins":dict(mismatch_rate_bins),
      "top40_anonymous_article_mismatch_profiles":top_counts,
      "exact_occurrence_anywhere_by_released_field":dict(field_exact),
      "normalized_occurrence_anywhere_by_released_field":dict(field_norm),
      "released_field_occurrence_classification":dict(mismatch_kind),
      "abstract_exact_occurrence_count_distribution":{str(k):v for k,v in sorted(unique_occurrence_count.items())},
      "unique_abstract_occurrence_offset_delta_top50":[{"delta":k,"count":v} for k,v in unique_offset_delta.most_common(50)],
      "offset_slice_similarity_bins":dict(similarity),
      "annotation_minus_offset_slice_length_delta_top50":[{"delta":k,"count":v} for k,v in len_delta.most_common(50)],
      "whitespace_token_coordinate_models_exact_match_counts":dict(token_model_counts),
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "interpretation":"Aggregate-only mechanism diagnostic. No boundary repair, row dropping, normalization policy, or training is authorized by this result."
    }

    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
