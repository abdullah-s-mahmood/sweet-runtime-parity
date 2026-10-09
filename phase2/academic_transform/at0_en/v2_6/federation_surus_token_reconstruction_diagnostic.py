#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
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


def is_punct(ch):
    cp=ord(ch)
    if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
        return True
    return unicodedata.category(ch).startswith("P")


def split_punct_preserve(text):
    out=[]
    buff=[]
    def flush():
        if buff:
            out.append("".join(buff))
            buff.clear()
    for ch in text:
        if ch.isspace():
            flush()
        elif is_punct(ch):
            flush()
            out.append(ch)
        else:
            buff.append(ch)
    flush()
    return " ".join(out)


def add_space_around_ascii_punct(text):
    return re.sub(r"\s+"," ",re.sub(r"([!-/:-@\[-`{-~])",r" \1 ",text)).strip()


def remove_space_around_punct(text):
    s=re.sub(r"\s+([!-/:-@\[-`{-~])",r"\1",text)
    s=re.sub(r"([!-/:-@\[-`{-~])\s+",r"\1",s)
    return s


def remove_space_before_punct(text):
    return re.sub(r"\s+([!-/:-@\[-`{-~])",r"\1",text)


def remove_space_after_punct(text):
    return re.sub(r"([!-/:-@\[-`{-~])\s+",r"\1",text)


def space_hyphen_slash_percent(text):
    return re.sub(r"\s+"," ",re.sub(r"([\-/%])",r" \1 ",text)).strip()


def space_parentheses(text):
    return re.sub(r"\s+"," ",re.sub(r"([()\[\]])",r" \1 ",text)).strip()


def transformations(src):
    return {
      "PUNCT_SPLIT_UNICODE_PRESERVE": split_punct_preserve(src),
      "ASCII_PUNCT_SPACE_AROUND": add_space_around_ascii_punct(src),
      "HYPHEN_SLASH_PERCENT_SPACE": space_hyphen_slash_percent(src),
      "PARENTHESES_SPACE": space_parentheses(src),
      "WS_COLLAPSE_ONLY": re.sub(r"\s+"," ",src).strip(),
    }


def inverse_ann_forms(ann):
    return {
      "REMOVE_SPACE_AROUND_ASCII_PUNCT": remove_space_around_punct(ann),
      "REMOVE_SPACE_BEFORE_ASCII_PUNCT": remove_space_before_punct(ann),
      "REMOVE_SPACE_AFTER_ASCII_PUNCT": remove_space_after_punct(ann),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    base=a.root/"data/dataset"
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    article_by_id={str(r["ID"]).strip():r for r in articles}

    direct=collections.Counter()
    inverse=collections.Counter()
    first_matching_rule=collections.Counter()
    unmatched_label=collections.Counter()
    matched_label=collections.Counter()
    matched_domain=collections.Counter()
    unmatched_domain=collections.Counter()
    matched_eval=collections.Counter()
    unmatched_eval=collections.Counter()
    char_diff_features=collections.Counter()

    mismatch_total=0
    explained_any=0

    ordered_rules=[
      "PUNCT_SPLIT_UNICODE_PRESERVE",
      "ASCII_PUNCT_SPACE_AROUND",
      "HYPHEN_SLASH_PERCENT_SPACE",
      "PARENTHESES_SPACE",
      "WS_COLLAPSE_ONLY",
    ]

    for r in anns:
        art=article_by_id[str(r["ArticleID"]).strip()]
        ann=str(r.get("Text") or "")
        s=safe_int(r.get("Start"))
        e=safe_int(r.get("End"))
        abstract=str(art.get("Abstract") or "")
        lid=str(r.get("LabelID") or "").strip()
        dom=str(art.get("Dataset") or "").strip()
        ev=str(art.get("EvalType") or "").strip()

        if s is None or e is None or not (0<=s<e<=len(abstract)):
            continue
        src=abstract[s:e]
        if src==ann:
            continue

        mismatch_total+=1

        # Difference-feature aggregates.
        if any(is_punct(c) for c in src) or any(is_punct(c) for c in ann):
            char_diff_features["HAS_PUNCTUATION"]+=1
        if "-" in src or "-" in ann:
            char_diff_features["HAS_HYPHEN"]+=1
        if "/" in src or "/" in ann:
            char_diff_features["HAS_SLASH"]+=1
        if "%" in src or "%" in ann:
            char_diff_features["HAS_PERCENT"]+=1
        if "(" in src or ")" in src or "(" in ann or ")" in ann:
            char_diff_features["HAS_PAREN"]+=1

        tf=transformations(src)
        matched=[]
        for name,val in tf.items():
            if val==ann:
                direct[name]+=1
                matched.append(name)

        inv=inverse_ann_forms(ann)
        for name,val in inv.items():
            if val==src:
                inverse[name]+=1
                matched.append(name)

        # Also test lower-case variants diagnostically only.
        for name,val in tf.items():
            if val.casefold()==ann.casefold() and val!=ann:
                direct[name+"_CASEFOLD"]+=1

        if matched:
            explained_any+=1
            first=None
            for name in ordered_rules:
                if name in matched:
                    first=name
                    break
            if first is None:
                first=sorted(matched)[0]
            first_matching_rule[first]+=1
            matched_label[lid]+=1
            matched_domain[dom]+=1
            matched_eval[ev]+=1
        else:
            unmatched_label[lid]+=1
            unmatched_domain[dom]+=1
            unmatched_eval[ev]+=1

    out={
      "state":"FEDERATION_SURUS_COORDINATE_TOKEN_RECONSTRUCTION_DIAGNOSTIC_V3_COMPLETE",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "mismatch_rows_at_released_offsets":mismatch_total,
      "rows_explained_by_at_least_one_fixed_spacing_rule":explained_any,
      "rows_unexplained_by_fixed_spacing_rules":mismatch_total-explained_any,
      "direct_source_slice_transform_matches":dict(direct),
      "inverse_annotation_transform_matches":dict(inverse),
      "first_matching_rule_counts":dict(first_matching_rule),
      "difference_feature_counts":dict(char_diff_features),
      "explained_by_label_id":dict(sorted(matched_label.items(),key=lambda x:int(x[0]))),
      "unexplained_by_label_id":dict(sorted(unmatched_label.items(),key=lambda x:int(x[0]))),
      "explained_by_dataset":dict(sorted(matched_domain.items())),
      "unexplained_by_dataset":dict(sorted(unmatched_domain.items())),
      "explained_by_eval_type":dict(sorted(matched_eval.items())),
      "unexplained_by_eval_type":dict(sorted(unmatched_eval.items())),
      "raw_text_emitted":False,
      "pmid_values_emitted":False,
      "article_ids_emitted":False,
      "scientific_metric_computed":False,
      "scientific_fit_performed":False,
      "repair_authorized":False,
      "interpretation":"Aggregate-only fixed token/punctuation-spacing diagnostic. Matching a rule is mechanistic evidence only and does not authorize source repair or training."
    }

    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
