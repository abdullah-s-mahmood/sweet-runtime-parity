#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import torch
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

VERSION="MPSEF_P2_V2_REAL_MODEL_STAGE0_V1"
EXPECTED_GED_WEIGHT_SHA="23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f"
EXPECTED_GEC_WEIGHT_SHA="5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f"
GED_MAX_SEQ_LENGTH=256
IGNORE_INDEX=-100


class Stage0Error(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def sha_json(obj) -> str:
    raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def morph_words(disambig, text: str):
    src_words=text.split()
    dis=disambig.disambiguate(src_words)
    if len(dis)!=len(src_words):
        raise Stage0Error(f"MORPH_COUNT_MISMATCH:{len(src_words)}!={len(dis)}")
    out=[]
    for i,item in enumerate(dis):
        if not item.analyses:
            raise Stage0Error(f"MORPH_NO_ANALYSIS:{i}")
        out.append(dediac_ar(item.analyses[0].analysis["diac"]))
    if len(out)!=len(src_words):
        raise Stage0Error("MORPH_OUTPUT_COUNT_MISMATCH")
    return out


def build_ged_segments(words, tokenizer, max_seq_length=GED_MAX_SEQ_LENGTH):
    budget=max_seq_length-2
    if budget<=0:
        raise Stage0Error("GED_INVALID_BUDGET")
    per_word=[]
    for wi,word in enumerate(words):
        pieces=tokenizer.tokenize(word)
        if len(pieces)==0:
            raise Stage0Error(f"GED_ZERO_TOKEN_WORD:{wi}")
        if len(pieces)>budget:
            raise Stage0Error(f"GED_SINGLE_WORD_OVER_BUDGET:{wi}:{len(pieces)}>{budget}")
        per_word.append((wi,word,pieces))

    raw_segments=[]
    current=[]
    n=0
    for rec in per_word:
        pieces=rec[2]
        if current and n+len(pieces)>budget:
            raw_segments.append(current)
            current=[]
            n=0
        current.append(rec)
        n+=len(pieces)
    if current:
        raw_segments.append(current)

    segments=[]
    flattened=[]
    for sid,seg in enumerate(raw_segments):
        tokens=[tokenizer.cls_token]
        token_type_ids=[0]  # single-sequence BERT segment id; tokenizer need not expose cls_token_type_id
        label_mask=[IGNORE_INDEX]
        records=[]
        pos=1
        for wi,word,pieces in seg:
            start=pos
            end=pos+len(pieces)
            records.append({
                "morph_word_index":wi,
                "morph_word_text":word,
                "ged_segment_id":sid,
                "ged_wordpiece_start":start,
                "ged_wordpiece_end":end,
                "ged_first_wordpiece_index":start,
                "ged_wordpieces":pieces,
            })
            tokens.extend(pieces)
            token_type_ids.extend([0]*len(pieces))
            label_mask.append(0)
            label_mask.extend([IGNORE_INDEX]*(len(pieces)-1))
            flattened.append(wi)
            pos=end

        tokens.append(tokenizer.sep_token)
        token_type_ids.append(0)
        label_mask.append(IGNORE_INDEX)
        input_ids=tokenizer.convert_tokens_to_ids(tokens)
        attention_mask=[1]*len(input_ids)

        if not (len(input_ids)==len(attention_mask)==len(token_type_ids)==len(label_mask)):
            raise Stage0Error("GED_SEGMENT_FIELD_LENGTH_MISMATCH")
        if len(input_ids)>max_seq_length:
            raise Stage0Error(f"GED_SEGMENT_OVERFLOW:{len(input_ids)}>{max_seq_length}")
        segments.append({
            "segment_id":sid,
            "input_ids":input_ids,
            "attention_mask":attention_mask,
            "token_type_ids":token_type_ids,
            "label_mask":label_mask,
            "word_records":records,
            "total_encoded_length":len(input_ids),
            "content_wordpieces":len(input_ids)-2,
        })

    if flattened!=list(range(len(words))):
        raise Stage0Error(f"GED_WORD_BIJECTION_FAILED:{flattened}")
    return segments


def infer_word_level_ged(words, tokenizer, model):
    segments=build_ged_segments(words,tokenizer)
    by_word={}
    trace=[]
    with torch.no_grad():
        for seg in segments:
            ids=torch.tensor([seg["input_ids"]],dtype=torch.long)
            mask=torch.tensor([seg["attention_mask"]],dtype=torch.long)
            types=torch.tensor([seg["token_type_ids"]],dtype=torch.long)
            logits=model(input_ids=ids,attention_mask=mask,token_type_ids=types).logits[0]
            pred_ids=logits.argmax(dim=-1).tolist()
            if len(pred_ids)!=len(seg["input_ids"]):
                raise Stage0Error("GED_LOGIT_LENGTH_MISMATCH")
            for wr in seg["word_records"]:
                wi=wr["morph_word_index"]
                if wi in by_word:
                    raise Stage0Error(f"GED_DUPLICATE_WORD_INDEX:{wi}")
                p=wr["ged_first_wordpiece_index"]
                if seg["label_mask"][p]==IGNORE_INDEX:
                    raise Stage0Error("GED_FIRST_WORDPIECE_MASKED")
                for q in range(wr["ged_wordpiece_start"]+1,wr["ged_wordpiece_end"]):
                    if seg["label_mask"][q]!=IGNORE_INDEX:
                        raise Stage0Error("GED_NONFIRST_WORDPIECE_UNMASKED")
                pid=int(pred_ids[p])
                label=model.config.id2label[pid]
                by_word[wi]=label
                trace.append({
                    **wr,
                    "ged_prediction_position":p,
                    "ged_label_id":pid,
                    "ged_label_name":label,
                })

    if set(by_word)!=set(range(len(words))):
        raise Stage0Error(f"GED_WORD_COVERAGE_FAILED:{sorted(by_word)}")
    labels=[by_word[i] for i in range(len(words))]
    if len(labels)!=len(words):
        raise Stage0Error("GED_WORD_LABEL_COUNT_MISMATCH")
    trace=sorted(trace,key=lambda x:x["morph_word_index"])
    for i,r in enumerate(trace):
        if r["morph_word_index"]!=i or r["morph_word_text"]!=words[i]:
            raise Stage0Error("GED_WORD_IDENTITY_ORDER_OR_TEXT_MISMATCH")
    return labels,segments,trace


def project_to_gec(words, labels, tokenizer, model):
    if len(words)!=len(labels):
        raise Stage0Error("GEC_WORD_LABEL_COUNT_MISMATCH")
    label2id=dict(model.config.ged_label2id)
    if "UC" not in label2id:
        raise Stage0Error("GEC_UC_LABEL_MISSING")
    tokens=[]
    expanded_names=[]
    word_map=[]
    for wi,(word,label) in enumerate(zip(words,labels)):
        pieces=tokenizer.tokenize(word)
        if not pieces:
            raise Stage0Error(f"GEC_ZERO_TOKEN_WORD:{wi}")
        if label not in label2id:
            raise Stage0Error(f"GEC_UNKNOWN_GED_LABEL:{label}")
        start=len(tokens)+1
        tokens.extend(pieces)
        expanded_names.extend([label]*len(pieces))
        end=len(tokens)+1
        word_map.append({
            "morph_word_index":wi,
            "morph_word_text":word,
            "gec_subword_start":start,
            "gec_subword_end":end,
            "gec_subwords":pieces,
        })

    input_ids=[tokenizer.bos_token_id,*tokenizer.convert_tokens_to_ids(tokens),tokenizer.eos_token_id]
    label_names=["UC",*expanded_names,"UC"]
    label_ids=[label2id[x] for x in label_names]
    attention_mask=[1]*len(input_ids)
    if not(len(input_ids)==len(label_ids)==len(attention_mask)):
        raise Stage0Error("GEC_CONDITIONING_LENGTH_MISMATCH")

    maxpos=getattr(model.config,"max_position_embeddings",None)
    if isinstance(maxpos,int) and len(input_ids)>maxpos:
        raise Stage0Error(f"GEC_INPUT_TOO_LONG:{len(input_ids)}>{maxpos}")
    return {
        "tokens":tokens,
        "input_ids":input_ids,
        "ged_label_names":label_names,
        "ged_label_ids":label_ids,
        "attention_mask":attention_mask,
        "word_map":word_map,
    }


def inspect_generation_config(model, tokenizer):
    cfg=model.config
    return {
        "decoder_start_token_id":cfg.decoder_start_token_id,
        "bos_token_id":cfg.bos_token_id,
        "eos_token_id":cfg.eos_token_id,
        "pad_token_id":cfg.pad_token_id,
        "tokenizer_bos_token_id":tokenizer.bos_token_id,
        "tokenizer_eos_token_id":tokenizer.eos_token_id,
        "tokenizer_pad_token_id":tokenizer.pad_token_id,
        "num_beams":5,
        "max_length":100,
        "num_return_sequences":1,
        "no_repeat_ngram_size":0,
        "early_stopping":False,
    }


def generate_with_ged_hook(tokenizer, model, prepared):
    encoder=model.model.encoder
    if not hasattr(encoder,"embed_ged_tags"):
        raise Stage0Error("GEC_GED_EMBEDDING_LAYER_MISSING")

    hook_calls=[]
    def hook(module,inputs,output):
        hook_calls.append({
            "input_shape":list(inputs[0].shape) if inputs else None,
            "output_shape":list(output.shape),
        })

    handle=encoder.embed_ged_tags.register_forward_hook(hook)
    try:
        with torch.no_grad():
            generated=model.generate(
                torch.tensor([prepared["input_ids"]],dtype=torch.long),
                num_beams=5,
                max_length=100,
                num_return_sequences=1,
                no_repeat_ngram_size=0,
                early_stopping=False,
                ged_tags=torch.tensor([prepared["ged_label_ids"]],dtype=torch.long),
                attention_mask=torch.tensor([prepared["attention_mask"]],dtype=torch.long),
            )
    finally:
        handle.remove()

    if not hook_calls:
        raise Stage0Error("GEC_GED_TAGS_NOT_CONSUMED_DURING_GENERATE")

    raw=generated[0].tolist()
    cfg=inspect_generation_config(model,tokenizer)
    prefix_len=1
    eos=cfg["eos_token_id"]
    body=raw[prefix_len:]
    eos_positions=[i+prefix_len for i,tok in enumerate(body) if tok==eos]
    if not eos_positions:
        raise Stage0Error("GEC_TERMINAL_EOS_UNPROVEN")
    terminal=eos_positions[0]
    hit_ceiling=len(raw)>=cfg["max_length"]
    if hit_ceiling and terminal==len(raw)-1:
        raise Stage0Error("GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED")

    text=tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]
    return {
        "generated_token_ids":raw,
        "terminal_eos_index":terminal,
        "hit_ceiling":hit_ceiling,
        "decoder_prefix_equals_eos":cfg["decoder_start_token_id"]==eos,
        "ged_embedding_hook_calls":hook_calls,
        "decoded_text":text,
        "effective_generation_config":cfg,
    }


def run(args):
    ged_weight=sha256_file(Path(args.ged_model_dir)/"pytorch_model.bin")
    gec_weight=sha256_file(Path(args.gec_model_dir)/"pytorch_model.bin")
    if ged_weight!=EXPECTED_GED_WEIGHT_SHA:
        raise Stage0Error(f"GED_WEIGHT_SHA_MISMATCH:{ged_weight}")
    if gec_weight!=EXPECTED_GEC_WEIGHT_SHA:
        raise Stage0Error(f"GEC_WEIGHT_SHA_MISMATCH:{gec_weight}")

    ged_tokenizer=AutoTokenizer.from_pretrained(args.ged_model_dir)
    ged_model=BertForTokenClassification.from_pretrained(args.ged_model_dir)
    ged_model.eval()
    gec_tokenizer=AutoTokenizer.from_pretrained(args.gec_model_dir)
    gec_model=MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    gec_model.eval()

    disambig=BERTUnfactoredDisambiguator.pretrained(
        model_name="msa",use_gpu=False,pretrained_cache=False
    )

    ged_id2label={str(k):v for k,v in ged_model.config.id2label.items()}
    ged_label2id={str(k):int(v) for k,v in ged_model.config.label2id.items()}
    gec_ged_label2id={str(k):int(v) for k,v in gec_model.config.ged_label2id.items()}

    identities={
        "ged_weight_sha256":ged_weight,
        "gec_weight_sha256":gec_weight,
        "ged_config_sha256":hashlib.sha256(ged_model.config.to_json_string().encode()).hexdigest(),
        "gec_config_sha256":hashlib.sha256(gec_model.config.to_json_string().encode()).hexdigest(),
        "ged_id2label_sha256":sha_json(ged_id2label),
        "ged_label2id_sha256":sha_json(ged_label2id),
        "gec_ged_label2id_sha256":sha_json(gec_ged_label2id),
        "ged_tokenizer_class":type(ged_tokenizer).__name__,
        "gec_tokenizer_class":type(gec_tokenizer).__name__,
        "ged_vocab_size":len(ged_tokenizer),
        "gec_vocab_size":len(gec_tokenizer),
        "ged_max_seq_length_contract":GED_MAX_SEQ_LENGTH,
        "gec_has_embed_ged_tags":hasattr(gec_model.model.encoder,"embed_ged_tags"),
    }

    # Public/synthetic examples only; no C_F/project source.
    sources=[
        "و قال له انه يحب اكل الطعام بكثره .",
        "هذه جمله بسيطه للاختبار .",
        "الجرعة 5 mg يوميا .",
    ]

    rows=[]
    for sid,source in enumerate(sources):
        words=morph_words(disambig,source)
        labels,segments,ged_trace=infer_word_level_ged(words,ged_tokenizer,ged_model)
        if len(labels)!=len(words):
            raise Stage0Error("REAL_GED_WORD_LABEL_COUNT_MISMATCH")
        prepared=project_to_gec(words,labels,gec_tokenizer,gec_model)
        gen=generate_with_ged_hook(gec_tokenizer,gec_model,prepared)

        rows.append({
            "synthetic_id":f"SYN-{sid+1:02d}",
            "source":source,
            "source_sha256":hashlib.sha256(source.encode()).hexdigest(),
            "morph_words":words,
            "morph_word_count":len(words),
            "word_level_ged_labels":labels,
            "ged_label_count":len(labels),
            "ged_segments":segments,
            "ged_word_identity_trace":ged_trace,
            "gec_word_map":prepared["word_map"],
            "gec_input_length":len(prepared["input_ids"]),
            "gec_label_length":len(prepared["ged_label_ids"]),
            "generation":gen,
        })

    # Repeat determinism on first synthetic source.
    first=rows[0]
    words=first["morph_words"]
    labels2,segments2,trace2=infer_word_level_ged(words,ged_tokenizer,ged_model)
    prepared2=project_to_gec(words,labels2,gec_tokenizer,gec_model)
    gen2=generate_with_ged_hook(gec_tokenizer,gec_model,prepared2)
    repeat_pass=(
        labels2==first["word_level_ged_labels"]
        and segments2==first["ged_segments"]
        and trace2==first["ged_word_identity_trace"]
        and prepared2["input_ids"]==[
            gec_tokenizer.bos_token_id,
            *gec_tokenizer.convert_tokens_to_ids(prepared2["tokens"]),
            gec_tokenizer.eos_token_id,
        ]
        and gen2["generated_token_ids"]==first["generation"]["generated_token_ids"]
    )
    if not repeat_pass:
        raise Stage0Error("REAL_MODEL_REPEAT_PARITY_FAILED")

    summary={
        "record_id":VERSION,
        "status":"PASS",
        "synthetic_sources":len(rows),
        "identities":identities,
        "rows":rows,
        "repeat_parity_first_source":True,
        "project_source_loaded":False,
        "project_gold_loaded":False,
        "project_metric_computed":False,
        "real_model_inference_run":True,
        "quality_claimed":False,
    }
    Path(args.out).write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "record_id":VERSION,
        "status":"PASS",
        "synthetic_sources":len(rows),
        "identities":identities,
        "repeat_parity_first_source":True,
        "project_source_loaded":False,
        "project_gold_loaded":False,
        "project_metric_computed":False,
        "real_model_inference_run":True,
        "quality_claimed":False,
    },ensure_ascii=False,indent=2))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ged-model-dir",required=True)
    ap.add_argument("--gec-model-dir",required=True)
    ap.add_argument("--out",default="MPSEF_P2_V2_REAL_MODEL_STAGE0_RESULT.json")
    args=ap.parse_args()
    run(args)


if __name__=="__main__":
    main()
