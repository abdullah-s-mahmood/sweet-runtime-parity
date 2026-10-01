#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "ACAD_PASS_PROGRESS_WATCHDOG_V2"


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


def load_state(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def validated_processed(st: dict):
    value = st.get("processed")
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
    return None


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
        print(
            f"WATCHDOG_STATUS_PUBLISH_FAILED {type(e).__name__}: {e}",
            flush=True,
        )
        return False


def terminate_process_group(child: subprocess.Popen, grace_seconds: float):
    result = {
        "sigterm_sent": False,
        "sigkill_sent": False,
        "term_grace_seconds": grace_seconds,
        "termination_error": None,
    }
    try:
        pgid = os.getpgid(child.pid)
    except Exception as exc:
        pgid = None
        result["termination_error"] = (
            f"GETPGID:{type(exc).__name__}:{exc}"
        )

    try:
        if pgid is not None:
            os.killpg(pgid, signal.SIGTERM)
        else:
            child.terminate()
        result["sigterm_sent"] = True
    except ProcessLookupError:
        return result
    except Exception as exc:
        result["termination_error"] = (
            f"SIGTERM:{type(exc).__name__}:{exc}"
        )

    deadline = time.monotonic() + grace_seconds
    while child.poll() is None and time.monotonic() < deadline:
        time.sleep(min(0.1, max(0.0, deadline - time.monotonic())))

    if child.poll() is None:
        try:
            if pgid is not None:
                os.killpg(pgid, signal.SIGKILL)
            else:
                child.kill()
            result["sigkill_sent"] = True
        except ProcessLookupError:
            pass
        except Exception as exc:
            result["termination_error"] = (
                f"SIGKILL:{type(exc).__name__}:{exc}"
            )

    # Never wait indefinitely after termination.
    try:
        child.wait(timeout=max(5.0, grace_seconds))
    except subprocess.TimeoutExpired:
        result["termination_error"] = (
            (result["termination_error"] + ";")
            if result["termination_error"] else ""
        ) + "PROCESS_SURVIVED_SIGKILL_TIMEOUT"
    return result


def write_watchdog_state(
    path: Path,
    *,
    child_pid: int,
    status: str,
    launch_utc: str,
    liveness_utc: str,
    initial_processed,
    observed_processed,
    last_actual_progress_utc: str,
    actual_progress_age_seconds: float,
    stale_seconds: float,
    termination: dict | None = None,
    message: str | None = None,
):
    atomic_write_json(
        path,
        {
            "schema": SCHEMA,
            "status": status,
            "child_pid": child_pid,
            "launch_at": launch_utc,
            "liveness_heartbeat_at": liveness_utc,
            "initial_processed": initial_processed,
            "observed_processed": observed_processed,
            "last_actual_progress_at": last_actual_progress_utc,
            "actual_progress_age_seconds": round(
                actual_progress_age_seconds, 3
            ),
            "stale_seconds": stale_seconds,
            "termination": termination,
            "message": message,
        },
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-file", required=True)
    ap.add_argument("--watchdog-state-file")
    ap.add_argument("--context", required=True)
    ap.add_argument("--poll-seconds", type=float, default=20.0)
    ap.add_argument("--publish-seconds", type=float, default=60.0)
    ap.add_argument("--stale-seconds", type=float, default=600.0)
    ap.add_argument("--term-grace-seconds", type=float, default=30.0)
    ap.add_argument("--kill-on-stale", action="store_true")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    if not args.command:
        raise SystemExit("No child command supplied")
    if args.poll_seconds <= 0:
        raise SystemExit("poll-seconds must be >0")
    if args.stale_seconds <= 0:
        raise SystemExit("stale-seconds must be >0")
    if args.term_grace_seconds < 0:
        raise SystemExit("term-grace-seconds must be >=0")

    cmd = (
        args.command[1:]
        if args.command and args.command[0] == "--"
        else args.command
    )
    state_path = Path(args.state_file)
    watchdog_path = (
        Path(args.watchdog_state_file)
        if args.watchdog_state_file
        else Path(str(state_path) + ".watchdog-v2.json")
    )

    target_url = None
    if (
        os.environ.get("GITHUB_SERVER_URL")
        and os.environ.get("GITHUB_REPOSITORY")
        and os.environ.get("GITHUB_RUN_ID")
    ):
        target_url = (
            f'{os.environ["GITHUB_SERVER_URL"]}/'
            f'{os.environ["GITHUB_REPOSITORY"]}/actions/runs/'
            f'{os.environ["GITHUB_RUN_ID"]}'
        )

    initial_state = load_state(state_path)
    initial_processed = validated_processed(initial_state)
    if initial_processed is None:
        initial_processed = 0

    launch_mono = time.monotonic()
    last_actual_progress_mono = launch_mono
    launch_utc = utc_now()
    last_actual_progress_utc = launch_utc
    last_observed_processed = initial_processed
    last_publish = 0.0

    print(
        "WATCHDOG_V2_START "
        + json.dumps(
            {
                "command": cmd,
                "state_file": str(state_path),
                "watchdog_state_file": str(watchdog_path),
                "initial_processed": initial_processed,
                "stale_seconds": args.stale_seconds,
                "term_grace_seconds": args.term_grace_seconds,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    # A new session gives the child a distinct process group so descendants
    # can be terminated together on stale execution.
    child = subprocess.Popen(cmd, start_new_session=True)
    stale_triggered = False
    termination = None

    while child.poll() is None:
        now_mono = time.monotonic()
        now_utc = utc_now()
        st = load_state(state_path)
        processed = validated_processed(st)

        if processed is not None:
            if processed < last_observed_processed:
                message = (
                    f"PROGRESS_REGRESSION:{processed}<"
                    f"{last_observed_processed}"
                )
                print("WATCHDOG_V2_INVALID_PROGRESS " + message, flush=True)
                termination = terminate_process_group(
                    child, args.term_grace_seconds
                )
                write_watchdog_state(
                    watchdog_path,
                    child_pid=child.pid,
                    status="INVALID_PROGRESS_TERMINATED",
                    launch_utc=launch_utc,
                    liveness_utc=now_utc,
                    initial_processed=initial_processed,
                    observed_processed=processed,
                    last_actual_progress_utc=last_actual_progress_utc,
                    actual_progress_age_seconds=(
                        now_mono - last_actual_progress_mono
                    ),
                    stale_seconds=args.stale_seconds,
                    termination=termination,
                    message=message,
                )
                publish_status(
                    "failure", message, args.context, target_url
                )
                raise SystemExit(125)

            if processed > last_observed_processed:
                last_observed_processed = processed
                last_actual_progress_mono = now_mono
                last_actual_progress_utc = now_utc
                print(
                    "WATCHDOG_V2_PROGRESS "
                    + json.dumps(
                        {
                            "processed": processed,
                            "total": st.get("total"),
                            "percent": st.get("percent"),
                            "stage": st.get("stage"),
                            "child_heartbeat_at": st.get("heartbeat_at"),
                            "last_actual_progress_at": (
                                last_actual_progress_utc
                            ),
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

        progress_age = now_mono - last_actual_progress_mono

        # Independent liveness heartbeat. This intentionally does NOT reset
        # last_actual_progress_mono.
        write_watchdog_state(
            watchdog_path,
            child_pid=child.pid,
            status="RUNNING",
            launch_utc=launch_utc,
            liveness_utc=now_utc,
            initial_processed=initial_processed,
            observed_processed=last_observed_processed,
            last_actual_progress_utc=last_actual_progress_utc,
            actual_progress_age_seconds=progress_age,
            stale_seconds=args.stale_seconds,
            message="child alive; liveness is independent of progress",
        )

        if now_mono - last_publish >= args.publish_seconds:
            total = st.get("total")
            pct = st.get("percent")
            desc = (
                f"alive; progress={last_observed_processed}/"
                f"{total}; no-actual-progress={int(progress_age)}s"
            )
            if pct is not None:
                desc += f"; pct={pct}%"
            publish_status(
                "pending", desc, args.context, target_url
            )
            last_publish = now_mono

        if progress_age >= args.stale_seconds:
            stale_triggered = True
            print(
                "WATCHDOG_V2_STALE "
                + json.dumps(
                    {
                        "processed": last_observed_processed,
                        "actual_progress_age_seconds": round(
                            progress_age, 3
                        ),
                        "pid": child.pid,
                    }
                ),
                flush=True,
            )
            publish_status(
                "pending",
                (
                    f"STALE: no actual progress "
                    f"{int(progress_age)}s; "
                    f"processed={last_observed_processed}"
                ),
                args.context,
                target_url,
            )
            if args.kill_on_stale:
                termination = terminate_process_group(
                    child, args.term_grace_seconds
                )
                write_watchdog_state(
                    watchdog_path,
                    child_pid=child.pid,
                    status="STALE_TERMINATED",
                    launch_utc=launch_utc,
                    liveness_utc=utc_now(),
                    initial_processed=initial_processed,
                    observed_processed=last_observed_processed,
                    last_actual_progress_utc=last_actual_progress_utc,
                    actual_progress_age_seconds=(
                        time.monotonic() - last_actual_progress_mono
                    ),
                    stale_seconds=args.stale_seconds,
                    termination=termination,
                    message=(
                        "stale actual-progress timer triggered "
                        "process-group termination"
                    ),
                )
                print(
                    "WATCHDOG_V2_END "
                    + json.dumps(
                        {
                            "returncode": child.poll(),
                            "reason": "STALE_TERMINATED",
                            "termination": termination,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                raise SystemExit(124)
            break

        time.sleep(args.poll_seconds)

    if stale_triggered and not args.kill_on_stale:
        rc = child.wait()
    else:
        rc = child.poll()
        if rc is None:
            # Defensive bounded wait only. Normal child completion reaches
            # this branch with a concrete return code.
            try:
                rc = child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                termination = terminate_process_group(
                    child, args.term_grace_seconds
                )
                rc = child.poll()
                if rc is None:
                    rc = 126

    final_state = load_state(state_path)
    processed = validated_processed(final_state)
    total = final_state.get("total")
    pct = final_state.get("percent")
    status = "CHILD_COMPLETED" if rc == 0 else "CHILD_FAILED"
    write_watchdog_state(
        watchdog_path,
        child_pid=child.pid,
        status=status,
        launch_utc=launch_utc,
        liveness_utc=utc_now(),
        initial_processed=initial_processed,
        observed_processed=(
            last_observed_processed if processed is None else processed
        ),
        last_actual_progress_utc=last_actual_progress_utc,
        actual_progress_age_seconds=(
            time.monotonic() - last_actual_progress_mono
        ),
        stale_seconds=args.stale_seconds,
        termination=termination,
        message=f"child returncode={rc}",
    )

    if rc == 0:
        publish_status(
            "success",
            f"child completed; progress={processed}/{total} ({pct}%)",
            args.context,
            target_url,
        )
    else:
        publish_status(
            "failure",
            f"child failed rc={rc}; progress={processed}/{total} ({pct}%)",
            args.context,
            target_url,
        )
    print(
        "WATCHDOG_V2_END "
        + json.dumps(
            {
                "returncode": rc,
                "state": final_state,
                "watchdog_state": load_state(watchdog_path),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    raise SystemExit(int(rc))


if __name__ == "__main__":
    main()
