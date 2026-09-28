"""Phase 2 development-only Selective Surgical Gate.

Fixed runtime-observable policy selected before this run:
- non-space INSERT: allow
- REPLACE with top-1 confidence >= 0.80: allow
- DELETE: abstain
- other operations: abstain

A public ZAEBUC CAMeLBERT GED-13 model is tested as an optional localization
gate. Nahw gold spans are used only after inference for development evaluation.
This is NOT a sealed evaluation and does not freeze thresholds.
"""
from __future__ import annotations

import collections
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, BertForTokenClassification

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
AR=ROOT/"phase2"/"arabic_eval"
ART=ROOT/"artifacts"
sys.path.insert(0,str(AR))
import prototype_surgical_renderer as surg

DEV=AR/"DEVELOPMENT_TARGETS.jsonl"
SCI=AR/"SCIENTIFIC_STRESS_CASES.jsonl"
SCI_CORR=AR/"SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"
GED_DIR=ROOT/"models"/"ged_zaebuc"


def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def operation_family(label):
    if "I_[" in label: return "INSERT"
    if "R_[" in label: return "REPLACE"
    if "D" in label: return "DELETE"
    if "A_[" in label: return "APPEND"
    return "OTHER"


def insertion_payload(label):
    m=re.search(r"I_\[([^\]]*)\]",label)
    return m.group(1) if m else ""


def operation_policy(edit):
    fam=operation_family(edit["label"])
    conf=float(edit["top1_confidence"])
    if fam=="INSERT":
        if insertion_payload(edit["label"]).strip()=="":
            return False,"ABSTAIN_INSERT_WHITESPACE"
        return True,"ALLOW_NONSPACE_INSERT"
    if fam=="REPLACE":
        return (True,"ALLOW_REPLACE_CONF_GE_0_80") if conf>=0.80 else (False,"ABSTAIN_REPLACE_CONF_LT_0_80")
    if fam=="DELETE":
        return False,"ABSTAIN_DELETE"
    return False,f"ABSTAIN_{fam}"


def whitespace_words(text):
    ms=list(re.finditer(r"\S+",text))
    return [m.group(0) for m in ms],[(m.start(),m.end()) for m in ms]


def apply_selected_edits(source,candidate_edits,selector):
    words,spans=whitespace_words(source)
    per_word=collections.defaultdict(list)
    abstained=[]
    for idx,e in enumerate(candidate_edits):
        ok,reason=selector(e)
        item={"candidate_edit_index":idx,**e,"gate_reason":reason}
        if ok: per_word[int(e["word_index"])].append(item)
        else: abstained.append(item)

    selected=[]
    word_replacements={}
    for wi,edits in per_word.items():
        original=words[wi]
        intervals=sorted((int(e["source_local_span"][0]),int(e["source_local_span"][1]),e) for e in edits)
        if any(intervals[i][0] < intervals[i-1][1] for i in range(1,len(intervals))):
            for _,_,e in intervals:
                abstained.append({**e,"gate_reason":"ABSTAIN_SELECTED_EDIT_OVERLAP"})
            continue
        new=original
        failed=False
        for a,b,e in sorted(intervals,key=lambda z:z[0],reverse=True):
            if original[a:b] != e["source_text"]:
                failed=True
                break
            new=new[:a]+e["replacement"]+new[b:]
        if failed:
            for _,_,e in intervals:
                abstained.append({**e,"gate_reason":"ABSTAIN_ROUNDTRIP_MISMATCH"})
            continue
        if new!=original:
            word_replacements[wi]=new
            selected.extend(e for _,_,e in intervals)

    output=source
    for wi in sorted(word_replacements,reverse=True):
        a,b=spans[wi]
        output=output[:a]+word_replacements[wi]+output[b:]
    return output,selected,abstained


def load_ged():
    tok=AutoTokenizer.from_pretrained(str(GED_DIR),local_files_only=True,use_fast=True)
    if not getattr(tok,"is_fast",False):
        raise RuntimeError("GED fast tokenizer required for source offsets")
    model=BertForTokenClassification.from_pretrained(str(GED_DIR),local_files_only=True).eval().cpu()
    if "UC" not in model.config.label2id:
        raise RuntimeError("GED model missing UC label")
    return tok,model


def ged_word_scores(text,tok,model):
    words,spans=whitespace_words(text)
    enc=tok(text,return_tensors="pt",return_offsets_mapping=True,truncation=True,max_length=512)
    offsets=enc.pop("offset_mapping")[0].tolist()
    with torch.no_grad():
        probs=torch.softmax(model(**enc).logits[0],dim=-1)
    uc_id=int(model.config.label2id["UC"])
    top=probs.argmax(-1).tolist()
    out=[{
        "word_index":i,"word":w,"span":list(spans[i]),
        "ged_error_probability":0.0,"ged_top_label":"UC",
        "ged_top_label_probability":1.0,"covered_subtokens":0
    } for i,w in enumerate(words)]
    for ti,(a,b) in enumerate(offsets):
        if a==b: continue
        wi=next((j for j,(wa,wb) in enumerate(spans) if a<wb and b>wa),None)
        if wi is None: continue
        p_error=float(1.0-probs[ti,uc_id].item())
        top_id=int(top[ti])
        out[wi]["covered_subtokens"]+=1
        if p_error>out[wi]["ged_error_probability"]:
            out[wi]["ged_error_probability"]=p_error
            out[wi]["ged_top_label"]=model.config.id2label[top_id]
            out[wi]["ged_top_label_probability"]=float(probs[ti,top_id].item())
    return out


def selector_with_ged(ged_by_word,mode,threshold=None):
    def sel(edit):
        ok,reason=operation_policy(edit)
        if not ok: return False,reason
        g=ged_by_word[int(edit["word_index"])]
        if mode=="top_non_uc":
            return (True,reason+"+GED_NON_UC") if g["ged_top_label"]!="UC" else (False,"ABSTAIN_GED_UC")
        if mode=="prob":
            return (True,reason+f"+GED_ERRPROB_GE_{threshold:.2f}") if g["ged_error_probability"]>=threshold else (False,f"ABSTAIN_GED_ERRPROB_LT_{threshold:.2f}")
        raise ValueError(mode)
    return sel


def target_word_index(row):
    _,spans=whitespace_words(row["source"])
    a,b=int(row["target_start"]),int(row["target_end"])
    return next((i for i,(wa,wb) in enumerate(spans) if a<wb and b>wa),None)


def summarize_variant(name,outputs,dev):
    exact=sum(int(surg.target_recovered(r,outputs[r["passage_id"]])) for r in dev)
    passages={r["passage_id"]:r["source"] for r in dev}
    changed=sum(outputs[pid]!=src for pid,src in passages.items())
    return {"name":name,"exact_target_recoveries":exact,"exact_target_recovery_rate":exact/len(dev),"changed_passages":changed}


def main():
    ART.mkdir(parents=True,exist_ok=True)
    upstream=subprocess.check_output(["git","-C",str(ROOT/"upstream"/"text-editing"),"rev-parse","HEAD"],text=True).strip()
    if upstream!="4d552ca3ae98029550f27fc52aa1b22883e16e61": raise RuntimeError(upstream)
    if not platform.python_version().startswith("3.10."): raise RuntimeError(platform.python_version())
    if not torch.__version__.startswith("1.12.1"): raise RuntimeError(torch.__version__)
    if transformers.__version__!="4.30.0": raise RuntimeError(transformers.__version__)

    nopnx=surg.load_model("nopnx")
    models={"nopnx":nopnx}
    ged_tok,ged_model=load_ged()
    dev=read_jsonl(DEV)
    sci=read_jsonl(SCI)
    assert len(dev)==150 and len({r["passage_id"] for r in dev})==41

    corrections={}
    if SCI_CORR.exists():
        corrections=json.loads(SCI_CORR.read_text(encoding="utf-8")).get("corrections",{})

    passages={}
    for r in dev: passages.setdefault(r["passage_id"],r["source"])
    variant_names=["op_aware","op_aware_ged_non_uc","op_aware_ged_p30","op_aware_ged_p50","op_aware_ged_p70"]
    variants={n:{} for n in variant_names}
    raw_passages={}

    for pid,source in passages.items():
        baseline_out,trace=surg.run_variant(source,models,"nopnx1")
        stage=trace[0]
        candidates=stage.get("applied_edits",[])
        ged=ged_word_scores(source,ged_tok,ged_model)
        ged_by_word={int(x["word_index"]):x for x in ged}

        selectors={
            "op_aware":operation_policy,
            "op_aware_ged_non_uc":selector_with_ged(ged_by_word,"top_non_uc"),
            "op_aware_ged_p30":selector_with_ged(ged_by_word,"prob",0.30),
            "op_aware_ged_p50":selector_with_ged(ged_by_word,"prob",0.50),
            "op_aware_ged_p70":selector_with_ged(ged_by_word,"prob",0.70),
        }
        metas={}
        for name,selector in selectors.items():
            out,selected,abstained=apply_selected_edits(source,candidates,selector)
            variants[name][pid]=out
            metas[name]={
                "selected_indices":[int(e["candidate_edit_index"]) for e in selected],
                "abstained_indices":[int(e["candidate_edit_index"]) for e in abstained],
            }

        enriched=[]
        for ei,e in enumerate(candidates):
            wi=int(e["word_index"])
            enriched.append({
                "edit_index":ei,**e,
                "operation_family":operation_family(e["label"]),
                "operation_policy_allow":operation_policy(e)[0],
                "operation_policy_reason":operation_policy(e)[1],
                "ged":ged_by_word[wi],
                "ged_gate_membership":{n:ei in metas[n]["selected_indices"] for n in metas if n!="op_aware"}
            })
        raw_passages[str(pid)]={
            "source":source,
            "baseline_surgical_output":baseline_out,
            "baseline_candidate_edits":enriched,
            "baseline_suppressed_hazards":stage.get("suppressed",[]),
            "operation_aware_output":variants["op_aware"][pid],
            "operation_aware_selected_indices":metas["op_aware"]["selected_indices"],
            "operation_aware_abstained_indices":metas["op_aware"]["abstained_indices"],
            "gate_outputs":{n:variants[n][pid] for n in variant_names if n!="op_aware"},
            "ged_words":ged,
        }

    summaries={n:summarize_variant(n,o,dev) for n,o in variants.items()}

    target_ged=[]
    for row in dev:
        pid=row["passage_id"]; wi=target_word_index(row)
        if wi is None:
            target_ged.append({"case_id":row["case_id"],"target_id":row["target_id"],"passage_id":pid,"word_index":None,"mapping_status":"NO_WORD_MAPPING"})
            continue
        g=raw_passages[str(pid)]["ged_words"][wi]
        target_ged.append({
            "case_id":row["case_id"],"target_id":row["target_id"],"passage_id":pid,"word_index":wi,
            "target_error":row["target_error"],"ged_top_label":g["ged_top_label"],
            "ged_error_probability":g["ged_error_probability"],
            "detected_top_non_uc":g["ged_top_label"]!="UC",
            "detected_p30":g["ged_error_probability"]>=0.30,
            "detected_p50":g["ged_error_probability"]>=0.50,
            "detected_p70":g["ged_error_probability"]>=0.70,
        })
    mapped=[x for x in target_ged if x.get("word_index") is not None]
    ged_recall={}
    for key in ("detected_top_non_uc","detected_p30","detected_p50","detected_p70"):
        det=sum(bool(x[key]) for x in mapped)
        ged_recall[key]={"detected":det,"mapped_targets":len(mapped),"published_target_recall":det/len(mapped)}

    sci_summary=collections.defaultdict(lambda:{"cases":0,"protected_exact":0,"source_exact_unchanged":0,"unk_outputs":0})
    sci_results=[]
    for row in sci:
        protected=corrections.get(row["case_id"],{}).get("effective_protected",row["protected"])
        source=row["source"]
        _,trace=surg.run_variant(source,models,"nopnx1",protected=protected)
        candidates=trace[0].get("applied_edits",[])
        ged=ged_word_scores(source,ged_tok,ged_model); gb={int(x["word_index"]):x for x in ged}
        sels={
            "op_aware":operation_policy,
            "op_aware_ged_non_uc":selector_with_ged(gb,"top_non_uc"),
            "op_aware_ged_p50":selector_with_ged(gb,"prob",0.50),
        }
        vr={}
        for name,selector in sels.items():
            out,selected,abstained=apply_selected_edits(source,candidates,selector)
            vr[name]={
                "output":out,"selected_edits":selected,"abstained_edits":abstained,
                "protected_exact":all(p in out for p in protected),
                "source_exact_unchanged":out==source,"contains_UNK":"[UNK]" in out
            }
            z=sci_summary[name];z["cases"]+=1;z["protected_exact"]+=int(vr[name]["protected_exact"]);z["source_exact_unchanged"]+=int(vr[name]["source_exact_unchanged"]);z["unk_outputs"]+=int(vr[name]["contains_UNK"])
        sci_results.append({"case_id":row["case_id"],"category":row["category"],"protected":protected,"variants":vr})

    result={
        "status":"PHASE2_SELECTIVE_SURGICAL_GATE_DEVELOPMENT",
        "not_sealed":True,
        "policy_origin":"Operation-aware rule fixed before this run from prior development adjudication; not a production threshold.",
        "runtime":{"python":platform.python_version(),"torch":torch.__version__,"transformers":transformers.__version__,"upstream_commit":upstream},
        "operation_policy":{"INSERT":"allow non-whitespace only","REPLACE":"allow iff top1>=0.80","DELETE":"abstain","OTHER":"abstain"},
        "variant_summaries":summaries,
        "ged_published_target_localization":{"warning":"Recall only; non-target GED predictions are not labeled false positives.","summary":ged_recall,"targets":target_ged},
        "scientific_stress_summary":dict(sci_summary),
        "scientific_cases":sci_results,
        "passages":raw_passages,
        "limitations":[
            "Same development passages used to choose the operation-aware rule; not an independent precision estimate.",
            "ZAEBUC GED feasibility uses raw source text, not the full contextual-morphological preprocessing from the 2023 paper.",
            "Automated exact target recovery is diagnostic and can contain alignment false positives.",
        ],
    }
    p=ART/"SELECTIVE_SURGICAL_GATE_RAW.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"variant_summaries":summaries,"ged_target_recall":ged_recall,"scientific_stress_summary":dict(sci_summary),"output":str(p)},ensure_ascii=False))


if __name__=="__main__":
    main()
