from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "2.4-gate0-v1"

CITATION_RE = re.compile(r"\[(CIT_[A-Za-z0-9_]+)\]")
TIME_RE = re.compile(r"\b(?:[01]\d|2[0-3]):[0-5]\d\b")
SEED_RE = re.compile(r"\bseed\s+(\d+)\b", re.I)
NUM_COUNT_RE = re.compile(r"\b(\d+)\s+(iterations?|vehicles?|densities?|nodes?|tasks?|reports?|measurements?)\b", re.I)
WORD_COUNT_RE = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(collection\s+vehicles?|traffic\s+densities?|iterations?|vehicles?|nodes?|tasks?|reports?|measurements?)\b",
    re.I,
)
GROUP_RE = re.compile(r"\bGroup\s+[A-Z]\b")
SYMBOL_RE = re.compile(r"[A-Za-z]_(?:\d+|[A-Za-z])")
EQUATION_RE = re.compile(r"\b[A-Za-z]_[A-Za-z0-9]+\s*=\s*[^.;]+?(?=\s+for\b|[.;])")
NUMBER_RE = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\w.])")
UNIT_RE = re.compile(r"\b(ms|s|sec(?:ond)?s?|min(?:ute)?s?|h(?:our)?s?|km|m|pps|mbps|gbps)\b|%", re.I)

WORD_NUM = {
    "one":1,"two":2,"three":3,"four":4,"five":5,"six":6,
    "seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,
}
UNIT_NORM = {
    "second":"s","seconds":"s","sec":"s","secs":"s","s":"s",
    "millisecond":"ms","milliseconds":"ms","ms":"ms",
    "minute":"min","minutes":"min","min":"min",
    "hour":"h","hours":"h","h":"h",
    "km":"km","m":"m","pps":"pps","mbps":"Mbps","gbps":"Gbps","%":"%",
}

def overlaps(span: tuple[int,int], occupied: Iterable[tuple[int,int]]) -> bool:
    a,b=span
    return any(a < y and x < b for x,y in occupied)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _candidate(kind: str, m: re.Match, normalized, quantity_kind="NOT_APPLICABLE"):
    return {
        "anchor_type":kind,
        "raw":m.group(0),
        "normalized":normalized,
        "quantity_kind":quantity_kind,
        "span":(m.start(),m.end()),
    }

def extract_anchor_candidates(text: str) -> list[dict]:
    out=[]
    occupied=[]

    for m in CITATION_RE.finditer(text):
        out.append(_candidate("CITATION",m,m.group(1)))
        occupied.append((m.start(),m.end()))

    equations=[]
    for m in EQUATION_RE.finditer(text):
        raw=m.group(0).strip()
        end=m.start()+len(raw)
        item={"anchor_type":"EQUATION","raw":raw,"normalized":re.sub(r"\s+","",raw),"quantity_kind":"NOT_APPLICABLE","span":(m.start(),end)}
        out.append(item); equations.append(item["span"])

    times=[]
    for m in TIME_RE.finditer(text):
        out.append(_candidate("TIME",m,m.group(0)))
        times.append((m.start(),m.end()))

    seeds=[]
    for m in SEED_RE.finditer(text):
        out.append(_candidate("SEED",m,int(m.group(1)),"ABSOLUTE"))
        seeds.append((m.start(),m.end()))

    counts=[]
    for m in NUM_COUNT_RE.finditer(text):
        if overlaps((m.start(),m.end()),seeds):
            continue
        out.append(_candidate("COUNT",m,int(m.group(1)),"ABSOLUTE"))
        counts.append((m.start(),m.end()))
    for m in WORD_COUNT_RE.finditer(text):
        out.append(_candidate("COUNT",m,WORD_NUM[m.group(1).lower()],"ABSOLUTE"))
        counts.append((m.start(),m.end()))

    groups=[]
    for m in GROUP_RE.finditer(text):
        out.append(_candidate("GROUP",m,m.group(0)))
        groups.append((m.start(),m.end()))

    symbols=[]
    citation_spans=[x["span"] for x in out if x["anchor_type"]=="CITATION"]
    for m in SYMBOL_RE.finditer(text):
        if overlaps((m.start(),m.end()),citation_spans):
            continue
        out.append(_candidate("SYMBOL",m,m.group(0)))
        symbols.append((m.start(),m.end()))

    blocked_for_number=citation_spans+equations+times+seeds+counts+symbols
    for m in NUMBER_RE.finditer(text):
        if overlaps((m.start(),m.end()),blocked_for_number):
            continue
        raw=m.group(0)
        val=float(raw) if "." in raw else int(raw)
        out.append(_candidate("VALUE",m,val,"ABSOLUTE"))

    for m in UNIT_RE.finditer(text):
        raw=m.group(0)
        # Unit tokens are accepted only when immediately preceded by a numeric expression
        prefix=text[max(0,m.start()-16):m.start()]
        if not re.search(r"[-+]?\d+(?:\.\d+)?\s*$",prefix):
            continue
        out.append(_candidate("UNIT",m,UNIT_NORM.get(raw.lower(),raw),"NOT_APPLICABLE"))

    out.sort(key=lambda x:(x["span"][0],x["span"][1],x["anchor_type"]))
    return out

def build_anchor_graph(case: dict) -> dict:
    text=case["source_text"]
    candidates=extract_anchor_candidates(text)
    evidence=[]
    anchors=[]
    for i,c in enumerate(candidates,1):
        aid=f"{case['case_id']}-ANC-{i:03d}"
        sid=f"{case['case_id']}-SP-{i:03d}"
        a,b=c["span"]
        evidence.append({
            "span_id":sid,
            "container_type":"PARAGRAPH",
            "container_id":f"{case['case_id']}:source",
            "char_start":a,
            "char_end":b,
            "quote":text[a:b],
        })
        anchors.append({
            "anchor_id":aid,
            "anchor_type":c["anchor_type"],
            "raw":c["raw"],
            "normalized":c["normalized"],
            "quantity_kind":c["quantity_kind"],
            "denominator":None,
            "uncertainty":None,
            "precision":None,
            "criticality":"MATERIAL",
            "evidence_span_ids":[sid],
        })

    return {
        "schema_version":SCHEMA_VERSION,
        "source_identity":{
            "document_id":case["case_id"],
            "source_version":"at0-en-cases-v1",
            "source_sha256":case["source_sha256"],
            "paragraph_id":case["case_id"],
            "allowed_context_ids":[],
        },
        "evidence_spans":evidence,
        "anchors":anchors,
        "assertions":[],
        "relations":[],
        "coverage":{
            "claim_bearing_span_ids":[],
            "represented_span_ids":[],
            "unrepresented_span_ids":[],
            "unowned_anchor_ids":[x["anchor_id"] for x in anchors],
            "coverage_status":"UNKNOWN",
            "notes":"Gate A1 deterministic anchor/provenance inventory only; semantic claim coverage and ownership are intentionally not assessed.",
        },
    }

def load_cases(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--cases",type=Path,required=True)
    ap.add_argument("--case-id",action="append")
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    wanted=set(args.case_id or [])
    rows=[]
    for case in load_cases(args.cases):
        if wanted and case["case_id"] not in wanted:
            continue
        rows.append(build_anchor_graph(case))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rows),encoding="utf-8")
