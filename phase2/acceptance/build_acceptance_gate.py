"""Build runtime-only features and retrospective policy diagnostics for the
Phase 2 Independent Candidate Acceptance Gate.

Runtime decisions are materialized before human adjudication labels are loaded.
Gold/previous labels are used only in the final evaluation section.
"""
from __future__ import annotations

import collections
import json
import math
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
ARABART=ART/"ARABART_SECOND_GENERATOR.json"
SURG_QUEUE=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl"
NORM_QUEUE=ROOT/"PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl"
MORPH_QUEUE=ROOT/"PHASE2_MORPH_SURFACE_ADJUDICATION_QUEUE.jsonl"
SURG_LABELS=ROOT/"PHASE2_SURGICAL_APPLIED_EDIT_ADJUDICATION.jsonl"
NORM_LABELS=ROOT/"PHASE2_NORMALIZED_CANDIDATE_ADJUDICATION.jsonl"

RUNTIME_FEATURES=ROOT/"PHASE2_ACCEPTANCE_RUNTIME_FEATURES.jsonl"
POLICY_RESULTS=ROOT/"PHASE2_ACCEPTANCE_POLICY_RESULTS.json"
NEW_EDITS=ROOT/"PHASE2_ARABART_NEW_EDIT_QUEUE.jsonl"
SUMMARY=ROOT/"PHASE2_ACCEPTANCE_GATE_SUMMARY.json"


def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def strip_marks(s):
    return "".join(ch for ch in unicodedata.normalize("NFC",s) if unicodedata.category(ch)!="Mn" and ch!="ـ")


def is_punc_or_symbol(ch):
    return unicodedata.category(ch)[0] in {"P","S"}


def token_base(s):
    s=strip_marks(s)
    return "".join(ch for ch in s if not is_punc_or_symbol(ch) and not ch.isspace())


def surface_core(s):
    s=unicodedata.normalize("NFC",s)
    return "".join(ch for ch in s if not is_punc_or_symbol(ch) and not ch.isspace())


def lexical_units(text):
    out=[]
    for wi,w in enumerate(text.split()):
        b=token_base(w)
        if b:
            out.append({"word_index":wi,"surface":w,"base":b})
    return out


def lev(a,b):
    if a==b:return 0
    if not a:return len(b)
    if not b:return len(a)
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]


def sub_cost(a,b):
    if a==b:return 0.0
    return min(1.0,lev(a,b)/max(len(a),len(b),1))


def align_words(src_text,out_text):
    src=lexical_units(src_text); out=lexical_units(out_text)
    n,m=len(src),len(out)
    dp=[[0.0]*(m+1) for _ in range(n+1)]
    back=[[None]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1):dp[i][0]=i;back[i][0]="D"
    for j in range(1,m+1):dp[0][j]=j;back[0][j]="I"
    for i in range(1,n+1):
        for j in range(1,m+1):
            opts=[
                (dp[i-1][j-1]+sub_cost(src[i-1]["base"],out[j-1]["base"]),"S"),
                (dp[i-1][j]+1.0,"D"),
                (dp[i][j-1]+1.0,"I"),
            ]
            dp[i][j],back[i][j]=min(opts,key=lambda z:z[0])
    pairs=[]; inserted=[]
    i,j=n,m
    while i or j:
        op=back[i][j]
        if op=="S":
            pairs.append((i-1,j-1));i-=1;j-=1
        elif op=="D":
            pairs.append((i-1,None));i-=1
        elif op=="I":
            inserted.append(j-1);j-=1
        else:
            raise RuntimeError(f"alignment backtrace failure {i},{j}")
    pairs.reverse();inserted.reverse()
    by_source={}
    for si,oi in pairs:
        s=src[si]
        o=out[oi] if oi is not None else None
        by_source[s["word_index"]]={
            "source_lexical_index":si,
            "output_lexical_index":oi,
            "source_surface":s["surface"],
            "source_base":s["base"],
            "output_surface":o["surface"] if o else None,
            "output_base":o["base"] if o else None,
            "substitution_cost":sub_cost(s["base"],o["base"]) if o else 1.0,
        }
    return {"source_units":src,"output_units":out,"by_source_word_index":by_source,"inserted_output_indices":inserted,"alignment_cost":dp[n][m]}


def op_family(label):
    if "I_[" in label:return "INSERT"
    if "R_[" in label:return "REPLACE"
    if "D" in label:return "DELETE"
    if "A_[" in label:return "APPEND"
    return "OTHER"


def operation_aware_runtime(label,confidence):
    fam=op_family(label)
    if fam=="INSERT":
        m=re.search(r"I_\[([^\]]*)\]",label)
        payload=m.group(1) if m else ""
        return bool(payload.strip())
    if fam=="REPLACE":
        return float(confidence)>=0.80
    return False


def hard_vetoes(row):
    veto=[]
    src=row["source_word"]; cand=row["candidate_word"]
    fam=row["operation_family"]
    if fam=="DELETE" and row.get("source_text") and all(is_punc_or_symbol(c) for c in row["source_text"]):
        veto.append("PUNCTUATION_STRUCTURE_DELETE")
    # Arabic defective noun risk: final kasratan often represents an elided yaa;
    # adding accusative alif without restoring yaa is unsafe.
    if "ٍ" in src:
        sb=token_base(src); cb=token_base(cand)
        if cb==sb+"ا" and not cb.endswith("يا"):
            veto.append("DEFECTIVE_NOUN_YAA_RESTORATION_RISK")
    if row.get("morph_top1_pos")=="noun_prop" and row.get("morph_top2_consensus"):
        veto.append("MORPH_PROPER_NOUN_FALLBACK_RISK")
    if token_base(src)==token_base(cand):
        veto.append("BASE_NOOP")
    return veto


def build_runtime_candidates():
    arabart=json.loads(ARABART.read_text(encoding="utf-8"))
    alignments={}
    for pid,p in arabart["passages"].items():
        alignments[int(pid)]=align_words(p["source"],p["generated_raw"])

    morph={}
    if MORPH_QUEUE.exists():
        for r in read_jsonl(MORPH_QUEUE):
            m=r.get("morphology",{})
            top=(m.get("contextual_bert_top1") or {})
            ana=(top.get("morph") or {})
            morph[r["candidate_id"]]={
                "morph_analyzable":bool(m.get("analyzable")),
                "morph_surface_count":m.get("unique_surface_count"),
                "morph_top1_surface":top.get("surface"),
                "morph_top1_pos":ana.get("pos"),
                "morph_top1_case":ana.get("cas"),
                "morph_top1_mood":ana.get("mod"),
                "morph_top1_aspect":ana.get("asp"),
                "morph_top2_consensus":m.get("bert_top2_surface_consensus"),
                "direct_patch":m.get("direct_patch"),
            }

    candidates=[]
    known_words=collections.defaultdict(set)

    # 60 surgical candidates from raw queue, no human labels.
    for p in read_jsonl(SURG_QUEUE):
        pid=int(p["passage_id"]); source=p["source"]
        edits=p["variants"]["nopnx1"]["applied_model_edits"]
        for ei,e in enumerate(edits):
            cid=f"SURG-{pid}-{ei}"
            wi=int(e["word_index"])
            cand_word=e.get("replacement")
            # Persisted surgical trace replacement may be only edited subword for
            # some labels; derive final word by applying the recorded local span.
            src_word=e["source_word"]
            a,b=map(int,e["source_local_span"])
            final_word=src_word[:a]+e["replacement"]+src_word[b:]
            al=alignments[pid]["by_source_word_index"].get(wi)
            ged=arabart["passages"][str(pid)]["ged_words"][wi] if wi<len(arabart["passages"][str(pid)]["ged_words"]) else None
            row={
                "candidate_id":cid,"stream":"SURGICAL_NOPNX1","passage_id":pid,
                "source_passage":source,"word_index":wi,"source_word":src_word,
                "candidate_word":final_word,"source_text":e["source_text"],
                "replacement":e["replacement"],"model_label":e["label"],
                "sweet_confidence":float(e["top1_confidence"]),"operation_family":op_family(e["label"]),
                "operation_aware_allow":operation_aware_runtime(e["label"],e["top1_confidence"]),
                "ged":ged,
                "arabart_alignment":al,
                "arabart_base_agree":bool(al and al["output_base"]==token_base(final_word)),
                "arabart_exact_core_agree":bool(al and surface_core(al["output_surface"] or "")==surface_core(final_word)),
                "arabart_changes_source":bool(al and al["output_base"]!=token_base(src_word)),
                "morph_analyzable":None,"morph_surface_count":None,"morph_top1_surface":None,
                "morph_top1_pos":None,"morph_top1_case":None,"morph_top1_mood":None,
                "morph_top1_aspect":None,"morph_top2_consensus":None,"direct_patch":None,
            }
            row["hard_vetoes"]=hard_vetoes(row)
            candidates.append(row);known_words[pid].add(wi)

    # 19 normalized candidates, no human labels.
    for r in read_jsonl(NORM_QUEUE):
        pid=int(r["passage_id"]);wi=int(r["word_index"]);cid=r["candidate_id"]
        candidate_word=r["normalized_single_candidate_result_word"]
        al=alignments[pid]["by_source_word_index"].get(wi)
        ged=arabart["passages"][str(pid)]["ged_words"][wi] if wi<len(arabart["passages"][str(pid)]["ged_words"]) else None
        mm=morph.get(cid,{})
        row={
            "candidate_id":cid,"stream":"NORMALIZED_FALLBACK","passage_id":pid,
            "source_passage":r["source_passage"],"word_index":wi,"source_word":r["source_word"],
            "candidate_word":candidate_word,"source_text":r["normalized_source_text"],
            "replacement":r["normalized_replacement"],"model_label":r["model_label"],
            "sweet_confidence":float(r["top1_confidence"]),"operation_family":op_family(r["model_label"]),
            "operation_aware_allow":operation_aware_runtime(r["model_label"],r["top1_confidence"]),
            "ged":ged,"arabart_alignment":al,
            "arabart_base_agree":bool(al and al["output_base"]==token_base(candidate_word)),
            "arabart_exact_core_agree":bool(al and surface_core(al["output_surface"] or "")==surface_core(candidate_word)),
            "arabart_changes_source":bool(al and al["output_base"]!=token_base(r["source_word"])),
            **{k:mm.get(k) for k in ("morph_analyzable","morph_surface_count","morph_top1_surface","morph_top1_pos","morph_top1_case","morph_top1_mood","morph_top1_aspect","morph_top2_consensus","direct_patch")},
        }
        row["hard_vetoes"]=hard_vetoes(row)
        candidates.append(row);known_words[pid].add(wi)

    if len(candidates)!=79:
        raise RuntimeError(f"expected 79 candidates, got {len(candidates)}")

    # Materialize runtime decisions before reading adjudication labels.
    for r in candidates:
        ged_error=bool(r.get("ged") and r["ged"].get("label")!="UC")
        ged_prob=float(r.get("ged",{}).get("error_probability",0.0) or 0.0)
        no_veto=not r["hard_vetoes"]
        ara=r["arabart_base_agree"]
        exact=r["arabart_exact_core_agree"]
        source_safe_direction=(r["stream"]=="SURGICAL_NOPNX1" or bool(r.get("direct_patch")) or bool(r.get("morph_top2_consensus")))

        r["runtime_policies"]={
            "ARABART_BASE_AGREEMENT": "ACCEPT" if ara and no_veto else ("REJECT" if r["hard_vetoes"] else "REVIEW"),
            "ARABART_BASE_PLUS_GED": "ACCEPT" if ara and ged_error and no_veto else ("REJECT" if r["hard_vetoes"] else "REVIEW"),
            "STRICT_CONSENSUS": "ACCEPT" if ara and ged_prob>=0.30 and no_veto and source_safe_direction else ("REJECT" if r["hard_vetoes"] else "REVIEW"),
            "REVIEW_FIRST": "ACCEPT" if exact and no_veto and source_safe_direction else ("REJECT" if r["hard_vetoes"] else "REVIEW"),
        }

    # AraBART edits not covered by the known 79-word candidate locations.
    new_edits=[]
    for pid,a in alignments.items():
        for wi,al in a["by_source_word_index"].items():
            if wi in known_words[pid]:continue
            if al["output_surface"] is None:continue
            if al["output_base"]==al["source_base"]:continue
            new_edits.append({
                "arabart_edit_id":f"AB-{pid}-{wi}",
                "passage_id":pid,"word_index":wi,
                "source_passage":arabart["passages"][str(pid)]["source"],
                "source_word":al["source_surface"],
                "arabart_word":al["output_surface"],
                "source_base":al["source_base"],"arabart_base":al["output_base"],
                "alignment_cost":al["substitution_cost"],
                "ged":arabart["passages"][str(pid)]["ged_words"][wi] if wi<len(arabart["passages"][str(pid)]["ged_words"]) else None,
                "status":"UNADJUDICATED_SECOND_GENERATOR_EDIT",
            })
    return candidates,new_edits,alignments


def evaluate(candidates):
    # Labels are intentionally loaded only after runtime policy fields exist.
    surg={}
    for x in read_jsonl(SURG_LABELS):
        surg[f"SURG-{int(x['passage_id'])}-{int(x['edit_index'])}"]=x
    norm={x["candidate_id"]:x for x in read_jsonl(NORM_LABELS)}

    def label_for(r):
        if r["stream"]=="SURGICAL_NOPNX1":
            x=surg[r["candidate_id"]]; cls=x["classification"]; sev=x.get("severity")
        else:
            x=norm[r["candidate_id"]]; cls=x["classification"]; sev=x.get("severity")
        good=cls in {"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
        return cls,sev,good

    policies=sorted(candidates[0]["runtime_policies"])
    results={}
    for p in policies:
        rows=[]
        for r in candidates:
            cls,sev,good=label_for(r)
            rows.append((r,r["runtime_policies"][p],cls,sev,good))
        accepted=[x for x in rows if x[1]=="ACCEPT"]
        review=[x for x in rows if x[1]=="REVIEW"]
        reject=[x for x in rows if x[1]=="REJECT"]
        results[p]={
            "candidates":len(rows),
            "accepted":len(accepted),"review":len(review),"rejected":len(reject),
            "accepted_supported":sum(x[4] for x in accepted),
            "accepted_wrong":sum(x[2]=="WRONG_CORRECTION" for x in accepted),
            "accepted_partial":sum(x[2]=="PARTIAL_CORRECTION" for x in accepted),
            "accepted_unnecessary":sum(x[2]=="UNNECESSARY_EDIT" for x in accepted),
            "accepted_review_required":sum(x[2]=="REVIEW_REQUIRED" for x in accepted),
            "accepted_high_or_critical_wrong":sum(x[2]=="WRONG_CORRECTION" and x[3] in {"HIGH","CRITICAL"} for x in accepted),
            "supported_precision":(sum(x[4] for x in accepted)/len(accepted)) if accepted else None,
            "supported_coverage_vs_all_supported":sum(x[4] for x in accepted)/sum(x[4] for x in rows),
            "accepted_ids":[x[0]["candidate_id"] for x in accepted],
        }

    # Known regression cases.
    checks={}
    for r in candidates:
        if r["candidate_id"] in {"NORM-38-24-0","NORM-63-24-0","NORM-63-11-0"}:
            cls,sev,good=label_for(r)
            checks[r["candidate_id"]]={
                "source_word":r["source_word"],"candidate_word":r["candidate_word"],
                "human_class_for_evaluation_only":cls,
                "arabart_alignment":r["arabart_alignment"],
                "hard_vetoes":r["hard_vetoes"],
                "runtime_policies":r["runtime_policies"],
                "morph_top1_surface":r.get("morph_top1_surface"),
                "morph_top2_consensus":r.get("morph_top2_consensus"),
            }

    by_stream={}
    for stream in ("SURGICAL_NOPNX1","NORMALIZED_FALLBACK"):
        rr=[r for r in candidates if r["stream"]==stream]
        by_stream[stream]={
            "n":len(rr),
            "arabart_base_agree":sum(r["arabart_base_agree"] for r in rr),
            "arabart_exact_core_agree":sum(r["arabart_exact_core_agree"] for r in rr),
            "ged_non_uc":sum(bool(r.get("ged") and r["ged"].get("label")!="UC") for r in rr),
            "hard_vetoed":sum(bool(r["hard_vetoes"]) for r in rr),
        }

    return {"policies":results,"known_regressions":checks,"feature_summary_by_stream":by_stream}


def main():
    candidates,new_edits,alignments=build_runtime_candidates()
    # Runtime features are persisted first, without human labels.
    RUNTIME_FEATURES.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in candidates)+"\n",encoding="utf-8")
    NEW_EDITS.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in new_edits)+"\n",encoding="utf-8")

    eval_result=evaluate(candidates)
    result={
        "status":"PHASE2_INDEPENDENT_ACCEPTANCE_GATE_DEVELOPMENT",
        "runtime_candidates":len(candidates),
        "candidate_passages":len({r["passage_id"] for r in candidates}),
        "runtime_decisions_materialized_before_labels":True,
        "no_gold_runtime_features":True,
        "policy_evaluation":eval_result,
        "arabart_new_unadjudicated_edits":len(new_edits),
        "limitations":[
            "All policy quality numbers are retrospective on previously adjudicated development candidates.",
            "AraBART output is aligned locally and never accepted as a full rewritten sentence.",
            "The 79 candidate population is clustered within the same 41 Nahw development passages.",
            "No policy is frozen for sealed evaluation by this script.",
        ],
    }
    POLICY_RESULTS.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    summary={
        "status":"READY_FOR_ACCEPTANCE_GATE_REVIEW",
        "runtime_candidates":79,
        "surgical_candidates":sum(r["stream"]=="SURGICAL_NOPNX1" for r in candidates),
        "normalized_candidates":sum(r["stream"]=="NORMALIZED_FALLBACK" for r in candidates),
        "arabart_new_unadjudicated_edits":len(new_edits),
        "policy_results":eval_result["policies"],
        "known_regressions":eval_result["known_regressions"],
        "runtime_features_file":RUNTIME_FEATURES.name,
        "new_arabart_edit_queue":NEW_EDITS.name,
        "development_only":True,
        "not_sealed":True,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))


if __name__=="__main__":
    main()
