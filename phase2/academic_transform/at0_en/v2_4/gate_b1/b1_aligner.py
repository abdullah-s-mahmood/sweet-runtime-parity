from __future__ import annotations

import itertools
import json
import re
from pathlib import Path
from typing import Iterable

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

def assertion_similarity(s:dict,c:dict)->float:
    score=0.0
    if s["predicate"]==c["predicate"]: score+=4.0
    score+=2.5*jacc(tokens(s["subject"]),tokens(c["subject"]))
    score+=2.5*jacc(tokens(s.get("object")),tokens(c.get("object")))
    score+=2.0*jacc(tokens(s.get("bindings",{})),tokens(c.get("bindings",{})))
    for field in ["time","population","baseline","scope"]:
        score+=0.7*jacc(tokens(s.get(field,[])),tokens(c.get(field,[])))
    if s["polarity"]==c["polarity"]: score+=0.5
    if s["causality"]==c["causality"]: score+=0.5
    if s["modality"]==c["modality"]: score+=0.3
    return score

def best_one_to_one(source:list[dict],candidate:list[dict])->list[tuple[list[dict],list[dict]]]:
    best=None
    for perm in itertools.permutations(candidate,len(source)):
        score=sum(assertion_similarity(s,c) for s,c in zip(source,perm))
        if best is None or score>best[0]:
            best=(score,perm)
    return [([s],[c]) for s,c in zip(source,best[1])]

def assertion_groups(source:list[dict],candidate:list[dict]):
    if len(source)==len(candidate):
        return best_one_to_one(source,candidate)
    if len(source)==1:
        return [(source,candidate)]
    if len(candidate)==1:
        return [(source,candidate)]
    # Small B1 mechanics set fallback: align best one-to-one first and group leftovers.
    n=min(len(source),len(candidate))
    base=best_one_to_one(source[:n],candidate[:n])
    if len(source)>n:
        base[-1][0].extend(source[n:])
    if len(candidate)>n:
        base[-1][1].extend(candidate[n:])
    return base

def group_semantics(group:list[dict])->dict:
    return {
        "predicates":{a["predicate"] for a in group},
        "subjects":set().union(*(tokens(a["subject"]) for a in group)),
        "objects":set().union(*(tokens(a.get("object")) for a in group)),
        "bindings":set().union(*(tokens(a.get("bindings",{})) for a in group)),
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

    # In 1:1 mappings, explicit binding dictionaries encode ownership and must not be
    # reduced to a bag of tokens (e.g., w_1->U_i vs w_1->D_i).
    if len(source)==1 and len(candidate)==1:
        sb=source[0].get("bindings",{})
        cb=candidate[0].get("bindings",{})
        if (sb or cb) and sb!=cb:
            return "ALTERED","Explicit key-to-value binding differs."

    # In split/merge mappings, binding atoms may be redistributed across nodes.
    if s["bindings"] or c["bindings"]:
        if s["bindings"]!=c["bindings"]:
            # Allow faithful split/merge if the source binding atoms are fully represented in
            # candidate subject/object/bindings and vice versa.
            s_all=s["subjects"]|s["objects"]|s["bindings"]
            c_all=c["subjects"]|c["objects"]|c["bindings"]
            if coverage(s["bindings"],c_all)<1.0 or coverage(c["bindings"],s_all)<0.75:
                return "ALTERED","Material value/symbol binding differs."

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
        status,reason=mapping_status(sg,cg)
        out.append({
            "alignment_id":f"A{i:03d}",
            "source_ids":[x["id"] for x in sg],
            "candidate_ids":[x["id"] for x in cg],
            "status":status,
            "criticality":"CRITICAL" if any(x["criticality"]=="CRITICAL" for x in sg+cg) else "MATERIAL",
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
