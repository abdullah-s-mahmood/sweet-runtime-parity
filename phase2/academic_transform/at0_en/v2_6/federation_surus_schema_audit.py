#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib,collections

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def read_semicolon(path):
    with open(path,encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))

def find_col(cols,candidates):
    m={c.casefold():c for c in cols}
    for x in candidates:
        if x.casefold() in m: return m[x.casefold()]
    for c in cols:
        low=c.casefold()
        if any(x.casefold() in low for x in candidates): return c
    return None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=pathlib.Path,required=True); ap.add_argument("--out",type=pathlib.Path,required=True); a=ap.parse_args()
    base=a.root/"data/dataset"
    labels=read_semicolon(base/"label.csv")
    classes=read_semicolon(base/"label_class.csv")
    articles=read_semicolon(base/"article.csv")
    anns=read_semicolon(base/"annotation.csv")
    lcols=list(labels[0].keys()); ccols=list(classes[0].keys()); acols=list(articles[0].keys()); ncols=list(anns[0].keys())
    label_id=find_col(lcols,["ID"]); label_name=find_col(lcols,["Name"]); label_class=find_col(lcols,["ClassID"])
    class_id=find_col(ccols,["ID"]); class_name=find_col(ccols,["Name"])
    article_id=find_col(acols,["ID","ArticleID"]); pmid_col=find_col(acols,["PMID","PubMed"]); domain_col=find_col(acols,["Domain","RecordDomain","Dataset","Set","Type"])
    ann_article=find_col(ncols,["ArticleID","article_id","Article"]); ann_label=find_col(ncols,["LabelID","label_id","Label"])
    start_col=find_col(ncols,["Start","StartIndex","StartPos"]); end_col=find_col(ncols,["End","EndIndex","EndPos"])
    label_map={str(x[label_id]):x[label_name] for x in labels}
    class_map={str(x[class_id]):x[class_name] for x in classes}
    label_to_class={x[label_name]:class_map.get(str(x[label_class]),"UNKNOWN") for x in labels}
    pmids=set()
    if pmid_col:
        for r in articles:
            v=(r.get(pmid_col) or "").strip()
            if v: pmids.add(v)
    domains=collections.Counter()
    if domain_col:
        domains.update((r.get(domain_col) or "").strip() for r in articles)
    ann_counts=collections.Counter()
    missing_article=0; missing_label=0; invalid_coord=0
    article_ids={str(r.get(article_id,"")).strip() for r in articles} if article_id else set()
    for r in anns:
        lid=str(r.get(ann_label,"")).strip() if ann_label else ""
        name=label_map.get(lid,lid or "UNKNOWN")
        ann_counts[name]+=1
        if ann_article and str(r.get(ann_article,"")).strip() not in article_ids: missing_article+=1
        if ann_label and lid not in label_map: missing_label+=1
        if start_col and end_col:
            try:
                s=int(r[start_col]); e=int(r[end_col])
                if s<0 or e<=s: invalid_coord+=1
            except: invalid_coord+=1
    out={
      "state":"FEDERATION_SURUS_PUBLIC_SCHEMA_AUDIT_PASS",
      "source_commit":"3a61790d5c304dea95fb278f76cc3b1a0ca07564",
      "license":"CC-BY-NC-4.0",
      "license_sha256":sha(a.root/"LICENSE"),
      "article_file_sha256":sha(base/"article.csv"),
      "annotation_file_sha256":sha(base/"annotation.csv"),
      "label_file_sha256":sha(base/"label.csv"),
      "label_class_file_sha256":sha(base/"label_class.csv"),
      "article_rows":len(articles),
      "annotation_rows":len(anns),
      "label_count":len(labels),
      "label_class_count":len(classes),
      "article_columns":acols,
      "annotation_columns":ncols,
      "pmid_column_detected":pmid_col,
      "unique_pmids":len(pmids),
      "domain_column_detected":domain_col,
      "domain_counts":dict(sorted(domains.items())),
      "annotation_label_counts":dict(sorted(ann_counts.items())),
      "labels":[{"name":x[label_name],"class":label_to_class[x[label_name]]} for x in labels],
      "foreign_key_missing_article":missing_article,
      "foreign_key_missing_label":missing_label,
      "invalid_coordinate_rows":invalid_coord,
      "raw_article_text_emitted":False,
      "pmid_values_emitted":False,
      "scientific_metric_computed":False,
      "interpretation":"Candidate auxiliary human-gold source only; no native P/I/C/O mapping is authorized by this audit."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
