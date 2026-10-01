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

    now_ts = time.time()
    started_ts = datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp()
    prev_heartbeat_ts = None
    if old.get("heartbeat_at"):
        try:
            prev_heartbeat_ts = datetime.fromisoformat(old["heartbeat_at"].replace("Z", "+00:00")).timestamp()
        except Exception:
            prev_heartbeat_ts = None

    if processed > prev_processed:
        last_progress_at = now

    pct = 0.0 if total <= 0 else min(100.0, max(0.0, processed * 100.0 / total))
    elapsed = max(0.001, now_ts - started_ts)
    overall_rate_per_min = processed / elapsed * 60.0 if processed > 0 else 0.0

    recent_rate_per_min = None
    if prev_heartbeat_ts is not None and processed > prev_processed:
        dt = max(0.001, now_ts - prev_heartbeat_ts)
        recent_rate_per_min = (processed - prev_processed) / dt * 60.0

    prev_ewma = old.get("ewma_rate_per_min")
    if recent_rate_per_min is not None:
        alpha = 0.35
        ewma_rate_per_min = (
            recent_rate_per_min
            if not isinstance(prev_ewma, (int, float)) or prev_ewma <= 0
            else alpha * recent_rate_per_min + (1.0 - alpha) * float(prev_ewma)
        )
    elif isinstance(prev_ewma, (int, float)) and prev_ewma > 0:
        ewma_rate_per_min = float(prev_ewma)
    else:
        ewma_rate_per_min = overall_rate_per_min

    # Blend long-run stability with recent behavior. Early estimates favor
    # overall rate; after enough progress, recent EWMA gets more weight.
    if overall_rate_per_min > 0 and ewma_rate_per_min > 0:
        recent_weight = min(0.75, max(0.25, processed / max(total, 1)))
        estimated_rate_per_min = (
            recent_weight * ewma_rate_per_min
            + (1.0 - recent_weight) * overall_rate_per_min
        )
    else:
        estimated_rate_per_min = max(overall_rate_per_min, ewma_rate_per_min, 0.0)

    eta_seconds = None
    estimated_finish_at = None
    eta_confidence = "UNAVAILABLE"
    if total > processed and estimated_rate_per_min > 0:
        eta_seconds = (total - processed) / estimated_rate_per_min * 60.0
        finish_ts = now_ts + eta_seconds
        estimated_finish_at = datetime.fromtimestamp(
            finish_ts, tz=timezone.utc
        ).isoformat().replace("+00:00", "Z")

        progress_fraction = processed / max(total, 1)
        if processed >= 100 and progress_fraction >= 0.25:
            eta_confidence = "MEDIUM"
        if processed >= 500 and progress_fraction >= 0.50:
            eta_confidence = "HIGH"
        elif processed >= 20:
            eta_confidence = "LOW"
    elif total <= processed and total > 0:
        eta_seconds = 0.0
        estimated_finish_at = now
        eta_confidence = "COMPLETE"

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
        "rate_per_min": round(estimated_rate_per_min, 4),
        "overall_rate_per_min": round(overall_rate_per_min, 4),
        "recent_rate_per_min": None if recent_rate_per_min is None else round(recent_rate_per_min, 4),
        "ewma_rate_per_min": round(ewma_rate_per_min, 4),
        "eta_seconds": None if eta_seconds is None else round(eta_seconds, 1),
        "estimated_finish_at_utc": estimated_finish_at,
        "eta_confidence": eta_confidence,
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
