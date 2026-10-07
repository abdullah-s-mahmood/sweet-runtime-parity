#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib
from r43_contextual_pair_preflight import parse_train

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"

def sha_file(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def sha_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    if sha_file(a.train)!=TRAIN_SHA: raise RuntimeError("TRAIN identity mismatch")
    m=json.loads(a.manifest.read_text())
    got=m.pop("manifest_sha256",None)
    if got!=MANIFEST_SHA or sha_text(json.dumps(m,sort_keys=True,separators=(",",":")))!=MANIFEST_SHA:
        raise RuntimeError("manifest identity mismatch")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); old=set(m["excluded_old_select_documents"])
    if len(design)!=256 or len(verify)!=64 or design&verify or design&old or verify&old:
        raise RuntimeError("partition identity mismatch")
    docs,empty,bad=parse_train(a.train)
    if bad or len(docs)!=400: raise RuntimeError("source parse mismatch")
    outdocs=[]
    for di in sorted(design):
        sents=[{"tokens":tokens,"tags":tags} for tokens,tags in docs[di]]
        outdocs.append({"original_document":di,"sentences":sents})
    payload={"state":"R44_DESIGN_SOURCE_MATERIALIZED",
             "source_train_sha256":TRAIN_SHA,"r44_manifest_sha256":MANIFEST_SHA,
             "documents":outdocs}
    p=a.out/"R44_DESIGN_SOURCE.json"
    p.write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    h=sha_file(p)
    summary={"state":"R44_DESIGN_SOURCE_PACKAGE_PASS","source_train_sha256":TRAIN_SHA,
             "r44_manifest_sha256":MANIFEST_SHA,"design_documents":len(outdocs),
             "sentences":sum(len(x["sentences"]) for x in outdocs),
             "tokens":sum(len(s["tokens"]) for x in outdocs for s in x["sentences"]),
             "design_source_sha256":h,
             "excluded_counts":{"verify_internal_documents":len(verify),"old_r43_select_documents":len(old)},
             "guards":{"scientific_training":False,"output_contains_verify":False,"output_contains_old_select":False}}
    (a.out/"R44_DESIGN_SOURCE_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":main()
