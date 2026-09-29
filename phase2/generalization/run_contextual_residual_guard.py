"""Contextual residual-risk guard over the frozen tri-model unanimity stream.

Diagnostic-only on the already-consumed tri-model slice.
Reads QALB RAW text and frozen model artifacts only.
Must not read gold or manual adjudication labels.
Persists no Arabic text.
"""
from __future__ import annotations
import hashlib, json, re, unicodedata
from pathlib import Path

from camel_tools.disambig.bert import BERTUnfactoredDisambiguator

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl
from phase2.generalization.materialize_trimodel_votes import main as materialize_votes

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
ART=ROOT/"artifacts"
VOTES=ART/"TRIMODEL_VOTE_FEATURES.jsonl"
FILES={
 "SWEET_Q14":ART/"sweet_q14"/"TRI_SWEET_Q14_EVENTS.jsonl",
 "SWEET_ZAEBUC":ART/"sweet_zaebuc"/"TRI_SWEET_ZAEBUC_EVENTS.jsonl",
 "ARABART_Q14":ART/"arabart_q14"/"TRI_ARABART_Q14_EVENTS.jsonl",
}
OUT=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_RUNTIME.json"
SOURCE_RUN=36517205396

ALIF_HAMZA=set("ااأإآ")
MORPH_KEYS=("pos","per","gen","num","asp","mod","vox","stt","cas")
CLITIC_KEYS=("prc0","prc1","prc2","prc3","enc0")

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def read_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def strip_marks(s):
    return "".join(ch for ch in unicodedata.normalize("NFC",s)
                   if unicodedata.category(ch)!="Mn" and ch!="ـ")

def norm_lex(x):
    if not x:return None
    x=strip_marks(str(x))
    x=re.sub(r"_[0-9]+$","",x)
    return x

def char_family(a,b):
    a=strip_marks(a);b=strip_marks(b)
    if len(a)!=len(b): return "OTHER"
    dif=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    if len(dif)!=1:return "OTHER"
    i=dif[0];x=a[i];y=b[i]
    if i==len(a)-1 and {x,y}=={"ى","ي"}:return "FINAL_MAQSURA_YA"
    if i==len(a)-1 and {x,y}=={"ه","ة"}:return "FINAL_HA_TA_MARBUTA"
    if x in ALIF_HAMZA and y in ALIF_HAMZA:return "ALIF_HAMZA"
    return "OTHER"

def get_analysis(dw):
    analyses=getattr(dw,"analyses",None) or []
    if not analyses:return {}
    top=analyses[0]
    return getattr(top,"analysis",{}) or {}

def reliable(a):
    if not a:return False
    pos=a.get("pos")
    lex=a.get("lex")
    src=str(a.get("source","")).lower()
    if not pos or not lex:return False
    if str(lex).upper().startswith("NOAN"):return False
    if "backoff" in src or src in {"none","noan"}:return False
    return True

def same_selected(a,b,keys):
    return all(str(a.get(k,""))==str(b.get(k,"")) for k in keys)

def key(e):
    return (int(e["line_id"]),tuple(map(int,e["source_lexical_span"])),
            tuple(e.get("source_bases") or []),tuple(e.get("output_bases") or []))

def distance_to_span(i,sp):
    a,b=map(int,sp)
    if a<0 or b<0:return 999
    if a<=i<b:return 0
    if b<=i:return i-b
    return a-(i+1)

def main():
    # Re-materialize frozen vote features from the downloaded canonical artifacts.
    materialize_votes()
    votes=[x for x in read_jsonl(VOTES)
           if x["runtime_decisions"]["UNANIMOUS_3"]=="ACCEPT"]
    assert len(votes)==142,len(votes)

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
        line_id=int(v["line_id"]); i=int(v["source_lexical_span"][0])
        k=(line_id,tuple(v["source_lexical_span"]),tuple(v["source_bases"]),tuple(v["output_bases"]))
        reps=by_key.get(k,{})
        assert len(reps)==3,(v["vote_id"],reps.keys())
        sample=next(iter(reps.values()))
        src_surface=(sample.get("source_surfaces") or [None])[0]
        cand_surface=(sample.get("output_surfaces") or [None])[0]
        assert src_surface and cand_surface

        source=raw[line_id-1]
        us=units(source)
        assert i<len(us),(line_id,i,len(us))
        target=us[i]
        wi=int(target["whitespace_word_index"])
        tokens=source.split()
        assert tokens[wi]==target["surface"],(tokens[wi],target["surface"])
        cand_tokens=list(tokens); cand_tokens[wi]=cand_surface

        if line_id not in source_cache:
            source_cache[line_id]=dis.disambiguate_sentence(tokens)
        src_dw=source_cache[line_id]
        cand_dw=dis.disambiguate_sentence(cand_tokens)
        assert len(src_dw)==len(tokens) and len(cand_dw)==len(cand_tokens)

        sa=get_analysis(src_dw[wi]); ca=get_analysis(cand_dw[wi])
        sr=reliable(sa); cr=reliable(ca)
        spos=sa.get("pos") if sr else None
        cpos=ca.get("pos") if cr else None
        lemma_same=bool(sr and cr and norm_lex(sa.get("lex"))==norm_lex(ca.get("lex")))
        morph_same=bool(sr and cr and same_selected(sa,ca,MORPH_KEYS))
        clitic_same=bool(sr and cr and same_selected(sa,ca,CLITIC_KEYS))

        nearby=False
        for voter,rows in by_line.items():
            for e in rows.get(line_id,[]):
                esp=e.get("source_lexical_span") or [-1,-1]
                if key(e)==k: continue
                if distance_to_span(i,esp)<=2:
                    nearby=True;break
            if nearby:break

        family=char_family(src_surface,cand_surface)
        safe_family=family!="OTHER"
        common_noun=sr and cr and spos=="noun" and cpos=="noun"
        noun_adv=sr and cr and spos in {"noun","adv"} and cpos in {"noun","adv"} and spos==cpos

        base_checks=safe_family and sr and cr and lemma_same and morph_same and clitic_same
        decisions={
          "ORTHO_ISOLATED_COMMON_NOUN_V1":"PASS" if (base_checks and common_noun and not nearby) else "REVIEW",
          "ORTHO_MORPH_COMMON_NOUN_V1":"PASS" if (base_checks and common_noun) else "REVIEW",
          "ORTHO_ISOLATED_NOUN_ADV_V1":"PASS" if (base_checks and noun_adv and not nearby) else "REVIEW",
        }
        out.append({
          "vote_id":v["vote_id"],"line_id":line_id,"line_hash":v["line_hash"],
          "source_lexical_span":v["source_lexical_span"],
          "source_hash":v["source_hash"],"output_hash":v["output_hash"],
          "surface_family":family,
          "source_analysis_reliable":sr,"candidate_analysis_reliable":cr,
          "source_pos":spos,"candidate_pos":cpos,
          "lemma_same":lemma_same,"morph_identity":morph_same,"clitic_identity":clitic_same,
          "nearby_other_edit_any_voter":nearby,
          "runtime_decisions":decisions,
        })
        print(f"[{n}/{len(votes)}] {v['vote_id']}",flush=True)

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    policies=list(out[0]["runtime_decisions"])
    counts={p:{
      "PASS":sum(x["runtime_decisions"][p]=="PASS" for x in out),
      "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in out),
    } for p in policies}
    summary={
      "status":"CONTEXTUAL_RESIDUAL_GUARD_RUNTIME_FROZEN",
      "diagnostic_only":True,
      "source_trimodel_run":SOURCE_RUN,
      "labels_or_gold_read":False,
      "rows":len(out),
      "decision_counts":counts,
      "features_sha256":file_sha(OUT),
      "qalb_text_persisted":False,
      "qalb15_test_read":False,
      "rules_frozen_before_labels":True,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    dumped=OUT.read_text(encoding="utf-8")+SUMMARY.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic/QALB text leaked"
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__": main()
