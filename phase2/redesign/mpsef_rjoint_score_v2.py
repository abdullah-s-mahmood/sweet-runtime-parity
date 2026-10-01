#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict

from mpsef_rjoint_core_v2 import (
    FAMILIES,
    FAMILY_MAP_VERSION,
    MATCHING_VERSION,
    build_targets,
    evaluate_action_against_gold,
    safe_div,
)

SCORER_VERSION = "MPSEF_RJOINT_SCORER_V2"
CLAIM_SCOPE = (
    "DEVELOPMENT_FEASIBILITY / ADAPTIVELY_CONSUMED QALB-2014 ORIGIN / "
    "NOT_INDEPENDENT_GENERALIZATION_EVIDENCE"
)

def nearest_rank(values, q):
    if not values:
        return None
    s=sorted(values)
    return s[max(0, min(len(s)-1, math.ceil(q*len(s))-1))]

def size_stats(values):
    if not values:
        return {"n":0,"mean":None,"median":None,"p95":None,"max":None}
    s=sorted(values)
    n=len(s)
    med=(s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2)
    return {
        "n":n,
        "mean":sum(s)/n,
        "median":med,
        "p95":nearest_rank(s,0.95),
        "max":max(s),
        "quantile_method":"NEAREST_RANK_CEIL_QN",
    }

def ratio_interval(lower_num, upper_num, den):
    if den==0:
        return {"lower":None,"upper":None,"exact":None,"denominator":0}
    lo=lower_num/den
    hi=upper_num/den
    return {
        "lower":lo,
        "upper":hi,
        "exact":lo if lower_num==upper_num else None,
        "denominator":den,
        "lower_numerator":lower_num,
        "upper_numerator":upper_num,
    }

def gate_from_interval(interval):
    if interval["denominator"]==0:
        return "INCONCLUSIVE_NO_TARGETS"
    lo,hi=interval["lower"],interval["upper"]
    if lo is not None and lo>=0.95:
        return "PASS_CANDIDATE_AVAILABILITY"
    if hi is not None and hi<0.95:
        return "FAIL_CANDIDATE_AVAILABILITY"
    return "INCONCLUSIVE_INTERVAL_CROSSES_GATE"

def word_spans(source):
    return [(m.start(),m.end(),m.group(0)) for m in re.finditer(r"\S+",source)]

def target_char_span(source, target):
    spans=word_spans(source)
    start,end=target["start"],target["end"]
    if start<0 or end<start or end>len(spans):
        raise RuntimeError(f'{target["target_id"]}: invalid target word offsets')
    if start==end:
        if not spans:
            pos=0
        elif start==len(spans):
            pos=len(source)
        else:
            pos=spans[start][0]
        if target["original"] not in {"",None}:
            raise RuntimeError(f'{target["target_id"]}: insertion target has non-empty original')
        return pos,pos
    cs,ce=spans[start][0],spans[end-1][1]
    observed=" ".join(source[cs:ce].split())
    expected=" ".join((target["original"] or "").split())
    if observed!=expected:
        raise RuntimeError(
            f'{target["target_id"]}: gold/source span mismatch: {observed!r}!={expected!r}'
        )
    return cs,ce

def apply_local_components(source, cs, ce, components):
    comps=sorted(components,key=lambda c:(c["source_start"],c["source_end"],c["output_start"],c["output_end"]))
    selected=[]
    unknown=False

    for c in comps:
        ss,se=c["source_start"],c["source_end"]
        insertion=(ss==se)

        if insertion:
            if ss==cs or ss==ce:
                # Attribution of an insertion exactly on a non-insertion target
                # boundary is diagnostic-ambiguous.
                if cs!=ce:
                    unknown=True
            if cs<ss<ce or (cs==ce and ss==cs):
                selected.append(c)
            continue

        if ss<cs<se or ss<ce<se:
            unknown=True
        if ss>=cs and se<=ce:
            selected.append(c)

    if unknown:
        return {"status":"UNKNOWN","local_output":None}

    if cs==ce:
        inserts=[c for c in selected if c["source_start"]==c["source_end"]==cs]
        if not inserts:
            return {"status":"FALSE","local_output":""}
        text="".join(c["output_text"] for c in sorted(inserts,key=lambda x:(x["output_start"],x["output_end"])))
        return {"status":"VALUE","local_output":text}

    cursor=cs
    chunks=[]
    for c in selected:
        ss,se=c["source_start"],c["source_end"]
        if ss==se:
            if ss<cursor:
                return {"status":"UNKNOWN","local_output":None}
            chunks.append(source[cursor:ss])
            chunks.append(c["output_text"])
            cursor=ss
        else:
            if ss<cursor:
                return {"status":"UNKNOWN","local_output":None}
            chunks.append(source[cursor:ss])
            chunks.append(c["output_text"])
            cursor=se
    chunks.append(source[cursor:ce])
    return {"status":"VALUE","local_output":"".join(chunks)}

def diagnostic_target_status(source, target, diagnostic_record):
    if diagnostic_record["source"]!=source:
        raise RuntimeError(f'{target["target_id"]}: diagnostic source mismatch')
    cs,ce=target_char_span(source,target)
    res=apply_local_components(source,cs,ce,diagnostic_record["components"])
    if res["status"]=="UNKNOWN":
        return "UNKNOWN"
    local=res["local_output"]
    expected=" ".join((target["correction"] or "").split())
    observed=" ".join((local or "").split())
    return "TRUE" if observed==expected else "FALSE"

def group_action_results(action_set, scored, proposer=None):
    eligible=[]
    for action in action_set["actions"]:
        if proposer is None:
            eligible.append(action)
        elif action["type"]=="KEEP" or proposer in action.get("provenance",[]):
            eligible.append(action)

    successful=[]
    failures=[]
    for a in eligible:
        r=scored[a["action_id"]]
        if "error" in r:
            failures.append(a)
        else:
            successful.append((a,r))

    target_count=max((r["gold"] for _,r in successful),default=0)
    lower=max((r["correct"] for _,r in successful),default=0)
    upper=target_count if failures else lower
    return {
        "lower":lower,
        "upper":upper,
        "successful":successful,
        "failures":failures,
        "exact":not failures or lower==upper,
    }

def evaluate_sentence(lev, source, primary_gold, action_set, evaluate_fn=None):
    if evaluate_fn is None:
        def evaluate_fn(output, src, gold):
            return evaluate_action_against_gold(lev,output,src,gold)

    scored={}
    for action in action_set["actions"]:
        try:
            scored[action["action_id"]]=evaluate_fn(action["output"],source,primary_gold)
        except Exception as e:
            scored[action["action_id"]]={"error":f"{type(e).__name__}: {str(e)[:300]}"}

    return {
        "scored":scored,
        "P1":group_action_results(action_set,scored,"P1"),
        "P2":group_action_results(action_set,scored,"P2"),
        "PAIR":group_action_results(action_set,scored,None),
    }

def best_clean_bounds(group, target_count):
    known=[r["correct"] for _,r in group["successful"] if r["extra"]==0]
    lower=max(known,default=0)
    upper=target_count if group["failures"] else lower
    return lower,upper

def best_family_bounds(group, family_indices):
    known=[]
    for _,r in group["successful"]:
        matched=set(r["matched_indices"])
        known.append(sum(i in matched for i in family_indices))
    lower=max(known,default=0)
    upper=len(family_indices) if group["failures"] else lower
    return lower,upper

def index_records(rows, key_fields):
    out={}
    for r in rows:
        key=tuple(r[k] for k in key_fields)
        if key in out:
            raise RuntimeError(f"duplicate record key {key}")
        out[key]=r
    return out

def score_population(
    lev,
    source_rows,
    action_sets,
    hypothesis_rows,
    diagnostic_rows,
    gold_by_uid,
    evaluate_fn=None,
):
    source=index_records(source_rows,["uid"])
    actions=index_records(action_sets,["uid"])
    hypotheses=index_records(hypothesis_rows,["uid","proposer"])
    diagnostic=index_records(diagnostic_rows,["uid","proposer"])

    uids=sorted(source)
    if set(uids)!=set(actions) or set(uids)!={k[0] for k in hypotheses} or set(uids)!={k[0] for k in diagnostic}:
        raise RuntimeError("population identity mismatch")
    if set(uids)!=set(gold_by_uid):
        raise RuntimeError("gold population identity mismatch")

    den=0
    nums={k:[0,0] for k in ("P1","P2","PAIR","CLEAN")}
    scope_counts=Counter()
    family_den=Counter()
    family_bounds={p:defaultdict(lambda:[0,0]) for p in ("P1","P2","PAIR")}
    raw_bounds=[0,0]
    raw_family=defaultdict(lambda:[0,0])
    four=Counter()
    scoring_failures=[]
    erroneous=complete_lo=complete_hi=clean_sentences=0
    clean_activity=Counter()
    protected_target_ids=set()
    protected_unreachable_ids=set()

    before_sizes=[]
    after_sizes=[]
    failure_states=Counter(r["final_state"] for r in hypothesis_rows)

    for uid in uids:
        src=source[uid]["source"]
        aset=actions[uid]
        if aset["source_sha256"]!=source[uid]["source_sha256"]:
            raise RuntimeError(f"{uid}: action/source hash mismatch")
        if not any(a["type"]=="KEEP" and a["output"]==src for a in aset["actions"]):
            raise RuntimeError(f"{uid}: KEEP missing")

        p1h=hypotheses[(uid,"P1")]
        p2h=hypotheses[(uid,"P2")]
        before_sizes.append(1+int(p1h["executable"])+int(p2h["executable"]))
        after_sizes.append(aset["unique_action_count"])

        all_gold=gold_by_uid[uid]
        all_targets=build_targets(uid,all_gold)
        for t in all_targets:
            scope_counts[t["scope"]]+=1

        keep_idx=[i for i,t in enumerate(all_targets) if t["scope"]!="PUNCTUATION_ONLY"]
        primary_gold=[all_gold[i] for i in keep_idx]
        targets=[all_targets[i] for i in keep_idx]

        den += len(targets)
        if targets:
            erroneous+=1
        else:
            clean_sentences+=1
            for p in ("P1","P2"):
                d=diagnostic[(uid,p)]
                clean_activity[p]+=int(d["output"]!=src)
            clean_activity["EITHER"]+=int(
                diagnostic[(uid,"P1")]["output"]!=src or diagnostic[(uid,"P2")]["output"]!=src
            )

        for t in targets:
            family_den[t["family"]]+=1

        ev=evaluate_sentence(lev,src,primary_gold,aset,evaluate_fn)
        for p in ("P1","P2","PAIR"):
            nums[p][0]+=ev[p]["lower"]
            nums[p][1]+=ev[p]["upper"]
            for a in ev[p]["failures"]:
                scoring_failures.append({"uid":uid,"group":p,"action_id":a["action_id"]})

        clo,chi=best_clean_bounds(ev["PAIR"],len(targets))
        nums["CLEAN"][0]+=clo
        nums["CLEAN"][1]+=chi

        repair_known=any(
            r["correct"]==len(targets) and r["extra"]==0
            for _,r in ev["PAIR"]["successful"]
        ) if targets else False
        complete_lo+=int(repair_known)
        complete_hi+=int(repair_known or (targets and bool(ev["PAIR"]["failures"])))

        fam_indices=defaultdict(list)
        for i,t in enumerate(targets):
            fam_indices[t["family"]].append(i)
        for fam,idxs in fam_indices.items():
            for p in ("P1","P2","PAIR"):
                lo,hi=best_family_bounds(ev[p],idxs)
                family_bounds[p][fam][0]+=lo
                family_bounds[p][fam][1]+=hi

        # Diagnostic-only R_raw. Unknown attribution becomes an interval.
        for i,t in enumerate(targets):
            s1=diagnostic_target_status(src,t,diagnostic[(uid,"P1")])
            s2=diagnostic_target_status(src,t,diagnostic[(uid,"P2")])
            definite=(s1=="TRUE" or s2=="TRUE")
            possible=definite or s1=="UNKNOWN" or s2=="UNKNOWN"
            raw_bounds[0]+=int(definite)
            raw_bounds[1]+=int(possible)
            raw_family[t["family"]][0]+=int(definite)
            raw_family[t["family"]][1]+=int(possible)

            if s1 in {"TRUE","FALSE"} and s2 in {"TRUE","FALSE"}:
                four[
                    "BOTH" if s1=="TRUE" and s2=="TRUE"
                    else "P1_ONLY" if s1=="TRUE"
                    else "P2_ONLY" if s2=="TRUE"
                    else "NEITHER"
                ]+=1
            else:
                four["UNKNOWN"]+=1

            tid=t["target_id"]
            if p1h["final_state"]=="PROTECTED_BLOCKED" and s1=="TRUE":
                protected_target_ids.add(tid)
            if p2h["final_state"]=="PROTECTED_BLOCKED" and s2=="TRUE":
                protected_target_ids.add(tid)

            # If diagnostic evidence reaches a target only through blocked actions
            # and no successful legal action achieved it, report it as potentially
            # protection-unreachable. Scoring failures leave this unknown.
            legal_known_reach=any(
                i in set(r["matched_indices"])
                for _,r in ev["PAIR"]["successful"]
            )
            if tid in protected_target_ids and not legal_known_reach and not ev["PAIR"]["failures"]:
                protected_unreachable_ids.add(tid)

    intervals={k:ratio_interval(v[0],v[1],den) for k,v in nums.items()}
    raw_interval=ratio_interval(raw_bounds[0],raw_bounds[1],den)

    pair=intervals["PAIR"]
    if raw_interval["upper"] is not None and pair["lower"] is not None and raw_interval["upper"]+1e-15 < pair["lower"]:
        raise RuntimeError("R_raw upper bound below R_joint lower bound")

    families={}
    for fam in FAMILIES:
        d=family_den[fam]
        if d==0:
            families[fam]={
                "targets":0,
                "P1":ratio_interval(0,0,0),
                "P2":ratio_interval(0,0,0),
                "PAIR":ratio_interval(0,0,0),
                "R_raw":ratio_interval(0,0,0),
            }
            continue
        families[fam]={
            "targets":d,
            "P1":ratio_interval(*family_bounds["P1"][fam],d),
            "P2":ratio_interval(*family_bounds["P2"][fam],d),
            "PAIR":ratio_interval(*family_bounds["PAIR"][fam],d),
            "R_raw":ratio_interval(*raw_family[fam],d),
        }

    exact_pair=pair["exact"]
    exact_raw=raw_interval["exact"]
    raw_gap=None if exact_pair is None or exact_raw is None else exact_raw-exact_pair

    result={
        "record_id":SCORER_VERSION,
        "claim_scope":CLAIM_SCOPE,
        "matching_version":MATCHING_VERSION,
        "family_map_version":FAMILY_MAP_VERSION,
        "primary_denominator_targets":den,
        "target_scope_counts":dict(scope_counts),
        "R_P1":intervals["P1"],
        "R_P2":intervals["P2"],
        "R_pair":pair,
        "R_joint":pair,
        "R_clean":intervals["CLEAN"],
        "R_raw":raw_interval,
        "R_raw_minus_R_joint_exact":raw_gap,
        "gate":gate_from_interval(pair),
        "complete_sentence_repair":{
            "erroneous_sentences":erroneous,
            "lower_count":complete_lo,
            "upper_count":complete_hi,
            "lower_rate":safe_div(complete_lo,erroneous),
            "upper_rate":safe_div(complete_hi,erroneous),
            "exact_rate":safe_div(complete_lo,erroneous) if complete_lo==complete_hi else None,
        },
        "clean_sentence_proposals":{
            "clean_sentences":clean_sentences,
            "P1_count":clean_activity["P1"],
            "P2_count":clean_activity["P2"],
            "either_count":clean_activity["EITHER"],
            "P1_rate":safe_div(clean_activity["P1"],clean_sentences),
            "P2_rate":safe_div(clean_activity["P2"],clean_sentences),
            "either_rate":safe_div(clean_activity["EITHER"],clean_sentences),
        },
        "four_way_reachability":dict(four),
        "families":families,
        "candidate_set_size":{
            "before_exact_text_dedup":size_stats(before_sizes),
            "after_exact_text_dedup":size_stats(after_sizes),
        },
        "failure_state_counts":dict(failure_states),
        "scoring_failures":scoring_failures,
        "protected_policy":{
            "blocked_hypotheses":failure_states["PROTECTED_BLOCKED"],
            "diagnostic_targets_reached_by_protected_blocked_hypothesis":len(protected_target_ids),
            "known_legally_unreachable_targets_due_to_protection":len(protected_unreachable_ids),
        },
        "exact_metric_available":pair["exact"] is not None,
    }
    return result

def self_test():
    # Diagnostic local-effect tests.
    src="ياولد هنا"
    target={
        "target_id":"T1","start":0,"end":1,
        "original":"ياولد","correction":"يا ولد",
        "scope":"LINGUISTIC","family":"SPLIT",
    }
    diag={
        "source":src,
        "components":[{
            "op":"INSERT","source_start":2,"source_end":2,
            "output_start":2,"output_end":3,
            "source_text":"","output_text":" ",
        }],
    }
    assert diagnostic_target_status(src,target,diag)=="TRUE"

    # Whole-action oracle must not union two proposals target-by-target.
    action_set={
        "actions":[
            {"action_id":"K","type":"KEEP","output":"SRC","provenance":["KEEP"]},
            {"action_id":"A","type":"P1_FINAL","output":"P1","provenance":["P1"]},
            {"action_id":"B","type":"P2_FINAL","output":"P2","provenance":["P2"]},
        ]
    }
    def fake(output,src,gold):
        m={"SRC":[],"P1":[0],"P2":[1]}[output]
        return {"matched_indices":m,"correct":len(m),"proposed":len(m),"gold":2,"extra":0}
    ev=evaluate_sentence(None,"SRC",[1,2],action_set,fake)
    assert ev["PAIR"]["lower"]==1 and ev["PAIR"]["upper"]==1

    # Scoring failure creates an interval; it does not become known zero.
    def flaky(output,src,gold):
        if output=="P2":
            raise RuntimeError("synthetic scorer failure")
        return fake(output,src,gold)
    ev2=evaluate_sentence(None,"SRC",[1,2],action_set,flaky)
    assert ev2["PAIR"]["lower"]==1 and ev2["PAIR"]["upper"]==2

    print(json.dumps({"self_test":"PASS","scorer_version":SCORER_VERSION},ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if not args.self_test:
        raise SystemExit(
            "PROJECT_MEASUREMENT_DISABLED_IN_SCORER_V2_LIBRARY; "
            "run --self-test only until a separately frozen measurement wrapper is authorized"
        )
    self_test()

if __name__=="__main__":
    main()
