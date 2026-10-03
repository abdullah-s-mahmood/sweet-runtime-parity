from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Decision = Literal["ENTAILS","CONTRADICTS","UNCERTAIN"]
Disposition = Literal["HARD_REJECT","SEMANTIC_REJECT","REVIEW","VERIFIED_FOR_REVIEW","KEEP"]

@dataclass(frozen=True)
class SemanticWitness:
    witness_id: str
    assertion_id: str
    direction: Literal["SOURCE_TO_CANDIDATE","CANDIDATE_TO_SOURCE"]
    decision: Decision
    calibrated: bool

@dataclass(frozen=True)
class HardFinding:
    code: str
    severity: Literal["HARD","NONE"]

def fuse(*, hard_findings:list[HardFinding], source_assertion_witnesses:list[SemanticWitness],
         candidate_claim_witnesses:list[SemanticWitness], exact_keep:bool=False) -> Disposition:
    if exact_keep:
        return "KEEP"
    if any(x.severity=="HARD" for x in hard_findings):
        return "HARD_REJECT"
    all_w = source_assertion_witnesses + candidate_claim_witnesses
    if not all_w or any(not x.calibrated for x in all_w):
        return "REVIEW"
    if any(x.decision=="UNCERTAIN" for x in all_w):
        return "REVIEW"
    by_key={}
    for w in all_w:
        by_key.setdefault((w.assertion_id,w.direction),set()).add(w.decision)
    if any(len(v)>1 for v in by_key.values()):
        return "REVIEW"
    # A contradiction in either direction is safety-significant only when no witness disagreement exists.
    if any(x.decision=="CONTRADICTS" for x in all_w):
        return "SEMANTIC_REJECT"
    # Every required source assertion and every extracted candidate claim must be positively supported.
    if all(x.decision=="ENTAILS" for x in all_w):
        return "VERIFIED_FOR_REVIEW"
    return "REVIEW"
