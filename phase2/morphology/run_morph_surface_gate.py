"""Phase 2 — Morphology-Aware Surface Realization Gate.

Development-only. Uses CAMeL Morph MSA + MLE morphology ranking to turn
adjudicated normalized candidates into source-preserving surface proposals.

Runtime policy never reads Nahw targets. Targets are joined only after
inference for evaluation. No proposal is written into the source corpus.

Outputs:
- PHASE2_MORPH_SURFACE_CANDIDATES.jsonl
- PHASE2_MORPH_SURFACE_GATE_RESULTS.json
- PHASE2_MORPH_SURFACE_TARGET_IMPACT.json
- PHASE2_MORPH_SURFACE_MANIFEST.json
"""
from __future__ import annotations

import collections
import difflib
import hashlib
import json
import platform
import re
import unicodedata
from pathlib import Path

import camel_tools
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB

ROOT=Path(__file__).resolve().parents[2]
ADJ=ROOT/"PHASE2_NORMALIZED_CANDIDATE_ADJUDICATION.jsonl"
QUEUE=ROOT/"PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl"
TARGETS=ROOT/"PHASE2_NORMALIZED_TARGET_IMPACT.json"
OUT_ROWS=ROOT/"PHASE2_MORPH_SURFACE_CANDIDATES.jsonl"
OUT_RESULTS=ROOT/"PHASE2_MORPH_SURFACE_GATE_RESULTS.json"
OUT_TARGETS=ROOT/"PHASE2_MORPH_SURFACE_TARGET_IMPACT.json"
OUT_MANIFEST=ROOT/"PHASE2_MORPH_SURFACE_MANIFEST.json"

ARABIC_MARK_CATEGORIES={"Mn"}
PUNCT_RE=re.compile(r"^([^\w\u0600-\u06FF]*)(.*?)([^\w\u0600-\u06FF]*)$",re.UNICODE)


def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()


def is_mark(ch):
    return ch=="\u0640" or unicodedata.category(ch) in ARABIC_MARK_CATEGORIES


def dediac_narrow(text):
    return "".join(ch for ch in text if not is_mark(ch))


def split_affixes(word):
    # Keep Arabic/Latin punctuation outside morphology core. Most data use only
    # trailing Arabic punctuation, but preserve both sides generically.
    start=0
    while start<len(word) and not (word[start].isalnum() or "\u0600"<=word[start]<="\u06FF"):
        start+=1
    end=len(word)
    while end>start and not (word[end-1].isalnum() or "\u0600"<=word[end-1]<="\u06FF" or is_mark(word[end-1])):
        end-=1
    return word[:start],word[start:end],word[end:]


def clusters(text):
    """Return [(base_char, marks_string)] excluding tatweel."""
    out=[]
    for ch in text:
        if ch=="\u0640":
            continue
        if unicodedata.category(ch)=="Mn":
            if out: out[-1]=(out[-1][0],out[-1][1]+ch)
            continue
        out.append((ch,""))
    return out


def mark_set(marks):
    return tuple(marks)


def base_string(text):
    return "".join(ch for ch,marks in clusters(text))


def align_source_to_candidate(source_core,candidate_core):
    s=[x[0] for x in clusters(source_core)]
    c=list(candidate_core)
    sm=difflib.SequenceMatcher(None,s,c,autojunk=False)
    src_to_cand={}
    cand_to_src={}
    changed_cand=set()
    changed_src=set()
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=="equal":
            for off in range(i2-i1):
                src_to_cand[i1+off]=j1+off
                cand_to_src[j1+off]=i1+off
        else:
            changed_src.update(range(i1,i2))
            changed_cand.update(range(j1,j2))
            # Include boundaries adjacent to changed regions because Arabic
            # case/mood marks often sit on the final unchanged base letter.
            if j1>0: changed_cand.add(j1-1)
            if j2<len(c): changed_cand.add(j2)
            if i1>0: changed_src.add(i1-1)
            if i2<len(s): changed_src.add(i2)
    return {
        "src_to_cand":src_to_cand,
        "cand_to_src":cand_to_src,
        "changed_cand":changed_cand,
        "changed_src":changed_src,
        "source_base":"".join(s),
        "candidate_base":"".join(c),
        "opcodes":[list(x) for x in sm.get_opcodes()],
    }


def analysis_to_minimal_surface(source_core,candidate_core,analysis_diac):
    ac=clusters(analysis_diac)
    if "".join(ch for ch,m in ac)!=candidate_core:
        return None
    sc=clusters(source_core)
    al=align_source_to_candidate(source_core,candidate_core)
    out=[]
    last_idx=len(ac)-1
    for ci,(ch,a_marks) in enumerate(ac):
        si=al["cand_to_src"].get(ci)
        if si is None:
            # Newly inserted/replaced base. Avoid importing full lexical
            # vocalization; keep only analyzer marks on the edited base.
            marks=a_marks
        else:
            s_marks=sc[si][1]
            in_neighborhood=(ci in al["changed_cand"] or si in al["changed_src"] or ci>=max(0,last_idx-1))
            if in_neighborhood:
                # Morphology may legitimately change case/mood/inflectional
                # marks near the edit. Use analyzer marks there.
                marks=a_marks
            else:
                # Preserve authoritative user/source marks elsewhere and do
                # not add analyzer vocalization to previously unmarked text.
                marks=s_marks
        out.append(ch+marks)
    return "".join(out)


def explicit_target_compatible(surface,target):
    """Allow source-preserved extra marks but require every target mark."""
    sp=[(c,m) for c,m in clusters(surface)]
    tp=[(c,m) for c,m in clusters(target)]
    if "".join(c for c,m in sp)!="".join(c for c,m in tp):
        return False
    if len(sp)!=len(tp): return False
    for (sc,sm),(tc,tm) in zip(sp,tp):
        if sc!=tc: return False
        for mark in tm:
            if mark not in sm:
                return False
    return True


def direct_patch(queue_row):
    proj=queue_row.get("projection",{})
    span=proj.get("source_local_span")
    if not span or proj.get("status")!="SOURCE_SPAN_IDENTIFIED_REVIEW_ONLY":
        return None
    removed=proj.get("removed_marks_inside_projected_span",[])
    if removed: return None
    src=queue_row["source_word"]
    repl=queue_row["normalized_replacement"]
    a,b=map(int,span)
    seg=src[a:b]
    if any(unicodedata.category(ch)=="Mn" for ch in seg):
        return None
    # Conservative local replacement: do not alter base length and do not
    # cross a combining-mark boundary immediately after the span.
    if len(clusters(seg))!=len(clusters(repl)):
        return None
    if a>0 and unicodedata.category(src[a-1])=="Mn":
        return None
    if b<len(src) and unicodedata.category(src[b])=="Mn":
        return None
    return src[:a]+repl+src[b:]


def compact_analysis(a):
    keys=["diac","lex","pos","cas","mod","stt","gen","num","per","asp","vox","form_gen","form_num"]
    return {k:a.get(k) for k in keys if k in a}



def contextual_tokens_with_candidate(passage, word_index, candidate_word, candidate_base):
    ws=passage.split()
    if not (0 <= int(word_index) < len(ws)):
        return None,None
    all_tokens=[]
    cand_index=None
    for wi,w in enumerate(ws):
        use=candidate_word if wi==int(word_index) else w
        toks=simple_word_tokenize(use)
        start=len(all_tokens)
        all_tokens.extend(toks)
        if wi==int(word_index):
            for ti,t in enumerate(toks):
                if dediac_narrow(t)==candidate_base:
                    cand_index=start+ti
                    break
            if cand_index is None:
                # Fallback to the first letter-bearing token in this whitespace word.
                for ti,t in enumerate(toks):
                    if any(unicodedata.category(ch).startswith("L") for ch in t):
                        cand_index=start+ti
                        break
    return all_tokens,cand_index


def scored_to_surface(scored,source_core,candidate_base,source_suffix):
    ana=scored.analysis
    diac=ana.get("diac",scored.diac)
    if dediac_narrow(diac)!=candidate_base:
        return None
    minsurf=analysis_to_minimal_surface(source_core,candidate_base,diac)
    if minsurf is None:
        return None
    return {
        "score":float(scored.score),
        "analysis":compact_analysis(ana),
        "full_diac_surface":diac,
        "minimal_source_preserving_surface":minsurf+source_suffix,
    }


def bert_consensus_surface(items,k=2):
    vals=[x["minimal_source_preserving_surface"] for x in items[:k] if x and "minimal_source_preserving_surface" in x]
    if not vals:
        return None
    return vals[0] if len(set(vals))==1 else None


def main():
    adj=read_jsonl(ADJ)
    queue=read_jsonl(QUEUE)
    target_doc=json.loads(TARGETS.read_text(encoding="utf-8"))
    assert len(adj)==19 and len(queue)==19
    qmap={x["candidate_id"]:x for x in queue}
    tmap={x["candidate_id"]:x for x in target_doc["targets"]}

    db=MorphologyDB.builtin_db("calima-msa-r13",flags="a")
    analyzer=Analyzer(db,backoff="ADD_PROP",cache_size=10000)
    mle=MLEDisambiguator.pretrained("calima-msa-r13",analyzer=analyzer,top=10,cache_size=10000)
    # Contextual morphology model. Its output is a ranking signal over CAMeL
    # analyses; it never edits source text directly.
    bert=BERTUnfactoredDisambiguator.pretrained(
        model_name="msa",top=10,use_gpu=False,batch_size=8,
        cache_size=10000,pretrained_cache=False,ranking_cache_size=10000
    )

    rows=[]
    runtime_auto=[]
    stats=collections.Counter()
    target_impacts=[]

    for arow in adj:
        cid=arow["candidate_id"]
        q=qmap[cid]
        source_word=arow["source_word"]
        _,source_core,source_suffix=split_affixes(source_word)
        _,cand_core,cand_suffix=split_affixes(arow["normalized_result_word"])
        candidate_base=dediac_narrow(cand_core)
        source_base=dediac_narrow(source_core)

        analyses_raw=analyzer.analyze(candidate_base)
        analyses=[]
        seen=set()
        for ana in analyses_raw:
            diac=ana.get("diac","")
            if dediac_narrow(diac)!=candidate_base:
                continue
            key=(diac,ana.get("pos"),ana.get("cas"),ana.get("mod"),ana.get("stt"),ana.get("lex"))
            if key in seen: continue
            seen.add(key)
            minsurf=analysis_to_minimal_surface(source_core,candidate_base,diac)
            if minsurf is None: continue
            analyses.append({
                "analysis":compact_analysis(ana),
                "full_diac_surface":diac,
                "minimal_source_preserving_surface":minsurf+source_suffix,
            })

        # MLE is explicitly an out-of-context morphology prior.
        mle_analyses=[]
        try:
            d=mle.disambiguate([candidate_base])[0]
            for scored in d.analyses[:10]:
                ana=scored.analysis
                diac=ana.get("diac",scored.diac)
                if dediac_narrow(diac)!=candidate_base:
                    continue
                minsurf=analysis_to_minimal_surface(source_core,candidate_base,diac)
                if minsurf is None: continue
                mle_analyses.append({
                    "score":float(scored.score),
                    "analysis":compact_analysis(ana),
                    "full_diac_surface":diac,
                    "minimal_source_preserving_surface":minsurf+source_suffix,
                })
        except Exception as exc:
            mle_analyses=[{"error":f"{type(exc).__name__}: {exc}"}]

        unique_all=sorted({x["minimal_source_preserving_surface"] for x in analyses})
        unique_mle=sorted({x["minimal_source_preserving_surface"] for x in mle_analyses if "minimal_source_preserving_surface" in x})
        top1=(mle_analyses[0]["minimal_source_preserving_surface"] if mle_analyses and "minimal_source_preserving_surface" in mle_analyses[0] else None)

        # Contextual BERT morphology: replace only the candidate whitespace word
        # in a tokenized copy of the passage. Gold targets are not consulted.
        bert_analyses=[]
        bert_error=None
        try:
            toks,cidx=contextual_tokens_with_candidate(
                arow["source_passage"],arow.get("word_index",q.get("word_index")),
                arow["normalized_result_word"],candidate_base
            )
            if toks is None or cidx is None:
                raise RuntimeError("candidate token could not be mapped into contextual tokenization")
            dw=bert.disambiguate(toks)[cidx]
            for scored in dw.analyses[:10]:
                item=scored_to_surface(scored,source_core,candidate_base,source_suffix)
                if item is not None:
                    bert_analyses.append(item)
        except Exception as exc:
            bert_error=f"{type(exc).__name__}: {exc}"

        unique_bert=sorted({x["minimal_source_preserving_surface"] for x in bert_analyses})
        bert_top1=bert_analyses[0]["minimal_source_preserving_surface"] if bert_analyses else None
        bert_top2_consensus=bert_consensus_surface(bert_analyses,2)

        direct=direct_patch(q)
        runtime_decision="ABSTAIN"
        runtime_surface=None
        runtime_reason="AMBIGUOUS_OR_NO_MORPHOLOGY_CONSENSUS"

        # This gate isolates SURFACE REALIZATION. Candidate linguistic support
        # was established in the previous adjudication and is used only to bound
        # this development experiment. Production needs an independent verifier.
        supported_class=arow["candidate_class"] in {"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}

        if supported_class and direct is not None and arow.get("surface_realization_class")=="BASE_LETTER_PLUS_PRESERVE_EXISTING_DIACRITICS":
            runtime_decision="DEVELOPMENT_AUTO_DIRECT_PATCH"
            runtime_surface=direct
            runtime_reason="PRIOR_SAFE_SURFACE_CLASS_AND_LOCAL_PATCH_NO_DIACRITIC_BOUNDARY_CROSSING"
        elif supported_class and bert_top2_consensus is not None and bert_top2_consensus in unique_all:
            runtime_decision="DEVELOPMENT_CONTEXTUAL_MORPH_CONSENSUS"
            runtime_surface=bert_top2_consensus
            runtime_reason="BERT_TOP2_CONTEXTUAL_ANALYSES_AGREE_AND_SURFACE_EXISTS_IN_MORPH_LATTICE"
        elif supported_class and bert_top1 is not None:
            runtime_decision="REVIEW_CONTEXTUAL_MORPH_TOP1"
            runtime_surface=bert_top1
            runtime_reason="BERT_CONTEXTUAL_TOP1_AVAILABLE_BUT_NO_TOP2_SURFACE_CONSENSUS"
        elif supported_class and top1 is not None:
            runtime_decision="REVIEW_MLE_TOP1"
            runtime_surface=top1
            runtime_reason="ONLY_OUT_OF_CONTEXT_MLE_SURFACE_AVAILABLE"
        else:
            runtime_decision="REVIEW_OR_ABSTAIN"
            runtime_reason="MORPHOLOGICAL_SURFACE_AMBIGUITY_OR_UNSUPPORTED_CANDIDATE"

        target=tmap.get(cid)
        target_eval=None
        if target:
            published=target["published_correction"]
            target_eval={
                "target_id":target["target_id"],
                "published_correction":published,
                "runtime_surface_compatible":bool(runtime_surface and explicit_target_compatible(runtime_surface,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)),
                "mle_top1_compatible":bool(top1 and explicit_target_compatible(top1,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)),
                "bert_top1_compatible":bool(bert_top1 and explicit_target_compatible(bert_top1,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)),
                "bert_top2_consensus_compatible":bool(bert_top2_consensus and explicit_target_compatible(bert_top2_consensus,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)),
                "any_morph_surface_compatible":any(
                    explicit_target_compatible(s,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)
                    for s in unique_all
                ),
                "compatible_morph_surface_count":sum(
                    explicit_target_compatible(s,published+source_suffix if source_suffix and not published.endswith(source_suffix) else published)
                    for s in unique_all
                ),
                "previous_target_impact":target["target_impact"],
            }
            target_impacts.append({"candidate_id":cid,**target_eval})

        if runtime_decision.startswith("DEVELOPMENT_AUTO") or runtime_decision=="DEVELOPMENT_CONTEXTUAL_MORPH_CONSENSUS":
            runtime_auto.append({
                "candidate_id":cid,
                "source_word":source_word,
                "surface":runtime_surface,
                "candidate_class":arow["candidate_class"],
                "target_eval":target_eval,
            })

        stats["candidates"]+=1
        stats[f"class_{arow['candidate_class']}"]+=1
        stats[f"decision_{runtime_decision}"]+=1
        stats["morph_analyzable"]+=int(bool(analyses))
        stats["morph_ambiguous_multiple_surfaces"]+=int(len(unique_all)>1)
        stats["morph_unique_surface"]+=int(len(unique_all)==1)
        if target_eval:
            stats["targets_touched"]+=1
            stats["target_any_morph_compatible"]+=int(target_eval["any_morph_surface_compatible"])
            stats["target_mle_top1_compatible"]+=int(target_eval["mle_top1_compatible"])
            stats["target_bert_top1_compatible"]+=int(target_eval["bert_top1_compatible"])
            stats["target_bert_top2_consensus_compatible"]+=int(target_eval["bert_top2_consensus_compatible"])
            stats["target_runtime_surface_compatible"]+=int(target_eval["runtime_surface_compatible"])

        rows.append({
            "candidate_id":cid,
            "passage_id":arow["passage_id"],
            "source_passage":arow["source_passage"],
            "source_word":source_word,
            "candidate_class":arow["candidate_class"],
            "surface_realization_class":arow.get("surface_realization_class"),
            "normalized_result_word":arow["normalized_result_word"],
            "candidate_base":candidate_base,
            "source_base":source_base,
            "source_suffix":source_suffix,
            "direct_patch":direct,
            "morph_analysis_count":len(analyses),
            "unique_minimal_surface_count":len(unique_all),
            "unique_minimal_surfaces":unique_all,
            "mle_top_analyses":mle_analyses,
            "mle_unique_minimal_surfaces":unique_mle,
            "bert_context_analyses":bert_analyses,
            "bert_context_error":bert_error,
            "bert_unique_minimal_surfaces":unique_bert,
            "bert_top1_surface":bert_top1,
            "bert_top2_surface_consensus":bert_top2_consensus,
            "runtime_decision":runtime_decision,
            "runtime_surface_proposal":runtime_surface,
            "runtime_reason":runtime_reason,
            "target_evaluation":target_eval,
            "all_morph_analyses":analyses[:200],
        })

    # Development safety evaluation is allowed only after the runtime decision.
    auto_supported=sum(x["candidate_class"] in {"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"} for x in runtime_auto)
    auto_partial=sum(x["candidate_class"]=="PARTIAL_CORRECTION" for x in runtime_auto)
    auto_wrong=sum(x["candidate_class"]=="WRONG_CORRECTION" for x in runtime_auto)
    auto_unnecessary=sum(x["candidate_class"]=="UNNECESSARY_EDIT" for x in runtime_auto)
    auto_target_correct=sum(bool(x["target_eval"] and x["target_eval"]["runtime_surface_compatible"]) for x in runtime_auto)

    result={
        "status":"PHASE2_MORPH_SURFACE_GATE_V2_DEVELOPMENT",
        "gate_version":2,
        "not_sealed":True,
        "no_source_corpus_modified":True,
        "runtime_policy_uses_nahw_gold":False,
        "camel_tools_version":getattr(camel_tools,"__version__","unknown"),
        "morphology_database":"calima-msa-r13",
        "ranking_prior":{
            "mle":"CAMeL MLE MSA (word-based/out-of-context)",
            "contextual":"CAMeL BERTUnfactoredDisambiguator MSA",
            "important_limit":"Contextual morphology ranks analyses; it is not a grammatical-correction verifier and never edits source directly.",
        },
        "source_preservation_policy":{
            "broad_normalization":False,
            "unaffected_source_marks_preserved":True,
            "edit_neighborhood_marks_from_morphology":True,
            "ambiguity":"abstain or review",
        },
        "summary":dict(stats),
        "runtime_auto_candidates":{
            "count":len(runtime_auto),
            "supported_or_alternative":auto_supported,
            "partial":auto_partial,
            "wrong":auto_wrong,
            "unnecessary":auto_unnecessary,
            "target_compatible":auto_target_correct,
            "rows":runtime_auto,
        },
        "rows":rows,
        "limitations":[
            "The MLE disambiguator is out-of-context; contextual BERT is evaluated separately.",
            "BERT top analysis is a morphosyntactic ranking signal, not proof that a correction candidate is linguistically correct.",
            "Human candidate class is used only to bound development realization and evaluate safety, not to claim a deployable verifier.",
            "Nahw target corrections are joined only after runtime proposals for evaluation.",
            "CAMeL Analyzer default normalization is countered by exact narrow-base filtering, but morphology analyses are not syntactic proof.",
        ],
    }

    OUT_ROWS.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    OUT_RESULTS.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    target_out={
        "status":"DEVELOPMENT_MORPH_SURFACE_TARGET_EVALUATION",
        "targets_touched":len(target_impacts),
        "any_morph_surface_compatible":sum(x["any_morph_surface_compatible"] for x in target_impacts),
        "mle_top1_compatible":sum(x["mle_top1_compatible"] for x in target_impacts),
        "bert_top1_compatible":sum(x["bert_top1_compatible"] for x in target_impacts),
        "bert_top2_consensus_compatible":sum(x["bert_top2_consensus_compatible"] for x in target_impacts),
        "runtime_surface_compatible":sum(x["runtime_surface_compatible"] for x in target_impacts),
        "targets":target_impacts,
    }
    OUT_TARGETS.write_text(json.dumps(target_out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    manifest={
        "repository":"abdullah-s-mahmood/sweet-runtime-parity",
        "branch":"phase2-arabic-eval",
        "phase":"Phase 2 — Morphology-Aware Surface Realization Gate",
        "input_candidates":19,
        "input_adjudication_sha256":sha256(ADJ),
        "input_queue_sha256":sha256(QUEUE),
        "input_target_impact_sha256":sha256(TARGETS),
        "camel_tools_version":getattr(camel_tools,"__version__","unknown"),
        "morphology_database":"calima-msa-r13",
        "outputs":[OUT_ROWS.name,OUT_RESULTS.name,OUT_TARGETS.name],
        "sealed":False,
        "source_applied":False,
    }
    OUT_MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    compact={
        "status":result["status"],
        "summary":result["summary"],
        "runtime_auto_candidates":result["runtime_auto_candidates"],
        "target_evaluation":{k:v for k,v in target_out.items() if k!="targets"},
    }
    print(json.dumps(compact,ensure_ascii=False))


if __name__=="__main__":
    main()