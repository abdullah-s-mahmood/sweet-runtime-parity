#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import types
import unicodedata
from pathlib import Path

import torch
from transformers import BertForTokenClassification, BertTokenizer

EXPECTED_MODEL_REV = "21286e56ce98a86362db540863f91c083b8970f9"
EXPECTED_WEIGHT_SHA = "9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d"
EXPECTED_UPSTREAM_REV = "4d552ca3ae98029550f27fc52aa1b22883e16e61"
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
PARITY_SALT = "MPSEF-P1-CF-BATCH-PREFLIGHT-V1-20260930"

def norm(text: str) -> str:
    return " ".join((text or "").strip().split())

def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rank_uid(uid: str) -> str:
    return sha_text(PARITY_SALT + "|" + uid)

def install_rewrite_compat(upstream_root: Path):
    upstream = upstream_root.resolve()
    sys.path.insert(0, str(upstream))
    sys.path.insert(0, str(upstream / "gec"))

    unicode_punct_symbol = frozenset(
        chr(i) for i in range(0x110000)
        if unicodedata.category(chr(i))[0] in {"P", "S"}
    )
    camel_tools_mod = types.ModuleType("camel_tools")
    camel_utils_mod = types.ModuleType("camel_tools.utils")
    camel_charsets_mod = types.ModuleType("camel_tools.utils.charsets")
    camel_normalize_mod = types.ModuleType("camel_tools.utils.normalize")
    camel_charsets_mod.UNICODE_PUNCT_SYMBOL_CHARSET = unicode_punct_symbol
    camel_charsets_mod.AR_LETTERS_CHARSET = frozenset(
        "ءآأؤإئابتثجحخدذرزسشصضطظعغـفقكلمنهوىيٱپچڤگ"
    )
    camel_normalize_mod.normalize_alef_ar = lambda s: re.sub("[إأٱآ]", "ا", s)
    camel_normalize_mod.normalize_alef_maksura_ar = lambda s: s.replace("ى", "ي")
    camel_normalize_mod.normalize_teh_marbuta_ar = lambda s: s.replace("ة", "ه")
    sys.modules["camel_tools"] = camel_tools_mod
    sys.modules["camel_tools.utils"] = camel_utils_mod
    sys.modules["camel_tools.utils.charsets"] = camel_charsets_mod
    sys.modules["camel_tools.utils.normalize"] = camel_normalize_mod

    from gec.tag import rewrite
    return rewrite

def infer_pass(model, tokenizer, rewrite, words_batch):
    enc = tokenizer(
        words_batch,
        return_tensors="pt",
        is_split_into_words=True,
        padding=True,
    )
    with torch.no_grad():
        label_ids = model(**enc).logits.argmax(dim=-1)

    traces = []
    for i in range(len(words_batch)):
        valid_n = int(enc["attention_mask"][i].sum().item())
        core_ids = enc["input_ids"][i][1:valid_n - 1]
        core_labels = label_ids[i][1:valid_n - 1]
        if len(core_ids) != len(core_labels):
            raise RuntimeError("token/label length mismatch")
        subwords = tokenizer.convert_ids_to_tokens(core_ids.tolist())
        labels = [model.config.id2label[int(v)] for v in core_labels.tolist()]
        output = norm(rewrite([subwords], [labels])[0][0])
        traces.append({
            "subwords": subwords,
            "labels": labels,
            "output": output,
        })
    return traces

def single_runner(model, tokenizer, rewrite, words):
    current = list(words)
    trace = []
    for pass_index in (1, 2):
        step = infer_pass(model, tokenizer, rewrite, [current])[0]
        step["pass"] = pass_index
        trace.append(step)
        current = step["output"].split()
    return trace

def batch_runner(model, tokenizer, rewrite, rows, batch_size):
    pass1 = []
    for start in range(0, len(rows), batch_size):
        words_batch = [
            row["source"].split()
            for row in rows[start:start + batch_size]
        ]
        steps = infer_pass(model, tokenizer, rewrite, words_batch)
        for step in steps:
            step["pass"] = 1
        pass1.extend(steps)

    pass2 = []
    for start in range(0, len(rows), batch_size):
        words_batch = [
            step["output"].split()
            for step in pass1[start:start + batch_size]
        ]
        steps = infer_pass(model, tokenizer, rewrite, words_batch)
        for step in steps:
            step["pass"] = 2
        pass2.extend(steps)

    return list(zip(pass1, pass2))

def align_components(source: str, output: str):
    matcher = difflib.SequenceMatcher(a=source, b=output, autojunk=False)
    components = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        components.append({
            "op": tag.upper(),
            "source_start": i1,
            "source_end": i2,
            "output_start": j1,
            "output_end": j2,
            "source_text": source[i1:i2],
            "output_text": output[j1:j2],
        })
    return components

def touched_protected_ids(components, spans):
    touched = set()
    for comp in components:
        a = comp["source_start"]
        b = comp["source_end"]
        for span in spans:
            s = span["source_start"]
            e = span["source_end"]
            if a == b:
                hit = s < a < e
            else:
                hit = a < e and b > s
            if hit:
                touched.add(span["protected_id"])
    return sorted(touched)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--preflight-n", type=int, default=64)
    ap.add_argument("--out-prefix", default="MPSEF_P1_CF_PROPOSALS_V1")
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.source_manifest).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != EXPECTED_CASES:
        raise RuntimeError(f"source manifest count mismatch: {len(rows)}")
    if len({row["uid"] for row in rows}) != EXPECTED_CASES:
        raise RuntimeError("duplicate UID in source manifest")
    if len({row["cluster_id"] for row in rows}) != EXPECTED_CLUSTERS:
        raise RuntimeError("C_F cluster count mismatch")
    if any(row.get("role") != "C_F" for row in rows):
        raise RuntimeError("non-C_F row in source manifest")

    weight_path = Path(args.model_dir) / "pytorch_model.bin"
    weight_sha = sha256_file(weight_path)
    if weight_sha != EXPECTED_WEIGHT_SHA:
        raise RuntimeError(f"P1 weight SHA mismatch: {weight_sha}")

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(args.model_dir)
    model = BertForTokenClassification.from_pretrained(args.model_dir)
    model.eval()

    preflight = sorted(rows, key=lambda row: rank_uid(row["uid"]))[:args.preflight_n]
    batch_preflight = batch_runner(
        model, tokenizer, rewrite, preflight, args.batch_size
    )
    parity_match = 0
    for row, (batch_p1, batch_p2) in zip(preflight, batch_preflight):
        single = single_runner(
            model, tokenizer, rewrite, row["source"].split()
        )
        if single[0] == batch_p1 and single[1] == batch_p2:
            parity_match += 1

    if parity_match != len(preflight):
        raise RuntimeError(
            f"batch/single parity failed: {parity_match}/{len(preflight)}"
        )

    traces = batch_runner(model, tokenizer, rewrite, rows, args.batch_size)

    out_rows = []
    changed_count = 0
    protected_touch_count = 0
    empty_count = 0

    for index, (row, (pass1, pass2)) in enumerate(zip(rows, traces), start=1):
        source = row["source"]
        final_output = pass2["output"]
        components = align_components(source, final_output)
        touched = touched_protected_ids(
            components, row.get("protected_spans", [])
        )
        empty = final_output == ""

        if final_output != source:
            changed_count += 1
        if touched:
            protected_touch_count += 1
        if empty:
            empty_count += 1

        output_sha = sha_text(final_output)
        bundle_id = sha_text(
            "P1_FINAL\n"
            + row["uid"] + "\n"
            + row["source_sha256"] + "\n"
            + output_sha
        )

        out_rows.append({
            "record_id": "MPSEF_P1_CF_PROPOSAL_V1",
            "case_id": row["case_id"],
            "uid": row["uid"],
            "cluster_id": row["cluster_id"],
            "role": "C_F",
            "source_record_id": row["uid"],
            "source_version_hash": row["source_sha256"],
            "source": source,
            "proposer_id": "P1_SWEET_QALB14_NOPNX_ITER2",
            "proposal_type": "P1_FINAL",
            "full_proposer_output": final_output,
            "output_sha256": output_sha,
            "bundle_id": bundle_id,
            "whole_hypothesis_inseparable": True,
            "primary_action_whole_hypothesis": True,
            "diagnostic_components_only": components,
            "source_to_output_alignment_status": "DETERMINISTIC_SEQUENCE_MATCHER_V1",
            "pass1_output": pass1["output"],
            "pass1_trace": pass1,
            "pass2_trace": pass2,
            "pass2_depends_on_pass1": True,
            "protected_spans": row.get("protected_spans", []),
            "protected_touch": bool(touched),
            "protected_ids_touched": touched,
            "source_only_executable_precheck": not touched and not empty,
            "source_only_failure_reason": (
                "EMPTY_OUTPUT" if empty
                else "PROTECTED_BLOCKED_PRECHECK" if touched
                else None
            ),
            "runtime": {
                "model_revision": EXPECTED_MODEL_REV,
                "model_weight_sha256": weight_sha,
                "upstream_text_editing_revision": EXPECTED_UPSTREAM_REV,
                "decode_iter": 2,
                "batch_size": args.batch_size,
            },
            "gold_reference_consulted": False,
            "feasibility_scored": False,
        })

        if index == 1 or index % 128 == 0 or index == len(rows):
            print(
                f"P1_CF_PROGRESS {index}/{len(rows)}",
                flush=True,
            )

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": "MPSEF_P1_CF_PROPOSALS_V1",
        "status": "PREMEASUREMENT_PROPOSALS_READY",
        "cases": len(out_rows),
        "clusters": len({row["cluster_id"] for row in out_rows}),
        "proposal_type": "P1_FINAL_WHOLE_HYPOTHESIS",
        "decode_iter": 2,
        "batch_size": args.batch_size,
        "batch_single_parity_n": len(preflight),
        "batch_single_parity_match": parity_match,
        "model_revision": EXPECTED_MODEL_REV,
        "weight_sha256": weight_sha,
        "upstream_revision": EXPECTED_UPSTREAM_REV,
        "changed_source_only_count": changed_count,
        "protected_touch_source_only_count": protected_touch_count,
        "empty_output_count": empty_count,
        "proposal_artifact_sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
        "gold_reference_consulted": False,
        "reference_content_used": False,
        "feasibility_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
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
