"""Label-blind retrospective CATiB PROP-to-NOM replication on the consumed 36-event morph lane."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import pandas as pd
from camel_tools.utils.dediac import dediac_ar

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
BASE=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"
ARA=ART/"tri_arabart"/"TRI_ARABART_Q14_EVENTS.jsonl"
RAW=ROOT/"upstream"/"arabic-gec"/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
CP=ROOT/"upstream"/"camel_parser"
OUT=ROOT/"PHASE2_CATIB_PROP_TO_NOM_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_CATIB_PROP_TO_NOM_RUNTIME.json"
PARSER_COMMIT="66f29f7e34e3b5b38780d08bd56cf481635bf1c6"

def jl(p):
    return read_jsonl(p)

def lines(p):
    return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def norm_form(x):
    from src.dependency_parser.biaff_parser import filter_tatweel
    return filter_tatweel(dediac_ar(str(x)))

def setup():
    sys.path.insert(0,str(CP.resolve()))
    from src.utils.model_downloader import get_model_name
    from src.data_preparation import get_tagset
    from src.initialize_disambiguator.disambiguator_interface import get_disambiguator
    mp=CP/"models"; mf=mp/get_model_name("catib",model_path=mp)
    tag=get_tagset("catib")
    dis=get_disambiguator("bert","r13")
    clitic=pd.read_csv(CP/"data/clitic_feats.csv").astype(str).astype(object)
    return mf,tag,dis,clitic

def build_maps(sentences,dis,clitic):
    from src.parse_disambiguation.disambiguation_analysis import to_sentence_analysis_list
    from src.parse_disambiguation.feature_extraction import get_word_features_df
    toks=[s.split() for s in sentences]
    dws=dis.disambiguate_sentences(toks)
    analyses=to_sentence_analysis_list(dws,toks)
    maps=[];expecteds=[]
    for words,alist in zip(toks,analyses):
        assert len(words)==len(alist)
        spans=[];expected=[];cur=0
        for a in alist:
            df=get_word_features_df(a,clitic)
            fs=[norm_form(x) for x in list(df["token"])]
            assert fs
            spans.append([cur,cur+len(fs)]);cur+=len(fs);expected.extend(fs)
        maps.append(spans);expecteds.append(expected)
    return maps,expecteds

def parse_batch(sentences,mf,tag,dis,clitic):
    from src.classes import PreprocessedTextParams
    from src.data_preparation import parse_text
    maps,exp=build_maps(sentences,dis,clitic)
    params=PreprocessedTextParams(sentences,mf,dis,clitic,tag,"")
    parsed=parse_text("preprocessed_text",params)
    assert len(parsed)==len(sentences)
    for rows,expected in zip(parsed,exp):
        actual=[norm_form(r[1]) for r in rows]
        assert actual==expected,(len(actual),len(expected))
    return parsed,maps

def anchor_pos(rows,span):
    a,b=span;bases=[]
    for i in range(a,b):
        feats={}
        for part in str(rows[i][5] or "").split("|"):
            if "=" in part:
                k,v=part.split("=",1);feats[k]=v
        if feats.get("token_type")=="baseword":bases.append(i)
    if len(bases)!=1:return None,len(bases)
    return str(rows[bases[0]][3]),1

def main():
    base=jl(BASE)
    pop=[x for x in base if x["runtime_decisions"]["ORTHO_MORPH_COMMON_NOUN_V1"]=="PASS"]
    assert len(pop)==36,len(pop)
    ara=jl(ARA);raw=lines(RAW)

    records=[];sentences=[];source_key_by_line={}
    for x in pop:
        lid=int(x["line_id"]);sp=list(map(int,x["source_lexical_span"]))
        matches=[e for e in ara if int(e["line_id"])==lid and tuple(map(int,e.get("source_lexical_span") or [-1,-1]))==tuple(sp) and e.get("source_hash")==x["source_hash"] and e.get("output_hash")==x["output_hash"]]
        assert matches,(x["vote_id"],len(matches))
        ev=matches[0];surf=ev.get("output_surfaces") or [];assert len(surf)==1

        src=raw[lid-1];us=units(src);wi=int(us[sp[0]]["whitespace_word_index"])
        ws=src.split();assert ws[wi]==us[sp[0]]["surface"]
        cand=list(ws);cand[wi]=surf[0];cand=" ".join(cand)

        if lid not in source_key_by_line:
            source_key_by_line[lid]=len(sentences);sentences.append(src)
        ci=len(sentences);sentences.append(cand)
        records.append((x,wi,source_key_by_line[lid],ci))

    mf,tag,dis,clitic=setup()
    parsed,maps=parse_batch(sentences,mf,tag,dis,clitic)

    out=[]
    for x,wi,si,ci in records:
        spos,sbc=anchor_pos(parsed[si],maps[si][wi])
        cpos,cbc=anchor_pos(parsed[ci],maps[ci][wi])
        reliable=(sbc==1 and cbc==1 and spos is not None and cpos is not None)
        decision="PASS" if (reliable and spos=="PROP" and cpos=="NOM") else "REVIEW"
        out.append({
          "vote_id":x["vote_id"],"line_id":x["line_id"],"line_hash":x["line_hash"],
          "source_lexical_span":x["source_lexical_span"],"source_hash":x["source_hash"],"output_hash":x["output_hash"],
          "strict_v1_pass":x["runtime_decisions"]["ORTHO_ISOLATED_COMMON_NOUN_V1"]=="PASS",
          "mapping_reliable":reliable,"source_catib_pos":spos,"candidate_catib_pos":cpos,
          "runtime_decision":decision,
        })

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
    obj={
      "status":"CATIB_PROP_TO_NOM_RETROSPECTIVE_RUNTIME_FROZEN",
      "diagnostic_only":True,"labels_or_gold_read":False,
      "population":"36 consumed ORTHO_MORPH_COMMON_NOUN_V1 events",
      "strict_v1_subset":sum(x["strict_v1_pass"] for x in out),
      "rows":len(out),"pass":sum(x["runtime_decision"]=="PASS" for x in out),
      "review":sum(x["runtime_decision"]=="REVIEW" for x in out),
      "strict_v1_pass_after_catib":sum(x["strict_v1_pass"] and x["runtime_decision"]=="PASS" for x in out),
      "parser_commit":PARSER_COMMIT,
      "features_sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),
      "rule_version":"CATIB_PROP_TO_NOM_EVIDENCE_V1",
      "rule_frozen_before_labels":True,
      "qalb_text_persisted":False,"qalb15_test_read":False,
    }
    RUNTIME.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(obj))

if __name__=="__main__":main()
