from __future__ import annotations

import itertools
import json
import re
from pathlib import Path
from typing import Iterable
from fractions import Fraction
from math import gcd

STOP={
    "the","a","an","and","or","of","to","in","on","for","with","as","at","by",
    "their","its","this","that","these","those","same","respective","quantity",
    "quantities","link","common","one"
}
SYN={
    "lowered":"reduce","lower":"reduce","reduced":"reduce","reduction":"reduce",
    "increased":"increase","greater":"increase","higher":"increase",
    "causes":"cause","causal":"cause","causality":"cause",
    "measured":"measure","measures":"measure",
    "defines":"define","defined":"define","denotes":"define",
    "required":"require","requires":"require",
    "uses":"use","using":"use",
    "runs":"run","running":"run",
    "stored":"store","stores":"store",
    "excluded":"exclude","excludes":"exclude",
    "evaluated":"evaluate","evaluation":"evaluate",
    "fixed":"fix","unchanged":"unchanged",
    "groups":"group","vehicles":"vehicle","findings":"finding",
}

def norm_token(t:str)->str:
    t=t.lower().strip("_-")
    return SYN.get(t,t)

def tokens(x)->set[str]:
    if x is None:
        return set()
    if isinstance(x,(int,float,bool)):
        return {str(x).lower()}
    if isinstance(x,dict):
        out=set()
        for k,v in x.items():
            if str(k).lower() not in {"value","unit"}:
                out |= tokens(str(k).replace("_"," "))
            out |= tokens(v)
        return out
    if isinstance(x,(list,tuple,set)):
        out=set()
        for v in x: out |= tokens(v)
        return out
    vals=re.findall(r"[A-Za-z]+(?:_[A-Za-z0-9]+)?|[-+]?\d+(?:\.\d+)?|%",str(x))
    return {norm_token(v) for v in vals if norm_token(v) not in STOP}

def jacc(a:set[str],b:set[str])->float:
    if not a and not b: return 1.0
    if not a or not b: return 0.0
    return len(a&b)/len(a|b)

def coverage(a:set[str],b:set[str])->float:
    if not a: return 1.0
    return len(a&b)/len(a)

def owner_tokens(x)->set[str]:
    raw=str(x or "")
    out=set(tokens(raw))
    for m in re.finditer(r"\bgroups?\s+([A-Za-z0-9]+)\s+and\s+([A-Za-z0-9]+)\b",raw,re.I):
        out.add("group:"+m.group(1).lower())
        out.add("group:"+m.group(2).lower())
    for m in re.finditer(r"\bgroup\s+([A-Za-z0-9]+)\b",raw,re.I):
        out.add("group:"+m.group(1).lower())
    for m in re.finditer(r"\b([A-Za-z]_[A-Za-z0-9]+)\b",raw):
        out.add("symbol:"+m.group(1).lower())
    return out

def owner_incompatible(s:dict,c:dict)->bool:
    so=owner_tokens(s.get("subject"))
    co=owner_tokens(c.get("subject"))
    sg={x for x in so if x.startswith("group:")}
    cg={x for x in co if x.startswith("group:")}
    if sg and cg and sg.isdisjoint(cg):
        return True
    ss={x for x in so if x.startswith("symbol:")}
    cs={x for x in co if x.startswith("symbol:")}
    if ss and cs and ss.isdisjoint(cs):
        return True
    return False

def assertion_similarity(s:dict,c:dict)->float:
    score=0.0
    if s["predicate"]==c["predicate"]: score+=4.0
    score+=3.0*jacc(owner_tokens(s["subject"]),owner_tokens(c["subject"]))
    score+=2.5*jacc(tokens(s.get("object")),tokens(c.get("object")))
    score+=2.0*jacc(tokens(s.get("bindings",{})),tokens(c.get("bindings",{})))
    for field in ["time","population","baseline","scope"]:
        score+=0.7*jacc(tokens(s.get(field,[])),tokens(c.get(field,[])))
    if s["polarity"]==c["polarity"]: score+=0.5
    if s["causality"]==c["causality"]: score+=0.5
    if s["modality"]==c["modality"]: score+=0.3
    return score

V2_6_MATCHER_NUMERIC_POLICY = "EXACT_RATIONAL_FORMULA_V1"
V2_6_MATCHER_ALGORITHM = "HUNGARIAN_EXACT_PARTIAL_WITH_DUMMIES_V1"

def exact_jacc(a:set[str],b:set[str])->Fraction:
    if not a and not b:
        return Fraction(1,1)
    if not a or not b:
        return Fraction(0,1)
    return Fraction(len(a & b),len(a | b))

def exact_assertion_similarity(s:dict,c:dict)->Fraction:
    score=Fraction(0,1)
    if s["predicate"]==c["predicate"]:
        score+=4
    score+=3*exact_jacc(owner_tokens(s["subject"]),owner_tokens(c["subject"]))
    score+=Fraction(5,2)*exact_jacc(tokens(s.get("object")),tokens(c.get("object")))
    score+=2*exact_jacc(tokens(s.get("bindings",{})),tokens(c.get("bindings",{})))
    for field in ["time","population","baseline","scope"]:
        score+=Fraction(7,10)*exact_jacc(tokens(s.get(field,[])),tokens(c.get(field,[])))
    if s["polarity"]==c["polarity"]:
        score+=Fraction(1,2)
    if s["causality"]==c["causality"]:
        score+=Fraction(1,2)
    if s["modality"]==c["modality"]:
        score+=Fraction(3,10)
    return score

def _lcm(a:int,b:int)->int:
    if a==0 or b==0:
        return 0
    return abs((a//gcd(a,b))*b)

def _lcm_many(values:Iterable[int])->int:
    out=1
    for value in values:
        out=_lcm(out,int(value))
    return out

def _hungarian_min(cost:list[list[int]])->list[int]:
    """Exact square Hungarian assignment over arbitrary-precision integer costs."""
    n=len(cost)
    if n==0:
        return []
    if any(len(row)!=n for row in cost):
        raise ValueError("V2.5 matcher requires a square cost matrix.")

    u=[0]*(n+1)
    v=[0]*(n+1)
    p=[0]*(n+1)
    way=[0]*(n+1)

    for i in range(1,n+1):
        p[0]=i
        j0=0
        minv=[None]*(n+1)
        used=[False]*(n+1)

        while True:
            used[j0]=True
            i0=p[j0]
            delta=None
            j1=0

            for j in range(1,n+1):
                if used[j]:
                    continue
                cur=cost[i0-1][j-1]-u[i0]-v[j]
                if minv[j] is None or cur<minv[j]:
                    minv[j]=cur
                    way[j]=j0
                if delta is None or minv[j]<delta:
                    delta=minv[j]
                    j1=j

            if delta is None:
                raise RuntimeError("Hungarian solver could not find an augmenting step.")

            for j in range(n+1):
                if used[j]:
                    u[p[j]]+=delta
                    v[j]-=delta
                elif j>0:
                    minv[j]-=delta

            j0=j1
            if p[j0]==0:
                break

        while True:
            j1=way[j0]
            p[j0]=p[j1]
            j0=j1
            if j0==0:
                break

    assignment=[-1]*n
    for j in range(1,n+1):
        if p[j]:
            assignment[p[j]-1]=j-1

    if any(j<0 for j in assignment):
        raise RuntimeError("Hungarian solver returned an incomplete assignment.")
    return assignment

def _exact_lexicographic_cost_matrix(source:list[dict],candidate:list[dict])->list[list[int]]:
    """
    Scalarize the declared V2.5 lexicographic objective exactly:
      1) minimize hard owner mismatches
      2) maximize owner similarity
      3) maximize semantic similarity
      4) choose lexicographically earliest candidate-index tuple
    """
    n=len(source)
    hard=[
        [int(owner_incompatible(source[i],candidate[j])) for j in range(n)]
        for i in range(n)
    ]
    owner=[
        [exact_jacc(owner_tokens(source[i]["subject"]),owner_tokens(candidate[j]["subject"])) for j in range(n)]
        for i in range(n)
    ]
    semantic=[
        [exact_assertion_similarity(source[i],candidate[j]) for j in range(n)]
        for i in range(n)
    ]

    owner_lcm=_lcm_many(x.denominator for row in owner for x in row)
    semantic_lcm=_lcm_many(x.denominator for row in semantic for x in row)

    owner_i=[[int(x*owner_lcm) for x in row] for row in owner]
    semantic_i=[[int(x*semantic_lcm) for x in row] for row in semantic]

    base=n+1
    tie_weight=[base**(n-1-i) for i in range(n)]
    max_tie=(n-1)*sum(tie_weight)

    owner_min=min(x for row in owner_i for x in row)
    owner_max=max(x for row in owner_i for x in row)
    semantic_min=min(x for row in semantic_i for x in row)
    semantic_max=max(x for row in semantic_i for x in row)

    owner_range=n*(owner_max-owner_min)
    semantic_range=n*(semantic_max-semantic_min)

    semantic_weight=max_tie+1
    owner_weight=semantic_range*semantic_weight+max_tie+1
    hard_weight=owner_range*owner_weight+semantic_range*semantic_weight+max_tie+1

    return [
        [
            hard[i][j]*hard_weight
            - owner_i[i][j]*owner_weight
            - semantic_i[i][j]*semantic_weight
            + j*tie_weight[i]
            for j in range(n)
        ]
        for i in range(n)
    ]

def best_one_to_one(source:list[dict],candidate:list[dict])->list[tuple[list[dict],list[dict]]]:
    """
    V2.5 exact scalable replacement for V2.4 factorial permutation enumeration.

    The pair formulas and priority order are unchanged mathematically.
    Numeric policy is explicitly versioned to exact rational formula evaluation.
    """
    if len(source)!=len(candidate):
        raise ValueError("best_one_to_one requires equal source/candidate counts.")
    if not source:
        return []

    assignment=_hungarian_min(_exact_lexicographic_cost_matrix(source,candidate))
    return [([source[i]],[candidate[j]]) for i,j in enumerate(assignment)]

def _exact_partial_cost_matrix(source:list[dict],candidate:list[dict])->list[list[int]]:
    """Square padded exact cost matrix. Dummy assignments make unmatched assertions explicit."""
    m=len(source); n=len(candidate); N=max(m,n)
    if N==0:
        return []
    if m and n:
        owner=[[exact_jacc(owner_tokens(source[i]["subject"]),owner_tokens(candidate[j]["subject"])) for j in range(n)] for i in range(m)]
        semantic=[[exact_assertion_similarity(source[i],candidate[j]) for j in range(n)] for i in range(m)]
        hard=[[int(owner_incompatible(source[i],candidate[j])) for j in range(n)] for i in range(m)]
        owner_lcm=_lcm_many(x.denominator for row in owner for x in row)
        semantic_lcm=_lcm_many(x.denominator for row in semantic for x in row)
        owner_i=[[int(x*owner_lcm) for x in row] for row in owner]
        semantic_i=[[int(x*semantic_lcm) for x in row] for row in semantic]
        owner_vals=[x for row in owner_i for x in row]
        semantic_vals=[x for row in semantic_i for x in row]
        match_count=min(m,n)
        owner_range=match_count*(max(owner_vals)-min(owner_vals))
        semantic_range=match_count*(max(semantic_vals)-min(semantic_vals))
    else:
        hard=[]; owner_i=[]; semantic_i=[]
        owner_range=0; semantic_range=0

    base=N+1
    tie_weight=[base**(N-1-i) for i in range(N)]
    max_tie=(N-1)*sum(tie_weight)
    semantic_weight=max_tie+1
    owner_weight=semantic_range*semantic_weight+max_tie+1
    hard_weight=owner_range*owner_weight+semantic_range*semantic_weight+max_tie+1

    cost=[]
    for i in range(N):
        row=[]
        for j in range(N):
            tie=j*tie_weight[i]
            if i<m and j<n:
                row.append(
                    hard[i][j]*hard_weight
                    - owner_i[i][j]*owner_weight
                    - semantic_i[i][j]*semantic_weight
                    + tie
                )
            else:
                row.append(tie)
        cost.append(row)
    return cost

def partial_one_to_one(source:list[dict],candidate:list[dict])->list[tuple[list[dict],list[dict]]]:
    """Exact deterministic rectangular assignment with explicit unmatched assertions."""
    if not source:
        return [([],[c]) for c in candidate]
    if not candidate:
        return [([s],[]) for s in source]
    N=max(len(source),len(candidate))
    assignment=_hungarian_min(_exact_partial_cost_matrix(source,candidate))
    matched_candidates=set()
    out=[]
    for i,s in enumerate(source):
        j=assignment[i]
        if j<len(candidate):
            matched_candidates.add(j)
            out.append(([s],[candidate[j]]))
        else:
            out.append(([s],[]))
    for j,c in enumerate(candidate):
        if j not in matched_candidates:
            out.append(([],[c]))
    return out

def assertion_groups(source:list[dict],candidate:list[dict]):
    if len(source)==len(candidate):
        return best_one_to_one(source,candidate)
    return partial_one_to_one(source,candidate)

def canonical_scalar(x)->str:
    if isinstance(x,float):
        return format(x,"g")
    return " ".join(sorted(tokens(x)))

def canonical_owner(x)->str:
    ot=owner_tokens(x)
    special=sorted(t for t in ot if t.startswith("group:") or t.startswith("symbol:"))
    if special:
        return "|".join(special)
    return " ".join(sorted(ot))

def canonical_binding_key(x)->str:
    raw=str(x)
    if re.fullmatch(r"[A-Za-z]_[A-Za-z0-9]+",raw):
        return raw.lower()
    gm=re.fullmatch(r"group[_\s]+([A-Za-z0-9]+)",raw,re.I)
    if gm:
        return "group:"+gm.group(1).lower()
    return canonical_scalar(raw.replace("_"," "))

def canonical_quantity(value,unit=None)->tuple[str,str]:
    if unit is not None:
        return canonical_scalar(value),canonical_scalar(unit)
    raw=str(value).strip()
    m=re.fullmatch(r"([-+]?\d+(?:\.\d+)?)\s*([A-Za-z%]+)",raw)
    if m:
        return canonical_scalar(m.group(1)),canonical_scalar(m.group(2))
    return canonical_scalar(value),""

def binding_facts(group:list[dict])->set[tuple]:
    facts=set()
    for a in group:
        b=a.get("bindings",{}) or {}
        owner=canonical_owner(a.get("subject"))

        if a.get("predicate")=="DEFINE":
            if "symbol" in b:
                facts.add(("DEFINE",canonical_scalar(b["symbol"]),canonical_scalar(a.get("object"))))
            for k,v in b.items():
                if k!="symbol":
                    facts.add(("DEFINE",canonical_binding_key(k),canonical_scalar(v)))
            if not b and a.get("object") is not None:
                facts.add(("DEFINE",owner,canonical_scalar(a.get("object"))))
            continue

        if "value" in b:
            value,unit=canonical_quantity(b["value"],b.get("unit") if "unit" in b else None)
            facts.add(("VALUE",owner,value,unit))

        for k,v in b.items():
            kl=str(k).lower()
            if kl in {"value","unit"}:
                continue
            km=re.fullmatch(r"group[_\s]+([a-z0-9]+)",kl)
            if km:
                value,unit=canonical_quantity(v)
                facts.add(("VALUE","group:"+km.group(1),value,unit))
            else:
                facts.add(("ATTR",owner,canonical_binding_key(k),canonical_scalar(v)))
    return facts

def group_semantics(group:list[dict])->dict:
    return {
        "predicates":{a["predicate"] for a in group},
        "subjects":set().union(*(owner_tokens(a["subject"]) for a in group)),
        "objects":set().union(*(tokens(a.get("object")) for a in group)),
        "bindings":set().union(*(tokens(a.get("bindings",{})) for a in group)),
        "binding_facts":binding_facts(group),
        "time":set().union(*(tokens(a.get("time",[])) for a in group)),
        "population":set().union(*(tokens(a.get("population",[])) for a in group)),
        "baseline":set().union(*(tokens(a.get("baseline",[])) for a in group)),
        "scope":set().union(*(tokens(a.get("scope",[])) for a in group)),
        "polarities":{a["polarity"] for a in group},
        "modalities":{a["modality"] for a in group},
        "causalities":{a["causality"] for a in group},
        "confidence":{a["confidence_status"] for a in group},
        "critical":any(a["criticality"]=="CRITICAL" for a in group),
    }

def incompatible_causality(s:set[str],c:set[str])->bool:
    if s==c: return False
    if "CAUSAL" in s and "EXPLICIT_NON_CAUSAL" in c: return True
    if "EXPLICIT_NON_CAUSAL" in s and "CAUSAL" in c: return True
    return False

def mapping_status(source:list[dict],candidate:list[dict])->tuple[str,str]:
    s=group_semantics(source); c=group_semantics(candidate)

    if (s["confidence"]-{"CERTAIN"}) or (c["confidence"]-{"CERTAIN"}):
        return "UNCERTAIN","Critical/source uncertainty is preserved rather than promoted by graph agreement."

    if s["polarities"]!=c["polarities"] or incompatible_causality(s["causalities"],c["causalities"]):
        return "CONTRADICTORY","Polarity or causality is contradicted."

    # Critical contextual/binding fields are exact semantic ownership constraints.
    for field,label in [("time","time"),("population","population"),("baseline","baseline"),("scope","scope")]:
        if s[field]!=c[field]:
            return "ALTERED",f"Material {label} binding differs."

    # Canonical ownership facts are the source of truth for explicit bindings.
    # This supports split/merge equivalence while still rejecting owner/value rebinding.
    if s["binding_facts"] or c["binding_facts"]:
        if s["binding_facts"]!=c["binding_facts"]:
            return "ALTERED","Canonical owner-to-value/meaning binding differs."

    # For split/merge, extra predicate detail is allowed if source predicates are retained.
    if not (s["predicates"] <= c["predicates"] or c["predicates"] <= s["predicates"]):
        return "ALTERED","Predicate relation changed."

    s_concepts=s["subjects"]|s["objects"]|s["bindings"]
    c_concepts=c["subjects"]|c["objects"]|c["bindings"]
    sc=coverage(s_concepts,c_concepts)
    cs=coverage(c_concepts,s_concepts)

    # Important source concepts must remain; candidate may add non-material packaging words.
    if sc<0.78 or cs<0.58:
        return "ALTERED",f"Scientific concept coverage differs (source->candidate={sc:.2f}, candidate->source={cs:.2f})."

    # Modality is material when it changes assertion strength.
    if s["modalities"]!=c["modalities"]:
        return "ALTERED","Modality/evidential commitment changed."

    return "PRESERVED","Assertion semantics and critical bindings are preserved."

def align_assertions(source:list[dict],candidate:list[dict])->list[dict]:
    out=[]
    for i,(sg,cg) in enumerate(assertion_groups(source,candidate),1):
        if len(sg)>1 or len(cg)>1:
            raise RuntimeError("V2.6 local-confidence invariant violated: alignment group is not atomic.")
        if not sg:
            status="NEW_INFORMATION"
            reason="Candidate assertion has no source counterpart under exact partial assignment."
        elif not cg:
            status="OMITTED"
            reason="Source assertion has no candidate counterpart under exact partial assignment."
        else:
            status,reason=mapping_status(sg,cg)
        present=sg+cg
        out.append({
            "alignment_id":f"A{i:03d}",
            "source_ids":[x["id"] for x in sg],
            "candidate_ids":[x["id"] for x in cg],
            "status":status,
            "criticality":"CRITICAL" if any(x["criticality"]=="CRITICAL" for x in present) else "MATERIAL",
            "reason":reason,
            "source_evidence":[x["evidence"] for x in sg],
            "candidate_evidence":[x["evidence"] for x in cg],
        })
    return out

def endpoint_matches(source_endpoint:str,candidate_endpoint:str,assertion_alignments:list[dict])->bool:
    # Literal endpoints (citations, external labels) must match exactly after normalization.
    source_ids={x for a in assertion_alignments for x in a["source_ids"]}
    candidate_ids={x for a in assertion_alignments for x in a["candidate_ids"]}
    if source_endpoint not in source_ids and candidate_endpoint not in candidate_ids:
        return tokens(source_endpoint)==tokens(candidate_endpoint)
    for a in assertion_alignments:
        if source_endpoint in a["source_ids"] and candidate_endpoint in a["candidate_ids"]:
            return True
    return False

def align_relations(source:list[dict],candidate:list[dict],assertion_alignments:list[dict])->list[dict]:
    out=[]
    used=set()
    for i,sr in enumerate(source,1):
        best=None
        for cr in candidate:
            if cr["id"] in used or cr["type"]!=sr["type"]:
                continue
            from_match=endpoint_matches(sr["from"],cr["from"],assertion_alignments)
            to_match=endpoint_matches(sr["to"],cr["to"],assertion_alignments)
            direct=from_match and to_match
            reverse=endpoint_matches(sr["from"],cr["to"],assertion_alignments) and endpoint_matches(sr["to"],cr["from"],assertion_alignments)
            partial=(from_match or to_match)
            rank=3 if direct else (2 if reverse else (1 if partial else 0))
            if best is None or rank>best[0]:
                best=(rank,cr,direct,reverse,partial)
        if best is None or best[0]==0:
            out.append({
                "alignment_id":f"R{i:03d}","source_relation_ids":[sr["id"]],"candidate_relation_ids":[],
                "status":"OMITTED","criticality":sr["criticality"],
                "reason":"No compatible candidate relation found.",
                "source_evidence":[sr["evidence"]],"candidate_evidence":[]
            })
            continue
        _,cr,direct,reverse,partial=best
        used.add(cr["id"])
        if sr["confidence_status"]!="CERTAIN" or cr["confidence_status"]!="CERTAIN":
            status="UNCERTAIN"; reason="Relation uncertainty is preserved."
        elif direct:
            status="PRESERVED"; reason="Relation type and endpoints are preserved."
        elif reverse and sr["type"] in {"PRECEDES"}:
            status="CONTRADICTORY"; reason="Directed relation is reversed."
        else:
            status="ALTERED"; reason="Relation endpoint ownership/binding differs."
        out.append({
            "alignment_id":f"R{i:03d}","source_relation_ids":[sr["id"]],"candidate_relation_ids":[cr["id"]],
            "status":status,"criticality":sr["criticality"],
            "reason":reason,"source_evidence":[sr["evidence"]],"candidate_evidence":[cr["evidence"]]
        })

    for cr in candidate:
        if cr["id"] not in used:
            out.append({
                "alignment_id":f"R{len(out)+1:03d}","source_relation_ids":[],"candidate_relation_ids":[cr["id"]],
                "status":"NEW_INFORMATION","criticality":cr["criticality"],
                "reason":"Candidate relation has no source counterpart.",
                "source_evidence":[],"candidate_evidence":[cr["evidence"]]
            })
    return out

def propagate_relation_failures(assertion_alignments:list[dict],relation_alignments:list[dict],source_relations:list[dict]):
    bad={"ALTERED","CONTRADICTORY","OMITTED","NEW_INFORMATION"}
    rel_by_id={r["id"]:r for r in source_relations}
    affected=set()
    for ra in relation_alignments:
        if ra["criticality"]=="CRITICAL" and ra["status"] in bad:
            for rid in ra["source_relation_ids"]:
                r=rel_by_id.get(rid)
                if r:
                    affected.add(r["from"]); affected.add(r["to"])
    for a in assertion_alignments:
        if a["status"]=="PRESERVED" and affected.intersection(a["source_ids"]):
            a["status"]="ALTERED"
            a["reason"]+=" Critical incident relation is not preserved."

def pair_outcome(assertion_alignments:list[dict],relation_alignments:list[dict])->str:
    reject={"ALTERED","CONTRADICTORY","OMITTED","NEW_INFORMATION"}
    if any(x["criticality"]=="CRITICAL" and x["status"] in reject for x in assertion_alignments+relation_alignments):
        return "REJECT"
    if any(x["status"]=="UNCERTAIN" for x in assertion_alignments+relation_alignments):
        return "REVIEW"
    return "PASS_CANDIDATE"

def align_pair(pair:dict)->dict:
    aa=align_assertions(pair["source_graph"]["assertions"],pair["candidate_graph"]["assertions"])
    ra=align_relations(pair["source_graph"]["relations"],pair["candidate_graph"]["relations"],aa)
    propagate_relation_failures(aa,ra,pair["source_graph"]["relations"])
    return {
        "pair_id":pair["pair_id"],
        "predicted_outcome":pair_outcome(aa,ra),
        "assertion_alignment":aa,
        "relation_alignment":ra,
        "model_inference":False,
    }

def load_pairs(path:Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--pairs",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    preds=[align_pair(p) for p in load_pairs(args.pairs)]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in preds),encoding="utf-8")
