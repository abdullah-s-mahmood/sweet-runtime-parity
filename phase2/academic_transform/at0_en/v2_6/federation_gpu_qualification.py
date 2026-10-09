#!/usr/bin/env python3
from __future__ import annotations
import argparse, gc, hashlib, json, os, platform
from pathlib import Path
import numpy as np
import torch
import transformers, tokenizers, huggingface_hub, safetensors, accelerate
from huggingface_hub import hf_hub_download
from transformers import AutoModel

MODELS=[
 {
  "role":"D0_D1_D2_D3_REFERENCE_ENCODER",
  "repo":"microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract",
  "revision":"d673b8835373c6fa116d6d8006b33d48734e305d",
  "weight_file":"pytorch_model.bin",
  "weight_sha256":"d513412d396cecec5f67936ac871b4aaf1178dfb5193776e790fd2b28bba240c",
  "seq_len":512,"vocab_size":28895
 },
 {
  "role":"D4_MODERN_CHALLENGER",
  "repo":"thomas-sounack/BioClinical-ModernBERT-base",
  "revision":"c3648aa87af95837c809e6f0c5f85d08160db437",
  "weight_file":"model.safetensors",
  "weight_sha256":"ea7388682b12cb833491ca8a697e84e3e67122c65c9c658f4ad3355fdd891546",
  "seq_len":8192,"vocab_size":50280
 },
 {
  "role":"PICOX_ADAPTED_COMPARATOR_ENCODER",
  "repo":"microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract",
  "revision":"f18ff5ec008285849e7c467b2618262b0def6238",
  "weight_file":"pytorch_model.bin",
  "weight_sha256":"2d7a3e00619bab3b5c9a9d04dc173c6197becd5a53a253999ded7ed742ba2419",
  "seq_len":512,"vocab_size":28895
 }
]

EXPECTED={
 "python":"3.11.16","numpy":"1.26.4","torch_base":"2.5.1","transformers":"4.48.0",
 "tokenizers":"0.21.0","huggingface_hub":"0.28.1","safetensors":"0.5.2","accelerate":"1.3.0"
}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def assert_versions():
    versions={
      "python":platform.python_version(),"numpy":np.__version__,"torch_base":torch.__version__.split("+",1)[0],
      "transformers":transformers.__version__,"tokenizers":tokenizers.__version__,
      "huggingface_hub":huggingface_hub.__version__,"safetensors":safetensors.__version__,
      "accelerate":accelerate.__version__
    }
    for k,v in EXPECTED.items():
        if versions[k]!=v: raise RuntimeError(f"version mismatch {k}: {versions[k]} != {v}")
    return versions

def one_model(spec,use_checkpointing,precision):
    torch.cuda.empty_cache(); gc.collect()
    weight=hf_hub_download(spec["repo"],filename=spec["weight_file"],revision=spec["revision"])
    actual=sha(weight)
    if actual!=spec["weight_sha256"]:
        raise RuntimeError(f"weight SHA mismatch for {spec['role']}: {actual}")
    model=AutoModel.from_pretrained(spec["repo"],revision=spec["revision"],trust_remote_code=False)
    if use_checkpointing:
        if not hasattr(model,"gradient_checkpointing_enable"):
            raise RuntimeError(f"gradient checkpointing unavailable: {spec['role']}")
        model.gradient_checkpointing_enable()
    model.cuda(); model.train()
    hidden=int(model.config.hidden_size)
    head=torch.nn.Linear(hidden,4).cuda()
    opt=torch.optim.AdamW(list(model.parameters())+list(head.parameters()),lr=2e-5,betas=(.9,.999),eps=1e-8,weight_decay=.01)
    ids=torch.randint(0,spec["vocab_size"],(1,spec["seq_len"]),device="cuda")
    mask=torch.ones_like(ids)
    torch.cuda.reset_peak_memory_stats()
    dtype=torch.bfloat16 if precision=="bf16" else torch.float16
    with torch.autocast(device_type="cuda",dtype=dtype):
        out=model(input_ids=ids,attention_mask=mask)
        h=out.last_hidden_state
        logits=head(h)
        loss=(logits.float().square().mean())
    loss.backward()
    torch.nn.utils.clip_grad_norm_(list(model.parameters())+list(head.parameters()),1.0)
    opt.step(); opt.zero_grad(set_to_none=True)
    torch.cuda.synchronize()
    peak=int(torch.cuda.max_memory_allocated())
    reserved=int(torch.cuda.max_memory_reserved())
    result={
      "role":spec["role"],"revision":spec["revision"],"weight_sha256":actual,
      "seq_len":spec["seq_len"],"microbatch":1,"precision":precision,
      "gradient_checkpointing":use_checkpointing,
      "peak_memory_allocated_bytes":peak,"peak_memory_reserved_bytes":reserved,
      "loss_finite":bool(torch.isfinite(loss.detach()).item())
    }
    del opt,head,model,ids,mask,out,h,logits,loss
    torch.cuda.empty_cache(); gc.collect()
    if not result["loss_finite"]: raise RuntimeError(f"nonfinite loss: {spec['role']}")
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--gradient-checkpointing",choices=["off","on"],default="off")
    a=ap.parse_args()
    versions=assert_versions()
    if not torch.cuda.is_available(): raise RuntimeError("CUDA GPU required")
    idx=torch.cuda.current_device(); props=torch.cuda.get_device_properties(idx)
    bf16=bool(torch.cuda.is_bf16_supported())
    precision="bf16" if bf16 else "fp16"
    torch.manual_seed(44); torch.cuda.manual_seed_all(44)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark=False
    use_gc=a.gradient_checkpointing=="on"
    rows=[]
    for spec in MODELS:
        rows.append(one_model(spec,use_gc,precision))
    out={
      "state":"FEDERATION_GPU_QUALIFICATION_PASS",
      "scientific_data_used":False,
      "scientific_attempt_consumed":False,
      "versions":versions,
      "torch_full":torch.__version__,
      "cuda_runtime":torch.version.cuda,
      "cudnn_version":torch.backends.cudnn.version(),
      "gpu_name":torch.cuda.get_device_name(idx),
      "gpu_total_memory_bytes":int(props.total_memory),
      "compute_capability":[int(props.major),int(props.minor)],
      "bf16_supported":bf16,
      "selected_precision_by_frozen_hardware_rule":precision,
      "microbatch":1,
      "native_effective_batch":8,
      "native_gradient_accumulation":8,
      "picox_boundary_effective_batch":8,
      "picox_boundary_gradient_accumulation":8,
      "picox_span_effective_batch":16,
      "picox_span_gradient_accumulation":16,
      "gradient_checkpointing":use_gc,
      "models":rows,
      "rules":[
        "This qualification uses synthetic inputs only.",
        "No scientific attempt is consumed.",
        "The exact GPU/runtime output must be frozen before first fit.",
        "If gradient checkpointing OFF fails, ON may be tested only before any scientific fit; the chosen mode must then be global/frozen for the campaign.",
        "If both modes fail, the backend is rejected; model/protocol parameters are not changed to fit the hardware."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
