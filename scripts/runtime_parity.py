from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
import transformers
from huggingface_hub import snapshot_download
from transformers import BertForTokenClassification, BertTokenizer

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
MODELS = ROOT / "models"
UPSTREAM = ROOT / "upstream" / "text-editing"

ART.mkdir(parents=True, exist_ok=True)
MODELS.mkdir(parents=True, exist_ok=True)

EXPECTED = {
    "nopnx": {
        "sha256": "584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6",
        "weight_size": 539450353,
        "labels": 315,
        "candidates": [
            "CAMeL-Lab/text-editing-zaebuc-nopnx",
            "CAMeL-Lab/text-editing-qalb14-zaebuc-nopnx",
        ],
    },
    "pnx": {
        "sha256": "195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3",
        "weight_size": 538638321,
        "labels": 51,
        "candidates": [
            "CAMeL-Lab/text-editing-zaebuc-pnx",
            "CAMeL-Lab/text-editing-qalb14-zaebuc-pnx",
        ],
    },
}

ALLOW = [
    "config.json",
    "pytorch_model.bin",
    "special_tokens_map.json",
    "tokenizer_config.json",
    "vocab.txt",
]

DEMO_INPUT = "يجب الإهتمام ب الصحه و لا سيما ف ي الصحه النفسيه ياشباب المستقبل،،"
PREVIOUS_NUMPY_NOPNX = "يجب الاهتمام بالصحة ولا سيما في الصحة النفسية يا شباب المستقبل ،"
PREVIOUS_NUMPY_FINAL = "يجب الاهتمام بالصحة ولا سيما في الصحة النفسية يا شباب المستقبل ."
PUBLIC_DEMO_FINAL = "يجب الاهتمام بالصحة ولا سيما في الصحة النفسية يا شباب المستقبل ."

# Small development-only punctuation probes. They are not a benchmark.
PNX_SANITY = [
    "هذه جملة بدون نقطة",
    "هذه جملة ، بسيطة",
    "هذه جملة، بسيطة",
    "هل هذا صحيح",
    "هل هذا صحيح ؟",
    "هذا صحيح ؛ ولكن هذا مثال",
]


def dump_json(name: str, obj) -> None:
    (ART / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(8 * 1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def git_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def download_model(kind: str) -> tuple[Path, str]:
    target = MODELS / kind
    target.mkdir(parents=True, exist_ok=True)
    errors = []
    for repo_id in EXPECTED[kind]["candidates"]:
        try:
            print(f"[{kind}] downloading from {repo_id}", flush=True)
            snapshot_download(
                repo_id=repo_id,
                local_dir=str(target),
                allow_patterns=ALLOW,
            )
            weight = target / "pytorch_model.bin"
            if weight.exists():
                return target, repo_id
            errors.append(f"{repo_id}: no pytorch_model.bin after snapshot_download")
        except Exception as exc:
            errors.append(f"{repo_id}: {type(exc).__name__}: {exc}")
            print(errors[-1], flush=True)

    raise RuntimeError(
        f"Could not download {kind}. Attempts:\n" + "\n".join(errors)
    )


def verify_model_artifacts(kind: str, model_dir: Path, repo_id: str) -> dict:
    files = {}
    for name in ALLOW:
        p = model_dir / name
        files[name] = {
            "exists": p.exists(),
            "size": p.stat().st_size if p.exists() else None,
            "sha256": sha256(p) if p.exists() else None,
        }

    weight = model_dir / "pytorch_model.bin"
    if not weight.exists():
        raise FileNotFoundError(weight)

    actual_hash = sha256(weight)
    actual_size = weight.stat().st_size
    hash_match = actual_hash == EXPECTED[kind]["sha256"]
    size_match = actual_size == EXPECTED[kind]["weight_size"]

    result = {
        "kind": kind,
        "resolved_repo_id": repo_id,
        "files": files,
        "weight_sha256": actual_hash,
        "expected_weight_sha256": EXPECTED[kind]["sha256"],
        "hash_match": hash_match,
        "weight_size": actual_size,
        "expected_weight_size": EXPECTED[kind]["weight_size"],
        "size_match": size_match,
    }
    dump_json(f"{kind}_artifact_verification.json", result)

    if not hash_match:
        raise RuntimeError(
            f"{kind} hash mismatch: {actual_hash} != {EXPECTED[kind]['sha256']}"
        )
    if not size_match:
        raise RuntimeError(
            f"{kind} size mismatch: {actual_size} != {EXPECTED[kind]['weight_size']}"
        )
    return result


def load_official(kind: str, model_dir: Path):
    tokenizer = BertTokenizer.from_pretrained(str(model_dir), local_files_only=True)
    model = BertForTokenClassification.from_pretrained(
        str(model_dir), local_files_only=True
    )
    model.eval()

    label_count = len(model.config.id2label)
    if label_count != EXPECTED[kind]["labels"]:
        raise RuntimeError(
            f"{kind} label mismatch: {label_count} != {EXPECTED[kind]['labels']}"
        )

    classifier_shape = list(model.classifier.weight.shape)
    expected_classifier = [EXPECTED[kind]["labels"], 768]
    if classifier_shape != expected_classifier:
        raise RuntimeError(
            f"{kind} classifier mismatch: {classifier_shape} != {expected_classifier}"
        )

    structure = {
        "label_count": label_count,
        "hidden_size": model.config.hidden_size,
        "num_hidden_layers": model.config.num_hidden_layers,
        "num_attention_heads": model.config.num_attention_heads,
        "vocab_size": model.config.vocab_size,
        "classifier_weight_shape": classifier_shape,
        "classifier_bias_shape": list(model.classifier.bias.shape),
        "model_class": type(model).__name__,
        "tokenizer_class": type(tokenizer).__name__,
    }
    dump_json(f"{kind}_structure.json", structure)
    return tokenizer, model, structure


def load_official_rewrite():
    if not UPSTREAM.exists():
        raise RuntimeError(f"Missing upstream repository: {UPSTREAM}")
    sys.path.insert(0, str(UPSTREAM))
    from gec.tag import rewrite  # noqa: E402

    return rewrite


def predict_iterations(
    model,
    tokenizer,
    rewrite,
    words: list[str],
    decode_iter: int,
    label: str,
) -> tuple[str, list[dict]]:
    current_words = list(words)
    traces = []

    for iteration in range(1, decode_iter + 1):
        t0 = time.perf_counter()
        tokenized = tokenizer(
            current_words,
            return_tensors="pt",
            is_split_into_words=True,
        )
        with torch.no_grad():
            logits = model(**tokenized).logits[0]
            probs = F.softmax(logits, dim=-1)
            confidence, pred_ids = torch.max(probs, dim=-1)

        pred_ids_np = pred_ids.cpu().numpy()
        edits = [model.config.id2label[int(p)] for p in pred_ids_np[1:-1]]
        conf = [float(x) for x in confidence[1:-1].cpu().tolist()]
        ids = tokenized["input_ids"][0][1:-1].cpu().tolist()
        subwords = tokenizer.convert_ids_to_tokens(ids)

        if len(edits) != len(subwords):
            raise RuntimeError(
                f"{label} iteration {iteration}: edit/subword length mismatch "
                f"{len(edits)} != {len(subwords)}"
            )

        rewritten = rewrite(subwords=[subwords], edits=[edits])
        output_text = rewritten[0][0]
        elapsed = time.perf_counter() - t0

        traces.append(
            {
                "stage": label,
                "iteration": iteration,
                "input_words": current_words,
                "input_ids_without_special_tokens": ids,
                "subwords": subwords,
                "predicted_label_ids_without_special_tokens": [
                    int(x) for x in pred_ids_np[1:-1].tolist()
                ],
                "raw_edit_labels": edits,
                "argmax_confidence": conf,
                "non_keep_label_count": sum(1 for e in edits if e != "K*"),
                "output_text": output_text,
                "runtime_seconds": elapsed,
                "non_applicable_edits": rewritten[2],
            }
        )

        current_words = output_text.split()

    return " ".join(current_words), traces


def run_pnx_once(model, tokenizer, rewrite, text: str, case_id: str) -> dict:
    output, traces = predict_iterations(
        model, tokenizer, rewrite, text.split(), 1, f"pnx:{case_id}"
    )
    t = traces[0]
    return {
        "case_id": case_id,
        "source": text,
        "raw_edit_labels": t["raw_edit_labels"],
        "non_keep_label_count": t["non_keep_label_count"],
        "output": output,
        "text_changed": output != text,
        "changed_with_all_keep_labels": (
            output != text and t["non_keep_label_count"] == 0
        ),
        "trace": t,
    }


def main() -> None:
    runtime = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "numpy": np.__version__,
        "upstream_text_editing_commit": git_sha(UPSTREAM),
        "cuda_available": torch.cuda.is_available(),
    }
    dump_json("runtime_versions.json", runtime)

    rewrite = load_official_rewrite()

    dirs = {}
    resolved = {}
    verification = {}
    loaded = {}

    for kind in ("nopnx", "pnx"):
        model_dir, repo_id = download_model(kind)
        dirs[kind] = model_dir
        resolved[kind] = repo_id
        verification[kind] = verify_model_artifacts(kind, model_dir, repo_id)
        tokenizer, model, structure = load_official(kind, model_dir)
        loaded[kind] = (tokenizer, model)

    nopnx_tokenizer, nopnx_model = loaded["nopnx"]
    pnx_tokenizer, pnx_model = loaded["pnx"]

    nopnx_output, nopnx_traces = predict_iterations(
        nopnx_model,
        nopnx_tokenizer,
        rewrite,
        DEMO_INPUT.split(),
        2,
        "nopnx",
    )

    pnx_output, pnx_traces = predict_iterations(
        pnx_model,
        pnx_tokenizer,
        rewrite,
        nopnx_output.split(),
        1,
        "pnx",
    )

    full = {
        "input": DEMO_INPUT,
        "nopnx_iteration_1": nopnx_traces[0]["output_text"],
        "nopnx_iteration_2": nopnx_traces[1]["output_text"],
        "pnx_iteration_1": pnx_traces[0]["output_text"],
        "final": pnx_output,
        "previous_numpy_nopnx": PREVIOUS_NUMPY_NOPNX,
        "previous_numpy_final": PREVIOUS_NUMPY_FINAL,
        "public_demo_final": PUBLIC_DEMO_FINAL,
        "nopnx_matches_previous_numpy": nopnx_output == PREVIOUS_NUMPY_NOPNX,
        "final_matches_previous_numpy": pnx_output == PREVIOUS_NUMPY_FINAL,
        "final_matches_public_demo": pnx_output == PUBLIC_DEMO_FINAL,
        "nopnx_traces": nopnx_traces,
        "pnx_traces": pnx_traces,
    }
    dump_json("full_pipeline.json", full)

    sanity = [
        run_pnx_once(
            pnx_model,
            pnx_tokenizer,
            rewrite,
            text,
            f"sanity_{i:02d}",
        )
        for i, text in enumerate(PNX_SANITY, 1)
    ]
    dump_json("pnx_sanity.json", sanity)

    spacing_side_effect_cases = [
        x["case_id"] for x in sanity if x["changed_with_all_keep_labels"]
    ]

    parity = {
        "nopnx_weight_hash_match": verification["nopnx"]["hash_match"],
        "pnx_weight_hash_match": verification["pnx"]["hash_match"],
        "nopnx_matches_previous_numpy": full["nopnx_matches_previous_numpy"],
        "final_matches_previous_numpy": full["final_matches_previous_numpy"],
        "final_matches_public_demo": full["final_matches_public_demo"],
        "pnx_sanity_changed_with_all_keep_labels": spacing_side_effect_cases,
        "official_runtime_executed": True,
        "official_rewrite_source": "CAMeL-Lab/text-editing gec.tag.rewrite",
        "official_rewrite_commit": runtime["upstream_text_editing_commit"],
    }

    parity["reference_runtime_parity_pass"] = bool(
        parity["nopnx_weight_hash_match"]
        and parity["pnx_weight_hash_match"]
        and parity["nopnx_matches_previous_numpy"]
        and parity["final_matches_previous_numpy"]
        and parity["final_matches_public_demo"]
    )

    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    parity["process_max_rss_kb_linux"] = int(max_rss)

    dump_json("parity_result.json", parity)

    report_lines = [
        "# SWEET Official Runtime Parity Result",
        "",
        f"- NoPnx weight hash match: {parity['nopnx_weight_hash_match']}",
        f"- Pnx weight hash match: {parity['pnx_weight_hash_match']}",
        f"- NoPnx output matches prior NumPy/SciPy result: {parity['nopnx_matches_previous_numpy']}",
        f"- Final output matches prior NumPy/SciPy result: {parity['final_matches_previous_numpy']}",
        f"- Final output matches public model-card demo: {parity['final_matches_public_demo']}",
        f"- Pnx sanity cases changed despite all-K* labels: {spacing_side_effect_cases}",
        f"- Upstream rewrite commit: {runtime['upstream_text_editing_commit']}",
        "",
        "OFFICIAL_REFERENCE_RUNTIME_PARITY: "
        + ("PASS" if parity["reference_runtime_parity_pass"] else "FAIL"),
    ]
    (ART / "PARITY_REPORT.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print("\n".join(report_lines), flush=True)

    if not parity["reference_runtime_parity_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except BaseException as exc:
        failure = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        dump_json("failure.json", failure)
        raise
