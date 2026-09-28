"""Phase 2 development-only source-preserving SWEET renderer.

Goal:
- preserve the exact source surface for every untouched region;
- apply only model-supported non-K subword edits;
- suppress edits on tokenizer-unknown words, protected scientific spans,
  unsafe merge edits, or words whose model tokens cannot be mapped exactly
  back to the source surface.

This is a bounded DEVELOPMENT prototype, not a production renderer and not a
sealed evaluation. It does not modify SWEET weights, labels, or the frozen
safety stack.
"""
from __future__ import annotations

import collections
import difflib
import hashlib
import json
import platform
import random
import re
import subprocess
import sys
from pathlib import Path

import torch
from transformers import BertForTokenClassification, BertTokenizer
import transformers

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ART = ROOT / "artifacts"
UPSTREAM = ROOT / "upstream" / "text-editing"

PINS = {
    "nopnx": "584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6",
    "pnx": "195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3",
}

DEV = HERE / "DEVELOPMENT_TARGETS.jsonl"
SCI = HERE / "SCIENTIFIC_STRESS_CASES.jsonl"
SCI_CORR = HERE / "SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_model(kind: str):
    folder = ROOT / "models" / kind
    weight = folder / "pytorch_model.bin"
    actual = sha256(weight)
    if actual != PINS[kind]:
        raise RuntimeError(f"{kind} hash mismatch: {actual}")
    tok = BertTokenizer.from_pretrained(str(folder), local_files_only=True)
    model = BertForTokenClassification.from_pretrained(str(folder), local_files_only=True)
    model.eval().cpu()
    return tok, model


def protected_ranges(text: str, protected: list[str]) -> list[tuple[int, int, str]]:
    out = []
    for p in protected:
        starts = [m.start() for m in re.finditer(re.escape(p), text)]
        if len(starts) != 1:
            raise ValueError(f"protected span must occur once: {p!r}; found {len(starts)} in {text!r}")
        a = starts[0]
        out.append((a, a + len(p), p))
    out.sort()
    return out


def overlaps(a: int, b: int, ranges: list[tuple[int, int, str]]) -> bool:
    return any(a < rb and b > ra for ra, rb, _ in ranges)


def apply_one_stage(text: str, tok, model, protected: list[str] | None = None) -> tuple[str, dict]:
    """Run model once but patch only supported edits onto the exact source string."""
    protected = protected or []
    locks = protected_ranges(text, protected) if protected else []

    words = [m.group(0) for m in re.finditer(r"\S+", text)]
    word_spans = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    if not words:
        return text, {"changed": False, "applied_edits": [], "suppressed": []}

    enc = tok(words, return_tensors="pt", is_split_into_words=True)
    with torch.no_grad():
        logits = model(**enc).logits[0]
        probs = torch.softmax(logits, dim=-1)
        conf, ids_pred = probs.max(dim=-1)

    ids = enc["input_ids"][0].tolist()[1:-1]
    subwords = tok.convert_ids_to_tokens(ids)
    labels = [model.config.id2label[int(x)] for x in ids_pred.tolist()[1:-1]]
    confs = [float(x) for x in conf.tolist()[1:-1]]

    manual_subwords = []
    word_for_subword = []
    for wi, word in enumerate(words):
        pieces = tok.tokenize(word)
        manual_subwords.extend(pieces)
        word_for_subword.extend([wi] * len(pieces))

    if manual_subwords != subwords:
        raise RuntimeError(
            "Per-word tokenization did not reproduce model tokenization; "
            "source-preserving projection is unsafe for this passage."
        )

    if len(labels) != len(subwords):
        raise RuntimeError("label/subword length mismatch")

    sys.path.insert(0, str(UPSTREAM))
    from edits.edit import SubwordEdit

    by_word = collections.defaultdict(list)
    for si, (wi, sw, label, cf) in enumerate(zip(word_for_subword, subwords, labels, confs)):
        by_word[wi].append((si, sw, label, cf))

    word_replacements = {}
    applied = []
    suppressed = []

    for wi, entries in by_word.items():
        wa, wb = word_spans[wi]
        original_word = text[wa:wb]
        non_keep = [(si, sw, lab, cf) for si, sw, lab, cf in entries if lab != "K*"]
        if not non_keep:
            continue

        if overlaps(wa, wb, locks):
            suppressed.append({
                "word_index": wi,
                "word": original_word,
                "reason": "PROTECTED_SPAN_LOCK",
                "labels": [x[2] for x in non_keep],
            })
            continue

        if any(sw == tok.unk_token for _, sw, _, _ in entries):
            suppressed.append({
                "word_index": wi,
                "word": original_word,
                "reason": "TOKENIZER_UNK_WORD",
                "labels": [x[2] for x in non_keep],
            })
            continue

        # Conservative initial renderer: merge-bearing edits can affect boundaries
        # outside one mapped token, so abstain instead of guessing.
        if any("M" in lab for _, _, lab, _ in non_keep):
            suppressed.append({
                "word_index": wi,
                "word": original_word,
                "reason": "UNSAFE_MERGE_EDIT",
                "labels": [x[2] for x in non_keep],
            })
            continue

        # Greedily map tokenizer pieces to exact source substrings inside this
        # whitespace-delimited word. If normalization prevents an exact mapping,
        # preserve the source word.
        token_ranges = []
        cursor = 0
        mapping_failed = False
        for _, sw, _, _ in entries:
            surface = sw[2:] if sw.startswith("##") else sw
            pos = original_word.find(surface, cursor)
            if pos < 0:
                mapping_failed = True
                break
            token_ranges.append((pos, pos + len(surface), surface))
            cursor = pos + len(surface)

        if mapping_failed or len(token_ranges) != len(entries):
            suppressed.append({
                "word_index": wi,
                "word": original_word,
                "reason": "SOURCE_MAPPING_UNSAFE",
                "labels": [x[2] for x in non_keep],
                "subwords": [x[1] for x in entries],
            })
            continue

        replacements = []
        word_hazard = None
        for (si, sw, lab, cf), (a, b, surface) in zip(entries, token_ranges):
            if lab == "K*":
                continue
            # Require source token surface to equal the model token surface exactly.
            # This prevents accidental normalization of diacritics/case/etc.
            if original_word[a:b] != surface:
                word_hazard = "TOKEN_SURFACE_MISMATCH"
                break
            try:
                edit = SubwordEdit(subword=sw, raw_subword=sw, edit=lab)
                if not edit.is_applicable(sw):
                    word_hazard = "EDIT_NOT_APPLICABLE"
                    break
                repl = edit.apply(sw)
            except Exception as exc:
                word_hazard = f"EDIT_EXCEPTION:{type(exc).__name__}"
                break
            if repl.startswith("##"):
                repl = repl[2:]
            if "[UNK]" in repl:
                word_hazard = "POST_EDIT_UNK"
                break
            replacements.append((a, b, repl, si, sw, lab, cf))

        if word_hazard:
            suppressed.append({
                "word_index": wi,
                "word": original_word,
                "reason": word_hazard,
                "labels": [x[2] for x in non_keep],
            })
            continue

        new_word = original_word
        for a, b, repl, si, sw, lab, cf in sorted(replacements, reverse=True):
            new_word = new_word[:a] + repl + new_word[b:]
            applied.append({
                "word_index": wi,
                "source_word": original_word,
                "subword_index": si,
                "subword": sw,
                "label": lab,
                "top1_confidence": cf,
                "source_local_span": [a, b],
                "source_text": original_word[a:b],
                "replacement": repl,
            })

        if new_word != original_word:
            word_replacements[wi] = new_word

    output = text
    # Whole-word patches are applied right-to-left, preserving every source byte
    # outside words with a safely projected model-supported edit.
    for wi in sorted(word_replacements, reverse=True):
        a, b = word_spans[wi]
        output = output[:a] + word_replacements[wi] + output[b:]

    return output, {
        "changed": output != text,
        "applied_edit_count": len(applied),
        "suppressed_count": len(suppressed),
        "applied_edits": applied,
        "suppressed": suppressed,
        "raw_non_keep_label_count": sum(lab != "K*" for lab in labels),
    }


def run_variant(source: str, models, variant: str, protected: list[str] | None = None):
    protected = protected or []
    trace = []
    text = source
    if variant in {"nopnx1", "nopnx2", "full"}:
        text, meta = apply_one_stage(text, *models["nopnx"], protected=protected)
        trace.append({"stage": "nopnx1", **meta, "output": text})
    if variant in {"nopnx2", "full"}:
        text, meta = apply_one_stage(text, *models["nopnx"], protected=protected)
        trace.append({"stage": "nopnx2", **meta, "output": text})
    if variant == "full":
        text, meta = apply_one_stage(text, *models["pnx"], protected=protected)
        trace.append({"stage": "pnx", **meta, "output": text})
    return text, trace


def equal_coverage(ref: str, out: str, a: int, b: int) -> int:
    if a == b:
        return 0
    covered = 0
    sm = difflib.SequenceMatcher(None, ref, out, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            continue
        ov1, ov2 = max(a, i1), min(b, i2)
        if ov1 < ov2:
            covered += ov2 - ov1
    return covered


def target_recovered(row: dict, out: str) -> bool:
    corr = row["target_correction"]
    a = row["target_start"]
    b = a + len(corr)
    return bool(corr) and equal_coverage(row["reference"], out, a, b) == len(corr)


def bootstrap_by_passage(case_rows: list[dict], key: str, n=2000):
    grouped = collections.defaultdict(list)
    for r in case_rows:
        grouped[r["passage_id"]].append(r)
    pids = list(grouped)
    rng = random.Random(20260928)
    vals = []
    for _ in range(n):
        sampled = rng.choices(pids, k=len(pids))
        sample = [r for pid in sampled for r in grouped[pid]]
        vals.append(sum(bool(r[key]) for r in sample) / len(sample))
    vals.sort()
    return [vals[49], vals[1949]]


def main():
    ART.mkdir(parents=True, exist_ok=True)
    git_commit = subprocess.check_output(
        ["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"], text=True
    ).strip()
    if git_commit != "4d552ca3ae98029550f27fc52aa1b22883e16e61":
        raise RuntimeError(f"unexpected upstream commit {git_commit}")
    if not platform.python_version().startswith("3.10."):
        raise RuntimeError(platform.python_version())
    if not torch.__version__.startswith("1.12.1"):
        raise RuntimeError(torch.__version__)
    if transformers.__version__ != "4.30.0":
        raise RuntimeError(transformers.__version__)

    models = {
        "nopnx": load_model("nopnx"),
        "pnx": load_model("pnx"),
    }

    dev = read_jsonl(DEV)
    if len(dev) != 150 or len({x["passage_id"] for x in dev}) != 41:
        raise RuntimeError("development dataset integrity failed")

    # Infer once per unique source passage.
    passage_outputs = {}
    passage_traces = {}
    for row in dev:
        pid = row["passage_id"]
        if pid in passage_outputs:
            continue
        source = row["source"]
        passage_outputs[pid] = {}
        passage_traces[pid] = {}
        for variant in ("nopnx1", "nopnx2", "full"):
            out, trace = run_variant(source, models, variant)
            passage_outputs[pid][variant] = out
            passage_traces[pid][variant] = trace

    target_rows = []
    summaries = {}
    for row in dev:
        item = {
            "case_id": row["case_id"],
            "target_id": row["target_id"],
            "passage_id": row["passage_id"],
            "category_hint": row["category_hint"],
            "target_error": row["target_error"],
            "target_correction": row["target_correction"],
        }
        for variant in ("nopnx1", "nopnx2", "full"):
            out = passage_outputs[row["passage_id"]][variant]
            item[f"{variant}_recovered_exact"] = target_recovered(row, out)
            item[f"{variant}_output_changed"] = out != row["source"]
        target_rows.append(item)

    for variant in ("nopnx1", "nopnx2", "full"):
        key = f"{variant}_recovered_exact"
        recovered = sum(bool(x[key]) for x in target_rows)
        summaries[variant] = {
            "targets": 150,
            "recovered_exact": recovered,
            "recovery_rate": recovered / 150,
            "passage_cluster_bootstrap_95pct": bootstrap_by_passage(target_rows, key),
            "changed_passages": sum(
                passage_outputs[pid][variant] != next(x["source"] for x in dev if x["passage_id"] == pid)
                for pid in passage_outputs
            ),
            "applied_model_edits": sum(
                stage["applied_edit_count"]
                for pid in passage_traces
                for stage in passage_traces[pid][variant]
            ),
            "suppressed_hazards": sum(
                stage["suppressed_count"]
                for pid in passage_traces
                for stage in passage_traces[pid][variant]
            ),
        }

    # Project-authored scientific stress: exact protected spans are locked.
    sci = read_jsonl(SCI)
    corrections = {}
    if SCI_CORR.exists():
        corrections = json.loads(SCI_CORR.read_text(encoding="utf-8")).get("corrections", {})
    sci_cases = []
    for row in sci:
        protected = corrections.get(row["case_id"], {}).get("effective_protected", row["protected"])
        case = {
            "case_id": row["case_id"],
            "category": row["category"],
            "source": row["source"],
            "protected": protected,
            "human_gold_status": row["human_gold_status"],
            "variants": {},
        }
        for variant in ("nopnx1", "nopnx2", "full"):
            out, trace = run_variant(row["source"], models, variant, protected=protected)
            case["variants"][variant] = {
                "output": out,
                "source_exact_unchanged": out == row["source"],
                "protected_exact": all(p in out for p in protected),
                "contains_UNK": "[UNK]" in out,
                "trace": trace,
            }
        sci_cases.append(case)

    sci_summary = {}
    for variant in ("nopnx1", "nopnx2", "full"):
        sci_summary[variant] = {
            "cases": 12,
            "protected_exact_cases": sum(x["variants"][variant]["protected_exact"] for x in sci_cases),
            "source_exact_unchanged_cases": sum(x["variants"][variant]["source_exact_unchanged"] for x in sci_cases),
            "outputs_with_UNK": sum(x["variants"][variant]["contains_UNK"] for x in sci_cases),
        }

    # Word/character-level source change diagnostics on unique passages.
    diff_summary = {}
    for variant in ("nopnx1", "nopnx2", "full"):
        ops = []
        for pid in passage_outputs:
            source = next(x["source"] for x in dev if x["passage_id"] == pid)
            out = passage_outputs[pid][variant]
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, source, out, autojunk=False).get_opcodes():
                if tag != "equal":
                    ops.append({
                        "passage_id": pid,
                        "tag": tag,
                        "source_text": source[i1:i2],
                        "output_text": out[j1:j2],
                    })
        diff_summary[variant] = {
            "non_equal_diff_ops": len(ops),
            "ops": ops,
        }

    result = {
        "status": "DEVELOPMENT_SOURCE_PRESERVING_SURGICAL_PROTOTYPE",
        "not_sealed": True,
        "architecture": {
            "principle": "apply only model-supported non-K edits onto exact source surface",
            "hazard_abstentions": [
                "protected-span overlap",
                "tokenizer [UNK] word",
                "unsafe merge edit",
                "source-token mapping mismatch",
                "non-applicable edit",
                "post-edit [UNK]",
            ],
            "untouched_text_policy": "byte-for-byte source preservation",
        },
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "upstream_commit": git_commit,
            "model_sha256": PINS,
        },
        "target_summary": summaries,
        "scientific_stress_summary": sci_summary,
        "target_rows": target_rows,
        "scientific_cases": sci_cases,
        "passage_outputs": passage_outputs,
        "passage_traces": passage_traces,
        "diff_summary": diff_summary,
        "raw_baseline_reference": {
            "raw_nopnx1_exact_recovery": 29,
            "raw_full_exact_recovery": 29,
            "raw_full_scientific_exact_protected": 4,
            "raw_full_scientific_UNK_cases": 6,
        },
    }
    out_path = ART / "SURGICAL_RENDERER_RESULTS.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    compact = {
        "target_summary": summaries,
        "scientific_stress_summary": sci_summary,
        "surgical_renderer_result": str(out_path),
    }
    print(json.dumps(compact, ensure_ascii=False))


if __name__ == "__main__":
    main()
