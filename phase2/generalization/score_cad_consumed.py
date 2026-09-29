"""Score consumed QALB15 evidence with the frozen externally-trained CAD feasibility model.

No current adjudication labels or corrected QALB15 data are read here.
Arabic text is used transiently for encoding and never persisted.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import joblib
import numpy as np

from phase2.generalization.cad_feasibility_common import (
    MODEL_ID, MODEL_REVISION, target_window, load_encoder, pair_feature_matrix
)
from phase2.arabart_audit.build_full_arabart_edit_queue import units

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"

MODEL_PATH=ROOT/"artifacts/cad_model/CAD_FEASIBILITY_MODEL.joblib"
SUMMARY_PATH=ROOT/"artifacts/cad_model/PHASE2_CAD_EXTERNAL_TRAINING_SUMMARY.json"

THIRD_FEATURES=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"
THIRD_ARABART=ROOT/"artifacts/third_arabart/VAL_ARABART_Q14_EVENTS.jsonl"

OLD_GUARD=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"
OLD_ARABART=ROOT/"artifacts/old_arabart/TRI_ARABART_Q14_EVENTS.jsonl"

OUT=ROOT/"PHASE2_CAD_CONSUMED_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_CAD_CONSUMED_RUNTIME.json"

def jl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def file_sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def read_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def event_map(path, wanted):
    out={}
    for e in jl(path):
        sp=e.get("source_lexical_span") or [-1,-1]
        if e.get("primitive_ops")!=["SUB"]: continue
        if len(e.get("source_bases") or [])!=1 or len(e.get("output_bases") or [])!=1: continue
        k=(int(e["line_id"]),tuple(map(int,sp)),e["source_hash"],e["output_hash"])
        if k in wanted:
            out[k]=e
    return out

def make_items():
    third=[x for x in jl(THIRD_FEATURES) if x["runtime_decision"]=="PASS"]
    assert len(third)==14,len(third)
    tkeys={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in third}
    tev=event_map(THIRD_ARABART,tkeys)
    assert len(tev)==14,(len(tev),len(tkeys))

    guard=jl(OLD_GUARD)
    old=[x for x in guard if x["runtime_decisions"]["ORTHO_MORPH_COMMON_NOUN_V1"]=="PASS"]
    strict_ids={x["vote_id"] for x in guard if x["runtime_decisions"]["ORTHO_ISOLATED_COMMON_NOUN_V1"]=="PASS"}
    assert len(old)==36,len(old)
    assert len(strict_ids)==19,len(strict_ids)
    okeys={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in old}
    oev=event_map(OLD_ARABART,okeys)
    assert len(oev)==36,(len(oev),len(okeys))

    items=[]
    for population,records,evs,strict in [
        ("THIRD_V1_14",tkeys,tev,set()),
        ("EARLIER_ORTHO_MORPH_36",okeys,oev,strict_ids),
    ]:
        for k,f in sorted(records.items()):
            items.append((population,f,evs[k],f["vote_id"] in strict))
    return items

def main():
    summary=json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    assert summary["external_feasibility_criterion_met"] is True
    assert summary["encoder_model_id"]==MODEL_ID
    assert summary["encoder_revision"]==MODEL_REVISION
    assert file_sha(MODEL_PATH)==summary["model_sha256"]

    payload=joblib.load(MODEL_PATH)
    assert payload["encoder_model_id"]==MODEL_ID
    assert payload["encoder_revision"]==MODEL_REVISION
    threshold=float(payload["threshold"])
    assert abs(threshold-float(summary["acceptance_threshold"]))<1e-15
    pipe=payload["pipeline"]

    raw=read_lines(RAW)
    items=make_items()

    transient=[]
    metadata=[]
    for population,f,e,strict in items:
        line_id=int(f["line_id"])
        lex_i=int(f["source_lexical_span"][0])
        text=raw[line_id-1]
        words=text.split()
        us=units(text)
        wi=int(us[lex_i]["whitespace_word_index"])
        src_surface=(e.get("source_surfaces") or [None])[0]
        cand_surface=(e.get("output_surfaces") or [None])[0]
        assert src_surface and cand_surface
        assert words[wi]==src_surface,(population,f["vote_id"],words[wi],src_surface)
        cand=list(words);cand[wi]=cand_surface
        transient.append((target_window(words,wi),target_window(cand,wi)))
        metadata.append({
            "population":population,
            "vote_id":f["vote_id"],
            "line_id":line_id,
            "line_hash":f["line_hash"],
            "source_lexical_span":f["source_lexical_span"],
            "source_hash":f["source_hash"],
            "output_hash":f["output_hash"],
            "strict_v1_member":bool(strict),
            "source_window_hash":sha(transient[-1][0]),
            "candidate_window_hash":sha(transient[-1][1]),
        })

    tok,enc=load_encoder()
    X=pair_feature_matrix(transient,tok,enc)
    probs=pipe.predict_proba(X)[:,1]
    rows=[]
    for m,p in zip(metadata,probs):
        r=dict(m)
        r["accept_probability"]=float(p)
        r["runtime_decision"]="PASS" if float(p)>=threshold else "REVIEW"
        rows.append(r)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    counts={}
    for pop in sorted({x["population"] for x in rows}):
        pr=[x for x in rows if x["population"]==pop]
        counts[pop]={
            "rows":len(pr),
            "pass":sum(x["runtime_decision"]=="PASS" for x in pr),
            "review":sum(x["runtime_decision"]=="REVIEW" for x in pr),
            "strict_v1_rows":sum(x["strict_v1_member"] for x in pr),
            "strict_v1_pass":sum(x["strict_v1_member"] and x["runtime_decision"]=="PASS" for x in pr),
        }

    rt={
        "status":"PHASE2_CAD_CONSUMED_FEATURES_FROZEN",
        "external_model_frozen":True,
        "current_labels_read":False,
        "qalb15_corrected_read":False,
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
        "encoder_model_id":MODEL_ID,
        "encoder_revision":MODEL_REVISION,
        "model_sha256":summary["model_sha256"],
        "acceptance_threshold":threshold,
        "rows":len(rows),
        "population_counts":counts,
        "features_sha256":file_sha(OUT),
    }
    RUNTIME.write_text(json.dumps(rt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+RUNTIME.read_text(encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in dumped)
    print(json.dumps(rt,ensure_ascii=False))

if __name__=="__main__":main()
