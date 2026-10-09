#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def plan_windows(piece_counts, max_content, stride):
    if max_content < 2 or stride < 1:
        raise ValueError("invalid max_content/stride")
    n=len(piece_counts)
    if any((not isinstance(x,int)) or x <= 0 for x in piece_counts):
        raise ValueError("every retained source word must have >=1 model piece; tokenizer-empty words must be mapped to explicit UNK before planning")
    if any(x > max_content for x in piece_counts):
        raise ValueError("single source word exceeds window limit")
    prefix=[0]
    for x in piece_counts:
        prefix.append(prefix[-1]+x)
    windows=[]
    start=0
    while start<n:
        end=start
        used=0
        while end<n and used+piece_counts[end] <= max_content:
            used+=piece_counts[end]
            end+=1
        if end<=start:
            raise RuntimeError("no forward progress")
        windows.append((start,end,used))
        if end==n:
            break
        target=prefix[start]+stride
        nxt=start+1
        while nxt<n and prefix[nxt] < target:
            nxt+=1
        if nxt>=end:
            nxt=max(start+1,end-1)
        if nxt<=start:
            raise RuntimeError("stride did not advance")
        start=nxt
    covered=[False]*n
    for s,e,_ in windows:
        for i in range(s,e):
            covered[i]=True
    if not all(covered):
        raise RuntimeError("incomplete source-word coverage")
    return windows

def choose_occurrence(word_index, windows, piece_counts):
    candidates=[]
    for wi,(s,e,_) in enumerate(windows):
        if s <= word_index < e:
            left=sum(piece_counts[s:word_index])
            right=sum(piece_counts[word_index+1:e])
            context=min(left,right)
            candidates.append((context,-wi,wi))
    if not candidates:
        raise ValueError("word not covered")
    candidates.sort(reverse=True)
    return candidates[0][2]

def synthetic_preflight():
    counts=[1,2,1,3,1,1,2,4,1,2,1,1,3,1,2,1]
    w1=plan_windows(counts,10,5)
    w2=plan_windows(counts,10,5)
    if w1!=w2:
        raise RuntimeError("non-deterministic planning")
    choices=[choose_occurrence(i,w1,counts) for i in range(len(counts))]
    if len(choices)!=len(counts):
        raise RuntimeError("missing occurrence choices")

    # Label-independence fixture: arbitrary gold arrays are never passed to the planner.
    labels_a=["O"]*len(counts)
    labels_b=["B-X" if i%3==0 else "I-X" for i in range(len(counts))]
    # Hash only to prove the labels differ; planning consumes only counts.
    ha=hashlib.sha256("\n".join(labels_a).encode()).hexdigest()
    hb=hashlib.sha256("\n".join(labels_b).encode()).hexdigest()
    if ha==hb:
        raise RuntimeError("label fixture unexpectedly equal")
    if plan_windows(counts,10,5)!=w1:
        raise RuntimeError("planner changed despite identical text pieces")

    # Explicit UNK policy: zero piece counts must fail before caller substitutes one UNK piece.
    failed_zero=False
    try:
        plan_windows([1,0,1],10,5)
    except ValueError:
        failed_zero=True
    if not failed_zero:
        raise RuntimeError("tokenizer-empty source word was silently dropped")

    # Oversized single word must fail.
    failed_long=False
    try:
        plan_windows([1,11,1],10,5)
    except ValueError:
        failed_long=True
    if not failed_long:
        raise RuntimeError("oversized source word silently truncated")

    # Full coverage under several deterministic fixtures.
    fixture_windows={}
    for maxc,stride in [(6,3),(8,4),(10,5),(12,6)]:
        ws=plan_windows(counts,maxc,stride)
        fixture_windows[f"{maxc}/{stride}"]=ws

    return {
        "state":"FEDERATION_TEXT_ONLY_WINDOWING_SYNTHETIC_PREFLIGHT_PASS",
        "scientific_data_used":False,
        "benchmark_text_used":False,
        "gold_labels_consumed_by_planner":False,
        "label_independence_fixture_sha256":{"a":ha,"b":hb},
        "unk_policy":"TOKENIZER_EMPTY_SOURCE_WORD_MUST_BE_EXPLICIT_UNK_ONE_PIECE_BEFORE_PLANNING",
        "oversized_word_policy":"FAIL_CLOSED",
        "deterministic":True,
        "full_coverage":True,
        "window_fixture":w1,
        "selected_occurrence_fixture":choices,
        "multi_fixture_windows":fixture_windows,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight:
        raise SystemExit("Only synthetic preflight is authorized at this stage")
    d=synthetic_preflight()
    s=json.dumps(d,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(s,encoding="utf-8")
    print(s,end="")
if __name__=="__main__":
    main()
