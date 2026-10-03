from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)

def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    os.replace(tmp, path)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_cases():
    return [json.loads(x) for x in (ROOT / "cases.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]

def build_context(case: dict) -> dict:
    return {
        "case_id": case["case_id"],
        "mode": case["mode"],
        "source_text": case["source_text"],
        "revision_need": case["revision_need"],
        "protected_challenge": case["protected_challenge"],
        "content_units": [{"id": f"CU{i+1}", "text": x} for i, x in enumerate(case["content_units"])],
        "protected_spans": case.get("protected_spans", []),
        "adjacent_context": case.get("adjacent_context"),
        "authorized_scope": {
            "source_sha256": case["source_sha256"],
            "scope": "TARGET_PARAGRAPH_ONLY",
            "immutable_adjacent_context": True,
        },
        "length_policy": {"soft_min_ratio": 0.85, "soft_max_ratio": 1.15},
        "required_output": {
            "status": "REVISE|KEEP|REVIEW",
            "revised_paragraph": "string|null",
            "content_unit_mapping": "array",
            "protected_status": "array",
            "uncertainty": "array",
        },
    }

def build_prompt(case: dict, stage: str, plan: dict | None = None) -> str:
    text = (ROOT / "prompts" / f"{stage}.md").read_text(encoding="utf-8")
    text += "\n\nINPUT\n" + json.dumps(build_context(case), ensure_ascii=False, indent=2)
    if stage == "PLAN":
        text += '\n\nReturn JSON only: {"status":"PLAN|REVIEW","operations":[],"uncertainty":[]}'
    if stage == "REALIZE":
        text += "\n\nPLAN\n" + json.dumps(plan or {}, ensure_ascii=False, indent=2)
    return text

def parse_json_text(text: str) -> dict:
    s = text.strip()
    if s.startswith("~~~"):
        parts = s.split("\n", 1)
        if len(parts) == 2 and "~~~" in parts[1]:
            s = parts[1].rsplit("~~~", 1)[0].strip()
    elif s.startswith("```"):
        parts = s.split("\n", 1)
        if len(parts) == 2 and "```" in parts[1]:
            s = parts[1].rsplit("```", 1)[0].strip()
    try:
        obj = json.loads(s)
    except Exception:
        start, end = s.find("{"), s.rfind("}")
        if start < 0 or end <= start:
            raise
        obj = json.loads(s[start:end+1])
    if not isinstance(obj, dict):
        raise ValueError("TOP_LEVEL_NOT_OBJECT")
    return obj

def http_json(url: str, payload: dict | None = None, timeout: int = 30):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def wait_server(base_url: str, proc: subprocess.Popen, timeout_s: int = 120):
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"llama-server exited early rc={proc.returncode}")
        try:
            http_json(base_url + "/health", timeout=3)
            return
        except Exception as exc:
            last = exc
            time.sleep(1)
    raise RuntimeError(f"llama-server health timeout: {last}")

def extract_content(response: dict) -> str:
    choices = response.get("choices") or []
    if not choices:
        raise ValueError("NO_CHOICES")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("NO_TEXT_CONTENT")
    return content.strip()

def runtime_snapshot() -> dict:
    disk = shutil.disk_usage(str(ROOT))
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "disk": {"total": disk.total, "used": disk.used, "free": disk.free},
    }

def validate_plan(obj: dict) -> list[str]:
    errors = []
    if obj.get("status") not in {"PLAN", "REVIEW"}:
        errors.append("PLAN_STATUS")
    if not isinstance(obj.get("operations"), list):
        errors.append("PLAN_OPERATIONS_TYPE")
    if not isinstance(obj.get("uncertainty"), list):
        errors.append("PLAN_UNCERTAINTY_TYPE")
    return errors

def validate_output(obj: dict) -> list[str]:
    errors = []
    required = {"status", "revised_paragraph", "content_unit_mapping", "protected_status", "uncertainty"}
    if not required.issubset(obj):
        errors.append("OUTPUT_REQUIRED_KEYS")
    status = obj.get("status")
    if status not in {"REVISE", "KEEP", "REVIEW"}:
        errors.append("OUTPUT_STATUS")
    if status == "REVISE" and (not isinstance(obj.get("revised_paragraph"), str) or not obj.get("revised_paragraph", "").strip()):
        errors.append("OUTPUT_REWRITE_REQUIRED")
    if status in {"KEEP", "REVIEW"} and obj.get("revised_paragraph") is not None and not isinstance(obj.get("revised_paragraph"), str):
        errors.append("OUTPUT_REWRITE_TYPE")
    if not isinstance(obj.get("content_unit_mapping"), list):
        errors.append("OUTPUT_CONTENT_UNIT_MAPPING_TYPE")
    if not isinstance(obj.get("protected_status"), list):
        errors.append("OUTPUT_PROTECTED_STATUS_TYPE")
    if not isinstance(obj.get("uncertainty"), list):
        errors.append("OUTPUT_UNCERTAINTY_TYPE")
    return errors

def request_messages(model_slot: str, prompt: str):
    if model_slot == "MODEL_B":
        return [
            {"role": "system", "content": "/no_think"},
            {"role": "user", "content": prompt},
        ]
    return [{"role": "user", "content": prompt}]

def generate(base_url: str, model_slot: str, prompt: str, max_tokens: int, seed: int):
    payload = {
        "model": model_slot,
        "messages": request_messages(model_slot, prompt),
        "temperature": 0.0,
        "seed": seed,
        "max_tokens": max_tokens,
        "stream": False,
    }
    started = time.time()
    raw = http_json(base_url + "/v1/chat/completions", payload, timeout=600)
    elapsed = time.time() - started
    text = extract_content(raw)
    return text, {
        "elapsed_seconds": round(elapsed, 3),
        "usage": raw.get("usage"),
        "server_response_model": raw.get("model"),
    }

def init_or_load_slots(out: Path, cases: list[dict], models: list[dict]):
    path = out / "slots.jsonl"
    if path.exists():
        return read_jsonl(path)
    rows = []
    for model in models:
        for case in cases:
            for arm in ("DIRECT", "PLANNED"):
                rows.append({
                    "slot_id": f"{model['slot']}-{case['case_id']}-{arm}",
                    "model_slot": model["slot"],
                    "case_id": case["case_id"],
                    "arm": arm,
                    "status": "NOT_RUN",
                    "logical_calls": 0,
                })
    write_jsonl(path, rows)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llama-server", required=True)
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--model-slot", choices=["MODEL_A", "MODEL_B"], required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    cfg = read_json(ROOT / "config.json")
    manifest = read_json(ROOT / "MODEL_MANIFEST.json")
    cases = load_cases()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    assert cfg["schema_version"] == "2.1.0"
    assert len(cases) == 12
    assert len(manifest["models"]) == 2
    assert cfg["live_slots"] == 48
    assert cfg["max_logical_calls"] == 72
    assert cfg["execution_concurrency"] == 1
    assert float(cfg["authorized_cost_ceiling"]) == 0.0

    model = next(x for x in manifest["models"] if x["slot"] == args.model_slot)
    model_path = Path(args.model_path)
    actual_hash = sha256_file(model_path)
    if actual_hash != model["artifact_sha256"]:
        raise RuntimeError(f"HASH_MISMATCH expected={model['artifact_sha256']} actual={actual_hash}")

    slots = init_or_load_slots(out, cases, manifest["models"])
    requests = read_jsonl(out / "requests.jsonl")
    responses = read_jsonl(out / "responses.jsonl")
    total_calls_before = sum(int(x.get("logical_calls", 0)) for x in slots)

    identity_path = out / "identity.json"
    if not identity_path.exists():
        write_json(identity_path, {
            "config_sha256": sha256_file(ROOT / "config.json"),
            "model_manifest_sha256": sha256_file(ROOT / "MODEL_MANIFEST.json"),
            "cases_sha256": sha256_file(ROOT / "cases.jsonl"),
            "model_artifacts": {m["slot"]: m["artifact_sha256"] for m in manifest["models"]},
            "github_sha": os.getenv("GITHUB_SHA"),
            "github_run_id": os.getenv("GITHUB_RUN_ID"),
        })

    server_log = out / f"{args.model_slot}_server.log"
    port = 18080
    with server_log.open("wb") as log:
        cmd = [
            str(Path(args.llama_server)),
            "-m", str(model_path),
            "--host", "127.0.0.1",
            "--port", str(port),
            "-c", str(cfg["generation"]["context_tokens_min"]),
            "-np", "1",
            "--seed", str(cfg["generation"]["seed"]),
            "--jinja",
        ]
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        try:
            wait_server(f"http://127.0.0.1:{port}", proc)
            write_json(out / f"{args.model_slot}_runtime_before.json", runtime_snapshot())

            for case in cases:
                for arm in ("DIRECT", "PLANNED"):
                    slot_id = f"{args.model_slot}-{case['case_id']}-{arm}"
                    row = next(x for x in slots if x["slot_id"] == slot_id)
                    if row["status"] != "NOT_RUN":
                        raise RuntimeError(f"REFUSE_RERUN_EXISTING_SLOT:{slot_id}")

                    try:
                        if arm == "DIRECT":
                            stage_specs = [("DIRECT", build_prompt(case, "DIRECT"), cfg["per_request_max_output_tokens"]["DIRECT"])]
                        else:
                            plan_prompt = build_prompt(case, "PLAN")
                            requests.append({"slot_id": slot_id, "stage": "PLAN", "prompt": plan_prompt, "prompt_sha256": sha256_text(plan_prompt)})
                            row["logical_calls"] = 1
                            write_jsonl(out / "requests.jsonl", requests)
                            write_jsonl(out / "slots.jsonl", slots)
                            plan_text, meta = generate(
                                f"http://127.0.0.1:{port}",
                                args.model_slot,
                                plan_prompt,
                                cfg["per_request_max_output_tokens"]["PLAN"],
                                cfg["generation"]["seed"],
                            )
                            responses.append({"slot_id": slot_id, "stage": "PLAN", "raw": plan_text, "runtime": meta})
                            write_jsonl(out / "requests.jsonl", requests)
                            write_jsonl(out / "responses.jsonl", responses)
                            write_jsonl(out / "slots.jsonl", slots)

                            try:
                                plan = parse_json_text(plan_text)
                            except Exception as exc:
                                row.update(status="FAILED_PARSE_PLAN", error=f"{type(exc).__name__}:{exc}")
                                write_jsonl(out / "slots.jsonl", slots)
                                continue
                            plan_errors = validate_plan(plan)
                            if plan_errors:
                                row.update(status="FAILED_SCHEMA_PLAN", schema_errors=plan_errors)
                                write_jsonl(out / "slots.jsonl", slots)
                                continue
                            if plan.get("status") != "PLAN":
                                row.update(status="PLAN_REVIEW", plan_status=plan.get("status"))
                                write_jsonl(out / "slots.jsonl", slots)
                                continue
                            stage_specs = [("REALIZE", build_prompt(case, "REALIZE", plan), cfg["per_request_max_output_tokens"]["REALIZE"])]

                        for stage, stage_prompt, max_tokens in stage_specs:
                            requests.append({"slot_id": slot_id, "stage": stage, "prompt": stage_prompt, "prompt_sha256": sha256_text(stage_prompt)})
                            row["logical_calls"] = 1 if arm == "DIRECT" else 2
                            write_jsonl(out / "requests.jsonl", requests)
                            write_jsonl(out / "slots.jsonl", slots)
                            text, meta = generate(
                                f"http://127.0.0.1:{port}",
                                args.model_slot,
                                stage_prompt,
                                max_tokens,
                                cfg["generation"]["seed"],
                            )
                            responses.append({"slot_id": slot_id, "stage": stage, "raw": text, "runtime": meta})
                            try:
                                parsed = parse_json_text(text)
                                schema_errors = validate_output(parsed)
                                row["output_status"] = parsed.get("status")
                                row["parsed_output"] = parsed
                                if schema_errors:
                                    row.update(status="FAILED_SCHEMA_OUTPUT", schema_errors=schema_errors)
                                else:
                                    row["status"] = "COMPLETE_RAW"
                            except Exception as exc:
                                row.update(status="FAILED_PARSE_OUTPUT", error=f"{type(exc).__name__}:{exc}")

                        write_jsonl(out / "requests.jsonl", requests)
                        write_jsonl(out / "responses.jsonl", responses)
                        write_jsonl(out / "slots.jsonl", slots)

                        calls_now = sum(int(x.get("logical_calls", 0)) for x in slots)
                        if calls_now > cfg["max_logical_calls"]:
                            raise RuntimeError("CALL_CEILING")
                    except (RuntimeError, subprocess.TimeoutExpired, urllib.error.URLError) as exc:
                        row.update(status="FAILED_RUNTIME", error=f"{type(exc).__name__}:{exc}")
                        write_jsonl(out / "slots.jsonl", slots)
                        write_jsonl(out / "requests.jsonl", requests)
                        write_jsonl(out / "responses.jsonl", responses)
                        raise

            write_json(out / f"{args.model_slot}_runtime_after.json", runtime_snapshot())
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

    total_calls_after = sum(int(x.get("logical_calls", 0)) for x in slots)
    summary = {
        "model_slot": args.model_slot,
        "new_logical_calls": total_calls_after - total_calls_before,
        "total_logical_calls_recorded": total_calls_after,
        "model_slots_complete_raw": sum(x["model_slot"] == args.model_slot and x["status"] == "COMPLETE_RAW" for x in slots),
        "model_slots_plan_review": sum(x["model_slot"] == args.model_slot and x["status"] == "PLAN_REVIEW" for x in slots),
        "model_slots_failed_parse": sum(x["model_slot"] == args.model_slot and x["status"].startswith("FAILED_PARSE") for x in slots),
        "additional_monetary_cost_usd": 0.0,
    }
    write_json(out / f"{args.model_slot}_backend_summary.json", summary)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
