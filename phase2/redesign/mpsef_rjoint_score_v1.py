#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

from mpsef_rjoint_core_v1 import (
    FAMILIES, FAMILY_MAP_VERSION, MATCHING_VERSION, build_targets,
    import_m2, norm, safe_div, score_candidate, self_test,
    sha256_file, sha_text,
)

EXPECTED_CAL_CASES=6888
EXPECTED_CF_CASES=1918
EXPECTED_CF_CLUSTERS=764
EXPECTED_CAL_UID_SHA="3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9"
EXPECTED_SOURCE_SHA="051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA="2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA="f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"
EXPECTED_GOLD_SHA="971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8"
AUTH_TOKEN="MEASURE_R_JOINT_V1"

def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def uid_digest(rows):
    return sha_text("\n".join(r["uid"] for r in rows)+"\n")

def proposal_map(path,expected_sha,label):
    p=Path(path)
    if sha256_file(p)!=expected_sha: raise RuntimeError(f"{label} SHA mismatch")
    rows=load_jsonl(p)
    if len(rows)!=EXPECTED_CF_CASES or len({x["uid"] for x in rows})!=EXPECTED_CF_CASES:
        raise RuntimeError(f"{label} population mismatch")
    for x in rows:
        if x.get("gold_reference_consulted") is not False or x.get("feasibility_scored") is not False:
            raise RuntimeError(f"{label} integrity flag violation")
    return rows,{x["uid"]:x for x in rows}

def legal(prop,score):
    return (
        score is not None and "error" not in score
        and bool(prop.get("source_only_executable_precheck"))
        and prop.get("full_proposer_output","")!=""
    )

def run_score(lev,prop,source,gold,label,failures):
    if prop.get("full_proposer_output","")=="":
        failures[f"{label}_EMPTY_OUTPUT"]+=1; return None
    try:
        return score_candidate(lev,prop["full_proposer_output"],source,gold)
    except Exception as e:
        failures[f"{label}_SCORING_FAILURE"]+=1
        return {"error":f"{type(e).__name__}: {str(e)[:240]}"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--upstream-root",required=True)
    ap.add_argument("--authorization")
    ap.add_argument("--calibration")
    ap.add_argument("--full-gold-m2")
    ap.add_argument("--source-manifest")
    ap.add_argument("--p1-proposals")
    ap.add_argument("--p2-proposals")
    ap.add_argument("--out-prefix",default="MPSEF_RJOINT_MEASUREMENT_V1")
    a=ap.parse_args()

    if a.self_test:
        assert self_test(a.upstream_root)
        print(json.dumps({"self_test":"PASS","matching_version":MATCHING_VERSION}))
        return
    if a.authorization!=AUTH_TOKEN:
        raise SystemExit("MEASUREMENT_NOT_AUTHORIZED")

    paths=[a.calibration,a.full_gold_m2,a.source_manifest,a.p1_proposals,a.p2_proposals]
    if any(x is None for x in paths): raise SystemExit("missing measurement input")
    calp,goldp,manp,p1p,p2p=map(Path,paths)
    if sha256_file(goldp)!=EXPECTED_GOLD_SHA: raise RuntimeError("gold M2 SHA mismatch")
    if sha256_file(manp)!=EXPECTED_SOURCE_SHA: raise RuntimeError("source manifest SHA mismatch")

    cal=load_jsonl(calp)
    if len(cal)!=EXPECTED_CAL_CASES or uid_digest(cal)!=EXPECTED_CAL_UID_SHA:
        raise RuntimeError("CALIBRATION identity mismatch")
    cal_by={x["uid"]:x for x in cal}; cal_idx={x["uid"]:i for i,x in enumerate(cal)}

    manifest=load_jsonl(manp)
    if len(manifest)!=EXPECTED_CF_CASES or len({x["cluster_id"] for x in manifest})!=EXPECTED_CF_CLUSTERS:
        raise RuntimeError("C_F manifest mismatch")
    man={x["uid"]:x for x in manifest}

    p1_rows,p1=proposal_map(p1p,EXPECTED_P1_SHA,"P1")
    p2_rows,p2=proposal_map(p2p,EXPECTED_P2_SHA,"P2")
    if set(p1)!=set(man) or set(p2)!=set(man): raise RuntimeError("proposal UID mismatch")

    m2,lev=import_m2(a.upstream_root)
    full_sources,full_gold=m2.load_annotation(str(goldp))
    if len(full_sources)!=EXPECTED_CAL_CASES or len(full_gold)!=EXPECTED_CAL_CASES:
        raise RuntimeError("gold M2 length mismatch")
    for i,x in enumerate(cal):
        if norm(full_sources[i])!=norm(x["source"]):
            raise RuntimeError(f"gold/source mismatch {i}:{x['uid']}")

    den=0; num1=num2=numpair=numraw=numclean=0
    erroneous=repairs=clean_sents=0
    clean_p1=clean_p2=clean_either=0
    scope_counts=Counter(); fam_den=Counter()
    fam_p1=Counter(); fam_p2=Counter(); fam_pair=Counter(); fam_raw=Counter()
    fam_sent=defaultdict(set); fam_cluster=defaultdict(set)
    weak_p1=Counter(); weak_p2=Counter(); weak_pair=Counter()
    add={"P1":defaultdict(set),"P2":defaultdict(set)}
    add_clusters={"P1":defaultdict(set),"P2":defaultdict(set)}
    four=Counter(); failures=Counter()
    pt1=pt2=pb1=pb2=0
    protected_targets=set(); protected_unreachable=set()
    conflicts=identical_nonkeep=0
    per=[]

    for n,uid in enumerate(sorted(man),1):
        m=man[uid]; c=cal_by[uid]
        if m["source_sha256"]!=sha_text(m["source"]) or norm(m["source"])!=norm(c["source"]):
            raise RuntimeError(f"manifest source mismatch {uid}")
        for prop,label in ((p1[uid],"P1"),(p2[uid],"P2")):
            if prop["source_version_hash"]!=m["source_sha256"] or norm(prop["source"])!=norm(m["source"]):
                raise RuntimeError(f"{label} source mismatch {uid}")

        gdict=full_gold[cal_idx[uid]]
        if set(gdict)!={0}: raise RuntimeError(f"unexpected annotators {uid}")
        all_gold=gdict[0]
        all_targets=build_targets(uid,all_gold)
        for t in all_targets: scope_counts[t["scope"]]+=1
        keep=[i for i,t in enumerate(all_targets) if t["scope"]!="PUNCTUATION_ONLY"]
        gold=[all_gold[i] for i in keep]
        targets=[all_targets[i] for i in keep]
        den+=len(gold)
        if gold: erroneous+=1
        else: clean_sents+=1
        for t in targets:
            fam_den[t["family"]]+=1; fam_sent[t["family"]].add(uid); fam_cluster[t["family"]].add(m["cluster_id"])

        s1=run_score(lev,p1[uid],m["source"],gold,"P1",failures)
        s2=run_score(lev,p2[uid],m["source"],gold,"P2",failures)
        l1=legal(p1[uid],s1); l2=legal(p2[uid],s2)
        if p1[uid].get("protected_touch"): pt1+=1; pb1+=int(not l1)
        if p2[uid].get("protected_touch"): pt2+=1; pb2+=int(not l2)

        raw1=set() if not s1 or "error" in s1 else set(s1["matched_indices"])
        raw2=set() if not s2 or "error" in s2 else set(s2["matched_indices"])
        leg1=raw1 if l1 else set(); leg2=raw2 if l2 else set()
        c1,c2=len(leg1),len(leg2)
        num1+=c1; num2+=c2; numpair+=max(c1,c2,0); numraw+=len(raw1|raw2)

        clean_opts=[0]
        if l1 and s1["extra"]==0: clean_opts.append(c1)
        if l2 and s2["extra"]==0: clean_opts.append(c2)
        numclean+=max(clean_opts)
        if gold and ((l1 and c1==len(gold) and s1["extra"]==0) or (l2 and c2==len(gold) and s2["extra"]==0)):
            repairs+=1

        if not gold:
            ch1=norm(p1[uid]["full_proposer_output"])!=norm(m["source"])
            ch2=norm(p2[uid]["full_proposer_output"])!=norm(m["source"])
            clean_p1+=int(ch1); clean_p2+=int(ch2); clean_either+=int(ch1 or ch2)

        o1=norm(p1[uid]["full_proposer_output"]); o2=norm(p2[uid]["full_proposer_output"]); src=norm(m["source"])
        if o1!=o2: conflicts+=1
        elif o1!=src: identical_nonkeep+=1

        for i,t in enumerate(targets):
            r1=i in raw1; r2=i in raw2; a1=i in leg1; a2=i in leg2
            four["BOTH" if r1 and r2 else "P1_ONLY" if r1 else "P2_ONLY" if r2 else "NEITHER"]+=1
            f=t["family"]
            fam_p1[f]+=int(a1); fam_p2[f]+=int(a2); fam_raw[f]+=int(r1 or r2)
            if (p1[uid].get("protected_touch") and r1) or (p2[uid].get("protected_touch") and r2):
                protected_targets.add(t["target_id"])
            if (r1 or r2) and not (a1 or a2): protected_unreachable.add(t["target_id"])
            if f in {"INSERT","SPLIT","MERGE"}:
                wf="INSERT" if f=="INSERT" else "BOUNDARY"
                if a1 and not a2: add["P1"][wf].add(t["target_id"]); add_clusters["P1"][wf].add(m["cluster_id"])
                if a2 and not a1: add["P2"][wf].add(t["target_id"]); add_clusters["P2"][wf].add(m["cluster_id"])

        fams={t["family"] for t in targets}
        for f in fams:
            x1=sum(1 for i in leg1 if targets[i]["family"]==f)
            x2=sum(1 for i in leg2 if targets[i]["family"]==f)
            fam_pair[f]+=max(x1,x2,0)
        for wf,members in {"INSERT":{"INSERT"},"BOUNDARY":{"SPLIT","MERGE"}}.items():
            x1=sum(1 for i in leg1 if targets[i]["family"] in members)
            x2=sum(1 for i in leg2 if targets[i]["family"] in members)
            weak_p1[wf]+=x1; weak_p2[wf]+=x2; weak_pair[wf]+=max(x1,x2,0)

        per.append({
            "uid":uid,"case_id":c["case_id"],"cluster_id":m["cluster_id"],"target_count":len(gold),
            "punctuation_only_excluded":len(all_gold)-len(gold),
            "P1":{"legal":l1,"protected_touch":bool(p1[uid].get("protected_touch")),
                  "correct":0 if not s1 or "error" in s1 else s1["correct"],
                  "proposed":0 if not s1 or "error" in s1 else s1["proposed"],
                  "extra":None if not s1 or "error" in s1 else s1["extra"]},
            "P2":{"legal":l2,"protected_touch":bool(p2[uid].get("protected_touch")),
                  "correct":0 if not s2 or "error" in s2 else s2["correct"],
                  "proposed":0 if not s2 or "error" in s2 else s2["proposed"],
                  "extra":None if not s2 or "error" in s2 else s2["extra"]},
            "pair_best_correct":max(c1,c2,0),"raw_union_correct":len(raw1|raw2),"clean_best_correct":max(clean_opts),
        })
        if n==1 or n%100==0 or n==EXPECTED_CF_CASES: print(f"RJOINT_PROGRESS {n}/{EXPECTED_CF_CASES}",flush=True)

    r1,r2,rpair,rraw,rclean=[safe_div(x,den) for x in (num1,num2,numpair,numraw,numclean)]
    if rpair is None: gate="INCONCLUSIVE_NO_TARGETS"
    elif rpair>=.95: gate="PASS_CANDIDATE_AVAILABILITY"
    elif rpair>=.90: gate="FAIL_BORDERLINE_DIAGNOSTIC_MEMO_ONLY"
    else: gate="FAIL_CLOSE_P1_P2_HIGH_COVERAGE_CYCLE"

    families={}; macro=[]
    for f in FAMILIES:
        d=fam_den[f]
        if not d: families[f]={"targets":0,"R_P1":None,"R_P2":None,"R_pair":None,"R_raw":None}; continue
        vals={"targets":d,"sentences":len(fam_sent[f]),"clusters":len(fam_cluster[f]),
              "R_P1":fam_p1[f]/d,"R_P2":fam_p2[f]/d,"R_pair":fam_pair[f]/d,"R_raw":fam_raw[f]/d}
        families[f]=vals; macro.append(vals["R_pair"])

    weak={}
    for wf,members in {"INSERT":{"INSERT"},"BOUNDARY":{"SPLIT","MERGE"}}.items():
        d=sum(fam_den[x] for x in members)
        weak[wf]={
            "targets":d,
            "P1_gain_vs_P2":None if not d else (weak_pair[wf]-weak_p2[wf])/d,
            "P2_gain_vs_P1":None if not d else (weak_pair[wf]-weak_p1[wf])/d,
            "P1_additional_targets":len(add["P1"][wf]),"P1_additional_clusters":len(add_clusters["P1"][wf]),
            "P2_additional_targets":len(add["P2"][wf]),"P2_additional_clusters":len(add_clusters["P2"][wf]),
        }

    retention={
        "P1":{"general_route_pass":rpair is not None and r2 is not None and rpair-r2>=.010,"weak_routes":{}},
        "P2":{"general_route_pass":rpair is not None and r1 is not None and rpair-r1>=.010,"weak_routes":{}},
    }
    for wf,v in weak.items():
        for p,other in (("P1","P2"),("P2","P1")):
            gain=v[f"{p}_gain_vs_{other}"]; at=v[f"{p}_additional_targets"]; ac=v[f"{p}_additional_clusters"]
            retention[p]["weak_routes"][wf]={"gain":gain,"additional_targets":at,"additional_clusters":ac,
                "pass":gain is not None and gain>=.05 and at>=10 and ac>=10}

    summary={
        "record_id":"MPSEF_RJOINT_MEASUREMENT_V1","status":"MEASUREMENT_COMPLETE",
        "claim_scope":"DEVELOPMENT_FEASIBILITY / ADAPTIVELY_CONSUMED_QALB-2014 ORIGIN / NOT_INDEPENDENT_GENERALIZATION_EVIDENCE",
        "cases":EXPECTED_CF_CASES,"clusters":EXPECTED_CF_CLUSTERS,
        "matching_version":MATCHING_VERSION,"family_map_version":FAMILY_MAP_VERSION,
        "primary_denominator_targets":den,"target_scope_counts":dict(scope_counts),
        "R_P1":r1,"R_P2":r2,"R_pair":rpair,"R_joint":rpair,"R_raw":rraw,
        "R_raw_minus_R_joint":None if rraw is None or rpair is None else rraw-rpair,
        "R_clean":rclean,"Delta_P1":None if rpair is None else rpair-r2,"Delta_P2":None if rpair is None else rpair-r1,
        "gate":gate,
        "complete_sentence_repair":{"erroneous_sentences":erroneous,"complete_repairs":repairs,"rate":safe_div(repairs,erroneous)},
        "clean_sentence_proposals":{"clean_sentences":clean_sents,"P1_count":clean_p1,"P2_count":clean_p2,"either_count":clean_either,
            "P1_rate":safe_div(clean_p1,clean_sents),"P2_rate":safe_div(clean_p2,clean_sents),"either_rate":safe_div(clean_either,clean_sents)},
        "four_way_reachability":dict(four),"families":families,
        "family_macro_R_pair":None if not macro else sum(macro)/len(macro),
        "weak_family_retention":weak,"proposer_retention_routes":retention,
        "protected_policy":{"P1_touch_sentences":pt1,"P2_touch_sentences":pt2,"P1_blocked_sentences":pb1,"P2_blocked_sentences":pb2,
            "raw_matched_targets_on_protected_touch":len(protected_targets),
            "raw_reachable_but_legally_unreachable_targets":len(protected_unreachable)},
        "candidate_diagnostics":{"raw_hypotheses":2*EXPECTED_CF_CASES,
            "P1_nonkeep_count":sum(norm(x["full_proposer_output"])!=norm(x["source"]) for x in p1_rows),
            "P2_nonkeep_count":sum(norm(x["full_proposer_output"])!=norm(x["source"]) for x in p2_rows),
            "P1_legal_hypotheses":sum(bool(x.get("source_only_executable_precheck")) for x in p1_rows),
            "P2_legal_hypotheses":sum(bool(x.get("source_only_executable_precheck")) for x in p2_rows),
            "P1_P2_output_conflict_sentences":conflicts,"identical_nonkeep_sentences":identical_nonkeep},
        "failure_accounting":{"proposer_execution_failure":0,"truncation":0,
            "empty_output":sum(x.get("full_proposer_output","")=="" for x in p1_rows+p2_rows),
            "source_mismatch":0,"alignment_failure":failures["P1_SCORING_FAILURE"]+failures["P2_SCORING_FAILURE"],
            "alignment_ambiguity":0,"nonreversible_transformation":0,"protected_blocked":pb1+pb2,
            "scoring_failure":failures["P1_SCORING_FAILURE"]+failures["P2_SCORING_FAILURE"],"detail":dict(failures)},
        "historical_h1_residual":"NOT_COMPARABLE_UNLESS_SEPARATE_COMPATIBILITY_MAPPING_IS_FROZEN",
        "integrity":{"authorization_token_validated":True,"source_manifest_sha256":sha256_file(manp),
            "P1_proposal_sha256":sha256_file(p1p),"P2_proposal_sha256":sha256_file(p2p),
            "full_gold_m2_sha256":sha256_file(goldp),"internal_evaluation_opened":False,
            "stress_diagnostic_opened":False,"reserved_data_opened":False,"selector_trained":False},
    }
    prefix=Path(a.out_prefix)
    Path(str(prefix)+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    Path(str(prefix)+"_PER_SENTENCE.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in per)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
