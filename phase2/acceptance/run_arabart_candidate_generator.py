"""Run the official CAMeL-Lab AraBART+Morph+GED pipeline on Phase 2 development passages.

DEVELOPMENT ONLY.

This script:
- never reads Nahw target corrections or human adjudication labels;
- generates one AraBART correction hypothesis per unique source passage;
- keeps the original source authoritative;
- aligns generated text back to source-local whitespace-token regions;
- emits AraBART output as independent candidate evidence, never as product text.

It follows the public CAMeL-Lab arabic-gec README architecture:
contextual morphology -> GED-13 -> AraBART+GED generation.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import platform
import re
import subprocess
import unicodedata
from pathlib import Path

import torch
import torch.nn.functional as F
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

ROOT=Path(__file__).resolve().parents[2]
AR=ROOT/"phase2"/"arabic_eval"
DEV=AR/"DEVELOPMENT_TARGETS.jsonl"
ART=ROOT/"artifacts"

GED_MODEL="CAMeL-Lab/camelbert-msa-qalb14-ged-13"
GEC_MODEL="CAMeL-Lab/arabart-qalb14-gec-ged-13"
UPSTREAM_COMMIT="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"


def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def strip_marks(s):
    return "".join(ch for ch in s if unicodedata.category(ch)!="Mn" and ch!="\u0640")


def canon_token(s):
    s=strip_marks(s)
    # Keep Arabic/Latin letters and digits; punctuation is alignment noise.
    return "".join(ch for ch in s if ch.isalnum() or "\u0600" <= ch <= "\u06ff")


def word_spans(text):
    ms=list(re.finditer(r"\S+",text))
    return [(m.start(),m.end(),m.group(0)) for m in ms]


def morph_preprocess(text,disambig):
    words=text.split()
    dis=disambig.disambiguate(words)
    out=[]
    diagnostics=[]
    for src,d in zip(words,dis):
        if d.analyses:
            analysis=d.analyses[0].analysis
            diac=analysis.get("diac",src)
            pp=dediac_ar(diac)
            out.append(pp)
            diagnostics.append({"source":src,"diac":diac,"model_view":pp,"analysis":{k:analysis.get(k) for k in ("lex","pos","cas","mod","stt","gen","num","per","asp","vox")}})
        else:
            out.append(dediac_ar(src))
            diagnostics.append({"source":src,"diac":src,"model_view":dediac_ar(src),"analysis":None})
    if len(out)!=len(words):
        raise RuntimeError("morph preprocessing word count mismatch")
    return out,diagnostics


def ged_labels_for_words(words,tokenizer,model):
    """One GED label per whitespace word using the first WordPiece."""
    pieces=[]
    starts=[]
    for w in words:
        wp=tokenizer.tokenize(w)
        if not wp:
            wp=[tokenizer.unk_token]
        starts.append(len(pieces))
        pieces.extend(wp)
    ids=tokenizer.convert_tokens_to_ids(pieces)
    input_ids=[tokenizer.cls_token_id]+ids+[tokenizer.sep_token_id]
    attention=[1]*len(input_ids)
    token_type=[0]*len(input_ids)
    with torch.no_grad():
        logits=model(
            input_ids=torch.tensor([input_ids]),
            attention_mask=torch.tensor([attention]),
            token_type_ids=torch.tensor([token_type]),
        ).logits[0]
        probs=F.softmax(logits,dim=-1)
    labels=[]
    details=[]
    for wi,pi in enumerate(starts):
        ti=1+pi
        score,pred=probs[ti].max(dim=-1)
        label=model.config.id2label[int(pred)]
        labels.append(label)
        details.append({"word_index":wi,"word":words[wi],"label":label,"score":float(score)})
    return labels,details


def generate_one(text,disambig,ged_tok,ged_model,gec_tok,gec_model):
    morph_words,morph_diag=morph_preprocess(text,disambig)
    ged_labels,ged_diag=ged_labels_for_words(morph_words,ged_tok,ged_model)

    ged_label2ids=gec_model.config.ged_label2id
    tokens=[]
    extended=[]
    token_to_word=[]
    for wi,(word,label) in enumerate(zip(morph_words,ged_labels)):
        wtokens=gec_tok.tokenize(word)
        if not wtokens:
            continue
        tokens.extend(wtokens)
        extended.extend([label]*len(wtokens))
        token_to_word.extend([wi]*len(wtokens))

    input_ids=gec_tok.convert_tokens_to_ids(tokens)
    input_ids=[gec_tok.bos_token_id]+input_ids+[gec_tok.eos_token_id]
    label_ids=[ged_label2ids.get(x,ged_label2ids["<pad>"]) for x in extended]
    label_ids=[ged_label2ids["UC"]]+label_ids+[ged_label2ids["UC"]]
    attention=[1]*len(input_ids)

    gen_kwargs={
        "num_beams":5,
        "max_length":min(1024,max(128,len(input_ids)*3)),
        "num_return_sequences":1,
        "no_repeat_ngram_size":0,
        "early_stopping":False,
        "ged_tags":torch.tensor([label_ids]),
        "attention_mask":torch.tensor([attention]),
    }
    with torch.no_grad():
        generated=gec_model.generate(torch.tensor([input_ids]),**gen_kwargs)
    out=gec_tok.batch_decode(generated,skip_special_tokens=True,clean_up_tokenization_spaces=False)[0]
    return out,{
        "morph_words":morph_words,
        "morphology":morph_diag,
        "ged":ged_diag,
        "gec_input_tokens":tokens,
        "gec_input_token_to_word":token_to_word,
    }


def align_words(source,generated):
    src=source.split()
    out=generated.split()
    src_keys=[canon_token(x) for x in src]
    out_keys=[canon_token(x) for x in out]
    sm=difflib.SequenceMatcher(None,src_keys,out_keys,autojunk=False)
    regions=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=="equal":
            continue
        regions.append({
            "tag":tag,
            "source_word_span":[i1,i2],
            "output_word_span":[j1,j2],
            "source_words":src[i1:i2],
            "output_words":out[j1:j2],
            "source_canonical":src_keys[i1:i2],
            "output_canonical":out_keys[j1:j2],
        })
    return regions


def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=ART/"ARABART_INDEPENDENT_GENERATOR.json")
    ap.add_argument("--model-revisions",type=Path,default=ART/"ACCEPTANCE_MODEL_REVISIONS.json")
    args=ap.parse_args()

    ART.mkdir(parents=True,exist_ok=True)
    dev=read_jsonl(DEV)
    passages={}
    for r in dev:
        passages.setdefault(int(r["passage_id"]),r["source"])
    assert len(dev)==150 and len(passages)==41

    repo=ROOT/"upstream"/"arabic-gec"
    commit=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    if commit!=UPSTREAM_COMMIT:
        raise RuntimeError(f"arabic-gec pin mismatch {commit}")

    disambig=BERTUnfactoredDisambiguator.pretrained()
    ged_tok=AutoTokenizer.from_pretrained(GED_MODEL)
    ged_model=BertForTokenClassification.from_pretrained(GED_MODEL).eval().cpu()
    gec_tok=AutoTokenizer.from_pretrained(GEC_MODEL)
    gec_model=MBartForConditionalGeneration.from_pretrained(GEC_MODEL).eval().cpu()

    results={}
    for n,(pid,source) in enumerate(sorted(passages.items()),1):
        print(f"[{n}/41] passage={pid}",flush=True)
        generated,trace=generate_one(source,disambig,ged_tok,ged_model,gec_tok,gec_model)
        results[str(pid)]={
            "source":source,
            "generated":generated,
            "changed":generated!=source,
            "alignment_regions":align_words(source,generated),
            "trace":trace,
        }

    revisions=json.loads(args.model_revisions.read_text(encoding="utf-8")) if args.model_revisions.exists() else None
    obj={
        "status":"DEVELOPMENT_ARABART_INDEPENDENT_GENERATOR_COMPLETE",
        "source_authoritative":True,
        "full_generated_output_auto_applied":False,
        "unique_passages":41,
        "runtime":{
            "python":platform.python_version(),
            "torch":torch.__version__,
            "arabic_gec_commit":commit,
            "ged_model":GED_MODEL,
            "gec_model":GEC_MODEL,
            "resolved_model_revisions":revisions,
        },
        "passages":results,
        "limitations":[
            "AraBART output is independent candidate evidence only; full generated sentences are never accepted directly.",
            "Whitespace-token SequenceMatcher alignment is a development local-evidence representation, not a production edit aligner.",
            "No Nahw target or human adjudication label is read by this generator.",
        ],
    }
    args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":obj["status"],
        "passages":41,
        "changed_passages":sum(x["changed"] for x in results.values()),
        "alignment_regions":sum(len(x["alignment_regions"]) for x in results.values()),
        "output":str(args.output),
    },ensure_ascii=False))


if __name__=="__main__":
    main()
