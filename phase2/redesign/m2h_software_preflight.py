#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys
from datetime import datetime, timezone

MODEL_ID="CAMeL-Lab/text-editing-qalb14-nopnx"
CAMEL_TOOLS_SHA="be79ca9fc493f0df795375a7255bafef246a802d"
OUT=pathlib.Path("m2h_preflight")
OUT.mkdir(exist_ok=True)

def sha256_file(p: pathlib.Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def hash_tree(root: pathlib.Path):
    rows=[]
    if not root.exists():
        return rows
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rows.append({"path":str(p.relative_to(root)),"bytes":p.stat().st_size,"sha256":sha256_file(p)})
    return rows

result={
    "record_id":"M2H_SOFTWARE_FEASIBILITY_PREFLIGHT_V1",
    "timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "evaluation_data_read":False,
    "qalb_read":False,
    "confirmation_opened":False,
    "holdout_opened":False,
    "a7ta_reserved_opened":False,
    "h1":{},
    "h3":{},
    "smoke_tests":{},
    "status":"STARTED"
}

# H1: resolve and snapshot exact HF revision, then hash every local artifact.
from huggingface_hub import HfApi, snapshot_download
api=HfApi()
info=api.model_info(MODEL_ID)
resolved_revision=info.sha
model_dir=pathlib.Path(snapshot_download(
    repo_id=MODEL_ID,
    revision=resolved_revision,
    local_dir=str(OUT/"h1_model"),
    local_dir_use_symlinks=False
))
h1_hashes=hash_tree(model_dir)
result["h1"]={
    "model_id":MODEL_ID,
    "resolved_revision":resolved_revision,
    "file_count":len(h1_hashes),
    "files":h1_hashes
}

# H1 smoke test: generic token-classification load and synthetic Arabic inference only.
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
tok=AutoTokenizer.from_pretrained(model_dir)
model=AutoModelForTokenClassification.from_pretrained(model_dir)
sample="هذا اختبار عربي بسيط"
enc=tok(sample,return_tensors="pt")
with torch.no_grad():
    out=model(**enc)
result["smoke_tests"]["h1"]={
    "synthetic_text":sample,
    "input_shape":list(enc["input_ids"].shape),
    "logits_shape":list(out.logits.shape),
    "pass":bool(out.logits.ndim==3 and out.logits.shape[0]==1)
}

# H3: install/download was performed by workflow before this script.
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
db=MorphologyDB.builtin_db("calima-msa-r13")
an=Analyzer(db)
words=["والكتاب","بالمدرسة","كتاب"]
counts={w:len(an.analyze(w)) for w in words}
result["smoke_tests"]["h3"]={
    "synthetic_tokens":words,
    "analysis_counts":counts,
    "pass":all(v>0 for v in counts.values())
}

# Hash CAMeL user data tree. This captures the actual morphology data artifacts installed.
camel_root=pathlib.Path(os.environ.get("CAMELTOOLS_DATA",pathlib.Path.home()/".camel_tools"))
camel_hashes=hash_tree(camel_root)
result["h3"]={
    "camel_tools_git_sha":CAMEL_TOOLS_SHA,
    "data_root":str(camel_root),
    "file_count":len(camel_hashes),
    "files":camel_hashes
}

# Environment lock and summary.
freeze=subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True)
(OUT/"M2H_PREFLIGHT_PIP_FREEZE.txt").write_text(freeze,encoding="utf-8")
result["environment_lock_sha256"]=sha256_file(OUT/"M2H_PREFLIGHT_PIP_FREEZE.txt")
result["versions"]={
    "python":sys.version,
    "torch":torch.__version__
}
import transformers, huggingface_hub, camel_tools
result["versions"].update({
    "transformers":transformers.__version__,
    "huggingface_hub":huggingface_hub.__version__,
    "camel_tools":getattr(camel_tools,"__version__","unknown")
})
result["status"]="PASS" if all(x.get("pass") for x in result["smoke_tests"].values()) else "FAIL"
(OUT/"M2H_PREFLIGHT_RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({
    "status":result["status"],
    "h1_revision":resolved_revision,
    "h1_files":len(h1_hashes),
    "camel_data_files":len(camel_hashes),
    "smoke_tests":result["smoke_tests"],
    "environment_lock_sha256":result["environment_lock_sha256"]
},ensure_ascii=False,indent=2))
