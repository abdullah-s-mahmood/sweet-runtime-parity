#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, gc, hashlib, json, math, os, pathlib, random, sys, time
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import AutoConfig, AutoTokenizer, BertModel, BertForTokenClassification, Trainer, TrainerCallback, TrainingArguments


SEED=44
CLASSES=["P","I","C","O"]
BIO_LABELS=["O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"]
BIO2ID={x:i for i,x in enumerate(BIO_LABELS)}
BOUNDARY_LABELS=["OUT","START","END","BOTH","IN"]
BOUNDARY2ID={x:i for i,x in enumerate(BOUNDARY_LABELS)}
EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_R44_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_CONVERTED_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"

def now(): return datetime.now(timezone.utc).isoformat()
def sha256_path(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def sha_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def write_json(path,obj):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(t,p)
def seed_all():
    os.environ["PYTHONHASHSEED"]=str(SEED)
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True,warn_only=True); torch.set_num_threads(2)
def overlap(a,b,c,d): return max(a,c)<min(b,d)

def source_spans(tags):
    out=[]; i=0
    while i<len(tags):
        tag=tags[i]
        if tag.startswith("B-"):
            typ=tag[2:]; j=i+1
            while j<len(tags) and tags[j]==f"I-{typ}": j+=1
            out.append((typ,i,j)); i=j
        else: i+=1
    return out

def source_boundary_tags(tags):
    y=["OUT"]*len(tags)
    for _,s,e in source_spans(tags):
        if e-s==1: y[s]="BOTH"
        else:
            y[s]="START"; y[e-1]="END"
            for i in range(s+1,e-1): y[i]="IN"
    return y

def section_labels(doc):
    cur="UNKNOWN"; out=[]
    for tokens,tags in doc:
        if tokens and tokens[0].lower()=="title": cur="TITLE"
        elif tokens and tokens[0].lower() in {"method","methods"}: cur="METHODS"
        out.append(cur)
    return out

class TokenDataset(torch.utils.data.Dataset):
    def __init__(self,rows,tokenizer,mode):
        self.items=[]
        mapper=BIO2ID if mode=="bio" else BOUNDARY2ID
        for tokens,tags,bound in rows:
            target=tags if mode=="bio" else bound
            enc=tokenizer(tokens,is_split_into_words=True,truncation=True,max_length=256,
                          padding="max_length",return_attention_mask=True)
            wids=enc.word_ids(); seen=set(); labels=[]; first=[]
            for wid in wids:
                if wid is None: labels.append(-100)
                elif wid not in seen:
                    seen.add(wid); first.append(wid); labels.append(mapper[target[wid]])
                else: labels.append(-100)
            if len(first)!=len(tokens): raise RuntimeError(f"{mode} truncation {len(first)} != {len(tokens)}")
            enc["labels"]=labels
            self.items.append({k:torch.tensor(v) for k,v in enc.items()})
    def __len__(self): return len(self.items)
    def __getitem__(self,i): return self.items[i]

class Progress(TrainerCallback):
    def __init__(self,path,module,offset,width):
        self.path=pathlib.Path(path); self.module=module; self.offset=offset; self.width=width
        self.started=time.time(); self.last=-1; self.latest=None
    def emit(self,state,stage,force=False):
        step=int(state.global_step or 0); total=int(state.max_steps or 0)
        if not force and step==self.last:return
        frac=step/total if total else 0.0
        pct=100*(self.offset+self.width*frac)/13.0
        payload={"state":"RUNNING","current_stage":stage,"active_module":self.module,
                 "progress_percent":round(pct,2),"current_epoch":float(state.epoch or 0),
                 "global_step":step,"total_steps":total or None,"latest_loss":self.latest,
                 "last_progress_at":now(),"failure_or_stall_reason":None}
        write_json(self.path,payload)
        print("PROCESS_STATUS "+json.dumps(payload,sort_keys=True),file=sys.stderr,flush=True)
        self.last=step
    def on_log(self,args,state,control,logs=None,**kwargs):
        if logs and isinstance(logs.get("loss"),(float,int)):self.latest=float(logs["loss"])
        self.emit(state,"TRAINING_LOG",True)
    def on_step_end(self,args,state,control,**kwargs):
        if int(state.global_step or 0)%10==0:self.emit(state,"TRAINING")
    def on_train_end(self,args,state,control,**kwargs):self.emit(state,"MODULE_TRAINING_COMPLETE",True)

def convert_base(model_dir,out):
    seed_all()
    base=BertModel.from_pretrained(model_dir,from_flax=True,local_files_only=True)
    if any(not torch.isfinite(p).all() for p in base.parameters()): raise RuntimeError("nonfinite base")
    out=pathlib.Path(out); out.mkdir(parents=True,exist_ok=False)
    base.save_pretrained(out,safe_serialization=True)
    tok=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,use_fast=True); tok.save_pretrained(out)
    got=sha256_path(out/"model.safetensors")
    if got!=EXPECTED_CONVERTED_SHA: raise RuntimeError(f"converted base mismatch {got}")
    del base; gc.collect(); return tok

def train_token(name,converted,dataset,out_dir,lr,wd,epochs,batch,status,offset,width):
    seed_all()
    labels=BIO_LABELS if name=="B_CANDIDATE" else BOUNDARY_LABELS
    mapper=BIO2ID if name=="B_CANDIDATE" else BOUNDARY2ID
    cfg=AutoConfig.from_pretrained(converted,local_files_only=True,num_labels=len(labels),
        id2label={i:x for i,x in enumerate(labels)},label2id=mapper)
    model=BertForTokenClassification.from_pretrained(converted,config=cfg,local_files_only=True)
    args=TrainingArguments(output_dir=str(out_dir/"trainer"),seed=SEED,data_seed=SEED,
        learning_rate=lr,weight_decay=wd,warmup_steps=0,max_grad_norm=1.0,lr_scheduler_type="linear",
        per_device_train_batch_size=batch,num_train_epochs=epochs,evaluation_strategy="no",save_strategy="no",
        logging_strategy="steps",logging_steps=10,load_best_model_at_end=False,report_to=[],disable_tqdm=True,
        save_safetensors=True,dataloader_num_workers=0)
    tr=Trainer(model=model,args=args,train_dataset=dataset,
               tokenizer=AutoTokenizer.from_pretrained(converted,local_files_only=True,use_fast=True),
               callbacks=[Progress(status,name,offset,width)])
    res=tr.train(); out_dir.mkdir(parents=True,exist_ok=True); tr.save_model(out_dir); tr.tokenizer.save_pretrained(out_dir)
    h=sha256_path(out_dir/"model.safetensors")
    info={"epochs":epochs,"global_step":int(tr.state.global_step),"train_loss":float(res.training_loss),
          "model_sha256":h}
    del tr,model; gc.collect(); return info

def word_batch(tok,rows):
    return tok(rows,is_split_into_words=True,padding=True,truncation=True,max_length=256,return_tensors="pt")

def first_positions(enc,bi,n):
    seen=set(); pos=[]
    for j,w in enumerate(enc.word_ids(batch_index=bi)):
        if w is not None and w not in seen:seen.add(w);pos.append(j)
    if len(pos)!=n:raise RuntimeError(f"inference truncation {len(pos)} != {n}")
    return pos

def decode_constrained(tags,conf):
    out=[]; violations=[]; i=0
    while i<len(tags):
        tag=tags[i]
        if tag.startswith("B-"):
            typ=tag[2:]; vals=[conf[i]]; j=i+1
            while j<len(tags) and tags[j]==f"I-{typ}":
                vals.append(conf[j]); j+=1
            out.append({"type":typ,"start":i,"end":j,"b_conf":float(min(vals))}); i=j; continue
        if tag.startswith("I-"):
            violations.append({"word_index":i,"predicted":tag,
                               "previous_predicted":tags[i-1] if i else "SEQUENCE_START"})
        i+=1
    return out,violations

def infer_heldout(bmodel,boundary,tok,docs,doc_ids,batch=8):
    sentence_rows=[]; sections={}
    for di in sorted(doc_ids):
        sec=section_labels(docs[di])
        for si,(tokens,tags) in enumerate(docs[di]):
            sentence_rows.append((di,si,tokens,tags)); sections[(di,si)]=sec[si]
    proposals={}; bviol=[]; bnd={}
    bmodel.eval(); boundary.eval()
    with torch.no_grad():
        for st in range(0,len(sentence_rows),batch):
            ch=sentence_rows[st:st+batch]
            enc=word_batch(tok,[x[2] for x in ch])
            bp=torch.softmax(bmodel(**enc).logits,dim=-1)
            qp=torch.softmax(boundary(**enc).logits,dim=-1)
            for bi,(di,si,tokens,tags_gold) in enumerate(ch):
                pos=first_positions(enc,bi,len(tokens))
                ptags=[]; conf=[]
                for p in pos:
                    v=bp[bi,p]; z=int(v.argmax()); ptags.append(BIO_LABELS[z]); conf.append(float(v[z]))
                pp,vv=decode_constrained(ptags,conf)
                for x in vv:bviol.append({"document":di,"sentence":si,**x})
                proposals[(di,si)]=pp
                q=qp[bi,pos,:].cpu().numpy()
                bnd[(di,si)]={"start":(q[:,BOUNDARY2ID["START"]]+q[:,BOUNDARY2ID["BOTH"]]).tolist(),
                              "end":(q[:,BOUNDARY2ID["END"]]+q[:,BOUNDARY2ID["BOTH"]]).tolist()}
    return sentence_rows,sections,proposals,bviol,bnd

def quantiles(vals):
    if not vals:return {"n":0}
    a=np.asarray(vals,dtype=float)
    return {"n":len(vals),"mean":float(a.mean()),"q05":float(np.quantile(a,.05)),
            "q50":float(np.quantile(a,.5)),"q95":float(np.quantile(a,.95))}

def candidate_bank(fold,docs,heldout,sections,proposals,bviol,bnd):
    rows=[]; gold_counts=collections.Counter(); tax=collections.Counter(); target_counts=collections.Counter()
    coord_avail=collections.Counter(); typed_avail=collections.Counter()
    predicted_counts=collections.Counter(); tp_conf=[]; fp_conf=[]; goldless_candidates=0
    gold_by={}
    for di in sorted(heldout):
        for si,(tokens,tags) in enumerate(docs[di]):
            gs=source_spans(tags); gold_by[(di,si)]=gs
            for c,s,e in gs:gold_counts[c]+=1
    seen_coords=set()
    for di in sorted(heldout):
        nsi=len(docs[di])
        for si,(tokens,tags) in enumerate(docs[di]):
            gs=gold_by[(di,si)]
            coord={(s,e):c for c,s,e in gs}
            is_goldless=(len(gs)==0)
            for q in proposals[(di,si)]:
                typ,s,e=q["type"],q["start"],q["end"]
                key=(di,si,s,e,typ)
                if key in seen_coords:raise RuntimeError(f"duplicate candidate {key}")
                seen_coords.add(key); predicted_counts[typ]+=1
                exact=coord.get((s,e))
                if exact is not None:
                    target=exact; coord_avail[exact]+=1
                    if typ==exact:
                        taxonomy="EXACT_TYPED"; typed_avail[exact]+=1; tp_conf.append(q["b_conf"])
                    else:
                        taxonomy="WRONG_TYPE_EXACT_COORD"; fp_conf.append(q["b_conf"])
                else:
                    target="NONE"; fp_conf.append(q["b_conf"])
                    ov=[g for g in gs if overlap(s,e,g[1],g[2])]
                    if any(g[0]==typ for g in ov): taxonomy="SAME_CLASS_WRONG_BOUNDARY"
                    elif ov: taxonomy="DIFFERENT_CLASS_WRONG_BOUNDARY"
                    else: taxonomy="SPURIOUS_NO_OVERLAP"
                tax[taxonomy]+=1; target_counts[target]+=1
                if is_goldless:goldless_candidates+=1
                bp=bnd[(di,si)]
                rows.append({
                  "fold":fold,"document":di,"sentence":si,"start":s,"end":e,"width":e-s,
                  "b_type":typ,"b_conf":q["b_conf"],
                  "boundary_start_prob":float(bp["start"][s]),"boundary_end_prob":float(bp["end"][e-1]),
                  "target":target,"taxonomy":taxonomy,"goldless_example":is_goldless,
                  "section":sections[(di,si)],
                  "normalized_example_index":si/max(1,nsi-1),
                  "normalized_span_start":s/max(1,len(tokens)-1)
                })
    rows.sort(key=lambda r:(r["document"],r["sentence"],r["start"],r["end"],r["b_type"]))
    per={}
    for c in CLASSES:
        g=gold_counts[c]; typed=typed_avail[c]; co=coord_avail[c]
        per[c]={"gold":g,"coordinate_available":co,"typed_B_available":typed,
                "coordinate_recall_ceiling":co/g if g else 0.0,
                "typed_B_recall":typed/g if g else 0.0}
    typed_total=sum(typed_avail.values()); coord_total=sum(coord_avail.values()); n=len(rows)
    metrics={"candidate_count":n,"gold_total":sum(gold_counts.values()),
             "exact_coordinate_total":coord_total,"exact_typed_total":typed_total,
             "native_typed_precision":typed_total/n if n else 0.0,
             "native_typed_recall":typed_total/sum(gold_counts.values()) if gold_counts else 0.0,
             "coordinate_precision":coord_total/n if n else 0.0,
             "coordinate_recall":coord_total/sum(gold_counts.values()) if gold_counts else 0.0,
             "per_class":per,"target_counts":dict(target_counts),"taxonomy":dict(tax),
             "predicted_type_counts":dict(predicted_counts),"goldless_candidate_count":goldless_candidates,
             "B_conf_exact_typed":quantiles(tp_conf),"B_conf_other":quantiles(fp_conf),
             "BIO_violation_count":len(bviol)}
    return rows,metrics

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--design-source",type=pathlib.Path,required=True)
    ap.add_argument("--design-summary",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--fold",type=int,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); seed_all(); a.out.mkdir(parents=True,exist_ok=False); status=a.out/"PROCESS_STATUS.json"
    if a.fold not in range(5):raise RuntimeError("fold must be 0..4")
    ds_summary=json.loads(a.design_summary.read_text())
    if ds_summary.get("state")!="R44_DESIGN_SOURCE_PACKAGE_PASS":raise RuntimeError("design source summary state")
    if ds_summary.get("source_train_sha256")!=EXPECTED_TRAIN_SHA:raise RuntimeError("source TRAIN provenance mismatch")
    if ds_summary.get("r44_manifest_sha256")!=EXPECTED_R44_MANIFEST_SHA:raise RuntimeError("design source manifest provenance mismatch")
    if sha256_path(a.design_source)!=ds_summary.get("design_source_sha256"):raise RuntimeError("design source physical hash mismatch")

    m=json.loads(a.manifest.read_text())
    ms=m.pop("manifest_sha256",None)
    got=sha_text(json.dumps(m,sort_keys=True,separators=(",",":")))
    if ms!=EXPECTED_R44_MANIFEST_SHA or got!=EXPECTED_R44_MANIFEST_SHA:raise RuntimeError("R44 manifest identity mismatch")
    if len(m["design_documents"])!=256 or len(m["verify_internal_documents"])!=64:raise RuntimeError("R44 split size mismatch")
    held=set(next(x["documents"] for x in m["oof_folds"] if x["fold"]==a.fold))
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    train_ids=design-held
    if not held or train_ids&held or train_ids&verify or held&verify or (design|verify)&oldsel:raise RuntimeError("document isolation failure")
    all_oof=set()
    for foldrow in m["oof_folds"]:all_oof.update(foldrow["documents"])
    if all_oof!=design:raise RuntimeError("OOF coverage mismatch")

    src=json.loads(a.design_source.read_text())
    if src.get("state")!="R44_DESIGN_SOURCE_MATERIALIZED":raise RuntimeError("design source state")
    docs={}
    for d in src["documents"]:
        di=int(d["original_document"])
        if di in docs:raise RuntimeError("duplicate design document")
        docs[di]=[(s["tokens"],s["tags"]) for s in d["sentences"]]
    if set(docs)!=design:raise RuntimeError("training artifact is not exact DESIGN set")
    if set(docs)&verify or set(docs)&oldsel:raise RuntimeError("excluded document present in training artifact")

    rows=[]; train_gold=collections.Counter()
    for di in sorted(train_ids):
        for tokens,tags in docs[di]:
            sp=source_spans(tags)
            for c,s,e in sp:train_gold[c]+=1
            rows.append((tokens,tags,source_boundary_tags(tags)))
    write_json(status,{"state":"RUNNING","current_stage":"INITIALIZING","fold":a.fold,
                       "progress_percent":0.0,"train_documents":len(train_ids),"heldout_documents":len(held),
                       "last_progress_at":now(),"failure_or_stall_reason":None})

    converted=a.out/"converted_base"; tok=convert_base(a.model_dir,converted)
    bds=TokenDataset(rows,tok,"bio")
    binfo=train_token("B_CANDIDATE",converted,bds,a.out/"b_candidate",5e-5,0.0,10,8,status,0,10)
    del bds;gc.collect()
    bndds=TokenDataset(rows,tok,"boundary")
    bdinfo=train_token("C_BOUNDARY",converted,bndds,a.out/"c_boundary",5e-5,.01,3,8,status,10,3)
    del bndds;gc.collect()

    bmodel=BertForTokenClassification.from_pretrained(a.out/"b_candidate",local_files_only=True)
    boundary=BertForTokenClassification.from_pretrained(a.out/"c_boundary",local_files_only=True)
    tok=AutoTokenizer.from_pretrained(a.out/"b_candidate",local_files_only=True,use_fast=True)
    sent,sections,proposals,viol,bnd=infer_heldout(bmodel,boundary,tok,docs,held)
    bank,metrics=candidate_bank(a.fold,docs,held,sections,proposals,viol,bnd)

    bank_path=a.out/f"R44A_FOLD_{a.fold}_CANDIDATES.jsonl"
    with bank_path.open("w",encoding="utf-8") as f:
        for r in bank:f.write(json.dumps(r,sort_keys=True)+"\n")
    bank_sha=sha256_path(bank_path)

    summary={
      "state":"R44A_FOLD_COMPLETE","fold":a.fold,"seed":SEED,
      "source_train_sha256":EXPECTED_TRAIN_SHA,"design_source_sha256":sha256_path(a.design_source),
      "r44_manifest_sha256":EXPECTED_R44_MANIFEST_SHA,
      "train_documents":len(train_ids),"heldout_documents":len(held),
      "train_document_ids_sha256":sha_text(json.dumps(sorted(train_ids))),
      "heldout_document_ids_sha256":sha_text(json.dumps(sorted(held))),
      "train_gold_counts":{c:int(train_gold[c]) for c in CLASSES},
      "models":{"B_CANDIDATE":binfo,"C_BOUNDARY":bdinfo},
      "converted_base_sha256":EXPECTED_CONVERTED_SHA,
      "candidate_bank":{"rows":len(bank),"sha256":bank_sha,"metrics":metrics},
      "bio_violations":viol,
      "guards":{"design_only_training":True,"heldout_fold_used_for_training":False,
                "training_artifact_contains_verify_internal":False,
                "training_artifact_contains_old_r43_select":False,
                "verify_internal_used":False,"old_r43_select_used":False,"historical_dev_read":False,
                "test_read":False,"other_folds_read":False,"factpico_used":False,
                "consumed_60_rct_holdout_used":False,"head_training":False,
                "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY"},
      "next_action":"AGGREGATE_ONLY_AFTER_ALL_FIVE_OOF_FOLDS"
    }
    write_json(a.out/f"R44A_FOLD_{a.fold}_SUMMARY.json",summary)
    write_json(status,{"state":"COMPLETED","current_stage":"OOF_FOLD_COMPLETE","fold":a.fold,
                       "progress_percent":100.0,"candidate_rows":len(bank),"last_progress_at":now(),
                       "failure_or_stall_reason":None,"next_expected_step":"NEXT_SEQUENTIAL_FOLD_OR_AGGREGATE"})
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":main()
