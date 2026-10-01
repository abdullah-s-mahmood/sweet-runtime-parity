#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

VERSION = "MPSEF_V4_STAGE1_PACKET_BUILDER_V1"
PACKET_VERSION = "MPSEF_V4_STAGE1_PACKET_V1"
EXPECTED_SOURCE_MANIFEST_SHA256 = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
PACKET_SIZE = 128
SALT = "MPSEF-V4-STAGE1-SOURCE-ONLY-20261001-A"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def canonical_json_sha(obj) -> str:
    return sha_text(json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ))


def load_jsonl(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def row_source_identity(row):
    allowed = {
        "case_id",
        "uid",
        "cluster_id",
        "role",
        "source",
        "source_sha256",
        "protected_detector_version",
        "protected_spans",
        "high_confidence_named_entity_detector_active",
    }
    extra = set(row) - allowed
    forbidden = {
        "reference","gold","edits","operations","corrected",
        "target","targets","correction","label","score","metric"
    }
    if forbidden & set(row):
        raise RuntimeError(
            f'{row.get("uid")}: forbidden source-manifest fields: '
            f'{sorted(forbidden & set(row))}'
        )
    # Extra fields are not automatically trusted: preserve no unknown content
    # in the Stage1 packet even if the historical source manifest grows later.
    out = {k: row[k] for k in allowed if k in row}
    if out.get("role") != "C_F":
        raise RuntimeError(f'{row.get("uid")}: non-C_F row')
    if sha_text(out["source"]) != out["source_sha256"]:
        raise RuntimeError(f'{row.get("uid")}: source SHA mismatch')
    return out, sorted(extra)


def rank_cluster(cluster_id: str) -> str:
    return sha_text(f"{SALT}|cluster|{cluster_id}")


def rank_uid(uid: str) -> str:
    return sha_text(f"{SALT}|uid|{uid}")


def build_packet(rows):
    if len(rows) != EXPECTED_CASES:
        raise RuntimeError(f"source case count mismatch: {len(rows)}")
    if len({r["uid"] for r in rows}) != EXPECTED_CASES:
        raise RuntimeError("duplicate source UID")

    clusters = defaultdict(list)
    sanitized = {}
    ignored_extra_fields = set()

    for row in rows:
        clean, extras = row_source_identity(row)
        ignored_extra_fields.update(extras)
        uid = clean["uid"]
        sanitized[uid] = clean
        clusters[clean["cluster_id"]].append(clean)

    if len(clusters) != EXPECTED_CLUSTERS:
        raise RuntimeError(f"source cluster count mismatch: {len(clusters)}")

    ordered_clusters = sorted(
        clusters,
        key=lambda cid: (rank_cluster(str(cid)), str(cid))
    )
    selected_clusters = ordered_clusters[:PACKET_SIZE]

    selected = []
    for cid in selected_clusters:
        candidates = sorted(
            clusters[cid],
            key=lambda r: (rank_uid(str(r["uid"])), str(r["uid"]))
        )
        chosen = dict(candidates[0])
        chosen["stage1_cluster_rank_sha256"] = rank_cluster(str(cid))
        chosen["stage1_uid_rank_sha256"] = rank_uid(str(chosen["uid"]))
        selected.append(chosen)

    # Stable artifact order independent of cluster-selection traversal.
    selected.sort(key=lambda r: str(r["uid"]))

    if len(selected) != PACKET_SIZE:
        raise RuntimeError("packet size mismatch")
    if len({r["uid"] for r in selected}) != PACKET_SIZE:
        raise RuntimeError("packet UID uniqueness failure")
    if len({r["cluster_id"] for r in selected}) != PACKET_SIZE:
        raise RuntimeError("packet cluster uniqueness failure")

    return selected, sorted(ignored_extra_fields)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--registry-sha256", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_V4_STAGE1_PACKET_V1")
    args = ap.parse_args()

    source_path = Path(args.source_manifest)
    actual_source_sha = sha_bytes(source_path.read_bytes())
    if actual_source_sha != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise RuntimeError(
            f"source manifest SHA mismatch: {actual_source_sha}"
        )

    registry_sha = args.registry_sha256.strip().lower()
    if len(registry_sha) != 64 or any(
        ch not in "0123456789abcdef" for ch in registry_sha
    ):
        raise RuntimeError("invalid registry SHA256")

    rows = load_jsonl(source_path)
    packet, ignored_extra_fields = build_packet(rows)

    prefix = Path(args.out_prefix)
    packet_path = Path(str(prefix) + ".jsonl")
    packet_path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True)
            for row in packet
        ) + "\n",
        encoding="utf-8",
    )

    uid_list = [str(r["uid"]) for r in packet]
    cluster_list = [str(r["cluster_id"]) for r in packet]

    uid_list_text = "\n".join(uid_list) + "\n"
    cluster_list_text = "\n".join(cluster_list) + "\n"

    uid_path = Path(str(prefix) + "_UIDS.txt")
    cluster_path = Path(str(prefix) + "_CLUSTERS.txt")
    uid_path.write_text(uid_list_text, encoding="utf-8")
    cluster_path.write_text(cluster_list_text, encoding="utf-8")

    source_row_hashes = [
        {
            "uid": r["uid"],
            "cluster_id": r["cluster_id"],
            "source_sha256": r["source_sha256"],
        }
        for r in packet
    ]
    row_hash_path = Path(str(prefix) + "_SOURCE_ROW_HASHES.json")
    row_hash_path.write_text(
        json.dumps(source_row_hashes, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": PACKET_VERSION,
        "builder_version": VERSION,
        "status": "PASS",
        "selection_salt": SALT,
        "selection_algorithm": (
            "rank clusters by SHA256(salt|cluster|cluster_id); "
            "take first 128; choose lowest SHA256(salt|uid|uid) row per cluster; "
            "sort final packet by uid"
        ),
        "source_manifest_sha256": actual_source_sha,
        "registry_namespace": REGISTRY_NAMESPACE,
        "registry_sha256": registry_sha,
        "packet_cases": len(packet),
        "packet_clusters": len({r["cluster_id"] for r in packet}),
        "packet_sha256": sha_bytes(packet_path.read_bytes()),
        "uid_list_sha256": sha_bytes(uid_path.read_bytes()),
        "cluster_list_sha256": sha_bytes(cluster_path.read_bytes()),
        "source_row_hashes_sha256": sha_bytes(row_hash_path.read_bytes()),
        "ignored_extra_source_manifest_fields": ignored_extra_fields,
        "project_source_loaded": True,
        "project_source_scope": "C_F_SOURCE_ONLY",
        "reference_content_used": False,
        "gold_edit_content_used": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
        "proposer_output_consulted_for_selection": False,
    }

    summary_path = Path(str(prefix) + "_SUMMARY.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
