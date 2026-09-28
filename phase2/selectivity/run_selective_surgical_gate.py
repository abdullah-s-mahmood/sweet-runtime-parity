"""Phase 2 development-only Selective Surgical Gate.

Runs NoPnx1 through the already validated source-preserving surgical renderer,
then applies a runtime-observable selective policy:
- non-space INSERT: allow
- REPLACE with top-1 confidence >= 0.80: allow
- DELETE: abstain
- all other/unsafe operations: abstain

Also evaluates an independent Arabic GED model as a localization signal. Nahw
target spans are used only for evaluation and never for runtime routing.

This is NOT a sealed evaluation and does not freeze thresholds.
"""
from __future__ import annotations

import collections
import difflib
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, BertForTokenClassification

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARABIC_EVAL = ROOT / "phase2" / "arabic_eval"
ART = ROOT / "artifacts"
sys.path.insert(0, str(ARABIC_EVAL))
import prototype_surgical_renderer as surg

DEV = ARABIC_EVAL / "DEVELOPMENT_TARGETS.jsonl"
SCI = ARABIC_EVAL / "SCIENTIFIC_STRESS_CASES.jsonl"
SCI_CORR = ARABIC_EVAL / "SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json"

GED_DIR = ROOT / "models" / "ged"


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def operation_family(label: str) -> str:
    if "I_[" in label:
        return "INSERT"
    if "R_[" in label:
        return "REPLACE"
    if "D" in label:
        return "DELETE"
    if "A_[" in label:
        return "APPEND"
    return "OTHER"


def insertion_payload(label: str) -> str:
    m = re.search(r"I_\[([^\]]*)\]", label)
    return m.group(1) if m else ""


def operation_policy(edit: dict) -> tuple[bool, str]:
    fam = operation_family(edit["label"])
    conf = float(edit["top1_confidence"])
    if fam == "INSERT":
        payload = insertion_payload(edit["label"])
        if payload.strip() == "":
            return False, "ABSTAIN_INSERT_WHITESPACE"
        return True, "ALLOW_NONSPACE_INSERT"
    if fam == "REPLACE":
        if conf >= 0.80:
            return True, "ALLOW_REPLACE_CONF_GE_0_80"
        return False, "ABSTAIN_REPLACE_CONF_LT_0_80"
    if fam == "DELETE":
        return False, "ABSTAIN_DELETE"
    return False, f"ABSTAIN_{fam}"


def whitespace_words(text: str):
    ms = list(re.finditer(r"\S+", text))
    return [m.group(0) for m in ms], [(m.start(), m.end()) for m in ms]


def apply_selected_edits(source: str, candidate_edits: list[dict], selector):
    words, spans = whitespace_words(source)
    selected = []
    abstained = []
    per_word = collections.defaultdict(list)
    for idx, e in enumerate(candidate_edits):
        decision, reason = selector(e)
        item = {"candidate_edit_index": idx, **e, "gate_reason": reason}
        if decision:
            selected.append(item)
            per_word[int(e["word_index"])].append(item)
        else:
            abstained.append(item)

    # Conservative overlap check within each source word.
    safe_selected = []
    for wi, edits in per_word.items():
        intervals = sorted((int(e["source_local_span"][0]), int(e["source_local_span"][1]), e) for e in edits)
        overlap = any(intervals[i][0] < intervals[i-1][1] for i in range(1, len(intervals)))
        if overlap:
            for _, _, e in intervals:
                e2 = dict(e)
                e2["gate_reason"] = "ABSTAIN_SELECTED_EDIT_OVERLAP"
                abstained.append(e2)
            continue
        safe_selected.extend(e for _, _, e in intervals)

    # Rebuild only words receiving selected edits. Untouched bytes remain exact.
    word_replacements = {}
    for wi in sorted({int(e["word_index"]) for e in safe_selected}):
        original = words[wi]
        es = [e for e in safe_selected if int(e["word_index"]) == wi]
        new = original
        for e in sorted(es, key=lambda z: int(z["source_local_span"][0]), reverse=True):
            a, b = map(int, e["source_local_span"])
            if new[a:b] != e["source_text"]:
                # The edit no longer maps after a prior patch; abstain from whole word.
                for x in es:
                    x2 = dict(x)
                    x2["gate_reason"] = "ABSTAIN_ROUNDTRIP_MISMATCH"
                    abstained.append(x2)
                new = original
                es = []
                break
            new = new[:a] + e["replacement"] + new[b:]
        if es and new != original:
            word_replacements[wi] = new

    output = source
    for wi in sorted(word_replacements, reverse=True):
        a, b = spans[wi]
        output = output[:a] + word_replacements[wi] + output[b:]

    actually_selected = [
        e for e in safe_selected
        if int(e["word_index"]) in word_replacements
    ]
    return output, actually_selected, abstained


def load_ged():
    tok = AutoTokenizer.from_pretrained(str(GED_DIR), local_files_only=True, use_fast=True)
    model = BertForTokenClassification.from_pretrained(str(GED_DIR), local_files_only=True)
    model.eval().cpu()
    if "UC" not in model.config.label2id:
        raise RuntimeError("GED model has no UC label")
    return tok, model


def ged_word_scores(text: str, tok, model):
    words, word_spans = whitespace_words(text)
    encoded = tok(
        text,
        return_tensors="pt",
        return_offsets_mapping=True,
        truncation=True,
        max_length=512,
    )
    offsets = encoded.pop("offset_mapping")[0].tolist()
    with torch.no_grad():
        logits = model(**encoded).logits[0]
        probs = torch.softmax(logits, dim=-1)
    uc_id = int(model.config.label2id["UC"])
    preds = probs.argmax(-1).tolist()
    out = [
        {
            "word_index": i,
            "word": w,
            "span": list(word_spans[i]),
            "ged_error_probability": 0.0,
            "ged_top_label": "UC",
            "ged_top_label_probability": 1.0,
            "covered_subtokens": 0,
        }
        for i, w in enumerate(words)
    ]
    for ti, (a, b) in enumerate(offsets):
        if a == b:
            continue
        wi = None
        for j, (wa, wb) in enumerate(word_spans):
            if a < wb and b > wa:
                wi = j
                break
        if wi is None:
            continue
        p_error = float(1.0 - probs[ti, uc_id].item())
        top_id = int(preds[ti])
        top_label = model.config.id2label[top_id]
        top_prob = float(probs[ti, top_id].item())
        out[wi]["covered_subtokens"] += 1
        if p_error > out[wi]["ged_error_probability"]:
            out[wi]["ged_error_probability"] = p_error
            out[wi]["ged_top_label"] = top_label
            out[wi]["ged_top_label_probability"] = top_prob
    return out


def selector_with_ged(base_selector, ged_by_word, mode: str, threshold: float | None = None):
    def _select(edit):
        ok, base_reason = base_selector(edit)
        if not ok:
            return False, base_reason
        wi = int(edit["word_index"])
        g = ged_by_word[wi]
        if mode == "top_non_uc":
            if g["ged_top_label"] != "UC":
                return True, base_reason + "+GED_NON_UC"
            return False, "ABSTAIN_GED_UC"
        if mode == "prob":
            assert threshold is not None
            if float(g["ged_error_probability"]) >= threshold:
                return True, base_reason + f"+GED_ERRPROB_GE_{threshold:.2f}"
            return False, f"ABSTAIN_GED_ERRPROB_LT_{threshold:.2f}"
        raise ValueError(mode)
    return _select


def target_recovered(row: dict, out: str) -> bool:
    return surg.target_recovered(row, out)


def target_word_index(row: dict) -> int | None:
    _, spans = whitespace_words(row["source"])
    a, b = int(row["target_start"]), int(row["target_end"])
    for i, (wa, wb) in enumerate(spans):
        if a < wb and b > wa:
            return i
    return None


def summarize_variant(name, outputs, dev):
    exact = 0
    changed = 0
    for row in dev:
        out = outputs[row["passage_id"]]
        exact += int(target_recovered(row, out))
    for pid, out in outputs.items():
        src = next(r["source"] for r in dev if r["passage_id"] == pid)
        changed += int(out != src)
    return {
        "name": name,
        "exact_target_recoveries": exact,
        "exact_target_recovery_rate": exact / len(dev),
        "changed_passages": changed,
    }


def main():
    ART.mkdir(parents=True, exist_ok=True)

    upstream_commit = subprocess.check_output(
        ["git", "-C", str(ROOT / "upstream" / "text-editing"), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if upstream_commit != "4d552ca3ae98029550f27fc52aa1b22883e16e61":
        raise RuntimeError(upstream_commit)
    if not platform.python_version().startswith("3.10."):
        raise RuntimeError(platform.python_version())
    if not torch.__version__.startswith("1.12.1"):
        raise RuntimeError(torch.__version__)
    if transformers.__version__ != "4.30.0":
        raise RuntimeError(transformers.__version__)

    nopnx = surg.load_model("nopnx")
    models = {"nopnx": nopnx}
    ged_tok, ged_model = load_ged()

    dev = read_jsonl(DEV)
    sci = read_jsonl(SCI)
    corrections = {}
    if SCI_CORR.exists():
        corrections = json.loads(SCI_CORR.read_text(encoding="utf-8")).get("corrections", {})

    passages = {}
    for r in dev:
        passages.setdefault(r["passage_id"], r["source"])

    raw_passages = {}
    variants = {
        "op_aware": {},
        "op_aware_ged_non_uc": {},
        "op_aware_ged_p30": {},
        "op_aware_ged_p50": {},
        "op_aware_ged_p70": {},
    }
    edit_records = []
    ged_records = []

    for pid, source in passages.items():
        baseline_out, trace = surg.run_variant(source, models, "nopnx1")
        stage = trace[0]
        candidate_edits = stage.get("applied_edits", [])
        ged = ged_word_scores(source, ged_tok, ged_model)
        ged_by_word = {int(x["word_index"]): x for x in ged}

        op_out, op_selected, op_abstained = apply_selected_edits(source, candidate_edits, operation_policy)
        variants["op_aware"][pid] = op_out

        ged_selectors = {
            "op_aware_ged_non_uc": selector_with_ged(operation_policy, ged_by_word, "top_non_uc"),
            "op_aware_ged_p30": selector_with_ged(operation_policy, ged_by_word, "prob", 0.30),
            "op_aware_ged_p50": selector_with_ged(operation_policy, ged_by_word, "prob", 0.50),
            "op_aware_ged_p70": selector_with_ged(operation_policy, ged_by_word, "prob", 0.70),
        }
        ged_variant_meta = {}
        for name, selector in ged_selectors.items():
            out, selected, abstained = apply_selected_edits(source, candidate_edits, selector)
            variants[name][pid] = out
            ged_variant_meta[name] = {
                "selected_indices": [int(e["candidate_edit_index"]) for e in selected],
                "abstained_indices": [int(e["candidate_edit_index"]) for e in abstained],
            }

        enriched = []
        for ei, e in enumerate(candidate_edits):
            wi = int(e["word_index"])
            enriched.append({
                "edit_index": ei,
                **e,
                "operation_family": operation_family(e["label"]),
                "operation_policy_allow": operation_policy(e)[0],
                "operation_policy_reason": operation_policy(e)[1],
                "ged": ged_by_word[wi],
                "ged_gate_membership": {
                    name: ei in meta["selected_indices"]
                    for name, meta in ged_variant_meta.items()
                },
            })

        raw_passages[pid] = {
            "source": source,
            "baseline_surgical_output": baseline_out,
            "baseline_candidate_edits": enriched,
            "baseline_suppressed_hazards": stage.get("suppressed", []),
            "operation_aware_output": op_out,
            "operation_aware_selected_indices": [int(e["candidate_edit_index"]) for e in op_selected],
            "operation_aware_abstained_indices": [int(e["candidate_edit_index"]) for e in op_abstained],
            "gate_outputs": {
                name: variants[name][pid]
                for name in ("op_aware_ged_non_uc","op_aware_ged_p30","op_aware_ged_p50","op_aware_ged_p70")
            },
            "ged_words": ged,
            "ged_variant_meta": ged_variant_meta,
        }
        for e in enriched:
            edit_records.append({"passage_id": pid, **e})
        for g in ged:
            ged_records.append({"passage_id": pid, **g})

    summaries = {
        name: summarize_variant(name, outputs, dev)
        for name, outputs in variants.items()
    }

    # GED published-target localization recall only. Non-target predictions are NOT
    # treated as false positives because the Nahw target extraction is not exhaustive.
    target_ged = []
    for row in dev:
        pid = row["passage_id"]
        wi = target_word_index(row)
        if wi is None:
            target_ged.append({
                "case_id": row["case_id"],
                "target_id": row["target_id"],
                "passage_id": pid,
                "word_index": None,
                "mapping_status": "NO_WORD_MAPPING",
            })
            continue
        g = raw_passages[pid]["ged_words"][wi]
        target_ged.append({
            "case_id": row["case_id"],
            "target_id": row["target_id"],
            "passage_id": pid,
            "word_index": wi,
            "target_error": row["target_error"],
            "ged_top_label": g["ged_top_label"],
            "ged_error_probability": g["ged_error_probability"],
            "detected_top_non_uc": g["ged_top_label"] != "UC",
            "detected_p30": g["ged_error_probability"] >= 0.30,
            "detected_p50": g["ged_error_probability"] >= 0.50,
            "detected_p70": g["ged_error_probability"] >= 0.70,
        })
    ged_recall = {}
    mapped = [x for x in target_ged if x.get("word_index") is not None]
    for key in ("detected_top_non_uc", "detected_p30", "detected_p50", "detected_p70"):
        ged_recall[key] = {
            "detected": sum(bool(x[key]) for x in mapped),
            "mapped_targets": len(mapped),
            "published_target_recall": sum(bool(x[key]) for x in mapped) / len(mapped),
        }

    # Scientific stress using the same operation-aware and GED gates. Protected
    # source spans are locked by the surgical candidate generator.
    sci_results = []
    sci_summary = collections.defaultdict(lambda: {"cases": 0, "protected_exact": 0, "source_exact_unchanged": 0, "unk_outputs": 0})
    for row in sci:
        protected = corrections.get(row["case_id"], {}).get("effective_protected", row["protected"])
        source = row["source"]
        baseline_out, trace = surg.run_variant(source, models, "nopnx1", protected=protected)
        candidates = trace[0].get("applied_edits", [])
        ged = ged_word_scores(source, ged_tok, ged_model)
        ged_by_word = {int(x["word_index"]): x for x in ged}
        sels = {
            "op_aware": operation_policy,
            "op_aware_ged_non_uc": selector_with_ged(operation_policy, ged_by_word, "top_non_uc"),
            "op_aware_ged_p50": selector_with_ged(operation_policy, ged_by_word, "prob", 0.50),
        }
        variants_out = {}
        for name, selector in sels.items():
            out, selected, abstained = apply_selected_edits(source, candidates, selector)
            variants_out[name] = {
                "output": out,
                "selected_edits": selected,
                "abstained_edits": abstained,
                "protected_exact": all(p in out for p in protected),
                "source_exact_unchanged": out == source,
                "contains_UNK": "[UNK]" in out,
            }
            z = sci_summary[name]
            z["cases"] += 1
            z["protected_exact"] += int(variants_out[name]["protected_exact"])
            z["source_exact_unchanged"] += int(variants_out[name]["source_exact_unchanged"])
            z["unk_outputs"] += int(variants_out[name]["contains_UNK"])
        sci_results.append({
            "case_id": row["case_id"],
            "category": row["category"],
            "protected": protected,
            "variants": variants_out,
        })

    result = {
        "status": "PHASE2_SELECTIVE_SURGICAL_GATE_DEVELOPMENT",
        "not_sealed": True,
        "policy_origin": "Retrospective development policy from prior adjudication; this run implements it prospectively with runtime-observable features only.",
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "upstream_commit": upstream_commit,
        },
        "operation_policy": {
            "INSERT": "allow only non-whitespace insertion",
            "REPLACE": "allow when top1 confidence >= 0.80",
            "DELETE": "abstain",
            "OTHER": "abstain",
        },
        "variant_summaries": summaries,
        "ged_published_target_localization": {
            "warning": "Recall against published target locations only; non-target GED predictions are not counted as false positives.",
            "summary": ged_recall,
            "targets": target_ged,
        },
        "scientific_stress_summary": dict(sci_summary),
        "scientific_cases": sci_results,
        "passages": raw_passages,
        "candidate_edits": edit_records,
    }
    out = ART / "SELECTIVE_SURGICAL_GATE_RAW.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "variant_summaries": summaries,
        "ged_target_recall": ged_recall,
        "scientific_stress_summary": dict(sci_summary),
        "output": str(out),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()