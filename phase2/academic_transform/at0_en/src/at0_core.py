from __future__ import annotations
import hashlib, json, re
from dataclasses import dataclass, asdict
from typing import Any

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def transaction_identity(payload: dict) -> str:
    excluded={"transaction_id","audit_events"}
    stable={k:v for k,v in payload.items() if k not in excluded}
    return sha256_text(canonical_json(stable))

def cp_to_utf8_byte(text: str, cp_index: int) -> int:
    if cp_index < 0 or cp_index > len(text): raise ValueError("cp range")
    return len(text[:cp_index].encode("utf-8"))

def cp_to_utf16_units(text: str, cp_index: int) -> int:
    if cp_index < 0 or cp_index > len(text): raise ValueError("cp range")
    return len(text[:cp_index].encode("utf-16-le"))//2

def english_word_count(text: str) -> int:
    return sum(1 for x in re.findall(r"\S+", text) if re.search(r"[^\W_]", x, re.UNICODE) or re.search(r"\d", x))

def sentence_units(text: str) -> list[str]:
    # Operational segmenter only; abbreviations/decimals are deliberately surfaced by diagnostics.
    parts=re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())
    return [p for p in parts if p]

def length_metrics(src: str, out: str) -> dict:
    sw,ow=english_word_count(src),english_word_count(out)
    ratio=(ow/sw) if sw else None
    ss,os=sentence_units(src),sentence_units(out)
    return {"source_words":sw,"output_words":ow,"length_ratio":ratio,
            "within_10pct": bool(ratio is not None and .9<=ratio<=1.1),
            "within_15pct": bool(ratio is not None and .85<=ratio<=1.15),
            "source_sentence_units":len(ss),"output_sentence_units":len(os),"sentence_count_delta":len(os)-len(ss)}

@dataclass
class Transaction:
    source_version: str
    source_text: str
    proposed_text: str
    scope_start_cp: int
    scope_end_cp: int
    language: str="en"
    operation: str="REWRITE_PARAGRAPH"
    provenance: list|None=None
    audit_events: list|None=None
    def payload(self):
        d=asdict(self); d['source_hash']=sha256_text(self.source_text); d['output_hash']=sha256_text(self.proposed_text)
        return d
    def identity(self): return transaction_identity(self.payload())

def validate_scope(document: str, tx: Transaction, expected_source_hash: str|None=None, expected_version: str|None=None, authorized_scope: tuple[int,int]|None=None) -> tuple[bool,str]:
    if tx.scope_start_cp < 0 or tx.scope_end_cp < tx.scope_start_cp or tx.scope_end_cp > len(document): return False,"INVALID_SCOPE"
    if authorized_scope is not None and (tx.scope_start_cp, tx.scope_end_cp) != authorized_scope: return False,"SCOPE_ESCAPE"
    scoped=document[tx.scope_start_cp:tx.scope_end_cp]
    if scoped != tx.source_text: return False,"SOURCE_TEXT_MISMATCH"
    if expected_source_hash is not None and sha256_text(tx.source_text)!=expected_source_hash: return False,"SOURCE_HASH_MISMATCH"
    if expected_version is not None and tx.source_version!=expected_version: return False,"STALE_VERSION"
    return True,"PASS"

def apply_transaction(document: str, tx: Transaction, expected_source_hash: str|None=None, expected_version: str|None=None, authorized_scope: tuple[int,int]|None=None) -> str:
    ok,reason=validate_scope(document,tx,expected_source_hash,expected_version,authorized_scope)
    if not ok: raise ValueError(reason)
    if tx.operation=="KEEP": return document
    if tx.operation!="REWRITE_PARAGRAPH": raise ValueError("UNSUPPORTED_OPERATION")
    return document[:tx.scope_start_cp]+tx.proposed_text+document[tx.scope_end_cp:]

def rollback(applied_document: str, tx: Transaction) -> str:
    out_start=tx.scope_start_cp; out_end=out_start+len(tx.proposed_text)
    if applied_document[out_start:out_end]!=tx.proposed_text: raise ValueError("OUTPUT_MISMATCH")
    return applied_document[:out_start]+tx.source_text+applied_document[out_end:]

def replay(document: str, tx: Transaction) -> str:
    return apply_transaction(document,tx,sha256_text(tx.source_text),tx.source_version)

def relation_findings(facts: dict, proposal: dict) -> list[dict]:
    findings=[]
    for key,expected in facts.items():
        got=proposal.get(key,"__MISSING__")
        if got!=expected: findings.append({"field":key,"expected":expected,"observed":got,"status":"VIOLATION"})
    return findings

class LanguageAdapter:
    language_code="unknown"
    def word_count(self,text:str): raise NotImplementedError
    def sentence_units(self,text:str): raise NotImplementedError
    def capability(self,name:str): return "NOT_IMPLEMENTED"

class EnglishAdapter(LanguageAdapter):
    language_code="en"
    def word_count(self,text): return english_word_count(text)
    def sentence_units(self,text): return sentence_units(text)
    def capability(self,name): return "SUPPORTED" if name in {"word_count","sentence_units","length_metrics"} else "NOT_IMPLEMENTED"

class StubAdapter(LanguageAdapter):
    language_code="stub"
    def word_count(self,text): return len(text)  # intentionally different semantics
    def sentence_units(self,text): return [text] if text else []