#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
import html
import json
import pathlib
import re
import unicodedata


def read_semicolon(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def all_occurrences(text, needle):
    if needle == "":
        return []
    out=[]
    start=0
    while True:
        i=text.find(needle,start)
        if i<0:
            return out
        out.append(i)
        start=i+1


def ws_norm(s):
    return re.sub(r"\s+"," ",s).strip()


def norm_forms(s):
    return {
        "NFC": unicodedata.normalize("NFC", s),
        "NFKC": unicodedata.normalize("NFKC", s),
        "HTML": html.unescape(s),
        "WS": ws_norm(s),
        "NFKC_WS": ws_norm(unicodedata.normalize("NFKC", s)),
        "HTML_NFKC_WS": ws_norm(unicodedata.normalize("NFKC", html.unescape(s))),
    }


def safe_int(v):
    try:
        return int(str(v).strip())
    except Exception:
        return None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a=ap.parse_args()

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")

    article_by_id={str(r["ID"]).strip():r for r in articles}

    overall=collections.Counter()
    by_domain=collections.Counter()
    by_eval=collections.Counter()
    by_label=collections.Counter()
    unique_delta=collections.Counter()
    unique_abs_delta=collections.Counter()
    normalized_slice_match=collections.Counter()
    composite_counts=collections.Counter()
    mismatch_label=collections.Counter()
    mismatch_domain=collections.Counter()
    mismatch_eval=collections.Counter()
    token_delta_relation=collections.Counter()

    separators={"EMPTY":"","SPACE":" ","NL":"\n","BLANKLINE":"\n\n"}

    total=0
    exact_abstract=0
    mismatch=0

    for r in anns:
        total+=1
        art=article_by_id[str(r["ArticleID"]).strip()]
        ann=str(r.get("Text") or "")
        s=safe_int(r.get("Start"))
        e=safe_int(r.get("End"))
        lid=str(r.get("LabelID") or "").strip()
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()
        title=str(art.get("Title") or "")
        abstract=str(art.get("Abstract") or "")

        if s is not None and e is not None and 0 <= s < e <= len(abstract) and abstract[s:e] == ann:
            exact_abstract+=1
            overall["ABSTRACT_HALF_OPEN_EXACT"]+=1
            continue

        mismatch+=1
        mismatch_label[lid]+=1
        mismatch_domain[dom]+=1
        mismatch_eval[ev]+=1

        if s is not None and e is not None and 0 <= s < e <= len(title) and title[s:e] == ann:
            overall["TITLE_HALF_OPEN_EXACT"]+=1
        else:
            overall["NOT_TITLE_HALF_OPEN_EXACT"]+=1

        occ=all_occurrences(abstract,ann)
        if len(occ)==1:
            overall["ABSTRACT_UNIQUE_EXACT_OCCURRENCE_OTHER_OFFSET"]+=1
            d=occ[0]-(s if s is not None else 0)
            unique_delta[d]+=1
            unique_abs_delta[abs(d)]+=1
            ts=safe_int(r.get("TokenStart"))
            if ts is not None:
                if d==0:
                    token_delta_relation["CHAR_DELTA_ZERO"]+=1
                elif abs(d)<=5:
                    token_delta_relation["CHAR_DELTA_ABS_LE_5"]+=1
                elif abs(d)<=20:
                    token_delta_relation["CHAR_DELTA_ABS_6_20"]+=1
                else:
                    token_delta_relation["CHAR_DELTA_ABS_GT_20"]+=1
        elif len(occ)>1:
            overall["ABSTRACT_MULTIPLE_EXACT_OCCURRENCES"]+=1
        else:
            overall["ABSTRACT_NO_EXACT_OCCURRENCE"]+=1

        # Compare the released offset slice under normalization, only when in bounds.
        if s is not None and e is not None and 0 <= s < e <= len(abstract):
            slice_text=abstract[s:e]
            af=norm_forms(ann)
            sf=norm_forms(slice_text)
            matched=False
            for key in af:
                if af[key] == sf[key] and ann != slice_text:
                    normalized_slice_match[key]+=1
                    matched=True
            if matched:
                overall["OFFSET_SLICE_MATCHES_AFTER_NORMALIZATION"]+=1
            else:
                overall["OFFSET_SLICE_STILL_DIFFERS_AFTER_NORMALIZATION"]+=1
        else:
            overall["OFFSET_OUTSIDE_ABSTRACT_BOUNDS"]+=1

        # Diagnostic-only candidate composite coordinate models.
        if s is not None and e is not None and s>=0 and e>s:
            for sep_name,sep in separators.items():
                comp=title+sep+abstract
                if e<=len(comp) and comp[s:e]==ann:
                    composite_counts[f"TITLE_{sep_name}_ABSTRACT_HALF_OPEN"]+=1

        by_domain[(dom, overall.most_common(1)[0][0] if overall else "UNKNOWN")]+=0
        by_label[lid]+=1
        by_eval[ev]+=1

    top_delta=[{"delta":k,"count":v} for k,v in unique_delta.most_common(40)]
    top_abs_delta=[{"abs_delta":k,"count":v} for k,v in unique_abs_delta.most_common(40)]

    out={
      "state":"FEDERATION_SURUS_COORDINATE_MISMATCH_DIAGNOSTIC_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "total_annotations":total,
      "abstract_half_open_exact":exact_abstract,
      "mismatch_rows":mismatch,
      "mismatch_rate":mismatch/total if total else None,
      "mismatch_mechanism_counts":dict(overall),
      "normalization_match_counts":dict(normalized_slice_match),
      "composite_coordinate_match_counts":dict(composite_counts),
      "unique_occurrence_offset_delta_top40":top_delta,
      "unique_occurrence_abs_delta_top40":top_abs_delta,
      "mismatch_by_label_id":dict(sorted(mismatch_label.items(), key=lambda x:int(x[0]))),
      "mismatch_by_dataset":dict(sorted(mismatch_domain.items())),
      "mismatch_by_eval_type":dict(sorted(mismatch_eval.items())),
      "token_delta_relation":dict(token_delta_relation),
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "protected_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "interpretation":"Aggregate-only diagnostic. It does not authorize coordinate repair, normalization, dropping rows, native mapping, or training."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
