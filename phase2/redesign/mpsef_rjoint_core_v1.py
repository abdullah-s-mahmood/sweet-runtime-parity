#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib, string, sys, unicodedata
from pathlib import Path

MATCHING_VERSION="MPSEF_RJOINT_M2_MATCH_V1"
FAMILY_MAP_VERSION="MPSEF_TARGET_FAMILY_MAP_V1"
UNICODE_PUNCT_SYMBOL=frozenset(
    chr(i) for i in range(0x110000)
    if unicodedata.category(chr(i))[0] in {"P","S"}
)
PNX_SET=frozenset(string.punctuation)|UNICODE_PUNCT_SYMBOL|frozenset("&amp;")
FAMILIES=("INSERT","DELETE","SPLIT","MERGE","SUBSTITUTE","COMPLEX")

def norm(s): return " ".join((s or "").strip().split())

def sha_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def strip_pnx_ws(s):
    return "".join(ch for ch in s if ch not in PNX_SET and not ch.isspace())

def pnx_chars(s):
    return "".join(ch for ch in s if ch in PNX_SET)

def target_scope(original,correction):
    pchg=pnx_chars(original)!=pnx_chars(correction)
    lchg=strip_pnx_ws(original)!=strip_pnx_ws(correction)
    if pchg and not lchg: return "PUNCTUATION_ONLY"
    if pchg and lchg: return "MIXED_PUNCT_LINGUISTIC"
    return "LINGUISTIC"

def target_family(start,end,original,correction):
    src=original.split() if original else []
    cor=correction.split() if correction else []
    if start==end and correction: return "INSERT"
    if start<end and not correction: return "DELETE"
    if start<end and len(src)==1 and len(cor)>1 and "".join(src)=="".join(cor):
        return "SPLIT"
    if start<end and len(src)>1 and len(cor)==1 and "".join(src)=="".join(cor):
        return "MERGE"
    if start<end and correction and len(src)==len(cor): return "SUBSTITUTE"
    return "COMPLEX"

def import_m2(upstream_root):
    sys.path.insert(0,str(Path(upstream_root).resolve()))
    m2=importlib.import_module("gec.utils.m2scorer.m2scorer")
    lev=importlib.import_module("gec.utils.m2scorer.levenshtein")
    return m2,lev

def candidate_edit_seq(lev,candidate,source,gold,max_unchanged_words=2):
    ct,st=candidate.split(),source.split()
    l1,b1=lev.levenshtein_matrix(st,ct,1,1,1)
    l2,b2=lev.levenshtein_matrix(st,ct,1,1,2)
    v1,e1,d1,x1=lev.edit_graph(l1,b1)
    v2,e2,d2,x2=lev.edit_graph(l2,b2)
    V,E,dist,edits=lev.merge_graph(v1,v2,e1,e2,d1,d2,x1,x2)
    V,E,dist,edits=lev.transitive_arcs(V,E,dist,edits,max_unchanged_words,False)
    local=lev.set_weights(E,dist,edits,gold,False,False)
    return lev.best_edit_seq_bf(V,E,local,edits,False)

def matched_indices(lev,edit_seq,gold):
    out=[]; last=0
    for e in reversed(edit_seq):
        for i in range(last,len(gold)):
            if lev.matchEdit(e,gold[i],False):
                out.append(i); last=i+1; break
    return out

def score_candidate(lev,candidate,source,gold):
    seq=candidate_edit_seq(lev,candidate,source,gold,2)
    matched=matched_indices(lev,seq,gold)
    return {
        "matched_indices":matched,
        "correct":len(matched),
        "proposed":len(seq),
        "gold":len(gold),
        "extra":len(seq)-len(matched),
    }

def build_targets(uid,gold):
    out=[]
    for idx,(start,end,original,corrections) in enumerate(gold):
        if len(corrections)!=1:
            raise RuntimeError(f"{uid}: expected one correction alternative")
        correction=corrections[0]
        scope=target_scope(original,correction)
        family=target_family(start,end,original,correction)
        tid=sha_text(f"{uid}\t{idx}\t{start}\t{end}\t{original}\t{correction}\t{MATCHING_VERSION}")
        out.append({
            "target_id":tid,"gold_index":idx,"start":start,"end":end,
            "original":original,"correction":correction,
            "scope":scope,"family":family,
        })
    return out

def safe_div(a,b): return None if b==0 else a/b

def self_test(upstream_root):
    _,lev=import_m2(upstream_root)
    source="انا احب العلم"
    gold=[(0,1,"انا",["أنا"]),(3,3,"",["."])]
    targets=build_targets("SYNTH",gold)
    keep=[i for i,t in enumerate(targets) if t["scope"]!="PUNCTUATION_ONLY"]
    assert keep==[0]
    sg=[gold[i] for i in keep]
    ok=score_candidate(lev,"أنا احب العلم",source,sg)
    bad=score_candidate(lev,source,source,sg)
    assert ok["correct"]==1 and ok["extra"]==0
    assert bad["correct"]==0 and bad["proposed"]==0
    assert target_family(0,1,"يابطل","يا بطل")=="SPLIT"
    assert target_family(0,2,"يا بطل","يابطل")=="MERGE"
    assert target_scope("",".")=="PUNCTUATION_ONLY"
    return True
