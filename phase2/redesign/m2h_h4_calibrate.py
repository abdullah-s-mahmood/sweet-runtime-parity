#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, unicodedata
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

SALT = "M2H-H4-GENERAL-NEGATIVE-V1-20260930-A"
ATTACH_PREFIX = {"و", "ف", "ب", "ك", "ل", "س"}
SEPARATE_PREFIX = {"يا", "ها"}
TOK_FIELDS = ("d3tok", "atbtok")

def compact(s):
    return "".join((s or "").split())

def pure_boundary(src, tgt):
    return bool(src) and bool(tgt) and compact(src) == compact(tgt)

def boundary_norm(s):
    out=[]
    trans={"إ":"ا","أ":"ا","آ":"ا","ٱ":"ا","ى":"ي","ة":"ه"}
    for ch in s or "":
        if ch=="ـ" or ch=="+":
            continue
        if unicodedata.category(ch) in {"Mn","Mc"} and "ARABIC" in unicodedata.name(ch,""):
            continue
        out.append(trans.get(ch,ch))
    return "".join(out)

def op_segments(op, src, tgt):
    if op=="SPLIT":
        return tgt.split(), compact(src)
    return src.split(), compact(tgt)

def structural_gate(op, src, tgt, invariant=True):
    if op not in {"SPLIT","MERGE"} or not src or not tgt:
        return False
    if not invariant or not pure_boundary(src,tgt):
        return False
    if op=="SPLIT":
        return len(src.split())==1 and len(tgt.split())>=2
    return len(src.split())>=2 and len(tgt.split())==1

def atom_for(op, src, tgt):
    segs = tgt.split() if op=="SPLIT" else src.split()
    return segs[0] if len(segs)==2 else None

def clitic_support(op, src, tgt):
    segs = tgt.split() if op=="SPLIT" else src.split()
    if len(segs)!=2:
        return False
    if op=="MERGE":
        return segs[0] in ATTACH_PREFIX and bool(segs[1])
    return segs[0] in SEPARATE_PREFIX and bool(segs[1])

def sha_rank(tag):
    return hashlib.sha256((SALT+"|"+tag).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--calibration",required=True)
    ap.add_argument("--h1-candidates",required=True)
    ap.add_argument("--out-prefix",default="M2H_H4_CALIBRATION_V1")
    args=ap.parse_args()

    from camel_tools.morphology.database import MorphologyDB
    from camel_tools.morphology.analyzer import Analyzer

    analyzer=Analyzer(MorphologyDB.builtin_db("calima-msa-r13"),backoff="NONE")

    rows=[json.loads(x) for x in Path(args.calibration).read_text(encoding="utf-8").splitlines() if x.strip()]
    h1=[json.loads(x) for x in Path(args.h1_candidates).read_text(encoding="utf-8").splitlines() if x.strip()]

    pure_cases=defaultdict(set)
    nonpure_cases=defaultdict(set)
    exact_merge_spans=set()
    exact_split_proposals=set()

    for r in rows:
        cid=r["case_id"]
        for e in r["gold_edits"]:
            mt=e["m2_type"]
            if mt not in {"Split","Merge"}: continue
            op=mt.upper()
            src=e["surface"]; tgt=e["replacement"]
            atom=atom_for(op,src,tgt)
            key=(op,atom)
            if pure_boundary(src,tgt):
                pure_cases[key].add(cid)
            else:
                nonpure_cases[key].add(cid)
            if op=="MERGE":
                exact_merge_spans.add((cid,tuple(e["source_span"])))
            else:
                exact_split_proposals.add((cid,tuple(e["source_span"]),tgt))

    @lru_cache(maxsize=50000)
    def morph_obs(joined):
        try:
            analyses=analyzer.analyze(joined)
        except Exception:
            return ("EXCEPTION",)
        obs=[]
        for a in analyses:
            if str(a.get("source",""))!="lex": continue
            for field in TOK_FIELDS:
                v=str(a.get(field,"") or "")
                if not v: continue
                pieces=[boundary_norm(p) for p in v.split("_") if boundary_norm(p)]
                if pieces:
                    obs.append(tuple(pieces))
        return tuple(obs)

    def morph_support(op,src,tgt):
        segs,joined=op_segments(op,src,tgt)
        prop=tuple(boundary_norm(x) for x in segs)
        obs=morph_obs(joined)
        if obs==("EXCEPTION",):
            return False,{"analyzer_exception":True,"comparable":0,"support":0}
        comparable=[o for o in obs if "".join(o)=="".join(prop)]
        sup=sum(o==prop for o in comparable)
        ratio=(sup/len(comparable)) if comparable else 0.0
        return len(comparable)>=2 and ratio>=0.80,{
            "analyzer_exception":False,
            "comparable":len(comparable),"support":sup,"support_ratio":ratio
        }

    def pattern_support(op,src,tgt,case_id=None,loo=False):
        atom=atom_for(op,src,tgt)
        if atom is None: return False,{"atom":None,"pure_other_cases":0,"nonpure_other_cases":0}
        pos=set(pure_cases.get((op,atom),set()))
        neg=set(nonpure_cases.get((op,atom),set()))
        if loo and case_id:
            pos.discard(case_id); neg.discard(case_id)
        ok=len(pos)>=5 and len(neg)==0
        return ok,{"atom":atom,"pure_other_cases":len(pos),"nonpure_other_cases":len(neg)}

    def evaluate(op,src,tgt,case_id=None,invariant=True,loo=False):
        structural=structural_gate(op,src,tgt,invariant)
        if not structural:
            return {"structural_gate":False,"supports":[],"support_count":0,"accepted":False}
        ms,me=morph_support(op,src,tgt)
        cs=clitic_support(op,src,tgt)
        ps,pe=pattern_support(op,src,tgt,case_id,loo)
        supports=[]
        if ms: supports.append("MORPH_SEGMENTATION")
        if cs: supports.append("CLITIC_LEGALITY")
        if ps: supports.append("DEVELOPMENT_PATTERN_SUPPORT")
        return {
            "structural_gate":True,
            "supports":supports,
            "support_count":len(supports),
            "accepted":len(supports)>=2,
            "morph_segmentation":me,
            "clitic_legality":cs,
            "development_pattern":pe,
        }

    decisions=[]
    gold_stats={op:Counter() for op in ("SPLIT","MERGE")}
    nonpure_stats={op:Counter() for op in ("SPLIT","MERGE")}

    for r in rows:
        cid=r["case_id"]
        for e in r["gold_edits"]:
            if e["m2_type"] not in {"Split","Merge"}: continue
            op=e["m2_type"].upper(); src=e["surface"]; tgt=e["replacement"]
            pure=pure_boundary(src,tgt)
            ev=evaluate(op,src,tgt,cid,True,loo=True)
            kind="GOLD_PURE" if pure else "GOLD_NONPURE_ADVERSARIAL"
            decisions.append({"kind":kind,"case_id":cid,"op":op,"source_span":e["source_span"],"source":src,"replacement":tgt,"evaluation":ev})
            if pure:
                gold_stats[op]["total"]+=1
                gold_stats[op]["accepted"]+=int(ev["accepted"])
            else:
                nonpure_stats[op]["total"]+=1
                nonpure_stats[op]["accepted"]+=int(ev["accepted"])

    h1_stats={op:Counter() for op in ("SPLIT","MERGE")}
    op_map={"PURE_SPLIT":"SPLIT","PURE_MERGE":"MERGE"}
    for c in h1:
        if c.get("derived_operation") not in op_map: continue
        op=op_map[c["derived_operation"]]
        ev=evaluate(op,c["source_surface"],c["candidate_replacement"],c["case_id"],all((c.get("invariant") or {}).values()),loo=False)
        h1_stats[op]["total"]+=1
        if ev["accepted"]:
            h1_stats[op]["accepted"]+=1
            h1_stats[op]["accepted_exact"]+=int(c.get("gold_support")=="EXACT_GOLD_SUPPORTED")
            h1_stats[op]["accepted_unsupported"]+=int(c.get("gold_support")!="EXACT_GOLD_SUPPORTED")
        decisions.append({"kind":"H1_STREAM","candidate_id":c["candidate_id"],"case_id":c["case_id"],"op":op,"source_span":c["source_span"],"source":c["source_surface"],"replacement":c["candidate_replacement"],"gold_support":c["gold_support"],"evaluation":ev})

    # Deterministic general no-boundary diagnostic controls
    merge_pool=[]
    split_pool=[]
    for r in rows:
        cid=r["case_id"]; toks=r["source"].split()
        for i in range(len(toks)-1):
            span=(i,i+2)
            if (cid,span) in exact_merge_spans: continue
            src=toks[i]+" "+toks[i+1]; tgt=toks[i]+toks[i+1]
            merge_pool.append((sha_rank(f"MERGE|{cid}|{i}"),cid,[i,i+2],src,tgt))
        for i,tok in enumerate(toks):
            if not (4<=len(tok)<=12): continue
            h=int(sha_rank(f"SPLITPOS|{cid}|{i}"),16)
            pos=1+(h%(len(tok)-1))
            tgt=tok[:pos]+" "+tok[pos:]
            key=(cid,(i,i+1),tgt)
            if key in exact_split_proposals: continue
            split_pool.append((sha_rank(f"SPLIT|{cid}|{i}|{pos}"),cid,[i,i+1],tok,tgt))

    diagnostic={}
    for op,pool in (("MERGE",merge_pool),("SPLIT",split_pool)):
        selected=sorted(pool,key=lambda x:x[0])[:1000]
        acc=0
        for _,cid,span,src,tgt in selected:
            ev=evaluate(op,src,tgt,cid,True,loo=False)
            acc+=int(ev["accepted"])
            decisions.append({"kind":"GENERAL_NO_BOUNDARY_DIAGNOSTIC","case_id":cid,"op":op,"source_span":span,"source":src,"replacement":tgt,"evaluation":ev})
        diagnostic[op]={"sampled":len(selected),"accepted":acc,"acceptance_rate":acc/len(selected) if selected else None}

    operation_summary={}
    for op in ("SPLIT","MERGE"):
        g=gold_stats[op]; hs=h1_stats[op]; np=nonpure_stats[op]
        recall=g["accepted"]/g["total"] if g["total"] else None
        precision=hs["accepted_exact"]/hs["accepted"] if hs["accepted"] else None
        supported=bool(
            g["total"]>=20 and recall is not None and recall>=0.70
            and hs["accepted"]>=20 and precision is not None and precision>=0.90
            and np["accepted"]==0
        )
        hard_stop=bool(hs["accepted"]>=20 and precision is not None and precision<0.80)
        operation_summary[op]={
            "gold_pure_total":g["total"],"gold_pure_accepted":g["accepted"],"recall":recall,
            "h1_stream_total":hs["total"],"h1_accepted":hs["accepted"],
            "h1_accepted_exact":hs["accepted_exact"],"h1_accepted_reference_unsupported":hs["accepted_unsupported"],
            "strict_reference_precision_lower_bound":precision,
            "nonpure_adversarial_total":np["total"],"nonpure_adversarial_accepted":np["accepted"],
            "general_no_boundary_diagnostic":diagnostic[op],
            "development_supported":supported,"hard_stop_precision_below_80":hard_stop,
        }

    summary={
        "record_id":"M2H_H4_BOUNDARY_CALIBRATION_V1","status":"PASS","scope":"CALIBRATION_ONLY",
        "evidence_rule":"AT_LEAST_2_OF_3_NON_H1_FAMILIES",
        "operations":operation_summary,
        "frozen_targets":{"recall_min":0.70,"precision_min":0.90,"hard_stop_precision_below":0.80},
        "integrity":{"internal_evaluation_opened":False,"stress_diagnostic_opened":False,"confirmation_opened":False,"holdout_opened":False,"a7ta_reserved_opened":False,"reserved_nahw_opened":False,"qalb15_test_opened":False},
    }
    p=Path(args.out_prefix)
    Path(str(p)+"_DECISIONS.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in decisions)+"\n",encoding="utf-8")
    Path(str(p)+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
