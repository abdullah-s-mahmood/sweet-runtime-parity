#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_SOURCE_MANIFEST_SHA256 = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_GED_REV = "447179dc63d186e4bff09a993e90e73ad622d571"
EXPECTED_GEC_REV = "410588a318d988cdcfdbf64cf5745ed4adea0f6a"
EXPECTED_GED_WEIGHT_SHA = "23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f"
EXPECTED_GEC_WEIGHT_SHA = "5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f"
EXPECTED_UPSTREAM_REV = "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
PARITY_SALT = "MPSEF-P2-CF-BATCH-PREFLIGHT-V1-20260930"

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

def morph_text(disambig, text: str) -> str:
    dis = disambig.disambiguate(text.split())
    out = []
    for item in dis:
        if not item.analyses:
            raise RuntimeError("No morphological analysis returned")
        out.append(dediac_ar(item.analyses[0].analysis["diac"]))
    return " ".join(out)

def ged_single(ged_tokenizer, ged_model, text: str):
    enc = ged_tokenizer([text], return_tensors="pt")
    with torch.no_grad():
        logits = ged_model(**enc).logits
    preds = F.softmax(logits, dim=-1).squeeze()[1:-1]
    return [
        ged_model.config.id2label[p.item()]
        for p in torch.argmax(preds, -1)
    ]

def make_gec_inputs(gec_tokenizer, gec_model, morph: str, ged_labels):
    ged_label2ids = gec_model.config.ged_label2id
    tokens = []
    expanded = []
    for word, label in zip(morph.split(), ged_labels):
        pieces = gec_tokenizer.tokenize(word)
        if pieces:
            tokens.extend(pieces)
            expanded.extend([label] * len(pieces))

    input_ids = [
        gec_tokenizer.bos_token_id,
        *gec_tokenizer.convert_tokens_to_ids(tokens),
        gec_tokenizer.eos_token_id,
    ]
    label_ids = [
        ged_label2ids["UC"],
        *[ged_label2ids.get(label, ged_label2ids["<pad>"]) for label in expanded],
        ged_label2ids["UC"],
    ]
    return tokens, input_ids, label_ids

def generate_single(gec_tokenizer, gec_model, input_ids, label_ids):
    attention_mask = [1] * len(input_ids)
    with torch.no_grad():
        generated = gec_model.generate(
            torch.tensor([input_ids]),
            num_beams=5,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=0,
            early_stopping=False,
            ged_tags=torch.tensor([label_ids]),
            attention_mask=torch.tensor([attention_mask]),
        )
    return gec_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

def single_runner(disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model, source: str):
    morph = morph_text(disambig, source)
    labels = ged_single(ged_tokenizer, ged_model, morph)
    tokens, input_ids, label_ids = make_gec_inputs(
        gec_tokenizer, gec_model, morph, labels
    )
    generated = generate_single(
        gec_tokenizer, gec_model, input_ids, label_ids
    )
    return {
        "morph_text": morph,
        "ged_labels": labels,
        "tokens": tokens,
        "input_ids": input_ids,
        "label_ids": label_ids,
        "generated_text": generated,
    }

def ged_batch(ged_tokenizer, ged_model, morphs):
    enc = ged_tokenizer(morphs, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = ged_model(**enc).logits
    out = []
    for i in range(len(morphs)):
        valid_n = int(enc["attention_mask"][i].sum().item())
        core = logits[i][1:valid_n - 1]
        ids = core.argmax(dim=-1).tolist()
        out.append([ged_model.config.id2label[int(v)] for v in ids])
    return out

def generate_batch(gec_tokenizer, gec_model, prepared):
    pad_id = gec_tokenizer.pad_token_id
    ged_pad_id = gec_model.config.ged_label2id["<pad>"]
    max_len = max(len(x["input_ids"]) for x in prepared)
    ids_batch = []
    labels_batch = []
    masks = []
    for item in prepared:
        n = len(item["input_ids"])
        pad_n = max_len - n
        ids_batch.append(item["input_ids"] + [pad_id] * pad_n)
        labels_batch.append(item["label_ids"] + [ged_pad_id] * pad_n)
        masks.append([1] * n + [0] * pad_n)

    with torch.no_grad():
        generated = gec_model.generate(
            torch.tensor(ids_batch),
            num_beams=5,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=0,
            early_stopping=False,
            ged_tags=torch.tensor(labels_batch),
            attention_mask=torch.tensor(masks),
        )
    return gec_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

def batch_runner(disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model, rows, batch_size):
    outputs = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start:start + batch_size]
        morphs = [morph_text(disambig, row["source"]) for row in chunk]
        labels_batch = ged_batch(ged_tokenizer, ged_model, morphs)

        prepared = []
        for morph, labels in zip(morphs, labels_batch):
            tokens, input_ids, label_ids = make_gec_inputs(
                gec_tokenizer, gec_model, morph, labels
            )
            prepared.append({
                "morph_text": morph,
                "ged_labels": labels,
                "tokens": tokens,
                "input_ids": input_ids,
                "label_ids": label_ids,
            })

        generated = generate_batch(gec_tokenizer, gec_model, prepared)
        for item, text in zip(prepared, generated):
            item["generated_text"] = text
            outputs.append(item)

        print(
            f"P2_CF_BATCH_PROGRESS {min(start + len(chunk), len(rows))}/{len(rows)}",
            flush=True,
        )
    return outputs

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
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--preflight-n", type=int, default=32)
    ap.add_argument("--out-prefix", default="MPSEF_P2_CF_PROPOSALS_V1")
    args = ap.parse_args()

    source_path = Path(args.source_manifest)
    observed_manifest_sha = sha256_file(source_path)
    if observed_manifest_sha != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise RuntimeError(
            f"source manifest SHA mismatch: {observed_manifest_sha}"
        )

    rows = [
        json.loads(line)
        for line in source_path.read_text(encoding="utf-8").splitlines()
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

    ged_weight_sha = sha256_file(Path(args.ged_model_dir) / "pytorch_model.bin")
    gec_weight_sha = sha256_file(Path(args.gec_model_dir) / "pytorch_model.bin")
    if ged_weight_sha != EXPECTED_GED_WEIGHT_SHA:
        raise RuntimeError(f"GED weight SHA mismatch: {ged_weight_sha}")
    if gec_weight_sha != EXPECTED_GEC_WEIGHT_SHA:
        raise RuntimeError(f"GEC weight SHA mismatch: {gec_weight_sha}")

    disambig = BERTUnfactoredDisambiguator.pretrained(
        model_name="msa",
        use_gpu=False,
        pretrained_cache=False,
    )
    ged_tokenizer = AutoTokenizer.from_pretrained(args.ged_model_dir)
    ged_model = BertForTokenClassification.from_pretrained(args.ged_model_dir)
    ged_model.eval()
    gec_tokenizer = AutoTokenizer.from_pretrained(args.gec_model_dir)
    gec_model = MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    gec_model.eval()

    preflight = sorted(rows, key=lambda row: rank_uid(row["uid"]))[:args.preflight_n]
    batch_pf = batch_runner(
        disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model,
        preflight, args.batch_size
    )
    parity = 0
    parity_fields = {
        "morph_text": 0,
        "ged_labels": 0,
        "tokens": 0,
        "input_ids": 0,
        "label_ids": 0,
        "generated_text": 0,
    }
    for row, batched in zip(preflight, batch_pf):
        single = single_runner(
            disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model,
            row["source"]
        )
        checks = {key: single[key] == batched[key] for key in parity_fields}
        for key, ok in checks.items():
            parity_fields[key] += int(ok)
        parity += int(all(checks.values()))

    if parity != len(preflight):
        raise RuntimeError(
            f"P2 batch/single parity failed: {parity}/{len(preflight)} "
            f"fields={parity_fields}"
        )

    proposals = batch_runner(
        disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model,
        rows, args.batch_size
    )

    out_rows = []
    changed_count = 0
    protected_touch_count = 0
    empty_count = 0

    for index, (row, proposal) in enumerate(zip(rows, proposals), start=1):
        source = row["source"]
        final_output = proposal["generated_text"]
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
            "P2_FINAL\n"
            + row["uid"] + "\n"
            + row["source_sha256"] + "\n"
            + output_sha
        )

        out_rows.append({
            "record_id": "MPSEF_P2_CF_PROPOSAL_V1",
            "case_id": row["case_id"],
            "uid": row["uid"],
            "cluster_id": row["cluster_id"],
            "role": "C_F",
            "source_record_id": row["uid"],
            "source_version_hash": row["source_sha256"],
            "source": source,
            "proposer_id": "P2_ARABART_QALB14_GEC_GED13",
            "proposal_type": "P2_FINAL",
            "full_proposer_output": final_output,
            "output_sha256": output_sha,
            "bundle_id": bundle_id,
            "whole_hypothesis_inseparable": True,
            "primary_action_whole_hypothesis": True,
            "diagnostic_components_only": components,
            "source_to_output_alignment_status": "DETERMINISTIC_SEQUENCE_MATCHER_V1",
            "morph_preprocessed_text": proposal["morph_text"],
            "ged_labels": proposal["ged_labels"],
            "gec_subword_tokens": proposal["tokens"],
            "gec_input_ids": proposal["input_ids"],
            "gec_ged_label_ids": proposal["label_ids"],
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
                "ged_revision": EXPECTED_GED_REV,
                "gec_revision": EXPECTED_GEC_REV,
                "ged_weight_sha256": ged_weight_sha,
                "gec_weight_sha256": gec_weight_sha,
                "upstream_arabic_gec_revision": EXPECTED_UPSTREAM_REV,
                "num_beams": 5,
                "max_length": 100,
                "num_return_sequences": 1,
                "no_repeat_ngram_size": 0,
                "early_stopping": False,
                "batch_size": args.batch_size,
            },
            "gold_reference_consulted": False,
            "feasibility_scored": False,
        })

        if index == 1 or index % 128 == 0 or index == len(rows):
            print(f"P2_CF_RECORD_PROGRESS {index}/{len(rows)}", flush=True)

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": "MPSEF_P2_CF_PROPOSALS_V1",
        "status": "PREMEASUREMENT_PROPOSALS_READY",
        "cases": len(out_rows),
        "clusters": len({row["cluster_id"] for row in out_rows}),
        "proposal_type": "P2_FINAL_WHOLE_HYPOTHESIS",
        "source_manifest_sha256": observed_manifest_sha,
        "batch_size": args.batch_size,
        "batch_single_parity_n": len(preflight),
        "batch_single_all_field_match": parity,
        "batch_single_field_matches": parity_fields,
        "ged_revision": EXPECTED_GED_REV,
        "gec_revision": EXPECTED_GEC_REV,
        "ged_weight_sha256": ged_weight_sha,
        "gec_weight_sha256": gec_weight_sha,
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
