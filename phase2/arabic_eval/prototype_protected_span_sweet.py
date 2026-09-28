"""Development-only prototype: preserve scientific protected spans exactly.

This is NOT a production implementation and does not modify the official SWEET model.
It evaluates a bounded architecture:
  exact protected-span segmentation
  + SWEET only on unprotected text
  + [UNK] pre/post hazard fallback
  + exact reinsertion of protected source spans

The 12 cases are project-authored NON_HUMAN_GOLD fidelity stress cases.
"""
import argparse, hashlib, json, platform, re, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ART=ROOT/"artifacts"

PINS={
 "nopnx":"584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6",
 "pnx":"195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3",
}

def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(4*1024*1024),b""): h.update(b)
 return h.hexdigest()

def locate_protected(source, protected):
 spans=[]
 used=[]
 for p in protected:
  starts=[m.start() for m in re.finditer(re.escape(p),source)]
  if len(starts)!=1:
   raise ValueError(f"protected span must occur exactly once: {p!r} in {source!r}; found {len(starts)}")
  a=starts[0];b=a+len(p)
  spans.append((a,b,p))
 spans.sort()
 for i,(a,b,p) in enumerate(spans):
  if i and a < spans[i-1][1]:
   raise ValueError(f"overlapping protected spans: {spans[i-1]} and {(a,b,p)}")
 return spans

def chunk_source(source, protected):
 spans=locate_protected(source,protected)
 chunks=[]
 cur=0
 for a,b,p in spans:
  if cur<a: chunks.append({"kind":"editable","text":source[cur:a]})
  chunks.append({"kind":"protected","text":source[a:b]})
  cur=b
 if cur<len(source): chunks.append({"kind":"editable","text":source[cur:]})
 return chunks

def split_outer_ws(text):
 m=re.match(r"^(\s*)(.*?)(\s*)$",text,flags=re.S)
 return m.group(1),m.group(2),m.group(3)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--nopnx",type=Path,default=ROOT/"models/nopnx")
 ap.add_argument("--pnx",type=Path,default=ROOT/"models/pnx")
 ap.add_argument("--gec-repo",type=Path,default=ROOT/"upstream/text-editing")
 ap.add_argument("--input",type=Path,default=HERE/"SCIENTIFIC_STRESS_CASES.jsonl")
 ap.add_argument("--output",type=Path,default=ART/"PROTECTED_SPAN_PROTOTYPE.json")
 args=ap.parse_args()

 git_commit=subprocess.check_output(["git","-C",str(args.gec_repo),"rev-parse","HEAD"],text=True).strip()
 assert git_commit=="4d552ca3ae98029550f27fc52aa1b22883e16e61"
 for name in PINS:
  folder=getattr(args,name)
  assert sha(folder/"pytorch_model.bin")==PINS[name]

 sys.path.insert(0,str(args.gec_repo.resolve()))
 import torch, transformers
 from transformers import BertTokenizer,BertForTokenClassification
 from gec.tag import rewrite
 assert platform.python_version().startswith("3.10.")
 assert torch.__version__.startswith("1.12.1")
 assert transformers.__version__=="4.30.0"

 models={}
 for name in ("nopnx","pnx"):
  folder=getattr(args,name)
  tok=BertTokenizer.from_pretrained(str(folder),local_files_only=True)
  model=BertForTokenClassification.from_pretrained(str(folder),local_files_only=True).eval().cpu()
  models[name]=(tok,model)

 def stage_core(core,name):
  """Return model output or exact input core on tokenizer/output hazard."""
  if not core:
   return core,{"applied":False,"reason":"empty","non_keep":0}
  tok,model=models[name]
  words=core.split()
  if not words:
   return core,{"applied":False,"reason":"whitespace_only","non_keep":0}
  encoded=tok(words,return_tensors="pt",is_split_into_words=True)
  ids=encoded["input_ids"][0].tolist()
  if tok.unk_token_id in ids:
   return core,{"applied":False,"reason":"preflight_UNK","non_keep":0}
  with torch.no_grad():
   logits=model(**encoded).logits[0]
   probs=torch.softmax(logits,dim=-1)
   maxprob,labels=probs.max(-1)
  subwords=tok.convert_ids_to_tokens(ids[1:-1])
  raw=[model.config.id2label[int(v)] for v in labels[1:-1]]
  non_keep=sum(x!="K*" for x in raw)
  if non_keep==0:
   return core,{"applied":False,"reason":"no_model_edits_exact_preserve","non_keep":0,"raw_labels":raw,"top1_confidence":maxprob[1:-1].tolist()}
  result=rewrite(subwords=[subwords],edits=[raw])
  out=result[0][0]
  if "[UNK]" in out:
   return core,{"applied":False,"reason":"postflight_UNK","non_keep":non_keep,"raw_labels":raw}
  return out,{
   "applied":out!=core,
   "reason":"safe_output",
   "non_keep":non_keep,
   "raw_labels":raw,
   "top1_confidence":maxprob[1:-1].tolist(),
  }

 def apply_to_editable(text,name):
  lead,core,trail=split_outer_ws(text)
  out,meta=stage_core(core,name)
  return lead+out+trail,meta

 def run_variant(source,protected,variant):
  chunks=chunk_source(source,protected)
  trace=[]
  out_parts=[]
  for ch in chunks:
   if ch["kind"]=="protected":
    out_parts.append(ch["text"])
    trace.append({"kind":"protected","input":ch["text"],"output":ch["text"],"exact_locked":True})
    continue
   text=ch["text"]
   metas=[]
   if variant in ("nopnx1","nopnx2","full"):
    text,m=apply_to_editable(text,"nopnx");metas.append({"stage":"nopnx1",**m})
   if variant in ("nopnx2","full"):
    text,m=apply_to_editable(text,"nopnx");metas.append({"stage":"nopnx2",**m})
   if variant=="full":
    text,m=apply_to_editable(text,"pnx");metas.append({"stage":"pnx",**m})
   out_parts.append(text)
   trace.append({"kind":"editable","input":ch["text"],"output":text,"stages":metas})
  output="".join(out_parts)
  return output,trace

 rows=[json.loads(x) for x in args.input.read_text(encoding="utf-8").splitlines() if x.strip()]
 assert len(rows)==12 and all(x["human_gold_status"]=="NON_HUMAN_GOLD" for x in rows)
 correction_path=HERE/"SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"
 corrections=json.loads(correction_path.read_text(encoding="utf-8"))["corrections"] if correction_path.exists() else {}
 def effective_protected(row):
  return corrections.get(row["case_id"],{}).get("effective_protected",row["protected"])
 variants=("nopnx1","nopnx2","full")
 cases=[]
 for row in rows:
  item={
   "case_id":row["case_id"],
   "category":row["category"],
   "source":row["source"],
   "protected_original":row["protected"],
   "protected_effective":effective_protected(row),
   "human_gold_status":"NON_HUMAN_GOLD",
   "variants":{},
  }
  for v in variants:
   protected=effective_protected(row)
   out,trace=run_variant(row["source"],protected,v)
   item["variants"][v]={
    "output":out,
    "trace":trace,
    "protected_exact":all(p in out for p in protected),
    "source_exact_unchanged":out==row["source"],
    "source_whitespace_insensitive_unchanged":re.sub(r"\\s+","",out)==re.sub(r"\\s+","",row["source"]),
    "contains_UNK":"[UNK]" in out,
   }
  cases.append(item)

 summary={}
 for v in variants:
  exact=sum(x["variants"][v]["protected_exact"] for x in cases)
  unchanged=sum(x["variants"][v]["source_exact_unchanged"] for x in cases)
  unk=sum(x["variants"][v]["contains_UNK"] for x in cases)
  compact_unchanged=sum(x["variants"][v]["source_whitespace_insensitive_unchanged"] for x in cases)
  preflight_fallbacks=0
  postflight_fallbacks=0
  applied_segments=0
  for x in cases:
   for tr in x["variants"][v]["trace"]:
    for st in tr.get("stages",[]):
     preflight_fallbacks += st.get("reason")=="preflight_UNK"
     postflight_fallbacks += st.get("reason")=="postflight_UNK"
     applied_segments += bool(st.get("applied"))
  summary[v]={
   "cases":12,
   "protected_exact_cases":exact,
   "protected_exact_rate":exact/12,
   "source_exact_unchanged_cases":unchanged,
   "source_exact_unchanged_rate":unchanged/12,
   "outputs_with_UNK":unk,
   "source_whitespace_insensitive_unchanged_cases":compact_unchanged,
   "source_whitespace_insensitive_unchanged_rate":compact_unchanged/12,
   "preflight_UNK_fallback_segments":preflight_fallbacks,
   "postflight_UNK_fallback_segments":postflight_fallbacks,
   "applied_editable_segments":applied_segments,
  }

 result={
  "status":"DEVELOPMENT_PROTOTYPE_NOT_PRODUCTION",
  "architecture":"protected-span segmentation + official SWEET on editable segments + UNK hazard fallback",
  "runtime":{"python":platform.python_version(),"torch":torch.__version__,"transformers":transformers.__version__,"gec_commit":git_commit},
  "model_sha256":PINS,
  "summary":summary,
  "cases":cases,
 }
 ART.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"protected_span_prototype":summary},ensure_ascii=False))

if __name__=="__main__":
 main()