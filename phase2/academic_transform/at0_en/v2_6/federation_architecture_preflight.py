#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,random
from dataclasses import dataclass
from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F

CLASSES=("P","I","C","O")
BIO_LABELS=("O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O")

def set_seed(seed=44):
    random.seed(seed)
    torch.manual_seed(seed)

def allowed_bio_transition(prev:int,cur:int)->bool:
    p=BIO_LABELS[prev]; c=BIO_LABELS[cur]
    if c=="O" or c.startswith("B-"): return True
    if c.startswith("I-"):
        typ=c[2:]
        return p in (f"B-{typ}",f"I-{typ}")
    return False

def viterbi_valid(logits):
    # logits [L,9], fixed constraints, no learned transition parameters.
    L,C=logits.shape
    neg=-1e30
    dp=logits[0].clone()
    # sequence cannot begin with I-X
    for j,l in enumerate(BIO_LABELS):
        if l.startswith("I-"): dp[j]=neg
    back=[]
    for t in range(1,L):
        nxt=torch.full((C,),neg,dtype=logits.dtype)
        bp=torch.full((C,),-1,dtype=torch.long)
        for cur in range(C):
            vals=[]
            for prev in range(C):
                if allowed_bio_transition(prev,cur):
                    vals.append((dp[prev].item()+logits[t,cur].item(),prev))
            best=max(vals,key=lambda z:z[0])
            nxt[cur]=best[0]; bp[cur]=best[1]
        dp=nxt; back.append(bp)
    cur=int(torch.argmax(dp))
    seq=[cur]
    for bp in reversed(back):
        cur=int(bp[cur]); seq.append(cur)
    seq=list(reversed(seq))
    for i,x in enumerate(seq):
        if i==0 and BIO_LABELS[x].startswith("I-"): raise RuntimeError("invalid initial I")
        if i and not allowed_bio_transition(seq[i-1],x): raise RuntimeError("invalid transition")
    return seq

class BIOHead(nn.Module):
    def __init__(self,h=768):
        super().__init__()
        self.drop=nn.Dropout(.1)
        self.fc=nn.Linear(h,len(BIO_LABELS))
    def forward(self,x):
        return self.fc(self.drop(x))

class TypedSpanHead(nn.Module):
    def __init__(self,h=768,d=64,k=4):
        super().__init__()
        self.k=k; self.d=d
        self.drop=nn.Dropout(.1)
        self.start=nn.Linear(h,k*d)
        self.end=nn.Linear(h,k*d)
    def forward(self,x):
        # x [B,L,H] -> [B,K,L,L]
        B,L,H=x.shape
        y=self.drop(x)
        s=self.start(y).view(B,L,self.k,self.d).permute(0,2,1,3)
        e=self.end(y).view(B,L,self.k,self.d).permute(0,2,1,3)
        z=torch.einsum("bkid,bkjd->bkij",s,e)/math.sqrt(self.d)
        tri=torch.triu(torch.ones(L,L,dtype=torch.bool,device=z.device))
        z=z.masked_fill(~tri,-1e4)
        return z

def multilabel_categorical_loss(logits,pos_mask,valid_mask):
    # logits/pos/valid [B,K,L,L].
    losses=[]
    for b in range(logits.shape[0]):
        for k in range(logits.shape[1]):
            z=logits[b,k]
            valid=valid_mask[b,k]
            pos=pos_mask[b,k] & valid
            neg=(~pos) & valid
            p=z[pos]; n=z[neg]
            lp=torch.logsumexp(torch.cat([torch.zeros(1,device=z.device),-p]),dim=0)
            ln=torch.logsumexp(torch.cat([torch.zeros(1,device=z.device),n]),dim=0)
            losses.append(lp+ln)
    return torch.stack(losses).mean()

class AuxSpanHeads(nn.Module):
    def __init__(self,h=768):
        super().__init__()
        self.ebm=TypedSpanHead(h,64,3)
        self.trialsieve=TypedSpanHead(h,64,20)
        self.evidence=TypedSpanHead(h,64,1)
        self.pico=TypedSpanHead(h,64,26)

def finite_grads(module):
    seen=0
    for p in module.parameters():
        if p.grad is not None:
            seen+=p.numel()
            if not torch.isfinite(p.grad).all(): return False,seen
    return seen>0,seen

def synthetic_span_masks(B,K,L):
    valid=torch.zeros(B,K,L,L,dtype=torch.bool)
    pos=torch.zeros_like(valid)
    for b in range(B):
      for k in range(K):
        for i in range(L):
          for j in range(i,min(L,i+4)):
            valid[b,k,i,j]=True
        # one class-specific positive
        i=(k+b)%max(1,L-1); j=min(L-1,i+(k%2))
        pos[b,k,i,j]=True
    return pos,valid

def train_step(module,loss):
    loss.backward()
    ok,n=finite_grads(module)
    if not ok: raise RuntimeError("nonfinite or missing gradients")
    return n

def preflight():
    set_seed(44)
    B,L,H=2,12,768
    x=torch.randn(B,L,H)

    # D0: native BIO only.
    d0=BIOHead(H)
    y=torch.randint(0,len(BIO_LABELS),(B,L))
    logits=d0(x)
    loss0=F.cross_entropy(logits.reshape(-1,9),y.reshape(-1))
    n0=train_step(d0,loss0)
    seq=viterbi_valid(logits[0].detach())

    # D1: native span.
    d1=TypedSpanHead(H,64,4)
    z1=d1(x)
    p1,v1=synthetic_span_masks(B,4,L)
    loss1=multilabel_categorical_loss(z1,p1,v1)
    n1=train_step(d1,loss1)

    # D2: BIO + human auxiliary span heads.
    d2_native=BIOHead(H); d2_aux=AuxSpanHeads(H)
    native_logits=d2_native(x)
    native_loss=F.cross_entropy(native_logits.reshape(-1,9),y.reshape(-1))
    aux_losses=[]
    for head,k in [(d2_aux.ebm,3),(d2_aux.trialsieve,20),(d2_aux.evidence,1),(d2_aux.pico,26)]:
        zz=head(x)
        pp,vv=synthetic_span_masks(B,k,L)
        aux_losses.append(multilabel_categorical_loss(zz,pp,vv))
    loss2=native_loss+.25*torch.stack(aux_losses).mean()
    loss2.backward()
    ok2a,n2a=finite_grads(d2_native); ok2b,n2b=finite_grads(d2_aux)
    if not(ok2a and ok2b): raise RuntimeError("D2 gradients invalid")

    # D3: native span + same aux.
    d3_native=TypedSpanHead(H,64,4); d3_aux=AuxSpanHeads(H)
    zz=d3_native(x); pp,vv=synthetic_span_masks(B,4,L)
    native3=multilabel_categorical_loss(zz,pp,vv)
    al=[]
    for head,k in [(d3_aux.ebm,3),(d3_aux.trialsieve,20),(d3_aux.evidence,1),(d3_aux.pico,26)]:
        a=head(x); ap,av=synthetic_span_masks(B,k,L)
        al.append(multilabel_categorical_loss(a,ap,av))
    loss3=native3+.25*torch.stack(al).mean()
    loss3.backward()
    ok3a,n3a=finite_grads(d3_native); ok3b,n3b=finite_grads(d3_aux)
    if not(ok3a and ok3b): raise RuntimeError("D3 gradients invalid")

    # D4 has same hidden size but separate scientific encoder family; head mechanics identical.
    d4=TypedSpanHead(H,64,4)
    zz=d4(x); pp,vv=synthetic_span_masks(B,4,L)
    loss4=multilabel_categorical_loss(zz,pp,vv)
    n4=train_step(d4,loss4)

    # Deterministic reconstruction check.
    set_seed(44)
    a=TypedSpanHead(H,64,4)
    set_seed(44)
    b=TypedSpanHead(H,64,4)
    if any(not torch.equal(pa,pb) for pa,pb in zip(a.parameters(),b.parameters())):
        raise RuntimeError("seeded initialization nondeterministic")

    return {
      "state":"FEDERATION_D0_D4_ARCHITECTURE_SYNTHETIC_PREFLIGHT_PASS",
      "scientific_data_used":False,
      "scientific_encoder_loaded":False,
      "scientific_training_performed":False,
      "torch_version":torch.__version__,
      "fixture":{"batch":B,"length":L,"hidden":H},
      "D0":{"loss":float(loss0.detach()),"trainable_parameters":sum(p.numel() for p in d0.parameters()),"gradient_parameters":n0,"viterbi_valid":True,"decoded_fixture":seq},
      "D1":{"loss":float(loss1.detach()),"trainable_parameters":sum(p.numel() for p in d1.parameters()),"gradient_parameters":n1,"score_shape":list(z1.shape)},
      "D2":{"loss":float(loss2.detach()),"native_parameters":sum(p.numel() for p in d2_native.parameters()),"aux_parameters":sum(p.numel() for p in d2_aux.parameters()),"native_gradient_parameters":n2a,"aux_gradient_parameters":n2b,"auxiliary_weight":0.25},
      "D3":{"loss":float(loss3.detach()),"native_parameters":sum(p.numel() for p in d3_native.parameters()),"aux_parameters":sum(p.numel() for p in d3_aux.parameters()),"native_gradient_parameters":n3a,"aux_gradient_parameters":n3b,"auxiliary_weight":0.25},
      "D4":{"loss":float(loss4.detach()),"trainable_head_parameters":sum(p.numel() for p in d4.parameters()),"gradient_parameters":n4,"mechanics_same_span_head_as_D1":True},
      "D5":"CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS",
      "seeded_head_initialization_deterministic":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight: raise SystemExit("Only synthetic preflight authorized")
    d=preflight()
    s=json.dumps(d,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(s,encoding="utf-8")
    print(s,end="")
if __name__=="__main__":main()
