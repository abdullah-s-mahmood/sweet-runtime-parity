#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_UID_ROLE_CLUSTER_SHA256 = "85a5dcb1b26a9773ea0ef7e04bb42e8e56dde5d44f1e63fcbe54141dbcb47dfc"
DETECTOR_VERSION = "MPSEF_PROTECTED_DETECTOR_V1"

DIGITS = "0-9٠-٩۰-۹"
NUMBER_CORE = rf"[+\-−]?[{DIGITS}]+(?:[.,٫٬][{DIGITS}]+)*(?:[eE][+\-]?[{DIGITS}]+)?"
UNITS = r"(?:kg|g|mg|ug|µg|km|cm|mm|um|µm|nm|m|L|mL|ml|uL|µL|Hz|kHz|MHz|GHz|V|mV|kV|A|mA|W|kW|MW|J|kJ|Pa|kPa|MPa|bar|mol|mmol|s|ms|min|h|K|°C|°F)"

PATTERNS = [
    ("URL_EMAIL", re.compile(r"https?://[^\s]+|www\.[^\s]+|[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("CITATION_DOI", re.compile(r"\b10\.\d{4,9}/[^\s]+|\[(?:\s*[0-9٠-٩۰-۹]+\s*(?:[-–,،]\s*[0-9٠-٩۰-۹]+\s*)*)\]")),
    ("EQUATION_FORMULA", re.compile(r"\$[^$\n]+\$|\\\([^\n]+?\\\)|\\\[[^\n]+?\\\]")),
    ("DOCUMENT_STRUCTURE", re.compile(r"<(?:FIGURE|TABLE|EQUATION|COMMENT|BOOKMARK|FIELD)[^>]*>|\[\[(?:FIGURE|TABLE|EQUATION|COMMENT|BOOKMARK|FIELD)[^\]]*\]\]", re.I)),
    ("NUMBER_UNIT_COUPLED", re.compile(rf"{NUMBER_CORE}\s*{UNITS}\b", re.I)),
    ("CODE_LATIN_TECHNICAL", re.compile(r"(?<![A-Za-z0-9_])[A-Za-z][A-Za-z0-9_.:+/#@\-]*(?![A-Za-z0-9_])")),
    ("NUMBER", re.compile(NUMBER_CORE + r"%?")),
]

def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def make_protected_spans(source: str):
    found = {}
    for category, pattern in PATTERNS:
        for m in pattern.finditer(source):
            if m.start() == m.end():
                continue
            found[(m.start(), m.end(), category)] = m.group(0)
    spans = []
    for idx, ((start, end, category), text) in enumerate(sorted(found.items()), start=1):
        spans.append({
            "protected_id": f"P{idx:04d}",
            "category": category,
            "source_start": start,
            "source_end": end,
            "text": text,
            "detector": DETECTOR_VERSION,
            "confidence": "DETERMINISTIC",
            "hard_protected": True,
        })
    return spans

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--roles", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_CF_SOURCE_MANIFEST_V1")
    args = ap.parse_args()

    role_rows = [
        json.loads(line)
        for line in Path(args.roles).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(role_rows) != 6888:
        raise RuntimeError(f"role manifest length mismatch: {len(role_rows)}")

    digest_payload = "\n".join(
        f'{row["uid"]}\t{row["role"]}\t{row["cluster_id"]}'
        for row in sorted(role_rows, key=lambda x: x["uid"])
    ) + "\n"
    digest = sha_text(digest_payload)
    if digest != EXPECTED_UID_ROLE_CLUSTER_SHA256:
        raise RuntimeError(f"role digest mismatch: {digest}")

    cf_rows = {row["uid"]: row for row in role_rows if row["role"] == "C_F"}
    if len(cf_rows) != EXPECTED_CASES:
        raise RuntimeError(f"C_F case count mismatch: {len(cf_rows)}")
    if len({row["cluster_id"] for row in cf_rows.values()}) != EXPECTED_CLUSTERS:
        raise RuntimeError("C_F cluster count mismatch")

    out_rows = []
    seen = set()
    for line in Path(args.calibration).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        uid = row["uid"]
        if uid not in cf_rows:
            continue

        source = row["source"]
        role = cf_rows[uid]
        out_rows.append({
            "case_id": row["case_id"],
            "uid": uid,
            "cluster_id": role["cluster_id"],
            "role": "C_F",
            "source": source,
            "source_sha256": sha_text(source),
            "protected_detector_version": DETECTOR_VERSION,
            "protected_spans": make_protected_spans(source),
            "high_confidence_named_entity_detector_active": False,
        })
        seen.add(uid)

    if seen != set(cf_rows):
        missing = sorted(set(cf_rows) - seen)[:10]
        raise RuntimeError(f"missing C_F UIDs: {missing}")

    out_rows.sort(key=lambda x: x["uid"])
    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": "MPSEF_CF_SOURCE_MANIFEST_V1",
        "status": "PASS",
        "role": "C_F",
        "cases": len(out_rows),
        "clusters": len({row["cluster_id"] for row in out_rows}),
        "source_manifest_sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
        "protected_detector_version": DETECTOR_VERSION,
        "hard_protection_active": True,
        "high_confidence_named_entity_detector_active": False,
        "reference_content_used": False,
        "gold_edit_content_used": False,
        "feasibility_metric_computed": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }
    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)

if __name__ == "__main__":
    main()
