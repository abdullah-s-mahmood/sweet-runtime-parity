from __future__ import annotations
import argparse,gc,hashlib,json,os,pathlib,socket,sys,time

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def rss_kb():
    try:
        for line in pathlib.Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"): return int(line.split()[1])
    except Exception: pass
    return None

ap=argparse.ArgumentParser()
ap.add_argument("--hhem",required=True)
ap.add_argument("--flan",required=True)
ap.add_argument("--deberta",required=True)
ap.add_argument("--hash-lock",required=True)
ap.add_argument("--output",required=True)
args=ap.parse_args()
dirs={k:pathlib.Path(v).resolve() for k,v in {"hhem":args.hhem,"flan_runtime_dependency":args.flan,"deberta_nli":args.deberta}.items()}
lock=json.loads(pathlib.Path(args.hash_lock).read_text())
section={"hhem":"hhem","flan_runtime_dependency":"flan_runtime_dependency","deberta_nli":"deberta_nli"}
checks=[]
for key,d in dirs.items():
    files=lock[section[key]]["files"]
    for name,expected in files.items():
        p=d/name
        actual=sha256(p)
        ok=actual==expected
        checks.append({"group":key,"file":name,"expected":expected,"actual":actual,"match":ok})
        if not ok: raise SystemExit(f"HASH_MISMATCH:{key}:{name}")

os.environ["HF_HUB_OFFLINE"]="1"
os.environ["TRANSFORMERS_OFFLINE"]="1"
os.environ["HF_DATASETS_OFFLINE"]="1"

# Block network after artifact acquisition.
_orig_connect=socket.socket.connect
def _blocked_connect(self,*a,**kw):
    raise RuntimeError("NETWORK_FORBIDDEN_DURING_LOAD_ONLY_SMOKE")
socket.socket.connect=_blocked_connect

import torch
from transformers import AutoConfig,AutoModelForSequenceClassification,AutoTokenizer
import transformers,safetensors,sentencepiece

# Make any forward invocation a hard failure.
_orig_call=torch.nn.Module.__call__
def _forbidden_forward(self,*a,**kw):
    raise RuntimeError("FORWARD_PASS_FORBIDDEN_IN_LOAD_ONLY_SMOKE")
torch.nn.Module.__call__=_forbidden_forward

result={
  "gate":"AT0_EN_V2_4_LOAD_ONLY_COMPATIBILITY_V1",
  "semantic_inference_performed":False,
  "forward_pass_performed":False,
  "network_after_acquisition":False,
  "hash_checks":checks,
  "runtime":{
    "python":sys.version.split()[0],
    "torch":torch.__version__,
    "transformers":transformers.__version__,
    "safetensors":safetensors.__version__,
    "sentencepiece":sentencepiece.__version__ if hasattr(sentencepiece,"__version__") else "unknown"
  },
  "models":[]
}

start=time.time()
hcfg=AutoConfig.from_pretrained(str(dirs["hhem"]),trust_remote_code=True,local_files_only=True)
hcfg.foundation=str(dirs["flan_runtime_dependency"])
htok=AutoTokenizer.from_pretrained(str(dirs["flan_runtime_dependency"]),local_files_only=True)
hmodel=AutoModelForSequenceClassification.from_pretrained(str(dirs["hhem"]),config=hcfg,trust_remote_code=True,local_files_only=True)
result["models"].append({
  "witness_id":"HHEM_2_1_OPEN",
  "class":hmodel.__class__.__name__,
  "config_class":hcfg.__class__.__name__,
  "tokenizer_class":htok.__class__.__name__,
  "parameters":sum(p.numel() for p in hmodel.parameters()),
  "rss_kb_after_load":rss_kb(),
  "load_seconds":round(time.time()-start,3),
  "foundation_local_override":str(dirs["flan_runtime_dependency"]),
  "forward_called":False
})
del hmodel,htok,hcfg
gc.collect()

start=time.time()
dcfg=AutoConfig.from_pretrained(str(dirs["deberta_nli"]),local_files_only=True)
dtok=AutoTokenizer.from_pretrained(str(dirs["deberta_nli"]),local_files_only=True)
dmodel=AutoModelForSequenceClassification.from_pretrained(str(dirs["deberta_nli"]),config=dcfg,local_files_only=True)
labels={str(k):v for k,v in dcfg.id2label.items()}
if labels!={"0":"entailment","1":"neutral","2":"contradiction"}:
    raise SystemExit(f"LABEL_MAP_MISMATCH:{labels}")
result["models"].append({
  "witness_id":"DEBERTA_NLI",
  "class":dmodel.__class__.__name__,
  "config_class":dcfg.__class__.__name__,
  "tokenizer_class":dtok.__class__.__name__,
  "parameters":sum(p.numel() for p in dmodel.parameters()),
  "labels":labels,
  "rss_kb_after_load":rss_kb(),
  "load_seconds":round(time.time()-start,3),
  "forward_called":False
})
del dmodel,dtok,dcfg
gc.collect()

result["status"]="PASS"
out=pathlib.Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(result,indent=2,ensure_ascii=False))
