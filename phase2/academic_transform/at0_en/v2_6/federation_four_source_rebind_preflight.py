#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re

ROOT_REL = pathlib.Path("phase2/academic_transform/at0_en/v2_6")

FILES = {
    "final_review": "FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md",
    "evidence_verification": "FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2_EVIDENCE_VERIFICATION_V1.json",
    "reversion_freeze": "AT0_EN_V26_SURUS_PAUSE_FOUR_SOURCE_REVERSION_FREEZE_V1.md",
    "sampler_contract": "AT0_EN_V26_FEDERATION_FOUR_SOURCE_SAMPLER_CONTRACT_V1.json",
    "protocol": "AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md",
    "source_admission": "AT0_EN_V26_FEDERATION_SOURCE_ADMISSION_V1.json",
    "source_pin": "AT0_EN_V26_FEDERATION_SOURCE_PIN_MANIFEST_V1.json",
    "runtime_contract": "AT0_EN_V26_FEDERATION_SCIENTIFIC_RUNTIME_CONTRACT_V1.json",
    "attempt_manifest": "AT0_EN_V26_FEDERATION_DEVELOPMENT_ATTEMPT_MANIFEST_V1.json",
    "data_custody_freeze": "AT0_EN_V26_FEDERATION_PER_FOLD_DATA_MANIFEST_CUSTODY_FREEZE_V1.md",
    "architecture_preflight": "federation_architecture_preflight.py",
    "adapter_contract": "AT0_EN_V26_FEDERATION_ADAPTER_CONTRACT_V1.md",
}

EXPECTED_AUX = ["EBM", "TrialSieve", "EvidenceOutcomes", "PICO"]
EXPECTED_DATA_HASHES = {
    0: "7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0",
    1: "1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02",
    2: "eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939",
}


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str):
    raise RuntimeError(msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--commit", required=True)
    args = ap.parse_args()

    base = args.repo_root / ROOT_REL
    p = {k: base / v for k, v in FILES.items()}
    for k, path in p.items():
        if not path.is_file():
            fail(f"missing required file {k}: {path}")

    review = p["final_review"].read_text(encoding="utf-8")
    if "**REJECT_OR_PAUSE_SURUS**" not in review:
        fail("final review verdict missing")
    if "**FREEZE_SURUS_PAUSE_AND_REBIND_ORIGINAL_FOUR_SOURCE_PREFIT_MANIFESTS**" not in review:
        fail("authorized next operation missing")

    ev = load_json(p["evidence_verification"])
    if ev.get("verdict") != "REJECT_OR_PAUSE_SURUS":
        fail("evidence verification verdict mismatch")
    if ev.get("evidence_zip", {}).get("internal_manifest_hash_mismatches") != 0:
        fail("evidence package has hash mismatches")

    sampler = load_json(p["sampler_contract"])
    srcs = sampler.get("auxiliary_sources", [])
    if [x.get("key") for x in srcs] != EXPECTED_AUX:
        fail(f"sampler source order mismatch: {[x.get('key') for x in srcs]}")
    if sampler.get("auxiliary_documents_per_optimizer_update") != 8:
        fail("auxiliary batch total is not 8")
    if any(x.get("documents_per_aux_update") != 2 for x in srcs):
        fail("four-source sampler is not 2/2/2/2")
    if any(abs(float(x.get("total_loss_coefficient")) - 0.0625) > 1e-12 for x in srcs):
        fail("per-source coefficient is not 0.0625")
    if abs(sum(float(x["total_loss_coefficient"]) for x in srcs) - 0.25) > 1e-12:
        fail("auxiliary coefficients do not sum to 0.25")
    if sampler.get("exclusions", {}).get("SURUS") != "PAUSED_NOT_ADMITTED_CURRENT_CAMPAIGN":
        fail("SURUS sampler exclusion not frozen")
    if sampler.get("scientific_training_authorized") is not False:
        fail("sampler unexpectedly authorizes training")

    admission = load_json(p["source_admission"])
    admission_text = json.dumps(admission, sort_keys=True).lower()
    if "surus" in admission_text:
        fail("SURUS unexpectedly present in source admission V1")
    admitted_aux_roles = {
        e.get("role") for e in admission.get("entries", [])
        if e.get("role") in {
            "auxiliary_pio",
            "auxiliary_native_26_type",
            "auxiliary_native_20_type",
            "auxiliary_outcome_only",
        }
    }
    expected_roles = {
        "auxiliary_pio",
        "auxiliary_native_26_type",
        "auxiliary_native_20_type",
        "auxiliary_outcome_only",
    }
    if admitted_aux_roles != expected_roles:
        fail(f"source admission auxiliary roles mismatch: {sorted(admitted_aux_roles)}")

    source_pin = load_json(p["source_pin"])
    if any("surus" in json.dumps(x, sort_keys=True).lower() for x in source_pin.get("repositories", [])):
        fail("SURUS unexpectedly present in source pin V1")

    runtime = load_json(p["runtime_contract"])
    if runtime.get("scientific_training_authorized") is not False:
        fail("runtime contract unexpectedly authorizes scientific training")
    pending = runtime.get("scientific_execution_runtime", {}).get("gpu_specific_fields_pending", [])
    if not pending:
        fail("GPU-specific runtime unexpectedly appears closed")

    attempts = load_json(p["attempt_manifest"])
    active = [a for a in attempts["attempts"] if a["arm"] in {"D0","D1","D2","D3","D4"}]
    d5 = [a for a in attempts["attempts"] if a["arm"] == "D5"]
    if len(active) != 45:
        fail(f"active attempt count {len(active)} != 45")
    if len({a["attempt_id"] for a in active}) != 45:
        fail("active attempt IDs not unique")
    if any(a.get("state") != "NOT_STARTED" or a.get("consumed") is not False or a.get("scientific_training_authorized") is not False for a in active):
        fail("one or more active attempts already started/consumed/authorized")
    if len(d5) != 9:
        fail("D5 slot count != 9")
    if any(a.get("state") != "CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS" or a.get("consumed") is not False for a in d5):
        fail("D5 cancellation state mismatch")
    by_fold = {}
    for fold in (0,1,2):
        hs = {a["data_manifest_sha256"] for a in active if int(a["fold"]) == fold}
        if hs != {EXPECTED_DATA_HASHES[fold]}:
            fail(f"fold {fold} data hash mismatch: {hs}")
        by_fold[str(fold)] = next(iter(hs))
    if {a.get("runtime_manifest_sha256") for a in active} != {"PENDING_GPU_QUALIFICATION"}:
        fail("active runtime binding is not uniformly pending GPU qualification")

    arch = p["architecture_preflight"].read_text(encoding="utf-8")
    required_arch = [
        "self.ebm=TypedSpanHead(h,64,3)",
        "self.trialsieve=TypedSpanHead(h,64,20)",
        "self.evidence=TypedSpanHead(h,64,1)",
        "self.pico=TypedSpanHead(h,64,26)",
        "native_loss+.25*torch.stack(aux_losses).mean()",
        "native3+.25*torch.stack(al).mean()",
    ]
    normalized = re.sub(r"\s+", "", arch)
    for sig in [re.sub(r"\s+", "", s) for s in required_arch]:
        if sig not in normalized:
            fail(f"four-source architecture signature missing: {sig}")
    if "surus" in normalized.lower():
        fail("SURUS unexpectedly present in four-source architecture preflight")

    data_freeze = p["data_custody_freeze"].read_text(encoding="utf-8")
    if "37897592120" not in data_freeze or "11601066403" not in data_freeze:
        fail("expected per-fold data manifest evidence IDs missing")

    attempt_ids = sorted(a["attempt_id"] for a in active)
    attempt_ids_sha = hashlib.sha256(("\n".join(attempt_ids)+"\n").encode()).hexdigest()

    file_hashes = {k: sha256_file(path) for k, path in p.items()}

    out = {
        "schema": "ACAD_PASS_FEDERATION_FOUR_SOURCE_PREFIT_REBIND_PREFLIGHT_V1",
        "state": "PASS_FOUR_SOURCE_PREFIT_REBIND",
        "git_commit": args.commit,
        "scientific_training_performed": False,
        "scientific_training_authorized": False,
        "protected_data_opened": False,
        "surus_diagnostic_repeated": False,
        "verdict": "REJECT_OR_PAUSE_SURUS",
        "active_auxiliary_sources": EXPECTED_AUX,
        "auxiliary_documents_per_optimizer_update": 8,
        "documents_per_source_per_aux_update": 2,
        "total_auxiliary_coefficient": 0.25,
        "effective_coefficient_per_source": 0.0625,
        "active_attempt_count": len(active),
        "active_attempt_ids_sha256": attempt_ids_sha,
        "active_attempt_ids": attempt_ids,
        "active_attempts_not_started_unconsumed_unauthorized": True,
        "d5_canceled_slots": len(d5),
        "d5_consumed_slots": sum(bool(a.get("consumed")) for a in d5),
        "per_fold_data_manifest_sha256": by_fold,
        "per_fold_data_evidence_run_id": 37897592120,
        "per_fold_data_evidence_artifact_id": 11601066403,
        "gpu_runtime_binding": "PENDING_GPU_QUALIFICATION",
        "runtime_gpu_fields_pending": pending,
        "file_sha256": file_hashes,
        "binding_interpretation": "Versioned non-scientific rebind of the already-existing four-source execution path after SURUS pause. Existing V1 manifests are preserved; no scientific attempt is consumed."
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
