#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib
import numpy as np
import torch
from transformers import AutoTokenizer, BertModel

EXPECTED_BASE_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"
EXPECTED_DESIGN_SHA="f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18"

def sha256(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def first_positions(enc,bi,n):
    seen=set(); pos=[]
    for j,w in enumerate(enc.word_ids(batch_index=bi)):
        if w is not None and w not in seen:
            seen.add(w); pos.append(j)
    if len(pos)!=n: raise RuntimeError(f"wordpiece truncation {len(pos)}!={n}")
    return pos

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",type=pathlib.Path,required=True)
    ap.add_argument("--design-source",type=pathlib.Path,required=True)
    ap.add_argument("--design-summary",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    ap.add_argument("--batch-size",type=int,default=8)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)

    if sha256(a.base/"model.safetensors")!=EXPECTED_BASE_SHA: raise RuntimeError("base SHA")
    if (a.base/"pytorch_model.bin").exists(): raise RuntimeError("pickle weights present")
    ds=json.loads(a.design_source.read_text())
    dss=json.loads(a.design_summary.read_text())
    if ds.get("state")!="R44_DESIGN_SOURCE_MATERIALIZED" or dss.get("state")!="R44_DESIGN_SOURCE_PACKAGE_PASS":
        raise RuntimeError("design state")
    if sha256(a.design_source)!=EXPECTED_DESIGN_SHA or dss.get("design_source_sha256")!=EXPECTED_DESIGN_SHA:
        raise RuntimeError("design SHA")

    rows=[]
    for d in ds["documents"]:
        di=int(d["original_document"])
        for si,s in enumerate(d["sentences"]):
            tokens=list(s["tokens"])  # labels intentionally not accessed
            rows.append((di,si,tokens))
    if len(rows)!=1034: raise RuntimeError(f"sentence count {len(rows)}")
    total_tokens=sum(len(x[2]) for x in rows)
    if total_tokens!=26595: raise RuntimeError(f"token count {total_tokens}")

    tok=AutoTokenizer.from_pretrained(a.base,local_files_only=True,use_fast=True)
    model=BertModel.from_pretrained(a.base,local_files_only=True)
    model.eval(); all_vec=[]; index=[]; offset=0
    with torch.no_grad():
        for st in range(0,len(rows),a.batch_size):
            ch=rows[st:st+a.batch_size]
            enc=tok([x[2] for x in ch],is_split_into_words=True,padding=True,truncation=True,max_length=256,return_tensors="pt")
            h=model(input_ids=enc["input_ids"],attention_mask=enc["attention_mask"]).last_hidden_state
            for bi,(di,si,tokens) in enumerate(ch):
                pos=first_positions(enc,bi,len(tokens))
                arr=h[bi,pos,:].cpu().float().numpy()
                if arr.shape!=(len(tokens),768): raise RuntimeError("context shape")
                all_vec.append(arr)
                index.append({"document":di,"sentence":si,"offset":offset,"length":len(tokens),
                              "tokens_sha256":hashlib.sha256(json.dumps(tokens,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()})
                offset+=len(tokens)

    vec=np.concatenate(all_vec,axis=0)
    if vec.shape!=(26595,768): raise RuntimeError(f"final shape {vec.shape}")
    if not np.isfinite(vec).all(): raise RuntimeError("nonfinite context")

    npy=a.out/"R44B_BASE_CONTEXT_FLOAT32.npy"
    np.save(npy,vec,allow_pickle=False)
    idx=a.out/"R44B_BASE_CONTEXT_INDEX.json"
    idx.write_text(json.dumps(index,indent=2,sort_keys=True)+"\n")
    summary={
      "state":"R44B_BASE_CONTEXT_CACHE_PASS",
      "base_model_sha256":EXPECTED_BASE_SHA,
      "design_source_sha256":EXPECTED_DESIGN_SHA,
      "documents":256,"sentences":1034,"tokens":26595,
      "shape":[26595,768],"dtype":"float32",
      "labels_used":False,
      "context_npy_sha256":sha256(npy),
      "index_sha256":sha256(idx),
      "verify_internal_used":False,
      "old_select_used":False,
      "protected_data_used":False,
    }
    (a.out/"R44B_BASE_CONTEXT_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__": main()
