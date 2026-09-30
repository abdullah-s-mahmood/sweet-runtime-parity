#!/usr/bin/env python3
from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--m2-dir", required=True)
    args, remainder = ap.parse_known_args()

    m2dir = Path(args.m2_dir).resolve()
    sys.path.insert(0, str(m2dir.parent))

    from m2scorer import util as m2_util
    from m2scorer import levenshtein as m2_levenshtein

    # The legacy edit_creator.py uses old-style absolute imports while
    # levenshtein.py uses package-relative imports. Supply aliases without
    # modifying the frozen upstream source.
    sys.modules["util"] = m2_util
    sys.modules["levenshtein"] = m2_levenshtein

    sys.argv = ["edit_creator.py"] + remainder
    runpy.run_module("m2scorer.edit_creator", run_name="__main__")


if __name__ == "__main__":
    main()
