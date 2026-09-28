"""Phase 2 — Reversible Normalized Candidate View.

Development-only candidate generator.

The original source is immutable. An internal model view removes only Unicode
combining marks (category Mn) and Arabic tatweel. Official pinned NoPnx1 runs
on that normalized view. Only source word locations previously suppressed by
TOKENIZER_UNK_WORD are inspected. Generated edits are REVIEW-ONLY candidates;
they are never applied to the original source in this script.

Outputs:
- artifacts/NORMALIZED_CANDIDATE_VIEW_RAW.json
- PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl
- PHASE2_NORMALIZED_CANDIDATE_QUEUE_SUMMARY.json
- PHASE2_NORMALIZED_CANDIDATE_MANIFEST.json
"""
from __future__ import annotations

import collections
import hashlib
import json
import platform
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import torch
import transformers

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
AR=ROOT/"phase2"/"arabic_eval"
ART=ROOT/"artifacts"
QUEUE=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl"
TARGET_ADJ=ROOT/"PHASE2_SURGICAL_TARGET_ADJUDICATION.jsonl"
DEV=AR/"DEVELOPMENT_TARGETS.jsonl"
SCI=AR/"SCIENTIFIC_STRESS_CASES.jsonl"
SCI_CORR=AR/"SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"

sys.path.insert(0,str(AR))
import prototype_surgical_renderer as surg

NOPNX_SHA="584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6"
UPSTREAM_SHA="4d552ca3ae98029550f27fc52aa1b22883e16e61"


def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def is_removed(ch):
    return ch=="\u0640" or unicodedata.category(ch)=="Mn"


def normalize_with_map(text):
    chars=[]
    norm_to_src=[]
    removed=[]
    src_boundary_to_norm=[0]*(len(text)+1)
    kept=0
    for i,ch in enumerate(text):
        src_boundary_to_norm[i]=kept
        if is_removed(ch):
            removed.append({
                "source_index":i,
                "char":ch,
                "unicode_name":unicodedata.name(ch,"UNKNOWN"),
            })
            continue
        chars.append(ch)
        norm_to_src.append(i)
        kept+=1
    src_boundary_to_norm[len(text)]=kept
    return {
        "normalized":"".join(chars),
        "norm_to_source":norm_to_src,
        "source_boundary_to_norm":src_boundary_to_norm,
        "removed":removed,
    }


def words_and_spans(text):
    ms=list(re.finditer(r"\S+",text))
    return [m.group(0) for m in ms],[(m.start(),m.end()) for m in ms]


def apply_edits_to_word(word,edits):
    out=word
    for e in sorted(edits,key=lambda x:int(x["source_local_span"][0]),reverse=True):
        a,b=map(int,e["source_local_span"])
        if out[a:b] != e["source_text"]:
            raise RuntimeError(f"normalized edit mapping drift: {out[a:b]!r} != {e['source_text']!r}")
        out=out[:a]+e["replacement"]+out[b:]
    return out


def word_normalization_map(source_word):
    chars=[]; local_map=[]; removed=[]
    for i,ch in enumerate(source_word):
        if is_removed(ch):
            removed.append({
                "source_local_index":i,
                "char":ch,
                "unicode_name":unicodedata.name(ch,"UNKNOWN"),
            })
            continue
        chars.append(ch);local_map.append(i)
    return "".join(chars),local_map,removed


def project_candidate_to_source_word(source_word,normalized_word,cand):
    norm_word,local_map,removed=word_normalization_map(source_word)
    if norm_word != normalized_word:
        return {
            "status":"UNSAFE_PROJECTABLE",
            "reason":"NORMALIZED_WORD_MISMATCH",
            "source_word":source_word,
            "normalized_word_expected":norm_word,
            "normalized_word_model":normalized_word,
        }
    a,b=map(int,cand["source_local_span"])
    if not (0 <= a <= b <= len(local_map)):
        return {"status":"UNSAFE_PROJECTABLE","reason":"NORMALIZED_SPAN_OUT_OF_RANGE"}
    if a==b:
        # No current SWEET surgical candidates are expected to use zero-width
        # source spans, but keep a conservative definition.
        if a==len(local_map):
            src_a=src_b=len(source_word)
        else:
            src_a=src_b=local_map[a]
    else:
        src_a=local_map[a]
        src_b=local_map[b-1]+1
    source_segment=source_word[src_a:src_b]
    seg_norm=normalize_with_map(source_segment)["normalized"]
    if seg_norm != cand["source_text"]:
        return {
            "status":"UNSAFE_PROJECTABLE",
            "reason":"SOURCE_SEGMENT_NORMALIZATION_MISMATCH",
            "source_local_span":[src_a,src_b],
            "source_segment":source_segment,
            "normalized_source_segment":seg_norm,
            "candidate_source_text":cand["source_text"],
        }
    removed_inside=[
        x for x in removed if src_a <= x["source_local_index"] < src_b
    ]
    # REVIEW_ONLY even when boundaries are identified. Removed marks inside the
    # projected span are explicitly surfaced because blindly replacing the span
    # could erase linguistically meaningful marks.
    return {
        "status":"SOURCE_SPAN_IDENTIFIED_REVIEW_ONLY",
        "reason":"EXACT_NORMALIZATION_ROUNDTRIP",
        "source_local_span":[src_a,src_b],
        "source_segment":source_segment,
        "removed_marks_inside_projected_span":removed_inside,
        "candidate_replacement_normalized":cand["replacement"],
        "auto_apply_allowed":False,
    }


def span_overlap(a,b,c,d):
    return a < d and b > c


def normalized_target_word_expected(row,source_word,word_span):
    wa,wb=word_span
    a,b=int(row["target_start"]),int(row["target_end"])
    if not span_overlap(wa,wb,a,b):
        return None
    local_a=max(a,wa)-wa
    local_b=min(b,wb)-wa
    # Only generate an exact expected word when the target is contained within
    # one whitespace word. Multi-word targets remain adjudication-only.
    if a < wa or b > wb:
        return {
            "status":"MULTIWORD_OR_PARTIAL_WORD_TARGET",
            "expected_normalized_word":None,
        }
    src_norm=normalize_with_map(source_word)
    na=src_norm["source_boundary_to_norm"][local_a]
    nb=src_norm["source_boundary_to_norm"][local_b]
    corr=normalize_with_map(row["target_correction"])["normalized"]
    expected=src_norm["normalized"][:na]+corr+src_norm["normalized"][nb:]
    return {
        "status":"SINGLE_WORD_EXPECTED_AVAILABLE",
        "expected_normalized_word":expected,
        "normalized_target_error":normalize_with_map(row["target_error"])["normalized"],
        "normalized_target_correction":corr,
        "normalized_local_span":[na,nb],
    }


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""): h.update(b)
    return h.hexdigest()


def main():
    ART.mkdir(parents=True,exist_ok=True)
    assert platform.python_version().startswith("3.10.")
    assert torch.__version__.startswith("1.12.1")
    assert transformers.__version__=="4.30.0"
    upstream=subprocess.check_output(["git","-C",str(ROOT/"upstream"/"text-editing"),"rev-parse","HEAD"],text=True).strip()
    assert upstream==UPSTREAM_SHA
    assert sha256_file(ROOT/"models"/"nopnx"/"pytorch_model.bin")==NOPNX_SHA

    dev=read_jsonl(DEV)
    queue=read_jsonl(QUEUE)
    target_adj=read_jsonl(TARGET_ADJ)
    assert len(dev)==150 and len({r["passage_id"] for r in dev})==41
    assert len(queue)==41
    assert len(target_adj)==150

    target_adj_map={x["case_id"]:x for x in target_adj}
    dev_by_pid=collections.defaultdict(list)
    for r in dev: dev_by_pid[int(r["passage_id"])].append(r)
    queue_by_pid={int(x["passage_id"]):x for x in queue}

    tok,model=surg.load_model("nopnx")
    models={"nopnx":(tok,model)}

    raw_passages={}
    candidate_queue=[]
    hazard_records=[]
    summary=collections.Counter()
    target_diag=[]

    for pid,item in sorted(queue_by_pid.items()):
        source=item["source"]
        src_words,src_word_spans=words_and_spans(source)
        hazards=[
            h for h in item["variants"]["nopnx1"]["suppressed_hazards"]
            if h.get("reason")=="TOKENIZER_UNK_WORD"
        ]
        hazard_word_indices=sorted({int(h["word_index"]) for h in hazards})
        summary["tokenizer_unk_hazards"]+=len(hazards)
        summary["unique_hazard_word_locations"]+=len(hazard_word_indices)

        nv=normalize_with_map(source)
        normalized_source=nv["normalized"]
        norm_words,norm_word_spans=words_and_spans(normalized_source)
        if len(norm_words)!=len(src_words):
            raise RuntimeError(f"word-count drift after normalization passage {pid}")

        # Official NoPnx1 on the normalized internal model view. Output itself is
        # diagnostic only; candidates are extracted from the surgical trace.
        normalized_output,trace=surg.run_variant(normalized_source,models,"nopnx1")
        all_candidates=trace[0].get("applied_edits",[])
        candidates_by_word=collections.defaultdict(list)
        for i,e in enumerate(all_candidates):
            ee={"normalized_candidate_index":i,**e}
            candidates_by_word[int(e["word_index"])].append(ee)

        passage_candidates=[]
        for wi in hazard_word_indices:
            source_word=src_words[wi]
            normalized_word=norm_words[wi]
            word_hazards=[h for h in hazards if int(h["word_index"])==wi]
            cands=candidates_by_word.get(wi,[])
            preview=apply_edits_to_word(normalized_word,cands) if cands else normalized_word

            target_rows=[
                r for r in dev_by_pid[pid]
                if span_overlap(src_word_spans[wi][0],src_word_spans[wi][1],int(r["target_start"]),int(r["target_end"]))
            ]
            target_context=[]
            for r in target_rows:
                expected=normalized_target_word_expected(r,source_word,src_word_spans[wi])
                prev=target_adj_map.get(r["case_id"],{})
                match=bool(expected and expected.get("expected_normalized_word") is not None and preview==expected["expected_normalized_word"])
                target_context.append({
                    "case_id":r["case_id"],
                    "target_id":r["target_id"],
                    "category_hint":r["category_hint"],
                    "target_error":r["target_error"],
                    "target_correction":r["target_correction"],
                    "published_reference":r["reference"],
                    "previous_surgical_classification":prev.get("classification"),
                    "expected_normalized":expected,
                    "automated_normalized_word_match":match,
                })
                summary["published_targets_overlapping_hazard_words"]+=1
                if match:
                    summary["automated_target_word_matches"]+=1
                    if prev.get("classification")=="ERROR_PRESERVED":
                        summary["automated_matches_on_previously_preserved_errors"]+=1

            hazard_rec={
                "passage_id":pid,
                "word_index":wi,
                "source_word":source_word,
                "normalized_word":normalized_word,
                "removed_chars":word_normalization_map(source_word)[2],
                "prior_hazards":word_hazards,
                "normalized_candidate_count":len(cands),
                "normalized_candidate_preview_word":preview,
                "targets":target_context,
            }
            hazard_records.append(hazard_rec)
            if cands:
                summary["hazard_word_locations_with_candidates"]+=1
            else:
                summary["hazard_word_locations_without_candidates"]+=1

            for ci,cand in enumerate(cands):
                projection=project_candidate_to_source_word(source_word,normalized_word,cand)
                result_word=apply_edits_to_word(normalized_word,[cand])
                overlaps_targets=[]
                for tc in target_context:
                    overlaps_targets.append({
                        "case_id":tc["case_id"],
                        "target_id":tc["target_id"],
                        "target_error":tc["target_error"],
                        "target_correction":tc["target_correction"],
                        "previous_surgical_classification":tc["previous_surgical_classification"],
                        "automated_full_word_match_after_all_candidates":tc["automated_normalized_word_match"],
                    })
                row={
                    "candidate_id":f"NORM-{pid}-{wi}-{ci}",
                    "passage_id":pid,
                    "word_index":wi,
                    "source_passage":source,
                    "source_word":source_word,
                    "normalized_model_view_word":normalized_word,
                    "removed_chars":word_normalization_map(source_word)[2],
                    "prior_tokenizer_unk_hazards":word_hazards,
                    "model":"CAMeL-Lab/text-editing-zaebuc-nopnx",
                    "stage":"NoPnx1",
                    "model_label":cand["label"],
                    "top1_confidence":cand["top1_confidence"],
                    "normalized_subword":cand["subword"],
                    "normalized_source_local_span":cand["source_local_span"],
                    "normalized_source_text":cand["source_text"],
                    "normalized_replacement":cand["replacement"],
                    "normalized_single_candidate_result_word":result_word,
                    "normalized_all_candidates_result_word":preview,
                    "projection":projection,
                    "overlapping_published_targets":overlaps_targets,
                    "runtime_policy":"REVIEW_ONLY_NEVER_AUTO_APPLY",
                    "adjudication_classes":[
                        "SUPPORTED_CORRECTION",
                        "SUPPORTED_ALTERNATIVE",
                        "PARTIAL_CORRECTION",
                        "UNNECESSARY_EDIT",
                        "WRONG_CORRECTION",
                        "REVIEW_REQUIRED"
                    ],
                }
                candidate_queue.append(row)
                passage_candidates.append(row)
                summary["normalized_candidates"]+=1
                if projection["status"]=="SOURCE_SPAN_IDENTIFIED_REVIEW_ONLY":
                    summary["source_spans_identified"]+=1
                else:
                    summary["unsafe_projection_candidates"]+=1

        raw_passages[str(pid)]={
            "source":source,
            "normalized_model_view":normalized_source,
            "removed_source_chars":nv["removed"],
            "normalized_full_nopnx1_output_diagnostic_only":normalized_output,
            "prior_unk_hazard_word_indices":hazard_word_indices,
            "normalized_candidates_at_hazard_words":passage_candidates,
            "normalized_stage_suppressed_hazards":trace[0].get("suppressed",[]),
        }

    # Deduplicate target diagnostic because a target can only overlap one word in
    # the current local-correction set in most cases, but preserve generality.
    seen=set()
    for h in hazard_records:
        for t in h["targets"]:
            key=t["case_id"]
            if key in seen: continue
            seen.add(key)
            target_diag.append({
                "case_id":t["case_id"],
                "target_id":t["target_id"],
                "passage_id":h["passage_id"],
                "word_index":h["word_index"],
                "source_word":h["source_word"],
                "normalized_candidate_preview_word":h["normalized_candidate_preview_word"],
                **t,
            })

    # Scientific authored stress probe: candidate generation only. Source output
    # is never modified and protected spans remain authoritative.
    sci=read_jsonl(SCI)
    corr=json.loads(SCI_CORR.read_text(encoding="utf-8")).get("corrections",{}) if SCI_CORR.exists() else {}
    sci_rows=[]
    sci_counts=collections.Counter()
    for r in sci:
        source=r["source"]
        protected=corr.get(r["case_id"],{}).get("effective_protected",r["protected"])
        nv=normalize_with_map(source)
        norm=nv["normalized"]
        out,trace=surg.run_variant(norm,models,"nopnx1")
        sci_counts["cases"]+=1
        sci_counts["original_source_unchanged_by_policy"]+=1
        sci_counts["protected_source_spans_intact_by_policy"]+=int(all(p in source for p in protected))
        sci_counts["normalized_view_candidates"]+=len(trace[0].get("applied_edits",[]))
        sci_rows.append({
            "case_id":r["case_id"],
            "source":source,
            "protected":protected,
            "normalized_model_view":norm,
            "normalized_output_diagnostic_only":out,
            "normalized_candidates":trace[0].get("applied_edits",[]),
            "delivered_source":source,
            "auto_apply":False,
        })

    summary_dict={
        "status":"READY_FOR_NORMALIZED_CANDIDATE_ADJUDICATION",
        "development_only":True,
        "not_sealed":True,
        "source_is_immutable":True,
        **dict(summary),
        "candidate_queue_rows":len(candidate_queue),
        "candidate_passages":len({x["passage_id"] for x in candidate_queue}),
        "scientific_stress":{
            "cases":sci_counts["cases"],
            "original_source_unchanged_by_policy":sci_counts["original_source_unchanged_by_policy"],
            "protected_source_spans_intact_by_policy":sci_counts["protected_source_spans_intact_by_policy"],
            "normalized_view_candidates":sci_counts["normalized_view_candidates"],
        },
        "normalization":"remove Unicode Mn combining marks and Arabic tatweel in internal model view only",
        "important_limitations":[
            "Automated target-word matching is diagnostic, not linguistic adjudication.",
            "Nahw references are localized corrections, not exhaustive passage gold.",
            "Normalized candidates are never auto-applied to original source.",
            "Removing diacritics can remove grammatically meaningful information; every normalized candidate requires adjudication.",
        ],
    }

    raw={
        "status":"PHASE2_REVERSIBLE_NORMALIZED_CANDIDATE_VIEW_DEVELOPMENT",
        "runtime":{
            "python":platform.python_version(),
            "torch":torch.__version__,
            "transformers":transformers.__version__,
            "nopnx_sha256":NOPNX_SHA,
            "upstream_commit":upstream,
        },
        "design":{
            "source_authority":"original source immutable",
            "normalization":"Mn + tatweel removal only",
            "scope":"previous TOKENIZER_UNK_WORD locations only",
            "candidate_policy":"REVIEW_ONLY_NEVER_AUTO_APPLY",
        },
        "summary":summary_dict,
        "hazard_records":hazard_records,
        "target_diagnostics":target_diag,
        "passages":raw_passages,
        "scientific_stress":sci_rows,
    }
    (ART/"NORMALIZED_CANDIDATE_VIEW_RAW.json").write_text(json.dumps(raw,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in candidate_queue)+"\n",encoding="utf-8")
    (ROOT/"PHASE2_NORMALIZED_CANDIDATE_QUEUE_SUMMARY.json").write_text(json.dumps(summary_dict,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    manifest={
        "repository":"abdullah-s-mahmood/sweet-runtime-parity",
        "branch":"phase2-arabic-eval",
        "phase":"Phase 2 — Reversible Normalized Candidate View",
        "source_targets":150,
        "source_passages":41,
        "normalization":"Mn combining marks + tatweel removed in internal model view only",
        "nopnx_sha256":NOPNX_SHA,
        "upstream_commit":upstream,
        "candidate_rows":len(candidate_queue),
        "queue_file":"PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl",
        "summary_file":"PHASE2_NORMALIZED_CANDIDATE_QUEUE_SUMMARY.json",
        "raw_artifact":"artifacts/NORMALIZED_CANDIDATE_VIEW_RAW.json",
        "auto_apply":False,
        "sealed":False,
    }
    (ROOT/"PHASE2_NORMALIZED_CANDIDATE_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print(json.dumps({"normalized_candidate_view_summary":summary_dict},ensure_ascii=False))


if __name__=="__main__":
    main()
