from __future__ import annotations
import hashlib, json, pathlib, py_compile

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[5]
MANIFEST=HERE/"PRE_GATE_C_PIPELINE_FREEZE_MANIFEST_V1.json"
OUT=HERE/"PRE_GATE_C_PIPELINE_FREEZE_INTEGRITY_SUMMARY.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

m=json.loads(MANIFEST.read_text(encoding="utf-8"))
checks=0
resolved=[]
for c in m["components"]:
    p=ROOT/c["path"]
    assert p.exists(), c["path"]
    actual=sha(p)
    exp=c.get("expected_sha256")
    if exp:
        assert actual==exp,(c["path"],actual,exp)
        checks+=1
    resolved.append({**c,"actual_sha256":actual})

# Compile executable Python runtime components.
for p in [
    ROOT/"phase2/academic_transform/at0_en/v2_4/gate_a/source_anchor_extractor.py",
    ROOT/"phase2/academic_transform/at0_en/v2_4/gate_a/source_assertion_extractor.py",
    ROOT/"phase2/academic_transform/at0_en/v2_4/gate_b2/b2_2_relation_aware_extractor.py",
    ROOT/"phase2/academic_transform/at0_en/v2_4/gate_b1/b1_aligner.py",
]:
    py_compile.compile(str(p),doraise=True)
    checks+=1

summary={
    "gate":"AT0_EN_V2_4_PRE_GATE_C_PIPELINE_FREEZE",
    "status":"PASS",
    "model_inference":False,
    "checks_passed":checks,
    "component_count":len(resolved),
    "components":resolved,
    "manifest_sha256":sha(MANIFEST),
}
OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
