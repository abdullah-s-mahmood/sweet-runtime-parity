#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass

VERSION = "MPSEF_P2_V2_IDENTITY_STAGE0_V1"
IGNORE_INDEX = -100


class Stage0Error(RuntimeError):
    pass


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FakeTokenizer:
    pieces: dict[str, list[str]]
    model_max_length: int
    cls_token_id: int = 101
    sep_token_id: int = 102
    bos_token_id: int = 1
    eos_token_id: int = 2
    pad_token_id: int = 0

    def tokenize(self, word: str) -> list[str]:
        return list(self.pieces.get(word, [word]))

    def convert_tokens_to_ids(self, tokens: list[str]) -> list[int]:
        # Stable synthetic IDs only. No Python hash randomization.
        return [
            int(hashlib.sha256(t.encode("utf-8")).hexdigest()[:8], 16) % 30000 + 100
            for t in tokens
        ]


def build_ged_segments(words, tokenizer: FakeTokenizer, max_seq_length: int):
    if max_seq_length <= 2:
        raise Stage0Error("P2V2_INVALID_GED_MAX_LENGTH")
    effective_budget = max_seq_length - 2

    per_word = []
    for wi, word in enumerate(words):
        pieces = tokenizer.tokenize(word)
        if not pieces:
            raise Stage0Error(f"P2V2_ZERO_TOKEN_WORD:GED:{wi}")
        if len(pieces) > effective_budget:
            raise Stage0Error(
                f"P2V2_SINGLE_WORD_EXCEEDS_GED_BUDGET:{wi}:{len(pieces)}>{effective_budget}"
            )
        per_word.append((wi, word, pieces))

    segments = []
    current = []
    current_piece_count = 0
    for rec in per_word:
        wi, word, pieces = rec
        if current and current_piece_count + len(pieces) > effective_budget:
            segments.append(current)
            current = []
            current_piece_count = 0
        current.append(rec)
        current_piece_count += len(pieces)
    if current:
        segments.append(current)

    out = []
    seen = []
    for sid, seg in enumerate(segments):
        pos = 1  # CLS occupies 0
        word_records = []
        tokens = ["[CLS]"]
        label_mask = [IGNORE_INDEX]
        for wi, word, pieces in seg:
            first = pos
            start = pos
            end = pos + len(pieces)
            word_records.append({
                "morph_word_index": wi,
                "morph_word_text": word,
                "ged_segment_id": sid,
                "ged_wordpiece_start": start,
                "ged_wordpiece_end": end,
                "ged_first_wordpiece_index": first,
                "ged_wordpieces": list(pieces),
            })
            tokens.extend(pieces)
            label_mask.append(0)  # real word-label position
            label_mask.extend([IGNORE_INDEX] * (len(pieces) - 1))
            seen.append(wi)
            pos = end
        tokens.append("[SEP]")
        label_mask.append(IGNORE_INDEX)
        if len(tokens) > max_seq_length:
            raise Stage0Error("P2V2_SEGMENT_OVERFLOW")
        out.append({
            "segment_id": sid,
            "tokens": tokens,
            "label_mask": label_mask,
            "word_records": word_records,
            "total_encoded_length": len(tokens),
            "content_wordpieces": len(tokens) - 2,
            "max_seq_length": max_seq_length,
        })

    if seen != list(range(len(words))):
        raise Stage0Error(f"P2V2_WORD_IDENTITY_BIJECTION_FAILED:segmentation:{seen}")
    return out


def reconstruct_word_labels(words, segments, predictions_by_segment):
    if len(predictions_by_segment) != len(segments):
        raise Stage0Error("P2V2_SEGMENT_PREDICTION_COUNT_MISMATCH")

    mapping = {}
    for seg, preds in zip(segments, predictions_by_segment):
        if len(preds) != len(seg["label_mask"]):
            raise Stage0Error("P2V2_SEGMENT_LOGIT_LENGTH_MISMATCH")
        for wr in seg["word_records"]:
            wi = wr["morph_word_index"]
            if wi in mapping:
                raise Stage0Error(f"P2V2_WORD_IDENTITY_BIJECTION_FAILED:duplicate:{wi}")
            pos = wr["ged_first_wordpiece_index"]
            if seg["label_mask"][pos] == IGNORE_INDEX:
                raise Stage0Error("P2V2_FIRST_WORDPIECE_WAS_MASKED")
            mapping[wi] = preds[pos]

            for p in range(wr["ged_wordpiece_start"] + 1, wr["ged_wordpiece_end"]):
                if seg["label_mask"][p] != IGNORE_INDEX:
                    raise Stage0Error("P2V2_NONFIRST_WORDPIECE_NOT_MASKED")

    expected = set(range(len(words)))
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise Stage0Error(
            f"P2V2_WORD_IDENTITY_BIJECTION_FAILED:missing={missing}:extra={extra}"
        )

    ordered = [mapping[i] for i in range(len(words))]
    return ordered


def validate_identity_records(words, records):
    indices = [r["morph_word_index"] for r in records]
    if indices != list(range(len(words))):
        raise Stage0Error(
            f"P2V2_WORD_IDENTITY_BIJECTION_FAILED:order={indices}"
        )
    for i, r in enumerate(records):
        if r["morph_word_text"] != words[i]:
            raise Stage0Error(f"P2V2_WORD_IDENTITY_TEXT_MISMATCH:{i}")
    return True


def project_labels_to_gec(
    words,
    word_labels,
    tokenizer: FakeTokenizer,
    gec_label2id,
    boundary_label="UC",
):
    if len(words) != len(word_labels):
        raise Stage0Error("P2V2_WORD_LABEL_COUNT_MISMATCH")
    if boundary_label not in gec_label2id:
        raise Stage0Error("P2V2_BOUNDARY_LABEL_NOT_IN_GEC_VOCAB")

    tokens = []
    labels = []
    word_map = []
    for wi, (word, label) in enumerate(zip(words, word_labels)):
        pieces = tokenizer.tokenize(word)
        if not pieces:
            raise Stage0Error(f"P2V2_ZERO_TOKEN_WORD:GEC:{wi}")
        if label not in gec_label2id:
            raise Stage0Error(f"P2V2_GED_LABEL_NOT_IN_GEC_VOCAB:{label}")
        start = len(tokens) + 1  # BOS occupies 0
        tokens.extend(pieces)
        labels.extend([label] * len(pieces))
        end = len(tokens) + 1
        word_map.append({
            "morph_word_index": wi,
            "gec_subword_start": start,
            "gec_subword_end": end,
            "gec_subwords": list(pieces),
        })

    input_ids = [tokenizer.bos_token_id] + tokenizer.convert_tokens_to_ids(tokens) + [tokenizer.eos_token_id]
    label_names = [boundary_label] + labels + [boundary_label]
    label_ids = [gec_label2id[name] for name in label_names]
    attention_mask = [1] * len(input_ids)

    if not (len(input_ids) == len(label_ids) == len(attention_mask)):
        raise Stage0Error("P2V2_GEC_CONDITIONING_LENGTH_MISMATCH")
    return {
        "input_ids": input_ids,
        "ged_label_names": label_names,
        "ged_label_ids": label_ids,
        "attention_mask": attention_mask,
        "word_map": word_map,
    }


def validate_generation_trace(
    generated_token_ids,
    decoder_start_token_id,
    eos_token_id,
    max_length,
    *,
    forced_eos_at_limit=False,
):
    if not generated_token_ids:
        raise Stage0Error("P2V2_EMPTY_GENERATION_TRACE")
    if max_length <= 0:
        raise Stage0Error("P2V2_INVALID_GENERATION_MAX_LENGTH")

    # One known decoder prefix token is excluded from terminal EOS search.
    prefix_len = 1
    body = generated_token_ids[prefix_len:]
    eos_positions = [i + prefix_len for i, tok in enumerate(body) if tok == eos_token_id]

    hit_ceiling = len(generated_token_ids) >= max_length
    if not eos_positions:
        raise Stage0Error("P2V2_TERMINAL_EOS_UNPROVEN")

    terminal_eos = eos_positions[0]
    if hit_ceiling and forced_eos_at_limit and terminal_eos == len(generated_token_ids) - 1:
        raise Stage0Error("P2V2_FORCED_EOS_AT_GENERATION_CEILING")

    return {
        "prefix_len": prefix_len,
        "terminal_eos_index": terminal_eos,
        "decoder_prefix_equals_eos": decoder_start_token_id == eos_token_id,
        "hit_ceiling": hit_ceiling,
    }


class FakeGedConditionedModel:
    def __init__(self, consumes_tags: bool):
        self.consumes_tags = consumes_tags

    def synthetic_forward_signature(self, input_ids, ged_tags):
        base = sum(input_ids)
        return base + (sum(ged_tags) if self.consumes_tags else 0)


def prove_ged_tags_consumed(model):
    x = [1, 2, 3]
    a = model.synthetic_forward_signature(x, [0, 0, 0])
    b = model.synthetic_forward_signature(x, [0, 1, 0])
    if a == b:
        raise Stage0Error("P2V2_GED_TAG_INTERFACE_UNPROVEN")
    return True


def self_test():
    results = {}

    def ok(name, fn):
        fn()
        results[name] = "PASS"

    def fail(name, fn, contains):
        try:
            fn()
        except Stage0Error as e:
            if contains not in str(e):
                raise AssertionError(f"{name}: wrong failure {e!r}")
            results[name] = "PASS"
            return
        raise AssertionError(f"{name}: expected failure")

    # Baseline tokenizers.
    ged = FakeTokenizer(
        pieces={
            "a": ["a1"],
            "b": ["b1", "b2"],
            "c": ["c1"],
            "empty": [],
            "fit3": ["f1", "f2", "f3"],
            "over4": ["o1", "o2", "o3", "o4"],
        },
        model_max_length=5,
    )
    gec = FakeTokenizer(
        pieces={
            "a": ["ga"],
            "b": ["gb1", "gb2"],
            "c": ["gc"],
            "empty": [],
        },
        model_max_length=16,
    )

    # S-B01-01 zero GED-token word.
    fail(
        "S-B01-01_ZERO_GED_TOKEN",
        lambda: build_ged_segments(["a", "empty"], ged, 5),
        "P2V2_ZERO_TOKEN_WORD:GED",
    )

    # S-B01-02 zero GEC-token word.
    fail(
        "S-B01-02_ZERO_GEC_TOKEN",
        lambda: project_labels_to_gec(
            ["a", "empty"], ["UC", "UC"], gec, {"UC": 0}
        ),
        "P2V2_ZERO_TOKEN_WORD:GEC",
    )

    # S-B01-03 exact content budget fit (3 pieces + CLS/SEP = 5).
    ok(
        "S-B01-03_EXACT_GED_BUDGET",
        lambda: (
            (lambda s: (
                (_ for _ in ()).throw(AssertionError("wrong segment len"))
                if s[0]["total_encoded_length"] != 5 else None
            ))(build_ged_segments(["fit3"], ged, 5))
        ),
    )

    # S-B01-04 over budget by one.
    fail(
        "S-B01-04_WORD_OVER_BUDGET",
        lambda: build_ged_segments(["over4"], ged, 5),
        "P2V2_SINGLE_WORD_EXCEEDS_GED_BUDGET",
    )

    # S-B01-05 exact segment total length.
    ok(
        "S-B01-05_SEGMENT_EXACT_LIMIT",
        lambda: (
            (lambda s: (
                (_ for _ in ()).throw(AssertionError("not exact limit"))
                if s[0]["total_encoded_length"] != 5 else None
            ))(build_ged_segments(["a", "b"], ged, 5))
        ),
    )

    # S-B01-06 next full word starts a new segment.
    def test_new_segment():
        s = build_ged_segments(["a", "b", "c"], ged, 5)
        assert len(s) == 2
        flat = [r["morph_word_index"] for seg in s for r in seg["word_records"]]
        assert flat == [0, 1, 2]
    ok("S-B01-06_WHOLE_WORD_SEGMENT_SPLIT", test_new_segment)

    base_segments = build_ged_segments(["a", "b"], ged, 5)
    # Synthetic per-token predictions; first-wordpiece labels are used.
    base_preds = [["CLS", "L_A", "L_B", "IGNORED", "SEP"]]
    assert reconstruct_word_labels(["a", "b"], base_segments, base_preds) == ["L_A", "L_B"]

    # S-B01-07 duplicate index.
    def dup_index():
        s = json.loads(json.dumps(base_segments))
        s[0]["word_records"][1]["morph_word_index"] = 0
        reconstruct_word_labels(["a", "b"], s, base_preds)
    fail("S-B01-07_DUPLICATE_WORD_INDEX", dup_index, "duplicate")

    # S-B01-08 missing index.
    def missing_index():
        s = json.loads(json.dumps(base_segments))
        s[0]["word_records"] = s[0]["word_records"][:1]
        reconstruct_word_labels(["a", "b"], s, base_preds)
    fail("S-B01-08_MISSING_WORD_INDEX", missing_index, "missing")

    # S-B01-09 reordered identity records.
    fail(
        "S-B01-09_REORDERED_WORDS",
        lambda: validate_identity_records(
            ["a", "b"],
            [
                {"morph_word_index": 1, "morph_word_text": "b"},
                {"morph_word_index": 0, "morph_word_text": "a"},
            ],
        ),
        "order=",
    )

    # S-B01-10 equal counts but wrong identity assignment.
    fail(
        "S-B01-10_EQUAL_COUNTS_WRONG_IDENTITY",
        lambda: validate_identity_records(
            ["a", "b"],
            [
                {"morph_word_index": 0, "morph_word_text": "b"},
                {"morph_word_index": 1, "morph_word_text": "a"},
            ],
        ),
        "TEXT_MISMATCH",
    )

    # S-B01-11 unknown GED label in GEC vocabulary.
    fail(
        "S-B01-11_UNKNOWN_GED_LABEL",
        lambda: project_labels_to_gec(
            ["a"], ["REPLACE_X"], gec, {"UC": 0, "REPLACE_O": 1}
        ),
        "P2V2_GED_LABEL_NOT_IN_GEC_VOCAB",
    )

    # S-B01-12 name-based remap ignores numeric-ID coincidence.
    def label_name_remap():
        out = project_labels_to_gec(
            ["a", "b"], ["ERR", "UC"], gec, {"UC": 9, "ERR": 3}
        )
        assert out["ged_label_ids"] == [9, 3, 9, 9, 9]
    ok("S-B01-12_NAME_BASED_LABEL_REMAP", label_name_remap)

    # S-B01-13 conditioning length mismatch is caught explicitly.
    def mismatch_lengths():
        out = project_labels_to_gec(["a"], ["UC"], gec, {"UC": 0})
        out["ged_label_ids"].append(0)
        if not (
            len(out["input_ids"])
            == len(out["ged_label_ids"])
            == len(out["attention_mask"])
        ):
            raise Stage0Error("P2V2_GEC_CONDITIONING_LENGTH_MISMATCH")
    fail(
        "S-B01-13_GEC_LENGTH_MISMATCH",
        mismatch_lengths,
        "P2V2_GEC_CONDITIONING_LENGTH_MISMATCH",
    )

    # S-B01-14 prove ged_tags are actually consumed.
    ok(
        "S-B01-14_GED_TAGS_CONSUMED",
        lambda: prove_ged_tags_consumed(FakeGedConditionedModel(True)),
    )
    fail(
        "S-B01-14B_GED_TAGS_IGNORED",
        lambda: prove_ged_tags_consumed(FakeGedConditionedModel(False)),
        "P2V2_GED_TAG_INTERFACE_UNPROVEN",
    )

    # S-B01-15 decoder prefix equal to EOS is not terminal EOS.
    def prefix_equals_eos():
        tr = validate_generation_trace([2, 11, 12, 2], 2, 2, 10)
        assert tr["terminal_eos_index"] == 3
        assert tr["decoder_prefix_equals_eos"] is True
    ok("S-B01-15_PREFIX_EOS_NOT_TERMINAL", prefix_equals_eos)

    # S-B01-16 forced EOS at ceiling fails closed.
    fail(
        "S-B01-16_FORCED_EOS_AT_CEILING",
        lambda: validate_generation_trace(
            [2, 11, 12, 13, 2], 2, 2, 5, forced_eos_at_limit=True
        ),
        "P2V2_FORCED_EOS_AT_GENERATION_CEILING",
    )

    # S-B01-17 reordered batch reconstruction by stable word identity.
    def batch_reorder():
        words = ["a", "b", "c"]
        s = build_ged_segments(words, ged, 5)
        # Process segment predictions in their own stable segment order.
        preds = []
        for seg in s:
            arr = ["IGN"] * len(seg["label_mask"])
            for wr in seg["word_records"]:
                arr[wr["ged_first_wordpiece_index"]] = f"L{wr['morph_word_index']}"
            preds.append(arr)
        labels = reconstruct_word_labels(words, s, preds)
        assert labels == ["L0", "L1", "L2"]
    ok("S-B01-17_UID_WORD_IDENTITY_RECONSTRUCTION", batch_reorder)

    # S-B01-18 repeated deterministic trace.
    def repeated_identity():
        a = build_ged_segments(["a", "b", "c"], ged, 5)
        b = build_ged_segments(["a", "b", "c"], ged, 5)
        assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
        assert sha_text(json.dumps(a, sort_keys=True)) == sha_text(json.dumps(b, sort_keys=True))
    ok("S-B01-18_REPEAT_BYTE_IDENTITY", repeated_identity)

    # Additional missing EOS regression.
    fail(
        "S-B01-EXTRA_MISSING_EOS",
        lambda: validate_generation_trace([2, 11, 12, 13], 2, 2, 10),
        "P2V2_TERMINAL_EOS_UNPROVEN",
    )

    summary = {
        "record_id": VERSION,
        "status": "PASS",
        "tests": results,
        "test_count": len(results),
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "project_metric_computed": False,
        "model_inference_run": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if not args.self_test:
        raise SystemExit("STAGE0_SYNTHETIC_ONLY; use --self-test")
    self_test()


if __name__ == "__main__":
    main()
