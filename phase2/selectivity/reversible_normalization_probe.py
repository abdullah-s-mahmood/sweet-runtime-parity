"""Reversible normalization feasibility probe for Phase 2 selectivity.

No correction is applied. This probe only measures whether removing Arabic
combining marks from the INTERNAL model view reduces tokenizer [UNK] words.
Every normalized character retains a source character index; delivered source
text remains untouched.
"""
from __future__ import annotations
import json, re, unicodedata, sys
from pathlib import Path
from transformers import BertTokenizer

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
AR=ROOT/"phase2"/"arabic_eval"
ART=ROOT/"artifacts"


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def normalize_view(word):
    out=[]
    mapping=[]
    removed=[]
    for i,ch in enumerate(word):
        if unicodedata.category(ch)=="Mn":
            removed.append({"source_index":i,"char":ch,"name":unicodedata.name(ch,"")})
            continue
        out.append(ch)
        mapping.append(i)
    return "".join(out),mapping,removed


def unk(tok,word):
    pieces=tok.tokenize(word)
    return tok.unk_token in pieces, pieces


def main():
    ART.mkdir(parents=True,exist_ok=True)
    tok=BertTokenizer.from_pretrained(str(ROOT/"models"/"nopnx"),local_files_only=True)
    dev=read_jsonl(AR/"DEVELOPMENT_TARGETS.jsonl")
    sci=read_jsonl(AR/"SCIENTIFIC_STRESS_CASES.jsonl")
    texts={}
    for r in dev:
        texts[f"nahw:{r['passage_id']}"]=r["source"]
    for r in sci:
        texts[f"sci:{r['case_id']}"]=r["source"]

    rows=[]
    total=orig_unk=norm_unk=resolved=new_unk=with_marks=0
    for text_id,text in texts.items():
        for wi,m in enumerate(re.finditer(r"\S+",text)):
            w=m.group(0)
            nv,mapping,removed=normalize_view(w)
            ou,op=unk(tok,w)
            nu,np=unk(tok,nv)
            total+=1
            orig_unk+=int(ou)
            norm_unk+=int(nu)
            resolved+=int(ou and not nu)
            new_unk+=int((not ou) and nu)
            with_marks+=int(bool(removed))
            if removed or ou or nu:
                rows.append({
                    "text_id":text_id,
                    "word_index":wi,
                    "source_span":[m.start(),m.end()],
                    "source_word":w,
                    "normalized_model_view":nv,
                    "normalized_to_source_index":mapping,
                    "removed_combining_marks":removed,
                    "original_pieces":op,
                    "normalized_pieces":np,
                    "original_has_UNK":ou,
                    "normalized_has_UNK":nu,
                    "resolved_UNK":ou and not nu,
                    "introduced_UNK":(not ou) and nu,
                })

    result={
        "status":"REVERSIBLE_NORMALIZATION_FEASIBILITY_ONLY",
        "corrections_applied":False,
        "source_delivery_changed":False,
        "normalization":"remove Unicode Mn combining marks in internal model view only",
        "summary":{
            "unique_texts":len(texts),
            "words_total":total,
            "words_with_combining_marks":with_marks,
            "original_UNK_words":orig_unk,
            "normalized_UNK_words":norm_unk,
            "UNK_words_resolved":resolved,
            "new_UNK_words_introduced":new_unk,
        },
        "rows":rows,
        "next_rule":"Only consider edit projection on normalized view if round-trip source offsets are exact and scientific/protected spans remain locked."
    }
    p=ART/"REVERSIBLE_NORMALIZATION_PROBE.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"normalization_probe":result["summary"],"output":str(p)},ensure_ascii=False))


if __name__=="__main__":
    main()
