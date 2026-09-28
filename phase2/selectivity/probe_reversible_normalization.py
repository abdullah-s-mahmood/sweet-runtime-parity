"""Reversible normalization feasibility probe for Phase 2 Selective Surgical Gate.

No correction is applied. The probe asks whether NoPnx tokenizer [UNK] hazards
become tokenizable after removing Arabic combining marks/tatweel from an
internal model view while retaining an exact source-index map.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
from transformers import BertTokenizer

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
QUEUE=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl"
TOKDIR=ROOT/"models"/"nopnx"
ART=ROOT/"artifacts"


def read_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def normalize_view(word):
    chars=[]; mapping=[]; removed=[]
    for i,ch in enumerate(word):
        if ch=="\u0640" or unicodedata.category(ch)=="Mn":
            removed.append({"source_index":i,"char":ch,"name":unicodedata.name(ch,"UNKNOWN")})
            continue
        chars.append(ch); mapping.append(i)
    return "".join(chars),mapping,removed


def main():
    tok=BertTokenizer.from_pretrained(str(TOKDIR),local_files_only=True)
    queue=read_jsonl(QUEUE)
    hazards=[]
    for item in queue:
        for h in item["variants"]["nopnx1"]["suppressed_hazards"]:
            if h.get("reason")!="TOKENIZER_UNK_WORD":
                continue
            word=h["word"]
            original_tokens=tok.tokenize(word)
            norm,mapping,removed=normalize_view(word)
            norm_tokens=tok.tokenize(norm)
            recovered=bool(norm_tokens) and tok.unk_token not in norm_tokens
            hazards.append({
                "passage_id":item["passage_id"],
                "word_index":h.get("word_index"),
                "source_word":word,
                "labels":h.get("labels",[]),
                "original_tokens":original_tokens,
                "normalized_model_view":norm,
                "source_index_map":mapping,
                "removed_source_chars":removed,
                "normalized_tokens":norm_tokens,
                "tokenizable_after_normalization":recovered,
                "roundtrip_policy":"Source text remains authoritative; normalized view is never delivered.",
            })
    result={
        "status":"DEVELOPMENT_REVERSIBLE_NORMALIZATION_PROBE",
        "no_edits_applied":True,
        "hazards":len(hazards),
        "tokenizable_after_normalization":sum(x["tokenizable_after_normalization"] for x in hazards),
        "still_unk_after_normalization":sum(not x["tokenizable_after_normalization"] for x in hazards),
        "normalization":"remove Unicode combining marks and Arabic tatweel in internal model view only",
        "important_limit":"Tokenizability recovery does not prove a normalized-model edit can be projected safely; actual edit application remains disabled.",
        "rows":hazards,
    }
    ART.mkdir(parents=True,exist_ok=True)
    p=ART/"REVERSIBLE_NORMALIZATION_PROBE.json"
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},ensure_ascii=False))


if __name__=="__main__":
    main()
