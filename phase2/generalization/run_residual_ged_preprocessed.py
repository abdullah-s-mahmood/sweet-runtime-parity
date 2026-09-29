"""Preprocessing-faithful residual GED replication on the consumed 14 ORTHO PASS events.

Uses the official pinned CAMeLIRA-preprocessed QALB15 TRAIN source representation.
Label-blind. Persists no Arabic text.
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
FEATURES=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"
ARABART=ROOT/"artifacts/arabart/VAL_ARABART_Q14_EVENTS.jsonl"
OUT=ROOT/"PHASE2_RESIDUAL_GED_PREPROCESSED_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_RESIDUAL_GED_PREPROCESSED_RUNTIME.json"

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
    att=[1]*len(input_ids);typ=[0]*len(input_ids)
    if len(input_ids)>model.config.max_position_embeddings:
        raise RuntimeError(f"sequence too long: {len(input_ids)}")
    with torch.no_grad():
        logits=model(input_ids=torch.tensor([input_ids]),attention_mask=torch.tensor([att]),token_type_ids=torch.tensor([typ])).logits[0]
        probs=torch.softmax(logits,dim=-1)
    out=[]
    for pi in first:
        score,pred=probs[1+pi].max(dim=-1)
        out.append({"label":model.config.id2label[int(pred)],"score":float(score)})
    return out

def main():
    frozen=[x for x in jl(FEATURES) if x["runtime_decision"]=="PASS"]
    assert len(frozen)==14
    frozen_by={(int(x["line_id"]),tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"]):x for x in frozen}
    evmap={}
    for e in jl(ARABART):
        sp=e.get("source_lexical_span") or [-1,-1]
        if e.get("primitive_ops")==["SUB"] and len(e.get("source_bases") or [])==1 and len(e.get("output_bases") or [])==1:
            k=(int(e["line_id"]),tuple(sp),e["source_hash"],e["output_hash"])
            if k in frozen_by:evmap[k]=e
    assert len(evmap)==14

    raw=read_lines(RAW);pre=read_lines(PRE)
    assert len(raw)==len(pre)
    loaded={}
    for name,(mid,rev) in MODELS.items():
        tok=AutoTokenizer.from_pretrained(mid,revision=rev,use_fast=False)
        model=AutoModelForTokenClassification.from_pretrained(mid,revision=rev).eval().cpu()
        loaded[name]=(tok,model)

    out=[]
    for n,(k,f) in enumerate(sorted(frozen_by.items()),1):
        e=evmap[k];line_id=int(f["line_id"]);lex_i=int(f["source_lexical_span"][0])
        raw_words=raw[line_id-1].split();pre_words=pre[line_id-1].split()
        assert len(raw_words)==len(pre_words),(line_id,len(raw_words),len(pre_words))
        us=units(raw[line_id-1]);wi=int(us[lex_i]["whitespace_word_index"])
        src_surface=(e.get("source_surfaces") or [None])[0]
        cand_surface=(e.get("output_surfaces") or [None])[0]
        assert src_surface and cand_surface and raw_words[wi]==src_surface
        pre_target=pre_words[wi]
        cand=list(pre_words)
        already=(pre_target==cand_surface)
        if not already:cand[wi]=cand_surface

        model_feats={}
        for name,(tok,model) in loaded.items():
            canp=predict_words(cand,tok,model)
            model_feats[name]={
              "candidate_target_label":canp[wi]["label"],
              "candidate_target_score":canp[wi]["score"],
              "candidate_window1_labels":[canp[j]["label"] for j in range(max(0,wi-1),min(len(canp),wi+2))],
              "candidate_window2_labels":[canp[j]["label"] for j in range(max(0,wi-2),min(len(canp),wi+3))],
            }

        def clean(rad):
            for m in model_feats.values():
                labels=m["candidate_target_label"] if rad==0 else m[f"candidate_window{rad}_labels"]
                if rad==0:
                    if labels!="UC":return False
                elif any(x!="UC" for x in labels):return False
            return True

        decisions={
          "GED_TARGET_CLEAN_BOTH":"PASS" if clean(0) else "REVIEW",
          "GED_WINDOW1_CLEAN_BOTH":"PASS" if clean(1) else "REVIEW",
          "GED_WINDOW2_CLEAN_BOTH":"PASS" if clean(2) else "REVIEW",
        }
        out.append({
          "vote_id":f["vote_id"],"line_id":line_id,"line_hash":f["line_hash"],
          "source_lexical_span":f["source_lexical_span"],
          "source_hash":f["source_hash"],"output_hash":f["output_hash"],
          "raw_token_count":len(raw_words),"preprocessed_token_count":len(pre_words),
          "preprocessed_target_hash":sha(pre_target),
          "candidate_surface_hash":sha(cand_surface),
          "preprocessing_already_candidate":already,
          "models":model_feats,"runtime_decisions":decisions,
        })
        print(f"[{n}/14] {f['vote_id']} already={already} {decisions}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    counts={p:{"PASS":sum(x["runtime_decisions"][p]=="PASS" for x in out),"REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in out)} for p in out[0]["runtime_decisions"]}
    rt={
      "status":"RESIDUAL_GED_PREPROCESSED_FEATURES_FROZEN",
      "diagnostic_only":True,"consumed_population":True,"labels_read":False,
      "rows":14,"decision_counts":counts,
      "preprocessing_already_candidate_count":sum(x["preprocessing_already_candidate"] for x in out),
      "preprocessing_source":"official pinned CAMeLIRA QALB15 TRAIN source",
      "preprocessing_faithful":True,
      "models":{k:{"model_id":v[0],"revision":v[1]} for k,v in MODELS.items()},
      "features_sha256":file_sha(OUT),"qalb15_test_read":False,"qalb_text_persisted":False,
    }
    RUNTIME.write_text(json.dumps(rt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+RUNTIME.read_text(encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in dumped)
    print(json.dumps(rt,ensure_ascii=False))

if __name__=="__main__":main()
