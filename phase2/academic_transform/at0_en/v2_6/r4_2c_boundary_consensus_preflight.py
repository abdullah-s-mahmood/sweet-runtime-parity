#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, pathlib
from collections import Counter
from datetime import datetime, timezone

EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_DEV_SHA="3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a"
EXPECTED_MODEL_SHA="3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c"
EXPECTED_BOUNDARY_CANONICAL="dc5920c1d3148f4b78c7fcde36d25efe78cbf3471db406a5c51e79d36b2d8431"
CLASSES=["P","I","C","O"]

def sha256(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def read_conll(path):
    out=[]; toks=[]; tags=[]
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            if toks: out.append((toks,tags)); toks=[]; tags=[]
            continue
        p=raw.split("\t")
        if len(p)!=2: p=raw.rsplit(None,1)
        if len(p)!=2: raise RuntimeError(f"bad line {raw!r}")
        tok,tag=p
        if tok=="-DOCSTART-":
            if toks: out.append((toks,tags)); toks=[]; tags=[]
            continue
        toks.append(tok); tags.append(tag)
    if toks: out.append((toks,tags))
    return out

def spans(tags):
    out=[]; cur=None
    for i,tag in enumerate(tags+["O"]):
        if tag=="O": pref=typ=None
        else: pref,typ=tag.split("-",1)
        if cur:
            if pref=="I" and typ==cur[0]: continue
            out.append((cur[0],cur[1],i)); cur=None
        if tag!="O": cur=(typ,i)
    return out

def quantile(xs,p):
    xs=sorted(xs)
    k=(len(xs)-1)*p; a=int(math.floor(k)); b=int(math.ceil(k))
    return float(xs[a] if a==b else xs[a]*(b-k)+xs[b]*(k-a))

def summarize(data):
    sc=Counter(); lens=[]; sent=[]
    for toks,tags in data:
        sent.append(len(toks))
        for c,s,e in spans(tags): sc[c]+=1; lens.append(e-s)
    return {
      "sentences":len(data),
      "span_counts":dict(sorted(sc.items())),
      "sentence_tokens":{"max":max(sent),"p95":quantile(sent,.95),"p99":quantile(sent,.99)},
      "span_length":{"max":max(lens),"median":quantile(lens,.5),"p95":quantile(lens,.95),"p99":quantile(lens,.99)}
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--train",required=True); p.add_argument("--dev",required=True)
    p.add_argument("--model",required=True); p.add_argument("--boundary-json",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args(); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=False)

    ids={"train":sha256(a.train),"dev":sha256(a.dev),"model":sha256(a.model)}
    if ids["train"]!=EXPECTED_TRAIN_SHA: raise SystemExit("train hash mismatch")
    if ids["dev"]!=EXPECTED_DEV_SHA: raise SystemExit("dev hash mismatch")
    if ids["model"]!=EXPECTED_MODEL_SHA: raise SystemExit("model hash mismatch")

    bd=json.loads(pathlib.Path(a.boundary_json).read_text(encoding="utf-8"))
    if bd.get("canonical_pre_hash_sha256")!=EXPECTED_BOUNDARY_CANONICAL:
        raise SystemExit("boundary diagnostic identity mismatch")

    train=read_conll(a.train); dev=read_conll(a.dev)
    tr=summarize(train); dv=summarize(dev)
    gold=Counter(c for _,tags in dev for c,_,_ in spans(tags))
    b=bd["threshold_false_positive_breakdown"]["0.95"]
    cap={}
    for c in CLASSES:
        tp=int(b[c]["exact_tp"])
        min_tp=max(10,math.ceil(.20*gold[c]))
        x=b[c]["breakdown"]
        overlap=x.get("BOUNDARY_ERROR_SAME_TYPE",0)+x.get("TYPE_AND_BOUNDARY_ERROR",0)+x.get("TYPE_ERROR_EXACT_BOUNDARY",0)
        spur=x.get("SPURIOUS",0)
        cap[c]={
          "gold":gold[c],"current_exact_tp":tp,"minimum_tp_required":min_tp,
          "tp_headroom":tp-min_tp,"overlap_related_errors_to_filter":overlap,
          "spurious_retained_in_oracle":spur,
          "oracle_precision_if_overlap_errors_removed":tp/(tp+spur) if tp+spur else 0.0,
          "oracle_recall_if_exact_tp_preserved":tp/gold[c],
        }

    fixtures=[
      (("P",1,4),("P",1,4),True),
      (("P",1,4),("P",1,3),False),
      (("P",1,4),("I",1,4),False),
      (("O",3,5),("O",2,5),False),
    ]
    scorer_ok=all(((x==y)==want) for x,y,want in fixtures)
    ready=(tr["sentences"]==1576 and dv["sentences"]==205 and scorer_ok and
           all(tr["span_counts"].get(c,0)>0 for c in CLASSES) and
           all(cap[c]["current_exact_tp"]>=cap[c]["minimum_tp_required"] for c in CLASSES) and
           all(cap[c]["oracle_precision_if_overlap_errors_removed"]>=.90 for c in CLASSES))

    result={
      "state":"R4_2C_PREFLIGHT_READY" if ready else "R4_2C_PREFLIGHT_NOT_READY",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "identities":ids,"boundary_diagnostic_canonical_sha256":EXPECTED_BOUNDARY_CANONICAL,
      "train":tr,"dev":dv,"threshold_0_95_capacity":cap,
      "exact_agreement_scorer_fixture_pass":scorer_ok,
      "guards":{"training_performed":False,"test_files_read":False,"factpico_used":False,
                "consumed_60_rct_holdout_used":False,"opened_30_rct_diagnostic_used":False,
                "thresholds_changed":False},
      "next_step":"FREEZE_R4_2C_TRAINING_PROTOCOL" if ready else "STOP_AND_REDESIGN_PREFLIGHT"
    }
    raw=json.dumps(result,sort_keys=True,separators=(",",":")).encode()
    result["canonical_pre_hash_sha256"]=hashlib.sha256(raw).hexdigest()
    (out/"R4_2C_BOUNDARY_CONSENSUS_PREFLIGHT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    status={"state":"COMPLETED" if ready else "FAILED","progress_percent":100.0,
            "current_stage":"R4_2C_PREFLIGHT_COMPLETE","completed_units":6,"total_units":6,
            "last_successful_checkpoint":"R4_2C_BOUNDARY_CONSENSUS_PREFLIGHT.json",
            "last_progress_at":datetime.now(timezone.utc).isoformat(),"next_expected_step":result["next_step"],
            "failure_or_stall_reason":None if ready else "PREFLIGHT_GATE_NOT_MET"}
    (out/"PROCESS_STATUS.json").write_text(json.dumps(status,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if not ready: raise SystemExit(2)
if __name__=="__main__": main()
