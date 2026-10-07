#!/usr/bin/env python3
from __future__ import annotations
import argparse, itertools, json, pathlib, hashlib, collections
import torch
from torch import nn

CLASSES=["NONE","P","I","C","O"]
TYPES=["P","I","C","O"]
SECTIONS=["TITLE","METHODS","UNKNOWN"]

def sha256(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

class J0(nn.Module):
    def __init__(self):
        super().__init__()
        self.proj=nn.ModuleList([nn.Linear(768,128) for _ in range(5)])
        self.edge_prev=nn.Parameter(torch.zeros(768))
        self.edge_next=nn.Parameter(torch.zeros(768))
        self.width=nn.Embedding(64,16)
        self.btype=nn.Embedding(4,16)
        self.section=nn.Embedding(3,8)
        self.norm=nn.LayerNorm(685)
        self.ff=nn.Linear(685,128)
        self.drop=nn.Dropout(.1)
        self.out=nn.Linear(128,5)
    def project(self,start,end,inside,prev,nxt,prev_edge,next_edge,width,btype,section,scalars):
        prev=torch.where(prev_edge[:,None],self.edge_prev[None,:],prev)
        nxt=torch.where(next_edge[:,None],self.edge_next[None,:],nxt)
        ps=[m(x) for m,x in zip(self.proj,[start,end,inside,prev,nxt])]
        z=torch.cat(ps+[self.width(width-1),self.btype(btype),self.section(section),scalars],dim=-1)
        if z.shape[-1]!=685: raise RuntimeError(f"feature dim {z.shape[-1]}")
        return ps,self.norm(z)
    def forward(self,*args):
        ps,z=self.project(*args)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        return self.out(h)

class J1(J0):
    def __init__(self):
        super().__init__()
        self.U=nn.Parameter(torch.empty(5,129,129))
        nn.init.xavier_uniform_(self.U)
    def forward(self,*args):
        ps,z=self.project(*args)
        h=self.drop(torch.nn.functional.gelu(self.ff(z)))
        base=self.out(h)
        b=z.shape[0]; ones=torch.ones((b,1),dtype=z.dtype,device=z.device)
        sa=torch.cat([ps[0],ones],dim=-1); ea=torch.cat([ps[1],ones],dim=-1)
        return base+torch.einsum("bi,kij,bj->bk",sa,self.U,ea)

def mechanics():
    torch.manual_seed(44)
    b=8
    vec=[torch.randn(b,768) for _ in range(5)]
    pe=torch.tensor([1,0,0,1,0,0,1,0],dtype=torch.bool)
    ne=~pe
    width=torch.tensor([1,2,3,4,5,8,16,64],dtype=torch.long)
    btype=torch.tensor([0,1,2,3,0,1,2,3],dtype=torch.long)
    section=torch.tensor([0,1,2,0,1,2,0,1],dtype=torch.long)
    scalars=torch.rand(b,5)
    y=torch.tensor([0,1,2,3,4,0,2,4],dtype=torch.long)
    out={}
    expected={"J0":584631,"J1":667836}
    for name,cls in [("J0",J0),("J1",J1)]:
        torch.manual_seed(44); m=cls()
        n=sum(p.numel() for p in m.parameters() if p.requires_grad)
        if n!=expected[name]: raise RuntimeError(f"{name} param mismatch {n}!={expected[name]}")
        logits=m(*vec,pe,ne,width,btype,section,scalars)
        if list(logits.shape)!=[b,5]: raise RuntimeError(f"{name} shape {list(logits.shape)}")
        loss=nn.CrossEntropyLoss()(logits,y); loss.backward()
        if not torch.isfinite(loss): raise RuntimeError(f"{name} nonfinite loss")
        if not all(p.grad is None or torch.isfinite(p.grad).all() for p in m.parameters()):
            raise RuntimeError(f"{name} nonfinite grad")
        out[name]={"parameters":n,"shape":list(logits.shape),"loss":float(loss.detach())}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--design-source",type=pathlib.Path,required=True)
    ap.add_argument("--design-summary",type=pathlib.Path,required=True)
    ap.add_argument("--r44a-summary",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)

    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720":
        raise RuntimeError("manifest identity")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    if len(design)!=256 or len(verify)!=64 or design&verify or design&oldsel or verify&oldsel:
        raise RuntimeError("top-level split guard")

    foldmap={int(x["fold"]):set(x["documents"]) for x in m["oof_folds"]}
    if set(foldmap)!=set(range(5)): raise RuntimeError("fold ids")
    union=set(); total=0
    for k,v in foldmap.items():
        if union&v: raise RuntimeError(f"fold overlap {k}")
        union|=v; total+=len(v)
    if union!=design or total!=256: raise RuntimeError("fold union")

    ds=json.loads(a.design_source.read_text())
    dss=json.loads(a.design_summary.read_text())
    if ds.get("state")!="R44_DESIGN_SOURCE_MATERIALIZED" or dss.get("state")!="R44_DESIGN_SOURCE_PACKAGE_PASS":
        raise RuntimeError("design source state")
    if sha256(a.design_source)!=dss.get("design_source_sha256"):
        raise RuntimeError("design source SHA")
    source_docs={int(x["original_document"]) for x in ds["documents"]}
    if source_docs!=design or source_docs&verify or source_docs&oldsel:
        raise RuntimeError("physical DESIGN isolation")

    r44a=json.loads(a.r44a_summary.read_text())
    if r44a.get("state")!="R44A_OOF_BANK_COMPLETE" or r44a.get("design_documents")!=256:
        raise RuntimeError("R44A aggregate identity")
    if r44a.get("candidate_rows")!=1942 or r44a.get("candidate_bank_sha256")!="6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946":
        raise RuntimeError("R44A aggregate mismatch")

    pairs=[]
    for a0,b0 in itertools.combinations(range(5),2):
        train=design-foldmap[a0]-foldmap[b0]
        if train&foldmap[a0] or train&foldmap[b0] or train&verify or train&oldsel:
            raise RuntimeError(f"pair isolation {a0},{b0}")
        if len(train)+len(foldmap[a0])+len(foldmap[b0])!=256:
            raise RuntimeError(f"pair partition {a0},{b0}")
        pairs.append({
          "pair":[a0,b0],
          "train_documents":len(train),
          "train_ids_sha256":hashlib.sha256(json.dumps(sorted(train)).encode()).hexdigest(),
          "heldout_a_documents":len(foldmap[a0]),
          "heldout_b_documents":len(foldmap[b0]),
        })
    if len(pairs)!=10: raise RuntimeError("pair count")

    outer=[]
    logical_edges=0
    pair_usage=collections.Counter()
    for k in range(5):
        outer_eval=foldmap[k]; outer_train=design-outer_eval
        covered=set()
        assembly=[]
        for j in range(5):
            if j==k: continue
            key=tuple(sorted((k,j))); pair_usage[key]+=1; logical_edges+=1
            physical_train=design-foldmap[key[0]]-foldmap[key[1]]
            if outer_eval & physical_train: raise RuntimeError(f"outer leakage k={k} j={j}")
            if foldmap[j] & physical_train: raise RuntimeError(f"row self leakage k={k} j={j}")
            if covered & foldmap[j]: raise RuntimeError("meta overlap")
            covered |= foldmap[j]
            assembly.append({"inner_validation_fold":j,"pair":list(key),"prediction_side":j,
                             "physical_train_documents":len(physical_train)})
        if covered!=outer_train: raise RuntimeError(f"outer train coverage {k}")
        outer.append({"outer_fold":k,"outer_eval_documents":len(outer_eval),
                      "outer_train_documents":len(outer_train),"meta_assembly":assembly})
    if logical_edges!=20 or len(pair_usage)!=10 or any(v!=2 for v in pair_usage.values()):
        raise RuntimeError("10-pair reduction proof failure")

    mech=mechanics()
    out={
      "state":"R44B_B1_PREFLIGHT_PASS",
      "manifest_sha256":m["manifest_sha256"],
      "design_source_sha256":sha256(a.design_source),
      "r44a_candidate_bank_sha256":r44a["candidate_bank_sha256"],
      "design_documents":256,
      "verify_internal_accessed":False,
      "old_select_accessed":False,
      "protected_data_accessed":False,
      "logical_inner_upstream_fits":20,
      "unique_physical_pair_upstream_fits":10,
      "pair_usage_count":{"-".join(map(str,k)):v for k,v in sorted(pair_usage.items())},
      "pair_jobs":pairs,
      "outer_assemblies":outer,
      "head_mechanics":mech,
      "head_schedule":{"seed":44,"epochs":10,"batch":64,"optimizer":"AdamW","lr":1e-3,
                       "weight_decay":.01,"loss":"ordinary_5way_cross_entropy",
                       "thresholds":[.80,.85,.90,.95],"early_stopping":False},
      "parallelization":{"pair_jobs_independent":True,"authorized_max_parallel_after_separate_training_authorization":10},
      "next_action":"FREEZE_PREFLIGHT_RESULT_AND_AUTHORIZE_10_PAIR_PARALLEL_UPSTREAM_GENERATION_ONLY",
    }
    (a.out/"R44B_B1_PREFLIGHT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    md=[
      "# ACAD_PASS — R44-B B1 Preflight",
      "",
      "**Verdict:** `R44B_B1_PREFLIGHT_PASS`",
      "",
      "- DESIGN documents: 256",
      "- Logical outer/inner upstream fits: 20",
      "- Unique physical pair-exclusion fits: 10",
      "- Every physical pair is reused by exactly two outer assemblies.",
      "- No pair model sees either excluded fold.",
      "- Every outer meta-training row is generated by a model excluding both the row fold and outer-eval fold.",
      "- J0 parameters: 584631",
      "- J1 parameters: 667836",
      "- No VERIFY_INTERNAL / old SELECT / protected data access.",
      "",
      "Next: separately authorize the 10 independent pair-exclusion scientific jobs, max-parallel=10."
    ]
    (a.out/"R44B_B1_PREFLIGHT.md").write_text("\n".join(md)+"\n")
    print(json.dumps({"state":out["state"],"logical":20,"physical":10,"J0":584631,"J1":667836},indent=2))

if __name__=="__main__": main()
