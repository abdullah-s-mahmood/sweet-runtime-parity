from __future__ import annotations
import hashlib, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[4]

PROTOCOL=HERE/"GATE_C_PROTOCOL_FINAL_V1.md"
PIPELINE=HERE/"PRE_GATE_C_PIPELINE_FREEZE_MANIFEST_V1.json"
PIPE_CLOSURE=HERE/"PRE_GATE_C_PIPELINE_FREEZE_CLOSURE.md"
RESPONSE=HERE/"PRE_GATE_C_HIGHER_MODEL_RESPONSE_V1.md"
OUT=HERE/"GATE_C_PROTOCOL_FINAL_INTEGRITY_SUMMARY.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

text=PROTOCOL.read_text(encoding="utf-8")
manifest=json.loads(PIPELINE.read_text(encoding="utf-8"))

required=[
    "80 original studies/papers",
    "200",
    "Gold REJECT -> automatic PASS:",
    "**0/80**",
    "Gold REVIEW -> automatic PASS:",
    "**0/40**",
    "**>=60/80 = 75%**",
    "**>=36/40 = 90%**",
    "original source study/paper",
    "prediction",
    "gold",
    "neutral item identifiers",
    "cluster bootstrap",
    "U = 1 - 0.05^(1/n)",
    "299 independent decisions",
    "NO GATE C SOURCE SAMPLING OR OPENING IS AUTHORIZED",
]
for q in required:
    assert q in text,q

# Ensure final protocol does not authorize execution.
for forbidden in [
    "Status: EXECUTED",
    "HOLDOUT OPENED",
    "PREDICTIONS COMPLETE",
]:
    assert forbidden not in text,forbidden

# Verify all pipeline components still match the freeze manifest.
component_checks=0
resolved=[]
for c in manifest["components"]:
    p=ROOT/c["path"]
    assert p.exists(),c["path"]
    actual=sha(p)
    exp=c.get("expected_sha256")
    if exp:
        assert actual==exp,(c["path"],actual,exp)
    component_checks+=1
    resolved.append({"path":c["path"],"sha256":actual})

summary={
    "gate":"AT0_EN_V2_4_PRE_GATE_C_FINAL_PROTOCOL_INTEGRITY",
    "status":"PASS",
    "holdout_opened":False,
    "source_sampling_authorized":False,
    "protocol_checks_passed":len(required)+3,
    "pipeline_component_checks":component_checks,
    "pipeline_components":resolved,
    "hashes":{
        "final_protocol_sha256":sha(PROTOCOL),
        "pipeline_manifest_sha256":sha(PIPELINE),
        "pipeline_freeze_closure_sha256":sha(PIPE_CLOSURE),
        "higher_model_response_sha256":sha(RESPONSE),
    }
}
OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
