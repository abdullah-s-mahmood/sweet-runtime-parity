from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
A2_PATH=HERE.parent/"gate_a"/"source_assertion_extractor.py"

spec=importlib.util.spec_from_file_location("a2",A2_PATH)
a2=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a2)

# Controlled lexical normalization only. These mappings preserve relation direction.
PRED_SYNONYMS={
    "lowered":"REDUCE",
    "reduced":"REDUCE",
    "decreased":"REDUCE",
    "increased":"INCREASE",
    "greater":"INCREASE",
    "higher":"INCREASE",
    "denotes":"DEFINE",
    "represents":"DEFINE",
}

TOKEN_SYNONYMS={
    "lowered":"reduce",
    "lower":"reduce",
    "reduced":"reduce",
    "decreased":"reduce",
    "greater":"increase",
    "higher":"increase",
    "increased":"increase",
    "denotes":"define",
    "represents":"define",
    "causal":"cause",
    "causes":"cause",
    "caused":"cause",
}

STOP={"the","a","an","this","that","these","those","same","separate","one","two","claim"}

SYMBOL=r"[A-Za-z]_[A-Za-z0-9]+"
CIT=r"CIT_[A-Za-z0-9_]+"

TAG_RE=re.compile(r"(?:&lt;|<)\\s*/?\\s*(?:s|sentence)\\s*(?:&gt;|>)",re.I)
ENTITY_REPLACEMENTS={
    "&amp;":"&",
    "&quot;":'"',
    "&#39;":"'",
    "&apos;":"'",
    "&lt;":"<",
    "&gt;":">",
}

def normalize_scientific_text(text:str):
    """Deterministic normalization with exact normalized-char -> original-index provenance."""
    out=[]
    mapping=[]
    events=[]
    i=0
    n=len(text)
    while i<n:
        tm=TAG_RE.match(text,i)
        if tm:
            events.append({"type":"REMOVED_SENTENCE_TAG","original_start":i,"original_end":tm.end(),"text":tm.group(0)})
            i=tm.end()
            continue
        matched=False
        for entity,repl in ENTITY_REPLACEMENTS.items():
            if text.startswith(entity,i):
                out.append(repl)
                mapping.append(i)
                events.append({"type":"HTML_ENTITY","original_start":i,"original_end":i+len(entity),"replacement":repl})
                i+=len(entity)
                matched=True
                break
        if matched:
            continue
        ch=text[i]
        if ch in " \\t\\r\\f\\v":
            if not out or out[-1] not in {" ","\\n"}:
                out.append(" "); mapping.append(i)
            i+=1
            continue
        if ch=="\\n":
            if out and out[-1]==" ":
                out.pop(); mapping.pop()
            if not out or out[-1]!="\\n":
                out.append("\\n"); mapping.append(i)
            i+=1
            continue
        out.append(ch); mapping.append(i); i+=1
    while out and out[0] in {" ","\\n"}:
        out.pop(0); mapping.pop(0)
    while out and out[-1] in {" ","\\n"}:
        out.pop(); mapping.pop()
    return "".join(out),mapping,events

def is_section_heading(sentence:str)->bool:
    s=sentence.strip()
    core=s.rstrip(":").strip()
    words=core.split()
    return bool(core) and (
        (s.endswith(":") and len(words)<=8)
        or (len(words)<=6 and any(ch.isalpha() for ch in core) and core.upper()==core)
    )

def sha_text(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def toks(text:str|None)->set[str]:
    if not text:
        return set()
    vals=re.findall(r"[A-Za-z]+(?:_[A-Za-z0-9]+)?|[-+]?\d+(?:\.\d+)?",text.lower())
    out=set()
    for v in vals:
        v=TOKEN_SYNONYMS.get(v,v)
        if v not in STOP:
            out.add(v)
    return out

def mk_assertion(idx:int, subject:str, predicate:str, obj:str|None, evidence:str, *,
                 criticality="CRITICAL", polarity="POSITIVE", modality="ASSERTED",
                 causality="NONE", scope=None, time=None, population=None, baseline=None,
                 bindings=None, confidence="CERTAIN"):
    return {
        "id":f"A{idx:03d}",
        "criticality":criticality,
        "subject":subject.strip(),
        "predicate":predicate,
        "object":obj.strip() if isinstance(obj,str) else obj,
        "polarity":polarity,
        "modality":modality,
        "causality":causality,
        "scope":list(scope or []),
        "time":list(time or []),
        "population":list(population or []),
        "baseline":list(baseline or []),
        "bindings":dict(bindings or {}),
        "confidence_status":confidence,
        "evidence":evidence.strip(),
    }

def mk_relation(idx:int, typ:str, from_id:str, to_id:str, evidence:str, *,
                criticality="CRITICAL", confidence="CERTAIN"):
    return {
        "id":f"R{idx:03d}",
        "type":typ,
        "from":from_id,
        "to":to_id,
        "criticality":criticality,
        "confidence_status":confidence,
        "evidence":evidence.strip(),
    }

def sentence_list(text:str)->list[str]:
    return [q for _,_,q in a2.sentence_spans(text)]

def strip_setting(sentence:str):
    s=sentence.strip()
    setting=None
    m=re.match(r"^In\s+the\s+([^,]+),\s*(.+)$",s,re.I)
    if m:
        setting=m.group(1).strip()
        s=m.group(2).strip()
    m2=re.search(r"\s+in\s+the\s+([^.;]+)$",s,re.I)
    if m2 and any(k in m2.group(1).lower() for k in ["corridor","simulation","dataset","cohort","window"]):
        setting=m2.group(1).strip()
        s=s[:m2.start()].strip()
    return s,setting

def parse_equation(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(rf"(?P<lhs>{SYMBOL})\s*=\s*(?P<rhs>.+)",s)
    if not m:
        return None
    lhs=m.group("lhs")
    rhs=m.group("rhs")
    bindings={}
    for term in re.split(r"\s*\+\s*",rhs):
        tm=re.fullmatch(rf"(?P<coef>{SYMBOL})\s*\*?\s*(?P<var>{SYMBOL})",term.strip())
        if tm:
            bindings[tm.group("coef")]=tm.group("var")
    # Supported equations require at least one explicit coefficient->variable binding.
    confidence="CERTAIN" if bindings else "UNCERTAIN"
    return [mk_assertion(idx,lhs,"DEFINE",rhs,sentence,bindings=bindings,confidence=confidence)]

def parse_symbol_definitions(sentence:str, start_idx:int):
    s=sentence.rstrip(".").strip()
    # Supports "X is Y", "X denotes Y", and coordinated "X denotes Y, while Z denotes W".
    parts=re.split(r"\s*,?\s+while\s+|\s*;\s*",s,flags=re.I)
    out=[]
    idx=start_idx
    for part in parts:
        m=re.fullmatch(rf"(?P<sym>{SYMBOL})\s+(?:is|denotes|represents)\s+(?P<obj>.+)",part.strip(),re.I)
        if not m:
            return None
        sym=m.group("sym")
        obj=m.group("obj").strip(" ,")
        out.append(mk_assertion(idx,sym,"DEFINE",obj,part,bindings={"symbol":sym}))
        idx+=1
    return out if out else None

def parse_quantitative_group_merge(sentence:str, start_idx:int):
    s=sentence.rstrip(".").strip()
    tm=re.match(r"^At\s+((?:[01]\d|2[0-3]):[0-5]\d),\s*(.+)$",s,re.I)
    time=[]
    body=s
    if tm:
        time=[tm.group(1)]
        body=tm.group(2).strip()

    # "... required 46.2 s for Group A and 49.8 s for Group B"
    m=re.fullmatch(
        r"(?P<object>.+?)\s+required\s+(?P<v1>[-+]?\d+(?:\.\d+)?)\s*(?P<u1>[A-Za-z%]+)\s+for\s+(?P<g1>Group\s+[A-Za-z0-9]+)\s+and\s+(?P<v2>[-+]?\d+(?:\.\d+)?)\s*(?P<u2>[A-Za-z%]+)\s+for\s+(?P<g2>Group\s+[A-Za-z0-9]+)",
        body,re.I)
    if m:
        obj=m.group("object").strip()
        return [
            mk_assertion(start_idx,m.group("g1"),"REQUIRE",obj,sentence,time=time,
                         bindings={"value":float(m.group("v1")),"unit":m.group("u1").lower()}),
            mk_assertion(start_idx+1,m.group("g2"),"REQUIRE",obj,sentence,time=time,
                         bindings={"value":float(m.group("v2")),"unit":m.group("u2").lower()}),
        ]

    # "Group A required 42.0 s"
    m=re.fullmatch(r"(?P<group>Group\s+[A-Za-z0-9]+)\s+required\s+(?P<value>[-+]?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-z%]+)",body,re.I)
    if m:
        value=float(m.group("value"))
        return [mk_assertion(start_idx,m.group("group"),"REQUIRE","completion",sentence,time=time,
                             bindings={"value":value,"unit":m.group("unit").lower()})]
    return None

def parse_run_seed(sentence:str, start_idx:int, previous_subject:str|None):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(r"(?P<subject>.+?)\s+runs?\s+for\s+(?P<n>\d+)\s+iterations?(?:\s+with\s+seed\s+(?P<seed>\d+))?",s,re.I)
    if m:
        b={"iterations":int(m.group("n"))}
        if m.group("seed") is not None:
            b["seed"]=int(m.group("seed"))
        return [mk_assertion(start_idx,m.group("subject"),"RUN","optimization",sentence,bindings=b)]
    m=re.fullmatch(r"(?:the\s+)?same\s+run\s+uses\s+seed\s+(?P<seed>\d+)",s,re.I)
    if m:
        subject=previous_subject or "UNRESOLVED_RUN_OWNER"
        conf="CERTAIN" if previous_subject else "UNCERTAIN"
        return [mk_assertion(start_idx,subject,"USE","seed",sentence,
                             bindings={"seed":int(m.group("seed"))},confidence=conf)]
    return None

def parse_scope_evaluation(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(r"(?P<subject>.+?)\s+was\s+not\s+evaluated\s+outside\s+(?P<obj>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"EVALUATE",m.group("obj"),sentence,
                             polarity="NEGATIVE",scope=["OUTSIDE"])]
    m=re.fullmatch(r"(?P<subject>.+?)\s+was\s+(?:also\s+)?evaluated\s+outside\s+(?P<obj>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"EVALUATE",m.group("obj"),sentence,
                             polarity="POSITIVE",scope=["OUTSIDE"])]
    return None

def parse_noncausal(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(r"(?P<subject>.+?)\s+does\s+not\s+establish\s+that\s+(?P<actor>.+?)\s+causes?\s+(?P<object>.+)",s,re.I)
    if m:
        obj=f"{m.group('actor').strip()} causes {m.group('object').strip()}"
        return [mk_assertion(idx,m.group("subject"),"NOT_ESTABLISH",obj,sentence,
                             polarity="NEGATIVE",causality="EXPLICIT_NON_CAUSAL")]
    m=re.fullmatch(r"(?P<subject>.+?)\s+does\s+not\s+establish\s+(?:a\s+)?causal\s+link",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"NOT_ESTABLISH","causal link",sentence,
                             polarity="NEGATIVE",causality="EXPLICIT_NON_CAUSAL")]
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:therefore\s+)?cannot\s+be\s+claimed\s+to\s+cause\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"NOT_CAUSE",m.group("object"),sentence,
                             polarity="NEGATIVE",causality="EXPLICIT_NON_CAUSAL")]
    return None

def parse_density_relation(sentence:str, idx:int):
    s,_=strip_setting(sentence.rstrip("."))
    # "Packet loss increased when roadside-unit density was reduced"
    m=re.fullmatch(r"(?P<object>.+?)\s+increased\s+when\s+(?P<subject>.+?)\s+was\s+reduced",s,re.I)
    if m:
        return [mk_assertion(idx,f"reduced {m.group('subject').strip()}","INCREASE",m.group("object"),sentence)]
    # "A separate experiment observed greater packet loss at lower roadside-unit density"
    m=re.fullmatch(r"(?:A|The)\s+.+?\s+(?:observed|found|reported)\s+(?:a\s+)?(?:greater|higher|increased)\s+(?P<object>.+?)\s+at\s+(?:lower|reduced)\s+(?P<subject>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,f"reduced {m.group('subject').strip()}","INCREASE",m.group("object"),sentence)]
    return None

def parse_reduce(sentence:str, idx:int):
    s,setting=strip_setting(sentence.rstrip("."))
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:reduced|lowered|decreased)\s+(?P<object>.+)",s,re.I)
    if not m:
        return None
    b={"setting":setting} if setting else {}
    return [mk_assertion(idx,m.group("subject"),"REDUCE",m.group("object"),sentence,bindings=b)]

def parse_distinct_mechanism(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()
    l=s.lower()
    if ("should not be treated as evidence" in l and "same mechanism" in l) or ("not evidence of one common mechanism" in l):
        return [mk_assertion(idx,"the two findings","DISTINCT_FROM","same mechanism",sentence,
                             polarity="NEGATIVE")]
    return None

def parse_measured_as(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(r"(?P<subject>.+?)\s+is\s+measured\s+as\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"MEASURE_AS",m.group("object"),sentence)]
    return None


def parse_explicit_scientific_predicate(sentence:str, idx:int):
    s=sentence.rstrip(".").strip()

    # Explicit negated scientific predicates are represented as negation, never folded into the subject.
    m=re.fullmatch(r"We\s+do\s+not\s+define\s+(?P<subject>.+?)\s+as\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"DEFINE",m.group("object"),sentence,polarity="NEGATIVE")]
    m=re.fullmatch(r"(?P<subject>.+?)\s+does\s+not\s+treat\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"TREAT",m.group("object"),sentence,polarity="NEGATIVE")]
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:are|is)\s+not\s+used\s+for\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"USE_FOR",m.group("object"),sentence,polarity="NEGATIVE")]

    # Explicit scientific definitions: "We define X as Y" / "X is defined as Y".
    m=re.fullmatch(r"We\s+define\s+(?P<subject>.+?)\s+as\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"DEFINE",m.group("object"),sentence)]
    m=re.fullmatch(r"(?P<subject>.+?)\s+is\s+defined\s+as\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"DEFINE",m.group("object"),sentence)]

    # Explicit purpose relation: "X aims to ..." with explicit modal preserved.
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:(?P<modal>may|can|could)\s+)?aims?\s+to\s+(?P<object>.+)",s,re.I)
    if m:
        mod={"may":"MAY","can":"CAN","could":"COULD"}.get((m.group("modal") or "").lower(),"ASSERTED")
        return [mk_assertion(idx,m.group("subject"),"AIM_TO",m.group("object"),sentence,modality=mod)]

    # Explicit treatment relation.
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:typically\s+)?treats?\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"TREAT",m.group("object"),sentence)]

    # Explicit passive use relation.
    m=re.fullmatch(r"(?P<subject>.+?)\s+(?:are|is)\s+(?:widely\s+)?used\s+for\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"USE_FOR",m.group("object"),sentence)]

    # Explicit introduction relation. Preserve authorship as attribution in the subject.
    m=re.fullmatch(r"(?P<subject>We|The authors?)\s+introduce(?:s)?\s+(?P<object>.+)",s,re.I)
    if m:
        return [mk_assertion(idx,m.group("subject"),"INTRODUCE",m.group("object"),sentence)]

    return None

def is_citation_relation(sentence:str)->bool:
    s=sentence.rstrip(".").strip()
    return bool(re.fullmatch(rf".+?\s+(?:cites|->)\s*{CIT}",s,re.I))

def parse_citation_spec(sentence:str):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(rf"(?P<label>.+?)\s+cites\s+(?P<cit>{CIT})",s,re.I)
    if not m:
        m=re.fullmatch(rf"(?P<label>.+?)\s*->\s*(?P<cit>{CIT})",s,re.I)
    if not m:
        return None
    return m.group("label").strip(),m.group("cit")

def parse_precedes_spec(sentence:str):
    s=sentence.rstrip(".").strip()
    m=re.fullmatch(r"(?P<a>[A-Za-z-]+ing)\s+precedes\s+(?P<b>[A-Za-z-]+ing)",s,re.I)
    return (m.group("a"),m.group("b")) if m else None

def action_root(x:str)->str:
    l=x.lower()
    for suf in ["ing","ization","ation"]:
        if l.endswith(suf) and len(l)>len(suf)+2:
            l=l[:-len(suf)]
            break
    aliases={"discard":"DISCARD","normaliz":"NORMALIZE","normalize":"NORMALIZE"}
    return aliases.get(l,l.upper())

def fallback_from_a2(a:dict, evidence_by_id:dict, anchors_by_id:dict, idx:int):
    sid=a["evidence_span_ids"][0]
    ev=evidence_by_id[sid]["quote"]
    bindings={}
    counts=0; symbols=0; equations=0
    for aid in a.get("anchor_refs",[]):
        anc=anchors_by_id.get(aid)
        if not anc: continue
        typ=anc["anchor_type"]; val=anc["normalized"]
        if typ=="VALUE": bindings.setdefault("value",val)
        elif typ=="UNIT": bindings.setdefault("unit",val)
        elif typ=="SEED": bindings["seed"]=val
        elif typ=="COUNT":
            counts+=1; bindings[f"count_{counts}"]=val
        elif typ=="SYMBOL":
            symbols+=1; bindings[f"symbol_{symbols}"]=val
        elif typ=="EQUATION":
            equations+=1; bindings[f"equation_{equations}"]=val
    return mk_assertion(
        idx,a["subject"],a["predicate_normalized"],a.get("object"),ev,
        criticality=a["criticality"],polarity=a["polarity"],modality=a["modality"],
        causality=a["causality"],scope=a["scope_operators"],time=a["temporal_context"],
        population=a["population"],baseline=a["baseline"],bindings=bindings,
        confidence=a["extraction_status"])

def resolve_label_assertion(label:str, assertions:list[dict]):
    lt=toks(label.replace("-"," "))
    scored=[]
    for a in assertions:
        hay=toks(a["subject"])|toks(a.get("object"))|toks(a["evidence"])
        overlap=len(lt & hay)
        scored.append((overlap,a["id"]))
    scored.sort(reverse=True)
    if not scored or scored[0][0]==0:
        return None
    if len(scored)>1 and scored[1][0]==scored[0][0]:
        return None
    return scored[0][1]

def relation_aware_extract(text:str, case_id:str)->dict:
    original_text=text
    text,normalized_to_original,normalization_events=normalize_scientific_text(text)
    raw_case={"case_id":case_id,"source_text":text,"source_sha256":sha_text(text)}
    base=a2.extract_source_assertions(raw_case)
    ev_by_id={e["span_id"]:e for e in base["evidence_spans"]}
    anchors_by_id={a["anchor_id"]:a for a in base["anchors"]}

    # Map A2 assertions to their exact evidence quote for fallback by sentence.
    base_by_quote={}
    for a in base["assertions"]:
        q=ev_by_id[a["evidence_span_ids"][0]]["quote"].strip()
        base_by_quote.setdefault(q,[]).append(a)

    assertions=[]
    pending_citations=[]
    pending_precedes=[]
    idx=1
    previous_subject=None
    section_headings=[]

    for sentence in sentence_list(text):
        if is_section_heading(sentence):
            section_headings.append(sentence)
            continue
        if is_citation_relation(sentence):
            pending_citations.append((sentence,parse_citation_spec(sentence)))
            continue
        ps=parse_precedes_spec(sentence)
        if ps:
            pending_precedes.append((sentence,ps))
            continue

        parsed=None
        for parser in [
            lambda s,i: parse_equation(s,i),
            lambda s,i: parse_symbol_definitions(s,i),
            lambda s,i: parse_quantitative_group_merge(s,i),
            lambda s,i: parse_run_seed(s,i,previous_subject),
            lambda s,i: parse_scope_evaluation(s,i),
            lambda s,i: parse_noncausal(s,i),
            lambda s,i: parse_density_relation(s,i),
            lambda s,i: parse_reduce(s,i),
            lambda s,i: parse_distinct_mechanism(s,i),
            lambda s,i: parse_measured_as(s,i),
            lambda s,i: parse_explicit_scientific_predicate(s,i),
        ]:
            parsed=parser(sentence,idx)
            if parsed:
                break

        if parsed:
            assertions.extend(parsed)
            idx+=len(parsed)
            # Local explicit continuation support only.
            previous_subject=parsed[-1]["subject"] if parsed[-1]["predicate"]=="RUN" else previous_subject
            continue

        # Fallback to frozen A2 clauses wholly contained in this sentence.
        matches=[]
        for q,alist in base_by_quote.items():
            if q and q in sentence:
                matches.extend(alist)
        if not matches:
            # Preserve text as unresolved rather than inventing semantics.
            assertions.append(mk_assertion(idx,sentence,"UNRESOLVED",None,sentence,
                                           criticality="MATERIAL",confidence="AMBIGUOUS"))
            idx+=1
            continue
        # Deduplicate by original assertion id.
        seen=set()
        for a in matches:
            if a["assertion_id"] in seen: continue
            seen.add(a["assertion_id"])
            assertions.append(fallback_from_a2(a,ev_by_id,anchors_by_id,idx))
            idx+=1

    relations=[]
    ridx=1

    # Explicit citation ownership.
    for evidence,spec in pending_citations:
        if not spec: continue
        label,cit=spec
        target=resolve_label_assertion(label,assertions)
        if target:
            relations.append(mk_relation(ridx,"CITES",target,cit,evidence))
            ridx+=1

    # Explicit procedure order only; no generic procedure parser.
    for evidence,(a,b) in pending_precedes:
        pa=action_root(a); pb=action_root(b)
        a_ids=[x["id"] for x in assertions if x["predicate"]==pa]
        b_ids=[x["id"] for x in assertions if x["predicate"]==pb]
        if len(a_ids)==1 and len(b_ids)==1:
            relations.append(mk_relation(ridx,"PRECEDES",a_ids[0],b_ids[0],evidence))
            ridx+=1

    # Explicit finding distinction relation if the text states it and the first two
    # substantive claims are uniquely identifiable.
    if any("different subsystems" in s.lower() for s in sentence_list(text)):
        substantive=[a for a in assertions if a["predicate"] not in {"DISTINCT_FROM","UNRESOLVED"}]
        if len(substantive)>=2:
            relations.append(mk_relation(ridx,"DISTINCT_FROM",substantive[0]["id"],substantive[1]["id"],
                                         "The findings concern different subsystems."))
            ridx+=1

    return {
        "graph_id":f"{case_id}-RELATION-AWARE",
        "assertions":assertions,
        "relations":relations,
        "audit":{
            "a2_assertion_count":len(base["assertions"]),
            "relation_aware_assertion_count":len(assertions),
            "relation_count":len(relations),
            "a2_anchor_count":len(base["anchors"]),
            "a2_source_sha256":base["source_identity"]["source_sha256"],
            "original_source_sha256":sha_text(original_text),
            "normalized_source_sha256":sha_text(text),
            "normalization_events":normalization_events,
            "normalized_to_original_index":normalized_to_original,
            "section_headings":section_headings,
        },
        "a2_graph":base,
    }
