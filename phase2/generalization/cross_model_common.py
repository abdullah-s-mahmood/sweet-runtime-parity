"""Shared pure-Python helpers for cross-model agreement generalization.

No gold logic lives here.
"""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep

SEED="phase2-cross-model-agreement-v1"
SLICE_N=50

def sha_text(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha_file(path:Path)->str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def read_nonempty_lines(path:Path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def select_raw_lines(path:Path):
    lines=read_nonempty_lines(path)
    scored=[(sha_text(SEED+"|"+s),i,s) for i,s in enumerate(lines,1)]
    scored.sort(key=lambda x:x[0])
    return scored[:min(SLICE_N,len(scored))],len(lines)

def eventize(source:str,output:str,line_id:int,line_hash:str,prefix:str):
    ops,total=align(source,output)
    rows=[]
    for gi,g in enumerate(group_nonkeep(ops),1):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        kinds=[x["op"] for x in g]
        if srcs:
            lexical=[x["lexical_index"] for x in srcs]
            span=[min(lexical),max(lexical)+1]
        else:
            span=[-1,-1]
        sb=[x["base"] for x in srcs]
        ob=[x["base"] for x in outs]
        rows.append({
            "event_id":f"{prefix}-{line_id:05d}-{gi:03d}",
            "line_id":line_id,
            "line_hash":line_hash,
            "event_type":kinds[0] if len(kinds)==1 else "COMPLEX",
            "primitive_ops":kinds,
            "source_lexical_span":span,
            "source_surfaces":[x["surface"] for x in srcs],
            "output_surfaces":[x["surface"] for x in outs],
            "source_bases":sb,
            "output_bases":ob,
            "source_hash":sha_text("\u241f".join(sb)),
            "output_hash":sha_text("\u241f".join(ob)),
            "event_cost":sum(float(x["cost"]) for x in g),
            "passage_alignment_cost":float(total),
        })
    return rows

def write_jsonl(path:Path,rows):
    path.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")

def read_jsonl(path:Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def protected_risk(event)->list[str]:
    reasons=[]
    surfaces=list(event.get("source_surfaces") or [])+list(event.get("output_surfaces") or [])
    joined=" ".join(surfaces)
    if re.search(r"[0-9A-Za-z]",joined):
        reasons.append("DIGIT_OR_LATIN_RISK")
    if re.search(r"\[[0-9]+\]|[%=<>±]",joined):
        reasons.append("SCIENTIFIC_SYMBOL_OR_CITATION_RISK")
    if event.get("source_bases")==event.get("output_bases"):
        reasons.append("NO_BASE_LETTER_CHANGE")
    return reasons
