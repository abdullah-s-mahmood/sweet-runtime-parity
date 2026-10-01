#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def parse_time(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()

def load_state(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def publish_status(state_name, description, context, target_url=None):
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    sha = os.environ.get("GITHUB_SHA")
    if not token or not repo or not sha:
        return False
    payload = {
        "state": state_name,
        "context": context[:100],
        "description": description[:140],
    }
    if target_url:
        payload["target_url"] = target_url
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/statuses/{sha}",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()
        return True
    except Exception as e:
        print(f"WATCHDOG_STATUS_PUBLISH_FAILED {type(e).__name__}: {e}", flush=True)
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-file", required=True)
    ap.add_argument("--context", required=True)
    ap.add_argument("--poll-seconds", type=int, default=20)
    ap.add_argument("--publish-seconds", type=int, default=60)
    ap.add_argument("--stale-seconds", type=int, default=600)
    ap.add_argument("--kill-on-stale", action="store_true")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    if not args.command:
        raise SystemExit("No child command supplied")
    cmd = args.command[1:] if args.command and args.command[0] == "--" else args.command
    state_path = Path(args.state_file)
    target_url = None
    if os.environ.get("GITHUB_SERVER_URL") and os.environ.get("GITHUB_REPOSITORY") and os.environ.get("GITHUB_RUN_ID"):
        target_url = f'{os.environ["GITHUB_SERVER_URL"]}/{os.environ["GITHUB_REPOSITORY"]}/actions/runs/{os.environ["GITHUB_RUN_ID"]}'

    print("WATCHDOG_START " + json.dumps({"command": cmd, "state_file": str(state_path)}, ensure_ascii=False), flush=True)
    child = subprocess.Popen(cmd)
    last_publish = 0.0
    last_seen_processed = None

    while child.poll() is None:
        now = time.time()
        st = load_state(state_path)
        processed = st.get("processed")
        total = st.get("total")
        pct = st.get("percent")
        last_progress_ts = parse_time(st.get("last_progress_at"))
        stale_for = None if last_progress_ts is None else max(0, int(now - last_progress_ts))
        alive = True

        if processed != last_seen_processed:
            print("WATCHDOG_PROGRESS " + json.dumps({
                "alive": alive, "processed": processed, "total": total,
                "percent": pct, "stale_seconds": stale_for,
                "stage": st.get("stage"), "heartbeat_at": st.get("heartbeat_at"),
                "eta_seconds": st.get("eta_seconds"),
                "estimated_finish_at_utc": st.get("estimated_finish_at_utc"),
                "eta_confidence": st.get("eta_confidence")
            }, ensure_ascii=False), flush=True)
            last_seen_processed = processed

        if now - last_publish >= args.publish_seconds:
            if processed is None or total is None:
                desc = "alive; waiting for first progress update"
            else:
                stale_txt = "unknown" if stale_for is None else str(stale_for)
                eta = st.get("eta_seconds")
                finish = st.get("estimated_finish_at_utc")
                conf = st.get("eta_confidence")
                eta_txt = "ETA=unknown"
                if isinstance(eta, (int, float)):
                    eta_min = eta / 60.0
                    eta_txt = f"ETA={eta_min:.1f}m"
                if finish:
                    eta_txt += f" finish={finish}"
                if conf:
                    eta_txt += f" conf={conf}"
                desc = f"alive {processed}/{total} ({pct}%), no-progress={stale_txt}s; {eta_txt}"
            publish_status("pending", desc, args.context, target_url)
            last_publish = now

        if stale_for is not None and stale_for >= args.stale_seconds:
            print("WATCHDOG_STALE " + json.dumps({
                "processed": processed, "total": total, "percent": pct,
                "stale_seconds": stale_for, "pid": child.pid
            }), flush=True)
            publish_status(
                "pending",
                f"STALE: alive but no progress {stale_for}s; {processed}/{total} ({pct}%)",
                args.context, target_url
            )
            if args.kill_on_stale:
                child.send_signal(signal.SIGTERM)
                break

        time.sleep(args.poll_seconds)

    rc = child.wait()
    st = load_state(state_path)
    processed, total, pct = st.get("processed"), st.get("total"), st.get("percent")
    if rc == 0:
        publish_status("success", f"completed {processed}/{total} ({pct}%)", args.context, target_url)
    else:
        publish_status("failure", f"failed rc={rc}; last {processed}/{total} ({pct}%)", args.context, target_url)
    print("WATCHDOG_END " + json.dumps({"returncode": rc, "state": st}, ensure_ascii=False), flush=True)
    raise SystemExit(rc)

if __name__ == "__main__":
    main()
