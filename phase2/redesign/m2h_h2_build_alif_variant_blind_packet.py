#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SALT = "M2H-H2-ALIF-VARIANT-BLIND-V1-20260930-A"
EXPECTED_UNSUPPORTED = 802
EXPECTED_SUPPORTED = 18536
N_UNSUPPORTED_SAMPLE = 200
N_CONTROL_SAMPLE = 50

def H(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def apply_candidate(source: str, span, replacement: str) -> str:
    toks = source.split()
    a, b = span
    if not (0 <= a <= b <= len(toks)):
        raise ValueError("span out of bounds")
    rep = replacement.split() if replacement else []
    out = toks[:a] + rep + toks[b:]
    return " ".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--inference", required=True)
    ap.add_argument("--out-dir", default="m2h_h2_alif_variant_blind_v1")
    args = ap.parse_args()

    from m2h_h2_calibrate import common_gate, match_families

    candidates = [
        json.loads(x) for x in Path(args.candidates).read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    inf = {
        r["case_id"]: r
        for r in (
            json.loads(x) for x in Path(args.inference).read_text(encoding="utf-8").splitlines()
            if x.strip()
        )
    }

    family = []
    for c in candidates:
        gate, _ = common_gate(c)
        if gate and "ALIF_VARIANT" in match_families(c["source_surface"], c["candidate_replacement"]):
            family.append(c)

    unsupported = [c for c in family if c["gold_support"] == "REFERENCE_UNSUPPORTED"]
    supported = [c for c in family if c["gold_support"] == "EXACT_GOLD_SUPPORTED"]

    if len(unsupported) != EXPECTED_UNSUPPORTED:
        raise SystemExit(f"unsupported population mismatch: {len(unsupported)}")
    if len(supported) != EXPECTED_SUPPORTED:
        raise SystemExit(f"supported population mismatch: {len(supported)}")

    unsupported.sort(key=lambda c: (H(f"{SALT}|UNSUPPORTED|{c['candidate_id']}"), c["candidate_id"]))
    supported.sort(key=lambda c: (H(f"{SALT}|CONTROL|{c['candidate_id']}"), c["candidate_id"]))

    selected = [(c, "UNSUPPORTED") for c in unsupported[:N_UNSUPPORTED_SAMPLE]]
    selected += [(c, "CONTROL") for c in supported[:N_CONTROL_SAMPLE]]
    selected.sort(key=lambda z: (H(f"{SALT}|PACKET|{z[0]['candidate_id']}"), z[0]["candidate_id"]))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    packet = []
    key = []
    for idx, (c, pop) in enumerate(selected, 1):
        src = inf[c["case_id"]]["source"]
        candidate_sentence = apply_candidate(src, c["source_span"], c["candidate_replacement"])
        packet_id = f"M2H-H2-AV-BLIND-{idx:04d}"

        packet.append({
            "packet_id": packet_id,
            "source_sentence": src,
            "source_span_token_indices": c["source_span"],
            "source_surface": c["source_surface"],
            "candidate_replacement": c["candidate_replacement"],
            "candidate_sentence": candidate_sentence,
            "reviewer_fields": {
                "necessity": None,
                "candidate_correctness": None,
                "meaning_fidelity": None,
                "final_blinded_disposition": None,
                "brief_rationale": None,
            }
        })
        key.append({
            "packet_id": packet_id,
            "candidate_id": c["candidate_id"],
            "case_id": c["case_id"],
            "uid": c["uid"],
            "hidden_population": pop,
            "hidden_gold_support": c["gold_support"],
        })

    packet_path = out_dir / "M2H_H2_ALIF_VARIANT_BLIND_PACKET_V1.jsonl"
    key_path = out_dir / "M2H_H2_ALIF_VARIANT_BLIND_KEY_V1.jsonl"

    packet_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in packet) + "\n",
        encoding="utf-8"
    )
    key_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in key) + "\n",
        encoding="utf-8"
    )

    packet_sha = hashlib.sha256(packet_path.read_bytes()).hexdigest()
    key_sha = hashlib.sha256(key_path.read_bytes()).hexdigest()

    summary = {
        "record_id": "M2H_H2_ALIF_VARIANT_BLIND_PACKET_V1",
        "status": "PASS",
        "salt": SALT,
        "family": "ALIF_VARIANT",
        "population": {
            "unsupported": len(unsupported),
            "exact_supported": len(supported),
        },
        "sample": {
            "unsupported": N_UNSUPPORTED_SAMPLE,
            "hidden_controls": N_CONTROL_SAMPLE,
            "packet_total": len(packet),
        },
        "blinding": {
            "packet_contains_gold_support": False,
            "packet_contains_qalb_reference": False,
            "packet_contains_h1_identity_or_confidence": False,
            "key_is_separate": True,
        },
        "sha256": {
            "blind_packet": packet_sha,
            "blind_key": key_sha,
        },
        "integrity": {
            "unique_packet_ids": len({x["packet_id"] for x in packet}) == len(packet),
            "unique_candidate_ids_in_key": len({x["candidate_id"] for x in key}) == len(key),
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "reserved_nahw_opened": False,
            "qalb15_test_opened": False,
        }
    }
    (out_dir / "M2H_H2_ALIF_VARIANT_BLIND_PACKET_SUMMARY_V1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
