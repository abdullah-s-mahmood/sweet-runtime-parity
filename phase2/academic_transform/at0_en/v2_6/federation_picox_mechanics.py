#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from dataclasses import dataclass
from pathlib import Path

BOUNDARY_GRID=(0.20,0.25,0.30,0.35,0.40,0.45,0.50)
SPAN_THRESHOLD=0.50

@dataclass(frozen=True)
class Span:
    start:int
    length:int

def extract_boundary_from_prob_dist(prob,threshold):
    # Upstream enum values: OUT=0, START=1, END=2, BOTH=3, IN=4.
    if len(prob)!=5: raise ValueError("expected five boundary probabilities")
    if any(not math.isfinite(float(x)) for x in prob): raise ValueError("nonfinite boundary probability")
    value=0
    if prob[1]>threshold or prob[3]>threshold: value|=1
    if prob[2]>threshold or prob[3]>threshold: value|=2
    return value

def extract_span_boundaries(boundary_pred):
    starts=[i for i,p in enumerate(boundary_pred) if p & 1]
    ends=[i for i,p in enumerate(boundary_pred) if p & 2]
    return [(s,e) for s in starts for e in ends if s<=e]

def text_span_iou(a,b):
    a_start,a_end=a.start,a.start+a.length
    b_start,b_end=b.start,b.start+b.length
    u=max(a_end,b_end)-min(a_start,b_start)
    if u==0: return 0.0
    inter=0.0
    if a_start<=b_end and b_start<=a_end:
        inter=min(a_end,b_end)-max(a_start,b_start)
    return inter/u

def nms_span(spans,span_class,confidence,iou_threshold=0.0):
    if not(len(spans)==len(span_class)==len(confidence)): raise ValueError("NMS length mismatch")
    keep=[True]*len(spans)
    for i in range(len(spans)-1):
        if not keep[i]: continue
        for j in range(i+1,len(spans)):
            if not keep[j] or span_class[i]!=span_class[j]: continue
            iou=text_span_iou(spans[i],spans[j])
            if iou>iou_threshold:
                if spans[i].length>spans[j].length: keep[i]=False
                else: keep[j]=False
    return ([s for s,k in zip(spans,keep) if k],
            [c for c,k in zip(span_class,keep) if k],
            [q for q,k in zip(confidence,keep) if k])

def synthetic_preflight():
    # Boundary extraction: BOTH can activate both bits.
    p=[.01,.10,.10,.80,.00]
    assert extract_boundary_from_prob_dist(p,.50)==3
    assert extract_boundary_from_prob_dist(p,.80)==0  # upstream uses strict >

    # Cartesian candidate construction.
    pred=[1,0,3,0,2]
    cand=extract_span_boundaries(pred)
    expected=[(0,2),(0,4),(2,2),(2,4)]
    if cand!=expected: raise RuntimeError((cand,expected))

    # Same-class overlap uses upstream length preference, not confidence.
    spans=[Span(0,4),Span(1,2),Span(5,1)]
    cls=["P","P","P"]; conf=[.99,.60,.70]
    kept,kcls,kconf=nms_span(spans,cls,conf,0.0)
    if kept!=[Span(1,2),Span(5,1)]:
        raise RuntimeError(f"NMS fixture mismatch: {kept}")

    # Different classes are never mutually suppressed.
    kept2,_,_=nms_span([Span(0,3),Span(1,1)],["I","C"],[.6,.6],0.0)
    if len(kept2)!=2: raise RuntimeError("cross-class suppression occurred")

    # Span threshold is fixed and multi-label.
    probs={"P":.51,"I":.49,"C":.90,"O":.50}
    accepted=[k for k,v in probs.items() if v>=SPAN_THRESHOLD]
    if accepted!=["P","C","O"]: raise RuntimeError("multi-label threshold fixture failed")

    # Prospective boundary grid is immutable and development-only.
    if BOUNDARY_GRID!=(.20,.25,.30,.35,.40,.45,.50): raise RuntimeError("grid changed")

    return {
      "state":"FEDERATION_PICOX_EXECUTABLE_MECHANICS_PREFLIGHT_PASS",
      "scientific_training_performed":False,
      "benchmark_test_used":False,
      "boundary_grid":list(BOUNDARY_GRID),
      "span_threshold":SPAN_THRESHOLD,
      "boundary_candidate_fixture":cand,
      "nms_policy":"SAME_CLASS_IOU_GT_0_DROP_LONGER_SPAN; TIE_DROPS_LATER",
      "cross_class_overlap_preserved":True,
      "multi_label_span_classification":True,
      "boundary_train_batch_size_frozen_adaptation":8,
      "span_train_batch_size":16,
      "checkpoint_policy":"FINAL_EPOCH_ONLY",
      "test_time_threshold_tuning":False
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    d=synthetic_preflight()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__": main()
