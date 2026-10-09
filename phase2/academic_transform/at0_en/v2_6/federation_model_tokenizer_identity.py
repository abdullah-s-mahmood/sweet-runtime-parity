#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,platform
from huggingface_hub import HfApi
from transformers import AutoTokenizer,AutoConfig
import transformers,huggingface_hub,tokenizers

MODELS=[
 ("BASE","microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract","d673b8835373c6fa116d6d8006b33d48734e305d","pytorch_model.bin","d513412d396cecec5f67936ac871b4aaf1178dfb5193776e790fd2b28bba240c"),
 ("MODERN","thomas-sounack/BioClinical-ModernBERT-base","c3648aa87af95837c809e6f0c5f85d08160db437","model.safetensors","ea7388682b12cb833491ca8a697e84e3e67122c65c9c658f4ad3355fdd891546"),
 ("PICOX","microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract","f18ff5ec008285849e7c467b2618262b0def6238","pytorch_model.bin","2d7a3e00619bab3b5c9a9d04dc173c6197becd5a53a253999ded7ed742ba2419")
]
TEXTS=[
 "Randomized participants received metformin or placebo for twelve weeks.",
 "Primary outcome was change in systolic blood pressure at 12 months.",
 "Interleukin-6–mediated response was assessed in adults with type 2 diabetes."
]

def sha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

api=HfApi()
out={
 "state":"FEDERATION_MODEL_TOKENIZER_IDENTITY_PREFLIGHT_PASS",
 "python":platform.python_version(),
 "transformers":transformers.__version__,
 "huggingface_hub":huggingface_hub.__version__,
 "tokenizers":tokenizers.__version__,
 "models":{}
}
for role,repo,rev,weight,expected_sha in MODELS:
    info=api.model_info(repo,revision=rev,files_metadata=True)
    if info.sha != rev:
        raise RuntimeError(f"{role}: resolved revision {info.sha} != {rev}")
    siblings={x.rfilename:x for x in info.siblings}
    if weight not in siblings:
        raise RuntimeError(f"{role}: missing {weight}")
    item=siblings[weight]
    lfs=getattr(item,"lfs",None)
    actual=None
    if lfs is not None:
        actual=getattr(lfs,"sha256",None)
        if actual is None and isinstance(lfs,dict): actual=lfs.get("sha256")
    if actual and actual != expected_sha:
        raise RuntimeError(f"{role}: weight sha mismatch {actual} != {expected_sha}")

    tok=AutoTokenizer.from_pretrained(repo,revision=rev,use_fast=True)
    cfg=AutoConfig.from_pretrained(repo,revision=rev)
    fixtures=[]
    for text in TEXTS:
        enc=tok(text,add_special_tokens=True,return_offsets_mapping=True,truncation=False)
        fixtures.append({
          "input_ids":enc["input_ids"],
          "attention_mask":enc["attention_mask"],
          "offset_mapping":[list(x) for x in enc["offset_mapping"]]
        })
    vocab=tok.get_vocab()
    vocab_digest=sha(sorted(vocab.items(),key=lambda z:z[0]))
    out["models"][role]={
      "repo":repo,"revision":rev,
      "resolved_revision":info.sha,
      "weight_file":weight,
      "expected_weight_sha256":expected_sha,
      "metadata_weight_sha256":actual,
      "tokenizer_class":tok.__class__.__name__,
      "is_fast":bool(tok.is_fast),
      "vocab_size":len(vocab),
      "vocab_digest_sha256":vocab_digest,
      "model_type":getattr(cfg,"model_type",None),
      "hidden_size":getattr(cfg,"hidden_size",None),
      "max_position_embeddings":getattr(cfg,"max_position_embeddings",None),
      "fixture_digest_sha256":sha(fixtures)
    }
print(json.dumps(out,indent=2,sort_keys=True))
