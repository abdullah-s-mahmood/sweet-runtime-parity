#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, os, random, tempfile
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from safetensors.torch import save_file, load_file

SEED=44
ENCODER_LR=2e-5
HEAD_LR=1e-4
WEIGHT_DECAY=.01
BETAS=(.9,.999)
EPS=1e-8
GRAD_CLIP=1.0
WARMUP_FRAC=.10
EFFECTIVE_BATCH=8
MICROBATCH=2
ACCUM=EFFECTIVE_BATCH//MICROBATCH
OPT_STEPS=12
CHECKPOINT_AFTER_STEP=5

class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder=nn.Sequential(nn.Linear(8,16),nn.LayerNorm(16),nn.GELU(),nn.Dropout(.2))
        self.head=nn.Linear(16,4)
    def forward(self,x):
        return self.head(self.encoder(x))

def set_seed(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)

def model_groups(model):
    decay=[]; no_decay=[]; head_decay=[]; head_no_decay=[]
    for name,p in model.encoder.named_parameters():
        (no_decay if name.endswith("bias") or "1." in name else decay).append(p)
    for name,p in model.head.named_parameters():
        (head_no_decay if name.endswith("bias") else head_decay).append(p)
    return [
      {"params":decay,"lr":ENCODER_LR,"weight_decay":WEIGHT_DECAY},
      {"params":no_decay,"lr":ENCODER_LR,"weight_decay":0.0},
      {"params":head_decay,"lr":HEAD_LR,"weight_decay":WEIGHT_DECAY},
      {"params":head_no_decay,"lr":HEAD_LR,"weight_decay":0.0},
    ]

def make_optimizer(model):
    return torch.optim.AdamW(model_groups(model),betas=BETAS,eps=EPS)

def lr_lambda(step):
    warm=max(1,int(math.ceil(OPT_STEPS*WARMUP_FRAC)))
    if step < warm:
        return float(step+1)/float(warm)
    remain=max(1,OPT_STEPS-warm)
    return max(0.0,float(OPT_STEPS-(step+1))/float(remain))

def make_scheduler(opt):
    return torch.optim.lr_scheduler.LambdaLR(opt,lr_lambda=lr_lambda)

def synthetic_dataset():
    # Data tensors are deterministic and do not consume the training RNG after construction.
    g=torch.Generator().manual_seed(20261009)
    x=torch.randn(64,8,generator=g)
    y=torch.randint(0,4,(64,),generator=g)
    return x,y

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def state_hash(model):
    h=hashlib.sha256()
    for k,v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

def optim_tensor_hash(opt):
    h=hashlib.sha256()
    sd=opt.state_dict()
    h.update(json.dumps(sd["param_groups"],sort_keys=True,default=str).encode())
    for pid,st in sorted(sd["state"].items(),key=lambda z:int(z[0])):
        h.update(str(pid).encode())
        for k,v in sorted(st.items()):
            h.update(k.encode())
            if torch.is_tensor(v): h.update(v.detach().cpu().contiguous().numpy().tobytes())
            else: h.update(repr(v).encode())
    return h.hexdigest()

def save_checkpoint(root,model,opt,sched,train_state):
    root.mkdir(parents=True,exist_ok=True)
    model_path=root/"model.safetensors"
    state_path=root/"training_state.pt"
    save_file({k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()},str(model_path))
    payload={
      "optimizer":opt.state_dict(),
      "scheduler":sched.state_dict(),
      "train_state":train_state,
      "python_rng":random.getstate(),
      "numpy_rng":np.random.get_state(),
      "torch_rng":torch.get_rng_state(),
    }
    torch.save(payload,state_path)
    manifest={
      "model_sha256":sha(model_path),
      "training_state_sha256":sha(state_path),
      "optimizer_step":train_state["optimizer_step"],
      "micro_cursor":train_state["micro_cursor"],
    }
    (root/"manifest.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    return manifest

def load_checkpoint(root,model,opt,sched):
    manifest=json.loads((root/"manifest.json").read_text())
    if sha(root/"model.safetensors")!=manifest["model_sha256"]: raise RuntimeError("model checkpoint hash mismatch")
    if sha(root/"training_state.pt")!=manifest["training_state_sha256"]: raise RuntimeError("training state hash mismatch")
    weights=load_file(str(root/"model.safetensors"))
    model.load_state_dict(weights,strict=True)
    payload=torch.load(root/"training_state.pt",map_location="cpu",weights_only=False)
    opt.load_state_dict(payload["optimizer"])
    sched.load_state_dict(payload["scheduler"])
    random.setstate(payload["python_rng"])
    np.random.set_state(payload["numpy_rng"])
    torch.set_rng_state(payload["torch_rng"])
    return payload["train_state"],manifest

def build_micro_schedule(n_micro):
    # Dedicated fixed generator: schedule is part of the execution state, not regenerated from labels/results.
    g=torch.Generator().manual_seed(440044)
    order=[]
    while len(order)<n_micro*MICROBATCH:
        order.extend(torch.randperm(64,generator=g).tolist())
    return order[:n_micro*MICROBATCH]

def run(outdir,interrupt=False):
    set_seed(SEED)
    torch.use_deterministic_algorithms(True)
    model=TinyModel()
    opt=make_optimizer(model); sched=make_scheduler(opt)
    x,y=synthetic_dataset()
    total_micro=OPT_STEPS*ACCUM
    schedule=build_micro_schedule(total_micro)
    state={"optimizer_step":0,"micro_cursor":0,"schedule":schedule,"loss_trace":[],"lr_trace":[]}
    opt.zero_grad(set_to_none=True)

    ckdir=outdir/"checkpoint"
    resumed=False
    while state["optimizer_step"]<OPT_STEPS:
        start=state["micro_cursor"]*MICROBATCH
        ids=state["schedule"][start:start+MICROBATCH]
        xb=x[ids]; yb=y[ids]
        logits=model(xb)
        loss=nn.functional.cross_entropy(logits,yb)/ACCUM
        state["loss_trace"].append(float(loss.detach()))
        loss.backward()
        state["micro_cursor"]+=1

        if state["micro_cursor"]%ACCUM==0:
            torch.nn.utils.clip_grad_norm_(model.parameters(),GRAD_CLIP)
            opt.step(); sched.step(); opt.zero_grad(set_to_none=True)
            state["optimizer_step"]+=1
            state["lr_trace"].append([float(g["lr"]) for g in opt.param_groups])

            if interrupt and state["optimizer_step"]==CHECKPOINT_AFTER_STEP and not resumed:
                save_checkpoint(ckdir,model,opt,sched,state)
                # Simulate fresh process objects; RNG and all optimizer/scheduler state must be restored.
                model2=TinyModel()
                opt2=make_optimizer(model2); sched2=make_scheduler(opt2)
                state2,_=load_checkpoint(ckdir,model2,opt2,sched2)
                model,opt,sched,state=model2,opt2,sched2,state2
                resumed=True

    return {
      "model_hash":state_hash(model),
      "optimizer_hash":optim_tensor_hash(opt),
      "scheduler_state":sched.state_dict(),
      "loss_trace":state["loss_trace"],
      "lr_trace":state["lr_trace"],
      "final_optimizer_step":state["optimizer_step"],
      "final_micro_cursor":state["micro_cursor"],
      "checkpoint_manifest":json.loads((ckdir/"manifest.json").read_text()) if interrupt else None,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        uninterrupted=run(root/"full",interrupt=False)
        resumed=run(root/"resume",interrupt=True)
        if uninterrupted["model_hash"]!=resumed["model_hash"]: raise RuntimeError("model state differs after resume")
        if uninterrupted["optimizer_hash"]!=resumed["optimizer_hash"]: raise RuntimeError("optimizer state differs after resume")
        if uninterrupted["scheduler_state"]!=resumed["scheduler_state"]: raise RuntimeError("scheduler state differs after resume")
        if uninterrupted["loss_trace"]!=resumed["loss_trace"]: raise RuntimeError("loss trace differs after resume")
        if uninterrupted["lr_trace"]!=resumed["lr_trace"]: raise RuntimeError("LR trace differs after resume")
        if resumed["final_optimizer_step"]!=OPT_STEPS or resumed["final_micro_cursor"]!=OPT_STEPS*ACCUM:
            raise RuntimeError("final counters differ")

        # Fail-closed checkpoint integrity fixture.
        ck=root/"resume/checkpoint/model.safetensors"
        raw=bytearray(ck.read_bytes()); raw[-1]^=1; ck.write_bytes(bytes(raw))
        model=TinyModel(); opt=make_optimizer(model); sched=make_scheduler(opt)
        tamper_guard=False
        try: load_checkpoint(root/"resume/checkpoint",model,opt,sched)
        except RuntimeError: tamper_guard=True
        if not tamper_guard: raise RuntimeError("tampered checkpoint accepted")

        out={
          "state":"FEDERATION_TRAINING_LOOP_CHECKPOINT_RESUME_SYNTHETIC_PASS",
          "scientific_data_used":False,
          "scientific_encoder_loaded":False,
          "scientific_training_performed":False,
          "seed":SEED,
          "optimizer":"AdamW",
          "encoder_lr":ENCODER_LR,
          "head_lr":HEAD_LR,
          "weight_decay":WEIGHT_DECAY,
          "betas":list(BETAS),
          "eps":EPS,
          "gradient_clip":GRAD_CLIP,
          "warmup_fraction":WARMUP_FRAC,
          "effective_batch":EFFECTIVE_BATCH,
          "synthetic_microbatch":MICROBATCH,
          "synthetic_gradient_accumulation":ACCUM,
          "optimizer_steps":OPT_STEPS,
          "checkpoint_after_optimizer_step":CHECKPOINT_AFTER_STEP,
          "uninterrupted_model_hash":uninterrupted["model_hash"],
          "resumed_model_hash":resumed["model_hash"],
          "uninterrupted_optimizer_hash":uninterrupted["optimizer_hash"],
          "resumed_optimizer_hash":resumed["optimizer_hash"],
          "exact_resume_equivalence":True,
          "loss_trace_exact_match":True,
          "lr_trace_exact_match":True,
          "checkpoint_hash_guard":True,
          "checkpoint_files":["model.safetensors","training_state.pt","manifest.json"],
          "scientific_total_update_formula":"20 * ceil(N_native_train / 8)",
          "gpu_specific_microbatch_and_accumulation":"MUST_BE_BOUND_BEFORE_FIRST_FIT_WHILE_PRESERVING_EFFECTIVE_BATCH_8"
        }
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
