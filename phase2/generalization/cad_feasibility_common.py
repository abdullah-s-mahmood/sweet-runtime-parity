"""Shared frozen representation for CAD feasibility training/scoring."""
from __future__ import annotations
import numpy as np
import torch
from transformers import AutoModel,AutoTokenizer

MODEL_ID="CAMeL-Lab/bert-base-arabic-camelbert-msa"
MODEL_REVISION="9c0a8968fc47b06469302963b68caa5ce5e943af"
WINDOW_RADIUS=12
MAX_LENGTH=64
BATCH_SIZE=64

def target_window(words,target_i):
    lo=max(0,target_i-WINDOW_RADIUS)
    hi=min(len(words),target_i+WINDOW_RADIUS+1)
    return " ".join(words[lo:hi])

def load_encoder():
    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=MODEL_REVISION,use_fast=True)
    model=AutoModel.from_pretrained(MODEL_ID,revision=MODEL_REVISION).eval().cpu()
    return tok,model

def encode_texts(texts,tok,model,batch_size=BATCH_SIZE):
    uniq=list(dict.fromkeys(texts))
    out={}
    with torch.no_grad():
        for i in range(0,len(uniq),batch_size):
            batch=uniq[i:i+batch_size]
            enc=tok(batch,padding=True,truncation=True,max_length=MAX_LENGTH,return_tensors="pt")
            hidden=model(**enc).last_hidden_state
            mask=enc["attention_mask"].unsqueeze(-1).to(hidden.dtype)
            pooled=(hidden*mask).sum(dim=1)/mask.sum(dim=1).clamp_min(1.0)
            arr=pooled.cpu().numpy().astype("float32")
            for t,v in zip(batch,arr):out[t]=v
    return out

def pair_feature_matrix(pairs,tok,model):
    texts=[]
    for s,c in pairs:texts.extend([s,c])
    emb=encode_texts(texts,tok,model)
    rows=[]
    for s,c in pairs:
        a=emb[s];b=emb[c]
        d=b-a
        rows.append(np.concatenate([d,np.abs(d),a*b]).astype("float32"))
    return np.stack(rows,axis=0)
