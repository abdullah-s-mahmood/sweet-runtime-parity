from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SMOKE_SOURCE = (
    "A pilot sensor recorded 14 observations during a two-hour calibration window. "
    "The calibration was exploratory, and the observations do not establish improved accuracy."
)
SMOKE_PROMPT = f"""You are performing a mechanical smoke test for an academic revision harness.

Rewrite the paragraph for concise academic English while preserving the number 14, the two-hour duration, the exploratory status, and the statement that improved accuracy is NOT established. Do not add facts.

Return JSON only with exactly these keys.
The status value MUST be exactly one of these three strings: REVISE, KEEP, or REVIEW.
Do not copy the list or the | separator characters as the status value.
If status is REVISE, revised_paragraph must contain the revision. If status is KEEP or REVIEW, revised_paragraph may be null.
{{\"status\":\"REVISE\",\"revised_paragraph\":\"string or null\",\"uncertainty\":[]}}

SOURCE:
{SMOKE_SOURCE}"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def http_json(url: str, payload: dict | None = None, timeout: int = 20):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait_server(base_url: str, proc: subprocess.Popen, timeout_s: int = 120) -> None:
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
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if not isinstance(content, str):
        raise ValueError("NO_TEXT_CONTENT")
    return content.strip()


def parse_json_text(text: str) -> dict:
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("TOP_LEVEL_NOT_OBJECT")
    return obj


def validate_smoke(obj: dict) -> list[str]:
    errors = []
    if set(obj) != {"status", "revised_paragraph", "uncertainty"}:
        errors.append("SCHEMA_KEYS")
    if obj.get("status") not in {"REVISE", "KEEP", "REVIEW"}:
        errors.append("STATUS")
    if not isinstance(obj.get("uncertainty"), list):
        errors.append("UNCERTAINTY_TYPE")
    text = obj.get("revised_paragraph")
    if obj.get("status") == "REVISE":
        if not isinstance(text, str) or not text.strip():
            errors.append("MISSING_REWRITE")
        else:
            low = text.lower()
            if "14" not in text:
                errors.append("NUMBER_14_LOST")
            if not any(x in low for x in ["two-hour", "two hour", "2-hour", "2 hour"]):
                errors.append("DURATION_LOST")
            if "explor" not in low:
                errors.append("EXPLORATORY_LOST")
            if "improv" in low and not any(
                x in low for x in ["not", "no evidence", "does not", "cannot", "did not"]
            ):
                errors.append("NEGATION_RISK")
    return errors


def runtime_snapshot() -> dict:
    snap = {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
    }
    try:
        snap["memory"] = Path("/proc/meminfo").read_text(encoding="utf-8").splitlines()[:5]
    except Exception:
        snap["memory"] = None
    disk = shutil.disk_usage(str(ROOT))
    snap["disk"] = {"total": disk.total, "used": disk.used, "free": disk.free}
    return snap


def run_smoke(
    model_path: Path,
    model_key: str,
    expected_sha: str,
    llama_server: Path,
    out_dir: Path,
    ctx: int,
    seed: int,
):
    started = time.time()
    actual_sha = sha256_file(model_path)
    if actual_sha != expected_sha:
        raise RuntimeError(f"HASH_MISMATCH expected={expected_sha} actual={actual_sha}")

    port = 18080
    log_path = out_dir / f"{model_key}_server.log"
    with log_path.open("wb") as log:
        cmd = [
            str(llama_server),
            "-m",
            str(model_path),
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "-c",
            str(ctx),
            "-np",
            "1",
            "--seed",
            str(seed),
            "--jinja",
        ]
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        try:
            wait_server(f"http://127.0.0.1:{port}", proc)
            messages = [{"role": "user", "content": SMOKE_PROMPT}]
            if model_key.startswith("SMOLLM3"):
                # SmolLM3 enables extended thinking by default. The model's
                # documented /no_think control prevents the fixed output cap
                # from being consumed by hidden reasoning during this bounded
                # structured-output feasibility test.
                messages = [
                    {"role": "system", "content": "/no_think"},
                    {"role": "user", "content": SMOKE_PROMPT},
                ]
            payload = {
                "model": model_key,
                "messages": messages,
                "temperature": 0.0,
                "seed": seed,
                "max_tokens": 400,
                "stream": False,
            }
            t0 = time.time()
            raw = http_json(
                f"http://127.0.0.1:{port}/v1/chat/completions",
                payload,
                timeout=180,
            )
            latency = time.time() - t0
            text = extract_content(raw)
            parsed = None
            parse_error = None
            try:
                parsed = parse_json_text(text)
            except Exception as exc:
                parse_error = f"{type(exc).__name__}: {exc}"
            errs = ["PARSE_ERROR"] if parse_error else validate_smoke(parsed)
            status = "PASS" if not errs else "FAIL"
            result = {
                "model_key": model_key,
                "status": status,
                "artifact_path": str(model_path),
                "artifact_sha256": actual_sha,
                "prompt_sha256": hashlib.sha256(SMOKE_PROMPT.encode()).hexdigest(),
                "raw_text": text,
                "parsed": parsed,
                "parse_error": parse_error,
                "validation_errors": errs,
                "latency_seconds": latency,
                "usage": raw.get("usage"),
                "server_response_model": raw.get("model"),
                "wall_seconds_total": time.time() - started,
            }
            write_json(out_dir / f"{model_key}_smoke.json", result)
            return result
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["smoke"], default="smoke")
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--model-key", required=True)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--llama-server", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--context", type=int, default=4096)
    ap.add_argument("--seed", type=int, default=20261003)
    args = ap.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / f"{args.model_key}_runtime_before.json", runtime_snapshot())
    result = run_smoke(
        Path(args.model_path),
        args.model_key,
        args.expected_sha256,
        Path(args.llama_server),
        out,
        args.context,
        args.seed,
    )
    write_json(out / f"{args.model_key}_runtime_after.json", runtime_snapshot())
    print(
        json.dumps(
            {
                "model_key": args.model_key,
                "status": result["status"],
                "errors": result["validation_errors"],
            }
        )
    )
    if result["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
