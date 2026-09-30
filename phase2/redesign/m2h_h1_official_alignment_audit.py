#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import string
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

PARITY_SALT = "M2H-H1-PUBLIC-PARITY-V1-20260930-A"
EXPECTED_CASES = 6888
EXPECTED_UID_SHA256 = "3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9"

def norm(s):
    return " ".join((s or "").strip().split())

def uid_digest(uids):
    return hashlib.sha256(("\\n".join(uids) + "\\n").encode("utf-8")).hexdigest()

def sha_rank(uid):
    return hashlib.sha256((PARITY_SALT + "|" + uid).encode("utf-8")).hexdigest()

UNICODE_PUNCT_SYMBOL = frozenset(
    chr(i) for i in range(0x110000)
    if unicodedata.category(chr(i))[0] in {"P", "S"}
)
PNX_SET = frozenset(string.punctuation) | UNICODE_PUNCT_SYMBOL | frozenset("&amp;")

def grouped_ops(edit):
    return re.findall(r'I_\\[.*?\\]+|R_\\[.*?\\]+|A_\\[.*?\\]+|D+|K+|.', edit)

def reconstruct_edit(pnx_edit, no_pnx_edit):
    def parse_edits(s):
        return re.findall(r'I_\\[.*?\\]+|R_\\[.*?\\]+|A_\\[.*?\\]+|D|K|.', s)
    def is_insert_or_append(e):
        return e.startswith("I") or e.startswith("A")
    def is_replace(e):
        return e.startswith("R")
    p = parse_edits(pnx_edit)
    n = parse_edits(no_pnx_edit)
    pc = Counter(p)
    nc = Counter(e for e in n if not is_insert_or_append(e))
    i = j = 0
    out = ""
    while i < len(p) and j < len(n):
        pe, ne = p[i], n[j]
        if pe == "K" and (ne in ["K", "D", "M"] or is_replace(ne)):
            out += ne; pc[pe] -= 1; nc[ne] -= 1; i += 1; j += 1
        elif is_replace(pe) and ne == "K":
            out += pe; pc[pe] -= 1; nc[ne] -= 1; i += 1; j += 1
        elif is_insert_or_append(pe):
            if pc["K"] != 0 and sum(nc.values()) == pc["K"]:
                out += pe; i += 1
            else:
                out += ne; j += 1
        else:
            out += ne; j += 1
    out += "".join(n[j:])
    out += "".join(p[i:])
    return out

def separate_pnx_edit(edit):
    ops = grouped_ops(edit)
    pnx_edit = ""
    no_pnx_edit = ""
    found_pnx = False
    for g in ops:
        if g.startswith("A_[") or g.startswith("I_[") or g.startswith("R_["):
            op = g[0]
            seq = re.sub(op + r'_\\[(.*?)\\]', r'\\1', g)
            seq = re.sub(" +", "", seq)
            is_pnx = bool(seq) and all(ch in PNX_SET for ch in seq)
            if is_pnx:
                pnx_edit += g
                found_pnx = True
                if op == "R":
                    no_pnx_edit += "K"
            else:
                no_pnx_edit += g
                if g.startswith("R_["):
                    pnx_edit += "K"
        elif g:
            no_pnx_edit += g
            if not (g.startswith("I") and g.startswith("M") and g.startswith("A")):
                pnx_edit += "K" * len(g)
    if not found_pnx:
        pnx_edit = ""
    pnx_final = pnx_edit if pnx_edit else "K"
    recon = reconstruct_edit(pnx_final, no_pnx_edit)
    if recon != edit:
        raise RuntimeError(f"PNX reconstruction mismatch: {edit} != {recon}")
    return {"no_pnx_edit": no_pnx_edit, "pnx_edit": pnx_final}

def compress_appends(subword_edit):
    edits = re.findall(r'I_\\[.*?\\]+|A_\\[.*?\\]+|R_\\[.*?\\]+|K\\*|.', subword_edit)
    compressed = []
    buf = []
    for edit in edits:
        if edit.startswith("A_"):
            buf.append(re.sub(r'A_\\[(.*?)\\]', r'\\1', edit))
        else:
            if buf:
                compressed.append(f"A_[{' '.join(buf)}]")
                buf = []
            compressed.append(edit)
    if buf:
        compressed.append(f"A_[{' '.join(buf)}]")
    return "".join(compressed)

def insert_to_append(edits, SubwordEdit):
    processed_edits = []
    start_inserts = []
    subwords = [e.subword for e in edits]
    raw_subwords = [e.raw_subword for e in edits]
    for edit in edits:
        edit_parts = re.findall(r'I_\\[.*?\\]+|R_\\[.*?\\]+|K\\*|.', edit.edit)
        all_inserts = all(e.startswith("I_[") for e in edit_parts)
        if all_inserts:
            if edit.subword != "":
                raise RuntimeError("Expected empty subword for insertion-only edit")
            append_edit = "".join(re.sub(r"^I", "A", e) for e in edit_parts)
            if processed_edits:
                processed_edits[-1] = compress_appends(processed_edits[-1] + append_edit)
            else:
                start_inserts.append(append_edit)
        else:
            if start_inserts:
                processed_edits.append(compress_appends("".join(start_inserts) + "".join(edit_parts)))
                start_inserts = []
            else:
                processed_edits.append("".join(edit_parts))
    subwords = [x for x in subwords if x != ""]
    raw_subwords = [x for x in raw_subwords if x != ""]
    if not processed_edits:
        return []
    if not (len(processed_edits) == len(subwords) == len(raw_subwords)):
        raise RuntimeError("insert_to_append length mismatch")
    if processed_edits[0].startswith("A") and re.sub(r'A_\\[.*?\\]', '', processed_edits[0]) == "K":
        processed_edits[0] = processed_edits[0].replace(
            "K", "K" * len(subwords[0].replace("##", ""))
        )
    return [SubwordEdit(s, r, e) for s, r, e in zip(subwords, raw_subwords, processed_edits)]

def apply_edits(tokenized_text, edits):
    if len(tokenized_text) != len(edits):
        raise RuntimeError("apply_edits length mismatch")
    rewritten = []
    for subword, edit in zip(tokenized_text, edits):
        rewritten_subword = edit.apply(subword)
        edit_ops = re.findall(r'I_\\[.*?\\]+|R_\\[.*?\\]+|A_\\[.*?\\]+|D+|K+|.', edit.edit)
        if "M" in edit_ops:
            if not rewritten:
                raise RuntimeError("Merge at start")
            rewritten[-1] = rewritten[-1] + rewritten_subword
        else:
            rewritten.append(rewritten_subword)
    collapsed = []
    for subword in rewritten:
        if subword.startswith("##"):
            if not collapsed:
                raise RuntimeError("Continuation at start")
            collapsed[-1] = collapsed[-1] + subword.replace("##", "")
        else:
            collapsed.append(subword)
    return [x.strip() for x in collapsed if x != ""]

def create_official_subword_edits(source, target, tokenizer, word_level_alignment,
                                  char_level_alignment, Edit, SubwordEdits, SubwordEdit):
    wa = word_level_alignment(src_sent=source, tgt_sent=target)
    ca = char_level_alignment(wa)
    aligned_src_words = wa["src"]
    aligned_tgt_words = wa["tgt"]
    aligned_src_chars = ca["src"]
    aligned_tgt_chars = ca["tgt"]
    if not (len(aligned_src_words) == len(aligned_tgt_words) ==
            len(aligned_src_chars) == len(aligned_tgt_chars)):
        raise RuntimeError("Official alignment length mismatch")
    subword_edits = []
    for src_chars, tgt_chars, src_words, _ in zip(
        aligned_src_chars, aligned_tgt_chars, aligned_src_words, aligned_tgt_words
    ):
        word_edit = Edit.create(src_chars, tgt_chars)
        sw = SubwordEdits.create(src_words, word_edit.edit, tokenizer)
        subword_edits.extend(sw.edits)
    return insert_to_append(subword_edits, SubwordEdit)

def parse_m2_summary(path):
    vals = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            vals[k.strip()] = float(v.strip())
    return vals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--h1-inference", required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--out-prefix", default="M2H_H1_OFFICIAL_ALIGNMENT_AUDIT_V1")
    args = ap.parse_args()

    rows = [json.loads(x) for x in Path(args.calibration).read_text(encoding="utf-8").splitlines() if x.strip()]
    inf = [json.loads(x) for x in Path(args.h1_inference).read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows) != EXPECTED_CASES or len(inf) != EXPECTED_CASES:
        raise SystemExit("Case count mismatch")
    if uid_digest([r["uid"] for r in rows]) != EXPECTED_UID_SHA256:
        raise SystemExit("CALIBRATION UID mismatch")
    if [r["case_id"] for r in rows] != [r["case_id"] for r in inf]:
        raise SystemExit("Inference ordering mismatch")

    upstream = Path(args.upstream_root).resolve()
    sys.path.insert(0, str(upstream))
    sys.path.insert(0, str(upstream / "edits"))

    import types
    camel_tools_mod = types.ModuleType("camel_tools")
    camel_utils_mod = types.ModuleType("camel_tools.utils")
    camel_charsets_mod = types.ModuleType("camel_tools.utils.charsets")
    camel_normalize_mod = types.ModuleType("camel_tools.utils.normalize")
    camel_charsets_mod.UNICODE_PUNCT_SYMBOL_CHARSET = UNICODE_PUNCT_SYMBOL
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

    from edits.tokenizer import Tokenizer
    from edits.alignment.aligner import word_level_alignment, char_level_alignment
    from edits.edit import Edit, SubwordEdits, SubwordEdit

    import torch
    import torch.nn.functional as F
    from transformers import BertTokenizer, BertForTokenClassification
    from gec.tag import rewrite as official_rewrite

    tok = BertTokenizer.from_pretrained(args.model_dir)
    model = BertForTokenClassification.from_pretrained(args.model_dir)
    model.eval()

    sample_idx = sorted(range(len(rows)), key=lambda i: sha_rank(rows[i]["uid"]))[:256]
    parity = Counter()
    mismatches = []
    with torch.no_grad():
        for i in sample_idx:
            text_words = rows[i]["source"].split()
            enc = tok(text_words, return_tensors="pt", is_split_into_words=True)
            logits = model(**enc).logits
            preds = F.softmax(logits.squeeze(0), dim=-1)
            pred_ids = torch.argmax(preds, dim=-1).cpu().numpy()
            labels = [model.config.id2label[int(p)] for p in pred_ids[1:-1]]
            subwords = tok.convert_ids_to_tokens(enc["input_ids"][0][1:-1])
            rewrite = norm(official_rewrite(subwords=[subwords], edits=[labels])[0][0])
            frozen = inf[i]
            ok_s = subwords == frozen["subwords"]
            ok_l = labels == frozen["top1_labels"]
            ok_r = rewrite == norm(frozen["h1_rewrite"])
            parity["subwords_match"] += int(ok_s)
            parity["labels_match"] += int(ok_l)
            parity["rewrite_match"] += int(ok_r)
            parity["all_match"] += int(ok_s and ok_l and ok_r)
            if not (ok_s and ok_l and ok_r):
                mismatches.append({
                    "case_id": rows[i]["case_id"], "uid": rows[i]["uid"],
                    "subwords_match": ok_s, "labels_match": ok_l, "rewrite_match": ok_r,
                })

    ext_tok = Tokenizer(args.model_dir)
    nopnx_refs = []
    failures = []
    pnx_changed = 0
    full_reconstruction_fail = 0

    for rec in rows:
        src, ref = norm(rec["source"]), norm(rec["reference"])
        try:
            edits = create_official_subword_edits(
                src, ref, ext_tok, word_level_alignment, char_level_alignment,
                Edit, SubwordEdits, SubwordEdit
            )
            raw_src, _ = ext_tok.tokenize(src, flatten=True)
            full = norm(" ".join(apply_edits(raw_src, edits)))
            if full != ref:
                full_reconstruction_fail += 1
                raise RuntimeError(f"Full reconstruction mismatch: {full} != {ref}")
            nopnx_edits = []
            for e in edits:
                sep = separate_pnx_edit(e.edit)
                nopnx_edits.append(SubwordEdit(e.subword, e.raw_subword, sep["no_pnx_edit"]))
            nopnx = norm(" ".join(apply_edits(raw_src, nopnx_edits)))
            nopnx_refs.append(nopnx)
            pnx_changed += int(nopnx != ref)
        except Exception as exc:
            failures.append({
                "case_id": rec["case_id"], "uid": rec["uid"],
                "error_type": type(exc).__name__, "error": str(exc)[:500],
            })
            nopnx_refs.append(None)

    if failures:
        summary = {
            "status": "FAIL_GOLD_CONSTRUCTION",
            "cases": len(rows),
            "parity_sample": 256,
            "parity": dict(parity),
            "parity_mismatches": len(mismatches),
            "gold_construction_failures": len(failures),
            "full_reconstruction_failures": full_reconstruction_fail,
            "integrity": {
                "internal_evaluation_opened": False,
                "stress_diagnostic_opened": False,
            },
        }
        Path(args.out_prefix + "_SUMMARY.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8"
        )
        Path(args.out_prefix + "_FAILURES.jsonl").write_text(
            "\\n".join(json.dumps(x, ensure_ascii=False) for x in failures) + "\\n", encoding="utf-8"
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    source_file = Path(args.out_prefix + "_SOURCE.txt")
    gold_target_file = Path(args.out_prefix + "_NOPNX_REFERENCE.txt")
    system_file = Path(args.out_prefix + "_H1_SYSTEM.txt")
    source_file.write_text("\\n".join(norm(r["source"]) for r in rows) + "\\n", encoding="utf-8")
    gold_target_file.write_text("\\n".join(nopnx_refs) + "\\n", encoding="utf-8")
    system_file.write_text("\\n".join(norm(x["h1_rewrite"]) for x in inf) + "\\n", encoding="utf-8")

    m2dir = upstream / "gec" / "utils" / "m2scorer"
    gold_m2 = Path.cwd() / (args.out_prefix + "_NOPNX_GOLD.m2")
    subprocess.run(
        [
            sys.executable, str(m2dir / "edit_creator.py"),
            "--max_unchanged_words", "2",
            "--output", str(gold_m2),
            str(source_file.resolve()), str(gold_target_file.resolve())
        ],
        cwd=str(m2dir), check=True
    )

    run_m2 = upstream / "gec" / "utils" / "run_m2scorer.py"
    subprocess.run(
        [
            sys.executable, str(run_m2),
            "--system_output", str(system_file.resolve()),
            "--m2_file", str(gold_m2.resolve()),
        ],
        check=True
    )
    m2 = parse_m2_summary(str(system_file) + ".m2")

    exact_sentence = sum(norm(x["h1_rewrite"]) == g for x, g in zip(inf, nopnx_refs))
    source_copy = sum(norm(x["h1_rewrite"]) == norm(r["source"]) for x, r in zip(inf, rows))
    gold_edit_lines = sum(
        1 for line in gold_m2.read_text(encoding="utf-8").splitlines()
        if line.startswith("A ")
    )

    summary = {
        "record_id": "M2H_H1_OFFICIAL_ALIGNMENT_AUDIT_V1",
        "status": "PASS",
        "scope": "CALIBRATION_ONLY",
        "cases": len(rows),
        "public_model_card_parity": {
            "sample_n": 256,
            **dict(parity),
            "mismatches": len(mismatches),
            "required_all_match": 256,
            "passed": parity["all_match"] == 256,
        },
        "official_nopnx_gold": {
            "construction_failures": 0,
            "full_reconstruction_failures": 0,
            "cases_where_nopnx_differs_from_full_reference": pnx_changed,
            "derived_gold_m2_edit_lines": gold_edit_lines,
        },
        "official_alignment_m2": {
            "precision": m2.get("Precision"),
            "recall": m2.get("Recall"),
            "f1": m2.get("F_1.0"),
            "f0_5": m2.get("F_0.5"),
            "frozen_h1_recall_gate": 0.80,
            "recall_gate_passed": (m2.get("Recall") is not None and m2["Recall"] >= 0.80),
        },
        "secondary": {
            "exact_nopnx_reference_sentences": exact_sentence,
            "exact_nopnx_reference_sentence_rate": exact_sentence / len(rows),
            "source_copy_sentences": source_copy,
            "source_copy_rate": source_copy / len(rows),
        },
        "sanity_reference_not_comparable": {
            "official_qalb14_dev_one_pass_nopnx_precision": 0.8825,
            "official_qalb14_dev_one_pass_nopnx_recall": 0.7766,
        },
        "integrity": {
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "reserved_nahw_opened": False,
            "qalb15_test_opened": False,
        },
    }

    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8"
    )
    Path(args.out_prefix + "_PARITY_MISMATCHES.jsonl").write_text(
        "\\n".join(json.dumps(x, ensure_ascii=False) for x in mismatches) + ("\\n" if mismatches else ""),
        encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
