#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WATCHDOG = ROOT / "run_with_progress_watchdog_v2.py"


def write(path: Path, text: str):
    path.write_text(textwrap.dedent(text), encoding="utf-8")


def run_watchdog(tmp: Path, child: Path, *, stale=2.0, grace=0.5):
    state = tmp / "progress.json"
    wdstate = tmp / "watchdog.json"
    cmd = [
        sys.executable,
        str(WATCHDOG),
        "--state-file", str(state),
        "--watchdog-state-file", str(wdstate),
        "--context", "watchdog-v2-synthetic",
        "--poll-seconds", "0.1",
        "--publish-seconds", "999",
        "--stale-seconds", str(stale),
        "--term-grace-seconds", str(grace),
        "--kill-on-stale",
        "--",
        sys.executable, str(child), str(state),
    ]
    p = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        timeout=20,
        env={k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"},
    )
    wd = json.loads(wdstate.read_text(encoding="utf-8"))
    st = (
        json.loads(state.read_text(encoding="utf-8"))
        if state.exists() else {}
    )
    return p, st, wd


def case_normal_completion(tmp: Path):
    child = tmp / "normal.py"
    write(child, r'''
        import json, sys, time
        from pathlib import Path
        p=Path(sys.argv[1])
        for i in range(3):
            p.write_text(json.dumps({
                "processed": i+1, "total": 3,
                "percent": (i+1)*100/3,
                "heartbeat_at": "synthetic"
            }), encoding="utf-8")
            time.sleep(0.15)
    ''')
    p, st, wd = run_watchdog(tmp, child)
    assert p.returncode == 0, p.stderr + p.stdout
    assert st["processed"] == 3
    assert wd["status"] == "CHILD_COMPLETED"


def case_progress_resets_stale(tmp: Path):
    child = tmp / "progress.py"
    write(child, r'''
        import json, sys, time
        from pathlib import Path
        p=Path(sys.argv[1])
        for i in range(4):
            p.write_text(json.dumps({
                "processed": i+1, "total": 4,
                "percent": (i+1)*25,
                "heartbeat_at": str(time.time())
            }), encoding="utf-8")
            time.sleep(0.6)
    ''')
    p, st, wd = run_watchdog(tmp, child, stale=1.0)
    assert p.returncode == 0, p.stderr + p.stdout
    assert st["processed"] == 4
    assert wd["status"] == "CHILD_COMPLETED"


def case_heartbeat_only_goes_stale(tmp: Path):
    child = tmp / "heartbeat_only.py"
    write(child, r'''
        import json, sys, time
        from pathlib import Path
        p=Path(sys.argv[1])
        start=time.time()
        while time.time()-start < 10:
            p.write_text(json.dumps({
                "processed": 0, "total": 10,
                "percent": 0,
                "heartbeat_at": str(time.time())
            }), encoding="utf-8")
            time.sleep(0.1)
    ''')
    p, st, wd = run_watchdog(tmp, child, stale=1.0)
    assert p.returncode == 124, p.stderr + p.stdout
    assert wd["status"] == "STALE_TERMINATED"
    assert wd["observed_processed"] == 0
    assert wd["termination"]["sigterm_sent"] is True


def case_sigterm_ignored_gets_sigkill(tmp: Path):
    child = tmp / "ignore_term.py"
    write(child, r'''
        import json, signal, sys, time
        from pathlib import Path
        p=Path(sys.argv[1])
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        p.write_text(json.dumps({
            "processed": 0, "total": 10,
            "percent": 0,
            "heartbeat_at": str(time.time())
        }), encoding="utf-8")
        while True:
            time.sleep(0.1)
    ''')
    p, st, wd = run_watchdog(
        tmp, child, stale=0.8, grace=0.3
    )
    assert p.returncode == 124, p.stderr + p.stdout
    assert wd["status"] == "STALE_TERMINATED"
    assert wd["termination"]["sigterm_sent"] is True
    assert wd["termination"]["sigkill_sent"] is True


def main():
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        cases = [
            ("NORMAL_COMPLETION", case_normal_completion),
            ("PROGRESS_RESETS_STALE", case_progress_resets_stale),
            ("HEARTBEAT_ONLY_STALE", case_heartbeat_only_goes_stale),
            ("SIGTERM_IGNORED_SIGKILL", case_sigterm_ignored_gets_sigkill),
        ]
        passed = []
        for name, fn in cases:
            td = base / name
            td.mkdir()
            fn(td)
            passed.append(name)
            print(f"WATCHDOG_V2_TEST_PASS {name}", flush=True)
        print(json.dumps({
            "record_id": "MPSEF_WATCHDOG_V2_SYNTHETIC_TEST_V1",
            "status": "PASS",
            "passed": passed,
            "count": len(passed),
        }, indent=2))


if __name__ == "__main__":
    main()
