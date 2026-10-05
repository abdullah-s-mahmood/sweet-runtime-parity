#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, pathlib, shutil
import torch
from transformers import AutoConfig, AutoTokenizer, BertModel, BertForTokenClassification

from r4_2_train_calibrate_witness import (
    LABELS, LABEL2ID, ID2LABEL, TokenDataset, read_conll, seed_all
)

def all_finite(model):
    bad=[]
    total=0
    for name,p in model.named_parameters():
        total+=p.numel()
        if not torch.isfinite(p).all():
            bad.append(name)
    return total,bad

def sha256(path:pathlib.Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",type=pathlib.Path,required=True)
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    seed_all()
    args.out.mkdir(parents=True,exist_ok=False)

    tokenizer=AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True,use_fast=True)

    # Convert ONLY the base BERT architecture from Flax first.
    base=BertModel.from_pretrained(
        args.model_dir,
        from_flax=True,
        local_files_only=True,
    )
    base_total,base_bad=all_finite(base)
    if base_bad:
        raise RuntimeError(f"non-finite base parameters after Flax conversion: {base_bad[:10]}")

    converted=args.out/"converted_base"
    base.save_pretrained(converted,safe_serialization=True)
    tokenizer.save_pretrained(converted)
    if not (converted/"model.safetensors").exists():
        raise RuntimeError("converted base safetensors missing")

    config=AutoConfig.from_pretrained(
        converted,
        local_files_only=True,
        num_labels=len(LABELS),
        label2id=LABEL2ID,
        id2label=ID2LABEL,
    )
    model=BertForTokenClassification.from_pretrained(
        converted,
        config=config,
        local_files_only=True,
    )
    model_total,model_bad=all_finite(model)
    if model_bad:
        raise RuntimeError(f"non-finite token-classification parameters before training: {model_bad[:10]}")

    sentences=read_conll(args.train)
    smoke_sentences=sentences[:8]
    ds=TokenDataset(smoke_sentences,tokenizer)
    batch={k:torch.stack([ds[i][k] for i in range(len(ds))]) for k in ds[0]}
    supervised=int((batch["labels"]!=-100).sum().item())
    entity_supervised=int(((batch["labels"]!=-100)&(batch["labels"]!=LABEL2ID["O"])).sum().item())
    if supervised<=0 or entity_supervised<=0:
        raise RuntimeError(f"invalid smoke labels supervised={supervised} entity={entity_supervised}")

    model.train()
    out=model(**batch)
    loss=out.loss
    if loss is None or not torch.isfinite(loss) or not (0.0 < float(loss.item()) < 100.0):
        raise RuntimeError(f"invalid pre-step loss: {loss}")

    probe_name="bert.encoder.layer.0.attention.self.query.weight"
    params=dict(model.named_parameters())
    before=params[probe_name].detach().clone()

    optimizer=torch.optim.AdamW(model.parameters(),lr=5e-5,weight_decay=0.01)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()

    grad_nonzero=0
    grad_bad=[]
    for name,p in model.named_parameters():
        if p.grad is not None:
            if not torch.isfinite(p.grad).all():
                grad_bad.append(name)
            if torch.count_nonzero(p.grad).item()>0:
                grad_nonzero+=1
    if grad_bad:
        raise RuntimeError(f"non-finite gradients: {grad_bad[:10]}")
    if grad_nonzero<=0:
        raise RuntimeError("no non-zero gradients")

    optimizer.step()
    after=params[probe_name].detach()
    probe_changed=not torch.equal(before,after)
    if not probe_changed:
        raise RuntimeError("probe base parameter did not change after optimizer step")

    post_total,post_bad=all_finite(model)
    if post_bad:
        raise RuntimeError(f"non-finite parameters after smoke optimizer step: {post_bad[:10]}")

    result={
        "smoke_id":"AT0_EN_V26_R4_2_SAFE_FLAX_BASE_LOAD_SMOKE_V1",
        "state":"PASS",
        "base_parameter_values":base_total,
        "base_nonfinite_parameter_tensors":len(base_bad),
        "model_parameter_values":model_total,
        "model_nonfinite_before":len(model_bad),
        "supervised_word_labels":supervised,
        "supervised_entity_word_labels":entity_supervised,
        "pre_step_loss":float(loss.item()),
        "nonzero_gradient_tensors":grad_nonzero,
        "probe_parameter":probe_name,
        "probe_changed_after_step":probe_changed,
        "model_nonfinite_after":len(post_bad),
        "converted_base_safetensors_sha256":sha256(converted/"model.safetensors"),
        "guards":{
            "smoke_training_sentences":len(smoke_sentences),
            "dev_used":False,
            "test_used":False,
            "factpico_used":False,
            "consumed_60_rct_holdout_used":False,
            "smoke_weights_discarded":True,
        }
    }
    raw=json.dumps(result,sort_keys=True,separators=(",",":")).encode()
    result["canonical_pre_hash_sha256"]=hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
