"""Shared helpers for fresh tri-model voting.

Raw-only selection. Explicitly excludes the previously consumed 50-line
Cross-Corpus Agreement slice before selecting the new 50-line slice.
"""
from __future__ import annotations
from pathlib import Path
from phase2.generalization.cross_model_common import (
    sha_text,sha_file,eventize,write_jsonl,read_jsonl,protected_risk,read_nonempty_lines
)

OLD_SEED="phase2-cross-model-agreement-v1"
OLD_N=50
NEW_SEED="phase2-trimodel-vote-v1"
SLICE_N=50

def select_fresh_raw_lines(path:Path):
    lines=read_nonempty_lines(path)
    old=[(sha_text(OLD_SEED+"|"+s),i,s) for i,s in enumerate(lines,1)]
    old.sort(key=lambda x:x[0])
    excluded={i for _,i,_ in old[:min(OLD_N,len(old))]}
    fresh=[(sha_text(NEW_SEED+"|"+s),i,s) for i,s in enumerate(lines,1) if i not in excluded]
    fresh.sort(key=lambda x:x[0])
    selected=fresh[:min(SLICE_N,len(fresh))]
    assert not any(i in excluded for _,i,_ in selected)
    return selected,len(lines),sorted(excluded)
