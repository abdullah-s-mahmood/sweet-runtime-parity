from __future__ import annotations
import hashlib, json, re
from dataclasses import dataclass
from typing import Any

def sha256_text(s:str)->str: return hashlib.sha256(s.encode("utf-8")).hexdigest()
def canonical_json(obj:Any)->str: return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def transaction_id(payload:dict)->str: return sha256_text(canonical_json(payload))
def word_count_en(text:str)->int: return sum(1 for tok in text.split() if any(ch.isalpha() or ch.isdigit() for ch in tok))
def sentence_units(text:str): return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])",text.strip()) if s.strip()]
def utf8_byte_offset(text:str,cp_index:int)->int: return len(text[:cp_index].encode("utf-8"))
def utf16_units(text:str,cp_index:int)->int: return len(text[:cp_index].encode("utf-16-le"))//2

@dataclass
class Source:
    version:str
    text:str
    @property
    def hash(self): return sha256_text(self.text)

@dataclass
class Proposal:
    source_version:str
    source_hash:str
    proposed_text:str
    scope_id:str="paragraph:0"
    provenance:dict|None=None

def apply_proposal(source:Source,p:Proposal,expected_scope="paragraph:0"):
    if p.source_version!=source.version: return False,"STALE_VERSION",source
    if p.source_hash!=source.hash: return False,"HASH_MISMATCH",source
    if p.scope_id!=expected_scope: return False,"SCOPE_ESCAPE",source
    return True,"STAGED",Source(version=source.version+"+1",text=p.proposed_text)

def rollback(original:Source,staged:Source): return Source(version=original.version,text=original.text)
def replay(original:Source,p:Proposal): return apply_proposal(original,p)
def length_metrics(src:str,out:str):
    a,b=word_count_en(src),word_count_en(out); ratio=(b/a) if a else None
    return {"source_words":a,"output_words":b,"length_ratio":ratio,"within_10pct":ratio is not None and .9<=ratio<=1.1,"within_15pct":ratio is not None and .85<=ratio<=1.15,"sentence_count_delta":len(sentence_units(out))-len(sentence_units(src))}
def check_quantity_relations(expected,observed): return expected==observed
def check_citation_links(expected,observed): return expected==observed
def check_assertions(expected,observed): return expected==observed
