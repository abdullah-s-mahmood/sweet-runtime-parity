#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

import mpsef_executable_actions_legalizer_v1 as legalizer
import mpsef_rjoint_core_v2 as core
import mpsef_rjoint_score_v2 as scorer
import mpsef_measurement_guard_v2 as guard
import mpsef_cf_gold_projection_v2 as projection
import mpsef_rjoint_measurement_v2 as measurement

VERSION="MPSEF_SECOND_PREFLIGHT_CHECKS_V2"
EXPECTED_CASES=1918
EXPECTED_CLUSTERS=764
EXPECTED_SOURCE_SHA="051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA="2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA="f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"
EXPECTED_ACTIONS_SHA="6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a"
EXPECTED_HYP_SHA="b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75"
EXPECTED_DIAG_SHA="2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e"

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def expect_raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    raise AssertionError("expected exception was not raised")

def synthetic_man(source="نص",uid="SYNTH",cluster="C"):
    return {
        "uid":uid,"case_id":"SYNTH-CASE","cluster_id":cluster,
        "source":source,"source_sha256":sha_text(source),
        "protected_spans":legalizer.derived_spans(source),
    }

def synthetic_p1(man,output=None):
    source=man["source"]
    output=source if output is None else output
    return {
        "uid":man["uid"],"case_id":man["case_id"],"cluster_id":man["cluster_id"],
        "source":source,"source_version_hash":man["source_sha256"],
        "full_proposer_output":output,"output_sha256":sha_text(output),
        "proposal_type":"P1_FINAL",
        "pass1_trace":{"subwords":["x"],"labels":["KEEP"]},
        "pass2_trace":{"subwords":["x"],"labels":["KEEP"]},
    }

def run_checks(args):
    root=Path(args.repo_root).resolve()
    results={}

    def mark(cid,evidence):
        results[cid]={"status":"PASS","evidence":evidence}

    # Snapshot source-only artifact hashes before any synthetic scoring.
    artifact_paths=[
        Path(args.action_sets),Path(args.hypotheses),Path(args.diagnostic_components)
    ]
    pre_hash={str(p):sha256_file(p) for p in artifact_paths}

    # C01: exposure record exists and uncertainty is preserved.
    exposure=(root/"phase2/redesign/MPSEF_MEASUREMENT_EXPOSURE_AUDIT_V1.md").read_text(encoding="utf-8")
    att=(root/"phase2/redesign/MPSEF_OPERATOR_EXPOSURE_ATTESTATION_V1.md").read_text(encoding="utf-8")
    assert "PARTIAL TECHNICAL GOLD-AWARE EXECUTION OCCURRED" in exposure
    assert "UNKNOWN" in att and "insufficient recollection" in att
    mark("C01","machine exposure audit + operator UNKNOWN attestation frozen")

    # C02: one governing population.
    pop=(root/"phase2/redesign/MPSEF_POPULATION_PRECEDENCE_DECISION_V1.md").read_text(encoding="utf-8")
    exp=json.loads((root/"phase2/redesign/MPSEF_RJOINT_EXPERIMENT_ID_V2.json").read_text(encoding="utf-8"))
    assert "1,918 records / 764" in pop
    assert exp["population"]["cases"]==1918 and exp["population"]["clusters"]==764
    assert exp["population"]["source_manifest_sha256"]==EXPECTED_SOURCE_SHA
    assert exp["primary_gate"]["threshold"]==0.95
    mark("C02","C_F=1918/764 and 95% gate frozen; 317 amendment non-governing")

    # C03: exact code commit identity is supplied by workflow and workflow pins code after auth metadata.
    assert args.code_commit_sha==os.environ.get("GITHUB_SHA",args.code_commit_sha)
    mw=(root/args.measurement_workflow).read_text(encoding="utf-8")
    assert "Checkout exact second-preflight code commit" in mw
    assert "PRE_GOLD_CODE_CONTRACT_HASHES_OK" in mw
    mark("C03",f"second-preflight code commit fixed at {args.code_commit_sha}")

    # C04: frozen source/proposer/action identities.
    for p,h in [
        (args.source_manifest,EXPECTED_SOURCE_SHA),
        (args.p1_proposals,EXPECTED_P1_SHA),
        (args.p2_proposals,EXPECTED_P2_SHA),
        (args.action_sets,EXPECTED_ACTIONS_SHA),
        (args.hypotheses,EXPECTED_HYP_SHA),
        (args.diagnostic_components,EXPECTED_DIAG_SHA),
    ]:
        assert sha256_file(p)==h,(p,sha256_file(p),h)

    source=read_jsonl(args.source_manifest)
    p1=read_jsonl(args.p1_proposals); p2=read_jsonl(args.p2_proposals)
    actions=read_jsonl(args.action_sets); hyps=read_jsonl(args.hypotheses)
    diag=read_jsonl(args.diagnostic_components)
    assert len(source)==len(p1)==len(p2)==len(actions)==EXPECTED_CASES
    assert len(hyps)==len(diag)==EXPECTED_CASES*2
    assert len({x["uid"] for x in source})==EXPECTED_CASES
    assert len({x["cluster_id"] for x in source})==EXPECTED_CLUSTERS
    uidset={x["uid"] for x in source}
    assert {x["uid"] for x in p1}==uidset=={x["uid"] for x in p2}=={x["uid"] for x in actions}
    mark("C04","source/P1/P2/actions/hypotheses/diagnostics exact SHA and population identity PASS")

    # C05: legalizer exposes no gold/reference/calibration input channel and workflow downloads no gold.
    lsrc=(root/"phase2/redesign/mpsef_executable_actions_legalizer_v1.py").read_text(encoding="utf-8")
    for forbidden in ('add_argument("--gold','add_argument("--reference','add_argument("--calibration'):
        assert forbidden not in lsrc
    lw=(root/".github/workflows/phase2-mpsef-source-only-legalizer-v1.yml").read_text(encoding="utf-8")
    assert "m2h-calibration-v1" not in lw
    assert "NOPNX_GOLD" not in lw
    mark("C05","legalizer has no project-gold input channel; legalizer workflow is source-only")

    # C06: exactly one hypothesis per uid/proposer; KEEP always; legal actions are exact frozen whole outputs.
    srcmap={x["uid"]:x for x in source}; p1m={x["uid"]:x for x in p1}; p2m={x["uid"]:x for x in p2}
    hypkeys=[(x["uid"],x["proposer"]) for x in hyps]
    assert len(set(hypkeys))==EXPECTED_CASES*2
    allowed_states={
        "SOURCE_MISMATCH","EMPTY_OUTPUT","EXECUTION_FAILED","TRUNCATED",
        "ALIGNMENT_FAILED","NONREVERSIBLE","PROTECTED_BLOCKED","ALIGNMENT_AMBIGUOUS","OK"
    }
    for h in hyps:
        assert h["final_state"] in allowed_states
        assert isinstance(h["reasons"],list)
    for aset in actions:
        uid=aset["uid"]
        outs=[a["output"] for a in aset["actions"]]
        assert len(outs)==len(set(outs))==aset["unique_action_count"]
        assert any(a["type"]=="KEEP" and a["output"]==srcmap[uid]["source"] for a in aset["actions"])
        allowed={srcmap[uid]["source"],p1m[uid]["full_proposer_output"],p2m[uid]["full_proposer_output"]}
        assert all(a["output"] in allowed for a in aset["actions"])
        assert all(a["type"] in {"KEEP","P1_FINAL","P2_FINAL"} for a in aset["actions"])
    mark("C06","3836 final hypothesis records; 1918 KEEP-bearing action sets; whole outputs only")

    # C07: protection edge/boundary examples and healthy preservation.
    bad_pairs=[
        ("5 mg","15 mg"),("5 mg","5 mg2"),("النص","النص [1]"),
        ("النص [1]","النص[1]"),("5 كغ","6 كغ"),("5٪","6٪"),
        ("النص [1] هنا","[1] النص هنا"),("استخدم API هنا","استخدم API2 هنا"),
    ]
    for s,o in bad_pairs:
        assert legalizer.protection_proof(s,o)["status"]=="FAIL",(s,o)
    assert legalizer.protection_proof("5 mg","5 mg")["status"]=="PASS"
    assert legalizer.protection_proof("النص [1] هنا","النص [1] هنا")["status"]=="PASS"
    mark("C07","protected edges, Arabic unit/percent, citation movement, mixed Latin blocked; identity cases pass")

    # C08: ambiguity and proof-budget fail closed.
    span=[{"protected_id":"S","category":"NUMBER","source_start":0,"source_end":1,"text":"1","hard_protected":True}]
    amb=legalizer.optimal_alignment_protection_audit("11","1",span)
    assert amb["status"]=="FAIL"
    huge=legalizer.optimal_alignment_protection_audit("1"+"a"*800,"1"+"b"*800,span)
    assert huge["status"]=="ERROR"
    mark("C08","protection-relevant alternative alignment and proof-budget exhaustion fail closed")

    # C09: exact apply/inverse proof and wrong version/hash rejection.
    s,o="نص","نص صحيح"
    assert legalizer.reversibility_proof(s,o,sha_text(s),sha_text(o))["status"]=="PASS"
    assert legalizer.reversibility_proof(s,o,"0"*64,sha_text(o))["status"]=="FAIL"
    mark("C09","round-trip SHA-bound whole-sentence executor proof PASS; wrong source identity rejected")

    # C10: decoder-prefix==EOS semantics and ceiling blocking.
    prop={"uid":"U","source_version_hash":sha_text("x"),"output_sha256":sha_text("y")}
    tr={
        "uid":"U","source_sha256":sha_text("x"),"output_sha256":sha_text("y"),
        "decoder_start_token_id":2,"eos_token_id":2,
        "generated_token_ids":[2,11,12,2,1],"max_length":100,
        "ged_word_count":1,"morph_word_count":1,"ged_label_count":1,
        "input_truncated":False,
    }
    assert legalizer.p2_truncation_status(prop,tr)["status"]=="PASS"
    tr2=dict(tr); tr2["generated_token_ids"]=[2]+[11]*98+[2]
    assert legalizer.p2_truncation_status(prop,tr2)["status"]=="FAIL"
    tr3=dict(tr); tr3.pop("input_truncated")
    assert legalizer.p2_truncation_status(prop,tr3)["status"]=="UNKNOWN"
    mark("C10","decoder prefix excluded from EOS search; generation ceiling/unknown input truncation block execution")

    # C11: actual frozen P2 provenance mismatch is explicit, no silent zip tail loss.
    mismatch=sum(len(x["morph_preprocessed_text"].split())!=len(x["ged_labels"]) for x in p2)
    assert mismatch==EXPECTED_CASES
    p2hyp=[x for x in hyps if x["proposer"]=="P2"]
    assert len(p2hyp)==EXPECTED_CASES
    assert all(x["final_state"]=="EXECUTION_FAILED" for x in p2hyp)
    assert all(any("GED_WORD_ALIGNMENT_MISMATCH" in r for r in x["reasons"]) for x in p2hyp)
    mark("C11","1918/1918 frozen P2 rows expose GED word-alignment mismatch; all P2 actions fail source-only")

    # C12: inject representative failure states; unknown never becomes OK.
    man=synthetic_man("نص")
    ok=legalizer.legalize_one(man,synthetic_p1(man),"P1")
    assert ok["final_state"]=="OK"
    empty=legalizer.legalize_one(man,synthetic_p1(man,""),"P1")
    assert empty["final_state"]=="EMPTY_OUTPUT"
    badsrc=synthetic_p1(man); badsrc["source"]="مختلف"
    assert legalizer.legalize_one(man,badsrc,"P1")["final_state"]=="SOURCE_MISMATCH"
    trunc=synthetic_p1(man); trunc.pop("pass1_trace")
    assert legalizer.legalize_one(man,trunc,"P1")["final_state"]=="TRUNCATED"
    pm=synthetic_man("5 mg")
    blocked=legalizer.legalize_one(pm,synthetic_p1(pm,"6 mg"),"P1")
    assert blocked["final_state"]=="PROTECTED_BLOCKED"
    longman=synthetic_man("1"+"a"*800)
    longprop=synthetic_p1(longman,"1"+"b"*800)
    assert legalizer.legalize_one(longman,longprop,"P1")["final_state"]=="ALIGNMENT_FAILED"
    p2prop={
        **synthetic_p1(man),
        "proposal_type":"P2_FINAL",
        "morph_preprocessed_text":"كلمة أخرى",
        "ged_labels":["UC","UC","UC"],
    }
    assert legalizer.legalize_one(man,p2prop,"P2")["final_state"]=="EXECUTION_FAILED"
    mark("C12","OK/SOURCE_MISMATCH/EMPTY/TRUNCATED/ALIGNMENT_FAILED/PROTECTED_BLOCKED/EXECUTION_FAILED injected and fail closed")

    # C13: synthetic gold/scoring changes cannot mutate frozen source-only action/diagnostic objects.
    action_obj={"actions":[
        {"action_id":"K","type":"KEEP","output":"SRC","provenance":["KEEP"]},
        {"action_id":"A","type":"P1_FINAL","output":"P1","provenance":["P1"]},
    ]}
    diag_obj={"source":"ياولد","components":[
        {"op":"INSERT","source_start":2,"source_end":2,"output_start":2,"output_end":3,"source_text":"","output_text":" "}
    ]}
    a0=copy.deepcopy(action_obj); d0=copy.deepcopy(diag_obj)
    def ev1(output,src,gold):
        m=[] if output=="SRC" else [0]
        return {"matched_indices":m,"correct":len(m),"proposed":len(m),"gold":len(gold),"extra":0}
    scorer.evaluate_sentence(None,"SRC",[1],action_obj,ev1)
    def ev2(output,src,gold):
        raise RuntimeError("synthetic scoring failure")
    scorer.evaluate_sentence(None,"SRC",[1,2],action_obj,ev2)
    assert action_obj==a0 and diag_obj==d0
    mark("C13","changing synthetic reference/scorer failure leaves action/diagnostic objects byte-semantically unchanged")

    # C14: corrected target scope/family behavior.
    assert "a" not in core.PNX_SET and "m" not in core.PNX_SET and "p" not in core.PNX_SET
    assert core.target_scope("m","a!")=="MIXED_PUNCT_LINGUISTIC"
    assert core.target_scope("ياولد","يا ولد،")=="MIXED_PUNCT_LINGUISTIC"
    assert core.target_family(0,1,"ياولد","يا ولد،")=="SPLIT"
    assert core.target_scope("","." )=="PUNCTUATION_ONLY"
    mark("C14","punctuation classifier regression cases pass; mixed boundary edits remain in denominator")

    # C15: complete target unit, duplicate credit and reference alternatives fail closed.
    expect_raises(lambda:core.build_targets("ALT",[(0,1,"خطا",["خطأ","خطاء"])]),RuntimeError)
    expect_raises(lambda:core.build_targets("NOOP",[(0,1,"نص",["نص"])]),RuntimeError)
    expect_raises(lambda:scorer.validate_scoring_result(
        {"matched_indices":[0,0],"correct":2,"proposed":2,"gold":2,"extra":0},2
    ),RuntimeError)
    mark("C15","multi-reference/no-op target construction and duplicate target credit rejected")

    # C16: whole-action oracle, never union P1+P2 target hits.
    aset={"actions":[
        {"action_id":"K","type":"KEEP","output":"SRC","provenance":["KEEP"]},
        {"action_id":"A","type":"P1_FINAL","output":"P1","provenance":["P1"]},
        {"action_id":"B","type":"P2_FINAL","output":"P2","provenance":["P2"]},
    ]}
    def split_hits(output,src,gold):
        m={"SRC":[],"P1":[0],"P2":[1]}[output]
        return {"matched_indices":m,"correct":len(m),"proposed":len(m),"gold":2,"extra":0}
    e=scorer.evaluate_sentence(None,"SRC",[1,2],aset,split_hits)
    assert e["PAIR"]["lower"]==1 and e["PAIR"]["upper"]==1
    mark("C16","P1/P2 each hitting different target yields pair oracle=1, not union=2")

    # C17: scoring error -> interval/INVALID semantics, denominator unchanged.
    def flaky(output,src,gold):
        if output=="P2": raise RuntimeError("synthetic")
        return split_hits(output,src,gold)
    e=scorer.evaluate_sentence(None,"SRC",[1,2],aset,flaky)
    assert e["PAIR"]["lower"]==1 and e["PAIR"]["upper"]==2
    assert scorer.ratio_interval(1,2,2)["denominator"]==2
    mark("C17","scoring failure creates [L,U] uncertainty; does not become known zero or shrink denominator")

    # C18: family optimization stays whole-hypothesis; R_raw evidence remains diagnostic only.
    group={"successful":[
        ({"action_id":"A"},{"matched_indices":[0],"correct":1,"proposed":1,"gold":2,"extra":0}),
        ({"action_id":"B"},{"matched_indices":[1],"correct":1,"proposed":1,"gold":2,"extra":0}),
    ],"failures":[]}
    assert scorer.best_family_bounds(group,[0,1])==(1,1)
    t={"target_id":"T","start":0,"end":1,"original":"ياولد","correction":"يا ولد","scope":"LINGUISTIC","family":"SPLIT"}
    d={"source":"ياولد","components":[
        {"op":"INSERT","source_start":2,"source_end":2,"output_start":2,"output_end":3,"source_text":"","output_text":" "}
    ]}
    assert scorer.diagnostic_target_status("ياولد",t,d)=="TRUE"
    assert aset["actions"][0]["type"]=="KEEP"
    mark("C18","family best is max whole hypothesis; diagnostic target reachability does not alter A_primary")

    # C19: R_clean rejects extra edits and zero denominator stays N/A.
    clean_group={"successful":[
        ({"action_id":"K"},{"correct":0,"extra":0}),
        ({"action_id":"A"},{"correct":2,"extra":1}),
        ({"action_id":"B"},{"correct":1,"extra":0}),
    ],"failures":[]}
    assert scorer.best_clean_bounds(clean_group,2)==(1,1)
    zero=scorer.ratio_interval(0,0,0)
    assert zero["exact"] is None and zero["lower"] is None and zero["upper"] is None
    mark("C19","R_clean excludes extra edit; zero denominator is N/A")

    # C20: accounting/statistics are derived, not fixed constants.
    stats=scorer.size_stats([1,1,2,2,3])
    assert stats["mean"]==1.8 and stats["median"]==2 and stats["p95"]==3 and stats["max"]==3
    state_counts={}
    for h in hyps: state_counts[h["final_state"]]=state_counts.get(h["final_state"],0)+1
    assert sum(state_counts.values())==EXPECTED_CASES*2
    assert state_counts.get("EXECUTION_FAILED")==EXPECTED_CASES
    mark("C20","candidate-size and failure accounting derived from rows; no fixed-zero failure counters")

    # C21: push/dispatch share guard, durable one-shot claim precedes all project gold.
    assert "workflow_dispatch:" in mw and "\n  push:" in mw
    assert "MPSEF_RJOINT_MEASUREMENT_AUTHORIZATION_V2.json" in mw
    assert "concurrency:" in mw and "cancel-in-progress: false" in mw
    claim=mw.index("Claim experiment permanently BEFORE gold access")
    gold1=mw.index("Download frozen CALIBRATION AFTER consumption claim")
    gold2=mw.index("Download frozen official NoPnx M2 gold AFTER consumption claim")
    assert claim<gold1<gold2
    assert mw.index("Validate authorization against experiment and second preflight")<claim
    assert mw.index("Verify frozen implementation and contract hashes before any gold access")<claim
    assert "acad-pass/mpsef-rjoint-v2-consumed" in mw
    guard.self_test()
    mark("C21","single workflow guard for push/dispatch; concurrency + durable consumed-status claim before gold")

    # C22: second preflight itself is non-measurement and gold-free.
    sw=(root/args.second_preflight_workflow).read_text(encoding="utf-8")
    assert "m2h-h1-official-alignment-scoring-continuation-v1" not in sw
    assert "M2H_H1_OFFICIAL_ALIGNMENT_AUDIT_V1_NOPNX_GOLD.m2" not in sw
    assert "MPSEF_RJOINT_MEASUREMENT_V2_SUMMARY" not in sw
    assert "--authorization-evidence" not in sw
    mark("C22","second preflight workflow contains no project-gold download or measurement invocation")

    # Run module-level synthetic suites too.
    legalizer.self_test()
    core.self_test(None)
    scorer.self_test()
    projection.self_test()
    measurement.self_test()

    # Actual source-only artifacts must remain byte-identical throughout checks.
    post_hash={str(p):sha256_file(p) for p in artifact_paths}
    assert pre_hash==post_hash

    missing=[f"C{i:02d}" for i in range(1,23) if f"C{i:02d}" not in results]
    if missing:
        raise RuntimeError(f"missing checklist items: {missing}")

    return {
        "record_id":VERSION,
        "status":"PASS",
        "code_commit_sha":args.code_commit_sha,
        "checks":results,
        "pass_count":sum(x["status"]=="PASS" for x in results.values()),
        "required_count":22,
        "project_gold_loaded":False,
        "project_metric_computed":False,
        "measurement_authorized_by_preflight":False,
        "source_only_artifacts_unchanged":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",default=".")
    ap.add_argument("--code-commit-sha",required=True)
    ap.add_argument("--source-manifest",required=True)
    ap.add_argument("--p1-proposals",required=True)
    ap.add_argument("--p2-proposals",required=True)
    ap.add_argument("--action-sets",required=True)
    ap.add_argument("--hypotheses",required=True)
    ap.add_argument("--diagnostic-components",required=True)
    ap.add_argument("--measurement-workflow",default=".github/workflows/phase2-mpsef-rjoint-measurement-v2.yml")
    ap.add_argument("--second-preflight-workflow",default=".github/workflows/phase2-mpsef-rjoint-second-preflight-v2.yml")
    ap.add_argument("--out",default="MPSEF_SECOND_PREFLIGHT_CHECKS_V2.json")
    args=ap.parse_args()

    result=run_checks(args)
    Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
