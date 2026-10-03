from __future__ import annotations

import importlib.util
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
A1_PATH=HERE/"source_anchor_extractor.py"
spec=importlib.util.spec_from_file_location("a1",A1_PATH)
a1=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a1)

SENT_RE=re.compile(r"[^.!?]+(?:[.!?]|$)")
SYMBOL_DEF_RE=re.compile(r"\b([A-Za-z]_[A-Za-z0-9]+)\s+is\s+([^.;,]+?)\s+and\s+([A-Za-z]_[A-Za-z0-9]+)\s+is\s+([^.;,]+?)(?=[.;]|$)",re.I)
FULL_SUBJECT_RE=re.compile(r"^(?:the|a|an|this|that|these|those|it|they|we|[A-Z][A-Za-z0-9_-]*)\b")

PREDICATES=[
    (r"does not establish", "NOT_ESTABLISH"),
    (r"should not be treated as", "NOT_TREAT_AS"),
    (r"was not evaluated", "NOT_EVALUATE"),
    (r"is not changed", "NOT_CHANGE"),
    (r"was associated with", "ASSOCIATE_WITH"),
    (r"is associated with", "ASSOCIATE_WITH"),
    (r"is measured as", "MEASURE_AS"),
    (r"is also measured", "MEASURE"),
    (r"are fixed", "FIX"),
    (r"is fixed", "FIX"),
    (r"are excluded", "EXCLUDE"),
    (r"is excluded", "EXCLUDE"),
    (r"uses", "USE"),
    (r"includes", "INCLUDE"),
    (r"calculates", "CALCULATE"),
    (r"obtains", "OBTAIN"),
    (r"required", "REQUIRE"),
    (r"increased", "INCREASE"),
    (r"reduced", "REDUCE"),
    (r"found", "FIND"),
    (r"reflect", "REFLECT"),
    (r"causes", "CAUSE"),
    (r"runs", "RUN"),
    (r"is stored", "STORE"),
    (r"stored", "STORE"),
    (r"discards", "DISCARD"),
    (r"normalizes", "NORMALIZE"),
    (r"concern", "CONCERN"),
    (r"is", "BE"),
]
PRED_RE=[(re.compile(r"\b"+p+r"\b",re.I),n) for p,n in PREDICATES]

def sentence_spans(text:str):
    """Sentence splitter that never treats decimal points (e.g. 42.0) as sentence boundaries."""
    out=[]
    start=0
    i=0
    n=len(text)
    while i<n:
        ch=text[i]
        boundary=False
        if ch in "!?":
            boundary=True
        elif ch==".":
            is_decimal=(i>0 and i+1<n and text[i-1].isdigit() and text[i+1].isdigit())
            boundary=not is_decimal
        if boundary:
            raw=text[start:i+1]
            lead=len(raw)-len(raw.lstrip())
            quote=raw.strip()
            if quote:
                s=start+lead
                out.append((s,s+len(quote),quote))
            start=i+1
        i+=1
    if start<n:
        raw=text[start:]
        lead=len(raw)-len(raw.lstrip())
        quote=raw.strip()
        if quote:
            s=start+lead
            out.append((s,s+len(quote),quote))
    return out

def safe_clause_spans(text:str, start:int, end:int):
    quote=text[start:end]
    stripped=quote.rstrip(".!?")
    base_end=start+len(stripped)

    # Two explicit symbol definitions coordinated by "and".
    m=SYMBOL_DEF_RE.search(stripped)
    if m and m.start()==0:
        left=f"{m.group(1)} is {m.group(2).strip()}"
        right=f"{m.group(3)} is {m.group(4).strip()}"
        li=stripped.find(left)
        ri=stripped.find(right,li+len(left))
        return [(start+li,start+li+len(left),left,False),
                (start+ri,start+ri+len(right),right,False)]

    # Semicolon separates explicit propositions, but retain uncertainty if context is shared.
    if ";" in stripped:
        parts=[]
        pos=0
        for seg in stripped.split(";"):
            lead=len(seg)-len(seg.lstrip())
            body=seg.strip()
            if body:
                s=start+pos+lead
                parts.append((s,s+len(body),body,True))
            pos+=len(seg)+1
        if len(parts)>1:
            return parts

    # Split ", but " only when the right side begins with an explicit surface subject.
    marker=", but "
    k=stripped.lower().find(marker)
    if k>=0:
        left=stripped[:k].strip()
        right=stripped[k+len(marker):].strip()
        if left and right and FULL_SUBJECT_RE.match(right):
            ls=start+stripped.find(left)
            rs=start+k+len(marker)+(len(stripped[k+len(marker):])-len(stripped[k+len(marker):].lstrip()))
            return [(ls,ls+len(left),left,False),(rs,rs+len(right),right,False)]

    return [(start,base_end,stripped,False)]

def context_prefixes(clause:str):
    temporal=[]; population=[]; baseline=[]; working=clause.strip()

    m=re.match(r"At\s+((?:[01]\d|2[0-3]):[0-5]\d)\s*,\s*",working,re.I)
    if m:
        temporal=[m.group(1)]
        working=working[m.end():].lstrip()

    m=re.match(r"Among\s+(.+?),\s*",working,re.I)
    if m:
        population=[m.group(1).strip()]
        working=working[m.end():].lstrip()

    m=re.match(r"Relative to\s+(.+?),\s*",working,re.I)
    if m:
        baseline=[m.group(1).strip()]
        working=working[m.end():].lstrip()

    return working,temporal,population,baseline

def find_predicate(text:str):
    best=None
    for rgx,norm in PRED_RE:
        m=rgx.search(text)
        if m and (best is None or m.start()<best[0] or (m.start()==best[0] and len(m.group(0))>best[2])):
            best=(m.start(),m.end(),len(m.group(0)),m.group(0),norm)
    if best is None:
        return None
    return best[0],best[1],best[3],best[4]

def classify(clause:str, norm:str|None, anchor_types:set[str]):
    l=clause.lower()
    if "does not establish" in l and ("cause" in l or "causal" in l):
        return "NEGATION"
    if "not evaluated outside" in l:
        return "SCOPE"
    if "associated with" in l:
        return "ASSOCIATIONAL"
    if " = " in clause or "equation" in l:
        return "EQUATION"
    if norm in {"MEASURE_AS","BE"} and re.search(r"\b(?:is|denotes?|represents?)\b",l):
        return "DEFINITIONAL"
    if any(x in l for x in ["first "," then ","before evaluation","before the run","runs for ","stored without","excluded from","uses the same parameter","fixed before"]):
        return "PROCEDURAL"
    if any(x in l for x in ["relative to","compared with","larger priority","higher than","lower than"]):
        return "COMPARATIVE"
    if anchor_types & {"VALUE","UNIT","COUNT","SEED","TIME","GROUP"} and norm in {"REQUIRE","INCREASE","REDUCE","RUN","CALCULATE"}:
        return "QUANTITATIVE"
    return "RELATIONAL"

def discourse_role(assertion_type:str, clause:str):
    l=clause.lower()
    if assertion_type=="PROCEDURAL":
        return "PROCEDURE"
    if assertion_type in {"DEFINITIONAL","EQUATION"}:
        return "DEFINITION"
    if assertion_type in {"NEGATION","SCOPE"} or "should not" in l:
        return "LIMITATION"
    if assertion_type in {"QUANTITATIVE","COMPARATIVE","ASSOCIATIONAL"} or any(x in l for x in ["found","reduced","increased"]):
        return "RESULT"
    if "evaluation" in l or "controller" in l:
        return "METHOD"
    return "OTHER"

def modality(clause:str):
    l=clause.lower()
    for word,val in [(" may ","MAY"),(" can ","CAN"),(" could ","COULD"),(" likely ","LIKELY"),(" possible ","POSSIBLE")]:
        if word in f" {l} ":
            return val
    return "ASSERTED"

def scope_and_quantifiers(clause:str):
    l=f" {clause.lower()} "
    scopes=[]; quants=[]
    if " only " in l: scopes.append("ONLY"); quants.append("ONLY")
    if " every " in l or " all " in l: scopes.append("ALL"); quants.append("ALL")
    if " some " in l: scopes.append("SOME"); quants.append("SOME")
    if " none " in l: scopes.append("NONE"); quants.append("NONE")
    if " and " in l: scopes.append("AND")
    if " or " in l: scopes.append("OR")
    if "not evaluated outside" in l: scopes.append("OUTSIDE_NOT_EVALUATED")
    return sorted(set(scopes)),sorted(set(quants))

def assertion_from_clause(case_id:str,idx:int,clause:str,span_id:str,anchors:list[dict],shared_context:bool):
    working,temporal,population,baseline=context_prefixes(clause)
    pred=find_predicate(working)
    unresolved=[]

    if pred is None:
        subject=working.strip() or "UNRESOLVED"
        pred_raw="UNRESOLVED"
        pred_norm="UNRESOLVED"
        obj=None
        unresolved.extend(["predicate","object"])
    else:
        ps,pe,praw,pnorm=pred
        subject=working[:ps].strip(" ,")
        subject=re.sub(r"\b(may|can|could|likely|possibly)\s*$","",subject,flags=re.I).strip()
        obj=working[pe:].strip(" ,") or None
        pred_raw=praw
        pred_norm=pnorm
        if not subject:
            subject="UNRESOLVED"
            unresolved.append("subject")

    if re.match(r"^(it|the result|the finding|these findings|the equation(?: itself)?)\b",subject,re.I):
        unresolved.append("coreference_subject")

    l=clause.lower()
    if shared_context:
        unresolved.append("shared_context_after_clause_split")
    if any(x in l for x in [", while "," compared with "," after which "]):
        unresolved.append("multi_relation_atomicity")
    if re.search(r"\b(?:found|reported|observed|showed|shows|indicates?|demonstrates?)\s+that\b",l):
        unresolved.append("embedded_proposition")
    if " whether " in f" {l} " or " rather than " in f" {l} ":
        unresolved.append("embedded_scope")

    anchor_types={a["anchor_type"] for a in anchors}
    a_type=classify(clause,pred_norm if pred else None,anchor_types)

    polarity="NEGATIVE" if re.search(r"\b(?:does not|not evaluated|should not|without further|not changed)\b",l) else "POSITIVE"
    mod=modality(clause)
    if "associated with" in l:
        evid="ASSOCIATED"; caus="ASSOCIATION_ONLY"
    elif re.search(r"does not establish.+caus",l):
        evid="OTHER"; caus="EXPLICIT_NON_CAUSAL"
    elif a_type=="PROCEDURAL":
        evid="PROCEDURAL"; caus="NONE"
    elif a_type in {"DEFINITIONAL","EQUATION"}:
        evid="DEFINED"; caus="NONE"
    elif any(x in l for x in ["reported","found"]):
        evid="REPORTED"; caus="NONE"
    elif any(x in l for x in ["reduced","increased","required"]):
        evid="OBSERVED"; caus="NONE"
    elif re.search(r"\bcauses?\b",l):
        evid="OTHER"; caus="CAUSAL"
    else:
        evid="OTHER"; caus="NONE"

    role=discourse_role(a_type,clause)
    state="IMPLEMENTED" if a_type=="PROCEDURAL" else ("OBSERVED" if role=="RESULT" else ("DEFINED" if role=="DEFINITION" else "OTHER"))
    scopes,quants=scope_and_quantifiers(clause)

    if pred is None or "subject" in unresolved:
        status="AMBIGUOUS"
    elif unresolved:
        status="UNCERTAIN"
    else:
        status="CERTAIN"

    criticality="CRITICAL" if (a_type!="RELATIONAL" or anchors or polarity=="NEGATIVE") else "MATERIAL"
    exclusions=[]
    if "excluded" in l:
        exclusions.append(clause)
    if "without further tuning" in l:
        exclusions.append("further tuning")

    return {
        "assertion_id":f"{case_id}-AS-{idx:03d}",
        "discourse_role":role,
        "assertion_type":a_type,
        "subject":subject,
        "predicate_raw":pred_raw,
        "predicate_normalized":pred_norm,
        "object":obj,
        "comparator":None,
        "direction":"INCREASE" if pred_norm=="INCREASE" else ("DECREASE" if pred_norm=="REDUCE" else "NONE"),
        "conditions":[],
        "temporal_context":temporal,
        "population":population,
        "baseline":baseline,
        "scope_operators":scopes,
        "modality":mod,
        "evidential_strength":evid,
        "polarity":polarity,
        "causality":caus,
        "state":state,
        "criticality":criticality,
        "extraction_status":status,
        "unresolved_slots":sorted(set(unresolved)),
        "exclusions":exclusions,
        "citation_refs":[],
        "equation_refs":[],
        "symbol_bindings":[],
        "quantifiers":quants,
        "anchor_refs":[a["anchor_id"] for a in anchors],
        "evidence_span_ids":[span_id],
    }

def extract_source_assertions(case:dict):
    graph=a1.build_anchor_graph(case)
    text=case["source_text"]
    evidence=list(graph["evidence_spans"])
    anchors=graph["anchors"]
    anchor_spans={}
    span_by_id={e["span_id"]:e for e in evidence}
    for a in anchors:
        e=span_by_id[a["evidence_span_ids"][0]]
        anchor_spans[a["anchor_id"]]=(e["char_start"],e["char_end"])

    assertions=[]
    claim_sentence_ids=[]
    represented_sentence_ids=[]
    unrepresented_sentence_ids=[]
    aidx=0; sidx=0; cidx=0

    for sstart,send,squote in sentence_spans(text):
        sidx+=1
        sid=f"{case['case_id']}-SENT-{sidx:03d}"
        evidence.append({
            "span_id":sid,"container_type":"SENTENCE","container_id":f"{case['case_id']}:source",
            "char_start":sstart,"char_end":send,"quote":squote
        })
        claim_sentence_ids.append(sid)
        produced=0

        for cstart,cend,cquote,shared_context in safe_clause_spans(text,sstart,send):
            cidx+=1
            cid=f"{case['case_id']}-CLAUSE-{cidx:03d}"
            evidence.append({
                "span_id":cid,"container_type":"SENTENCE","container_id":sid,
                "char_start":cstart,"char_end":cend,"quote":cquote
            })
            overlapping=[]
            for a in anchors:
                x,y=anchor_spans[a["anchor_id"]]
                if cstart <= x and y <= cend:
                    overlapping.append(a)
            aidx+=1
            assertions.append(assertion_from_clause(case["case_id"],aidx,cquote,cid,overlapping,shared_context))
            produced+=1

        if produced:
            represented_sentence_ids.append(sid)
        else:
            unrepresented_sentence_ids.append(sid)

    graph["evidence_spans"]=evidence
    graph["assertions"]=assertions
    graph["relations"]=[]
    graph["coverage"]={
        "claim_bearing_span_ids":claim_sentence_ids,
        "represented_span_ids":represented_sentence_ids,
        "unrepresented_span_ids":unrepresented_sentence_ids,
        "unowned_anchor_ids":[a["anchor_id"] for a in anchors],
        "coverage_status":"UNKNOWN",
        "notes":"Gate A2 structural claim-span accounting only. Semantic completeness, atomicity correctness, and anchor ownership require Gate A3 validation."
    }
    return graph
