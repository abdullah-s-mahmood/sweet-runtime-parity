"""Gold-independent runtime candidate acceptance gate.

Consumes:
- AraBART independent passage outputs (no gold)
- 60 unlabeled surgical NoPnx1 edits from the passage queue
- 19 unlabeled normalized candidates
- morphology analyses for normalized candidates, but explicitly ignores all
  human/gold fields in that file.

Produces runtime decisions and a feature table WITHOUT reading Nahw targets or
human adjudication labels. A separate evaluator may load labels afterwards.
"""
from __future__ import annotations

import collections
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
ARABART=ART/"ARABART_INDEPENDENT_GENERATOR.json"
SURG_QUEUE=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl"
NORM_QUEUE=ROOT/"PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl"
MORPH=ROOT/"PHASE2_MORPH_SURFACE_CANDIDATES.jsonl"


def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def strip_marks(s):
    return "".join(ch for ch in s if unicodedata.category(ch)!="Mn" and ch!="\u0640")


def canon(s):
    s=strip_marks(s)
    return "".join(ch for ch in s if ch.isalnum() or "\u0600" <= ch <= "\u06ff")


def op_family(label):
    if "I_[" in label: return "INSERT"
    if "R_[" in label: return "REPLACE"
    if "D" in label: return "DELETE"
    if "A_[" in label: return "APPEND"
    return "OTHER"


def nonspace_insert(label):
    return op_family(label)=="INSERT" and "I_[ ]" not in label and "I_[  ]" not in label


def surgical_op_aware(label,conf):
    fam=op_family(label)
    if fam=="INSERT": return nonspace_insert(label)
    if fam=="REPLACE": return float(conf)>=0.80
    return False


def apply_local(source_word,span,replacement):
    a,b=map(int,span)
    if source_word[a:b]=="" and a==b:
        return source_word[:a]+replacement+source_word[b:]
    if source_word[a:b] is None:
        return source_word
    return source_word[:a]+replacement+source_word[b:]


def scientific_risk(word):
    return bool(
        re.search(r"[0-9A-Za-z]",word)
        or re.search(r"\[[0-9]+\]",word)
        or re.search(r"[%=<>±]",word)
    )


def arabart_local_evidence(pass_rec,word_index,candidate_result):
    regions=pass_rec["alignment_regions"]
    hits=[]
    cand=canon(candidate_result)
    for reg in regions:
        i1,i2=reg["source_word_span"]
        if i1 <= int(word_index) < i2 or (i1==i2==int(word_index)):
            outs=[canon(x) for x in reg["output_words"]]
            out_join="".join(outs)
            exact_local=(len(outs)==1 and outs[0]==cand)
            normalized_support=(cand!="" and (cand in outs or cand==out_join))
            hits.append({
                "region":reg,
                "exact_local":exact_local,
                "normalized_support":normalized_support,
            })
    if not hits:
        # If no changed region covers the word, AraBART left this local position
        # unchanged under the coarse alignment.
        return {
            "changed_same_region":False,
            "exact_local_agreement":False,
            "normalized_local_agreement":False,
            "regions":[],
        }
    return {
        "changed_same_region":True,
        "exact_local_agreement":any(x["exact_local"] for x in hits),
        "normalized_local_agreement":any(x["normalized_support"] for x in hits),
        "regions":[x["region"] for x in hits],
    }


def ged_for_word(pass_rec,word_index):
    ged=pass_rec["trace"]["ged"]
    wi=int(word_index)
    if 0 <= wi < len(ged):
        return ged[wi]
    return {"word_index":wi,"label":"UNKNOWN","score":0.0}


def safe_morph_features(row):
    """Extract only runtime morphology fields. Never expose candidate_class/target_evaluation."""
    analyses=row.get("all_morph_analyses",[])
    pos=[x.get("analysis",{}).get("pos") for x in analyses]
    nonprop=[p for p in pos if p and p!="noun_prop"]
    top=row.get("bert_context_analyses",[])[:3]
    top_pos=[x.get("analysis",{}).get("pos") for x in top]
    top_lex=[x.get("analysis",{}).get("lex") for x in top]
    return {
        "direct_patch":row.get("direct_patch"),
        "morph_analysis_count":int(row.get("morph_analysis_count",0)),
        "noun_prop_only":bool(analyses) and not nonprop,
        "bert_top1_surface":row.get("bert_top1_surface"),
        "bert_top2_surface_consensus":row.get("bert_top2_surface_consensus"),
        "bert_top_pos":top_pos,
        "bert_top_lex":top_lex,
    }


def build_candidates():
    surg=[]
    for passage in read_jsonl(SURG_QUEUE):
        pid=int(passage["passage_id"])
        for i,e in enumerate(passage["variants"]["nopnx1"]["applied_model_edits"]):
            src=e["source_word"]
            result=apply_local(src,e["source_local_span"],e["replacement"])
            surg.append({
                "candidate_id":f"SURG-{pid}-{i}",
                "stream":"SURGICAL",
                "passage_id":pid,
                "word_index":int(e["word_index"]),
                "source_passage":passage["source"],
                "source_word":src,
                "candidate_result_word":result,
                "model_label":e["label"],
                "model_confidence":float(e["top1_confidence"]),
                "operation_family":op_family(e["label"]),
                "operation_aware":surgical_op_aware(e["label"],e["top1_confidence"]),
                "direct_patch":None,
                "morph":None,
            })
    assert len(surg)==60, len(surg)

    morph_rows={x["candidate_id"]:safe_morph_features(x) for x in read_jsonl(MORPH)}
    norm=[]
    for x in read_jsonl(NORM_QUEUE):
        cid=x["candidate_id"]
        mf=morph_rows.get(cid,{
            "direct_patch":None,"morph_analysis_count":0,"noun_prop_only":False,
            "bert_top1_surface":None,"bert_top2_surface_consensus":None,
            "bert_top_pos":[],"bert_top_lex":[],
        })
        norm.append({
            "candidate_id":cid,
            "stream":"NORMALIZED",
            "passage_id":int(x["passage_id"]),
            "word_index":int(x["word_index"]),
            "source_passage":x["source_passage"],
            "source_word":x["source_word"],
            "candidate_result_word":x["normalized_all_candidates_result_word"],
            "model_label":x["model_label"],
            "model_confidence":float(x["top1_confidence"]),
            "operation_family":op_family(x["model_label"]),
            "operation_aware":None,
            "direct_patch":mf["direct_patch"],
            "morph":mf,
        })
    assert len(norm)==19, len(norm)
    return surg+norm


def deterministic_veto(c):
    reasons=[]
    if scientific_risk(c["source_word"]):
        reasons.append("PROTECTED_SCIENTIFIC_RISK")
    if canon(c["source_word"])==canon(c["candidate_result_word"]):
        # If the only difference is removed/changed marks, do not auto-accept
        # without a dedicated diacritic validator.
        reasons.append("NO_BASE_LETTER_CHANGE_OR_MARK_ONLY")
    if c["stream"]=="NORMALIZED":
        m=c["morph"] or {}
        if m.get("noun_prop_only"):
            reasons.append("MORPH_NOUN_PROP_FALLBACK_RISK")
        if c["operation_family"]=="DELETE":
            reasons.append("DELETE_OR_DIRECTION_LOSS_RISK")
    return reasons


def decisions(c):
    veto=c["veto_reasons"]
    agree=c["arabart"]["normalized_local_agreement"]
    exact=c["arabart"]["exact_local_agreement"]
    ged_error=c["ged"]["label"] not in ("UC","UNKNOWN")

    direct_safe=bool(c.get("direct_patch")) and not veto
    if c["stream"]=="SURGICAL":
        base_eligible=bool(c["operation_aware"])
    else:
        base_eligible=True

    # A: narrow conservative reference.
    if direct_safe:
        pa="ACCEPT"
    elif veto:
        pa="REJECT"
    else:
        pa="REVIEW"

    # B: independent multi-model agreement.
    if veto:
        pb="REJECT"
    elif direct_safe:
        pb="ACCEPT"
    elif base_eligible and agree:
        pb="ACCEPT"
    else:
        pb="REVIEW"

    # C: same but GED must independently mark the location for agreement branch.
    if veto:
        pc="REJECT"
    elif direct_safe:
        pc="ACCEPT"
    elif base_eligible and agree and ged_error:
        pc="ACCEPT"
    else:
        pc="REVIEW"

    # D: strongest exact-local agreement only.
    if veto:
        pd="REJECT"
    elif direct_safe:
        pd="ACCEPT"
    elif base_eligible and exact:
        pd="ACCEPT"
    else:
        pd="REVIEW"

    return {
        "DIRECT_PATCH_SAFE":pa,
        "INDEPENDENT_AGREEMENT":pb,
        "AGREEMENT_PLUS_GED":pc,
        "EXACT_LOCAL_AGREEMENT":pd,
    }


def main():
    ara=json.loads(ARABART.read_text(encoding="utf-8"))
    candidates=build_candidates()
    out=[]
    counts=collections.Counter()
    for c in candidates:
        pass_rec=ara["passages"][str(c["passage_id"])]
        c["arabart"]=arabart_local_evidence(pass_rec,c["word_index"],c["candidate_result_word"])
        c["ged"]=ged_for_word(pass_rec,c["word_index"])
        c["veto_reasons"]=deterministic_veto(c)
        c["runtime_decisions"]=decisions(c)
        for pol,d in c["runtime_decisions"].items():
            counts[f"{pol}:{d}"]+=1
        out.append(c)

    result={
        "status":"PHASE2_INDEPENDENT_ACCEPTANCE_RUNTIME_COMPLETE",
        "development_only":True,
        "gold_or_human_labels_read":False,
        "candidate_rows":len(out),
        "streams":{
            "SURGICAL":sum(x["stream"]=="SURGICAL" for x in out),
            "NORMALIZED":sum(x["stream"]=="NORMALIZED" for x in out),
        },
        "runtime_decision_counts":dict(counts),
        "policy_definitions":{
            "DIRECT_PATCH_SAFE":"ACCEPT direct source patch only; deterministic veto -> REJECT; otherwise REVIEW",
            "INDEPENDENT_AGREEMENT":"ACCEPT direct patch or base-eligible candidate with AraBART normalized local agreement; veto -> REJECT; otherwise REVIEW",
            "AGREEMENT_PLUS_GED":"as independent agreement, but non-direct branch also requires GED non-UC",
            "EXACT_LOCAL_AGREEMENT":"as independent agreement, but require exact one-word canonical AraBART local agreement",
        },
        "rows":out,
        "limitations":[
            "AraBART local evidence uses development whitespace-token alignment and must not be treated as production alignment.",
            "Deterministic vetoes are conservative prototypes and do not rewrite text.",
            "No target, reference, explanation, human correctness label, or sealed evidence is read by this runtime gate.",
        ],
    }
    ART.mkdir(parents=True,exist_ok=True)
    (ART/"INDEPENDENT_ACCEPTANCE_RUNTIME.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"PHASE2_INDEPENDENT_ACCEPTANCE_FEATURES.jsonl").write_text(
        "\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8"
    )
    compact={
        "status":result["status"],
        "candidate_rows":len(out),
        "streams":result["streams"],
        "runtime_decision_counts":result["runtime_decision_counts"],
        "arabart_agreement":{
            "normalized":sum(x["arabart"]["normalized_local_agreement"] for x in out),
            "exact":sum(x["arabart"]["exact_local_agreement"] for x in out),
        },
        "veto_rows":sum(bool(x["veto_reasons"]) for x in out),
    }
    print(json.dumps(compact,ensure_ascii=False))


if __name__=="__main__":
    main()
