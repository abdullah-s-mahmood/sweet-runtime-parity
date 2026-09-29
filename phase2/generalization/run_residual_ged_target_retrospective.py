"""Retrospective replication of preprocessing-faithful GED_TARGET_CLEAN_BOTH.

Population is selected label-blind from frozen contextual-guard runtime decisions:
36 ORTHO_MORPH_COMMON_NOUN_V1 PASS events, with nested 19 strict V1 PASS.
Persists no Arabic text.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import torch
from transformers import AutoTokenizer,AutoModelForTokenClassification
from phase2.arabart_audit.build_full_arabart_edit_queue import units

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
PRE=ROOT/"upstream/arabic-gec/data/gec/camelira_gec/qalb15/qalb15_train.src.txt"
GUARD=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"
ARABART=ROOT/"artifacts/arabart/TRI_ARABART_Q14_EVENTS.jsonl"
OUT=ROOT/"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_RUNTIME.json"

MODELS={
 "QALB14":("CAMeL-Lab/camelbert-msa-qalb14-ged-13","447179dc63d186e4bff09a993e90e73ad622d571"),
 "ZAEBUC":("CAMeL-Lab/camelbert-msa-zaebuc-ged-13","40c80685157d65504c942a8730f4f6b11c249679"),
}

def jl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def read_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def predict_words(words,tok,model):
    pieces=[];first=[]
    for w in words:
        wp=tok.tokenize(w) or [tok.unk_token]
        first.append(len(pieces));pieces.extend(wp)
    ids=tok.convert_tokens_to_ids(pieces)
    input_ids=[tok.cls_token_id]+ids+[tok.sep_token_id]
    if len(input_ids)>model.config.max_position_embeddings:
        raise RuntimeError(f"sequence too long: {len(input_ids)}")
    att=[1]*len(input_ids);typ=[0]*len(input_ids)
    with torch.no_grad():
        logits=model(input_ids=torch.tensor([input_ids]),attention_mask=torch.tensor([att]),token_type_ids=torch.tensor([typ])).logits[0]
        probs=torch.softmax(logits,dim=-1)
    out=[]
    for pi in first:
        score,pred=probs[1+pi].max(dim=-1)
        out.append({"label":model.config.id2label[int(pred)],"score":float(score)})
    return out

def main():
    guard=jl(GUARD)
    primary=[x for x in guard if x["runtime_decisions"]["ORTHO_MORPH_COMMON_NOUN_V1"]=="PASS"]
    strict={x["vote_id"] for x in guard if x["runtime_decisions"]["ORTHO_ISOLATED_COMMON_NOUN_V1"]=="PASS"}
    assert len(primary)==36,len(primary)
    assert len(strict)==19,len(strict)

    frozen={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in primary}
    evmap={}
    for e in jl(ARABART):
        sp=e.get("source_lexical_span") or [-1,-1]
        if e.get("primitive_ops")==["SUB"] and len(e.get("source_bases") or [])==1 and len(e.get("output_bases") or [])==1:
            k=(int(e["line_id"]),tuple(sp),e["source_hash"],e["output_hash"])
            if k in frozen:evmap[k]=e
    assert len(evmap)==36,(len(evmap),len(frozen))

    raw=read_lines(RAW);pre=read_lines(PRE);assert len(raw)==len(pre)
    loaded={}
    for name,(mid,rev) in MODELS.items():
        tok=AutoTokenizer.from_pretrained(mid,revision=rev,use_fast=False)
        model=AutoModelForTokenClassification.from_pretrained(mid,revision=rev).eval().cpu()
        loaded[name]=(tok,model)

    out=[]
    for n,(k,f) in enumerate(sorted(frozen.items()),1):
        e=evmap[k];line_id=int(f["line_id"]);lex_i=int(f["source_lexical_span"][0])
        rw=raw[line_id-1].split();pw=pre[line_id-1].split()
        assert len(rw)==len(pw),(line_id,len(rw),len(pw))
        wi=int(units(raw[line_id-1])[lex_i]["whitespace_word_index"])
        src=(e.get("source_surfaces") or [None])[0];cand=(e.get("output_surfaces") or [None])[0]
        assert src and cand and rw[wi]==src
        pre_target=pw[wi];cw=list(pw)
        already=(pre_target==cand)
        if not already:cw[wi]=cand

        mf={}
        for name,(tok,model) in loaded.items():
            pred=predict_words(cw,tok,model)
            mf[name]={"candidate_target_label":pred[wi]["label"],"candidate_target_score":pred[wi]["score"]}
        passed=all(m["candidate_target_label"]=="UC" for m in mf.values())
        out.append({
          "vote_id":f["vote_id"],"line_id":line_id,"line_hash":f["line_hash"],
          "source_lexical_span":f["source_lexical_span"],"source_hash":f["source_hash"],"output_hash":f["output_hash"],
          "strict_v1_subset":f["vote_id"] in strict,
          "raw_token_count":len(rw),"preprocessed_token_count":len(pw),
          "preprocessed_target_hash":sha(pre_target),"candidate_surface_hash":sha(cand),
          "preprocessing_already_candidate":already,
          "models":mf,"runtime_decision":"PASS" if passed else "REVIEW",
        })
        print(f"[{n}/36] {f['vote_id']} strict={f['vote_id'] in strict} already={already} {'PASS' if passed else 'REVIEW'}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    rt={
      "status":"RESIDUAL_GED_TARGET_RETROSPECTIVE_FEATURES_FROZEN",
      "diagnostic_only":True,"consumed_population":True,"labels_read":False,
      "rows":36,"strict_v1_rows":19,
      "pass":sum(x["runtime_decision"]=="PASS" for x in out),
      "review":sum(x["runtime_decision"]=="REVIEW" for x in out),
      "strict_v1_pass":sum(x["strict_v1_subset"] and x["runtime_decision"]=="PASS" for x in out),
      "preprocessing_already_candidate_count":sum(x["preprocessing_already_candidate"] for x in out),
      "preprocessing_faithful":True,
      "features_sha256":file_sha(OUT),
      "models":{k:{"model_id":v[0],"revision":v[1]} for k,v in MODELS.items()},
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    RUNTIME.write_text(json.dumps(rt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+RUNTIME.read_text(encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in dumped)
    print(json.dumps(rt,ensure_ascii=False))

if __name__=="__main__":main()
