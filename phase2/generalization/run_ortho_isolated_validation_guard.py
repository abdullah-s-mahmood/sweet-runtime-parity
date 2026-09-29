"""Apply frozen ORTHO_ISOLATED_COMMON_NOUN_V1 on the third slice. Gold-blind."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl
from phase2.generalization.run_contextual_residual_guard import (
    char_family,get_analysis,reliable,norm_lex,same_selected,
    MORPH_KEYS,CLITIC_KEYS,distance_to_span,key
)

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
ART=ROOT/"artifacts"
VOTES=ART/"ORTHO_VALIDATION_VOTE_FEATURES.jsonl"
FILES={
 "SWEET_Q14":ART/"sweet_q14"/"VAL_SWEET_Q14_EVENTS.jsonl",
 "SWEET_ZAEBUC":ART/"sweet_zaebuc"/"VAL_SWEET_ZAEBUC_EVENTS.jsonl",
 "ARABART_Q14":ART/"arabart_q14"/"VAL_ARABART_Q14_EVENTS.jsonl",
}
OUT=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_RUNTIME.json"

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def read_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    votes=read_jsonl(VOTES)
    event_rows={v:read_jsonl(p) for v,p in FILES.items()}
    by_key={}
    by_line={v:{} for v in FILES}
    for voter,rows in event_rows.items():
        for e in rows:
            by_line[voter].setdefault(int(e["line_id"]),[]).append(e)
            sp=e.get("source_lexical_span") or [-1,-1]
            if e.get("primitive_ops")==["SUB"] and len(e.get("source_bases") or [])==1 and len(e.get("output_bases") or [])==1 and sp[0]>=0 and sp[1]-sp[0]==1:
                by_key.setdefault(key(e),{})[voter]=e

    raw=read_lines(RAW)
    dis=BERTUnfactoredDisambiguator.pretrained()
    source_cache={}
    out=[]

    for n,v in enumerate(votes,1):
        line_id=int(v["line_id"]);i=int(v["source_lexical_span"][0])
        k=(line_id,tuple(v["source_lexical_span"]),tuple(v["source_bases"]),tuple(v["output_bases"]))
        reps=by_key.get(k,{})
        assert len(reps)==3,(v["vote_id"],reps.keys())
        sample=next(iter(reps.values()))
        src_surface=(sample.get("source_surfaces") or [None])[0]
        cand_surface=(sample.get("output_surfaces") or [None])[0]
        assert src_surface and cand_surface

        source=raw[line_id-1]
        us=units(source);target=us[i]
        wi=int(target["whitespace_word_index"])
        tokens=source.split();assert tokens[wi]==target["surface"]
        cand_tokens=list(tokens);cand_tokens[wi]=cand_surface

        if line_id not in source_cache:source_cache[line_id]=dis.disambiguate(tokens)
        src_dw=source_cache[line_id];cand_dw=dis.disambiguate(cand_tokens)
        sa=get_analysis(src_dw[wi]);ca=get_analysis(cand_dw[wi])
        sr=reliable(sa);cr=reliable(ca)
        spos=sa.get("pos") if sr else None;cpos=ca.get("pos") if cr else None
        lemma_same=bool(sr and cr and norm_lex(sa.get("lex"))==norm_lex(ca.get("lex")))
        morph_same=bool(sr and cr and same_selected(sa,ca,MORPH_KEYS))
        clitic_same=bool(sr and cr and same_selected(sa,ca,CLITIC_KEYS))

        nearby=False
        for voter,lines in by_line.items():
            for e in lines.get(line_id,[]):
                if key(e)==k:continue
                if distance_to_span(i,e.get("source_lexical_span") or [-1,-1])<=2:
                    nearby=True;break
            if nearby:break

        family=char_family(src_surface,cand_surface)
        passed=(
          family!="OTHER" and sr and cr and
          spos=="noun" and cpos=="noun" and
          lemma_same and morph_same and clitic_same and not nearby
        )
        out.append({
          "vote_id":v["vote_id"],"line_id":line_id,"line_hash":v["line_hash"],
          "source_lexical_span":v["source_lexical_span"],
          "source_hash":v["source_hash"],"output_hash":v["output_hash"],
          "surface_family":family,
          "source_analysis_reliable":sr,"candidate_analysis_reliable":cr,
          "source_pos":spos,"candidate_pos":cpos,
          "lemma_same":lemma_same,"morph_identity":morph_same,"clitic_identity":clitic_same,
          "nearby_other_edit_any_voter":nearby,
          "runtime_decision":"PASS" if passed else "REVIEW",
        })
        print(f"[{n}/{len(votes)}] {v['vote_id']} {'PASS' if passed else 'REVIEW'}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    obj={
      "status":"ORTHO_ISOLATED_COMMON_NOUN_V1_FRESH_RUNTIME_FROZEN",
      "labels_or_gold_read":False,"rows":len(out),
      "pass":sum(x["runtime_decision"]=="PASS" for x in out),
      "review":sum(x["runtime_decision"]=="REVIEW" for x in out),
      "features_sha256":file_sha(OUT),"rule_version":"ORTHO_ISOLATED_COMMON_NOUN_V1",
      "qalb_text_persisted":False,"qalb15_test_read":False,
      "rule_frozen_before_labels":True,
    }
    SUMMARY.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+SUMMARY.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
