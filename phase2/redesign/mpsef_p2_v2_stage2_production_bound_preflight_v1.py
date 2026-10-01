#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path

import mpsef_p2_v2_identity_stage0 as legacy_b01
import mpsef_p2_v2_stage2_production_adapter_v1 as prod


VERSION = "MPSEF_P2_V2_STAGE2_PRODUCTION_BOUND_PREFLIGHT_V1"


class FakeGecTokenizer:
    def batch_decode(
        self,
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    ):
        return ["تصحيح اختباري ."]


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def synthetic_row(case_id):
    source = "هذا اختبار ."
    return {
        "uid": f"SYN:{case_id}",
        "case_id": case_id,
        "cluster_id": f"SYN-C:{case_id}",
        "source": source,
        "source_sha256": sha_text(source),
    }


def valid_segments():
    return [{
        "segment_id": 0,
        "input_ids": [101, 1001, 1002, 102],
        "attention_mask": [1, 1, 1, 1],
        "token_type_ids": [0, 0, 0, 0],
        "label_mask": [-100, 0, 0, -100],
        "word_records": [
            {
                "morph_word_index": 0,
                "morph_word_text": "هذا",
                "ged_segment_id": 0,
                "ged_wordpiece_start": 1,
                "ged_wordpiece_end": 2,
                "ged_first_wordpiece_index": 1,
                "ged_wordpieces": ["هذا"],
            },
            {
                "morph_word_index": 1,
                "morph_word_text": "اختبار",
                "ged_segment_id": 0,
                "ged_wordpiece_start": 2,
                "ged_wordpiece_end": 3,
                "ged_first_wordpiece_index": 2,
                "ged_wordpieces": ["اختبار"],
            },
        ],
        "total_encoded_length": 4,
        "content_wordpieces": 2,
    }]


def valid_infer(words, tokenizer, model, segments):
    labels = ["UC", "UC"]
    trace = [
        {
            **segments[0]["word_records"][0],
            "ged_prediction_position": 1,
            "ged_label_id": 0,
            "ged_label_name": "UC",
        },
        {
            **segments[0]["word_records"][1],
            "ged_prediction_position": 2,
            "ged_label_id": 0,
            "ged_label_name": "UC",
        },
    ]
    return labels, trace, [[4, 2]]


def valid_project(words, labels, tokenizer, model):
    return {
        "tokens": ["هذا", "اختبار"],
        "input_ids": [1, 10, 11, 2],
        "ged_label_names": ["UC", "UC", "UC", "UC"],
        "ged_label_ids": [0, 0, 0, 0],
        "attention_mask": [1, 1, 1, 1],
        "word_map": [
            {
                "morph_word_index": 0,
                "morph_word_text": "هذا",
                "gec_subword_start": 1,
                "gec_subword_end": 2,
                "gec_subwords": ["هذا"],
            },
            {
                "morph_word_index": 1,
                "morph_word_text": "اختبار",
                "gec_subword_start": 2,
                "gec_subword_end": 3,
                "gec_subwords": ["اختبار"],
            },
        ],
    }


def valid_generate(tokenizer, model, prepared):
    class Generated:
        def __getitem__(self, i):
            return self
        def tolist(self):
            return [2, 20, 21, 2]

    evidence = {
        "effective_generation_config": {
            "decoder_start_token_id": 2,
            "eos_token_id": 2,
            "max_length": 100,
        },
        "generated_token_ids": [2, 20, 21, 2],
        "generation_token_count": 4,
        "terminal_eos_index": 3,
        "generation_hit_ceiling": False,
        "decoder_prefix_equals_eos": True,
        "ged_embedding_hook_calls": [{
            "input_shape": [1, 4],
            "output_shape": [1, 4, 16],
        }],
    }
    return Generated(), evidence


def raise_error(message, *, ged_evidence=None, gen_evidence=None):
    exc = prod.Stage0Error(message)
    if ged_evidence is not None:
        setattr(exc, "p2_stage2_ged_evidence", ged_evidence)
    if gen_evidence is not None:
        setattr(exc, "p2_stage2_generation_evidence", gen_evidence)
    raise exc


@contextlib.contextmanager
def patched_production(case):
    originals = {
        "morph_words": prod.morph_words,
        "build_ged_segments": prod.build_ged_segments,
        "infer_ged_with_preserved_segments": (
            prod.infer_ged_with_preserved_segments
        ),
        "project_to_gec": prod.project_to_gec,
        "generate_with_evidence": prod.generate_with_evidence,
    }

    prod.morph_words = lambda disambig, source: ["هذا", "اختبار"]
    prod.build_ged_segments = (
        lambda words, tok: valid_segments()
    )
    prod.infer_ged_with_preserved_segments = valid_infer
    prod.project_to_gec = valid_project
    prod.generate_with_evidence = valid_generate

    failure_map = {
        "S-B01-01_ZERO_GED_TOKEN": (
            "build_ged_segments", "GED_ZERO_TOKEN_WORD:1"
        ),
        "S-B01-02_ZERO_GEC_TOKEN": (
            "project_to_gec", "GEC_ZERO_TOKEN_WORD:1"
        ),
        "S-B01-04_WORD_OVER_BUDGET": (
            "build_ged_segments",
            "GED_SINGLE_WORD_OVER_BUDGET:0:4>3",
        ),
        "S-B01-07_DUPLICATE_WORD_INDEX": (
            "infer_ged_with_preserved_segments",
            "GED_DUPLICATE_WORD_INDEX:0",
        ),
        "S-B01-08_MISSING_WORD_INDEX": (
            "infer_ged_with_preserved_segments",
            "GED_WORD_COVERAGE_FAILED:[0]",
        ),
        "S-B01-09_REORDERED_WORDS": (
            "infer_ged_with_preserved_segments",
            "GED_WORD_IDENTITY_ORDER_OR_TEXT_MISMATCH",
        ),
        "S-B01-10_EQUAL_COUNTS_WRONG_IDENTITY": (
            "infer_ged_with_preserved_segments",
            "GED_WORD_IDENTITY_ORDER_OR_TEXT_MISMATCH",
        ),
        "S-B01-11_UNKNOWN_GED_LABEL": (
            "project_to_gec",
            "GEC_UNKNOWN_GED_LABEL:ERR",
        ),
        "S-B01-13_GEC_LENGTH_MISMATCH": (
            "project_to_gec",
            "GEC_CONDITIONING_LENGTH_MISMATCH",
        ),
        "S-B01-14B_GED_TAGS_IGNORED": (
            "generate_with_evidence",
            "GEC_GED_TAGS_NOT_CONSUMED_DURING_GENERATE",
        ),
        "S-B01-16_FORCED_EOS_AT_CEILING": (
            "generate_with_evidence",
            "GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED",
        ),
        "S-B01-EXTRA_MISSING_EOS": (
            "generate_with_evidence",
            "GEC_TERMINAL_EOS_UNPROVEN",
        ),
    }

    if case in failure_map:
        fn, message = failure_map[case]
        if fn == "infer_ged_with_preserved_segments":
            ged_ev = {
                "partial_ged_word_identity_trace": [{
                    "morph_word_index": 0,
                    "morph_word_text": "هذا",
                }],
                "partial_ged_logits_shapes": [[4, 2]],
                "partial_ged_word_labels_by_index": {"0": "UC"},
            }
            setattr(
                prod,
                fn,
                lambda *a, _m=message, _e=ged_ev, **k:
                    raise_error(_m, ged_evidence=_e),
            )
        elif fn == "generate_with_evidence":
            gen_ev = {
                "effective_generation_config": {
                    "decoder_start_token_id": 2,
                    "eos_token_id": 2,
                    "max_length": 100,
                },
                "generated_token_ids": [2, 20, 21, 2],
                "generation_token_count": 4,
                "terminal_eos_index": (
                    3 if "CEILING" in message else None
                ),
                "generation_hit_ceiling": (
                    True if "CEILING" in message else False
                ),
                "decoder_prefix_equals_eos": True,
                "ged_embedding_hook_calls": [{
                    "input_shape": [1, 4],
                    "output_shape": [1, 4, 16],
                }],
            }
            setattr(
                prod,
                fn,
                lambda *a, _m=message, _e=gen_ev, **k:
                    raise_error(_m, gen_evidence=_e),
            )
        else:
            setattr(
                prod,
                fn,
                lambda *a, _m=message, **k: raise_error(_m),
            )

    try:
        yield
    finally:
        for name, value in originals.items():
            setattr(prod, name, value)


def expected_failure_stage(case):
    if case in {
        "S-B01-01_ZERO_GED_TOKEN",
        "S-B01-04_WORD_OVER_BUDGET",
    }:
        return "GED_TOKENIZATION"
    if case in {
        "S-B01-07_DUPLICATE_WORD_INDEX",
        "S-B01-08_MISSING_WORD_INDEX",
        "S-B01-09_REORDERED_WORDS",
        "S-B01-10_EQUAL_COUNTS_WRONG_IDENTITY",
    }:
        return "GED_WORD_IDENTITY"
    if case == "S-B01-02_ZERO_GEC_TOKEN":
        return "GEC_TOKENIZATION"
    if case in {
        "S-B01-11_UNKNOWN_GED_LABEL",
        "S-B01-13_GEC_LENGTH_MISMATCH",
    }:
        return "GEC_PROJECTION"
    if case in {
        "S-B01-14B_GED_TAGS_IGNORED",
        "S-B01-16_FORCED_EOS_AT_CEILING",
        "S-B01-EXTRA_MISSING_EOS",
    }:
        return "GENERATION"
    return None


def adapter_routing_suite():
    legacy_cases = [
        "S-B01-01_ZERO_GED_TOKEN",
        "S-B01-02_ZERO_GEC_TOKEN",
        "S-B01-03_EXACT_GED_BUDGET",
        "S-B01-04_WORD_OVER_BUDGET",
        "S-B01-05_SEGMENT_EXACT_LIMIT",
        "S-B01-06_WHOLE_WORD_SEGMENT_SPLIT",
        "S-B01-07_DUPLICATE_WORD_INDEX",
        "S-B01-08_MISSING_WORD_INDEX",
        "S-B01-09_REORDERED_WORDS",
        "S-B01-10_EQUAL_COUNTS_WRONG_IDENTITY",
        "S-B01-11_UNKNOWN_GED_LABEL",
        "S-B01-12_NAME_BASED_LABEL_REMAP",
        "S-B01-13_GEC_LENGTH_MISMATCH",
        "S-B01-14_GED_TAGS_CONSUMED",
        "S-B01-14B_GED_TAGS_IGNORED",
        "S-B01-15_PREFIX_EOS_NOT_TERMINAL",
        "S-B01-16_FORCED_EOS_AT_CEILING",
        "S-B01-17_UID_WORD_IDENTITY_RECONSTRUCTION",
        "S-B01-18_REPEAT_BYTE_IDENTITY",
        "S-B01-EXTRA_MISSING_EOS",
    ]

    fake_models = (
        object(),
        object(),
        FakeGecTokenizer(),
        object(),
        object(),
        {"synthetic": True},
    )

    rows = []
    for case in legacy_cases:
        with patched_production(case):
            rec1 = prod.run_one(synthetic_row(case), fake_models)
            rec2 = (
                prod.run_one(synthetic_row(case), fake_models)
                if case == "S-B01-18_REPEAT_BYTE_IDENTITY"
                else None
            )

        exp = expected_failure_stage(case)
        if exp is None:
            ok = rec1["execution_state"] == "OK"
            if case == "S-B01-18_REPEAT_BYTE_IDENTITY":
                signature_keys = [
                    "execution_state",
                    "output_sha256",
                    "stage_status",
                    "morph_words",
                    "word_level_ged_labels",
                    "ged_word_identity_trace",
                    "gec_input_ids_sha256",
                    "gec_ged_label_ids_sha256",
                    "generated_token_ids",
                ]
                ok = ok and all(
                    rec1.get(k) == rec2.get(k)
                    for k in signature_keys
                )
        else:
            ok = (
                rec1["execution_state"] != "OK"
                and rec1["failure_stage"] == exp
                and rec1["stage_status"][exp] == "FAIL"
            )
            if exp == "GED_WORD_IDENTITY":
                ok = ok and (
                    rec1["partial_ged_word_identity_trace"]
                    is not None
                )
            if exp == "GENERATION":
                ok = ok and (
                    rec1["effective_generation_config"]
                    is not None
                )

        if not ok:
            raise RuntimeError(
                f"PRODUCTION_ADAPTER_B01_ROUTING_FAILED:{case}:"
                f"{rec1}"
            )
        rows.append({
            "case": case,
            "status": "PASS",
            "execution_state": rec1["execution_state"],
            "failure_stage": rec1["failure_stage"],
        })
    return rows


def source_free_real_model(models):
    sources = [
        "و قال له انه يحب اكل الطعام بكثره .",
        "هذه جمله بسيطه للاختبار .",
        "الجرعة 5 mg يوميا .",
    ]
    rows = []
    for i, source in enumerate(sources, start=1):
        row = {
            "uid": f"REAL-SYN:{i:02d}",
            "case_id": f"REAL-SYN-{i:02d}",
            "cluster_id": f"REAL-SYN-C-{i:02d}",
            "source": source,
            "source_sha256": sha_text(source),
        }
        rec = prod.run_one(row, models)
        if rec["execution_state"] != "OK":
            raise RuntimeError(
                f"REAL_MODEL_ADAPTER_FAILED:{row['uid']}:"
                f"{rec['execution_state']}:"
                f"{rec['failure_reasons']}"
            )
        if not all(rec["stage_status"][s] == "PASS" for s in prod.STAGES):
            raise RuntimeError(
                f"REAL_MODEL_STAGE_LEDGER_NOT_ALL_PASS:{row['uid']}"
            )
        if not rec["ged_embedding_hook_calls"]:
            raise RuntimeError(
                f"REAL_MODEL_GED_HOOK_UNPROVEN:{row['uid']}"
            )
        rows.append(rec)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # Exact existing B01 semantic suite.
    with contextlib.redirect_stdout(io.StringIO()):
        legacy = legacy_b01.self_test()
    if legacy["status"] != "PASS" or legacy["test_count"] != 20:
        raise RuntimeError(
            f"LEGACY_B01_REGRESSION_FAILED:{legacy['test_count']}"
        )

    # Same 20 named cases are routed through production adapter run_one().
    routing = adapter_routing_suite()
    if len(routing) != 20:
        raise RuntimeError("ADAPTER_B01_ROUTING_COUNT_MISMATCH")

    # Exact frozen real models/runtime are exercised through production run_one.
    models = prod.build_models(args)
    real_rows = source_free_real_model(models)

    result = {
        "record_id": VERSION,
        "status": "PASS",
        "adapter_version": prod.VERSION,
        "legacy_b01_semantic_tests": 20,
        "legacy_b01_semantic_pass": 20,
        "production_adapter_b01_routing_tests": 20,
        "production_adapter_b01_routing_pass": 20,
        "real_model_source_free_cases": 3,
        "real_model_source_free_pass": 3,
        "model_identities": models[-1],
        "routing_rows": routing,
        "real_model_rows": real_rows,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "quality_claimed": False,
    }
    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "record_id": VERSION,
        "status": "PASS",
        "adapter_version": prod.VERSION,
        "legacy_b01_semantic_pass": "20/20",
        "production_adapter_b01_routing_pass": "20/20",
        "real_model_source_free_pass": "3/3",
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
