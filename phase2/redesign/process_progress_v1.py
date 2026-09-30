#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def atomic_write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def update_state(path: Path, process_id: str, stage: str, processed: int, total: int,
                 status: str = "RUNNING", message: str | None = None,
                 started_at: str | None = None):
    old = {}
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            old = {}

    now = utc_now()
    started = started_at or old.get("started_at") or now
    prev_processed = int(old.get("processed", 0) or 0)
    last_progress_at = old.get("last_progress_at") or started
    if processed > prev_processed:
        last_progress_at = now

    pct = 0.0 if total <= 0 else min(100.0, max(0.0, processed * 100.0 / total))
    elapsed = max(0.001, time.time() - datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp())
    rate_per_min = processed / elapsed * 60.0 if processed > 0 else 0.0
    eta_seconds = None
    if total > processed and rate_per_min > 0:
        eta_seconds = (total - processed) / rate_per_min * 60.0

    payload = {
        "schema": "ACAD_PASS_PROCESS_PROGRESS_V1",
        "process_id": process_id,
        "status": status,
        "stage": stage,
        "processed": int(processed),
        "total": int(total),
        "percent": round(pct, 4),
        "started_at": started,
        "heartbeat_at": now,
        "last_progress_at": last_progress_at,
        "rate_per_min": round(rate_per_min, 4),
        "eta_seconds": None if eta_seconds is None else round(eta_seconds, 1),
        "message": message,
    }
    atomic_write_json(path, payload)
    return payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-file", required=True)
    ap.add_argument("--process-id", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--processed", type=int, required=True)
    ap.add_argument("--total", type=int, required=True)
    ap.add_argument("--status", default="RUNNING")
    ap.add_argument("--message")
    args = ap.parse_args()
    payload = update_state(
        Path(args.state_file), args.process_id, args.stage,
        args.processed, args.total, args.status, args.message
    )
    print("PROGRESS_STATE " + json.dumps(payload, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
