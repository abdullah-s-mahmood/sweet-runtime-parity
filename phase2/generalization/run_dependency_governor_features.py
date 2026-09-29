"""Label-blind dependency/governor features for the 14 consumed fresh-V1 PASS events.

Reads QALB15 TRAIN RAW and frozen model artifacts ephemerally.
Persists no Arabic text.
"""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
import pandas as pd
from camel_tools.utils.dediac import dediac_ar

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
SAFE=ART/"ortho_safe"/"PHASE2_ORTHO_ISOLATED_VALIDATION_FEATURES.jsonl"
ARA=ART/"ortho_arabart"/"VAL_ARABART_Q14_EVENTS.jsonl"
RAW=ROOT/"upstream"/"arabic-gec"/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
CP=ROOT/"upstream"/"camel_parser"
OUT=ROOT/"PHASE2_DEPENDENCY_GOVERNOR_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_DEPENDENCY_GOVERNOR_RUNTIME.json"
PARSER_COMMIT="66f29f7e34e3b5b38780d08bd56cf481635bf1c6"

def sha(s):
    return hashlib.sha256(str(s).encode("utf-8")).hexdigest()

def jl(p):
    return read_jsonl(p)

def read_lines(p):
    return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def load_parser():
    sys.path.insert(0,str(CP.resolve()))
    from src.utils.model_downloader import get_model_name
    from src.data_preparation import get_tagset
    from src.initialize_disambiguator.disambiguator_interface import get_disambiguator
    model_path=CP/"models"
    model_name=get_model_name("catib",model_path=model_path)
    tagset=get_tagset("catib")
    dis=get_disambiguator("bert","r13")
    clitic=pd.read_csv(CP/"data/clitic_feats.csv").astype(str).astype(object)
    return model_path/model_name,tagset,dis,clitic

def normalize_form(x):
    from src.dependency_parser.biaff_parser import filter_tatweel
    return filter_tatweel(dediac_ar(str(x)))

def parse_with_map(sentence, model_file, tagset, dis, clitic):
    from src.classes import PreprocessedTextParams
    from src.data_preparation import parse_text
    from src.parse_disambiguation.disambiguation_analysis import to_sentence_analysis_list
    from src.parse_disambiguation.feature_extraction import get_word_features_df

    words=sentence.split()
    dws=dis.disambiguate_sentences([words])
    analyses=to_sentence_analysis_list(dws,[words])[0]
    assert len(analyses)==len(words)

    spans=[]; expected=[]; cursor=0
    for a in analyses:
        df=get_word_features_df(a,clitic)
        forms=[normalize_form(x) for x in list(df["token"])]
        assert forms
        spans.append([cursor,cursor+len(forms)])
        expected.extend(forms);cursor+=len(forms)

    params=PreprocessedTextParams([sentence],model_file,dis,clitic,tagset,"")
    parsed=parse_text("preprocessed_text",params)[0]
    actual=[normalize_form(r[1]) for r in parsed]
    assert expected==actual,(len(expected),len(actual))
    assert cursor==len(parsed)
    return parsed,spans

def featdict(row):
    out={}
    raw=str(row[5] or "")
    for part in raw.split("|"):
        if "=" in part:
            k,v=part.split("=",1);out[k]=v
    return out

def anchor_for_span(rows, span):
    a,b=span
    idxs=list(range(a,b))
    bases=[i for i in idxs if featdict(rows[i]).get("token_type")=="baseword"]
    return bases[0] if len(bases)==1 else None, len(bases)

def word_anchor(rows,spans,wi):
    if wi<0 or wi>=len(spans): return None
    a,_=anchor_for_span(rows,spans[wi])
    return a

def direction_bucket(anchor_idx, head_id, target_ids):
    if head_id==0:return "ROOT"
    if head_id in target_ids:return "TARGET"
    hid=head_id-1
    d=hid-anchor_idx
    side="LEFT" if d<0 else "RIGHT"
    ad=abs(d)
    if ad==1:b="1"
    elif ad==2:b="2"
    elif ad<=5:b="3_5"
    else:b="6PLUS"
    return side+"_"+b

def summarize(rows,spans,wi):
    sp=spans[wi]; target_idxs=list(range(sp[0],sp[1]))
    target_ids={int(rows[i][0]) for i in target_idxs}
    anchor,base_count=anchor_for_span(rows,sp)
    res={
      "target_parser_tokens":len(target_idxs),
      "baseword_anchor_count":base_count,
      "mapping_reliable":anchor is not None,
    }
    if anchor is None:return res
    row=rows[anchor]; aid=int(row[0]); head=int(row[6]); dep=str(row[7]); pos=str(row[3])
    res.update({
      "anchor_pos":pos,
      "anchor_deprel":dep,
      "target_form_hash":sha(normalize_form(row[1])),
      "head_kind":"ROOT" if head==0 else ("TARGET" if head in target_ids else "EXTERNAL"),
      "head_direction_bucket":direction_bucket(anchor,head,target_ids),
    })
    if head>0:
        hr=rows[head-1]
        res["head_pos"]=str(hr[3])
        res["head_deprel"]=str(hr[7])
        res["head_form_hash"]=sha(normalize_form(hr[1]))
    else:
        res["head_pos"]="ROOT";res["head_deprel"]="ROOT";res["head_form_hash"]=None

    extdeps=[]
    for rr in rows:
        if int(rr[6])==aid and int(rr[0]) not in target_ids:
            extdeps.append(str(rr[7]))
    res["external_dependent_relations"]=sorted(extdeps)

    for label,nwi in [("prev",wi-1),("next",wi+1)]:
        na=word_anchor(rows,spans,nwi)
        if na is None:
            res[label+"_pos"]=None;res[label+"_deprel"]=None
        else:
            res[label+"_pos"]=str(rows[na][3])
            res[label+"_deprel"]=str(rows[na][7])

    fp=[
      res["anchor_pos"],res["anchor_deprel"],res["head_kind"],
      res["head_pos"],res["head_deprel"],res["head_direction_bucket"],
      ",".join(res["external_dependent_relations"]),
      str(res["prev_pos"]),str(res["prev_deprel"]),
      str(res["next_pos"]),str(res["next_deprel"]),
    ]
    res["structural_fingerprint_hash"]=sha("|".join(fp))
    return res

def main():
    safe=[x for x in jl(SAFE) if x["runtime_decision"]=="PASS"]
    assert len(safe)==14,len(safe)
    ara=jl(ARA)
    lines=read_lines(RAW)
    model_file,tagset,dis,clitic=load_parser()
    source_cache={}
    out=[]

    for n,x in enumerate(safe,1):
        lid=int(x["line_id"]); span=list(map(int,x["source_lexical_span"]))
        matches=[
          e for e in ara
          if int(e["line_id"])==lid
          and list(map(int,e.get("source_lexical_span") or [-1,-1]))==span
          and e.get("source_hash")==x["source_hash"]
          and e.get("output_hash")==x["output_hash"]
        ]
        assert matches,(x["vote_id"],len(matches))
        ev=matches[0]
        surf=ev.get("output_surfaces") or []
        assert len(surf)==1,(x["vote_id"],surf)

        source=lines[lid-1]
        us=units(source); i=span[0]
        assert 0<=i<len(us)
        wi=int(us[i]["whitespace_word_index"])
        words=source.split()
        assert words[wi]==us[i]["surface"]
        cand=list(words);cand[wi]=surf[0]
        candidate=" ".join(cand)

        if lid not in source_cache:
            source_cache[lid]=parse_with_map(source,model_file,tagset,dis,clitic)
        sr,smap=source_cache[lid]
        cr,cmap=parse_with_map(candidate,model_file,tagset,dis,clitic)
        assert len(smap)==len(words)==len(cmap)

        s=summarize(sr,smap,wi); c=summarize(cr,cmap,wi)
        keys=[
          "target_parser_tokens","baseword_anchor_count","mapping_reliable",
          "anchor_pos","anchor_deprel","head_kind","head_direction_bucket",
          "head_pos","head_deprel","external_dependent_relations",
          "prev_pos","prev_deprel","next_pos","next_deprel",
          "structural_fingerprint_hash","head_form_hash"
        ]
        changes={k:(s.get(k)!=c.get(k)) for k in keys}
        out.append({
          "vote_id":x["vote_id"],"line_id":lid,"line_hash":x["line_hash"],
          "source_lexical_span":span,"source_hash":x["source_hash"],"output_hash":x["output_hash"],
          "whitespace_word_index":wi,
          "source_dependency":s,"candidate_dependency":c,
          "changed":changes,
          "any_structural_category_changed":any(
              changes[k] for k in keys
              if k not in {"structural_fingerprint_hash","head_form_hash","target_parser_tokens","baseword_anchor_count","mapping_reliable"}
          ),
        })
        print(f"[{n}/{len(safe)}] {x['vote_id']}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic text leaked"
    obj={
      "status":"PHASE2_DEPENDENCY_GOVERNOR_FEATURES_FROZEN",
      "diagnostic_only":True,"labels_or_gold_read":False,
      "population":"14 consumed ORTHO_ISOLATED_COMMON_NOUN_V1 fresh PASS events",
      "rows":len(out),"parser_commit":PARSER_COMMIT,
      "mapping_reliable_rows":sum(bool(x["source_dependency"].get("mapping_reliable") and x["candidate_dependency"].get("mapping_reliable")) for x in out),
      "any_structural_category_changed":sum(x["any_structural_category_changed"] for x in out),
      "features_sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),
      "qalb_text_persisted":False,"qalb15_test_read":False,
      "rule_defined":False,
    }
    RUNTIME.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(obj))

if __name__=="__main__":main()
