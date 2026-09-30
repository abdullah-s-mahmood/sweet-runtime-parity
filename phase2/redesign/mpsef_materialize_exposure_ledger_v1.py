#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

REV = "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
BASE = (
    "https://raw.githubusercontent.com/CAMeL-Lab/arabic-gec/"
    + REV
    + "/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
)
PREFIX = {
    "train": "QALB-2014-L1-Train",
    "dev": "QALB-2014-L1-Dev",
}
DOC_RE = re.compile(r"^(.*)_\d+\.ar$")


def norm(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).strip().split())


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def parse_id(full_line: str) -> tuple[str, str]:
    first, sep, rest = full_line.partition(" ")
    if not sep:
        raise RuntimeError("QALB .sent line has no sentence-id separator")
    sid = first.strip()
    m = DOC_RE.match(sid)
    doc = m.group(1) if m else sid
    return sid, rest


def fetch_sentence_ids(split: str, needed_lines: set[int], expected_source_by_line: dict[int, str]):
    url = f"{BASE}/{split}/{PREFIX[split]}.sent"
    tmp = Path(f"qalb14_{split}.sent")
    urllib.request.urlretrieve(url, tmp)

    found = {}
    with tmp.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if line_no not in needed_lines:
                # Do not retain or expose non-CALIBRATION text.
                continue
            sid, text = parse_id(line.rstrip("\n"))
            expected = norm(expected_source_by_line[line_no])
            observed = norm(text)
            if expected != observed:
                raise RuntimeError(
                    f"source mismatch {split}:{line_no}: "
                    f"{sha256_text(expected)} != {sha256_text(observed)}"
                )
            m = DOC_RE.match(sid)
            doc_id = m.group(1) if m else sid
            found[line_no] = {
                "qalb_sentence_id": sid,
                "document_id": doc_id,
            }

    missing = sorted(needed_lines - set(found))
    if missing:
        raise RuntimeError(f"missing QALB ids for {split}: {missing[:20]}")
    tmp.unlink(missing_ok=True)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_EXPOSURE_LEDGER_V1")
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.calibration).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != 6888:
        raise RuntimeError(f"expected 6888 CALIBRATION records, got {len(rows)}")

    by_split_lines = defaultdict(set)
    source_by_split_line = defaultdict(dict)
    for r in rows:
        by_split_lines[r["split"]].add(int(r["line_no"]))
        source_by_split_line[r["split"]][int(r["line_no"])] = r["source"]

    ids = {}
    for split in ("train", "dev"):
        ids[split] = fetch_sentence_ids(
            split,
            by_split_lines[split],
            source_by_split_line[split],
        )

    ledger = []
    for r in rows:
        meta = ids[r["split"]][int(r["line_no"])]
        origin = r["split"]

        training_overlap = {
            "p1_dataset_scope": "QALB-2014",
            "p2_dataset_scope": "QALB-2014",
            "record_level_overlap_verified": False,
            "origin_role": origin,
            "status": (
                "DATASET_SCOPE_CONFIRMED_RECORD_LEVEL_UNRESOLVED"
            ),
            "interpretation": (
                "Development feasibility only; do not treat this record as "
                "independent generalization evidence."
            ),
        }

        ledger.append({
            "case_id": r["case_id"],
            "uid": r["uid"],
            "origin_split": origin,
            "line_no": int(r["line_no"]),
            "qalb_sentence_id": meta["qalb_sentence_id"],
            "document_id": meta["document_id"],
            "author_id": None,
            "author_status": "UNAVAILABLE_IN_CURRENT_ALLOWED_METADATA",
            "source_sha256": sha256_text(norm(r["source"])),
            "source_word_count": len(norm(r["source"]).split()),
            "exposure": {
                "source_only_exposed": "YES",
                "gold_reference_exposed": "YES",
                "aggregate_result_exposed": "YES",
                "error_analysis_exposed": "UNKNOWN",
                "fit_exposed": "NO_PROJECT_MODEL_FIT_KNOWN",
                "threshold_selection_exposed": "NO_FROZEN_GATES_USED",
                "unknown_exposure": "YES",
                "historically_independent": "NO",
            },
            "exposure_basis": [
                "CALIBRATION reference/gold materialized for all 6888 records",
                "H1 official-alignment aggregate feasibility used all records",
                "exact manual/error-analysis exposure per record not reconstructed",
            ],
            "proposer_training_overlap": training_overlap,
        })

    ledger.sort(key=lambda x: x["case_id"])

    out = Path(args.out_prefix + ".jsonl")
    out.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in ledger) + "\n",
        encoding="utf-8",
    )

    counts = Counter(x["origin_split"] for x in ledger)
    docs = {x["document_id"] for x in ledger}
    exact_src = Counter(x["source_sha256"] for x in ledger)

    uid_digest = hashlib.sha256(
        ("\n".join(x["uid"] for x in ledger) + "\n").encode("utf-8")
    ).hexdigest()
    ledger_digest = hashlib.sha256(out.read_bytes()).hexdigest()

    summary = {
        "record_id": "MPSEF_EXPOSURE_LEDGER_V1",
        "status": "PASS",
        "scope": "CALIBRATION_ONLY",
        "cases": len(ledger),
        "origin_counts": dict(counts),
        "document_ids_available": len(docs),
        "author_ids_available": 0,
        "exact_source_duplicate_groups": sum(1 for n in exact_src.values() if n > 1),
        "exact_source_duplicate_records": sum(n for n in exact_src.values() if n > 1),
        "historical_independence": False,
        "all_records_gold_reference_exposed": True,
        "all_records_aggregate_result_exposed": True,
        "record_level_error_analysis_exposure": "UNKNOWN",
        "future_role_split_restores_historical_independence": False,
        "training_overlap": {
            "p1_qalb14_dataset_scope_confirmed": True,
            "p2_qalb14_dataset_scope_confirmed": True,
            "record_level_overlap_verified": False,
            "claim_scope": "DEVELOPMENT_FEASIBILITY_ONLY",
        },
        "uid_sha256": uid_digest,
        "ledger_sha256": ledger_digest,
        "integrity": {
            "calibration_only": True,
            "internal_evaluation_text_materialized": False,
            "stress_diagnostic_text_materialized": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "qalb15_test_opened": False,
        },
    }

    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
