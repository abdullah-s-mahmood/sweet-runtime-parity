"""Phase 2 WAW_ALIF morphosyntactic recovery runtime on a fresh ZAEBUC TRAIN slice.

RAW only. Corrected text is not read here.
"""
from __future__ import annotations
import hashlib,json,re,subprocess
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

from phase2.acceptance.run_arabart_candidate_generator import generate_one
from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep, base

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.raw"
LIC=UP/"data/gec/ZAEBUC-v1.0/LICENCE.txt"
PREV=ROOT/"PHASE2_FINAL_ALIF_GENERALIZATION_RESULTS.json"
ART=ROOT/"artifacts"
EVENTS=ART/"WAW_ALIF_MORPH_RUNTIME_EVENTS.jsonl"
SUMMARY=ART/"WAW_ALIF_MORPH_RUNTIME_SUMMARY.json"

UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
SEED="phase2-waw-alif-morph-v1"
SLICE_N=60

NOMINAL_POS={"noun","noun_prop","noun_num","noun_quant","adj","adj_comp","adj_num"}

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def has_terminal_waw_token(line):
    for tok in line.split():
        b=base(tok)
        if b.endswith("و") and not b.endswith("وا"):
            return True
    return False

def choose(lines,excluded):
    scored=[]
    for i,s in enumerate(lines,1):
        if i in excluded: continue
        if not has_terminal_waw_token(s): continue
        scored.append((sha_text(SEED+"|"+s),i,s))
    scored.sort()
    return scored[:min(SLICE_N,len(scored))],len(scored)

def top_analysis(dw):
    if not dw or not getattr(dw,"analyses",None): return None
    return dw.analyses[0].analysis

def safe_top(a):
    if not a:return None
    return {k:a.get(k) for k in ("pos","num","per","asp","mod","cas","gen","vox","source","form_num","form_gen")}

def lexical_flags(analyzer,token):
    ans=analyzer.analyze(token)
    def anyf(pred): return any(pred(a) for a in ans)
    return {
        "analysis_count":len(ans),
        "has_plural_verb":anyf(lambda a:a.get("pos")=="verb" and a.get("num")=="p"),
        "has_singular_verb":anyf(lambda a:a.get("pos")=="verb" and a.get("num")=="s"),
        "has_nominal":anyf(lambda a:a.get("pos") in NOMINAL_POS),
        "pos_set":sorted({str(a.get("pos")) for a in ans}),
        "verb_num_set":sorted({str(a.get("num")) for a in ans if a.get("pos")=="verb"}),
    }

def candidate_license(a):
    if not a:return False
    if a.get("pos")!="verb" or a.get("num")!="p": return False
    if a.get("source") in {"backoff","foreign","digit","punct"}: return False
    asp=a.get("asp"); mod=a.get("mod")
    return asp in {"p","c"} or (asp=="i" and mod in {"s","j"})

def build_events(source,generated,trace,disambig,analyzer,line_id,line_hash):
    ops,total=align(source,generated)
    out_dis=disambig.disambiguate(generated.split())
    rows=[]
    for gi,g in enumerate(group_nonkeep(ops),1):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        kinds=[x["op"] for x in g]
        if srcs:
            lex=[x["lexical_index"] for x in srcs]
            lex_span=[min(lex),max(lex)+1]
        else:
            lex_span=[-1,-1]

        shape=False
        source_flags=None
        candidate_flags=None
        source_top=None
        candidate_top=None
        if len(g)==1 and kinds==["SUB"] and len(srcs)==1 and len(outs)==1:
            s=srcs[0]["base"]; o=outs[0]["base"]
            cost=float(g[0]["cost"])
            shape=(cost<=0.25 and s.endswith("و") and not s.endswith("وا") and o==s+"ا")
            if shape:
                swi=srcs[0]["whitespace_word_index"]
                owi=outs[0]["whitespace_word_index"]
                source_top=safe_top((trace["morphology"][swi] or {}).get("analysis") if swi < len(trace["morphology"]) else None)
                candidate_top=safe_top(top_analysis(out_dis[owi]) if owi < len(out_dis) else None)
                source_flags=lexical_flags(analyzer,s)
                candidate_flags=lexical_flags(analyzer,o)

        strict=False; recovery=False
        if shape and candidate_license(candidate_top) and candidate_flags and candidate_flags["has_plural_verb"]:
            if source_flags:
                strict=(
                    source_flags["has_plural_verb"]
                    and not source_flags["has_singular_verb"]
                    and not source_flags["has_nominal"]
                )
                recovery=(
                    not source_flags["has_singular_verb"]
                    and not source_flags["has_nominal"]
                )

        event={
            "event_id":f"ZWAW-{line_id:03d}-{gi:03d}",
            "line_id":line_id,
            "line_hash":line_hash,
            "source_lexical_span":lex_span,
            "event_type":kinds[0] if len(kinds)==1 else "COMPLEX",
            "primitive_ops":kinds,
            "event_cost":sum(float(x["cost"]) for x in g),
            "passage_alignment_cost":total,
            "source_bases":[x["base"] for x in srcs],
            "candidate_bases":[x["base"] for x in outs],
            "source_hash":sha_text("\u241f".join(x["base"] for x in srcs)),
            "candidate_hash":sha_text("\u241f".join(x["base"] for x in outs)),
            "source_contextual_top":source_top,
            "candidate_contextual_top":candidate_top,
            "source_lexical_flags":source_flags,
            "candidate_lexical_flags":candidate_flags,
            "features":{
                "waw_alif_shape":shape,
                "candidate_plural_verb_licensed":candidate_license(candidate_top) if shape else False,
                "strict_eligible":strict,
                "recovery_eligible":recovery,
            },
            "runtime_decisions":{
                "SOURCE_SHAPE_ONLY":"DIAGNOSTIC" if shape else "REVIEW",
                "WAW_ALIF_MORPH_RECOVERY":"DIAGNOSTIC" if recovery else "REVIEW",
                "WAW_ALIF_MORPH_STRICT":"ACCEPT" if strict else "REVIEW",
            }
        }
        rows.append(event)
    return rows

def main():
    ART.mkdir(exist_ok=True)
    commit=subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip()
    assert commit==UPSTREAM_COMMIT
    lines=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    prev=json.loads(PREV.read_text(encoding="utf-8"))
    excluded=set(int(x) for x in prev["selected_line_ids"])
    selected,eligible_count=choose(lines,excluded)
    assert selected, "No eligible raw-only lines"

    disambig=BERTUnfactoredDisambiguator.pretrained()
    analyzer=Analyzer(MorphologyDB.builtin_db("calima-msa-r13","a"),"NONE")
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    rows=[];changed=0
    for n,(h,line_id,source) in enumerate(selected,1):
        print(f"[WAW RAW {n}/{len(selected)}] line={line_id}",flush=True)
        generated,trace=generate_one(source,disambig,ged_tok,ged_model,gec_tok,gec_model)
        changed+=int(generated!=source)
        rows.extend(build_events(source,generated,trace,disambig,analyzer,line_id,h))

    EVENTS.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    def cnt(p,val):
        return sum(x["runtime_decisions"][p]==val for x in rows)
    summary={
        "status":"WAW_ALIF_MORPH_RUNTIME_COMPLETE",
        "development_generalization_only":True,
        "external_corpus":"ZAEBUC-v1.0 Arabic TRAIN fresh raw-selected slice",
        "external_license":"CC BY-NC-SA 4.0",
        "selection_seed":SEED,
        "eligible_raw_lines_after_exclusion":eligible_count,
        "selected_line_ids":[i for _,i,_ in selected],
        "selected_line_hashes":[h for h,_,_ in selected],
        "excluded_previous_line_ids":sorted(excluded),
        "selected_lines":len(selected),
        "changed_lines":changed,
        "runtime_events":len(rows),
        "shape_candidates":cnt("SOURCE_SHAPE_ONLY","DIAGNOSTIC"),
        "recovery_candidates":cnt("WAW_ALIF_MORPH_RECOVERY","DIAGNOSTIC"),
        "strict_accepts":cnt("WAW_ALIF_MORPH_STRICT","ACCEPT"),
        "gold_read_by_runtime":False,
        "zaebuc_dev_read":False,
        "zaebuc_test_read":False,
        "raw_sha256":sha_file(RAW),
        "license_sha256":sha_file(LIC),
        "upstream_commit":commit,
        "model_stack":{"ged":GED_MODEL,"gec":GEC_MODEL},
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="selected_line_hashes"},ensure_ascii=False))

if __name__=="__main__":
    main()
