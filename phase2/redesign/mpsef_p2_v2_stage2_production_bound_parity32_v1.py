#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


VERSION = "MPSEF_P2_V2_STAGE2_PRODUCTION_BOUND_PARITY32_V1"
EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_FROZEN_P2_SHA = "df89c7dc2c7f177b3c4ca02e8df8a291b6de917a81246c5258f1f66652e1f69e"
EXPECTED_N = 32


def sha_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_text(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def write_jsonl(path: Path, rows):
    path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in rows
        ) + "\n",
        encoding="utf-8",
    )


def legacy_signature(rec):
    keys = [
        "uid",
        "source_sha256",
        "execution_state",
        "output_sha256",
        "morph_word_count",
        "ged_label_count",
        "ged_segment_count",
        "gec_input_length",
        "gec_label_length",
        "generation_token_count",
        "generation_hit_ceiling",
        "terminal_eos_index",
        "decoder_prefix_equals_eos",
        "ged_embedding_hook_call_count",
        "gec_input_ids_sha256",
        "gec_ged_label_ids_sha256",
        "generated_token_ids",
        "word_level_ged_labels",
        "ged_word_identity_trace",
        "ged_segments",
        "gec_word_map",
    ]
    return {k: rec.get(k) for k in keys}


def current_signature(rec):
    return legacy_signature(rec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--frozen-p2", required=True)
    ap.add_argument("--fresh", required=True)
    ap.add_argument("--repeat", required=True)
    ap.add_argument("--reversed", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    frozen_path = Path(args.frozen_p2)
    if sha_file(manifest_path) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_file(frozen_path) != EXPECTED_FROZEN_P2_SHA:
        raise RuntimeError("FROZEN_P2_SHA_MISMATCH")

    manifest = load_jsonl(manifest_path)
    frozen = load_jsonl(frozen_path)
    fresh = load_jsonl(Path(args.fresh))
    repeat = load_jsonl(Path(args.repeat))
    reversed_rows = load_jsonl(Path(args.reversed))

    if len(manifest) != EXPECTED_N:
        raise RuntimeError(f"PARITY32_N_MISMATCH:{len(manifest)}")

    by_frozen = {r["uid"]: r for r in frozen}
    by_fresh = {r["uid"]: r for r in fresh}
    by_repeat = {r["uid"]: r for r in repeat}
    by_reverse = {r["uid"]: r for r in reversed_rows}

    expected_uids = [m["uid"] for m in manifest]
    expected_set = set(expected_uids)
    for name, by in (
        ("frozen", by_frozen),
        ("fresh", by_fresh),
        ("repeat", by_repeat),
        ("reversed", by_reverse),
    ):
        if name == "frozen":
            missing = expected_set - set(by)
            if missing:
                raise RuntimeError(
                    f"{name.upper()}_UIDS_MISSING:{sorted(missing)}"
                )
        elif set(by) != expected_set or len(by) != EXPECTED_N:
            raise RuntimeError(
                f"{name.upper()}_UID_SET_MISMATCH"
            )

    counts = {
        "fresh_vs_repeat": 0,
        "fresh_vs_reordered": 0,
        "fresh_vs_frozen_trace_output": 0,
    }
    rows = []

    for m in manifest:
        uid = m["uid"]
        fr = by_fresh[uid]
        rp = by_repeat[uid]
        rv = by_reverse[uid]
        fz = by_frozen[uid]

        if fr["source_sha256"] != m["source_sha256"]:
            raise RuntimeError(f"FRESH_SOURCE_SHA_MISMATCH:{uid}")
        if sha_text(fr["source"]) != m["source_sha256"]:
            raise RuntimeError(f"FRESH_SOURCE_TEXT_SHA_MISMATCH:{uid}")

        sig_fr = current_signature(fr)
        sig_rp = current_signature(rp)
        sig_rv = current_signature(rv)
        sig_fz = legacy_signature(fz)

        a = sig_fr == sig_rp
        b = sig_fr == sig_rv
        c = sig_fr == sig_fz

        counts["fresh_vs_repeat"] += int(a)
        counts["fresh_vs_reordered"] += int(b)
        counts["fresh_vs_frozen_trace_output"] += int(c)

        mismatch_keys = [
            k for k in sig_fr
            if sig_fr.get(k) != sig_fz.get(k)
        ]

        rows.append({
            "uid": uid,
            "rank_index": m["rank_index"],
            "source_sha256": m["source_sha256"],
            "fresh_execution_state": fr.get("execution_state"),
            "frozen_execution_state": fz.get("execution_state"),
            "fresh_output_sha256": fr.get("output_sha256"),
            "frozen_output_sha256": fz.get("output_sha256"),
            "fresh_vs_repeat": a,
            "fresh_vs_reordered": b,
            "fresh_vs_frozen_trace_output": c,
            "frozen_mismatch_keys": mismatch_keys,
        })

    status = (
        "PASS"
        if all(v == EXPECTED_N for v in counts.values())
        else "FAIL"
    )

    result = {
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "frozen_p2_sha256": EXPECTED_FROZEN_P2_SHA,
        "counts": counts,
        "true_model_batch_call_supported": False,
        "batch_vs_single_parity": (
            "NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION"
        ),
        "rows": rows,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_PARITY32_ONLY",
        "project_gold_loaded": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "quality_claimed": False,
        "production_adapter_cli_used": True,
    }

    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "counts": counts,
        "production_adapter_cli_used": True,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
    }, ensure_ascii=False, indent=2))

    if status != "PASS":
        failures = [
            r for r in rows
            if not (
                r["fresh_vs_repeat"]
                and r["fresh_vs_reordered"]
                and r["fresh_vs_frozen_trace_output"]
            )
        ]
        print(json.dumps(
            {"parity_failures": failures},
            ensure_ascii=False,
            indent=2,
        ))
        raise RuntimeError(
            "P2_STAGE2_PRODUCTION_BOUND_PARITY32_FAILED"
        )


if __name__ == "__main__":
    main()
