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

def validate_scoring_result(result, target_count):
    if not isinstance(result,dict):
        raise RuntimeError("scorer returned non-dict")
    required={"matched_indices","correct","proposed","gold","extra"}
    if not required.issubset(result):
        raise RuntimeError("scorer result missing required fields")
    matched=result["matched_indices"]
    if not isinstance(matched,list) or any(not isinstance(i,int) for i in matched):
        raise RuntimeError("matched_indices malformed")
    if len(set(matched))!=len(matched):
        raise RuntimeError("duplicate target credit")
    if any(i<0 or i>=target_count for i in matched):
        raise RuntimeError("matched target index out of range")
    if result["gold"]!=target_count:
        raise RuntimeError("scorer gold denominator mismatch")
    if result["correct"]!=len(matched):
        raise RuntimeError("scorer correct count mismatch")
    if result["proposed"]<result["correct"]:
        raise RuntimeError("proposed < correct")
    if result["extra"]!=result["proposed"]-result["correct"]:
        raise RuntimeError("extra count mismatch")
    return result

def evaluate_sentence(lev, source, primary_gold, action_set, evaluate_fn=None):
    if evaluate_fn is None:
        def evaluate_fn(output, src, gold):
            return evaluate_action_against_gold(lev,output,src,gold)

    scored={}
    for action in action_set["actions"]:
        try:
            raw=evaluate_fn(action["output"],source,primary_gold)
            scored[action["action_id"]]=validate_scoring_result(raw,len(primary_gold))
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

def difference_interval(a, b):
    if a["denominator"] != b["denominator"]:
        raise RuntimeError("interval denominator mismatch")
    if a["denominator"] == 0:
        return {"lower":None,"upper":None,"exact":None,"denominator":0}
    lo=max(0.0, a["lower"] - b["upper"])
    hi=max(0.0, a["upper"] - b["lower"])
    return {
        "lower":lo,
        "upper":hi,
        "exact":lo if abs(lo-hi)<1e-15 else None,
        "denominator":a["denominator"],
    }

def diagnostic_components_overlap(d1, d2):
    def spans(rec):
        out=[]
        for comp in rec["components"]:
            s,e=comp["source_start"],comp["source_end"]
            out.append((s,e))
        return out
    a,b=spans(d1),spans(d2)
    for s1,e1 in a:
        for s2,e2 in b:
            if s1==e1 and s2==e2 and s1==s2:
                return True
            if s1==e1 and s2<=s1<=e2:
                return True
            if s2==e2 and s1<=s2<=e1:
                return True
            if s1<e2 and e1>s2:
                return True
    return False

def route_status(gain_interval, add_lo, add_hi, clusters_lo, clusters_hi):
    if (
        gain_interval["lower"] is not None
        and gain_interval["lower"] >= 0.05
        and add_lo >= 10
        and clusters_lo >= 10
    ):
        return "PASS"
    if (
        gain_interval["upper"] is None
        or gain_interval["upper"] < 0.05
        or add_hi < 10
        or clusters_hi < 10
    ):
        return "FAIL"
    return "INCONCLUSIVE"

def score_population(
    lev,
    source_rows,
    action_sets,
    hypothesis_rows,
    diagnostic_rows,
    gold_by_uid,
    evaluate_fn=None,
    progress_callback=None,
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
    family_sent=defaultdict(set)
    family_cluster=defaultdict(set)
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
    sentence_records=[]

    full_output_difference=0
    diagnostic_overlap_count=0
    different_and_overlap=0
    different_without_overlap=0

    weak_names={"INSERT":{"INSERT"},"BOUNDARY":{"SPLIT","MERGE"}}
    weak_add_lower={p:{w:set() for w in weak_names} for p in ("P1","P2")}
    weak_add_upper={p:{w:set() for w in weak_names} for p in ("P1","P2")}
    weak_cluster_lower={p:{w:set() for w in weak_names} for p in ("P1","P2")}
    weak_cluster_upper={p:{w:set() for w in weak_names} for p in ("P1","P2")}

    for ordinal,uid in enumerate(uids,start=1):
        src=source[uid]["source"]
        aset=actions[uid]
        cluster_id=source[uid]["cluster_id"]
        if aset["source_sha256"]!=source[uid]["source_sha256"]:
            raise RuntimeError(f"{uid}: action/source hash mismatch")
        if not any(a["type"]=="KEEP" and a["output"]==src for a in aset["actions"]):
            raise RuntimeError(f"{uid}: KEEP missing")
        if aset.get("unique_action_count") != len(aset["actions"]):
            raise RuntimeError(f"{uid}: action count field mismatch")
        if len(aset["actions"])<1 or len(aset["actions"])>3:
            raise RuntimeError(f"{uid}: action-set size violation")

        p1h=hypotheses[(uid,"P1")]
        p2h=hypotheses[(uid,"P2")]
        before_sizes.append(1+int(p1h["executable"])+int(p2h["executable"]))
        after_sizes.append(aset["unique_action_count"])

        d1=diagnostic[(uid,"P1")]
        d2=diagnostic[(uid,"P2")]
        diff=(d1["output"]!=d2["output"])
        overlap=diagnostic_components_overlap(d1,d2)
        full_output_difference+=int(diff)
        diagnostic_overlap_count+=int(overlap)
        different_and_overlap+=int(diff and overlap)
        different_without_overlap+=int(diff and not overlap)

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
            clean_activity["P1"]+=int(d1["output"]!=src)
            clean_activity["P2"]+=int(d2["output"]!=src)
            clean_activity["EITHER"]+=int(d1["output"]!=src or d2["output"]!=src)

        for t in targets:
            family_den[t["family"]]+=1
            family_sent[t["family"]].add(uid)
            family_cluster[t["family"]].add(cluster_id)

        ev=evaluate_sentence(lev,src,primary_gold,aset,evaluate_fn)
        sentence_failure_ids=set()
        for p in ("P1","P2","PAIR"):
            nums[p][0]+=ev[p]["lower"]
            nums[p][1]+=ev[p]["upper"]
            for a in ev[p]["failures"]:
                scoring_failures.append({"uid":uid,"group":p,"action_id":a["action_id"]})
                sentence_failure_ids.add(a["action_id"])

        clo,chi=best_clean_bounds(ev["PAIR"],len(targets))
        nums["CLEAN"][0]+=clo
        nums["CLEAN"][1]+=chi

        repair_known=any(
            rr["correct"]==len(targets) and rr["extra"]==0
            for _,rr in ev["PAIR"]["successful"]
        ) if targets else False
        repair_possible=bool(repair_known or (targets and ev["PAIR"]["failures"]))
        complete_lo+=int(repair_known)
        complete_hi+=int(repair_possible)

        fam_indices=defaultdict(list)
        for i,t in enumerate(targets):
            fam_indices[t["family"]].append(i)
        for fam,idxs in fam_indices.items():
            for p in ("P1","P2","PAIR"):
                lo,hi=best_family_bounds(ev[p],idxs)
                family_bounds[p][fam][0]+=lo
                family_bounds[p][fam][1]+=hi

        raw_sent_lo=0
        raw_sent_hi=0
        for i,t in enumerate(targets):
            s1=diagnostic_target_status(src,t,d1)
            s2=diagnostic_target_status(src,t,d2)
            definite=(s1=="TRUE" or s2=="TRUE")
            possible=definite or s1=="UNKNOWN" or s2=="UNKNOWN"
            raw_bounds[0]+=int(definite)
            raw_bounds[1]+=int(possible)
            raw_sent_lo+=int(definite)
            raw_sent_hi+=int(possible)
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

            known={}
            possible_group={}
            for p in ("P1","P2"):
                known[p]=any(i in set(rr["matched_indices"]) for _,rr in ev[p]["successful"])
                possible_group[p]=known[p] or bool(ev[p]["failures"])

            for weak,members in weak_names.items():
                if t["family"] not in members:
                    continue
                for p,other in (("P1","P2"),("P2","P1")):
                    if known[p] and not known[other] and not ev[other]["failures"]:
                        weak_add_lower[p][weak].add(tid)
                        weak_cluster_lower[p][weak].add(cluster_id)
                    if possible_group[p] and not known[other]:
                        weak_add_upper[p][weak].add(tid)
                        weak_cluster_upper[p][weak].add(cluster_id)

            legal_known_reach=any(
                i in set(rr["matched_indices"])
                for _,rr in ev["PAIR"]["successful"]
            )
            if tid in protected_target_ids and not legal_known_reach and not ev["PAIR"]["failures"]:
                protected_unreachable_ids.add(tid)

        sentence_records.append({
            "uid":uid,
            "case_id":source[uid]["case_id"],
            "cluster_id":cluster_id,
            "target_count":len(targets),
            "punctuation_only_excluded":len(all_targets)-len(targets),
            "action_count":aset["unique_action_count"],
            "P1_final_state":p1h["final_state"],
            "P2_final_state":p2h["final_state"],
            "P1_bounds":{"lower":ev["P1"]["lower"],"upper":ev["P1"]["upper"]},
            "P2_bounds":{"lower":ev["P2"]["lower"],"upper":ev["P2"]["upper"]},
            "PAIR_bounds":{"lower":ev["PAIR"]["lower"],"upper":ev["PAIR"]["upper"]},
            "R_clean_bounds":{"lower":clo,"upper":chi},
            "R_raw_bounds":{"lower":raw_sent_lo,"upper":raw_sent_hi},
            "complete_repair_lower":bool(repair_known),
            "complete_repair_upper":bool(repair_possible),
            "scoring_failure_action_ids":sorted(sentence_failure_ids),
            "P1_P2_full_output_different":diff,
            "P1_P2_diagnostic_source_span_overlap":overlap,
        })

        if progress_callback is not None:
            progress_callback(ordinal,len(uids),uid)

    intervals={k:ratio_interval(v[0],v[1],den) for k,v in nums.items()}
    raw_interval=ratio_interval(raw_bounds[0],raw_bounds[1],den)

    pair=intervals["PAIR"]
    if raw_interval["upper"] is not None and pair["lower"] is not None and raw_interval["upper"]+1e-15 < pair["lower"]:
        raise RuntimeError("R_raw upper bound below R_joint lower bound")

    families={}
    macro_lo=[]
    macro_hi=[]
    for fam in FAMILIES:
        d=family_den[fam]
        if d==0:
            families[fam]={
                "targets":0,"sentences":0,"clusters":0,
                "P1":ratio_interval(0,0,0),
                "P2":ratio_interval(0,0,0),
                "PAIR":ratio_interval(0,0,0),
                "R_raw":ratio_interval(0,0,0),
            }
            continue
        fam_pair=ratio_interval(*family_bounds["PAIR"][fam],d)
        families[fam]={
            "targets":d,
            "sentences":len(family_sent[fam]),
            "clusters":len(family_cluster[fam]),
            "P1":ratio_interval(*family_bounds["P1"][fam],d),
            "P2":ratio_interval(*family_bounds["P2"][fam],d),
            "PAIR":fam_pair,
            "R_raw":ratio_interval(*raw_family[fam],d),
        }
        macro_lo.append(fam_pair["lower"])
        macro_hi.append(fam_pair["upper"])

    macro={
        "nonempty_families":len(macro_lo),
        "lower":None if not macro_lo else sum(macro_lo)/len(macro_lo),
        "upper":None if not macro_hi else sum(macro_hi)/len(macro_hi),
    }
    macro["exact"]=macro["lower"] if macro["lower"] is not None and abs(macro["lower"]-macro["upper"])<1e-15 else None

    delta_p1=difference_interval(pair,intervals["P2"])
    delta_p2=difference_interval(pair,intervals["P1"])

    weak_routes={}
    for weak,members in weak_names.items():
        d=sum(family_den[x] for x in members)
        if d==0:
            weak_routes[weak]={"targets":0,"P1":{"status":"N/A"},"P2":{"status":"N/A"}}
            continue
        p1_pair=ratio_interval(
            sum(family_bounds["PAIR"][x][0] for x in members),
            sum(family_bounds["PAIR"][x][1] for x in members),d)
        p2_only=ratio_interval(
            sum(family_bounds["P2"][x][0] for x in members),
            sum(family_bounds["P2"][x][1] for x in members),d)
        p1_only=ratio_interval(
            sum(family_bounds["P1"][x][0] for x in members),
            sum(family_bounds["P1"][x][1] for x in members),d)
        gain_p1=difference_interval(p1_pair,p2_only)
        gain_p2=difference_interval(p1_pair,p1_only)
        weak_routes[weak]={
            "targets":d,
            "P1":{
                "gain_vs_P2":gain_p1,
                "additional_targets_lower":len(weak_add_lower["P1"][weak]),
                "additional_targets_upper":len(weak_add_upper["P1"][weak]),
                "additional_clusters_lower":len(weak_cluster_lower["P1"][weak]),
                "additional_clusters_upper":len(weak_cluster_upper["P1"][weak]),
            },
            "P2":{
                "gain_vs_P1":gain_p2,
                "additional_targets_lower":len(weak_add_lower["P2"][weak]),
                "additional_targets_upper":len(weak_add_upper["P2"][weak]),
                "additional_clusters_lower":len(weak_cluster_lower["P2"][weak]),
                "additional_clusters_upper":len(weak_cluster_upper["P2"][weak]),
            },
        }
        weak_routes[weak]["P1"]["status"]=route_status(
            gain_p1,
            weak_routes[weak]["P1"]["additional_targets_lower"],
            weak_routes[weak]["P1"]["additional_targets_upper"],
            weak_routes[weak]["P1"]["additional_clusters_lower"],
            weak_routes[weak]["P1"]["additional_clusters_upper"],
        )
        weak_routes[weak]["P2"]["status"]=route_status(
            gain_p2,
            weak_routes[weak]["P2"]["additional_targets_lower"],
            weak_routes[weak]["P2"]["additional_targets_upper"],
            weak_routes[weak]["P2"]["additional_clusters_lower"],
            weak_routes[weak]["P2"]["additional_clusters_upper"],
        )

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
        "Delta_P1":delta_p1,
        "Delta_P2":delta_p2,
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
        "family_macro_R_pair":macro,
        "weak_family_retention":weak_routes,
        "candidate_set_size":{
            "before_exact_text_dedup":size_stats(before_sizes),
            "after_exact_text_dedup":size_stats(after_sizes),
        },
        "proposal_relationships":{
            "P1_P2_full_output_different_sentences":full_output_difference,
            "P1_P2_diagnostic_source_span_overlap_sentences":diagnostic_overlap_count,
            "different_outputs_with_diagnostic_overlap":different_and_overlap,
            "different_outputs_without_diagnostic_overlap":different_without_overlap,
        },
        "failure_state_counts":dict(failure_states),
        "scoring_failures":scoring_failures,
        "protected_policy":{
            "blocked_hypotheses":failure_states["PROTECTED_BLOCKED"],
            "diagnostic_targets_reached_by_protected_blocked_hypothesis":len(protected_target_ids),
            "known_legally_unreachable_targets_due_to_protection":len(protected_unreachable_ids),
        },
        "exact_metric_available":pair["exact"] is not None,
        "per_sentence":sentence_records,
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

    # Duplicate target credit must invalidate that action score.
    def duplicate_credit(output,src,gold):
        if output=="P1":
            return {"matched_indices":[0,0],"correct":2,"proposed":2,"gold":2,"extra":0}
        return fake(output,src,gold)
    ev_bad=evaluate_sentence(None,"SRC",[1,2],action_set,duplicate_credit)
    assert ev_bad["P1"]["failures"], ev_bad

    # Scoring failure creates an interval; it does not become known zero.
    def flaky(output,src,gold):
        if output=="P2":
            raise RuntimeError("synthetic scorer failure")
        return fake(output,src,gold)
    ev2=evaluate_sentence(None,"SRC",[1,2],action_set,flaky)
    assert ev2["PAIR"]["lower"]==1 and ev2["PAIR"]["upper"]==2

    # R_clean must exclude known extra edits.
    clean_group={
        "successful":[
            ({"action_id":"K"},{"correct":0,"extra":0}),
            ({"action_id":"A"},{"correct":2,"extra":1}),
            ({"action_id":"B"},{"correct":1,"extra":0}),
        ],
        "failures":[],
    }
    assert best_clean_bounds(clean_group,2)==(1,1)

    # Candidate-size statistics use the frozen nearest-rank definition.
    st=size_stats([1,1,2,2,3])
    assert st["mean"]==1.8 and st["median"]==2 and st["p95"]==3 and st["max"]==3

    # Weak-route status must require all three preregistered conditions.
    assert route_status(
        {"lower":0.05,"upper":0.06},10,10,10,10
    )=="PASS"
    assert route_status(
        {"lower":0.04,"upper":0.06},10,20,10,20
    )=="INCONCLUSIVE"
    assert route_status(
        {"lower":0.01,"upper":0.04},100,100,100,100
    )=="FAIL"

    # Frozen 95% interval gate semantics.
    assert gate_from_interval(ratio_interval(19,19,20))=="PASS_CANDIDATE_AVAILABILITY"
    assert gate_from_interval(ratio_interval(18,18,20))=="FAIL_CANDIDATE_AVAILABILITY"
    assert gate_from_interval(ratio_interval(18,19,20))=="INCONCLUSIVE_INTERVAL_CROSSES_GATE"

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
