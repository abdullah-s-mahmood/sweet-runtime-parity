#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from pathlib import Path
import torch, transformers, tokenizers, huggingface_hub, safetensors, accelerate, numpy as np
from transformers import AutoConfig, AutoTokenizer

MODELS=[
 {"role":"reference_base","id":"microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract","revision":"d673b8835373c6fa116d6d8006b33d48734e305d","expected_model_type":"bert"},
 {"role":"picox_large","id":"microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract","revision":"6611fb0be85c82ae6089ab63a0d81edfcd956dae","expected_model_type":"bert"},
 {"role":"modern_challenger","id":"thomas-sounack/BioClinical-ModernBERT-base","revision":"c3648aa87af95837c809e6f0c5f85d08160db437","expected_model_type":"modernbert"},
]

def stable_tokenizer_signature(tok):
    special={
      "cls_token":tok.cls_token,"sep_token":tok.sep_token,"pad_token":tok.pad_token,
      "unk_token":tok.unk_token,"mask_token":tok.mask_token,
      "model_max_length":tok.model_max_length,
      "vocab_size":tok.vocab_size,
      "padding_side":tok.padding_side,"truncation_side":tok.truncation_side,
    }
    return hashlib.sha256(json.dumps(special,sort_keys=True,default=str).encode()).hexdigest(),special

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    versions={
      "python":platform.python_version(),
      "torch":torch.__version__,
      "transformers":transformers.__version__,
      "tokenizers":tokenizers.__version__,
      "huggingface_hub":huggingface_hub.__version__,
      "safetensors":safetensors.__version__,
      "accelerate":accelerate.__version__,
      "numpy":np.__version__,
    }
    expected={
      "torch":"2.5.1","transformers":"4.48.0","tokenizers":"0.21.0",
      "huggingface_hub":"0.28.1","safetensors":"0.5.2","accelerate":"1.3.0","numpy":"1.26.4"
    }
    for k,v in expected.items():
        if versions[k] != v: raise RuntimeError(f"version mismatch {k}: {versions[k]} != {v}")

    models=[]
    for m in MODELS:
        cfg=AutoConfig.from_pretrained(m["id"],revision=m["revision"],trust_remote_code=False)
        tok=AutoTokenizer.from_pretrained(m["id"],revision=m["revision"],use_fast=True,trust_remote_code=False)
        if cfg.model_type != m["expected_model_type"]:
            raise RuntimeError(f"model type mismatch for {m['id']}: {cfg.model_type}")
        sig,special=stable_tokenizer_signature(tok)
        item={
          **m,
          "config_model_type":cfg.model_type,
          "hidden_size":getattr(cfg,"hidden_size",None),
          "num_hidden_layers":getattr(cfg,"num_hidden_layers",None),
          "num_attention_heads":getattr(cfg,"num_attention_heads",None),
          "max_position_embeddings":getattr(cfg,"max_position_embeddings",None),
          "tokenizer_class":type(tok).__name__,
          "tokenizer_signature_sha256":sig,
          "tokenizer_specials":special,
        }
        # Architecture invariants used by protocol.
        if m["role"]=="reference_base":
            if item["hidden_size"]!=768: raise RuntimeError("reference base hidden size changed")
        if m["role"]=="modern_challenger":
            if item["hidden_size"]!=768 or item["max_position_embeddings"]!=8192:
                raise RuntimeError("ModernBERT architecture invariant changed")
        models.append(item)

    out={
      "state":"FEDERATION_RUNTIME_MODEL_IDENTITY_PREFLIGHT_PASS",
      "scientific_training":False,
      "weights_loaded":False,
      "cuda_available":torch.cuda.is_available(),
      "platform":platform.platform(),
      "versions":versions,
      "models":models,
      "determinism_policy":{
        "torch_use_deterministic_algorithms":True,
        "cudnn_benchmark":False,
        "seed_set":["python","numpy","torch","torch.cuda"],
        "final_checkpoint_only":True
      },
      "limitations":[
        "This CPU/runtime identity preflight does not qualify a future GPU training host.",
        "Model weights are not loaded; weight SHA/download closure is a separate step.",
        "Scientific batch memory feasibility is not established by this preflight."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True,default=str))
if __name__=="__main__": main()
