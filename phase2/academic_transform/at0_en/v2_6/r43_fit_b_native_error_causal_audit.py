#!/usr/bin/env python3
"""Read-only FIT-only replay of frozen Stage-A BIO model.

No training, no SELECT/DEV/TEST. Check native candidate error blind spot.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib
import torch
from transformers import AutoTokenizer,BertForTokenClassification

from r43_contextual_pair_preflight import parse_train,spans_for_sentence
from r43_stage_b_h0_h1_diagnostic import make_sentence_rows,infer_b,word_batch,first_positions,BID2,overlap

TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
SPLIT_SHA="fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226"
B_SHA="4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05"

def file_sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--train",type=pathlib.Path,required=True)
    p.add_argument("--split",type=pathlib.Path,required=True)
    p.add_argument("--b-model",type=pathlib.Path,required=True)
    p.add_argument("--out",type=pathlib.Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)

    assert file_sha(args.train)==TRAIN_SHA
    assert file_sha(args.b_model/"model.safetensors")==B_SHA
    split=json.loads(args.split.read_text())
    assert split["manifest_sha256"]==SPLIT_SHA
    fit=set()
    for e in split["entries"]:
        if e["partition"]=="FIT":fit.update(e["documents"])
    assert len(fit)==320
    docs,empty,bad=parse_train(args.train)
    assert len(docs)==400 and not bad

    tok=AutoTokenizer.from_pretrained(args.b_model,local_files_only=True,use_fast=True)
    model=BertForTokenClassification.from_pretrained(args.b_model,local_files_only=True)
    model.eval()
    sents=make_sentence_rows(docs,fit)
    preds=infer_b(model,tok,sents)

    totals=collections.Counter()
    class_totals=collections.defaultdict(collections.Counter)
    sample_err=[]
    goldless_fp_count=0
    for di in sorted(fit):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            gold,bad,_=spans_for_sentence(doc,si)
            if bad:raise RuntimeError(f"bad gold source BIO {di}/{si}")
            g={(c,s,e) for c,s,e in gold}
            q=preds[(di,si)]
            no_gold=(len(g)==0)
            totals["sentences"]+=1
            totals["goldless_sentences" if no_gold else "gold_bearing_sentences"]+=1
            totals["gold_entities"]+=len(g)
            totals["proposals"]+=len(q)
            for pp in q:
                typ,s,e=pp["type"],pp["start"],pp["end"]
                if (typ,s,e) in g:
                    totals["exact_proposals"]+=1
                    class_totals[typ]["exact"]+=1
                    continue
                totals["false_proposals"]+=1
                class_totals[typ]["false"]+=1
                if no_gold:
                    totals["false_proposals_in_goldless_sentences"]+=1
                    class_totals[typ]["false_goldless"]+=1
                    if len(sample_err)<10:
                        sample_err.append({"document":di,"sentence":si,"class":typ,"start":s,"end":e,
                                           "kind":"GOLDLESS_SENTENCE","conf":pp["b_conf"]})
                else:
                    totals["false_proposals_in_gold_bearing_sentences"]+=1
                    class_totals[typ]["false_gold_bearing"]+=1
                    if any(overlap(s,e,gs,ge) for _,gs,ge in g):
                        totals["false_overlap_gold"]+=1
                    else:
                        totals["false_spurious_in_gold_bearing_sentence"]+=1
                    if len(sample_err)<10:
                        sample_err.append({"document":di,"sentence":si,"class":typ,"start":s,"end":e,
                                           "kind":"GOLD_BEARING_SENTENCE","conf":pp["b_conf"]})

    # Raw predicted BIO transition audit on FIT.
    transitions=collections.Counter()
    invalid_examples=[]
    with torch.no_grad():
        for k in range(0,len(sents),8):
            chunk=sents[k:k+8]
            enc=word_batch(tok,[r["tokens"] for r in chunk])
            pro=model(**enc).logits.argmax(-1)
            for bi,row in enumerate(chunk):
                wpos=first_positions(enc,bi,len(row["tokens"]))
                pred=[BID2[int(pro[bi,j])] for j in wpos]
                prev="O"
                for wi,tag in enumerate(pred):
                    if tag.startswith("I-"):
                        typ=tag[2:]
                        if prev not in (f"B-{typ}",f"I-{typ}"):
                            transitions["invalid_I_transition"]+=1
                            transitions["initial" if wi==0 else "internal"]+=1
                            if len(invalid_examples)<8:
                                invalid_examples.append({"document":row["doc"],"sentence":row["sent"],"word_index":wi,
                                                         "previous_predicted":prev,"predicted":tag})
                    prev=tag
                transitions["predicted_words"]+=len(pred)

    eligible=totals["false_proposals_in_gold_bearing_sentences"]
    missed=totals["false_proposals_in_goldless_sentences"]
    out={"state":"R43_FIT_ONLY_B_NATIVE_ERROR_CAUSAL_AUDIT_COMPLETE",
         "source_B_sha256":B_SHA,"source_TRAIN_sha256":TRAIN_SHA,"source_split_sha256":SPLIT_SHA,
         "FIT_documents":len(fit),"totals":dict(totals),
         "per_class":{c:dict(x) for c,x in sorted(class_totals.items())},
         "invalid_BIO_transitions":dict(transitions),"invalid_examples":invalid_examples,
         "example_false_proposals":sample_err,
         "native_slot_analysis":{
           "false_proposals_in_gold_bearing_sentences_are_eligible":eligible,
           "false_proposals_in_goldless_sentences_cannot_be_selected_under_current_code":missed,
           "mechanism":"materialize_final_fit_examples loops only over positive gold spans and scans same-sentence proposals",
           "required_remedy":"TRAIN-only group-disjoint OOF candidate mining, plus coverage of goldless sentences; future protocol only"
         },
         "guards":{"stage_a_unchanged":True,"fit_only":True,"SELECT_read":False,
                    "historical_DEV_read":False,"protected_TEST_read":False,
                    "FactPICO_read":False,"scientific_training":False}}
    (args.out/"R43_FIT_B_NATIVE_ERROR_CAUSAL_AUDIT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":main()
