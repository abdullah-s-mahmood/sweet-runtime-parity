"""Phase 2 development-only Selective Surgical Gate.

Uses runtime-observable features only. Nahw targets are evaluation-only.
Primary policy:
  non-space INSERT -> allow
  REPLACE with top1 confidence >= 0.80 -> allow
  DELETE/other -> abstain

Secondary variants additionally require an independently predicted Arabic GED
non-UC signal. No threshold is frozen and no sealed data are used.
"""
from __future__ import annotations
import collections, json, platform, re, subprocess, sys
from pathlib import Path
import torch, transformers

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
AR=ROOT/"phase2"/"arabic_eval"
ART=ROOT/"artifacts"
sys.path.insert(0,str(AR))
import prototype_surgical_renderer as surg

DEV=AR/"DEVELOPMENT_TARGETS.jsonl"
SCI=AR/"SCIENTIFIC_STRESS_CASES.jsonl"
SCI_CORR=AR/"SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def op_family(label):
    if "I_[" in label: return "INSERT"
    if "R_[" in label: return "REPLACE"
    if "D" in label: return "DELETE"
    if "A_[" in label: return "APPEND"
    return "OTHER"


def insert_payload(label):
    m=re.search(r"I_\[([^\]]*)\]",label)
    return m.group(1) if m else ""


def base_allow(e):
    fam=op_family(e["label"])
    conf=float(e["top1_confidence"])
    if fam=="INSERT":
        return (insert_payload(e["label"]).strip()!="","ALLOW_NONSPACE_INSERT")
    if fam=="REPLACE":
        return (conf>=0.80,"ALLOW_REPLACE_GE_0_80" if conf>=0.80 else "ABSTAIN_REPLACE_LT_0_80")
    if fam=="DELETE": return (False,"ABSTAIN_DELETE")
    return (False,f"ABSTAIN_{fam}")


def words_and_spans(text):
    ms=list(re.finditer(r"\S+",text))
    return [m.group(0) for m in ms],[(m.start(),m.end()) for m in ms]


def apply_subset(source,candidates,allow_indices):
    words,spans=words_and_spans(source)
    byword=collections.defaultdict(list)
    for i,e in enumerate(candidates):
        if i in allow_indices:
            byword[int(e["word_index"])].append((i,e))
    applied=[]; abstained=[]
    replacements={}
    for wi,items in byword.items():
        ints=sorted((int(e["source_local_span"][0]),int(e["source_local_span"][1]),i,e) for i,e in items)
        if any(ints[k][0] < ints[k-1][1] for k in range(1,len(ints))):
            abstained += [{"edit_index":i,"reason":"OVERLAP"} for _,_,i,_ in ints]
            continue
        original=words[wi]; new=original; ok=True
        for a,b,i,e in sorted(ints,reverse=True):
            if new[a:b] != e["source_text"]:
                ok=False; break
            new=new[:a]+e["replacement"]+new[b:]
        if not ok:
            abstained += [{"edit_index":i,"reason":"ROUNDTRIP_MISMATCH"} for _,_,i,_ in ints]
            continue
        if new!=original:
            replacements[wi]=new
            applied += [i for _,_,i,_ in ints]
    out=source
    for wi in sorted(replacements,reverse=True):
        a,b=spans[wi]; out=out[:a]+replacements[wi]+out[b:]
    return out,sorted(applied),abstained


def ged_lookup(ged_artifact,model,pid):
    preds=ged_artifact["passages"][str(pid)]["models"][model]
    return {int(x["word_index"]):x for x in preds}


def summary(outputs,dev):
    recovered=sum(surg.target_recovered(r,outputs[r["passage_id"]]) for r in dev)
    pids=set(outputs)
    changed=sum(outputs[p]!=next(r["source"] for r in dev if r["passage_id"]==p) for p in pids)
    return {"exact_target_recoveries":recovered,"exact_target_recovery_rate":recovered/len(dev),"changed_passages":changed}


def main():
    ART.mkdir(parents=True,exist_ok=True)
    commit=subprocess.check_output(["git","-C",str(ROOT/"upstream/text-editing"),"rev-parse","HEAD"],text=True).strip()
    assert commit=="4d552ca3ae98029550f27fc52aa1b22883e16e61"
    assert platform.python_version().startswith("3.10.")
    assert torch.__version__.startswith("1.12.1")
    assert transformers.__version__=="4.30.0"

    ged=json.loads((ART/"SELECTIVE_GED_LOCALIZATION.json").read_text(encoding="utf-8"))
    nopnx=surg.load_model("nopnx")
    models={"nopnx":nopnx}
    dev=read_jsonl(DEV)
    passages={}
    for r in dev: passages.setdefault(r["passage_id"],r["source"])

    variant_names=["op_aware","ged_zaebuc","ged_qalb14","ged_union","ged_intersection"]
    outputs={k:{} for k in variant_names}
    passage_records={}

    for pid,source in passages.items():
        baseline,trace=surg.run_variant(source,models,"nopnx1")
        candidates=trace[0].get("applied_edits",[])
        base=set()
        candidate_rows=[]
        z=ged_lookup(ged,"zaebuc_ged13",pid)
        q=ged_lookup(ged,"qalb14_ged13",pid)
        for i,e in enumerate(candidates):
            allow,reason=base_allow(e)
            if allow: base.add(i)
            wi=int(e["word_index"])
            ze=bool(z[wi]["is_error"]); qe=bool(q[wi]["is_error"])
            candidate_rows.append({
                "edit_index":i,**e,
                "operation_family":op_family(e["label"]),
                "base_policy_allow":allow,
                "base_policy_reason":reason,
                "ged":{
                    "zaebuc":{"label":z[wi]["label"],"score":z[wi]["score"],"is_error":ze},
                    "qalb14":{"label":q[wi]["label"],"score":q[wi]["score"],"is_error":qe},
                }
            })
        gates={
            "op_aware":base,
            "ged_zaebuc":{i for i in base if candidate_rows[i]["ged"]["zaebuc"]["is_error"]},
            "ged_qalb14":{i for i in base if candidate_rows[i]["ged"]["qalb14"]["is_error"]},
            "ged_union":{i for i in base if candidate_rows[i]["ged"]["zaebuc"]["is_error"] or candidate_rows[i]["ged"]["qalb14"]["is_error"]},
            "ged_intersection":{i for i in base if candidate_rows[i]["ged"]["zaebuc"]["is_error"] and candidate_rows[i]["ged"]["qalb14"]["is_error"]},
        }
        gate_meta={}
        for name,idxs in gates.items():
            out,applied,abst=apply_subset(source,candidates,idxs)
            outputs[name][pid]=out
            gate_meta[name]={"requested_indices":sorted(idxs),"applied_indices":applied,"mapping_abstentions":abst}
        passage_records[str(pid)]={
            "source":source,
            "baseline_surgical_output":baseline,
            "baseline_candidate_edits":candidate_rows,
            "baseline_suppressed_hazards":trace[0].get("suppressed",[]),
            "outputs":{k:outputs[k][pid] for k in variant_names},
            "gate_meta":gate_meta,
        }

    summaries={k:summary(outputs[k],dev) for k in variant_names}

    # Scientific authored stress cases: locks are applied before selection.
    corr=json.loads(SCI_CORR.read_text(encoding="utf-8")).get("corrections",{}) if SCI_CORR.exists() else {}
    sci_rows=read_jsonl(SCI); sci_summary={}
    # GED variants are not run on authored stress here; primary op-aware safety is the gate invariant.
    exact=unchanged=unk=0
    sci_cases=[]
    for r in sci_rows:
        protected=corr.get(r["case_id"],{}).get("effective_protected",r["protected"])
        source=r["source"]
        baseline,trace=surg.run_variant(source,models,"nopnx1",protected=protected)
        candidates=trace[0].get("applied_edits",[])
        idxs={i for i,e in enumerate(candidates) if base_allow(e)[0]}
        out,applied,abst=apply_subset(source,candidates,idxs)
        exact+=int(all(p in out for p in protected)); unchanged+=int(out==source); unk+=int("[UNK]" in out)
        sci_cases.append({"case_id":r["case_id"],"protected":protected,"output":out,"applied_indices":applied,"mapping_abstentions":abst})
    sci_summary["op_aware"]={"cases":len(sci_rows),"protected_exact_cases":exact,"source_exact_unchanged_cases":unchanged,"outputs_with_UNK":unk}

    result={
        "status":"PHASE2_SELECTIVE_SURGICAL_GATE_DEVELOPMENT",
        "not_sealed":True,
        "runtime":{"python":platform.python_version(),"torch":torch.__version__,"transformers":transformers.__version__,"sweet_commit":commit},
        "policy":{"INSERT":"allow non-space only","REPLACE":"allow confidence >=0.80","DELETE":"abstain","OTHER":"abstain"},
        "ged_models":["zaebuc_ged13","qalb14_ged13"],
        "variant_summaries":summaries,
        "scientific_stress_summary":sci_summary,
        "scientific_cases":sci_cases,
        "passages":passage_records,
        "anti_leakage":"Nahw target spans are not used by any runtime gate."
    }
    p=ART/"SELECTIVE_SURGICAL_GATE_RAW.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"variant_summaries":summaries,"scientific_stress_summary":sci_summary,"output":str(p)},ensure_ascii=False))


if __name__=="__main__":
    main()
